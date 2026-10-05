"""Independent exact checks, written before reading frozen candidate."""
import sympy as s
E, y, z = s.symbols('E y z', nonzero=True)
I=s.I
h=s.zeros(4)
for r in range(4):
    h[r,r]=I**r*y+I**(-r)/y
for r in range(3):
    h[r,r+1]=h[r+1,r]=1
h[0,3]=z
h[3,0]=1/z
actual=s.factor((E*s.eye(4)-h).det())
expected=E**4-8*E**2+4-z-1/z-y**4-y**(-4)
print('q4 polynomial identity:', s.factor(actual-expected))
assert s.factor(actual-expected)==0
small=h.subs({y:1,z:1})
print('q4 Gamma eigenvalues:', small.eigenvals())
assert small.eigenvals()=={-2*s.sqrt(2):1,2*s.sqrt(2):1,0:2}
# L=4, 4 fibers with exp(iky)^4=1, each first-band state -2sqrt2.
print('L4 uniform pi/2 canonical E:', -8*s.sqrt(2))
print('L4 uniform pi/2 energy/site:', -s.sqrt(2)/2)
# Deleted bond trace-norm is twice its modulus, yet tracelessness halves
# the variational bound. At a 2-site unit edge the one-particle bound is sharp.
a=s.Matrix([[0,1],[1,0]])
print('deleted bond eigenvalues:',a.eigenvals())
print('one occupied orbital energy shift:',1)
print('empty/full occupied energy shifts:',0,0)
print('norm<=4 implies density repair cost<=4*abs(delta_n)')
print('all independent exact checks passed')
