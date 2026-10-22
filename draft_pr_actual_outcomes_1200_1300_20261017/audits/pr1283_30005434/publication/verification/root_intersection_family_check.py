#!/usr/bin/env python3
"""Independent finite intersection-family diagnostics, not a universal proof."""
import itertools,json,sys
def need(v,message):
    if not v:raise RuntimeError(message)
def check(family,meet,op,e,joint):
    for x,y,z in itertools.product(family,repeat=3):
        need(op(x,meet(y,z))==meet(op(x,y),op(x,z)),'S1')
        need(op(meet(x,y),z)==op(op(x,y),op(x,z)),'S3')
        if joint:need(op(op(x,y),op(x,z))==op(op(y,x),op(y,z)),'cycloid')
    for x in family:
        need(op(e,x)==x,'left identity');need(op(x,e)==e,'absorption')
        if joint:need(op(x,x)==e,'diagonal')
    if joint:
        for x,y in itertools.product(family,repeat=2):
            need((op(x,y)==e)==(meet(x,y)==x),'order equality')
            need((op(x,y)==e and op(y,x)==e)==(x==y),'separation')

def run():
    if '--inject-failure' in sys.argv:need(False,'injected explicit predicate')
    counts=[];m3_seen=False;n5_seen=False;no_top_seen=False
    for size in range(4):
        subsets=tuple(range(1<<size));retained=pointed=top_count=triples=0
        for mask in range(1,1<<len(subsets)):
            family=tuple(x for x in subsets if mask>>x&1)
            members=set(family)
            if not all(x&y in members for x,y in itertools.product(family,repeat=2)):continue
            retained+=1
            for e in family:
                check(family,lambda x,y:x&y,lambda x,y:y,e,False);pointed+=1
            union=0
            for x in family:union|=x
            if union not in members:no_top_seen=True;continue
            top_count+=1;e=union
            def op(x,y):return e if x&y==x else x&y
            check(family,lambda x,y:x&y,op,e,True);triples+=len(family)**3
            if size==3 and members=={0,1,2,4,7}:m3_seen=True
            if size==3 and members=={0,1,3,4,7}:n5_seen=True
        counts.append({'ground_size':size,'all_intersection_closed_nonempty_families':retained,'all_pointed_projection_instances':pointed,'families_with_greatest_element':top_count,'joint_triples_checked':triples})
    need(m3_seen and n5_seen and no_top_seen,'Required structural boundaries not represented')
    # The unrelated y-valued formula on the Boolean square must fail S1.
    square=(0,1,2,3);e=3
    def wrong(x,y):return e if x&y==x else y
    need(wrong(1,1&2)!=wrong(1,1)&wrong(1,2),'Problem10 negative control did not fail')
    return {'status':'PASS','mechanism':'All nonempty intersection-closed families of subsets of ground sets0..3; independent of natural-poset enumeration. Ground-labelled families are not deduplicated.','counts':counts,'M3_included':m3_seen,'N5_included':n5_seen,'no_greatest_family_included':no_top_seen,'distinct_y_branch_negative_control':True,'scope':'Finite diagnostics of universal equations only. No exhaustive arbitrary multiplication search, infinite verification, historical aggregate replay or proof-assistant certification.'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
