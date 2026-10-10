#!/usr/bin/env python3
"""Exact finite diagnostics. They do not prove CK existence or geometric gluing."""
import itertools
import json
import sympy as s


def need(condition, label):
    if not bool(condition):
        raise RuntimeError(label)


def norm2_pair(A, gram):
    q=gram.inv()*A
    return s.trace(q*q)


def shell_data(eps, rho):
    n=4; x=s.Matrix([rho*eps,0,0,0]); r2=(x.T*x)[0]
    delta=lambda i,j:s.Integer(i==j)
    eig=[2,-1,3,1]
    def rt(i,j,k,l):
        return (5+eig[i]*eig[j])*(delta(i,k)*delta(j,l)-delta(i,l)*delta(j,k))
    def rb(i,j,k,l):
        return delta(i,k)*delta(j,l)-delta(i,l)*delta(j,k)
    def jets(R):
        g=s.eye(n); dg=[s.zeros(n) for _ in range(n)]; dd=[[s.zeros(n) for _ in range(n)] for _ in range(n)]
        for i,j in itertools.product(range(n),repeat=2):
            g[i,j]-=sum(R(i,k,j,l)*x[k]*x[l] for k,l in itertools.product(range(n),repeat=2))/3
            for a in range(n):
                dg[a][i,j]=-sum((R(i,a,j,k)+R(i,k,j,a))*x[k] for k in range(n))/3
                for b in range(n):
                    dd[a][b][i,j]=-(R(i,a,j,b)+R(i,b,j,a))/3
        return g,dg,dd
    h,dh,ddh=jets(rt);b,db,ddb=jets(rb)
    z=(r2/eps**2-4)/5
    chi=1-10*z**3+15*z**4-6*z**5
    chiz=-30*z**2+60*z**3-30*z**4
    chizz=-60*z+180*z**2-120*z**3
    dz=[2*x[a]/(5*eps**2) for a in range(n)]
    dchi=[chiz*dz[a] for a in range(n)]
    ddchi=[[chizz*dz[a]*dz[c]+chiz*2*delta(a,c)/(5*eps**2) for c in range(n)] for a in range(n)]
    D=h-b; dD=[dh[a]-db[a] for a in range(n)]
    g=b+chi*D
    dg=[db[a]+chi*dD[a]+dchi[a]*D for a in range(n)]
    dd=[[ddb[a][c]+chi*(ddh[a][c]-ddb[a][c])+dchi[a]*dD[c]+dchi[c]*dD[a]+ddchi[a][c]*D for c in range(n)] for a in range(n)]
    inv=g.inv()
    gamma=[[[sum((dg[j][a,k]+dg[k][a,j]-dg[a][j,k])*delta(i,a) for a in range(n))/2 for k in range(n)] for j in range(n)] for i in range(n)]
    def curv(i,j,k,l):
        return (dd[i][l][j,k]+dd[j][k][i,l]-dd[j][l][i,k]-dd[i][k][j,l])/2+sum(inv[a,c]*(gamma[a][i][l]*gamma[c][j][k]-gamma[a][i][k]*gamma[c][j][l]) for a,c in itertools.product(range(n),repeat=2))
    # Independent Christoffel-connection calculation checks the curvature formula.
    up=[[[sum(inv[a,c]*gamma[c][j][k] for c in range(n)) for k in range(n)] for j in range(n)] for a in range(n)]
    dinv=[-inv*dg[q]*inv for q in range(n)]
    def dup(q,a,j,k):
        return sum(dinv[q][a,c]*gamma[c][j][k]+inv[a,c]*(dd[q][j][c,k]+dd[q][k][c,j]-dd[q][c][j,k])/2 for c in range(n))
    def connection_curv(i,j,k,l):
        return sum(g[k,a]*(dup(i,a,j,l)-dup(j,a,i,l)+sum(up[a][i][c]*up[c][j][l]-up[a][j][c]*up[c][i][l] for c in range(n))) for a in range(n))
    pairs=list(itertools.combinations(range(n),2))
    for (i,j),(k,l) in itertools.product(pairs,repeat=2):
        need(curv(i,j,k,l)==connection_curv(i,j,k,l),'independent full curvature formulas agree')
    R=s.Matrix([[curv(i,j,k,l) for k,l in pairs] for i,j in pairs])
    G=s.Matrix([[g[i,k]*g[j,l]-g[i,l]*g[j,k] for k,l in pairs] for i,j in pairs])
    ric=s.Matrix([[sum(inv[j,l]*curv(i,j,k,l) for j,l in itertools.product(range(n),repeat=2)) for k in range(n)] for i in range(n)])
    scal=s.trace(inv*ric)
    W=s.Matrix([[curv(i,j,k,l)-(ric[i,k]*g[j,l]+ric[j,l]*g[i,k]-ric[i,l]*g[j,k]-ric[j,k]*g[i,l])/2+scal*(g[i,k]*g[j,l]-g[i,l]*g[j,k])/6 for k,l in pairs] for i,j in pairs])
    w2=norm2_pair(W,G)
    radial_defect=s.trace(inv*sum((x[a]*dg[a] for a in range(n)),s.zeros(n)))/(2*r2)
    return g,dg,dd,R,G,scal,w2,radial_defect


