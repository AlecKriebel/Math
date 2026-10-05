#!/usr/bin/env python3
"""Independent exact audit. Standard library only; no author code is imported.
Finite group orders are measured as cycle orders of faithful permutation actions.
Run without arguments to reproduce AUDIT_CHECK_RESULTS.json. Optional
--author-dir verifies the original frozen CHECK_RESULTS.json and all 183 maps.
"""
import argparse, hashlib, itertools, json, math
from collections import Counter, deque
from pathlib import Path


def factors(n):
    out=set()
    for d in range(2,math.isqrt(n)+1):
        if n%d==0:
            out.add(d)
            while n%d==0: n//=d
        if d*d>n: break
    if n>1: out.add(n)
    return out


def sieve(n):
    flag=bytearray(b'\1')*(n+1); flag[0:2]=b'\0\0'
    for p in range(2,math.isqrt(n)+1):
        if flag[p]: flag[p*p:n+1:p]=b'\0'*len(range(p*p,n+1,p))
    return [p for p in range(n+1) if flag[p]]


def order(p):
    seen=bytearray(len(p)); result=1
    for a in range(len(p)):
        if seen[a]: continue
        b=a; k=0
        while not seen[b]: seen[b]=1; k+=1; b=p[b]
        result=math.lcm(result,k)
    return result


def graph(vertices,orders):
    return {'vertices':sorted(vertices),'edges':[list(e) for e in itertools.combinations(sorted(vertices),2) if any(t%(e[0]*e[1])==0 for t in orders)]}


def graph_pgl(q):
    verts=factors(q*(q-1)*(q+1))
    return {'vertices':sorted(verts),'edges':[[a,b] for a,b in itertools.combinations(sorted(verts),2) if (q-1)%(a*b)==0 or (q+1)%(a*b)==0]}


def counts(c): return {str(a):c[a] for a in sorted(c)}


def compose(a,b): return tuple(a[i] for i in b)


def generated(gens,degree,expected):
    one=tuple(range(degree)); seen={one}; todo=deque([one])
    while todo:
        a=todo.popleft()
        for b in gens:
            c=compose(a,b)
            if c not in seen:
                seen.add(c); todo.append(c)
                assert len(seen)<=expected
    assert len(seen)==expected
    return sorted(seen)


def encode_module(n,mode='deleted'):
    dim=n if mode=='full' else n-1-(mode=='deleted' and n%2==0)
    mask=(1<<dim)-1
    def decode(v): return v if mode=='full' else v|((v.bit_count()%2)<<dim)
    def encode(v):
        if mode=='deleted' and n%2==0 and (v>>(n-1))&1: v^=(1<<n)-1
        return v&mask
    return dim,decode,encode


def module_action(g,mode='deleted'):
    dim,decode,encode=encode_module(len(g),mode)
    def move(v): return sum(((v>>i)&1)<<g[i] for i in range(len(g)))
    columns=[encode(move(decode(1<<i))) for i in range(dim)]
    a=[0]*(1<<dim)
    for v in range(1,1<<dim):
        low=v&-v; a[v]=a[v^low]^columns[low.bit_length()-1]
    return tuple(a)


def symmetric(n,mode='deleted'):
    base=Counter(); affine=Counter(); actions=set()
    for g in itertools.permutations(range(n)):
        rho=module_action(g,mode); actions.add(rho)
        assert order(rho)==order(g)
        base[order(g)]+=1
        for v in range(len(rho)):
            affine[order(tuple(v^a for a in rho))]+=1
    assert len(actions)==math.factorial(n)  # Faithful: cycle order is group order.
    d=n if mode=='full' else n-1-(mode=='deleted' and n%2==0)
    result={'n':n,'mode':mode,'module_order':2**d,'group_order':sum(affine.values()),'base_element_order_counts':counts(base),'affine_element_order_counts':counts(affine),'graph':graph(sieve(n),affine)}
    if mode=='deleted': assert result['graph']==graph(sieve(n),base)
    return result


def rank2(columns):
    pivots={}
    for v in columns:
        while v:
            i=v.bit_length()-1
            if i in pivots: v^=pivots[i]
            else: pivots[i]=v; break
    return len(pivots)


