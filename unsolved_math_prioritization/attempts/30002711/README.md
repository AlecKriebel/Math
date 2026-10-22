# 30002711: prescribed cyclotomic local-lift partials

**Unsolved, five of five approaches used. Qualified audit pass only.** This package preserves the author freeze and independent audit unchanged. The complete universal prescribed-coefficient-ring lifting question remains unresolved by this work. This is not a general counterexample, new universal theorem, human peer review, novelty certification, or worldwide-openness certification.

## Controlling correction: read before the frozen Proposition 3.1

The following is the audit's exact replacement for the standalone proposition's statement, and is adopted by this release:

> Let R be a complete DVR of characteristic zero, and let a faithful cyclic group of order q act continuously by R-algebra automorphisms on R[[Z]]. If the action fixes Z = 0, the derivative of a generator is a primitive qth root of unity in R. The conclusion also holds for an R-valued fixed section Z = b with b in the maximal ideal of R, after the continuous R-algebra change of coordinate Z to Z - b.

The origin-fixed derivative argument remains valid without completeness. The nonzero-section translation requires the stated complete coefficient DVR and a faithful, continuous, R-linear action. Every intended application already uses complete W(k) or a finite cyclotomic extension, so none of the retained partial conclusions changes. See [the full qualification and dependency sweep](independent_audit/AUDIT_REPORT.md#3-required-qualification-nonzero-section-translation).

The hypothesis is necessary for the coordinate-change step: over the noncomplete DVR R=Z_(3), there is a series H(Z) in R[[Z]] with H(0)=1 and H(Z)^2=1+2Z. Translation by 3 would force a rational square root of 7 after taking the constant term, which is impossible. This is a counterexample to unrestricted translation, not to the original lifting problem.

## What survives and what remains missing

- The known order-p construction is proved at its stated scope, with an invariant-ring and finite-flatness argument.
- An unmarked C3 action lifts over W(k), with no W(k)-valued fixed section. It refutes an added necessity claim about individual unmarked lifts, not sufficiency of the larger prescribed cyclotomic ring.
- The higher-order direct formula has the desired generic order but reduced order p, so it loses the required faithful special action.
- The bad birational C3 model has generic different degree 6 versus special degree 4. It diagnoses failure of smoothness of that model, not failure of the universal lifting assertion.
- The formal-smoothness descent criterion is conditional. The finite-flat arithmetic obstruction model is not identified with the deformation ring of a cyclic local action.

The inspected 2026 Kummer–Artin–Schreier–Witt isogeny/unramified-cover result does not supply the missing smooth ramified mixed-characteristic local lift after arbitrary pole substitution. The 2026 tower theorem is equal characteristic and permits coefficient extension. These distinctions are documented in the proof and audit; no general resolution is inferred from them.

## Read and reproduce

- [Frozen proofs and exact gaps](author/publication/RESULTS.md), subject to the controlling correction above
- [Independent audit](independent_audit/AUDIT_REPORT.md)
- [Current publication disposition](PUBLICATION_STATUS.json)
- [Author source metadata](author/publication/SOURCE_VERIFICATION.json) and [independent source checks](independent_audit/SOURCE_CHECKS.json)

Python 3.10+ and the standard library suffice; no network is required. From this directory:

    python3 -B verify_publication.py --expected-manifest <trusted PUBLICATION_MANIFEST.json SHA-256> --self-test
    python3 -B -O verify_publication.py --expected-manifest <the same trusted SHA-256> --self-test

Use the publication manifest pin supplied in the accompanying PR, not a pin recomputed from an untrusted copy. The wrapper checks the exact file/directory inventory, all hashes and sizes, unchanged author and audit manifests, both archives and all their members, and the audit-to-author binding before executing code. It replays the unchanged audit in normal and optimized Python; each audit replay tests the author in normal/optimized and relocated modes, reproduces 6,527 author checks and 1,987 independent checks, and exercises six author corruption controls per wrapper plus twelve independent integrity challenges. Publication-level corruption tests use disposable copies. All these finite checks supplement the scoped written proofs; they do not prove the unrestricted target.

The author status and research log retain their historical pre-audit wording. The audit retains its historical no-remote-write statements. These describe their own frozen stages. This release guide and PUBLICATION_STATUS.json identify the completed qualified audit; neither original freeze was silently rewritten.

## Immutable bindings and disclosure boundary

- Author manifest: 362a6ed1502b421e00efab914b4f02d125e7788a906f7273cb25cf074a83f177
- Author archive: ae4193f1e0c8a555b5d46ec59ae3aacea615a2536d578eaf4aa9a97e0a5ee9c0, 20,745 bytes
- Audit manifest: 40cacbf44a5a42a85bba9c8f5b558fd54fbabba952846bf00bd9a94ef055294c
- Audit archive: 6e1872fbed32079808a271f2af23abb4db8d361ae5281d84e048b0f87f1e1de9, 25,207 bytes

The live catalogue's exact current text and raw AI corpus remain uninspected. Source checks are bounded and do not certify historical priority or global openness. Only authored proof/audit text, code, deterministic results, public verification metadata and their safe archives are included. Source PDFs, extracts, rendered images, raw source records, dataset contents and private coordination files are excluded.

The accompanying queue patch changes only this row's Status to unsolved and Turns to 5/5. Existing Findings, Chat, DOI, all other rows, and the pre-existing header bytes remain unchanged. No queue regeneration, merge, GitHub release, DOI creation, or external outreach is part of this publication.
