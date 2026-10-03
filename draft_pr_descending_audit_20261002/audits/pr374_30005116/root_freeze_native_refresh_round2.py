"""Repeat the actual-head freeze on the second normal current-main refresh."""
from pathlib import Path
import hashlib,json
A=Path(__file__).resolve().parent
p=json.loads((A/'root_post_native_refresh_round2_api.stdout').read_bytes())
HEAD=p['head']['sha'];MAIN='eb3c6dbe6a1d978e39c30518137264bdc69ec30b';OLD='4afe89d1439e0d0d2a28a55f27709192cd56738e'
assert p['base']['sha']==MAIN and HEAD!=OLD
import subprocess
TREE=subprocess.check_output(['git','rev-parse',HEAD+'^{tree}'],cwd=A.parents[2]).decode().strip()
original=(A/'root_freeze_native_refresh.py').read_text()
adapt=original.replace("I=A/'live_acceptance_inputs'","I=A/'live_acceptance_inputs_round2'")
adapt=adapt.replace("OLD='26df33899c95d860403ab311c568e0328bc87eeb';MAIN='8e04757bff6e5c6c25d2dbf23ce10f736da8c5c8';HEAD='4afe89d1439e0d0d2a28a55f27709192cd56738e';TREE='9b4c96e230fc3aecca24760e6804ea671d559ca4'",f"OLD={OLD!r};MAIN={MAIN!r};HEAD={HEAD!r};TREE={TREE!r}")
adapt=adapt.replace("live_snapshot_manifest.json","live_snapshot_manifest_round2.json").replace("native_refresh_verification.json","native_refresh_verification_round2.json").replace("native_refresh_input_bindings.json","native_refresh_input_bindings_round2.json").replace("live_accepted_pr_body.txt","live_accepted_pr_body_round2.txt").replace("live_merge_body.txt","live_merge_body_round2.txt")
adapt=adapt.replace("First queue-only refreshed head: {OLD}, with parent ceada39994b1cd2c4935709143b53e2f7a581a45. After a persistent stale GitHub test-merge cache, the normal expected-head branch update merged current main {MAIN} into that reviewed head, producing final reviewed head {HEAD}","First queue-only refreshed head: 26df33899c95d860403ab311c568e0328bc87eeb, with parent ceada39994b1cd2c4935709143b53e2f7a581a45. After a persistent stale GitHub test-merge cache, the first normal expected-head update produced intermediate head {OLD}, with parents [26df33899c95d860403ab311c568e0328bc87eeb, 8e04757bff6e5c6c25d2dbf23ce10f736da8c5c8] and tree9b4c96e230fc3aecca24760e6804ea671d559ca4. Concurrent acceptance advanced main and its other queue rows. A second normal expected-head update merged current main {MAIN} into that reviewed head, producing final reviewed head {HEAD}")
code=A/'root_freeze_native_refresh_round2_generated.py';code.write_text(adapt)
assert "FIRST_UNUSED_PLACEHOLDER" not in adapt
record={'original_code_sha256':hashlib.sha256(original.encode()).hexdigest(),'generated_code_sha256':hashlib.sha256(adapt.encode()).hexdigest(),'changes':'Metadata constants and distinct round2 output names; exact initial45-byte, complete-main-map and two-cell queue guards retained. Body distinguishes both historical normal refreshes from final actual stage.','head':HEAD,'main':MAIN,'previous_head':OLD,'tree':TREE}
(A/'root_freeze_native_refresh_round2_recipe.json').write_text(json.dumps(record,indent=2)+'\n')
exec(compile(adapt,str(code),'exec'),{'__file__':str(code)})
