#!/usr/bin/env python3
"""Replay the frozen preparer's actual offline controls, without writing its tree."""
from pathlib import Path
import hashlib,importlib.util,json,sys
BASE=Path(__file__).resolve().parent
AUDIT=BASE.parents[1]
SOURCE=AUDIT/'publication_operations_preparation/offline_controls.py'
EXPECTED='7a0b78fd3387fa3399ab8b77cae6cbcd548bfcfc20e945ea2a66ac8d8e5f7b3d'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=EXPECTED:raise RuntimeError('Control binding changed')
sys.path.insert(0,str(AUDIT))
spec=importlib.util.spec_from_file_location('bound_preparer_offline_controls',SOURCE)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
# main installs process/network/provider traps before any test. Only its private
# scratch/output location is redirected; helper and fixture bytes are unchanged.
module.HERE=BASE/('operations_replay_optimized' if sys.flags.optimize else 'operations_replay_normal')
module.HERE.mkdir(exist_ok=True)
module.main()
