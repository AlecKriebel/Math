# PR369 independent function-theory review

Frozen head: d9e4600d05b8272fe913a22ae7dcc0fbe0a26344. Original base: efd29c05204703acca9a0860812f54b94fae54b1. Exact problem: Hayman–Lingham Problem 2.55 / 2302055 / AMR-022-2055.

## Verdict

PASS for the stated partial mathematical results, with the original problem unresolved at 5/5. No mandatory mathematical or artifact correction was found. The source-first baseline was sealed at 2026-10-03T12:02:27Z, and the full mathematical verdict was sealed at 2026-10-03T12:08:18Z, before candidate implementation, receipts, final/status/history packet, or prior review was inspected. The sealed independent verdict and proofs remained byte-identical throughout artifact replay. No sibling or root mathematical findings informed the sealed verdict.

The result has the exact original ambient-entire restriction scope. The strongest explicit input class permits a single R(exp(Q)) summand with Laurent polynomial R and polynomial Q, while the other two nonconstant entire inputs are arbitrary. A further finite-exclusion inverse-monodromy criterion permits virtually nilpotent monodromy. Polynomial coordinate precomposition preserves the source property in both directions. On the triple-double-exponential surface, characters and finite-dimensional translation orbits yield only constants (and zero for nontrivial characters). These theorems do not settle arbitrary bounded entire restrictions for three unrestricted inputs.

All classical qualifications are retained. In particular, the source theorem of Rubel–Squires–Taylor is explicitly stated in Demailly's primary paper, but its original full Annals proof was not retrieved. Lin's theorem requires ultra-Liouville base/action hypotheses; ordinary Liouville, amenability, and finitely many singular values are not replacements. No novelty certification or human peer-review claim is made.

## Independent function-theory checks

FUNCTION_THEORY_PROOFS.md derives every universal claim in all five mathematical turns. It uses a finite free algebra to check ambient-entire characteristic coefficients at colliding roots; checks the growth qualification for zero-free finite-order functions using a logarithm and Cauchy estimates; verifies finite plurisubharmonic maxima and global maximum attainment; examines all exceptional fibers, inverse singularities, rational endpoint punctures and nonproper isotopies; derives the complete double-exponential inverse monodromy; and checks fractional character descent at divisor crossings and all finite-dimensional translation spectra.

Additional falsification mechanisms are recorded without promoting them to source solutions:

* Two successive Little Picard arguments show every entire map C→V_2 is constant. Thus a connected family of entire curves cannot prove the unresolved Liouville assertion on that test surface.
* The natural separated tangent field on the already affirmative triple-exponential surface has a logistic equation with finite complex-time poles. Global completeness cannot be inferred from local tangent directions.
* Dropping the three-nonconstant-input hypothesis gives an exact bounded nonconstant ambient restriction: exp((x-y)/2) takes alternating ±1 values on exp x-exp y=0. This is a boundary counterexample, not an admissible original-problem counterexample.

These deductions are included with checkable proofs. The Picard theorem was independently verified from Christopher Bishop's Stony Brook Complex Analysis notes, in addition to the five candidate-routed primary PDFs. No historical novelty is claimed for the deductions.

## Artifact reproduction

ARTIFACT_REPRODUCTION.json records successful checks of all 50 snapshot files, all nine historical/source/author/publication/review manifests, and all seven frozen scripts. The five author outputs match their frozen receipts byte for byte and total 38,066 exact assertions. The prior independent checker reproduces 1,420 assertions, and the prior author-replay output also matches exactly. Review and status files agree with the independently sealed scope: partial results pass; source problem remains unsolved 5/5. The queue row likewise records unsolved 5/5.

INDEPENDENT_FUNCTION_CONTROLS.json records 48 additional exact checks, including full entire matrix exponentials on repeated nilpotent fibers, the tangent logistic identity and pole certificate, the strict subunit exponent boundary, and the two-input parity example. Finite exact checks certify these stated algebraic identities only; the universal analytic and topological reasoning is in the proof document.

The independent checker initially compared expanded and factored SymPy expressions with structural equality. CONTROL_FAILURE_RECORD.json retains the failure and its correction to an expanded-difference-zero test. This was a checker implementation error and did not change any sealed mathematical claim. No failed research mechanism was erased.

## Reproduction and isolation

Run audit_frozen_artifacts.py with Python plus SymPy to read the sibling frozen snapshot and replay only private copies. Run independent_function_controls.py with the same Python to reproduce the 48-check receipt. verify_public_manifest.py checks every public file binding. The actual replay used the already existing private runtime at audits/pr378_30004322/sources_effective_review/private_runtime/bin/python; no installation or repository clone occurred.

Raw primary PDFs, source text and renders, and frozen script replay copies are under private/ and ignored. PUBLIC_MANIFEST.json has an explicit own root and excludes itself and the entire private/ subtree; it binds only original review prose/code and generated metadata/receipts. This review made no Git/index/ref/checkout/remote/service mutations, and contacted no individual. Audit completion is 100%; the mathematical source goal remains unresolved.
