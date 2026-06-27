import json
import logging
import os
import random
import re
import string
import warnings
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, train_test_split
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR, SequentialLR
from torch.utils.data import Dataset
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import GINEConv, global_add_pool, global_mean_pool
from torch_geometric.utils import add_self_loops, degree, softmax as pyg_softmax
import contractions
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import fasttext
import preprocessor as p
from bs4 import BeautifulSoup
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colorbar
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import optuna
import wandb
from optuna.integration.wandb import WeightsAndBiasesCallback
from torch_geometric.data import Batch
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
logging.getLogger('nltk').setLevel(logging.CRITICAL)
logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore", category=UserWarning)
    
    
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    

def true_metric_loss(true, no_of_classes, scale=1):
    batch_size = true.size(0)
    true = true.view(batch_size,1)
    true_labels = torch.LongTensor(true.cpu()).repeat(1, no_of_classes).float().to(device)
    class_labels = torch.arange(no_of_classes).float().to(device)
    phi = (scale * torch.abs(class_labels - true_labels))
    y = nn.Softmax(dim=1)(-phi)
    return y

def loss_function(output, labels, scale=2.0, gamma=2.0):
    targets = true_metric_loss(labels, 4, scale)
    log_probs = F.log_softmax(output, -1)
    ce_loss = - (targets * log_probs).sum(-1)
    pt = torch.exp(-ce_loss)
    focal_loss = ((1 - pt) ** gamma) * ce_loss
    return focal_loss.mean()

def gr_metrics(op, t):
    TP = (op==t).sum()
    FN = (t>op).sum()
    FP = (t<op).sum()

    GP = TP/(TP + FP)
    GR = TP/(TP + FN)

    FS = 2 * GP * GR / (GP + GR)

    OE = (t-op > 1).sum()
    OE = OE / op.shape[0]

    return GP, GR, FS


class EarlyStopping:
    def __init__(self, patience=5, verbose=False, delta=0, path='checkpoint_weighted_abl.pt'):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = float('inf')
        self.delta = delta
        self.path = path

    def __call__(self, val_loss, model):
        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            if self.verbose:
                print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}). Saving model...')
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss
        
class TextGraphDataset(Dataset):    
    def __init__(self, data_path: str, fasttext_model_path: str, max_seq_len: int):
        self.max_seq_len = max_seq_len
        try:
            self.ft_model = fasttext.load_model(fasttext_model_path)
        except:
            print("Warning: FastText model not found. Using random embeddings for demo.")
            self.ft_model = None
            
        self.embed_dim = 300
        
        with open(data_path, 'r') as f:
            self.data = json.load(f)
            
        self.entity_vocab = {}
        self.relation_vocab = {}
        self._build_vocab()
        
    def _build_vocab(self):
        entity_set = set()
        relation_set = set()
        
        for item in self.data:
            for triplet in item['triplet']:
                entity_set.add(triplet[0])
                entity_set.add(triplet[2])
                relation_set.add(triplet[1])

        self.entity_vocab = {entity: idx for idx, entity in enumerate(entity_set)}
        self.relation_vocab = {rel: idx for idx, rel in enumerate(relation_set)}
        
    def _get_embedding(self, text: str) -> np.ndarray:
        if self.ft_model is None:
            return np.random.randn(self.embed_dim)
        return self.ft_model.get_word_vector(text)
        
    def _tokenize_text(self, text: str) -> List[str]:
        return text.lower().split()[:self.max_seq_len]
        
    def _create_pyg_graph(self, triplets: List[List[str]]) -> Data:
        edge_index = [[], []]
        edge_attr = []
        
        entity_to_idx = {}
        node_features = []
        
        for triplet in triplets:
            src, rel, dst = triplet
            
            if src not in entity_to_idx:
                entity_to_idx[src] = len(entity_to_idx)
                node_features.append(self._get_embedding(src))
                
            if dst not in entity_to_idx:
                entity_to_idx[dst] = len(entity_to_idx)
                node_features.append(self._get_embedding(dst))
                
            edge_index[0].append(entity_to_idx[src])
            edge_index[1].append(entity_to_idx[dst])
            edge_attr.append(self._get_embedding(rel))

            
        if not edge_index[0]:
            x = torch.randn(1, self.embed_dim)
            edge_index = torch.tensor([[], []], dtype=torch.long)
            edge_attr = torch.empty((0, self.embed_dim), dtype=torch.float32)

            return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)


        x = torch.tensor(np.array(node_features), dtype=torch.float32)
        edge_index = torch.tensor(edge_index, dtype=torch.long)
        edge_attr = torch.tensor(np.array(edge_attr), dtype=torch.float32)


        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)

        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        label_map = {'mild': 1, 'moderate': 2, 'severe': 3, 'minimum': 0}

        item = self.data[idx]
        
        tokens = self._tokenize_text(item['text'])
        text_embeddings = []
        
        for token in tokens:
            text_embeddings.append(self._get_embedding(token))
            
        while len(text_embeddings) < self.max_seq_len:
            text_embeddings.append(np.zeros(self.embed_dim))
            
        text_embeddings = text_embeddings[:self.max_seq_len]
        text_tensor = torch.tensor(np.array(text_embeddings), dtype=torch.float32)
        graph = self._create_pyg_graph(item['triplet'])
        label = torch.tensor(label_map[item['label']], dtype=torch.long)
        return {
            'text': text_tensor,
            'length': len(tokens) if len(tokens) < self.max_seq_len else self.max_seq_len,
            'graph': graph,
            'label': label

        }


