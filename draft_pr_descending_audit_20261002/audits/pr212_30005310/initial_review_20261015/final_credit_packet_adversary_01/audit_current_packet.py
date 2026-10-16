#!/usr/bin/env python3
"""Read-only packet/source binding; isolated replay writes only below this audit."""
from pathlib import Path, PurePosixPath
import ast, hashlib, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
A=Path(__file__).resolve().parent
D=A.parent
C=D/'corrected_packet'
P=A/'private'/'current_packet_replay'
H=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
manifest=read(D/'PROPOSED_CURRENT_PACKET_MANIFEST.json')
plan=read(D/'PROPOSED_NATIVE_CHANGES.json')
intake=read(D/'INTAKE.json')
rows=manifest['files']
assert H((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes())=='7a85e7988166e1058cf8eb1116344058feb9c76e1a8c19950a1083d8c4f04111'
assert H((D/'PROPOSED_NATIVE_CHANGES.json').read_bytes())=='e251d163fb730872a13165ea6c1e1c469c44932734099addf9a90b4b15db9210'
assert plan['packet_manifest_sha256']==H((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes())
assert len(rows)==35==plan['planned_source_files']
seen=set()
for r in rows:
 rel=PurePosixPath(r['path'])
 assert not rel.is_absolute() and '..' not in rel.parts and rel.as_posix()==r['path']
 assert r['path'] not in seen
 seen.add(r['path'])
 f=C/r['path'];assert f.resolve().is_relative_to(C.resolve()) and not f.is_symlink()
 b=f.read_bytes();assert len(b)==r['bytes'] and H(b)==r['sha256']
 assert f.suffix in ('.md','.json','.py')
assert seen=={f.relative_to(C).as_posix() for f in C.rglob('*') if f.is_file()}
archives=[]
prefix=intake['native_source_prefix']
for r in intake['original_source_files']:
 rel=r['native_path'].removeprefix(prefix)
 p=C/'original_submission'/rel
 b=p.read_bytes()
 assert len(b)==r['bytes'] and H(b)==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['native_blob']
 archives.append(rel)
assert len(archives)==20==manifest['archive_files']==plan['original_archive_files']
assert {'original_submission/'+r for r in archives}=={x for x in seen if x.startswith('original_submission/')}
core=lambda b:b.split(b'## 2. Model, statistics and sample convention',1)[1].split(b'## 8.',1)[0]
co=core((C/'PROOF.md').read_bytes())
assert co==core((C/'original_submission/PROOF.md').read_bytes())
assert H(co)==manifest['mathematical_core_sha256']
assert (C/'verify.py').read_bytes()==(C/'original_submission/verify.py').read_bytes()
assert (C/'source_record.json').read_bytes()==(C/'original_submission/source_record.json').read_bytes()
manifest_checks=[]
for root,names in [(C,['MANIFEST.json','PUBLICATION_MANIFEST.json']),(C/'original_submission',['MANIFEST.json','PUBLICATION_MANIFEST.json']),(C/'original_submission/independent_review',['REVIEW_MANIFEST.json'])]:
 for name in names:
  m=read(root/name)
  rr=m['files'] if 'files' in m else [{'path':k,'sha256':v} for k,v in m.items()]
  for r in rr:
   rel=PurePosixPath(r['path']);assert not rel.is_absolute() and '..' not in rel.parts
   f=root/r['path'];assert f.resolve().is_relative_to(root.resolve()) and not f.is_symlink()
   b=f.read_bytes();assert H(b)==r['sha256']
   if 'bytes' in r:assert len(b)==r['bytes']
  manifest_checks.append({'path':(root/name).relative_to(C).as_posix(),'entries':len(rr)})
old=plan['old_row'].split('|');new=plan['new_row'].split('|')
assert len(old)==len(new)
assert old[8].strip()=='claimed_solved' and new[8].strip()=='already_solved'
assert old[9].strip()==new[9].strip()=='1/5'
assert [i for i,(x,y) in enumerate(zip(old,new)) if x!=y]==[8,11]
assert plan['old_row']==intake['queue_row']
assert plan['original_head']==intake['head']==manifest['original_head']
assert plan['native_mutations_performed'] is False
sources=[]
source_names={'owr2022.pdf':'owr2022_55.pdf','rigidity.pdf':'rigidity_v3.pdf','blekherman_sinn.pdf':'blekherman_sinn_v2.pdf'}
for r in read(C/'source_manifest.json')['sources']:
 p=D/'private_reading'/source_names.get(r['file'],r['file'])
 b=p.read_bytes();assert H(b)==r['sha256']
 if 'bytes' in r:assert len(b)==r['bytes']
 sources.append({'name':r['file'],'bytes':len(b),'sha256':H(b)})
# Current and historical programs inspected before these copies are executed.
assert not P.exists()
shutil.copytree(C,P)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
replays=[]
for name,program,output in [('current_author','verify.py','verification.json'),('original_author','original_submission/verify.py','original_submission/verification.json'),('original_independent','original_submission/independent_review/independent_check.py','original_submission/independent_review/INDEPENDENT_CHECKS.json')]:
 before=(P/output).read_bytes()
 run=subprocess.run([sys.executable,str(P/program)],cwd=P,env=env,capture_output=True,timeout=120)
 (A/'private'/f'current_revision_{name}.stdout.txt').write_bytes(run.stdout)
 (A/'private'/f'current_revision_{name}.stderr.txt').write_bytes(run.stderr)
 assert run.returncode==0,(name,run.stderr)
 after=(P/output).read_bytes();assert after==before
 result=json.loads(after)
 replays.append({'name':name,'exit_code':run.returncode,'byte_identical_receipt':True,'assertions':result['assertions'],'receipt_sha256':H(after),'program_sha256':H((P/program).read_bytes())})
assert all(H((P/r['path']).read_bytes())==r['sha256'] for r in rows)
# Current author receipt differs only by the dynamically evaluated adjacent proof hash.
x=read(C/'verification.json');y=read(C/'original_submission/verification.json')
assert x.pop('proof_sha256')==H((C/'PROOF.md').read_bytes())
assert y.pop('proof_sha256')==H((C/'original_submission/PROOF.md').read_bytes())
assert x==y
helper=D/'apply_credited_correction.py'
ast.parse(helper.read_text())
assert 'CLASSIFICATION_REPAIR_REQUEST.json' in helper.read_text()
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','payload_files':35,'archive_files':20,'all_payloads_exact':True,'safe_paths_and_no_symlinks':True,'core_sections_2_7_unchanged':True,'core_sha256':H(co),'core_bytes':len(co),'manifest_checks':manifest_checks,'source_pins_verified':sources,'isolated_replays':replays,'all_35_copied_bytes_unchanged_after_reproduction':True,'native_row_changed_columns':[8,11],'author_counter':'1/5 preserved','provider_or_Git_mutations':0,'packet_manifest_sha256':H((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes()),'native_plan_sha256':H((D/'PROPOSED_NATIVE_CHANGES.json').read_bytes()),'helper_sha256_reviewed':H(helper.read_bytes()),'python':sys.version,'sympy':__import__('sympy').__version__}
(A/'CURRENT_PACKET_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
