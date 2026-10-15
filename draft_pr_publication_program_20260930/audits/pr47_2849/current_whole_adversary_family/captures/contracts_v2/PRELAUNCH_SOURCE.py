"""Private independent contract controls; never execute production source."""
from pathlib import Path, PurePosixPath
import ctypes, datetime as dt, hashlib, json, math, os, re, stat, sys
F=Path(__file__).absolute().parent;assert __debug__ and not sys.flags.optimize
T=F/'private_fixtures_v2';T.mkdir(exist_ok=False);checks=[]
def ck(n,v):
 if v is not True:raise AssertionError(n)
 checks.append(n)
def reject(n,fun):
 try:fun()
 except (ValueError,AssertionError,OSError,TypeError,KeyError):checks.append(n);return
 raise AssertionError('Expected rejection: '+n)
def relative(n):
 if not(type(n) is str and n and '\\' not in n and '\0' not in n):raise ValueError('path')
 p=PurePosixPath(n)
 if p.is_absolute() or p.as_posix()!=n or {'.','..','.git','__pycache__'}.intersection(p.parts):raise ValueError('path')
 return n
def rows(rs):
 if type(rs) is not list:raise ValueError('list')
 found=set()
 for x in rs:
  if type(x) is not dict or set(x)!={'path','bytes','sha256'}:raise ValueError('keys')
  n=relative(x['path'])
  if n in found:raise ValueError('duplicate')
  if type(x['bytes']) is not int or x['bytes']<0 or type(x['sha256']) is not str or re.fullmatch('[0-9a-f]{64}',x['sha256']) is None:raise ValueError('types')
  found.add(n)
 return found
def regular(p):
 if p.is_symlink() or any(q.is_symlink() for q in p.parents) or not stat.S_ISREG(p.stat().st_mode):raise ValueError('regular')
 return p.read_bytes()
def inventory(root):
 fs=set();ds=set()
 for p in root.rglob('*'):
  if p.is_symlink():raise ValueError('symlink')
  n=relative(p.relative_to(root).as_posix())
  if p.is_file():fs.add(n)
  elif p.is_dir():ds.add(n)
  else:raise ValueError('special')
 inferred={q.as_posix() for n in fs for q in PurePosixPath(n).parents if q.as_posix()!='.'}
 if inferred!=ds:raise ValueError('extra empty directory')
 return fs
def frozen(root,rs):
 names=rows(rs)
 if inventory(root)!=names:raise ValueError('topology')
 for x in rs:
  p=root/x['path'];b=regular(p)
  if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256'] or stat.S_IMODE(p.stat().st_mode)!=0o444:raise ValueError('body/mode')
mode=T/'mode';mode.write_bytes(b'full permission fixture')
for m in range(4096):
 ck('logical frozen mode '+str(m),(m==0o444)==(m&0o7777==0o444))
 mode.chmod(m);actual=stat.S_IMODE(mode.stat().st_mode)
 ck('physical exact chmod mode '+str(m),actual==m)
 ck('physical frozen admission '+str(m),(actual==0o444)==(m==0o444))
mode.chmod(0o444)
for n in ['',1,True,None,'/a','a//b','a/./b','a/../b','../x','a\\b','a\0b','.git/x','__pycache__/x']:
 reject('unsafe lexical '+repr(n),lambda n=n:relative(n))
ck('isolated dot honestly admitted',relative('.')=='.')
reject('dot directory later rejected',lambda:regular(T/'.'))
good={'path':'body','bytes':1,'sha256':hashlib.sha256(b'x').hexdigest()}
ck('valid typed row',rows([good])=={'body'})
for value in [True,False,1.0,-1,None,'1']:
 x=dict(good,bytes=value);reject('wrong byte scalar '+repr(value),lambda x=x:rows([x]))
reject('duplicate rows',lambda:rows([good,good]));reject('extra row key',lambda:rows([dict(good,approved=True)]))
for value in [False,0,'F'*64,'x'*63,'0'*65]:
 reject('wrong SHA scalar '+repr(value),lambda value=value:rows([dict(good,sha256=value)]))
