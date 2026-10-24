#!/usr/bin/env python3
"""Independent bounded audit. Unbounded deductions are checked in AUDIT.md.

Uses integer matrix powers, breadth-first graph components, and RAAG pilings,
rather than the author's binomial formula, union-find, and cancellation scan.
"""
from collections import deque
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'special_construction'
NAMES = ['ALGEBRAIC_REDUCTIONS.md', 'SPECIAL_ANALOGUE_LIFT.md',
         'FIBER_ABELIAN_COVER_OBSTRUCTION.md', 'check_algebraic_reductions.py',
         'algebraic_reduction_checks.json', 'check_finite_covers.py',
         'finite_cover_results.json']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def identity(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))

def mm(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))

def mv(a, v):
    return tuple(sum(x*y for x,y in zip(row,v)) for row in a)

def mp(a, k):
    n = len(a)
    if k < 0:
        # Invert I+N by its finite geometric series, with N strictly upper triangular.
        ident = identity(n)
        nil = tuple(tuple(a[i][j] - ident[i][j] for j in range(n)) for i in range(n))
        power = ident
        inverse = [list(row) for row in ident]
        for exponent in range(1,n):
            power = mm(power, nil)
            for i in range(n):
                for j in range(n):
                    inverse[i][j] += (-1)**exponent * power[i][j]
        a = tuple(map(tuple, inverse))
        k = -k
    answer = identity(n)
    while k:
        if k & 1:
            answer = mm(answer, a)
        a = mm(a, a)
        k //= 2
    return answer

class Semi:
    def __init__(self,n,p=None,height=None):
        self.n,self.p,self.height = n,p,height
        self.j = tuple(tuple(int(i==j) + int(j==i+1) for j in range(n))
                       for i in range(n))
        self.powers = {}
        self.one = ((0,)*n,0)
    def normalize(self,x):
        v,k = x
        if self.p is not None:
            v = tuple(a%self.p for a in v)
        if self.height is not None:
            k %= self.height
        return v,k
    def phi(self,v,k):
        if k not in self.powers:
            self.powers[k] = mp(self.j,k)
        return mv(self.powers[k],v)
    def mul(self,x,y):
        v,k=x; w,l=y
        pw = self.phi(w,-k)
        return self.normalize((tuple(a+b for a,b in zip(v,pw)),k+l))
    def inv(self,x):
        v,k=x
        return self.normalize((self.phi(tuple(-a for a in v),k),-k))
    def comm(self,x,y):
        return self.mul(self.mul(self.mul(x,y),self.inv(x)),self.inv(y))
    def basis(self,j):
        return tuple(int(i==j) for i in range(self.n))
    def generators(self):
        s = self.normalize(((0,)*self.n,-1))
        u = {self.n:(self.basis(self.n-1),0)}
        for i in range(self.n-1,0,-1):
            u[i]=self.mul(self.mul(self.inv(u[i+1]),s),u[i+1])
        return [s] + [u[i] for i in range(1,self.n+1)]

def integral_checks():
    cases=[]
    for n in range(3,41):
        group=Semi(n)
        gs=group.generators(); s=gs[0]; U=gs[1]
        V=group.mul(group.mul(gs[n],s),group.inv(gs[n]))
        assert U==(group.basis(0),-1)
        assert V==(tuple(-a for a in group.basis(n-2)),-1)
        W=group.comm(U,V)
        assert W==(tuple(-a for a in group.basis(n-3)),0)
        for _ in range(n-3):
            W=group.comm(V,W)
        assert W==(tuple(-a for a in group.basis(0)),0)
        assert group.mul(W,U)==s
        a=group.inv(group.mul(V,group.inv(s)))
        assert a==(group.basis(n-2),0)
        for i in range(n-3,-1,-1):
            a=group.comm(s,a)
            assert a==(group.basis(i),0)
        for u in gs[1:n]:
            assert u[0][-1]==0 and u[1]==-1
        cases.append(n)
    return cases

def cover_check(n,p):
    height=1
    while height<n:
        height*=p
    group=Semi(n,p,height)
    vectors=list(product(range(p),repeat=n))
    elems=[(v,k) for k in range(height) for v in vectors]
    indexes={g:i for i,g in enumerate(elems)}
    gs=group.generators()
    action=[[indexes[group.mul(g,x)] for g in elems] for x in gs]
    size=len(elems)
    # Build the whole edge-midpoint transport graph, then BFS its components.
    adjacency=[[] for _ in range(size*(n+1))]
    def edge(g,i):
        return g*(n+1)+i
    def add(a,b):
        adjacency[a].append(b);adjacency[b].append(a)
    for g in range(size):
        for i in range(1,n+1):
            add(edge(g,i),edge(action[0][g],i))
            add(edge(g,0),edge(action[i][g],i-1))
    components=[-1]*len(adjacency); count=0
    for start in range(len(adjacency)):
        if components[start]>=0:
            continue
        components[start]=count; todo=deque([start])
        while todo:
            u=todo.popleft()
            for v in adjacency[u]:
                if components[v]<0:
                    components[v]=count;todo.append(v)
        count+=1
    witnesses=[]
    for g in range(size):
        for i in range(1,n+1):
            if components[edge(g,0)]==components[edge(g,i)]:
                witnesses.append({'vertex':g,'square':i})
                if len(witnesses)==12:
                    break
        if len(witnesses)==12:
            break
    # Verify the stronger all-vertex, all-claimed-square obstruction.
    if n>=3:
        for g in range(size):
            for i in range(1,n-1):
                assert components[edge(g,0)]==components[edge(g,i)]
    return {'rank':n,'prime':p,'vertices':size,'hyperplanes':count,
            'self_crossing':bool(witnesses),'first_self_crossings':witnesses,
            'all_claimed_squares_checked':size*max(n-2,0)}

