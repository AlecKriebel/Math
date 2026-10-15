"""Prepare an explicit-scope native integration draft for whole-package review."""
from pathlib import Path
import datetime,hashlib,json,shutil
A=Path(__file__).resolve().parent;P=A/'publication_package_v1';D=A/'integration_preparation/native_template_pending_01';D.mkdir(parents=True,exist_ok=False);t=datetime.datetime.now(datetime.UTC).isoformat()
def write(n,s):
 p=D/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def copy(p,n):
 q=D/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
original=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
for x in original['files']:
 p=A/'original_submission/files'/x['path'];b=p.read_bytes()
 if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:raise RuntimeError('Original pin drift')
 rel=Path(x['path']).relative_to('unsolved_math_prioritization/attempts/5000007').as_posix();copy(p,'historical_original/'+rel)
copy(A/'CURRENT_PROOF.md','PROOF_V2.md')
for n in ['check_certificate.py','check_half_turn.py','test_reconstruction.py']:copy(A/'current_verification'/n,n)
for p in (A/'current_verification').iterdir():
 if p.is_file():copy(p,'verification/current/'+p.name)
copy(A/'exact_reproduction_adversary/independent_exact.py','independent_review/reviewer_exact_check.py')
copy(A/'root_independent_replays_02/exact_reproduction_adversary_normal.stdout.json','independent_review/reviewer_exact_check_output.json')
copy(A/'root_verification_runs/check_certificate_normal.stdout','check_certificate_output.json')
copy(A/'root_verification_runs/check_half_turn_normal.stdout','check_half_turn_output.json')
raw=json.loads((A/'ROOT_UPSTREAM_TARGET_AND_PRIOR_01.json').read_text())['files'][0]['selected'];prior=json.loads((A/'ROOT_UPSTREAM_PRIOR_LOOKUP_CORRECTION_02.json').read_text())['selected_prior_report']
write('source_record.json',json.dumps(raw,indent=2)+'\n');write('prior_imported_report.json',json.dumps(prior,indent=2)+'\n')
interpretation={'original_target':'Bare beta-alpha=2pi/5 exclusion at graphdistance2','literal_answer':'FALSE, exactly two direct proper face diagonals per initial face/vertex','adopted_class':'Edges or non-edge even-N short paths with transported boundary beta-alpha=2pi/5','adopted_class_answer':'PROVED endpoints cannot have graphdistance2','source_author_authenticated_erratum':False,'unique_author_intent_certified':False,'classical_mechanism':'AAH virtual-Weierstrass/midpoint reversal; Troubetzkoy refolding antecedent','exact_current_overlap':'Ferudun AMR-049 DOI10.5281/zenodo.23267641 current primary manuscript','historical_priority_or_independence_certified':False,'original_historical_effort':'unknown/5 (interrupted)','native_stage':'Prepared draft for whole-package review; no publication or PR disposition yet'}
write('source_interpretation.json',json.dumps(interpretation,indent=2)+'\n')
write('README.md',"""# 5000007: two formulations of the dodecahedral endpoint question

The imported bare-angle exclusion is false: exactly the two direct proper face diagonals per fixed initial face and vertex are additional paths at graph distance2. The expressly adopted parity-selected A0 convention has a complete unbounded exclusion proof. [Current proof](PROOF_V2.md) states both results and the interpretation limit; it is not an affirmative proof of the unqualified imported sentence or an authenticated author erratum.

Classical midpoint symmetry is credited to Athreya–Aulicino–Hooper and Troubetzkoy. Ferudun's current AMR-049 preprint, DOI10.5281/zenodo.23267641, overlaps the two formulations and public face-word A1 correction. Our draft PR creation01Oct and the related DOI registration09Oct are documented with historical visibility/version/awareness limits. Nofirstness, guaranteed novelty, present openness or independence certification is made.

Current first-party scripts use optimization-safe guards. Run Python3.11+:

    python3 -B check_certificate.py
    python3 -B check_half_turn.py
    python3 -B independent_review/reviewer_exact_check.py
    python3 -B verification/current/run_verification.py

[Research-note package](../../../draft_pr_publication_program_20260930/audits/pr190_5000007/publication_package_v1/) includes the four-page paper, exact supporting data, distinct independent scientific audits and bounded priority ledgers. It is prepared for the required successive NEW whole-package adversarial reviews. This native template makes no completed publication/merge/tracker claim.

historical_original/ preserves all22 immutable original artifacts, including superseded scope phrasing, unsafe guards, draft-only receipt and prior reviews. Raw source_record.json and prior_imported_report.json are historical dataset records; their open-status/triage claims are not present-day acceptance. Current interpretation is separate. Historical effort remains unknown/5(interrupted), without a new budget or rewritten state history.

Extensive AI was used; the work is unrefereed and has not undergone conventional human peer review.
""")
write('CANDIDATE_PROOF.md',"""# Current and historical proof custody

The current explicitly qualified two-part proof is PROOF_V2.md. The recovered original candidate is preserved byte-for-byte under historical_original/CANDIDATE_PROOF.md and the original V2 under historical_original/PROOF_V2.md. Neither historical description is a present-day priority or publication certificate. Current core mathematics is independently audited; complete-package reviews and actual publication/disposition remain pending in this prepared native template.
""")
write('LITERATURE_CHECK.md',"""# Completed bounded priority audit; historical priority not certified

AAH2018v1/2019v2 supplies the translation cover and virtual-Weierstrass midpoint rotational reversal. Troubetzkoy2022v3 supplies the related elementary refolding argument for the other four solids. The current Ferudun AMR-049 manuscript, DOI10.5281/zenodo.23267641, contains a checkable overlapping theorem, parity/diagonal distinction and16-face A1 correction. These results are credited explicitly; no new symmetry mechanism or certified theorem novelty is claimed.

GitHub records PR190 creation2026-10-01T04:03:35Z. The initial artifact commit contains the authenticated original V2. DataCite records related DOI registration2026-10-09T17:25:41Z. Commit dates/current public visibility do not certify historical exact-byte visibility or awareness/independence. Current website and DOI-deposited file equality remains unverified403.

AAH/Troubetzkoy journal-version bodies were not compared to read preprints. Fuchs2014 body remained unavailable; Veech originals were not read by these primary families. Current citation indexes were demonstrably incomplete. Failed searches do not establish openness/firstness. Exact source versions/read depth and bounded queries are in the case priority-family reports and package; the original limited search is retained under historical_original/.
""")
write('EXTERNAL_CERTIFICATE_AUDIT.md',"""# Exact pinned-artifact audit

Commit7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9 proof text was independently authenticated via raw HTTPS and GitHub API, SHA25684baf6ab43b2c33c7a1b11e50e47fe2b48d891da981f44da9da18f4a5ba60513.

The literal16-face word independently reconstructs a legal vertex-to-first-vertex path of graphdistance2 and squared unit-edge length(307+137sqrt5)/2. All15 interior crossings and first-vertex tests pass. The transported terminal ray is2->16(216deg), whereas the outward physical-face ray2->10 is108deg. Figure8's supplement gives beta-alpha144deg, A1 under the adopted convention.

Separately, displayed eta=e^(i*pi/5), A=(31+13sqrt5)/2, B=-17-8sqrt5 have norm(425+189sqrt5)/2, not the advertised norm. Difference59+26sqrt5. This is an internal coordinate identity defect; valid reconstructed face-word geometry is preserved. Current PROOF_V2 and verification include both distinctions, with no claim about people or authorship.
""")
write('SIMPLIFICATION_NOTE.md',"""# The graph obstruction

The universal proof needs no finite trajectory enumeration. Once the midpoint physical half-turn exchanges endpoints, a distance2 pair would force its unique common neighbor to be fixed (dodecahedral girth5). A nonidentity half-turn fixes no vertex, whose rotational stabilizer has order3. Current exact enumerations corroborate15 distinct axes indexed by30 edges; they are not a premise replacing the analytic proof.
""")
write('independent_review/FINAL_REVIEW.md',"""# Current explicit-scope scientific review summary

Three newly assigned source-first independent families accepted the unbounded parity-selected theorem and exhaustive two-diagonal literal-angle counterexamples. The original imported bare-angle sentence is false; no author-authenticated source correction or unique intended definition is certified. Exact reproduction independently validates the face word and detects both its transported-type issue and displayed-coordinate norm inconsistency.

All28 canonical scientific assert guards were independently transformed into explicit raises and verified with ordinary/optimized baselines and meaningful wrong-science controls. The current reviewer_exact_check.py is the new independent exact implementation, not the historical reviewer script. Original review artifacts remain under historical_original/independent_review/.

Two completed independent deep bounded priority audits authenticate classical inputs and current Ferudun overlap, retaining exact body/version/chronology gaps. They do not certify firstness, novelty, current openness or author independence. Full publication-package reviews remain pending in this native preparation. Scientific/priority evidence is at draft_pr_publication_program_20260930/audits/pr190_5000007.
""")
write('independent_review/REVIEW_V1.md','Historical reviewV1 is retained unchanged at ../historical_original/independent_review/REVIEW_V1.md; current scientific scope is documented in FINAL_REVIEW.md and PROOF_V2.md.\n')
write('PUBLICATION_RECEIPT.md',"""# Draft chronology and publication boundary

GitHub records the original draft PR190 as created2026-10-01T04:03:35Z. The initial artifact commit c9162a45d30120b10b42b1f79c50bab417ed287b contains the original V2 proof, SHA256f96288e95c946731091989cea3eb087829c94cf966898dae792122567da3f16b. Original head0c3346c8ebcb3b967a1d8bf9a283f027b44b738c is preserved.

The exact qualified note packet is prepared for successive NEW whole-package adversarial reviews. This native draft has no completed Zenodo publication, tracker or merge receipt. Actual acceptance must be recorded separately after the required gates. Historical draft-only receipt is retained under historical_original/PUBLICATION_RECEIPT.md.
""")
write('recovery_manifest.json',json.dumps({'target_id':'5000007','original_PR':190,'original_head':'0c3346c8ebcb3b967a1d8bf9a283f027b44b738c','historical_attempt':'previously started/interrupted; lost turn count unknown and nonzero','historical_turn_count':None,'historical_turn_lower_bound':1,'new_five_turn_budget_created':False,'current_result':interpretation,'original_recovery_manifest':'historical_original/recovery_manifest.json','state_json_or_history_rewritten':False,'UTC':t},indent=2)+'\n')
old=(A/'original_submission/files/unsolved_math_prioritization/attempts/5000007/RESEARCH_LOG.md').read_text()
write('RESEARCH_LOG.md',old+'\n\n'+t+' — Publication workflow62%: three new scientific-family audits and Root exact controls accept qualified two-part result; deep priority audits authenticate classical inputs and contemporary exact overlap, with explicit limits. Original budget unknown/5 retained. Four-page exact packet protected for successive NEW whole-package reviews; no publication/tracker/merge claim in this pending native template.\n')
pins={p.relative_to(D).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file()}
write('independent_review/reviewed_hashes.json',json.dumps({'UTC':t,'PROOF_V2_SHA256':pins['PROOF_V2.md']['sha256'],'check_certificate_SHA256':pins['check_certificate.py']['sha256'],'check_half_turn_SHA256':pins['check_half_turn.py']['sha256'],'reviewer_exact_check_SHA256':pins['independent_review/reviewer_exact_check.py']['sha256'],'scope':'Current explicit qualified science; package review/publication stillpending'},indent=2)+'\n')
pins={p.relative_to(D).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file()}
for p in D.rglob('*'):
 if p.is_file():p.chmod(0o444)
