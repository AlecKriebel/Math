# Fresh complete adversarial acceptance audit of PR 22

**Verdict: PASS for already-solved partial acceptance of the known negative answer to the literal AIM target.** No mathematical, source-scope, attribution, receipt, or current-package repair is required. The historical queue-scope error has been corrected in the current candidate and the live PR body. Record 20002052 is a duplicate of 20002011, with one shared original substantive attempt of five. No paper, new deposit, DOI, release or publication-tracker row is warranted.

This verdict certifies the supplied **current** candidate, rather than recycling the old PASS. Current `SOURCE_STATUS.md` SHA-256 is `3e0972f867bfd3fb380634dcf9b11b3155660508405f853b04a7e9bcde10603e`; current `MANIFEST.json` SHA-256 is `97649814d8d8b671c00ea2d8384bc824adf649c2df8b58b681f85cc211f35c36`, binding 19 files. The original PR head is `5dff69d1f25ac585a87bd8c71bc9d9c136e8c13c`, with 15 preserved original attempt files. This is independent AI verification, not human peer review or a formal proof-assistant certificate. Assigned audit completion is 100%; the parent still owns integration and durable queue reconciliation.

## Independence, criterion and scope

I first read both governing AGENTS.md files, queue workflow, current written proof, exact full AIM assertion and surrounding definitions, both current source records, and both complete pinned upstream reports. Source titles, desk scores and earlier reports were hypotheses. I did not inspect historical `independent_review`, author scripts or receipts, root/family mathematical derivations, or their detailed reports before sealing `FIRST_PASS.md` at **2026-10-01T19:47:50.001459Z**, SHA-256 `201d7e080eb5058819fd306d9fd8c42c29852a5a61aae6b2e0cf06421a6689e0`.

The honest independence boundary is recorded in `FIRST_PASS_SEAL.json`. Allowed current input documents contained high-level claims that previous checks passed; those claims were not evidence. I initially saw a source-only AIM excerpt in the root cache, then independently downloaded the original PDF before the seal. Detailed Branson proof inspection, old/family code, all receipts and root/sibling reasoning occurred after the seal. No historical PASS served as authority.

