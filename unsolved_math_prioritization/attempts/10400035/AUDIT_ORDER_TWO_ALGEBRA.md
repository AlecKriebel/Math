# Independent exact algebra audit of the order-two kernel argument

**Theoretical-edition note.** This is the complete authored mathematical audit, with only the provenance/privacy and unavailable-artifact edits documented in PROVENANCE.md. Its computational passages describe historical supplementary checks. The scripts, fixtures, outputs, and logs are not included, and preparation of this edition did not rerun them. This is an AI mathematical audit, not human peer review or formal proof-assistant verification. Original authored-artifact hashes below identify the pre-edition documents, not any edited public copies.

## Verdict

PASS for the algebraic claims inspected. No algebraic error was found. This is an algebra audit, conditional on the geometric witnesses, their coordinate values, the finite-type spanning theorem, and the topological interpretation of the Artin/Magnus calculation. It is not an independent certification of those geometric or source inputs.

The audited final `PROOF_KERNEL_ORDER_TWO.md` (before the documented edition-only redactions) has SHA256 `01185b1eafcce7b6a1ef55ebf5bc5f4a4bed784b82f75b1e232aa5a30a09a58f` and 18,400 bytes. The report and its original checks were read only. Their hashes and byte counts are recorded in the results and reread at the end of each successful run.

## 1. Independent braid calculation

The new checker stores an automorphism as complete freely reduced images of the free generators. It does not import the author's code or transport conjugators through braid composition. After computing the full action of the commutator, it cyclically peels inverse end letters from each generator image, then normalizes the recovered conjugator's exponent sum in its own meridian to zero. This recovers exactly all three conjugator words printed in the report.

The composition used is the final report's explicit convention, Phi_AB = Phi_A composed with Phi_B. Both inverse identities, the adjacent Artin relation, and the distant commutation relation are checked for ranks two through six.

For beta = sigma_1^2 sigma_2^2 sigma_1^-2 sigma_2^-2, the exact normalized Magnus expansions are:

- E(c_1) = 1 + X_2 X_3 - X_3 X_2 + O(3).
- E(c_2) = 1 - X_1 X_3 + X_3 X_1 + O(3).
- E(c_3) = 1 + X_1 X_2 - X_2 X_1 + O(3).

The degree-two extraction is implemented twice: truncated noncommutative multiplication and a separate prefix-exponent-sum calculation. The results agree. All three self exponents and all linear Magnus terms vanish. Thus the selected algebraic coefficient is +1 in the stated conjugation convention; changing the longitude convention can change its sign without affecting the elimination argument.

Deletion is tested in two ways. First, erasing the appropriate free generators from the full images leaves each surviving generator unchanged. Second, the checker tracks endpoint labels at every crossing and deletes braid strands before evaluating the resulting two-strand braid. Every resulting two-strand braid has exponent sum zero and identity Artin action. The crossing-label computation also independently returns zero for all pairwise linking numbers.

## 2. Nonadjacent labels and basing

For every selected triple among three, four, five, or six endpoints (35 triples in total), the checker constructs a permutation braid carrying the first three meridian labels to the selected labels, conjugates beta by that braid, and calculates the complete free-group action. The resulting degree-two conjugator expansions have precisely the three relabeled commutators. No outside variable appears. All pairwise linking numbers vanish. Deletion to every other triple has identity Artin action.

These finite checks support, but do not replace, the all-rank filtration argument. A meridian changed by conjugation has Magnus expansion 1 + X_i + O(2). Substitution into 1 + P_2 + O(3) therefore preserves its homogeneous degree-two term P_2. Conjugating such a longitude also preserves P_2.

A change of whisker can include the additional factor Phi(q) q^-1. The report's c_j lie in the second lower-central term, so Phi(x_j) equals x_j modulo the third lower-central term. Consequently Phi(q) q^-1 has no Magnus term of degree one or two for any word q. The full changed conjugator Phi(q) c_j q^-1 has the same degree-two part as c_j. Exact checks cover 24 whisker choices, including outside meridians, and 12 independent meridian-basing substitutions. A nonzero degree-three term for q = x_1 verifies that the whisker test is not merely checking an accidentally trivial automorphism.

