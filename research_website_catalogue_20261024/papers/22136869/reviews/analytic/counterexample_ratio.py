"""Independent exact counterexample to the p12 forced e/d ratio statement.

No submitted verifier, certificate, or historical review is imported or read.
The formulas come directly from the published p12 ansatz and p6 equation (7).
The result refutes a derivation assertion, not the displayed collision theorem.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import datetime,hashlib,json,sys
import sympy as s

records=[]
def ck(label,condition):
    assert condition,label
    records.append(label)

# First reconstruct the two independent positive factorization conditions.
b,k,r,d=s.symbols('b k r d',positive=True)
one=s.Integer(1);tau=s.Rational(1,3)
U=[one,b*tau,b,tau];V=[one,b,b*tau,tau]
S=[one,k*d,d,r*d];T=[one,d,k*d,r*d]
def mixture(U,V,S,T,y,z):
    return (S[y]*S[z]*U[y^z]+S[y]*T[z]*U[y]*V[z]
            +T[y]*S[z]*U[z]*V[y]+T[y]*T[z]*V[y^z])/4
M=s.Matrix(4,4,lambda y,z:s.factor(mixture(U,V,S,T,y,z)))
eq1=s.factor(M[1,3]**2-M[0,1]**2*M[3,3])
eq2=s.factor(M[1,2]**2*M[3,3]-M[0,3]**2*M[1,1]**2)
ck('first factorization equation',eq1==b**2*d**4*r**2*(5*k*k-9)/81)
ck('ratio cancels from both positive conditions',s.degree(eq1,r)==s.degree(eq2,r)==2 and s.diff(s.cancel(eq1/r**2),r)==s.diff(s.cancel(eq2/r**2),r)==0)

# Independent algebraic-field arithmetic for an actual admissible alternative.
hs=s.root(s.Rational(1,5),4);F=s.QQ.algebraic_field(hs);h=F.from_sympy(hs)
f=lambda n,den=1:F.convert(s.Rational(n,den));one=f(1);zero=f(0)
ck('positive quartic root relation',5*h**4==one)
K=[one,f(1,2),f(1,2),f(1,2)]
U=[one,h/3,h,f(1,3)];V=[one,h,h/3,f(1,3)]
S=[one,3*h*h/4,f(1,4),f(1,4)]
T=[one,f(1,4),3*h*h/4,f(1,4)]
P=[one,(5*h**3+h)/4,(5*h**3+h)/4,h*h]
B=[one,h*h/2,h*h/2,5*h*h/12]
alpha=[K[i]*K[i]*P[i] for i in range(4)]
beta=[K[i]*B[i] for i in range(4)]
ck('ansatz has d=e=1/4 and hence e/d=1',S[2]==S[3]==f(1,4) and S[3]/S[2]==one)
ck('ratio differs from claimed forced 6/5',S[3]/S[2]!=f(6,5))
ck('ansatz has kappa=3/sqrt5',S[1]/S[2]==3*h*h)
for y,z in product(range(4),repeat=2):
    ck(f'exact core factorization {y}{z}',mixture(U,V,S,T,y,z)==P[y^z]*B[y]*B[z])

# Rational interval bounds, not decimal approximations, certify positivity.
# h is the positive root of 5x^4-1; 2/3<h<7/10.
lo,hi=Q(2,3),Q(7,10)
ck('root isolation lower',5*lo**4<1)
ck('root isolation upper',5*hi**4>1)
def interval_add(a,b):return (a[0]+b[0],a[1]+b[1])
def interval_mul(a,b):
    z=[x*y for x in a for y in b];return min(z),max(z)
def bound(a):
    z=(Q(0),Q(0))
    for c in a.to_list():
        cc=Q(int(c.numerator),int(c.denominator))
        z=interval_add(interval_mul(z,(lo,hi)),(cc,cc))
    return z
chars=[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
def row(a):return [sum((a[g]*chars[g][j] for g in range(4)),zero)/4 for j in range(4)]
intervals={}
for label,a in [('K',K),('U',U),('V',V),('S',S),('T',T),('E1',[v*v for v in K]),('tree_alpha',alpha),('tree_beta',beta)]:
    ck(label+' normalized identity character',a[0]==one)
    for i,v in enumerate(a[1:],1):
        ck(f'{label} eigenvalue {i} strictly between zero and one',bound(v)[0]>0 and bound(one-v)[0]>0)
    rr=row(a);ck(label+' transition row sums to one',sum(rr,zero)==one)
    for i,v in enumerate(rr):
        z=bound(v);ck(f'{label} transition probability {i} strictly positive',z[0]>0)
        intervals[f'{label}.p{i}']=list(map(str,z))

# Literal retained-graph descendant sums: all 64 coordinates, including zeros.
arcs=[('rho','l1','K'),('rho','u','K'),('u','p','U'),('u','q','V'),
      ('p','r2','S'),('q','r2','T'),('p','r3','S'),('q','r3','T'),
      ('r2','l2','K'),('r3','l3','K')]
vecs={'K':K,'U':U,'V':V,'S':S,'T':T}
def graph_fourier(labels):
    if labels[0]^labels[1]^labels[2]:return zero
    total=zero
    for a,c in product(['p','q'],repeat=2):
        kept=[edge for edge in arcs if not (edge[1]=='r2' and edge[0]!=a) and not (edge[1]=='r3' and edge[0]!=c)]
        children={}
        for u,v,n in kept:children.setdefault(u,[]).append(v)
        def descend(v):
            if v in ['l1','l2','l3']:return labels[int(v[-1])-1]
            out=0
            for w in children.get(v,[]):out^=descend(w)
            return out
        val=one
        for u,v,n in kept:val*=vecs[n][descend(v)]
        total+=val/4
    return total
fourier={}
for xyz in product(range(4),repeat=3):
    val=graph_fourier(xyz);tree=alpha[xyz[0]]*beta[xyz[1]]*beta[xyz[2]] if xyz[0]^xyz[1]^xyz[2]==0 else zero
    ck('graph/tree Fourier equality '+str(xyz),val==tree);fourier[xyz]=val
probs=[]
for ijk in product(range(4),repeat=3):
    val=sum((q*chars[x][ijk[0]]*chars[y][ijk[1]]*chars[z][ijk[2]] for (x,y,z),q in fourier.items()),zero)/64
    ck('pattern probability positive '+str(ijk),bound(val)[0]>0);probs.append(val)
ck('all pattern probabilities normalize',sum(probs,zero)==one)

out={'status':'EXACT_COUNTEREXAMPLE_TO_FORCED_RATIO_CONFIRMED','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'checks':len(records),'check_labels':records,'claim_location':'Published main PDF p12, paragraph after Theorem12; TeX lines414-422',
     'statement_refuted':'Positive ansatz plus tau=1/3 and core tree factorization forces e/d=6/5.',
     'counterexample':{'h':'positive root of 5h^4-1','tau':'1/3','b':'h','kappa':'3h^2','d':'1/4','e':'1/4','e_over_d':'1',
                      'U':'(1,h/3,h,1/3)','V':'(1,h,h/3,1/3)','S':'(1,3h^2/4,1/4,1/4)','T':'(1,1/4,3h^2/4,1/4)',
                      'P':'(1,(5h^3+h)/4,(5h^3+h)/4,h^2)','B':'(1,h^2/2,h^2/2,5h^2/12)','factorization':'M[y,z]=P[y xor z]*B[y]*B[z]'},
     'independent_symbolic_equations':{'eq1':str(eq1),'eq2':str(eq2)},'rational_transition_bounds':intervals,
     'scope':'Refutes the stated necessity of e/d=6/5 only. Does not refute the chosen e/d=6/5 witness or the main collision/rank/IFT/grafting theorems; those latter global certificate chains were not completed after this stopping defect.',
     'python':sys.version,'sympy':s.__version__,'submitted_code_or_certificates_imported':False}
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path(__file__).with_name('counterexample_ratio_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','checks','statement_refuted','scope']},indent=2))
