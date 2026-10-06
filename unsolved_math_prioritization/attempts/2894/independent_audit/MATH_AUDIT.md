# Mathematical audit of K3 Problem 4.18

Audit date: 6 October 2026. Problem ID: 2894.

## Acceptance recommendation

Accept part (a) as an affirmative prior result obtained from Hambleton--Unlu (HU), Corollary D and Corollary 4.9, together with Kasprowski--Nicholson--Vesela (KNV), Theorem C. This is acceptance of the stated literature implication relative to those theorem dependencies. It is not an independent verification of all underlying L-theory, a computer-certified proof of the cited theorems, or a new solution.

Part (b) is not resolved by this argument. The combined record must retain the canonical disposition `unsolved`, with the established part (a) and unresolved part (b) explained separately. The latest inspected Kupers--Powell (KP) manuscript explicitly retains the h-versus-s question as open.

The corrected proof's added paragraph about the oriented involution and localization at 2 is mathematically correct. The distinctions and justification are expanded below. No further mandatory mathematical correction was found.

## Target and quantifiers

K3 Problem 4.18, printed/PDF page 204, has two existence questions about pairs of smooth closed four-manifolds. In part (a), an actual homotopy equivalence must exist, while every simple homotopy equivalence between the endpoints must be excluded. In part (b), an actual smooth h-cobordism must exist, while every smooth s-cobordism between the endpoints must be excluded. Neither part imposes an orientability restriction. Connected oriented examples therefore qualify.

These quantifiers rule out two shortcuts. A homotopy equivalence with nonzero torsion alone does not exclude a different simple equivalence. Likewise, an h-cobordism with nonzero torsion alone does not exclude a different s-cobordism. The packet correctly avoids both shortcuts. Smooth compact manifolds have finite triangulations, so finite-complex simple homotopy theory applies to the final smooth examples.

