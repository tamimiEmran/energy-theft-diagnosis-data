# Energy-theft diagnosis data

Dataset and saved model outputs for **From Detection to Diagnosis: Fine-Tuned Open-Weight LLMs for Explainable Energy-Theft Identification in Smart Grids**, by Emran Altamimi, Moaz Jemmieh, Abdulaziz Al-Ali, and Qutaibah M. Malluhi.

The benchmark combines measured consumption profiles with synthetic theft transformations. Each example contains a query day, the consumer's preceding reference week, an attack label, and a teacher-generated rationale. It supports binary detection, identification of twelve attack mechanisms, and evaluation of explanations and numerical diagnostic outputs.

| Split | Consumers | Consumer-days |
|---|---:|---:|
| Training | 259 | 6,589 |
| Evaluation | 65 | 1,650 |
| Total | 324 | 8,239 |

Consumers do not overlap between training and evaluation. The evaluation set has 130 benign and 1,520 manipulated days. These are synthetic attacks on measured consumption, not records of confirmed theft incidents.

## Files

| Path | Contents |
|---|---|
| `data/explainability_dataset2.csv` | The complete derived benchmark. |
| `data/f008_split_manifest.json` | Frozen split membership, dataset checksum, and subset definitions. |
| `results/predictions/` | 35 saved prediction files, including zero-shot and fine-tuned models, classical baselines, and experimental variants. |
| `results/metrics/` | Metrics saved with the experiments. |
| `results/gemini/` | Gemini responses, matched metrics, and paired comparisons. |
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Field definitions and join keys. |
| `file_manifest.json` | SHA-256 checksums and sizes for the release files. |

Result filenames preserve experiment identifiers to associate predictions with their metrics:

| Identifier | Experiment |
|---|---|
| `F010`-`F016` | Seven-model screening; `base` files are zero-shot evaluations. |
| `F005` | Training-set size experiments. |
| `F006` | Held-out attack-family evaluations. |
| `F008` | Explanation-supervision variants. |
| `F018` | Theft-magnitude and manipulated-window outputs. |
| `F004` | LoRA-rank sweep. |
| `B-*` | Classical benchmark predictions. |

The CSV label `attackieee` corresponds to `attack13` in the manuscript. Use `row_id` to join predictions to the dataset. Held-out-family files cover their designated subsets rather than all 1,650 evaluation days.

## Load and validate

Use Python 3.10 or later:

```sh
python -m pip install -r requirements.txt
python validate_data.py
```

The script checks file hashes, the frozen dataset checksum, consumer separation, row counts, prediction joins, and Gemini's evaluation-set alignment.

```python
import json
import pandas as pd

data = pd.read_csv("data/explainability_dataset2.csv")
with open("data/f008_split_manifest.json") as stream:
    split = json.load(stream)["split"]
train = data[data.consumer_id.isin(split["train_consumers"])]
evaluation = data[data.consumer_id.isin(split["eval_consumers"])]
```

## Source and citation

The original consumption measurements are from:

Trindade, A. (2015). *ElectricityLoadDiagrams20112014* [Dataset]. UCI Machine Learning Repository. [doi:10.24432/C58C86](https://doi.org/10.24432/C58C86).

This release adds synthetic manipulations, selected consumer-days, serialized inputs, labels, teacher rationales, and model outputs. Cite the UCI source and this derived release when using the data. GitHub's **Cite this repository** menu provides the citation in [CITATION.cff](CITATION.cff).

The data and accompanying documentation are available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE) for attribution details. The frozen release is tagged `v1.0.0`.

For questions or corrections, open an issue with the relevant filename and row identifier.
