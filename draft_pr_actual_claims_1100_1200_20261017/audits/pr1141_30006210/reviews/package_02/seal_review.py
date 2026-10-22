#!/usr/bin/env python3
"""Finish custody and seal this reviewer folder without circular self hashes."""
from pathlib import Path
import datetime,hashlib,json,sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
def require(c,m):
    if not c:raise RuntimeError(m)
def fp(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    start=json.loads((HERE/'START_CUSTODY.json').read_text())
    end=[fp(Path(r['path'])) for r in start['files']]
    require([{k:v for k,v in x.items() if k!='purpose'} for x in start['files']]==end,'six frozen release files changed')
    (HERE/'END_CUSTODY.json').write_text(json.dumps({'utc':now,'all_six_unchanged':True,'files':end},indent=2)+'\n')
    ledger=json.loads((HERE/'READ_LEDGER.json').read_text());by={}
    for row in ledger:
        path=row['path'];key=(path,row['bytes'],row['sha256'])
        item=by.setdefault(key,{'path':path,'bytes':row['bytes'],'sha256':row['sha256'],'first_read_utc':row['utc'],'last_read_utc':row['utc'],'read_events':0,'purposes':[]})
        item['last_read_utc']=row['utc'];item['read_events']+=1
        if row['purpose'] not in item['purposes']:item['purposes'].append(row['purpose'])
    for row in by.values():
        current=fp(Path(row['path']))
        require(current['bytes']==row['bytes'] and current['sha256']==row['sha256'],'recorded read input changed '+row['path'])
    (HERE/'INPUT_END_AUTHENTICATION.json').write_text(json.dumps({'utc':now,'all_recorded_read_inputs_still_match':True,'distinct_path_content_records':len(by),'read_events':len(ledger),'files':list(by.values())},indent=2)+'\n')
    with (HERE/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+now+' — 100%: Complete bounded whole-publication-package review, CLEAN_PASS with no required operative fixes. All six frozen release files and every recorded input remain unchanged. Independent source core, complete authored packet review, eight offline baselines/40 failures, byte-identical disposable rebuild, all-page image correspondence, final fresh controls/counterfactual limitations and late prior-verdict exposure are fully disclosed. Final external receipt seal follows; historical novelty remains uncertified.\n')
    authored=[];caches=[]
    for p in sorted(HERE.rglob('*')):
        if not p.is_file():continue
        if '__pycache__' in p.parts:caches.append(str(p));continue
        if p in [HERE/'RECEIPT.json',HERE/'RECEIPT.sha256']:continue
        authored.append(fp(p))
    receipt={'schema':'fresh-whole-publication-package-review-02-v1','sealed_utc':now,'verdict':'CLEAN_PASS','required_global_operative_fixes':[],'completion_percent':100,'exact_target':'Nonzero real degree<=d multilinear functions on independent uniform signs, full Fourier squared norm including constant: disjointness => max relative influence>=1/(1024*d^8); <=1/(4096*d^8) suffices for common nonzero vertex.','mathematical_gap':'None found for exact target.','priority_limit':'Bounded negative source search; no novelty/firstness/global-openness certificate. Full ePrint2022/218 and2023/570 inaccessible.','independence':{'route_constants_known_from_assignment':True,'independent_primary_core_utc':'2026-10-17T23:03:10.652577+00:00','prior_reports_read_only_after_core':True,'package_01_folder_read':False,'late_root_previous_verdict_exposure_utc':'2026-10-17T23:07:24.210470+00:00','late_exposed_record':{'path':str(BASE/'root_reproduction/PACKAGE01_REVIEW_AUTH.json'),'bytes':1931,'sha256':'56760332d3ea39f6b11b79c39721712f2eecfd92f49a2666bbf98b935bd11982'},'exposure_scope':'Prior CLEAN_PASS/counts through non-allowlisted root authentication record; also new PACKAGE_ROOT_* records. Independent core, mathematical/paper/report/code review, own144-case baselines, eight/forty replay and exact rebuild preceded this exposure. Parent promptly informed; no earlier verdict used as evidence. No complete information-isolation claim through completion.','prior_verdict_used_as_evidence':False},'execution_summary':json.loads((HERE/'EXECUTION_SUMMARY.json').read_text()),'packet_authentication_summary':json.loads((HERE/'PACKET_AUTHENTICATION.json').read_text()),'six_release_files_start':start,'six_release_files_end':end,'nonself_and_custody_input_records':list(by.values()),'all_recorded_input_fingerprints_reauthenticated_at_end':True,'authored_artifacts_including_private_execution_evidence':authored,'excluded_generated_bytecode_caches':caches,'actions':{'writes_confined_to_review_folder':True,'git_read_only_cat_file_and_check_ignore':True,'git_index_refs_branch_mutations':False,'pr_zenodo_tracker_release_mutations':False,'external_individual_contact_or_outreach_preparation':False,'additional_agents_spawned':False},'receipt_policy':'This receipt and its external SHA256 sidecar are excluded from authored membership to avoid circularity. All other current reviewer artifacts, including log, read ledger, report, source code, results, private web returns and disposable extraction evidence, are pinned. Receipt SHA256 is delivered externally to parent.'}
    data=(json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode();p=HERE/'RECEIPT.json';p.write_bytes(data)
    sha=hashlib.sha256(data).hexdigest();(HERE/'RECEIPT.sha256').write_text(sha+'  RECEIPT.json\n')
    print(json.dumps({'verdict':'CLEAN_PASS','receipt_bytes':len(data),'receipt_sha256':sha,'authored_artifacts':len(authored),'distinct_read_path_content_records':len(by),'read_events':len(ledger),'all_six_unchanged':True},indent=2))

if __name__=='__main__':main()
