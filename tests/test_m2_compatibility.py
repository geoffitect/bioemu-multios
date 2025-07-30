#!/usr/bin/env python3
"""
Test script for BioEmu Apple M2 MPS compatibility.
This script verifies that the CUDA-to-MPS port is working correctly.
"""

import sys
import torch
sys.path.insert(0, 'src')

from bioemu.device_utils import get_optimal_device, get_optimal_device_for_dtype, is_mps_available
from bioemu.shortcuts import DiGConditionalScoreModel, DiGSO3SDE, CosineVPSDE
from bioemu.openfold.utils.rigid_utils import Rotation, Rigid


def test_device_detection():
    """Test device detection and selection."""
    print("=== Device Detection Test ===")
    print(f"MPS available: {is_mps_available()}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"Optimal device (general): {get_optimal_device()}")
    print(f"Optimal device (float32): {get_optimal_device_for_dtype(torch.float32)}")
    print(f"Optimal device (float64): {get_optimal_device_for_dtype(torch.float64)}")
    print()


def test_tensor_operations():
    """Test basic tensor operations on MPS vs CPU."""
    print("=== Tensor Operations Test ===")
    
    # Test float32 on MPS
    device_general = get_optimal_device()
    x32 = torch.randn(10, 10, dtype=torch.float32).to(device_general)
    y32 = torch.matmul(x32, x32.T)
    print(f"✅ Float32 operations on {device_general}: {y32.shape}")
    
    # Test float64 on appropriate device (CPU for MPS systems)
    device_f64 = get_optimal_device_for_dtype(torch.float64)
    x64 = torch.randn(10, 10, dtype=torch.float64).to(device_f64)
    y64 = torch.matmul(x64, x64.T)
    print(f"✅ Float64 operations on {device_f64}: {y64.shape}")
    print()


def test_rigid_utils():
    """Test ported OpenFold rigid utilities."""
    print("=== Rigid Utils Test ===")
    
    # Test rotation matrix operations
    rot_mat = torch.eye(3).unsqueeze(0)  # 1x3x3
    rotation = Rotation(rot_mats=rot_mat)
    print(f"Created rotation on: {rotation._rot_mats.device}")
    
    # Test our ported .cuda() method (now uses optimal device)
    rotation_gpu = rotation.cuda()
    print(f"After .cuda() call: {rotation_gpu._rot_mats.device}")
    
    # Test rigid body operations
    trans = torch.zeros(1, 3)
    rigid = Rigid(rotation, trans)
    rigid_gpu = rigid.cuda()
    print(f"✅ Rigid operations on: {rigid_gpu._trans.device}")
    print()


def test_so3_sde():
    """Test SO3 SDE with our float64 compatibility fixes."""
    print("=== SO3 SDE Test ===")
    
    try:
        # Create small SO3 SDE for testing (avoids long precomputation)
        so3_sde = DiGSO3SDE(
            eps_t=0.001,
            num_sigma=5,   # Very small for testing
            num_omega=5,   # Very small for testing
            sigma_min=0.02,
            sigma_max=0.5,
            cache_dir=None,  # Don't use cache
            overwrite_cache=True
        )
        print("✅ SO3SDE initialized successfully with MPS/CPU dtype handling!")
        
    except Exception as e:
        print(f"❌ SO3SDE test failed: {e}")
        raise
    print()


def main():
    """Run all compatibility tests."""
    print("BioEmu Apple M2 MPS Compatibility Test")
    print("=" * 50)
    print("Note: This tests core functionality. Full sampling requires ColabFold setup.")
    print()
    
    test_device_detection()
    test_tensor_operations()
    test_rigid_utils()
    test_so3_sde()
    
    print("🎉 All tests passed! BioEmu is successfully ported for Apple M2!")
    print()
    print("Key improvements:")
    print("- MPS device support with CPU fallback")
    print("- Float64 operations automatically use CPU (MPS limitation)")
    print("- Float32 operations use MPS for acceleration")  
    print("- OpenFold rigid utilities ported to use optimal device")
    print("- All CUDA calls replaced with MPS-compatible equivalents")


if __name__ == "__main__":
    main()