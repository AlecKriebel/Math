#!/usr/bin/env python3
"""Prepare truthful current edition and a source-body-free portable package."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
EDITION=AUDIT/'current_edition'
PACKAGE=ROOT/'verification'
NAMES=['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']
def binding(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def copy(src,rel):
    dst=PACKAGE/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
def main():
    if not (AUDIT/'PRIORITY_ADJUDICATION.json').exists():raise RuntimeError('Priority adjudication required before edition/package preparation')
    EDITION.mkdir(exist_ok=True);PACKAGE.mkdir(exist_ok=True)
    old=(AUDIT/'submitted/PROOF.md').read_text().split('## Status and exact claim',1)[1]
    old=old.replace('This claim concerns monomials, not every polynomial simultaneously.','This original construction concerns monomials; the separate current argument above handles every polynomial simultaneously.')
    old=old.replace('Theorem 4.1 fixes p before constructing F. It does not assert one F fails\nfor all nonconstant polynomials simultaneously. The monomial assertion\nin Section 3 is the explicitly proved simultaneous special case.','The original Theorem4.1 fixes p before constructing F and establishes no all-polynomial conclusion by itself. The separate current argument above proves simultaneous all-polynomial failure by a different mechanism; no quantifier exchange is used.')
    current=(ROOT/'CURRENT_SIMULTANEOUS_PROOF.md').read_text()
    (EDITION/'PROOF.md').write_text(current+'\n# Retained original fixed-polynomial argument\n\nThe following original argument remains valid. Its scope and historical novelty caveats belong to that original argument; current prior implications and the additional simultaneous theorem are stated above. Full original submitted bytes are separately preserved.\n\n## Original status and exact claim'+old)
    historical=(AUDIT/'submitted/AUDIT.md').read_text().split('\n',1)[1]
    (EDITION/'AUDIT.md').write_text('# Current audit record and retained historical audit\n\nThe original submitted mathematical argument passes fresh root and independent adversarial review without mathematical repair. A source-question-only reconstruction and a separate candidate-aware adversary additionally prove dense simultaneous all-polynomial failure by relative Baire and direct successive-block mechanisms. Two initially independent priority families find positive older implications from Nikula and an earlier Gaussian eigenfield route. Current publication is an attributed historical negative-answer / elementary alternative-proof note, without a new first solution or first existence claim. The dated current reports and fresh exact executables accompany the portable verification package. AI use was extensive; no external human review or formal certification is claimed.\n\n## Historical audit, retained verbatim below\n\nAll first-person inspection, execution, independence and distribution statements in the following historical audit refer to that earlier edition. In particular its statement that publication preparation made no new executions is historical; the current2026-10-17 preparation DID perform fresh source reads and new exact executions, separately recorded in current SOURCES.json and VERIFICATION.json. The historical audit covers fixed-p and monomial claims, not the added simultaneous theorem.\n\n'+historical)
    (EDITION/'README.md').write_text('''# Problem30000921 / OWR-1787-006: attributed negative-answer note

The original PR explicitly claimed a complete negative answer to the pointwise polynomial preservation question and was therefore in scope under the actual-outcome gate. Its mathematics passed fresh extensive review. The current edition additionally proves a dense family of differentiation-hypercyclic entire functions simultaneously defeating every nonconstant complex polynomial, with escaping product derivative evaluations.

Priority audit found positive older implications: Nikula arXiv1209.6209v1 Theorem1 already yields an even stronger frequently hypercyclic conclusion by elementary Gaussian bounds. An earlier general Bayart–Matheron eigenfield theorem also supplies that Gaussian law. The exact multiplier corollary was not located explicitly in a read older source; first explicit recognition and earliest priority remain undetermined. We publish an attributed historical negative answer and self-contained elementary alternative proof, with no new first-solution/current-openness/first-existence claim.

PROOF.md contains the current self-contained simultaneous argument and retained original fixed-p argument. AUDIT.md explicitly separates current and historical reviews. SOURCES.json and VERIFICATION.json distinguish current acts from original historical metadata. ACCEPTANCE.json binds the current documents; MANIFEST.json binds all other seven current edition files. Original submitted bytes are separately captured in SUBMITTED_SNAPSHOT.json and the verification archive, without silently changing old records.

The separate preprint verification archive contains executable stdlib exact diagnostics, new receipts, source-question reconstruction freeze, independent analytic and annular reviews, prior-implication derivations and extensive bounded priority reports. Finite checks corroborate coefficient algebra; the infinite-dimensional conclusions rest on written proofs. Downloaded third-party source bodies and images are not distributed. Historical omitted checks remain metadata, not authenticated replays.

AI tools were used extensively in proof development, source research, independent internal adversarial checking, exact computation and writing. This preprint is unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification is claimed. Publication and sequential fresh whole-package review receipts are kept separately from this mathematical edition.
''')
    (EDITION/'ACCEPTANCE.md').write_text('''# Current mathematical acceptance

Accepted: complete negative answer to historical Costakis Question5 (pointwise multiplication), dense simultaneous all-nonconstant-polynomial failures, and universal polynomial preservers exactly nonzero constants. The original fixed-p null-orbit proof needs no mathematical repair. The added theorem has separately passed relative-Baire and explicit successive-block adversarial review.

Priority status: POSITIVE EARLIER GENERAL IMPLICATION FOUND. Nikula's2012 versioned random-function theorem already implies dense simultaneous frequently hypercyclic counterexamples; the exact-annulus existence also follows after null-orbit clipping. A checked earlier2011 general Gaussian eigenfield specialization supplies another underpinning. The current note is an attributed historical answer / elementary alternative proof. No first resolution, first existence, new mechanism, earliest-priority or current-openness certificate is asserted; the first explicitly printed polynomial corollary was not identified.

The same f defeats all nonconstant p; limit thresholds may depend on p. This is not inferred by exchanging the original fixed-p quantifiers. A residual positive common-preservation family can coexist with the constructed dense meagre exceptional family.

The current mathematical edition and immutable original submitted edition have separate exact bindings. Fresh finite checks, original-question-only reconstruction, candidate-aware reviews, older-implication challenges, and primary-source retrieval scopes are separately reproducible or documented in the verification archive. Source retrieval is not full-source inspection. Historical omitted receipt hashes do not authenticate an unavailable execution.

AI use was extensive. Acceptance is an internal AI audit judgment, not external human peer review, journal acceptance, or formal proof-assistant certification. Whole-package publication reviews and external publication receipts are separate gates.
''')
    sources={'schema':'hypercyclic-current-sources-v1','problem_id':30000921,'historical_submitted_source_record':json.loads((AUDIT/'submitted/SOURCES.json').read_text()),'current_root_source_record':json.loads((AUDIT/'ROOT_SOURCE_RECEIPT.json').read_text()),'current_root_priority_scope':json.loads((AUDIT/'ROOT_PRIORITY_SOURCE_SCOPE.json').read_text()),'fresh_candidate_aware_source_record':json.loads((AUDIT/'reviews/analytic_source_adversary/source_receipt.json').read_text()),'priority_adjudication':json.loads((AUDIT/'PRIORITY_ADJUDICATION.json').read_text()),'distribution':'Authored source/priority records only; no downloaded third-party source bodies. Original recorded historical acts remain historical. Fresh current source reads do not retroactively authenticate all historical omitted receipts.'}
    save(EDITION/'SOURCES.json',sources)
    ver={'schema':'hypercyclic-current-verification-v1','problem_id':30000921,'historical_submitted_metadata':json.loads((AUDIT/'submitted/VERIFICATION.json').read_text()),'current_root_replay':json.loads((AUDIT/'ROOT_REPLAY_RECEIPT.json').read_text()),'current_root_exact_results':json.loads((AUDIT/'ROOT_EXACT_DIAGNOSTICS.json').read_text()),'fresh_source_analytic_review':json.loads((AUDIT/'reviews/analytic_source_adversary/VERDICT.json').read_text()),'control_scope_clarification':'Root exact driver executes three altered algorithm variants. Independent analytic driver uses five deliberately false fault-model predicates on fixed algebra fixtures; these are not five executed mutated programs.','new_executions_during_current_preparation':True,'new_source_inspection_during_current_preparation':True,'analytic_scope':'Finite exact diagnostics corroborate coefficient identities; entire convergence, infinite hypercyclicity, all-polynomial escape, Baire density and Gaussian probability implications are written analytic proofs.','historical_limit':'No replay/authentication claim for unavailable original omitted receipt bodies. Current original bytes and new current driver outputs are independently bound.'}
    save(EDITION/'VERIFICATION.json',ver)
    save(EDITION/'ACCEPTANCE.json',{'schema':'hypercyclic-current-acceptance-v1','problem_id':30000921,'source_problem':'OWR-1787-006','status':'ACCEPT_VALID_ATTRIBUTED_HISTORICAL_NEGATIVE_ANSWER','simultaneous_all_nonconstant_polynomials':True,'ordinary_hypercyclic_elementary_proof':'current self-contained relative Baire; separate direct-block adversary','frequent_hypercyclic_prior_implication':'Nikula2012 theorem plus elementary Gaussian bounds; exact-annulus clipping checked separately','original_fixed_p_proof_mathematical_repairs':[],'priority':'positive older implication; no firstness/new-existence/current-openness claim','first_explicit_multiplier_corollary_priority':'not determined','AI_use':'extensive; unrefereed; no external human peer review/formal certification','current_document_bindings':{n:binding(EDITION/n) for n in ['PROOF.md','AUDIT.md','ACCEPTANCE.md']},'original_submission_head':'3ee95e0e22a7bb21d7d08e3c4dcd40f60dfd47c3','original_submission_snapshot':'SUBMITTED_SNAPSHOT.json','publication_gate':'separate exact preprint/archive and sequential fresh package review/publication receipts'})
    save(EDITION/'MANIFEST.json',{'schema':'hypercyclic-current-edition-manifest-v1','members':NAMES,'entries':[{'file':n,**binding(EDITION/n)} for n in NAMES if n!='MANIFEST.json'],'self_hash_excluded':'MANIFEST.json'})
    save(EDITION/'CURRENT_EDITION_BINDINGS.json',{'files':{n:binding(EDITION/n) for n in NAMES},'original_snapshot':json.loads((AUDIT/'SUBMITTED_SNAPSHOT.json').read_text())})
    for n in NAMES:copy(EDITION/n,'current_edition/'+n);copy(AUDIT/'submitted'/n,'original_submitted/'+n)
    for n in ['SUBMITTED_SNAPSHOT.json','MATH_GATE.json','ROOT_ANALYTIC_REVIEW.md','ROOT_EXACT_DIAGNOSTICS.json','ROOT_REPLAY_RECEIPT.json','ROOT_SOURCE_RECEIPT.json','ROOT_PRIOR_IMPLICATION.md','ROOT_PRIORITY_SOURCE_SCOPE.json','PRIORITY_ADJUDICATION.json']:
        copy(AUDIT/n,'provenance/'+n)
    copy(AUDIT/'root_diagnostics.py','diagnostics/root_diagnostics.py')
    copy(ROOT/'manuscript/main.tex','manuscript/main.tex');copy(ROOT/'CURRENT_SIMULTANEOUS_PROOF.md','CURRENT_SIMULTANEOUS_PROOF.md')
    for family in ['source_question_family','analytic_source_adversary','annular_baire_adversary','nikula_corollary_adversary']:
        folder=AUDIT/'reviews'/family
        for p in sorted(folder.rglob('*')):
            if not p.is_file() or any(v in {'sources','__pycache__','_local'} for v in p.relative_to(folder).parts):continue
            if p.suffix not in {'.md','.json','.py'} and p.name not in {'SHA256SUMS','.gitignore'}:continue
            copy(p,'reviews/'+family+'/'+p.relative_to(folder).as_posix())
    for p in sorted((AUDIT/'priority').rglob('*')):
        if p.is_file() and not any(v in {'sources','__pycache__','_local'} for v in p.relative_to(AUDIT/'priority').parts) and p.suffix in {'.md','.json','.py','.jsonl'}:
            copy(p,'priority/'+p.relative_to(AUDIT/'priority').as_posix())
    print(json.dumps({'current_edition_files':len(NAMES),'portable_files':sum(p.is_file() for p in PACKAGE.rglob('*'))}))
if __name__=='__main__':main()
