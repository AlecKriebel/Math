"""Read-only canonical native tree subset; verbatim AST blocks from pinned PR206 reference.
No transport, object mutation, reference update, global writer, or CLI exists.
"""
import hashlib, re
from pathlib import PurePosixPath
MAX_ENTRIES=30000
MAX_DEPTH=64

def need(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)

def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def hexid(v,n=40):return type(v) is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',v) is not None

def rel(v):
 need(type(v) is str and v and not PurePosixPath(v).is_absolute() and '\\' not in v and '\0' not in v and all(x not in ('','.','..') for x in v.split('/')),'Unsafe relative path');return v

def tree_hash(rows):
 rows=sorted(rows,key=lambda x:x[0].encode()+ (b'/' if x[1]=='040000' else b''))
 raw=b''.join((mode.lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(oid) for name,mode,kind,oid in rows)
 return native('tree',raw)

class NativeTrees:
 """Authenticate only needed immediate trees; equal foreign SHAs stay opaque."""
 def __init__(self,api):self.api=api;self.cache={};self.inspected=0
 def get(self,oid,depth):
  need(hexid(oid) and depth<=MAX_DEPTH,'Native tree identity/depth bound')
  if oid in self.cache:return self.cache[oid]
  j=self.api('GET','git/trees/'+oid);need(j.get('sha')==oid and j.get('truncated') is False and type(j.get('tree')) is list,'Complete immediate native tree required')
  need(len(j['tree'])<=MAX_ENTRIES-self.inspected,'Actually inspected native entry bound')
  rows=[];names=set()
  for e in j['tree']:
   name=e['path'];need(type(name) is str and name and '/' not in name and '\0' not in name and name not in ('.','..') and name not in names and hexid(e['sha']),'Native tree entry')
   name.encode('utf-8');names.add(name);mode=e['mode'];kind=e['type']
   need((mode,kind) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')),'Native mode/type');rows.append((name,mode,kind,e['sha']))
  need(rows==sorted(rows,key=lambda x:x[0].encode()+(b'/' if x[1]=='040000' else b'')) and tree_hash(rows)==oid,'Immediate native tree order/SHA1 mismatch')
  self.inspected+=len(rows);self.cache[oid]={name:(mode,kind,sha1) for name,mode,kind,sha1 in rows};return self.cache[oid]
 def lookup(self,root,path):
  parts=rel(path).split('/');need(len(parts)-1<=MAX_DEPTH,'Lookup depth bound');oid=root
  for depth,name in enumerate(parts):
   entry=self.get(oid,depth).get(name)
   if entry is None:return None
   if depth==len(parts)-1:return entry
   if entry[0:2]!=('040000','tree'):return None
   oid=entry[2]
 def expected(self,root,overlay):
  trie={};missing=set();newdirs=set()
  for path,raw in overlay.items():
   parts=rel(path).split('/');need(len(parts)-1<=MAX_DEPTH,'Archive path depth bound');node=trie
   for name in parts[:-1]:
    need(name not in node or type(node[name]) is dict,'Overlay ancestor/file collision');node=node.setdefault(name,{})
   need(parts[-1] not in node,'Overlay path/ancestor collision');node[parts[-1]]=raw
  def rebuild(oid,node,prefix,depth):
   need(depth<=MAX_DEPTH,'Expected tree depth bound');entries=dict(self.get(oid,depth)) if oid is not None else {}
   for name,value in node.items():
    old=entries.get(name);path=prefix+name
    if type(value) is bytes:
     wanted=('100644','blob',native('blob',value));need(old is None or old==wanted,'Preexisting allowlist path mismatches')
     if old is None:missing.add(path)
     entries[name]=wanted
    else:
     need(old is None or old[0:2]==('040000','tree'),'Allowlist ancestor is a native leaf')
     if old is None:newdirs.add(path)
     entries[name]=('040000','tree',rebuild(old[2] if old else None,value,path+'/',depth+1))
   return tree_hash([(name,*entry) for name,entry in entries.items()])
  return rebuild(root,trie,'',0),missing,newdirs
 def changes(self,before,after):
  leaves=set();added=set();deleted=set()
  def compare(old,new,prefix,depth):
   need(depth<=MAX_DEPTH,'Changed subtree depth bound')
   if old==new:return
   left=self.get(old,depth) if old else {};right=self.get(new,depth) if new else {}
   for name in sorted(set(left)|set(right),key=lambda x:x.encode()):
    a=left.get(name);b=right.get(name)
    if a==b:continue
    path=prefix+name;at=a is not None and a[0:2]==('040000','tree');bt=b is not None and b[0:2]==('040000','tree')
    if at and bt:compare(a[2],b[2],path+'/',depth+1)
    else:
     if at:deleted.add(path);compare(a[2],None,path+'/',depth+1)
     if bt:added.add(path);compare(None,b[2],path+'/',depth+1)
     if (a is not None and not at) or (b is not None and not bt):leaves.add(path)
  compare(before,after,'',0);return leaves,added,deleted

