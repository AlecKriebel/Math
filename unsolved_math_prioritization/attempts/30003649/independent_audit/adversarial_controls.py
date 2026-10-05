#!/usr/bin/env python3
"""Fresh negative controls; source witness contents never enter output files."""
import copy
from fractions import Fraction as F
import gzip
from itertools import permutations
import json
from pathlib import Path
import random
import shutil
import sys
import tempfile
from independent_verifier import Field, all_cofactors, check, facet_checks, full_rank, gram_checks, load, seed_checks


def rejected(name, thunk, text):
    try: thunk()
    except ValueError as exc:
        check(text in str(exc), 'unexpected failure in '+name+': '+str(exc))
        return {'case':name,'rejected':True,'reason':str(exc)}
    raise RuntimeError('corruption accepted: '+name)


def det_permutation(a):
    n=len(a); total=0
    for order in permutations(range(n)):
        inv=sum(order[i]>order[j] for i in range(n) for j in range(i+1,n))
        term=(-1)**inv
        for i,j in enumerate(order):term*=a[i][j]
        total+=term
    return total


def arithmetic_controls():
    rng=random.Random(30003649)
    for _ in range(2000):
        a=[F(rng.randrange(-20,21),rng.randrange(1,21)) for _ in range(3)]
        b=[F(rng.randrange(-20,21),rng.randrange(1,21)) for _ in range(3)]
        polynomial=[F(0)]*5
        for i in range(3):
            for j in range(3):polynomial[i+j]+=a[i]*b[j]
        polynomial[0]+=2*polynomial[3]; polynomial[1]+=2*polynomial[4]
        check(Field(a)*Field(b)==Field(polynomial[:3]),'independent schoolbook multiplication')
    for case in range(24):
        rows=[[rng.randrange(-9,10) for _ in range(7)] for _ in range(6)]
        if case%6==0: rows[-1]=rows[0][:]
        _,actual=next(all_cofactors(rows))
        expected=tuple((-1)**j*det_permutation([[x for k,x in enumerate(row) if k!=j] for row in rows]) for j in range(7))
        check(actual==expected,'Laplace versus permutation cofactors')
    check(full_rank([[1,0,0],[0,1,0],[0,0,1]],3),'full rank positive control')
    check(not full_rank([[1,0,0],[0,1,0],[1,1,0]],3),'rank negative control')
    check(Field([0,0,1])*Field([0,1,0])==2,'root relation')
    check(Field([-2,0,0]).interval(F(1),F(2))[1]<0,'negative sign')
    return {'field_products':2000,'cofactor_permutation_comparisons':24,'rank_controls':2,'root_and_sign_controls':2}


def run(data):
    arithmetic=arithmetic_controls();seed,cone,facets,R=load(data)
    P,O,interval=seed_checks(seed,cone);results=[]
    s=copy.deepcopy(seed);s['orthogonal_matrix'][0][0][0]=str(F(s['orthogonal_matrix'][0][0][0])+1)
    results.append(rejected('alter_orthogonal_entry',lambda:seed_checks(s,cone),'orthogonality'))
    s=copy.deepcopy(seed);s['Q'][0][0][0]=str(F(s['Q'][0][0][0])+1)
    results.append(rejected('alter_trace',lambda:seed_checks(s,cone),'trace zero'))
    s=copy.deepcopy(seed)
    for key in ['Q','Qprime']:
        s[key]=[[[str(-F(c)) for c in x] for x in row] for row in s[key]]
    s['restricted_gram']=[[[[str(-F(c)) for c in x] for x in row] for row in H] for H in s['restricted_gram']]
    results.append(rejected('consistent_negative_form_preserves_trace_and_kernel',lambda:seed_checks(s,cone),'local first minor'))
    c=copy.deepcopy(cone);c['barycentric_coefficients']=[['0','0','0']]*3
    results.append(rejected('remove_barycentric_inclusion',lambda:seed_checks(seed,c),'barycentric positivity'))
    c=copy.deepcopy(cone);c['generators'][0][0]=str(F(c['generators'][0][0])+1)
    results.append(rejected('alter_generator',lambda:seed_checks(seed,c),'generator identity'))
    c=copy.deepcopy(cone);c['positive_slice_functional']=[str(-F(x)) for x in c['positive_slice_functional']]
    results.append(rejected('reverse_pointing_functional',lambda:seed_checks(seed,c),'pointedness'))
    f=copy.deepcopy(facets);f['facet_normals'].pop()
    results.append(rejected('omit_complete_halfspace',lambda:facet_checks(P,f,R),'complete facet normals'))
    f=copy.deepcopy(facets);f['facet_normals'][0]=[-x for x in f['facet_normals'][0]]
    results.append(rejected('reverse_facet_orientation',lambda:facet_checks(P,f,R),'complete facet normals'))
    with tempfile.TemporaryDirectory() as temp:
        dest=Path(temp)
        for item in data.iterdir():
            if item.is_file():shutil.copy2(item,dest/item.name)
        path=dest/'A_integer.mtx.gz';lines=gzip.decompress(path.read_bytes()).decode().splitlines()
        candidates=[i for i,x in enumerate(lines) if x and not x.startswith('%')]
        i=candidates[1];a,b,z=map(int,lines[i].split());lines[i]=f'{a} {b} {z+1}'
        path.write_bytes(gzip.compress(('\n'.join(lines)+'\n').encode(),mtime=0))
        results.append(rejected('Gram_hash_pin',lambda:load(dest),'pinned input mismatch'))
        results.append(rejected('Gram_value_mathematical_check',lambda:gram_checks(dest,R),'Gram equality'))
        lines[i]=f'{a} {b} {z}';lines[candidates[-1]]=lines[i]
        path.write_bytes(gzip.compress(('\n'.join(lines)+'\n').encode(),mtime=0))
        results.append(rejected('Gram_duplicate_coordinate',lambda:gram_checks(dest,R),'Gram unique index'))
    return {'status':'PASS','arithmetic':arithmetic,'corruption_controls':results,'count':len(results),'scope':'After validating original pins, in-memory negative tests exercise mathematical predicates independently of hash rejection.'}


if __name__=='__main__':print(json.dumps(run(Path(sys.argv[1])),sort_keys=True,indent=2))
