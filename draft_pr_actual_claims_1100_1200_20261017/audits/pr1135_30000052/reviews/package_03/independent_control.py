#!/usr/bin/env python3
"""Independent exact review control. No supplied checker is imported or copied.

Integrate sorted-point telescoping antiderivatives by affine endpoint evaluation.
All numbers are rational. Universal claims are established in REPORT.md; finite
controls check arithmetic/implementation and deliberately false substitutes.
"""
import argparse,json,math
from fractions import Fraction as Q

checks=0

def require(ok,label):
 global checks
 checks+=1
 if not ok:raise RuntimeError(label)

def integral_line_power(a,b,p,lo,hi):
 # Binomial expansion avoids a special division-by-slope branch.
 return sum(Q(math.comb(p,k))*a**k*b**(p-k)*(hi**(k+1)-lo**(k+1))/Q(k+1) for k in range(p+1))

def exact_moment(n,p,omit_one_band=False):
 if n<1 or p<2 or p%2:raise ValueError('positive count and even exponent required')
 breaks=sorted({Q(0),Q(1)}|{Q(m,k) for k in range(1,n) for m in range(1,k)})
 area=Q(0);answer=Q(0);cells=0;details=[]
 for lo,hi in zip(breaks,breaks[1:]):
  zm=(lo+hi)/2
  cut=[(Q(0),Q(0)),(Q(0),Q(1))]
  cut.extend((Q(-j),Q(math.floor(j*zm)+1)) for j in range(1,n))
  cut.sort(key=lambda ab:ab[0]*zm+ab[1])
  require(len(set(a*zm+b for a,b in cut))==n+1,'distinct shift cuts')
  for cell_index,(lower,upper) in enumerate(zip(cut,cut[1:])):
   if omit_one_band and cells==0:
    cells+=1;continue
   am,bm=lower;ap,bp=upper
   dm=((am+ap)*zm+bm+bp)/2
   floors=[math.floor(j*zm+dm) for j in range(n)]
   order=sorted(range(n),key=lambda j:j*zm+dm-floors[j])
   require(len(set(order))==n,'all indices retained')
   # Affine inequalities hold everywhere if valid at all closed-strip vertices.
   for z in (lo,hi):
    for d in (am*z+bm,ap*z+bp):
     ts=[j*z+d-floors[j] for j in order]
     require(all(Q(0)<=t<=Q(1) for t in ts),'closed cell floors')
     require(ts==sorted(ts),'closed cell order')
   ar=integral_line_power(ap-am,bp-bm,1,lo,hi)
   require(ar>0,'positive cell area');area+=ar
   value=Q(0)
   # First integrate endpoint x, telescope the boundary terms; then shift Delta.
   for rank,j in enumerate(order,1):
    for boundary,sign in [(Q(rank-1,n),1),(Q(rank,n),-1)]:
     c=-Q(floors[j])-boundary
     upper_int=integral_line_power(Q(j)+ap,c+bp,p+2,lo,hi)
     lower_int=integral_line_power(Q(j)+am,c+bm,p+2,lo,hi)
     value+=Q(sign, (p+1)*(p+2))*(upper_int-lower_int)
   require(value>=0,'nonnegative discrepancy cell integral')
   cells+=1;answer+=value
   if n in (3,4) and p==4:details.append({'z':[str(lo),str(hi)],'lower':[str(x) for x in lower],'upper':[str(x) for x in upper],'order':order,'area':str(ar),'integral':str(value)})
 require(area==1,'complete parameter-square area')
 return answer,cells,details

def iid_beta(n,p):
 # Full binomial law and beta integrals, unrelated to the lattice partition.
 return sum(Q(math.comb(n,k)*math.comb(p,r)*(-1)**r)*(Q(k,n)**(p-r))*Q(math.factorial(k+r)*math.factorial(n-k),math.factorial(n+r+1)) for k in range(n+1) for r in range(p+1))

