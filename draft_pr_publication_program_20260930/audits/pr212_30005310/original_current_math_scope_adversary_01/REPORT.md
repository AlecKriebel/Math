# Independent original/current mathematical source and claim audit

Checkpoint: 2026-10-17 21:23:20 UTC. Completion estimate: **100% of this mathematical source/logic audit**. This is neither a full-package promotion review nor a priority adjudication. The bare Boolean discovery goal remains unresolved by these artifacts.

## Verdict and mandatory boundary

**PASS for the explicitly qualified numerical counterexample in both frozen versions.** I found no false mathematical step or mandatory mathematical repair in their common K4,4 proof. Its exact result is

    I_(G,3) != (0), I_(G,4)=(0), WMLT(G)=2,

for both singleton-colored K4,4 and the model obtained by tying only concentration diagonals 1 and 2. The singleton model additionally has MLT=4 by the correctly applied cited theorem. The tied model's exact MLT is not proved or needed.

This disproves the numerical threshold assertions at n=3, including the claimed WMLT=n consequence of the positive-definite-intersection antecedent. It does **not** refute Boolean signed-SOS-or-intersection exhaustion: the example satisfies the intersection antecedent. Both submitted versions explicitly preserve this distinction. The current version's added colored-C4 mathematical route is also valid and disproves the numerical claims under a four-cycle restriction; no historical precedence conclusion is drawn here.

No bare Conjecture 4 resolution, priority finding, publication readiness, or future sequential full-package review acceptance is conveyed by this PASS. In particular, the current already_solved disposition remains a claim for a later priority stage.

## Inputs, independence, and actual reading

The Root custody acceptance (6,525 bytes, SHA256 c240a9b71efee22f0699f42d1437d5731b5542024704c2ca7ceb129badbe3529) and Root original-source acceptance (2,616 bytes, SHA256 1c8f87035bb530c77a2ee335b63288b7ce17e5c4a5c23b2d1ceb70f098c9a2db) were read and independently size/hash verified before any submitted proof was opened. Both body ledgers and the 4,094-byte public custody manifest were independently size/hash checked. Subsequently all original 20 and current 35 frozen body files were rehashed against those ledgers; all match.

Original PROOF.md is 12,506 bytes, SHA256 69ffeade6c2ee758e3c2869d9c5b7dd607c9a1b6782f7ecebfb81d0812fdb676. Current PROOF.md is 13,266 bytes, SHA256 ae9971d5944d6a1dd7a4b7d0f19043809c7420f9f0006dc8834965e6e07250af. Sections 2-7 are byte-identical: 8,932 bytes. Both full proofs, submitted author verify.py, and inherited independent_check.py were read before any submitted execution. Relevant original/current status, metadata, source records, source manifests, and verification-boundary documents were also read. The archived historical review verdict was not used as mathematical evidence; no other current mathematical auditor's report was read. Current PRIORITY_AUDIT.md was not read in this mathematical stage.

My original-question reading was frozen independently in ../original_question_scope_01 before any submitted mathematics. It used actual whole-page pixels of the official report's printed pp.3146-3149, zero-based PDF pp.25-28. This report does not change that preartifact freeze retroactively. The submitted source_record's cleaned question explicitly incorporates the numerical claims, but the terse original Conjecture 4 does not uniquely remove its Boolean-versus-numerical interpretation ambiguity. This distinction remains mandatory.

For mathematical dependency verification only, I read the precise primary versions cited by the submitted proof. Source hashes and exact reading scopes are in SOURCE_READ_SCOPE.json. No priority search was performed. The only network use in this stage fetched three mathematical primary sources already cited by the submission. No Git command, original-artifact mutation, provider action, public release, tracker mutation, or external communication was performed. All writes are inside this new owned folder. Third-party PDFs, text extracts, rendered pages, and isolated submitted-code copies are private and excluded from the authored public selection.

## Independent verification of the common K4,4 proof

### 1. The model is admissible

The graph has parts {1,2,3,4} and {5,6,7,8}, with all 16 cross edges. Under the report's partition definition, singleton vertex/edge colors are admissible. The tied variant merges just diagonal coordinates s11,s22 into s11+s22. All cross-edge entries remain individually observed. This is precisely the concentration equality K11=K22; it imposes no equality on the sample covariance diagonal entries individually. Identity is a feasible positive-definite concentration matrix in both models. The graph is connected, and the tied variant is a nontrivially colored instance.

### 2. Nonzero I3 is an exact ideal statement

The determinant of the 4-by-4 observed cross block B is an actual 4-minor of the full symmetric indeterminate matrix, using the left vertices as rows and right vertices as columns. Replacing each cross entry by its individual statistic coordinate changes this polynomial only modulo the linear statistic equations. Thus det(B) belongs to the exact contracted elimination ideal, and it is a nonzero polynomial because its value at B=I4 is one. The argument holds in the tied variant since no edge coordinate was merged. This does not rely on PSD inequalities, principal-minor substitution, or identifying a merely computed subideal with the full ideal.

