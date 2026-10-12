#!/usr/bin/env python3
"""Exact diagnostics for the credited radius theorem; not a proof by sampling."""
from pathlib import Path
from hashlib import sha256
import json
import sympy as s

count = 0
sections = {}
def check(ok, section):
    global count
    assert bool(ok), section
    count += 1
    sections[section] = sections.get(section, 0) + 1
def zero(expr, section):
    check(s.simplify(expr) == 0, section)

z,a,r,rho,b,x,y=s.symbols('z a r rho b x y',real=True)
D=1-2*a*z+z*z
f=z/s.sqrt(D)
w=z*(a-z)/(1-a*z)
q=(1-a*z)/D
B=1-a*z+(a*a-2)*z*z+a*z**3
zero(z*s.diff(f,z)/f-q,'symbolic derivatives')
zero(s.diff(f,z)-(1-a*z)/D**s.Rational(3,2),'symbolic derivatives')
zero(1+z*s.diff(f,z,2)/s.diff(f,z)-B/((1-a*z)*D),'symbolic derivatives')
zero(q-1/(1-w),'symbolic derivatives')
zero(q+z*s.diff(q,z)/q-(1+z*s.diff(w,z))/(1-w),'symbolic derivatives')
zero(f.subs(z,0),'normalization')
zero(s.diff(f,z).subs(z,0)-1,'normalization')
zero((1-a*z)**2-(a-z)**2-(1-a*a)*(1-z*z),'disk automorphism')
zero(s.re(1/(1-x-s.I*y))-s.Rational(1,2)-(1-x*x-y*y)/(2*((1-x)**2+y*y)),'half-plane identity')
zero(s.re((1+x+s.I*y)/(1-x-s.I*y))-(1-x*x-y*y)/((1-x)**2+y*y),'half-plane identity')
Q=rho*rho-(1-r*r)*rho+1-2*r*r
zero(Q-(rho-(1-r*r)/2)**2-(3-6*r*r-r**4)/4,'quadratic lower bound')
zero((1-r*r)*(1-rho*rho)-(r*r-rho*rho)*(1+rho)-(1+rho)*Q,'quadratic lower bound')
R=s.sqrt(2*s.sqrt(3)-3); h=2-s.sqrt(3); A=h/R
zero(R**4+6*R**2-3,'exact radius')
zero(R**2-(1-2*h),'exact radius')
zero(h*h-4*h+1,'exact radius')
zero(A*A-(2/s.sqrt(3)-1),'exact radius')
check(0<R<1,'exact radius');check(0<h<R,'exact radius');check(0<A<1,'exact radius')
zero(B.subs({z:R,a:A}),'extremal contact')
zero(R*s.diff(B,z).subs({z:R,a:A})+6*h,'extremal contact')
zero(w.subs({z:R,a:A})+h,'extremal contact')
zero((z*s.diff(w,z)).subs({z:R,a:A})+1,'extremal contact')
zero(((R**2-h**2)/(1-R**2))-(1-h),'extremal contact')
check(s.simplify(B.subs({z:s.Rational(7,10),a:A})).is_negative,'extremal beyond radius')
# Published Singh--Goel Theorem4.2 branch and displayed equation4.9.
transition=20*b**4-52*b**3+15*b*b+12*b-4
zero(transition.subs(b,0)+4,'published specialization')
zero(transition.subs(b,s.Rational(1,2))-s.Rational(1,2),'published specialization')
sg=(5*b-1)/(4*b*b-b+1+4*b*s.sqrt(b*b-3*b+2))
zero(sg.subs(b,s.Rational(1,2))-R**2,'published specialization')
sg_eq=(8*b*b-3*b-1)*r**4-(8*b*b-2*b+2)*r*r+5*b-1
zero(sg_eq.subs(b,s.Rational(1,2))+(r**4+6*r*r-3)/2,'published specialization')
# A rational certificate below the exact threshold; no rounded comparison.
for rv in (s.Rational(1,10),s.Rational(1,3),s.Rational(1,2),s.Rational(3,5),s.Rational(2,3)):
    check(3-6*rv*rv-rv**4>0,'positive threshold controls')
    for j in range(11):
        tv=rv*s.Rational(j,10)
        check(Q.subs({r:rv,rho:tv})>0,'quadratic rational controls')
# Exact rational complex Blaschke jets. Includes both orientations and phases.
jet_cases=0
for av in (s.Rational(-3,4),s.Rational(-1,3),s.Rational(0),s.Rational(1,3),s.Rational(3,4)):
    for phase in (1,-1,s.I,-s.I,(3+4*s.I)/5):
        for rv in (s.Rational(1,10),s.Rational(1,2),s.Rational(2,3),s.Rational(7,10)):
            W=s.cancel(phase*w.subs(a,av)); U=s.expand_complex(W.subs(z,rv)); DU=s.expand_complex((z*s.diff(W,z)-W).subs(z,rv))
            norm=s.simplify(U*s.conjugate(U)); dnorm=s.simplify(DU*s.conjugate(DU))
            check(norm<1,'Blaschke rational controls');check(norm<=rv*rv,'Blaschke rational controls')
            zero(dnorm-((rv*rv-norm)/(1-rv*rv))**2,'Schwarz--Pick equality controls')
            kval=s.simplify(s.re((1+z*s.diff(W,z)).subs(z,rv)/(1-U)))
            if rv<=s.Rational(2,3): check(kval>0,'convexity rational controls')
            jet_cases+=1
# Boundary case w(z)=phase*z in the derivative estimate.
for phase in (1,-1,s.I):
    zero(z*s.diff(phase*z,z)-phase*z,'constant quotient cases')

receipt={'problem_id':2306022,'result':'PASS','assertions':count,'sections':sections,
 'exact_radius':'sqrt(2*sqrt(3)-3)','extremal_a':'sqrt(2/sqrt(3)-1)',
 'rational_blaschke_jet_cases':jet_cases,'arithmetic':'exact SymPy; no floating point tests',
 'artifact_sha256':sha256(Path('KNOWN_RESULT.md').read_bytes()).hexdigest(),
 'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'limitation':'Finite diagnostics support the written all-function proof; they are not exhaustive analytic verification.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
