#!/usr/bin/env python3
"""Independent finite controls for restricted122 construction obstructions.

S4 is AGL(2,2), not the author's point-permutation enumeration. Binary wreath
groups use recursive multiplication tables. No author code is imported.
"""
from pathlib import Path
from itertools import product
from collections import Counter, defaultdict
from math import gcd
from datetime import datetime, timezone
import json


def word_inverse(w):
    return tuple(-x for x in reversed(w))


def free_reduce(w):
    out=[]
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def words():
    c=(-1,-2,1,2)
    cx=(-1,)+c+(1,)
    return {
        'x_fourth':(1,1,1,1),
        'commutator_squared':c+c,
        'commutator_with_its_x_conjugate':word_inverse(c)+word_inverse(cx)+c+cx,
        'squared_commutator_of_squares':(-1,-1,-2,-2,1,1,2,2)*2,
    }


class FiniteGroup:
    def __init__(self, items, multiply, identity):
        self.items=list(items)
        self.index={g:i for i,g in enumerate(self.items)}
        self.identity=self.index[identity]
        self.size=len(self.items)
        self.table=[[self.index[multiply(a,b)] for b in self.items] for a in self.items]
        self.inverse=[]
        for a in range(self.size):
            options=[b for b in range(self.size) if self.table[a][b]==self.identity and self.table[b][a]==self.identity]
            assert len(options)==1
            self.inverse.append(options[0])

    def mul(self,a,b):return self.table[a][b]

    def power(self,a,n):
        if n<0:return self.power(self.inverse[a],-n)
        out=self.identity
        while n:
            if n&1:out=self.mul(out,a)
            a=self.mul(a,a);n//=2
        return out

    def eval(self,w,args):
        out=self.identity
        for letter in w:
            a=args[abs(letter)-1]
            out=self.mul(out,a if letter>0 else self.inverse[a])
        return out


def affine_s4():
    vectors=list(product(range(2),repeat=2))
    matrices=[]
    for m in product(range(2),repeat=4):
        if (m[0]*m[3]-m[1]*m[2])%2:matrices.append(m)
    def action(m,v):return ((m[0]*v[0]+m[1]*v[1])%2,(m[2]*v[0]+m[3]*v[1])%2)
    def mm(a,b):
        return ((a[0]*b[0]+a[1]*b[2])%2,(a[0]*b[1]+a[1]*b[3])%2,
                (a[2]*b[0]+a[3]*b[2])%2,(a[2]*b[1]+a[3]*b[3])%2)
    def mult(a,b):
        m,u=a;n,v=b
        mv=action(m,v)
        return mm(m,n),tuple((x+y)%2 for x,y in zip(u,mv))
    group=FiniteGroup(list(product(matrices,vectors)),mult,((1,0,0,1),(0,0)))
    nonzero=[(1,0),(0,1),(1,1)]
    parity=[]
    for m,v in group.items:
        p=[nonzero.index(action(m,x)) for x in nonzero]
        parity.append(sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2)
    assert group.size==24 and Counter(parity)=={0:12,1:12}
    assert all(parity[group.mul(a,b)]==(parity[a]+parity[b])%2 for a in range(24) for b in range(24))
    return group,parity


def intersection_dynamic_counts(sets,max_n):
    membership=Counter(sum(1<<j for j,s in enumerate(sets) if value in s) for value in set.union(*sets))
    dp={(1<<len(sets))-1:1}
    out={}
    for n in range(1,max_n+1):
        new=Counter()
        for old,count in dp.items():
            for mask,multiplicity in membership.items():
                overlap=old&mask
                if overlap:new[overlap]+=count*multiplicity
        dp=new
        out[str(n)]=sum(dp.values())
    return out


def controller_checks():
    g,q=affine_s4()
    pair_group=[(x,y) for x,y in product(range(g.size),repeat=2) if q[x]==q[y]]
    assert len(pair_group)==288
    out={}
    for name,w in words().items():
        restricted={h:set() for h in product(range(2),repeat=2)}
        for x,y in product(range(g.size),repeat=2):restricted[q[x],q[y]].add(g.eval(w,(x,y)))
        sets=list(restricted.values())
        expected_pairs=set.union(*(set(product(s,repeat=2)) for s in sets))
        # Direct word evaluation on the finite two-factor fiber product.
        direct=set()
        for x,y in product(pair_group,repeat=2):
            direct.add((g.eval(w,(x[0],y[0])),g.eval(w,(x[1],y[1]))))
        assert direct==expected_pairs
        counts=intersection_dynamic_counts(sets,12)
        assert counts['1']==len(set.union(*sets)) and counts['2']==len(direct)
        out[name]={'parity_fiber_counts':{str(h):len(s) for h,s in restricted.items()},
                   'word_image_on_n_fold_fiber_product':counts,
                   'exact_n2_union_crosscheck':len(direct)}
    # Empty index boundary: the product group is trivial, with one word value.
    # Deterministic nonidentity outputs are not active coordinates.
    deterministic={'C2_identity_quotient':{'S_0':[0],'S_1':[1],'active':False},
                   'empty_index_word_image_size':1}
    return {'model':'AGL(2,2) with sign quotient C2; quotient kernel order12',
            'group_order':g.size,'two_factor_fiber_product_order':len(pair_group),
            'results':out,'boundaries':deterministic}


