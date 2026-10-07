#!/usr/bin/env python3
"""Finite exact checks of the reviewer-created priority bridge; no orbit search."""
import hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
import sympy as sp

checks = []
def eq(name, expr):
    got = sp.factor(sp.simplify(expr))
    if got != 0:
        raise RuntimeError(name + ": " + str(got))
    checks.append(name)
def truth(name, condition):
    if not condition:
        raise RuntimeError(name)
    checks.append(name)

a,b,lam,L,N,d,h,U = sp.symbols("a b lam L N d h U", positive=True)
t = sp.symbols("t", real=True)
C=(1-t*t)/(1+t*t)
S=2*t/(1+t*t)
g=a*a*S*S+b*b*C*C
r=sp.sqrt(g)
w=sp.Matrix([-a*S/r,b*C/r])
Z=sp.diag(a,b)*w
normal=sp.Matrix([-S,C])
point=sp.Matrix([d,0])
Rplus=point+(r-point.dot(normal))*normal
Rminus=point+(r+point.dot(normal))*(-normal)
pair=sp.simplify((Rplus+Rminus)/2)
eq("unit_original_direction",w.dot(w)-1)
eq("hodograph_vertex_on_same_ellipse",(Z[0]/a)**2+(Z[1]/b)**2-1)
eq("unit_hodograph_normal",normal.dot(normal)-1)
eq("hodograph_normal_first_component", Z[0]/a**2-normal[0]/r)
eq("hodograph_normal_second_component", Z[1]/b**2-normal[1]/r)
eq("hodograph_tangent_support",normal.dot(Z)-r)
eq("pedal_pair_x",pair[0]-d*C*C)
eq("pedal_pair_y",pair[1]-d*S*C)
K=a*a*b*b-lam*(a*a-b*b)
T=sp.diag(h*K/(d*a*a*(b*b-lam)),h*K/(d*a*b*(b*b-lam)))
# Qpair is accepted candidate Eq.(8)/2; this does not re-prove it.
Qpair=sp.Matrix([-h+h*K*C*C/(a*a*(b*b-lam)),h*K*S*C/(a*b*(b*b-lam))])
bridge=sp.Matrix([-h,0])+T*pair
eq("antipedal_pedal_bridge_x",Qpair[0]-bridge[0])
eq("antipedal_pedal_bridge_y",Qpair[1]-bridge[1])
J=sp.sqrt(lam)/(a*b)
Hbt=(1-(L/J-N*(a*a+b*b))/(N*(a*a-b*b)))/2
Hcandidate=a*a/(a*a-b*b)*(1-b*L/(2*a*sp.sqrt(lam)*N))
eq("BT_harmonic_to_candidate_H",Hbt-Hcandidate)
V=sp.sqrt(lam)*r/(a*b)
A=sp.Matrix([a*(C*U+S*V), b*(S*U-C*V)])
B=sp.Matrix([a*(C*U-S*V), b*(S*U+C*V)])
Dinvsquared=sp.diag(1/a**2,1/b**2)
eq("original_incoming_chord_J_sign",A.dot(Dinvsquared*w)+J)
eq("original_outgoing_chord_J_sign",B.dot(Dinvsquared*w)-J)
newout=-sp.diag(1/a,1/b)*B
eq("hodograph_outgoing_J_same",newout.dot(Dinvsquared*Z)+J)
p,e=sp.symbols("p e", positive=True)
rho=(1+e*C)/p
X,Y=rho*C,rho*S
eq("focus_inversion_limaçon_equation",(p*(X*X+Y*Y)-e*X)**2-X*X-Y*Y)
eq("homothetic_confocal_obstruction", (a*a-lam)/a**2-(b*b-lam)/b**2-lam*(a*a-b*b)/(a*a*b*b))
eq("circle_affine_map_not_conformal",(1/b**2-1/a**2)-(a*a-b*b)/(a*a*b*b))
truth("raw_focus_ray_not_outer_normal_at_example",sp.det(sp.Matrix([[-4,0],[3,sp.Rational(1,3)]])) == sp.Rational(-4,3))
source=Path(__file__).read_bytes()
receipt={"schema":"pr140-priority-bridge-controls/v1","utc":datetime.now(timezone.utc).isoformat(),
 "pid":os.getpid(),"python":sys.version,"optimization":sys.flags.optimize,
 "sympy":sp.__version__,"source_sha256":hashlib.sha256(source).hexdigest(),
 "condition_count":len(checks),"conditions":checks,"status":"PASS",
 "scope":"Finite algebraic transformation checks only; candidate Eq8 is a premise; not a prior publication or all-orbit proof."}
print(json.dumps(receipt,indent=2))