Source: [K3, Problem 4.18, pages 204--205](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf#page=204).

## The exact assembly condition supplied by HU

For a finite 2-group G, write the oriented degree-two assembly components as kappa_s and kappa_h, with source H_2(G; Z/2) and simple and homotopy decorations respectively. HU Corollary D, page 5, gives the strict direction

    ker(kappa_s) is a proper subgroup of ker(kappa_h).

The direction also follows from the decoration-forgetting map: kappa_h factors through kappa_s. Corollary 4.9, page 16, gives the stronger witness G = SmallGroup(128,1377), for which kappa_s is nonzero and kappa_h is zero. Thus its homotopy-decorated kernel is the whole source, while its simple-decorated kernel is proper. The witness is not merely a discrepancy between unrelated homomorphisms or between Whitehead groups.

HU states the simple-to-homotopy comparison in the standard oriented involution g -> g^(-1). This agrees with the oriented assembly components used by KNV. In particular, the degree-two cohomology class later used in KNV is normal 1-type/Stiefel--Whitney data, not a nontrivial orientation character.

Source: [HU v1, pages 1--5 and Corollary 4.9 on page 16](https://arxiv.org/pdf/2602.05003v1).

## Localization and completion are different steps

HU's global convention on page 2 localizes the abelian L-groups at 2. KNV's assembly components take values in the integral oriented groups L_4^s(ZG) and L_4^h(ZG). The subscript 0 used in parts of HU is compatible with the subscript 4 by the ordinary four-periodicity of the relevant surgery L-groups.

For either assembly component, every image element y is killed by 2, since the source H_2(G; Z/2) is killed by 2. The localization map A -> A tensor Z_(2) reflects zero on such elements: if y maps to zero, some odd integer r kills y, and integers u,v satisfying ur + 2v = 1 give y = 0. Therefore the integral and 2-localized assembly components have identical kernels. This proves the compatibility asserted by the added paragraph in the corrected PROOF.md. This argument concerns localization of L-groups; it does not silently identify that operation with a change of group-ring coefficients.

HU also uses the distinct coefficient homomorphism ZG -> Z_2-hat G. The barred assembly symbols refer to this 2-adic step. Vanishing of a barred homomorphism alone does not imply integral vanishing. HU supplies the additional detection argument: Lemma 3.4, pages 9--10, detects the relevant torsion using both 2-adic coefficients and abelianization. Theorem B and the proof of Corollary D, pages 11--12, apply this detection. In the specified example, the abelianization is elementary abelian, so its weakly simple degree-two assembly component vanishes. The even-dimensional comparison from weakly simple to homotopy decoration then gives the unbarred vanishing recorded in Corollary 4.9. The packet does not need an unjustified inference from 2-adic vanishing.

## Inspection of the HU proof dependency chain

The inspected chain is as follows.

1. Section 4b gives a class-two central extension of the order-128 witness by C_2, with the extension group identified as SmallGroup(256,8177).
2. Lemma 4.4 and Theorem 4.1 show a failure of surjectivity on the relevant SK_1 groups. Lemma 4.5 passes the failure to the needed Tate-cohomology groups using the exponent-2 property.
3. Lemma 4.6 supplies the lifting condition for inverse-conjugate elements. Together with Theorem 4.3, this makes the simple L-theory boundary homomorphism nonzero.
4. Lemma 4.7 makes the required Tate cohomology of Wh-prime vanish. Theorem C, with the diagram in Theorem 3.1, gives nonvanishing of the simple assembly component.
5. The detection and decoration comparisons described above give vanishing of the homotopy component. Corollary 4.9 records both conclusions for the same G.

This is a coherent theorem chain. The supporting statements from Milgram--Oliver, Oliver, Wall, and earlier surgery-obstruction work remain dependencies. This audit did not independently calculate the relevant L-groups, SK_1 groups, or assembly maps, and did not rerun a GAP identification of the group presentation. The finite checks below cover only explicit local group-algebra assertions.

## Local source typos and independent finite checks

Three local typographical points in HU's pages 15--16 deserve precise interpretation.

- In the parity arguments for Lemmas 4.4 and 4.6, the stated test on q_5 uses modulus 4, although the central generator x_5 has order 2 and the preceding formula gives its exponent modulo 2. The needed test is q_5 even. The written parity arguments establish the stronger impossibility under that weaker, correct condition. The accompanying script checks that condition directly, rather than relying on the printed modulus 4.
- In Lemma 4.5, the printed rank for H_2(G/Z(G); Z) is 4. The presented class-two model has G/Z(G) = (C_2)^4, whose integral second homology is its exterior square (C_2)^6. The proof only needs exponent 2, which is unchanged. The script checks that the reduced commutator form has zero radical; the rank-six homology conclusion then uses the standard exterior-square formula, not a computed Schur multiplier of G.
- Near the bottom of page 15, the first branch of Lemma 4.6 leaves both parity words attached to n_1. In the branch where m_1 is even and q_8 is odd, the formula forces m_4 odd and n_1 even. This gives the remaining stated contradiction. Reading n_1 as odd would be incorrect. The exhaustive check does not depend on that prose typo.

The apparent use of the class of x_3 among generators of the denominator in Lemma 4.7 need not assert that x_3 itself is inverse-conjugate. Its abelianization class is generated by the classes of x_1, x_1*x_2, and x_1*x_2*x_3, which the displayed conjugacy relations supply. The four relevant abelianization classes span all of (C_2)^4.

The independently authored `check_hu_parity.py` uses central bit coordinates, an alternating commutator form, and its quadratic square map. It checks:

- All 256 pairs of parity vectors for each of the two obstruction equations: zero counterexamples.
- All 65,536 pairs of exponent vectors with coordinates in {0,1,2,3}: zero counterexamples to either equation.
- All 256 quadratic-polarization identities.
- A trivial radical for the commutator form after the indicated central quotient.
- The four inversion identities relevant to Lemma 4.7 and the full span of their abelianization classes.
- Three basic sanity controls that detect nonzero commutators, nonzero squares, and a zero square.

These finite results support the local interpretations above. They do not certify the full HU theorem. The executable script and deterministic results explicitly retain this limitation. Reproduce them with:

    python3 check_hu_parity.py --check HU_PARITY_RESULTS.json

## Applying KNV and checking the resulting manifolds

KNV Theorem C, pages 3 and 20--21, requires a finitely presented group with unequal assembly kernels. Every finite group is finitely presented, for example through its finite multiplication-table presentation. No additional good-group hypothesis is imposed by this theorem.

The proof forms the free product pi = G*G. Consequently, the smooth example's fundamental group must not be described as the finite group G. KNV Remark 1.4 on page 3 makes this distinction explicit.

The construction doubles a class x in the homotopy kernel but outside the simple kernel. It uses normal 1-type data (w,w), and the resulting mod-2 pairing cancels as w(x)+w(x)=0. This is the smoothing step's relevant Kirby--Siebenmann calculation. The proof first obtains topological representatives and then stabilizes sufficiently to obtain smooth representatives and an actual homotopy equivalence. The final conclusion is therefore stronger than only a stable relation between topological manifolds.

The stabilization convention on page 2 allows connected sums with nonnegative numbers of copies of S^2 x S^2 on the two sides. The final pair remains inequivalent by simple homotopy after any such stabilizations. Taking zero copies on each side gives part (a).

Source: [KNV v2, pages 2--3, Remark 2.8 on page 6, and the proof on pages 20--21](https://arxiv.org/pdf/2405.06637v2).

## Unmarked and unoriented conclusions

The obstruction in KNV's proof is nonzero in the quotient of the tertiary group by the image of ker(kappa_s). Mere nonzero tertiary class would only establish a weaker distinction, so the kernel-image quotient matters.

Remark 2.8 shows that the actions changing normal 1-smoothings preserve the relevant kernel-image subgroup, by naturality of assembly. They need not literally fix the chosen representative (x,x), but they preserve its nonmembership. Thus the proof excludes all markings and all simple homotopy equivalences, rather than only a selected equivalence inducing a prescribed group identification.

The comparison manifold is xi-nullbordant. Reversing its orientation leaves its bordism class zero. An orientation-reversing simple equivalence to that manifold would become an orientation-preserving simple equivalence after reversing its orientation, which the same obstruction excludes. Equivalently, negating the mod-2 obstruction cannot make its nonzero quotient class vanish. Thus forgetting the extra orientations does not weaken the conclusion required by K3.

The packet's explanatory sentence about a nonzero tertiary class is acceptable in context; the more precise statement is nonzero image in E-infinity_(2,2) modulo the simple-assembly kernel image.

## Why part b remains separate

A smooth s-cobordism induces a simple equivalence of its endpoints, by composing one simple boundary inclusion with a homotopy inverse of the other. Therefore a smoothly h-cobordant pair having no simple equivalence would settle part (b). HU plus KNV does not supply the smooth h-cobordism required for that deduction.

KP v2, Question 1.2 on page 1, explicitly retains the general compact smooth h-versus-s question as open and relates it to K3 Problem 4.18. Theorem A and Corollary B, pages 1--2, give positive h-implies-s results for connected oriented manifolds with finite fundamental group under three alternatives: vanishing SK_1 plus injectivity of the L_5 decoration-forgetting map; vanishing SK_1 plus topological pre-stabilization; or smooth pre-stabilization. The orientation and finite-group hypotheses apply to all three alternatives. The cyclic-group example is correctly reported. These results do not answer the unrestricted existence question in part (b).

Source: [KP v2, pages 1--2](https://arxiv.org/pdf/2604.27635v2).

## Bibliographic status and final scope

The arXiv records inspected on 6 October 2026 show HU v1 dated 4 February 2026 with no journal reference, KNV v2 dated 9 October 2025 with the journal reference Proceedings of the London Mathematical Society 131 (2025), no. 5, e70101, and KP v2 dated 22 July 2026. HU is therefore described here as a public preprint, not as a peer-reviewed publication. The absence of a later solution to part (b) is reported within the inspected-source scope, not inferred solely from unsuccessful searching.

Records: [HU](https://arxiv.org/abs/2602.05003), [KNV](https://arxiv.org/abs/2405.06637), [KP](https://arxiv.org/abs/2604.27635).

Final recommendation: accept the corrected packet's mathematical conclusion for part (a) relative to the identified HU and KNV theorem dependencies; retain part (b) as unresolved and the combined disposition as `unsolved`. Do not represent the parity script, packet validation tests, or metadata checks as independent certification of the surgery-theoretic source results.
