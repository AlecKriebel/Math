#!/usr/bin/env python3
"""Independent exact controls. Finite algebra checks supplement the analytic proof.

No files, network, or external services are used. Assertions are intentionally
absent, so guards remain effective under python -O. Negative mutations are
deliberate in-memory alterations and must exit 4 with InvalidClaim.
"""
import argparse
import json
import sys

import sympy as s


class InvalidClaim(RuntimeError):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--corrupt', choices=(
        'connection_sign', 'covariant_sign', 'drop_second_covariant_slot',
        'holonomy_half', 'geodesic_sign', 'pseudo_potential_cubic',
        'pretend_local_positive_descends', 'pretend_indefinite_is_positive'))
    args = parser.parse_args()
    checks = []

    def exact(name, expression, expected=0):
        difference = s.simplify(expression - expected)
        if difference != 0:
            raise InvalidClaim(name + ': nonzero exact residual ' + str(difference))
        checks.append(name)

    def matrix(name, actual, expected):
        if actual.shape != expected.shape:
            raise InvalidClaim(name + ': shape mismatch')
        for i in range(actual.rows):
            for j in range(actual.cols):
                exact(f'{name}_{i}_{j}', actual[i, j], expected[i, j])

    x, y, t, u, v, m, n, p, q = s.symbols('x y t u v m n p q', real=True)
    z = (x, y)
    A, B, C = (s.Function(name)(x, y) for name in ('A', 'B', 'C'))
    g = s.Matrix([[A, B], [B, C]])
    gamma = [[[s.Integer(0) for k in range(2)] for j in range(2)] for i in range(2)]
    gamma[1][0][0] = -t if args.corrupt == 'connection_sign' else t

    def dg(tensor, i, j, k):
        first = sum(gamma[a][i][j] * tensor[a, k] for a in range(2))
        second = sum(gamma[a][i][k] * tensor[j, a] for a in range(2))
        sign = 1 if args.corrupt == 'covariant_sign' else -1
        if args.corrupt == 'drop_second_covariant_slot':
            second = 0
        return s.diff(tensor[j, k], z[i]) + sign * (first + second)

    cov_expected = [
        [[s.diff(A,x)-2*t*B, s.diff(B,x)-t*C],
         [s.diff(B,x)-t*C, s.diff(C,x)]],
        [[s.diff(A,y), s.diff(B,y)], [s.diff(B,y), s.diff(C,y)]]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                exact(f'covariant_{i}_{j}_{k}', dg(g,i,j,k), cov_expected[i][j][k])

    e0 = s.diff(B,x)-s.diff(A,y)-t*C
    e1 = s.diff(C,x)-s.diff(B,y)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                expected = 0 if i == j else (1 if i == 0 else -1)*(e0 if k == 0 else e1)
                exact(f'codazzi_{i}_{j}_{k}', dg(g,i,j,k)-dg(g,j,i,k), expected)
    exact('global_exterior_derivative', s.diff(B,x)-s.diff(A,y)-e0, t*C)

    for a in range(2):
        for i in range(2):
            for j in range(2):
                exact(f'torsion_{a}_{i}_{j}', gamma[a][i][j]-gamma[a][j][i])
                for k in range(2):
                    curvature = s.diff(gamma[a][j][k],z[i])-s.diff(gamma[a][i][k],z[j])
                    curvature += sum(gamma[a][i][b]*gamma[b][j][k]-gamma[a][j][b]*gamma[b][i][k] for b in range(2))
                    exact(f'curvature_{a}_{i}_{j}_{k}', curvature)
    omega = s.Matrix([[0,1],[-1,0]])
    for i in range(2):
        for j in range(2):
            for k in range(2):
                exact(f'parallel_area_{i}_{j}_{k}', dg(omega,i,j,k))

    F = s.Matrix([x, y+t*x*x/2])
    J = F.jacobian(z)
    exact('developing_jacobian', J.det(), 1)
    inverse = s.Matrix([u, v-t*u*u/2])
    matrix('developing_inverse', F.subs({x:inverse[0],y:inverse[1]},simultaneous=True), s.Matrix([u,v]))
    for i in range(2):
        for j in range(2):
            column = J.inv()*s.Matrix([s.diff(F[a],z[i],z[j]) for a in range(2)])
            for a in range(2):
                exact(f'pullback_connection_{a}_{i}_{j}',column[a], gamma[a][i][j])

    def rho(mm,nn,U,V):
        half = 1 if args.corrupt == 'holonomy_half' else s.Rational(1,2)
        return s.Matrix([U+mm,V+nn+t*mm*U+half*t*mm*mm])
    matrix('deck_equivariance',F.subs({x:x+m,y:y+n},simultaneous=True),rho(m,n,F[0],F[1]))
    inner = rho(p,q,u,v)
    matrix('holonomy_composition',rho(m,n,inner[0],inner[1]),rho(m+p,n+q,u,v))
    H = rho(m,n,u,v).jacobian((u,v))
    matrix('linear_holonomy',H,s.Matrix([[1,0],[t*m,1]]))
    exact('linear_holonomy_volume',H.det(),1)
    exact('linear_holonomy_nontrivial_shear',H[1,0].subs(m,1),t)

    time, x0, y0, aa, bb = s.symbols('time x0 y0 aa bb',real=True)
    factor = 1 if args.corrupt == 'geodesic_sign' else -1
    trajectory = s.Matrix([x0+aa*time,y0+bb*time+factor*t*aa*aa*time*time/2])
    for a in range(2):
        accel = s.diff(trajectory[a],time,2)
        accel += sum(gamma[a][i][j]*s.diff(trajectory[i],time)*s.diff(trajectory[j],time) for i in range(2) for j in range(2))
        exact(f'complete_geodesic_{a}',accel)
    matrix('developed_geodesic_line',F.subs({x:trajectory[0],y:trajectory[1]},simultaneous=True),
           s.Matrix([x0+aa*time,y0+t*x0*x0/2+(bb+t*x0*aa)*time]))

    # A global nondegenerate indefinite counter-control.
    pseudo = s.Matrix([[0,1],[1,0]])
    for i in range(2):
        for j in range(2):
            for k in range(2):
                exact(f'indefinite_codazzi_{i}_{j}_{k}',dg(pseudo,i,j,k)-dg(pseudo,j,i,k))
    exact('indefinite_determinant',pseudo.det(),-1)
    coefficient = s.Rational(1,6) if args.corrupt == 'pseudo_potential_cubic' else s.Rational(1,3)
    potential = u*v-coefficient*t*u**3
    matrix('indefinite_affine_hessian_pullback',J.T*s.hessian(potential,(u,v)).subs(u,x)*J,pseudo)
    increment = potential.subs({u:rho(m,n,u,v)[0],v:rho(m,n,u,v)[1]},simultaneous=True)-potential
    exact('indefinite_potential_affine_increment',increment,m*v+(n+t*m*m/2)*u+m*n+t*m**3/6)
    for i in (u,v):
        for j in (u,v):
            exact(f'potential_increment_second_derivative_{i}_{j}',s.diff(increment,i,j))
    if args.corrupt == 'pretend_indefinite_is_positive':
        exact('false_positive_indefinite_claim',pseudo[1,1],1)

    # Positive Euclidean metric in developing coordinates: valid only on cover.
    local_positive = J.T*J
    matrix('local_positive_components',local_positive,s.Matrix([[1+t*t*x*x,t*x],[t*x,1]]))
    exact('local_positive_determinant',local_positive.det(),1)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                exact(f'local_positive_codazzi_{i}_{j}_{k}',dg(local_positive,i,j,k)-dg(local_positive,j,i,k))
    failure = local_positive.subs(x,x+1)-local_positive
    matrix('local_positive_descent_failure',failure,s.Matrix([[t*t*(2*x+1),t],[t,0]]))
    exact('local_positive_failed_periodic_cross_coefficient',failure[0,1],t)
    if args.corrupt == 'pretend_local_positive_descends':
        exact('false_local_positive_descent_claim',failure[0,1])

    # Constant-tensor/zero-mode tests, not a replacement for positivity/Stokes.
    Abar, Bbar, Cbar, kk, ll = s.symbols('Abar Bbar Cbar kk ll',real=True)
    constant = s.Matrix([[Abar,Bbar],[Bbar,Cbar]])
    exact('averaged_codazzi_obstruction',dg(constant,0,1,0)-dg(constant,1,0,0),-t*Cbar)
    for parameter in (s.Integer(0),s.Integer(1),s.Integer(-1),s.Rational(1,1000000000),-s.Rational(1,1000000000)):
        exact('parameterized_obstruction_'+str(parameter),(-t*Cbar).subs(t,parameter),-parameter*Cbar)
    fourier0 = 2*s.pi*s.I*(kk*Bbar-ll*Abar)-t*Cbar
    fourier1 = 2*s.pi*s.I*(kk*Cbar-ll*Bbar)
    exact('fourier_zero_mode_first',fourier0.subs({kk:0,ll:0}),-t*Cbar)
    exact('fourier_zero_mode_second',fourier1.subs({kk:0,ll:0}))
    central = s.eye(2)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                exact(f'central_positive_codazzi_{i}_{j}_{k}',(dg(central,i,j,k)-dg(central,j,i,k)).subs(t,0))
    semidefinite = s.Matrix([[s.Function('a')(x),0],[0,0]])
    for i in range(2):
        for j in range(2):
            for k in range(2):
                exact(f'degenerate_semidefinite_codazzi_{i}_{j}_{k}',dg(semidefinite,i,j,k)-dg(semidefinite,j,i,k))

    # Distinct cover-potential / commuting affine-cocycle mechanism.
    la, lb, lc, pd, pe, pf = s.symbols('la lb lc pd pe pf',real=True)
    L = la*u+lb*v+lc
    P = pd*u+pe*v+pf
    shear = rho(1,0,u,v)
    vertical = rho(0,1,u,v)
    cocycle = L.subs({u:shear[0],v:shear[1]},simultaneous=True)-L
    cocycle -= P.subs({u:vertical[0],v:vertical[1]},simultaneous=True)-P
    exact('commuting_cocycle_residual',cocycle,la+lb*t*u+lb*t/2-pe)
    exact('commuting_cocycle_positive_increment_obstruction',s.diff(cocycle,u),lb*t)
    exact('commuting_cocycle_vertical_coefficient',s.diff(cocycle,v))
    sigma = s.symbols('sigma',real=True)
    exact('cubic_parameter_connection_coefficient',gamma[1][0][0].subs(t,sigma**3),sigma**3)
    exact('cubic_parameter_developing_coefficient',F[1].subs(t,sigma**3),y+sigma**3*x*x/2)
    exact('cubic_parameter_real_period_cubed',(-sigma)**3,-sigma**3)

    print(json.dumps({'verdict':'PASS','check_count':len(checks),'checks':checks,
                      'symbolic_parameter':'all real t',
                      'analytic_dependency':'periodic lift/global alpha + Stokes + C>0; proved in REPORT.md',
                      'assertions_used':False,'writes_files':False,'external_service_calls':0},sort_keys=True,indent=2))


if __name__ == '__main__':
    try:
        main()
    except InvalidClaim as exc:
        print('InvalidClaim: '+str(exc),file=sys.stderr)
        sys.exit(4)