The [AIM 2003 primary document](https://aimath.org/WWN/confstruct/confstruct.pdf), pp. 11–18 and 27–28, places the target in even-dimensional Riemannian geometry and uses density-valued invariants. Conjecture 1, p. 17, is reprinted as Problem 30, p. 28. It asserts that a natural density with conformally invariant integral can be written as constant times critical Q, plus a pointwise conformal invariant, plus a conformal gradient of an integral of a single-metric local density. The displayed antecedent has no formal-self-adjointness requirement. Spectral determinants motivate it but are not an additional antecedent. The exact source images pp. 17 and 28 were inspected.

The neighboring Conjectures 2–3 and Problems 31–32 allow arbitrary divergences and are different claims. The explanatory text after Conjecture 1, page-number artifacts in its extraction, distinct upstream titles and separate narrow prior calculations do not create a second target. The intended polynomial, parity-even, critical-weight category already contains the submitted example. No broad nonpolynomial interpretation of “natural” is needed. One closed six-dimensional counterexample falsifies the all-dimensional implication; neither a six-dimensional affirmative theorem nor counterexamples in every dimension are required.

The acceptance test was a complete necessary-variational-symmetry proof, full actual density variation and adjoint, an admissible global smooth witness and integrated obstruction, positive published-prior attribution, exact receipt reproduction, and complete source/package/history binding. The repaired formally self-adjoint/generalized-Q formulation was explicitly kept separate.

## Independently verified universal proof

For fixed g use affine conformal coordinates `g_u=exp(2u)g`. If a smooth natural local functional has gradient density H, then its derivative in the fixed direction v is `∫v H_(g_u)`. Equality of mixed derivatives in arbitrary fixed directions v,w forces

`∫v D_gH(w) = ∫w D_gH(v)`.

Smooth finite-jet metric dependence supplies the required differentiability. Neither direction is recomputed along the metric family. The critical Q-density has self-adjoint critical GJMS linearization, a classical property confirmed from the AIM body and Branson's actual definitions. A pointwise conformally invariant density has zero conformal linearization. Every asserted decomposition therefore has a formally self-adjoint **density** linearization. This is a necessary condition and requires no inverse-variational converse. Allowing another permitted Q representative, including Branson's larger generalized-Q space, does not help: its defining linearization is also self-adjoint. Adding invariant or gradient terms cannot change a nonzero skew part.

Invariance of `∫S` says only `D_gS*1=0`. It does not say `D_gS=D_gS*`. The second derivative of the zero functional `∫S` is not the Hessian of a proposed functional with first derivative `∫wS`. Confusing those two functions would wrongly discard the obstruction.

With `Δ=∇^i∇_i`, `J=R/(2(n−1))`, `P=(Ric−Jg)/(n−2)`, and `B=|P|²`, varying the connection, inverse metrics, Schouten tensor and volume gives

`δΓ^k_ij=δ^k_i w_j+δ^k_j w_i−g_ij w^k`,

`δP_ij=−Hess_ij w`,

`δB=−4wB−2P^ij Hess_ij w`,

`δ(Δb)=−2wΔb+(n−2)<dw,db>+Δδb`, and `δdV=nw dV`.

Consequently the complete density variation of `S=(ΔB)dV` has scalar coefficient

`A_n w=(n−6)wΔB+(n−10)<dw,dB>−4BΔw−2Δ(P^ij Hess_ij w)`.

At n=6 this becomes exactly

`A w=−4 div(B grad w)−2ΔT w`, where `T w=P^ij Hess_ij w`.

The first summand is symmetric. Integrating T by parts twice, in its actual derivative order, yields

`T*h=∇_j∇_i(P^ij h)=T h+2<dJ,dh>+(ΔJ)h`.

The contracted Bianchi identity supplies the trace terms. No generally false commutation of tensor covariant derivatives is used. Since Δ is self-adjoint, the complete skew part is

`A−A*=−2(ΔT−T*Δ)`.

The adjoint uses the fixed background metric measure; the density derivative already includes its volume variation. Varying that volume again during adjoint formation would double count it. The written proof handles the actual Hessian connection rather than substituting coordinate second derivatives away from the flat jet.

The scalar has physical scaling dimension length to the power −6. Under a constant metric scaling its Schouten covariant tensor is unchanged, B scales by the fourth inverse power, Δ by the second inverse power, and six-dimensional volume by the sixth power. Thus the density has exactly critical weight zero. It is a universal parity-even polynomial curvature contraction with two curvature factors and two derivatives. Its integral is zero on every closed six-manifold, for every metric, by Stokes. This is stronger than the conformal-integral antecedent. The same dimension-six cancellation must not be silently used as a critical formula in other dimensions.

For the submitted witness, choose a coordinate ball in a flat oriented six-torus and a smooth cutoff equal to one near its center. Extend `f=χx1x2x3` by zero and set `g=exp(2f)g_flat`. This is globally smooth, positive definite and conformally flat. Take w to have the same local cubic. At p=0, `f=df=Hess f=0`, so Γ and its first derivative vanish there, `P=0`, and `∇P=−∂³f`. Lower jets of w also vanish. No unconstrained non-realizable curvature jet is assumed.

The exact trace expression `J=−exp(−2f)(Δ0f+2|df|²)` has order at least four because the cubic is harmonic. Thus `dJ(p)=0`. In `Δ(Tw)(p)` only the mixed derivative term remains, equal to `−2∑f_ijk²=−12`; six ordered permutations have value one. The three types of terms in `T*Δw` contain respectively P, dJ, or Δw at p and all vanish. Hence `(A−A*)w(p)=24`, with `Aw(p)=24` and `A*w(p)=0`.

This point computation becomes a global integral obstruction because its smooth skew output stays positive on a neighborhood. A nonnegative nonzero smooth v supported there gives `∫v(A−A*)w dV>0`. Closed-manifold integration by parts identifies that integral with the difference of the two required bilinear variations. The cutoff changes no local jets and creates no boundary terms. In particular v=w would give zero skew pairing and is not the test chosen. Reversing the Laplacian sign reverses the relevant witness sign but cannot restore symmetry.

The Ricci comparison is also correct: `|Ric|²=16|P|²+14J²`. Varying `∫J³dV` directly gives `−3∫wΔ(J²)dV`. Thus the J-squared divergence is a conformal gradient and has zero skew contribution. The Ricci-norm divergence has the original obstruction multiplied by sixteen, giving 384. No unsolved inverse-variational theorem is smuggled into this conversion.

## Positive published prior and exact repaired boundary

I read [Branson, Q-curvature and spectral invariants](https://www.dml.cz/bitstream/handle/10338.dmlcz/701742/WSGP_24-2004-1_3.pdf), including its publication cover and full relevant printed pp. 31–42, rather than its abstract. Actual images of pp. 34 and 40 were inspected. The volume and institutional record give **2005**; 2004 in the filename is not the publication year.

Definition 2 and Proposition 13 distinguish density linearization, integrated conformal variation and formal self-adjointness. Conjecture 14 uses the self-adjoint subspace and generalized Q-space. The six-dimensional basis, variation computations and equations (53)–(54) demonstrate strict containment in the space of conformal-index densities. The following proof paragraph identifies `V=∇^c(P_ab|c P^ab)` as another nonzero skew representative, even in conformally flat geometry. Metric compatibility gives `V=(1/2)∇^c∇_c|P|²`, so the submitted S is twice that divergence under the note's convention. The derivative mechanism matches the cutoff cubic. This explicit adapter, together with necessary symmetry, establishes the known negative answer to the literal earlier sentence. It is not merely an inference from an abstract dimension count. Branson need not have called this specific AIM record by its numeric modern identifier.

[Alexakis, actual Theorem 1.1](https://sigma-journal.com/2011/019/sigma11-019.pdf), pp. 1–2, has polynomial complete-contraction, weight-minus-n and universal closed-manifold hypotheses, and permits an arbitrary natural divergence in its conclusion. This S is already such a divergence. There is no conflict. I checked the theorem's actual scope, not the entire multi-paper proof series; that theorem is unnecessary for the counterexample.

[Case–Lin–Yuan](https://arxiv.org/pdf/1711.05579), actual retrieved arXiv v1 stamped 15 November 2017, pp. 5–8 and 30–32, confirms the variational criterion, reference-metric dependence at critical dimension, and the weight-six gradient combinations. Its J-cubed formula agrees with the direct derivation. A variational combination containing `Δ|P|²` does not make that component separately variational. The audit does not claim to have inspected 2019 journal pagination.

[Case–Gover's current survey preprint](https://arxiv.org/pdf/2509.16047), §§3.1–3.2, already assumes densities arising as functional gradients in its anomaly discussion. Its reference to a BRST proof sketch therefore does not remove the missing hypothesis from the literal AIM sentence. This audit does not equate every BRST, natural-local, generalized-Q or repaired formulation. It does not certify the global modern status of that separate problem. Bounded searches for the exact Branson title with erratum and the repaired conjecture supplied no contrary primary evidence; absence of search results is not a theorem about all errata or literature.

The strongest verified result is the **published negative resolution of the exact literal target**, not a new discovery and not an affirmative solution of the repaired conjecture. The present counterexample is outside the repaired antecedent. The remaining repaired-target question is not a gap in the literal counterexample; it requires a separately fixed statement and source audit before new research or status promotion.

## Reproduction, new falsification controls and integrity

`reproduce_and_bind.py` independently downloaded all 15 original attempt files from the exact remote head, compared them byte for byte with the frozen snapshot, and verified every snapshot SHA-256, byte count and Git blob SHA-1. It executes no Git command. All 19 current manifest entries and the exact inventory pass. The original provenance/readiness are preserved byte for byte under their original-prefixed names. Current SOURCE_STATUS mathematical sections 1 onward are byte-identical to the old frozen proof. Both source records, old reviews, original scripts/receipts and shared turns remain unchanged.

With `/usr/bin/python3` 3.9.6 and SymPy 1.14.0, isolated copies reproduce the original author's **25** assertions and historical reviewer's **21** assertions, with receipts byte-identical to hashes `64a635ffdc36fecd4d0bee11932e1ef38ab97e8280f51aa6c54d840246efd6f4` and `6ba7b807490e68b76e7b0411fe8ed3241dca26f6e1318c6262d775c23914ae8a`. Both newer family programs also reproduce their **3,391** and **3,194** assertions and saved receipts byte for byte. Their code was inspected, not merely executed.

The family cubic controls include every ordered pair of a 56-dimensional six-variable cubic basis. Independently checking the mechanism gives point defect `4(<A,B>−<tr A,tr B>)`. Its harmonic subspace has dimension 50 and positive form; the trace part has dimension six and negative form. A pure cube may have zero self-pair without being in the bilinear nullspace. This corroborates the family nonharmonic, trace, negative, orthogonal and full-background controls rather than mistaking their PASS for proof.

My materially new control uses a **globally periodic integral witness**, independent of the original point-jet and family cubic mechanisms. `fresh_periodic_controls.py` implements exact sparse Fourier/Laurent differentiation and integration, contracting all six Schouten indices despite two active variables. On `(R/2πZ)^6`, set

`g=exp(2εcos x1)g_flat`, `w=cos(x1+x2)`, `v=cos(2x1+x2)`.

The complete density is an exact finite polynomial after the critical exponential cancellation, not a truncated expansion. Its normalized integrated skew is exactly

`3ε/2+99ε³/8`.

At ε=1/10 it is **1299/8000**, so the unnormalized integral is `(2π)^6·1299/8000>0`. The engine checks five mode/amplitude cases, integral-zero and constant-direction controls, full intrinsic/coordinate operator equality, and detects mutations omitting connection, trace, volume, product-divergence or transverse six-dimensional contraction terms. All **37** distinct assertions pass.

`periodic_analytic_crosscheck.py` imports none of that engine. It independently writes the six-dimensional diagonal Schouten norm as `C=ε²cos²x+ε³cos x sin²x+(3/2)ε⁴sin⁴x`, derives the test-mode variation, integrates each pairing by parts, averages the second angle, and integrates exact trigonometric polynomials. Its **three** assertions recover the same full polynomial and rational witness and verify the density integral is zero. An early draft of this auditor's second calculation omitted the `−4CΔw` variation term and disagreed; including the required term resolved the discrepancy exactly. The failed draft and diagnostic are preserved in ignored tmp and the research log. This did not change the candidate or its proof. Repeated-case labels in the first draft were corrected before freezing the new receipt.

In total **6,671** exact assertions pass across the six reproduced programs, including 40 new assertions from this audit. These are finite falsification controls. Universal symmetry necessity, naturality and the original closed localization are proved separately in the sealed first pass. No finite-check extrapolation, floating tolerance, stochastic sample, novel-proof claim or formal-verification claim is made.

Fresh upstream LFS pointers at dataset revision `37e53eabe540fb458758e198be61634bd02ee008` match SHA-256 and size of both complete cached dataset files. Selected canonical records and full prior reports equal those read at the beginning and the stored current records. Problem-number keys are unique for these two IDs. The prior surface C1 theorem and four-dimensional parity-even coefficient theorem are restricted valid results; neither settles the universal target, and their stale unresolved disposition does not override positive published six-dimensional evidence.

All 39 entries in the three family integrity manifests pass independently. Historical review source/report hash bindings are correct. Root reproduction claims match this auditor's fresh receipt hashes and counts. Root's disclosed imperfect blindness is not treated as an additional independent certificate; the fresh sealed first pass establishes this gate's early independence.

## Current metadata, actions and disposition

Read-only public PR API checks confirm draft/open state and the same exact head, five commits in chronological scope order, and precisely 15 attempt paths plus QUEUE.md. The QUEUE patch changes exactly the two selected rows: 20002011 to already_solved at 1/5, and 20002052 to duplicate at 0/5. It adds no separate duplicate attempt. The original queue-update commits follow the provenance/review artifacts, explaining the dated old exclusion statement.

The earlier P3 issue was that historical provenance and PR body excluded queue edits while the eventual exact head included both rows. The current candidate explicitly retains and supersedes the historical flag, reports `shared_queue_modified:true` with both IDs, and the repaired live body acknowledges both changed rows. I independently read that body back; **the issue is resolved**. A sealed historical document need not be rewritten to pretend it described later commits. Pending-gate wording in the frozen current folder describes its pre-audit checkpoint; this report supplies the subsequently completed gate without editing that folder.

**Open actionable findings: none.** There are no required mathematical/source/current-package repairs or positive-prior access holds. The operational next step belongs to the parent: preserve these byte bindings during integration, reconcile durable effective canonical status/history/counters and regenerate the queue, and record valid already_solved partial acceptance with the duplicate linked. Do not promote the literal affirmative formula to verified_solved or count a new solution. If the mathematical claim or reviewed package is materially edited, this verdict cannot be silently transferred to the changed bytes; apply the required new full gate.

The original source correction used one substantive attempt of five. This audit verifies a completed candidate and adds zero proof-search attempts. No separate target or fresh budget is created for 20002052. No external individual was contacted; public-source retrieval is read-only. This auditor made no Git, PR, canonical queue or publication mutation, and all first-party work resides in `final_adversary/`; foreign sources and runs remain ignored under `tmp/`.
