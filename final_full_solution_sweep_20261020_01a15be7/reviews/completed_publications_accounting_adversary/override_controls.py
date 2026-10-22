#!/usr/bin/env python3
from pathlib import Path
import copy,datetime as dt,importlib.util,json,shutil,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
S=R/'inputs/effort'
F=R/'fixtures/coverage_snapshot_captured'
if F.exists():
 F=R/'fixtures/coverage_snapshot_expanded_controls'
 if F.exists():raise RuntimeError('Refusing to replace existing expanded fixture')
F.mkdir(parents=True)
for p in S.glob('*'):
 if p.is_file():shutil.copyfile(p,F/p.name)
sp=importlib.util.spec_from_file_location('fixture_coverage',F/'coverage_snapshot.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
base={p.name:p.read_bytes() for p in F.iterdir() if p.is_file()}
def set_json(file,fn):
 d=json.loads((F/file).read_text());fn(d);(F/file).write_text(json.dumps(d,indent=2)+'\n')
def state(fn):set_json('STATE.json',fn)
def replacement(fn):set_json('PR0280_REOPENED_DISPOSITION.json',fn)
def publication(fn):set_json('PR0280_REOPENED_PUBLICATION_VERIFICATION.json',fn)
def run(name,fn,expected_reject):
 for f,b in base.items():(F/f).write_bytes(b)
 fn();e=None
 try:v=mod.snapshot();accepted=True
 except Exception as exc:e=type(exc).__name__+': '+str(exc);accepted=False;v=None
 changes={f.name:json.loads(f.read_text()) if f.suffix=='.json' else f.read_text() for f in F.iterdir() if f.is_file() and f.read_bytes()!=base[f.name]}
 (R/'fixtures'/f'{name}.json').write_text(json.dumps({'mutated_inputs':changes},indent=2)+'\n')
 return {'name':name,'expected_reject':expected_reject,'accepted':accepted,'error':e,'control_pass':accepted!=expected_reject,'effective_published_count':v['disposition_counts'].get('published_verified_full_solution') if v else None}
cases=[
 ('baseline',lambda:None,False),
 ('alter_historical_hash',lambda:state(lambda d:d['reopened_disposition_overrides'][0].update(historical_disposition_sha256='0'*64)),True),
 ('duplicate_override',lambda:state(lambda d:d['reopened_disposition_overrides'].append(copy.deepcopy(d['reopened_disposition_overrides'][0]))),True),
 ('duplicate_doi',lambda:state(lambda d:d['completed_publications'][0].update(doi=d['completed_publications'][1]['doi'])),True),
 ('publication_flag_false',lambda:publication(lambda d:d.update(published=False)),True),
 ('wrong_completed_doi',lambda:state(lambda d:d['completed_publications'][3].update(doi='10.5281/zenodo.99999999')),True),
 ('publication_row_mismatch',lambda:publication(lambda d:d.update(ledger_row=179)),True),
 ('wrong_replacement_pr',lambda:replacement(lambda d:d.update(pr=999)),True),
 ('wrong_publication_pr',lambda:publication(lambda d:d.update(pr=999)),True),
 ('wrong_replacement_row',lambda:replacement(lambda d:d.update(ledger_row=179)),True),
 ('wrong_completed_verification_path',lambda:state(lambda d:d['completed_publications'][3].update(verification='PR0292_PUBLICATION_VERIFICATION.json')),True),
 ('wrong_completed_record',lambda:state(lambda d:d['completed_publications'][3].update(record=23524971)),True),
 ('wrong_completed_problem',lambda:state(lambda d:d['completed_publications'][3].update(problem_id='30001608')),True),
 ('wrong_replacement_problem',lambda:replacement(lambda d:d.update(problem_ids=['30001608'])),True),
 ('wrong_publication_record',lambda:publication(lambda d:d.update(record=23524971)),True),
 ('missing_public_files',lambda:publication(lambda d:d.update(files=[])),True),
 ('ordinary_wrong_completed_doi',lambda:state(lambda d:d['completed_publications'][0].update(doi='10.5281/zenodo.99999999')),True),
 ('ordinary_wrong_completed_pr',lambda:state(lambda d:d['completed_publications'][0].update(pr=293)),True),
 ('duplicate_completed_pr_new_doi',lambda:state(lambda d:d['completed_publications'].append(dict(d['completed_publications'][0],doi='10.5281/zenodo.99999999'))),True),
 ('unbound_extra_publication',lambda:state(lambda d:d['completed_publications'].append(dict(d['completed_publications'][0],pr=999,doi='10.5281/zenodo.99999999'))),True),
 ('noncanonical_original_verification_for_292',lambda:state(lambda d:d['completed_publications'][0].update(verification='PR0397_PUBLICATION_VERIFICATION.json')),True),
]
results=[run(*case) for case in cases]
for f,b in base.items():(F/f).write_bytes(b)
o={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'Isolated fixture copies only; acceptance of false bound identities is a validation gap, not evidence of canonical bad data.','results':results}
(R/'OVERRIDE_CONTROLS.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
