"""Independent zero-mode curvature and one-edge boundary controls."""
import sympy as s
x=s.symbols('x');f=s.sqrt(4+s.sqrt(12+2*x));kap=(7*s.sqrt(3)-9)/144
assert s.simplify(-256*s.diff(f,x,2).subs(x,0)-64*kap)==0
A=s.Matrix([[0,1],[1,0]]);P=(s.eye(2)-A)/2
assert P*P==P and s.trace(P*A)==-1
print('Uniform horizontal link perturbation curvature: exact symbolic match to full Hessian zero block.')
print('Every all-size result requires written universal argument; sampled controls are supporting evidence only.')
print('Thermodynamic lower comparison permits every integer box rank 0,...,l^2; envelope endpoints have F_l(0)=F_l(l^2)=0.')
