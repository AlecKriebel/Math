#!/usr/bin/env python3
"""Exact independent check of the seven-point C15 primary-model obstruction."""
from pathlib import Path
from itertools import combinations
import hashlib,json,datetime
from independent_audit import det,need
from lattice_row_reproduction import row_hnf,member

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
A=(0,1,2,3,4,7,9)
COORDS=A[1:]

def relation(left,right):
    return tuple(int(x in left)-int(x in right) for x in COORDS)

def audit():
    files=['relation_cover/MIXED_PRIME_BARRIER.md','relation_cover/mixed_prime_barrier_check.json']
    manifest=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();dest=HERE/'snapshot'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        manifest.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    selected=[((0,3),(1,2)),((0,4),(1,3)),((1,4),(2,3)),((0,7),(3,4)),((0,9),(2,7)),((7,9),(0,1))]
    rows=[]
    for left,right in selected:
        need(len(set(left+right))==4,'vertices not four-distinct')
        need(set(left+right)<=set(A) and (sum(left)-sum(right))%15==0,'not a C15 collision')
        rows.append(relation(left,right))
    need(abs(det([list(r) for r in rows]))==15,'unexpected relation-lattice determinant')
    # Check explicit integral consequences, rather than divide by a group integer.
    certs={2:[0,1,-1,0,0,0],3:[1,1,-1,0,0,0],4:[1,2,-1,0,0,0],
           7:[2,3,-2,1,0,0],9:[2,4,-3,1,1,0]}
    for a,c in certs.items():
        v=tuple(sum(c[i]*rows[i][j] for i in range(6)) for j in range(6))
        want=tuple(int(x==a)-a*int(x==1) for x in COORDS)
        need(v==want,'false affine-value certificate')
    annihilator=(-4,-7,5,-2,-1,1)
    v=tuple(sum(annihilator[i]*rows[i][j] for i in range(6)) for j in range(6))
    need(v==(15,0,0,0,0,0),'false 15t annihilator certificate')
    # All collision rows are contained in the selected six-relation integer lattice.
    H=row_hnf(rows,6);all_collisions=[]
    for e,f in combinations(list(combinations(A,2)),2):
        if sum(e)%15!=sum(f)%15:continue
        need(not set(e)&set(f),'shared-endpoint collision')
        row=relation(e,f);need(member(H,row),'missing actual collision consequence')
        all_collisions.append([e,f])
    # Verify the positive cycle independently, including its closing edge.
    old=json.loads((ROOT/files[1]).read_text());c=tuple(old['cyclic_witness'])
    need(len(c)==len(A) and set(c)==set(A),'cycle not an enumeration')
    sums=[(c[i]+c[(i+1)%len(c)])%15 for i in range(len(c))]
    need(len(set(sums))==len(c) and sums==old['edge_sums'],'invalid rainbow cycle')
    # For cyclic primary targets these enumerate every allowed t and all induced maps.
    examples=[]
    for p in (2,3,5,7,11):
        q=p**3;ts=[t for t in range(q) if 15*t%q==0]
        for t in ts:
            values={a:a*t%q for a in A}
            need(all((sum(values[a] for a in e)-sum(values[a] for a in f))%q==0 for e,f in all_collisions),'induced map misses collision')
            need(len(set(values.values()))<len(A),'injective primary model')
            if p==3:need(values[3]==values[0],'p=3 pair')
            elif p==5:need(values[9]==values[4],'p=5 pair')
            else:need(len(set(values.values()))==1,'other-prime constant map')
        examples.append({'target_order':q,'prime':p,'allowed_t_count':len(ts),'max_image_size':max(len({a*t%q for a in A}) for t in ts)})
    for entry in manifest:need(hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],'source changed during review')
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':manifest,'subset':A,
            'six_relations_four_distinct_and_valid':True,'selected_relation_lattice_index':15,
            'affine_value_integer_certificates':certs,'annihilator_integer_coefficients':annihilator,
            'all_actual_distinct_edge_collision_count':len(all_collisions),'all_actual_collisions_implied':True,
            'cycle':c,'edge_sums':sums,'primary_cyclic_examples':examples,'passed':True}

if __name__=='__main__':
    r=audit();(HERE/'mixed_prime_barrier_audit_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
