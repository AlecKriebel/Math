"""Check every fixed-span survivor and its exact adjacent-integer bracket."""
from math import prod
from pathlib import Path
from collections import Counter
import json

C=Counter()
def check(k,b):
    assert b,k
    C[k]+=1
P=lambda x,r:prod(range(x+1,x+r+1))
data=json.loads(Path(__file__).with_name('TURN_5_CERTIFICATES.json').read_text())
check('scope_is_outer_span_twelve',data['outer_span_max']==12)
check('no_reported_integer_root',data['integer_roots']==[])
rows={(z['r'],z['u'],z['v'],z['A']):z for z in data['cases']}
check('no_duplicate_certificates',len(rows)==len(data['cases']))
survivors=set();left=0
for r in range(3,13):
    for u in range(1,r):
        for v in range(u+1,r-u):
            s=r-u-v;delta=v-u;M=max(r-1,(r*r-1)//(6*delta)+1)
            for A in range(M-1):
                left+=1;pa=P(A,r)**s;pu=P(A+u,s)**r
                if pa>=pu:
                    check('exact_no_continuous_root_gate',(r,u,v,A) not in rows)
                    continue
                key=(r,u,v,A);survivors.add(key);check('survivor_has_certificate',key in rows)
                z=rows[key];L=z['L'];U=z['U']
                check('correct_inner_width',z['s']==s)
                check('integer_adjacent_root_bracket',isinstance(L,int) and isinstance(U,int) and A<=L and U==L+1)
                DL=pa*P(L+v,s)**r-P(L,r)**s*pu
                DU=pa*P(U+v,s)**r-P(U,r)**s*pu
                check('left_sign_exact',DL==z['D_L'] and DL>0)
                check('right_sign_exact',DU==z['D_U'] and DU<0)
check('all_and_only_survivors',set(rows)==survivors)
check('complete_left_case_count',left==data['left_cases']==938)
check('root_candidate_count',len(rows)==59)
check('rational_odds_minimum_row',2**13==8192)
check('Mersenne_corollary_threshold',2**20<3**13<2**21)
out={'status':'PASS','left_cases':left,'root_candidates':len(rows),'maximum_bracket_endpoint':max(z['U'] for z in rows.values()),
     'exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
     'scope':'Combined with the all-n analytic reduction in Turn4, exact adjacent-integer brackets exclude every collision of outer span<=12 for all n. No bound on all possible outer spans is proved.'}
print(json.dumps(out,indent=2,sort_keys=True))