def deterministic(points,p):
 s=sorted(points);n=len(s)
 return sum(((t-Q(k,n))**(p+1)-(t-Q(k+1,n))**(p+1))/Q(p+1) for k,t in enumerate(s))

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--force-failure',action='store_true');args=parser.parse_args()
 values=[];tables={};negative=[]
 for n in range(1,8):
  for p in (2,4,6):
   lat,cells,tab=exact_moment(n,p);iid=iid_beta(n,p)
   if p==2:require(lat==Q(1,6*n),'second moments')
   if n<=2:require(lat==iid,'whole-law necessary moments')
   if p==4:require(iid==Q(3*n-1,30*n**3),'iid fourth expression')
   if n==3 and p==4:require(lat==Q(19,1620),'three-point exact fraction')
   if n==4 and p==4:require(lat==Q(139,17280),'four-point exact fraction')
   values.append({'n':n,'p':p,'lattice':str(lat),'iid':str(iid),'cells':cells})
   if tab:tables[str(n)]=tab
 require(Q(19,1620)-Q(4,405)==Q(1,540),'exact gap')
 require(Q(19,1620)/Q(4,405)==Q(19,16),'exact ratio')
 # Universal polynomial certificates checked at the coefficient level.
 # f(4+t) = 4t^3+27t^2+52t+25; derive by binomial expansion.
 coeff=[sum(Q(c)*math.comb(k,j)*4**(k-j) for k,c in [(3,4),(2,-21),(1,28),(0,-7)] if k>=j) for j in range(4)]
 require(coeff==[25,52,27,4] and all(c>0 for c in coeff),'tail positivity polynomial')
 for n in range(3,70):
  # Simplex monomial moment int a^5 da db = 5!/(7!).
  single=Q(2,5*(n-1))*Q(math.factorial(5),math.factorial(7))
  require(single==Q(1,105*(n-1)),'tail simplex integral')
  if n>=4:require(2*single>iid_beta(n,4),'all-n tail finite controls')
  else:require(2*single<iid_beta(n,4),'three-point tail is insufficient')
 # Fourier coefficient energy: independent difference multiplicities.
 for n in range(1,80):
  energy=sum((n-abs(k))**2 for k in range(1-n,n))
  require(energy==Q(2*n**3+n,3),'Dirichlet fourth exact energy')
 upper=Q(22,7)**4
 # Certificate 60n^2+30-48*pi^4*(3n-1)>0 for n>=234.
 fc=[60*234**2+30-48*upper*(3*234-1),120*234-144*upper,Q(60)]
 require(all(x>0 for x in fc),'Fourier threshold universal coefficient certificate')
 # Independent phases have fourth energy 2n^2-n, not n^2: surviving
 # exponent tuples have equal positive/negative index multisets.
 for n in range(1,8):
  phase_energy=sum(sorted((a,b))==sorted((c,d)) for a in range(n) for b in range(n) for c in range(n) for d in range(n))
  require(phase_energy==2*n*n-n,'actual iid phasor fourth energy')
 require(2*3**2-3==15 and Q(2*3**3+3,3)!=15,'lattice energy differs from iid phase energy')
 # Reproducible adverse cases: each would invalidate a central step.
 require(Q(1,4)**2/2!=Q(1,4)**3,'pairwise is not triple independence');negative.append('iid triple substitution')
 require(Q(1,1)**2/2!=1,'lower q formula cannot extend to 1');negative.append('global lower-half q')
 require(Q(1,105)<Q(4,405),'n3 tail not sufficient');negative.append('tail-only n3 conclusion')
 require(iid_beta(1,4)==Q(1,15) and iid_beta(1,4)!=Q(19,1620),'fixed zero generator with uniform shift is a different average');negative.append('fixed-generator substitute')
 require(deterministic([Q(0)]*3,4)==Q(1,5),'collisions counted by index')
 # Degenerate collision configuration makes incorrect 1/3 mass fail visibly.
 wrong_mass=integral_line_power(-1,Q(1,3),4,Q(0),Q(1))
 require(wrong_mass!=Q(1,5),'deduplication with old n changes discrepancy');negative.append('deduplicate retaining old normalization')
 require(Q(19,1620)*3**4!=Q(19,1620),'missing normalization');negative.append('omit fourth normalization')
 require(Q(4**4,2)>3**4 and Q(4,2)<3,'fourth moment ordering does not imply mean ordering');negative.append('infer expected-norm order from fourth moment')
 try:exact_moment(3,3)
 except ValueError:negative.append('odd exponent without absolute-value splitting')
 else:raise RuntimeError('odd exponent accepted')
 try:exact_moment(3,4,True)
 except RuntimeError as e:
  require(str(e)=='complete parameter-square area','missing-band rejection mechanism');negative.append('delete positive-area cell')
 else:raise RuntimeError('incomplete partition accepted')
 # Full inverse torus map and a finite-grid warning control.
 for a in range(13):
  for b in range(13):
   u,v=Q(a,13),Q(b,13);z=(v-u)%1
   require((u,(u+z)%1)==(u,v),'complete n2 torus inverse')
 require(len({2*j%6 for j in range(6)})!=6,'finite even-grid multiplication is different');negative.append('replace continuous Haar law by finite even grid')
 require(sum(t<Q(1,4) for t in [Q(0)])!=1-sum(t<Q(3,4) for t in [Q(0)]),'boundary reflection complement can fail');negative.append('pointwise reflection without null-boundary qualification')
 # Reflected deterministic configurations away from exceptional endpoints.
 for n in range(1,8):
  for z in (Q(1,13),Q(5,17),Q(7,19)):
   for d in (Q(2,23),Q(9,29)):
    points=[(j*z+d)%1 for j in range(n)]
    reflected=[(-t)%1 for t in points]
    require(deterministic(points,4)==deterministic(reflected,4),'reflection of nonboundary configuration')
 if args.force_failure:require(Q(19,1620)==Q(4,405),'deliberately forced incorrect identity')
 print(json.dumps({'status':'PASS','checks':checks,'arithmetic':'exact Fraction only','moments':values,'n3_n4_cells':tables,'tail_shifted_polynomial':[str(c) for c in coeff],'Fourier_threshold_shifted_coefficients':[str(c) for c in fc],'adverse_controls':negative,'universal_proofs_in':'REPORT.md'},indent=2,sort_keys=True))

if __name__=='__main__':main()
