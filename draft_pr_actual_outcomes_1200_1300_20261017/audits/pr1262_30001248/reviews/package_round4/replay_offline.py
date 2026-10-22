#!/usr/bin/env python3
"""Run the actual supplied mocked workers; redirect only temporary output roots."""
import importlib.util,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
def load(p):
    spec=importlib.util.spec_from_file_location('round4_'+p.stem,p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
kind=sys.argv[1]
if kind=='repair':
    m=load(AUDIT/'reviews/draft_repair_tooling/offline_fault_checks.py')
    m.F=HERE/'_local'/'repair-worker';(m.F/'_local').mkdir(parents=True,exist_ok=True)
elif kind=='workflow':
    m=load(AUDIT/'publication/workflow_regression.py')
    m.REPORT_ROOT=HERE/'_local'/'workflow-worker'
else:raise ValueError(kind)
print(json.dumps(m.worker(),sort_keys=True))
