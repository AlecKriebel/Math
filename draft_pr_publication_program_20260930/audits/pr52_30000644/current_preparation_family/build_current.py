#!/usr/bin/env python3
"""Private text-only builder. No math checker or external helper execution."""
from pathlib import Path
from datetime import datetime,timezone
import difflib,hashlib,json,stat
from closure_common import HERE,bind,require,external,science,COUNTER,sha

A=HERE.parent
O=A/'original_preparation_family'
C=A.parent/'pr45_9900007'
HEAD='d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a'
def utc():return datetime.now(timezone.utc).isoformat()
def put(name,value):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def text(name,value):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value)
require(not (HERE/'original_head_archive').exists(),'archive initially absent')
require(not (HERE/'current_science').exists(),'operative packet initially absent')
auth=json.loads((O/'ORIGINAL_AUTHENTICATION.json').read_bytes())
require(auth['head']==HEAD and auth['science_file_count']==19,'authentic original source head/count')
originals={}
git={}
for item in auth['primary_science_files']:
    source=Path(item['local_identity']['path'])
    rel=source.relative_to(O/'original').as_posix()
    body=source.read_bytes()
    require(hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==item['git_blob_sha1'],'authentic whole original Git blob')
    require(len(body)==item['local_identity']['bytes'] and sha(body)==item['local_identity']['sha256'],'authentic original SHA256/length')
    originals[rel]=body;git[rel]=item['git_blob_sha1']
    for top in ('original_head_archive','current_science'):
        p=HERE/top/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
require(len(originals)==19,'nineteen distinct originals')
qualifier='''# Operative qualification for the credited Q-algebra theorem

The displayed mathematical reconstruction is retained unchanged below and
is credited to van den Essen, Maubach and Venereau, JPAA 210 (2007), 141–146,
DOI 10.1016/j.jpaa.2006.09.013. Current outcome: already_solved, no campaign
discovery or new paper. It covers every commutative unital Q-algebra R and
all m,n >=1, for input polynomial automorphisms of determinant exactly one.
No reducedness/domain/Noetherian/tameness hypothesis is added.

GLOBAL_QUALIFICATIONS.json applies to every historical header, PASS, source
status, checksum, model/runtime, pending review or publication statement in
this packet. The appended original header and historical receipts identify
the literal original archive, not current ROOT acceptance. No full JPAA
article proof, formal proof certificate or human peer review is claimed.

The fresh first-party universal proofs are linked from README.md; the two
review families have actual ROOT closure and separate readback, as bound
in ../EXTERNAL_BINDINGS.json. Their universal arguments support the claim;
finite checks are corroboration. This text preparation is not a third
independent mathematical review or an approval for native/remote action.

Historical original text follows; its mathematical sections are unchanged.

---

'''
for name in ('KNOWN_THEOREM.md','review/KNOWN_THEOREM.md'):
    prefix=qualifier if name=='KNOWN_THEOREM.md' else qualifier.replace('GLOBAL_QUALIFICATIONS.json','../GLOBAL_QUALIFICATIONS.json').replace('README.md','../README.md').replace('../EXTERNAL_BINDINGS.json','../../EXTERNAL_BINDINGS.json')
    text('current_science/'+name,prefix+originals[name].decode())