def fixed_dimensions():
    tests=0; absent=0; summary=[]
    for n in range(5,101):
        dim,decode,encode=encode_module(n)
        local=0
        for r in sieve(n):
            if r==2:continue
            for k in range(1,n//r+1):
                g=list(range(n))
                for offset in range(0,k*r,r):
                    for i in range(r):g[offset+i]=offset+(i+1)%r
                cols=[]
                for j in range(dim):
                    v=decode(1<<j)
                    image=sum(((v>>i)&1)<<g[i] for i in range(n))
                    cols.append(encode(image)^(1<<j))
                measured=dim-rank2(cols)
                expected=n-k*(r-1)-1-(n%2==0)
                assert measured==expected
                if 2+r>n: assert measured==0; absent+=1
                tests+=1;local+=1
        summary.append({'n':n,'conjugacy_types_checked':local})
    return {'linear_rank_tests':tests,'nonadjacent_prime_types':absent,'per_n':summary}


class Field:
    """F_p[X]/(monic modulus), implemented by base-p coefficient lists."""
    def __init__(self,p,mod):
        self.p=p;self.mod=mod;self.f=len(mod)-1;self.q=p**self.f
        self.coeffs=[[(a//p**i)%p for i in range(self.f)] for a in range(self.q)]
        def pack(a):return sum((t%p)*p**i for i,t in enumerate(a))
        self.add=[[pack([(x+y)%p for x,y in zip(self.coeffs[a],self.coeffs[b])]) for b in range(self.q)] for a in range(self.q)]
        self.mul=[]
        for a in range(self.q):
            row=[]
            for b in range(self.q):
                c=[0]*(2*self.f-1)
                for i,x in enumerate(self.coeffs[a]):
                    for j,y in enumerate(self.coeffs[b]):c[i+j]=(c[i+j]+x*y)%p
                for i in range(2*self.f-2,self.f-1,-1):
                    lead=c[i]
                    for j in range(self.f+1):c[i-self.f+j]=(c[i-self.f+j]-lead*mod[j])%p
                row.append(pack(c[:self.f]))
            self.mul.append(row)
        self.neg=[pack([-x for x in c]) for c in self.coeffs]
        self.inv={a:next(b for b in range(1,self.q) if self.mul[a][b]==1) for a in range(1,self.q)}
        # Explicit inverses verify these small quotient rings are fields.
    def power(self,a,n):
        out=1
        for _ in range(n):out=self.mul[out][a]
        return out


def semilinear(f,mod):
    F=Field(2,mod);q=F.q;add=F.add;mul=F.mul
    vec=[(x,y) for x in range(q) for y in range(q)]
    def perm(fun):return tuple(fun(x,y)[0]*q+fun(x,y)[1] for x,y in vec)
    gens=[]
    for a in range(1,q):
        gens.append(perm(lambda x,y,a=a:(add[x][mul[a][y]],y)))
        gens.append(perm(lambda x,y,a=a:(x,add[y][mul[a][x]])))
    gens.append(perm(lambda x,y:(mul[x][x],mul[y][y])))
    base=generated(gens,q*q,f*q*(q*q-1)); bc=Counter();ac=Counter();checks=0
    for g in base:
        o=order(g);bc[o]+=1
        for v in range(q*q):
            h,k=vec[v]
            trans=tuple(add[h][vec[i][0]]*q+add[k][vec[i][1]] for i in g)
            ac[order(trans)]+=1
            if o>2 and len(factors(o))==1 and o in factors(o) and v and g[v]==v:
                def tv(x,y):
                    b=add[mul[x][k]][mul[y][h]]
                    return add[x][mul[b][h]],add[y][mul[b][k]]
                t=perm(tv)
                assert order(t)==2 and t in base
                assert compose(t,g)==compose(g,t)
                assert order(compose(t,g))==2*o
                checks+=1
    assert graph(factors(len(base)),bc)==graph(factors(len(base)),ac)
    return {'f':f,'q':q,'base_order':len(base),'affine_order':sum(ac.values()),'base_element_order_counts':counts(bc),'affine_element_order_counts':counts(ac),'fixed_vector_transvection_checks':checks,'graph':graph(factors(len(base)),bc)}


def symplectic4():
    def B(a,b):return ((a&3)&((b>>2)&3)).bit_count()%2 ^ (((a>>2)&3)&(b&3)).bit_count()%2
    trans=[tuple(w^(v if B(w,v) else 0) for w in range(16)) for v in range(1,16)]
    base=generated(trans,16,720);bc=Counter();ac=Counter();checks=0
    for g in base:
        o=order(g);bc[o]+=1
        for v in range(16):
            ac[order(tuple(a^v for a in g))]+=1
            if o in (3,5) and v and g[v]==v:
                t=trans[v-1];assert compose(t,g)==compose(g,t)
                assert order(compose(t,g))==2*o;checks+=1
    assert graph({2,3,5},bc)==graph({2,3,5},ac)
    return {'group':'Sp4(2)','base_order':720,'affine_order':sum(ac.values()),'base_element_order_counts':counts(bc),'affine_element_order_counts':counts(ac),'fixed_vector_transvection_checks':checks,'graph':graph({2,3,5},bc)}


def affine_characteristic3_control():
    # The augmentation module of S3 over F3: (a,b,-a-b).
    vectors=[(a,b) for a in range(3) for b in range(3)]
    index={v:i for i,v in enumerate(vectors)}
    bc=Counter();ac=Counter();fixed_order2=0
    for g in itertools.permutations(range(3)):
        images=[]
        for a,b in vectors:
            w=(a,b,(-a-b)%3);z=[0,0,0]
            for i in range(3):z[g[i]]=w[i]
            images.append(index[(z[0],z[1])])
        rho=tuple(images);assert order(rho)==order(g)
        bc[order(g)]+=1
        if order(g)==2:fixed_order2+=sum(i>0 and rho[i]==i for i in range(9))
        for a,b in vectors:
            t=tuple(index[((vectors[i][0]+a)%3,(vectors[i][1]+b)%3)] for i in rho)
            ac[order(t)]+=1
    assert graph({2,3},bc)['edges']==[]
    assert graph({2,3},ac)['edges']==[[2,3]] and fixed_order2==6
    return {'group':'F3^2 semidirect S3 on augmentation module','base_order':6,'affine_order':54,'base_element_order_counts':counts(bc),'affine_element_order_counts':counts(ac),'order2_nonzero_fixed_pairs':fixed_order2,'new_edge':[2,3]}


def projective(p,mod):
    F=Field(p,mod);q=F.q;inf=q
    primitive=next(a for a in range(1,q) if len({F.power(a,i) for i in range(q-1)})==q-1)
    gens=[tuple(F.add[x][p**i] for x in range(q))+(inf,) for i in range(F.f)]
    gens.append(tuple(F.mul[primitive][x] for x in range(q))+(inf,))
    gens.append(tuple(inf if x==0 else F.inv[x] for x in range(q))+(0,))
    base=generated(gens,q+1,q*(q*q-1));c=Counter(map(order,base))
    expected={d for n in (q-1,q+1) for d in range(1,n+1) if n%d==0}|{p}
    assert set(c)==expected
    assert graph(factors(len(base)),c)==graph_pgl(q)
    return {'q':q,'characteristic':p,'modulus_low_to_high':mod,'order':len(base),'element_order_counts':counts(c),'graph':graph_pgl(q)}


def primepowers(bound):
    out={}
    for p in sieve(bound):
        if p==2:continue
        q=p;f=1
        while q<=bound:
            if q>=5:out[q]=[p,f]
            q*=p;f+=1
    return out


def valid_map(q,r,m):
    a,b=graph_pgl(q),graph_pgl(r)
    if q==r or set(m)!=set(a['vertices']) or len(set(m.values()))!=len(m) or set(m.values())!=set(b['vertices']):return False
    edges={tuple(e) for e in b['edges']}
    return all(((q-1)%(x*y)==0 or (q+1)%(x*y)==0)==(tuple(sorted((m[x],m[y]))) in edges) for x,y in itertools.combinations(a['vertices'],2))


def signature(q):return sorted([len(factors(q-1)-{2}),len(factors(q+1)-{2})])


def collision_map(q,r):
    u=[sorted(factors(q-1)-{2}),sorted(factors(q+1)-{2})]
    v=[sorted(factors(r-1)-{2}),sorted(factors(r+1)-{2})]
    if len(u[0])!=len(v[0]):v.reverse()
    result={next(iter(factors(q))):next(iter(factors(r))),2:2}
    for a,b in zip(u,v):result.update(zip(a,b))
    return result


def census():
    powers=primepowers(10000);targets=sorted(q for q in powers if q<=1000)
    assert len(targets)==183
    cert=[]
    for q in targets:
        # Largest available witness intentionally differs from author search.
        r=next(r for r in sorted(powers,reverse=True) if r!=q and signature(q)==signature(r))
        m=collision_map(q,r);assert valid_map(q,r,m)
        assert q*(q*q-1)!=r*(r*r-1)
        cert.append({'q':q,'q_prime_power':powers[q],'witness_q':r,'witness_prime_power':powers[r],'q_group_order':q*(q*q-1),'witness_group_order':r*(r*r-1),'vertex_map':{str(a):b for a,b in sorted(m.items())}})
    wrong=collision_map(169,181);wrong[3],wrong[5]=wrong[5],wrong[3]
    assert not valid_map(169,181,wrong)
    wrong2=collision_map(169,181);wrong2[3]=wrong2[5]
    assert not valid_map(169,181,wrong2)
    return {'target_count':len(targets),'excluded':len(cert),'unmatched':[],'max_target':1000,'max_witness_search':10000,'max_witness_used':max(c['witness_q'] for c in cert),'certificates':cert,'cross_branch_and_nonbijective_mutations_rejected':True}


def verify_author(author,result):
    raw=(author/'CHECK_RESULTS.json').read_bytes();a=json.loads(raw)
    for x,y in zip(a['symmetric_affine'],result['symmetric_affine']):assert x==y
    for x,y in zip(a['semilinear_affine'],result['semilinear_affine']):
        x={k:v for k,v in x.items() if k!='irreducible_polynomial_binary'};assert x==y
    for x,y in zip(a['pgl_matrix_enumerations'],result['pgl_projective_action']):
        assert x['p']==y['q']
        assert all(x[k]==y[k] for k in ('order','element_order_counts','graph'))
    targets=set(primepowers(1000));cert=a['pgl_census']['certificates']
    assert len(cert)==183 and {x['q'] for x in cert}==targets
    largest=0
    for c in cert:
        q,r=c['q'],c['witness_q'];m={int(x):y for x,y in c['vertex_map'].items()}
        assert r in primepowers(10000) and valid_map(q,r,m)
        assert q*(q*q-1)!=r*(r*r-1);largest=max(largest,r)
    for c in a['pgl_named_collisions']:
        assert valid_map(c['q'],c['r'],{int(x):y for x,y in c['vertex_map'].items()})
        assert c['q_graph']==graph_pgl(c['q']) and c['r_graph']==graph_pgl(c['r'])
    return {'status':'PASS','author_results_sha256':hashlib.sha256(raw).hexdigest(),'all_183_maps_checked':True,'edge_and_nonedge_checks':True,'distinct_group_orders_checked':True,'maximum_author_witness':largest,'histograms_match':True,'named_collisions_checked':3}


def run():
    result={'status':'PASS','original_problem_solved':False,'method':'Independently written; faithful permutation cycle orders, generated group closures, and GF(2) linear ranks. No author code imported.'}
    result['symmetric_affine']=[symmetric(n) for n in (5,6,7)]
    result['fixed_dimensions']=fixed_dimensions()
    result['semilinear_affine']=[semilinear(2,[1,1,1]),semilinear(3,[1,1,0,1])]
    result['higher_rank_symplectic']=symplectic4()
    result['affine_characteristic3_control']=affine_characteristic3_control()
    result['pgl_projective_action']=[projective(p,[0,1]) for p in (5,7,11,13)]
    result['pgl_extension_field_action']=[projective(3,[1,0,1]),projective(5,[2,0,1]),projective(3,[1,2,0,1])]
    result['pgl_independent_census']=census()
    full=symmetric(5,'full');augmentation=symmetric(6,'augmentation')
    assert [2,5] in full['graph']['edges'] and [2,5] in augmentation['graph']['edges']
    result['negative_controls']={'S5_full_module':full,'S6_unquotiented_augmentation':augmentation}
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--author-dir',type=Path);args=p.parse_args()
    result=run();path=Path(__file__).with_name('AUDIT_CHECK_RESULTS.json')
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:assert json.loads(path.read_text())==result
    summary={'status':'PASS','original_problem_solved':False,'permutation_affine_groups_checked':7,'PGL_projective_groups_checked':7,'independent_collisions':183,'linear_rank_checks':result['fixed_dimensions']['linear_rank_tests']}
    if args.author_dir:summary['author_comparison']=verify_author(args.author_dir,result)
    print(json.dumps(summary,indent=2))
