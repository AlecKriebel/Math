"""Exact symbolic controls for the fixed signature differential criterion."""
import json
from pathlib import Path
import sympy as s

t = s.symbols('t', nonzero=True)
i = s.I
checks = {}

def require(name, expression):
    reduced = s.simplify(expression)
    if reduced != 0:
        raise AssertionError((name, reduced))
    checks[name] = 'PASS'

# Independent graph convention: x=t,y=t^2, z=x+iy,w=x-iy.
z = t+i*t**2
w = t-i*t**2
R = s.diff(z,t)/s.diff(w,t)
eta = s.diff(R,t)/R
metric = s.diff(z,t)*s.diff(w,t)
u = -eta**2/(4*metric)
v = i*s.diff(u,t)/eta
require('graph_curvature_square_sign',u-4/(1+4*t**2)**3)
require('graph_curvature_derivative_sign',v+24*t/(1+4*t**2)**3)
require('graph_eta',eta-i*s.diff(u,t)/v)
require('graph_metric',metric-s.diff(u,t)**2/(4*u*v**2))
a = 2*v*s.diff(z,t)/s.diff(u,t)
omega = (i*s.diff(u,t)/v-s.diff(u,t)/u)/2
require('graph_omega',s.diff(a,t)/a-omega)
require('graph_plus_form',s.diff(z,t)-a*s.diff(u,t)/(2*v))
require('graph_minus_form',s.diff(w,t)-s.diff(u,t)/(2*u*v*a))

# Both rational ODEs hold, although the irregular logarithmic factor is transcendental.
omega = i/t**2-1/t
A = -t-i
B = i/t**2-1/t
require('irregular_plus_rational_ode',s.diff(A,t)+omega*A-1/t**2)
require('irregular_minus_rational_ode',s.diff(B,t)-omega*B-1/t**4)
a = s.exp(-i/t)/t
z = a*A
w = B/a
require('irregular_plus_form',s.diff(z,t)-a/t**2)
require('irregular_minus_form',s.diff(w,t)-1/(a*t**4))
require('irregular_coordinate_product',z*w-(1+1/t**2))

result = {'method':'Exact SymPy simplification, no numerical integration',
          'sympy_version':s.__version__, 'checks':checks, 'all_pass':True}
path = Path(__file__).with_name('SYMBOLIC_CHECKS.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
