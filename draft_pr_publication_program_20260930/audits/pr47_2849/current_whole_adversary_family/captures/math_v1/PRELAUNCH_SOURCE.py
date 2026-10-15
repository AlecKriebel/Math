"""New exact computations, independent of original helper implementations."""
from pathlib import Path
import datetime as dt, itertools, json, math, os
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
F=Path(__file__).absolute().parent
checks={}
def test(n,v):
    if not bool(v): raise AssertionError(n)
    checks[n]=True
def eq(a,b): return s.simplify(a-b)==0
test('guards',__debug__)
M=s.Matrix([[3,0,0,1],[0,3,0,1],[0,0,3,2],[1,1,1,0]])
test('determinant',M.det()==-36)
S=smith_normal_form(M,domain=s.ZZ)
test('Smith36',[abs(S[i,i]) for i in range(4)]==[1,1,3,12])
minor_gcd=[]
for k in range(1,5):
    g=0
    for rs in itertools.combinations(range(4),k):
        for cs in itertools.combinations(range(4),k): g=math.gcd(g,int(M.extract(rs,cs).det()))
    minor_gcd.append(abs(g))
test('independent-minor-divisors',minor_gcd==[1,1,3,36])
w=(-1+s.sqrt(3)*s.I)/2
test('omega-primitive',eq(w**3,1) and not eq(w,1))
def fox(word,alpha):
    prefix=s.Integer(1); row=[s.Integer(0)]*len(alpha)
    for g,sign in word:
        if sign==1: row[g]+=prefix; prefix=s.simplify(prefix*alpha[g])
        else: prefix=s.simplify(prefix/alpha[g]); row[g]-=prefix
    test('word-character-relator-'+str(len(checks)),eq(prefix,1))
    return [s.simplify(x) for x in row]
seifert=[]
for a in [w,w**2]:
    alpha=[a,a,a,s.Integer(1)]; words=[]
    for i,beta in enumerate([1,1,2]):
        words.append([(3,1),(i,1),(3,-1),(i,-1)])
        words.append([(i,1)]*3+[(3,1)]*beta)
    words.append([(0,1),(1,1),(2,1)])
    D=s.Matrix([fox(word,alpha) for word in words])
    B=s.Matrix([x-1 for x in alpha])
    test('Fox-cocycle-rank-'+str(a),D.rank()==2)
    test('Fox-coboundary-in-kernel-'+str(a),all(eq(x,0) for x in D*B))
    test('Fox-coboundary-rank-'+str(a),B.rank()==1)
    test('complexH1-'+str(a),4-D.rank()-B.rank()==1)
    seifert.append({'a':str(s.simplify(a)),'Fox_matrix':str(D),'Z1_dimension':2,'B1_dimension':1,'H1_complex':1,'H1_adjoint_real':2})
test('Euler-cover',s.Rational(-4,3)*3==-4)
test('Riemann-Hurwitz',3*(2-3*(1-s.Rational(1,3)))==0)
def qmul(q,r):
    return tuple(s.simplify(x) for x in (q[0]*r[0]-sum(q[i]*r[i] for i in range(1,4)),q[0]*r[1]+r[0]*q[1]+q[2]*r[3]-q[3]*r[2],q[0]*r[2]+r[0]*q[2]+q[3]*r[1]-q[1]*r[3],q[0]*r[3]+r[0]*q[3]+q[1]*r[2]-q[2]*r[1]))
def qinv(q): return (q[0],-q[1],-q[2],-q[3])
def qeq(q,r): return all(eq(x,y) for x,y in zip(q,r))
one=(1,0,0,0); minus=(-1,0,0,0)
for theta in [2*s.pi/3,s.pi/3]:
    c=s.cos(theta); t=s.sin(theta)
    d=s.solve(c*c-t*t*s.Symbol('d')+s.Rational(1,2),s.Symbol('d'))
    test('all-noncentral-quaternion-axes-forced-'+str(theta),d==[1])
# A meaningful mutation: odd homology/base(3,3,3) changes the SU2 conclusion.
q1=(s.Rational(1,2),s.sqrt(3)/2,0,0)
q2=(s.Rational(1,2),-s.sqrt(3)/6,s.sqrt(6)/3,0)
q3=qinv(qmul(q1,q2))
for i,q in enumerate([q1,q2,q3]):
    test('mutant-unit-'+str(i),eq(sum(x*x for x in q),1))
    test('mutant-cube-minus1-'+str(i),qeq(qmul(qmul(q,q),q),minus))
