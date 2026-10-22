"""PR210 finite native custody verification; standard library, no network/code runs.
Run: python3 -E -S -B -P /absolute/path/verify_native_custody_offline.py
Add --full to check all67 direct original/revised custody bodies. Default verifies
original20 from the existing published ZIP and the explicit finite public bodies.
This does not verify mathematics, priority, external publication or whole QUEUE.
"""
from pathlib import Path
import argparse,hashlib,json,stat,zipfile
BASE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true');args=parser.parse_args()
def check(ok,msg):
 if not ok:raise RuntimeError(msg)
def load(name):return json.loads((BASE/name).read_bytes())
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def body(name,wanted,kind=None,oid=None):
 p=BASE/name;check(p.resolve()==p and p.is_file() and not p.is_symlink() and stat.S_ISREG(p.stat().st_mode) and stat.S_IMODE(p.stat().st_mode)==0o444,'Canonical 0444 body '+name);raw=p.read_bytes();check(pin(raw)=={k:wanted[k] for k in ('bytes','sha256')},'Byte identity '+name)
 if kind:check(native(kind,raw)==oid,'Native identity '+name)
 return raw
treefile=load('AUTHENTICATED_NATIVE_TREES.json');trees={}
for oid,rows in treefile['trees'].items():
 check(rows==sorted(rows,key=lambda r:r['name'].encode()+(b'/' if r['mode']=='040000' else b'')) and len({r['name'] for r in rows})==len(rows),'Tree ordering/duplicate names')
 for r in rows:check((r['mode'],r['type']) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')),'Native mode/type')
 raw=b''.join((r['mode'].lstrip('0')+' '+r['name']).encode()+b'\0'+bytes.fromhex(r['sha']) for r in rows);check(native('tree',raw)==oid,'Native tree SHA')
 trees[oid]={r['name']:{'mode':r['mode'],'type':r['type'],'git_object':r['sha']} for r in rows}
def lookup(root,path):
 for name in path.split('/'):
  r=trees[root].get(name)
  if r is None:return None
  root=r['git_object']
 return r
inventories={}
for label in ('ORIGINAL','REVISED','MERGE','CURRENT_MAIN'):
 inv=load(label+'_NATIVE_INVENTORY.json');inventories[label]=inv;check(inv['leaf_count']==len(inv['leaves']),'Inventory leaf count')
 for r in inv['leaves']:check(lookup(inv['root_tree'],r['path'])=={'mode':r['mode'],'type':r['type'],'git_object':r['git_object']},'Inventory/root association')
for label in ('MERGE','CURRENT_MAIN'):check(inventories[label]['attempt_entry']==inventories['REVISED']['attempt_entry'],'Own native tree drift')
commits=load('EXACT_NATIVE_COMMIT_BODIES.json')
for row in commits['records']:
 raw=body(row['archival_path'],row,'commit',row['sha']);head=raw.split(b'\n\n',1)[0].decode().splitlines();check(head[0]=='tree '+row['tree'],'Commit/tree association');check([x[7:] for x in head if x.startswith('parent ')]==row['parents'],'Commit parents')
snap=load('NATIVE_SNAPSHOTS.json');bycommit={r['sha']:r for r in commits['records']}
for name in ('original_native_commit','revised_native_commit','actual_merge_native_commit','MAIN_native_commit','actual_merge_first_parent_native_commit'):
 j=snap[name];check(bycommit[j['sha']]['tree']==j['tree']['sha'] and bycommit[j['sha']]['parents']==[p['sha'] for p in j['parents']],'Captured commit association')
delta=load('ACTUAL_MERGE_COMPLETE_NATIVE_DELTA.json');leaves={};added={};deleted={}
def compare(a,b,prefix='',depth=0):
 check(depth<=64,'Depth bound')
 if a==b:return
 left=trees[a] if a else {};right=trees[b] if b else {}
 for name in sorted(set(left)|set(right)):
  x=left.get(name);y=right.get(name)
  if x==y:continue
  path=prefix+name;xt=x is not None and x['type']=='tree';yt=y is not None and y['type']=='tree';change={'before':x,'after':y}
  if xt and yt:compare(x['git_object'],y['git_object'],path+'/',depth+1)
  else:
   if xt:deleted[path]=change;compare(x['git_object'],None,path+'/',depth+1)
   if yt:added[path]=change;compare(None,y['git_object'],path+'/',depth+1)
   if (x is not None and not xt) or (y is not None and not yt):leaves[path]=change
compare(delta['before_tree'],delta['after_tree'])
for field,actual in [('leaf_changes',leaves),('added_directories',added),('deleted_directories',deleted)]:
 claimed={r['path']:{k:v for k,v in r.items() if k!='path'} for r in delta[field]};check(len(claimed)==len(delta[field]) and claimed==actual,'Complete merge native delta '+field)
prefix='unsolved_math_prioritization/attempts/5100033/';audit='draft_pr_descending_audit_20261002/audits/pr210_5100033/';queuepath='unsolved_math_prioritization/QUEUE.md'
check(len(leaves)==123 and sum(p.startswith(prefix) for p in leaves)==47 and sum(p.startswith(audit) for p in leaves)==75 and queuepath in leaves,'Exact actual merge scope')
check(all(p.startswith(prefix) or p.startswith(audit) or p==queuepath for p in leaves),'Foreign scope changed')
for row in load('FINITE_PUBLIC_BODY_MANIFEST.json')['files']:
 raw=body(row['path'],row)
 if row.get('git_blob'):check(native('blob',raw)==row['git_blob'],'Finite native science body identity')
for row in load('PUBLISHED_FINITE_PACKAGE_IDENTITY.json')['artifacts']:
 raw=body(row['archival_path'],row);e=lookup(inventories['CURRENT_MAIN']['root_tree'],row['native_current_MAIN_path']);check(e==row['native_entry'] and e['type']=='blob' and native('blob',raw)==e['git_object'],'Published artifact/native current association')
manifest=load('archive/published/SOURCE_MANIFEST.json');m={r['path']:r for r in manifest['files']};check(len(m)==len(manifest['files'])==180,'Finite source manifest')
root='k605a_outer_focal_pedal_product/';zipfile_path=BASE/'archive/published/k605a-source-verification.zip';original=load('ORIGINAL_BODY_CUSTODY.json');revised=load('REVISED_BODY_CUSTODY.json');original_lookup={r['relative_path']:r for r in original['leaves']}
with zipfile.ZipFile(zipfile_path) as z:
 infos=z.infolist();check(len(infos)==181 and len({i.filename for i in infos})==181,'ZIP finite exact count')
 for info in infos:
  check(info.filename.startswith(root) and not info.is_dir() and info.file_size<=1000000 and stat.S_IFMT(info.external_attr>>16)!=stat.S_IFLNK,'ZIP member bounds/type');rel=info.filename[len(root):];check(not rel.startswith('/') and all(x not in ('','.','..') for x in rel.split('/')),'ZIP relative path');raw=z.read(info);wanted=pin((BASE/'archive/published/SOURCE_MANIFEST.json').read_bytes()) if rel=='SOURCE_MANIFEST.json' else {k:m[rel][k] for k in ('bytes','sha256')};check(pin(raw)==wanted,'ZIP member manifest binding')
 check({i.filename[len(root):] for i in infos}==set(m)|{'SOURCE_MANIFEST.json'},'ZIP exact closure')
 for rel,row in original_lookup.items():
  raw=z.read(root+'verification/original_submission/'+rel);check(pin(raw)=={k:row[k] for k in ('bytes','sha256')} and native('blob',raw)==row['git_blob'],'Original20 published ZIP/native identity')
for row in original['leaves']:
 r=next(x for x in revised['leaves'] if x['relative_path']=='history/original_submission_20261015/'+row['relative_path']);check(all(row[k]==r[k] for k in ('mode','type','git_blob','bytes','sha256')),'Original20 revised history identity')
if args.full:
 for inv in (original,revised):
  for row in inv['leaves']:body(row['archival_path'],row,'blob',row['git_blob'])
for row in load('OWN_QUEUE_IDENTITIES_AND_FOREIGN_PRESERVATION.json')['rows']:body(row['own_row_archival_path'],row['own_row_pin'])
package=load('archive/published/PACKAGE_MANIFEST.json');published={r['path']:r for r in load('PUBLISHED_FINITE_PACKAGE_IDENTITY.json')['artifacts']}
for row in package['submission_files']+[package['manuscript_source'],package['metadata'],package['source_manifest']]:check({k:published[row['path']][k] for k in ('bytes','sha256')}=={k:row[k] for k in ('bytes','sha256')},'Outer package manifest binding')
print(json.dumps({'verified':True,'mode':'full_private_custody' if args.full else 'finite_public_packet','native_trees':len(trees),'exact_native_commit_bodies':len(commits['records']),'original20_from_existing_published_ZIP_verified':True,'finite_public_bodies':14,'all67_direct_native_body_copies_verified':args.full,'actual_merge_delta_leaves_independently_recomputed':123,'owned_case_audit_metadata_only_leaves':75,'published_ZIP_entries_verified':181,'whole_foreign_QUEUE_byte_difference_not_recomputed_offline':True,'network_author_proof_execution_or_mathematical_acceptance':False},sort_keys=True))
