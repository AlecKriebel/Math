#!/usr/bin/env python3
"""Read-only importer/hash-role audit; outputs only in this additive qualification folder."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=HERE.parents[4])
parser.add_argument('--problems',type=Path,required=True)
parser.add_argument('--reports',type=Path,required=True)
a=parser.parse_args();repo=a.repo.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
family=repo/'draft_pr_publication_program_20260930/audits/pr34_7000004/differential_family'
snapshot=family.parent/'source_snapshot'
old_manifest=family/'MANIFEST.json';old_bytes=old_manifest.read_bytes();m=json.loads(old_bytes)
assert sha(old_bytes)=='8d51ceee6eba20546e8592122594be32318a13eb21e57f12faea5554c72e9366'
for member in m['members']:
    b=(family/member['path']).read_bytes()
    assert len(b)==member['bytes'] and sha(b)==member['sha256'],member['path']
source_manifest=json.loads((repo/'unsolved_math_prioritization/manifest.json').read_text())
files=[]
for name,path in [('problems.json',a.problems),('research_results.json',a.reports)]:
    b=path.read_bytes();expected=source_manifest['files'][name]
    assert len(b)==expected['bytes'] and sha(b)==expected['sha256'],name
    files.append({'source_name':name,'bytes':len(b),'sha256':sha(b),'url':'https://huggingface.co/datasets/ulamai/UnsolvedMath/resolve/'+source_manifest['revision']+'/'+name})
problems=json.loads(a.problems.read_text());reports=json.loads(a.reports.read_text())
assert len(problems)==15458 and len({str(p['id']) for p in problems})==15458
selected=[p for p in problems if p['id']==7000004];assert len(selected)==1
p=selected[0];assert p['problem_number']=='AMR-069-0004'
assert sum(z['problem_number']=='AMR-069-0004' for z in problems)==1
r=reports[p['problem_number']]
assert p==json.loads((snapshot/'source_record.json').read_text())
assert r==json.loads((snapshot/'prior_report.json').read_text())
queuefile=repo/'unsolved_math_prioritization/queue.py'
spec=importlib.util.spec_from_file_location('read_only_queue_hash_role_probe',queuefile)
queue=importlib.util.module_from_spec(spec);spec.loader.exec_module(queue)
policy=json.loads((repo/'unsolved_math_prioritization/policy.json').read_text())
# score is a pure function: sync, rank, show, status and connect are NEVER invoked.
actual=queue.score(p,r,policy)
serialized=json.dumps([p,r],sort_keys=True)
computed=sha(serialized.encode())
ready=json.loads((snapshot/'readiness.json').read_text())
verdict=json.loads((snapshot/'review/verdict.json').read_text())
review_document=(snapshot/'review/REVIEW.md').read_bytes()
review_document_sha=sha(review_document)
assert actual['review_hash']==computed==ready['review_hash']=='2e49912828f018ce3f85114143f107c8b3315172c5e5538a6231c128efb1d086'
assert actual['statement_hash']==ready['statement_hash']
assert review_document_sha==verdict['review_sha256']=='0d8a579e9273e3bd7e5bc170b7964b2754a0404896c35dc47e1512e4f46326a0'
assert review_document_sha!=computed
mutants=[]
for name,pp,rr in [('raw_source_changed',dict(p,status='fabricated_hash_role_control'),r),('report_changed',p,dict(r,fabricated_hash_role_control=True)),('report_deleted',p,{})]:
    changed=queue.score(pp,rr,policy)['review_hash']
    assert changed!=computed,name
    mutants.append({'name':name,'new_importer_source_pair_hash':changed,'original_readiness_source_binding_rejects':True,'review_document_hash_unchanged':sha(review_document)==review_document_sha})
assert sha((review_document.decode()+'\nAltered document control.\n').encode())!=review_document_sha
assert queue.score(p,r,policy)['review_hash']==computed
mutants.append({'name':'review_document_only_changed','source_pair_hash_unchanged':True,'verdict_document_hash_rejects':True})
assert review_document_sha!=queue.score(p,r,policy)['review_hash']
mutants.append({'name':'source_binding_replaced_by_review_document_hash','actual_importer_binding_rejects':True})
assert sha(json.dumps([p,r],sort_keys=True,separators=(',',':')).encode())!=computed
mutants.append({'name':'wrong_serialization_compact_separators','actual_importer_binding_rejects':True})
assert sha(json.dumps([r,p],sort_keys=True).encode())!=computed
mutants.append({'name':'source_pair_order_swapped','actual_importer_binding_rejects':True})
for member in m['members']:
    b=(family/member['path']).read_bytes()
    assert len(b)==member['bytes'] and sha(b)==member['sha256'],member['path']
assert old_manifest.read_bytes()==old_bytes
out={'passed':True,'original_closed_24_members_unchanged':True,'original_closed_manifest_sha256':sha(old_bytes),'source_revision':source_manifest['revision'],'fresh_complete_files':files,'full_record_count':len(problems),'selected_numeric_id':p['id'],'selected_problem_number':p['problem_number'],'full_raw_record_matches_frozen_original':True,'full_separate_prior_report_matches_frozen_original':True,'actual_importer':{'path':'unsolved_math_prioritization/queue.py','bytes':queuefile.stat().st_size,'sha256':sha(queuefile.read_bytes()),'pure_function_called':'score(p,r,policy)','hash_definition':'SHA256(json.dumps([full_raw_source_record, full_separate_prior_report], sort_keys=True).encode())','serialization_defaults':'ensure_ascii=True; default separators including spaces; source then report'},'hash_roles':{'readiness_review_hash_source_pair':computed,'verdict_review_sha256_document':review_document_sha,'statement_hash':actual['statement_hash']},'mandatory_issue_3_withdrawn':True,'source_pair_hash_must_remain_2e499128':True,'science_or_proof_changed':False,'original_attempts_added':0,'mutants':mutants,'qualified_historical_files':['REPORT.md mandatory integration issue3','ORIGINAL_INTEGRITY.json readiness_review_hash_actual/stored comparison and stale-discrepancy prose','RESEARCH_LOG.md 03:44 checkpoint stale original readiness hash statement'],'scope':'The old comparison recorded two real different hashes but assigned the wrong semantic role. It is not a mismatch in the original readiness source binding.'}
text=json.dumps(out,indent=2,sort_keys=True)+'\n';(HERE/'RESULTS.json').write_text(text);print(text,end='')