COMMUTE={frozenset((1,2)),frozenset((2,3)),frozenset((1,4))}
def piling_trivial(word):
    stacks={i:[] for i in range(1,5)}
    for x in word:
        i=abs(x); sign=1 if x>0 else -1
        blockers=[j for j in stacks if j!=i and frozenset((i,j)) not in COMMUTE]
        if stacks[i] and stacks[i][-1]==-sign:
            stacks[i].pop()
            for j in blockers:
                assert stacks[j] and stacks[j][-1]==0
                stacks[j].pop()
        else:
            stacks[i].append(sign)
            for j in blockers:
                stacks[j].append(0)
    return all(not stack for stack in stacks.values())

IMAGES={1:[1],2:[2],3:[-3,1,3],4:[4,3]}
def inverse(word):
    return [-x for x in reversed(word)]
def expand(word):
    answer=[]
    for x in word:
        answer.extend(IMAGES[x] if x>0 else inverse(IMAGES[-x]))
    return answer
def reduced(word):
    ans=[]
    for x in word:
        if ans and ans[-1]==-x:
            ans.pop()
        else:
            ans.append(x)
    return ans

def small_rank_checks():
    # The three Reidemeister--Schreier presentation relators.
    relations=[[1,2,-1,-2],[2,3,-2,-3],[-4,1,4,-3]]
    assert all(piling_trivial(expand(w)) for w in relations)
    # Independent finite check of F(x,w) injection by free expansion in F(p,c).
    free_tests=0
    for length in range(1,9):
        for word in product((1,-1,3,-3),repeat=length):
            if len(reduced(word))!=length:
                continue
            assert reduced(expand(word))
            free_tests+=1
    # New sample stream; test source Britton reducedness independently.
    rng=random.Random(962125)
    samples=0
    for _ in range(16000):
        eps=[rng.choice((-1,1)) for _ in range(rng.randrange(1,13))]
        source=[]
        for i,e in enumerate(eps):
            source.append(4*e)
            if i+1<len(eps):
                while True:
                    fw=reduced([rng.choice((1,-1,3,-3)) for _ in range(rng.randrange(12))])
                    power=rng.randrange(-5,6)
                    prohibited=(power==0 and
                        ((e==-1 and eps[i+1]==1 and all(abs(x)==1 for x in fw)) or
                         (e==1 and eps[i+1]==-1 and all(abs(x)==3 for x in fw))))
                    if not prohibited:
                        break
                source+=fw+[2 if power>0 else -2]*abs(power)
        assert not piling_trivial(expand(source))
        samples+=1
    # Check original words x=asa^-1,y=s,w=u,r=a^2 satisfy their RS identities
    # directly using the original free-by-cyclic normal form. Matrix checks
    # cannot establish those nonabelian identities, so AUDIT supplies RS proof.
    return {'relator_checks':len(relations),'free_base_words':free_tests,
            'independent_britton_samples':samples,'method':'RAAG piling'}

def coset_counterexample():
    group=Semi(2,2,2)
    s,u,a=group.generators()
    # P=<u, a s a^-1> equals {1,u} in this order-eight quotient.
    v=group.mul(group.mul(a,s),group.inv(a))
    assert u==v and group.mul(u,u)==group.one
    subgroup={group.one,u}
    g=a; h=group.mul(a,u)
    assert group.mul(group.inv(g),h) in subgroup
    assert group.mul(h,group.inv(g)) not in subgroup
    return {'quotient_order':8,'g':g,'h':h,'P':sorted(subgroup),
            'g_inverse_h_in_P':True,'h_g_inverse_in_P':False,
            'conclusion':'transport components use gP; standard terminology is left coset'}

def author_reproduction():
    answer={}
    with tempfile.TemporaryDirectory(prefix='p21125-constructive-audit-') as tmp:
        tmp=Path(tmp)
        for script,output in [('check_algebraic_reductions.py','algebraic_reduction_checks.json'),
                              ('check_finite_covers.py','finite_cover_results.json')]:
            shutil.copy2(INPUT/script,tmp/script)
            p=subprocess.run([sys.executable,str(tmp/script)],check=True,
                             capture_output=True,text=True)
            actual=json.loads((tmp/output).read_text())
            expected=json.loads((INPUT/output).read_text())
            assert actual==expected,(script,'output mismatch')
            answer[script]={'exact_json_reproduced':True,'stdout':p.stdout.strip()}
    return answer

def main():
    start=datetime.now(timezone.utc).isoformat()
    before={name:digest(INPUT/name) for name in NAMES}
    author=author_reproduction()
    integral=integral_checks()
    raag=small_rank_checks()
    expected=json.loads((INPUT/'finite_cover_results.json').read_text())['results']
    covers=[]
    for row in expected:
        result=cover_check(row['rank'],row['prime'])
        for key in ['rank','prime','vertices','hyperplanes','self_crossing','first_self_crossings']:
            assert result[key]==row[key],(key,result,row)
        covers.append(result)
    after={name:digest(INPUT/name) for name in NAMES}
    assert before==after,'Frozen author input changed during review'
    result={'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),
            'frozen_inputs':before,'author_reproduction':author,
            'integral_ranks_checked':integral,'small_rank':raag,'finite_covers':covers,
            'coset_wording_counterexample':coset_counterexample(),
            'scope':'All tests bounded. Unbounded proofs and scope corrections are in AUDIT.md.',
            'all_bounded_checks_passed':True}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':'PASS','integral_ranks':len(integral),
                      'finite_quotient_covers':len(covers),**raag}))

if __name__=='__main__':
    main()
