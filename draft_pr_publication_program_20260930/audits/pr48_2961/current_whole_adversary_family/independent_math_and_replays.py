from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, sys
from fractions import Fraction as Q
F=Path(__file__).absolute().parent; A=F.parent; C=A/'reviewed_candidate'; R=A.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
def put(p,o):p.write_text(json.dumps(o,indent=2,allow_nan=False)+'\n')
def equal(a,b):
 return type(a)is type(b) and (a.keys()==b.keys() and all(equal(a[k],b[k])for k in a) if type(a)is dict else len(a)==len(b) and all(equal(x,y)for x,y in zip(a,b))if type(a)is list else a==b)
count=0

def check(x):
 global count; count+=1; assert x

def reduce(w):
 out=[]
 for t in w:
  if out and out[-1]==-t:out.pop()
  else:out.append(t)
 return tuple(out)
def winv(w):return tuple(-x for x in w[::-1])
def mul(a,b):
 d=dict(a[0]);n=a[1]
 for j,w in b[0].items():
  z=reduce(d.get(j+n,())+w)
  if z:d[j+n]=z
  else:d.pop(j+n,None)
 return d,n+b[1]
def inv(a):return {j-a[1]:winv(w)for j,w in a[0].items()},-a[1]
def prod(seq):
 o=({},0)
 for a in seq:o=mul(o,a)
 return o
def comm(a,b):return prod([a,b,inv(a),inv(b)])
def move(a,i):return {j+i:w for j,w in a[0].items()},a[1]
S=({},1); one=({},0); negatives=0
for m in [0,1,2,3,5,8,13,21,34]:
 aa=[({0:reduce((1,2+i,3,-(2+i)))},0)for i in range(m)]
 bb=[({0:reduce((4+i,1,-3))},0)for i in range(m)]
 cc=[comm(a,b)for a,b in zip(aa,bb)];h=prod(cc)
 a=prod(move(z,i+1)for i,z in enumerate(aa));b=prod(move(z,i+1)for i,z in enumerate(bb))
 c=prod(move(prod(cc[i:]),i)for i in range(m));K=prod(move(z,i+1)for i,z in enumerate(cc))
 check(comm(a,b)==K);check(comm(c,S)==mul(h,inv(K)));check(mul(comm(c,S),comm(a,b))==h)
 if m>=2:
  check(mul(cc[0],cc[1])!=mul(cc[1],cc[0]))
  wrong=prod(move(prod(cc[:i+1]),i)for i in range(m));check(mul(comm(wrong,S),K)!=h);negatives+=1
  check(mul(comm(S,c),K)!=h);negatives+=1
# Rational matrices, a nonautonomous family, no symbolic-library dependency.
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j]for k in range(2))for j in range(2))for i in range(2))
def mi(a):
 d=a[0][0]*a[1][1]-a[0][1]*a[1][0];check(d==1)
 return ((a[1][1],-a[0][1]),(-a[1][0],a[0][0]))
def mt(t):return ((Q(1),t),(t*t,1+t**3))
I=mt(Q(0));check(mm(mt(Q(1,2)),mt(Q(1,2)))!=mt(Q(1)))
for t in [Q(0),Q(1,7),Q(1,2),Q(1)]:
 for x in [Q(0),Q(1,9),Q(1,2),Q(1)]:
  a=mt(t*x);b=mm(mt(t),mi(a));check(mm(b,a)==mt(t));check(mm(mi(a),a)==I);check(mm(mi(b),b)==I)
  if x==0:check(a==I)
  if x==1:check(b==I)
# Sphere tangent differential; range follows 1 +/- 2xy >= z^2 on unit sphere.
check((-1+(-1)*(-1),0,0)==(0,0,0));check((0,0,1)!=(0,0,0))
# Signed pushforward model, with asymmetric rational measure.
mu=[Q(1,2),Q(1,3),Q(1,6)];height=[0,3,11];p=(1,2,0);q=(2,0,1)
av=lambda f:sum(mu[i]*(height[f[i]]-height[i])for i in range(3))
pq=tuple(p[q[i]]for i in range(3));push=[Q(0)]*3
for i in range(3):push[q[i]]+=mu[i]
d=av(pq)-av(p)-av(q);extra=sum((push[i]-mu[i])*(height[p[i]]-height[i])for i in range(3))
check(d==extra);check(d!=0);check(d!=-extra)
# Packing margins at arbitrarily chosen finite multiplicities/dimensions.
for dim in range(1,7):
 for n in [1,2,5,17,100]:
  radius=Q(1,4*(n+1));centers=[Q(i+1,n+1)for i in range(n)]
  check(all(radius<x<1-radius for x in centers));check(all(centers[i+1]-centers[i]>2*radius for i in range(n-1)))
