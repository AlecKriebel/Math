#!/usr/bin/env python3
"""Independent exact audit, no import or execution of authored verifier code.
Finite checks supplement the analytic audit; exact infinite-order certificates
are checked, rather than inferring infinite order from long finite orbits.
"""
from pathlib import Path
from fractions import Fraction
from copy import deepcopy
from itertools import product
import hashlib, json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'frozen'
report={'arithmetic':'Python integers/Fractions and exact SymPy polynomial algebra', 'checks':[]}
def record(name, **data): report['checks'].append(dict(name=name,passed=True,**data))

# Independent scalar-sequence implementation; tangent rows are advanced with
# the scalar sequence, not by multiplying the author's step matrices.
def strict_replay(cert):
    n=6; values=list(cert['initial']); rows=[list(row) for row in s.eye(n).tolist()]
    wins=[]; gaps=[]
    for offset in range(cert['period']):
        opts=[(values[offset+j],j) for j in cert['support']]
        if cert['constant']: opts.append((0,-1))
        high=max(v for v,j in opts)
        chosen=[j for v,j in opts if v==high]
        assert len(chosen)==1, ('non-strict comparison',offset,opts)
        j=chosen[0]; gaps.append(high-max(v for v,q in opts if q!=j)); wins.append(j)
        values.append(high-values[offset])
        winner=[0]*n if j==-1 else rows[offset+j]
        rows.append([winner[q]-rows[offset][q] for q in range(n)])
    final=values[-6:]; matrix=s.Matrix(rows[-6:])
    assert final==cert['initial'], ('not a return', final)
    assert wins==cert['winners'], 'winner sequence mismatch'
    assert matrix.tolist()==cert['return_matrix'], 'return matrix mismatch'
    assert min(gaps)==cert['minimum_strict_margin']
    return matrix, wins, gaps

certs=json.loads((SOURCE/'turn02_verification.json').read_text())['strict_cycle_certificates']
t=s.Symbol('t')
for c in certs:
    M,w,g=strict_replay(c)
    poly=M.charpoly(t).as_expr(); assert s.expand(poly-s.sympify(c['characteristic_polynomial']))==0
    if c['name']=='bd_no_constant':
        cubic=t**3-4*t**2+3*t-1
        assert s.expand(poly-(t-1)**3*cubic)==0
        assert cubic.subs(t,3)<0<cubic.subs(t,4)
        obstruction='A real eigenvalue lies in (3,4).'
    elif c['name']=='bd_with_constant':
        cubic=t**3+7*t-1
        assert s.expand(poly-(t-1)**3*cubic)==0
        assert cubic.subs(t,0)<0<cubic.subs(t,1)
        obstruction='A real eigenvalue lies in (0,1).'
    else:
        if c['constant']: u=s.Matrix([0,0,1,0,-1,-1]); v=s.Matrix([2,-1,0,-1,0,0])
        else: u=s.Matrix([1,1,0,0,1,-1]); v=s.Matrix([0,0,-1,-1,-1,-1])
        N=M-s.eye(6)
        assert N==u*v.T and N!=s.zeros(6) and (v.T*u)[0]==0 and N*N==s.zeros(6)
        obstruction='M=I+N with N nonzero and N squared zero, so M^n=I+nN.'
    record(c['name'],period=c['period'],strict_minimum=min(g),characteristic_polynomial=str(s.factor(poly)),infinite_order_reason=obstruction)

# Audit's controls catch edited certificates before any conclusion.
for field in ['winner','matrix','period','constant']:
    wrong=deepcopy(certs[1] if field=='constant' else certs[0])
    if field=='winner': wrong['winners'][0]=1
    elif field=='matrix': wrong['return_matrix'][0][0]+=1
    elif field=='period': wrong['period']-=1
    else: wrong['constant']=False
    try: strict_replay(wrong)
    except AssertionError: pass
    else: raise AssertionError('mutated certificate accepted: '+field)
record('mutation_controls',rejected=['wrong winner','wrong matrix entry','truncated return time','wrong constant status'])

# An exact algebraic field represented by degree <=2 polynomials in alpha,
# alpha^3-alpha^2-1=0. Signs are certified by rational interval arithmetic.
a=s.Symbol('a'); minimal=a**3-a*a-1
low=Fraction(1); high=Fraction(3,2)
def reduce(expr): return s.rem(s.Poly(expr,a),s.Poly(minimal,a)).as_expr()
def field_sign(expr):
    global low,high
    expr=reduce(expr)
    if expr==0:return 0
    coefficients=[Fraction(c) for c in s.Poly(expr,a).all_coeffs()]
    while True:
        L=H=Fraction(0)
        for c in coefficients:
            vals=[L*low,L*high,H*low,H*high]; L=min(vals)+c;H=max(vals)+c
        if L>0:return 1
        if H<0:return -1
        mid=(low+high)/2; val=mid**3-mid**2-1
        if val<0: low=mid
        else: high=mid

