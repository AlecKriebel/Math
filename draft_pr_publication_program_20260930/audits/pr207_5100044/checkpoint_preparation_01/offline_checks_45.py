"""Small owned-only guards for PR207 checkpoint tree replacement and lock behavior."""
import importlib.util,json,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checkpoint_fixture_subject',BASE/'checkpoint207_v2_findings45.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);c=m.core()
results=[]
def check(name,fn):
 fn();results.append({'name':name,'pass':True})
def same(a,b):m.need(a==b,'Fixture equality')
def refuses(fn):
 try:fn()
 except (RuntimeError,BlockingIOError,FileExistsError,OSError):return
 raise RuntimeError('Expected refusal did not occur')
class Store:
 def __init__(self):self.trees={};self.bodies={}
 def blob(self,raw):oid=c.native('blob',raw);self.bodies[oid]=raw;return ('100644','blob',oid)
 def tree(self,entries):
  rows=sorted([(name,*entry) for name,entry in entries.items()],key=lambda x:x[0].encode()+(b'/' if x[1]=='040000' else b''));oid=c.tree_hash(rows);self.trees[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':mo,'type':k,'sha':s} for n,mo,k,s in rows]};return oid
 def build(self,files):
  trie={}
  for path,value in files.items():
   node=trie
   for part in path.split('/')[:-1]:node=node.setdefault(part,{})
   node[path.split('/')[-1]]=value
  def rec(node):return self.tree({name:('040000','tree',rec(value)) if type(value) is dict else value for name,value in node.items()})
  return rec(trie)
 def api(self,method,path,body=None):
  m.need(method=='GET' and body is None,'Fixture is GET-only');kind,oid=path.split('/')[1:]
  if kind=='trees':return self.trees[oid]
  if kind=='blobs':
   import base64
   raw=self.bodies[oid];return {'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
  raise RuntimeError('Unexpected fixture API')
store=Store();old={path:('old '+path).encode() for path in m.VIEWS[1:]};files={path:store.blob(raw) for path,raw in old.items()}
empty=store.tree({});files['FOREIGN_EMPTY']=('040000','tree',empty);files['foreign_symlink']=('120000','blob',store.blob(b'foreign target')[2]);files['foreign_gitlink']=('160000','commit','e'*40);queue='unsolved_math_prioritization/QUEUE.md';files[queue]=store.blob(b'foreign QUEUE stays exact\n')
root=store.build(files);overlay={path:('new '+path).encode() for path in m.VIEWS};extra=m.CASE+'fixed_audit/REPORT.txt';overlay[extra]=b'fixed report\n';pre=[]
for path in m.VIEWS:pre.append({'path':path,'exists':path in old,**({'git_blob':store.blob(old[path])[2],**m.pin(old[path])} if path in old else {})})
manifest={'preimages':pre};trees=c.NativeTrees(store.api);wanted,changed,dirs=m.expected(c,trees,root,overlay,manifest)
newfiles={**files,**{path:store.blob(raw) for path,raw in overlay.items()}};actual=store.build(newfiles)
check('Computed replacement tree equals independent construction',lambda:same(wanted,actual))
check('Actual native change allowlist exact without deletions',lambda:same(c.NativeTrees(store.api).changes(root,actual),(changed,dirs,set())))
def foreign():
 t=c.NativeTrees(store.api)
 for path in ('FOREIGN_EMPTY','foreign_symlink','foreign_gitlink',queue):same(t.lookup(root,path),t.lookup(actual,path))
check('Foreign empty tree symlink gitlink and full QUEUE tuple preserved',foreign)
def wrong_preimage():
 f=dict(files);f[m.VIEWS[2]]=store.blob(b'unexpected program view');bad=store.build(f);refuses(lambda:m.expected(c,c.NativeTrees(store.api),bad,overlay,manifest))
check('Unexpected existing program preimage refuses',wrong_preimage)
def absent_program():
 f=dict(files);del f[m.VIEWS[2]];bad=store.build(f);refuses(lambda:m.expected(c,c.NativeTrees(store.api),bad,overlay,manifest))
check('Missing accepted program view refuses',absent_program)
def old_audit_mismatch():
 f=dict(files);f[extra]=store.blob(b'different existing evidence');bad=store.build(f);refuses(lambda:m.expected(c,c.NativeTrees(store.api),bad,overlay,manifest))
check('Different preexisting selected audit source refuses overwrite',old_audit_mismatch)
owned=Path(tempfile.mkdtemp(prefix='offline_fixtures_',dir=BASE));m.PROGRAM=owned/'program';m.PROGRAM.mkdir();lock=m.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock';lock.write_bytes(m.LOCK_BYTES);lock.chmod(0o444)
def contention():
 with m.WriterLock():refuses(lambda:m.WriterLock().__enter__())
check('Stable shared lock excludes second descriptor',contention)
def bad_lock():
 lock.chmod(0o644);lock.write_bytes(b'wrong');lock.chmod(0o444);refuses(lambda:m.WriterLock().__enter__())
check('Altered stable lock payload refuses',bad_lock)
route_journal=owned/'route_journal';route_journal.mkdir();route_api=m.API(c,route_journal,mutate=True)
check('Ref PATCH refuses before any service request',lambda:refuses(lambda:route_api('PATCH','git/refs/heads/main',{'sha':'f'*40})))
check('Ref POST refuses before any service request',lambda:refuses(lambda:route_api('POST','git/refs',{'ref':'refs/heads/main','sha':'f'*40})))
print(json.dumps({'schema':'pr207-small-owned-offline-guards-v1','source_pin':m.pin((BASE/'checkpoint207_v2_findings45.py').read_bytes()),'core_pin':m.pin((BASE/'archive206_verified_reference.py').read_bytes()),'checks':len(results),'all_pass':True,'results':results,'limits':'Owned in-memory native trees and lock fixtures only; no service/native/global-five action. No arbitrary same-UID writer guarantee or five-file transaction claimed.'},sort_keys=True,indent=2))
