#!/usr/bin/env python3
"""Independent finite controls and frozen-payload audit for KOU-21.39.

Standard-library only. This is not a proof assistant or an infinite-group
existence test. It never modifies the supplied author directory. Source PDFs
and full corpora are optional read-only inputs and never copied to the output.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, permutations, product
import hashlib
import json
from math import lcm
from pathlib import Path
import subprocess
import sys
import tempfile

C = Counter()
PIN = 'e618e640ee11d95fe411e007e34a3c851f31420e7e0ce33e37db6c4a4f5c0429'

def ck(ok, category):
    if not ok:
        raise AssertionError(category)
    C[category] += 1


def digest(b):
    return hashlib.sha256(b).hexdigest()


def verify_inventory(root):
    b = (root / 'AUTHOR_MANIFEST.json').read_bytes()
    ck(len(b) == 1725 and digest(b) == PIN, 'frozen_manifest_pin')
    m = json.loads(b)
    names = [x['path'] for x in m['files']]
    ck(len(names) == len(set(names)) == 9, 'manifest_unique_nine_files')
    for x in m['files']:
        p = Path(x['path'])
        ck(not p.is_absolute() and '..' not in p.parts, 'manifest_safe_path')
        f = root / p
        ck(f.is_file() and not f.is_symlink(), 'manifest_regular_file')
        b = f.read_bytes()
        ck(len(b) == x['bytes'] and digest(b) == x['sha256'], 'manifest_entry_exact_match')
    ck({str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} ==
       set(names) | {'AUTHOR_MANIFEST.json'}, 'manifest_complete_inventory')
    return m


def replay(root):
    run = subprocess.run([sys.executable, '-B', str(root / 'verify_math.py')],
                         check=True, capture_output=True)
    old = (root / 'CHECK_RESULTS.json').read_bytes()
    ck(run.stdout == old, 'author_byte_exact_replay')
    r = json.loads(run.stdout)
    ck(r['total_assertions'] == sum(r['assertion_counts'].values()) == 116329,
       'author_assertion_sum')
    a = r['assertion_counts']
    # Independently derive the dominant iteration counts, rather than merely
    # trusting the reported total or the author's counter implementation.
    ck(a['extraspecial_commutator_formula'] == 27**2 + 125**2 + 243**2,
       'author_pair_count')
    ck(a['extraspecial_associativity_exhaustive_E3'] == 27**3,
       'author_triple_count')
    ck(a['extraspecial_generators_homomorphisms_E3'] == (8 + 2 + 2)*27**2,
       'author_automorphism_count')
    ck(a['mclain_double_commutator_extraction'] ==
       sum((n*(n-1)//2)*(p-1)*p**(n*(n-1)//2-1)
           for p,n in [(2,3),(3,3),(5,3),(2,4),(3,4)]), 'author_extraction_count')
    # Tamper tests run on disposable copies, never on frozen originals.
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='k2139-manifest-') as td:
        dst = Path(td)
        for f in root.iterdir():
            if f.is_file():
                (dst/f.name).write_bytes(f.read_bytes())
        target = dst/'RESULT.md'
        original = target.read_bytes()
        target.write_bytes(original+b'\n')
        q = subprocess.run([sys.executable,'-B',str(dst/'verify_manifest.py')],
                           capture_output=True)
        ck(q.returncode != 0, 'negative_manifest_detects_content_tamper')
        outcomes.append('content_tamper_rejected')
        target.write_bytes(original)
        extra = dst/'unexpected.bin'; extra.write_bytes(b'X')
        q = subprocess.run([sys.executable,'-B',str(dst/'verify_manifest.py')],
                           capture_output=True)
        ck(q.returncode != 0, 'negative_manifest_detects_extra_file')
        outcomes.append('extra_file_rejected')
    return {'assertions':116329,'byte_exact':True,'manifest_negative_controls':outcomes}


def a5():
    elems = list(permutations(range(5)))
    even = [x for x in elems if sum(x[i]>x[j] for i,j in combinations(range(5),2))%2==0]
    idx = {x:i for i,x in enumerate(even)}
    e = idx[tuple(range(5))]
    table = [[idx[tuple(x[y[k]] for k in range(5))] for y in even] for x in even]
    inverse = [next(j for j in range(60) if table[i][j]==e) for i in range(60)]
    classes=[]; unseen=set(range(60))
    while unseen:
        x=min(unseen)
        cl={table[table[h][x]][inverse[h]] for h in range(60)}
        classes.append(cl); unseen-=cl
    ck(sorted(map(len,classes)) == [1,12,12,15,20], 'independent_A5_inner_classes')
    nonid=[cl for cl in classes if e not in cl]
    normal=[]
    for flags in product([False,True],repeat=len(nonid)):
        s={e}.union(*(cl for cl,f in zip(nonid,flags) if f))
        if 60%len(s)==0 and all(table[i][j] in s for i in s for j in s):
            normal.append(len(s))
    ck(sorted(normal)==[1,60], 'independent_A5_normal_subgroup_class_unions')
    def order(i):
        v=e
        for t in range(1,61):
            v=table[v][i]
            if v==e:return t
        raise AssertionError('not periodic')
    orders=[order(i) for i in range(60)]
    ck(Counter(orders)=={1:1,2:15,3:20,5:24},'independent_A5_orders')
    for x in even:
        orb=set()
        for h in elems:
            ih=tuple(h.index(k) for k in range(5))
            orb.add(tuple(h[x[ih[k]]] for k in range(5)))
        ck(orb=={y for y in even if orders[idx[y]]==orders[idx[x]]},
           'independent_A5_S5_order_transitivity')
    t=orders.index(2)
    cent=sum(table[t][x]==table[x][t] for x in range(60))
    ck(cent==4,'independent_A5_involution_centralizer')
    ck(60//cent != (60//cent)**2,'negative_equal_order_atomic_orbits')
    spectrum=sorted({lcm(1,*(q for q,f in zip([2,3,5],flags) if f))
                     for flags in product([0,1],repeat=3)})
    ck(spectrum==[1,2,3,5,6,10,15,30], 'independent_boolean_eight_order_lower_bound')
    return {'order':60,'inner_class_sizes':sorted(map(len,classes)),
            'normal_subgroup_orders':normal,'boolean_orders':spectrum,'involution_centralizer':cent}


def pointed_partitions():
    # Prefix substitutions give honest clopen homeomorphisms, even when
    # differently sized finite prefix partitions require further refinements.
    def valid(d):
        keys=list(d)
        return (sum(Fraction(1,2**len(k)) for k in keys)==1 and
                all(not (a.startswith(b) or b.startswith(a)) for a,b in combinations(keys,2)))
    def split(d,key):
        v=d.pop(key); d[key+'0']=v; d[key+'1']=v
    cases=0
    for flags in product([0,1],repeat=3):
        types=[q for q,f in zip([2,3,5],flags) if f]
        s={format(i,'03b'): (types[(i-1)%len(types)] if i and types else 1) for i in range(8)}
        t=dict(s)
        for j in range(17):split(s,sorted(s)[j%len(s)])
        for j in range(11):split(t,sorted(t,reverse=True)[j%len(t)])
        for label in [1]+types:
            while sum(v==label for v in s.values())<sum(v==label for v in t.values()):
                split(s,next(k for k,v in s.items() if v==label))
            while sum(v==label for v in t.values())<sum(v==label for v in s.values()):
                split(t,next(k for k,v in t.items() if v==label))
        ck(valid(s) and valid(t),'prefix_partitions_complete_disjoint')
        mapping={}
        for label in [1]+types:
            a=sorted(k for k,v in s.items() if v==label)
            b=sorted(k for k,v in t.items() if v==label)
            mapping.update(zip(a,b))
        ck(set(mapping)==set(s) and set(mapping.values())==set(t), 'prefix_matching_bijective')
        ck(all(s[a]==t[b] for a,b in mapping.items()), 'prefix_matching_preserves_order_fibers')
        z=next(k for k in s if set(k)<={'0'})
        ck(set(mapping[z])<={'0'},'prefix_homeomorphism_fixes_point')
        cases+=1
    return {'order_type_patterns':cases,'pointed_prefix_homeomorphisms':cases}


# Sparse strictly upper triangular coordinates for 1+A. Identity is {}.
def plusmul(a,b,p):
    c=dict(a)
    for ij,v in b.items():c[ij]=(c.get(ij,0)+v)%p
    for (i,k),u in a.items():
        for (j,l),v in b.items():
            if k==j:c[i,l]=(c.get((i,l),0)+u*v)%p
    return {ij:v for ij,v in c.items() if v}


def inv(a,p,n):
    # In a finite unitriangular p-group, raising to q-1 computes inverse,
    # where q is a p-power at least n. This is independent of the author's
    # entry-by-entry triangular inverse algorithm.
    q=p
    while q<n:q*=p
    return power(a,q-1,p)


def power(a,k,p):
    r={}
    while k:
        if k&1:r=plusmul(r,a,p)
        a=plusmul(a,a,p); k//=2
    return r


def comm(a,b,p,n):
    r={}
    for v in [inv(a,p,n),inv(b,p,n),a,b]:r=plusmul(r,v,p)
    return r


def triangular():
    cases=0; extraction=0; first=0
    for p,m in [(2,3),(3,3),(5,3),(2,4),(3,4)]:
        slots=list(combinations(range(1,m+1),2)); n=m+2
        for vals in product(range(p),repeat=len(slots)):
            g={ij:v for ij,v in zip(slots,vals) if v}
            ck(plusmul(g,inv(g,p,n),p)=={},'sparse_inverse')
            for i in range(1,m+1):
                row={(0,k):v for (j,k),v in g.items() if j==i}
                got=comm({(0,i):1},g,p,n)
                ck(got==row,'sparse_first_commutator_row_extraction'); first+=1
            for (i,j),v in g.items():
                got=comm(comm({(0,i):1},g,p,n),{(j,n-1):1},p,n)
                ck(got=={(0,n-1):v},'sparse_double_commutator_extraction'); extraction+=1
            cases+=1
    ordercert=[]
    for p in [2,3,5,7]:
        for n in range(2,30):
            g={(i,i+1):1 for i in range(n-1)}; q=p
            while q<n:q*=p
            ck(power(g,q,p)=={} and power(g,q//p,p)!={},'sparse_exact_jordan_order')
            ordercert.append([p,n,q])
        g={(i,i+1):1 for i in range(p)}
        ck(power(g,p,p)!={},'negative_bounded_exponent_McLain')
    # Removing the outer fresh-index condition must fail; a conjugation
    # by a transvection at an already-used interior index is not row extraction.
    g={(0,1):1,(2,3):1}
    ck(comm({(1,2):1},g,3,4)!={(1,3):1},
       'negative_unjustified_row_formula_without_fresh_index')
    return {'all_interior_matrices':cases,'first_row_checks':first,
            'nonzero_entry_extractions':extraction,'jordan_orders':ordercert}


def heisenberg():
    result=[]
    for p,n in [(3,1),(5,1),(3,2)]:
        vectors=list(product(range(p),repeat=2*n)); zvec=(0,)*(2*n)
        el=[v+(z,) for v in vectors for z in range(p)]; index={x:i for i,x in enumerate(el)}
        def dot(x,y):return sum(a*b for a,b in zip(x,y))%p
        def form(v,w):return (dot(v[:n],w[n:])-dot(v[n:],w[:n]))%p
        def mul(x,y):return tuple((a+b)%p for a,b in zip(x[:-1],y[:-1]))+((x[-1]+y[-1]+dot(x[:n],y[n:2*n]))%p,)
        table=[[index[mul(x,y)] for y in el] for x in el]
        e=index[zvec+(0,)]; inverse=[next(j for j in range(len(el)) if table[i][j]==e) for i in range(len(el))]
        centers=[i for i in range(len(el)) if all(table[i][j]==table[j][i] for j in range(len(el)))]
        derived=set()
        for i,x in enumerate(el):
            for j,y in enumerate(el):
                k=table[table[table[inverse[i]][inverse[j]]][i]][j]
                ck(el[k]==zvec+(form(x[:-1],y[:-1]),),'Heisenberg_commutator'); derived.add(k)
                # Coordinate conversion z=a+(1/2)x.y from alternating law.
                a=(x[-1]-pow(2,-1,p)*dot(x[:n],x[n:2*n]))%p
                b=(y[-1]-pow(2,-1,p)*dot(y[:n],y[n:2*n]))%p
                xy=el[table[i][j]]
                lhs=(xy[-1]-pow(2,-1,p)*dot(xy[:n],xy[n:2*n]))%p
                ck(lhs==(a+b+pow(2,-1,p)*form(x[:-1],y[:-1]))%p,'Heisenberg_alternating_coordinate_isomorphism')
        ck(set(centers)==derived=={index[zvec+(t,)] for t in range(p)},'Heisenberg_center_derived')
        ck(1<len(centers)<len(el),'negative_characteristic_center')
        for i in range(len(el)):
            j=e
            for _ in range(p):j=table[j][i]
            ck(j==e,'Heisenberg_exponent')
        if n==1:
            for i in range(len(el)):
                for j in range(len(el)):
                    for k in range(len(el)):
                        ck(table[table[i][j]][k]==table[i][table[j][k]],'Heisenberg_associativity_exhaustive')
        maps=[]
        def lift(T,lam,ell):
            out=[]
            for x in el:
                v=x[:-1]; w=T(v)
                a=(x[-1]-pow(2,-1,p)*dot(v[:n],v[n:]))%p
                out.append(index[w+((lam*a+ell(v)+pow(2,-1,p)*dot(w[:n],w[n:]))%p,)])
            return out
        for u in vectors[1:]:
            maps.append(lift(lambda v,u=u:tuple((a+form(v,u)*b)%p for a,b in zip(v,u)),1,lambda v:0))
        for lam in range(1,p):
            maps.append(lift(lambda v,lam=lam:tuple((lam*a if j<n else a)%p for j,a in enumerate(v)),lam,lambda v:0))
        for j in range(2*n):maps.append(lift(lambda v:v,1,lambda v,j=j:v[j]))
        # Full multiplication-table checks for every selected automorphism in
        # every test group, including the rank-two group (author tested only E3).
        for f in maps:
            ck(len(set(f))==len(el),'Heisenberg_lift_bijection')
            ck(all(f[table[i][j]]==table[f[i]][f[j]] for i in range(len(el)) for j in range(len(el))),
               'Heisenberg_lift_full_homomorphism')
        unseen=set(range(len(el))); sizes=[]
        while unseen:
            seed=min(unseen); seen={seed}; todo=deque([seed])
            while todo:
                i=todo.popleft()
                for f in maps:
                    j=f[i]
                    if j not in seen:seen.add(j);todo.append(j)
            sizes.append(len(seen)); unseen-=seen
        ck(sorted(sizes)==[1,p-1,len(el)-p],'Heisenberg_three_certified_orbits')
        result.append({'prime':p,'rank':n,'order':len(el),'orbit_sizes':sorted(sizes),
                       'automorphisms_fully_checked':len(maps),'all_associativity_triples_checked':n==1})
    return result


def amalgam():
    result=[]
    for p in [3,5,7]:
        def mul(x,y):return ((x[0]+y[0])%p,(x[1]+y[1])%p,(x[2]+y[2]+x[0]*y[1])%p)
        def iv(x):return (-x[0]%p,-x[1]%p,(x[0]*x[1]-x[2])%p)
        def cm(x,y):return mul(mul(mul(iv(x),iv(y)),x),y)
        z=(0,0,1); x=(1,0,0); y=(0,1,0)
        ck(cm(x,y)==z,'amalgam_c_commutator_A')
        ck(all(cm(z,h)==(0,0,0) for h in product(range(p),repeat=3)), 'amalgam_c_central_A')
        c=list(product(range(p),repeat=2))
        ea=lambda v:(0,0,v[0],v[1]); eb=lambda v:(v[0],0,v[1])
        ck(len({ea(v) for v in c})==len({eb(v) for v in c})==p*p,'amalgam_injective')
        for v,w in product(c,repeat=2):
            u=((v[0]+w[0])%p,(v[1]+w[1])%p)
            ck(mul(eb(v),eb(w))==eb(u),'amalgam_B_homomorphism')
            ck(mul(ea(v)[:3],ea(w)[:3])+((ea(v)[3]+ea(w)[3])%p,)==ea(u),'amalgam_A_homomorphism')
        ck(cm(eb((1,0)),y)==eb((0,1))!=(0,0,0),'negative_class_two_amalgam')
        result.append({'prime':p,'A_order':p**4,'B_order':p**3,'C_order':p*p})
    return result


def source_checks(root, args):
    expected = json.loads((root/'SOURCE_VERIFICATION.json').read_bytes())
    out = {}
    if args.source_dir:
        records=[]
        for name, rec in zip(['primary.pdf','dantas2026.pdf','pseudofinite2025.pdf','course2026.pdf'], expected['sources']):
            b=(args.source_dir/name).read_bytes()
            ck(b.startswith(b'%PDF-'), 'source_pdf_signature')
            ck(len(b)==rec['bytes'] and digest(b)==rec['sha256'],'source_pdf_hash_size')
            records.append({'title':rec['title'],'public_url':rec['url'],
                            'bytes':len(b),'sha256':digest(b)})
        out['pdf_files']=records
    for flag,key in [('problems','problems_json'),('research_results','research_results_json'),('catalog','catalog_descriptor')]:
        path=getattr(args,flag)
        if path:
            b=path.read_bytes(); rec=expected['datasets'][key]
            ck(len(b)==rec['bytes'] and digest(b)==rec['sha256'],'dataset_hash_size')
            data=json.loads(b)
            value={'bytes':len(b),'sha256':digest(b),'entry_count':len(data)}
            if flag=='research_results':
                ck('KOU-21.39' not in data and '2548' not in data,'research_exact_target_absent')
                value['exact_target_keys_present']=False
            else:
                rows=[r for r in data if str(r.get('id'))=='2548']
                ck(len(rows)==1 and rows[0]['problem_number']=='KOU-21.39','dataset_exact_target_identity')
                value['exact_target_matches']=len(rows)
                if flag=='catalog':
                    ck(rows[0]['rank']==767,'catalog_rank')
                    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\x00'+b).hexdigest()
                    ck(blob==rec['computed_git_blob_sha'],'catalog_git_blob_hash')
                    value['git_blob_sha1']=blob
                    value['rank']=767
                    value['statement_hash']=rows[0]['statement_hash']
                    value['review_hash']=rows[0]['review_hash']
            out[flag]=value
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--author',type=Path,required=True)
    ap.add_argument('--source-dir',type=Path)
    ap.add_argument('--problems',type=Path);ap.add_argument('--research-results',type=Path);ap.add_argument('--catalog',type=Path)
    a=ap.parse_args(); root=a.author.resolve()
    verify_inventory(root)
    out={'schema':'kourovka-2548-independent-finite-audit-v1','author_manifest_sha256':PIN,
         'original_problem_solved':False,'scope':'Finite-model controls plus frozen-payload verification; infinite proofs require mathematical audit.'}
    out['author_replay']=replay(root); out['a5']=a5();out['pointed_cantor_controls']=pointed_partitions()
    out['mclain']=triangular();out['extraspecial']=heisenberg();out['amalgam']=amalgam()
    out['optional_source_checks']=source_checks(root,a)
    verify_inventory(root)
    out['assertion_counts']=dict(sorted(C.items()));out['total_independent_assertions']=sum(C.values())
    out['status']='PASS';print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