class TextEncoder(nn.Module):
    def __init__(self, embed_size, hidden_size, num_layers=2, num_heads = 4, dropout=0.3):
        super(TextEncoder, self).__init__()
        
        self.lstm = nn.LSTM(
            embed_size, 
            hidden_size // 2, 
            num_layers=num_layers,
            bidirectional=True, 
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        self.norm = nn.LayerNorm(hidden_size)
        self.unigram_attention = nn.MultiheadAttention(hidden_size, num_heads, batch_first=True, dropout=dropout)
        self.conv = nn.Conv1d(
            in_channels=hidden_size,
            out_channels=hidden_size,
            kernel_size=2,
            stride=1,
            padding = 0
        )
        
       
    
    def forward(self, x, lengths):
        batch_size, max_seq_len, _ = x.shape
        device = x.device
        
        mask = torch.arange(max_seq_len, device=device).expand(batch_size, max_seq_len) >= lengths.to(device).unsqueeze(1)
        
        packed_x = pack_padded_sequence(x, lengths.cpu(), batch_first=True, enforce_sorted=False)
        lstm_out, _ = self.lstm(packed_x)
        lstm_out, _ = pad_packed_sequence(lstm_out, batch_first=True, total_length=max_seq_len)
        
        lstm_out = self.norm(lstm_out)
        
        uni_out, uni_weights = self.unigram_attention(
            lstm_out, lstm_out, lstm_out,
            key_padding_mask=mask
        )
        
        conv_out = self.conv(uni_out.permute(0, 2, 1))
        conv_out = conv_out.permute(0, 2, 1)
        conv_out = F.gelu(conv_out)
        

        return conv_out, uni_weights



class GINENet(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, edge_dim, num_layers=2, dropout=0.5):
        super(GINENet, self).__init__()
        
        self.dropout = dropout
        self.num_layers = num_layers
        self.hidden_dim = hidden_channels
        
        self.input_norm = nn.LayerNorm(in_channels)
        
        self.convs = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        
        self.convs.append(GINEConv(
            nn.Sequential(
                nn.Linear(in_channels, hidden_channels),
                nn.LayerNorm(hidden_channels),
                nn.GELU(), 
                nn.Linear(hidden_channels, hidden_channels),
            ),
            edge_dim=edge_dim
        ))
        self.batch_norms.append(nn.LayerNorm(hidden_channels))
        
        for _ in range(num_layers - 1):
            self.convs.append(GINEConv(
                nn.Sequential(
                    nn.Linear(hidden_channels, hidden_channels),
                    nn.LayerNorm(hidden_channels),
                    nn.GELU(),
                    nn.Linear(hidden_channels, hidden_channels),
                ),
                edge_dim=edge_dim
            ))
            self.batch_norms.append(nn.LayerNorm(hidden_channels))
        
        self.output_proj = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.LayerNorm(hidden_channels),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels, out_channels)
        )
        
        self.residual_proj = nn.Linear(in_channels, hidden_channels)
    
    def forward(self, bi_text_repr, graph_batch, ):

        batch_size = bi_text_repr.size(0)
        x = graph_batch.x
        edge_index = graph_batch.edge_index
        edge_attr = graph_batch.edge_attr
        batch_idx = graph_batch.batch


        x = self.input_norm(x)
        
        res = self.residual_proj(x)
        
        for i, (conv, norm) in enumerate(zip(self.convs, self.batch_norms)):
            x_new = conv(x, edge_index, edge_attr)
            x_new = norm(x_new)
            
            if i == 0:
                x_new = x_new + res
                
            x_new = F.gelu(x_new)
            x_new = F.dropout(x_new, p=self.dropout, training=self.training)
            
            x = x_new
        
        max_nodes = bi_text_repr.size(1)  
        
        graph_node_reprs = []
        for i in range(batch_size):
            mask = (batch_idx == i)
            graph_nodes = x[mask]  
            
            if graph_nodes.size(0) >= max_nodes:
                graph_nodes = graph_nodes[:max_nodes]
            else:
                padding = torch.zeros(max_nodes - graph_nodes.size(0), self.hidden_dim, 
                                    device=graph_nodes.device, dtype=graph_nodes.dtype)
                graph_nodes = torch.cat([graph_nodes, padding], dim=0)
            
            graph_node_reprs.append(graph_nodes)
        
        graph_repr = torch.stack(graph_node_reprs, dim=0) 
        
        return graph_repr



