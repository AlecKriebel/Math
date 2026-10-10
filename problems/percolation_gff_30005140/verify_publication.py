#!/usr/bin/env python3
"""Read-only packet integrity and portable exact finite replay; standard library only."""
import argparse,base64,hashlib,io,json,os,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
SPECS=[('PERCOLATION_GFF_30005140_AUTHOR_SAFE_FREEZE.zip', 'author', 'percolation_gff_30005140', 23503, 'c3f8c9d1de2e3ff41b40a70de3cde559ff534de22b641d81a0db6db86d71f3f1', 'MANIFEST.json', '893d076a0508af3f02cbed181cc5ad4349446f6e6e883c66f8bc415b8d7f6ad7', 11), ('PERCOLATION_GFF_30005140_INDEPENDENT_AUDIT_SAFE.zip', 'audit', 'percolation_gff_30005140_independent_audit', 48473, 'b5897372bf180c4d8ccb5d01bfeafc3d17645abcd0ee93c487ff2dbc8958b397', 'MANIFEST.json', '024101535a5cb26831433c79a1e2d606ccf91c846ef268b4cd228552e912a246', 25)]
def require(ok,label):
 if not ok: raise ValueError(label)
def meta(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def expected_dirs(files): return {p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix()!='.'}
def inventory(root):
 require(not root.is_symlink(),'Symlink root')
 files,dirs=set(),set()
 for p in root.rglob('*'):
  n=p.relative_to(root).as_posix();require(not p.is_symlink(),'Symlink entry')
  if p.is_dir(): dirs.add(n)
  else: require(p.is_file(),'Nonregular entry');files.add(n)
 return files,dirs
def rows_check(root,rows,files):
 require(len(rows)==len({r['path'] for r in rows}),'Duplicate manifest entry')
 require({r['path'] for r in rows}==files,'Manifest file set')
 for r in rows:
  p=PurePosixPath(r['path']);require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==r['path'],'Unsafe manifest path')
  require(meta((root/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')},'Changed member: '+r['path'])
def integrity(root,expected_manifest=None):
 root=Path(root);require(__debug__ and sys.flags.optimize==0,'Assertions must remain enabled; no -O or PYTHONOPTIMIZE')
 raw=(root/'PUBLICATION_MANIFEST.json').read_bytes();pin=meta(raw)['sha256']
 if expected_manifest: require(pin==expected_manifest,'External publication manifest pin')
 rows=json.loads(raw)['files'];want={r['path'] for r in rows}|{'PUBLICATION_MANIFEST.json'}
 require(inventory(root)==(want,expected_dirs(want)),'Exact recursive inventory')
 rows_check(root,rows,want-{'PUBLICATION_MANIFEST.json'})
 for name,folder,prefix,size,digest,mname,mpin,count in SPECS:
  frozen=root/folder;m=(frozen/mname).read_bytes();require(meta(m)['sha256']==mpin,'Frozen manifest pin')
  rows=json.loads(m)['files'];names={r['path'] for r in rows}|{mname}
  require(len(names)==count and inventory(frozen)==(names,expected_dirs(names)),'Frozen recursive inventory')
  rows_check(frozen,rows,names-{mname})
  enc=(root/'frozen_archives'/(name+'.b64')).read_bytes();data=base64.b64decode(enc.strip(),validate=True)
  require(base64.b64encode(data)+b'\n'==enc,'Canonical archive encoding');require(meta(data)=={'bytes':size,'sha256':digest},'Original ZIP identity')
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   entries=z.infolist();expected={prefix+'/'+n for n in names}
   require(len(entries)==count and {m.filename for m in entries}==expected,'ZIP exact member set');require(z.testzip() is None,'ZIP CRC')
   for member in entries:
    p=PurePosixPath(member.filename)
    require(len(p.parts)>=2 and p.parts[0]==prefix and '..' not in p.parts and not p.is_absolute(),'Unsafe ZIP path')
    require(not member.is_dir() and not stat.S_ISLNK(member.external_attr>>16) and not member.flag_bits&1,'Unsafe ZIP member')
    require(z.read(member)==(frozen/Path(*p.parts[1:])).read_bytes(),'ZIP/directory byte mismatch')
 require((root/'CORRECTIONS_AND_CLARIFICATIONS.md').read_bytes()==(root/'audit/CORRECTIONS_AND_CLARIFICATIONS.md').read_bytes(),'Source corrections addendum changed')
 return {'publication_manifest_sha256':pin,'packet_files':len(want)}
def run(script,*args):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 return subprocess.check_output([sys.executable,'-B',str(script),*map(str,args)],env=env,timeout=120)
def queue_check(root,before,after):
 d=json.loads((root/'QUEUE_DELTA.json').read_bytes());b=Path(before).read_bytes();a=Path(after).read_bytes()
 require(meta(b)==d['before'] and meta(a)==d['after'],'Complete queue hashes')
 lines=b.splitlines(keepends=True);matches=[i for i,l in enumerate(lines) if b'| 30005140 / OWR-10252936-003 |' in l];require(len(matches)==1,'Exact queue target match')
 i=matches[0];fields=lines[i].split(b'|');require(fields[8:10]==[b' queued ',b' 0/5 '],'Queue old fields')
 fields[8:10]=[b' unsolved ',b' 5/5 '];lines[i]=b'|'.join(fields)
 require(b''.join(lines)==a,'Only Status and Turns may change; preserve every other byte')
 return 'PASS_EXACT_FULL_BYTES'
def verify(root=ROOT,expected_manifest=None,before=None,after=None):
 root=Path(root).resolve();result=integrity(root,expected_manifest)
 ar=json.loads(run(root/'author/verify.py'));am=json.loads(run(root/'author/verify_manifest.py'))
 saved=json.loads((root/'audit/results/author_replay.json').read_bytes())
 require(ar==saved['verify.py'] and am==saved['verify_manifest.py'],'Complete saved author replay equality')
 require(ar['assertions_passed']==168 and ar['results_match'] and am['files_checked']==10,'Author assertion and manifest counts')
 require(json.loads(run(root/'audit/author/verify.py'))==ar,'Audit embedded-author replay equality')
 require(json.loads(run(root/'audit/author/verify_manifest.py'))==am,'Audit embedded-author manifest equality')
 for p in (root/'author').rglob('*'):
  if p.is_file(): require(p.read_bytes()==(root/'audit/author'/p.relative_to(root/'author')).read_bytes(),'Embedded author byte equality')
 audit_manifest=json.loads(run(root/'audit/code/verify_manifest.py'))
 require(audit_manifest['status']=='PASS' and audit_manifest['files_checked']==24,'Frozen audit manifest replay')
 im=json.loads(run(root/'audit/code/independent_math.py'))
 require(im=={'status':'PASS','assertions_passed':15108,'graph_patterns':4096,'results_match':True},'Complete independent replay summary')
 saved_im=json.loads((root/'audit/results/independent_math.json').read_bytes())
 require(saved_im['assertions_passed']==15108 and sum(saved_im['checks_by_category'].values())==15108 and saved_im['graph_counts']['patterns']==4096,'Independent assertion accounting')
 with tempfile.TemporaryDirectory(prefix='percolation-publication-') as tmp:
  name=SPECS[0][0];p=Path(tmp)/name;p.write_bytes(base64.b64decode((root/'frozen_archives'/(name+'.b64')).read_bytes(),validate=False))
  identity=json.loads(run(root/'audit/code/verify_inputs.py','--author-zip',p))
 require(identity['status']=='PASS' and identity['checks']=={'author_zip':'PASS'},'Frozen author ZIP input binding')
 status=json.loads((root/'audit/STATUS.json').read_bytes())
 require(status['full_problem_status']=='UNSOLVED_IN_THIS_INVESTIGATION' and status['approaches_used']==5 and status['approach_limit']==5 and not status['full_problem_resolved'],'Original target status')
 require(status['independent_audit_status']=='PASS_SCOPED_PARTIALS' and not status['sixth_research_approach_attempted'] and not status['novelty_claim'] and not status['editorial_readiness_claim'],'Qualified audit status')
 require((before is None)==(after is None),'Supply both queue inputs or neither')
 queue=queue_check(root,before,after) if before else 'NOT_RUN_EXTERNAL_QUEUE_INPUTS_REQUIRED'
 require(integrity(root,expected_manifest)==result,'Replay altered packet')
 result.update(status='PASS',problem_id='30005140',assertions_enabled=True,author_assertions=168,independent_assertions=15108,exhaustive_finite_box_patterns=4096,complete_result_equality=True,both_frozen_archives_verified=True,all_frozen_author_copies_byte_identical=True,audit_clarifications_verified=True,original_target='UNSOLVED',approaches_used='5/5',queue_delta=queue,external_source_metadata_replay='NOT_RUN_BY_THIS_COMMAND_EXTERNAL_INPUTS_REQUIRED',finite_checks_are_formal_proof=False,hosted_ci_pass_claimed=False)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',default=str(ROOT));p.add_argument('--expected-manifest');p.add_argument('--queue-before');p.add_argument('--queue-after');a=p.parse_args()
 print(json.dumps(verify(a.root,a.expected_manifest,a.queue_before,a.queue_after),indent=2,sort_keys=True))
