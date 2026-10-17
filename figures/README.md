# Figures

`make_figures_extra.py` rebuilds Figures 1, 3 and 4 from the released data and writes every plotted value to `figure_values.txt`:

```
cd figures
mkdir -p figures
python make_figures_extra.py ../study1_architecture/study1b/results/scored_items.csv ../study2_prefix_repair/data/annotator_A.csv
```

`make_figure_main.py` draws Figure 2 from values reported in Tables 2-4. Both scripts use the Linux Biolinum font if installed; edit the `FD` path or remove the font lines to use the default font.