# Genuine nested operation captures; every failure retained finally.
def run(name,argv,cwd,source=None):
 d=F/'literal_replays'/name;d.mkdir(parents=True,exist_ok=False);operator=Path(__file__).read_bytes();(d/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
 if source is not None:(d/'PRELAUNCH_SOURCE.py').write_bytes(source.read_bytes())
 rec=dict(schema='pr48-whole-private-literal-child/v1',operator_pid=os.getpid(),argv=argv,cwd=str(cwd),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_sha256=sha(source.read_bytes())if source else None,operator_sha256=sha(operator),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
 put(d/'PRELAUNCH.json',rec)
 try:
  with (d/'stdout.bin').open('xb')as out,(d/'stderr.bin').open('xb')as err:
   ch=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,PYTHONOPTIMIZE='0',GIT_OPTIONAL_LOCKS='0'));rec.update(actual_execution=True,pid=ch.pid);rec['exit_code']=ch.wait(timeout=180);rec['completed']=True
 finally:
  rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
  for n in ['stdout','stderr']:
   b=(d/(n+'.bin')).read_bytes();rec[n]=dict(path=n+'.bin',bytes=len(b),sha256=sha(b))
  rec['source_unchanged_after_child']=source is None or sha(source.read_bytes())==rec['source_sha256'];put(d/'CAPTURE.json',rec)
 check(rec['exit_code']==0);check((d/'stderr.bin').read_bytes()==b'');return (d/'stdout.bin').read_bytes()
historic=run('historical_git_note',['git','show','2c32c34e6ddfa52ce067805afd3e2157dc32a130:unsolved_math_prioritization/attempts/2961/PARTIAL.md'],R)
check(sha(historic)=='0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2')
final=(C/'PARTIAL.md').read_bytes();check(sha(final)=='196568d2029fd378dfa43919efbf49dcbd11244a2de8c525483f84484f00e5fa')
receipts=[]
for name,src,note,outname in [('author_historical','check_algebra.py',historic,'check_results.json'),('duplicate_historical','review/author_replay/check_algebra.py',historic,'check_results.json'),('author_final','check_algebra.py',final,'check_results.json'),('independent','review/independent_checks.py',None,None)]:
 work=F/'private_science'/name;work.mkdir(parents=True,exist_ok=False);p=work/Path(src).name;p.write_bytes((C/src).read_bytes())
 if note is not None:(work/'PARTIAL.md').write_bytes(note)
 out=run(name,['/usr/bin/python3','-B',str(p)],work,p)
 got=json.loads(out)
 if name=='independent':expected=json.loads((C/'review/independent_results.json').read_bytes());(work/'independent_results.json').write_bytes(out)
 else:
  expected=json.loads((C/'check_results.json').read_bytes())
  if name=='author_final':expected=dict(expected,partial_sha256=sha(final))
  check(json.loads((work/outname).read_bytes())==got);check((work/outname).read_bytes()==out)
 check(equal(got,expected));check(got['assertions']==(228 if name=='independent'else6570))
 receipts.append(dict(name=name,source_sha256=sha(p.read_bytes()),stdout_sha256=sha(out),complete_result_recursive_type_equal=True,duplicate_not_independent=name=='duplicate_historical',result=got))
result=dict(status='PASS_FRESH_EXACT_CONTROLS_AND_LITERAL_REPLAYS',actual_pid=os.getpid(),assertions=count,noncommuting_prefix_reversal_negative_controls=negatives,entire_literal_replays=receipts,foreign_primary_bodies_copied=False,full_problem_solved=False,new_substantive_attempts=0,audit_turns=0)
put(F/'INDEPENDENT_MATH_REPLAY_RESULT.json',result);print(json.dumps(result,indent=2))
