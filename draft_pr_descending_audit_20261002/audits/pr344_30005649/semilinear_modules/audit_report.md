# PR344 independent semilinear-family audit

Status: mathematical checks passed; awaiting root report/code review and one-time closure authorization. This report is not yet a sealed artifact.

## Conclusion and scope

The candidate at PR344 head 86a758b1cc9c94322ce6afc3d17150fa2c90327a passes this family's independent audit. It supplies permitted p>3, algebraically closed k examples for every n>=3. Their special fibers satisfy the exact qss filtration definition, admit the explicit p-killed finite flat W(k) realization, and are not isomorphic to their Cartier duals. Hence their W-groups cannot be self-dual either. The source's universal higher-n automatic-self-duality assertion is refuted within its stated setup.

No mathematical correction to TURN_1.md is required by this audit. The suggested improvement concerns reproducibility controls: the submitted F_25 test cannot distinguish Frobenius from inverse; the portable independent verifier uses degree-three extensions and nonprime coefficient matrices.

## Independence and literal source gate

The baseline was frozen before candidate access, with a SHA256 source manifest, exposure gate, and native freeze receipt. All five original Takao page renders and the complete contribution including references were inspected. The high-resolution original page 103 corrected an initial low-resolution glyph misreading **before freeze**: the Proposition 2 hypothesis is roman G, the special fiber; the conclusion is roman G and calligraphic G. This correction is preserved honestly. It matches Definition 1's separate base conventions. The literal target does not require a W-level qss filtration.

The first candidate assessment was frozen after reading only the four root-permitted candidate files, before primary Hoshi content, historical review/results, or sibling content. After this family's proof, program, successful controls, report and preclosure preflight were complete, a team-status tool incidentally returned a completed sibling's brief PASS/controls final summary. No sibling artifact was opened or used, and no mathematical result changed. The exact dated addendum is incidental_team_status_exposure.md; its first checkpoint is 2026-10-04 04:07:27 UTC. No historical candidate review or result was opened. All work is within the owned semilinear_modules namespace; no Git write, installation, or external-person contact occurred.

## Checkable independent mechanism

The frozen baseline derived both dual formulas and the universal matrix equations

    P A = sigma(B^t) sigma(P),
    P B = sigma^(-1)(A^t) sigma^(-1)(P).

The independent proof in semilinear_proof.md permits arbitrary k-valued P. Intertwining the two squares forces columns 2 and 4 of P into the same dual e0 line. Therefore every such P is singular. This is a universal coefficient obstruction; it does not rely on the supplied finite computations. Direct sums with standard supersingular blocks preserve the same forced columns.

The qss basis has an independently calculated integer determinant 1 and an integer inverse. Calculating the transformed matrices from that basis verifies both stable subspaces and all three quotient actions. The numeral 2 in w introduces no denominator or exceptional p. Contravariance reverses the exact filtration, preserving its factors. Each rank-two module is deformable with im F=im V, so Hoshi Lemma 4.9 provides the elliptic p-torsion identity over algebraically closed k.

The finite Honda conditions are supported by explicit basis witnesses: im F=ker V, im V=ker F, [im F basis | L basis] is a permutation matrix, and V(L) has three independent displayed basis vectors. Hoshi Remark 3.5.1 and Proposition 3.11(2)/(5), visually verified on the original manuscript pages 7–9, classify exactly the required p-torsion W-group and its reduction. There is no illicit transfer to lifting an unrelated p-divisible group, and no unproved W-qss-filtration claim is required.

## Independent code and adversarial controls

verify_semilinear.py is a portable standard-library verifier with no private paths, network calls, submitted checker import, or historical-results dependency. It computes the basis inverse rather than accepting the submitted transformed matrices. Its native run passed 33,802 checks, exit 0, with unchanged pinned inputs.

The controls include exact integer support certificates for F^2,V^2 and their duals; FV=VF=0; the qss basis and flag; Honda permutation witnesses; direct sums; concrete n=0,1,2 positive controls; the independently frozen n=4 negative control; a broken mixed relation; a broken filtration; and extension fields F_125 and F_343 using the irreducible cubic t^3+t+1. The cubic has no roots at p=5 or 7, which verifies irreducibility. Nonprime diagonal basis changes produce nonprime coefficients, requiring the coefficient Frobenius twists in the dual matrices.

Frobenius and inverse are unequal in both degree-three fields. Exhaustive single-coordinate scalar pairing controls passed. A deliberately omitted coefficient Frobenius gave 372/1026 failing scalar pairings, and substituting sigma for sigma^(-1) likewise gave 372/1026 failures. This confirms that those controls detect both mistakes; it is stronger than a degree-two field check. The all-k mathematical proof remains the forced-column argument, rather than a finite extension-field enumeration.

The small-rank code fixtures establish concrete split positive controls only, not a new proof of the source's full n<=2 statement. The source-only n=4 control is retained without rewriting its frozen stage-specific W-realization gap into a claim it was already certified at that time.

## Provenance and limits

Source and candidate hashes, exposure UTC, exact argv/interpreter, UTC starts/ends, full stdout/stderr, statuses, and pre/post input pins are retained. Receipts made by run_receipted.py genuinely capture a subprocess's returned code and streams using subprocess.run. By contrast, source_only_native_receipt.json is an internally assembled execution record whose declared status was separately returned as 0 in the actual exec_command tool result. The two failed Hoshi subprocess reads are preserved with externally captured return code 1; they failed only because extracted small-cap headings contain internal spaces. The complete primary-source subprocess read returned 0. The relevant source pages and definitions were independently inspected visually.

The pre-freeze instruction/source read commands use the actual conversation tool receipts, explicitly distinguished from native subprocess receipts. Separate native stderr and pre/post stability cannot be reconstructed retroactively and are not invented. The initial Hoshi locator receipt covers only its enumerated PDF/code/spec inputs; observed hashes for its dynamically discovered filenames are observations, not retroactive stability guarantees. The successful primary read and subsequent control runs do retain all their enumerated code and inputs. These provenance limits do not affect the hand-checkable proof, but remain visible rather than being silently upgraded.

The proposed seal_audit.py closure_native_receipt.json is explicitly an **internally assembled execution record**: its exit/status field is an internal declaration, not an independently captured return code for its own process. Root will retain a genuinely externally captured read-only whole-namespace replay outside this namespace before precise closure authorization. Any actual final sealer return code must likewise be captured externally by the invoking tool or a root-owned subprocess wrapper; the internal record cannot certify that it successfully wrote itself or later exited as declared. No seal has run and no closure authorization has been granted.

At root's bounded provenance-correction request (checkpoint 2026-10-04 04:11:00 UTC), complete old report/plan/sealer/log/addendum bytes were archived before changes. historical_input_versions.json binds those historical versions so that old native input pins remain checkable. Neither early gates nor historical native evidence was rewritten. The independent proof and control program are unchanged.

Classification theorems are authoritative source inputs, not formalized from foundations here. Novelty/current-literature and broader Jacobian/Coleman questions are outside this independent family certification. The frozen source-only baseline's independent n=4 route was a control, not an additional original-research effort.

Completion estimate: 95% of this family audit. Remaining 5% is root's independent externally captured replay, precise authorization, and final inventory/seal. The namespace is intentionally unsealed and stopped pending that root work.
