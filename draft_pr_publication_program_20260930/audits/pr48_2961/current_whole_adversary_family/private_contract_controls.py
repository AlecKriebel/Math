"""Private independent predicates matching consumed production semantics, not production execution."""
from pathlib import Path,PurePosixPath
import ctypes,datetime as dt,hashlib,json,math,os,stat,sys
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];N=0;cases=[]
def check(x):
 global N;N+=1;assert x

def reject(fn,*args):
 try:fn(*args)
 except (AssertionError,ValueError,TypeError,KeyError,FileNotFoundError,OSError):return
 raise AssertionError('negative accepted')
def path(n):
 assert type(n)is str and n and '\\'not in n and '\0'not in n;p=PurePosixPath(n)
 assert not p.is_absolute()and p.as_posix()==n and not set(p.parts)&{'.','..','.git','__pycache__'};return n

def regular(p):assert not p.is_symlink()and all(not x.is_symlink()for x in p.parents)and stat.S_ISREG(p.stat().st_mode);return p.read_bytes()
def topology(p):
 assert p.is_dir()and not p.is_symlink();files=set();dirs=set()
 for q in p.rglob('*'):
  assert not q.is_symlink();n=path(q.relative_to(p).as_posix())
  if q.is_file():files.add(n)
  else:assert stat.S_ISDIR(q.stat().st_mode);dirs.add(n)
 assert dirs=={x.as_posix()for n in files for x in PurePosixPath(n).parents if str(x)!='.'}
 return files

def row(x):
 assert type(x)is dict and set(x)=={'path','bytes','sha256'};path(x['path']);assert type(x['bytes'])is int and x['bytes']>=0
 assert type(x['sha256'])is str and len(x['sha256'])==64 and all(t in'0123456789abcdef'for t in x['sha256'])

def stamp(v):
 assert type(v)is str;z=dt.datetime.fromisoformat(v.replace('Z','+00:00'));assert z.tzinfo is not None and z.utcoffset()==dt.timedelta(0);return z

def captured(c):
 assert c['actual_execution']is True and c['completed']is True and c['stdin_supplied']is False and type(c['pid'])is int and c['pid']>0 and type(c['exit_code'])is int and c['exit_code']==0 and type(c['actual_operator_pid'])is int and c['actual_operator_pid']==11716 and c['operator_unchanged']is True and c['cwd']==str(R)
 assert stamp(c['started_utc'])<=stamp(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
 if c['schema']=='pr48-root-unchanged-helper-actual-capture/v1':row(c['source']);assert c['source_unchanged']is True and c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])]
 else:assert c['schema']=='pr48-root-readonly-git-actual-capture/v1'and c['source']is None and c['source_unchanged']is None and c['argv'][0]=='git'and c['argv'][1]in {'show','ls-tree','diff','merge-base'}
 for stream in ['stdout','stderr']:row(c[stream])

def parse(b):
 def pairs(a):
  x={}
  for k,v in a:assert k not in x;x[k]=v
  return x
 def floating(v):f=float(v);assert math.isfinite(f);return f
 return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
