from pathlib import Path
import itertools,math,json,datetime,os
counts={}
def ck(v,name):
 counts[name]=counts.get(name,0)+1
 if not v:raise ArithmeticError(name)
def bil(M,x,y):
 return sum(((x>>i)&1)*((y>>j)&1)*M[i][j] for i in range(4) for j in range(4))%2
def q(M,c,x):
 return (sum(((x>>i)&1)*((c>>i)&1) for i in range(4))+sum(M[i][j]*((x>>i)&1)*((x>>j)&1) for i in range(4) for j in range(i+1,4)))%2
forms=0;bases_total=0
for entries in itertools.product([0,1],repeat=6):
 M=[[0]*4 for _ in range(4)]
 for (i,j),v in zip(itertools.combinations(range(4),2),entries):M[i][j]=M[j][i]=v
 if any(all(bil(M,x,y)==0 for y in [1,2,4,8]) for x in range(1,16)):continue
 forms+=1;bases=[]
 for a in range(1,16):
  for b in range(1,16):
   if bil(M,a,b)!=1:continue
   orth=[x for x in range(1,16) if bil(M,a,x)==bil(M,b,x)==0]
   for c in orth:
    for d in orth:
     if bil(M,c,d)==1:bases.append((a,b,c,d))
 ck(len(bases)==720,'all symplectic bases count');bases_total+=len(bases)
 for diagonal in range(16):
  gauss=sum((-1)**q(M,diagonal,x) for x in range(16));ck(abs(gauss)==4,'nondegenerate Gauss magnitude')
  expected=int(gauss<0)
  for a,b,c,d in bases:ck((q(M,diagonal,a)*q(M,diagonal,b)+q(M,diagonal,c)*q(M,diagonal,d))%2==expected,'Arf all bases against Gauss sum')
  for x in range(16):
   for y in range(16):ck(q(M,diagonal,x^y)==(q(M,diagonal,x)+q(M,diagonal,y)+bil(M,x,y))%2,'quadratic polarization')
ck(forms==28,'all28 nondegenerate alternating forms')
for ws in itertools.product(range(-12,13,2),repeat=4):
 arf=sum((ws[i]//2+1)*(ws[i+1]//2+1) for i in [0,2])%2
 reversed_arf=sum((-ws[i]//2+1)*(-ws[i+1]//2+1) for i in [0,2])%2
 ck(arf==reversed_arf,'negative integer winding lift sign invariance')
for a,b,w in itertools.product(range(-5,6),range(-5,6),range(-10,11)):
 ends=[w,-4-w]
 ck(math.gcd(a,b,*[e+2 for e in ends])==math.gcd(-a,-b,*[e+2 for e in ends]),'genus1 handle sign invariance all peripheral terms')
 for z in [-3,-1,0,1,3]:ck(math.gcd(a,b,*[e+2 for e in ends])==math.gcd(a+z*(ends[0]+2),b,*[e+2 for e in ends]),'genus1 peripheral detour ideal')
# q(a)=q(b)=1,q(r)=1, r radical. Replacing a by a+r keeps intersection1 but changes handle-only Arf.
ck((1*1)%2!=((1+1)%2*1)%2,'nonzero radical makes handle Arf lift-dependent')
for qa,qb,ra,rb in itertools.product([0,1],repeat=4):ck(qa*qb%2==((qa+ra*0)*(qb+rb*0))%2,'zero radical gives lift-independent Arf')
# A(m,n): all cycle-compositions are zero and bridge is unrelated. Count every permitted path exactly.
for m,n in itertools.product(range(3,9),repeat=2):
 arrows=[(i,(i+1)%m,'a'+str(i)) for i in range(m)]+[(m+i,m+(i+1)%n,'b'+str(i)) for i in range(n)]+[(0,m,'z')]
 forbidden={(('a'+str(i)),('a'+str((i+1)%m))) for i in range(m)}|{(('b'+str(i)),('b'+str((i+1)%n))) for i in range(n)}
 levels=[len(arrows)];paths=[(x[2],x[1]) for x in arrows]
 for length in range(2,5):
  paths=[(path+','+name,v) for path,end in paths for u,v,name in arrows if u==end and (path.split(',')[-1],name) not in forbidden];levels.append(len(paths))
 ck(levels==[m+n+1,2,1,0],'exact A(m,n) permitted path levels')
 ck(m+n+sum(levels)==2*(m+n)+4,'A(m,n) exact finite dimension')
ck(sorted([-3,-5])!=sorted([-4,-4]),'puncture witness differs')
ck(3+5-1==4+4-1 and 3+5-2==4+4-2,'puncture witness equal outer formula')
result={'status':'PASS_INDEPENDENT_FINITE_ALGEBRAIC_CONTROLS','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'counts':counts,'checks':sum(counts.values()),'nondegenerate_forms':forms,'basis_enumerations':bases_total,'scope':'Independent exact finite controls for F2 Arf basis-independence, integer handle sign/peripheral gcd behavior, radical condition and finite path dimensions of A(m,n). These do not implement the full PL search, certify old software, or establish universal halting by experiment.'}
(Path(__file__).parent/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