text('current_science/README.md','''# 30000644: credited special-automorphism lifting theorem

The exact Q-algebra problem was already solved by Arno van den Essen,
Stefan Maubach and Stephane Venereau, JPAA 210 (2007), 141–146,
DOI 10.1016/j.jpaa.2006.09.013. Operative disposition: **already_solved**,
original 0/5 fresh proof-search attempts, one separately identified credited
known-theorem validation activity, no new discovery and no new paper.

[KNOWN_THEOREM.md](KNOWN_THEOREM.md) retains the complete reconstruction
for every commutative unital Q-algebra and all m,n >=1. The input is an
existing determinant-one automorphism; its lift has an actual polynomial
inverse and determinant exactly one over R[t] before reduction. Nilpotents
and zero divisors are included. Jacobian conjecture, general tameness,
non-Q-algebra cases and infinite formal lifting are outside this claim.

The newly reviewed first-party universal proofs are
[divergence/shear reconstruction](../../divergence_shear_adversary_family/INDEPENDENT_PROOF.md)
and [finite-jet reconstruction](../../nilpotent_jet_adversary_family/UNIVERSAL_JET_PROOF.md).
Their [reports](review/REVIEW.md) and actual closed input identities are
referenced in place, with no source-PDF or image duplication. They report
6,681 and 9,612 new exact finite controls, which supplement the proofs.
This current preparation reuses the completed first reviewer and provides
no third mathematical independence claim.

[GLOBAL_QUALIFICATIONS.json](GLOBAL_QUALIFICATIONS.json) governs every
retained historical field: raw prior key absent; selected SQLite report
is non-NULL text '{}'; original prior_report.json is the literal JSON null
absence display. Old proof hashes and receipts refer to the archived
original proof bodies. The nineteen original files remain literal in
[original_head_archive](../original_head_archive).

The unchanged author and old-review scripts/results are retained as
historical reproducibility artifacts. They were already replayed privately
in the actual closed original preparation. To rerun, copy the relevant
archived proof and checker to a temporary directory; those scripts write
their result files and must not be run against a frozen packet. No script
is rerun in this text preparation. Current editorial proof wrappers have
different hashes; old receipts are not represented as new receipts for
those wrappers. No full journal proof, human peer review or formal proof
certificate was obtained. ROOT acceptance, merge and publication are
separate later operations.
''')
text('current_science/SOURCE_AUDIT.md','''# Operative credited-result and source qualification

The exact target 30000644 / OWR-1452-008 is already_solved: every
commutative unital ring containing Q, all m,n >=1, existing polynomial
automorphisms of determinant exactly one. Credit: van den Essen, Maubach
and Venereau, JPAA 210 (2007), 141–146, DOI 10.1016/j.jpaa.2006.09.013.
OWR printed p.26 supplies an affirmative credited answer immediately after
the selected question. Acta printed p.317 explicitly confirms the full
Q-algebra parameter scope. The motivating reducedness assumption belongs
to a different construction. The decisive page image resolves the >=
versus > extraction error. See the [original primary-source audit](../original_head_archive/SOURCE_AUDIT.md)
and the actually closed new families' source observations, linked through
../EXTERNAL_BINDINGS.json. This current preparer does not claim a new
download or a new visual inspection of source PDFs in this preparation.

The complete JPAA journal article was not obtained or line-by-line audited.
The exact original affirmative source statements and the checkable
first-party reconstructions remain distinct evidence. No open question
over other coefficient rings is substituted for the selected Q-algebra
target, and no novel theorem, human refereeing or formal certificate is
claimed. No new paper or DOI is appropriate under the user's process.

The literal original archive preserves the historical open triage and
ambiguous prior-join wording. Operatively: the raw research_results key
OWR-1452-008 is ABSENT; the selected SQLite report cell is non-NULL text
'{}', decoded as an empty object; original prior_report.json is exactly
'null\\n', decoded as JSON null. The latter was the author's absence
display convention, not a present null upstream key or SQL NULL. The
closed original preparation's SOURCE_PRECISION_QUALIFICATIONS.md and
SELECTED_LITERAL_SOURCE.json bind that distinction in place; this packet
does not copy or modify raw datasets or SQL.

Original final accounting is zero substantive fresh search attempts, 0/5,
plus one credited known-theorem validation activity. The old 1/5 research
log wording is historical and superseded by that final classification.
There is no separate supplied original-response count to invent. All old
PASS/checksum/model/runtime/status/pending/readiness fields are dated
historical evidence under GLOBAL_QUALIFICATIONS.json, with no current
ROOT or native acceptance authority. No native queue/catalog/state is
re-read or changed here.
''')
text('current_science/review/REVIEW.md','''# Operative review references for the credited theorem

This wrapper is current text preparation, not a third independent review.
The complete [historical review](../../original_head_archive/review/REVIEW.md)
and its unchanged checker/results/verdict remain archived. Its old PASS,
hashes, runtime/model and pending/publication language are historical.
The old hashes refer to archived original proof bodies, not editorial
wrappers. ../GLOBAL_QUALIFICATIONS.json applies throughout.

The two fresh mathematical reviews are the
[divergence/shear family](../../../divergence_shear_adversary_family/REPORT.md)
and [nilpotent-jet family](../../../nilpotent_jet_adversary_family/REPORT.md).
They independently formed their routes before convergence. Both found
no mandatory mathematical correction within the literal all-Q-algebra,
all-positive-m,n claim. Their universal proofs are first-party checkable
artifacts; finite counts (6,681 and 9,612) are corroboration. The latter
family retained its initially interrupted computation and then ran its
revised exact quotient checker successfully; the interruption is not
represented as a mathematical counterexample or a successful run.

All three predecessor packages have actual ROOT closure and separate
readback, as shown by the six complete CAP4 records bound in
../../EXTERNAL_BINDINGS.json. Closure provides body/mode custody and
genuine process chronology, not native/merge/publication approval.
The reused preparer supplies no new ROOT personal-read attestation.

The outcome remains already_solved, credited to the 2007 authors, with
0/5 fresh searches plus one known-theorem validation activity and no new
paper. No complete JPAA proof, human peer review or formal proof certificate
was obtained. The existing input automorphism, Q-algebra assumption,
exact determinant-one condition, arbitrary constant base automorphism
and finite jet restriction remain essential.
''')
text('current_science/RESEARCH_LOG.md','''# Operative accounting and historical log qualification

The complete timestamped [original log](../original_head_archive/RESEARCH_LOG.md)
remains unchanged. Its early phrase 'substantive reconstruction 1/5' was
explicitly reclassified in the final original ledger as one credited
known-theorem validation activity, with zero fresh proof-search attempts.
The operative accounting is therefore 0/5, plus that one validation
activity. No new original response count or discovery credit is created.

The original source-curation finding was already_solved. Two subsequent
independent mathematical families reconstructed and challenged the exact
Q-algebra theorem, and ROOT genuinely closed/read both packages. Their
actual evidence is bound in ../EXTERNAL_BINDINGS.json. This present text
preparation reuses a completed reviewer and is not another independent
mathematical family. Its actual private builder capture is in
../builder_capture; its timestamps and PID are recorded after execution.

All historical source/status/PASS/PDF/hash/model/runtime/pending/readiness
statements are governed by GLOBAL_QUALIFICATIONS.json. No current native,
Git, remote, paper, DOI, tracker, human review or formal-proof approval is
claimed. Current SOURCE custody and later acceptance remain separate.
''')
text('current_science/pr_body.md','''## Credit the prior theorem and correct the extracted open status

The selected Q-algebra reduction-map problem was already answered by
Arno van den Essen, Stefan Maubach and Stephane Venereau, JPAA 210 (2007),
141–146, DOI 10.1016/j.jpaa.2006.09.013. The original OWR report p.26
gives the affirmative credited answer immediately after the question;
Acta p.317 confirms every commutative unital Q-algebra and all m,n >=1.

This partial-result package records the prior-result/source correction,
preserves the nineteen original files, and retains a fully credited
all-ring reconstruction. The existing input is a determinant-one
polynomial automorphism; invariant shears and finite jet corrections
give actual polynomial inverses and determinant one before reduction.
Two fresh independent mathematical audits found no mandatory correction,
with universal proofs and 6,681/9,612 exact finite controls. Actual ROOT
closure/readback evidence is retained. No campaign discovery is claimed.

Original accounting remains 0/5 substantive fresh searches plus one
credited known-theorem validation activity. The original JSON-null prior
display is qualified against the absent raw key and non-NULL SQLite '{}'
cell. Historical receipts and proof hashes identify the archived originals.
Full JPAA journal proof access was unavailable; AI verification is not
human peer review or formal certification. This already_solved outcome
requires no new paper or DOI. Native integration and merge are later
workflow actions, not claims made by this SOURCE package.
''')
record=json.loads(originals['source_record.json'])
record['status']='already_solved'
record['literature_assessment']='The exact Q-algebra reduction-map target was already answered affirmatively in its cited original source and credited to van den Essen, Maubach and Venereau, JPAA210(2007)141–146, DOI10.1016/j.jpaa.2006.09.013. No campaign novelty is claimed.'
record['literature_checked_at']='2026-10-03'
record['background']='Operative corrected view: the exact commutative unital Q-algebra theorem, for all m,n>=1 and existing determinant-one polynomial automorphisms, is already solved. OWR printed p.26 gives its affirmative credited answer; Acta printed p.317 confirms the general Q-algebra scope. The prior 2026-08-21 open triage is preserved unchanged in ../original_head_archive/source_record.json and superseded only in this operative view. No live dataset/catalog update or new discovery is implied.'
record['tags']=['literature-status:already_solved' if a=='literature-status:open' else a for a in record['tags']]
record['operative_view_qualification']={'schema':'pr52-qualified-operative-source-view/v1','literal_original':'../original_head_archive/source_record.json','live_catalog_modified':False,'original_dates_and_nonstatus_metadata_remain_historical':True,'new_discovery':False,'full_JPAA_article_read':False}
put('current_science/source_record.json',record)
put('current_science/GLOBAL_QUALIFICATIONS.json',{
 'schema':'pr52-current-global-qualifications/v1','utc':utc(),
 'scope':'All nineteen original archive files and all nineteen operative source/proof/ledger/helper/result/review files.',
 'global_rule':'Old PASS, proof hashes, source status/search/visual/PDF/model/runtime/deadline/pending/readiness/publication fields are dated historical evidence, not current acceptance authority. Historical receipts reference archived original proof bodies, not editorial current wrappers.',
 'raw_prior_key_present':False,'raw_prior_key':'OWR-1452-008',
 'selected_sql_report_text':'{}','selected_sql_report_is_SQL_NULL':False,
 'original_prior_report_bytes':'null\n','original_prior_report_decoded':None,
 'source_precision_reference':'../../original_preparation_family/SOURCE_PRECISION_QUALIFICATIONS.md',
 'original_substantive_search_attempts':0,'original_substantive_attempt_limit':5,
 'original_known_theorem_validation_activities':1,'original_response_count_supplied':False,
 'earlier_reconstruction_1_of_5_phrase_is_historical':True,
 'new_substantive_proof_search_attempts':0,'current_text_preparation_math_assertions':0,
 'new_independent_mathematical_family':False,'preparer_reused_from':'divergence_shear_adversary_family',
 'operative_problem_status':'already_solved','new_discovery':False,
 'literal_scope':'Every commutative unital Q-algebra and m,n >=1; existing polynomial automorphisms, determinant exactly1; genuine finite polynomial lift before reduction.',
 'full_JPAA_article_read':False,'human_peer_review':False,'formal_proof_certificate':False,
 'historical_source_PDF_hashes_are_not_new_downloads':True,
 'ROOT_acceptance_authority':False,'native_authority':False,'Git_authority':False,
 'remote_authority':False,'new_paper':False,'new_DOI':False,'tracker_authority':False})
