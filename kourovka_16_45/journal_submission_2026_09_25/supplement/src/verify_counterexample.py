#!/usr/bin/env python3
"""Independent, standard-library-only verification of the finite certificates.

No GAP, group catalogue, numerical optimizer, network, or saved table is used.
The proof for *all* subgroups/actions is in the accompanying journal manuscript;
this program verifies its concrete finite inputs and its explicit witnesses.

Usage: python3 src/verify_counterexample.py --outdir build
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

Matrix = tuple[int, int, int, int]
I: Matrix = (1, 0, 0, 1)
A: Matrix = (0, 28, 1, 0)
B: Matrix = (2, 7, 12, 28)
R: tuple[Matrix, ...] = (A, (12, 24, 0, 17), (25, 3, 4, 4))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mm(x: Matrix, y: Matrix, p: int = 29) -> Matrix:
    a,b,c,d=x; e,f,g,h=y
    return ((a*e+b*g)%p, (a*f+b*h)%p,
            (c*e+d*g)%p, (c*f+d*h)%p)


def mpow(x: Matrix, exponent: int, p: int = 29) -> Matrix:
    y=I
    for _ in range(exponent):
        y=mm(y,x,p)
    return y


def closure(generators, identity, multiply):
    """Positive-word BFS. Finiteness makes this the generated subgroup."""
    elements=[identity]; known={identity}
    for x in elements:
        for g in generators:
            y=multiply(x,g)
            if y not in known:
                known.add(y);elements.append(y)
    return elements


def all_subgroups(table):
    """All actual subgroups, not conjugacy representatives.

    From each known H, adjoin every x outside H. Any subgroup K is reached
    by following a generating sequence for K, starting at {1}.
    """
    n=len(table)
    groups=[(frozenset({0}), ())]; seen={groups[0][0]}
    for elements, generators in groups:
        for x in range(n):
            if x in elements:
                continue
            gens=generators+(x,)
            h=frozenset(closure(gens,0,lambda a,b:table[a][b]))
            if h not in seen:
                seen.add(h);groups.append((h,gens))
    return groups


def meet(family, full):
    result=full
    for h in family:
        result &= h
    return result


def certify_ranks(table, subs):
    n=len(table);full=(1<<n)-1
    masks=[sum(1<<x for x in h) for h,_ in subs if len(h)<n]
    count4=0
    # Any subfamily of a meet-irredundant family is meet-irredundant.
    # Therefore absence of an irredundant 4-family rules out every larger rank.
    for a,b,c,d in itertools.combinations(masks,4):
        count4+=1
        all4=a&b&c&d
        require(not (b&c&d!=all4 and a&c&d!=all4 and
                     a&b&d!=all4 and a&b&c!=all4),
                'An unexpected irredundant 4-family exists')
    count3=0
    for a,b,c in itertools.combinations(masks,3):
        count3+=1
        require(not (a&b&c==1 and a&b!=1 and a&c!=1 and b&c!=1),
                'An unexpected faithful minimal 3-family exists')
    return {'all_proper_subgroup_4_families_checked':count4,
            'irredundant_4_families':0,
            'all_proper_subgroup_3_families_checked':count3,
            'faithful_minimal_3_families':0}


def affine_mul(x, y, p=29):
    vx,vy,a,b,c,d=x; wx,wy,e,f,g,h=y
    return ((vx+a*wx+b*wy)%p,(vy+c*wx+d*wy)%p,
            (a*e+b*g)%p,(a*f+b*h)%p,
            (c*e+d*g)%p,(c*f+d*h)%p)


def aff(v, h):
    return (v[0],v[1],*h)


def pcompose(a,b):
    return tuple(a[b[i]] for i in range(len(a)))


def run(outdir=None):
    start=time.perf_counter(); p=29;z=(28,0,0,28)
    H=closure([A,B],I,mm);idx={h:i for i,h in enumerate(H)}
    require(len(H)==120,'Complement order is not 120')
    require(all((a*d-b*c)%29==1 for a,b,c,d in H),'Determinant failure')
    require(mpow(A,2)==mpow(B,3)==mpow(mm(A,B),5)==z,'Triangle relations fail')
    table=[[idx[mm(x,y)] for y in H] for x in H]
    inv=[next(j for j in range(120) if table[i][j]==0) for i in range(120)]
    # Independently certify isomorphism to the concrete group SL(2,5).
    A5=(0,4,1,0);B5=(0,4,1,1)
    pairs=closure([(A,A5),(B,B5)],(I,I),lambda x,y:(mm(x[0],y[0]),mm(x[1],y[1],5)))
    full_sl5={(a,b,c,d) for a,b,c,d in itertools.product(range(5),repeat=4) if (a*d-b*c)%5==1}
    require(len(pairs)==120 and len({x for x,y in pairs})==120 and
            {y for x,y in pairs}==full_sl5,'SL(2,5) isomorphism failure')
    # Certify the quotient map onto A5 using permutation multiplication.
    pa=(1,0,3,2,4)   # (1 2)(3 4), in one-based notation
    pb=(2,1,4,3,0)   # (1 3 5)
    pm=closure([(A,pa),(B,pb)],(I,tuple(range(5))),lambda x,y:(mm(x[0],y[0]),pcompose(x[1],y[1])))
    require(len(pm)==120 and len({x for x,y in pm})==120 and len({y for x,y in pm})==60,'A5 quotient failure')
    require({x for x,y in pm if y==tuple(range(5))}=={I,z},'Quotient kernel failure')
    # Full subgroup enumeration, independent of the C++ enumerator.
    subs=all_subgroups(table)
    require(len(subs)==76,'Unexpected number of complement subgroups')
    zi=idx[z]
    odd_orders=sorted({len(h) for h,_ in subs if len(h)%2})
    require(odd_orders==[1,3,5],'Unexpected odd subgroup')
    require([i for i in range(1,120) if table[i][i]==0]==[zi],'Involution is not unique')
    normals=[]
    for h,gs in subs:
        if all(table[table[inv[g]][x]][g] in h for g in range(120) for x in gs):normals.append(h)
    require(sorted(map(len,normals))==[1,2,120],'Normal subgroups mismatch')
    ranks=certify_ranks(table,subs)
    # Independent triple in the complement, and its normal-bottom 3-family.
    require(all(r in idx for r in R),'Independent matrix missing')
    omit_H=[set(closure([r for j,r in enumerate(R) if j!=i],I,mm)) for i in range(3)]
    require([len(h) for h in omit_H]==[8,12,20],'Pair subgroup orders mismatch')
    require(len(closure(R,I,mm))==120,'Triple does not generate H')
    require(set.intersection(*omit_H)=={I,z},'Omission intersection in H is not Z')
    require(all(R[i] not in omit_H[i] for i in range(3)),'Triple not independent')
    # All thirty F_29-lines; each stabilizer must be C4.
    lines=[(1,a) for a in range(p)]+[(0,1)]
    stabilizers=[]
    for x,y in lines:
        st=[h for h in H if ((h[0]*x+h[1]*y)*y-(h[2]*x+h[3]*y)*x)%p==0]
        require(len(st)==4 and any(mpow(h,2)==z for h in st),'A line stabilizer is not C4')
        stabilizers.append([idx[h] for h in st])
    # Actual affine generation, without a 100920-by-100920 table.
    identity=aff((0,0),I);translation=aff((1,0),I)
    S=[translation]+[aff((0,0),r) for r in R]
    fullG=closure(S,identity,affine_mul)
    require(len(fullG)==100920,'Affine group order mismatch')
    omissions=[set(closure(S[:i]+S[i+1:],identity,affine_mul)) for i in range(4)]
    omission_orders=[len(h) for h in omissions]
    require(omission_orders==[120,6728,10092,16820],'Affine omission orders mismatch')
    require(all(S[i] not in omissions[i] for i in range(4)),'4-set is not independent')
    total_omission=set.intersection(*omissions)
    Zaff={identity,aff((0,0),z)}
    require(total_omission==Zaff,'Affine omission intersection is not the complement center')
    tinv=aff((28,0),I)
    moved_z=affine_mul(affine_mul(translation,aff((0,0),z)),tinv)
    require(moved_z==aff((2,0),z) and moved_z not in Zaff,'Nonnormality witness failure')
    # Explicit faithful minimal 3-family, each subgroup of order 58.
    base_gens=[ [aff((1,0),I),aff((0,0),z)],
                [aff((0,1),I),aff((0,0),z)],
                [aff((1,1),I),aff((2,0),z)] ]
    base_subs=[set(closure(gs,identity,affine_mul)) for gs in base_gens]
    require([len(h) for h in base_subs]==[58]*3,'3-family subgroup sizes mismatch')
    require(set.intersection(*base_subs)=={identity},'3-family is not faithful')
    pair_meets=[base_subs[(i+1)%3]&base_subs[(i+2)%3] for i in range(3)]
    require([len(h) for h in pair_meets]==[2]*3,'3-family is not minimal')
    # Core calculation for the three preimages; first omission core is trivial.
    core_orders=[]
    for k in omit_H:
        ki={idx[x] for x in k};core=set(range(120))
        for g in range(120):core&={table[table[inv[g]][x]][g] for x in ki}
        require(core=={0,zi},'Pair subgroup core is not Z')
        core_orders.append(841*len(core))
    Haff=omissions[0]
    conjugate_H={affine_mul(affine_mul(translation,h),tinv) for h in Haff}
    require(Haff & conjugate_H=={identity},'Complement core not certified trivial')
    # Adversarial characteristic 11: a faithful 4-family DOES exist.
    p11=11;z11=(10,0,0,10);A11=(0,10,1,0);B11=(0,2,5,1)
    H11=closure([A11,B11],I,lambda x,y:mm(x,y,11))
    require(len(H11)==120,'Characteristic-11 complement wrong')
    c=next(h for h in H11 if mpow(h,10,11)==I and mpow(h,5,11)==z11 and mpow(h,2,11)!=I)
    eiglines=[(1,a) for a in range(11)]+[(0,1)]
    eiglines=[(x,y) for x,y in eiglines if ((c[0]*x+c[1]*y)*y-(c[2]*x+c[3]*y)*x)%11==0]
    require(len(eiglines)==2,'Split torus does not have two eigenlines')
    am11=lambda x,y:affine_mul(x,y,11)
    gs11=[[aff(eiglines[0],I),aff((0,0),c)],
          [aff(eiglines[1],I),aff((0,0),c)],
          [aff((1,0),I),aff((0,1),I),aff((0,0),mpow(c,5,11))],
          [aff((1,0),I),aff((0,1),I),aff((0,0),mpow(c,2,11))]]
    fam11=[set(closure(gs,identity,am11)) for gs in gs11]
    require([len(h) for h in fam11]==[110,110,242,605],'Characteristic-11 subgroup sizes wrong')
    require(set.intersection(*fam11)=={identity},'Characteristic-11 family not faithful')
    deletion11=[len(set.intersection(*(fam11[:i]+fam11[i+1:]))) for i in range(4)]
    require(deletion11==[11,11,5,2],'Characteristic-11 minimality failure')
    summary={
        'result':'PASS','prime':29,'group_order':100920,
        'claimed_invariants_proved_in_manuscript':{'b':3,'mu_prime':4,'faithful_maximum_minimal_base':3},
        'complement':{'order':120,'subgroups':76,'normal_subgroup_orders':[1,2,120],
                      'odd_subgroup_orders':odd_orders,'unique_involution':z,
                      'isomorphism_to_SL2_5_verified':True,'quotient_A5_verified':True,
                      **ranks},
        'line_stabilizers':{'number_of_lines':30,'all_orders':4,'all_cyclic':True},
        'independent_set':S,'omission_orders':omission_orders,
        'omission_total_intersection_order':2,'omission_intersection_normal':False,
        'omission_core_orders':[1]+core_orders,
        'faithful_3_family':{'subgroup_orders':[58]*3,'pair_intersection_orders':[2]*3,
                             'total_intersection_order':1,'coset_action_degree':5220},
        'adversarial_prime_11':{'torus_generator':c,'eigenlines':eiglines,
                              'subgroup_orders':[110,110,242,605],
                              'deletion_intersection_orders':deletion11},
        'affine_elements_sha256':hashlib.sha256(json.dumps(sorted(fullG),separators=(',',':')).encode()).hexdigest(),
        'seconds':round(time.perf_counter()-start,3),
        'scope':'The program verifies finite certificates. The universal upper bound on all affine subgroup families is structural, not a large-group enumeration.'}
    if outdir is not None:
        outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
        (outdir/'verification_python.json').write_text(json.dumps(summary,indent=2)+'\n')
        cert={'prime':29,'generators':[A,B],'matrices':H,
              'subgroups':[{'elements':sorted(h),'generators':list(gs)} for h,gs in subs],
              'line_vectors':lines,'line_stabilizers':stabilizers,
              'isomorphism_SL2_5':[{'matrix29':x,'matrix5':y} for x,y in pairs],
              'quotient_A5':[{'matrix':x,'permutation':y} for x,y in pm],
              'faithful_base_subgroup_generators':base_gens,
              'faithful_base_pair_intersections':[sorted(h) for h in pair_meets]}
        (outdir/'finite_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir',type=Path,default=None)
    args=parser.parse_args()
    print(json.dumps(run(args.outdir),indent=2))
