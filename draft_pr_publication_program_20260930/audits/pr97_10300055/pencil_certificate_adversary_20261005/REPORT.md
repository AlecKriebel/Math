# PR97: independent contact-pencil and certificate adversary

Closed bounded review of problem 10300055 / AMR-102-0055. The incoming CANDIDATE.md is a complete conditional affirmative argument for Calegari Question 13.2, not an existence result for Question 13.1. This review has no historical-priority or service/publication authority.

**Verdict: the stated mathematics passes this independent audit; the original diagnostic runners require a minor enforcement repair before treating optimized execution as verification.** Both original runners use Python assertions for every check. Optimization suppresses those assertions and an intentionally false control is recorded as PASS. Explicit exception guards correct that defect without changing the identities, numerical/symbolic computations, or candidate text. No proof or central research attempt was extended.

## Independence and scope

I read the complete original CANDIDATE.md, verify.py, and review/independent_checks.py. I wrote OWN_DERIVATION.md before reading prior or other fresh review reports; I have read none of those reports. I then compared the original finite receipts and frozen artifact digests, executed fresh source copies, wrote an independently implemented dot/cross-product certificate, and inspected relevant primary-source pages. All modifications and actual process artifacts are confined to this reviewer folder. The incoming archive remains unchanged.

The hypothesis under review is a closed oriented smooth three-manifold with a cooriented taut C2 foliation without spherical leaves; global C1 forms alpha and omega with alpha nowhere zero; d alpha = alpha wedge omega; and omega wedge d omega nowhere zero. The conclusion is tightness of ker omega. Globality, contactness, compactness, coorientation, and tautness are real assumptions. Atoroidality, minimality, and nonzero Godbillon-Vey evaluation from the problem's more restrictive setting are not otherwise needed. Minimality excludes spherical leaves. Nothing here guarantees that a contact connection form exists.

## Mathematical falsification attempts

The differentiated connection relation is legitimate at the stated regularity: d squared alpha vanishes distributionally, while alpha wedge omega is C1, so the product derivative produces the continuous identity alpha wedge d omega = 0 pointwise. Together with omega wedge d alpha = 0 and alpha wedge d alpha = 0, this yields an unchanged contact volume for every spatially constant real shift omega+s alpha. A contact three-form also prevents zeros of the shifted one-form. The volume identity is global and requires no local gauge stitching.

Compactness supplies a positive minimum norm of alpha and a finite bound for omega. The normalized forms alpha+omega/s therefore converge uniformly to alpha as s tends to positive infinity. A single sufficiently large finite S places the endpoint inside the contact-tightness neighborhood of the foliation. The proof applies smooth Gray stability only on [0,S], where every form is contact. It does not apply Gray at a foliated endpoint or at infinity. A theorem asserting merely the existence of some tight approximation would be inadequate; the sources actually state a neighborhood assertion for every sufficiently close contact structure.

For C1 inputs, smooth approximations a and eta yield a smooth path eta+s a on that fixed compact interval. If B bounds the form and derivative norms and delta bounds each corresponding error, the contact-volume error is at most 2B delta+delta squared. Choosing errors smaller than delta/(1+S), with this expression below half the positive contact margin, gives contactness on the entire interval. Independent endpoint closeness puts the endpoint in the foliation's neighborhood. The smooth a need not be integrable and need not satisfy a connection equation; approximating a finite interval is sufficient. Thus every sufficiently C1-close smooth eta is tight.

The disk smoothing bridge is also correct under its stated smooth-or-C2 disk criterion. In a fixed tubular chart, the boundary evaluation q_j of a smooth approximation tends to zero in C1. Subtracting q_j times a smooth cutoff times dt annihilates the boundary tangent exactly, while the correction tends to zero in C1. Contactness and the distinct disk/contact tangent planes persist by compact-boundary openness. For a C2 disk, smooth embedding approximations converge in C2, and the corresponding boundaries are graphs in a fixed smooth chart; bounded graph derivatives and the chain rule give the same C1-small moving correction. This argument does not smuggle in a C1 version of Gray or smooth the foliation itself.

I tested disconnected manifolds and opposite signs. The contact sign is constant on each component; compactness gives finitely many components and common finite bounds. Reorienting a negative component does not change disk existence or tightness. Using positive s for convergence avoids a coorientation reversal in the normalization. Noncompact manifolds, manifolds with boundary, zeros of alpha, non-taut foliations, and locally defined forms are outside the theorem; the proof does not extend to them without additional hypotheses.

