"""Fresh exact Temperley--Lieb/Jones calibration; no imported verifier code.

All coefficients are integers, then invariant normalization uses Fraction.
Boundary points are ordered top-left to right, then bottom-left to right.
Positive braid generator: A*identity + A**(-1)*e_i.
Closure trace: delta**(number_of_loops-1), delta=-A**2-A**(-2).
Jones normalization: (-A**3)**(-w), q=A**(-4).
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import datetime, hashlib, json, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parent

def add(a,b):
    c=defaultdict(int,a)
    for k,v in b.items(): c[k]+=v
    return {k:v for k,v in c.items() if v}

def mul(a,b):
    c=defaultdict(int)
    for x,u in a.items():
        for y,v in b.items(): c[x+y]+=u*v
    return {k:v for k,v in c.items() if v}

def shift(a,s,sign=1): return {k+s:sign*v for k,v in a.items()}

@lru_cache(None)
def delta_power(k):
    assert k>=0
    out={0:1}
    for _ in range(k): out=mul(out,{2:-1,-2:-1})
    return out

class DSU:
    def __init__(self,n): self.parent=list(range(n))
    def root(self,x):
        while self.parent[x]!=x:
            self.parent[x]=self.parent[self.parent[x]]; x=self.parent[x]
        return x
    def join(self,a,b): self.parent[self.root(a)]=self.root(b)

@lru_cache(None)
def identity(m): return tuple(list(range(m,2*m))+list(range(m)))

@lru_cache(None)
def generator(m,i):
    a=list(identity(m)); a[i]=i+1; a[i+1]=i
    a[m+i]=m+i+1; a[m+i+1]=m+i
    return tuple(a)

@lru_cache(None)
def compose(a,b):
    m=len(a)//2; d=DSU(3*m)
    for x,y in enumerate(a): d.join(x,y)
    for x,y in enumerate(b):
        d.join(x+m,y+m)
    external=list(range(m))+list(range(2*m,3*m))
    groups=defaultdict(list)
    for x in external: groups[d.root(x)].append(x)
    allroots={d.root(x) for x in range(3*m)}
    loops=len(allroots-set(groups))
    matching=[None]*(2*m)
    toboundary=lambda x:x if x<m else x-m
    for endpoints in groups.values():
        assert len(endpoints)==2
        x,y=map(toboundary,endpoints); matching[x]=y; matching[y]=x
    return tuple(matching),loops

@lru_cache(None)
def closure_loops(a):
    m=len(a)//2; d=DSU(2*m)
    for x,y in enumerate(a): d.join(x,y)
    for i in range(m): d.join(i,m+i)
    return len({d.root(x) for x in range(2*m)})

@lru_cache(None)
def jones(m,word):
    state={identity(m):{0:1}}
    for letter in word:
        assert 1<=abs(letter)<m
        s=1 if letter>0 else -1; e=generator(m,abs(letter)-1)
        new={}
        for basis,coeff in state.items():
            new[basis]=add(new.get(basis,{}),shift(coeff,s))
            composed,loops=compose(basis,e)
            term=mul(shift(coeff,-s),delta_power(loops))
            new[composed]=add(new.get(composed,{}),term)
        state={b:p for b,p in new.items() if p}
    bracket={}
    for basis,coeff in state.items():
        bracket=add(bracket,mul(coeff,delta_power(closure_loops(basis)-1)))
    writhe=sum(1 if x>0 else -1 for x in word)
    normalized=shift(bracket,-3*writhe,-1 if writhe%2 else 1)
    assert all(a%4==0 for a in normalized),('link or convention error',m,word,normalized)
    return {-a//4:c for a,c in sorted(normalized.items())}

def jones_invariants(J):
    one=sum(J.values()); first=sum(k*c for k,c in J.items())
    second=sum(k*(k-1)*c for k,c in J.items())
    third=sum(k*(k-1)*(k-2)*c for k,c in J.items())
    assert one==1 and first==0
    return Fraction(-second,6),Fraction(-(third+3*second),36)

def gauss_from_braid(m,word):
    at_position=list(range(m)); visits=[[] for _ in range(m)]
    signs={}
    for crossing,letter in enumerate(word):
        i=abs(letter)-1; left,right=at_position[i:i+2]
        positive=letter>0; signs[crossing]=1 if positive else -1
        visits[left].append((crossing,positive))
        visits[right].append((crossing,not positive))
        at_position[i:i+2]=[right,left]
    successor={strand:pos for pos,strand in enumerate(at_position)}
    components=[]; seen=set()
    for start in range(m):
        if start in seen: continue
        seq=[]; strand=start
        while strand not in seen:
            seen.add(strand); seq.extend(visits[strand]); strand=successor[strand]
        assert strand==start
        components.append(seq)
    return components,signs

P=((3,0),(5,1),(2,4))
T=((3,0),(1,4),(5,2))

def pattern_key(pairs):
    return min(tuple(sorted(((t+r)%6,(h+r)%6) for t,h in pairs)) for r in range(6))

PK,TK=pattern_key(P),pattern_key(T)

def arrow_evaluation(seq,signs):
    endpoints=defaultdict(dict)
    for position,(crossing,over) in enumerate(seq):
        endpoints[crossing]['t' if over else 'h']=position
    totals={'P_signed':0,'T_signed':0,'P_unsigned':0,'T_unsigned':0}
    for triple in combinations(sorted(endpoints),3):
        selected=sorted(endpoints[c][role] for c in triple for role in ['t','h'])
        relabel={old:new for new,old in enumerate(selected)}
        pairs=[(relabel[endpoints[c]['t']],relabel[endpoints[c]['h']]) for c in triple]
        key=pattern_key(pairs)
        name='P' if key==PK else 'T' if key==TK else None
        if name:
            weight=1
            for c in triple: weight*=signs[c]
            totals[name+'_signed']+=weight; totals[name+'_unsigned']+=1
    value=Fraction(totals['P_signed'],2)+totals['T_signed']
    return value,totals

def validate_case(name,m,word,expected=None):
    word=tuple(word); components,signs=gauss_from_braid(m,word)
    if len(components)!=1: return None
    J=jones(m,word); v2,v3=jones_invariants(J)
    arrow,counts=arrow_evaluation(components[0],signs)
    n=len(word); floor=n*(n*n-1)//24
    even=Fraction(n*(n*n-4),24) if n%2==0 else None
    row={'name':name,'strands':m,'word':word,'crossings':n,'jones':J,'v2':str(v2),'jones_v3':str(v3),'arrow_v3':str(arrow),'counts':counts,'floor_bound':floor,'even_bound':str(even) if even is not None else None}
    assert v3.denominator==1,('integrality',row)
    assert arrow==v3,('arrow/Jones mismatch',row)
    assert abs(v3)<=floor,('target violation',row)
    if even is not None: assert even.denominator==1 and abs(v3)<=even,('even violation',row)
    if expected is not None: assert v3==expected,('expected normalization',row,expected)
    # Reverse orientation changes endpoint order but not over/under roles.
    assert arrow_evaluation(list(reversed(components[0])),signs)[0]==v3,('orientation reversal',row)
    return row

def main():
    rows=[]; skipped=0
    def check(name,m,word,expected=None):
        nonlocal skipped
        row=validate_case(name,m,word,expected)
        if row is None: skipped+=1
        else: rows.append(row)
        return row
    curated=[('unknot',1,[],0),('positive_RI',2,[1],0),('negative_RI',2,[-1],0),('right_trefoil',2,[1]*3,1),('left_trefoil',2,[-1]*3,-1),('figure_eight',3,[1,-2]*2,0),('T_2_5',2,[1]*5,5),('T_2_7',2,[1]*7,14),('T_2_9',2,[1]*9,30),('T_3_4',3,[1,2]*4,10),('T_3_5',3,[1,2]*5,20),('T_4_3',4,[1,2,3]*3,10),('T_5_2',5,[1,2,3,4]*2,5),('trefoil_sum_trefoil',3,[1]*3+[2]*3,2),('trefoil_sum_mirror',3,[1]*3+[-2]*3,0)]
    for name,m,word,expected in curated:
        base=check(name,m,word,expected)
        mirror=check(name+'_mirror',m,[-x for x in word],-expected)
        if m<5:
            for sign in (-1,1):
                stabilized=check(name+'_Markov_'+str(sign),m+1,word+[sign*m],expected)
                assert stabilized['jones']==base['jones']
        if m>=2:
            for i in range(1,m):
                inserted=check(name+'_RII_'+str(i),m,word[:len(word)//2]+[i,-i]+word[len(word)//2:],expected)
                assert inserted['jones']==base['jones']
        if word:
            cyclic=check(name+'_cyclic',m,word[1:]+word[:1],expected)
            assert cyclic['jones']==base['jones']
    # Bounded exhaustive 3-braid words, length <=5, including every sign.
    for length in range(1,6):
        for word in product((-2,-1,1,2),repeat=length):
            check('exhaustive_3_braid',3,list(word))
    # Fixed seeded signed closures, lengths 6--14, 3--5 strands.
    rng=random.Random(10400033)
    for index in range(160):
        m=rng.choice((3,4,5)); length=rng.randrange(6,15)
        word=[rng.choice((-1,1))*rng.randrange(1,m) for _ in range(length)]
        base=check('seeded_'+str(index),m,word)
        if base:
            mirror=check('seeded_'+str(index)+'_mirror',m,[-x for x in word])
            assert Fraction(mirror['jones_v3'])==-Fraction(base['jones_v3'])
            assert mirror['jones']=={-int(k):c for k,c in base['jones'].items()}
    # Positive and negative RIII, closed inside arbitrary short suffixes.
    for sign in (-1,1):
        for suffix in ([1],[2],[1,2,1],[-2,1,-2],[-1,2,1,-2,1]):
            left=check('RIII_left',3,[sign,2*sign,sign]+suffix)
            right=check('RIII_right',3,[2*sign,sign,2*sign]+suffix)
            assert (left is None)==(right is None)
            if left: assert left['jones']==right['jones'] and left['jones_v3']==right['jones_v3']
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'exact integer Temperley--Lieb matching multiplication and full normalized Jones polynomial','evaluated_knot_closures':len(rows),'skipped_multicomponent_closures':skipped,'distinct_braid_words':len({(r['strands'],tuple(r['word'])) for r in rows}),'max_crossings':max(r['crossings'] for r in rows),'all_calibration_checks_passed':True,'rows':rows}
    (ROOT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
    print('Known-example polynomial calibrations:')
    for row in rows:
        if row['name'] in {'right_trefoil','left_trefoil','figure_eight','T_3_4','trefoil_sum_trefoil','trefoil_sum_mirror'}: print(json.dumps(row))

if __name__=='__main__': main()