class KnowledgeAwareHierarchicalModel(nn.Module):
    def __init__(self, 
                 embed_size, 
                 hidden_dim, 
                 num_class, 
                 num_lstm_layers = 2,
                 num_heads = 4,
                 num_bi_heads = 4,
                 num_gnn_layers=2, 
                 dropout=0.3):
        super(KnowledgeAwareHierarchicalModel, self).__init__()
        
        
        self.text_encoder = TextEncoder(
            embed_size=embed_size,
            hidden_size=hidden_dim,
            num_layers = num_lstm_layers,
            num_heads = num_heads,
            dropout=dropout
            
        )

        self.graph_encoder = GINENet(
            in_channels=embed_size,
            hidden_channels=hidden_dim,
            out_channels=hidden_dim,
            edge_dim=embed_size,
            num_layers=num_gnn_layers,
            dropout=dropout
        )

        
        self.bigram_attention = nn.MultiheadAttention(hidden_dim, num_bi_heads, batch_first=True, dropout=dropout)
        self.output_proj = nn.Linear(hidden_dim, embed_size)
        self.classifier = nn.Sequential(
            nn.Linear(embed_size, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_class)
        )
        
        self.embed_size = embed_size
        self.hidden_dim = hidden_dim
        self.num_class = num_class
        self.dropout = dropout
        
        try:
            self._init_weights()
        except Exception as e:
            print(f"Error: {e}")
    
    def _init_weights(self):
        for name, param in self.named_parameters():
            if 'norm' in name and 'weight' in name:
                nn.init.ones_(param)
            elif 'norm' in name and 'bias' in name:
                nn.init.zeros_(param)
            elif 'bias' in name:
                nn.init.zeros_(param)
            elif 'weight' in name and 'lstm' in name:
                nn.init.orthogonal_(param)
            elif 'weight' in name:
                if param.dim() >= 2:
                    try:
                        nn.init.kaiming_normal_(param, nonlinearity='gelu')
                    except ValueError:
                        nn.init.xavier_uniform_(param)
                else:
                    nn.init.normal_(param, std=0.02)
                
    def forward(self, uni_grams, lens, graph_batch):
        device = uni_grams.device
        batch_size, max_seq_len, _ =  uni_grams.shape
        device = uni_grams.device
        
        main_mask = torch.arange(max_seq_len, device=device).expand(batch_size, max_seq_len) >= lens.to(device).unsqueeze(1)
        bi_text_repr, uni_attention_weights= self.text_encoder(uni_grams, lens)        
        graph_repr = self.graph_encoder(bi_text_repr, graph_batch)
        
        effective_seq_len = min(bi_text_repr.size(1), max_seq_len-1)
        adjusted_mask = main_mask[:, :effective_seq_len] if effective_seq_len < main_mask.size(1) else main_mask


        attended_features, bi_weights = self.bigram_attention(
            query=bi_text_repr[:, :effective_seq_len],    
            key=graph_repr[:, :effective_seq_len],         
            value=bi_text_repr[:, :effective_seq_len],    
            key_padding_mask=adjusted_mask
        )


        float_mask = (~adjusted_mask).float().unsqueeze(-1)
        masked_sum = torch.sum(attended_features * float_mask, dim=1)
        lengths_for_division = lens.to(device).clamp(min=1).float().unsqueeze(-1)
        global_repr = masked_sum / lengths_for_division
        global_repr = self.output_proj(global_repr)
        logits = self.classifier(global_repr)

        
        return logits, uni_attention_weights , bi_weights


