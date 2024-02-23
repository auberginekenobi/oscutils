#!/bin/bash

# bioconda recommended setup
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict

conda create -n py3
conda activate py3
conda install -y python
conda install -y numpy pandas matplotlib-base scikit-learn seaborn statsmodels pip
conda install -y -c conda-forge jupyterlab
