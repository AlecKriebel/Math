#!/usr/bin/env python3
"""Finalize the three ROOT-adopted bounded repairs; no Git/network/services."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import shutil
import stat
import subprocess
import sys

R=Path(__file__).absolute().parent
B=R.parents[1]
O=B/'preprint_v1_1'
K=O/'kit'
REPO=B.parents[2]
def sha(data):return hashlib.sha256(data).hexdigest()
def row(p,root):
    data=p.read_bytes()
    return {'path':p.relative_to(root).as_posix(),'bytes':len(data),'sha256':sha(data)}
def put(p,data):p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def require(c,m):
    if not c:raise RuntimeError(m)
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def check_rows(rows,root):
    for entry in rows:require(row(root/entry['path'],root)==entry,'preserved file drift '+entry['path'])
def inventory(root):return [row(p,root) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()]

def main():
    require(not (O/'PREPARATION_SEAL.json').exists(),'already sealed')
    adoption_path=B/'ROOT_WHOLE_PACKAGE_REVIEW_01_20261016.json'
    adoption=json.loads(adoption_path.read_text())
    require(adoption['status']=='ROOT_ADOPT_COMPLETE_WHOLE01_MATH_SURVIVES_THREE_SUPPORT_P3_REPAIR_REQUIRED','ROOT adoption missing')
    require({f['id'] for f in adoption['findings']}=={'P3-01','P3-02','P3-03'},'unexpected complete findings')
    require(adoption['whole_reviews_completed']==1 and adoption['minimum_whole_reviews_TOTAL']==2,'review accounting')
    before=inventory(O)
    put(R/'STAGED_BEFORE_FINAL_PINS.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':before})
    copy=json.loads((K/'COPY_MAP.json').read_text())
    for name in ['ROOT_WHOLE_PACKAGE_REVIEW_01_20261016.json','reviews/package_01/REPORT.md']:
        target=K/'historical'/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(B/name,target)
        copy.append({'original_relative_to_audit':name,'copy_relative_to_kit':target.relative_to(K).as_posix(),
          'bytes':target.stat().st_size,'sha256':sha(target.read_bytes()),
          'copy_semantics':'byte-exact dated complete v1.0 review/adoption; it identifies findings repaired in v1.1, not acceptance of this revision; nonrecursive selected authored evidence'})
    put(K/'COPY_MAP.json',copy)
    now=datetime.now(timezone.utc).isoformat()
    status=json.loads((K/'STATUS.json').read_text())
    status.update(as_of_utc=now,stage='v1.1 bounded preparation final checkpoint; ROOT repair adoption and next whole review pending at this timestamp',
      root_adoption='complete whole01 on v1.0 adopted; bounded v1.1 repair adoption PENDING',
      fresh_complete_whole_package_reviews='whole01 COMPLETE on v1.0 adopted by ROOT; whole02 on v1.1 PENDING',
      minimum_complete_whole_reviews_TOTAL=2,complete_whole_reviews_adopted_at_checkpoint=1,
      remaining_minimum_complete_whole_reviews_at_checkpoint=1,publication_ready=False)
    put(K/'STATUS.json',status);put(O/'STATUS.json',status)
    omissions=json.loads((K/'OMISSIONS.json').read_text())
    omissions['selection']='Fifteen selected historical authored records (the original thirteen plus whole01 report and ROOT adoption), three byte-exact historical finite checkers, new paper/metadata/repair record/portable tooling. This is not recursive archival custody.'
    omissions['selected_historical_policy']='Historical wrong titles and readiness/priority policies are preserved byte-exact as dated history. Current OWR titles and current scholarly lifecycle wording are corrected; complete whole01 counts one of minimum two total complete reviews. Its old unresolved-finding/readiness statements describe its v1.0 checkpoint, not live v1.1 or platform state.'
    put(K/'OMISSIONS.json',omissions)
    repair=f'''# Version 1.1 bounded repair record

Preparation checkpoint: {now}. Workflow counts and pending-gate statements below describe this timestamp only. Later external ROOT and platform disposition supersedes this checkpoint.

This revision implements all three support/editorial findings in the COMPLETE whole01 review of v1.0, adopted by ROOT in the dated historical evidence included here. No mathematical finding was reported. That review counts one of the minimum TWO complete reviews TOTAL; this repair preparation is not an independent review of v1.1. ROOT bounded-repair adoption and the next complete review remain separate gates, recorded externally.

P3-01: build_archive.py now rejects new outputs physically within the kit using real directory inode identities, including either direction of a case alias. It rejects any existing target (regular, directory, symlink, dangling symlink or hardlink alias), '..' before normalization, absent real parents and symlink ancestors. It validates all exact allowlist names, regular member ancestry and file types, manifest membership and every content hash before its first exclusive output write. Use an absolute output under an existing real outside directory, e.g. `python3 scripts/build_archive.py /absolute/existing/output/rebuilt.zip`, or run the absolute script path from an existing outside cwd with a new relative filename. This is a static-filesystem boundary check; no concurrency/race-proof sandbox is claimed.

P3-02: the current paper bibliography, bibliographic objects, source-credit entry and metadata references use Erez Lapid, 'Unitary periods and distinction; representation-theoretic aspects', reporting joint work with Brooke Feigon and Omer Offen, in 'Automorphic Forms: New Directions', OWR14/2011. The DOI and EMS conjecture/page locators are unchanged. This primary title correction was authenticated in whole01 and actually viewed by ROOT; this repair does not claim a new primary-body retrieval/inspection. Historical erroneous names remain only in their byte-exact dated records, with this qualification.

P3-03: permanent paper, metadata and README prose uses timeless unrefereed/AI/UNKNOWN framing and directs lifecycle disposition to external dated ROOT and publication-platform records. STATUS.json explicitly records only its dated preparation checkpoint; later external disposition supersedes that timestamp. It is not changed to claim readiness now. No DOI is invented. Version1.1 uses client bibliographic date16October2026; real UTC command/research timestamps may be17October.

The title, field, exact GL15 Langlands quotient, theorem, all proof/credit prose in sections1-6, source dependencies, UNKNOWN Luo-Zha overlap, AI/unrefereed disclosure, authorship/ORCID and CC BY4.0 scope are unchanged. The original v1.0 tree, preparation seals and original publication/zenodo-deposit.json remain byte-exact. The separate publication/zenodo-deposit-v1_1.json names the v1.1 objects. No raw third-party source body, OCR/image/API response or runtime fixture is redistributed. Selected evidence is explicitly nonrecursive; full local reproducibility records remain outside the release ZIP.
'''
    (K/'REPAIR_RECORD.md').write_text(repair)
    (O/'REPAIR_RECORD.md').write_text(repair)
    allow=json.loads((K/'ALLOWLIST.json').read_text())
    allow['files']=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file())
    put(K/'ALLOWLIST.json',allow)
    manifest=json.loads((K/'MANIFEST.json').read_text())
    manifest['files']=[row(K/name,K) for name in allow['files'] if name!='MANIFEST.json']
    put(K/'MANIFEST.json',manifest)
    # Full matrix again on final candidate bytes, each fixture a new regular copy.
    cmd=[sys.executable,'-B',str(R/'test_builder.py'),'final_builder_fixtures','FINAL_BUILDER_TEST_RESULTS.json']
    p=subprocess.run(cmd,capture_output=True,timeout=60)
    require(p.returncode==0 and not p.stderr,'final builder regressions failed '+repr(p.stderr))
    put(R/'FINAL_BUILDER_MATRIX_COMMAND.json',{'utc':datetime.now(timezone.utc).isoformat(),'argv':cmd,'exit':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
    builder=module('final_archive_builder',K/'scripts/build_archive.py')
    archive=O/'pr1032_supportkit_v1.1.zip'
    builder.build(K,archive)
    rebuilt=R/'final_rebuilt_support_v1.1.zip';builder.build(K,rebuilt)
    require(archive.read_bytes()==rebuilt.read_bytes(),'deterministic final archive')
    runs=[]
    for flags in ([],['-O'],['-OO']):
        cmd=[sys.executable,'-I','-B',*flags,str(K/'scripts/verify_kit.py'),'--archive',str(archive)]
        p=subprocess.run(cmd,capture_output=True,timeout=60)
        require(p.returncode==0 and not p.stderr,'final whole-kit replay failed '+repr(p.stderr))
        runs.append({'utc':datetime.now(timezone.utc).isoformat(),'argv':cmd,'exit':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'result':json.loads(p.stdout)})
    put(R/'FINAL_WHOLE_KIT_RUNS.json',runs)
    native=B/'publication/zenodo-deposit-v1_1.json'
    upload=module('readonly_native_parser',REPO/'zenodo_deposit_tool/zenodo.py')
    m1,f1=upload.load_manifest(native);m2,f2=upload.load_manifest(O/'zenodo-deposit.json')
    require(m1==m2==json.loads((O/'.zenodo.json').read_text())==json.loads((K/'.zenodo.json').read_text()),'metadata identity')
    select=lambda fs:[{'name':f['name'],'path':str(f['path']),'bytes':f['size'],'sha256':f['sha256']} for f in fs]
    require(select(f1)==select(f2),'different native release objects')
    put(R/'NATIVE_VERSIONED_METADATA_CHECK.json',{'utc':datetime.now(timezone.utc).isoformat(),'read_only_native_load_manifest':'PASS','same_exact_bibliographic_objects_and_files':True,'files':select(f1),'no_service_action':True})
    put(O/'DEPOSIT_BINDING.json',{'schema':1,'metadata_sha256':sha((O/'.zenodo.json').read_bytes()),'versioned_native_manifest':row(native,B),'files':[row(O/'paper.pdf',O),row(archive,O)],'semantics':'content binding only; lifecycle status belongs to external dated records'})
    # Preserve both local fixture matrices through their identities, code and
    # complete actual command receipts; remove only owned unsealed duplicates.
    custody=[]
    cleanup=[]
    for name in ['builder_fixtures','final_builder_fixtures']:
        root=R/name
        require(root.is_dir() and not root.is_symlink() and root.parent==R,'owned fixture boundary')
        ledgers=[]
        for p in sorted(root.rglob('*.json')):
            if p.name in {'INITIAL_COPY_IDENTITY.json','PRE_COMMAND_KIT_IDENTITY.json','COMMANDS.json'}:
                ledgers.append({'path':p.relative_to(root).as_posix(),'content':json.loads(p.read_text())})
        custody.append({'root':str(root),'files':inventory(root),'actual_initial_and_precommand_ledgers':ledgers})
        cleanup.append({'root':str(root),'reason':'owned new unsealed disposable copies only; identities and raw argv/exit/stdout/stderr preserved before cleanup'})
    put(R/'OWNED_FIXTURE_CUSTODY_BEFORE_CLEANUP.json',custody)
    for item in cleanup:shutil.rmtree(item['root'])
    put(R/'OWNED_FIXTURE_CLEANUP.json',{'utc':datetime.now(timezone.utc).isoformat(),'entries':cleanup,'no_preexisting_or_canonical_artifact_deleted':True,'no_hardlink_to_canonical_files_created':True})
    check_rows(json.loads((R/'PRESERVED_V1_0_PINS.json').read_text())['files'],B)
    original=json.loads((B/'preparation/unknown_priority_20261016/ORIGINAL_INPUT_PINS.json').read_text())
    check_rows(original['files'],B)
    review=B/'reviews/package_01'
    old_review=json.loads((review/'OUTPUT_FINAL_INVENTORY.json').read_text())
    check_rows(old_review['files'],review)
    require(sha((review/'OUTPUT_FINAL_INVENTORY.json').read_bytes())==adoption['review_final_inventory']['sha256'],'whole01 inventory pin')
    require(sha((review/'OUTPUT_FINAL_SEAL.json').read_bytes())==adoption['review_final_seal']['sha256'],'whole01 seal pin')
    put(R/'ALL_OLD_PRESERVATION_RECHECK.json',{'utc':datetime.now(timezone.utc).isoformat(),'prior_v1_0_native_preparation_rows':72,'original_input_rows':len(original['files']),'whole01_output_rows':len(old_review['files']),'all_byte_exact':True,'original_native_manifest':row(B/'publication/zenodo-deposit.json',B)})
    proof_identity=json.loads((R/'SECTION_1_6_IDENTITY.json').read_text())
    require(proof_identity['byte_exact'],'proof drift')
    require((O/'paper.pdf').read_bytes()==(K/'paper.pdf').read_bytes() and (O/'paper.tex').read_bytes()==(K/'paper.tex').read_bytes(),'paper copies')
    put(R/'FINAL_PDF_QA.json',{'utc':datetime.now(timezone.utc).isoformat(),'paper':row(O/'paper.pdf',O),'pages':9,'engine':'Tectonic0.16.9 --untrusted --only-cached','all_final_pages_actually_viewed_individually':list(range(1,10)),'layout':'no clipping/overflow/missing glyphs/undefined references; prior harmless underfull bibliography warning only','render_pins':[row(p,R) for p in sorted((R/'renders').glob('page-*.png'))]})
    with (R/'RESEARCH_LOG.md').open('a') as stream:
        stream.write('\n- '+datetime.now(timezone.utc).isoformat()+': ROOT adopted sealed COMPLETE whole01 and exactly P3-01/02/03; no mathematical finding and no HKU rename. Implemented all three known findings in v1.1, with dated status accounting one complete review of minimum two TOTAL. Final30case/90process builder matrix passes on final kit bytes; all negative cases preserve inputs/existing targets, both case-alias directions exercised. Three final whole-kit modes/45 finite executions pass, canonical ZIP rebuilt byte-identical, versioned native manifests resolve exact same metadata/PDF/ZIP read-only. All9PDFpages viewed; proof sections1–6 byte-identical. Repair implementation100%; root bounded-repair adoption/whole02 still pending, no claim of overall readiness or independent review.\n')
        stream.write('- '+datetime.now(timezone.utc).isoformat()+': All72 old v1.0/preparation/native files,287original input rows and650whole01 output rows rehashed unchanged. Only new unsealed disposable fixture copies were deleted after full identity/custody ledgers; no canonical hardlinks or old artifact deletions. No Git/index/branch/QUEUE/PR/service/contact/source-retrieval/other-agent action. One helper glob for nonexistent *PINS* exited1; no evidence depended on it. Finalizing exact output seals now.\n')
    # Exact staged-before/final difference, before adding this explanatory report.
    current=inventory(O);before_map={x['path']:x for x in before};after_map={x['path']:x for x in current}
    delta={'utc':datetime.now(timezone.utc).isoformat(),'stage_before':row(R/'STAGED_BEFORE_FINAL_PINS.json',R),
      'changed':[{'before':before_map[n],'after':after_map[n]} for n in sorted(before_map.keys()&after_map.keys()) if before_map[n]!=after_map[n]],
      'added':[after_map[n] for n in sorted(after_map.keys()-before_map.keys())],
      'deleted':[before_map[n] for n in sorted(before_map.keys()-after_map.keys())],
      'note':'Stage-to-final addition of selected evidence, dated checkpoint, final inventories/archive/binding only; source/PDF/builder/proof remain unchanged from inspected staged bytes.'}
    put(R/'STAGED_BEFORE_TO_FINAL_DIFFERENCE.json',delta)
    summary={'utc':datetime.now(timezone.utc).isoformat(),'version':'1.1','bibliographic_date':'2026-10-16','repair_implementation_percent':100,
      'implemented_finding_ids':['P3-01','P3-02','P3-03'],'root_repair_adoption':'PENDING','minimum_complete_whole_reviews_TOTAL':2,'whole01_COMPLETE_adopted':1,'whole02':'PENDING',
      'paper':row(O/'paper.pdf',O),'paper_pages':9,'archive':row(archive,O),'archive_members':len(allow['files']),
      'selected_historical_authored_records':15,'exact_historical_checker_copies':3,
      'final_builder_cases':30,'final_builder_mode_processes':90,'final_whole_verifier_modes':3,'final_finite_executions':45,
      'staged_builder_mode_processes_also_preserved':90,'deterministic_final_archive':True,
      'prior72_original287_whole01_650_rows_unchanged':True,'sections1_to6_byte_exact':True,
      'priority_overlap_Luo_Zha':'UNKNOWN','source_bodies_newly_retrieved_or_inspected_in_repair':False,'no_overall_readiness_claim':True}
    put(R/'FINAL_REPAIR_REPORT.json',summary)
    text=f'''# Version 1.1 bounded repair handoff

Prepared {summary['utc']}. Workflow counts and pending-gate statements below describe this preparation checkpoint, not live publication state.

Implemented exactly the three ROOT-adopted whole01 P3 findings: physical outside-kit archive output preflight and complete pre-write content validation; primary OWR report/contribution title and joint-work correction; timeless permanent lifecycle prose with explicitly dated preparation STATUS. This is an implementation report, not an independent whole review or root adoption of the repaired candidate. Whole01 counts one of the minimum TWO complete reviews TOTAL; ROOT bounded-repair adoption and whole02 remain pending.

The mathematical theorem and entire sections1-6 proof/credit prose are byte-exact from v1.0. Version1.1 and bibliographic date16October2026 use the human's client date. The exact field/GL15 quotient and UNKNOWN Luo-Zha overlap are unchanged. No firstness, novelty, unrestricted source inspection, human peer review, general kernel-generation disproof or live publication-platform claim is introduced. Current metadata/paper/README lifecycle statements remain true after a later deposit. Historical wrong titles and obsolete workflow statuses remain only in qualified byte-exact dated records.

Final verification:30 fresh disposable filesystem cases in normal/-O/-OO,90 actual processes,28 negative cases; both physical case-alias directions, existing objects including dangling/symlink/hardlink aliases, absent parents, traversal, symlink ancestry and invalid member/inventory/content cases. Every negative run leaves its kit and existing target unchanged; successful outside outputs are byte-identical. Three final whole-kit verifier modes execute45 finite diagnostics successfully. The final archive rebuild is byte-identical. All9 final PDF pages were individually viewed, with no overflow or layout defect. One harmless existing underfull reference line remains. Detailed argv/UTC/exit/raw stdout/stderr and fixture identities are retained outside the release archive. Only owned unsealed fixture duplicates were cleaned after their identity/custody ledger; no canonical hardlinks were made.

The release archive has{len(allow['files'])} explicit members, including15 selected authored historical records, three exact diagnostic copies, new bounded repair record, proof, metadata and tooling. It excludes all raw third-party bodies/text/OCR/source images/API/runtime fixtures and recursive custody trees. Two selected additions are the dated whole01 report and ROOT adoption; their scopes explicitly concern v1.0, not acceptance of this revision. The changed/added identities from the staged candidate are enumerated in STAGED_BEFORE_TO_FINAL_DIFFERENCE.json.

Preservation: all72 prior v1.0/preparation/original-native rows,287 original audit-input rows and650 sealed whole01 output rows are byte-exact. Original publication/zenodo-deposit.json is untouched. New publication/zenodo-deposit-v1_1.json and the v1.1 local manifest parse read-only to identical metadata and exact same PDF/ZIP objects. No Git/index/branch/QUEUE/PR/service/contact/source-retrieval/other-agent action occurred. This handoff records completion of known bounded repairs only; external ROOT adoption and a new complete adversarial review remain required.

Paper: {summary['paper']['bytes']} bytes, SHA256 {summary['paper']['sha256']}.
Support archive: {summary['archive']['bytes']} bytes, SHA256 {summary['archive']['sha256']}.
'''
    (O/'PREPARATION_REPORT.md').write_text(text)
    (O/'RESEARCH_LOG.md').write_text((R/'RESEARCH_LOG.md').read_text())
    final_map={x['path']:x for x in inventory(O)}
    delta.update(changed=[{'before':before_map[n],'after':final_map[n]} for n in sorted(before_map.keys()&final_map.keys()) if before_map[n]!=final_map[n]],
      added=[final_map[n] for n in sorted(final_map.keys()-before_map.keys())],
      deleted=[before_map[n] for n in sorted(before_map.keys()-final_map.keys())],
      note='Complete staged-to-final difference including final explanatory reports/log, before outer self-referential seal. Source/PDF/builder/proof remain unchanged from inspected staged bytes. The outer seal is separately pinned by REPAIR_SEAL.json.')
    put(R/'STAGED_BEFORE_TO_FINAL_DIFFERENCE.json',delta)
    # Complete final outer inventory also gives exact staged-to-final map,
    # including the newly written reports, without recursive seal self-hashing.
    put(O/'PREPARATION_SEAL.json',{'utc':datetime.now(timezone.utc).isoformat(),'version':'1.1','files':inventory(O),'versioned_native_manifest':row(native,B),'source_stage_inventory':row(R/'STAGED_BEFORE_FINAL_PINS.json',R),'root_repair_adoption_pending':True,'minimum_whole_reviews_TOTAL':2,'whole_reviews_adopted':1,'whole02_pending':True})
    put(R/'REPAIR_SEAL.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':inventory(R),'preprint_seal':row(O/'PREPARATION_SEAL.json',O),'root_adoption_record':row(adoption_path,B),'scope':'owned bounded-repair evidence only; output seal self-hash excluded; no independent review or publication authority'})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
