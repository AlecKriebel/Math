#!/usr/bin/env python3
"""Actual put/tree/validate_saved over a pure in-memory Git protocol fixture.

This does not create real Git objects or validate any live Git integration.
"""
import datetime,hashlib,importlib.util,json,pathlib,sys
F=pathlib.Path(__file__).resolve().parent;A=F.parents[1];P=A/'publication'
def need(c,m):
 if not c:raise RuntimeError(m)
def main():
 spec=importlib.util.spec_from_file_location('actual_updater_memory_git',P/'update_pr_publication.py');u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u);objects={};commits={};calls=[]
 def oid(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
 def blob(data):
  key=oid('blob',data);objects[key]=('blob',data);return key
 def make(entries):
  entries=sorted(entries,key=lambda e:e[3]+(b'/' if e[1]=='tree' else b''));raw=b''.join(mode.encode()+b' '+name+b'\0'+bytes.fromhex(key) for mode,kind,key,name in entries);key=oid('tree',raw);objects[key]=('tree',entries);return key
 def tree_from_flat(flat):
  children={}
  for raw,data in flat.items():
   parts=raw.split('/',1)
   if len(parts)==1:children[parts[0]]=data
   else:children.setdefault(parts[0],{})[parts[1]]=data
  return make([('040000','tree',tree_from_flat(data),name.encode()) if isinstance(data,dict) else ('100644','blob',blob(data),name.encode()) for name,data in children.items()])
 def flatten(key,prefix=''):
  if key in commits:key=commits[key][0]
  out={}
  for mode,kind,child,name in objects[key][1]:
   raw=prefix+name.decode()
   if kind=='tree':out.update(flatten(child,raw+'/'))
   else:out[raw]=objects[child][1]
  return out
 originals={u.BASE+'/'+p.name:p.read_bytes() for p in (A/'submitted').iterdir()};base={**originals,'README.md':b'UNRELATED ROOT MUST SURVIVE','attempts/elsewhere/result.txt':b'OTHER SHARD MUST SURVIVE'};commits[u.ORIGINAL]=(tree_from_flat(base),['a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f']);wanted={u.BASE+'/'+p.name:p.read_bytes() for p in (A/'current_edition').iterdir()}
 for name in ['Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf','Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip','zenodo-deposit.json']:wanted[u.BASE+'/publication_20261017/'+name]=(P/name).read_bytes()
 wanted[u.BASE+'/publication_20261017/PUBLICATION_RECEIPT.json']=b'SYNTHETIC PUBLICATION RECEIPT FIXTURE ONLY\n';wanted[u.BASE+'/publication_20261017/README.md']=b'SYNTHETIC PUBLICATION NOTE FIXTURE ONLY\n';need(len(wanted)==14,'fourteen intended paths')
 def git(*args,data=None):
  calls.append(args[0])
  if args[0]=='ls-tree':
   key=args[-1];key=commits[key][0] if key in commits else key
   return b''.join((mode+' '+kind+' '+child).encode()+b'\t'+name+b'\0' for mode,kind,child,name in objects[key][1])
  if args[0]=='mktree':
   entries=[]
   for e in data.rstrip(b'\0').split(b'\0'):
    meta,name=e.split(b'\t',1);mode,kind,key=meta.decode().split();entries.append((mode,kind,key,name))
   return (make(entries)+'\n').encode()
  if args[0]=='rev-list':return (args[-1]+' '+' '.join(commits[args[-1]][1])+'\n').encode()
  if args[0]=='diff-tree':
   commit=args[-1];current=flatten(commit);parent=flatten(commits[commit][1][0]);return ('\n'.join(sorted(p for p in set(current)|set(parent) if current.get(p)!=parent.get(p)))+'\n').encode()
  if args[0]=='show':
   commit,path=args[1].split(':',1);return flatten(commit)[path]
  raise RuntimeError('unmodeled Git protocol '+repr(args))
 u.git=git;root=u.ORIGINAL
 for path,data in sorted(wanted.items()):root=u.put(root,path.split('/'),blob(data))
 expected={**base,**wanted};need(flatten(root)==expected,'actual put/tree failed exact intended tree')
 commit=oid('commit',(root+'\n'+u.ORIGINAL).encode());commits[commit]=(root,[u.ORIGINAL]);identity={'pr':1280,'base':u.ORIGINAL,'branch':u.BRANCH,'paths':sorted(wanted),'files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(wanted.items())}};saved={**identity,'commit':commit};need(u.validate_saved(saved,identity,wanted)==commit,'saved actual tree rejected')
 rejected=[]
 for label,parents in [('no_parent',[]),('wrong_parent',['0'*40]),('two_parents',[u.ORIGINAL,'1'*40])]:
  commits[commit]=(root,parents)
  try:u.validate_saved(saved,identity,wanted)
  except RuntimeError:rejected.append(label)
  else:raise RuntimeError('bad parent accepted')
 commits[commit]=(root,[u.ORIGINAL]);foreign=u.put(root,['foreign','results.txt'],blob(b'UNAUTHORIZED'));commits[commit]=(foreign,[u.ORIGINAL])
 try:u.validate_saved(saved,identity,wanted)
 except RuntimeError:rejected.append('foreign_changed_path')
 else:raise RuntimeError('foreign path accepted')
 return {'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'intended_files':len(wanted),'unchanged_unrelated_files_preserved':2,'all_resulting_bytes_exact':True,'actual_functions':['put','tree','validate_saved'],'protocol_operations':dict((name,calls.count(name)) for name in sorted(set(calls))),'negative_controls':rejected,'scope':'Pure in-memory protocol fixture for actual recursive tree construction and saved-tree validator. Two publication prose/receipt bodies are explicitly synthetic; local document/artifact bytes are actual. No real Git object, ref, index, worktree, subprocess, network or remote operation.'}
if __name__=='__main__':
 r=main();(F/('OBJECT_CONSTRUCTION_MODE_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
