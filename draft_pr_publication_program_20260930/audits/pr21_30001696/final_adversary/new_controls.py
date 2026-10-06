"""New adversarial controls. No import of candidate/previous-audit code.
Exact combinatorial elementary collapses, collar staircase, convex face posets,
and polynomial-coordinate orbit zero strata. Finite checks are supplementary.
"""
from itertools import combinations,product
from fractions import Fraction as Q
from math import comb
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,random
import sympy as sp
counts=Counter()
def check(label,c):
    if not c: raise AssertionError(label)
    counts[label]+=1

def subsets(a,empty=True):
    a=tuple(a)
    return [frozenset(c) for n in range(0 if empty else 1,len(a)+1) for c in combinations(a,n)]
def complex_of(facets):
    return set().union(*(set(subsets(f)) for f in facets))
def switches(w): return tuple(j for j in range(len(w)-1) if w[j]!=w[j+1])
def facets(d,i,final=None):
    return [frozenset((j+1)*s for j,s in enumerate(w)) for w in product((-1,1),repeat=d) if len(switches(w))<=i and (final is None or w[-1]==final)]
def free_pair(C,A,B,label):
    check(label,A in C and B in C and len(B)==len(A)+1 and A<B)
    check(label, {s for s in C if A<s}=={B})
    C.remove(A); C.remove(B)

def link_collapse(d,i,sgn):
    ordered=sorted([w for w in product((-1,1),repeat=d) if w[-1]==sgn and len(switches(w))<=i],key=lambda w:(len(switches(w)),switches(w)))
    Fs=[frozenset((j+1)*s for j,s in enumerate(w[:-1])) for w in ordered]
    C=complex_of(Fs); seq=[]
    for w,F in reversed(list(zip(ordered[1:],Fs[1:]))):
        R=frozenset((j+1)*w[j] for j in switches(w))
        check('shelling_restriction_proper',R<F)
        v=min(F-R)
        for G in sorted([G for G in subsets(F-{v}) if R<=G],key=lambda x:(-len(x),sorted(x))):
            B=G|{v};free_pair(C,G,B,'actual_link_free_pair');seq.append((G,B))
    v=min(Fs[0])
    for G in sorted(subsets(Fs[0]-{v},False),key=lambda x:(-len(x),sorted(x))):
        B=G|{v};free_pair(C,G,B,'first_simplex_free_pair');seq.append((G,B))
    check('link_collapses_to_vertex',C=={frozenset(),frozenset({v})})
    return seq,v

def classical():
    parameter_rows=[]
    for d in range(2,9):
        for i in range(d-1):
            C=complex_of(facets(d,i)); start=len(C); pairs=0
            for j in range(d,i+1,-1):
                for sgn in (1,-1):
                    seq,v=link_collapse(j,i,sgn); apex=sgn*j
                    for A,B in seq:
                        free_pair(C,A|{apex},B|{apex},'actual_union_cone_free_pair');pairs+=1
                    free_pair(C,frozenset({apex}),frozenset({apex,v}),'last_cone_edge_free_pair');pairs+=1
                check('embedded_coordinate_equator_exact',C==complex_of(facets(j-1,i)))
            core=complex_of(facets(i+1,i))
            check('entire_embedded_collapse_exact',C==core)
            check('collapse_face_accounting',start-len(core)==2*pairs)
            parameter_rows.append({'d':d,'i':i,'pairs':pairs,'final_core_faces':len(core)})
    for d in range(2,9):
        allF=facets(d,d-1)
        for i in range(d-1):
            KF=set(facets(d,i)); CF=set(allF)-KF
            K=complex_of(KF); C=complex_of(CF)
            boundary=[]
            for R in (s for s in K if len(s)==d-1):
                incid=[F for F in allF if R<F]
                check('ambient_ridge_two_facets',len(incid)==2)
                if sum(F in KF for F in incid)==1:boundary.append(R)
            shared=complex_of(boundary)
            check('all_strata_common_frontier',K&C==shared)
            complement_map=[frozenset(v if abs(v)%2 else -v for v in F) for F in facets(d,d-i-2)]
            check('exact_complementary_signed_isomorphism',set(complement_map)==CF)
    for d in range(2,9):
        w=tuple((-1)**j for j in range(d)); R=frozenset((j+1)*w[j] for j in switches(w)); F=frozenset((j+1)*w[j] for j in range(d-1))
        check('full_sphere_link_negative_control',R==F)
    return parameter_rows

