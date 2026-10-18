#!/usr/bin/env python3
"""Replay the unchanged scalar code and ported independent mathematical controls."""
from pathlib import Path
import json,os,subprocess,sys,tempfile
sys.dont_write_bytecode=True
from VERIFY_PUBLIC import verify

ROOT=Path(__file__).resolve().parent
integrity=verify()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
with tempfile.TemporaryDirectory(prefix='orbitwise-30001568-') as tmp:
    output=Path(tmp)
    author=subprocess.run([sys.executable,str(ROOT/'author/orbitwise_evaluator.py')],check=True,capture_output=True,text=True,env=env)
    author_json=json.loads(author.stdout)
    assert author_json==json.loads((ROOT/'author/AUTHOR_TESTS.json').read_text())
    (output/'AUTHOR_TEST_RERUN.json').write_text(author.stdout)
    subprocess.run([sys.executable,str(ROOT/'review/portable_independent_controls.py'),str(output)],check=True,capture_output=True,text=True,env=env)
    independent=json.loads((output/'INDEPENDENT_CONTROLS.json').read_text())
    mathematical=[c for c in independent['checks'] if c['category'] not in ['integrity','author_reproduction']]
    frozen=json.loads((ROOT/'review/MATHEMATICAL_CHECKS.json').read_text())
    frozen_math=[c for c in frozen['checks'] if c['category'] not in ['integrity','author_reproduction']]
    assert mathematical==frozen_math
    assert len(mathematical)==98 and independent['passed']==108 and independent['failed']==0
    result={'id':30001568,'author_diagnostics':author_json['passed'],'additional_independent_mathematical_assertions':len(mathematical),'portable_independent_total':independent['passed'],'historical_independent_total':150,'all_mathematical_outputs_match_frozen_review':True,'public_integrity':integrity,'status':'pass','novelty_claim':False,'efficiency_claim':False}
verify()
print(json.dumps(result,indent=2))
