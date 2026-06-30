# AttentionDep

## LLM Prompts for Semantic Graph Construction

The following prompts were used with GPT-4o-mini for constructing the Mental Health Knowledge Graph (MHKG).

### Triplet Extraction

```
Your task is to transform the given text into a mental health related semantic graph in the form of
a list of triples. The triples must be in the form of [Entity1, Relationship, Entity2]. In your answer,
please strictly only include the triples and do not include any explanation or apologies.
Keep the entities and relations as simple and short as possible,
and do not make them long, if it is not necessary.

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

The following 30 core Wikipedia topics.

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

The following 153 secondary, extended set of mental health Wikipedia topics provide symptoms, causes, treatments, and related constructs.

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


## Normalised Relation Types

The following 177 normalised and human-validated relation types are.

| # | Relation Type |
|---|---------------|
| 1 | source_or_authority |
| 2 | diagnostic_indication |
| 3 | clinical_recommendation |
| 4 | categorization |
| 5 | context_dependent |
| 6 | background_factors |
| 7 | instance_of |
| 8 | opposite_of |
| 9 | aims_to_help |
| 10 | family_history |
| 11 | helps_manage |
| 12 | unavailable |
| 13 | negation |
| 14 | engagement |
| 15 | potential_cause |
| 16 | used_in |
| 17 | helps_with_process |
| 18 | occurs_in_context |
| 19 | similar_to |
| 20 | prevalence |
| 21 | has_condition |
| 22 | structural_attribute |
| 23 | overlaps_with |
| 24 | helps_develop |
| 25 | comparative_benefit |
| 26 | targets_patients |
| 27 | aims_to_improve |
| 28 | treatment_practice |
| 29 | treatment_line |
| 30 | exclusion |
| 31 | remission_timeline |
| 32 | resolves_with |
| 33 | symptom similarity |
| 34 | part_of |
| 35 | potential_effectiveness |
| 36 | frequently_co_occurs |
| 37 | causes |
| 38 | illustrates |
| 39 | treatment_preference |
| 40 | side_effect |
| 41 | examplesinclude |
| 42 | onset_age |
| 43 | has_heritability |
| 44 | addresses |
| 45 | treatment_magnitude |
| 46 | temporal_property |
| 47 | defines |
| 48 | complicated_by |
| 49 | measured_by |
| 50 | comparative_magnitude |
| 51 | created_by |
| 52 | limitation |
| 53 | definedas |
| 54 | alternative_to |
| 55 | likelihood |
| 56 | enhanced_effectiveness |
| 57 | not only |
| 58 | diagnosis_related |
| 59 | helps_prevent |
| 60 | communication |
| 61 | adverse_effect_or_outcome |
| 62 | has_severity |
| 63 | inhibits |
| 64 | modifies |
| 65 | modulates |
| 66 | response_rate |
| 67 | frequency_pattern |
| 68 | aims_to_resolve |
| 69 | usage |
| 70 | field_of_work |
| 71 | requires |
| 72 | susceptibility |
| 73 | helps_distinguish |
| 74 | onset |
| 75 | varies |
| 76 | requires_exposure |
| 77 | assists_with |
| 78 | recovery_rate |
| 79 | treatment_access |
| 80 | prescriptive_authority |
| 81 | found_in |
| 82 | has_goal |
| 83 | classification |
| 84 | has_model |
| 85 | redefined_as |
| 86 | helps_identify |
| 87 | shares_mechanism_with |
| 88 | reduced_by |
| 89 | helps_provide |
| 90 | has_role |
| 91 | evidence_based |
| 92 | is_reflection_of |
| 93 | historical_finding |
| 94 | compared_with |
| 95 | different_from |
| 96 | has_mechanism |
| 97 | complementary_to |
| 98 | clinical_expectation |
| 99 | theoretical_framework |
| 100 | topic_related |
| 101 | genetic_association |
| 102 | synonym |
| 103 | induces |
| 104 | has_method |
| 105 | aims_to_change |
| 106 | term_equivalence |
| 107 | potential_history |
| 108 | clinical_practice |
| 109 | indicated_for |
| 110 | belief_claim |
| 111 | helps_treat |
| 112 | occurs_after |
| 113 | affected_group |
| 114 | research_focus |
| 115 | caused_by |
| 116 | differential_diagnosis |
| 117 | educates |
| 118 | conceptual_model |
| 119 | eliminates |
| 120 | potential_harm |
| 121 | negatively_associated_with |
| 122 | explains |
| 123 | has_attribute |
| 124 | evidence_detail |
| 125 | contraindication |
| 126 | evidence_claim |
| 127 | potential_involvement |
| 128 | suggests |
| 129 | occurs_during |
| 130 | has_part |
| 131 | aims_to_reduce |
| 132 | has_characteristic |
| 133 | historical_classification |
| 134 | affects |
| 135 | developed_from |
| 136 | disrupts |
| 137 | manages |
| 138 | common_pattern |
| 139 | prevents |
| 140 | occurs_independently |
| 141 | avoidance_level |
| 142 | effective |
| 143 | combination_therapy |
| 144 | correlates_with |
| 145 | exacerbates |
| 146 | authorization |
| 147 | has_component |
| 148 | frequency |
| 149 | occurs_on_top_of |
| 150 | trained_in |
| 151 | example |
| 152 | treats |
| 153 | involved_in |
| 154 | occurs_before |
| 155 | subtype_of |
| 156 | key_factor_for |
| 157 | related_to |
| 158 | early_onset |
| 159 | has_type |
| 160 | is_a |
| 161 | needs_adaptation |
| 162 | has_diagnosis |
| 163 | not_caused_by |
| 164 | common_occurrence |
| 165 | used_for |
| 166 | cannot_occur_during |
| 167 | origin |
| 168 | follows |
| 169 | helps_change |
| 170 | represents |
| 171 | potential_benefit |
| 172 | avoids |
| 173 | current_status |
| 174 | outcomes |
| 175 | untreated_outcome |
| 176 | shows |
| 177 | delivery_method |