def collar():
    bases=[complex_of(facets(d,d-1)) for d in range(1,5)]
    bases += [complex_of([{1,2},{2,3},{2,4}]),complex_of([{1,2,3},{3,4,5}])]
    for P in bases:
        def bottom(F):return frozenset((v,0) for v in F)
        C=set(); B=complex_of([bottom(F)|{('apex',-1)} for F in P if F])
        for F in P:
            vs=sorted(F)
            for j in range(len(vs)):
                T=frozenset([(v,0) for v in vs[:j+1]]+[(v,1) for v in vs[j:]])
                C|=set(subsets(T))
        C|=B
        for F in sorted([F for F in P if F],key=lambda F:(-len(F),sorted(F))):
            vs=sorted(F)
            for j in range(len(vs)):
                A=frozenset([(v,0) for v in vs[:j]]+[(v,1) for v in vs[j:]])
                upper=A|{(vs[j],0)}
                free_pair(C,A,upper,'collar_staircase_relative_free_pair')
                check('collar_preserves_all_glued_K_faces',B<=C)
        check('collar_exact_relative_remainder',C==B)

def rank(points):
    if len(points)<=1:return 0
    p0=points[0]
    return sp.Matrix([[x-y for x,y in zip(p,p0)] for p in points[1:]]).rank()
def faces_from_facets(vertices,facets):
    faces={frozenset(vertices)}
    for fac in facets:
        faces|={f&fac for f in list(faces)}
    return {f for f in faces if f}

def cell_posets():
    rows=[]
    for m in range(1,5):
        for n in range(1,5):
            labels=[(a,-1) for a in range(m)]+[(a,b) for a in range(m) for b in range(n)]
            # Truncated simplex facets come from alpha_a=0,beta_b=0,sum(beta)=1/2.
            trunc_facets=[frozenset(v for v in labels if v[0]!=a) for a in range(m)]
            trunc_facets += [frozenset(v for v in labels if v[1]!=b) for b in range(n)]
            trunc_facets += [frozenset(v for v in labels if v[1]!=-1)]
            # Product simplex x simplex facets: first or second coordinate omitted.
            prod_facets=[frozenset(v for v in labels if v[0]!=a) for a in range(m)]
            prod_facets += [frozenset(v for v in labels if v[1]!=b) for b in range(-1,n)]
            TF=faces_from_facets(labels,trunc_facets);PF=faces_from_facets(labels,prod_facets)
            check('independent_inequality_face_posets',TF==PF)
            def tv(v):
                a,b=v; p=[Q(0)]*(m+n);p[a]=Q(1) if b==-1 else Q(1,2)
                if b!=-1:p[m+b]=Q(1,2)
                return p
            def pv(v):
                a,b=v;p=[Q(0)]*(m+n+1);p[a]=1;p[m+b+1]=1;return p
            for F in TF:
                check('actual_convex_cell_affine_dimensions',rank([tv(v) for v in F])==rank([pv(v) for v in F]))
            # Restrictions to A',B' are exactly the same labelled faces in both realizations.
            for F in TF:
                for a in range(m):
                    check('cell_compatibility_E_subface', (F&frozenset(v for v in labels if v[0]!=a)) in TF|{frozenset()})
                for b in range(n):
                    check('cell_compatibility_F_subface',(F&frozenset(v for v in labels if v[1]!=b)) in TF|{frozenset()})
            rows.append({'sigma_vertices':m,'tau_vertices':n,'faces':len(TF)})
    # A naive join formula on a diagonal has a quadratic component on every interval.
    for x in [Q(j,16) for j in range(1,13)]:
        h=Q(1,32);f=lambda u:u*(1-u)
        check('bilinear_map_is_not_PL_negative_control',f(x+h)-2*f(x)+f(x-h)==-2*h*h)
    return rows

