"""Independent audit of the frozen packet, not a new optimization or proof search.
Reconstructs existing exact fixtures from explicit expected normals without importing
the author's verifier. Recomputes diagnostics of saved numerical runs only.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sympy as s
import numpy as np

ROOT=Path(__file__).resolve().parent.parent
P=ROOT
assertions=0

def ok(claim, label):
    global assertions
    if not bool(claim):
        raise AssertionError(label)
    assertions += 1

def eq(a,b,label):
    ok(s.simplify(a-b)==0,label)

def nn(a,label):
    ok(s.simplify(a).is_nonnegative is True,label)

def pos(a,label):
    ok(s.simplify(a).is_positive is True,label)

def fixture(name, points, normals):
    x=list(map(s.Matrix, points)); n=list(map(s.Matrix, normals)); m=len(x)
    edge=[x[(i+1)%m]-x[i] for i in range(m)]
    lengths=[s.sqrt(e.dot(e)) for e in edge]
    for v in lengths: pos(v,name+' positive edge')
    u=[e/l for e,l in zip(edge,lengths)]
    turns=[u[i-1]-u[i] for i in range(m)]
    a=[s.sqrt(v.dot(v)) for v in turns]
    for v in a: pos(v,name+' nonzero turn')
    for i in range(m):
        eq(n[i].dot(n[i]),1,name+' unit expected normal')
        for j in range(len(x[0])): eq(turns[i][j],a[i]*n[i][j],name+' reflection direction')
    y=[xx-nn for xx,nn in zip(x,n)]
    allpoints=x+y
    pair_distances=[]
    for i in range(2*m):
        for j in range(i):
            d=allpoints[i]-allpoints[j]; d2=s.simplify(d.dot(d))
            nn(1-d2,name+' all exact diameter constraints')
            pair_distances.append(d2)
    for i in range(m):
        eq((x[i]-y[i]).dot(x[i]-y[i]),1,name+' exact diameter pair')
        for j in range(m):
            d=x[j]-x[i]
            nn(-2*d.dot(n[i])-d.dot(d),name+' supporting ball contact')
    L=s.simplify(sum(lengths)); A=s.simplify(sum(a)); lam=[aa/A for aa in a]
    sig=s.simplify(sum(v*v for v in lam))
    eq(sum(aa*xx.dot(nn_) for aa,xx,nn_ in zip(a,x,n)),L,name+' perimeter identity')
    nn(L-A*(1-s.sqrt((1-sig)/2)),name+' moment inequality')
    nn(A-4,name+' turn lower bound')
    if m>2: pos(L-2,name+' longer than two')
    return {'name':name,'L':str(L),'A':str(A),'sigma':str(sig),
            'pairwise_squared_distances':sorted(set(map(str,pair_distances))),
            'certified_diameter':1}

manifest=[]
for line in (P/'SHA256SUMS').read_text().splitlines():
    wanted,fn=line.split(maxsplit=1)
    actual=hashlib.sha256((P/fn).read_bytes()).hexdigest()
    ok(actual==wanted,'manifest '+fn); manifest.append(fn)

R=s.Rational
fixtures=[]
fixtures.append(fixture('diameter',[(0,0),(1,0)],[(-1,0),(1,0)]))
fixtures.append(fixture('square',[(R(1,2),0),(0,R(1,2)),(-R(1,2),0),(0,-R(1,2))],[(1,0),(0,1),(-1,0),(0,-1)]))
a=R(3,10);b=R(1,10)
spatial=[(a,b,a),(a,-b,-a),(-a,b,-a),(-a,-b,a)]
nspatial=[[s.Rational(1)/s.sqrt(22)*v for v in row] for row in [(3,2,3),(3,-2,-3),(-3,2,-3),(-3,-2,3)]]
fixtures.append(fixture('symmetric spatial four orbit',spatial,nspatial))
xsp=list(map(s.Matrix,spatial)); vol=s.det(s.Matrix.hstack(*[v-xsp[0] for v in xsp[1:]]))
eq(vol,-R(18,125),'spatial nondegeneracy volume');pos(-vol,'spatial nonzero volume')
nt=[(1,0),(-R(1,2),s.sqrt(3)/2),(-R(1,2),-s.sqrt(3)/2)]
pt=[[R(15,32)*v for v in row] for row in nt]
fixtures.append(fixture('smooth support triangle',pt,nt))

# Polynomial scale expansions, independently expanded before unit-normal reduction.
t=s.symbols('t',positive=True);d=s.Matrix(s.symbols('d0:3'));ni=s.Matrix(s.symbols('i0:3'));nj=s.Matrix(s.symbols('j0:3'))
eq((t*d+nj).dot(t*d+nj)-1, t*t*d.dot(d)+2*t*d.dot(nj)+nj.dot(nj)-1,'ordered XY expansion')
v=t*d-ni+nj
eq(v.dot(v),t*t*d.dot(d)-2*t*d.dot(ni-nj)+(ni-nj).dot(ni-nj),'YY expansion')

# Family algebra and the two exact branch gaps.
a,b=s.symbols('a b',positive=True);q=s.sqrt(a*a+b*b);r=s.sqrt(2*a*a+4*b*b)
x=list(map(s.Matrix,[(a,b,a),(a,-b,-a),(-a,b,-a),(-a,-b,a)]))
for i in range(4):
    e=x[(i+1)%4]-x[i];eq(e.dot(e),4*q*q,'family squared side')
u=[(x[(i+1)%4]-x[i])/(2*q) for i in range(4)]
eq((u[-1]-u[0]).dot(u[-1]-u[0]),r*r/(q*q),'family turn norm')
for k,v in enumerate([a,2*b,a]):eq((u[-1]-u[0])[k],v/q,'family reflection numerator')
z,Q=s.symbols('z Q',real=True)
Asq=(1-z)*(1/s.sqrt(2+2*z)-Q)**2
Bsq=z*(2/s.sqrt(2+2*z)-Q)**2
F=(1+3*z)/(2+2*z)-s.sqrt(1+z)/(2*s.sqrt(2))+R(1,16)
eq((Asq+Bsq).subs(Q,R(1,4)),F,'family F formula')
eq(s.diff(F,z),1/(1+z)**2-1/(4*s.sqrt(2)*s.sqrt(1+z)),'family F derivative')
eq(F.subs(z,R(1,8)),R(43,144),'family branch two value')
pos(R(43,144)-R(1,4),'family branch two strict gap')
eq(R(7,8)*(R(2,3)-R(1,4))**2,R(175,1152),'family branch one value')
pos(R(175,1152)-R(1,8),'family branch one strict gap')
pos(R(31,12)-s.sqrt(3),'length two spatial negative control')

# Existing smooth support-function fixture, including the omitted exact rho bounds.
th=s.symbols('theta',real=True);h=R(1,2)-s.cos(3*th)/32
rho=s.simplify(h+s.diff(h,th,2));eq(h+h.subs(th,th+s.pi),1,'support constant width')
eq(rho,R(1,2)+s.cos(3*th)/4,'curvature radius')
eq(rho-R(1,4),(1+s.cos(3*th))/4,'curvature lower bound identity')
eq(R(3,4)-rho,(1-s.cos(3*th))/4,'curvature upper bound identity')
for ang in [0,2*s.pi/3,4*s.pi/3]:
    eq(h.subs(th,ang),R(15,32),'contact support value')
    eq(s.diff(h,th).subs(th,ang),0,'contact derivative')
odd=sum(s.sqrt(3)*(h.subs(th,ang)-R(1,2)) for ang in [0,2*s.pi/3,4*s.pi/3])
eq(odd,-3*s.sqrt(3)/32,'odd cancellation fails');pos(-odd,'odd failure nonzero')

# Read existing optimizer outputs; do not run the optimizer or add starts.
saved=json.loads((P/'search_four_results.json').read_text()); numeric=[]; discrepancies=[]
for record in saved['runs']:
    x=np.array(record['coordinates'],dtype=float)
    e=np.roll(x,-1,axis=0)-x;le=np.linalg.norm(e,axis=1);u=e/le[:,None]
    turn=np.roll(u,1,axis=0)-u;al=np.linalg.norm(turn,axis=1);n=turn/al[:,None]
    S=np.concatenate((x,x-n))
    # Include even the antipodal pairs omitted as tautologies by the author.
    allslack=min(1-np.dot(S[i]-S[j],S[i]-S[j]) for i in range(8) for j in range(i))
    slack=min(allslack,float((le-1e-5).min()),float((al-1e-5).min()))
    L=float(le.sum());volume=float(np.linalg.det(x[1:]))
    discrepancies.append([abs(L-record['length']),abs(slack-record['minimum_constraint_slack']),abs(volume-record['tetrahedron_six_volume'])])
    numeric.append({'run':record['run'],'length':L,'all_pair_minimum_slack':float(slack),
                    'meets_diagnostic_tolerance':bool(slack>=-1e-7),
                    'minimum_edge':float(le.min()),'minimum_turn':float(al.min())})
feasible=[v for v in numeric if v['meets_diagnostic_tolerance']]
rerun=json.loads(subprocess.check_output(['python',str(P/'verify_exact.py')]))
recorded=json.loads((P/'verify_exact_results.json').read_text())
ok(rerun==recorded,'author verifier result reproduces recorded JSON')
ok(sorted(v['run'] for v in numeric)==list(range(80)),'saved run index coverage')

result={'status':'PASS for audited partial claims only; original target unresolved',
        'independent_exact_assertions':assertions,'sympy':s.__version__,
        'manifest_entries':len(manifest),'manifest_sha256':hashlib.sha256((P/'SHA256SUMS').read_bytes()).hexdigest(),
        'author_exact_assertions_reproduced':rerun['assertions'],
        'fixtures':fixtures,
        'numerical_diagnostics':{'runs':len(numeric),'tolerance_feasible_count':len(feasible),
            'best':min(feasible,key=lambda v:v['length']),
            'maximum_saved_discrepancy_length_slack_volume':np.max(discrepancies,axis=0).tolist(),
            'noncertified':True,'optimizer_rerun':False}}
print(json.dumps(result,indent=2))
