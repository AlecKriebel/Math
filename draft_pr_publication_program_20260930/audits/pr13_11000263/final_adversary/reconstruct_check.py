#!/usr/bin/env python3
"""Independent direct-word and mutation checks for PR13, without verifier imports."""
from pathlib import Path
import hashlib, json, datetime
import sympy as S

ROOT = Path(__file__).resolve().parent
q, u, amp, t, z = S.symbols('q u amp t z')
checks = []
mutations = []

def normalize(a):
    return a.applyfunc(S.cancel) if isinstance(a, S.MatrixBase) else S.cancel(a)

def equal(name, a, b):
    d = normalize(a-b)
    assert d == (S.zeros(*d.shape) if isinstance(d, S.MatrixBase) else 0), name
    checks.append(name)

def unequal(name, a, b):
    d = normalize(a-b)
    assert d != (S.zeros(*d.shape) if isinstance(d, S.MatrixBase) else 0), name
    mutations.append({'check':name,'nonzero_entry':next((str(S.factor(x)) for x in d if x != 0),str(d)) if isinstance(d,S.MatrixBase) else str(S.factor(d))})

def matrices(m, U):
    out = {}
    for i in range(1,m):
        a = S.eye(m)
        a[i-1:i+1,i-1:i+1] = S.Matrix([[1-U,U],[1,0]])
        out[i] = a
    return out

def words(b, m):
    def word(indices):
        out = S.eye(m)
        for i in indices: out = out*b[i]
        return out
    return word

def construct(m,Q,U):
    b = matrices(m,U); word = words(b,m); I = S.eye(m)
    x = {2:normalize(Q*b[1].inv()+(1-Q)*I-b[1])}
    for k in range(3,m+1):
        x[k] = normalize((Q**(k-1)*word(range(k-1,0,-1)).inv()-word(range(1,k)))*x[k-1])
    return b,word,x

def rows(m,Q,b,word,x,prefix):
    equal(prefix+' exceptional R2',(Q*b[2].inv()+(1-Q)*S.eye(m)-b[2])*x[2],
          (Q*word([2,1]).inv()-word([1,2]))*x[2])
    for k in range(3,m):
        lhs = Q**(k-1)*word(range(k,1,-1)).inv()-word(range(2,k+1))
        rhs = Q**(k-1)*word(range(k,0,-1)).inv()-word(range(1,k+1))
        equal(prefix+f' legal R{k}',lhs*x[k],rhs*x[k])

# Arbitrary amplitude local identities avoid any dependence on a guessed rank.
b=matrices(3,u); P=b[1]; T=b[2]; w=S.Matrix([amp,-amp/u,0])
equal('local forward',P*T*w,S.Matrix([0,amp,-amp/u]))
equal('local inverse with whole-word order',P.inv()*T.inv()*w,S.Matrix([0,amp/u,-amp/u**2]))
equal('left block inverse',P.inv()*P,S.eye(3))
equal('right block inverse',P*P.inv(),S.eye(3))
equal('braid identity',P*T*P,T*P*T)
unequal('incorrect inverse order changes local vector',T.inv()*P.inv()*w,P.inv()*T.inv()*w)

symbolic_cases=[]
for m in (3,4,5,6):
    b,word,x=construct(m,q,u)
    rows(m,q,b,word,x,f'symbolic m={m}')
    lam=S.Matrix([[-1,1]+[0]*(m-2)])
    c=S.Integer(1)
    for k in range(2,m+1):
        c*=q**(k-1)-u
        v=S.zeros(m,1); v[k-2]=u**(2-k); v[k-1]=-u**(1-k)
        equal(f'm={m} formula X{k}',x[k],c*v*lam)
    equal(f'm={m} X3 entry',x[3][1,0],-(q-u)*(q**2-u)/u)
    assert normalize(x[3][1,0])!=0
    checks.append(f'm={m} generic X3 nonzero')
    equal(f'm={m} first twist',b[1]*x[2],-u*x[2])
    equal(f'm={m} full twist on X3',word([1,2])**3*x[3],u**3*x[3])
    equal(f'm={m} u=q kills X2',x[2].subs(u,q),S.zeros(m))
    equal(f'm={m} u=q^2 kills X3',x[3].subs(u,q**2),S.zeros(m))
    if m>=4:
        equal(f'm={m} u=q^3 kills X4',x[4].subs(u,q**3),S.zeros(m))
        assert normalize(x[3][1,0].subs(u,q**3))!=0
        checks.append(f'm={m} Laurent q^3 retains generic X3')
    symbolic_cases.append({'matrix_strands':m,'A_index':m,'C_index':m-1 if m>=4 else None,'legal_rows':list(range(2,m)),'X4_defined':m>=4})

