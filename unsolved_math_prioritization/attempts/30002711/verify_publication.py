#!/usr/bin/env python3
"""Pinned portable publication replay. Finite diagnostics do not settle the target."""
import argparse, hashlib, json, os, pathlib, shutil, stat, subprocess, sys, tempfile, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
PINS={
 'author/publication/MANIFEST.json':'362a6ed1502b421e00efab914b4f02d125e7788a906f7273cb25cf074a83f177',
 'author/AUTHOR_PACKET.zip':'ae4193f1e0c8a555b5d46ec59ae3aacea615a2536d578eaf4aa9a97e0a5ee9c0',
 'independent_audit/AUDIT_MANIFEST.json':'40cacbf44a5a42a85bba9c8f5b558fd54fbabba952846bf00bd9a94ef055294c',
 'INDEPENDENT_AUDIT.zip':'6e1872fbed32079808a271f2af23abb4db8d361ae5281d84e048b0f87f1e1de9',
}
def require(ok,message):
 if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def regular(p):return stat.S_ISREG(p.lstat().st_mode)
def safe_name(name):
 p=pathlib.PurePosixPath(name)
 return bool(name) and not p.is_absolute() and '..' not in p.parts and str(p)==name and '\\' not in name

def inventory(root,pin):
 mp=root/'PUBLICATION_MANIFEST.json'
 require(regular(mp),'nonregular manifest')
 raw=mp.read_bytes();require(digest(raw)==pin,'publication pin mismatch')
 m=json.loads(raw)
 require(m['schema']=='cyclic-lifts-publication-manifest-v1' and m['problem_id']=='30002711','wrong manifest identity')
 records=m['files'];require(len(records)==26,'wrong payload count')
 require(all(safe_name(n) for n in records),'unsafe file name')
 for p in root.rglob('*'):
  require(not p.is_symlink(),'symlink forbidden')
  require(p.is_dir() or regular(p),'special file forbidden')
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 dirs={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
 require(actual==set(records)|{'PUBLICATION_MANIFEST.json'},'nonexact file inventory')
 require(dirs=={'author','author/publication','independent_audit'},'nonexact directory inventory')
 bodies={}
 for name,row in records.items():
  b=(root/name).read_bytes();require(len(b)==row['bytes'] and digest(b)==row['sha256'],'file mismatch: '+name);bodies[name]=b
 for name,expected in PINS.items():require(digest(bodies[name])==expected,'frozen pin mismatch: '+name)
 manifests={}
 for directory,manifest in [('author/publication','MANIFEST.json'),('independent_audit','AUDIT_MANIFEST.json')]:
  im=json.loads(bodies[directory+'/'+manifest]);entries=im['files'];require(len(entries)==9,'wrong inner payload count')
  require({p.name for p in (root/directory).iterdir()}==set(entries)|{manifest},'wrong inner inventory')
  for name,row in entries.items():
   require(safe_name(name) and '/' not in name,'unsafe inner name')
   b=bodies[directory+'/'+name];require(len(b)==row['bytes'] and digest(b)==row['sha256'],'inner manifest mismatch')
  manifests[directory]=im
 for name,size,directory in [('author/AUTHOR_PACKET.zip',20745,'author/publication'),('INDEPENDENT_AUDIT.zip',25207,'independent_audit')]:
  require(len(bodies[name])==size,'wrong archive size')
  with zipfile.ZipFile(root/name) as z:
   names=z.namelist();require(len(names)==len(set(names))==10,'duplicate/wrong archive members')
   require(set(names)=={p.name for p in (root/directory).iterdir()},'archive inventory mismatch')
   for info in z.infolist():
    require(not info.is_dir() and not(info.flag_bits&1),'unexpected archive member')
    require((info.external_attr>>16)&0o170000!=0o120000,'archive symlink')
    require(z.read(info.filename)==bodies[directory+'/'+info.filename],'archive member differs')
   require(z.testzip() is None,'archive CRC failure')
 binding=json.loads(bodies['independent_audit/BINDING.json'])
 require(binding['author_manifest_sha256']==PINS['author/publication/MANIFEST.json'],'wrong audit target')
 require(binding['author_manifest_bytes']==len(bodies['author/publication/MANIFEST.json']),'wrong audit manifest size')
 require(binding['bound_author_payload']==manifests['author/publication']['files'],'wrong audit payload binding')
 require(binding['author_archive']['sha256']==PINS['author/AUTHOR_PACKET.zip'] and binding['author_archive']['bytes']==20745,'wrong author archive binding')
 require(manifests['independent_audit']['author_manifest_sha256']==PINS['author/publication/MANIFEST.json'],'wrong audit manifest target')
 status=json.loads(bodies['PUBLICATION_STATUS.json']);audit=json.loads(bodies['independent_audit/AUDIT_STATUS.json'])
 require(status['queue_status']=='unsolved' and status['turns']=='5/5','wrong disposition')
 require(audit['verdict']==status['audit_verdict']=='qualified_pass_partial_mathematics','wrong audit verdict')
 report=bodies['independent_audit/AUDIT_REPORT.md'].decode()
 replacement='Let R be a complete DVR'+report.split('> Let R be a complete DVR')[1].split('\n\n')[0]
 require(status['controlling_replacement']==replacement and '> '+replacement in bodies['README.md'].decode(),'missing exact controlling correction')
 require(audit['mandatory_qualification']['required_hypothesis']=='R is complete; the action is continuous and R-linear','wrong qualification')
 for key in ['complete_solution','general_counterexample','verified_prior_complete_solution','novelty_certified','worldwide_openness_certified','human_peer_review','finite_checks_prove_unrestricted_target','live_catalogue_text_inspected','raw_ai_corpus_inspected']:
  require(status[key] is False,'unsupported evidence promotion: '+key)
 require(status['author_checks_per_mathematical_replay']==6527 and status['independent_checks_per_run']==1987,'wrong checks')
 return bodies,raw

def corruptions(root,pin):
 cases=['author_same_length_byte_flip','missing_audit_file','extra_file','extra_directory','payload_symlink','manifest_symlink','changed_publication_manifest','changed_author_manifest','changed_audit_report','changed_author_archive','changed_audit_archive','removed_controlling_qualification','self_consistent_payload_manifest_rewrite','wrong_external_pin']
 for case in cases:
  with tempfile.TemporaryDirectory(prefix='cyclic-publication-negative-') as td:
   dst=pathlib.Path(td)/'packet';shutil.copytree(root,dst);badpin=pin
   if case=='author_same_length_byte_flip':
    p=dst/'author/publication/RESULTS.md';b=p.read_bytes();p.write_bytes(b[:-1]+bytes([b[-1]^1]))
   elif case=='missing_audit_file':(dst/'independent_audit/AUDIT_STATUS.json').unlink()
   elif case=='extra_file':(dst/'extra.txt').write_text('extra')
   elif case=='extra_directory':(dst/'extra').mkdir()
   elif case=='payload_symlink':p=dst/'README.md';p.unlink();p.symlink_to(dst/'RESEARCH_LOG.md')
   elif case=='manifest_symlink':
    p=dst/'PUBLICATION_MANIFEST.json';q=dst.parent/'manifest.json';q.write_bytes(p.read_bytes());p.unlink();p.symlink_to(q)
   elif case=='changed_publication_manifest':p=dst/'PUBLICATION_MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
   elif case=='changed_author_manifest':p=dst/'author/publication/MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
   elif case=='changed_audit_report':p=dst/'independent_audit/AUDIT_REPORT.md';p.write_bytes(p.read_bytes()+b'corrupt')
   elif case=='changed_author_archive':p=dst/'author/AUTHOR_PACKET.zip';p.write_bytes(p.read_bytes()+b'x')
   elif case=='changed_audit_archive':p=dst/'INDEPENDENT_AUDIT.zip';p.write_bytes(p.read_bytes()+b'x')
   elif case=='removed_controlling_qualification':
    p=dst/'README.md';p.write_text(p.read_text().replace('complete DVR','DVR'))
   elif case=='self_consistent_payload_manifest_rewrite':
    p=dst/'README.md';p.write_bytes(p.read_bytes()+b'corrupt');q=dst/'PUBLICATION_MANIFEST.json';m=json.loads(q.read_text());m['files']['README.md']={'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())};q.write_text(json.dumps(m))
   elif case=='wrong_external_pin':badpin='0'*64
   try:inventory(dst,badpin)
   except (ValueError,OSError,KeyError,zipfile.BadZipFile):continue
   raise ValueError('accepted corruption: '+case)
 return cases

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
 require(sys.version_info>=(3,10),'Python 3.10+ required')
 require(len(a.expected_manifest)==64 and all(c in '0123456789abcdef' for c in a.expected_manifest),'invalid manifest pin')
 before,mb=inventory(ROOT,a.expected_manifest)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 outputs=[]
 for flags in ([],['-O']):
  p=subprocess.run([sys.executable,'-B',*flags,str(ROOT/'independent_audit/replay_audit.py'),str(ROOT/'author/publication')],cwd=tempfile.gettempdir(),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  require(p.returncode==0,'audit replay failed: '+p.stderr.decode())
  require(p.stdout==before['independent_audit/REPLAY_RESULTS.json'],'saved audit replay differs')
  outputs.append(p.stdout)
 require(outputs[0]==outputs[1],'normal/optimized audit replay differs')
 rejected=corruptions(ROOT,a.expected_manifest) if a.self_test else []
 after,ma=inventory(ROOT,a.expected_manifest);require(before==after and mb==ma,'original bytes changed')
 print(json.dumps({'schema':'cyclic-lifts-publication-replay-v1','problem_id':'30002711','result':'PASS_SCOPED_QUALIFIED_PARTIALS','queue_status':'unsolved','turns':'5/5','publication_manifest_sha256':a.expected_manifest,'packet_files':27,'frozen_files_and_archives_preserved':22,'author_checks_per_mathematical_replay':6527,'independent_checks_per_run':1987,'author_controls_per_wrapper':6,'independent_integrity_cases_per_audit_replay':12,'audit_replays_normal_and_optimized_byte_identical':True,'author_normal_optimized_relocated_replays_within_each_audit':True,'rejected_publication_corruptions':rejected,'exact_controlling_correction_present':True,'original_bytes_preserved':True,'complete_solution':False,'finite_checks_are_unrestricted_proof':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
