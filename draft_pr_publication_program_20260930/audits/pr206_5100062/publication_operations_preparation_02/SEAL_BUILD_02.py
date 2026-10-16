"""Preserve first seal and add a second seal for the corrected integrity verifier."""
from pathlib import Path
import datetime, hashlib, json, os, stat
D=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p):
 raw=p.read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def save(p,value):
 raw=(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444)
 fd=os.open(p.parent,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
need(not (D/'SAFE_MANIFEST_02.json').exists() and not (D/'SEAL_02.json').exists(),'Additive seal already exists')
need(pin(D/'SAFE_MANIFEST.json')==dict(bytes=12921,sha256='c528032f398b180f1c8a050c3da6bccf1092404ecfd8c0346245d63725ec98c0'),'Initial manifest changed')
need(pin(D/'SEAL.json')==dict(bytes=1958,sha256='cdbb67708d5ac66eebb0f1cc45cdf0198df8920164adb074494a27a670441166'),'Initial seal changed')
old=json.loads((D/'SAFE_MANIFEST.json').read_bytes())
for e in old['files']:need(pin(D/e['path'])=={k:e[k] for k in ('bytes','sha256')},'Initial payload changed')
sources=json.loads((D/'FINAL_SOURCE_PINS.json').read_bytes())
for n,w in sources.items():need(pin(D/n)==w,'Operational source changed')
files=[]
for p in sorted(D.rglob('*')):
 need(not p.is_symlink(),'Symlink refused')
 if p.is_file():
  need(stat.S_ISREG(p.stat().st_mode) and p.suffix not in ('.pyc','.pyo') and '__pycache__' not in p.parts,'Unsafe payload')
  if stat.S_IMODE(p.stat().st_mode)!=0o444:p.chmod(0o444)
  files.append(dict(path=p.relative_to(D).as_posix(),**pin(p)))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
save(D/'SAFE_MANIFEST_02.json',dict(schema='pr206-ops-family02-author-safe-manifest-v2',UTC=now,evidence_scope='AUTHOR_SOURCE_ONLY_NOT_ROOT_AUTHORITY',scope='Additive final packet preserving all first-seal payloads and first seal, plus exact failed integrity replay and corrected verifier.',excluded_payloads=old['excluded_payloads'],self_reference_rule='Only SAFE_MANIFEST_02.json and SEAL_02.json excluded; all first-seal artifacts retained.',files=files))
seal=json.loads((D/'SEAL.json').read_bytes())
seal.update(schema='pr206-ops-family02-author-seal-v2',UTC=now,manifest_pin=pin(D/'SAFE_MANIFEST_02.json'),payload_file_count=len(files),payload_total_bytes=sum(e['bytes'] for e in files),prior_manifest_pin=pin(D/'SAFE_MANIFEST.json'),prior_seal_pin=pin(D/'SEAL.json'),all_initial73_payloads_preserved=True,artifact_verifier_failure_preserved=True,artifact_verifier_correction='ARTIFACT_INTEGRITY_CORRECTION_01.md',corrected_verifier_pin=pin(D/'verify_artifacts_02.py'),read_only_verification=['/opt/homebrew/opt/python@3.14/bin/python3.14','-E','-S','-B','-P','verify_artifacts_02.py'])
save(D/'SEAL_02.json',seal)
print(json.dumps(dict(status='ADDITIVELY_SEALED',payload_files=len(files),manifest=pin(D/'SAFE_MANIFEST_02.json'),seal=pin(D/'SEAL_02.json')),sort_keys=True))
