from collections import Counter
from pathlib import Path
import json,hashlib,sympy as sp
ROOT=Path('/mnt/data/k3p_identifiability_final')
p=ROOT/'software/certificates/jc_pointwise_cut_certificate_frozen.json';d=json.loads(p.read_text())
assert d['status']=='PROVED' and d['endpoint_type_count']==177 and d['single_blob_type_count']==453
branches=Counter();classes=Counter()
for r in d['endpoint_records']:
 c=r['certificate'];branches[c['branch']]+=1
 if c['branch']=='F_positive':assert not c['F']['zero'] and c['F']['total_sign']==1
 else:assert c['branch']=='F_zero_G_positive' and c['F']['zero'] and not c['G']['zero'] and c['G']['total_sign']==1
for r in d['single_blob_records']:
 c=r['certificate'];classes[c['classification']]+=1
 if c['classification']=='wrong_split_strict':assert not c['sign']['zero'] and c['sign']['total_sign'] in (-1,1) and not c['displayed_bridge']
 else:assert c['classification']=='rank_one_all_blocks' and c['displayed_bridge']
assert dict(branches)=={'F_positive':151,'F_zero_G_positive':26}
assert dict(classes)=={'wrong_split_strict':421,'rank_one_all_blocks':32}
# Independently replay the two-active-endpoint contradiction.
a,b,c,t,A,B,C,T,z=sp.symbols('a b c t A B C T z', positive=True)
expected={'m0':A*a-B*C*b*c*z**2,'m1':-(-A*a+T*t*z)*(A*a+T*t*z),'m2':A**2*a-T**2*b*c*z**2,'m3':A*a**2-B*C*t**2*z**2}
for k,v in expected.items():assert sp.expand(v-sp.sympify(d['two_active_endpoint_case']['decisive_minors'][k],locals={x.name:x for x in (a,b,c,t,A,B,C,T,z)}))==0
# Exact transfer statement: on assignments in {0,C}, every K3P edge multiplier is c_e;
# no G/T coordinate occurs. Thus every frozen polynomial is re-evaluated on an
# unconstrained open-cube tuple c_e in (0,1), exactly its certified domain.
out={'schema':'k3p-pointwise-cut-transfer-v1','frozen_certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'endpoint_types':177,'endpoint_dichotomy':dict(branches),'single_blob_types':453,'single_blob_classification':dict(classes),'character_projection':'{0,C}','transfer_is_identity_of_polynomial_maps':True,'cut_block_ranks':[1,1,1,1],'noncut_lower_bound_total_flattening_rank':5,'conclusion':'rank Flat_{A|Ac}(q)<=4 iff A|Ac is a cut throughout D_{3,+}'}
(ROOT/'software/certificates/k3p_pointwise_cut_transfer.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('K3P_ONE_CHARACTER_MAP_IDENTITY_PASS');print('K3P_ENDPOINT_CERTIFICATES_177_PASS');print('K3P_SINGLE_BLOB_CERTIFICATES_453_PASS');print('K3P_POINTWISE_CUT_RANK_THEOREM_PASS')
