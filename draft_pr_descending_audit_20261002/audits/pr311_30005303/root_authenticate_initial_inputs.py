"""Read-only binding of the original target, manifests, source intake and native replays."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess
A = Path(__file__).resolve().parent
R = A.parents[2]
D = A/'root_authentication_private'
D.mkdir(exist_ok=False)
sha = lambda b:hashlib.sha256(b).hexdigest()
utc = lambda:datetime.now(timezone.utc).isoformat()
def require(c,label):
    if not c:
        raise RuntimeError(label)
def run(label,args):
    started = utc()
    q = subprocess.run(args,cwd=R,capture_output=True)
    for k,b in [('stdout',q.stdout),('stderr',q.stderr)]:
        (D/(label+'.'+k)).write_bytes(b)
    e = {'argv':args,'started_utc':started,'ended_utc':utc(),'exit_code':q.returncode,'stdout_bytes':len(q.stdout),
         'stdout_sha256':sha(q.stdout),'stderr_bytes':len(q.stderr),'stderr_sha256':sha(q.stderr)}
    (D/(label+'.json')).write_text(json.dumps(e,indent=2)+'\n')
    require(q.returncode == 0,'Read-only native command failed: '+label)
    return q.stdout
m = json.loads((A/'snapshot_manifest.json').read_bytes())
require(m['pr'] == 311 and len(m['files']) == 30,'Original scope differs')
api = json.loads(run('live_pr',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']))
require(api['state'] == 'open' and api['draft'] and api['head']['sha'] == m['head'],'Live original head changed')
pages = json.loads(run('live_files',['/opt/homebrew/bin/gh','api','--paginate','--slurp','repos/AlecKriebel/Math/pulls/311/files']))
live = {e['filename']:e for page in pages for e in page}
require(set(live) == {e['path'] for e in m['files']},'Live changed paths differ')
for i,e in enumerate(m['files']):
    b = (A/'snapshot'/e['path']).read_bytes()
    require(len(b) == e['bytes'] and sha(b) == e['sha256'],'Snapshot byte pin changed')
    blob = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    require(blob == e['git_blob_sha'] == live[e['path']]['sha'],'API/Git blob differs')
    require(run('object_'+str(i),['/usr/bin/git','show',m['head']+':'+e['path']]) == b,'Git contents differ')
    mode = run('mode_'+str(i),['/usr/bin/git','ls-tree',m['head'],'--',e['path']]).split(b'\t',1)[0].split()
    require(mode == [b'100644',b'blob',blob.encode()],'Original Git mode differs')
T = A/'snapshot'/m['target_prefix']
counts = {}
for name in ['TURN_1_MANIFEST.json','FINAL_PACKET_MANIFEST.json','PUBLICATION_MANIFEST.json','review/REVIEW_MANIFEST.json']:
    j = json.loads((T/name).read_bytes())
    entries = j['files']
    require(isinstance(entries,list),'Manifest schema differs')
    require(len({e['path'] for e in entries}) == len(entries),'Duplicate manifest path')
    for e in entries:
        p = (T/'review'/e['path']) if name.startswith('review/') else T/e['path']
        b = p.read_bytes()
        require(len(b) == e['bytes'] and sha(b) == e['sha256'],'Manifest file differs')
    counts[name] = len(entries)
require(list(counts.values()) == [10,18,28,7],'Bound manifest counts differ')
intake = json.loads((A/'ROOT_SOURCE_INTAKE.json').read_bytes())
require(intake['submitted_source_record_equal_raw'] and not intake['raw_prior_report_key_present'],'Unexpected source/prior status')
source = json.loads((A/'source_inputs_recovery_private/problem_payload.json').read_bytes())
require(source == json.loads((T/'source_record.json').read_bytes()),'Source payload differs')
require(json.loads((A/'source_inputs_recovery_private/prior_research.json').read_bytes()) == {},'Imported report no longer empty')
replays = {}
for label, output, count in [
    ('pr311_author_c4_actual001','checks/turn1_c4_output.json',332),
    ('pr311_author_c6_actual001','checks/turn1_c6_output.json',13520),
    ('pr311_author_closure_actual001','checks/turn2_output.json',550337),
    ('pr311_inherited_review_actual001','review/independent_output.json',89324)]:
    folder = A/'root_runs_private'/label
    e = json.loads((folder/'execution.json').read_bytes())
    b = (folder/'stdout.bin').read_bytes()
    require(e['exit_code'] == 0 and not (folder/'stderr.bin').read_bytes(),'Replay failed')
    require(b == (T/output).read_bytes() and len(b) == e['stdout_bytes'] and sha(b) == e['stdout_sha256'],'Whole actual stdout differs')
    require(json.loads(b)['assertions'] == count,'Replay count differs')
    for p in e['programs']:
        code = Path(p['path']).read_bytes()
        require(len(code) == p['bytes'] and sha(code) == p['sha256'],'Executed program changed')
    replays[label] = e
out = {'utc':utc(),'status':'PASS_PR311_ORIGINAL_GIT_API_MANIFEST_SOURCE_AND_FOUR_NATIVE_REPLAYS',
    'original_head':m['head'],'original_paths':30,'original_target_files':29,'all_original_API_Git_disk_bytes_modes_equal':True,
    'manifest_bound_counts':counts,'source_intake_sha256':sha((A/'ROOT_SOURCE_INTAKE.json').read_bytes()),
    'raw_source_revision':intake['raw_revision'],'raw_problem_report_equal_readonly_database':True,
    'prior_report_absence_authenticated':True,'review_hash':intake['review_hash'],'full_native_replays':replays,
    'total_author_assertions':564189,'inherited_assertions':89324,'root_full_candidate_and_inherited_proofs_code_read':True,
    'primary_visual_pages':[3125,3126,3127],'original_author_turns':'2/5','candidate_mathematical_acceptance':False,
    'priority_acceptance':False,'math_percent':45,'workflow_percent':15,'shared_tracked_writes_paused':True}
(A/'ROOT_INITIAL_INPUT_BINDINGS.json').write_text(json.dumps(out,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+out['utc']+' — Original30 Git/API/disk objects and10/18/28/7 manifests verified; three author full outputs564189 and inherited89324 reproduced byte-identically. All29 target proofs/code/metadata reviewed; finite binary/global-Markov/zeros/signed-factor/isolated conventions preserved. Root finds no gap so far; independent source-first candidate assessments still pending. Math45%, workflow15%; priority/preprint gates not entered, tracked writes paused.\n')
print(json.dumps({'status':out['status'],'original_paths':30,'manifests':counts,'author_assertions':564189,'inherited_assertions':89324,'math_percent':45,'workflow_percent':15},indent=2))
