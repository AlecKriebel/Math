#!/usr/bin/env python3
"""Independent exact checks of the new source's finite algebra.

Symbolic equalities and finite rational regressions are deliberately counted
separately. This program neither parses Lean nor verifies any analytic,
extremal, compactness, or arbitrary-input theorem.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports' / 'source_completion'
Q = s.Rational
J = s.diag(1, -1, -1, -1)
rays = [s.eye(4)[:, j] for j in range(4)] + [s.Matrix([1, 1, -1, -1])]
u = s.Matrix([1, 1, 0, 0])
records: list[dict[str, str]] = []


def eq(name: str, lhs, rhs, kind: str = 'symbolic_identity') -> None:
    d = lhs-rhs
    entries = list(d) if isinstance(d, s.MatrixBase) else [d]
    bad = [s.cancel(s.expand(v)) for v in entries]
    if any(v != 0 for v in bad):
        raise AssertionError(f'{name}: {bad}')
    records.append({'name': name, 'kind': kind})


def pauli(v):
    t, x, y, z = v
    return s.Matrix([[t+z, x-s.I*y], [x+s.I*y, t-z]])


def coords(A):
    return s.Matrix([s.re(A[0, 0]+A[1, 1])/2,
                     s.re(A[0, 1]), -s.im(A[0, 1]),
                     s.re(A[0, 0]-A[1, 1])/2]).applyfunc(s.expand)


def gram(p):
    a, b, c, d = p
    e = a+b+c+d-Q(1, 2)
    return s.Matrix([[0,Q(1,2),a,b],[Q(1,2),0,c,d],[a,c,0,e],[b,d,e,0]])


def variation(h):
    a,b,c,d = h
    e = a+b+c+d
    return s.Matrix([[0,0,a,b],[0,0,c,d],[a,c,0,e],[b,d,e,0]])


def seed(c):
    a,b,d,e,f = c
    z = (f-a-b-d-e)/4
    return s.Matrix([[a/2,z,0,0],[z,b/2,0,0],[0,0,d/2,0],[0,0,0,e/2]])


def mass(P):
    return (u.T*P*u)[0]


def quad(G, x):
    return (x.T*G*x)[0]


def polar(z, x):
    return s.Matrix([[1+z,x],[x,1-z]])/2


def pauli_suite():
    x=s.Matrix(s.symbols('x0:4', real=True)); y=s.Matrix(s.symbols('y0:4', real=True))
    eq('pauli_decode_encode', coords(pauli(x)), x)
    eq('pauli_hermitian', pauli(x).H, pauli(x))
    eq('pauli_trace', s.trace(pauli(x)), 2*x[0])
    eq('pauli_determinant', pauli(x).det(), quad(J,x))
    eq('pauli_trace_product', s.trace(pauli(x)*pauli(y)), 2*(x.T*y)[0])
    cr=s.symbols('cr0:4', real=True); ci=s.symbols('ci0:4', real=True)
    C=s.Matrix(2,2,[a+s.I*b for a,b in zip(cr,ci)])
    vv=s.Matrix(list(C))
    rho=vv*vv.H
    eq('pure_density_trace',s.trace(rho),s.trace(C*C.H))
    lhs=s.trace(rho*s.kronecker_product(pauli(x),pauli(y)))
    rhs=s.trace(pauli(x)*C*pauli(y).T*C.H)
    eq('complex_born_steering',lhs,rhs)
    wrong=s.trace(pauli(x)*C*pauli(y)*C.H)
    if s.expand(lhs-wrong)==0:
        raise AssertionError('Missing-Bob-transpose mutation was not rejected')
    records.append({'name':'missing_Bob_transpose_rejected','kind':'negative_control'})
    T=C*pauli(y).T*C.H
    eq('steered_determinant',T.det(),C.det()*s.conjugate(C.det())*pauli(y).det())
    E=s.Matrix(4,4,s.symbols('e0:16',real=True))
    Y=s.Matrix(4,4,s.symbols('y0:16',real=True))
    S=J*E*Y/2
    P=E.T*J*E*Y
    for i in range(4):
        for j in range(4):
            eq(f'frame_probability_{i}_{j}',s.trace(pauli(E[:,i])*pauli(S[:,j])),P[i,j])
    for j in range(4):
        eq(f'frame_steering_square_{j}',quad(J,S[:,j]),quad(E.T*J*E,Y[:,j])/4)


def incidence_suite():
    p=s.Matrix(s.symbols('p0:4')); h=s.Matrix(s.symbols('h0:4'))
    c=s.Matrix(s.symbols('c0:5')); G=gram(p); H=variation(h)
    eq('metric_affine_difference',gram(p+h)-G,H)
    eq('metric_unit',quad(G,u),1)
    for j,r in enumerate(rays):
        eq(f'coefficient_null_{j}',quad(G,r),0)
        eq(f'five_value_seed_{j}',2*quad(seed(c),r),c[j])
    t=s.symbols('t')
    y=s.Matrix(s.symbols('v0:4')); z=s.Matrix(s.symbols('w0:4'))
    f=quad(G+t*H,y+t*z)
    derivative=2*(y.T*G*z)[0]+quad(H,y)
    eq('universal_null_product_derivative',s.diff(f,t).subs(t,0),derivative)
    P=s.Matrix(4,4,s.symbols('Y0:16')); Z=s.Matrix(4,4,s.symbols('Z0:16'))
    D=s.diff((G+t*H)*(P+t*Z),t).subs(t,0)
    eq('universal_block_product_derivative',D,H*P+G*Z)
    eq('universal_mass_derivative',s.diff(mass((G+t*H)*(P+t*Z)),t).subs(t,0),mass(H*P+G*Z))
    # The exact finite gap, before null/metric stationarity are imposed, has
    # precisely these two constraint residuals; this avoids assuming the
    # desired equality when constructing the independent check.
    gp=s.symbols('g0:10'); Gp=s.Matrix([[gp[0],gp[1],gp[2],gp[3]],
      [gp[1],gp[4],gp[5],gp[6]],[gp[2],gp[5],gp[7],gp[8]],
      [gp[3],gp[6],gp[8],gp[9]]])
    yp=s.Matrix(s.symbols('new0:4'))
    eq('exact_gap_residual_certificate',
       -2*(y.T*Gp*yp)[0]+2*quad(G,y)-quad(Gp,yp-y),
       -quad(Gp,yp)+quad(G,y)-quad(Gp-G,y))
    E=s.Matrix(4,4,s.symbols('E0:16')); D=s.Matrix(4,4,s.symbols('D0:16'))
    eq('gram_product_derivative',s.diff((E+t*D).T*J*(E+t*D),t).subs(t,0),D.T*J*E+E.T*J*D)
    lam=s.symbols('lambda')
    eq('gram_scalar_homogeneity',quad(G,t*z),t*t*quad(G,z))


def cone_suite():
    n=s.Matrix([0,*s.symbols('n1:4')]); x=s.Matrix(s.symbols('x0:4'))
    a=(n.T*x)[0]; xp=x-a*n
    eq('compression_residual_certificate',quad(J,xp)-quad(J,x)-a*a,(1-(n.T*n)[0])*a*a)
    y=s.Matrix(s.symbols('y0:4'))
    eq('pairing_compression_residual',(y.T*xp)[0]-(y.T*x)[0],-a*(y.T*n)[0])
    T,r=s.symbols('T r'); d=s.Matrix([0,*s.symbols('d1:4')]); e0=s.eye(4)[:,0]
    plus=(T+r)*(e0+d)/2; minus=(T-r)*(e0-d)/2
    eq('null_split_sum',plus+minus,T*e0+r*d)
    eq('null_plus_residual',quad(J,plus),(T+r)**2*(1-(d.T*d)[0])/4)
    eq('null_minus_residual',quad(J,minus),(T-r)**2*(1-(d.T*d)[0])/4)
    # Exact rational cases include zero vector, boundary rays, time axis,
    # non-collinear directions, and the negative spatial direction.
    normals=[s.Matrix([0,0,0,1]),s.Matrix([0,Q(3,5),Q(4,5),0])]
    directions=[s.Matrix([0,1,0,0]),s.Matrix([0,0,0,1])]
    for ni,(normal,direction) in enumerate(zip(normals,directions)):
        for ti in range(5):
            for rr in range(-ti,ti+1):
                v=ti*e0+rr*direction
                rho=s.sqrt(sum(v[j]**2 for j in range(1,4)))
                dd=direction if rho==0 else s.Matrix([0,v[1],v[2],v[3]])/rho
                pieces=[(ti+rho)*(e0+dd)/2,(ti-rho)*(e0-dd)/2]
                eq(f'cone_case_{ni}_{ti}_{rr}_sum',sum(pieces,s.zeros(4,1)),v,'rational_regression')
                for j,w in enumerate(pieces):
                    eq(f'cone_case_{ni}_{ti}_{rr}_{j}_null',quad(J,w),0,'rational_regression')
                    eq(f'cone_case_{ni}_{ti}_{rr}_{j}_plane',(normal.T*w)[0],0,'rational_regression')
                    if w[0]<0: raise AssertionError('Negative future coordinate')


def physical_suite():
    rng=random.Random(21699161)
    eye=s.eye(2); zero=s.zeros(2); py=s.Matrix([[0,-s.I],[s.I,0]])
    aux=[s.Matrix([[16,-4],[-4,1]])/25,s.Matrix([[1,-4],[-4,16]])/25,s.Matrix([[8,8],[8,8]])/25]
    A=[[(eye+py)/2,(eye-py)/2,zero],aux]
    E=s.Matrix.hstack(coords(A[0][0]),coords(A[0][1]),coords(A[1][0]),coords(A[1][1]))
    G=E.T*J*E
    eq('physical_frame_metric',G,gram([G[0,2],G[0,3],G[1,2],G[1,3]]),'rational_regression')
    if E.det()==0: raise AssertionError('Frame not full rank')
    eq('physical_frame_unit',E*u,s.eye(4)[:,0],'rational_regression')
    Cs=[s.diag(Q(3,5),Q(4,5)),s.Matrix([[1,s.I],[1,-s.I]])/2,s.diag(Q(5,13),Q(12,13))]
    Us=[eye,s.Matrix([[Q(3,5),Q(4,5)],[-Q(4,5),Q(3,5)]])]
    case=0
    for C in Cs:
        for U in Us:
            eq(f'unitary_{case}',U*U.H,eye,'rational_regression')
            B=[[U*b*U.H for b in block] for block in A]
            S=s.Matrix.hstack(*[coords(C*N.T*C.H) for N in [B[0][0],B[0][1],B[1][0],B[1][1]]])
            P=2*E.T*S; Y=G.inv()*P
            eq(f'physical_mass_{case}',mass(P),1,'rational_regression')
            for j,r in enumerate(rays):
                eq(f'physical_null_{case}_{j}',quad(G,Y*r),0,'rational_regression')
                if (E*Y*r)[0]<=0: raise AssertionError('Nonfuture physical ray')
            # Explicit right inverse of all SIX constraint derivatives.
            for trial in range(3):
                targets=s.Matrix([rng.randint(-5,5) for _ in range(5)])
                mass_target=s.Integer(rng.randint(-5,5))
                Z0=P.T.inv()*seed(targets)
                Z=Z0+(mass_target-mass(G*Z0))*Y
                for j,r in enumerate(rays):
                    eq(f'jacobian_preimage_{case}_{trial}_{j}',2*(r.T*Y.T*G*Z*r)[0],targets[j],'rational_regression')
                eq(f'jacobian_mass_{case}_{trial}',mass(G*Z),mass_target,'rational_regression')
                raw=s.Matrix(4,4,[rng.randint(-3,3) for _ in range(16)]); H=raw+raw.T
                D=J*E.T.inv()*H/2
                eq(f'gram_preimage_{case}_{trial}',D.T*J*E+E.T*J*D,H,'rational_regression')
            # Complete complex-qubit whitening, with rational Hermitian positive
            # roots chosen directly rather than using a numerical eigensolver.
            R=s.Matrix([[2,s.I],[-s.I,2]])/3
            Ri=R.inv()
            for ai,M in enumerate(aux):
                for bi,N in enumerate(aux):
                    eq(f'whitening_pair_{case}_{ai}_{bi}',
                      s.trace((Ri.H*M*Ri)*(R*(C*N.T*C.H)*R.H)),
                      s.trace(M*C*N.T*C.H),'rational_regression')
            case+=1


def strengthened_suite():
    a,b,z,x,k=s.symbols('a b z x k',real=True)
    C=s.diag(a,b); vv=s.Matrix(list(C)); rho=vv*vv.H
    aux=[s.Matrix([[k*k,k],[k,1]])/2,s.Matrix([[k*k,-k],[-k,1]])/2,s.diag(1-k*k,0)]
    A=[[polar(z,x),polar(-z,-x),s.zeros(2)],
       [polar(-z,x),polar(z,-x),s.zeros(2)],aux]
    B=[[polar(0,1),polar(0,-1)],[polar(1,0),polar(-1,0)]]
    def born(i,j,u,v): return s.trace(rho*s.kronecker_product(A[i][u],B[j][v]))
    def corr(i,j): return sum((-1 if u==1 else 1)*(1 if v==0 else -1)*born(i,j,u,v) for u in range(3) for v in range(2))
    val=10*(corr(0,0)+corr(0,1)+corr(1,0)-corr(1,1))+Q(3,5)*(born(2,0,0,0)+born(2,0,1,1))+Q(4,5)*born(2,1,2,0)
    wanted=40*x*a*b+20*z*(a*a+b*b)+Q(3,10)*(k*a+b)**2+Q(4,5)*(1-k*k)*a*a
    eq('strengthened_full_Born_polynomial',val,wanted)
    for i in range(3): eq(f'strengthened_A_normalization_{i}',sum(A[i],s.zeros(2)),s.eye(2))
    for j in range(2): eq(f'strengthened_B_normalization_{j}',sum(B[j],s.zeros(2)),s.eye(2))
    G0=s.Matrix([[k,1],[k,1]])/2; G1=s.Matrix([[k,-1],[k,-1]])/2
    eq('strengthened_auxiliary_Gram0',G0.H*G0,aux[0]);eq('strengthened_auxiliary_Gram1',G1.H*G1,aux[1])
    eq('strengthened_auxiliary_scaled_projection',(1-k*k)*polar(1,0),aux[2])
    for j in range(3):eq(f'strengthened_auxiliary_determinant_{j}',aux[j].det(),0)
    q=s.symbols('q',positive=True)
    asq=(q+1)/(2*q); bsq=(q-1)/(2*q)
    def even_substitute(expr):
        return s.cancel(s.expand(s.cancel(expr)).subs({a*a:asq,b*b:bsq}))
    def mod_q(name,expr):
        num,den=s.fraction(s.cancel(expr)); rem=s.rem(num,q*q-7813,q)
        eq(name,rem,0)
        if den==0: raise AssertionError('Zero rational-function denominator')
    eq('strengthened_state_normalization',asq+bsq,1)
    mod_q('strengthened_q_product',q*q*asq*bsq-1953)
    mod_q('strengthened_observable_normalization',(q/125)**2+4*q*q*asq*bsq/125**2-1)
    full=even_substitute(wanted.subs({z:q/125,x:2*q*a*b/125,k:3*b/(5*a)}))
    mod_q('strengthened_attained_value',full-(16+8*q)/25)
    # Exact square comparisons, avoiding floating-point radical evaluations.
    eq('strengthened_vs_simple_square_margin',64*7813-500**2*2,32)
    if not (7813>1 and 64*7813>500**2*2): raise AssertionError('Square comparison failed')
    eq('stronger_appendix_integer_certificate',960**2*7813-56782**2,3976265276)


SUITES={'pauli':pauli_suite,'incidence':incidence_suite,'cone':cone_suite,'physical':physical_suite,'strengthened':strengthened_suite}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite',choices=[*SUITES,'all'],default='all')
    args=parser.parse_args()
    chosen=SUITES if args.suite=='all' else {args.suite:SUITES[args.suite]}
    OUT.mkdir(parents=True,exist_ok=True)
    report_path=OUT/f'exact_{args.suite}.json'
    report={'status':'in_progress','lean_compiled':False,'lean_kernel_checked':False,
      'scope':'finite algebra only; does not verify general physical reductions or analysis',
      'suite':args.suite,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'sympy_version':s.__version__}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    try:
        for name,fn in chosen.items():
            fn()
            print(f'{name}: passed',flush=True)
    except Exception as exc:
        report.update(status='failed',error=str(exc),records=records)
        report_path.write_text(json.dumps(report,indent=2)+'\n')
        raise
    counts={kind:sum(r['kind']==kind for r in records) for kind in ('symbolic_identity','rational_regression','negative_control')}
    report.update(status='passed',counts=counts,records=records)
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','suite','counts','lean_kernel_checked')},indent=2))

if __name__=='__main__':main()
