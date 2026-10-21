#!/usr/bin/env python3
"""Fresh nonexecuting hostile packet controls using captured trusted verifier."""
import copy,hashlib,json,os,shutil,sys,types,zipfile
from pathlib import Path
R=Path(__file__).absolute().parent;root=R/'tmp/capsule';source=(root/'verify_package.py').read_bytes();m=types.ModuleType('round4_trusted_capture');m.__file__=str(root/'verify_package.py');exec(compile(source,m.__file__,'exec'),m.__dict__)
T=R/'tmp'/('capsule-boundaries-opt'if sys.flags.optimize else'capsule-boundaries-normal')
if T.exists():shutil.rmtree(T)
T.mkdir(parents=True);results=[]
def need(c,label):
 if not c:raise RuntimeError(label)
def reject(name,mutate):
 p=T/name;shutil.copytree(root,p);mutate(p)
 try:m.verify(p)
 except (ValueError,FileNotFoundError,NotADirectoryError):results.append({'name':name,'status':'REJECTED'});return
 raise RuntimeError('accepted '+name)
def rewrite(p,mut):
 d=json.loads((p/m.MANIFEST).read_bytes());mut(d);(p/m.MANIFEST).write_bytes(m.json_bytes(d))
for name,path in [('dot_path','./requirements.txt'),('double_slash','reviews//freegroup_01/controls.py'),('trailing_slash','requirements.txt/'),('dotdot_embedded','reviews/freegroup_01/../freegroup_01/controls.py'),('NUL_path','a\x00b'),('DEL_path','a\x7fb')]:
 reject(name,lambda p,path=path:rewrite(p,lambda d:d['files'][0].update(path=path)))
for name,mut in [('negative_size',lambda d:d['files'][0].update(bytes=-1)),('bool_file_count',lambda d:d.update(file_count=True)),('sha_uppercase',lambda d:d['files'][0].update(sha256=d['files'][0]['sha256'].upper())),('sha_wrong_type',lambda d:d['files'][0].update(sha256=1)),('record_extra_key',lambda d:d['files'][0].update(extra=1)),('schema_boolean',lambda d:d.update(schema=True)),('manifest_extra_top_key',lambda d:d.update(extra=True))]:reject(name,lambda p,mut=mut:rewrite(p,mut))
def mutate_source(p):
 target=p/'reviews/freegroup_01/controls.py';target.write_bytes(b"raise RuntimeError('CORRUPTED_PACKET_CODE_MUST_NEVER_EXECUTE')\n");m.rewrite_manifest(p,'reviews/freegroup_01/controls.py')
reject('rehashed_executable_frozen_by_family_capture',mutate_source)
def expanded_scope(p):
 d=json.loads((p/'CLAIM_SCOPE.json').read_bytes());d['every_degree_failure_claim']=True;(p/'CLAIM_SCOPE.json').write_bytes(m.json_bytes(d));m.rewrite_manifest(p,'CLAIM_SCOPE.json')
reject('rehashed_every_degree_expansion',expanded_scope)
def unexpected_dir(p):(p/'reviews/unknown').mkdir()
reject('nested_empty_directory',unexpected_dir)
# All positive output manifests are checked before and after; the builder is
# deliberately invoked elsewhere only against the immutable verified baseline.
need(m.verify(root)['status']=='PASS','baseline changed')
print(json.dumps({'schema':'pr681-round4-capsule-boundaries-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','count':len(results),'controls':results,'trusted_verifier_sha256':hashlib.sha256(source).hexdigest(),'corrupted_packet_code_executed':False},indent=2,sort_keys=True))
