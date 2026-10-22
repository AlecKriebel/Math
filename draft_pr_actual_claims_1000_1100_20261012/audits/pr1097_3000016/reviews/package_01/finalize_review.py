#!/usr/bin/env python3
"""Seal only this review; candidate inputs are read and rehashed, never edited."""
import sys
sys.dont_write_bytecode=True
import datetime,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
A=R.parent.parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'bytes':Path(p).stat().st_size,'sha256':sha(p)}
def load(p):return json.loads(Path(p).read_text())
def write(n,d):(R/n).write_text(json.dumps(d,indent=2)+'\n')
def need(q,m):
    if not q:raise ValueError(m)

utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
baseline=load(R/'INPUT_PINS.json')
rows=[]
for r in baseline['files']:
    got=pin(A/r['path']);need(got=={'bytes':r['size'],'sha256':r['sha256']},'Frozen input changed: '+r['path'])
    rows.append({'path':r['path'],**got,'unchanged':True})
write('INPUT_PRESERVATION.json',{'utc':utc,'count':len(rows),'all_unchanged':True,'records':rows})
normal=load(R/'INDEPENDENT_NORMAL.json');need(normal==load(R/'INDEPENDENT_OPTIMIZED.json'),'math results differ')
package=load(R/'PACKAGE_REPRODUCTION.json');need(package['status']=='PASS','package reproduction incomplete')
case=load(R/'CASE_ALIAS_FINDING.json');need(len(case['commands'])==4 and all(r['exit_code']==0 and r['actual_output_created_inside_protected_kit'] for r in case['commands']),'case alias evidence incomplete')
finding={'id':'P3_CASE_ALIAS_PROTECTED_OUTPUT_BYPASS','priority':'P3','file':'preprint_v1_0/kit/scripts/common.py','lines':[56,57,66,67,68,69,70,71,72],
         'title':'Use filesystem identity to protect case aliases of the kit root',
         'body':'Actual clean/CLEAN aliases share an existing parent inode on this case-insensitive filesystem, but lexical containment atline72 accepts both writers. Four normal/optimized commands create fresh archive or compiler-child outputs inside the protected kit. This is fresh insertion, not existing-byte overwrite or a mathematical defect.',
         'evidence':'CASE_ALIAS_FINDING.json; reproduce_case_alias.py',
         'repair':'Retain lexical checks and reject existing parent ancestors with the same filesystem identity as existing protected roots. Add actual casealias controls, preserve missing-root behavior, and rebuild all dependent inventories/archives/bindings before a new complete review.'}
verdict={'utc':utc,'pr':1097,'problem_id':3000016,'head_oid':'ad7b0eeef847da65afe1b691705cfa6e832e8201',
         'status':'COMPLETE_WHOLE_PACKAGE_REVIEW_01_REQUIRES_BOUNDED_REPAIR_ONE_P3',
         'complete_whole_package_review':True,'mathematics':'PASS_EXACT_STATED_SCOPE','source_credit_and_qualified_framing':'PASS',
         'priority':'UNKNOWN','current_worldwide_openness':'UNKNOWN','independent_discovery':'UNKNOWN',
         'actionable_findings':[finding],'finding_counts':{'P0':0,'P1':0,'P2':0,'P3':1},
         'candidate_inputs_rehashed_unchanged':len(rows),'actual_Git_bodies_compared':8,
         'preparation_outputs_rehashed':131,'preparation_inputs_rehashed':165,'custody_exact_copies':83,'custody_exclusions':82,
         'independent_closed_ZIP_members':103,'independent_control_coverage':normal['coverage'],'independent_faults_detected':len(normal['faults_detected']),
         'complete_normal_optimized_results_equal':True,'actual_canonical_PDF_pages_viewed':6,
         'real_normal_optimized_clean_compilation':'PASS_IDENTICAL_PDF','builtin_compiler':'SUCCESS',
         'standard_package_commands':package['command_count'],'expected_rejections':package['expected_nonzero_rejections'],
         'actual_case_alias_bypass_commands':4,'native_repository_uploader_local_check':'PASS',
         'new_complete_whole_reviews_completed':1,'minimum_new_complete_whole_reviews':2,'new_clean_whole_reviews_completed':0,
         'publication_ready':False,'published':False,'ordered_service_hold_pr':1032,
         'performed_Git_mutation_external_service_PR_or_outreach_action':False,
         'candidate_or_original_modified':False,'completion_percent_delegated_review':100,
         'next_step':'Root reproduce/adopt finding; bounded guard repair and all dependent updates; NEW complete adversarial review02, further loops if findings.'}
write('VERDICT.json',verdict)
with (R/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+utc+' - Complete independent whole review01: math/source credit/6actualpages/native/CLOSED103ZIP/83commands pass; one actual P3 casealias fresh-output insertion bypass reproduced in4normal/optimized writer commands. All306frozeninputs unchanged. Review completion100%; publishing workflow incomplete, held1032. No canonical/Git/service/outreach change.\n')
    f.write('\nChronology note: the frozen derivation heading used15October from the supplied environment date. The authoritative actual input-freeze timestamp is '+baseline['utc']+' and all tool/command receipts are UTC. Its frozen content is preserved unchanged; later source/preparation/new-audit report reads are documented in this final report.\n')
inventory=[]
for p in sorted(R.rglob('*')):
    if p.is_file() and p.name not in {'OUTPUT_PINS.json','FINAL_SEAL.json'}:
        inventory.append({'path':p.relative_to(R).as_posix(),**pin(p)})
write('OUTPUT_PINS.json',{'utc':utc,'scope':'Every review output except this inventory and its separate final seal','entries':inventory})
write('FINAL_SEAL.json',{'utc':utc,'status':verdict['status'],'review_complete':True,'completion_percent_delegated_review':100,
      'output_pins':{'path':'OUTPUT_PINS.json',**pin(R/'OUTPUT_PINS.json')},'outputs_bound':len(inventory),
      'input_preservation':{'path':'INPUT_PRESERVATION.json',**pin(R/'INPUT_PRESERVATION.json')},
      'frozen_inputs_unchanged':len(rows),'finding_counts':verdict['finding_counts'],
      'candidate_paper':pin(A/'preprint_v1_0/paper.pdf'),'candidate_support_archive':pin(A/'preprint_v1_0/pr1097_support_v1_0.zip'),
      'new_complete_whole_reviews_completed':1,'minimum_new_complete_whole_reviews':2,
      'publication_ready':False,'published':False,'ordered_service_hold_pr':1032})
print(json.dumps({'status':verdict['status'],'outputs':len(inventory),'inputs_unchanged':len(rows),'findings':verdict['finding_counts'],'seal':pin(R/'FINAL_SEAL.json')},sort_keys=True))
