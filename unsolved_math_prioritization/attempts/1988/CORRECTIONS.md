# Two exact scope corrections

The candidate's core argument is sound, but its exact prose needs two qualifications. The accompanying CORRECTIONS.patch changes only authored/PROOF.md. The input proof is 16,461 bytes with SHA256 8c4d56bb0e21785f4aeb21239518783dcf139afd10839c6514fea6472e0ad0b7. The immutable original was not edited in this audit.

## Edition status

These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” refers only to the corrected partial results in this edition. No external human peer review, journal acceptance, formal proof-assistant certification, novelty or exhaustive worldwide-status determination is claimed.

Both changes are already applied in the distributed PROOF.md. CORRECTIONS.patch is preserved byte for byte as the two-hunk historical patch against the original authored/PROOF.md, whose unchanged copy is not distributed. Do not apply it again to this edition. The patch records only the required mathematical qualifications; other documents carry separately recorded editorial framing.

## 1. Positive interval-start parameters

In Theorem 1, replace “only finitely many integers n” by “only finitely many positive integers n.”

Reason: if all integers are admitted, every n<0 yields 2n-C<n and hence an empty interval. Empty intervals are subsets of every S, giving infinitely many vacuous counterexamples to the literal finite-count claim. The proof already studies unbounded positive n. The intended eventual-large-n statement, its applications, and the deficit formulation require no mathematical change.

## 2. Infinite-intersection and positive-coordinate qualification

Replace the first paragraph of “Affine extension and limits” by the paragraph supplied in the patch. It defines T={t in N : r+dt belongs to S}; when T is infinite, restriction and the inverse affine map give an omega enumeration of T. When T is finite, the eventual noncontainment conclusion is immediate. Thus for every fixed C>=0, the coordinate interval {r+dt : n<=t<=2n-C} fails to lie wholly in S for all sufficiently large positive n.

Reason: an infinite 3-permutable set can meet a particular affine lattice only finitely often, or not at all. For example, S={3^k : k>=0} is set-theoretically 3-AP-free and contains no even numbers. Its admissibility follows because in 3^a+3^c=2*3^b with a<b<c, the 3-adic valuations of the two sides would be a and b. Restricting it to the even lattice does not produce an infinite set. Also, for arbitrary r, unrestricted inverse coordinates need not all be positive. The new paragraph deals with both issues without weakening the intended eventual conclusion.

## Acceptance effect

These are local domain qualifications, not repairs to mirror propagation, C3, the transplantation argument, or Proposition 7. The corrected partial results are accepted within the scope stated in ACCEPTANCE.md. The uncorrected finite-count sentence and unqualified affine-intersection sentence are not accepted literally. No correction gives a solution of the two-set problem or certifies novelty.
