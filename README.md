# Supplementary material

Data and code for "From Architecture to Output: Testing Component-Level Accounts of Hallucination in Language Models".

| Folder | Contents | Paper section |
|---|---|---|
| `study1_architecture/` | Pythia vs. Mamba at matched data and scale: free recall (1a), context conflict on 14 models (1b) and the 1b pilot | Section 4 |
| `study2_prefix_repair/` | Prefix substitution on 111 erroneous answers from three models | Section 5 |
| `companion_study/` | Anonymised data and code of the companion study cited in Section 6 | Section 6 |
| `figures/` | Scripts that draw Figures 1-4 and the plotted values | all |

Each folder has its own README with file descriptions and the commands that reproduce the reported numbers.

Requirements: Python 3.10 or later. Install the analysis dependencies with

```
pip install -r study1_architecture/requirements.txt
pip install scipy statsmodels scikit-learn pandas
```

Data files are released under CC BY 4.0 and code under the MIT license. SimpleQA questions and gold answers are from OpenAI's SimpleQA benchmark (MIT license).
