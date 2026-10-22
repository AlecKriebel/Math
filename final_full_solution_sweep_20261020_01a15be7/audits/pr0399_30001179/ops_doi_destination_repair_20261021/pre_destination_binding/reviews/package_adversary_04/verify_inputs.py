#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,subprocess,zipfile,sys
R=Path(__file__).resolve().parent;A=R.parents[1];ROOT=A.parents[1];REPO=ROOT.parent;P=ROOT/'private/pr0399_package04'
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();OUTPUT=R/'INPUT_VERIFICATION.json'
if args.output is not None:
 if not args.output.is_absolute() or not args.output.is_relative_to(ROOT/'private') or args.output.exists():raise RuntimeError('New private output path required')
 args.output.parent.mkdir(parents=True,exist_ok=True);OUTPUT=args.output
def sha(b):return hashlib.sha256(b).hexdigest()
def check(root, entries):
 seen=set()
 for e in entries:
  n=e['path'];q=PurePosixPath(n)
  if n in seen or q.is_absolute() or any(v in ('','.','..') for v in n.split('/')) or '\\' in n:raise RuntimeError('unsafe '+n)
  p=root/n
  if p.is_symlink() or any(v.is_symlink() for v in p.parents):raise RuntimeError('symlink')
  b=p.read_bytes()
  if len(b)!=e['bytes'] or sha(b)!=e['sha256']:raise RuntimeError('binding '+str(p))
  seen.add(n)
 return len(seen)
def git(*args):
 return subprocess.check_output(['git',*args],cwd=REPO,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
H=A/'ops_record_url_repair_20261021';O=H/'pre_record_url_binding';summary={}
m=json.loads((H/'MANIFEST.json').read_bytes())
if sha((H/'MANIFEST.json').read_bytes())!='151a3c3c1dffa10750fad0ba8fdb189ba27698c30c3d0d2c000c98dbc48e732b':raise RuntimeError('new manifest')
summary['new356']=check(A,m['files']);summary['new_immutable']=check(A,m['immutable_inputs'])
old=json.loads((O/'ops_identity_repair_20261021/MANIFEST.json').read_bytes());summary['old156']=check(O,old['files'])
orig=json.loads((O/'publication_operations_preparation/MANIFEST.json').read_bytes());nested=O/'ops_identity_repair_20261021/pre_review02_binding';summary['old42plus26']=check(nested,orig['files']+orig['immutable_inputs'])
summary['supplemental64_current']=check(A,json.loads((H/'SUPPLEMENTAL_PRESERVATION.json').read_bytes())['files']);summary['supplemental64_old']=check(O,json.loads((H/'SUPPLEMENTAL_PRESERVATION.json').read_bytes())['files'])
summary['preparer108']=check(A,json.loads((A/'publication_support/PREPARER_FILE_MANIFEST.json').read_bytes())['files'])
for family in ['measure_ordinal','continuity_core','priority_source','package_adversary_01','package_adversary_02','package_adversary_03']:
 d=A/'reviews'/family;v=json.loads((d/'AUTHORED_FILE_MANIFEST.json').read_bytes());summary[family]=check(d,v['files'])
 if (d/'AUTHORED_FILE_MANIFEST.sha256').read_text().split()[0]!=sha((d/'AUTHORED_FILE_MANIFEST.json').read_bytes()):raise RuntimeError('checksum '+family)
snapshot=json.loads((A/'SOURCE_SNAPSHOT.json').read_bytes());head=snapshot['head'];parent=snapshot['comparison_base']
if git('show','-s','--format=%P',head).decode().strip()!=parent:raise RuntimeError('parent')
for e in snapshot['files']:
 b=(A/e['snapshot']).read_bytes()
 if b!=git('show',head+':'+e['repository_path']) or len(b)!=e['bytes'] or sha(b)!=e['sha256']:raise RuntimeError('original')
 if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=e['git_blob']:raise RuntimeError('blob')
summary['original11_actual_git']=len(snapshot['files'])
q='unsolved_math_prioritization/QUEUE.md';rows={}
for commit in [parent,head]:
 row=[s for s in git('show',commit+':'+q).decode().splitlines() if '| 30001179 / OWR-3392-005 |' in s]
 if len(row)!=1:raise RuntimeError('queue')
 rows[commit]=row[0]
summary['queue_rows']=rows
pub=A/'preprint/publication';release=json.loads((pub/'RELEASE_FILES.json').read_bytes());summary['release5']=check(pub,release['files'])
z=zipfile.ZipFile(pub/'free-product-tensor-core-verification.zip');names=z.namelist()
if len(names)!=82 or len(set(names))!=82 or z.testzip():raise RuntimeError('archive')
prefix='free-product-tensor-core-verification/';listing=json.loads(z.read(prefix+'FILES.json'))
if len(listing['files'])!=81 or set(names)!={prefix+'FILES.json'}|{prefix+e['path'] for e in listing['files']}:raise RuntimeError('archive inventory')
for e in listing['files']:
 b=z.read(prefix+e['path'])
 if sha(b)!=e['sha256'] or len(b)!=e['bytes']:raise RuntimeError('archive binding')
for e in snapshot['files']:
 if z.read(prefix+e['snapshot'])!=(A/e['snapshot']).read_bytes():raise RuntimeError('archive original')
if z.read(prefix+'manuscript/main.tex')!=(pub/'free-product-tensor-core.tex').read_bytes():raise RuntimeError('TeX')
if not (P/'archive').exists():z.extractall(P/'archive')
summary.update(archive_payloads=81,archive_originals=11,source_tex_identical=True,root_reconciliation_sha256=sha((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes()),publication_clearance_exists=(A/'ROOT_PUBLICATION_CLEARANCE.json').exists())
OUTPUT.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
