#!/usr/bin/env python3
"""Owned preparation adapter; no provider calls/ref writes; imports a pinned reader."""
from pathlib import Path
import hashlib,importlib.util,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
R=Path('/Users/alec/Documents/Math')
W=R/'draft_pr_descending_audit_20261002/audits/pr263_30000170/initial_review_20261011'
B=R/'draft_pr_descending_audit_20261002/audits/pr278_30005468/resume_20261011'
H=B/'checkpoint_resume/prepare_checkpoint.py'
assert ROOT==W/'publication_checkpoint_20261011' and ROOT.resolve()==ROOT
assert hashlib.sha256(H.read_bytes()).hexdigest()=='e5399e719a2a93a0e7d34670ff503a897a18cb2c8632a766248d21d50b3dd298'
spec=importlib.util.spec_from_file_location('pinned_scoped_checkpoint',H)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.ROOT=ROOT;m.DRIVER=ROOT/'driver.git';m.OBJECTS=ROOT/'private_objects'
m.ALTERNATES=[W/'integration_preparation/private_objects',B/'checkpoint_resume/private_objects',B/'reconciliation/private_objects',B/'objects.git/objects']
for p in [m.DRIVER,m.OBJECTS]:assert p.resolve()==p and not p.is_symlink() and p.is_relative_to(ROOT)
for p in m.ALTERNATES:assert p.resolve()==p and not p.is_symlink() and (p.is_relative_to(W) or p.is_relative_to(B))
# Only the explicit Root allowlist may select these UTF8, non-NUL evidence files.
# Authored verifier stdout and exact published Git commit bytes are useful evidence.
m.TEXT_SUFFIXES=m.TEXT_SUFFIXES|{'.stdout','.raw'}
if __name__=='__main__':m.main()
