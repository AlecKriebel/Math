#!/usr/bin/env python3
"""Exact finite audit diagnostics; no analytic or formal-proof certification."""
import json
import sympy as s
checks = []
def require(name, condition):
    if condition is not True and condition != True:
        raise RuntimeError(name)
    checks.append(name)
def kron(*factors):
    return s.kronecker_product(*factors)
def clifford(n):
    m = n // 2
    X=s.Matrix([[0,1],[1,0]])
    Y=s.Matrix([[0,-s.I],[s.I,0]])
    Z=s.diag(1,-1); I=s.eye(2)
    out=[]
    for j in range(m):
        for P in [X,Y]:
            out.append(s.I*kron(*([Z]*j+[P]+[I]*(m-j-1))))
    if n%2:
        out.append(s.I*kron(*([Z]*m)))
        volume=s.I**((n+1)//2)*s.prod(out)
        if volume == -s.eye(2**m):out[-1]=-out[-1]
    return out
for n in [3,5]:
    C=clifford(n); d=C[0].rows; I=s.eye(d); J=s.eye(d*d)
    for i in range(n):
        require(f'n{n}_skew_{i}',C[i].H==-C[i])
        for j in range(n):
            require(f'n{n}_clifford_{i}_{j}', C[i]*C[j]+C[j]*C[i]==(-2*I if i==j else s.zeros(d)))
    require(f'n{n}_volume',s.I**((n+1)//2)*s.prod(C)==I)
    V=C[-1]; T=C[0]
    chi=-kron(V.T,V); L=s.I*kron(I,V*T); normal=kron(I,V)
    require(f'n{n}_chi_self_adjoint',chi.H==chi)
    require(f'n{n}_chi_involution',chi*chi==J)
    require(f'n{n}_L_self_adjoint',L.H==L)
    require(f'n{n}_L_involution',L*L==J)
    require(f'n{n}_symbol_anticommutes',L*chi+chi*L==s.zeros(d*d))
    require(f'n{n}_normal_commutes',normal*chi==chi*normal)
    require(f'n{n}_half_boundary_rank',(chi-J).rank()==d*d//2)
    require(f'n{n}_complementing_symbol', (L-J).col_join(chi-J).rank()==d*d)
    identity=s.Matrix([I[i,j] for j in range(d) for i in range(d)])
    require(f'n{n}_identity_plus_kernel',chi*identity==identity)
    anti=s.zeros(0,d*d)
    intertwine_opposite=s.zeros(0,d*d)
    for Cj in C:
        anti=anti.col_join(kron(I,Cj)+kron(Cj.T,I))
        intertwine_opposite=intertwine_opposite.col_join(kron(I,Cj)-kron((-Cj).T,I))
    require(f'n{n}_odd_anticommutant_zero',anti.rank()==d*d)
    require(f'n{n}_opposite_module_rejects_identity',intertwine_opposite*identity!=s.zeros(n*d*d,1))
# Negative mathematical controls: omitted hypotheses change the algebra or critical scaling.
C=clifford(2); volume=C[0]*C[1]
require('even_volume_nonzero',volume!=s.zeros(2))
require('even_volume_anticommutes',all(volume*Cj+Cj*volume==s.zeros(2) for Cj in C))
a,k,r=s.symbols('a k r',positive=True)
lo=s.exp(-2*k);hi=s.exp(-k)
log_norm_sq=s.simplify(s.integrate(2*s.pi/(k*k*r),(r,lo,hi)))
require('log_transverse_norm_exact',log_norm_sq==2*s.pi/k)
require('log_transverse_norm_vanishes',s.limit(log_norm_sq,k,s.oo)==0)
naive=s.simplify(s.integrate(2*s.pi*r/s.exp(-2*k),(r,s.exp(-k)/2,s.exp(-k))))
require('ordinary_cutoff_not_small',naive==3*s.pi/4)
codim2=s.simplify(s.integrate(2/(k*k*r*r),(r,lo,hi)))
require('codim_two_same_L2_method_diverges',s.limit(codim2,k,s.oo)==s.oo)
# Interior-only face homeomorphism has a degenerate pullback at the corner.
x=s.symbols('x',nonnegative=True)
require('singular_corner_map_detected',s.diff(x**3,x).subs(x,0)==0)
# Opposite interior/exterior convention breaks the contraction comparison.
require('correct_angle_contraction',s.Rational(2,3)/s.Rational(3,4)<=1)
require('reversed_angle_not_contraction',s.Rational(3,4)/s.Rational(2,3)>1)
print(json.dumps({'passed_checks':len(checks),'check_names':checks,'arithmetic':'SymPy exact integer, rational, Gaussian and symbolic arithmetic','sympy_version':s.__version__,'analytic_scope':'Finite convention and scaling diagnostics only; not a PDE, compactness, index, or formal proof certificate.'},indent=2,sort_keys=True))
