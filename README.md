# `euPOLIS`

Scripts to analys data from from the euPOLIS project.

## Main dependencies

* _python3.13_ ([anaconda distribution](https://www.anaconda.com/products/distribution) is preferred)
* other _python_ dependencies are specified in `environment.yaml`

## Setup

1. Clone the repo: `git@github.com:MikoBie/eupolis_analysis.git`.
2. Set up the proper virtual environment.
```bash
cd heart_data
conda env create --file environment.yaml
```
3. Activate `pre-commit`.
```bash
pre-commit install
```
4. Cross fingers.

## Running

Beofre trying to produce graphs please make sure you have the data folder in
the main directory. Other than that it should be enough to run the following
(ignore the warnings it will probably print out -- I was too lazy to deal with
them).

```bash
bash plot.sh
```

