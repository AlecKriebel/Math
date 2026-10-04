from itertools import product,cycle,islice
from collections import deque
from math import gcd
import json
checks=0

def verify(condition):
 global checks
 if not condition: raise AssertionError('independent falsifier check failed')
 checks+=1

def transform(word,tau,antimorphic=True):
 return tuple(tau[x] for x in (reversed(word) if antimorphic else word))

def literal_alternating(word,r,tau,antimorphic=True):
 if r<=0: raise ValueError('period must be positive')
 if len(word)<=r: return True
 seed=word[:r]
 return word==tuple(islice(cycle(seed+transform(seed,tau,antimorphic)),len(word)))

def canonical_graph_word(p,q,n):
 adj=[[] for _ in range(n)]
 for r in (p,q):
  for i in range(r,n):
   base=i%(2*r)
   if base<r: j,sign=base,0
   else: j,sign=2*r-1-base,1
   adj[i].append((j,sign));adj[j].append((i,sign))
 seen=[False]*n;parity=[0]*n;word=[None]*n;tau=[];components=[]
 for origin in range(n):
  if seen[origin]: continue
  seen[origin]=True;queue=deque([origin]);members=[];forced=False
  while queue:
   here=queue.popleft();members.append(here)
   for there,sign in adj[here]:
    wanted=parity[here]^sign
    if not seen[there]: seen[there]=True;parity[there]=wanted;queue.append(there)
    elif parity[there]!=wanted: forced=True
  a=len(tau)
  if forced:
   tau.append(a)
   for i in members: word[i]=a
  else:
   tau.extend((a+1,a))
   for i in members: word[i]=a+parity[i]
  components.append({'positions':members,'forced_fixed':forced})
 return tuple(word),tuple(tau),components

# Explicit alphabets: arbitrary fixed letters, complement, and mixed involutions.
word_domains=[('unary_identity',(0,),12),('binary_reversal',(0,1),10),('binary_reverse_complement',(1,0),10),('ternary_reversal',(0,1,2),8),('ternary_mixed',(1,0,2),8),('quaternary_mixed',(1,0,2,3),7)]
word_report=[]
for name,tau,limit in word_domains:
 words=0;qualifying=0;period_tests=0
 for n in range(limit+1):
  for word in product(range(len(tau)),repeat=n):
   words+=1
   ps=[r for r in range(1,n+4) if literal_alternating(word,r,tau)]
   period_tests+=n+3
   for p in ps:
    for q in ps:
     d=gcd(p,q)
     if n>=p+q-d:
      verify(literal_alternating(word,d,tau));qualifying+=1
   if n==0: verify(len(ps)==3)
 word_report.append({'name':name,'tau':tau,'lengths':[0,limit],'words':words,'period_tests':period_tests,'qualifying_ordered_pairs':qualifying})

# Convention and excluded morphic controls. A binary theta-period is not generally alternating.
verify(literal_alternating((),1,(0,1)))
verify(literal_alternating((0,),3,(0,1)))
try: literal_alternating((),0,(0,1));raise AssertionError('zero period accepted')
except ValueError: checks+=1
verify(not literal_alternating((0,0,1),1,(1,0)))
verify(literal_alternating((0,0,1),1,(1,0),False)==False)
verify(transform((0,1,2),(1,0,2))==(2,0,1))
verify(transform((0,1,2),(1,0,2),False)==(1,0,2))
# Fixed and transposed letters coexist; transformation is involutive.
verify(transform(transform((0,2,1),(1,0,2)),(1,0,2))==(0,2,1))

# Unrestricted-alphabet canonical graph: each fixed finite pair is universal in A,tau.
maximum=200;threshold_pairs=0;longer_pairs=0;below_failures=0;below_examples=[];between_cases=0;max_symbols=0;fixed_and_free_cases=0
for p in range(1,maximum+1):
 for q in range(1,p+1):
  d=gcd(p,q);n0=p+q-d
  for n,kind in ((n0,'threshold'),(p+q-1,'longer')):
   word,tau,parts=canonical_graph_word(p,q,n)
   verify(literal_alternating(word,p,tau));verify(literal_alternating(word,q,tau));verify(literal_alternating(word,d,tau))
   max_symbols=max(max_symbols,len(tau))
   if any(c['forced_fixed'] for c in parts) and any(not c['forced_fixed'] for c in parts):fixed_and_free_cases+=1
   if kind=='threshold': threshold_pairs+=1
   else: longer_pairs+=1
  if p<=50:
   for n in range(n0+1,p+q-1):
    word,tau,_=canonical_graph_word(p,q,n)
    verify(literal_alternating(word,p,tau));verify(literal_alternating(word,q,tau));verify(literal_alternating(word,d,tau));between_cases+=1
  n=n0-1
  word,tau,_=canonical_graph_word(p,q,n)
  verify(literal_alternating(word,p,tau));verify(literal_alternating(word,q,tau))
  if not literal_alternating(word,d,tau):
   below_failures+=1
   if len(below_examples)<20: below_examples.append({'p':p,'q':q,'gcd':d,'length':n,'word':word,'tau':tau})
# Original sharpness witness, checked literally with reversal.
verify(literal_alternating((0,1,1),2,(0,1)))
verify(literal_alternating((0,1,1),3,(0,1)))
verify(not literal_alternating((0,1,1),1,(0,1)))
print(json.dumps({'status':'PASS','assertions':checks,'explicit_alphabet_domains':word_report,'unrestricted_alphabet_graph':{'maximum_period':maximum,'threshold_pairs':threshold_pairs,'longer_pairs_at_p_plus_q_minus_one':longer_pairs,'all_interior_lengths_for_periods_at_most_50':between_cases,'maximum_canonical_alphabet_size':max_symbols,'cases_with_forced_fixed_and_free_components':fixed_and_free_cases,'below_threshold_failed_gcd_cases':below_failures,'first_below_threshold_witnesses':below_examples},'scope':'Finite evidence only in period parameters. Signed-component construction is exact for all alphabets/involutions at each checked finite triple. Literal alternating oracle verifies all premise and conclusion words.'},indent=2))
