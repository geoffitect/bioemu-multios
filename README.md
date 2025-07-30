
<h1>
<p align="center">
    <img src="assets/emu_apple.png" alt="BioEmu logo wearing Apple Computer sunglasses" width="300"/>
</p>
</h1>

[![DOI:10.1101/2024.12.05.626885](https://zenodo.org/badge/DOI/10.1101/2024.12.05.626885.svg)](https://doi.org/10.1101/2024.12.05.626885)
[![Requires Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://python.org/downloads)


# Biomolecular Emulator (BioEmu) Multi-OS Edition

Biomolecular Emulator (BioEmu for short) is a model that samples from the approximated equilibrium distribution of structures for a protein monomer, given its amino acid sequence. It can now run on Linux + CUDA or Apple Silicon (MPS).

For more information see our [paper](assets/bioemu_paper.pdf), [citation below](#citation).

This repository contains inference code and model weights.

## Table of Contents
- [Installation](#installation)
- [Sampling structures](#sampling-structures)
- [Get in touch](#get-in-touch)
- [Citation](#citation)

## Installation
bioemu-multios is provided as a Linux, MacOS pip-installable package:

```bash
pip install setup.py
```

### MacOS
This version of BioEmu is designed for full compatibility with Apple Silicon - MPS. No CUDA device is needed.

> [!NOTE]
> The first time `bioemu` is used to sample structures, it will also setup [Colabfold](https://github.com/sokrypton/ColabFold) on a separate virtual environment for MSA and embedding generation. The dependencies for this environment will automatically be selected based on your OS. By default this setup uses the `~/.bioemu_colabfold` directory, but if you wish to have this changed please manually set the `BIOEMU_COLABFOLD_DIR` environment variable accordingly before sampling for the first time.


## Sampling structures
You can sample structures for a given protein sequence using the `sample` module. To run a tiny test using the default model parameters and denoising settings:
```
python -m bioemu.sample --sequence GYDPETGTWG --num_samples 10 --output_dir ~/test-chignolin
```

Alternatively, you can use the Python API:

```python
from bioemu.sample import main as sample
sample(sequence='GYDPETGTWG', num_samples=10, output_dir='~/test_chignolin')
```

The model parameters will be automatically downloaded from [huggingface](https://huggingface.co/microsoft/bioemu). A path to a single-sequence FASTA file can also be passed to the `sequence` argument.

Sampling times will depend on sequence length and available infrastructure. The following table gives times for collecting 1000 samples measured on an A100 GPU with 80 GB VRAM for sequences of different lengths (using a `batch_size_100=20` setting in `sample.py`):
 | sequence length | time / min |
 | --------------: | ---------: |
 |             100 |          4 |
 |             300 |         40 |
 |             600 |        150 |

By default, unphysical structures (steric clashes or chain discontinuities) will be filtered out, so you will typically get fewer samples in the output than requested. The difference can be very large if your protein has large disordered regions which are very likely to produce clashes. If you want to get all generated samples in the output, irrespective of whether they are physically valid, use the `--filter_samples=False` argument.


> [!NOTE]
> If you wish to use your own generated MSA instead of the ones retrieved via Colabfold, you can pass an A3M file containing the query sequence as the first row to the `sequence` argument. Additionally, the `msa_host_url` argument can be used to override the default Colabfold MSA query server. See [sample.py](./src/bioemu/sample.py) for more options.

This code only supports sampling structures of monomers. You can try to sample multimers using the [linker trick](https://x.com/ag_smith/status/1417063635000598528), but in our limited experiments, this has not worked well.



## Reproducing results from the preprint
You can use this code together with code from [bioemu-benchmarks](https://github.com/microsoft/bioemu-benchmarks) to approximately reproduce results from our [preprint](https://www.biorxiv.org/content/10.1101/2024.12.05.626885v1).

The `bioemu-v1.0` checkpoint contains the model weights used to produce the results in the preprint. Due to simplifications made in the embedding computation and a more efficient sampler, the results obtained with this code are not identical but consistent with the statistics shown in the preprint, i.e., mode coverage and free energy errors averaged over the proteins in a test set. Results for individual proteins may differ. For more details, please check the [BIOEMU_RESULTS.md](https://github.com/microsoft/bioemu-benchmarks/blob/main/bioemu_benchmarks/BIOEMU_RESULTS.md) document on the bioemu-benchmarks repository.


## Side-chain reconstruction and MD-relaxation (To be implemented in MPS)
BioEmu outputs structures in backbone frame representation. To reconstruct the side-chains, several tools are available. As an example, we interface with [HPacker](https://github.com/gvisani/hpacker) to conduct side-chain reconstruction, and also provide basic tooling for running a short molecular dynamics (MD) equilibration.

> [!WARNING]
> This portion of the code is under construction.


## Third-party code
The code in the `openfold` subdirectory is copied from [openfold](https://github.com/aqlaboratory/openfold) with minor modifications. The modifications are described in the relevant source files.
## Get in touch
If you have any questions not covered here, please create an issue or contact the BioEmu team by writing to the corresponding author on our [preprint](https://doi.org/10.1101/2024.12.05.626885).

Write to the author of this port, [@Geoffitect](https://github.com/geoffitect), [here](mailto:gtaghon@icloud.com).

## Citation
If you are using our code or model, please cite the following paper:
```bibtex
@article{bioemu2025,
  title={Scalable emulation of protein equilibrium ensembles with generative deep learning},
  author={Lewis, Sarah and Hempel, Tim and Jim{\'e}nez-Luna, Jos{\'e} and Gastegger, Michael and Xie, Yu and Foong, Andrew YK and Satorras, Victor Garc{\'\i}a and Abdin, Osama and Veeling, Bastiaan S and Zaporozhets, Iryna and Chen, Yaoyi and Yang, Soojung and Foster, Adam E. and Schneuing, Arne and Nigam, Jigyasa and Barbero, Federico and Stimper Vincent and  Campbell, Andrew and Yim, Jason and Lienen, Marten and Shi, Yu and Zheng, Shuxin and Schulz, Hannes and Munir, Usman and Sordillo, Roberto and Tomioka, Ryota and Clementi, Cecilia and No{\'e},  Frank},
  journal={Science},
  pages={eadv9817},
  year={2025},
  publisher={American Association for the Advancement of Science},
  doi={10.1126/science.adv9817}
}
```
