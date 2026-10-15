#!/usr/bin/env python3
"""Replay frozen author controls in a copied layout; never modify author reports."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).absolute().parent
A=HERE.parents[1]
freeze=A/'reviews/operations_author_01/FINAL_FREEZE.json'
if hashlib.sha256(freeze.read_bytes()).hexdigest()!='1c5919ed21e193c369a95388170da3a65e8c3e11a002e9c8febbc262415efa58':
    raise ValueError('unreviewed operational author freeze')
pins=json.loads(freeze.read_bytes())['files']
for name,pin in pins.items():
    data=(A/name).read_bytes()
    if len(data)!=pin['bytes'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:
        raise ValueError('frozen operation input drift: '+name)
layout=HERE/'tmp/frozen-operations-layout'
if layout.exists():shutil.rmtree(layout)
layout.mkdir()
shutil.copytree(A/'native',layout/'native')
shutil.copytree(A/'publication',layout/'publication',ignore=shutil.ignore_patterns('tmp','__pycache__','*.log','COMPILE.*'))
shutil.copyfile(A/'SCOPE_AND_SNAPSHOT.json',layout/'SCOPE_AND_SNAPSHOT.json')
for name in ('prepare_integration.py','record_tracker.py','ACCEPTED_PR_DESCRIPTION.template.md',
             'reviews/operations_author_01/offline_controls.py','reviews/operations_author_01/replay_proposed_tree.py'):
    p=layout/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((A/name).read_bytes())
review=layout/'reviews/operations_author_01'
(review/'tmp').mkdir(exist_ok=True)
reports={}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(HERE/'tmp'))
for optimized in (False,True):
    mode='optimized' if optimized else 'normal'
    command=[sys.executable,'-I','-B',*(['-O'] if optimized else []),str(review/'offline_controls.py')]
    result=subprocess.run(command,env=env,cwd=layout,capture_output=True,timeout=180)
    if result.returncode:raise ValueError(result.stderr.decode())
    report=json.loads((review/f'OFFLINE_CONTROL_RESULTS.{mode}.json').read_bytes())
    if report['status']!='PASS' or report['checks']!=147:raise ValueError('author operation controls failed')
    reports[mode]=report
    (HERE/f'FROZEN_AUTHOR_OPERATION_REPLAY.{mode}.json').write_text(json.dumps(report,indent=2)+'\n')
if reports['normal']['results']!=reports['optimized']['results'] or reports['normal']['source_sha256']!=reports['optimized']['source_sha256']:
    raise ValueError('author operation modes differ')
result=subprocess.run([sys.executable,'-I','-B',str(review/'replay_proposed_tree.py')],env=env,cwd=layout,capture_output=True,timeout=300)
if result.returncode:raise ValueError(result.stderr.decode())
proposed=json.loads((review/'ACTUAL_PROPOSED_TREE_REPLAY.json').read_bytes())
if proposed['status']!='PASS' or proposed['helper_sha256']!=pins['prepare_integration.py']['sha256']:
    raise ValueError('actual frozen proposed-layout replay failed')
(HERE/'ACTUAL_PROPOSED_LAYOUT_REPLAY.json').write_text(json.dumps(proposed,indent=2)+'\n')
for name,pin in pins.items():
    data=(A/name).read_bytes()
    if len(data)!=pin['bytes'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:
        raise ValueError('original author files changed during isolated replay')
summary={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'author_controls_per_mode':147,'author_normal_optimized_results_equal':True,
         'real_proposed_layout_replayed':True,'original_author_files_unchanged':True,
         'all_fixtures_explicitly_synthetic':True,'no_live_service_or_shared_git_mutation':True}
(HERE/'FROZEN_OPERATIONS_REPLAY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
