"""ROOT's final read-only actual-window gate; no Git/native/service mutation."""
import argparse, datetime, hashlib, importlib.util, json, os, stat, subprocess, sys
from pathlib import Path, PurePosixPath
from capture import capture, reserve_evidence_capacity

if sys.flags.optimize:
    raise RuntimeError('Optimization disables checks')
R = Path('/Users/alec/Documents/Math')
A = R/'draft_pr_publication_program_20260930/audits/pr80_30000177'
F = Path(__file__).parent
parser=argparse.ArgumentParser()
parser.add_argument('--plan',required=True)
arguments=parser.parse_args()
PLAN = Path(arguments.plan).resolve()
assert PLAN.parent==A and PLAN.name.endswith('.json')
ACK = R/'draft_pr_descending_audit_20261002/audits/pr305_5100034/root_during_peer_pause_20261005/ROOT_EXCLUSIVE_PR80_PUBLICATION_INTEGRATION_ACK.json'
STATUS = R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'

def load(p): return json.loads(p.read_bytes())
def pin(p):
    assert p.is_file() and not p.is_symlink() and p.resolve()==p and p.is_relative_to(R)
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for b in iter(lambda:stream.read(1024*1024),b''): h.update(b)
    return {'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':h.hexdigest(),
            'mode':stat.S_IMODE(p.stat().st_mode)}
def utc(): return datetime.datetime.now(datetime.timezone.utc)

plan,ack = load(PLAN),load(ACK)
plan_pin,ack_pin,status_pin = pin(PLAN),pin(ACK),pin(STATUS)
assert plan['ROOT_reviewed_for_execution'] is True and plan['PR']==ack['PR']==80
assert ack['writer_window_granted'] is True and ack['stable_Git_configuration_held'] is True
assert ack['ROOT_plan_sha256']==plan_pin['sha256']
assert ack['covers_phases']==plan['phase_order']==['merge','accept','checkpoint']
assert ack['exact_owned_paths']==plan['exact_owned_paths']
assert ack['token']=='9c9c35b7-756d-4983-aab5-dec348577203'
stamp = datetime.datetime.fromisoformat(ack['UTC'].replace('Z','+00:00'))
assert datetime.datetime.fromisoformat(plan['UTC'])<=stamp<=utc()
assert (utc()-stamp).total_seconds()<=600
held_pin = plan['held_foreign_manifest']
assert pin(R/held_pin['path'])==held_pin and ack['held_foreign_manifest_sha256']==held_pin['sha256']
held = load(R/held_pin['path'])
assert held['coordinator_asserted_known_held_untracked_complete'] is True
assert held['cooperative_control']==status_pin
status = load(STATUS)
assert status['shared_git_writes_paused'] is True
assert status['ascending_pr80_publication_integration_lease_token']==ack['token']
assert ack['starting_main']==held['starting_main']=='83fe73d348b24881989569e5e50d7b19a9458004'
for entry in plan['bound_inputs']:
    assert pin(R/entry['path'])==entry
own = set(plan['exact_owned_paths'])
held_names = {entry['path'] for entry in held['files']}
assert len(own)==len(plan['exact_owned_paths']) and len(held_names)==len(held['files'])
assert not own.intersection(held_names)
for rel in own|held_names:
    p = PurePosixPath(rel)
    assert str(p)==rel and not p.is_absolute() and '..' not in p.parts and '.' not in p.parts
for entry in held['files']:
    assert pin(R/entry['path'])==entry
assert plan['evidence_capacity_policy']['reservation_bytes']==300*1024*1024
assert plan['evidence_capacity_policy']['stream_codec']=='gzip'
capacity = reserve_evidence_capacity(plan['evidence_capacity_policy']['reservation_bytes'])

number = 0
records = []
def run(argv):
    global number
    number += 1
    record,out,err = capture('actual_window_'+str(number),argv,
                            sources=[str(Path(__file__).resolve()),str(PLAN),str(ACK)])
    assert record['exit_code']==0
    records.append(record)
    return out
def git(*args):return run(['git','--no-optional-locks',*args])
assert git('branch','--show-current').strip()==b'main'
assert git('rev-parse','HEAD').decode().strip()==ack['starting_main']
destination = json.loads(run(['/opt/homebrew/bin/python3','-E','-B',str(F/'get_approved_git_endpoint.py')]))
assert destination['URL_rewrite_rules_absent'] is True and destination['credential_free_expected_repository'] is True
assert destination['endpoint']==plan['approved_git_endpoints']['push'] and destination['fetch_endpoint']==plan['approved_git_endpoints']['fetch']
assert git('ls-remote','origin','refs/heads/main').split()[0].decode()==ack['starting_main']
assert git('diff','--cached','--name-only','-z')==b'' and not (R/'.git/MERGE_HEAD').exists()
index,flags = git('ls-files','--stage','-z'),git('ls-files','-v','-z')
for actual,expected in ((index,held['entire_index']),(flags,held['entire_flags'])):
    assert len(actual)==expected['bytes'] and hashlib.sha256(actual).hexdigest()==expected['sha256']
