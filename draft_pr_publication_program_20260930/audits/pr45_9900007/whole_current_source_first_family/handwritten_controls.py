import json, math
from fractions import Fraction

def positions(r):
    l=2**r;s=2**(r+1)-2
    return [(s+j,s+l+j) for j in range(l)]

def key(n):
    r=0
    while n>=2**(r+2)-2:r+=1
    l=2**r;s=2**(r+1)-2
    return r,(n-s)%l

coverage=[z for r in range(8) for pair in positions(r) for z in pair]
assert sorted(coverage)==list(range(510)) and len(set(coverage))==510
windows=[]
for h in [1,2,3,7,16,31]:
    first=next(r for r in range(12) if 2**r>h)
    start=2**(first+1)-2
    for n in range(start,start+300):
        assert len({key(n+j) for j in range(h)})==h
    windows.append({'length':h,'first_large_block_start':start,'tested_starts':300,'proof_needed':'all later pair gaps exceed window length'})
# Complete truth table, preserving all variables rather than only its count.
truth=[]
for x in [0,1]:
 for ya in [0,1]:
  for yb in [0,1]:
   da=int(x!=ya);db=int(x!=yb);dy=int(ya!=yb)
   assert dy<=da+db
   truth.append({'common_x':x,'ya':ya,'yb':yb,'y_mismatch':dy,'a_error':da,'b_error':db})
offsets=[]
for b in [0,1,2,5,12]:
 m=next(m for m in range(1,100) if Fraction(2*b+1,2**m)<Fraction(1,10))
 r=next(r for r in range(20) if 2**r>m*(2*b+1)+2*b)
 pairs=positions(r)[:1]
 a=pairs[0][0];l=2**r
 for k in range(-b,b+1):
  coords=[a+i*(2*b+1)+k for i in range(m)]+[a+l+i*(2*b+1)+k for i in range(m)]
  assert len(set(coords))==2*m and min(coords)>=0
 offsets.append({'bound':b,'constraints':m,'block':r,'iid_union_upper_bound':str(Fraction(2*b+1,2**m))})
metrics=[]
for n in [1,2,10,100,1000]:
 y=math.log(n+1);x=y+1/(n+1)
 err=min(1,abs(x-y));stretched=min(1,abs(math.exp(x)-math.exp(y)))
 assert stretched>0.999999999
 metrics.append({'index':n,'ordinary':err,'stretched_component':stretched,'exceedance_probability':str(Fraction(1,n+1))})
print(json.dumps({'schema':'pr45-independent-handwritten-controls/v1','complete_pair_truth_table':truth,'finite_window_controls':windows,'finite_offset_constraints':offsets,'metric_hostile_controls':metrics,'dependent_offset_periodic_example':{'x':[n%2 for n in range(12)],'y_phase0':[n%2 for n in range(12)],'y_phase1':[(n+1)%2 for n in range(12)],'S':'phase','T':0},'setwise_hostile_set':'first coordinate positive','escaping_offset_tail_bound':'2^-n','limits':'finite controls check algebra/indexing; universal statements rely on the accompanying proofs'},indent=2))
