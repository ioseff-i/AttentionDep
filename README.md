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

## Secondary Mental Health Topics

The following 153 secondary Wikipedia topics provide expanded coverage of symptoms, causes, treatments, and related constructs, supporting fine-grained contextual representation in the MHKG.

| # | Topic |
|---|-------|
| 1 | Psychiatric hospital |
| 2 | Mental distress |
| 3 | Mental toughness |
| 4 | Mental state |
| 5 | Philosophy of mind |
| 6 | Mental chronometry |
| 7 | Mental mapping |
| 8 | Mental Health Act |
| 9 | Orientation (mental) |
| 10 | Insanity defense |
| 11 | Mental age |
| 12 | Mental disability |
| 13 | Mental therapy |
| 14 | Mini–mental state examination |
| 15 | Positive mental attitude |
| 16 | Mental health inequality |
| 17 | Insanity |
| 18 | Creativity and mental health |
| 19 | Mental Hygiene |
| 20 | Mental lexicon |
| 21 | Mental reservation |
| 22 | Mental health triage |
| 23 | Mental illness in media |
| 24 | Mental health service |
| 25 | Mental health nursing |
| 26 | Narcissistic personality disorder |
| 27 | Mental status examination |
| 28 | Menstruation and mental health |
| 29 | Mental environment |
| 30 | Mental operations |
| 31 | Abortion and mental health |
| 32 | Mental health law |
| 33 | Rethink Mental Illness |
| 34 | Postpartum depression |
| 35 | Telephone phobia |
| 36 | Anxiolytic |
| 37 | Social anxiety |
| 38 | Castration anxiety |
| 39 | Death anxiety |
| 40 | Hypochondriasis |
| 41 | Social anxiety disorder |
| 42 | Anxiety dream |
| 43 | Stimulant psychosis |
| 44 | Substance-induced psychosis |
| 45 | Postpartum psychosis |
| 46 | Tardive psychosis |
| 47 | Caffeine-induced psychosis |
| 48 | Schizoaffective disorder |
| 49 | Folie à deux |
| 50 | Unitary psychosis |
| 51 | Antipsychotic |
| 52 | Brief psychotic disorder |
| 53 | List of antidepressants |
| 54 | Antidepressant discontinuation syndrome |
| 55 | SSRI |
| 56 | TCA |
| 57 | TeCA |
| 58 | SNRI |
| 59 | Atypical antidepressant |
| 60 | Pharmacology of antidepressants |
| 61 | Antidepressants and suicide risk |
| 62 | Hydrazine (antidepressant) |
| 63 | Second-gen antidepressant |
| 64 | Trazodone |
| 65 | Countries by antidepressant use |
| 66 | Fluoxetine |
| 67 | Tachyphylaxis |
| 68 | Mirtazapine |
| 69 | Antidepressants in Japan |
| 70 | Bupropion |
| 71 | Gestalt psychology |
| 72 | Analytical psychology |
| 73 | Shadow (psychology) |
| 74 | Educational psychology |
| 75 | Evolutionary psychology |
| 76 | Positive psychology |
| 77 | Filipino psychology |
| 78 | Association (psychology) |
| 79 | Developmental psychology |
| 80 | International psychology |
| 81 | Physiological psychology |
| 82 | Manipulation (psychology) |
| 83 | Doctor of Psychology |
| 84 | Narrative psychology |
| 85 | Transpersonal psychology |
| 86 | Individual psychology |
| 87 | Psychopathology |
| 88 | Biological psychopathology |
| 89 | Developmental psychopathology |
| 90 | HiTOP |
| 91 | Child psychopathology |
| 92 | RCAP |
| 93 | Development and Psychopathology |
| 94 | Avolition |
| 95 | Diathesis–stress model |
| 96 | MMPI |
| 97 | PANSS |
| 98 | Stress (biology) |
| 99 | Stressor |
| 100 | Psychological stress |
| 101 | Stress management |
| 102 | Stress hormone |
| 103 | Chronic stress |
| 104 | Anorexia nervosa |
| 105 | Anorexia (symptom) |
| 106 | Anorexia mirabilis |
| 107 | Anorexia athletica |
| 108 | Pro-ana |
| 109 | Sexual anorexia |
| 110 | Atypical anorexia nervosa |
| 111 | History of anorexia nervosa |
| 112 | People with anorexia |
| 113 | Deaths from anorexia |
| 114 | Cachexia |
| 115 | Infection-induced anorexia |
| 116 | Bulimia nervosa |
| 117 | Appetite |
| 118 | Disorganized schizophrenia |
| 119 | Sluggish schizophrenia |
| 120 | Childhood schizophrenia |
| 121 | Risk factors of schizophrenia |
| 122 | Evolution of schizophrenia |
| 123 | Religion and schizophrenia |
| 124 | Origin of influencing machine |
| 125 | People with schizophrenia |
| 126 | Anhedonia |
| 127 | Thought disorder |
| 128 | History of schizophrenia |
| 129 | Bipolar I disorder |
| 130 | Bipolar II disorder |
| 131 | People with bipolar disorder |
| 132 | Cyclothymia |
| 133 | Mood stabilizer |
| 134 | Lamotrigine |
| 135 | Sleep in bipolar disorder |
| 136 | Mood disorder |
| 137 | Epigenetics of bipolar disorder |
| 138 | Mood (psychology) |
| 139 | Mood congruence |
| 140 | Mood tracking |
| 141 | Euphoria |
| 142 | Mood management theory |
| 143 | Psychopathy |
| 144 | Big Five traits |
| 145 | Personality psychology |
| 146 | Antisocial personality disorder |
| 147 | Dissociative identity disorder |
| 148 | Schizoid personality disorder |
| 149 | Personality change |
| 150 | Enneagram of Personality |
| 151 | OCPD |
| 152 | Avoidant personality disorder |
| 153 | Histrionic personality disorder |