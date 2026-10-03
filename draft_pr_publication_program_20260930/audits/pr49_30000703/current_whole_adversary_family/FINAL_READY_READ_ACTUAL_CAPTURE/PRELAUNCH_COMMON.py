"""Bounded private review readiness predicates; no production/native operations."""
from pathlib import Path
from datetime import datetime
import json,hashlib,stat,os
F=Path(__file__).resolve().parent;R=F.parents[3]
def ref(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_nlink==1,str(p)
    b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=stat.S_IMODE(s.st_mode))
def body(p,v,mode=True):
    q=ref(p)
    for k in ['bytes','sha256']+(['full_mode'] if mode else []):
        assert type(v[k]) is type(q[k]) and q[k]==v[k],(str(p),k)
    return q
def load(p):return json.loads(p.read_bytes())
def topology():
    files=[];dirs=[];dm=[dict(path='.',full_mode=stat.S_IMODE(F.lstat().st_mode))]
    for root,ds,fs in os.walk(F,followlinks=False):
        for n in ds:
            p=Path(root)/n; s=p.lstat();assert stat.S_ISDIR(s.st_mode) and not p.is_symlink()
            v=str(p.relative_to(F));dirs.append(v);dm.append(dict(path=v,full_mode=stat.S_IMODE(s.st_mode)))
        for n in fs:
            p=Path(root)/n;ref(p);files.append(str(p.relative_to(F)))
    assert len({v.casefold() for v in [*files,*dirs]})==len(files)+len(dirs)
    expected=set()
    for n in files:
        p=Path(n).parent
        while str(p)!='.':expected.add(str(p));p=p.parent
    assert set(dirs)==expected,'Extra empty directories forbidden'
    return sorted(files),sorted(dirs),sorted(dm,key=lambda v:v['path'])
CAPS={
 'CURRENT_READ_ACTUAL_CAPTURE':(59270,1),
 'CURRENT_READ_V2_ACTUAL_CAPTURE':(59973,1),
 'CURRENT_READ_V3_ACTUAL_CAPTURE':(61152,1),
 'CURRENT_READ_V4_ACTUAL_CAPTURE':(62254,0),
 'AUTHOR_LITERAL_ACTUAL_CAPTURE':(60270,0),
 'DUPLICATE_LITERAL_ACTUAL_CAPTURE':(60400,0),
 'HISTORICAL_INDEPENDENT_LITERAL_ACTUAL_CAPTURE':(60399,0),
 'TARGET_CONTROLS_ACTUAL_CAPTURE':(62256,0),
 'RECEIPT_COMPARISON_ACTUAL_CAPTURE':(63339,0)
}
def inspect_complete():
    v=load(F/'VERDICT.json');body(F/'REPORT.md',v['report'],False)
    assert v['mandatory_corrections']==[] and v['status']=='already_solved'
    assert v['candidate_manifest']['sha256']=='8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47'
    for k in ['future_acceptance_approved','ROOT_approval_created','production_imported_compiled_executed','native_write','index_or_Git_ref_mutation','remote_or_GH_write','paper_created','new_DOI_created','tracker_row_created','external_communication','project_solved','novelty_claimed','blind_new_math_family','full_2007_journal_proof_independently_certified']:assert v[k] is False,k
    for k in ['current_body_mode_read_ledger','literal_reproduction','exact_target_controls']:body(R/v[k]['path'],v[k],False)
    ledger=load(F/'CURRENT_READ_LEDGER.json')
    assert ledger['candidate_manifest']==v['candidate_manifest'] and ledger['payload_count']==1544 and ledger['dependency_count']==1407
    external=[]
    for w in ledger['full_body_mode_rows']:external.append(body(R/w['path'],w))
    assert len(external)==3087 and len({w['path'] for w in external})==3087
    captures=[]
    for name,(pid,rc) in CAPS.items():
        d=F/name;q=load(d/'CAPTURE.json');pre=load(d/'PRELAUNCH.json')
        assert q['pid']==pid and q['exit_code']==rc and q['actual_execution'] is True and q['completed'] is True
        assert q['source_unchanged'] is True and q['operator_unchanged'] is True
        assert datetime.fromisoformat(q['started_utc'])<datetime.fromisoformat(q['finished_utc'])
        assert pre=={k:q[k] for k in pre}
        assert q['cwd']==str(R) and q['stdin_supplied'] is False and q['argv'][0:2]==['/usr/bin/python3','-B']
        p=Path(q['argv'][2]);assert p.is_relative_to(F)
        body(p,q['source'],False);body(d/'PRELAUNCH_SOURCE.py',q['source'],False)
        body(d/'PRELAUNCH_OPERATOR.py',q['operator'],False)
        for k in ['stdout','stderr']:body(R/q[k]['path'],q[k],False)
        captures.append(dict(capture=ref(d/'CAPTURE.json'),pid=pid,exit_code=rc,started_utc=q['started_utc'],finished_utc=q['finished_utc']))
    repro=load(F/'LITERAL_REPRODUCTION_RESULT.json');assert repro['status']=='PASS' and repro['strict_current_JSON_objects']==728
    controls=load(F/'TARGET_CONTROL_RESULTS.json');assert controls['status']=='PASS' and len(controls['cases'])==13
    files,dirs,dm=topology()
    return dict(external_rows=external,captures=captures,owned_files=files,directories=dirs,directory_full_modes=dm)
