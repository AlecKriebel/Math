"""Copy nominated explicit scientific guards; preserve all historical sources."""
from pathlib import Path
from hashlib import sha256
import json, os
A=Path(__file__).resolve().parent.parent
D=A/'guarded_support_v1'
C=A/'verification_code_adversary_20261008/candidate_guards_original20'
S=A/'verification_code_adversary_20261008/support_checker_hardening_20261008/guarded_candidates'
def put(name, source, expected):
    b=source.read_bytes()
    if sha256(b).hexdigest()!=expected: raise RuntimeError('nominated source pin mismatch: '+name)
    target=D/name; target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f: f.write(b); os.fchmod(f.fileno(),420)
    return {'path':name,'bytes':len(b),'sha256':expected,'mode':420,'nominated_source':str(source.relative_to(A))}
D.mkdir(exist_ok=False)
members=[]
for name,expected in [('author/verify.py','b115b61b69928b9d266a3852ad9c865ef457a7b6b2e6e7a9a312d78a7149cf9c'),('inherited/independent_checks.py','a1ab853a5bc08a55e61e9b19fbf5dcd5bc1d3019122e8ff87c6faf88ddca375f'),('analytic/check_analytic_family.py','7209a6bc74fe5680df5eede6fbb526c6747321b1cff5b06e32db481a01915704'),('geometry/independent_geometry.py','b7309c40750b268df5f852f3000d5d8c2234e0c62702ebc62a0755ee759e2dec')]:
    source={'author/verify.py':C/'verify.py','inherited/independent_checks.py':C/'review/independent_checks.py'}.get(name,S/name)
    members.append(put(name,source,expected))
for name,source,expected in [
    ('author/COUNTEREXAMPLE.md',A/'original_submitted_attempt/COUNTEREXAMPLE.md','5553f899b1098a321fe2164c3ba0d6eed87bc2424dc8021dee50e01fc14dc4ab'),
    ('inherited/author_replay/COUNTEREXAMPLE.md',A/'original_submitted_attempt/COUNTEREXAMPLE.md','5553f899b1098a321fe2164c3ba0d6eed87bc2424dc8021dee50e01fc14dc4ab'),
    ('author/expected_verification.json',A/'original_submitted_attempt/verification.json','fa59d8484cb4ca6d8a411e39d4ed320755932b5f5f69b70eff127dd1a5d80a42'),
    ('inherited/expected_independent_results.json',A/'original_submitted_attempt/review/independent_results.json','a64abe47712fee04c8647643d40246d3858f4244bb4ef1fbceb29ea6227790b9')]:
    members.append(put(name,source,expected))
manifest={'schema':'pr148-guarded-support-sources/v1','original_head':'538fd2584f7dc7375e4eaa91d73daddde3d073cd','original_effort':'1/5','new_central_proof_search_turns':0,'members':members,'historical_original20_modified':False,'mathematics_changed':False,'publication_clearance':False}
(D/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'GUARDED_SUPPORT_COPIED_NOT_PUBLICATION_CLEARANCE','members':len(members),'manifest_sha256':sha256((D/'SOURCE_MANIFEST.json').read_bytes()).hexdigest()}))
