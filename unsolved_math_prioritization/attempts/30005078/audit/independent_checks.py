"""Independent audit: product-cover Cech, column reduction, Koszul controls.

No author computational routine is reused in the reference calculations. The
frozen author module is imported only as the system under test. Standard library.
Usage: python independent_checks.py /path/to/frozen_author_directory
"""
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import hashlib, importlib.util, json, math, random, sys


def rank_columns(columns, characteristic):
    pivots = {}
    for col in columns:
        v = [x % characteristic if characteristic else Fraction(x) for x in col]
        for k in sorted(pivots):
            if v[k]:
                t = v[k]
                v = [(a - t*b) % characteristic if characteristic else a-t*b
                     for a,b in zip(v,pivots[k])]
        k = next((i for i,x in enumerate(v) if x), None)
        if k is not None:
            t = pow(v[k], -1, characteristic) if characteristic else 1/v[k]
            pivots[k] = [(x*t) % characteristic if characteristic else x*t for x in v]
    return len(pivots)


def blocks(sizes):
    out=[]; start=0
    for n in sizes:
        out.append(tuple(range(start,start+n))); start+=n
    return out


def alive(degree, inverted, gens):
    free = set(range(len(degree))) - set(inverted)
    return all(degree[j]>=0 for j in free) and all(
        any(degree[j]<g[j] for j in free) for g in gens)


def product_cech(sizes, gens, degree, p=0):
    """Iterated block-cover total complex, instead of Cech on all B generators."""
    bs=blocks(sizes)
    choices=[sum(([s for s in combinations(b,k)] for k in range(1,len(b)+1)), []) for b in bs]
    dim=sum(sizes)-len(sizes)+1
    terms=[[] for _ in range(dim+1)]
    if alive(degree,(),gens): terms[0]=[None]
    for rect in product(*choices):
        if alive(degree,tuple(j for b in rect for j in b),gens):
            terms[sum(len(b)-1 for b in rect)+1].append(rect)
    ranks=[0]
    for i in range(dim):
        index={x:k for k,x in enumerate(terms[i+1])}
        cols=[]
        for rect in terms[i]:
            col=[0]*len(index)
            if i==0:
                col=[1]*len(index)
            else:
                for bno,b in enumerate(bs):
                    for j in b:
                        if j not in rect[bno]:
                            nxt=list(rect); nxt[bno]=tuple(sorted(rect[bno]+(j,))); nxt=tuple(nxt)
                            if nxt in index:
                                sign=(-1)**(sum(len(t)-1 for t in rect[:bno])+nxt[bno].index(j))
                                col[index[nxt]]=sign
            cols.append(col)
        ranks.append(rank_columns(cols,p))
    ranks.append(0)
    ans=tuple(len(t)-ranks[i]-ranks[i+1] for i,t in enumerate(terms))
    assert min(ans)>=0
    return ans+(0,)*(math.prod(sizes)+1-len(ans))


def cells(sizes,gens):
    cap=tuple(max((g[j] for g in gens),default=0) for j in range(sum(sizes)))
    for typ in product(*(range(-1,c+1) for c in cap)):
        upper=tuple(None if x==c else x for x,c in zip(typ,cap))
        yield typ,upper


def shifts(total,r):
    return (x for x in product(range(total+1),repeat=r) if sum(x)==total)


def bad_profiles(sizes,gens,p):
    out=set()
    for a,up in cells(sizes,gens):
        cu=tuple(None if any(up[j] is None for j in b) else sum(up[j] for j in b)
                 for b in blocks(sizes))
        for i,h in enumerate(product_cech(sizes,gens,a,p)):
            if h:out.add((i,cu))
    return out


def member(profiles,d,kind='module'):
    r=len(d)
    for i,up in profiles:
        if kind=='sheaf' and i<2:continue
        starts=(tuple(d[j]+(j==k) for j in range(r)) for k in range(r)) if i==0 else (
            tuple(d[j]-s[j] for j in range(r)) for s in shifts(i-1,r))
        if any(all(t is None or v<=t for v,t in zip(start,up)) for start in starts):return False
    return True


