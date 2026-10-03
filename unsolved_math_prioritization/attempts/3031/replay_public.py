#!/usr/bin/env python3
"""Portable public replay; explicitly account for the omitted administrative file."""
import hashlib,json,pathlib,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent

def check(path,record):
 data=path.read_bytes()
 assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'],str(path)

def integrity():
 distribution=json.loads((HERE/'PUBLIC_DISTRIBUTION_MANIFEST.json').read_text())
 for r in distribution['files']:check(HERE/r['path'],r)
 scope=json.loads((HERE/'PUBLICATION_SCOPE.json').read_text())
 omitted={r['path']:r for r in scope['distribution_omissions']}
 for sub in ['packet','review']:
  manifest=json.loads((HERE/sub/'MANIFEST.json').read_text());count=0
  for r in manifest['files']:
   relative=sub+'/'+r['path']
   if relative in omitted:
    assert not (HERE/relative).exists()
    assert omitted[relative]['sha256']==r['sha256']
   else:check(HERE/relative,r);count+=1
  print(f'{sub}: {count} distributed frozen entries verified.')
 assert set(omitted)=={'packet/SOURCE_GATE.md'}
 print('One omitted administrative entry is accounted for by identity only, not reverified from unavailable bytes.')

integrity()
subprocess.run(['sh','replay_all.sh'],cwd=HERE/'packet',check=True)
subprocess.run(['sh','replay_review.sh'],cwd=HERE/'review',check=True)
for relative,wanted in [('packet/rooted_c112_m43.json',0),('packet/failed_extension_c113_m43.json',1),('review/invalid_upper_float.json',2)]:
 p=subprocess.run([sys.executable,str(HERE/'review/rooted_verify_strict.py'),str(HERE/relative),'--full-spectrum'],capture_output=True,text=True)
 assert p.returncode==wanted,(relative,p.returncode,p.stderr)
integrity()
print('Public replay PASS. Original conjecture remains unsolved, exhausted 5/5; novelty unverified.')