### 3. Zero I4 follows from real dominance, with a second analytic certificate

The submitted derivative argument for the rank-four Gram map is correct. At X=(I4;V), V has rows e1+e2, e2+e3, e3+e4, e4+e1. Arbitrary cross derivatives can be absorbed in dV after choosing dU=D. Left diagonal derivatives determine D_ii, and the four right diagonal derivatives can then be changed independently using the four distinct unordered off-diagonal pairs 12,23,34,41. The real submersion theorem gives an open image in all 24 sufficient-statistic coordinates. Every element of I4 vanishes on this open image, so is identically zero. The tied statistic map is a surjective linear quotient, yielding open image in 23 coordinates.

An independent dual derivation avoids constructing the displayed right inverse. Write a concentration-space matrix as

    K = [ A  B ; B^T  D ],

with A,D diagonal. If KX=0 at the same X, then B^T=-DV and A=V^T D V. The four off-diagonal entries of A corresponding to 12,23,34,41 force the four diagonal entries of D individually to zero, hence B=A=0. Thus the derivative dual is injective. The tied concentration space is a subspace, so it also has trivial dual kernel. My standard-library exact checker obtains determinant-one full-column-rank minors in the 32-by-24 and 32-by-23 stress coefficient matrices. This is an independent supporting certificate for the same dominance argument, not an assumption of generic-completion-rank/MLT equality.

### 4. WMLT=2 has the correct probability quantifier

At the rank-two data matrix with left rows e1 and right rows e2, all observed diagonals are one and all cross entries are zero, matching I8. More substantially, the submitted open box of radius epsilon=1/100 gives a positive-definite matching completion throughout the box: diagonal entries are at least 9801/10000, and each of four cross entries in a row has absolute value at most 202/10000. The strict row-dominance margin is 8993/10000>0. The left/right two-row determinant is bounded below by 1-2 epsilon=49/50>0, so the data have rank exactly two there.

A nondegenerate known-zero-mean Gaussian has a strictly positive joint density throughout the finite-dimensional data space; the open box therefore has strictly positive probability for every positive-definite covariance allowed by either model. This proves WMLT<=2 analytically, not by simulation or a single exceptional configuration.

For one observation x, edge 3--5 and both of its endpoint diagonals are individually observed in both models. Their prescribed principal 2-by-2 matrix has determinant x3^2*x5^2-(x3*x5)^2=0. No positive-definite completion is possible, including at zero entries. Thus one-observation success is impossible and WMLT>=2. All lower sample sizes relevant to the claimed weak threshold are covered.

The source's original short report does not explicitly spell out mean treatment, but the exact cited rigidity source defines N(0,Sigma) and S=XX^T/d. The additional colored-model source likewise uses a centered Gaussian and scatter divided by n. This verifies applicability of the submission's explicitly fixed rank-indexed convention. No unannounced unknown-mean n-1 convention is used.

### 5. The intersection antecedent holds for the entire ideal

The rank-two Gram matrix has exactly the same statistics as I8. Since its rank is at most three, every polynomial in I3 vanishes at those statistics. Therefore pi_G(I8) is in V_R(I3). This uses a genuine real PSD preimage, avoiding the algebraic-closure-to-real-lift gap flagged in my preartifact freeze.

Even a proposed extra reading requiring a preimage of rank exactly n=3 cannot rescue the numerical conclusion. An independent 8-by-3 Gram factor with rows

    e1, e3, e1, e1, e2, e2, e2, e2

has rank exactly three and the same all-one diagonal and zero cross statistics as I8. This extra witness is in INDEPENDENT_CHECKS.json; it is not needed for the literal variety antecedent.

At the positive-diagonal Cholesky factor I8, every ideal polynomial's pullback is zero. Thus no ideal element, and in particular no selected generator, is everywhere nonvanishing on that domain. The conclusion is robust to the source's generator-list ambiguity. Nevertheless the Boolean alternative holds because its B branch holds. Calling this example a Boolean counterexample would be false.

### 6. Exact MLT=4 is correctly credited and applied only to singleton colors

Blekherman-Sinn Theorem 2.7 in the exact cited v2 states the complete-bipartite formula used by both proofs. For a=b=4, k=3 gives k(k+1)/2=6<8 and k=4 gives 10>=8; min(4,5)=4. The paper's definition is almost-sure positive-definite completion for generic rank-r PSD data, matching the fixed sampling convention. Theorem 2.1's generic-completion-rank value four is also consistent with, but unnecessary for, the direct ideal proof.

The formula's theorem, assumptions, definitions, and proof context were inspected. I have not substituted a running example from another paper. The exact tied-model MLT is not inferred from the ordinary graph theorem. WMLT=2<n=3 already contradicts the numerical conclusion, so the central counterexample remains valid even if the exact MLT dependency is removed.

