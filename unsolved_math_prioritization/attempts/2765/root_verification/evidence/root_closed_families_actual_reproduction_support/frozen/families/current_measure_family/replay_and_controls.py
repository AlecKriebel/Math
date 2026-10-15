#!/usr/bin/env python3
"""Private exact original replays and real code/prose false-packet controls."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent/'source_snapshot'
PRIVATE = ROOT/'isolated_original'
MUTATIONS = ROOT/'mutations'
OUT = ROOT/'streams'
for path in [PRIVATE,MUTATIONS,OUT]:path.mkdir(exist_ok=True)
def sha(data):return hashlib.sha256(data).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest_file=ROOT.parent/'snapshot_manifest.json'
manifest=json.loads(manifest_file.read_text())
expected_manifest='2c58f3aa5f73920fa62c7103648deee899db3a12f3f48c940576f99eff74dfe2'
assert sha(manifest_file.read_bytes())==expected_manifest
input_rows=[]
for row in manifest['files']:
    path=row['path'];data=(SOURCE/path).read_bytes()
    assert sha(data)==row['sha256'] and len(data)==row['size'],path
    blob=subprocess.check_output(['git','hash-object','--stdin'],input=data,cwd=ROOT).decode().strip()
    assert blob==row['git_blob'],path
    target=PRIVATE/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    input_rows.append({'path':path,'bytes':len(data),'sha256':sha(data),'git_blob':blob})
(ROOT/'replay_inputs.json').write_text(json.dumps({'time_utc':now(),'snapshot_manifest_sha256':expected_manifest,'exact_original_file_count':len(input_rows),'files':input_rows},indent=2)+'\n')
def run(label,script,cwd,expected=None):
    start=now();p=subprocess.run(['/usr/bin/python3',str(script)],cwd=cwd,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(p.stdout);(OUT/(label+'.stderr')).write_bytes(p.stderr)
    row={'label':label,'started_utc':start,'ended_utc':now(),'command':['/usr/bin/python3',str(script)],'cwd':str(cwd),'script_sha256':sha(script.read_bytes()),'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr)}
    if expected is not None:
        packet=expected.read_bytes();row.update({'expected_packet_sha256':sha(packet),'byte_whole_packet_identical':p.stdout==packet,'whole_json_equal':json.loads(p.stdout)==json.loads(packet) if p.returncode==0 else False})
    return row
rows=[]
for label,script,packet in [('original_author',PRIVATE/'verify.py',PRIVATE/'verification.json'),('original_review',PRIVATE/'review/independent_checks.py',PRIVATE/'review/independent_results.json')]:
    r=run(label,script,script.parent,packet);assert r['exit_code']==0 and r['byte_whole_packet_identical'] and r['whole_json_equal'];rows.append(r)
code=(PRIVATE/'verify.py').read_text();prose=(PRIVATE/'RESULTS.md').read_text()
controls=[]
def control_case(label,code_text,prose_text,expect_exit_zero,semantic_rejection):
    case=MUTATIONS/label;case.mkdir(exist_ok=True)
    (case/'verify.py').write_text(code_text);(case/'RESULTS.md').write_text(prose_text)
    r=run(label,case/'verify.py',case,PRIVATE/'verification.json')
    r.update({'mutated_results_sha256':sha((case/'RESULTS.md').read_bytes()),'original_code_hash_matches':sha((case/'verify.py').read_bytes())==sha((PRIVATE/'verify.py').read_bytes()),'original_prose_hash_matches':sha((case/'RESULTS.md').read_bytes())==sha((PRIVATE/'RESULTS.md').read_bytes()),'semantic_or_provenance_rejection':semantic_rejection})
    assert (r['exit_code']==0)==expect_exit_zero,label
    controls.append(r)
control_case('wrong_hyperbolic_trace',code.replace('check((A*B).trace()==6,','check((A*B).trace()==7,'),prose,False,'Original assertion rejects wrong trace; exact AB trace is 6.')
control_case('false_reversal_word',code.replace("reverse=word[::-1]","reverse='aaabbb'"),prose,False,'Original generic polynomial assertion rejects the actual different word; a universal reversal cannot be freely replaced.')
control_case('assertions_bypassed_false_trace',code.replace('assert bool(ok), name','pass').replace('check((A*B).trace()==6,','check((A*B).trace()==7,'),prose,True,'The full expected PASS packet still prints when check assertions are disabled. Script input SHA256 differs and the actual trace claim is false; output-only promotion is invalid.')
controls[-1]['byte_whole_packet_identical_even_with_false_code']=controls[-1]['byte_whole_packet_identical']
assert controls[-1]['byte_whole_packet_identical'] and not controls[-1]['original_code_hash_matches']
prose_cases={
 'false_compactness_atomicity':('\n\nCompactness proves that every member of F_gamma is a finite convex combination of closed-curve currents.\n','Rejected: the actual normalized current slice contains scaled non-atomic Liouville; compactness supplies no finite convex theorem for F_gamma.'),
 'false_ml_converse':('\n\nEquality of intersection against every measured lamination is sufficient for membership in F_gamma.\n','Rejected: Leininger Section 6.3 gives filling closed-curve currents with identical all-ML data but different hyperbolic length functions.'),
 'false_signed_rigidity':('\n\nProposition 2 also holds if signed currents are admitted.\n','Rejected: a nonzero signed difference of length-twin counting currents annihilates all Liouville tests; adding it to m alpha produces a signed nontrivial point of the simple-reference fiber.'),
 'false_complete_only_singleton':('\n\nThe singleton argument applies to all complete hyperbolic metrics on the thrice-punctured topological surface, without finite area.\n','Rejected: complete infinite-area pants with three funnel ends carry three positive variable boundary-core lengths; completeness does not force the cusped singleton family.')}
for label,(addition,rejection) in prose_cases.items():
    control_case(label,code,prose+addition,True,rejection)
    assert controls[-1]['byte_whole_packet_identical'] and controls[-1]['original_code_hash_matches'] and not controls[-1]['original_prose_hash_matches']
summary={'time_utc':now(),'python_version':subprocess.check_output(['/usr/bin/python3','--version']).decode().strip(),'original_replays':rows,'negative_controls':controls,'all_controls_met_expected_behavior':True,'scope':'Two actual original programs, exact original inputs and byte-whole-JSON comparisons. Code/prose mutations really executed; prose false claims leave original computational PASS unchanged because the checker does not read RESULTS.md. The written independent proof and primary hypotheses, not these finite packets, establish the scoped mathematics.'}
(ROOT/'replay_results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'original_replays':rows,'control_labels':[x['label'] for x in controls],'all_controls_met_expected_behavior':True},indent=2))