def wreath_checks():
    previous=FiniteGroup([0],lambda a,b:0,0)
    out=[]
    for depth in range(1,4):
        p=previous
        items=list(product(range(p.size),range(p.size),range(2)))
        def multiply(g,h):
            a,b,flip=g;c,d,other=h
            first,second=((b,a) if other else (a,b))
            return p.mul(first,c),p.mul(second,d),flip^other
        g=FiniteGroup(items,multiply,(p.identity,p.identity,0))
        tau=g.index[(p.identity,p.identity,1)]
        conjugates={g.mul(g.mul(g.inverse[h],tau),h) for h in range(g.size)}
        centralizer=sum(g.mul(h,tau)==g.mul(tau,h) for h in range(g.size))
        assert g.size==2**(2**depth-1)
        assert len(conjugates)==p.size and centralizer==2*p.size
        values={name:len({g.eval(w,(x,y)) for x,y in product(range(g.size),repeat=2)}) for name,w in words().items()}
        out.append({'depth':depth,'order':g.size,'root_flip_class_size':len(conjugates),
                    'root_flip_centralizer_order':centralizer,'word_image_sizes':values})
        previous=g
    assert [v['root_flip_class_size'] for v in out]==[1,2,8]
    assert [v['word_image_sizes']['x_fourth'] for v in out]==[1,1,2]
    assert [v['word_image_sizes']['commutator_squared'] for v in out]==[1,1,2]
    return out


def heisenberg(p):
    def mult(g,h):
        a,b,c=g;x,y,z=h
        return (a+x)%p,(b+y)%p,(c+z+a*y)%p
    g=FiniteGroup(list(product(range(p),repeat=3)),mult,(0,0,0))
    quotient=[(a,b) for a,b,c in g.items]
    kernel=[j for j,(a,b,c) in enumerate(g.items) if a==b==0]
    return g,quotient,kernel


def cyclic_central():
    g=FiniteGroup(list(product(range(8),range(2))),lambda a,b:((a[0]+b[0])%8,(a[1]+b[1])%2),(0,0))
    q=[a%2 for a,b in g.items]
    kernel=[j for j,x in enumerate(q) if x==0]
    return g,q,kernel


def central_checks():
    out=[]
    test_words=words()|{'mixed_positive_negative':(1,1,-2,-2,-2,-2),'identity':()}
    for name,(g,q,kernel) in [('UT3_F2',heisenberg(2)),('UT3_F3',heisenberg(3)),('C8_times_C2_to_C2',cyclic_central())]:
        assert all(g.mul(a,k)==g.mul(k,a) for a in range(g.size) for k in kernel)
        cases={}
        for wname,w in test_words.items():
            r=[sum(1 if x==j else -1 if x==-j else 0 for x in w) for j in [1,2]]
            d=gcd(*r)
            power_set={g.power(k,d) for k in kernel}
            restricted=defaultdict(set)
            bases={}
            for a,b in product(range(g.size),repeat=2):
                h=q[a],q[b]
                restricted[h].add(g.eval(w,(a,b)))
                bases.setdefault(h,(a,b))
            for h,values in restricted.items():
                z=g.eval(w,bases[h])
                assert values=={g.mul(z,s) for s in power_set}
                assert len(values)==len(power_set)
            cases[wname]={'exponent_sums':r,'gcd':d,'constant_lift_image_size':len(power_set),
                           'quotient_input_tuples':len(restricted)}
        out.append({'model':name,'order':g.size,'central_kernel_order':len(kernel),'cases':cases})
    g,q,kernel=heisenberg(3)
    x=g.index[(1,0,0)];y=g.index[(0,1,0)]
    c=(-1,-2,1,2)
    assert g.eval(c,(x,y))!=g.eval(c,(x,x))
    # Quotient is abelian, so both quotient commutators are the identity.
    # Nonsplit extension control C4->C2: every element with order dividing2
    # projects to0. Set-theoretic local sections still exist.
    assert all(a%2==0 for a in range(4) if 2*a%4==0)
    return {'central_lift_controls':out,'same_quotient_word_value_different_cocycle':True,
            'C4_to_C2_no_group_homomorphic_section':True,
            'local_sections_do_not_require_splitting':True}


def isolated_square_controls():
    out=[]
    for p in [3,5,7]:
        for exponent in range(4):
            modulus=p**exponent
            squares={((1+(-1)**k)*a%modulus,2*k%4) for a,k in product(range(modulus),range(4))}
            expected={(a,0) for a in range(modulus)}|{(0,2)}
            assert squares==expected and len(squares)==modulus+1
            out.append({'p':p,'exponent':exponent,'image_size':len(squares),
                        'singleton_nonidentity_C4_coset':True})
    w=words()['commutator_with_its_x_conjugate']
    assert free_reduce(w)
    return {'finite_semidirect_square_cases':out,'candidate_word_freely_reduced':free_reduce(w),
            'scope':'Isolated image point does not imply finite image; these finite controls are not counterexamples.'}


def compare_author(controller,wreath):
    source=Path(__file__).resolve().parent.parent/'counterexample/finite_model_results.json'
    a=json.loads(source.read_text())
    for name,v in controller['results'].items():
        for key,value in v.items():assert a['finite_common_controller_S4_to_C2'][name][key]==value,(name,key)
    assert a['binary_iterated_wreath']['exact_small_groups']==wreath
    return {'all_independently_calculated_controller_and_small_wreath_fields_match':True}


def main():
    controller=controller_checks();wreath=wreath_checks()
    out={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Restricted-model audit only; no full21.122 result or novelty claim',
         'independent_implementation':'AGL(2,2), recursive wreath tables, Heisenberg central extensions',
         'finite_controller':controller,'wreath':wreath,'central_extensions':central_checks(),
         'isolated_square_control':isolated_square_controls(),'author_comparison':compare_author(controller,wreath)}
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'verdict':'PASS','controller_words':4,'wreath_depths':3,
                      'central_extension_models':3,'isolated_square_cases':12,'author_fields_match':True}))


if __name__=='__main__':main()