def tangent_iterate(base,direction,support,constant,count):
    z=list(base);v=list(direction);ties_list=[]; chosen_list=[]; positive_gaps=[]
    for offset in range(count):
        opts=[(z[offset+j],j,v[offset+j]) for j in support]
        if constant:opts.append((0,-1,s.Integer(0)))
        top=max(b for b,j,d in opts)
        tied=[(j,d) for b,j,d in opts if b==top]
        j,d=tied[0]
        for j2,d2 in tied[1:]:
            if field_sign(d2-d)>0:j,d=j2,d2
        for j2,d2 in tied:
            sign=field_sign(d-d2); assert sign>=0
            if j2!=j:positive_gaps.append(str(reduce(d-d2)))
        z.append(top-z[offset]); v.append(reduce(d-v[offset]))
        ties_list.append([j for j,d in tied]);chosen_list.append(j)
    return z[-6:],v[-6:],ties_list,chosen_list,positive_gaps

for name,support,vector,expected_ties in [
    ('bc',[1,2,4,5],[a-1,0,-1,0,a*a-a,0],[[2],[1,2,5],[1,4,5],[4]]),
    ('cd',[2,3,4],[0,a-1,0,-1,0,a*a-a],[[2,3],[2],[4],[3,4]])]:
    for const in [False,True]:
        base=[0,0,1,1,0,0]
        z,v,ties,winners,gaps=tangent_iterate(base,vector,support,const,4)
        assert z==base and ties==expected_ties
        assert all(reduce(vi-a*wi)==0 for vi,wi in zip(v,vector))
        assert any(wi!=0 for wi in vector)
        record(name+'_expanding_tangent_'+str(const),base_ties=ties,automatically_selected_winners=winners,gaps=gaps,
            multiplier='alpha>1, alpha^3-alpha^2-1=0')
        # Positive scaling stays on the same tangent ray (homogeneity).
        _,v2,_,_,_=tangent_iterate(base,v,support,const,4)
        assert all(reduce(vi-a*a*wi)==0 for vi,wi in zip(v2,vector))
# Reversing an eigenvector is unsafe for a piecewise-linear tangent map:
# maxima reverse branch preferences. This deliberate false ray is rejected.
false_ray=[1-a,0,1,0,a-a*a,0]
_,false_image,_,false_winners,_=tangent_iterate([0,0,1,1,0,0],false_ray,[1,2,4,5],False,4)
assert any(reduce(vi-a*wi)!=0 for vi,wi in zip(false_image,false_ray))
record('invalid_expanding_ray_control',candidate='Negative of the valid bc eigenray',rejected=True,actual_winners=false_winners)
record('algebraic_sign_interval',alpha_enclosure=[str(low),str(high)],method='Exact rational interval bisection; no floating point.')

# Derive the entire {1,5} tangent return symbolically from its base orbit.
u,v,c,d,e,f,h=s.symbols('u v c d e f h',real=True)
start=s.Matrix([u,v,c,d,e,f]); delta=s.Matrix([0,0,-1,0,1,0]);base=[0,0,1,0,1,0]
for const in [False,True]:
    z=base[:];w=list(start);ties=[]
    for offset in range(5):
        opts=[(z[offset+j],w[offset+j],j) for j in [1,5]]
        if const:opts.append((0,s.Integer(0),-1))
        mx=max(x[0] for x in opts); chosen=[x for x in opts if x[0]==mx]
        ties.append([x[2] for x in chosen])
        z.append(mx-z[offset]); w.append(s.Max(*[x[1] for x in chosen])-w[offset])
    assert z[-6:]==base
    m=s.Max(v,f,0) if const else s.Max(v,f)
    expected=s.Matrix([f,m-u,c-v,-v,e-d,-d]); actual=s.Matrix(w[-6:])
    assert all(s.simplify(x)==0 for x in actual-expected)
    equiv=actual.subs({c:c-h,e:e+h},simultaneous=True)-actual-h*delta
    assert equiv==s.zeros(6,1)
    initial=s.Matrix([0,0,0,-1,0,0]);values=initial;orbit=[]
    for _ in range(3):
        values=actual.subs(dict(zip(start,values)),simultaneous=True);orbit.append(list(values))
    assert values==initial+delta
    record('b_symbolic_tangent_'+str(const),base_ties=ties,derived_return=str(actual),three_return_orbit=[[int(x) for x in q] for q in orbit],equivariance=True)

