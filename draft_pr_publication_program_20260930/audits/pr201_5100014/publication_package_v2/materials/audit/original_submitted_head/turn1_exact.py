"""Exact direct outer-pedal control, using installed SymPy; author-generated."""
import sympy as s
u,v=s.symbols('u v',real=True)
H=[(2,0),(s.Rational(4,3),s.sqrt(5)/3),(-s.Rational(4,3),s.sqrt(5)/3),(-2,0),(-s.Rational(4,3),-s.sqrt(5)/3),(s.Rational(4,3),-s.sqrt(5)/3)]
V=[(0,1),(-4*s.sqrt(2)/3,s.Rational(1,3)),(-4*s.sqrt(2)/3,-s.Rational(1,3)),(0,-1),(4*s.sqrt(2)/3,-s.Rational(1,3)),(4*s.sqrt(2)/3,s.Rational(1,3))]
def area(P):return s.simplify(sum(x*b-y*a for (x,y),(a,b) in zip(P,P[1:]+P[:1]))/2)
for name,P in [('H',H),('V',V)]:
 P=[tuple(map(s.sympify,p)) for p in P]
 T=[];Q=[]
 for (x,y),(a,b) in zip(P,P[1:]+P[:1]):
  det=x*b-y*a;T.append((s.simplify(4*(b-y)/det),s.simplify((x-a)/det)))
  nx,ny=x/4,y;fac=s.simplify((1-nx*u-ny*v)/(nx*nx+ny*ny));Q.append((s.simplify(u+fac*nx),s.simplify(v+fac*ny)))
 Ap=area(T);Am=area(Q);print(name,'outer=',T,'pedal=',Q,'Ap=',Ap,'Am=',s.factor(Am),'product=',s.factor(Ap*Am))