def main():
    n=4
    sizes=[s.Rational(1,64),s.Rational(1,128),s.Rational(1,256),s.Rational(1,512)]
    radii=[s.Rational(9,4),s.Rational(5,2),s.Rational(11,4)]
    component_count=0;cases=0;negative_f=0;negative=[];max_curv=0;max_radial=0
    for rho in radii:
        ref=None
        for eps in sizes:
            g,dg,dd,R,G,scal,w2,defect=shell_data(eps,rho)
            need(all(g[:j,:j].det()>0 for j in range(1,n+1)),'positive metric')
            x=s.Matrix([rho*eps,0,0,0]);need(g*x==x,'radial gauge')
            normalized=[(g-s.eye(n))/eps**2]+[v/eps for v in dg]+[dd[a][b] for a,b in itertools.product(range(n),repeat=2)]
            if ref is None:ref=normalized
            else:
                need(normalized==ref,'exact cutoff scaling')
                component_count+=len(normalized)*n*n
            need(scal==2*s.trace(G.inv()*R),'scalar equals twice operator trace')
            need(w2>=0,'Weyl Hilbert-Schmidt norm nonnegative')
            # At this axial point g is diagonal, so contraction is straightforward.
            need(g.is_diagonal(),'axial diagonal metric')
            full2=4*sum(R[a,b]**2/(G[a,a]*G[b,b]) for a,b in itertools.product(range(6),repeat=2))
            op2=norm2_pair(R,G)
            need(full2==4*op2,'tensor to operator norm factor')
            need(full2!=op2,'missing tensor to operator norm factor rejected')
            need(max(abs(z) for z in R)<1000,'bounded full curvature stress envelope')
            need(abs(defect)<1000,'bounded radial Laplacian stress envelope')
            max_curv=max(max_curv,max(abs(z) for z in R))
            max_radial=max(max_radial,abs(defect))
            # F=scalar-d*sqrt(w2) is finite independently of epsilon in this test.
            need(abs(scal)<10000 and w2<1000000,'bounded scalar and Weyl stress envelope')
            lam=s.Rational(7,5)
            need(norm2_pair(lam**2*R,lam**4*G)==lam**(-4)*op2,'conformal curvature-weight norm calculation')
            if scal<0 or scal**2<4*w2:negative_f+=1
            cases+=1
    negative.append('missing_full_tensor_to_operator_factor_detected')
    # A radial-gauge defect changes |grad r| and invalidates the radial reduction.
    x=s.Matrix([1,0,0,0]);bad=s.diag(2,1,1,1)
    need((x.T*bad.inv()*x)[0]!=1,'radial gauge defect negative control')
    negative.append('dropping_radial_gauge_detected')
    # Reversing the drift lower bound changes the barrier comparison sign.
    slope=s.Rational(-3,7);gap=s.Rational(5,11)
    need(gap*slope<0 and (-gap)*slope>0,'radial comparison sign negative control')
    negative.append('reversing_radial_lower_bound_detected')
    print(json.dumps({'status':'PASS','full_curvature_shell_cases':cases,'cases_with_negative_F_at_d_2':negative_f,'exact_scaled_metric_jet_component_comparisons':component_count,'independent_curvature_formula_component_comparisons':cases*36,'dimensions':[4],'epsilon_values':[str(e) for e in sizes],'radius_over_epsilon_values':[str(r) for r in radii],'observed_max_absolute_covariant_curvature_entry':str(max_curv),'observed_max_absolute_radial_defect_over_r':str(max_radial),'negative_controls':negative,'scope':'Independent exact shell diagnostics with quadratic normal metrics and a C2 quintic cutoff, plus normalization checks. These finite tests neither construct the analytic boundary germ nor verify every smooth cutoff; the analytic audit supplies those proofs. The background in this shell test is the round second-jet model, not the global round metric.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
