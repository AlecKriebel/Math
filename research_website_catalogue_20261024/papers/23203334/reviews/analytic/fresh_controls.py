#!/usr/bin/env python3
"""Independent exact controls, not a verification of the PDE theorem.

No submitted modules imported. Main mechanisms: initial Maxwell trace,
positive cone flux, mass/charge bookkeeping, and an exact positive linear
combination of exponent inequalities. All assertions are explicit checks.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

count = 0
def check(condition, message):
    global count
    count += 1
    if not condition:
        raise RuntimeError(message)

def dot(x, y):
    return sum((a*b for a,b in zip(x,y)), F(0))

def cross(x, y):
    return (x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0])

# Stereographic parameterization gives unit normals without square roots.
normals=[]
for a,b in product([F(-2),F(-1,3),F(0),F(2,5),F(3)], repeat=2):
    den=1+a*a+b*b
    n=(2*a/den,2*b/den,(1-a*a-b*b)/den)
    check(dot(n,n)==1, 'unit normal')
    normals.append(n)
fields=[(F(0),F(0),F(0)), (F(1),F(-2),F(3)), (F(-3,5),F(4,7),F(9,11))]
for n,E,B in product(normals,fields,fields):
    nB=cross(n,B)
    H=tuple(E[i]+nB[i] for i in range(3))
    lhs=(dot(E,E)+dot(B,B))/2-dot(n,cross(E,B))
    rhs=(dot(H,H)+dot(n,B)**2)/2
    check(lhs==rhs and lhs>=0, 'positive exact EM cone flux')

# Along an axial source velocity v, angular electric terms have the form
# 2*pi*(constant + coefficient*log((1+v)/(1-v))). The sum must give
# -4*pi*v at initial time, i.e. the Maxwell -j term after division by 4*pi.
# This catches losing the initial-cone term even when interior algebra passes.
trace_rows=[]
for v in [F(-99,100),F(-3,5),F(-1,7),F(1,11),F(2,3),F(999,1000)]:
    boundary=( -2/v, (1-v*v)/(v*v) )
    interior=(2*(1-v*v)/v, -(1-v*v)/(v*v))
    check(boundary[0]+interior[0]==-2*v, 'correct initial current constant')
    check(boundary[1]+interior[1]==0, 'exact cancellation of logarithm')
    check(interior[1]!=0, 'omitting initial cone detected')
    trace_rows.append({'speed':str(v),'boundary_over_2pi':list(map(str,boundary)),
                       'interior_over_2pi':list(map(str,interior)),
                       'sum_over_2pi':str(-2*v)})
# At v=0 the original integrands are n and have zero spherical mean;
# no division by zero or appeal to the rational formula is needed.

species=[(F(1),F(1)),(F(1),F(-1)),(F(2),F(3)),(F(1,1000),F(-7)),(F(19),F(0))]
for m,e in species:
    check(m*(e/m)==e, 'kinetic work equals Maxwell work')
for (ma,ea),(mb,eb) in product(species,repeat=2):
    la,lb=ea/ma,eb/mb
    c=la*eb
    check(c==ea*eb/ma and c*lb==ea*eb*eb/(ma*mb),'pair coefficients')
    check((-ea/ma)*(-eb)==c,'simultaneous charge and field reversal')
    check(ea!=0 or c==0,'neutral receiver')
    check(eb!=0 or (c==0 and lb==0),'neutral source')
    if mb!=1 and ea*eb!=0:
        check(la*lb!=c,'wrong charge-to-mass product detected')
for lam in [F(-7,3),F(1,5),F(8)]:
    masses=[F(1,3),F(11),F(2)]
    densities=[F(3,7),F(5),F(0)]
    rho=sum(lam*m*f for m,f in zip(masses,densities))
    g=sum(lam*lam*m*f for m,f in zip(masses,densities))
    check(lam*rho==g,'common-ratio transformed Maxwell source')

# Derive an exact separating inequality, retaining the sharp small-Delta bound.
# Near + improved far + first unsafe inequality imply
# 187 H < 74 z + 974 Delta -348 alpha -600 min(alpha,c).
# Earlier energy-far + unsafe imply H > z/2+3(alpha+c)-4 Delta.
# Combining gives (39/2)z+909 alpha+561 c+600 min <1722 Delta.
# Since Delta/z<4/99995, even alpha=c=0 makes this impossible.
beta=F(29,25)
eps=F(1,100000)
delta=4*eps/(1-5*eps)
check(300*(F(1,3)+beta/4)==187,'H coefficient')
check(300*(beta/2-F(1,3))==74,'z coefficient')
check(300*(beta/2+F(8,3))==974,'Delta coefficient')
check(300*beta==348,'alpha coefficient')
check(187*F(1,2)-74==F(39,2),'combined z coefficient')
check(3*187+348==909 and 3*187==561,'nonnegative extra terms')
check(4*187+974==1722,'combined Delta coefficient')
contradiction_margin=F(39,2)-1722*delta
check(contradiction_margin>0,'strict positive separating margin')

# A rational witness satisfies the earlier near/energy/stable-cell and unsafe
# inequalities. It fails the improved-occupation far inequality. Thus the latter
# is an essential analytic input, not removable by arithmetic certificates.
alpha=c=F(1,100); z=1-c; H=F(3,5); y=F(3,10); b=F(23,40)
D=eps*(alpha+b+y+H)
check(2*alpha+H/2+2*y<z+D,'witness near selection')
check(H>2*c and b<H-c-alpha+D,'witness energy far')
check(b>2*H/3+z/6-D/3 and b<H+2*y-z/2+D,'witness unsafe')
check(b<H/2-min(alpha,c)+y+F(2,1000)*z,'witness stable-cell far')
check(F(16,100)*max(z,1-alpha)<y<F(49,100)*min(z,1-alpha),'witness window')
check(not b<H/2-min(alpha,c)+beta*y/2+D,'improved far excludes witness')

# Closure has to work for arbitrarily large fixed exterior coefficients.
closure=[]
eta=F(1,1024); sqrteta=F(1,32)
for C in [F(1,100),F(1),F(7),F(10**3),F(10**12)]:
    M=max(F(32),8*C)
    sqrtA=16*C+16*M+1
    A=sqrtA*sqrtA
    first=(C+2*M*sqrteta)/M
    second=(C*(M+sqrtA)+2*A*eta)/A
    check(A>=max(F(1),16*C*M,256*C*C),'admissible closure parameters')
    check(first<F(1,2) and second<F(1,2),'uniform strict improvement')
    closure.append({'C':str(C),'M':str(M),'A':str(A),
                    'sqrtI_ratio':str(first),'I_ratio':str(second)})

# Low-frequency Coulomb energy in dimension d has radial exponent d-3.
# It is integrable at zero exactly when d>2 for nonzero total charge.
check(3-3>-1 and not 2-3>-1,'nonneutral Coulomb L2 dimension boundary')
# Worst cone kernel and cutoff error in d=3: both vanish linearly with tip size.
for gamma in [F(1,2**k) for k in range(1,17)]:
    kernel_integral=gamma # integral_0^gamma r^2/r^2 dr
    cutoff_integral=((2*gamma)**2-gamma**2)/(2*gamma)
    check(cutoff_integral==F(3,2)*gamma and kernel_integral==gamma,'cone-tip integrability')

result={'status':'PASS','exact_conditions':count,
        'initial_trace_rows':trace_rows,
        'sharp_delta_over_z':str(delta),
        'separating_inequality_margin':str(contradiction_margin),
        'negative_control':'Earlier exponent inequalities allow alpha=c=1/100,z=99/100,H=3/5,y=3/10,b=23/40; improved occupation is essential and rejects this witness.',
        'closure_rows':closure,
        'limits':'Finite exact corroboration of analytic calculations; no proof of occupation estimates, global PDE regularity, novelty or formalization.',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
