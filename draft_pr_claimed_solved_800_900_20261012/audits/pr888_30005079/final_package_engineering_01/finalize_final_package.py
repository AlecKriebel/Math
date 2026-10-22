"""Post-execution closed-core readback and safe engineering envelope."""
from pathlib import Path
import datetime,hashlib,json,stat
H=Path(__file__).absolute().parent;A=H.parent;C=A/'candidate'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
tool=(A/'publication_tools_01/portable.py').read_bytes();require(pin(tool)['sha256']=='bcaac73bf1620098e0d24f2a2cb9399613567be6018b99329c0a58b6e0101910','frozen tool')
m={'__name__':'frozen_portable_API','__file__':str(A/'publication_tools_01/portable.py')};exec(compile(tool,m['__file__'],'exec',optimize=0),m)
def readjson(name):return m['strict_json']((H/name).read_bytes())
def main():
    corebytes=(H/'CANDIDATE_CORE_PINS.json').read_bytes();core=m['strict_json'](corebytes);pins=m['rows_map'](core['files']);require(len(pins)==179,'closed core count')
    m['closed_tree'](C,set(pins));blobs={}
    for name,row in pins.items():
        raw=m['read_regular'](m['within'](C,name),row['bytes']);require(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'candidate changed since seal: '+name)
        require(stat.S_IMODE((C/name).lstat().st_mode)==0o644,'non0644 candidate file')
        blobs[name]=raw
    currentpin=pin(blobs['CURRENT_PUBLICATION_MANIFEST.json']);indexpin=pin(blobs['verification/package_index.json'])
    m['current_inputs'](C,currentpin['sha256'])
    runs=[]
    for label in ('DEFAULT_BUILD','CURRENT_NORMAL','CURRENT_OPTIMIZED'):
        envelope=readjson(label+'_EXECUTION_RECEIPT.json');data=readjson(label+'_PUBLIC_STDOUT.json')
        require(envelope['exit_code']==0 and data['status']=='PASS','failed actual final execution')
        r=(data['verification'] if label=='DEFAULT_BUILD' else data['portable'])['replay']
        require(r['status']=='PASS' and r['direct_root_launches']==1 and r['nested_subprocess_count']==6 and r['counts']=={'positive':2,'negative':2,'corrupt':2},'replay count contract')
        require(r['launcher']['root_flags']['optimize']==0 and r['root_compile_optimize']==0 and r['checker_compile_optimize']==0,'root/assertion flags')
        expected=1 if label=='CURRENT_OPTIMIZED' else 0
        require(r['outer_measured_optimize']==expected and all(e['measured_flags']['optimize']==expected for e in r['launcher']['events']),'actual requested/effective flags')
        if label=='DEFAULT_BUILD':require(data['verification']['index_sha256']==indexpin['sha256'] and data['sha256']==pin(blobs['rank-two-fano-verification.zip'])['sha256'],'default build not final ZIP')
        else:require(data['current_manifest_sha256']==currentpin['sha256'],'current run used another sealed core')
        runs.append({'label':label,'requested_outer_flags':envelope['requested_outer_flags'],'actual_outer_optimize':expected,'actual_original_root_flags':r['launcher']['root_flags'],'actual_checker_optimize_values':sorted({e['measured_flags']['optimize'] for e in r['launcher']['events']}),'checker_and_root_compile_optimize':0,'actual_outer_CLI_subprocesses':1,'actual_root_processes':1,'actual_checker_subprocesses':6,'counts':r['counts'],'in_process_patch_controls':3,'raw_stdout':envelope['raw_stdout'],'public_stdout':envelope['public_stdout'],'raw_stderr':envelope['raw_stderr'],'public_stderr':envelope['public_stderr'],'sanitization':envelope['sanitization']})
    source=readjson('SOURCE_ONLY_PUBLIC_STDOUT.json');require(source['status']=='PASS' and len(source['inputs'])==3 and source['archival_code_read'] is False and source['archival_code_executed'] is False and len(source['primary_sources']['pins'])==7,'final source-only evidence')
    independent=readjson('INDEPENDENT_ZIP_REBUILD_RECEIPT.json');require(independent['status']=='PASS' and independent['member_count']==150 and independent['package_index_sha256']==indexpin['sha256'] and independent['sha256']==pin(blobs['rank-two-fano-verification.zip'])['sha256'],'independent final ZIP differs')
    rawind=(H/'INDEPENDENT_ZIP_REBUILD_RECEIPT.json').read_bytes();(H/'private_tmp/independent_final_raw_receipt.json').write_bytes(rawind)
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    final={'timestamp_utc':now,'completion_estimate_percent':100,'status':'FINAL_ASSEMBLY_AND_AUXILIARY_REPLAYS_PASS','scope':'Final candidate assembly/auxiliary evidence only; no mathematical, priority, whole-package CLEAR, human-review, novelty or publication verdict.','candidate_files':179,'portable_ZIP_members':150,'original_source_files':21,'original_source_bytes':98055,'original_effort':'1/5','core_pin_list':pin(corebytes),'current_manifest':currentpin,'portable_index':indexpin,'PDF':pin(blobs['rank-two-fano-note.pdf']),'ZIP':pin(blobs['rank-two-fano-verification.zip']),'TeX':pin(blobs['note.tex']),'metadata':pin(blobs['metadata.json']),'deposit':pin(blobs['zenodo-deposit.json']),'tool':pin(tool),'actual_final_runs':runs,'final_core_replay_totals':{'actual_outer_CLI_processes':3,'actual_original_root_processes':3,'actual_checker_subprocesses':18,'counts':{'positive':6,'negative':6,'corrupt':6},'in_process_patch_controls':9},'count_scope':'Only the three named final-core full-replay pipelines. Separately successful pre-README-clarification build is preserved privately and excluded from these totals; source-only and manual reconstruction are not original-root/checker processes.','source_only':{'actual_outer_CLI_processes':1,'complete_corpora_authenticated_before_extraction':3,'canonical_pair_bytes':source['canonical_pair_bytes'],'canonical_pair_sha256':source['canonical_pair_sha256'],'primary_route_bodies_pinned':7,'archival_code_read':False,'archival_code_executed':False,'not_every_newly_cited_paper':'Li-Li and additional priority sources use the separate priority-ledger pins.'},'independent_final_ZIP_rebuild':independent,'independent_receipt_raw_private_pin':pin(rawind),'independent_receipt_public_pin':pin(rawind),'post_replay_closed_core_unchanged':True,'all_candidate_files_regular0644_nonsymlink_no_extras':True,'four_authorized_outer_original_changes':['README.md','RESEARCH_LOG.md','PUBLICATION.md','LITERATURE_AND_SCOPE.md'],'all21_originals_inside_verification_source_unchanged':True,'actual_final_assembly_failed_CLI_runs':0,'historical_failure_preserved':'format_review_01/safe/ACTUAL_CLI_RECEIPTS.json retains its hostile-environment replay ENOSPC failure; no synthetic PASS or whole-package clearance is inferred.','all_scratch_under_final_engineering_private_tmp':True,'no_self_changing_receipts_inside_final_ZIP':True,'runtime_limitations':['Selected CPython/stdlib trusted and unpinned; no OS sandbox or adversarial concurrent-filesystem guarantee.','Same-runtime compressed-byte identity only.','Tool authenticates PDF and checks its prefix; parent separately rendered and visually inspected all5pages.','Historical reports/fixture receipts remain dated snapshots, and some audit scripts require private fixtures.'],'mutations_outside_new_candidate_and_final_engineering':'NONE','Git_PR_queue_remote_DOI_deposit_mutations':'NONE','outside_individuals_contacted':False}
    final['failed_portable_tool_CLI_runs']=final.pop('actual_final_assembly_failed_CLI_runs')
    final['failed_engineering_helper_attempts']=1
    final['finalization_incident']=readjson('FINALIZATION_INCIDENT.json')
    (H/'FINAL_PACKAGE_ENGINEERING_RECEIPT.json').write_text(json.dumps(final,indent=2,sort_keys=True)+'\n')
    log=H/'RESEARCH_LOG.md';log.write_text(log.read_text()+'\n- '+now+' — Final post-replay closed179file core readback passed; all regular0644/non-symlink files and directory inventory unchanged. Explicit safe engineering envelope and external pins prepared outside candidate. Completion estimate100% for assigned assembly and auxiliary checks only; parent whole-package review/publication work remains separate.\n')
    public=['PACKAGE_README.md','assemble_candidate.py','run_final_cli.py','apply_readme_clarification.py','prepare_independent_final_helper.py','independent_zip_rebuild_final.py','seal_candidate.py','repair_outer_current_guides.py','finalize_final_package.py','ASSEMBLY_INPUT_AUTHENTICATION.json','README_CLARIFICATION_RECEIPT.json','INDEPENDENT_HELPER_SCOPE_DELTA.json','SEALED_CANDIDATE_RECEIPT.json','OUTER_CURRENT_GUIDE_REPAIR_RECEIPT.json','CANDIDATE_CORE_PINS.json','INDEPENDENT_ZIP_REBUILD_RECEIPT.json','FINAL_PACKAGE_ENGINEERING_RECEIPT.json','RESEARCH_LOG.md']
    public.append('FINALIZATION_INCIDENT.json')
    for label in ('DEFAULT_BUILD','CURRENT_NORMAL','CURRENT_OPTIMIZED','SOURCE_ONLY'):
        public.extend([label+'_EXECUTION_RECEIPT.json',label+'_PUBLIC_STDOUT.json',label+'_PUBLIC_STDERR.txt'])
    # These markers are scanned, never written into public receipts as values.
    forbidden=[str(A).encode(),str(A.resolve()).encode(),bytes([47])+b'Users'+bytes([47])+b'alec'+bytes([47]),b'/' + b'var' + b'/' + b'folders' + b'/',b'/' + b'private' + b'/' + b'var' + b'/' + b'folders' + b'/']
    for name in public:
        raw=(H/name).read_bytes();require(not any(t in raw for t in forbidden),'private path in safe engineering file: '+name)
    privacy={'timestamp_utc':now,'completion_estimate_percent':100,'status':'PASS','scan_scope':'Explicit safe engineering files only; candidate closed inventory independently reauthenticated.','personal_absolute_prefix_disclosures':0,'published_raw_private_traces':0,'published_private_bodies_wheels_runtimes_fixtures':0,'engineering_receipts_in_final_ZIP':False,'safe_files_before_this_receipt':len(public),'manifest_and_external_pin_receipt_deliberately_self_excluded':True}
    (H/'PRIVACY_AND_PAYLOAD_CHECK.json').write_text(json.dumps(privacy,indent=2,sort_keys=True)+'\n');public.append('PRIVACY_AND_PAYLOAD_CHECK.json')
    envelope={'schema':'rank-two-fano-30005079-final-engineering-safe-v1','problem_id':'30005079','self_excluded':True,'external_pin_required':True,'scope':'Final assembly engineering artifacts only; outside the sealed candidate and final ZIP.','files':[{'path':n,**pin((H/n).read_bytes())} for n in sorted(public)]}
    eraw=(json.dumps(envelope,indent=2,sort_keys=True)+'\n').encode();(H/'SAFE_PAYLOAD_MANIFEST.json').write_bytes(eraw)
    external={'timestamp_utc':now,'schema':'rank-two-fano-30005079-final-engineering-external-pins-v1','safe_manifest':pin(eraw),'safe_payload_files':len(public),'core_pin_list':pin(corebytes),'candidate_manifest':currentpin,'portable_index':indexpin,'PDF':final['PDF'],'ZIP':final['ZIP'],'tool':final['tool'],'scope':'Separate delivery pins; this record and safe manifest are outside the safe payload manifest to avoid self-reference.'}
    (H/'EXTERNAL_PINS.json').write_text(json.dumps(external,indent=2,sort_keys=True)+'\n')
    print(json.dumps(external,indent=2,sort_keys=True))
if __name__=='__main__':main()