class PyGDataLoader:    
    def __init__(self, dataset, batch_size=32, shuffle=False, num_workers=0, pin_memory=False):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        
        graphs = [dataset[i]['graph'] for i in range(len(dataset))]
        self.graph_loader = DataLoader(graphs, batch_size=batch_size, shuffle=shuffle)
        
        indices = list(range(len(dataset)))
        if shuffle:
            np.random.shuffle(indices)
            
        self.batched_indices = [indices[i:i+batch_size] for i in range(0, len(indices), batch_size)]
        
    def __iter__(self):
        graph_iter = iter(self.graph_loader)
        
        for batch_indices in self.batched_indices:
            try:
                graph_batch = next(graph_iter)
            except StopIteration:
                break
                
            text_batch = torch.stack([self.dataset[i]['text'] for i in batch_indices])
            label_batch = torch.stack([self.dataset[i]['label'] for i in batch_indices])
            lengths = torch.tensor([self.dataset[i]['length'] for i in batch_indices])
            
            yield {
                'text': text_batch,
                'length': lengths,
                'graph': graph_batch,
                'label': label_batch
            }
            
    def __len__(self):
        return len(self.batched_indices)
    
def collate_fn(batch):
    
    
    texts = torch.stack([item['text'] for item in batch])
    graphs = [item['graph'] for item in batch]
    labels = torch.stack([item['label'] for item in batch])
    lengths = torch.tensor([item['length'] for item in batch])
    
    graph_batch = Batch.from_data_list(graphs)
    
    return {
        'text': texts,
        'length': lengths,
        'graph': graph_batch,
        'label': labels
    }




def train_epoch(model, train_loader, optimizer, criterion, device, epoch, scale, gamma, grad_clip=1.0):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.train()
    running_loss = 0.0
    all_preds = []
    all_labels = []
    
    for batch in train_loader:
        text_batch = batch['text'].to(device)
        graph_batch = batch['graph'].to(device)
        labels = batch['label'].to(device)
        lengths = batch['length']

            
        optimizer.zero_grad()
        
        logits,_,_ = model(text_batch, lengths, graph_batch)
        
        loss = criterion(logits, labels, scale=scale, gamma=gamma)
        
        optimizer.zero_grad()
        loss.backward()
        
        if grad_clip > 0:
            nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            
        optimizer.step()
        
        
        running_loss += loss.item()
        _, preds = torch.max(logits, 1)
        
        all_preds.extend(preds.cpu().tolist())
        all_labels.extend(labels.cpu().tolist())

    
    avg_loss = running_loss / len(train_loader)
    return avg_loss


def evaluate(model, data_loader, criterion, device,scale, gamma, phase='val'):    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model.eval()
    running_loss = 0.0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for batch in data_loader:
            text_batch = batch['text'].to(device)
            graph_batch = batch['graph'].to(device)
            labels = batch['label'].to(device)
            lengths = batch['length']
            
            logits,_,_ = model(text_batch, lengths, graph_batch)
        
            loss = criterion(logits, labels, scale=scale, gamma=gamma)
            
            running_loss += loss.item()
            _, preds = torch.max(F.softmax(logits, dim=-1), 1)
            
            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(labels.cpu().tolist())
    
    avg_loss = running_loss / len(data_loader)
    gp, fr, fs = gr_metrics(np.array(all_preds), np.array(all_labels))
    return avg_loss, gp, fr, fs

