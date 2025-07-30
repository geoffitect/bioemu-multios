# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Device utilities for Apple M2 MPS compatibility with CPU fallback."""

import logging
import torch
from typing import Optional

logger = logging.getLogger(__name__)


def get_optimal_device(prefer_mps: bool = True) -> torch.device:
    """
    Get the optimal device for computation with MPS/CPU fallback.
    
    Args:
        prefer_mps: If True, prefer MPS over CPU when available
        
    Returns:
        torch.device: The optimal device (mps, cuda, or cpu)
    """
    if torch.cuda.is_available():
        logger.info("Using CUDA device")
        return torch.device("cuda:0")
    elif prefer_mps and torch.backends.mps.is_available():
        logger.info("Using MPS device")
        return torch.device("mps")
    else:
        logger.info("Using CPU device")
        return torch.device("cpu")


def to_device(tensor: torch.Tensor, device: Optional[torch.device] = None) -> torch.Tensor:
    """
    Move tensor to device with MPS/CPU fallback handling.
    Handles MPS dtype limitations (no float64 support).
    
    Args:
        tensor: Input tensor
        device: Target device (if None, uses get_optimal_device())
        
    Returns:
        torch.Tensor: Tensor moved to target device
    """
    if device is None:
        device = get_optimal_device()
    
    original_dtype = tensor.dtype
    
    try:
        # Handle MPS float64 limitation
        if device.type == "mps" and tensor.dtype == torch.float64:
            logger.info("Converting float64 to float32 for MPS compatibility")
            tensor = tensor.to(torch.float32)
        
        return tensor.to(device)
    except RuntimeError as e:
        if "mps" in str(device).lower():
            logger.warning(f"MPS failed ({e}), falling back to CPU")
            # Restore original dtype and move to CPU
            if original_dtype != tensor.dtype:
                tensor = tensor.to(original_dtype)
            return tensor.to("cpu")
        else:
            raise e


def get_device_type(device: torch.device) -> str:
    """Get device type string for compatibility checks."""
    return str(device).split(':')[0]


def is_mps_available() -> bool:
    """Check if MPS is available and functional."""
    return torch.backends.mps.is_available()


def is_cuda_available() -> bool:
    """Check if CUDA is available.""" 
    return torch.cuda.is_available()


def get_optimal_device_for_dtype(dtype: torch.dtype) -> torch.device:
    """
    Get optimal device considering dtype limitations.
    For float64 operations, prefer CUDA over MPS since MPS doesn't support float64.
    
    Args:
        dtype: The tensor dtype that will be used
        
    Returns:
        torch.device: The optimal device for the given dtype
    """
    if dtype == torch.float64:
        # For float64, prefer CUDA over MPS (which doesn't support it)
        if torch.cuda.is_available():
            return torch.device("cuda:0")
        else:
            # Fall back to CPU for float64 if no CUDA
            logger.info("Using CPU for float64 operations (MPS doesn't support float64)")
            return torch.device("cpu")
    else:
        # For other dtypes, use normal priority
        return get_optimal_device()