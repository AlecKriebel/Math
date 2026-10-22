#!/usr/bin/env python3
"""Authenticate the externally pinned public proposal closure; no source execution."""
from pathlib import Path
import argparse,hashlib,json,stat
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
p=argparse.ArgumentParser();p.add_argument('--readiness-sha256',required=True);p.add_argument('--check-current-protected',action='store_true');a=p.parse_args()
def need(ok,m):
 if not ok:raise RuntimeError(m)
def raw(path):
 path=Path(path);parts=path.relative_to(ROOT).parts;need(all(x not in ('','.','..') for x in parts),'safe repository path')
 for i in range(len(parts)+1):need(not ROOT.joinpath(*parts[:i]).is_symlink(),'no linked input')
 need(path.is_file() and stat.S_ISREG(path.stat().st_mode),'regular input');return path.read_bytes()
def pin(path):
 b=raw(path);return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(path.stat().st_mode,'06o')}
readiness=raw(OWN/'PROPOSAL_READINESS.json');need(hashlib.sha256(readiness).hexdigest()==a.readiness_sha256,'external readiness pin');doc=json.loads(readiness);files=doc['files'];allowed=doc['explicit_public_allowlist'];need(type(files) is dict and type(allowed) is list and len(allowed)==len(set(allowed)) and set(files)==set(allowed),'explicit public closure')
for name,item in files.items():need(pin(ROOT/name)==item,'public file changed '+name)
if a.check_current_protected:
 for item in doc['protected_inputs'].values():need(pin(ROOT/item['path'])['sha256']==item['sha256'],'protected input changed '+item['path'])
need(doc['actual_remote_mutation_calls']==0 and doc['scientific_acceptance_authority'] is False and doc['fresh_whole_review_credit'] is False,'proposal scope')
print(json.dumps({'status':'PASS_PUBLIC_PROPOSAL_CLOSURE','readiness_sha256':a.readiness_sha256,'authenticated_public_files':len(files),'current_protected_inputs_checked':a.check_current_protected,'source_executed':False,'acceptance_authority':False},sort_keys=True))
