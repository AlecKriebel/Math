#!/usr/bin/env python3
"""Independent finite exact diagnostics for the application, not a PDE proof."""
from fractions import Fraction as Q
from itertools import product
import json
import sys

CHECKS = []
def require(label, condition):
    if not condition:
        raise RuntimeError(label)
    CHECKS.append(label)

def tr(A): return [list(c) for c in zip(*A)]
def mm(A,B): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def mv(A,v): return [sum(a*b for a,b in zip(r,v)) for r in A]
def dot(v,w): return sum(a*b for a,b in zip(v,w))
def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def inv(A):
    n=len(A); B=[list(map(Q,r))+s for r,s in zip(A,eye(n))]
    for j in range(n):
        k=next(i for i in range(j,n) if B[i][j]); B[j],B[k]=B[k],B[j]
        a=B[j][j]; B[j]=[x/a for x in B[j]]
        for i in range(n):
            if i!=j:
                a=B[i][j]; B[i]=[x-a*y for x,y in zip(B[i],B[j])]
    return [r[n:] for r in B]

# Tiny one-variable polynomial arithmetic, independent of external libraries.
def p(a):
    a=list(map(Q,a if isinstance(a,(tuple,list)) else [a]))
    while len(a)>1 and a[-1]==0: a.pop()
    return tuple(a)
