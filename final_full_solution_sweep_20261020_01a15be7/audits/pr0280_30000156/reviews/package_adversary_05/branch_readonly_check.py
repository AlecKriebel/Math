#!/usr/bin/env python3
"""GET-only immutable pushed-commit comparison; no local Git object/ref/index writes."""
from pathlib import Path
import base64,hashlib,json,os,subprocess
O=Path(__file__).resolve().parent;A=O.parents[1];R=A.parents[1];W=R/'private/pr0280_package05/branch_get';W.mkdir(parents=True,exist_ok=True)
H='8aebb819bfac9c12340d2f1469408943549ab530';old='091bdecef6f84154f5d5c205a4b07eeb6391b8f8';calls=[]
def ck(v,m):
 if not v:raise RuntimeError(m)
def get(ep):
 r=subprocess.run(['gh','api','--hostname','github.com','repos/AlecKriebel/Math/'+ep,'--method','GET'],capture_output=True)
 ck(r.returncode==0,'GET failed');calls.append(ep);(W/(str(len(calls))+'.json')).write_bytes(r.stdout);return json.loads(r.stdout)
def localtree(path):
 b=subprocess.check_output(['git','ls-tree',old+(':'+path if path else '')],cwd=R.parent,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
 return {v.decode().split('\t',1)[1]:tuple(v.decode().split('\t',1)[0].split()) for v in b.splitlines()}
def remote_tree(sha,recursive=False):
 v=get('git/trees/'+sha+('?recursive=1' if recursive else ''));ck(not v.get('truncated'),'no truncation');return {e['path']:(e['mode'],e['type'],e['sha']) for e in v['tree']}
c=get('git/commits/'+H);ck([p['sha'] for p in c['parents']]==[old],'soleparent');tree=c['tree']['sha'];path=''
for component in ['unsolved_math_prioritization','attempts','30000156']:
 new=remote_tree(tree);baseline=localtree(path);ck({k:v for k,v in new.items() if k!=component}=={k:v for k,v in baseline.items() if k!=component},'unselected sibling comparison '+path);tree=new[component][2];path=(path+'/' if path else '')+component
new=remote_tree(tree,True);baseline=localtree(path);ss=json.loads((A/'SOURCE_SNAPSHOT.json').read_text());release=json.loads((A/'preprint/publication/RELEASE_FILES.json').read_text());expect={e['path'].split('30000156/',1)[1]:('100644','blob',e['git_blob']) for e in ss['files']}
for e in release['files']:
 b=(A/'preprint/publication'/e['path']).read_bytes();expect['preprint/'+e['path']]=('100644','blob',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())
ck({k:v for k,v in new.items() if v[1]!='tree'}==expect,'exact 17+5 leaf projection');ck({k:(v[0],v[1]) for k,v in new.items() if v[1]=='tree'}=={'checks':('040000','tree'),'independent_review':('040000','tree'),'preprint':('040000','tree')},'exact directory inventory')
(O/'BRANCH_GET_VERIFICATION.json').write_text(json.dumps({'commit':H,'sole_parent':old,'tree':c['tree']['sha'],'exact_original17_plus_scientific5':True,'queue_and_all_unselected_root_unsolved_attempt_siblings_preserved_by_blob_tree_identity':True,'exact_selected_directory_inventory':True,'read_only_methods':['GET'],'requests':len(calls),'local_git_mutations':False,'scope':'Immutable pushed child body only; does not certify current PR/main/test merge or authorize repeated commit/merge.'},indent=2)+'\n');print('Exact immutable pushed child verified with GET-only comparison.')
