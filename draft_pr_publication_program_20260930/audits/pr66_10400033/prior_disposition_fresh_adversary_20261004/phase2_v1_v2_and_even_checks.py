from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib,json
BASE=Path(__file__).resolve().parent
AUDIT=BASE.parent
NAMES={'CURRENT_RESULT.md','CURRENT_PRIORITY_SPECIALIZATION.md','PR_BODY.md','DISPOSITION_PROPOSAL.json'}
packets=[]
for directory,key in [('attributed_prior_result_preparation_20261004','path'),('attributed_prior_result_preparation_v2_20261004','name')]:
 folder=AUDIT/directory;m=json.loads((folder/'MANIFEST.json').read_text());rows=[]
 assert {r[key] for r in m['files']}==NAMES
 for row in m['files']:
  d=(folder/row[key]).read_bytes();assert len(d)==row['bytes'] and hashlib.sha256(d).hexdigest()==row['sha256']
  rows.append({'name':row[key],'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'matches':True})
 packets.append({'directory':directory,'four_exact_pins_match':True,'files':rows})
v1=AUDIT/packets[0]['directory'];v2=AUDIT/packets[1]['directory']
m2=json.loads((v2/'MANIFEST.json').read_text())
assert m2['previous_packet_directory']==str(v1)
assert m2['previous_packet_pins_unchanged']=={r['name']:r['sha256'] for r in packets[0]['files']}
assert m2['immutable_original_head']=='78f4a7fadac0fd24e147a617956cb409eb6a579e'
a=json.loads((v1/'DISPOSITION_PROPOSAL.json').read_text());b=json.loads((v2/'DISPOSITION_PROPOSAL.json').read_text())
assert all(b[k]==v for k,v in a.items())
assert b['even_refinement_prior_ingredient_corollary_verified'] is True
assert b['earlier_explicit_even_formula_located'] is False
assert b['distinct_tournament_mechanism_novelty_established'] is False
rows=[]
for n in range(2,22,2):
 pairs=F(n*(n-2),2)
 prior=F(comb(n,3)+pairs,4)
 candidate=F(n*(n*n-4),24)
 assert prior==candidate and candidate.denominator==1
 rows.append({'n':n,'linked_pair_upper_bound':str(pairs),'prior_ingredient_corollary':str(prior),'candidate_even':str(candidate)})
result={'scope':'complete v1 and v2 pinned prospective packets, plus post-FIRST ROOT-suggested comparative even-valence deduction','packets':packets,'v1_unchanged':True,'v2_disposition_preserves_every_v1_field':True,'v2_new_flags_consistent':True,'actual_v2_created_utc':m2['created_utc'],'v2_disposition_utc_retains_v1_date':b['utc'],'even_formula_exact_arithmetic_n2_to20':rows,'universal_reason':'classical even intersection valence + n even gives every degree <= n-2, m <= n(n-2)/2; source formula1 gives 4|v3| <= binom(n,3)+m; exact symbolic simplification gives n(n^2-4)/24; n=0 separately zero','finite_checks_are_not_universal_proof':True}
(BASE/'PACKET_V1_V2_PIN_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