def add(a,b):
    a,b=p(a),p(b); return p([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a): return p([-x for x in p(a)])
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    a,b=p(a),p(b); c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return p(c)
def half(a): return p([x/2 for x in p(a)])
def dx(a): return p([i*x for i,x in enumerate(p(a))][1:] or [0])
def val(a,x): return sum(c*x**i for i,c in enumerate(p(a)))
def psum(terms):
    ans=p(0)
    for term in terms: ans=add(ans,term)
    return ans

X=p([0,1]); D=add(1,mul(4,mul(X,X))); Z=p(0); O=p(1)
# F(x,y,z)=(x,y+x^2,z), inverse (X,Y,Z)->(X,Y-X^2,Z).
A=[[O,Z,Z],[mul(2,X),O,Z],[Z,Z,O]]
G=[[D,mul(2,X),Z],[mul(2,X),O,Z],[Z,Z,O]]
GI=[[O,mul(-2,X),Z],[mul(-2,X),D,Z],[Z,Z,O]]
def pmm(A,B): return [[psum(mul(a,b) for a,b in zip(r,c)) for c in zip(*B)] for r in A]
require('nonlinear_pullback_gram',pmm(tr(A),A)==G)
require('nonlinear_metric_inverse',pmm(G,GI)==[[p(i==j) for j in range(3)] for i in range(3)])
require('nonlinear_metric_determinant_one',sub(D,mul(mul(2,X),mul(2,X)))==O)
def partial(a,i): return dx(a) if i==0 else Z
Gamma=[[[half(psum(mul(GI[k][l],sub(add(partial(G[l][j],i),partial(G[l][i],j)),partial(G[i][j],l))) for l in range(3))) for j in range(3)] for i in range(3)] for k in range(3)]
require('only_connection_component_is_Gamma_y_xx_2',all(Gamma[k][i][j]==p(2 if (k,i,j)==(1,0,0) else 0) for k,i,j in product(range(3),repeat=3)))
for k,l,i,j in product(range(3),repeat=4):
    R=add(sub(partial(Gamma[k][j][l],i),partial(Gamma[k][i][l],j)),psum(sub(mul(Gamma[k][i][m],Gamma[m][j][l]),mul(Gamma[k][j][m],Gamma[m][i][l])) for m in range(3)))
    require(f'nonlinear_Riemann_{k}{l}{i}{j}',R==Z)
# For the bottom facet y=0, outward unnormalized metric normal is (2x,-D,0).
V=[mul(2,X),neg(D),Z]
require('nonlinear_outward_normal_push', [psum(mul(a,b) for a,b in zip(r,V)) for r in A]==[mul(2,X),p(-1),Z])
require('nonlinear_normal_norm_squared',psum(mul(V[i],psum(mul(G[i][j],V[j]) for j in range(3))) for i in range(3))==D)
pushed_normal=[psum(mul(a,b) for a,b in zip(r,V)) for r in A]
pushed_interior_direction=[r[1] for r in A]
require('nonlinear_outward_side',psum(mul(a,b) for a,b in zip(pushed_normal,pushed_interior_direction))==p(-1))
# div_g(V/sqrt(D)) = (2D-x D')/D^(3/2)=2/D^(3/2)>0.
require('sphere_positive_mean_curvature_numerator',sub(mul(2,D),mul(X,dx(D)))==p(2))
for x in [Q(-7),Q(-1,3),Q(0),Q(2,5),Q(11)]:
    require(f'positive_metric_and_mean_denominator_{x}',val(D,x)>0)
    def forward(v): return [v[0],v[1]+v[0]**2,v[2]]
    def backward(v): return [v[0],v[1]-v[0]**2,v[2]]
    point=[x,Q(4,7),Q(-3,2)]
    require(f'smooth_nonlinear_inverse_{x}',backward(forward(point))==point and forward(backward(point))==point)
# Reflection of first output coordinate reverses ambient orientation; Gram is identical.
AR=[list(r) for r in A]; AR[0]=[neg(x) for x in AR[0]]
require('orientation_reversal_same_pullback',pmm(tr(AR),AR)==G)
require('orientation_reversal_normal_push',[psum(mul(a,b) for a,b in zip(r,V)) for r in AR]==[mul(-2,X),p(-1),Z])

# Nonsimple cross-polytope corner e1: 2^(n-1) facets meet, exceeding n.
for n in [3,4,7]:
    B=eye(n)
    for i in range(n-1): B[i][i+1]=Q(i+2)
    BI=inv(B); g=mm(tr(B),B); gi=inv(g)
    require(f'n{n}_metric_inverse',mm(g,gi)==eye(n))
    normals=[[Q(1)]+list(map(Q,s)) for s in product([-1,1],repeat=n-1)]
    require(f'n{n}_nonsimple_active_count',len(normals)==2**(n-1) and len(normals)>n)
    for a,u in enumerate(normals):
        pushed=mv(B,mv(gi,u)); target=mv(tr(BI),u)
        require(f'n{n}_normal_push_{a}',pushed==target)
        require(f'n{n}_normal_norm_{a}',dot(u,mv(gi,u))==dot(target,target)>0)
        # One adjacent facet differs in the last sign; closures meet at e1.
        v=u[:]; v[-1]=-v[-1]
        require(f'n{n}_adjacent_gram_{a}',dot(u,mv(gi,v))==dot(target,mv(tr(BI),v)))
    gp=[r+[Q(0)] for r in g]+[[Q(0)]*n+[Q(1)]]; gip=inv(gp)
    require(f'n{n}_product_preserves_old_pairings',[r[:n] for r in gip[:n]]==gi)
    require(f'n{n}_product_caps_orthogonal',all(gip[i][n]==0 for i in range(n)))

# Flatness plus zero facet curvature alone does not force reference angle equality.
s=Q(3,4); shear=[[Q(1),s],[Q(0),Q(1)]]; gi=inv(mm(tr(shear),shear))
require('shear_flat_metric_changed_angle',gi[0][1]==-s)
require('shear_exterior_cos_negative_three_fifths',gi[0][1]**2/(gi[0][0]*gi[1][1])==Q(9,25) and gi[0][1]<0)
require('opposite_shear_corner_angle_goes_the_other_way',dot([-1,0],mv(gi,[0,1]))>0)
# Since arccos is decreasing: theta_D=pi-alpha_D, theta_D<theta_P iff alpha_D>alpha_P.
theta_ref=Q(1,2); theta_comp=Q(2,5)
require('interior_exterior_reversal',theta_comp<theta_ref and 1-theta_comp>1-theta_ref)

# Standard exact turning budget, units of pi: any strict decrease forces negative k.
for m in [3,4,5,9,17,31]:
    theta=Q(m-2,m); eps=theta/7
    require(f'polygon_{m}_reference_turn',m*(1-theta)==2)
    require(f'polygon_{m}_strict_turn_excess',m*(1-theta)+eps==2+eps and -eps<0)

# Smooth map without smooth inverse at endpoint: g=(d(x^3))^2=9x^4, zero at x=0.
singular_pullback=mul(dx(mul(mul(X,X),X)),dx(mul(mul(X,X),X)))
require('corner_singular_metric_detected',singular_pullback==p([0,0,0,0,9]) and val(singular_pullback,0)==0)

print(json.dumps({'passed_checks':len(CHECKS),'check_names':CHECKS,'arithmetic':'Python standard-library Fraction and explicit exact polynomial arithmetic','scope':'finite application/convention diagnostics only; no proof of Bi analytic, index, trace or compactness theorem','python_version':sys.version.split()[0]},indent=2,sort_keys=True))
