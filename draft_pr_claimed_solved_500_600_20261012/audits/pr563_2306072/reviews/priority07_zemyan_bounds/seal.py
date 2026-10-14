#!/usr/bin/env python3
"""Seal authored files; terminal SEAL binds manifest and verification receipt."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
here=Path(__file__).resolve().parent
names=['.gitignore','RESEARCH_LOG.md','SOURCE_IDENTITY.json','SOURCE_COVERAGE.json','INDEPENDENT_DERIVATION.md','REPORT.md','VERDICT.json','checks.py','CHECKS.json','seal.py','verify_manifest.py']
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'authored files only; raw PDFs/text/images ignored and excluded','terminal_seal_convention':'SEAL.json binds this manifest and MANIFEST_CHECKS.json; it is the terminal non-self-hashed integrity root.','files':[{'path':n,'sha256':digest(here/n),'size':(here/n).stat().st_size} for n in names]}
(here/'SEAL.json').unlink(missing_ok=True)
(here/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
run=subprocess.run([sys.executable,str(here/'verify_manifest.py')],capture_output=True,text=True)
if run.returncode:
    print(run.stdout);print(run.stderr);sys.exit(run.returncode)
(here/'MANIFEST_CHECKS.json').write_text(run.stdout)
(here/'SEAL.json').write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'binds':{'MANIFEST.json':digest(here/'MANIFEST.json'),'MANIFEST_CHECKS.json':digest(here/'MANIFEST_CHECKS.json')},'raw_sources_excluded':True},indent=2)+'\n')
print(json.dumps({'sealed_authored_files':len(names),'manifest_checks':json.loads(run.stdout)}))