toy=T/'toy';toy.mkdir();(toy/'body').write_bytes(b'x');(toy/'body').chmod(0o444)
frozen(toy,[good]);checks.append('positive full closure')
(toy/'body').chmod(0o644);reject('wrong full mode',lambda:frozen(toy,[good]));(toy/'body').chmod(0o444)
(toy/'empty').mkdir();reject('empty directory',lambda:frozen(toy,[good]));(toy/'empty').rmdir()
(toy/'extra').write_bytes(b'y');reject('extra file',lambda:frozen(toy,[good]));(toy/'extra').unlink()
(toy/'alias').symlink_to(toy/'body');reject('symlink member',lambda:frozen(toy,[good]));(toy/'alias').unlink()
ancestor=T/'ancestor';ancestor.symlink_to(toy);reject('symlink ancestor',lambda:regular(ancestor/'body'));ancestor.unlink()
os.mkfifo(toy/'pipe');reject('FIFO topology',lambda:frozen(toy,[good]));(toy/'pipe').unlink()
(toy/'body').chmod(0o644);(toy/'body').write_bytes(b'z');(toy/'body').chmod(0o444);reject('same-length whole body mutation',lambda:frozen(toy,[good]))
(toy/'body').chmod(0o644);(toy/'body').write_bytes(b'x');(toy/'body').chmod(0o444)
# The actual filesystem enforces absent-only publication and case aliases.
lib=ctypes.CDLL(None,use_errno=True);rename=lib.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
source=T/'exclusive_source';source.mkdir();(source/'body').write_bytes(b'new')
existing=T/'existing';existing.mkdir();(existing/'body').write_bytes(b'old')
ck('exclusive rename refuses existing',rename(os.fsencode(source),os.fsencode(existing),4)!=0 and (existing/'body').read_bytes()==b'old' and (source/'body').read_bytes()==b'new')
destination=T/'new_destination';ck('exclusive rename actual absent success',rename(os.fsencode(source),os.fsencode(destination),4)==0 and (destination/'body').read_bytes()==b'new')
case=T/'Case';case.write_bytes(b'case')
try:
 with (T/'case').open('xb') as f:f.write(b'bad')
except FileExistsError:checks.append('actual case alias exclusive create refusal')
else:raise AssertionError('Case-sensitive filesystem differs; record honestly')
def clock(s):
 p=dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s)
 if p.tzinfo is None or p.utcoffset()!=dt.timedelta(0):raise ValueError('UTC')
 return p
for value in ['2026-10-03T05:00:00','2026-10-03T05:00:00-07:00','bad']:
 reject('not aware UTC '+value,lambda value=value:clock(value))
ck('actual aware UTC',clock('2026-10-03T05:00:00Z').utcoffset()==dt.timedelta(0))
def named_science(x):
 if x['reading_completed'] is not True or x['full_problem_solved'] is not False or x['current_verdict'] is not None or type(x['original_substantive_attempts']) is not int or x['original_substantive_attempts']!=1:raise ValueError('named fields')
good_science={'reading_completed':True,'full_problem_solved':False,'current_verdict':None,'original_substantive_attempts':1}
named_science(good_science);checks.append('positive named science')
for k,v in [('reading_completed',1),('full_problem_solved',0),('current_verdict',False),('original_substantive_attempts',False)]:
 reject('typed named field '+k,lambda k=k,v=v:named_science(dict(good_science,**{k:v})))