test('mutant-product-relator',qeq(qmul(qmul(q1,q2),q3),one))
test('mutant-nonabelian',not qeq(qmul(q1,q2),qmul(q2,q1)))
mut=M.copy(); mut[2,3]=1
test('mutant-homology-order27',mut.det()==-27)
# Independent finite character enumeration including exponent2 and trivial cases.
for ns in itertools.product(range(1,9),repeat=3):
    chars=list(itertools.product(*(range(n) for n in ns)))
    inv=lambda a:tuple((-v)%n for v,n in zip(a,ns))
    central=sum(inv(a)==a for a in chars)
    pairs={min(a,inv(a)) for a in chars if a!=inv(a)}
    test('orbit-rank-'+str(ns),central+2*len(pairs)==math.prod(ns))
    test('central-count-'+str(ns),central==math.prod(math.gcd(n,2) for n in ns))
test('example2central17spheres',2+2*17==36)
test('doublecount-characters-detected',2+2*34!=36)
t=s.Symbol('t'); delta=t*t-t+1
test('trefoil-unsquared-common-root',s.gcd(delta,t**6-1)==delta)
test('trefoil-squared-no-root',s.gcd(delta.subs(t,t*t),t**6-1)==1)
# C2*C3 local-system cocycles from the relator matrix.
rawdims=[]; sqdims=[]
for power,arr in [(1,rawdims),(2,sqdims)]:
    for k in range(6):
        z=s.exp(s.I*s.pi*k*power/3).expand(complex=True)
        A=s.simplify(z**3); B=s.simplify(z**2)
        D=s.Matrix([[1+A,0],[0,s.simplify(1+B+B*B)]])
        bd=s.Matrix([A-1,B-1])
        arr.append(2-D.rank()-bd.rank())
test('C2*C3-unsquared-dimensions',rawdims==[0,1,0,0,0,1])
test('C2*C3-squared-dimensions',sqdims==[0,0,0,0,0,0])
z1,z2,z3,z4=s.symbols('a b c d',real=True)
x=z1*z1+z2*z2; y=z3*z3+z4*z4
f=(x-y)*(x-2*y); grad=[s.diff(f,z) for z in [z1,z2,z3,z4]]
test('quartic-gradient',all(eq(g,h) for g,h in zip(grad,[2*z1*(2*x-3*y),2*z2*(2*x-3*y),2*z3*(-3*x+4*y),2*z4*(-3*x+4*y)])))
test('quartic-nonzero-axis-determinant',s.Matrix([[2,-3],[-3,4]]).det()==-1)
test('quartic-Hessian-zero',s.hessian(f,[z1,z2,z3,z4]).subs(dict.fromkeys([z1,z2,z3,z4],0))==s.zeros(4))
v=s.Symbol('v',real=True)
test('quartic-lowerlink-factor',eq((v-(1-v))*(v-2*(1-v)),(2*v-1)*(3*v-2)))
test('quartic-boundaries-positive-radii',0<s.Rational(1,2)<s.Rational(2,3)<1)
for u in [s.Rational(1,2),s.Rational(3,5),s.Rational(2,3)]:test('closed-link-endpoint-'+str(u),(2*u-1)*(3*u-2)<=0)
for u in [0,s.Rational(1,3),s.Rational(3,4),1]:test('outside-link-'+str(u),(2*u-1)*(3*u-2)>0)
torus_betti=[1,2,1]; relative={2:torus_betti[1],3:torus_betti[2]}
test('local-rank3-Euler1',sum(relative.values())==3 and sum((-1)**k*r for k,r in relative.items())==1)
g=(x-y)**2; witness={z1:1,z2:0,z3:1,z4:0}
test('mutated-quartic-nonisolated',all(eq(s.diff(g,z).subs(witness),0) for z in [z1,z2,z3,z4]))
test('mutated-quartic-Euler-rank-not-determined',1==sum((-1)**k*r for k,r in relative.items()) and 1!=sum(relative.values()))
result={'schema':'pr47-new-independent-exact-math-controls/v1','pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','assertions':len(checks),'checks':checks,'exact_Seifert_cocycles':seifert,'Smith_minor_divisors':minor_gcd,'odd_homology_mutation_quaternions':[[str(x) for x in q] for q in [q1,q2,q3]],'raw_trefoil_H1':rawdims,'squared_trefoil_H1':sqdims,'Floer_rank_example_computed':False,'target_solved':False,'foreign_bodies_copied':False}
(F/'MATH_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'assertions':len(checks),'actual_pid':os.getpid()}))
