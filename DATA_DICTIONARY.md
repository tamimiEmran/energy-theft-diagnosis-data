# Data dictionary

## Derived benchmark

`data/explainability_dataset2.csv` has one row per evaluated or training
consumer-day scenario. `row_id` is the stable key used by the split and prediction
files. The original CSV is preserved byte for byte so its hash agrees with the
frozen manifest.

| Column | Meaning |
|---|---|
| `row_id` | Unique integer row identifier. |
| `consumer_id` | Anonymized consumer identifier; the split is grouped by this field. |
| `query_day` | Query-day label in the serialized input, e.g. `Thu 2013-05-23`. |
| `label_attack` | Ground-truth scenario label. `Benign` is unmodified; `attackieee` is called `attack13` in the paper. |
| `label_binary` | `benign` or `theft`. |
| `gen_params_factor` | Recorded attack-specific numeric parameter. Its meaning depends on the attack; it is not a common theft fraction for all classes. |
| `gen_params_interval_start`, `gen_params_interval_end` | Recorded bounds for attacks with a localized interval. |
| `input` | Serialized preceding reference week and query day supplied to the models. |
| `rationale` | Teacher-generated explanation used as a reference or training target. |
| `observed_factor` | Numeric parameter extracted from the teacher response. |
| `observed_interval_start`, `observed_interval_end` | Interval bounds extracted from the teacher response. |
| `gen_method` | `label_blind` or `rationalization`, indicating whether the teacher was given the label. |

Empty parameter cells represent unavailable or inapplicable values. They must not
be replaced with zero. The `observed_*` fields are model outputs, not independent
ground truth. The input strings preserve the actual prompts rather than
reconstructing them from rounded summary values.

## Split

`data/f008_split_manifest.json` records the dataset SHA-256, consumer membership,
class counts, and experiment-specific subsets. Use `split.train_consumers` and
`split.eval_consumers` to select rows. The evaluation split contains 130 benign
and 1,520 manipulated days. A consumer belongs to only one side of the split.

## Prediction files

The Parquet files use `row_id` to join to the CSV. Common fields are `consumer_id`,
`y_true_binary`, `pred_binary`, `y_true_multiclass`, `pred_multiclass`, and
`score_manipulated`. Explanation variants also retain generated text and parsed
parameters. Held-out-family files contain their corresponding evaluation subsets;
they should not be treated as predictions for all 1,650 days.

The Gemini CSV preserves the supplied response, parsed decision, token counts,
and recorded parameters. `results/gemini/analysis.json` contains the matched
metrics and consumer-level paired comparisons. The correctness flags in the
Gemini CSV were checked against the supplied predictions and labels.