dirty = {p.decode() for p in git('diff','--name-only','-z','HEAD').split(b'\0') if p}
hidden = {p.decode()[2:] for p in flags.split(b'\0')
          if p and (chr(p[0]).islower() or chr(p[0]).upper()=='S')}-own
assert not dirty.intersection(own) and dirty|hidden<=held_names
assert sorted(dirty)==held['ordinary_foreign_dirty_paths'] and sorted(hidden)==held['hidden_flagged_foreign_paths']

# Validate effective endpoints privately; never retain or print raw configuration.
allowed = {b'https://github.com/AlecKriebel/Math.git',b'https://github.com/AlecKriebel/Math',
           b'git@github.com:AlecKriebel/Math.git',b'ssh://git@github.com/AlecKriebel/Math.git'}
origin = []
for purpose,args in [('fetch',['git','remote','get-url','--all','origin']),
                     ('push',['git','remote','get-url','--push','--all','origin'])]:
    p = subprocess.Popen(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    assert p.returncode==0 and len(out.splitlines())==1 and out.strip() in allowed
    origin.append({'purpose':purpose,'actual_PID':p.pid,'exit_code':p.returncode,
                   'one_exact_authorized_credential_free_endpoint':True})
pr = json.loads(run(['/opt/homebrew/bin/gh','pr','view','80','--repo','AlecKriebel/Math',
                     '--json','number,state,isDraft,baseRefName,headRefOid,title,body']))
assert pr['number']==80 and pr['state']=='OPEN' and pr['isDraft'] is True
assert pr['baseRefName']=='main' and pr['headRefOid']==plan['head']
assert pr['title']==plan['submitted_title'] and hashlib.sha256(pr['body'].encode()).hexdigest()==plan['submitted_body_sha256']
spec = importlib.util.spec_from_file_location('native_read_only',F/'native_integrate.py')
native = importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
identity = native.sourcepair()
assert not (R/native.PREFIX).exists()
queue = (R/native.QUEUE).read_bytes()
assert queue==git('show',ack['starting_main']+':'+native.QUEUE)
assert native.row(queue).decode().split('|')[8].strip()=='queued'
assert native.row(queue).decode().split('|')[9].strip()=='0/5'

for p,expected in ((PLAN,plan_pin),(ACK,ack_pin),(STATUS,status_pin),(R/held_pin['path'],held_pin)):
    assert pin(p)==expected
for entry in held['files']:
    assert pin(R/entry['path'])==entry
result = {'UTC':utc().isoformat(),'actual_PID':os.getpid(),
          'status':'ROOT_ACTUAL_EXACT_THREE_PHASE_WINDOW_VERIFIED',
          'ROOT_authorizes_exact_plan':True,'ROOT_verified_known_held_scope':True,
          'plan_sha256':plan_pin['sha256'],'plan':plan_pin,'ACK':ack_pin,
          'held_foreign_manifest':held_pin,'cooperative_control':status_pin,
          'starting_main':ack['starting_main'],'actual_remote_main':ack['starting_main'],
          'entire_index_empty':True,'entire_index_and_flags_match_prepared_baseline':True,
          'ordinary_dirty_count':len(dirty),'hidden_flagged_count':len(hidden),
          'known_held_file_count':len(held_names),'all_held_body_size_mode_checks_pass':True,
          'owned_held_overlap':False,'current_PR_open_draft_base_head_metadata_match':True,
          'origin_repository':'github.com/AlecKriebel/Math','origin_checks':origin,
          'fresh_URL_rewrite_rules_absent':True,'coordinator_holds_stable_Git_configuration':True,
          'operative_approved_git_endpoints':plan['approved_git_endpoints'],
          'actual_evidence_capacity_allocation':capacity,
          'source_identity':identity,'fresh_read_only_child_count':len(records),
          'native_operator_sha256':pin(F/'native_integrate.py')['sha256'],
          'conditional_scope_report_sha256':pin(A/'operational_review_20261004/concrete_plan_review_20261005/REPORT.md')['sha256'],
          'repaired_push_source_report_sha256':pin(A/'operational_review_20261004/push_binding_repair_20261005/rewrite_guard_followup/REPORT.md')['sha256'],
          'native_or_Git_mutation_done':False,'phase_order':['merge','accept','checkpoint'],
          'foreign_assurance_scope':held['assurance_scope'],'original_budget':'1/5',
          'new_central_proof_search_turns':0,'workflow_percent':90,'program_completed':'9/99'}
with (A/'ROOT_ACTUAL_NATIVE_WINDOW_GATE_20261004.json').open('x') as stream:
    stream.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