def koszul_reg(gens,n,p=0):
    if (0,)*n in gens:return None
    cap=[max((g[j] for g in gens),default=0) for j in range(n)]
    answer=None
    for a in product(*(range(c+1) for c in cap)):
        terms=[]
        for k in range(n+1):
            terms.append([s for s in combinations(range(n),k)
                if alive(tuple(a[j]-(j in s) for j in range(n)),(),gens)])
        ranks=[0]
        for k in range(1,n+1):
            lookup={s:i for i,s in enumerate(terms[k-1])}
            columns=[]
            for s in terms[k]:
                v=[0]*len(lookup)
                for h,j in enumerate(s):
                    t=tuple(x for x in s if x!=j)
                    if t in lookup:v[lookup[t]]=(-1)**h
                columns.append(v)
            ranks.append(rank_columns(columns,p))
        ranks.append(0)
        for k,t in enumerate(terms):
            if len(t)>ranks[k]+ranks[k+1]:answer=max(answer if answer is not None else -999,sum(a)-k)
    return answer


def check():
    root=Path(sys.argv[1]).resolve()
    spec=importlib.util.spec_from_file_location('author_under_test',root/'monomial_regularity.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    MQ=module.MonomialQuotient
    original=json.loads((root/'RESULTS.json').read_text())
    counts={'fixed_case_fields':0,'fixed_region_degrees':0,'fine_degree_product_cover_comparisons':0,
            'singly_graded_koszul_comparisons':0,'cell_invariance_comparisons':0,
            'diagonal_controls':0,'extra_module_sheaf_memberships':0,'frontier_box_and_minimality':0}
    for p in (0,2,3,101):
        for ex in original['examples']:
            gens=ex['generators']; sizes=ex['block_sizes'];m=MQ(sizes,gens,p)
            profiles=bad_profiles(sizes,gens,p)
            result=m.regularity()
            for a,_ in cells(sizes,gens):
                assert product_cech(sizes,gens,a,p)==m.fine_cohomology(a)
                counts['fine_degree_product_cover_comparisons']+=1
            for d in product(range(-3,7),repeat=2):
                assert member(profiles,d)==module.satisfies(result['clauses'],d)
                counts['fixed_region_degrees']+=1
            mins=[]
            cap=[max((g[j] for g in gens),default=0) for j in range(sum(sizes))]
            box=[(-len(b),math.prod(sizes)+sum(cap[j]-1 for j in b)) for b in blocks(sizes)]
            for d in product(*(range(lo,hi+1) for lo,hi in box)):
                if member(profiles,d) and all(not member(profiles,tuple(x-(j==k) for j,x in enumerate(d))) for k in range(len(sizes))):mins.append(d)
            assert set(mins)==set(result['minimal_elements'])
            counts['frontier_box_and_minimality']+=1
            counts['fixed_case_fields']+=1
    rng=random.Random(30005078)
    monomials=[a for a in product(range(4),repeat=2) if sum(a)]
    for _ in range(80):
        gens=rng.sample(monomials,rng.randint(0,5))
        expected=koszul_reg(gens,2)
        assert MQ((2,),gens).regularity()['minimal_elements']==((expected,),)
        counts['singly_graded_koszul_comparisons']+=1
    for _ in range(12):
        gens=[tuple(rng.randint(0,2) for _ in range(4)) for _ in range(3)]
        cc=list(cells((2,2),gens))
        for a,upper in rng.sample(cc,min(12,len(cc))):
            b=tuple(x-11 if x<0 else x+13 if u is None else x for x,u in zip(a,upper))
            h=product_cech((2,2),gens,a)
            assert h==product_cech((2,2),gens,b)==MQ((2,2),gens).fine_cohomology(b)
            counts['cell_invariance_comparisons']+=1
    # Derive P1 H1 through its two-chart Laurent basis: surviving exponents
    # have both coordinates negative and sum equal to the line-bundle degree.
    def p1_h1(deg):return sum(1 for x in range(deg+1,0) if deg-x<0)
    for a,b in product(range(-20,21),repeat=2):
        sheaf_ok=all(p1_h1(a+b-1+increment)==0 for increment in (0,1,2,43))
        assert sheaf_ok==(a+b>=0)
        if a<0 or b<0:
            e=(a,max(b,-a)) if a<0 else (max(a,-b),b)
            assert min(e)<0 and sum(e)>=0 and sum(e)+1>0
            module_ok=False
        else:
            # Restriction x^i y^j -> s^(i+j)t^(a+b-i-j) spans every exponent.
            assert {i+j for i in range(a+1) for j in range(b+1)}==set(range(a+b+1))
            module_ok=sheaf_ok
        assert module_ok==(a>=0 and b>=0)
        counts['diagonal_controls']+=1
    edgecases=[((2,),[]),((3,),[]),((2,3),[]),((2,2),[(0,0,0,0)]),
               ((2,2),[(1,0,0,0),(0,1,0,0)]),((2,2),[(1,0,0,0),(0,0,1,0)]),
               ((2,2),[(1,0,0,0),(0,0,1,0),(2,0,0,0),(1,0,0,0)]),
               ((2,2),[(2,0,0,0),(0,2,0,0),(0,0,2,0),(0,0,0,2)]),
               ((2,2),[(1,0,0,0)]),((2,2),[(0,0,1,0)]),((2,3),[(1,0,1,0,0)]),((2,2,2),[(1,0,0,0,0,0),(0,0,1,0,0,0),(0,0,0,0,1,0)])]
    edge_results=[]
    for sizes,gens in edgecases:
        profiles=bad_profiles(sizes,gens,0)
        for kind in ('module','sheaf'):
            got=MQ(sizes,gens).regularity(kind=kind)
            for d in product(range(-4,6),repeat=len(sizes)):
                assert member(profiles,d,kind)==module.satisfies(got['clauses'],d)
                assert member(profiles,d,kind)==any(all(t is None or v>=t for t,v in zip(o,d)) for o in got['generalized_orthants'])
                counts['extra_module_sheaf_memberships']+=1
            edge_results.append({'sizes':sizes,'generators':gens,'kind':kind,'minimal_elements':got['minimal_elements'],'orthants':got['generalized_orthants']})
    # A six-vertex triangulation of RP2 gives actual characteristic-sensitive
    # local cohomology, beyond a standalone rank([[1,1],[1,-1]]) unit test.
    facets=[(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),
            (1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
    nonfaces=[s for s in combinations(range(6),3) if s not in facets]
    gens=[tuple(int(j in s) for j in range(6)) for s in nonfaces]
    torsion=[]
    for p in (0,2,3,101):
        h=product_cech((6,),gens,(0,)*6,p)
        got=MQ((6,),gens,p)
        assert h==got.fine_cohomology((0,)*6)
        expected=(0,0,1,1,0,0,0) if p==2 else (0,)*7
        assert h==expected,(p,h)
        reg=got.regularity()['minimal_elements']
        expected_reg=koszul_reg(gens,6,p)
        assert reg==((expected_reg,),)
        assert expected_reg==(3 if p==2 else 2),(p,expected_reg)
        torsion.append({'characteristic':p,'degree_zero_local_cohomology':h,'regularity':reg})
    from frontier_box import regularity_with_box
    wrapper_cases=0
    for sizes,gens in edgecases:
        for kind in ('module','sheaf'):
            obj=MQ(sizes,gens);out=regularity_with_box(obj,kind=kind)
            box=out.pop('minimal_element_box')
            assert out==obj.regularity(kind=kind)
            assert all(all(lo<=v<=hi for v,(lo,hi) in zip(d,box)) for d in out['minimal_elements'])
            wrapper_cases+=1
    counts['frontier_box_wrapper_cases']=wrapper_cases
    validation=[]
    for sizes,gens,p in [((),[],0),((1,),[],0),((2,),[],1),((2,),[],4),((2,),[],-3),((2,),[(-1,0)],0),((2,),[(1,)],0)]:
        try:MQ(sizes,gens,p)
        except ValueError:validation.append('rejected')
        else:raise AssertionError((sizes,gens,p))
    return {'status':'PASS','problem_id':30005078,'counts':counts,'edge_cases':edge_results,
            'characteristic_torsion_controls':torsion,'invalid_inputs_rejected':len(validation),
            'independent_method':'Iterated block-cover total Cech complex, independent column-space rank, direct bad-cell tests, exhaustive proved-box minima, independent Koszul homology.',
            'general_problem_solved':False}

if __name__=='__main__':
    out=check();Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='edge_cases'},indent=2))
