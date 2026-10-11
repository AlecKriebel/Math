"""Close the actually held second whole review after ROOT's proof/output reading."""
from root_submission_gate import *
from root_closed_namespace_tools import verify_historical_namespaces
import re,sys
assert __debug__ and sys.flags.optimize==0
N=A/'preprint_review_02';D=N/'phase3'
assert not (A/'ROOT_PREPRINT02_CLOSURE.json').exists()
assert not (A/'PUBLISHING_CLEARANCE.json').exists()
freeze=load(N/'FULL_REVIEW_FREEZE.json')
assert pin(N/'FULL_REVIEW_FREEZE.json')['sha256']=='ceb2beb03f6cf3e66962acf6ff1e2d0883d621c8400635ef4d4ba0ef111e2449'
assert pin(D/'FINAL_NATIVE_CAPTURE.json')['sha256']=='ec60d1be51c02e8ce4584729499f2cf10f17ed33ca4202c2d90a521446e1648d'
assert freeze['stage']=='whole-preprint-review-complete-held-for-external-ROOT-closure'
assert freeze['only_inventory_exclusions']==['FULL_REVIEW_FREEZE.json','phase3/FINAL_NATIVE_CAPTURE.json']
assert freeze['stable_claim_ids']==74 and freeze['remaining_mathematical_gaps']==0
assert not freeze['candidate_repair_requested'] and not freeze['publication_approval'] and not freeze['self_certification']
before=inventory(N)
def objects(inv):
    rows=[dict(path=n,type='directory',mode_octal=m) for n,m in inv['directory_modes'].items()]
    rows.extend(dict(path=n,type='file',mode_octal=e['mode'],bytes=e['bytes'],sha256=e['sha256']) for n,e in inv['payloads'].items())
    return sorted(rows,key=lambda x:x['path'])