def cross_validate(params, n_splits=5, save_global_best=True):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print(f"Loading data from {params['data_path']}...")
    dataset = TextGraphDataset(
        data_path=params["data_path"], 
        fasttext_model_path="crawl-300d-2M-subword.bin",  
        max_seq_len= params['max_seq_len']
    )
    print(f"Loaded {len(dataset)} samples")
    
    labels = [data['label'].item() for data in dataset]
    
    
    precisions, recalls, f_scores = [], [], []
    best_f1_score = 0.0
    best_global_model = None
    
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    fold_iterator = enumerate(skf.split(np.arange(len(dataset)), labels))
    
    train_dataset,test_dataset,train_labels,test_labels = train_test_split(
        dataset,
        labels,
        test_size=0.2,
        random_state=SEED,
        stratify=labels
    )
    
    test_loader = PyGDataLoader(
        test_dataset, 
        batch_size=params['batch_size'], 
        shuffle=False,
        pin_memory=torch.cuda.is_available(),
        num_workers=4 if torch.cuda.is_available() else 0
    )


    fold_idx = 0
    for train_indices, val_indices in skf.split(np.arange(len(train_dataset)), train_labels):
        print(f"\nFold {fold_idx+1}/{n_splits}")
        train_dataset = [train_dataset[i] for i in train_indices]
        val_dataset = [train_dataset[i] for i in val_indices]
        fold_idx += 1
    
        
        print(f"Train: {len(train_dataset)}, Validation: {len(val_dataset)}")
        
        use_cuda = torch.cuda.is_available()
    
        
        train_loader = PyGDataLoader(
            train_dataset, 
            batch_size=params['batch_size'], 
            shuffle=True,
            pin_memory=use_cuda,
            num_workers=4 if use_cuda else 0
        )
        
        val_loader = PyGDataLoader(
            val_dataset, 
            batch_size=params['batch_size'], 
            shuffle=False,
            pin_memory=use_cuda,
            num_workers=4 if use_cuda else 0
        )
        
        device = torch.device('cuda' if use_cuda else 'cpu')
        print(f"Using device: {device}")
        
        model = KnowledgeAwareHierarchicalModel(embed_size = params['embedding_dim'], 
                                                hidden_dim = params['hidden_dim'], 
                                                num_class = params['num_classes'], 
                                                num_lstm_layers = params['lstm_layers'], 
                                                num_heads = params['heads'], 
                                                num_bi_heads = params['bi_heads'],
                                                num_gnn_layers=params['gnn_layers'], 
                                                dropout=params['dropout']).to(device)
        
        
        criterion = loss_function
        optimizer = torch.optim.Adam(
            model.parameters(), 
            lr=params['learning_rate'],
            weight_decay=1e-5
        )
        


        warmup_epochs = max(1, params['epochs'] // 20)

        scheduler = SequentialLR(
            optimizer,
            schedulers=[
                LinearLR(optimizer, start_factor=0.1, total_iters=warmup_epochs),
                CosineAnnealingLR(optimizer, T_max=params['epochs']-warmup_epochs, eta_min=params['learning_rate']*params['scheduler_factor'])
            ],
            milestones=[warmup_epochs]
        )


        best_model_path = f'best_model_fold_{fold_idx}_weighted_abl.pt'
        early_stopping = EarlyStopping(
            patience=params['patience'], 
            verbose=True, 
            path=best_model_path
        )
        
        for epoch in range(params['epochs']):
            train_loss = train_epoch(
                model, train_loader, optimizer, criterion, device, epoch, 
                scale=params['scale'], gamma=params['gamma']
            )
            
            val_loss, _, _, _ = evaluate(
                model, val_loader, criterion, device, scale=params['scale'], gamma=params['gamma'], phase='val'
            )
            
            print(f'Epoch {epoch+1}/{params["epochs"]}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
            
            scheduler.step()
            
            early_stopping(val_loss, model)
            if early_stopping.early_stop:
                print(f'Early stopping at epoch {epoch+1}')
                break
        
        model.load_state_dict(torch.load(best_model_path))
        
        _, precision, recall, fscore = evaluate(
            model, test_loader, criterion, device,scale=params['scale'], gamma=params['gamma'], phase='test'
        )
        
        precisions.append(precision)
        recalls.append(recall)
        f_scores.append(fscore)
        
        if fscore > best_f1_score:
            best_f1_score = fscore
            if save_global_best:
                torch.save(model.state_dict(), 'best_global_model_weighted_exp_test.pt')
                best_global_model = model
                print(f"New best global model saved with F1: {fscore:.4f}")
        
        try:
            os.remove(best_model_path)
        except:
            pass
    
    print("\nCross-validation Results:")
    print(f'F Scores: {f_scores}')
    print(f'Precisions: {precisions}')
    print(f'Recalls: {recalls}')
    
    print(f'MEDIAN F: {np.median(f_scores):.4f}, PRECISION: {np.median(precisions):.4f}, RECALL: {np.median(recalls):.4f}')
    print(f'MEAN F: {np.mean(f_scores):.4f}, PRECISION: {np.mean(precisions):.4f}, RECALL: {np.mean(recalls):.4f}')
    print(f'STD F: {np.std(f_scores):.4f}, PRECISION: {np.std(precisions):.4f}, RECALL: {np.std(recalls):.4f}')

    return np.mean(f_scores)


    
    
    
if __name__ == "__main__":

    params = { 
        "data_path": "retrieved_d4_depression_data.json",
        "embedding_dim": 300,
        "hidden_dim": 256, 
        "num_classes": 4,
        "batch_size": 128, 
        "learning_rate": 5.193535501133039e-05, 
        "dropout":  0.2847875260866256, 
        "patience": 22, 
        "scale": 3.432501194578878,
        "gamma": 1.0980225566576172, 
        "lstm_layers": 1, 
        "gnn_layers": 2, 
        "heads": 4, 
        "bi_heads": 2,
        "epochs": 200,
        'scheduler_factor':0.2160334737842532,
        'max_seq_len': 256
    }
    
    results = cross_validate(params, n_splits=5)
    
        