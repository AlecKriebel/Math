"""Additional exact checks. No external packages, network, or randomness."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
T=json.loads((ROOT/'example_tiling.json').read_text())
N=T['side'];tiles=T['tiles']
# Independent grid-cell coverage of this integral-coordinate example.
for a in range(N):
 for b in range(N):
  assert sum(x<=a and a+1<=x+s and y<=b and b+1<=y+s for x,y,s in tiles)==1
# Horizontal/vertical line metrics have unit length after normalization.
for axis in [0,1]:
 for a in range(N):
  assert sum(F(s,N) for x,y,s in tiles if [x,y][axis]<=F(2*a+1,2)<[x,y][axis]+s)==1
assert sum(F(s*s,N*N) for x,y,s in tiles)==1
z=json.loads((ROOT/'exact_crossings_results.json').read_text())
checks=0
for p in [F(k,20) for k in range(21)]:
 q=sum(F(a)*p**k*(1-p)**(7-k) for k,a in enumerate(z['H_by_black_count']))
 direct=p*(1-(1-p)**3)**2+(1-p)*p*p
 assert q==direct
 # Exact derivative and pivotal inequality on interior probabilities.
 if 0<p<1:
  derivative=(1-(1-p)**3)**2+6*p*(1-(1-p)**3)*(1-p)**2+2*p-3*p*p
  assert q*(1-q)<=p*(1-p)*derivative
  if p>=F(1,2):
   assert F(65,128)>=q/(2*p)**7
   assert F(65,128)>=q*q/(2*(p*p+(1-p)**2))**7
 checks+=1
assert sum(F(t) for t in z['influences'])==F(107,64)
bounds={}
for K in range(6,11):
 first=F(4**(K+1),2**(2**(K-2)));ratio=F(4,2**(2**(K-2)))
 bound=first/(1-ratio)
 bounds[str(K)]={'numerator':str(bound.numerator),'denominator':str(bound.denominator),'decimal_diagnostic':float(bound)}
assert F(4096,16383)<F(1,3)
assert bounds==json.loads((ROOT/'dyadic_exact_bounds.json').read_text())
result={'integer_grid_cells_checked':N*N,'line_metric_checks':2*N,'rational_probability_points':checks,'influence_sum':'107/64','dyadic_bounds_checked':5,'arithmetic':'integer and Fraction exact; JSON decimal fields are diagnostics only','status':'PASS'}
print(json.dumps(result,indent=2));(ROOT/'rational_results.json').write_text(json.dumps(result,indent=2)+'\n')
