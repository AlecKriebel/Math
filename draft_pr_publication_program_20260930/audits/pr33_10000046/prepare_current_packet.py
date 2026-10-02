"""Freeze a prospective corrected partial packet; never change shared inputs."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone

A = Path(__file__).resolve().parent
ROOT = A.parents[2]
C = A / 'reviewed_candidate'
assert not C.exists(), 'An existing frozen candidate must not be overwritten.'
UTC = datetime.now(timezone.utc).isoformat()
HEAD = 'de5877c38bf3604f0a8e074af7a9c55fca334522'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
def bound(p, base, role=None):
    d = dict(path=p.relative_to(base).as_posix(), bytes=p.stat().st_size, sha256=sha(p))
    if role:
        d['role'] = role
    return d

shutil.copytree(A / 'source_snapshot', C)
shutil.copyfile(C / 'PARTIAL.md', C / 'ORIGINAL_PARTIAL.md')
shutil.copyfile(C / 'readiness.json', C / 'ORIGINAL_readiness.json')
metadata = json.loads((A / 'pr_input.json').read_text())
(C / 'ORIGINAL_PR_BODY.md').write_text(metadata['body'])
original = (C / 'PARTIAL.md').read_text()
marker = '## A precise finite-transport formulation\n'
prefix, finite = original.split(marker, 1)
old_final = 'The combined target stays unresolved, with credited four-dimensional prior progress.'
new_final = ('The combined target stays unresolved. The four-dimensional preprint is credited for '
             'its stated intended theorem; a complete independently checked proof, including '
             'corrected quantitative estimates and initialization for arbitrary fixed starts, '
             'is not supplied by this package.')
assert finite.count(old_final) == 1
finite = finite.replace(old_final, new_final)
new_prefix = '''# 10000046: verified finite transport partial; three-dimensional gap

**Outcome: unsolved.** The standard finite transport and compactness reformulation and the elementary bounds below are verified. They do not decide the three-dimensional question. A 2024 preprint states the intended four-dimensional result, but this package does not certify its complete proof. No novel resolution, paper or DOI is claimed.

## Exact target and scope

[Benjamini, *Coarse Geometry and Randomness*](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf), dated October 30, 2013, Open Problem 12.33 on printed/PDF p.104, asks about couplings of simple random walks in dimensions 3 or 4, starting at graph distance 10, with positive probability of disjoint paths. Page 5 defines nearest-neighbour simple random walk and graph distance. The recovered archived author PDF and rendered question were checked. This package records separate dimension-3 and dimension-4 components and treats every pair of starts at lattice distance ten; the latter is an explicit stronger interpretation of the terse question.

Fix x,y in Z^d with l1 distance ten, and the laws mu_x,mu_y of the complete walks, including time zero. The desired coupling must give strictly positive probability to X_i != Y_j for **every** i,j >= 0. Both entire marginal path laws must have iid uniform nearest-neighbour increments. Correct one-time distributions alone do not suffice. Simultaneous avoidance X_n != Y_n is weaker than the full-range condition. No joint Markovian or co-adapted restriction is imposed by the source.

## Current literature qualification

[Benjamini–Kozma, *Coupled but distant*](https://arxiv.org/abs/2412.16600v1), December 21, 2024, states a positive four-dimensional theorem on p.2 and leaves dimension three unresolved in its introduction. Its definitions include initial vertices and intersections at unequal times, and its final proof writes a fixed nonzero starting displacement. It uses Hall matching and annular coupling. These are statements and proof intentions of that preprint, not a complete proof certificate supplied here.

The independent probability audit read the complete main proof and appendix against the freshly retrieved v1 PDF and TeX. It found more literal auxiliary-statement errors than the original package listed: reversed exceptional-event polarity, the wrong alphabet normalization, omitted path losses and strict Hall margins, singular good-time kernels at returns, undefined or overrun near-exit times, negative spatial-logarithm bounds, temporal multiplicity in a trace count, boundary conventions and conditioning issues. The conditional Hall repair and averaged final recursion check out **assuming** corrected quantitative lemmas and initialization. Corrected good-time/rare-hittability estimates (Lemmas 5/6), the old-prefix estimate (Lemma 9), and the required arbitrary-fixed-start initialization remain unverified here. These gaps do not refute the intended theorem; they prevent an unqualified assertion that this audit has established the four-dimensional result.

[Lawler–Limic, *Random Walk: A Modern Introduction*](https://math.uchicago.edu/~lawler/srwbook10.pdf), Theorem 4.3.1, Lemma 6.3.7 and Theorem 6.3.9, supports the regularized Green/hitting and exterior-boundary estimates with its stated hypotheses. That book is different from Lawler's *Intersections of Random Walks*, cited by the preprint for initialization. Neither the conditional repair nor this source check supplies the missing full quantitative certificate. See CURRENT_SOURCE_QUALIFICATION.md and the closed probability audit for exact locations and distinctions.

The bounded search did not locate a verified three-dimensional solution. [Shi et al., *Intersection Exponents of Simple Random Walks in Two and Three Dimensions*](https://arxiv.org/abs/2609.25968v1), September 2026, studies independent-walk numerical exponents, not unrestricted couplings. Its computations are not certified by this package. The upstream OPEN-TRIAGE report is retained as historical source metadata; it missed the 2024 preprint and is not evidence that all dimensions have no prior progress or that worldwide current openness has been proved.

'''
(C / 'PARTIAL.md').write_text(new_prefix + marker + finite)
assert (C / 'PARTIAL.md').read_text().split(marker, 1)[1].replace(new_final, old_final) == original.split(marker, 1)[1]

roots = [
    'ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json', 'ROOT_SOURCE_RETRIEVAL.json',
    'ROOT_BOOK_SOURCE_RETRIEVAL.json', 'ROOT_PRIMARY_COMPARISON_FAILURE.json',
    'ROOT_PROBABILITY_REPLAY_SETUP_FAILURE.json', 'ROOT_PROBABILITY_REPRODUCTION.json',
    'ROOT_TRANSPORT_PRIMARY_REPRODUCTION.json', 'ROOT_RECONSTRUCTION.md',
    'ROOT_SCOPE_CHECKPOINT.json']
family_manifests = [('transport_family', 'FINAL_MANIFEST.json'),
                    ('primary_scope_family', 'MANIFEST.json'),
                    ('probability_prior_family', 'FILE_MANIFEST.json')]
deps = []
for folder, name in family_manifests:
    m = A / folder / name
    d = json.loads(m.read_text())
    for item in d['files']:
        p = A / folder / item['path']
        assert p.is_file() and sha(p) == item['sha256'] and p.stat().st_size == item['bytes']
        deps.append(bound(p, A, 'closed_family_first_party_or_selected_raw_record'))
    deps.append(bound(m, A, 'closed_family_manifest'))
assert len(deps) == 44
seal = {'utc': UTC, 'scope': 'Root universal reconstruction and actual replays, original partial only; current package needs a new adversary.',
        'files': [bound(A / n, A) for n in roots] + [bound(A / f / n, A) for f, n in family_manifests],
        'original_head': HEAD, 'new_substantive_attempts': 0,
        'root_manual_annotations_are_not_program_output': True}
js(A / 'ROOT_RECONSTRUCTION_SEAL.json', seal)
for n in roots + ['ROOT_RECONSTRUCTION_SEAL.json']:
    deps.append(bound(A / n, A, 'root_proof_or_actual_reproduction_and_scope_receipt'))
for n in ['snapshot_manifest.json', 'ORIGINAL_COMPARISON.json', 'pr_input.json', 'pr_input/pr.json', 'pr_input/diff.patch']:
    deps.append(bound(A / n, A, 'frozen_original_git_metadata'))
for p in sorted((A / 'source_snapshot').rglob('*')):
    if p.is_file():
        deps.append(bound(p, A, 'immutable_original_numeric_artifact'))
assert len(deps) == 72 and len({d['path'] for d in deps}) == 72
js(C / 'CURRENT_PROOF_DEPENDENCIES.json', {'utc': UTC, 'base': '../', 'scope': 'Exact closure: 41 family members + 3 closed manifests + 10 root artifacts + 5 original metadata members + 13 original numeric artifacts.',
                                         'foreign_pdfs_and_full_upstream_files': 'Ignored local inputs, not first-party findings; source bytes/locations recorded in receipts.', 'files': deps})
shutil.copyfile(A / 'ROOT_RECONSTRUCTION.md', C / 'CURRENT_COMPLETION_PROOF.md')

queue = ROOT / 'unsolved_math_prioritization/QUEUE.md'
qb = queue.read_bytes()
lines = qb.decode().splitlines(keepends=True)
headers = [l for l in lines if l.startswith('| Rank |')]
assert len(headers) == 1
names = [x.strip() for x in headers[0].strip().split('|')[1:-1]]
assert names == ['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
rows = [(i,l) for i,l in enumerate(lines) if l.startswith('| ') and len(l.split('|')) == 14 and l.split('|')[2].strip().startswith('10000046 / ')]
assert len(rows) == 1
i, row = rows[0]
parts = row.rstrip('\n').split('|')
before = dict(zip(names, [x.strip() for x in parts[1:-1]]))
assert before['Status'] == 'queued' and before['Turns'] == '0/5'
note = ('2026-10-02: Audited standard finite/infinite full-path transport equality and elementary bounds; no uniform 3D Hall bound. Benjamini–Kozma v1 states the intended 4D result, but corrected quantitative estimates and arbitrary-fixed-start initialization are not independently certified here. Combined target unsolved; original1/5, verification0. Partial acceptance pending fresh complete gate. PR: https://github.com/AlecKriebel/Math/pull/33.')
for key, val in {'Status':'unsolved','Turns':'1/5','Findings':note}.items():
    parts[names.index(key)+1] = ' '+val+' '
after = '|'.join(parts)+'\n'
for key in names:
    if key not in ('Status','Turns','Findings'):
        assert parts[names.index(key)+1] == row.rstrip('\n').split('|')[names.index(key)+1]
ql = lines[:]
ql[i] = after
js(C / 'CURRENT_QUEUE_PATCH.json', {'utc': UTC, 'phase': 'prospective only; fresh full gate then accepted wording required before merge',
                                   'whole_queue_preimage_sha256': hashlib.sha256(qb).hexdigest(),
                                   'whole_queue_prospective_sha256': hashlib.sha256(''.join(ql).encode()).hexdigest(),
                                   'header_names': names, 'row_before': row, 'row_prospective': after,
                                   'allowed_named_changes': ['Status','Turns','Findings'],
                                   'all_other_lines_and_fields_byte_preserved': True})
raw = json.loads((C / 'source_record.json').read_text())
prior = json.loads((C / 'prior_report.json').read_text())
js(C / 'CURRENT_SOURCE_CONTEXT.json', {'utc': UTC, 'id':10000046, 'problem_number':'AMR-099-0046',
                                     'raw_source_record_sha256':sha(C / 'source_record.json'),
                                     'raw_separate_prior_report_sha256':sha(C / 'prior_report.json'),
                                     'review_hash': '7113131d180ad4fc26f7c07dfcd858a7a4d2a8a66d520478b0b2105ca126e8f3',
                                     'statement_hash':'843571f90f1db50ceea703161b9882e11f19ad0a8c48fbb85e0a889538d013a0',
                                     'raw_status':raw['status'], 'raw_prior_classification':prior['classification'],
                                     'qualification': 'Historical exact imported record/report pair, not a solution certificate or global openness verdict; complete pinned importer serialization independently checked.',
                                     'current_main': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                                     'current_queue_named_row': before, 'original_attempts':'1/5',
                                     'new_substantive_attempts':0})
(C / 'CURRENT_SOURCE_QUALIFICATION.md').write_text('''# Current source and proof boundaries

The original source_record.json and separate prior_report.json are unchanged historical imported objects. Exact review/statement binding and unique ID/code were checked against both complete pinned upstream files and the actual SQLite importer serialization. Their OPEN-TRIAGE labels and source-side metadata are not mathematical truth. The original model/reasoning fields are self-reported. The current PARTIAL.md is edited and has a new hash; no old verdict is transferred to it.

Benjamini's October 2013 Problem 12.33, p.104, and standing SRW/distance conventions, p.5, are the literal target. Arbitrary complete path-law couplings, initial vertices and all unequal times are retained. This package explicitly treats all starts at l1 distance ten. It records separate dimension-3 and dimension-4 components of the source's terse “or” wording.

Benjamini–Kozma arXiv:2412.16600v1 states the intended four-dimensional theorem. The full main proof/appendix and source were independently read by the probability family. Several literal auxiliary assertions fail; the conditional architecture can be repaired, but the corrected quantitative Lemmas5/6 and9 and arbitrary-fixed-start initialization are not certified. Credit the stated theorem and intended progress without asserting that this audit establishes a full4D proof or refutes the intended result. See probability_prior_family/PRIOR_AUDIT.md in CURRENT_PROOF_DEPENDENCIES.json for precise falsifiers and dependencies. No verified three-dimensional solution was located in a bounded search; this is not worldwide exhaustive nonfinding.

Lawler–Limic's author book, Theorem4.3.1/proof, Lemma6.3.7/proof and Theorem6.3.9/proof, supports the regularized hitting and exterior-boundary estimates. Starts and boundary conventions matter. It is not Lawler's Intersections of Random Walks, used by the preprint for initialization; no theorem-number substitution is legitimate. Shi et al. arXiv:2609.25968v1 concerns independent-walk numerical exponents and does not settle the coupling target; its experiments are not certified here.

Foreign PDFs/TeX and entire upstream datasets stay ignored local inputs. Fresh retrieval receipts bind exact URL, version, size and SHA256. The original thirteen numeric files and old reviews are immutable archives. Exact replays and extensive finite tests support those diagnostics, not every adjacent assertion or any uniform infinite estimate. Current proof acceptance requires a new full-package adversary.

The three original families independently sealed their reconstructions before old reviews/root or sibling conclusions. Root then read the complete reports and actual diagnostic programs and replayed them in private copies. Every actual output field is compared; manually appended final-stage provenance annotations are separately qualified. Both root comparison/setup failures are preserved. Historical main snapshots remain dated; the separate named-column correction on main has fixed Chat/Findings errors in previously accepted24–31. OriginalPR33 always placed its note correctly in Findings.

The original single substantive transport route remains blocked at the equivalent unsupported uniform Hall-deficiency estimate. Verification adds zero turns. Prospective unsolved1/5 acceptance permits no new preprint, DOI, release or publication-sheet row. The current main target remains queued0/5 until a clean fresh full gate and guarded integration; no accepted-state history has been fabricated.
''')
(C / 'review/CURRENT_NOTICE.md').write_text('''# Historical review scope

All original review files are byte-unchanged. Their reviewed_sha256 refers to ORIGINAL_PARTIAL.md (also preserved in source_snapshot/PARTIAL.md), not the edited current PARTIAL.md. Historical PASS_PARTIAL and no-required-corrections conclusions do not certify the current candidate. Original pending/no-PR readiness and original PR-body scope/no-merge wording are preserved as archives; current user authorization and administrative files supersede them. Three original-stage families and root reconstruction precede a new complete current gate; that gate is pending.
''')
(C / 'CURRENT_AUDIT_SCOPE.md').write_text('''# Prospective complete partial acceptance

Original head de5877c38bf3604f0a8e074af7a9c55fca334522, base c6975ca76f9f667f1250ba403d0e6da2aafe14d0: thirteen numeric artifacts and fourteen changed paths including QUEUE.md. Original1/5, verification0. Combined and three-dimensional targets unsolved. The finite transport proof/bounds are unchanged except the final four-dimensional attribution sentence; current literary and administrative qualifications are edited. All original bytes are archived and closed-family seals are preserved.

CURRENT_PROOF_DEPENDENCIES.json binds the exact original/family/root closure. MANIFEST.json binds the whole edited current packet and is self-excluding. Universal deduction and finite diagnostics have separate roles. No new paper or DOI is justified. Current readiness is prospective: a new complete adversarial review must read and test this edited candidate before any merge, accepted source-state mirror or body acceptance wording. Preserve all unrelated queue rows and target Chat/DOI/rank/source fields by named header mapping. Legacy eight-column rank()/cache helpers are only investigated in private control copies and never run on live inputs.
''')
status = {'utc':UTC,'id':10000046,'pr':33,'original_head':HEAD,
          'current_gate':'pending_NEW_complete_whole_current_packet_adversary',
          'queue_status_proposed':'unsolved','original_budget':'1/5','new_attempts':0,
          'workflow_completion_estimate_percent':75,'full_target_resolved':False,
          'four_dimensional_full_proof_independently_certified':False,'paper_doi_tracker':'none'}
js(C / 'current_status.json', status)
readiness = json.loads((C / 'ORIGINAL_readiness.json').read_text())
readiness.update(status)
readiness.update(status='unresolved_stalled', independent_review='original_three_families_and_root_complete; NEW_complete_current_gate_pending',
                 publication='No paper, DOI or tracker row; prospective partial merge after clean new gate.',
                 artifact_sha256=sha(C / 'PARTIAL.md'),
                 exact_claim='For each dimension3 and4 and every pair at lattice distance ten: strictly positive full-range avoidance with both entire SRW marginals. Source has terse “or”; all-pair scope is explicit package interpretation.',
                 current_scope='Edited literature qualification plus unchanged finite theorem/bounds; archives and complete dependencies bound.',
                 remaining_gap='Uniform positive three-dimensional finite-path avoidance mass, or proof it vanishes; complete corrected four-dimensional prior-proof certificate not supplied.',
                 prior_attempt_gap='Raw upstream web/arXiv OPEN-TRIAGE only; actual one substantive route preserved. No new original problem attempt in this audit.')
js(C / 'readiness.json', readiness)
(C / 'README.md').write_text('''# PR33 current finite transport partial

Read PARTIAL.md for the universal finite/infinite transport equality, elementary bounds and exact unresolved gap. The combined target is unsolved. The four-dimensional preprint is credited for its intended theorem; a complete corrected proof is not certified here. No novelty, preprint or DOI is claimed.

CURRENT_COMPLETION_PROOF.md reconstructs the deduction and acceptance boundary. CURRENT_SOURCE_QUALIFICATION.md and CURRENT_SOURCE_CONTEXT.json qualify sources and historical metadata. CURRENT_PROOF_DEPENDENCIES.json binds the closed original-family/root support; MANIFEST.json binds the edited current packet. ORIGINAL_PARTIAL.md, ORIGINAL_readiness.json and ORIGINAL_PR_BODY.md preserve superseded originals; unchanged review files apply only to ORIGINAL_PARTIAL.md. RESEARCH_LOG.md and turns.jsonl are historical original records; CURRENT_RESEARCH_LOG.md records this audit.

Both original diagnostics were replayed byte-exact. New independent transport certificates/tamper controls, complete-word-law countermodels and6993 probability controls were also actually reproduced in private copies. Check counts do not prove the unresolved uniform estimate. Python3.10+ is required by the new transport code's int.bit_count; Python3.14.6 was used by root. These codes are finite diagnostics, with no extra mathematical dependencies or external outreach.

Original1/5; verification0. The new complete edited-package adversarial gate is pending; prospective QUEUE.md changes affect only named Status, Turns and Findings, preserving every unrelated field/row. Partial merge and a source-bound accepted-state mirror follow only a clean full gate. No paper, Zenodo deposition or publication-sheet entry for this unsolved result.
''')
(C / 'pr_body.md').write_text('''The combined random-walk coupling target remains unsolved. This package proves the standard finite matching/Hall-deficiency equality for optimal full-path avoidance, its compactness limit and elementary bounds. It supplies no uniform three-dimensional positive bound.

The current literature account credits Benjamini–Kozma v1 for its stated intended four-dimensional theorem while recording the unverified corrected quantitative lemmas and arbitrary-fixed-start initialization. Literal auxiliary-statement errors do not refute the intended theorem. Independent-walk numerical exponents and historical OPEN-TRIAGE metadata do not settle unrestricted coupling.

Original thirteen numeric artifacts and fourteen changed paths, including the correctly named Findings queue edit, are frozen at de5877c38bf3604f0a8e074af7a9c55fca334522. Edited PARTIAL/readiness and current administrative scope preserve all original bytes in archives. Three independent original-stage families, universal root reconstruction and actual byte-bound replays precede a NEW complete edited-package gate, which is pending. Original1/5, verification0. Prospective acceptance is an unsolved partial without a paper, DOI or tracker row. Guarded integration must preserve unrelated queue rows and target Chat/DOI fields, then import only the exact accepted source-bound state. Current human authorization supersedes the archived draft's no-merge wording.
''')
(C / 'CURRENT_RESEARCH_LOG.md').write_text(f'{UTC} —75% partial-acceptance workflow: three original-stage families closed (41members +3manifests), actual root replays and universal reconstruction complete. Edited literature/admin/source boundaries globally consistent within this prospective packet; original bytes/1/5 retained, new0. A NEW complete current-package adversary is pending. Combined target unsolved; verified3D solution progress remains5% original estimate, no full4D certification, paper/DOI/tracker.\n')
members = [bound(p,C) for p in sorted(C.rglob('*')) if p.is_file()]
js(C / 'MANIFEST.json', {'utc':UTC,'scope':'Exact edited prospective current partial packet; NEW full gate pending; self-excludes MANIFEST.json',
                         'original_head':HEAD,'file_count':len(members),'files':members})
print(json.dumps({'utc':UTC,'current_packet_members':len(members),'dependency_members':len(deps),
                  'current_partial_sha256':sha(C/'PARTIAL.md'),'manifest_sha256':sha(C/'MANIFEST.json'),
                  'shared_queue_unchanged':sha(queue)==hashlib.sha256(qb).hexdigest()},indent=2))
