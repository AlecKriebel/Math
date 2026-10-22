"""Prepare an explicitly dated native presentation locally; no provider/Git writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

BASE = Path(__file__).resolve().parent
D = BASE.parent / 'initial_review_20261015'
ORIGINAL = D / 'submitted/unsolved_math_prioritization/attempts/5100033'
NATIVE = BASE / 'pr_update/5100033'
HISTORY = NATIVE / 'history/original_submission_20261015'


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    assert not NATIVE.exists(), 'Do not overwrite a prepared/reviewed native packet.'
    NATIVE.mkdir(parents=True)
    HISTORY.mkdir(parents=True)
    pins = []
    for p in sorted(ORIGINAL.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(ORIGINAL)
        for target in [NATIVE/rel, HISTORY/rel]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
            assert target.read_bytes() == p.read_bytes()
        raw = p.read_bytes()
        pins.append(dict(path=rel.as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    assert len(pins) == 20
    now = datetime.now(timezone.utc).isoformat()
    proof = (ORIGINAL/'PROOF.md').read_text()
    proof = proof.replace('**5100033 / AMR-050-0033 / arXiv k605,a. Complete author-turn-1 candidate; separate review pending.** No novelty or priority claim.',
        '**5100033 / AMR-050-0033 / arXiv k605,a = published k606. Current mathematical presentation after full source, mathematical and bounded priority audit.** Historical novelty and public proof priority remain undetermined. The standalone note and dated release receipts provide the publication record; no first-proof claim.')
    proof = proof.replace('Hyperbolic or collapsed caustics and relabeling repetitions of shorter orbits are outside the restored source scope.',
        'The theorem states its strictly nested nondegenerate elliptical-caustic domain explicitly. Primitive/star/repetition conventions are proved formulations here, rather than attributed verbatim to the source tables. Hyperbolic and collapsed caustics are outside this theorem; fixed repeats follow from the direct corollary below.')
    proof = proof.replace('This source-specific outer-focal-pedal argument needs its own uninvolved independent review. No exhaustive novelty search or historical-first claim is made.',
        'Three fresh independent mathematical/source adversaries and two distinct bounded priority investigations have checked this target, followed by root replays and synthesis. These are AI-assisted internal checks, not independent human peer review or formal proof-assistant verification. Required whole-manuscript reviews and actual release receipts are recorded separately. No exhaustive novelty search or historical-first claim is made.')
    proof = proof.replace('The present author did not coauthor those candidates. ', '')
    proof += '''

## 8. Current source, credit and repeated-traversal clarification

The original source construction is in Figure1/introduction and sections3.4/3.7; section2 supplies the signed-area convention. The literal primed product already appears in arXiv2004.12497v1,26April2020,Table5 k604,p6. It is k605,a in v11(29October2020), and k606 in the2021 published companion. Those edition labels are not interchangeable with the unprimed product. The v11 arXiv-record title is *Eighty New Invariants of N-Periodics in the Elliptic Billiard*; the shorter printed PDF heading does not change its identity.

An s-fold fixed traversal repeats every determinant s times, hence B_e^(s)=s B_e and the product scales by s². Reversal negates both signed areas. These are direct deductions here, not source wording. Circular boundaries give regular stars and a rotation-invariant product directly.

The auxiliary-circle property, Jacobi functions and compact-torus divisor argument are classical. Credit also belongs to the earlier complex Poncelet-area and complementary-area literature (Akopyan-Schwartz-Tabachnikov, Chavez-Caliz, Roitman-Garcia-Reznik) and cyclic-identity methods of Khare-Lakshminarayan-Sukhatme. Khare-Sukhatme, *Connecting Jacobi elliptic functions with different modulus parameters*, Pramana63(2004),921-936, DOI10.1007/BF02704331, Eq7/p923 and section2.1, proves the old arbitrary-order dn sum identity. The accompanying archive gives a complete exact focal-projective/polar bicentric contact-area and phase reduction to that identity. This is an additional checkable geometric application, not a newly discovered analytic method or evidence of earlier exact-target publication.

Ferudun, *Products of the Two Focal Inversion Areas in Elliptic Billiards* (2October2026,v1.0,DOI10.5281/zenodo.23096994) proves the original-vertex inverse product. The additional outer-foot pole lemma above puts B_e and the opposite-focus inverse area D_-e in the same two-simple-pole antiperiodic space; matching residues gives B_e=gamma D_-e. The geometric comparison is spelled out in the archive and is not printed in that inverse paper. Ferudun's *Outer-Pedal Area Products in Elliptic Billiards* (1October2026,v1.1,DOI10.5281/zenodo.23088516) includes related parallel-residue cancellation, under different parity/reference-point hypotheses. Both works require substantive method/current-work credit. The exact triangular inputs reused for controls also appear in the inverse paper; they are not a new parameter discovery.

Historical novelty and public proof priority remain undetermined after a bounded literature audit; no first-proof, new general elliptic-method or current-worldwide-open claim is made. Actual primary passages, source hashes and access gaps are recorded in the source/verification archive. Extensive AI tools supported solving, verification, literature work and writing. This is unrefereed and has no represented independent human peer review or formal proof-assistant verification. All20 original files, including stale candidate/pending metadata and original bindings, remain byte-exact under history/original_submission_20261015/. They are historical evidence, not the current assessment.
'''
    (NATIVE/'PROOF.md').write_text(proof)
    (NATIVE/'README.md').write_text('''# Reviewed outer focal-pedal area product

`PROOF.md` proves the signed outer-tangent focal-pedal area product at the original foci for every admitted odd primitive period/star, with direct fixed-repetition scaling s² and a circular case. Exact target: arXiv v11 k605,a = published k606, originally v1April2020k604. Full mathematical/source and bounded priority audits have been integrated. Historical novelty and public proof priority remain undetermined; no first-proof, new general elliptic-method, current-world-open or human-peer-review claim is made.

`history/original_submission_20261015/` preserves all20 original files, including the independent_review/ packet, byte-for-byte. Top-level `verification.json` explicitly wraps an inherited run binding the original proof; it does not pretend to bind this edited presentation. `verify.py` is unchanged and, if run here, will produce a new result binding the adjacent current proof. The portable harness runs the original checkers in isolated folders and leaves all archived inputs unchanged.

Current top-level manifests bind the reconciled presentation. The top-level MANIFEST_V1.json is historical: evaluate its entries against history/original_submission_20261015/, allowing the one documented superseded SOURCES.md hash, never against edited current files. Old pending-review statements, source-only checkpoint and worktree paths are preserved as dated history. `readiness.json` separates the immutable imported review hash from the current assessment. Author research turn1/5 is preserved.

The standalone note, exact planned metadata, source/verification archive and independent audit records accompany the case. This is a dated source snapshot; required whole-package review and publication outcomes are recorded in the case's final clearance and later native release receipts. See `PUBLICATION_STATUS.md`.
''')
    (NATIVE/'SOURCES.md').write_text('''# Current sources, exact construction and bounded priority

Reznik-Garcia-Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, [arXiv2004.12497v11](https://arxiv.org/abs/2004.12497v11),29October2020: Table7p9k605,a is the product of the two primed outer focal-pedal signed areas. Figure1/introduction and sections3.4/3.7 give the outer-tangent construction; section2 gives signed shoelace area. The PDF printed heading is shorter than its arXiv-record title. Earliest inspected literal statement in the series is v1,26April2020,Table5p6k604, under its *Forty New Invariants...* title. The source tables do not expressly define primitive/star/repetition conventions.

The [published companion](https://doi.org/10.1007/s40598-021-00174-y), *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal7(2021),341-355, online18February2021, calls the same primed formula k606 in Table7p349. Published k605 concerns original-chord pedals. Actual table pages and definitions, rather than code matching, control the source identity.

Stachel, *On the motion of billiards in ellipses*, EJM8(2022),1602-1622, [Theorem4.3 and Eq4.9p1614](https://doi.org/10.1007/s40879-021-00524-2), supplies the canonical phase, coprime windings and semiaxis relation. [DLMF22.4](https://dlmf.nist.gov/22.4), [22.8](https://dlmf.nist.gov/22.8), [22.13](https://dlmf.nist.gov/22.13) supply period/shift/addition/derivative facts. The correct dn real shift is dn(u+2K)=dn(u); a separate erroneous sign in Stachel's auxiliary prose is not used.

Classical auxiliary-circle and polarity geometry, compact-torus principal parts, and older complex Poncelet-area mechanisms are credited to the existing literature. Relevant read sources include Akopyan-Schwartz-Tabachnikov, *Billiards in ellipses revisited*, [arXiv2001.02934v2](https://arxiv.org/abs/2001.02934v2); Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, AMJ7(2021),91-106; Roitman-Garcia-Reznik, [*New Invariants of Poncelet-Jacobi Bicentric Polygons*](https://doi.org/10.1007/s40598-021-00188-6); and Khare-Lakshminarayan-Sukhatme, [Cyclic Identities II](https://arxiv.org/abs/math-ph/0207019v2). Their objects/hypotheses are distinguished in the detailed ledgers.

Khare-Sukhatme, [*Connecting Jacobi elliptic functions with different modulus parameters*](https://doi.org/10.1007/BF02704331), Pramana63(2004),921-936, Eq7p923/proofsection2.1pp924-926, gives the actual old arbitrary-order dn sum theorem. The archive's exact bicentric/contact-area/phase bridge reduces this particular target to it, including stars, signs and the half-period alignment. The geometric application was freshly written in this audit; neither its historical novelty nor its earlier publication is certified.

Ferudun, [*Products of the Two Focal Inversion Areas in Elliptic Billiards*](https://doi.org/10.5281/zenodo.23096994),v1.0,2October2026, proves the original-vertex inverse product. Its actual pole proof plus the explicit additional outer-foot lemma yields B_e=gamma D_-e and thus this product. Ferudun, [*Outer-Pedal Area Products in Elliptic Billiards*](https://doi.org/10.5281/zenodo.23088516),v1.1,1October2026, contains related parallel-residue cancellation under different parity/reference-point hypotheses. The source archive preserves the complete comparison and credits; no label-based dismissal is appropriate.

The pinned imported report at dataset37e53eabe540fb458758e198be61634bd02ee008 is historical triage, not a current theorem or novelty certificate. Its exact hash is retained in readiness.json and the original history. Two new bounded priority families and root checks verified no earlier printed general exact-target proof in the inspected corpus. Historical/public priority remains undetermined; no current-world-open assertion is made. Source author inventories and selected passages are not exhaustive proof coverage. The final *Talented Mr. Inversive Triangle* edition was incompletely compared, Stachel's *Triple* full PDF was inaccessible, and videos exposed no inspectable proof/transcript. No proof absence is inferred from those gaps.

`source_manifest.json` preserves the three original primary PDF hashes; external third-party texts are excluded from public payloads. The portable source archive retains dated version/source ledgers, actual read scopes, hashes and limitations. Full proofs and finite computational evidence are distinguished throughout.
''')
    ready = json.loads((ORIGINAL/'readiness.json').read_text())
    ready.update(gate_status='mathematical_source_and_bounded_priority_accepted',literature_checked_at='2026-10-15',
        original_imported_review_hash_role='Historical upstream triage binding, not a current priority certificate',
        original_gate_and_budget_history='history/original_submission_20261015/readiness.json',
        current_priority='Historical novelty/public priority undetermined; old KS analytic theorem and current Ferudun geometric comparisons credited; qualified proof/application only',
        current_review_receipts='Case initial_review_20261015 and final clearance/release records',
        source_locator_correction='Outer construction Figure1/introduction and sections3.4/3.7; signed area section2',
        repeated_traversal_corollary='Fixed s-fold traversal scales both signed areas by s and product by s²',
        current_snapshot_utc=now)
    save(NATIVE/'readiness.json', ready)
    turn = json.loads((ORIGINAL/'turn_ledger.json').read_text())
    turn.update(status='mathematical_source_and_bounded_priority_accepted',
        historical_original='history/original_submission_20261015/turn_ledger.json',
        current_assessment_utc=now,
        current_release_record='Case final clearance/native release receipt; historical candidate outcomes remain unchanged below')
    save(NATIVE/'turn_ledger.json', turn)
    save(NATIVE/'verification.json', dict(kind='Historical original-author run; not a current-presentation proof binding',
        original_proof_sha256=hashlib.sha256((ORIGINAL/'PROOF.md').read_bytes()).hexdigest(),
        original_head='2180d64b648b81ac660a792f7823d0b715f9cf12',
        original_receipt='history/original_submission_20261015/verification.json',
        current_note='Unchanged verify.py can be run to bind the adjacent proof; portable original replay uses frozen original proof in an isolated directory',
        original_result=json.loads((ORIGINAL/'verification.json').read_text())))
    (NATIVE/'SOURCE_CHECKPOINT.md').write_text('''# Source checkpoint: current/history distinction

The original source-only checkpoint and its worktree paths, zero author-turn count and pending descriptions are preserved byte-exact at `history/original_submission_20261015/SOURCE_CHECKPOINT.md`. Those statements describe1October2026. The current assessment is in PROOF.md, SOURCES.md, readiness.json and the case audit: full mathematical/source acceptance and bounded priority integration, qualified historical priority, one original substantive author turn. Later final clearance/native release receipts record actual publication and merge outcomes. This source snapshot alone does not claim those outcomes.
''')
    (NATIVE/'METADATA_CORRECTION.md').write_text('''# Metadata and presentation reconciliation

The original1October2026 bibliography correction and both original manifests remain under `history/original_submission_20261015/`. This15October presentation adds exact edition chronology, correct outer-construction locator, explicit primitive/star/repetition formulation, old-method/current-work credits and bounded-priority limitations. The original proof and all20 original files remain byte-exact in history; verify.py and the inherited independent_review/ packet are unchanged. Inherited checker hashes bind their original proof, while current manifests bind this reconciled presentation. No historical priority or human-peer-review claim is added.
''')
    (NATIVE/'PUBLICATION_STATUS.md').write_text('''# Publication record and dated source snapshot

This is the15October2026 reconciled prepublication source snapshot for the exact outer focal-pedal theorem k605,a/publishedk606. Full mathematical/source audit and bounded priority integration are accepted. Classical methods and current related work are credited; historical novelty/public proof priority remain undetermined. Extensive AI assistance and unrefereed status apply; no independent human peer review or formal proof-assistant verification is represented.

The complete original20-file submission, including old pending/no-merge language and old binding hashes, is preserved as historical evidence under `history/original_submission_20261015/`. Current wrappers distinguish that history from the present mathematical/priority assessment. The top-level verification.json labels an original run, rather than falsely binding an edited proof. The author used one original substantive research turn.

The standalone note, exact planned metadata and portable source archive accompany this case under the repository's descending audit programme. Preparation and packaging are not publication clearance. Required fresh sequential whole-manuscript reviews, resolutions and final byte seals are recorded in the case's FINAL_CLEARANCE.json. Actual DOI, tracker row and merge outcomes are recorded in the later native RELEASE_RECEIPT.json and current Queue pointer. This dated source snapshot does not forecast or self-certify those later events. The native release must add the actual receipts before merge.
''')
    (NATIVE/'RESEARCH_LOG.md').open('a').write(f'\n{now} — case60% current presentation reconciliation: all20 original files archived and verified byte-exact. Updated current source/history/credit/scope wrappers; mathematical argument unchanged apart from explicit repetitions and credit. Original verification hash labelled historical; unchanged scripts remain available for isolated replay. Preprint under preparation, actual final review/publication receipts separate.\n')
    save(BASE/'NATIVE_RELEASE_PLAN.json', dict(schema='pr210-native-release-plan-v1',
        original_head='2180d64b648b81ac660a792f7823d0b715f9cf12',
        target_prefix='unsolved_math_prioritization/attempts/5100033/',
        queue_path='unsolved_math_prioritization/QUEUE.md',
        original_queue_blob='7a62a969eddd1b1b7a35f24de59acb5f868ea093',
        original_files=pins,
        source_snapshot_role='Dated prepared presentation. Later actual administrative release fields are added only after publication/reviews; proof/checker bytes remain bound.',
        permitted_later_additions=['actual DOI/deposit receipt','actual tracker four-cell readback','version-bound full-manuscript review/resolution receipts','native RELEASE_RECEIPT.json','current publication status and manifests','single exact target Queue row'],
        required_native_guard='Fresh open draft original head and exact claimed_solved row; compare full path scope; preserve every foreign path and Queue row; native sole-parent nonforce branch update; native merge with expected head after audit and release readbacks',
        no_publication_or_native_mutation_performed_by_this_script=True))
    print(json.dumps(dict(prepared=str(NATIVE), original_files=len(pins), utc=now), indent=2))


if __name__ == '__main__':
    main()
