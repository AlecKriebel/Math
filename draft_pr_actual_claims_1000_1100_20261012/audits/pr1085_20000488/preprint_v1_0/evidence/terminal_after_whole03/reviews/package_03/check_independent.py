from fractions import Fraction as F
import math, json, argparse

def require(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b):return [x+y for x,y in zip(a+[F(0)]*max(0,len(b)-len(a)),b+[F(0)]*max(0,len(a)-len(b)))]
def scale(a,c):return [x*c for x in a]
def derivative(a):return [F(k)*a[k] for k in range(1,len(a))] or [F(0)]
def integral_product(a,b,rate):return sum(x*y*F(math.factorial(i+j),1)/rate**(i+j+1) for i,x in enumerate(a) for j,y in enumerate(b))
def value(a):return a[0]
def norm(a,b,rate):return integral_product(a,a,rate)+integral_product(b,b,rate)
def run(mutation=None):
 count={'polynomial_complex_vertical':0,'metric_complex':0,'weighted_trace':0,'normal_orientation':0,'dilation':0,'capacity':0,'Hardy_regularizer':0}
 # Polynomial-times-exponential complex profiles produce mixed cross terms unlike prior two-exponential probes.
 for beta,p,rho in [(F(7),F(24),F(25)),(F(8),F(15),F(17)),(F(1),F(0),F(1))]:
  for k in [F(1,7),F(3,2),F(19)]:
   for a,b in [([F(2),F(-3),F(1,5)],[F(-1),F(4,3)]),([F(0),F(7,4)],[F(3),F(-2),F(5,6)])]:
    da=add(derivative(a),scale(a,-k));db=add(derivative(b),scale(b,-k));a0=value(a)**2+value(b)**2
    E=norm(da,db,2*k)+(beta*beta+p*p)*norm(a,b,2*k)-(beta if mutation!='endpoint' else -beta)*a0
    comp=norm(add(da,scale(a,rho)),add(db,scale(b,rho)),2*k)+(rho-beta)*a0
    require(E==comp and E>=0,'complex polynomial Fourier square');count['polynomial_complex_vertical']+=1
 # Complex metric; general large signed slopes, with G bound exact and coercivity from universal triangle inequality.
 for g in [[F(-3),F(4),F(-12)],[F(1,11),F(-2,13),F(0)],[F(0),F(0),F(0)]]:
  G2=sum(t*t for t in g)
  for ar,ai,br,bi in [([F(3),F(-7),F(2)],[F(-1),F(2),F(9)],F(2),F(-3)),([F(0),F(1,3),F(-1)],[F(4),F(0),F(1)],F(-5),F(7))]:
   lhs=sum(t*t for t in ar+ai)+br*br+bi*bi;rhs=2*(1+G2)*(sum((x-t*br)**2+(y-t*bi)**2 for x,y,t in zip(ar,ai,g))+br*br+bi*bi)
   require(lhs<=rhs,'complex coercivity');count['metric_complex']+=1
 for beta,k in [(F(2,3),F(1,9)),(F(11),F(7,3)),(F(1,100),F(2))]:
  for a,b in [([F(1),F(2),F(-3)],[F(4),F(-2)]),([F(0),F(1)],[F(1),F(2,5),F(7)])]:
   da=add(derivative(a),scale(a,-k));db=add(derivative(b),scale(b,-k));L=norm(a,b,2*(beta+k));cross=integral_product(a,da,2*(beta+k))+integral_product(b,db,2*(beta+k))
   require(2*beta*L-2*cross==value(a)**2+value(b)**2,'weighted trace with mixed polynomial terms');count['weighted_trace']+=1
 # Unit normals from exact Pythagorean points, including upward-pointing and obstacle sides.
 for nx,ny,surf in [(F(3,5),F(-4,5),F(5,4)),(F(-3,5),F(4,5),F(5,4)),(F(0),F(1),F(1)),(F(0),F(-1),F(1))]:
  require(nx*nx+ny*ny==1 and 1+ny>=0,'unit-normal nonnegative defect')
  actual=(1+ny)*(F(1) if mutation=='surface' else surf)
  if ny==F(-4,5):require(actual==F(1,4),'surface Jacobian retained')
  count['normal_orientation']+=1
 for m in [3,4,8]:
  a=F(m-2,2)
  for r2,d2 in [(F(0),F(1)),(F(1,3),F(2,7)),(F(100),F(1,100))]:
   coeff=a*((m-2)*r2+m*d2)-a*a*r2
   require(coeff==a*a*r2+a*m*d2 and coeff>=a*a*r2,'regularized Hardy exact coefficient');count['Hardy_regularizer']+=1
 require(F(2-2,2)==0 and F(1-2,2)<0,'Hardy limiting dimensions')
 for beta,R,M,D,c in [(F(7,3),F(2),F(1,8),F(1,100),F(1,4)),(F(1,20),F(4,3),F(2),F(1,2),F(1,3))]:
  # Exponential arguments equal exactly. Polynomial factor transforms beta*(2beta A+sqrt A) to 2A'+sqrt A'.
  A=4*R*R;Rp=beta*R;Ap=4*Rp*Rp
  require(4*beta*M==4*(beta*M) and beta*(2*beta*A+2*R)==2*Ap+2*Rp,'physical dilation to beta one');count['dilation']+=1
 beta=F(3,2);B=F(1,9)
 require(F(2,100)/(2*beta)-beta*B<0,'m1 capacity cutoff');count['capacity']+=1
 require(F(2)*F(22,7)/100/(2*beta)-beta*B<0,'m2 logarithmic R/R0=exp(100) cutoff');count['capacity']+=1
 theta=F(1,4);require(1-(4 if mutation=='old_theta' else 2)*theta>0,'published source range')
 require(F(1250,2501)-F(1,480)==F(597499,1200480),'exact Hardy margin')
 return {'passed':True,'counts':count,'finite_diagnostics_only':True,'universal_proof_in':'INDEPENDENT_DERIVATION.md','new_mechanism':'complex polynomial-exponential vertical profiles; exact physical dilation; signed 3-component complex slope controls'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--mutation');a=p.parse_args();print(json.dumps(run(a.mutation),sort_keys=True,indent=2))