## 3. Entire linking-polynomial block

Write d = binomial(k,2). The complete polynomial basis contains 1, every linking variable, every linking square, and every product of two different linking variables. Its dimension is (d+1)(d+2)/2. In particular the last class includes both shared-endpoint and four-distinct-endpoint products.

Evaluation at 0, each +e_i and -e_i, and each e_i+e_j isolates the coefficients by exact finite differences:

- Constant: Q(0).
- Linear i: [Q(e_i)-Q(-e_i)]/2.
- Square i: [Q(e_i)+Q(-e_i)-2Q(0)]/2.
- Mixed i,j: Q(e_i+e_j)-Q(e_i)-Q(e_j)+Q(0).

These identities establish faithfulness for every finite d over the rationals. They are stronger than a finite sample alone and agree with the report's integer-lattice argument. The exact sparse evaluation matrix is reduced by uniform determinant-preserving row operations to diagonal entries 1, then d copies of (1,2), then 1 for every mixed monomial. Its determinant is 2^d for every d. The checker performs these operations for every k from two through eight, including all 210 four-distinct-endpoint products at k=8.

## 4. Remaining coordinate systems

Keeping every unspecified linking and plat coordinate symbolic, and replacing the rational-witness value by w and the second component coefficient by q, the six-by-six matrix has determinant

2 w (1-q^2).

It is independent of the five unspecified linking/plat values. At w=1 and q=5 it is exactly -48. The component-pair matrix has determinant 1-25 = -24.

For general k, use the two equations on components 1 and 2, then one equation involving components 1 and j for each j from 3 to k. The component determinant is

(1-q^2) q^(k-2),

hence -24 * 5^(k-2) at q=5, nonzero for every k at least two. The checker also confirms the symbolic formula for k=2 through 12. The rational witnesses give an identity block on all w_ij coordinates; unknown Nogueira plat values below that block can be removed by row operations. Thus no uncomputed plat value or linking number enters the asserted full-rank conclusion.

## 5. Exact torus polynomial cross-check

Exact division gives

[(x^12-1)(x-1)] / [(x^3-1)(x^4-1)] = x^6-x^5+x^3-x+1.

The checker does not only insert the proposed Conway polynomial. It solves for the unknown even coefficients of degree at most six in the Laurent identity

h^6 C(h-h^-1) = Delta(h^2).

The unique result is C(z)=1+5z^2+5z^4+z^6. It therefore independently reproduces the z^2 coefficient 5 from the standard Alexander formula assumed in this algebra check. The exact torus-coefficient formula in the report also evaluates to 5. The polynomial is even, so the usual mirror substitution does not change this coefficient. The validity of the knot/source identification and the standard polynomial normalization remain topological inputs to the separate audit.

## 6. Optimization safety and negative controls

Both ordinary Python and Python -O pass the same 825 explicit guards, with identical semantic output apart from the optimization flag. There are no assert-based proof guards.

Ten meaningful mutations are each rejected in both execution modes: wrong frozen report identity; erased commutator; reversed commutator; incorrect inverse-Artin letter; incorrect claimed conjugator; incorrect claimed Magnus sign; erased rational-witness w value; collapsed component-coefficient gap; omission of a four-distinct-endpoint linking product; and an incorrect torus Conway coefficient. The runner verifies each expected failing guard, rather than accepting an arbitrary crash as a successful negative control.

## Computational artifact boundary

The original audit included executable checkers, machine-readable results, mutation fixtures, and execution logs. They are not included in this theoretical edition, and no reproduction command is presented as runnable from this package. The preceding mathematical exposition and historical verification account are retained; no computational rerun is claimed for this edition.
