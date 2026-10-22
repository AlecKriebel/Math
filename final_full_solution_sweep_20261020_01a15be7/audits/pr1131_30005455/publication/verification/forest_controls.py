#!/usr/bin/env python3
"""Exact mathematical controls only; no private capture or foundational certification."""
import importlib.util, json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'audit/forest/verify_forest.py'
s=importlib.util.spec_from_file_location('fresh_forest_controls',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
print(json.dumps(m.finite_controls(),sort_keys=True))