A variable shift h has the additional volume term omega wedge d h wedge alpha. This term can cancel the contact volume, so it cannot replace the constant pencil. Removing the differentiated constraint alpha wedge d omega = 0 also permits cancellation in a first-jet model. The candidate explicitly restricts to constant shifts, and no such invalid extension appears in its proof.

## Exact reproduction and guard falsification

CERTIFICATE_REPRODUCTION.json records 18 actual child processes using CPython 3.9.6 and SymPy 1.14.0, each with source/candidate pins, complete stdout/stderr, actual PID, UTC timing, and exit code. Input source copies were read-only; the independent runner's generated result is written only inside its fresh case directory.

- Original author, original author replay, and original independent runner, each in ordinary and optimized modes: six exits 0. Their JSON receipts equal the corresponding incoming receipts exactly. Author/replay count 87 and independent count 89.
- Original intentionally false author/independent controls, ordinary mode: two exits 1 identifying the false control.
- The same original false controls under -O: two exits 0 with status PASS and counts 88/90, respectively. This is actual observed unsound enforcement, not a hypothetical concern.
- Minimal explicit-guard author/independent replacements, both modes: four exits 0 with the original 87/89 count and check contents.
- Those replacements with the same false controls, both modes: four exits 1 identifying the deliberate false control.

All five entries in the original frozen_artifacts.json match their actual source bytes. The original author receipt binds the authentic candidate and verifier digests; the independent historical receipt binds the same authentic candidate. The replay candidate and source remain exact original copies. The original independent receipt does not include a verifier digest; this review's process records bind that actual source separately. The recorded positive counts are finite diagnostics, not complete mathematical proofs.

The only proposed source edits are in prepared_minimal_guard_corrections. Author SHA256: `009845e507b2dcfed4c681b6514e9be22aa56e979168b3c1834dbc5b44f70af0`. Independent SHA256: `b3a08e300c19e3aabf2782716825463feedb40d9e82b946729cdbc3975fb4652`. Their diffs only replace the assert statement in each ck with an explicit if/raise AssertionError. New receipts should be generated for repaired current artifacts, while historical original sources and receipts should remain labeled historical. I have not made those global/native changes.

## Distinct independently implemented checks

OWN_EXACT_RESULTS.json records four actual child processes: two positive ordinary/optimized runs and two deliberately false controls, with both false controls rejected. The positive runs agree exactly. A standard-library integer/Fraction dot/cross implementation checks 271589 obligations over 11808 nonzero-contact point triples. It covers the differentiated constraint, constant pencils at five rational positive/negative/zero parameters, nonzero shifted forms, volume signs, normalized pencils, gradient remainders for variable shifts, nonzero common rescaling, and explicit cancellations when requisite constraints are removed. These are independently implemented verification controls for the algebra, not another proof-search attempt or evidence of global tautness.

## Primary-source confirmation and limits

I read and visually inspected six complete relevant PDF pages: Calegari printed p.29; Vogel 2011 pp.42-43; Vogel 2016 pp.2448 and 2451; Dathe-Rukimbira printed p.5. Text contexts also supplied the tautness definition and Vogel 2016 Theorem 2.31.

Calegari's original Question 13.2 explicitly assumes a contact form and inherits Question 13.1's minimal taut C2 setting; it is not the existence/weak-sign question. Vogel 2011 and Dathe-Rukimbira explicitly give the needed every-nearby-contact tightness statement. Their disk definitions confirm the transverse-boundary criterion and its reduction to ordinary contact tightness. Vogel 2016 explicitly admits C1 contact planes but states the Gray theorem for smooth families of smooth structures on a closed manifold, matching the candidate's regularization route. No direct read of the entire Eliashberg-Thurston book is claimed. The imported neighborhood/fillability theorem and smooth Gray theorem remain established external mathematical inputs; symbolic programs do not verify those theorems from first principles.

No historical priority audit was performed. In particular Dathe-Rukimbira Proposition 3.4 concerns a closed defining form, whereas the incoming theorem permits d alpha nonzero; its related mechanism is credited but this reviewer has no authority to decide novelty. This review is AI-assisted and unrefereed; it is not human peer review, permission to publish, or a decision to merge.

Final bounded audit completion estimate: 100%, with one required certificate guard repair and no mathematical repair identified. Original central proof-search use remains 2/5; additional proof-search use by this reviewer is 0.
