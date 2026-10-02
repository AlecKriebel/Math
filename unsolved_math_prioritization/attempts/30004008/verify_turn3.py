"""Independent finite checks of exact Hall quotas and projected-root capacities."""
import itertools as it,json,random
N=0
def check(x):
 global N
 N+=1
 assert x

def matching(a,labels,J):
 slots=[j for j,k in enumerate(a) for _ in range(k)];m={}
 def aug(j,seen):
  for c,l in enumerate(labels):
   if c not in J and l!=j and c not in seen:
    seen.add(c)
    if c not in m or aug(m[c],seen):m[c]=j;return True
  return False
 return all(aug(j,set()) for j in slots)

def lower(a,labels):
 A=sum(a);return [max(0,labels.count(j)-A+a[j]) for j in range(len(a))]

def quota(a,labels,J):return all(sum(labels[c]==j for c in J)>=L for j,L in enumerate(lower(a,labels)))

def criterion(d,proj,L,attach,P):
 vs=set(proj);m={v:proj.count(v) for v in vs};lo={v:sum(L[j] for j,x in enumerate(attach) if x==v) for v in vs}
 cap={v:m[v] if v in P else min(1,m[v]) for v in vs}
 return all(lo[v]<=cap[v] for v in vs) and sum(lo.values())<=d<=sum(cap.values())

def main():
 hall_cases=0;instances=0;capacity_cases=0
 # Full count vectors for up to three pieces, pendant sizes1 or2, core d0..2,
 # q<=7. -1 labels colors rooted inside the core.
 for t in range(1,4):
  for a in it.product([1,2],repeat=t):
   for d in range(3):
    q=sum(a)+d
    if q>7:continue
    for labels in it.combinations_with_replacement(range(-1,t),q):
     L=lower(a,list(labels));anyJ=False
     for J0 in it.combinations(range(q),d):
      J=set(J0);x=quota(a,list(labels),J);check(x==matching(a,labels,J));hall_cases+=1;anyJ|=x
     check(anyJ==(sum(L)<=d));check(anyJ==all(sum(a)+d-labels.count(j)>=a[j] for j in range(t)));instances+=1
 rng=random.Random(300040083)
 for rep in range(1000):
  s=rng.randrange(2,7);d=s-1;t=rng.randrange(0,4);a=[rng.randrange(1,3) for _ in range(t)];q=sum(a)+d
  if q>10:continue
  labels=[rng.randrange(-1,t) for _ in range(q)] if t else [-1]*q
  attach=[rng.randrange(s) for _ in range(t)]
  proj=[attach[j] if j>=0 else rng.randrange(s) for j in labels];L=lower(a,labels)
  feasible=[]
  for J0 in it.combinations(range(q),d):
   J=set(J0)
   if quota(a,labels,J):feasible.append({v for v in set(proj) if sum(proj[c]==v for c in J)>=2})
  for k in range(3):
   for P0 in it.combinations(range(s),k):
    P=set(P0);expected=any(z<=P for z in feasible);check(criterion(d,proj,L,attach,P)==expected);capacity_cases+=1
 # Explicit quota obstruction despite enough unconditioned capacity.
 a=[1,1,1];labels=[0]*4+[1]*4+[2]*4;proj=labels;L=lower(a,labels);check(L==[2,2,2]);check(3+3+3==9)
 check(not any(criterion(9,proj,L,[0,1,2],set(P)) for P in it.combinations(range(3),2)))
 check(sum(L)<=9);check(lower([2],[0,0,0])==[3]);check(not matching([2],[0,0,0],{0}))
 print(json.dumps({'problem_id':30004008,'turn':3,'status':'PASS','exact_assertions':N,'exhaustive_hall_instances':instances,'reserved_subsets_compared_to_matching':hall_cases,'projected_capacity_subcases':capacity_cases,'scope':'Exact bounded verification of matching/quota equivalence and the at-most-two-multi-root reserve criterion; no general core existence asserted.'},indent=2))
if __name__=='__main__':main()