families=[];rows={}
expected_specs=[('original_preparation_family','pr52-original-source-self-closure/v1','422c318a21d8aa912080c64b1cf1bfba45511e643bf8b20dba09eb15efc867a5',194),
 ('divergence_shear_adversary_family','pr52-divergence-shear-self-closure-v1','5bcf514d64da5d3de4bd8b21247f8258ed406584db71b8105655e60639170886',27),
 ('nilpotent_jet_adversary_family','pr52-nilpotent-jet-self-closure/v1','64e5170cf0692357c61fb98f3c494d2e07cd6bba9fa859a637bd595b4db1faa8',25)]
for name,schema,digest,count in expected_specs:
    home=A/name;mf=bind(home/'SELF_MANIFEST.json')
    require(mf['sha256']==digest,'actual predecessor manifest pin')
    value=json.loads((home/'SELF_MANIFEST.json').read_bytes())
    require(value['schema']==schema,'explicit three distinct actual schemas')
    for p in sorted(home.rglob('*')):
        if p.is_file():rows[str(p)]=bind(p)
    dirs=[home]+sorted(p for p in home.rglob('*') if p.is_dir())
    families.append({'path':str(home),'schema':schema,'manifest':mf,'payload_files':count,
                     'directories':[{'path':str(p),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')} for p in dirs]})
caps=[]
for name,pid in [('original_preparation_closure',83035),('original_preparation_closed_readback',83411),
                 ('divergence_shear_closure',2468),('divergence_shear_closed_readback',2863),
                 ('nilpotent_jet_closure',2475),('nilpotent_jet_closed_readback',2865)]:
    home=C/('root_pr52_'+name+'_actual_capture')
    cap=json.loads((home/'CAPTURE.json').read_bytes())
    require(cap['pid']==pid and cap['actual_execution'] is True,'exact six genuine ROOT child PIDs')
    for rel in ('CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'):
        rows[str(home/rel)]=bind(home/rel)
    caps.append({'path':str(home),'actual_pid':pid,'argv':cap['argv'],
                 'invoked_source':bind(Path(cap['argv'][2])),
                 'stdout_typed':json.loads((home/'stdout.bin').read_bytes())})
put('EXTERNAL_BINDINGS.json',{'schema':'pr52-current-lean-external-bindings/v1','utc':utc(),
 'files':[rows[p] for p in sorted(rows)],'closed_families':families,
 'actual_ROOT_captures':caps,'no_input_bodies_copied_except_nineteen_originals':True,
 'no_raw_PDF_or_pixels_copied':True,'native_dated_input_files_are_not_live_native_authority':True,
 'ROOT_personal_read_attestation_supplied_by_preparer':False,'future_acceptance_authority':False})
archive_rows=[];operative_rows=[]
for rel in sorted(originals):
    p=HERE/'original_head_archive'/rel
    archive_rows.append({**bind(p,True),'relative_path':rel,'git_blob_sha1':git[rel],'original_git_mode':'100644'})
for p in sorted((HERE/'current_science').rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(HERE/'current_science').as_posix()
    body=p.read_bytes();same=rel in originals and body==originals[rel]
    diff=None
    if rel in originals and not same:
        diff=''.join(difflib.unified_diff(originals[rel].decode().splitlines(keepends=True),body.decode().splitlines(keepends=True),fromfile='original_head_archive/'+rel,tofile='current_science/'+rel))
    operative_rows.append({**bind(p,True),'relative_path':rel,
                           'change':'retained_literal' if same else ('added_global_qualification' if rel not in originals else 'operative_qualification'),
                           'exact_text_diff_from_original':diff})
put('SCIENCE_INDEX.json',{'schema':'pr52-current-lean-science-index/v1','utc':utc(),
 'original_head':HEAD,'original_archive':archive_rows,'operative':operative_rows,
 'science_file_count':39,'native_or_ROOT_acceptance_authority':False,
 'old_checksum_references_identify_original_archive':True})
count=external();science_count=science()
require(count==273 and science_count==39,'bounded current preparation sizes')
result={'schema':'pr52-current-text-builder-result/v1','status':'PASS_TEXT_ONLY_PREPARATION',
 'utc':utc(),'integrity_checks':COUNTER[0],'science_files':39,
 'literal_original_files':19,'operative_files':20,
 'operative_literal_retained_files':sum(r['change']=='retained_literal' for r in operative_rows),
 'operative_qualified_files':sum(r['change']=='operative_qualification' for r in operative_rows),
 'external_full_body_rows':count,'actual_ROOT_capture_children':[83035,83411,2468,2863,2475,2865],
 'mathematical_helpers_executed':False,'new_mathematical_independence':False,
 'native_Git_remote_paper_or_DOI_changes':False}
put('PREPARATION_READBACK.json',result)
print(json.dumps(result,indent=2,sort_keys=True))
