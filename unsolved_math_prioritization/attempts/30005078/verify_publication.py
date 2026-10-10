#!/usr/bin/env python3
"""Exact immutable packet inventory, scoped numerical replay and queue patch."""
import argparse,base64,hashlib,io,json,os,shutil,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SPECS=[
 ('MULTIGRADED_REGULARITY_30005078_AUTHOR_SAFE_FREEZE.zip','author',23313,'fac44aee178ad76fbeb347c1bab796ed5b877a470a4bd69ca63777886dd6012d','AUTHOR_MANIFEST.json','ac613e4ee58fa4a7fe816e6c67995742af775e09e4bab4a9aa0cf417b02e37b9',9),
 ('MULTIGRADED_REGULARITY_30005078_INDEPENDENT_AUDIT_SAFE.zip','audit',22716,'1faf2aeafdc1b1f382e8197feb72736f4376cf3934bc2e819152d684edffbc12','AUDIT_MANIFEST.json','0f54d0a84cc908db3152c522687790442fb5ee19ddb3696f1a56d01e8b88c360',12)]
HELPER_PIN='a4ed52a04300d85e9ed83059b3db4bccb93aa78a46e346630f5a1cc2cea43a85'
COUNTS={'fixed_case_fields':36,'fixed_region_degrees':3600,'fine_degree_product_cover_comparisons':2028,'singly_graded_koszul_comparisons':80,'cell_invariance_comparisons':144,'diagonal_controls':1681,'extra_module_sheaf_memberships':3840,'frontier_box_and_minimality':36,'frontier_box_wrapper_cases':24}
def require(ok,why):
 if not ok:raise ValueError(why)
def meta(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def inventory(root):
 require(not root.is_symlink(),'Symlink root');files,dirs=set(),set()
 for p in root.rglob('*'):
  n=p.relative_to(root).as_posix();require(not p.is_symlink(),'Symlink entry')
  if p.is_dir():dirs.add(n)
  else:require(p.is_file(),'Nonregular entry');files.add(n)
 return files,dirs
def expected_dirs(files):return {p.as_posix() for n in files for p in Path(n).parents if p.as_posix()!='.'}
def rows_check(root,rows,files):
 require(len(rows)==len({r['path'] for r in rows}),'Duplicate manifest entries')
 require({r['path'] for r in rows}==files,'Manifest file set')
 for r in rows:
  n=r['path'];p=Path(n);require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==n,'Unsafe path')
  require(meta((root/n).read_bytes())=={k:r[k] for k in ('bytes','sha256')},'Changed member: '+n)
def integrity(root,expected_manifest=None):
 root=Path(root);require(__debug__ and sys.flags.optimize==0,'Assertions must remain enabled; no -O or PYTHONOPTIMIZE.')
 raw=(root/'PUBLICATION_MANIFEST.json').read_bytes();pin=meta(raw)['sha256']
 if expected_manifest:require(pin==expected_manifest,'External publication manifest pin')
 manifest=json.loads(raw);rows=manifest['files'];want={r['path'] for r in rows}|{'PUBLICATION_MANIFEST.json'}
 require(inventory(root)==(want,expected_dirs(want)),'Exact recursive inventory');rows_check(root,rows,want-{'PUBLICATION_MANIFEST.json'})
 for name,folder,size,digest,mname,mpin,count in SPECS:
  frozen=root/folder;m=(frozen/mname).read_bytes();require(meta(m)['sha256']==mpin,'Frozen manifest pin')
  rows=json.loads(m)['files'];names={r['path'] for r in rows}|{mname};require(len(names)==count,'Frozen file count')
  require(inventory(frozen)==(names,expected_dirs(names)),'Frozen recursive inventory');rows_check(frozen,rows,names-{mname})
  enc=(root/'frozen_archives'/(name+'.b64')).read_bytes();data=base64.b64decode(enc.strip(),validate=True)
  require(base64.b64encode(data)+b'\n'==enc,'Canonical archive encoding');require(meta(data)=={'bytes':size,'sha256':digest},'Original ZIP identity')
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   entries=z.infolist();require(len(entries)==count and {m.filename for m in entries}==names,'ZIP exact member set');require(z.testzip() is None,'ZIP CRC')
   for member in entries:
    require(not member.is_dir() and not stat.S_ISLNK(member.external_attr>>16) and not member.flag_bits&1,'Unsafe ZIP member')
    require(z.read(member)==(frozen/member.filename).read_bytes(),'ZIP/directory byte mismatch')
 require(meta((root/'audit/frontier_box.py').read_bytes())['sha256']==HELPER_PIN,'Box helper pin')
 require(manifest['general_problem_solved'] is False and manifest['turns']=='5/5','Publication disposition')
 audit=json.loads((root/'audit/AUDIT_REPLAY.json').read_bytes());independent=json.loads((root/'audit/INDEPENDENT_RESULTS.json').read_bytes())
 require(audit['general_problem_solved'] is False and audit['proof_search_families_used']==audit['proof_search_limit']==5,'Audit disposition')
 require(independent['counts']==COUNTS and independent['invalid_inputs_rejected']==7,'Independent control counts')
 torsion=independent['characteristic_torsion_controls'];require(len(torsion)==4,'RP2 field count')
 for t,p in zip(torsion,[0,2,3,101]):
  require(t['characteristic']==p and t['regularity']==[[3 if p==2 else 2]],'RP2 regularity')
  require(t['degree_zero_local_cohomology']==([0,0,1,1,0,0,0] if p==2 else [0]*7),'RP2 torsion')
 provenance=json.loads((root/'audit/PROVENANCE_RESULTS.json').read_bytes());require(provenance['statement_and_review_hashes_match_catalog'] is True,'Completed review hash')
 source=json.loads((root/'audit/SOURCE_AUDIT.json').read_bytes());require(source['primary']['publication_date']=='2023-04-14' and source['primary']['volume_year']==2022,'Publication date distinction')
 return {'publication_manifest_sha256':pin,'packet_files':len(want)}