named_science(dict(good_science,future_merge_approved=True));checks.append('unknown key limit honestly retained')
# Independently transcribed class-sensitive predicate, reconciled with V2 text.
import copy
A=F.parent;R=A.parents[2]
summary=json.loads((A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json').read_bytes())
snap=json.loads((A/'snapshot_manifest.json').read_bytes())
capture_keys={'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged'}
def equal(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return a==b
def completed(c,kind,argv,expected_source,parent):
 if type(c) is not dict or set(c)!=capture_keys or c['schema']!='pr47-root-literal-operation-capture/v1':raise ValueError('schema')
 if kind not in {'helper','git'} or type(c['argv']) is not list or not all(type(x) is str for x in c['argv']) or not equal(c['argv'],argv) or c['cwd']!=str(R):raise ValueError('argv')
 if type(parent) is not int or parent<=0 or type(c['actual_operator_pid']) is not int or c['actual_operator_pid']!=parent or type(c['pid']) is not int or c['pid']<=0:raise ValueError('PID')
 if c['actual_execution'] is not True or c['completed'] is not True or c['stdin_supplied'] is not False or type(c['exit_code']) is not int or c['exit_code']!=0:raise ValueError('child')
 if not clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc):raise ValueError('time')
 for k in ['stdout','stderr']:
  row=c[k];rows([row]);b=regular(R/row['path'])
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256'] or k=='stderr' and b!=b'':raise ValueError('stream')
 if kind=='helper':
  if type(c['source']) is not dict or not equal(c['source'],expected_source) or c['source_unchanged'] is not True:raise ValueError('helper source')
  rows([c['source']]);b=regular(R/c['source']['path'])
  if len(b)!=c['source']['bytes'] or hashlib.sha256(b).hexdigest()!=c['source']['sha256']:raise ValueError('helper body')
 elif expected_source is not None or c['source'] is not None or c['source_unchanged'] is not None:raise ValueError('Git nullsource')
spec=[]
for c,(private,original) in zip(summary['complete_actual_helper_captures'],[('author/verify.py','verify.py'),('submitted_copy/submitted_verify.py','review/submitted_verify.py'),('historical_independent/independent_checks.py','review/independent_checks.py')]):
 body=regular(A/'source_snapshot'/original)
 sr={'path':(A/'source_snapshot'/original).relative_to(R).as_posix(),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
 spec.append((c,'helper',['/usr/bin/python3','-B',str(A/'root_original_actual_reproduction'/private)],sr))
argvs=[]
for row in snap['files']:argvs.extend([['git','show',snap['head']+':'+row['path']],['git','ls-tree',snap['head'],'--',row['path']]])
argvs.append(['git','diff','--no-ext-diff','--no-textconv','--binary',snap['merge_base'],snap['head'],'--'])
for c,argv in zip(summary['complete_actual_Git_captures'],argvs):spec.append((c,'git',argv,None))
ck('genuine3helper33Gitcount',len(spec)==36)
mutation_count=0
for i,(c,kind,argv,src) in enumerate(spec):
 completed(c,kind,argv,src,summary['actual_operator_pid']);checks.append('genuine capture '+str(i))
 variants=[]
 for key in capture_keys:
  bad=copy.deepcopy(c);bad.pop(key);variants.append(('missing '+key,bad))
 for key,value in [('schema','wrong'),('actual_execution',1),('completed',1),('stdin_supplied',0),('exit_code',False),('exit_code',0.0),('exit_code',1),('pid',True),('pid',0),('actual_operator_pid',True),('actual_operator_pid',summary['actual_operator_pid']+1),('cwd',str(F)),('argv',['git','status']),('started_utc','2026-10-03T06:00:00'),('finished_utc','2026-10-03T06:00:00-07:00'),('finished_utc','2099-10-03T06:00:00Z'),('finished_utc','2020-10-03T06:00:00Z'),('source',None if kind=='helper' else spec[0][3]),('source_unchanged',None if kind=='helper' else True)]:
  bad=copy.deepcopy(c);bad[key]=value;variants.append((key+' '+repr(value),bad))
 bad=copy.deepcopy(c);bad['approved']=True;variants.append(('extra key',bad))
 for k in ['stdout','stderr']:
  for field,value in [('bytes',True),('bytes',-1),('sha256','0'*64),('path','../escape')]:
   bad=copy.deepcopy(c);bad[k][field]=value;variants.append((k+' '+field+' '+repr(value),bad))
 for label,bad in variants:
  reject('malformed capture '+str(i)+' '+label,lambda bad=bad,kind=kind,argv=argv,src=src:completed(bad,kind,argv,src,summary['actual_operator_pid']));mutation_count+=1
for value in [True,False,292.0,-1,4096,'0444',None]:
 reject('bad fullmode scalar '+repr(value),lambda value=value:(_ for _ in ()).throw(ValueError('typed fullmode')) if type(value) is not int or not 0<=value<4096 else None)
def unique_json(b):
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('duplicate')
   out[k]=v
  return out
 def floating(v):
  x=float(v)
  if not math.isfinite(x):raise ValueError('nonfinite')
  return x
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)),parse_float=floating)
for b in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}','{"x":1e999}']:reject('invalidJSON '+b,lambda b=b:unique_json(b))
ck('bool differs from int',not equal(True,1))
ck('null differs from false and empty',not equal(None,False) and not equal(None,{}))
ck('no future approval from currentcard',json.loads((A/'reviewed_candidate/status.json').read_bytes())['current_verdict'] is None)
# Further actual exclusive-rename destination types and observed case alias.
for label,kind in [('empty','directory'),('file','file'),('alias','symlink')]:
 source=T/('src_'+label);source.mkdir();(source/'body').write_bytes(b'new')
 dest=T/('dest_'+label)
 if kind=='directory':dest.mkdir()
 elif kind=='file':dest.write_bytes(b'old')
 else:dest.symlink_to(T/'existing')
 ck('actual rename rejects '+kind,rename(os.fsencode(source),os.fsencode(dest),4)!=0 and (source/'body').read_bytes()==b'new')
 if kind=='symlink':dest.unlink()
source=T/'case_src';source.mkdir();(source/'body').write_bytes(b'new')
ck('actual rename rejects case alias',rename(os.fsencode(T/'case_src'),os.fsencode(T/'CASE'),4)!=0 and case.read_bytes()==b'case')
result={'schema':'pr47-whole-independent-private-contract-controls/v1','actual_pid':os.getpid(),'passed':len(checks),'failed':0,'checks':checks,'capture_mutations_rejected':mutation_count,'genuine_capture_classes_accepted':{'helper':3,'Git_null_source':33},'all4096_actual_full_modes_tested':True,'source_consistent_dot_and_unknownkey_limits':True,'production_run':False,'future_acceptance_approved':False}
(F/'PRIVATE_CONTROLS_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['schema','actual_pid','passed','failed','production_run','future_acceptance_approved']},indent=2))
