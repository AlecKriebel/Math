#!/usr/bin/env python3
"""Non-destructive packet tamper controls; all mutation is in temporary copies."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
if sys.flags.optimize:raise SystemExit('Optimized Python is unsupported')
root=Path(__file__).resolve().parent;anchor=hashlib.sha256((root/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest();results={}
with tempfile.TemporaryDirectory(prefix='hairs-publication-tamper-') as td:
 def case(name,change=None,flags=(),success=False):
  p=Path(td)/name;shutil.copytree(root,p)
  if change:change(p)
  r=subprocess.run([sys.executable,*flags,'-B',str(p/'verify_publication.py'),'--expected-manifest',anchor,'--integrity-only'],capture_output=True,timeout=120)
  if (r.returncode==0)!=success:raise RuntimeError('Unexpected result '+name)
  results[name]='PASS_ACCEPTED' if success else 'PASS_REJECTED'
 case('relocated',success=True)
 case('changed_proof',lambda p:(p/'author_v2/REPORT.md').write_text('altered'))
 case('missing_result',lambda p:(p/'v2_acceptance/ACCEPTANCE.json').unlink())
 case('extra_file',lambda p:(p/'extra').write_text('extra'))
 case('extra_directory',lambda p:(p/'empty').mkdir())
 case('symlink',lambda p:(p/'link').symlink_to(p/'README.md'))
 case('changed_archive',lambda p:(p/'frozen_archives/EXPONENTIAL_PARAMETER_HAIRS_5300062_AUTHOR_V2_SAFE_FREEZE.zip.b64').write_text('corrupt'))
 def coherent(p):
  (p/'README.md').write_text('altered');m=json.loads((p/'PUBLICATION_MANIFEST.json').read_bytes())
  for r in m['files']:
   b=(p/r['path']).read_bytes();r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
 case('coherent_rewrite_external_anchor',coherent)
 case('optimized_O',flags=('-O',));case('optimized_OO',flags=('-OO',))
print(json.dumps({'result':'PASS_PUBLICATION_INTEGRITY_CONTROLS','cases':results,'source_packet_modified':False},indent=2,sort_keys=True))
