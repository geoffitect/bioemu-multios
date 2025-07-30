#!/bin/bash

set -ex

echo "Setting up colabfold for Apple M2..."
BASE_PYTHON=$1
VENV_FOLDER=$2

${BASE_PYTHON} -m venv --without-pip ${VENV_FOLDER}

# Install ColabFold without CUDA dependencies for Apple M2
echo "Installing ColabFold with Apple Silicon compatibility..."
${BASE_PYTHON} -m uv pip install --python ${VENV_FOLDER}/bin/python 'colabfold[alphafold-minus-jax]==1.5.4'

# Install JAX for Apple M2 (CPU version)
echo "Installing JAX for Apple Silicon..."
${BASE_PYTHON} -m uv pip install --python ${VENV_FOLDER}/bin/python --force-reinstall \
    "jax[cpu]==0.4.35" \
    "numpy==1.26.4"

# Note: We skip all CUDA-specific packages as they're not needed/available on M2:
# - nvidia-cublas-cu12, nvidia-cuda-*, nvidia-cudnn-cu12, etc.

# Patch colabfold install (same patches as original)
echo "Patching colabfold installation..."
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SITE_PACKAGES_DIR=${VENV_FOLDER}/lib/python3.*/site-packages
patch ${SITE_PACKAGES_DIR}/alphafold/model/modules.py ${SCRIPT_DIR}/modules.patch
patch ${SITE_PACKAGES_DIR}/colabfold/batch.py ${SCRIPT_DIR}/batch.patch

touch ${VENV_FOLDER}/.COLABFOLD_PATCHED_M2
echo "Colabfold installation complete for Apple M2!"