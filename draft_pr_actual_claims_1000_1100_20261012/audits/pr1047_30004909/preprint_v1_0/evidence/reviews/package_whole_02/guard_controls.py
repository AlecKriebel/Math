#!/usr/bin/env python3
from pathlib import Path
import json,shutil,subprocess,datetime,hashlib,zipfile,stat
OUT=Path(__file__).resolve().parent
BASE=OUT/'clean_extraction';FAULT=OUT/'fault_controls';FAULT.mkdir(exist_ok=True)
def run(root,script):
 p=subprocess.run(['python3','-I','-B','scripts/'+script],cwd=root,capture_output=True,text=True)
 return {'command':['python3','-I','-B','scripts/'+script],'actual_exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def clone(name):
 root=FAULT/name;shutil.copytree(BASE,root);return root
def load(root,file):return json.loads((root/file).read_text())
def save(root,file,data):(root/file).write_text(json.dumps(data,indent=2)+'\n')
rows=[]
def verify_fault(name,mutate,rebuild=False):
 root=clone(name);mutate(root)
 if rebuild:require=run(root,'build_supportkit.py');assert require['actual_exit']==0,require
 result=run(root,'verify_package.py');assert result['actual_exit']!=0,name
 rows.append({'name':name,'rebuilt_manifest_before_check':rebuild,'expected_rejection':True,**result})
def builder_fault(name,mutate):
 root=clone(name);mutate(root);result=run(root,'build_supportkit.py');assert result['actual_exit']!=0,name
 rows.append({'name':name,'expected_rejection':True,**result})
def alter(root,file,key,value):
 d=load(root,file);d[key]=value;save(root,file,d)
verify_fault('payload_corrupt',lambda r:(r/'LICENSE.md').write_text('corrupt\n'))
verify_fault('metadata_bare_wrapper',lambda r:save(r,'zenodo_metadata.json',load(r,'zenodo_metadata.json')['metadata']),True)
verify_fault('metadata_equivalence',lambda r:alter(r,'.zenodo.json','title','Different title'),True)
verify_fault('publication_state_true',lambda r:alter(r,'CURRENT_REVIEW_STATE.json','publication_ready',True),True)
verify_fault('checker_scope_changed',lambda r:(r/'scripts/check_mathematics.py').write_text((r/'scripts/check_mathematics.py').read_text().replace('range(1,201)','range(1,11)')),True)
verify_fault('original_body_changed',lambda r:(r/'evidence/submitted/REPORT.md').write_text('not the exact original proof\n'),True)
def duplicate_copy(r):
 d=load(r,'EVIDENCE_COPY_MAP.json');d['copies'].append(d['copies'][0]);save(r,'EVIDENCE_COPY_MAP.json',d)
verify_fault('duplicate_evidence_path',duplicate_copy,True)
def bad_members(r):
 d=load(r,'MANIFEST.json');d['members']=sorted(d['members']);save(r,'MANIFEST.json',d)
# Sorting manifest members changes the exact declared append convention and should be rejected;
# ordinary unsorted append of MANIFEST.json is correct, independently of ZIP sort order.
verify_fault('manifest_convention_changed',bad_members)
def extra_allow(r,name):
 d=load(r,'ALLOWLIST.json');d['members']=sorted(d['members']+[name]);save(r,'ALLOWLIST.json',d)
builder_fault('absolute_path',lambda r:extra_allow(r,'/absolute.txt'))
builder_fault('traversal_path',lambda r:extra_allow(r,'../outside.txt'))
builder_fault('circular_manifest',lambda r:extra_allow(r,'MANIFEST.json'))
builder_fault('zip_member',lambda r:extra_allow(r,'extra.zip'))
def leaf_link(r):
 p=r/'LICENSE.md';p.unlink();p.symlink_to(r/'README.md')
builder_fault('symlink_leaf',leaf_link)
def ancestor_link(r):
 shutil.move(str(r/'paper'),str(r/'paper_original'));(r/'paper').symlink_to(r/'paper_original',target_is_directory=True)
builder_fault('symlink_ancestor',ancestor_link)
def dir_member(r):
 (r/'extra_directory').mkdir();extra_allow(r,'extra_directory')
builder_fault('directory_member',dir_member)
# An extra local reproduction artifact must not enter the explicit allowlist ZIP.
r=clone('unlisted_file_excluded');(r/'unlisted_file.txt').write_text('local review output\n');positive=run(r,'build_supportkit.py');assert positive['actual_exit']==0
assert (r/'pr1047_supportkit_v1.0.zip').read_bytes()==(OUT/'frozen/preprint_v1_0/pr1047_supportkit_v1.0.zip').read_bytes()
rows.append({'name':'unlisted_file_excluded','expected_rejection':False,'byte_identical_archive':True,**positive})
# Independently reproduce ZIP storage from the checked manifest, without executing supplied builder.
with zipfile.ZipFile(OUT/'independently_rebuilt.zip','w',compression=zipfile.ZIP_STORED) as z:
 names=load(BASE,'ALLOWLIST.json')['members']
 for name in sorted(names+['MANIFEST.json']):
  i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_STORED
  z.writestr(i,(BASE/name).read_bytes())
assert (OUT/'independently_rebuilt.zip').read_bytes()==(OUT/'frozen/preprint_v1_0/pr1047_supportkit_v1.0.zip').read_bytes()
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','negative_controls_rejected':len(rows)-1,'positive_control':True,'independent_zip_byte_equal':True,'controls':rows,'scope':'all mutations occur only in reviewer-owned copies'}
(OUT/'GUARD_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='controls'},indent=2))
