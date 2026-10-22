"""Own exact controls for the localized free-product and polynomial intersection.

Finite word controls supplement, and do not replace, the all-word proof.
"""
from collections import Counter
from itertools import product
import json
import sympy as s

C=Counter()
def check(v,key):
    assert v,key
    C[key]+=1

def reduce_ab(word):
    out=[]
    for letter,a in word:
        if not a: continue
        if out and out[-1][0]==letter:
            a+=out.pop()[1]
        if a: out.append((letter,a))
    return out

def reduce_g(word):
    out=[]
    for a,e in word:
        if not a: continue
        if out and out[-1]==(a,-e): out.pop()
        else: out.append((a,e))
    return out

def alpha(b,word):
    out=[]
    for a,e in word:
        out+=([(a+b,1),(b,-1)] if e==1 else [(b,1),(a+b,-1)])
    return reduce_g(out)

def normal(word):
    # (h,c) denotes h A_c. B_t = G_(-t)^(-1) A_(-t).
    h=[];c=0
    for letter,t in word:
        if letter=='A': c+=t
        else:
            h=reduce_g(h+alpha(c,[(-t,-1)]))
            c-=t
    return h,c

def rebuild(h,c):
    out=[]
    for a,e in h:
        out+=([('A',a),('B',a)] if e==1 else [('B',-a),('A',-a)])
    return reduce_ab(out+[('A',c)])

letters=list(product('AB',[-2,-1,1,2]))
word_count=0
for length in range(5):
    for word in product(letters,repeat=length):
        h,c=normal(word)
        check(rebuild(h,c)==reduce_ab(word),'semidirect_normal_form')
        check(c==sum(t if k=='A' else -t for k,t in word),'character_coordinate')
        word_count+=1
for a,b,c in product(range(-3,4),repeat=3):
    check(alpha(b,alpha(c,[(a,1)]))==alpha(b+c,[(a,1)]),'additive_action_identity')
    check(reduce_ab([('A',b),('A',a),('B',a),('A',-b)])==
          reduce_ab([('A',a+b),('B',a+b),('B',-b),('A',-b)]),
          'family_conjugation_identity')
for a in [-3,-2,-1,1,2,3]:
    check(normal([('A',a),('B',a)])==([(a,1)],0),'free_generator_normal_form')
    for b in [-3,-2,-1,1,2,3]:
        h,c=normal([('A',a),('B',a),('B',-b),('A',-b)])
        check(c==0 and sum(e for _,e in h)==0,'known_relative_word_augmentation')
        check((h==[])==(a==b),'relative_word_nonidentity')

x,y,z,a,b,u,v=s.symbols('x y z a b u v')
D=x*x*y+z*z
Ay=y-2*a*z*D/x-a*a*D**2
By=y+2*a*z**3/x
check(s.expand(x*Ay).subs(x,0)==-2*a*z**3,'actual_A_pole')
check(s.expand(x*By).subs(x,0)==2*a*z**3,'actual_B_pole')
Av={u:u,v:v+a*x*u}
Bv={u:u+2*a*x*v**3,v:v}
AB={q:s.expand(Bv[q].xreplace(Av)) for q in (u,v)}
check(AB[v]==v+a*x*u,'ring_composition_v')
check(s.expand(AB[u]-(u+2*a*x*(v+a*x*u)**3))==0,'ring_composition_u')
# Exact small cyclic-word degrees. x=1 is a nonzero K coefficient;
# arbitrary nonzero coefficients and every length are proved in TURN_3.md.
for block in [[(1,1)],[(1,2),(-1,3)],[(2,-1),(1,1),(-2,3)]]:
    U,V=u,v
    for aa,bb in block:
        Vnew=s.expand(V+aa*U)
        U,V=s.expand(U+2*bb*Vnew**3),Vnew
    r=len(block)
    check(s.Poly(U,u,v).total_degree()==3**r,'cyclic_block_degree_u')
    check(s.Poly(V,u,v).total_degree()==3**(r-1),'cyclic_block_degree_v')

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),
 'formal_words':word_count,'families':dict(C),
 'scope':'Finite symbolic and abstract-word diagnostics for the proved relative subgroup classification. No membership or nonmembership verdict for the full polynomial-LND generated subgroup.'},indent=2,sort_keys=True))