# Mask exhaustiveness is independent of arbitrary coefficient magnitudes.
all_masks={tuple(j for j,on in zip('bcd',bits) if on) for bits in product([False,True],repeat=3)}
excluded={('b',),('b','c'),('b','d'),('c','d'),('b','c','d')}
classical={(),('c',),('d',)}
assert len(all_masks)==8 and excluded.isdisjoint(classical) and excluded|classical==all_masks
record('exhaustive_support_partition',excluded=[list(q) for q in sorted(excluded)],surviving=[list(q) for q in sorted(classical)],constant_statuses=2,excluded_cases=10)

# The order-two boundary return is derived anew by rational recurrence.
x,y,A=s.symbols('x y A',positive=True);vals=[x,y]
for _ in range(5):vals.append(s.cancel((A+vals[-1])/vals[-2]))
Hx,Hy=vals[-2:]; hx0=s.cancel(Hx).subs(x,0);hy0=s.cancel(Hy).subs(x,0)
assert hx0==0 and s.cancel(hy0-A*y)==0
assert s.factor(s.denom(Hx).subs(x,0))==(A+y)**2
assert s.factor(s.denom(Hy).subs(x,0))==(A+y)**2
assert s.cancel(s.cancel(Hx/x).subs(x,0)-(A*y+1)/(A+y))==0
record('lynness_boundary_extension',image=['0','A*y'],both_boundary_denominators='(A+y)^2',parameter_necessity='For A>0, finite order implies A^p=1 and hence A=1.')

# Additional controls: nonidentity does not imply infinite order, and
# unit-circle eigenvalues do not imply a matrix is finite-order.
rotation=s.Matrix([[0,-1],[1,0]])
assert rotation!=s.eye(2) and rotation**4==s.eye(2)
unipotent=s.Matrix([[1,1],[0,1]])
assert s.expand(unipotent.charpoly(t).as_expr()-(t-1)**2)==0
assert unipotent!=s.eye(2) and (unipotent-s.eye(2))**2==s.zeros(2)
record('finite_order_logic_controls',nonidentity_finite_order_example=rotation.tolist(),unit_circle_infinite_order_example=unipotent.tolist())

# Exact odd two-cycle determinant identity without symmetry: this verifies
# the algebraic Floquet formula; symmetry is used separately for equal sums.
for k in [3,5,7]:
    m=(k-1)//2;coeff=s.symbols('a1:'+str(k)); u,v=s.symbols('u v',nonzero=True)
    E=sum(coeff[2*r-1]*t**r for r in range(1,m+1));O=sum(coeff[2*r]*t**r for r in range(m))
    H=t**(m+1)*O-E;C=E**2-t*O**2
    def D(first,second):
        rows=[]
        for i in range(k-1): rows.append([int(j==i+1) for j in range(k)])
        rows.append([-second/first]+[q/first for q in coeff]);return s.Matrix(rows)
    char=(D(v,u)*D(u,v)).charpoly(t).as_expr()
    assert s.cancel(char-(t**k-1-((u+v)*H+C)/(u*v)))==0
record('odd_floquet_formula_without_symmetry',orders=[3,5,7])

# Direct six-dimensional exact checks for sufficient periods, including all
# five surviving families, are independent of a claimed dilation theorem.
from fractions import Fraction as Q
initial=[Q(2),Q(3),Q(5),Q(7),Q(11),Q(13)]
for name,period,num in [('identity',6,None),('reciprocal',12,(Q(4),Q(0),Q(0))),('homogeneous_d',18,(Q(0),Q(0),Q(3))),('lyness_d',15,(Q(9),Q(0),Q(3))),('lyness_c',16,(Q(9),Q(3),Q(0)))]:
    z=initial[:];returns=[]
    for n in range(1,period+1):
        nxt=z[0] if num is None else (num[0]+num[1]*(z[2]+z[4])+num[2]*z[3])/z[0]
        z=z[1:]+[nxt]
        if z==initial: returns.append(n)
    assert returns==[period]
    record('survivor_positive_data_'+name,first_return=period,role='Consistency and least-period witness, not a substitute for the base rational identities.')

report['all_passed']=True
(ROOT/'checks'/'independent_results.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print(json.dumps({'all_passed':True,'check_count':len(report['checks']),'output':'checks/independent_results.json'},indent=2))
