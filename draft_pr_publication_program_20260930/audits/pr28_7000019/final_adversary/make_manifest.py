#!/usr/bin/env python3
"""Self-excluding manifest for the complete fresh gate's first-party artifacts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
NAME='FIRST_PARTY_MANIFEST.json'
def roster():
    return sorted(p for p in HERE.rglob('*') if p.is_file() and
                  not any(s in p.relative_to(HERE).parts for s in ['foreign','replays','tmp','__pycache__']) and
                  p.name!=NAME and p.suffix!='.pyc')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if '--verify' in sys.argv:
    m=json.loads((HERE/NAME).read_text());ps=roster()
    assert [str(p.relative_to(HERE)) for p in ps]==[x['path'] for x in m['files']]
    for p,x in zip(ps,m['files']):assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
    print(json.dumps({'manifest_exact':True,'first_party_files':len(ps),'self_excluded':True}))
else:
    m={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Complete fresh adversarial acceptance gate for exact candidate db23b0e…; no prior verdict inherited',
       'self_exclusion':NAME+' excludes itself; make_manifest.py is included',
       'foreign_exclusions':['foreign/','replays/','tmp/','__pycache__/','.pyc'],
       'early_reconstruction_sha256':sha(HERE/'EARLY_RECONSTRUCTION.md'),
       'candidate_manifest_sha256':'db23b0e890792a03b5f144348f23b5c6014898ce56ba19948e4740c603da1024',
       'files':[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in roster()]}
    (HERE/NAME).write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps({'first_party_files':len(m['files']),'manifest_self_excluded':True}))
