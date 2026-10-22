#!/usr/bin/env python3
"""Independent corruption controls against a frozen local verifier, never the candidate."""
from pathlib import Path
import importlib.util,json,hashlib,shutil,stat,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'private/frozen_inputs/preprint_v1_0'
spec=importlib.util.spec_from_file_location('candidate_verifier',SOURCE/'verify_support.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
controls=[]
def require(c,m):
 if not c:raise RuntimeError(m)
def attempt(label,modify,method='payload',expected='reject'):
 with tempfile.TemporaryDirectory(dir=ROOT/'private',prefix='control-') as td:
  work=Path(td)/'package';shutil.copytree(SOURCE,work);mod.ROOT=work
  modify(work)
  try:
   if method=='payload':mod.verify_payload()
   elif method=='archive':mod.verify_archive(work/'pr1052_support_v1_0.zip',json.loads((work/'SUPPORT_ALLOWLIST.json').read_text())['members'])
   else:mod.verify_upload_if_present()
  except Exception as exc:actual='reject';kind=type(exc).__name__
  else:actual='accept';kind=None
  require(actual==expected,label+': unexpected '+actual)
  controls.append({'label':label,'expected':expected,'actual':actual,'exception':kind})
def modify_json(w,name,fn):
 p=w/name;data=json.loads(p.read_text());fn(data);p.write_text(json.dumps(data))
attempt('untouched payload',lambda w:None,expected='accept')
attempt('untouched archive',lambda w:None,'archive','accept')
attempt('untouched optional descriptor',lambda w:None,'upload','accept')
attempt('README byte corruption',lambda w:(w/'README.md').write_bytes((w/'README.md').read_bytes()+b'x'))
attempt('duplicate allowlist',lambda w:modify_json(w,'SUPPORT_ALLOWLIST.json',lambda d:d['members'].append(d['members'][0])))
attempt('unsafe allowlist',lambda w:modify_json(w,'SUPPORT_ALLOWLIST.json',lambda d:d['members'].append('../x')))
attempt('missing manifest entry',lambda w:modify_json(w,'SUPPORT_MANIFEST.json',lambda d:d['entries'].pop()))
def payload_symlink(w):
 raw=(w/'README.md').read_bytes();(w/'README.md').unlink();out=w.parent/'outside.txt';out.write_bytes(raw);(w/'README.md').symlink_to(out)
attempt('symlink payload',payload_symlink)
def parent_symlink(w):
 out=w.parent/'outside-support';shutil.move(w/'support',out);(w/'support').symlink_to(out,target_is_directory=True)
attempt('symlink parent escaping root',parent_symlink)
def zip_edit(w,kind):
 old=w/'pr1052_support_v1_0.zip'
 with zipfile.ZipFile(old) as z:rows=[(i,z.read(i)) for i in z.infolist()]
 if kind=='order':rows=list(reversed(rows))
 if kind=='duplicate':rows.append(rows[0])
 with zipfile.ZipFile(old,'w') as z:
  for idx,(i,data) in enumerate(rows):
   info=zipfile.ZipInfo(i.filename,i.date_time);info.create_system=3;info.external_attr=i.external_attr;info.compress_type=i.compress_type
   if idx==0:
    if kind=='mode':info.external_attr=(stat.S_IFREG|0o600)<<16
    if kind=='type':info.external_attr=(stat.S_IFLNK|0o644)<<16
    if kind=='timestamp':info.date_time=(2026,10,13,0,0,0)
    if kind=='compression':info.compress_type=zipfile.ZIP_DEFLATED
    if kind=='bytes':data+=b'x'
   z.writestr(info,data)
 Path(str(old)+'.sha256').write_text(hashlib.sha256(old.read_bytes()).hexdigest()+'  '+old.name+'\n')
for kind in ['order','duplicate','mode','type','timestamp','compression','bytes']:
 attempt('archive '+kind,lambda w,k=kind:zip_edit(w,k),'archive')
attempt('archive bad sidecar',lambda w:(w/'pr1052_support_v1_0.zip.sha256').write_text('bad'),'archive')
attempt('wrapper boolean byte length',lambda w:modify_json(w,'zenodo-deposit.json',lambda d:d['files'][0].update(bytes=True)),'upload')
attempt('wrapper metadata mismatch',lambda w:modify_json(w,'zenodo-deposit.json',lambda d:d['metadata'].update(title='other')),'upload')
attempt('wrapper array instead of object',lambda w:(w/'zenodo-deposit.json').write_text('[]'),'upload')
attempt('wrapper null file list',lambda w:modify_json(w,'zenodo-deposit.json',lambda d:d.update(files=None)),'upload')
def wrapper_symlink(w,dangling=False):
 raw=(w/'zenodo-deposit.json').read_bytes();(w/'zenodo-deposit.json').unlink();out=w.parent/'descriptor.json'
 if not dangling:out.write_bytes(raw)
 (w/'zenodo-deposit.json').symlink_to(out)
attempt('wrapper symlink follows valid bytes (observed scope)',wrapper_symlink,'upload','accept')
attempt('dangling wrapper symlink treated absent (observed scope)',lambda w:wrapper_symlink(w,True),'upload','accept')
print(json.dumps({'all_controls_as_expected':True,'controls':controls,'blocking_findings':[],'nonblocking_scope_observations':['Optional external descriptor is not itself subjected to the regular-file policy: a live symlink is parsed and a dangling symlink is treated absent. Actual supplied descriptor is regular; distribution excludes it; no hostile-local-files security guarantee is claimed.']},sort_keys=True,indent=2))
