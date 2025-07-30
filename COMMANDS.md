# BioEmu Apple M2 MPS Port - Testing Commands

This document contains CLI commands for testing the CUDA-to-MPS port of BioEmu on Apple M2.

## Prerequisites

Ensure you're using the `bioemu` conda environment:
```bash
~/miniconda3/envs/bioemu/bin/python --version
```

**Apple M2 ColabFold Setup**: The first time you run sampling, BioEmu will automatically detect Apple Silicon and install a compatible ColabFold environment (without CUDA dependencies). This may take several minutes.

⚠️ **Important**: If you get an "AssertionError: Colabfold not patched!" error, remove the broken installation with `rm -rf ~/.bioemu_colabfold` and try again. This can happen if an earlier CUDA installation failed.

## Quick Compatibility Test

Run the comprehensive compatibility test:
```bash
~/miniconda3/envs/bioemu/bin/python test_m2_compatibility.py
```

This tests:
- Device detection (MPS/CUDA/CPU)
- Float32 operations on MPS
- Float64 operations on CPU (MPS limitation)
- OpenFold rigid utilities
- SO3 SDE initialization

## Basic Sampling Commands

### Test Sequence (Fast)
Sample structures for the test sequence from the README:
```bash
~/miniconda3/envs/bioemu/bin/python -m bioemu.sample \
    --sequence GYDPETGTWG \
    --num_samples 5 \
    --output_dir ~/bioemu_test_samples \
    --batch_size_100 1
```

### Custom Sequence
Sample structures for your own sequence:
```bash
~/miniconda3/envs/bioemu/bin/python -m bioemu.sample \
    --sequence "YOUR_PROTEIN_SEQUENCE" \
    --num_samples 10 \
    --output_dir ~/bioemu_custom_samples \
    --batch_size_100 2
```

### From FASTA File
Sample from a FASTA file:
```bash
# Create a FASTA file first
echo ">test_protein" > test.fasta
echo "GYDPETGTWG" >> test.fasta

# Sample from it
~/miniconda3/envs/bioemu/bin/python -m bioemu.sample \
    --sequence test.fasta \
    --num_samples 5 \
    --output_dir ~/bioemu_fasta_samples
```

## Python API Usage

You can also use the Python API directly:
```bash
~/miniconda3/envs/bioemu/bin/python -c "
import sys
sys.path.insert(0, 'src')
from bioemu.sample import main as sample

sample(
    sequence='GYDPETGTWG',
    num_samples=5,
    output_dir='~/bioemu_api_samples'
)
"
```

## Device Testing Commands

### Check Device Availability
```bash
~/miniconda3/envs/bioemu/bin/python -c "
import sys
sys.path.insert(0, 'src')
from bioemu.device_utils import get_optimal_device, is_mps_available
import torch

print(f'MPS available: {is_mps_available()}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'Optimal device: {get_optimal_device()}')
"
```

### Test MPS vs CPU Device Selection
```bash
~/miniconda3/envs/bioemu/bin/python -c "
import sys
sys.path.insert(0, 'src')
import torch
from bioemu.device_utils import get_optimal_device_for_dtype

print('Device selection by dtype:')
print(f'Float32: {get_optimal_device_for_dtype(torch.float32)}')
print(f'Float64: {get_optimal_device_for_dtype(torch.float64)}')
"
```

## Performance Monitoring

### Monitor Memory Usage
```bash
# In one terminal, run sampling:
~/miniconda3/envs/bioemu/bin/python -m bioemu.sample \
    --sequence GYDPETGTWG \
    --num_samples 5 \
    --output_dir ~/bioemu_perf_test

# In another terminal, monitor:
top -pid $(pgrep -f bioemu)
```

### Check GPU Memory (MPS)
```bash
# Monitor GPU memory usage during sampling
sudo powermetrics --samplers gpu_power -a --hide-cpu-duty-cycle -n 1
```