def queue_check(root,before,after):
 d=json.loads((root/'QUEUE_DELTA.json').read_bytes());b=Path(before).read_bytes();a=Path(after).read_bytes();require(meta(b)==d['before'] and meta(a)==d['after'],'Complete queue hashes')
 lines=b.splitlines(keepends=True);matches=[i for i,l in enumerate(lines) if b'| 30005078 / OWR-10252925-002 |' in l];require(len(matches)==1,'Exact queue target match')
 i=matches[0];fields=lines[i].split(b'|');require(fields[8:10]==[b' queued ',b' 0/5 '],'Queue old fields');fields[8]=b' unsolved ';fields[9]=b' 5/5 ';lines[i]=b'|'.join(fields)
 require(b''.join(lines)==a,'Only Status and Turns may change; preserve every other byte');return 'PASS_EXACT_FULL_BYTES'
def verify(root=ROOT,expected_manifest=None,before=None,after=None):
 root=Path(root).resolve();result=integrity(root,expected_manifest)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 with tempfile.TemporaryDirectory(prefix='regularity-publication-') as td:
  work=Path(td);audit=work/'audit';shutil.copytree(root/'audit',audit)
  archive=work/SPECS[0][0];archive.write_bytes(base64.b64decode((root/'frozen_archives'/(SPECS[0][0]+'.b64')).read_bytes()))
  p=subprocess.run([sys.executable,'-B',str(audit/'replay_audit.py'),str(archive)],cwd=work,env=env,capture_output=True,check=True)
  replay=json.loads(p.stdout);require(replay['status']=='PASS','Audit replay status')
  require(p.stdout==(root/'audit/AUDIT_REPLAY.json').read_bytes(),'Audit stdout byte-identical')
  require(replay['independent_counts']==COUNTS,'Replayed exact independent counts')
  for f in (root/'audit').iterdir():require(f.read_bytes()==(audit/f.name).read_bytes(),'Audit output changed: '+f.name)
  require(inventory(audit)==inventory(root/'audit'),'Replay extra output')
  require(meta(archive.read_bytes())=={'bytes':SPECS[0][2],'sha256':SPECS[0][3]},'Replay changed original archive')
 require((before is None)==(after is None),'Supply both queue inputs or neither');queue=queue_check(root,before,after) if before else 'NOT_RUN_EXTERNAL_QUEUE_INPUTS_REQUIRED'
 require(integrity(root,expected_manifest)==result,'Replay altered packet')
 result.update(status='PASS',problem_id='30005078',assertions_enabled=True,author_and_audit_outputs_byte_identical=True,both_frozen_archives_verified=True,helper_pin_verified=True,independent_counts=COUNTS,rp2_field_controls=4,invalid_inputs_rejected=7,disposition='unsolved',turns='5/5',queue_delta=queue,full_dataset_and_primary_source_reinspection='NOT_RUN_EXTERNAL_INPUTS_REQUIRED',hosted_ci_pass_claimed=False)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',default=str(ROOT));p.add_argument('--expected-manifest');p.add_argument('--queue-before');p.add_argument('--queue-after');a=p.parse_args()
 print(json.dumps(verify(a.root,a.expected_manifest,a.queue_before,a.queue_after),indent=2,sort_keys=True))