# Mutations that a shallow verifier might miss.
b,word,x=construct(4,q,u)
bad_X3=normalize((q**2*b[2].inv()*b[1].inv()-b[1]*b[2])*x[2])
unequal('reversing inverse factors changes recursive X3',bad_X3,x[3])
generic_row2=(q*word([2]).inv()-word([2])-q*word([2,1]).inv()+word([1,2]))*x[2]
unequal('omitting exceptional (1-q)I fails R2',generic_row2,S.zeros(4))
left3=q**2*word([3,2]).inv()-word([2,3])
right3=q**2*word([3,2,1]).inv()-word([1,2,3])
unequal('sign-corrupted terminal C3 row fails',left3*x[3],-right3*x[3])
unequal('full twist is not scalar on entire unreduced module',word([1,2])**3,u**3*S.eye(4))
unequal('arbitrary independent twist t fails',b[1]*x[2],t*x[2])

# Rational controls are evaluations of the integral Laurent model, not maps F->Q.
numerical_cases=[]
params=[(-2,-8),(-1,-1),(-1,2),(1,3),(0,2),(S.Rational(2,3),S.Rational(8,27)),(2,4)]
for m in (3,4,7,10):
    for Q,U in params:
        b,word,x=construct(m,Q,U)
        rows(m,Q,b,word,x,f'numeric m={m},q={Q},u={U}')
        expected3=0 if U in {Q,Q**2} else 1
        assert x[3].rank()==expected3
        checks.append(f'numeric m={m},q={Q},u={U} rank X3')
        if m>=4:
            expected4=0 if U in {Q,Q**2,Q**3} else 1
            assert x[4].rank()==expected4
            checks.append(f'numeric m={m},q={Q},u={U} rank X4')
        numerical_cases.append({'matrix_strands':m,'q':str(Q),'u':str(U),'rank_X3':expected3,
                                'within_inherited_source_units':Q not in {0,1}})
equal('determinant excludes u=0',P.det(),-u)
assert P.subs(u,0).det()==0
checks.append('u=0 singular and inadmissible')

# Scalar obstructions, including the exceptional algebraic q=s control.
x2=q/z+1-q-z
x3=(q**2/z**2-z**2)*x2
x4=(q**3/z**3-z**3)*x3
r2=q/z+1-q-z-q/z**2+z**2
r3=q**2/z**2-z**2-q**2/z**3+z**3
r4=q**3/z**3-z**3-q**3/z**4+z**4
equal('scalar X2 factorization',x2,(1-z)*(z+q)/z)
equal('scalar R2 factorization',r2,(z**2-q)*(z**2-z+1)/z**2)
equal('scalar R3 factorization',r3,(z-1)*(q**2+z**5)/z**3)
equal('scalar R4 factorization',r4,(z-1)*(q**3+z**7)/z**4)
def reduce_sixth(expr):
    num,den=S.fraction(S.cancel(expr))
    f=z**2-z+1
    return S.rem(S.rem(num,f,z)*S.invert(S.rem(den,f,z),f,z),f,z)
equal('scalar q=s exceptional R3',reduce_sixth(r3.subs(q,z)),0)
equal('scalar q=s exceptional X4=2X3',reduce_sixth((x4-2*x3).subs(q,z)),0)
equal('scalar q=-s kills X2',normalize(x2.subs(q,-z)),0)
residual=reduce_sixth((r4*x4).subs(q,z))
equal('scalar next row residual',residual,4-8*z)
assert S.rem(4-8*z,z**2-z+1,z)!=0
checks.append('scalar nonzero residual rules out fifth strand')

output={'status':'passed','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'sympy_version':S.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'equality_or_boundary_assertions':len(checks),'mutation_failures_detected':len(mutations),
        'checks':checks,'mutations':mutations,'symbolic_cases':symbolic_cases,'numerical_cases':numerical_cases,
        'scope':'Finite direct-word checks and adversarial controls supplement independently reconstructed all-index proof. Numeric q=0,1 are outside inherited source units; all numerical q values evaluate an integral Laurent model, never the entire rational-function field.'}
(ROOT/'reconstruction_results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in {'checks','mutations','numerical_cases','symbolic_cases'}},indent=2))
