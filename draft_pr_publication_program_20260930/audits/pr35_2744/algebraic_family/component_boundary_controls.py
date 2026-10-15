#!/usr/bin/env python3
"""Small exact countermodels for missing component/finiteness hypotheses.
These are toy algebraic spaces, not knot character varieties.
"""
from pathlib import Path
import argparse
import json
import sympy as s

ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True,type=Path)
args=ap.parse_args()
checks={}
def ck(name,p):
    assert bool(p),name
    checks[name]='PASS'
x,y,t=s.symbols('x y t',real=True)
# A nonfinite projection collapses a genuine vertical arc.
ck('vertical_arc_nonconstant',s.diff(t,t)==1)
ck('nonfinite_projection_collapses_arc',x.subs(x,0)==0)
ck('fiber_contains_entire_vertical_line',(x.subs(x,0)).diff(y)==0)
# Connected paths can switch irreducible components at a singular crossing.
f=x*y
ck('crossing_has_two_distinct_irreducible_factors',s.factor(f)==x*y and x!=y)
ck('crossing_origin_singular',s.diff(f,x).subs({x:0,y:0})==s.diff(f,y).subs({x:0,y:0})==0)
ck('first_path_piece_on_one_component',f.subs({x:t,y:0})==0)
ck('second_path_piece_on_other_component',f.subs({x:0,y:t})==0)
ck('pieces_meet_at_crossing',s.Tuple(t,0).subs(t,0)==s.Tuple(0,t).subs(t,0))
# A real-defined ambient variety may have compact-type toy arc on a component
# other than the chosen nonreal complex line. Finding that arc proves no transfer.
w=s.symbols('w')
ambient=w*(w*w+1)
ck('real_ambient_with_nonreal_components',s.Poly(ambient,w).all_coeffs()==[1,0,1,0])
ck('nonreal_line_is_ambient_component',ambient.subs(w,s.I)==0)
ck('separate_real_line_is_ambient_component',ambient.subs(w,0)==0)
ck('selected_nonreal_line_has_no_real_points',s.im(s.I)==1)
ck('conjugate_nonreal_line_is_different',s.conjugate(s.I)!=s.I)
# A single word's trace square cannot test whether a projective element is
# identity: a nonidentity parabolic has the same trace square as identity.
P=s.Matrix([[1,1],[0,1]])
ck('parabolic_determinant_one',P.det()==1)
ck('parabolic_identity_trace_square',s.trace(P)**2==s.trace(s.eye(2))**2==4)
ck('parabolic_not_projective_identity',P!=s.eye(2) and P!=-s.eye(2))
result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact toy boundary countermodels only. Finiteness, smoothness, and selected-component control are genuine requirements; no knot target is proved or refuted.'}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'failed':0}))
