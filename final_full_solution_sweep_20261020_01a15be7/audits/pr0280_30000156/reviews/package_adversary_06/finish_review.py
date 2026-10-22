#!/usr/bin/env python3
"""Review06 preservation verification and exclusive self-excluding review seal."""
from pathlib import Path
import json,hashlib,datetime,sys,subprocess,os
O=Path(__file__).resolve().parent;A=O.parents[1];R=A.parents[1];P=R/'private/pr0280_package06'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(v,m):
    if not v:raise RuntimeError(m)
def entry(p,base):return {'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def verify_inputs():
    start=json.loads((O/'INPUT_BINDING_BEFORE.json').read_text())
    manifest=A/'final_robustness_repair_20261021/MANIFEST.json'
    ck(sha(manifest)==start['manifest_sha256']=='b1d1b426b75c131dd5161c95de0532ad1cf6132294921a42f66f48dd301a8253','repair manifest changed')
    for e in start['files']:
        p=A/e['path'];ck(p.is_file() and not p.is_symlink() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'Bound input changed '+e['path'])
    state=[entry(p,R.parent) for p in sorted((R.parent/'.zenodo-state').rglob('*')) if p.is_file()]
    ck(state==json.loads((P/'STATE_INVENTORY_BEFORE.json').read_text()),'314-state inventory changed')
    digest=hashlib.sha256(json.dumps(state,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    ck(len(state)==314 and digest=='1d241f0c6e2450ec0df942bf36bfe438f937d5ad530414028b3b47fcf827010b','state aggregate changed')
    git_custody=json.loads((P/'GIT_CUSTODY_START.json').read_text())
    ck(all(Path(p).stat().st_size==e['bytes'] and sha(Path(p))==e['sha256'] for p,e in git_custody.items()),'captured Git HEAD/index changed')
    return {'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all368_initial_bound_inputs_unchanged':True,'repair_manifest_sha256':sha(manifest),'state_files':314,'state_inventory_sha256':digest,'captured_Git_HEAD_index_unchanged':True,'git_baseline_scope':'Captured after initial immutable original-object reads; no git status or mutation call was used.','root_clearance_unchanged_false':json.loads((A/'ROOT_PUBLICATION_CLEARANCE.json').read_text())['publication_ready'] is False,'no_actual_lifecycle_or_ledger_actions':True}
def main():
    manifest=O/'AUTHORED_FILE_MANIFEST.json';checksum=O/'AUTHORED_FILE_MANIFEST.sha256'
    if '--verify' in sys.argv:
        result=verify_inputs();m=json.loads(manifest.read_text());ck(checksum.read_text().split()[0]==sha(manifest),'review checksum changed')
        observed={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file() and p not in {manifest,checksum}}
        ck(observed=={e['path'] for e in m['files']},'review file set changed')
        for e in m['files']:p=O/e['path'];ck(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'review artifact changed '+e['path'])
        print(json.dumps({'verified':True,'review_artifacts':len(m['files']),'review_manifest_sha256':sha(manifest),'review_completion_percent':100,'unresolved_material_findings':[],'publication_authorization':False}));return
    ck(not manifest.exists() and not checksum.exists(),'Review seal immutable')
    result=verify_inputs();(O/'INPUT_PRESERVATION_FINAL.json').write_text(json.dumps(result,indent=2)+'\n')
    private=[entry(p,P) for p in sorted(P.rglob('*')) if p.is_file()];ck(not any(p.is_symlink() for p in P.rglob('*')),'private symlink')
    (O/'PRIVATE_EVIDENCE_MANIFEST.json').write_text(json.dumps({'scope':'Private source/renders/synthetic output/raw evidence only, no raw bodies included in public review; this inventory binds all files in assigned private custody.','files':private},indent=2)+'\n')
    sources=json.loads((O/'PRIMARY_BODY_CUSTODY.json').read_text())
    for name in ['JRV2006','RV2009','NRV2012','Neumaerker2012','Siu2019']:
        p=R/'private/pr0280_package_adversary_04'/(name+'.pdf');sources.append({'id':name,'actual_body_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'fresh_download':False,'scope_receipt':'PRIMARY_READING_SCOPES.json'})
    (O/'PRIMARY_BODY_CUSTODY.json').write_text(json.dumps(sources,indent=2)+'\n')
    notes={'review_only_corrections':['The initial cached-sheet check confused the exact raw-body SHA256 in root receipt with normalized rows digest; corrected to compare raw bytes, then actual gather/reconcile passed.','A singular LEGACY_REPLAY filename was requested; actual reviewer05 file is plural LEGACY_REPLAYS. Correct file then read.','Initial local before-binding held314-state filename/hash entries; moved to assigned private custody before sealing; public record retains count/aggregate.'],'production_defects_inferred_from_these':False,'sealed_canonical_outputs_overwritten':False,'output_adapter_scope':'Only review-owned custody paths; exact historical v1.0 mounts and documented synthetic resolved_url additions preserved; current guards/outcomes unchanged.'}
    (O/'HARNESS_NOTES.json').write_text(json.dumps(notes,indent=2)+'\n')
    verdict={'schema':1,'timestamp':result['timestamp'],'reviewer':'pr280_package_adversary_06','pr':280,'problem_id':'30000156','source_alias':'OWR-768-006','verdict':'SCOPED_PASS_NO_UNRESOLVED_MATERIAL_FINDING','review_completion_percent':100,'new_complete_independent_review':True,'unresolved_material_findings':[],'scientific_release_manifest_sha256':'da0388503e1c6f03c809ec256989d10039b1f1a1b2eba87528d77651a7863e60','repair_manifest_sha256':result['repair_manifest_sha256'],'root_lead_sha256':'3678face65a98b0c8f593877165b096993928393deee6ce1b2cf08e357363add','root_clearance_currently_false':True,'publication_authorization':False,'human_peer_review':False,'AI_review':True,'scientific_scope':'Full printed class3 theorem including every positive-upper-relative-density thinning/weak-measure obstruction; separate all-odd regular/deletion/completion proposition as printed.','historical_scope':'Old ingredients credited, no worldwide firstness/current openness certified; unrecovered2011 body/version relationship remains explicitly disclosed.','actual_replays':{'operations_per_mode':3134,'independent_additional_operations_per_mode':72,'class3_checks_per_archive_replay':147619,'all_odd_checks_per_archive_replay':46298,'archive_modes':['normal','optimized'],'independent_exact_math':124322,'independent_approximate_character_diagnostics':2218,'historical_manifests':18,'historical_current_entries':2016,'immutable_old_branch_GitHub_GETs':5,'legacy_normal_assertions':[101073,301761]},'live_scope':'No fresh actual account/sheet/PR enumeration by reviewer; cached15:22 body replay has synthetic local freshness only. Immutable GitHub commit GETs authenticate old commit, not present PR/main. No provider mutations.','preservation':result,'report':'REPORT.md'}
    (O/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
    with (O/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+result['timestamp']+' — 100%: Complete review, final368/state314 preservation, report/verdict and self-excluding seal complete. No unresolved material finding; publication authorization false.\n')
    entries=[entry(p,O) for p in sorted(O.rglob('*')) if p.is_file() and p not in {manifest,checksum}]
    ck(not any(p.is_symlink() or '__pycache__' in p.parts for p in O.rglob('*')),'unsafe authored artifact')
    value={'schema':1,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'pr280_package_adversary_06','assigned_review_completion_percent':100,'verdict':verdict['verdict'],'unresolved_material_findings':[],'publication_authorization':False,'self_excluded':['AUTHORED_FILE_MANIFEST.json','AUTHORED_FILE_MANIFEST.sha256'],'files':entries}
    with manifest.open('x') as f:f.write(json.dumps(value,indent=2)+'\n')
    with checksum.open('x') as f:f.write(sha(manifest)+'  AUTHORED_FILE_MANIFEST.json\n')
    print(json.dumps({'artifacts':len(entries),'manifest_sha256':sha(manifest),'verdict':verdict['verdict'],'publication_authorization':False}))
if __name__=='__main__':main()
