#!/user/bin/env bash

## Naive way of plotting everything.

python scripts/translate_greek.py
for f in scripts/plot_*
do
echo "Plotting $f"
python $f
done
