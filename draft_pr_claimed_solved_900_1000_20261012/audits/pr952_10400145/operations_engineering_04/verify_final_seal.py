#!/usr/bin/env python3
"""Read-only exact public installed engineering seal authentication."""
from pathlib import Path
import argparse,hashlib,json,stat
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent;A=P/'audits/pr952_10400145'
p=argparse.ArgumentParser();p.add_argument('--seal-sha256',required=True);a=p.parse_args()
def need(ok,m):
 if not ok:raise RuntimeError(m)
def raw(path):
 path=Path(path);parts=path.relative_to(ROOT).parts;need(all(x not in ('','.','..') for x in parts),'safe input')
 for i in range(len(parts)+1):need(not ROOT.joinpath(*parts[:i]).is_symlink(),'no linked input')
 need(path.is_file() and stat.S_ISREG(path.stat().st_mode),'regular input');return path.read_bytes()
def pin(path):
 b=raw(path);return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(path.stat().st_mode,'06o')}
manifest=raw(OWN/'MANIFEST.json');need(hashlib.sha256(manifest).hexdigest()==a.seal_sha256,'external seal');doc=json.loads(manifest);files=doc['files'];allowed=doc['explicit_public_allowlist'];need(type(files) is dict and type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(files),'exact explicit public closure')
for name,item in files.items():need(pin(ROOT/name)==item,'public member changed '+name)
mutable={str((P/name).relative_to(ROOT)) for name in ['CURRENT_STATE.json','inventory.json','RESEARCH_LOG.md']}|{str((A/'RESEARCH_LOG.md').relative_to(ROOT))}
need(not(set(files)&mutable) and not any((ROOT/name).is_relative_to(A/'publication/workflow') for name in files),'mutable shared bookkeeping excluded')
need(doc['acceptance_authority'] is False and doc['fresh_whole_review_credit'] is False,'engineering scope')
print(json.dumps({'status':'PASS_INSTALLED_ENGINEERING_PUBLIC_SEAL','seal_sha256':a.seal_sha256,'authenticated_public_files':len(files),'mutable_active_bookkeeping_paths_excluded':True,'actual_installed_core_sha256':pin(P/'accept_pr952.py')['sha256'],'acceptance_authority':False,'source_executed':False},sort_keys=True))
