"""Fresh reaction-derived exact controls; no submitted code/certificates imported."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json
import sympy as s

C=Counter();details=[]
def check(v,label):
    if not v: raise RuntimeError(label)
    C[label]+=1
def zero(v): return all(s.cancel(x)==0 for x in v)
def network(m,a=s.S.One,b=s.S.One):
    n=m+1
    def v(d):return s.Matrix([d.get(i,0) for i in range(n)])
    rr=[(v({}),v({0:1}),a)]
    rr += [(v({0:1,i:1}),v({0:1,i+1:1}),a) for i in range(1,m-2)]
    rr += [(v({0:1,m-2:1}),v({m-1:2}),a),(v({m-1:2}),v({1:1}),a),(v({m:2}),v({0:1,m-1:1}),b),(v({0:1,m-1:1}),v({m:2}),b)]
    x=s.symbols('x:'+str(n));G=s.Matrix.hstack(*(target-source for source,target,k in rr));Y=s.Matrix.hstack(*(source for source,target,k in rr))
    f=s.zeros(n,1)
    for source,target,k in rr:f+=(target-source)*k*s.prod(x[i]**source[i] for i in range(n))
    A=f.jacobian(x).subs(dict.fromkeys(x,1))
    Hess=[s.hessian(f[i],x) for i in range(n)]
    def B(u,v):return s.Matrix([(u.T*H*v)[0] for H in Hess])
    return rr,x,G,Y,f,A,B
def hurwitz(poly):
    coeff=s.Poly(poly,lam).all_coeffs();n=len(coeff)-1
    H=s.Matrix(n,n,lambda i,j:coeff[2*j-i+1] if 0<=2*j-i+1<=n else 0)
    return all(H[:j,:j].det(method='domain-ge')>0 for j in range(1,n+1))
lam=s.symbols('lambda')

# Symbolic triad algebra, including positive equilibrium scaling.
a,b,h,k,z=s.symbols('a b h k z',positive=True)
T=s.Matrix([[-a-b,-b,2*b],[2*a-b,-4*a-b,2*b],[2*b,2*b,-4*b]])*s.diag(h,k,z)
co=T.charpoly(lam).all_coeffs();gap=s.Poly(s.expand(co[1]*co[2]-co[3]),a,b,h,k,z)
check(co[3]==16*a*a*b*h*k*z,'symbolic_triad_constant')
check(len(gap.terms())==14 and all(v>0 for _,v in gap.terms()),'symbolic_triad_14_term_gap')
check(s.Matrix([[-a-b,-a,-b],[-a,-a,2*a],[2*a-b,2*a,-4*a-b]]).det()==2*a*a*b,'symbolic_core_remainder')

for m in range(3,7):
    n=m+1;rr,x,G,Y,f,A,B=network(m)
    c=s.Matrix([0]+[4]*(m-2)+[2,1]);rho=s.Matrix([2]+[-2]*(m-2)+[0,1])
    check(len(rr)==m+2 and all(sum(y)<=2 and sum(q)<=2 for y,q,_ in rr),'binary_complex_and_reaction_count')
    check(G.rank()==m and len(G.nullspace())==2,'stoichiometric_rank_flux_dimension')
    check(zero(G*s.ones(m+2,1)) and zero(c.T*G) and zero(A*rho),'flux_conservation_kernel')
    check(A==G*Y.T and zero(f.subs(dict.fromkeys(x,1))),'reaction_jacobian_equilibrium')
    for av,bv in [(s.Rational(5,4),s.Rational(7,3)),(s.S.One,s.Integer(2))]:
        _,_,_,_,_,AA,_=network(m,av,bv);hs=[s.Rational(i+3,i+2) for i in range(n)];J=AA*s.diag(*hs)
        for order in range(1,m):
            for I in combinations(range(n),order):
                check(hurwitz(J.extract(I,I).charpoly(lam).as_expr()),'finite_all_principal_Hurwitz')
        for omit in range(n):
            I=[j for j in range(n) if j!=omit]
            got=(-1)**m*J.extract(I,I).det(method='domain-ge')
            expected=(-2*av**(m-1)*bv*s.prod(hs[:m]) if omit==m else 0 if omit in (0,m-1) else 16*av**(m-1)*bv*hs[m]*s.prod(hs[j] for j in range(m) if j!=omit))
            check(got==expected,'finite_complete_omission_table')
    # Reaction-level physical realization at arbitrary positive equilibrium.
    hs=[s.Rational(i+2,i+1) for i in range(n)];subs={x[i]:hs[i]*x[i] for i in range(n)};xs={x[i]:1/hs[i] for i in range(n)}
    physical=f.subs(subs,simultaneous=True)
    check(zero(physical.subs(xs)) and physical.jacobian(x).subs(xs)==A*s.diag(*hs),'physical_equilibrium_and_column_scaling')
    check(hurwitz(s.cancel(A.charpoly(lam).as_expr()/lam)),'finite_homogeneous_relative_Hurwitz')
    # Exact zero and near-threshold ray signs at unit equilibrium.
    dd=[s.S.One]*m+[s.Integer(8*(m-2))]
    check(sum(((-1)**m*A.extract([j for j in range(n) if j!=i],[j for j in range(n) if j!=i]).det())*dd[i] for i in range(n))==0,'strict_ray_boundary_beta_zero')
    check(8*(m-2)>1,'equal_diffusion_not_eligible')

for m in (3,4,5,7,9):
    n=m+1;rr,x,G,Y,f,A,B=network(m);nu=m-2
    c=s.Matrix([0]+[4]*(m-2)+[2,1]);rho=s.Matrix([2]+[-2]*(m-2)+[0,1])
    K=lambda i:s.Integer(91*m-181-i)
    r=s.Matrix([1]+[-K(i)/(63*nu) for i in range(2,m)]+[-s.Rational(2,9),s.Rational(5,14)])
    ell=s.Matrix([-s.Rational(266,815)]+[s.Rational(78260*nu,163)/K(i-1) for i in range(2,m)]+[s.Rational(18368,7335),1])
    d=[s.Rational(23,63)]+[1/K(i) for i in range(2,m)]+[s.Rational(1,7),s.Rational(16,45)];D=s.diag(*d)
    check(zero((A-D)*r) and zero(ell.T*(A-D)),'critical_right_left_exact')
    check((ell.T*r)[0]<0 and (ell.T*D*r)[0]<0,'transverse_simple_pairings')
    check((A-D).rank()==n-1,'critical_geometric_dimension')
    forcing=-B(r,r)/4
    augmented=A.col_join(c.T);w0=list(s.linsolve((augmented,forcing.col_join(s.Matrix([0])))))[0];w0=s.Matrix(w0)
    w2=(A-4*D).inv()*forcing
    check(zero(A*w0-forcing) and (c.T*w0)[0]==0 and zero((A-4*D)*w2-forcing),'direct_harmonic_solves')
    check(not zero(A*w0+B(r,r)/2),'wrong_Fourier_factor_countercontrol')
    num=(ell.T*(B(r,w0)+B(r,w2)/2))[0];cub=s.cancel(num/(ell.T*r)[0])
    check(num>s.Rational(1,100) and cub<0,'direct_cubic_sign_and_margin')
    hh=sum(1/K(j) for j in range(1,m-1));S=(ell.T*B(r,rho))[0]
    check(S==-4*(1760850*hh-10253)/462105 and -s.Rational(1,10)<S<0,'direct_gauge_contraction')
    L0=1/s.sqrt(3) if nu==1 else s.sqrt(5)/(2*s.sqrt(nu));L1=s.Rational(90*nu,90*nu+1)
    for L in (L0,L1):
        hs=[s.S.One]+[K(i)/(L*K(i-1)) for i in range(2,m)]+[s.S.One,s.S.One];H=s.diag(*hs);g=H.inv()*c
        ellscaled=H.inv()*ell;wL=w0-rho*(g.T*w0)[0]/(g.T*rho)[0]
        tau=s.simplify(-(g.T*w0)[0]/(g.T*rho)[0]);numL=s.simplify((ell.T*(B(r,wL)+B(r,w2)/2))[0])
        check(zero((H*(A-D))*r) and zero(ellscaled.T*H*(A-D)),'scaled_left_right_pairings')
        check(s.simplify((ellscaled.T*r)[0])<0 and numL>s.Rational(1,200),'scaled_simple_zero_cubic_margin')
        check(s.simplify((g.T*wL)[0])==0 and s.simplify(numL-num-tau*S)==0,'physical_mass_gauge_identity')
        check(tau<s.Rational(1,20),'gauge_upper_bound_control')
        physd=[s.simplify(hs[i]*d[i]) for i in range(n)]
        # Extreme-entry formulas are checked by exact comparisons with every entry.
        dmax=s.Rational(23,63);dmin=1/(91*nu*L);hmax=(91*nu-1)/(91*nu*L)
        check(all(s.simplify(t-dmin)>=0 and s.simplify(dmax-t)>=0 for t in physd),'physical_diffusion_extrema')
        check(all(s.simplify(t-1)>=0 and s.simplify(hmax-t)>=0 for t in hs),'equilibrium_extrema')
        check(s.simplify((dmax/dmin)*hmax-s.Rational(23,63)*(91*nu-1))==0,'fixed_contrast_product')
    if m==3:
        H=s.diag(1,s.Rational(4,3),1,1)
        check(not zero(ell.T*H*(A-D)) and zero((H.inv()*ell).T*H*(A-D)),'wrong_scaled_adjoint_countercontrol')
    if m<=5:
        for t in (1,4,9):
            p=(A-t*D).charpoly(lam).as_expr()
            check(hurwitz(s.cancel(p/lam) if t==1 else p),'finite_unit_allmode_complements')
    details.append({'m':m,'cubic':str(cub),'eta':str(s.cancel((ell.T*D*r)[0]/(ell.T*r)[0]))})

# Reconstruct all four all-dimensional modulus certificates directly from
# their printed formulas. Full supports are retained as fresh artifacts.
x,y,z,u,Apar=s.symbols('x y z u A',real=True);q=x+s.I*y;t=1+u
P=q**4+12*q**3+42*q**2+47*q+16;R=5*q**2+33*q+16
g1=q+2+s.Rational(23,63)*t;gm=q+5+t/7;gz=q+4+s.Rational(16,45)*t
F=g1*gm*gz-4*g1-4*gm+gz;GG=gz*(4*g1+gm)-36;F0=q**3+11*q**2+31*q+16
ab=lambda w:s.expand(w*s.conjugate(w))
expressions={'E35':ab(1+q)*ab(P)-ab(R),'E77':(s.Rational(91,90)**2+y*y)*ab(F)-ab(GG),'E84':s.Rational(91,90)**2*(1+Apar*x+y*y/3)*ab(F)-ab(GG),'E22':(1+(Apar+s.Rational(1,4))*x+s.Rational(5,4)*y*y)*ab(F0)-ab(R)}
certs={}
for name,expr in expressions.items():
    terms=s.Poly(s.expand(expr),x,y,u).terms();out=[]
    for powers,coef in terms:
        check(powers[1]%2==0,'modulus_even_imaginary_degree')
        check(all(c>0 for c in s.Poly(coef,Apar).coeffs()),'modulus_coefficient_nonnegative')
        out.append({'powers':[powers[0],powers[1]//2,powers[2]],'coefficient':str(coef)})
    check(len(terms)=={'E35':35,'E77':77,'E84':84,'E22':22}[name],'modulus_exact_support_count')
    check(s.expand(expr).subs({x:0,y:0,u:0})==0,'modulus_equality_origin')
    certs[name]=out
# A genuine sharp-certificate negative control, not a dynamical claim.
Bpar=s.symbols('B')
co=s.expand((1+Bpar*y*y)*ab(F0.subs(x,0))-ab(R.subs(x,0))).coeff(y,2)
check(co==256*Bpar-320 and co.subs(Bpar,1)<0,'homogeneous_certificate_5_over_4_boundary')

# General theorem includes n=2; reproduce a legal one-bad-minor example.
J=s.Matrix([[1,-2],[1,-2]]);D=s.diag(1,3);q=s.symbols('s',nonnegative=True)
check(s.expand((q*D-J).det())==3*q*q-q,'n2_ray_threshold_example')
check(s.diff((lam*s.eye(2)+q*D-J).det(),lam)==2*lam+4*q+1,'n2_characteristic_monotonicity')
out={'status':'PASS','exact_check_count':sum(C.values()),'families':dict(C),'direct_cubic_instances':details,'arithmetic':'SymPy exact rational/algebraic; no submitted helpers imported','scope':'Symbolic universal certificate controls plus finite reaction-derived instances; universal logical and functional-analytic arguments audited separately.'}
root=Path(__file__).parent
(root/'fresh_exact.json').write_text(json.dumps(out,indent=2)+'\n');(root/'fresh_modulus_coefficients.json').write_text(json.dumps(certs,indent=2)+'\n');print(json.dumps(out,indent=2))
