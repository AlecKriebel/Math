# Locally authored exploratory search. Only certified Artin/Markov moves, no external knot package.
from collections import deque
from itertools import combinations
import json
W=(-1,-1,2,2,2,-1,3,2,2,2,3)
# A state is (strand count, word). Paths explicitly retain every move.
def neighbors(n,w):
 l=len(w)
 if l:
  yield (n,w[1:]+w[:1]),('cyclic_left',)
 for i in range(l-1):
  if w[i]==-w[i+1]:yield (n,w[:i]+w[i+2:]),('cancel',i)
  if abs(abs(w[i])-abs(w[i+1]))>1:
   yield (n,w[:i]+(w[i+1],w[i])+w[i+2:]),('commute',i)
 for i in range(l-2):
  a,b,c=w[i:i+3]
  if a==c and abs(abs(a)-abs(b))==1 and (a>0)==(b>0):
   yield (n,w[:i]+(b,a,b)+w[i+3:]),('artin',i)
 # Inverse/mixed Artin consequences are handled as explicit three-letter equality.
 # a b a^-1 = b^-1 a b for neighboring same-sign generators a,b.
  if a==-c and abs(abs(a)-abs(b))==1 and (a>0)==(b>0):
   yield (n,w[:i]+(-b,a,b)+w[i+3:]),('mixed_artin',i)
  # reverse mixed equality b^-1 a b = a b a^-1
  if a==-c and abs(abs(a)-abs(b))==1 and (a>0)!=(b>0):
   yield (n,w[:i]+(b,-a,-b)+w[i+3:]),('mixed_artin_reverse',i)
 if n>1:
  for end in (1,n-1):
   ix=[i for i,x in enumerate(w) if abs(x)==end]
   if len(ix)==1:
    i=ix[0];out=w[:i]+w[i+1:]
    if end==1:out=tuple((1 if x>0 else -1)*(abs(x)-1) for x in out)
    yield (n-1,out),('destabilize_end',end,i)

def search(changes,limit=200000):
 w=tuple(-x if i in changes else x for i,x in enumerate(W));start=(4,w);todo=deque([start]);pred={start:None}
 while todo and len(pred)<limit:
  s=todo.popleft()
  if s==(1,()):
   path=[]
   while pred[s] is not None:
    old,op=pred[s];path.append({'before':[old[0],list(old[1])],'move':op,'after':[s[0],list(s[1])]});s=old
   return {'changes_zero_based':changes,'initial':[4,list(w)],'moves':path[::-1],'states_seen':len(pred)}
  for t,op in neighbors(*s):
   if t not in pred:pred[t]=(s,op);todo.append(t)
 return {'changes_zero_based':changes,'found':False,'states_seen':len(pred),'exhausted_this_move_graph':not todo}
results=[];found=None
for k in (2,3):
 for changes in combinations(range(len(W)),k):
  r=search(changes);results.append(r)
  if 'moves' in r:found=r;break
 if found:break
two=[r for r in results if len(r['changes_zero_based'])==2]
out={'two_change_subsets':len(two),'two_change_total_states':sum(r['states_seen'] for r in two),'all_two_change_move_graphs_exhausted':all(r['exhausted_this_move_graph'] for r in two),'first_successful_three_change_subset':found['changes_zero_based'] if found else None,'total_starting_subsets_tried':len(results),'certificate_moves':len(found['moves']) if found else None,'failure_scope':'Only the stated non-length-increasing Artin/Markov move graph; not all diagrams or even a complete unknot-recognition algorithm.'}
print(json.dumps(out,indent=2))
