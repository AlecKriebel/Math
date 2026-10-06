"""Independent coefficient restrictions, using line vectors rather than inverse defining-form coordinates.
All 7,175 unions of 1--3 rational lines, and all 15,488 plane multisets of degrees 2--5.
Finite controls over F2 extend as rank statements to its algebraic closure; not an adjoint certificate.
"""
import collections,datetime,functools,hashlib,itertools,json,os,pathlib
counts=collections.Counter()
def ck(x,label):
    if not x: raise RuntimeError(label)
    counts[label]+=1
def span2(u,v): return tuple(sorted((u,v,u^v)))
vectors=tuple(range(1,16))
lines=tuple(sorted({span2(u,v) for u,v in itertools.combinations(vectors,2)}))
ck(len(lines)==35,'all_35_rational_lines')
def dot(u,v): return (u&v).bit_count()%2
planes=tuple(range(1,16))
incidence=tuple(tuple(h for h in planes if all(dot(h,u)==0 for u in L)) for L in lines)
ck(all(len(hs)==3 for hs in incidence),'three_planes_through_each_rational_line')
@functools.lru_cache(None)
def mons(d,n=4):
    if n==1: return ((d,),)
    return tuple((a,)+r for a in range(d+1) for r in mons(d-a,n-1))
def rank(rows):
    piv={}
    for row in rows:
        while row:
            lead=row.bit_length()-1
            if lead in piv: row ^= piv[lead]
            else: piv[lead]=row; break
    return len(piv)
def vec_rank(vs): return rank(vs)
def poly_mul(a,b):
    out=set()
    for x in a:
        for y in b:
            z=tuple(i+j for i,j in zip(x,y))
            if z in out: out.remove(z)
            else: out.add(z)
    return out
@functools.lru_cache(None)
def constraints(idx,d,m):
    u,v=lines[idx][:2]; basis=[u,v]
    for a in (1,2,4,8):
        if vec_rank(basis+[a])>len(basis): basis.append(a)
    ck(len(basis)==4,'vector_parametrization_invertible')
    linear=[{tuple(int(j==b) for j in range(4)) for b,a in enumerate(basis) if a>>i&1} for i in range(4)]
    rows=collections.defaultdict(int)
    for col,ex in enumerate(mons(d)):
        f={(0,0,0,0)}
        for i,e in enumerate(ex):
            for _ in range(e): f=poly_mul(f,linear[i])
        for target in f:
            if target[2]+target[3]<m: rows[target]^=1<<col
    return tuple(rows.values())
def ker_exists(indices,d,m=1): return rank(itertools.chain.from_iterable(constraints(i,d,m) for i in indices))<len(mons(d))
def coplanar(indices): return bool(set.intersection(*(set(incidence[i]) for i in indices)))
def common_point(indices): return bool(set.intersection(*(set(lines[i]) for i in indices)))
unions=collections.Counter(); digest=hashlib.sha256()
for n in (1,2,3):
    for ids in itertools.combinations(range(35),n):
        a=1 if ker_exists(ids,1) else 2
        ck(a==1 or ker_exists(ids,2),'three_lines_have_alpha_at_most_two')
        double2=ker_exists(ids,2,2); double3=ker_exists(ids,3,2)
        ck(not double2 or double3,'double_degree_monotonicity')
        equality=double2 if a==1 else (not double2 and double3)
        cp=coplanar(ids)
        expected=cp or (n==3 and common_point(ids))
        ck(equality==expected,'all_small_union_equality_cases_classified')
        unions[(n,a,equality,cp)]+=1
        digest.update(json.dumps([ids,a,double2,double3,equality,cp],separators=(',',':')).encode()+b'\n')
plane_summary=collections.Counter(); plane_digest=hashlib.sha256()
for d in range(2,6):
    for hs in itertools.combinations_with_replacement(planes,d):
        mult=collections.Counter(hs)
        ids=tuple(i for i,ps in enumerate(incidence) if sum(mult[h] for h in ps)>=2)
        ck(bool(ids),'plane_product_double_locus_nonempty')
        no_triple=all(sum(h in ps for h in mult)<=2 for ps in incidence)
        squarefree=len(mult)==d
        low=ker_exists(ids,d-2)
        cp=coplanar(ids)
        expected_low=not(squarefree and no_triple) if d>=3 else False
        ck(low==expected_low,'plane_multiset_repetition_and_triple_line_obstruction')
        if squarefree and no_triple:
            ck(len(ids)==d*(d-1)//2,'complete_pair_intersection_count')
            ck(ker_exists(ids,d-1),'star_initial_degree_upper_bound')
            ck(not low,'star_initial_degree_lower_bound')
        plane_summary[(d,squarefree,no_triple,cp,low)]+=1
        plane_digest.update(json.dumps([hs,ids,low,cp],separators=(',',':')).encode()+b'\n')
result={'status':'PASS_INDEPENDENT_GF2_BOUNDED_FALSIFICATION','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'explicit_checks':sum(counts.values()),'counts':dict(sorted(counts.items())),'union_count':sum(unions.values()),'union_table':[{'lines':k[0],'alpha':k[1],'equality':k[2],'coplanar':k[3],'count':v} for k,v in sorted(unions.items())],'union_digest_sha256':digest.hexdigest(),'plane_multiset_count':sum(plane_summary.values()),'plane_multiset_table':[{'degree':k[0],'squarefree':k[1],'no_triple_line':k[2],'coplanar':k[3],'degree_d_minus_two_form_exists':k[4],'count':v} for k,v in sorted(plane_summary.items())],'plane_multiset_digest_sha256':plane_digest.hexdigest(),'qualification':'Exact F2 coefficient ranks over its algebraic closure. Exhaustive only for unions of at most three F2-rational lines and plane multisets of total degree two through five. Not a validation of the integral-surface adjoint input or a universal proof.'}
print(json.dumps(result,indent=2,sort_keys=True))
