# Adversarial controls and limits

## Mathematical controls

1. **Missing root containment.** An interval that merely meets a relatively open portion need not lie in it. The explicit replacement in `AUDIT.md` keeps every descendant in an ambient open set defining the portion. This repairs the small-diameter dependency in Proposition 3 without changing original bytes.
2. **Dense orbits.** E0's distinct finite-flip orbits have the same closure. A closure-intersection code cannot classify them. Continuity of the reduction alone does not fix the defect.
3. **Nonrectangular pullback.** Coordinate duplication forces equality of two target coordinates. No full product of nonempty perfect factors lies in its image; some target rectangles have empty preimage.
4. **One class versus smoothness.** Rational-coordinate translation orbits have countable projections and contain no perfect product, yet independent antichains yield equality on a perfect product.
5. **Rejected counterexample.** E1 is nonsmooth on every perfect product but does not meet the source's orbit-reducibility hypothesis, by the actual scope of Kechris-Louveau Theorem 4.2.
6. **Perfect subset versus product.** A diagonal Cantor set can support a smooth E1 restriction while containing no admissible full product.
7. **Closed stages versus closed limit.** The increasing union of closed tail equivalence relations is E1. Finite initial blocks of ones converge to an inequivalent infinite tail. No finite-coordinate test certifies the infinite statement.
8. **Unprotected fusion.** Repeatedly selecting only one child can leave a singleton. The reviewed fusion preserves both children of every existing leaf and splits every coordinate infinitely often.
9. **Continuity on the wrong set.** Borel-to-continuous thinning must supply a full product and must be applied to a genuine classifier to make the equivalence graph closed. A continuous orbit reduction is insufficient.
10. **Nonuniform compact-class coding.** Choosing arbitrary codes for compact classes is not enough. The compact projection argument proves Borel dependence on x. The distance functions need not be continuous; the independent model exhibits this distinction.
11. **A nearby theorem with stronger hypotheses.** KLy's theorem starts with smooth relations. Its Example 2.2 also has a source-only overstatement about Borel bireducibility, independently corrected in `AUDIT.md`. Neither can solve the general question.
12. **Misreading an auxiliary axiom.** The KL proof's auxiliary MA plus not-CH argument does not restrict its theorem to models of that assumption; its stated conclusion is in ZFC.

## Independent executable controls

`INDEPENDENT_CONTROLS.py` is independently written and does not import either submitted Python file. It checks the externally anchored nine-file set before and after all execution. It uses distinct finite cyclic-orbit and weighted-series examples, a finite cylinder-fusion scheduling model with future reservoir restrictions, and a compact-class distance discontinuity example. The fusion model explicitly checks surviving labels, nesting, pairwise disjointness, and preservation of earlier requirements; it is still only a finite model.

Eleven independent mutations are rejected: same-size payload alteration; missing payload; extra hidden file; nested directory; symlink substitution; manifest-only alteration; coordinated payload-plus-manifest alteration; an unlisted synthetic PDF; manifest traversal; changed problem ID; and changed disposition. All mutations occur in temporary copies. The coordinated alteration is important: a verifier that trusts only a mutable self-consistent manifest cannot establish the original release identity. The externally supplied manifest digest provides that anchor.

After these independent controls, the submitted verifier is replayed. Its exact example-output comparison and seven submitted mutations are reported separately, without counting them as independent mathematical evidence.

To reproduce, use Python 3.11 or later:

    python3 -B INDEPENDENT_CONTROLS.py --release /path/to/frozen/release

The generated JSON should equal `RESULTS.json` byte for byte. The audit manifest excludes itself; record its digest externally. No count of passing assertions can validate the reviewed infinite proofs or demonstrate the unrestricted target.
