"""Independent stdlib controls, supplementary to the all-point proof in REPORT.md.

No assert is used: optimized Python executes exactly the same checks. The source
candidate is read only for its final SHA256 pin, never imported or executed.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import os
import sys

HERE = Path(__file__).resolve().parent
COUNT = 0

def check(condition, label):
    global COUNT
    COUNT += 1
    if not condition:
        raise ValueError(label)

def polyadd(a,b):
    out=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a):out[i]+=x
    for i,x in enumerate(b):out[i]+=x
    while len(out)>1 and out[-1]==0:out.pop()
    return out

def polymul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def scale(a,b):return [F(b)*x for x in a]
def deriv(a):return [F(i)*a[i] for i in range(1,len(a))]
def peval(a,s):return sum(x*s**i for i,x in enumerate(a))

N=list(map(F,[-4,5,-1])); D=list(map(F,[1,0,1]))
DER=polyadd(polymul(deriv(N),D),scale(polymul(N,deriv(D)),-1))
check(DER==list(map(F,[5,6,-5])), 'quotient-rule derivative numerator')
GP=polyadd(polymul(N,D),polymul([0,2],DER))
check(GP==list(map(F,[-4,15,7,-5,-1])), 'Cartesian radial Jacobian eigenvalue numerator')
DIV=scale(polyadd(polymul(N,D),polymul([0,1],DER)),2)
check(DIV==list(map(F,[-8,20,2,0,-2])), 'Cartesian divergence numerator')
check(polyadd(N,scale(D,4))==list(map(F,[0,5,3])), 'f >= -4 nonnegative numerator')
check(polyadd(scale(D,3),scale(N,-2))==[F(11),F(-10),F(5)], 'f < 3/2 numerator')
check(polyadd(polymul([-1,1],[-1,1]),[F(6,5)])==[F(11,5),F(-2),F(1)], 'positive-square upper-bound certificate')
check(polyadd(scale(polymul(D,D),11),scale(DIV,-1))==list(map(F,[19,-20,20,0,13])), 'one-oscillator divergence <= 11 polynomial')
check(polyadd(scale(polymul([F(-1,2),1],[F(-1,2),1]),20),[14,0,0,0,13])==list(map(F,[19,-20,20,0,13])), 'positive-square divergence certificate')
for s in [F(0),F(1),F(4)]:
    check(peval(N,s)/peval(D,s)=={F(0):F(-4),F(1):F(0),F(4):F(0)}[s], 'scalar stationary value')
check(peval(GP,F(1))/peval(D,F(1))**2==3, 'inner-circle radial rate')
check(peval(GP,F(4))/peval(D,F(4))**2==F(-24,17), 'outer-circle radial rate')
check(F(1918,625)==peval(DIV,F(3,4))/peval(D,F(3,4))**2, 'strict finite-time-transient control')
check(F(4)+F(3836,62500)-F(203,50)==F(43,31250)>0, 'finite-time value cannot be declared 203/50 everywhere')

TYPE={'O':(F(-4),F(-4)), 'U':(F(3),F(0)), 'S':(F(0),F(-24,17))}
EXPECTED_KY={'OO':F(0),'OU':F(11,4),'OS':F(1),'UU':F(203,50),'US':F(6827,1700),'SS':F(2)}
EXPECTED_FIXED={'OO':F(96,25),'OU':F(79,20),'OS':F(332,85),'UU':F(203,50),'US':F(6827,1700),'SS':F(1688,425)}

def ky(spectrum):
    spectrum=sorted(spectrum,reverse=True)
    sums=[F(0)]
    for x in spectrum:sums.append(sums[-1]+x)
    admissible=[j for j in range(len(sums)) if sums[j]>=0]
    j=max(admissible)
    if j==len(spectrum):return F(j)
    check(spectrum[j]<0, 'strict denominator after final nonnegative partial sum')
    return F(j)+sums[j]/(-spectrum[j])

table={}; MAX=[None]*5
for a,b in product(TYPE,repeat=2):
    unsorted=TYPE[a]+TYPE[b]+(F(-100),)
    spectrum=tuple(sorted(unsorted,reverse=True))
    sums=tuple(sum(spectrum[:k],F(0)) for k in range(1,6))
    for k in range(1,6):
        exterior=[sum((unsorted[i] for i in I),F(0)) for I in combinations(range(5),k)]
        check(max(exterior)==sums[k-1], 'fixed coordinate-wedge maximum equals singular-value sum')
        for v in exterior:check(v<=sums[k-1], 'every coordinate wedge is bounded by top sum')
        MAX[k-1]=sums[k-1] if MAX[k-1] is None else max(MAX[k-1],sums[k-1])
    key=''.join(sorted((a,b),key=lambda x:list(TYPE).index(x)))
    pointwise=ky(spectrum)
    fixed=F(4)+sums[3]/100
    check(pointwise==EXPECTED_KY[key], 'ordered-type pointwise KY')
    check(fixed==EXPECTED_FIXED[key], 'ordered-type fixed-global-index expression')
    check(spectrum[-1]==-100, 'fifth exponent is always -100')
    check(pointwise<=F(203,50) and fixed<=F(203,50), 'all-point dimension ceiling')
    check((pointwise==F(203,50))==(a==b=='U'), 'exact pointwise maximum locus')
    check((fixed==F(203,50))==(a==b=='U'), 'exact fixed-index maximum locus')
    table[a+b]={'spectrum':list(map(str,spectrum)), 'sums':list(map(str,sums)), 'pointwise_KY':str(pointwise), 'fixed_global_j4':str(fixed)}
check(MAX==list(map(F,[3,6,6,6,-94])), 'global partial sums, all nine ordered types')
check(next(j for j in range(5) if MAX[j]<0)==4, 'minimal fixed global index')
for key in ['OO','OU','OS','US','SS']:
    check(F(203,50)>EXPECTED_KY[key], 'strict pointwise comparison')
    check(F(203,50)>EXPECTED_FIXED[key], 'strict fixed-index comparison')
check(F(203,50)-EXPECTED_KY['US']==F(3,68), 'smallest asymptotic KY gap')

def transpose(a):return list(map(list,zip(*a)))
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def diag(v):return [[v[i] if i==j else F(0) for j in range(len(v))] for i in range(len(v))]
def orthogonal(c,s):return [[c,-s,F(0),F(0),F(0)],[s,c,F(0),F(0),F(0)],[F(0),F(0),c,-s,F(0)],[F(0),F(0),s,c,F(0)],[F(0),F(0),F(0),F(0),F(1)]]

def det(m):
    if len(m)==1:return m[0][0]
    return sum(((-1)**j*m[0][j]*det([r[:j]+r[j+1:] for r in m[1:]]) for j in range(len(m))),F(0))

def compound(m,k):
    choices=list(combinations(range(len(m)),k))
    return [[det([[m[i][j] for j in J] for i in I]) for J in choices] for I in choices]

Q0=orthogonal(F(3,5),F(4,5)); Qt=orthogonal(F(5,13),F(12,13))
check(mm(transpose(Q0),Q0)==diag([F(1)]*5), 'fixed initial frame exactly orthogonal')
check(mm(transpose(Qt),Qt)==diag([F(1)]*5), 'final frame exactly orthogonal')
frame_controls=0
for vals in [(F(1,2),F(1,3),F(2),F(1),F(1,5)),(F(7),F(1),F(7),F(1),F(1,9)),(F(1),)*5,(F(1,100),F(1,100),F(1),F(1,8),F(1,1000))]:
    m=mm(mm(Qt,diag(vals)),transpose(Q0))
    check(mm(m,transpose(Q0))!=diag(vals) or vals==(F(1),)*5, 'nontrivial Cartesian frame control')
    gram=mm(transpose(m),m)
    check(mm(mm(transpose(Q0),gram),Q0)==diag([v*v for v in vals]), 'Cartesian singular values exactly positive diagonal entries')
    for k in range(1,6):
        C=compound(m,k); C0=compound(Q0,k)
        products=[math.prod(vals[i] for i in I) for I in combinations(range(5),k)]
        result=mm(mm(transpose(C0),mm(transpose(C),C)),C0)
        check(result==diag([v*v for v in products]), 'all exterior singular products in Cartesian coordinates')
        frame_controls+=1

# Independent Cartesian ODE + Cartesian variational integration. These are
# finite floating-point controls, not proof of the asymptotic classification.
def ff(s):return (-(s-1)*(s-4))/(1+s*s)
def dff(s):
    n=-(s-1)*(s-4); nd=5-2*s; d=1+s*s; dd=2*s
    return (nd*d-n*dd)/(d*d)
def gg(r):return r*ff(r*r)
def rhs(v,omega):
    x,y,a,b,c,d=v; s=x*x+y*y; f=ff(s); fp=dff(s)
    j00=f+2*fp*x*x; j01=2*fp*x*y-omega
    j10=2*fp*x*y+omega; j11=f+2*fp*y*y
    return [f*x-omega*y,omega*x+f*y,j00*a+j01*c,j00*b+j01*d,j10*a+j11*c,j10*b+j11*d]
def integrate(r,theta,omega,t,step):
    count=math.ceil(t/step); h=t/count
    v=[r*math.cos(theta),r*math.sin(theta),1.,0.,0.,1.]
    for _ in range(count):
        k1=rhs(v,omega); k2=rhs([x+h*y/2 for x,y in zip(v,k1)],omega)
        k3=rhs([x+h*y/2 for x,y in zip(v,k2)],omega)
        k4=rhs([x+h*y for x,y in zip(v,k3)],omega)
        v=[x+h*(a+2*b+2*c+d)/6 for x,a,b,c,d in zip(v,k1,k2,k3,k4)]
    return v
def frame_entries(alpha,beta,theta,t,omega):
    c0,s0=math.cos(theta),math.sin(theta); c,s=math.cos(theta+omega*t),math.sin(theta+omega*t)
    return [c*alpha*c0+s*beta*s0,c*alpha*s0-s*beta*c0,s*alpha*c0-c*beta*s0,s*alpha*s0+c*beta*c0]

numeric=[]; maximum_error=0.
for r,omega,t in product([0.,.25,.75,.999,1.,1.001,1.5,1.99,2.],[1.,math.sqrt(2.)],[.125,.5,2.]):
    theta=.37; v=integrate(r,theta,omega,t,.0005); rt=math.hypot(v[0],v[1])
    if r==0:alpha=beta=math.exp(-4*t)
    elif r in (1.,2.):alpha=math.exp((3. if r==1 else -24/17)*t); beta=1.
    else:alpha=gg(rt)/gg(r); beta=rt/r
    expected=frame_entries(alpha,beta,theta,t,omega)
    error=max(abs(x-y) for x,y in zip(v[2:],expected))
    relative=error/max(1.,alpha,beta)
    maximum_error=max(maximum_error,relative)
    check(relative<2.e-8, 'independent Cartesian variational replay')
    numeric.append({'r0':r,'omega':omega,'time':t,'relative_max_matrix_error':relative})

mutants=[]
def reject(label,bad,good):
    check(bad!=good, 'meaningful mathematical mutant rejection: '+label)
    mutants.append(label)
reject('origin falsely assigned angular zero',ky((F(-4),F(0),F(-4),F(-4),F(-100))),F(0))
reject('unstable radial rate uses f instead of g prime',ky((F(0),F(0),F(-4),F(-4),F(-100))),F(11,4))
reject('outer-circle radial rate uses minus 3/2',ky((F(3),F(0),F(0),F(-3,2),F(-100))),F(6827,1700))
reject('w mode omitted',ky((F(3),F(3),F(0),F(0))),F(203,50))
reject('w contraction weakened to -10',ky((F(3),F(3),F(0),F(0),F(-10))),F(203,50))
reject('fixed-index formula relabeled pointwise at origin',F(96,25),F(0))
reject('fixed-index formula relabeled pointwise at periodic orbit',F(79,20),F(11,4))
reject('US partial-sum arithmetic loses zero',F(3)+F(27,1700),F(6827,1700))
reject('all-time finite maximum declared exactly 203/50',F(63459,15625),F(203,50))
reject('global first negative sum index chosen as 3',MAX[3]<0,True)
rv=.75; wv=integrate(rv,.37,1.,.5,.0005); rnow=math.hypot(wv[0],wv[1])
correct=frame_entries(gg(rnow)/gg(rv),rnow/rv,.37,.5,1.)
bad=frame_entries(gg(rnow)/gg(rv),1.,.37,.5,1.)
reject('heteroclinic angular stretch set to one',bad,correct)
bad=frame_entries(gg(rnow)/gg(rv),rnow/rv,.37,0.,1.)
reject('final orthogonal frame silently omitted',bad,correct)

source=HERE.parent/'original_head_authentication_20261006/original_attempt/COUNTEREXAMPLE.md'
body=source.read_bytes()
out={'schema':'pr111-independent-lyapunov-dimension-checks/v1','utc':datetime.now(timezone.utc).isoformat(),'actual_pid':os.getpid(),'optimized':bool(sys.flags.optimize),'check_count':COUNT,'passed':True,'source':{'path':str(source),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()},'nine_ordered_type_table':table,'global_partial_sums':list(map(str,MAX)),'orthogonal_exterior_controls':frame_controls,'cartesian_variational_controls':len(numeric),'maximum_cartesian_relative_error':maximum_error,'numeric_details':numeric,'meaningful_mathematical_mutants_rejected':mutants,'finite_time_transient':{'squared_radii':'3/4','one_oscillator_instantaneous_divergence':'1918/625','small_positive_time_local_KY_limit':'63459/15625','excess_over_203_50':'43/31250'},'analytic_proof_required':'REPORT.md proves the every-point classification and limit conventions; finite controls do not replace that proof.'}
destination=HERE/('CHECKS_OPTIMIZED.json' if sys.flags.optimize else 'CHECKS_NORMAL.json')
destination.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['actual_pid','optimized','check_count','passed','cartesian_variational_controls','maximum_cartesian_relative_error']}))