## Independent check of the current added four-cycle route

Current PROOF.md lines 37-44 additionally invokes Homs-Kuznetsova-Stolz v1 Propositions 3.9 and 3.26. The actual primary statement and its proof concern a cycle with all vertices in one color class and all edges individually colored. For C4 it gives gcr=2 and MLT=1. The elimination statement uses the same statistic space as the report up to invertible factor-two rescaling of edge coordinates. The mathematical bridge is valid.

For clarity, here is a complete independent C4 derivation in the original report's coordinates. Its five statistics are total diagonal sum and the four individual edge entries.

* I1 is nonzero: f=t12*t34-t23*t41 is a nonzero polynomial and is the observed 2-minor with row set {1,3} and column set {2,4}, modulo the linear statistic equations.
* I2 is zero: at X with rows e1,0,e2,0 in R2, a concentration-space matrix K with KX=0 must have columns 1 and 3 zero. Equal diagonals and the four distinct edges then force every parameter of K to vanish. The derivative dual is injective and the Gram map is a submersion onto all five statistics. My exact independent coefficient matrix has a 5-by-5 minor of determinant -1.
* MLT=1: write K=lambda I+A, with A supported on cycle edges. Let J=diag(1,-1,1,-1). Every edge joins opposite signs, so JA+AJ=0 and x^T J A x=0. If Kx=0, then lambda*(x1^2-x2^2+x3^2-x4^2)=0. Outside the zero set of that nonzero polynomial, lambda=0. A PSD matrix with every diagonal zero is zero; hence no nonzero PSD concentration-space matrix annihilates such x. By strict separation of the affine completion fiber from the PD cone, this is equivalent to existence of a PD completion. The exceptional quadratic zero set has Gaussian probability zero, so p1=1 and MLT=WMLT=1.

This supplies I1 nonzero/I2 zero at n=1 while the printed numerical scenarios both require MLT=2. It addresses the numerical assertion even if a four-cycle-only restriction is imposed. It still does not refute Boolean exhaustion: x=e1 has statistics matching (1/4)I4, so the intersection mechanism holds here too.

This paragraph verifies mathematical theorem content and implication only. It does not certify dates, first solutions, prior anticipation, or the status already_solved. Those remain outside this stage.

## Reproduction and what the checks do not prove

After code reading, submitted code ran only in isolated owned copies. Original author: 188 exact assertions PASS; current author: 188 PASS; inherited checker: 1,808 PASS. All three emitted receipts reproduce the corresponding submitted receipts byte for byte. The inherited script hardcodes the original proof hash and is only historical; it does not authenticate the current proof. The current author script correctly hashes its actual adjacent current PROOF.md. Runtime: /opt/homebrew/bin/python3.11, Python 3.11.8 and SymPy 1.14.0, with -E -B -P.

My own independent_scope_checks.py uses only exact Fraction arithmetic and the Python standard library. It passes 18 controls covering stress injectivity, the rank-exactly-three enhancement, uniform margins, and C4 dual identities. Universal probability conclusions and full ideal statements rest on the analytic arguments above; finite checks are supporting controls. No attempt was made to infer a universal SOS impossibility from failed numerical optimization.

## Mandatory findings, repairs, and promotion conditions

1. **No mathematical defect found in the common qualified numerical proof.** No change to its model, ideal proof, open probability argument, or numerical conclusion is required.
2. **Mandatory scope restriction, already obeyed by both versions:** any accepted result must say numerical counterexample/source correction. It must not say that the bare SOS/intersection alternative is solved. If an uncaveated full-Conjecture-4 tag is used downstream, repair it by restricting the title/status/claim, or supply a genuinely different argument for Boolean exhaustion/refutation. Rewording this example cannot turn its true B antecedent into a Boolean counterexample.
3. **Four-cycle qualification:** the original K4,4 proof alone does not resolve a four-cycle-only problem. The current independent C4 route validly resolves its numerical version. Retain that distinction between versions; do not backdate the current extension into the original proof.
4. **Priority and publication remain unaccepted:** current already_solved, earlier-coverage, and first-recognition wording must be independently assessed at the later priority gate. A mathematical PASS does not validate those historical assertions or authorize publication. No historical verdict is supplied here.
5. **No hidden exact-threshold claim for the tied model:** retain its exact MLT as unclaimed. Neither a false equality transfer nor an exact intermediate MLE probability was found in the submitted qualified proof.

Source ambiguities are not evidence of false mathematics: singleton-color admissibility is explicit; known-zero-mean sampling is now verified against cited primary definitions; source generator and nonvanishing ambiguities do not affect these examples; and the source's possible narrow intended scope is distinguished from its unrestricted formal display. The strongest verified result is a numerical counterexample in both versions, plus mathematical validity of the current C4 numerical route. The exact remaining substantive question is Boolean SOS/intersection exhaustion, together with a separate unaudited historical classification.
