"""ROOT records the substantive final decision on fixed PR18 publication inputs."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:]:
    raise RuntimeError('Nonoptimized no-argument execution required')
own = Path(__file__).resolve().parent
a18 = own.parent
program = a18.parents[1]
repo = program.parent
def sha(b):
    return hashlib.sha256(b).hexdigest()
def require(v,msg):
    if not v:
        raise RuntimeError(msg)
repro = json.loads((own/'ROOT_REPRODUCTION.json').read_bytes())
pins = repro['pins']
for name,pin in pins.items():
    require(sha((a18/'preprint_v1'/name).read_bytes()) == pin,'Publication input drift: '+name)
r1path = a18/'preprint_round1_adversary_family/VERDICT.json'
r2path = a18/'preprint_round2_adversary_family/VERDICT.json'
r1 = json.loads(r1path.read_bytes())
r2 = json.loads(r2path.read_bytes())
require(r1['status']=='PASS_BOUNDED_FIXED_PACKAGE_REVIEW' and not r1['unresolved_substantive_findings'], 'First review unresolved')
require(r2['verdict']=='PASS_FRESH_WHOLE_PACKAGE_REVIEW_NO_UNRESOLVED_SUBSTANTIVE_ISSUE' and not r2['unresolved_substantive_issues'] and not r2['new_global_package_changes_required'], 'Second review unresolved')
for name,pin in r1['source_pins'].items():
    require(sha((a18/'preprint_v1'/name).read_bytes())==pin,'First review binding drift')
for name,item in r2['exact_final_inputs'].items():
    require(sha((a18/'preprint_v1'/name).read_bytes())==item['sha256'],'Second review binding drift')
require(sha((a18/'preprint_round2_adversary_family/REPORT.md').read_bytes()) == r2['report']['sha256'],'Second report drift')
manifest = json.loads((own/'zenodo-deposit.json').read_bytes())
require(manifest['metadata']==json.loads((a18/'preprint_v1/zenodo_metadata.json').read_bytes())['metadata'],'Metadata mapping drift')
require(manifest['files']==[{'path':'../preprint_v1/common_tangent_nullness.pdf'},{'path':'../preprint_v1/common_tangents_null_locus_v1.zip'}],'Upload domain drift')
head = '99e403e85d38d92b021198c4a57bbad3cd8775ba'
queue = subprocess.run(['git','show',head+':unsolved_math_prioritization/QUEUE.md'],cwd=repo,capture_output=True,check=True).stdout.decode()
rows = [line for line in queue.splitlines() if line.startswith('|') and len(line.split('|'))>3 and line.split('|')[2].strip().startswith('30001075 /')]
require(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='1/5','Submitted eligibility drift')
utc = dt.datetime.now(dt.timezone.utc).isoformat()
record = {'schema':'root-pr18-final-submission-decision/v1','UTC':utc,'actual_author_pid':os.getpid(),
 'status':'READY_FOR_HUMAN_AUTHORIZED_PRODUCTION_ZENODO_UPLOAD',
 'original_pr':18,'original_head':head,'problem_id':'30001075','submitted_status':'claimed_solved','original_attempts':'1/5',
 'publication_pins':pins,'production_manifest_sha256':sha((own/'zenodo-deposit.json').read_bytes()),
 'first_fresh_review_verdict_sha256':sha(r1path.read_bytes()),'second_NEW_fresh_review_verdict_sha256':sha(r2path.read_bytes()),
 'ROOT_judgment':'Complete universal outer-nullness proof matches literal Conjecture4; all affine dimensions and nonclosed/unbounded inputs are covered; source, PDF, finite controls and intended metadata agree. No unresolved substantive mathematical, source-access or package concern was located.',
 'priority':'Historical open provenance established; complete named2024 article supplies no exact prior resolution or sufficient adapter; negative audit is bounded and no global-first or exhaustive-current-openness certificate is claimed.',
 'source_erratum':'Simon printed60 augmented Jacobian estimate and domain/projection notation slips were independently corrected; correct standard theorem and this application remain sound. See ANALYTIC_SOURCE_NOTE.md; publication bytes unchanged.',
 'proof_not_finite_control_oracle':True,'conjecture3_proved':False,'external_human_peer_review':False,
 'user_authorization':'Persistent human request explicitly authorizes exact Zenodo upload/publication after clean fresh review loop.',
 'workflow_percent':90,'new_central_attempts':0,'deposit_published':False,'assigned_DOI':None,
 'tracker_status':'CLI401 expired/revoked; reconnect question remains pending','native_merge':False}
(own/'ROOT_FINAL_SUBMISSION_DECISION.json').write_text(json.dumps(record,indent=2)+'\n')
entry = '\n## '+utc+' — PR18 final publication decision\n\nBoth fresh whole-package reviews pass on the same fixed PDF/source/archive/metadata bytes, with no unresolved substantive package issue. ROOT independently checked the complete proof and corrected the upstream area-formula proof estimate in the audit notes. The standard theorem and manuscript application remain sound. Bounded priority/source limits and extensive AI/unrefereed disclosure are retained. The exact prepared package is cleared for the human-authorized production Zenodo publication. No deposit, DOI, tracker row or merge is claimed yet. Workflow estimate90%; original1/5 accounting unchanged, new central-attempt credit0.\n'
for p in [a18/'RESEARCH_LOG.md',program/'RESEARCH_LOG.md']:
    with p.open('ab') as f:
        f.write(entry.encode())
print(json.dumps({'decision':'ROOT_FINAL_SUBMISSION_DECISION.json','sha256':sha((own/'ROOT_FINAL_SUBMISSION_DECISION.json').read_bytes()),'UTC':utc,'actual_pid':os.getpid()},indent=2))
