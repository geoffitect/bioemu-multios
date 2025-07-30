# BioEmu MultiOS Fork 🍎

> **Apple M Compatible Version** of Microsoft's BioEmu Protein Folding AI

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org/downloads)
[![Apple Silicon](https://img.shields.io/badge/Apple-Silicon-black.svg)](https://support.apple.com/en-us/HT211814)
[![MPS Accelerated](https://img.shields.io/badge/MPS-Accelerated-orange.svg)](https://developer.apple.com/metal/pytorch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h1>
<p align="center">
    <img src="assets/emu_apple.png" alt="BioEmu logo with Apple sunglasses" width="300"/>
</p>
</h1>

This is an **Apple Silicon optimized fork** of Microsoft's [BioEmu](https://github.com/microsoft/bioemu) that replaces CUDA operations with Metal Performance Shaders (MPS) and CPU fallback for seamless operation on Apple M1/M2/M3 Macs.

## 🎯 What's New in This Fork

### ✅ **Complete CUDA-to-MPS Port**
- **MPS Acceleration**: Uses Metal Performance Shaders for GPU operations
- **Smart Device Selection**: Automatic MPS/CPU routing based on operation type
- **Float64 Compatibility**: CPU fallback for float64 operations (MPS limitation)
- **Error Handling**: Robust fallback mechanisms

### ✅ **Apple Silicon ColabFold**
- **M2-Compatible Setup**: Custom ColabFold installation for Apple Silicon
- **JAX CPU Backend**: Optimized for Apple Silicon architecture
- **Automatic Detection**: Platform-aware installation scripts
- **No CUDA Dependencies**: Clean Apple Silicon deployment

### ✅ **Enhanced Testing & Documentation**
- **M2 Test Suite**: Comprehensive Apple Silicon compatibility tests
- **Installation Guides**: Step-by-step Apple Silicon setup
- **Performance Benchmarks**: Expected performance on different Mac models
- **Troubleshooting**: Common issues and solutions

## 🚀 Quick Start

### Installation
```bash
# Clone the Apple Silicon fork
git clone https://github.com/latent-spacecraft/bioemu-multios.git
cd bioemu-apple

# Create environment
conda create -n bioemu python=3.11
conda activate bioemu

# Install package
pip install -e .
```

### Basic Usage
```bash
# Test Apple Silicon compatibility
bioemu-test-m2

# Sample protein structures
bioemu-sample --sequence GYDPETGTWG --num_samples 10 --output_dir ~/samples
```

## 📊 Performance Comparison

| Hardware | Original (CUDA) | Apple Fork (MPS+CPU) | Status |
|----------|----------------|---------------------|--------|
| Apple M1 | ❌ Not Supported | ✅ Working | ~90s/sample* |
| Apple M2 | ❌ Not Supported | ✅ **Optimized** | ~60s/sample* |
| Apple M3 | ❌ Not Supported | ✅ **Optimized** | ~45s/sample* |
| Intel Mac | ⚠️ CPU Only | ✅ CPU + Fallback | ~120s/sample* |

*_10-residue protein, 1 sample. Performance varies by sequence length._

## 🛠 Technical Details

### Device Selection Logic
```python
# Automatic device optimization
MPS → CUDA → CPU          # For float32 operations (model inference)
CUDA → CPU → MPS          # For float64 operations (numerical precision)
```

### Key Components
- **`device_utils.py`**: Smart device management
- **`colabfold_setup/setup_m2.sh`**: Apple Silicon ColabFold installer
- **Modified modules**: `sample.py`, `so3_sde.py`, `rigid_utils.py`
- **Test suite**: `tests/test_m2_compatibility.py`

## 🆚 Differences from Original

| Feature | Original BioEmu | Apple Silicon Fork |
|---------|----------------|-------------------|
| **GPU Support** | CUDA only | MPS + CPU fallback |
| **ColabFold** | CUDA installation | Apple Silicon compatible |
| **Float64 Ops** | CUDA/CPU | CPU (MPS limitation) |
| **Installation** | Linux focused | macOS optimized |
| **Testing** | CUDA tests | MPS + M2 tests |
| **Dependencies** | NVIDIA packages | Apple optimized |

## 📦 Package Distribution

### Install from Package
```bash
# Install the pre-built package from wheel

pip install dist/bioemu_multios-0.1.12a1-py3-none-any.whl
```

### Build from Source
```bash
# Build wheel
python -m build --wheel

# Install built package
pip install dist/bioemu_multios-*.whl
```

## 🧪 Testing

### Compatibility Test
```bash
bioemu-test-m2
```

### End-to-End Test
```bash
bioemu-sample --sequence GYDP --num_samples 1 --output_dir ~/test
```

### Expected Output
```
=== BioEmu Apple M2 MPS Compatibility Test ===
MPS available: True
CUDA available: False
Optimal device: mps
✅ Float32 operations on mps: torch.Size([10, 10])
✅ Float64 operations on cpu: torch.Size([10, 10])
✅ Rigid operations on: mps:0
✅ SO3SDE initialized successfully with MPS/CPU dtype handling!
🎉 All tests passed! BioEmu is successfully ported for Apple M2!
```

## 🤝 Contributing

This fork maintains compatibility with the original BioEmu while adding Apple Silicon support. 

### Contribution Areas
- Apple Silicon optimizations
- MPS compatibility improvements  
- Performance benchmarking
- Documentation updates
- Bug fixes and testing

### Guidelines
1. Test on Apple Silicon hardware
2. Ensure MPS compatibility
3. Maintain CPU fallback functionality
4. Update tests and documentation

## 📄 License & Attribution

- **License**: MIT (same as original)
- **Original Work**: Microsoft Research - [BioEmu](https://github.com/microsoft/bioemu)
- **Apple Silicon Port**: [Geoff Taghon](https://github.com/geoffitect)
- **Citation**: Please cite both the original BioEmu paper and mention this Apple Silicon fork

### Original Citation
```bibtex
@article {BioEmu2024,
    author = {Lewis, Sarah and Hempel, Tim and Jiménez-Luna, José and ...},
    title = {Scalable emulation of protein equilibrium ensembles with generative deep learning},
    year = {2024},
    doi = {10.1101/2024.12.05.626885},
    journal = {bioRxiv}
}
```

## 🔗 Links

- **Original Repository**: [microsoft/bioemu](https://github.com/microsoft/bioemu)
- **Apple Silicon Fork**: [latent-spacecraft/bioemu-multios](https://github.com/yourusername/bioemu-apple)
- **Documentation**: [Installation Guide](./INSTALL_APPLE.md)
- **Commands Reference**: [Commands Guide](./COMMANDS.md)

---

**🍎 Optimized for Apple | 🔬 Powered by BioEmu | 🧬 Advancing Protein Science**
