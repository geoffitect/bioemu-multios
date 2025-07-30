#!/usr/bin/env python3
"""
setup.py for BioEmu Apple Silicon Fork

Apple M2/M3 compatible version of Microsoft's BioEmu protein folding AI.
This fork replaces CUDA operations with MPS (Metal Performance Shaders) and CPU fallback.

Author: Apple Silicon Port
Original: Microsoft Research
License: MIT

Note: Most configuration is in pyproject.toml. This file provides compatibility
for older pip versions and custom platform-specific logic.
"""

from setuptools import setup

# Platform-specific customizations can be added here if needed
# For now, we rely on pyproject.toml for configuration

setup()