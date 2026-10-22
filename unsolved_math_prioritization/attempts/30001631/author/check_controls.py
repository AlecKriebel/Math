#!/usr/bin/env python3
"""Exact finite controls for RESEARCH.md; no sampled TZ-curvature computation."""
import json
import platform
import sympy as s


def zero(expr):
    assert s.simplify(expr) == 0, expr


def main():
    out = {
        'scope': 'Exact general-identity and model controls only. No actual TZ curvature sign is tested.',
        'python': platform.python_version(),
        'sympy': s.__version__,
        'tests': []
    }
    def record(name, **data):
        out['tests'].append({'name': name, 'passed': True, **data})

    # Fourier coefficient integral, divided by the common factor pi**(-5).
    coefficient = s.Rational(s.factorial(4), 4**5)
    assert coefficient == s.Rational(3, 128)
    finite_norm = sum(s.Rational(a*a, n**5) for n, a in enumerate([1,2,-3], 1))
    assert finite_norm == s.Rational(251, 216)
    record('cusp_Fourier_coefficient', coefficient_without_pi=str(coefficient),
           finite_normalized_norm=str(finite_norm),
           note='The finite coefficient example is not asserted to come from a finite-type surface.')

    # Positive sum defect for two real rational positive-definite Hermitian matrices.
    A=s.Matrix([[2,1],[1,3]])
    B=s.Matrix([[4,-1],[-1,2]])
    for M in [A,B,A+B]:
        assert M[0,0] > 0 and M.det() > 0
    a=s.Matrix([[1,2]])
    b=s.Matrix([[-2,3]])
    c=(a+b)*(A+B).inv()
    defect=(a*A.inv()*a.T+b*B.inv()*b.T-(a+b)*(A+B).inv()*(a+b).T)[0]
    squares=((a-c*A)*A.inv()*(a-c*A).T+(b-c*B)*B.inv()*(b-c*B).T)[0]
    zero(defect-squares)
    assert defect > 0
    common=s.Matrix([[2,-1]])
    ea,eb=common*A,common*B
    equality=(ea*A.inv()*ea.T+eb*B.inv()*eb.T-(ea+eb)*(A+B).inv()*(ea+eb).T)[0]
    zero(equality)
    record('sum_curvature_defect', defect=str(defect), squares=str(squares), equality_case=str(equality))

    # Fixed Hilbert-space holomorphic Gram curvature control.
    U=s.Matrix([[1,0],[0,1],[1,1]])
    d=s.Matrix([1,-2,4])
    G=U.T*U
    P=U*G.inv()*U.T
    R=(-d.T*d+d.T*U*G.inv()*U.T*d)[0]
    normal=(((s.eye(3)-P)*d).T*((s.eye(3)-P)*d))[0]
    zero(R+normal)
    assert R < 0
    record('Gram_projection_curvature', curvature=str(R), squared_normal=str(normal))

    z,zb,a,C,L,p=s.symbols('z zb a C L p', positive=True)
    psi=z*zb+a*(z*zb)**2
    g=s.diff(psi,z,zb)
    R=-s.diff(g,z,zb)+s.diff(g,z)*s.diff(g,zb)/g
    R0=s.simplify(R.subs({z:0,zb:0}))
    zero(R0+4*a)
    record('potential_fourth_jet', origin_curvature=str(R0))

    # Nonholomorphic smooth Gram representation does not imply nonpositive curvature.
    g=s.exp(-z*zb)
    R=-s.diff(g,z,zb)+s.diff(g,z)*s.diff(g,zb)/g
    assert s.simplify(R.subs({z:0,zb:0})) == 1
    record('smooth_Gram_positive_curvature', origin_curvature='1')

    # Delta_0 F(-log r)=F''(-log r)/r^2; express r as exp(-L).
    log_lambda=s.log(C)+2*L-p*s.log(L)
    K=-s.diff(log_lambda,L,2)*L**p/(2*C)
    zero(K+p*L**(p-2)/(2*C))
    record('cusp_model_curvature', curvature=str(s.simplify(K)), p4=str(s.simplify(K.subs(p,4))))

    # Radial distance for p=4, infinity minus lower endpoint.
    radial=s.integrate(s.sqrt(C)/L**2,L)
    zero(radial+s.sqrt(C)/L)
    record('p4_radial_length_primitive', primitive=str(radial))

    h=s.sin(L**3)/L
    h2=(2/L**3-9*L**3)*s.sin(L**3)
    zero(s.diff(h,L,2)-h2)
    record('oscillatory_metric_second_derivative', second_derivative=str(h2),
           positive_curvature_subsequence='L^3 = pi/2 + 2*pi*k, L>=1',
           negative_curvature_subsequence='L^3 = 3*pi/2 + 2*pi*k, L>=1')

    lam=1+4*z*zb
    K=-2/lam*s.diff(s.log(lam),z,zb)
    zero(K+8/(1+4*z*zb)**3)
    record('flat_ambient_negative_slice', Gaussian_curvature=str(s.factor(K)))

    # Scalar conformal comparison at a point, exact jet variables.
    f,w,fx,fy,fxx,fyy,wx,wy,wxx,wyy=s.symbols('f w fx fy fxx fyy wx wy wxx wyy')
    laplogf=(fxx+fyy)/f-(fx**2+fy**2)/f**2
    laplogw=(wxx+wyy)/w-(wx**2+wy**2)/w**2
    g=f*w
    gx=fx*w+f*wx
    gy=fy*w+f*wy
    gxx=fxx*w+2*fx*wx+f*wxx
    gyy=fyy*w+2*fy*wy+f*wyy
    Kg=-((gxx+gyy)/g-(gx**2+gy**2)/g**2)/(2*g)
    Kw=-laplogw/(2*w)
    zero(Kg-(Kw-laplogf/(2*w))/f)
    record('conformal_comparison', residual='0')

    # Determinant factorization underlying the Ricci comparison.
    W=s.Matrix([[2,1],[1,2]])
    G=s.Matrix([[3,-1],[-1,4]])
    detA=(W.inv()*G).det()
    assert detA>0 and G.det()==W.det()*detA
    record('determinant_comparison', det_W=str(W.det()), det_G=str(G.det()), det_A=str(detA))

    out['passed']=len(out['tests'])
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