## Output Verification

### Check Generated Files
```bash
# After sampling completes, check outputs:
ls -la ~/bioemu_test_samples/

# Should see:
# - sequence.fasta (input sequence)
# - samples_*.npz (raw samples)
# - samples.pdb (structures)
# - samples.xtc (trajectory)
```

### Visualize Structures
```bash
# If you have PyMOL or similar installed:
pymol ~/bioemu_test_samples/samples.pdb

# Or check structure info:
head -20 ~/bioemu_test_samples/samples.pdb
```

## Troubleshooting Commands

### Check Import Issues
```bash
~/miniconda3/envs/bioemu/bin/python -c "
import sys
sys.path.insert(0, 'src')

modules = [
    'bioemu.device_utils',
    'bioemu.sample', 
    'bioemu.models',
    'bioemu.so3_sde',
    'bioemu.openfold.utils.rigid_utils'
]

for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except Exception as e:
        print(f'❌ {module}: {e}')
"
```

### Test Tensor Operations
```bash
~/miniconda3/envs/bioemu/bin/python -c "
import sys
sys.path.insert(0, 'src')
import torch
from bioemu.device_utils import get_optimal_device

device = get_optimal_device()
print(f'Testing operations on: {device}')

try:
    x = torch.randn(100, 100).to(device)
    y = torch.matmul(x, x.T)
    print(f'✅ Matrix ops successful: {y.shape}')
except Exception as e:
    print(f'❌ Matrix ops failed: {e}')
"
```

## Key Differences from CUDA Version

1. **Device Selection**: Automatically uses MPS when available, falls back to CPU
2. **Float64 Operations**: Automatically routed to CPU (MPS limitation)
3. **Memory Management**: MPS has different memory characteristics than CUDA
4. **Performance**: Float32 operations accelerated on MPS, float64 on CPU

## ColabFold Setup Commands

### Check Platform Detection
```bash
~/miniconda3/envs/bioemu/bin/python -c "
import sys
sys.path.insert(0, 'src')
import platform
from bioemu.get_embeds import _get_colabfold_install_script

print(f'Platform: {platform.system()} {platform.machine()}')
print(f'ColabFold script: {_get_colabfold_install_script()}')
"
```

### Manual ColabFold Setup (if needed)
```bash
# Set environment variables
export BIOEMU_COLABFOLD_DIR=~/.bioemu_colabfold

# Run M2-compatible setup manually
~/miniconda3/envs/bioemu/bin/python \
  src/bioemu/colabfold_setup/setup_m2.sh \
  $(which python) \
  $BIOEMU_COLABFOLD_DIR
```

### Check ColabFold Installation
```bash
ls -la ~/.bioemu_colabfold/
# Should see .COLABFOLD_PATCHED_M2 file when setup completes

# Test ColabFold executable
~/.bioemu_colabfold/bin/colabfold_batch --help
```

### Quick End-to-End Test
```bash
# Test complete pipeline with tiny sequence (fast validation)
~/miniconda3/envs/bioemu/bin/python -m bioemu.sample \
    --sequence GYDP \
    --num_samples 1 \
    --output_dir ~/bioemu_validation_test \
    --batch_size_100 1
```

## Expected Behavior

- **Fast Operations**: Model inference (float32) runs on MPS
- **Precise Operations**: SO3 computations (float64) run on CPU  
- **Fallback**: If MPS fails, automatically falls back to CPU
- **Compatibility**: All original CUDA functionality preserved
- **ColabFold**: Automatically installs M2-compatible version (JAX CPU, no CUDA)

## Sample Output Structure

After successful sampling, you'll see:
```
output_dir/
├── sequence.fasta          # Input sequence
├── samples_batch_0.npz     # Raw sample data
├── samples.pdb             # PDB structures
└── samples.xtc             # Trajectory file
```

Use these commands to test and validate the Apple M2 MPS port of BioEmu!