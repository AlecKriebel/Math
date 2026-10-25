from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile,stat
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23444606')
O=B/'reviews/analytic';S=B/'sources';P=S/'published-source/initial-omnific-models-source-and-verification'
def h(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pin(path):
 p=Path(path);d=p.read_bytes();return {'path':str(p),'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
def save(name,v): (O/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
now=datetime.now(timezone.utc).isoformat()
receipt=json.loads((S/'receipt.json').read_text());record=json.loads((S/'record.json').read_text())
assert h(S/'record.json')==receipt['record_sha256']
assets=[]
for item in receipt['files']:
 d=(S/item['name']).read_bytes(); actual={'bytes':len(d),'md5':hashlib.md5(d).hexdigest(),'sha256':hashlib.sha256(d).hexdigest()}
 assert all(actual[k]==item[k] for k in actual)
 assets.append({**item,'rechecked_utc':now,'actual':actual,'all_match':True})
old=json.loads((O/'initial-source-hashes.json').read_text())
current={str(p.relative_to(P)):h(p) for p in sorted(P.rglob('*')) if p.is_file()}
assert current==old and len(current)==145
C=O/'replay/source-copy'
copy={str(p.relative_to(C)):h(p) for p in sorted(C.rglob('*')) if p.is_file()}
assert copy==current
manifest=json.loads((P/'SOURCE_MANIFEST.json').read_text())
assert len(manifest)==144
for name,want in manifest.items():
 assert pin(P/name)['bytes']==want['bytes'] and h(P/name)==want['sha256']
archive=S/'initial-omnific-models-source-and-verification.zip'
with zipfile.ZipFile(archive) as z:
 members=[x for x in z.infolist() if not x.is_dir()]
 assert len(members)==145
 for x in members:
  q=Path(x.filename)
  assert not q.is_absolute() and '..' not in q.parts and not stat.S_ISLNK(x.external_attr>>16)
  assert hashlib.sha256(z.read(x)).hexdigest()==current[x.filename]
 assert z.read('output/pdf/initial-omnific-models.pdf')==(S/'initial-omnific-models.pdf').read_bytes()
used=['main.tex','SOURCE_MANIFEST.json','verification/CONTROL_PLAN.json','verification/verify_all.py','verification/package_common.py','verification/self_test.py','draft_pr_actual_claims_1100_1200_20261017/audits/pr1151_30003321/FINAL_PROOF.md','draft_pr_actual_claims_1100_1200_20261017/audits/pr1151_30003321/pr_repair_candidate/DEPENDENCY_PROOF.md','draft_pr_actual_claims_1100_1200_20261017/audits/pr1151_30003321/verify_finite_signs.py']
custody={'checked_utc':now,'record':pin(S/'record.json'),'receipt':pin(S/'receipt.json'),'assets':assets,'regular_archive_members':145,'all_145_extracted_files_unchanged':True,'all_145_archive_members_match_extraction':True,'isolated_replay_copy_145_files_identical_after_run':True,'manifest_payload_members':144,'manifest_all_pins_match':True,'embedded_pdf_identical':True,'additional_reader_pdfs':[],'nested_archives':[],'initial_snapshot':pin(O/'initial-source-hashes.json'),'used_sources':[pin(P/u) for u in used],'source_mutations':False}
save('source-custody.json',custody)
coverage={
'ek-author': {'role':'central primary theorem and normal-form interfaces','read':'Definitions and pp.1–9, Lemma3.1 with proof, Propositions3.2–3.3, Lemma5.1, Theorem5.1 and proof, Proposition5.2, §6.2 omnific criterion, Question9.1.','conclusion':'Exact canonical-image, truncation/cross-section, initial coefficients and dyadic right-predecessor interfaces match; current appendix independently supplies sufficiency.','limits':'Primary author edition; not byte-authenticated against publisher body. Foundational monographs and full2001 predecessor not independently rederived/read.'},
'kaplan-thesis2015': {'role':'original question','read':'§7.1 Question1 and preceding half-integer group example, printedp47.','conclusion':'Original additive question and isomorphic-versus-already-contained distinction match.','limits':'Not full thesis review.'},
'owr2016-60': {'role':'published question/context','read':'Kaplan joint-work contribution model/theorem/question context, printedpp3354–3356, Question1.','conclusion':'The additive-group question has no multiplicative closure assumption.','limits':'Not a review of unrelated report contributions.'},
'ek-arxiv-v1': {'role':'historical edition numbering','read':'Question2 and preceding discrete subgroup/subdomain context.','conclusion':'Earlier question numbering accurately distinguished from author edition.','limits':'Earlier version not silently substituted for current author theorem numbering.'},
'adh-v3': {'role':'credited minimum-exponent observation','read':'Lemma3.2 and proof with initial-set/Hahn-group context, p11.','conclusion':'Minimum of initial exponent set is negative ordinal; current bottom lemma reproves needed part.','limits':'No import of unrelated H-field assertions.'},
'kks-v3': {'role':'credited general transport machinery','read':'Proposition3.9 full proof and Construction3.10 formula/hypotheses.','conclusion':'Positive coefficient scaling and exponent order relabeling are established; restricted current image checked directly.','limits':'No full proof audit of automorphism classification or global novelty claim.'},
'bvh-v1': {'role':'nearby background construction','read':'Thin-partition context and Theorem6.7 proof; §7.2 fixed set-sized subgroup and Proposition7.1 proof.','conclusion':'General surreal substructures/translation action results do not by themselves establish the exact all-G initial omnific image.','limits':'Fresh May2023 arXiv body, not separately cited April2022 author edition; no absence-of-prior-result certification.'}
}
pr=B/'reviews/scope/primary-source-receipts.json';data=json.loads(pr.read_text());rows=[]
for item in data['sources']:
 p=Path(item['path']);t=p.with_suffix('.txt')
 assert h(p)==item['sha256'] and h(t)==item['text_sha256']
 rows.append({**{k:item[k] for k in ['name','url','version_description','retrieved_utc','path','bytes','sha256','text_sha256']},**coverage[item['name']],'bytes_rechecked':True})
save('primary-interface-ledger.json',{'checked_utc':now,'raw_acquisition_receipt':pin(pr),'entries':rows,'opinions_read':False,'source_of_bytes':'Fresh raw primary cache shared by acquisition agent; scope/sibling review bodies excluded.'})
fresh=json.loads((O/'fresh-control-results.json').read_text());rp=json.loads((O/'replay/verify-all.stdout.json').read_text());rr=json.loads((O/'replay/receipt.json').read_text())
assert fresh['assertions']==1206538 and fresh['script_sha256']==h(O/'fresh_controls.py')
assert rp['status']=='PASS' and len(rp['runs'])==2 and len(rp['actual_wrong_result_failures'])==8
assert rr['exit_code']==0 and rr['stdout_sha256']==h(O/'replay/verify-all.stdout.json')
assert all(r['exit']==0 and r['stderr']['bytes']==0 for r in rp['runs'])
assert all(r['exit']==1 for r in rp['actual_wrong_result_failures'])
assert rp['runs'][0]['complete_stdout']==rp['runs'][1]['complete_stdout']==(P/'verification/EXPECTED_FINITE_SIGNS.stdout.json').read_text()
assert (O/'replay/verify-all.stderr.txt').stat().st_size==0
save('evidence.json',{'created_utc':now,'independent_controls_before_submitted_helper_read':True,'fresh_control_started_utc':fresh['started_utc'],'fresh_control_finished_utc':fresh['finished_utc'],'fresh_assertion_count':fresh['assertions'],'fresh_scope':fresh['scope'],'fresh_count_warning':'Total includes repeated finite checks and one finite-stage illustration; not a count of independent proofs. No universal ordinal/class conclusion follows from computation.','fresh_counts':fresh['counts'],'fresh_artifacts':[pin(O/x) for x in ['fresh_controls.py','fresh-control-results.json','fresh-controls.stdout.txt','fresh-controls.stderr.txt']],'submitted_replay_receipt':rr,'submitted_positive_modes':[r['mode'] for r in rp['runs']],'submitted_positive_expected_output_identical':True,'submitted_expected_mutation_failures':rp['actual_wrong_result_failures'],'submitted_replay_artifacts':[pin(O/x) for x in ['replay/receipt.json','replay/verify-all.stdout.json','replay/verify-all.stderr.txt']],'not_executed':['build_package.py','verification/self_test.py','historical family helper programs'],'source_custody':pin(O/'source-custody.json'),'primary_interfaces':pin(O/'primary-interface-ledger.json'),'independence_disclosure':'Necessary FINAL_PROOF.md and DEPENDENCY_PROOF.md and manuscript contain incidental historic AI/status/priority text. Dedicated historical, priority and sibling report bodies unread; incidental judgments not adopted.','no_mathematical_defect_identified':True})
print(json.dumps({'checked_utc':now,'assets':len(assets),'source_files_unchanged':len(current),'manifest':len(manifest),'primary_bodies':len(rows),'fresh_assertions':fresh['assertions'],'positive_replays':len(rp['runs']),'negative_replays':len(rp['actual_wrong_result_failures'])}))