def kval(N,k,j):
    return sum((-1)**ell*(comb(j,ell) if 0<=ell<=j else 0)*(comb(N-j,k-ell) if 0<=k-ell<=N-j else 0) for ell in range(k+1))
def lo_var(v):
    s=[1 if x>0 else -1 for x in v if x];return sum(a!=b for a,b in zip(s,s[1:]))
def hi_var(v):
    zeros=[j for j,x in enumerate(v) if not x];out=0
    for fill in product((-1,1),repeat=len(zeros)):
        w=list(v)
        for j,s in zip(zeros,fill):w[j]=s
        out=max(out,lo_var(w))
    return out

def orbit_controls():
    a=sp.Symbol('a');rng=random.Random(30001696);rows=[];zero_roots=0
    for d in range(2,7):
        N=d-1
        for r in range(1,d):
            for seed in range(8):
                coeff=[rng.randrange(-3,4) for k in range(d)]
                if not any(coeff[:r]):coeff[0]=1
                if not any(coeff[r:]):coeff[-1]=1
                fs=[sp.Poly(sum(coeff[k]*kval(N,k,j)*a**k for k in range(d)),a,domain=sp.QQ) for j in range(d)]
                nonzero=[f for f in fs if not f.is_zero];master=sp.Poly(1,a)
                for f in nonzero:master=sp.lcm(master,f)
                master=master.sqf_part()
                isolates=[iv for iv,mult in master.intervals(eps=sp.Rational(1,10000)) if iv[0]>0]
                def val(x):return [int(sp.sign(f.eval(x))) for f in fs]
                probes=[];left=sp.Rational(0)
                for low,high in isolates:
                    probes.append((left+low)/2)
                    left=high
                probes.append(left+1)
                members=[lo_var(val(x))<=r-1 for x in probes]
                check('exact_orbit_allowed_initial_interval',members[0] and not members[-1] and members==sorted(members,reverse=True))
                check('exact_orbit_allowed_strict_interiors',all(hi_var(val(x))<=r-1 for x,m in zip(probes,members) if m))
                boundary_count=0
                for h,(low,high) in enumerate(isolates):
                    if low==high:v=val(low)
                    else:
                        v=[0 if f.is_zero or f.count_roots(low,high) else int(sp.sign(f.eval((low+high)/2))) for f in fs]
                    zeros=sum(x==0 for x in v);zero_roots+=zeros
                    member=lo_var(v)<=r-1;interior=hi_var(v)<=r-1
                    # Lower-interval closure means every isolated root strictly before exit is interior.
                    check('exact_zero_stratum_orbit_membership',member==members[h])
                    check('exact_zero_stratum_orbit_interior',interior==(members[h] and members[h+1]))
                    if member and not interior:boundary_count+=1
                check('exact_orbit_unique_zero_boundary',boundary_count==1)
                rows.append({'d':d,'r':r,'seed':seed,'positive_coordinate_root_strata':len(isolates)})
    return {'orbits':len(rows),'zero_coordinate_incidences':zero_roots,'rows':rows}

def main():
    started=datetime.now(timezone.utc).isoformat()
    rows=classical();collar();cells=cell_posets();orbits=orbit_controls()
    out={'status':'PASS','started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy':sp.__version__,'arithmetic':'exact finite combinatorics, rationals and certified real polynomial root isolations','counts':dict(counts),'assertions':sum(counts.values()),'embedded_collapse_parameters':rows,'truncated_cell_parameters':cells,'polynomial_orbit_controls':orbits,'prior_control_imports':False,'scope':'Falsification controls supplementary to the universal proof; no universal conclusion inferred from enumeration.'}
    Path(__file__).with_name('NEW_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['embedded_collapse_parameters','truncated_cell_parameters','polynomial_orbit_controls']},indent=2))
if __name__=='__main__':main()