pointer={'UTC':t,'current_template':D.name,'status':'PENDING_WHOLE_PACKAGE_REVIEW_NOT_INTEGRATED','original_head':'0c3346c8ebcb3b967a1d8bf9a283f027b44b738c','files':pins,'package':'publication_package_v1','publication_ready':False,'original_historical_files':22}
(A/'integration_preparation/CURRENT_TEMPLATE.json').write_text(json.dumps(pointer,indent=2)+'\n')
pr={'title':"5000007: two formulations of Fuchs's dodecahedral endpoint question",'body':"The imported bare-angle graph-distance-two exclusion is false by exactly two proper face diagonals. The expressly adopted parity-selected class has a complete unbounded endpoint-exclusion proof. The source interpretation is qualified; no authenticated author erratum or uniquely forced printed reading is claimed.\\n\\nThe note credits AAH's classical midpoint mechanism, Troubetzkoy's refolding antecedent, and Ferudun's current contemporaneous overlapping theorem/formulation/witness-type correction. Exact reproduction distinguishes the valid16-face word from terminal-angle and displayed-coordinate certificate errors; current guards survive optimization with meaningful negative controls. Three fresh source-first scientific audits and two bounded priority audits are recorded; firstness, historical public visibility, source-version identity and author independence remain uncertified.\\n\\nThe exact four-page paper and supporting packet are prepared for the required successive new whole-package adversarial reviews. Extensive AI was used; unrefereed, no conventional human peer review. Actual Zenodo/tracker/merge acceptance must be appended only after those actions succeed.",'state':'CONCRETE_REVIEW_PROPOSAL_NOT_SENT'}
pr['body']=pr['body'].replace('\\n','\n')
(A/'PR_METADATA_PROPOSAL_01.json').write_text(json.dumps(pr,indent=2)+'\n')
tracker={'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,'tab':'Math Puzzles','columns':{'A':'Fuchs Conjecture3.2 /5000007: distinguish false bare-angle exclusion from adopted parity-selected endpoint theorem','B':'','C':'Actual DOI URL assigned after authorized publication; none invented','D':'Qualified two-part research note. Classical AAH/Troubetzkoy mechanisms and Ferudun current contemporaneous overlap credited. Nofirstness/authenticated source erratum/current openness or independence certification; chronology/version gaps explicit. Exact current controls and pinned-coordinate norm inconsistency. Extensive AI; unrefereed.'},'state':'REVIEW_PROPOSAL_NOT_APPENDED'}
(A/'TRACKER_ROW_PROPOSAL_01.json').write_text(json.dumps(tracker,indent=2)+'\n')
print(json.dumps({'status':'CONCRETE_NATIVE_AND_EXTERNAL_METADATA_REVIEW_DRAFT_PREPARED','native_files':len(pins),'originals_retained':22,'remote_mutations':0}))
