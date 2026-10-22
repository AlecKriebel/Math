#!/usr/bin/env python3
"""Freeze local preservation and execution receipts; no providers or Git calls."""
from pathlib import Path
import datetime as dt,hashlib,json
from controls_support import HERE as H,AUDIT as A,NAMES
E=A.parents[1];REPO=E.parent;O=H/'pre_record_url_binding'
OLD='53aeb70604d4f28f4986cf2e30f5cb90ccd900de7fff96a2d60bb31c03be886f'
LEAD='af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39'

def sha(b):return hashlib.sha256(b).hexdigest()
def entry(root,name):
    p=root/name;b=p.read_bytes()
    if p.is_symlink():raise RuntimeError('Symlink input')
    return {'path':name,'bytes':len(b),'sha256':sha(b)}
def verify(root,entries):
    for e in entries:
        if entry(root,e['path'])!=e:raise RuntimeError('Changed input '+str(root/e['path']))
def write(name,value):(H/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def state(paths):
    values=[[p.relative_to(REPO).as_posix(),p.stat().st_size,sha(p.read_bytes())] for p in sorted(paths)]
    return {'files':len(values),'aggregate_sha256':sha(json.dumps(values,separators=(',',':')).encode())}

def main():
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    old_path='ops_identity_repair_20261021/MANIFEST.json';old=json.loads((O/old_path).read_bytes())
    if sha((A/old_path).read_bytes())!=OLD or (A/old_path).read_bytes()!=(O/old_path).read_bytes():raise RuntimeError('Historical156 seal changed')
    verify(O,old['files']);verify(A,[e for e in old['files'] if e['path'] not in {n+'.py' for n in NAMES}])
    extra=json.loads((H/'SUPPLEMENTAL_PRESERVATION.json').read_bytes())['files'];verify(O,extra);verify(A,extra)
    snapshot=json.loads((A/'SOURCE_SNAPSHOT.json').read_bytes());original=[]
    for f in snapshot['files']:
        b=(A/f['snapshot']).read_bytes()
        if len(b)!=f['bytes'] or sha(b)!=f['sha256'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=f['git_blob']:raise RuntimeError('Original snapshot changed')
        original.append(entry(A,f['snapshot']))
    release=json.loads((A/'preprint/publication/RELEASE_FILES.json').read_bytes());payloads=[]
    for f in release['files']+release['preparation_auxiliary_files']:
        p='preprint/publication/'+f['path'];actual=entry(A,p)
        if actual!={'path':p,'bytes':f['bytes'],'sha256':f['sha256']}:raise RuntimeError('Release changed')
        payloads.append(actual)
    if sha((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes())!=LEAD:raise RuntimeError('Root lead changed')
    review=A/'reviews/package_adversary_03';rman=review/'AUTHORED_FILE_MANIFEST.json'
    if sha(rman.read_bytes())!='e797d9c8580b3dbaf64ca568e1a7516346269f9248eb1fdbeefb0562a06cfbbb':raise RuntimeError('Review03 seal changed')
    review_files=json.loads(rman.read_bytes())['files'];verify(review,review_files)
    statuses=['ROOT_PACKAGE_REVIEW03_ACCEPTANCE.json','ROOT_RECORD_URL_FINDING.json'];bindings=[]
    for n in statuses:
        b=(A/n).read_bytes();json.loads(b);(H/('parent_'+n)).write_bytes(b);bindings.append(entry(A,n))
    write('ROOT_READ_STATUS_BINDING.json',{'timestamp_utc':now,'root_authored_current_status_receipts':bindings,'complete_review03_report_read_bytes':32994,'complete_review03_report_sha256':sha((review/'REPORT.md').read_bytes()),'review03_manifest_sha256':sha(rman.read_bytes()),'all26_review03_artifacts_verified':len(review_files),'root_full_read_claims_are_parent_authored_not_new_live_outcomes':True,'preparer_read_scope':'Complete review03 REPORT, VERDICT, actual novel control program, public route evidence JSON and root receipts; all26 hashes verified. No new public route download or entire account-body read claimed.','publication_ready':False})
    current_state={'flat_json':state((REPO/'.zenodo-state').glob('*.json')),'recursive_all_regular_files':state(p for p in (REPO/'.zenodo-state').rglob('*') if p.is_file())}
    baseline=json.loads((H/'LOCAL_STATE_BASELINE.json').read_bytes())
    if any(current_state[k]!=baseline[k] for k in current_state):raise RuntimeError('Local state inventory changed')
    write('LOCAL_STATE_PRESERVATION.json',{'timestamp_utc':now,**current_state,'unchanged_against_baseline':True,'scope':'241 direct JSON files and314 recursive regular files are separate aggregate scopes; sorted repository-relative path, bytecount, SHA256 triples encoded JSON with compact separators. No path/body list copied.','actual_local_state_mutations':0})
    source=A.parent/'pr0280_30000156';source_manifest=source/'ops_record_url_repair_20261021/MANIFEST.json';data=source_manifest.read_bytes()
    if sha(data)!='b12e7262026d780029a7eeee1fb8d0c8a514c4a2ab382faadebad40a84dba55d':raise RuntimeError('Optional comparison source seal changed')
    source_entries=json.loads(data)['files'];changed=[]
    for e in source_entries:
        try:matches=entry(source,e['path'])==e
        except FileNotFoundError:matches=False
        if not matches:changed.append(e['path'])
    capture=H/'final_comparison_source/ops_record_url_repair_20261021'
    (capture/'MANIFEST.json').write_bytes(data);(capture/'MANIFEST.sha256').write_bytes((source_manifest.parent/'MANIFEST.sha256').read_bytes())
    expected={e['path']:e for e in source_entries};captured=[]
    for p in (H/'final_comparison_source').rglob('*'):
        if not p.is_file():continue
        name=p.relative_to(H/'final_comparison_source').as_posix()
        if name in expected:
            if entry(H/'final_comparison_source',name)!=expected[name]:raise RuntimeError('Comparison copied bytes differ')
            captured.append(expected[name])
    write('FINAL_COMPARISON_SOURCE_FINAL_CHECK.json',{'timestamp_utc':now,'source_manifest_sha256':sha(data),'bound_source_artifacts':len(source_entries),'source_changes_since_initial390verification':changed,'source_unchanged_at_final_check':not changed,'captured_exact_bound_files':captured,'source_files_written':0,'source_seal_and_parser_not_publication_clearance':True,'adoption_scope':'Own proposal built and benchmarked before comparison. Compared full final280 parser/report/four-helper diff read-only; adopted no-model-shortcut ordering in standalone matches; own399 all-cell collector/gate and strict bindings retained. Bounded own route/subresource and bibliography logic remains independently authored.'})
    immutable=original+payloads+[entry(A,n) for n in ['SOURCE_SNAPSHOT.json','preprint/publication/RELEASE_FILES.json','ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',old_path,'ops_identity_repair_20261021/MANIFEST.sha256','publication_operations_preparation/MANIFEST.json','publication_operations_preparation/MANIFEST.sha256',*statuses,'reviews/package_adversary_03/AUTHORED_FILE_MANIFEST.json','reviews/package_adversary_03/AUTHORED_FILE_MANIFEST.sha256']]
    immutable += [{'path':'reviews/package_adversary_03/'+e['path'],'bytes':e['bytes'],'sha256':e['sha256']} for e in review_files]
    write('IMMUTABLE_INPUT_BINDING.json',{'timestamp_utc':now,'files':sorted(immutable,key=lambda e:e['path']),'original11':len(original),'repository_publication_payloads':5,'preparation_notices':3,'root_lead_sha256':LEAD,'historical156_copies_verified':len(old['files']),'historical_current_nonhelper_entries_unchanged':len(old['files'])-7,'supplemental_top_level_files_verified':len(extra),'actual_git_object_read_during_this_repair':False,'git_blob_check_scope':'Frozen original snapshots bytehash and blob-form SHA1 rechecked against frozen source inventory; prior actual parent/head object checks preserved, no new Git command invoked.','publication_ready':False})
    replays=[]
    for mode in ['normal','optimized']:
        source=E/'private/pr0399_record_url_repair'/('final_verified_'+mode)/'REPLAY_READ_ONLY_RECEIPT.json';body=source.read_bytes();result=json.loads(body)
        if result['current_total']!=1651 or result['actual_provider_attempts']!=0:raise RuntimeError('Actual replay receipt differs')
        (H/('READ_ONLY_REPLAY_'+mode+'.json')).write_bytes(body);replays.append({'mode':mode,'private_receipt_sha256':sha(body),'current_total':1651,'historical_counterexamples':79,'cached_rows':176})
    tests=[]
    for mode in ['normal','optimized']:
        own='CURRENT_CONTROLS_OPTIMIZED.json' if mode=='optimized' else 'CURRENT_CONTROLS.json';v=json.loads((H/own).read_bytes())
        prior=json.loads((H/('prior530_canonical_'+mode)/'REPLAY_RECEIPT.json').read_bytes());root=json.loads((H/('ROOT_BENCHMARK_canonical_'+mode+'.json')).read_bytes())
        if v['controls']!=818 or not v['all_controls_passed'] or prior['controls']!=530 or root['positive_outcomes']['silently_missed']:raise RuntimeError('Final controls differ')
        tests.append({'mode':mode,'actual_current_pipeline':818,'previous_regressions':530,'exact_root_benchmark':303,'current_total':1651,'old_failure_replay':72,'old_recognized_rejection_replay':7,'cached_ledger_rows_separate_not_new_controls':176,'provider_attempts':0,'pipeline_receipt':entry(H,own),'previous_receipt':entry(H,'prior530_canonical_'+mode+'/REPLAY_RECEIPT.json'),'root_receipt':entry(H,'ROOT_BENCHMARK_canonical_'+mode+'.json')})
    write('TEST_SUMMARY.json',{'timestamp_utc':now,'helper_bindings':json.loads((H/'CURRENT_HELPER_BINDING.json').read_bytes())['files'],'modes':tests,'read_only_runner_actual_replays':replays,'formal_current_controls_per_mode':1651,'cached_sheet_is_not_fresh_live_gate':True,'actual_provider_attempts':0,'publication_ready':False})
    print(json.dumps({'immutable_inputs':len(immutable),'historical156_preserved':156,'state_unchanged':True,'comparison_source_changed_paths':changed,'current_controls_per_mode':1651,'root_status_bindings':bindings},indent=2))
if __name__=='__main__':main()
