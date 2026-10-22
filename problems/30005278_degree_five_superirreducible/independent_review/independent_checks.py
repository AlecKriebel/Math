"""Independent exact controls for the reviewed packet; Python3 + SymPy."""
import argparse,itertools,json,math
from pathlib import Path
from fractions import Fraction
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);args=ap.parse_args();p=args.packet
checks=0
def ck(x):
 global checks
 checks+=1;assert x
x,M,N=s.symbols('x M N');f=x**5+2*x+1
# Multiplication matrix, independently of the resultant used by the author.
T=s.zeros(5)
for j in range(5):
 r=s.Poly(s.rem((M*x+N)*x**j,f,x),x)
 for i in range(5):T[i,j]=r.nth(i)
ck(s.expand(T.det()-(N**5+2*M**4*N-M**5))==0)
ck(s.discriminant(f,x)==11317)
q=x*x-8*x-7;rr=x**3+8*x*x+3*x-5
ck(s.Poly(q*rr-f,x,modulus=17).is_zero)
ck(s.Poly(q,x,modulus=17).is_irreducible);ck(s.Poly(rr,x,modulus=17).is_irreducible)
ck(s.Poly(f.subs(x,2*x*x+x),x,modulus=11).is_irreducible)
# Primitive dyadic squares in a separate coefficient formula implementation.
for a0 in range(1,16,2):
 for half in itertools.product(range(8),repeat=4):
  a1,a2,a3,a4=[2*h for h in half]
  coeff=[a0*a0-2*a1*a4-2*a2*a3,2*a0*a1-4*a1*a4-4*a2*a3-2*a2*a4-a3*a3,2*a0*a2+a1*a1-4*a2*a4-2*a3*a3-2*a3*a4,2*a0*a3+2*a1*a2-4*a3*a4-a4*a4,2*a0*a4+2*a1*a3+a2*a2-2*a4*a4]
  if all(v%16==0 for v in coeff[2:]):ck(coeff[0]%8==1 and coeff[1]%8==0)
# Exact rational exceptional-point exclusions.
for d in (1,2,4):
 for sg in (-1,1):
  t=Fraction(sg,d);ck(4*t**5+8*t**3-1!=0)
for d in (1,2,4,8):
 for sg in (-1,1):
  t=Fraction(sg,d);ck(-8*t**6-8*t**5+4*t*t+4*t+1!=0)
for t in (-2,-1,1,2):ck(t*(t*t+2)**3-2*(t*t+1)!=0)
# Check the literal complete certificate independently via its square-gap data.
cert=json.loads((p/'TURN_4_SMALL_CERTIFICATE.json').read_text());rows=cert['rows'];keys=set()
for row in rows:
 a,r,n=row['a'],row['r'],row['n'];keys.add((a,r,n));nn=n*n+8*r;d=nn**5+8192*nn-(4*a)**5
 ck(row['N']==nn and row['D']==d)
 if d<0:ck(row.get('negative') is True)
 else:
  y=row['floor_sqrt'];ck(y*y<d<(y+1)**2);ck(row['lower_gap']==d-y*y);ck(row['upper_gap']==(y+1)**2-d)
ck(len(rows)==600 and keys==set(itertools.product((2,-2),(-1,0,1),range(1,200,2))))
n,r=s.symbols('n r');P=n**5+20*r*n**3+120*r*r*n
for a in (2,-2):
 D=(n*n+8*r)**5+8192*(n*n+8*r)-(4*a)**5
 E=320*r**3*n**4+(6080*r**4+8192)*n*n+32768*r**5+65536*r-(4*a)**5
 ck(s.expand(D-P*P-E)==0)
# Bound margins at n=200; all negative powers decrease and 2n-40/n increases.
ck(Fraction(400)-Fraction(40,200)-Fraction(1,200**4)>399)
ck(Fraction(320)+Fraction(14272,200**2)+Fraction(131072,200**4)<321)
# Signed cyclic blocks: accumulated sign determines a length-ten orbit.
for perm in itertools.permutations(range(5)):
 orbit=[];z=0
 while z not in orbit:orbit.append(z);z=perm[z]
 if len(orbit)!=5:continue
 for signs in itertools.product((0,1),repeat=5):
  z=(0,0);seen=set()
  while z not in seen:seen.add(z);z=(perm[z[0]],z[1]^signs[z[0]])
  ck(len(seen)==(10 if sum(signs)%2 else 5))
# Odd-degree norm-square congruence, with independent exhaustive residue search.
square_norm_cases=0
for degree,polys in [(3,list(itertools.product(range(-2,3),repeat=3))), (5,[(1,2,0,0,0),(-1,-1,0,0,0),(1,0,1,0,0)])]:
 for low in polys:
  cc=list(low)+[1]
  for mm in list(range(-12,0))+list(range(1,13)):
   for nn in range(-12,13):
    dd=-sum(cc[j]*(-nn)**j*mm**(degree-j) for j in range(degree+1))
    if dd<=0 or math.isqrt(dd)**2!=dd:continue
    square_norm_cases+=1;ck(any((b*b-nn)%abs(mm)==0 for b in range(abs(mm))))
# Independent formal power-series reduction to order twelve.
u=s.symbols('u');z=sum(s.binomial(s.Rational(1,2),j)*u**j*x**j for j in range(13));zr=s.Poly(s.rem(z,f,x),x)
AA=[s.expand(zr.nth(i)) for i in range(5)]
lead=[1,s.Rational(1,2),-s.Rational(1,8),s.Rational(1,16),-s.Rational(5,128)]
for i in range(5):
 ck(s.expand(AA[i]).coeff(u,i)==lead[i]);ck(all(s.expand(AA[i]).coeff(u,j)==0 for j in range(i)))
gap=s.expand(AA[2]*AA[4]-AA[3]**2);ck(gap.coeff(u,6)==s.Rational(1,1024));ck(all(gap.coeff(u,j)==0 for j in range(6)))
err=s.Poly(s.rem(s.expand(zr.as_expr()**2-1-u*x),f,x),x)
for i in range(5):
 for j in range(13):ck(s.expand(err.nth(i)).coeff(u,j)==0)
ck(6%4 not in {b*b%4 for b in range(4)} and 6**2-2*4**2==4)
print(json.dumps({'assertions':checks,'certificate_rows':len(rows),'signed_lifts':768,'odd_degree_square_norm_cases':square_norm_cases,'formal_square_root_order':12,'scope':'Exact supplemental controls; original existence question unresolved'},indent=2))
