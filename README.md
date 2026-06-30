# AttentionDep

## LLM Prompts for Semantic Graph Construction

The following prompts were used with GPT-4o-mini for constructing the Mental Health Knowledge Graph (MHKG).

### Triplet Extraction

```
Your task is to transform the given text into a mental health related 
semantic graph in the form of a list of triples. The triples must be 
in the form of [Entity1, Relationship, Entity2]. In your answer, please 
strictly only include the triples and do not include any explanation or 
apologies. Keep the entities and relations as simple and short as 
possible, and do not make them long, if it is not necessary.

Here are some examples:
{few_shot_examples}

Now please extract triplets from the following text.
Text: {input_text}
```

### Triplet Validation

```
You are given a knowledge triplet in the form [subject, relation, object].
Determine if this triplet expresses a valid and meaningful relationship 
in the context of mental health.

A valid relation is one that expresses a clear, interpretable, and 
contextually appropriate connection—such as causal, descriptive, 
indicative, or therapeutic—between two mental health-relevant concepts.

Evaluate the triplet based on:
- The subject and object must both be specific, meaningful, and clearly 
  related to mental health (e.g., symptoms, disorders, emotions, 
  behaviors, treatments, or psychological mechanisms). Avoid vague, 
  overly broad, or overly technical terms unless they directly 
  contribute to mental health understanding.
- The relation must express a plausible and interpretable connection 
  within the mental health domain.

Return only: yes or no.

Example (invalid due to vague object):
["models", "explain", "link between altered brain function and schizophrenia"] → no
```




## Core Mental Health Topics

The following 30 core Wikipedia topics form the backbone of the mental health context corpus used to construct the MHKG.

| # | Topic |
|---|-------|
| 1 | Mental health |
| 2 | Mental disorder |
| 3 | Psychology |
| 4 | Major depressive disorder |
| 5 | Depression (mood) |
| 6 | Bipolar disorder |
| 7 | Schizophrenia |
| 8 | Anxiety |
| 9 | Anxiety disorder |
| 10 | Personality disorder |
| 11 | DSM-5 |
| 12 | Diagnostic and Statistical Manual of Mental Disorders |
| 13 | Classification of mental disorders |
| 14 | Causes of mental disorders |
| 15 | Antidepressant |
| 16 | Psychotherapy |
| 17 | Cognitive behavioral therapy |
| 18 | Psychosis |
| 19 | Post-traumatic stress disorder |
| 20 | Eating disorder |
| 21 | Dysthymia |
| 22 | Panic attack |
| 23 | Suicide |
| 24 | Social psychology |
| 25 | Personality |
| 26 | Generalized anxiety disorder |
| 27 | Borderline personality disorder |
| 28 | Stress |
| 29 | Mood swing |
| 30 | Cognitive psychology |


::: table*
  ------------------------------------ ------------------------------ --------------------------------- -------------------------------------------------------
  Mental health                        Mental disorder                Psychology                        Major depressive disorder
  Depression (mood)                    Bipolar disorder               Schizophrenia                     Anxiety
  Anxiety disorder                     Personality disorder           DSM-5                             Diagnostic and Statistical Manual of Mental Disorders
  Classification of mental disorders   Causes of mental disorders     Antidepressant                    Psychotherapy
  Cognitive behavioral therapy         Psychosis                      Post-traumatic stress disorder    Eating disorder
  Dysthymia                            Panic attack                   Suicide                           Social psychology
  Personality                          Generalized anxiety disorder   Borderline personality disorder   Stress
  Mood swing                           Cognitive psychology                                             
  ------------------------------------ ------------------------------ --------------------------------- -------------------------------------------------------
:::
