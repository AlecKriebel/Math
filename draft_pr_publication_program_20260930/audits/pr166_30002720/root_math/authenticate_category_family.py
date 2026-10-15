from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parents[1];F=A/'category_consequence_adversary'
def require(x,msg):
 if not x:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(p.stat().st_mode),'04o'))
def check(p,r):
 x=pin(p);require(x['sha256']==r['sha256'] and x['bytes']==r['size'] and int(x['mode'],8)==int(r['mode'],8),'Identity differs '+str(p));return x
manifest=F/'MANIFEST.json';require(pin(manifest)['sha256']=='78e472150da76fa56088f295631de7f449eebb653ed47a6aec980e55f14abe47','Externally delivered inventory differs')
j=json.loads(manifest.read_text());rows=j['retained_files'];artifacts=[check(Path(r['path']),r) for r in rows]
actual=set()
for p in F.rglob('*'):
 require(not p.is_symlink(),'Unexpected symlink')
 if p.is_file():actual.add(p.relative_to(F).as_posix())
require(actual=={r['relative_path'] for r in rows}|{'MANIFEST.json'} and j['retained_file_count']==len(rows),'Inventory incomplete')
external=[check(Path(r['path']),r) for r in j['external_inputs']];require(len(external)==j['external_input_count'],'External input count')
first=json.loads((F/'FIRST_SEAL.json').read_text());check(Path(first['assessment']['path']),first['assessment'])
first_inputs=[check(Path(r['path']),r) for r in first['inputs']]
require(pin(F/'FIRST_SEAL.json')['mode']==pin(F/'FIRST_ASSESSMENT.md')['mode']=='0444','First assessment unfrozen')
wl=json.loads((F/'PUBLIC_ALLOWLIST.json').read_text());public=[r['relative_path'] for r in wl['allowed_files']]
require(len(set(public))==len(public) and set(public)<=actual and all(not r.startswith(('private_sources/','scratch/')) for r in public),'Private allowlist violation')
auth=dict(UTC=datetime.now(timezone.utc).isoformat(),status='CATEGORY_FAMILY_COMPLETE_INVENTORY_INPUTS_AND_FIRST_SEAL_AUTHENTICATED',manifest=pin(manifest),retained_identities=artifacts,external_inputs=external,first_seal_inputs=first_inputs,first_seal=pin(F/'FIRST_SEAL.json'),public_allowlist=public,private_bodies_excluded=True,no_MAIN_Git_PR_or_publication_action=True)
out=A/'root_math/CATEGORY_FAMILY_AUTHENTICATION.json';out.write_text(json.dumps(auth,indent=2)+'\n')
r=json.loads((F/'RESULT.json').read_text());require(r['verdict']=='VALID_NEWLY_ASSEMBLED_LOGICAL_CONSEQUENCE' and r['remaining_gap_within_claim'] is None,'Universal scientific verdict differs')
gate=dict(UTC=auth['UTC'],PR=166,problem_id=30002720,status='ROOT_CATEGORY_GATE_PASS_NEWLY_ASSEMBLED_RESIDUAL_CONTINUITY_RANK_ALL_CENTER_THEOREM',mathematical_clearance=True,claim=r['claim'],root_read_entire_derivation_review_result_and_analytic_controls=True,artifacts=[pin(F/n) for n in ['DERIVATION.md','REVIEW.md','CONTROL_DERIVATIONS.md','RESULT.json']],authentication=pin(out),mechanisms=r['mechanisms'],essential_rank_cell_transfer=True,relative_local_constancy_alone_insufficient=True,root_independent_reconstruction='Direct simultaneous cost bound is o_P(n); nonroot jump +/-pi(W) dense; fixed-boundary mixture has equal unequal atoms; all-center concentration<=1/2; exact half-open rank-cell equality supplies open failure sets; Baire complement is ambient dense G_delta; universal-center tail bound holds at arbitrarily late indices for every radius.',scope_limits=r['scope_limits'],historical_preemption=False,original_square_rank_membership_proved=False,measure_a_e_claim=False,original_problem_new_first_resolution_clearance=False,publication_clearance=False,MAIN_writer_authority=False,no_new_paper_DOI_tracker=True)
target=A/'ROOT_CATEGORY_GATE.json';target.write_text(json.dumps(gate,indent=2)+'\n')
print(json.dumps(dict(authentication=pin(out),gate=pin(target),retained=len(artifacts),external=len(external),public_files=len(public),status=gate['status']),indent=2))