rows=objects(before);exclusions=set(freeze['only_inventory_exclusions'])
assert [x for x in rows if x['path'] not in exclusions]==freeze['objects']
assert len(before['payloads'])==653 and len(before['directory_modes'])==36
canonical=sha((json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode())
assert canonical=='84e1fae82e4ef1111cfe1bc817990ea86153082ce37702034a82cd5ed6771a4d'
def validate_native(expected,out,err):
    assert not err
    if out.startswith(b'.|'):
        found={}
        for line in out.decode().splitlines():
            n,kind,m,size=line.rsplit('|',3);found[n]=(kind,f'{int(m,8):04o}',int(size))
        assert set(found)=={x['path'] for x in expected}
        for x in expected:
            kind,m,size=found[x['path']]
            assert kind==('Directory' if x['type']=='directory' else 'Regular File') and m==x['mode_octal']
            if x['type']=='file':assert size==x['bytes']
    else:
        found={}
        for line in out.decode().splitlines():
            match=re.fullmatch(r'([0-9a-f]{64})  (.*)',line);assert match,line
            assert match[2] not in found;found[match[2]]=match[1]
        assert found=={x['path']:x['sha256'] for x in expected if x['type']=='file'}
capture=load(D/'FINAL_NATIVE_CAPTURE.json')
assert capture['executed_body_sha256_before']==capture['executed_body_sha256_after']==pin(D/'freeze_full_review.py')['sha256']
for key in ['complete_native_file_hash_receipt','complete_native_modes_receipt']:
    rec=capture[key];assert rec['exit_status']==0 and rec['cwd']==str(N)
    assert rec['utc_start']<=rec['utc_end'] and rec['clock_argv']==['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ']
    for k in ['stdout','stderr']:
        raw=rec[k].encode();assert len(raw)==rec[k+'_bytes'] and sha(raw)==rec[k+'_sha256']
    validate_native(freeze['objects'],rec['stdout'].encode(),rec['stderr'].encode())
# The earlier external exposure gates remain dated records. Only the log may append.
for name in ['ROOT_PREPRINT02_SOURCE_GATE.json','ROOT_PREPRINT02_FIRST_CANDIDATE_GATE.json']:
    gate=load(A/name)
    for x in gate['objects']:
        p=N/x['path'];assert not p.is_symlink()
        assert f'{stat.S_IMODE(p.stat().st_mode):04o}'==x['mode_octal']
        if x['type']=='directory':assert p.is_dir()
        else:
            b=p.read_bytes()
            if x['path']=='RESEARCH_LOG.md':b=b[:x['bytes']]
            assert len(b)==x['bytes'] and sha(b)==x['sha256']
family=load(A/'ROOT_PREPRINT02_FAMILIES_GATE.json')
for n,e in family['namespaces'].items():assert inventory(N/'families'/n)==e
ledger=load(D/'CLAIM_STATUS.json');old=[]
for line in (N/'FIRST_CANDIDATE_ASSESSMENT.md').read_text().splitlines():
    if re.match(r'^\| [CSM]\d{3} \|',line):old.append([x.strip() for x in line.split('|')[1:-1]])
assert len(old)==len(ledger['claims'])==74
assert ledger['all_exact_mathematical_gaps_closed'] and not ledger['candidate_repair_requested']
for original,e in zip(old,ledger['claims']):
    assert [e[k] for k in ['id','original_location','original_claim','frozen_first_assessment']]==original
    assert e['exact_mathematical_gap'] is None
    for p in e['evidence']:
        actual=pin(N/p['path']);assert actual['bytes']==p['bytes'] and actual['sha256']==p['sha256']
assert len(re.findall(r'^\| [CSM]\d{3} \|',(D/'CLAIM_STATUS.md').read_text(),re.M))==74
comparison=load(A/'ROOT_PREPRINT02_PACKET_REPLAYS.json')
for e in comparison['comparisons']:
    assert pin(D/e['comparison'])['sha256']==e['reviewer_output_sha256']
    assert e['all_remaining_structured_content_equal']
private=A/'root_preprint_private/preprint02_current_packet_external'
preserve=load(private/'EARLY_STAGE_PRESERVATION.json');prior=load(D/'EARLY_STAGE_PRESERVATION.json')
ignored=['utc_start','utc_end','argv','executed_body_sha256_before','executed_body_sha256_after']
assert {k:v for k,v in preserve.items() if k not in ignored}=={k:v for k,v in prior.items() if k not in ignored}
runtime=load(A/'root_runs_private/preprint02_final_preservation_root001/execution.json')
assert runtime['exit_code']==0 and runtime['stderr_bytes']==0
Q=A/'preprint/qualification_v03';q=load(Q/'QUALIFICATION.json')
assert q['status']=='NATIVELY_QUALIFIED_FOR_FRESH_ADVERSARIAL_REVIEW' and q['input_count']==8
for n,e in q['inputs'].items():assert pin(Q/'inputs'/n)=={k:e[k] for k in ['bytes','sha256','mode']}
mapping=dict(zip(FORMAL,['manuscript.tex','manuscript.pdf','verification.zip','zenodo-deposit.json']))
for n,qn in mapping.items():assert pin(O/n)==pin(Q/'inputs'/qn)
# Root-native external capture includes both unavoidable self-reference exclusions.
cap=Capture('preprint02_whole_external')
hs=cap.run('whole_hashes',['/usr/bin/shasum','-a','256',*before['payloads']],cwd=N)
ms=cap.run('whole_modes',['/usr/bin/stat','-f','%N|%HT|%OLp|%z',*sorted(before['payloads'].keys()|before['directory_modes'].keys())],cwd=N)
validate_native(rows,hs.stdout,hs.stderr);validate_native(rows,ms.stdout,ms.stderr)
assert inventory(N)==before
namespaces,external,limits=verify_historical_namespaces()
namespaces['preprint_review_02']=dict(excluded_roots=[],inventory=before,historical_external_manifest=pin(N/'FULL_REVIEW_FREEZE.json'))
sealed=dict(utc=utc(),status='ALL_CURRENT_SCIENTIFIC_AND_REVIEW_NAMESPACES_EXTERNALLY_BOUND',namespaces=namespaces,external_files=external,historical_boundaries=limits,source_first_stage_boundaries='Parent source-only and first-candidate stages externally bound before respective release. Narrow family early baselines were hash-recorded, without an earlier whole-namespace root-native seal.',current_review02_canonical_inventory_sha256=canonical)
(A/'ROOT_FINAL_CLOSED_EVIDENCE.json').write_text(json.dumps(sealed,indent=2)+'\n')
manifest=dict(utc=utc(),namespace=str(N),inventory=before,canonical_inventory_sha256=canonical,actual_root_native_captures=cap.entries,reviewer_native_capture=pin(D/'FINAL_NATIVE_CAPTURE.json'),reviewer_manifest=pin(N/'FULL_REVIEW_FREEZE.json'),held_namespace_unchanged=True)
(A/'ROOT_PREPRINT02_NAMESPACE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
closure=dict(utc=utc(),status='PASS_ROOT_EXTERNALLY_CLOSED_CLEAN_FULL_PREPRINT_REVIEW',review=2,qualified_candidate='v03',unresolved_findings=0,early_stages_externally_verified=True,complete_independent_outputs_compared=True,held_namespace_unchanged=True,namespace_files=653,namespace_directories=36,stable_claims=74,mathematical_claims=61,source_disclosure_claims=9,metadata_claims=4,root_fresh_family_replays=8,root_current_packet_comparisons=3,root_current_preservation_replay=runtime,complete_preservation_result_equal=True,preservation_metadata_exclusions=ignored,canonical_inventory_sha256=canonical,whole_review=pin(D/'WHOLE_PREPRINT_REVIEW.md'),claim_ledger=pin(D/'CLAIM_STATUS.json'),namespace_manifest=pin(A/'ROOT_PREPRINT02_NAMESPACE_MANIFEST.json'),root_read_scope='Complete held whole report, all74 readable claim closures and original frozen fields; complete two fresh family reports and arithmetic/moduli/source/public reports; all scientific/consistency bodies and current preservation/freezer code; full root eight family outputs, original29 public science/negative/guard/verifier streams and actual failures; full current historical reconstruction and exact structured binding comparisons. Operative primary bytes match previously root-read sources. All held objects/modes externally bound with native hash/stat, without pretending every raw hash row requires semantic mathematical reading.',strongest_verified_result='Entire explicitly normalized regular-pentagon pencil, full25-point normalization kernel and exact arithmetic coordinate field on every allowed fiber, with classical inputs credited.',boundary_counterexample_retained=family['boundary_counterexample'],historical_capture_boundary=comparison['historical_capture_boundary'],first_priority_certified=False,external_human_peer_review=False,mathematical_verification_percent=100,priority_percent=100,workflow_percent=80,merge_pending=True,zenodo_pending=True,tracker_pending=True,persistent_goal_complete=False)
(A/'ROOT_PREPRINT02_CLOSURE.json').write_text(json.dumps(closure,indent=2)+'\n')
immutable=['ROOT_CURRENT_MATHEMATICAL_GATE.json','ROOT_PRIORITY_CLOSURE.json','ROOT_PREPRINT01_CLOSURE.json','ROOT_PREPRINT01_REPAIR_COMPLETION.json','ROOT_PREPRINT02_SOURCE_GATE.json','ROOT_PREPRINT02_FIRST_CANDIDATE_GATE.json','ROOT_PREPRINT02_FAMILIES_GATE.json','ROOT_PREPRINT02_PACKET_REPLAYS.json','ROOT_PREPRINT02_CLOSURE.json','ROOT_PREPRINT02_NAMESPACE_MANIFEST.json','ROOT_FINAL_CLOSED_EVIDENCE.json','preprint/qualification_v03/QUALIFICATION.json','ROOT_PDF_QA006.json']
clear=dict(utc=utc(),status='READY_AFTER_GLOBAL_REPAIR_AND_NEW_FULL_PREPRINT_REVIEW',original_head=ORIGINAL_HEAD,original_status='claimed_solved',final_clean_review=2,unresolved_findings=0,historical_review01_finding_retained=True,first_priority_certified=False,qualified_candidate='v03',formal_submission_files={n:pin(O/n) for n in FORMAL},immutable_root_artifact_pins={n:pin(A/n) for n in immutable},final_review_closure='ROOT_PREPRINT02_CLOSURE.json',mathematical_verification_percent=100,priority_percent=100,workflow_percent=80,merge_pending=True,zenodo_pending=True,tracker_pending=True,persistent_goal_complete=False)
(A/'PUBLISHING_CLEARANCE.json').write_text(json.dumps(clear,indent=2)+'\n')
assert inventory(N)==before;current_clearance()
print(json.dumps({k:closure[k] for k in ['utc','status','namespace_files','namespace_directories','stable_claims','unresolved_findings','qualified_candidate','canonical_inventory_sha256','workflow_percent']},indent=2))