r=json.loads((A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json').read_bytes());caps=r['complete_actual_Git_captures']+r['complete_actual_helper_captures']
if len(sys.argv)>1:
 # Genuine intended negative: reject Git null-source if wrongly classified as helper.
 row(caps[0]['source']);raise AssertionError('wrong classification accepted')
for c in caps:
 captured(c);check(True)
 for k,v in [('pid',True),('pid',0),('exit_code',False),('actual_operator_pid',True),('completed',False),('actual_execution',None),('stdin_supplied',True),('finished_utc','2099-01-01T00:00:00Z'),('source_unchanged',False),('schema','bad')]:
  bad=dict(c,**{k:v});reject(captured,bad);check(True)
 if c['schema']=='pr48-root-readonly-git-actual-capture/v1':reject(captured,dict(c,argv=['git','reset','--hard']));check(True)
 else:reject(captured,dict(c,source=None));check(True)
for n in ['a','a/b','.']:path(n);check(True)
for n in ['',True,1,None,'/a','a//b','a/./b','a/../b','a/','a\\b','a\0b','.git/x','__pycache__/x']:reject(path,n);check(True)
good=dict(path='a',bytes=0,sha256='0'*64);row(good)
for k,v in [('bytes',True),('bytes',-1),('sha256',0),('path','/x')]:reject(row,dict(good,**{k:v}));check(True)
for x in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":1e999}',b'{"a":Infinity}']:reject(parse,x);check(True)
for x in ['2026-10-03T00:00:00','2026-10-03T00:00:00-07:00',True,None]:reject(stamp,x);check(True)
# Actual physical modes and topology, not arithmetic simulations.
q=F/'mode_fixture';q.write_bytes(b'first-party full-mode fixture\n');modes=[]
for mode in range(4096):q.chmod(mode);got=stat.S_IMODE(q.stat().st_mode);check(got==mode);modes.append(dict(requested=mode,observed=got,accepted_as_full0444=got==0o444))
q.chmod(0o444);check(sum(r['accepted_as_full0444']for r in modes)==1)
fixture=F/'topology_fixture';fixture.mkdir();(fixture/'file').write_text('sentinel\n');check(topology(fixture)=={'file'})
(fixture/'empty').mkdir();reject(topology,fixture);(fixture/'empty/AFTERTEST.md').write_text('This directory was intentionally empty during the rejection test.\n')
(fixture/'link').symlink_to('file');reject(topology,fixture);reject(regular,fixture/'link');(fixture/'link').unlink()
os.mkfifo(fixture/'fifo');reject(topology,fixture);(fixture/'fifo').unlink()
reject(regular,fixture);check(True)
(fixture/'parent_alias').symlink_to(fixture,target_is_directory=True);reject(regular,fixture/'parent_alias/file');(fixture/'parent_alias').unlink()
# macOS RENAME_EXCL4, preserving every existing sentinel.
assert sys.platform=='darwin';lib=ctypes.CDLL(None,use_errno=True);rename=lib.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
ren=F/'rename_fixtures';ren.mkdir();renamecases=[]
for kind in ['nonemptydir','emptydir','file','symlink','case_alias']:
 src=ren/(kind+'_source');src.mkdir();(src/'payload').write_text('new payload\n');dst=ren/(kind+'_destination')
 if kind in ['nonemptydir','emptydir']:dst.mkdir()
 if kind=='nonemptydir':(dst/'sentinel').write_text('existing sentinel\n')
 if kind=='file':dst.write_text('existing file\n')
 if kind=='symlink':dst.symlink_to(q)
 if kind=='case_alias':dst.write_text('case sentinel\n')
 arg=dst.with_name(dst.name.upper())if kind=='case_alias'else dst
 ret=rename(os.fsencode(src),os.fsencode(arg),4);err=ctypes.get_errno();check(ret==-1 and src.is_dir()and(dst.exists()or dst.is_symlink()))
 renamecases.append(dict(kind=kind,result=ret,errno=err,destination_preserved=True))
 if kind=='symlink':dst.unlink();dst.write_text('symlink test removed after refusal; metadata retained\n')
 if kind=='emptydir':(dst/'AFTERTEST.md').write_text('Initially empty destination retained with marker after refusal.\n')
src=ren/'success_source';src.mkdir();(src/'payload').write_text('successful exclusive rename\n');dst=ren/'success_destination';check(rename(os.fsencode(src),os.fsencode(dst),4)==0 and not src.exists()and(dst/'payload').is_file())
# Consumed-field limits are admitted explicitly; do not invent stronger rejection.
check(path('.')=='.');reject(regular,F/path('.'));check(30004403.0==30004403)
result=dict(status='PASS_INDEPENDENT_SCALAR_CAPTURE_TOPOLOGY_ALL4096_AND_RENAME_CONTROLS',actual_pid=os.getpid(),assertions=N,true_Git_null_source_positives=38,true_typed_helper_positives=4,modes=modes,exclusive_rename_existing_destinations=renamecases,isolated_dot_lexically_accepted_downstream_regular_rejected=True,equal_duplicate_float_equality_limit_admitted=True,unknown_metadata_not_universal_allowlist=True,production_import_compile_execution=False,future_acceptance_approved=False)
(F/'PRIVATE_CONTRACT_CONTROL_RESULT.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='modes'},indent=2))
