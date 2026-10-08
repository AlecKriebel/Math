"""Finite exact controls only. They do not prove an infinite-dimensional PDE claim."""
from fractions import Fraction as F
from itertools import product


def run(claims):
    count = 0
    def check(condition, label):
        nonlocal count
        count += 1
        if not condition:
            raise ValueError('control failed: ' + label)
    def mm(a,b):
        return [[sum(a[i][j]*b[j][k] for j in range(len(b))) for k in range(len(b[0]))] for i in range(len(a))]
    def mv(a,v):
        return [sum(x*y for x,y in zip(row,v)) for row in a]
    def dot(v,w):
        return sum(x*y for x,y in zip(v,w))
    # Exact polar formulas; samples supplement the global written proof.
    for j in range(257):
        c=F(j,128)-1
        r=1+c/4
        rp2=F(9,16)*(1-c*c)
        rpp=-F(9,4)*c
        check(r*r+2*rp2-r*rpp == F(17,8)+F(11,4)*c-c*c/2, 'curvature polynomial')
        check(r>=F(3,4), 'radial lower bound')
        check(r**4>F(9,64)*(r*r+rp2), 'strict support bound')
    check(F(-9,8)/F(27,64)==F(-8,3), 'curvature at the marked point')
    check(36>34, 'support bound square comparison')
    check(F(claims['geometric_controls']['curvature_at_pi_over_3']) == F(-8,3), 'claimed curvature')
    # Positive-metric example and its zero quadratic form.
    A=claims['matrix_A']; P=claims['matrix_P']; v=claims['zero_vector']
    check(mm(A,[[1,-2],[0,1]]) == [[1,0],[0,1]], 'right inverse')
    check(mm([[1,-2],[0,1]],A) == [[1,0],[0,1]], 'left inverse')
    PA=mm(P,A)
    check(PA==[[1,1],[-1,1]], 'weighted product')
    check(P[0][0]>0 and P[0][0]*P[1][1]-P[0][1]*P[1][0]>0, 'positive metric minors')
    check(dot(mv(A,v),v)==0 and dot(v,v)>0, 'zero numerical form')
    for x,y in product(range(-6,7), repeat=2):
        w=[F(x,3),F(y,4)]
        check(dot(mv(PA,w),w)==dot(w,w), 'weighted identity')
        check(dot(mv(P,w),w)>=0, 'metric sample')
    # Telescoping defect identity for weighted nilpotent shifts.
    for n in range(1,9):
        for trial in range(1,17):
            weights=[F((trial+j)%5,4) for j in range(n-1)]
            x=[F(((trial+3*j)%11)-5,3) for j in range(n)]
            T=lambda u:[weights[j]*u[j+1] for j in range(n-1)]+[F(0)]
            defect=[F(1)]+[1-w*w for w in weights]
            u=x[:]; total=F(0)
            for j in range(n):
                total+=sum(defect[z]*u[z]**2 for z in range(n))
                u=T(u)
            check(all(z==0 for z in u), 'nilpotence')
            check(total==dot(x,x), 'defect telescoping')
            check(dot(T(x),T(x))<=dot(x,x), 'weighted-shift contraction')
    T=[[0,2],[0,0]]; IminusT=[[1,-2],[0,1]]
    check(mm(T,T)==[[0,0],[0,0]], 'acyclic countermodel nilpotence')
    check(dot(mv(IminusT,[1,1]),[1,1])==0, 'acyclic countermodel zero form')
    # Finite block exact certificates: no square-root rounding is used.
    for a,d,b,lamb in [(F(2),F(3),F(1),F(1)),(F(3,4),F(1,2),F(1,4),F(1,4)),(F(5),F(2),F(1),F(1))]:
        check(a>0 and d>0 and a*d>b*b, 'positive block determinant')
        check(a>=lamb and d>=lamb and (a-lamb)*(d-lamb)>=b*b, 'rational lower certificate')
        for x,y in product(range(-8,9),repeat=2):
            check(a*x*x+d*y*y-2*b*x*y>=lamb*(x*x+y*y), 'block quadratic inequality')
    # Positive diagonal finite-gap surrogate. The exponential family is proved in text.
    for n in range(2,65):
        gap=F(1,2**n)
        for j in range(33):
            s=F(j,32)
            check(gap*s+F(1,2)*(1-s)>=gap, 'diagonal minimal gap')
    return {'problem_id':30003533,'status':'PASS_FINITE_CONTROLS_ONLY','exact_controls':count,'pde_target_resolved':False}
