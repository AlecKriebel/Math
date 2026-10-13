"""Bounded test of one proposed K9 -> K11, three -> four color extension.
The new vertices are uniform to old three-vertex blocks A and B, with rows
(0,3) and (1,3); their mutual edge is color 3. Only six cross edges remain.
A negative result rejects this particular ansatz, not any global theorem.
"""
from itertools import combinations, product
import json,signal,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'extend_k7_results.json').read_text())
oldcolors={tuple(v[:2]):v[2] for v in r['edge_colors']}
n=9;pairs=list(combinations(range(n),2));trips=list(combinations(range(n),3))
def sig(cs):return tuple(sorted(cs))
old=[(set(t),sig(oldcolors[e] for e in combinations(t,2))) for t in trips]
def valid(p):
 for i,j in pairs:
  ty=sig((p[i],p[j],oldcolors[i,j]))
  if any(i not in t and j not in t and ty==s for t,s in old):return False
 return True

def run():
 start=time.monotonic();ps=[(0,)*3+(3,)*3+p for p in product(range(4),repeat=3)];rs=[(1,)*3+(3,)*3+p for p in product(range(4),repeat=3)]
 ps=[p for p in ps if valid(p)];rs=[p for p in rs if valid(p)];tested=0;found=None
 for p,r in product(ps,rs):
  tested+=1
  wedgesp=[(set((i,j)),sig((p[i],p[j],oldcolors[i,j]))) for i,j in pairs]
  wedgesr=[(set((i,j)),sig((r[i],r[j],oldcolors[i,j]))) for i,j in pairs]
  if any(s.isdisjoint(t) and a==b for s,a in wedgesp for t,b in wedgesr):continue
  if any(i not in t and sig((p[i],r[i],3))==ty for i in range(n) for t,ty in old):continue
  found=(p,r);break
 out={'target_n':11,'target_q':4,'first_patterns_tested':64,'second_patterns_tested':64,'valid_first_patterns':len(ps),'valid_second_patterns':len(rs),'valid_pair_combinations_tested':tested,'status':'FOUND' if found else 'ANSATZ_REJECTED'}
 if found:
  p,r=found;colors=dict(oldcolors);colors.update({(i,9):p[i] for i in range(n)});colors.update({(i,10):r[i] for i in range(n)});colors[9,10]=3
  ts=list(combinations(range(11),3));checked=0
  for t,u in combinations(ts,2):
   if set(t).isdisjoint(u):
    assert sig(colors[e] for e in combinations(t,2))!=sig(colors[e] for e in combinations(u,2));checked+=1
  out.update(first_pattern=p,second_pattern=r,edge_colors=[[*e,c] for e,c in sorted(colors.items())],disjoint_pairs_checked=checked)
 else:out['warning']='Rejects only the specified uniform-block new-pair ansatz. No lower bound for g(11).'
 out['elapsed_seconds']=round(time.monotonic()-start,3)
 (ROOT/'pair_amplification_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':signal.alarm(30);run()
