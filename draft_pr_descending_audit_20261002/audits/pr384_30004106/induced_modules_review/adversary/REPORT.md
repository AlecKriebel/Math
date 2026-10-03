# Adversarial checkpoint: PR384 Turn 5

UTC: 2026-10-03T02:18:02.154955+00:00. Frozen target: `682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6`, bound through `snapshot_manifest.json`. All 52 frozen file lengths and SHA-256 values match. The independent reconstruction was saved before consulting the parent reconstruction or controls. Only files inside this `adversary/` folder were written. No Git mutation, outside-individual communication, PR/service action, new author search, or new author turn occurred.

**Verdict: no mandatory mathematical or report-scope repair is identified.** The written theorem survives the listed adversarial checks. This is verification of the scoped Turn 5 claim, not a novelty or merge-readiness certification. The original universal symmetry question remains unsolved at 5/5 substantive author turns.

## Attempts to falsify the written theorem

- **Arbitrary-field induction and module injection:** the local-endomorphism tensor argument is valid because the group-algebra complement has augmentation quotient exactly k. It does not need a false theorem that arbitrary tensor products of local algebras are local. The two nilpotent ideals commute as ideal products; their sum is nilpotent with division-algebra quotient, hence the endomorphism algebra is local. For finite-dimensional module tensor factors the Hom factorization remains valid over arbitrary k.
- **Recovery of H and t:** an endotrivial restriction to an order-p subgroup has dimension prime to p and is nonprojective. Copies of a nonprojective module cannot collectively become projective, because every summand of a projective is projective. Mackey gives a free restriction exactly on the ordinary order-p subgroups outside H. Those within H determine H, and the restriction back to H recovers the core by Krull-Schmidt. This establishes distinct actual indecomposable coordinates before any formal lattice algebra.
- **Mackey normalization and duality:** the coefficient is exactly [E:HK][E:H intersect K]/([E:H][E:K])=1. Trivial intersection contributes only projectives. All other extra summands are projective and induce projectively. Finite-group duality commutes with induction and inverts the stable endotrivial class.
- **Möbius blocks:** setting e_1=0 is compatible with full-lattice inversion at every nontrivial subgroup. The zeta matrix is injective on the actual coordinate span. Thus p_H are nonzero self-adjoint orthogonal idempotents, sum to the stable unit, and have the stated projection action.
- **Completion, signed/complex coefficients, and surjectivity:** the H-coordinate of Phi_H(f) is precisely f, so lower-level collisions cannot cancel the lower norm bound. Restriction core dimensions are at most the original dimensions, proving the upper bound. Both estimates pass to arbitrary completed l1 elements by density. The lower bound gives closed range; the projection images of all dense generators lie in this range. This proves completed surjectivity, not just a formal finite-support bijection. The finite number of subgroup blocks makes the full inverse bounded. No all-infinite-sums claim is inferred from numerical tests.
- **Unitary characters and symmetry:** the credited subexponential growth applies separately to t and t inverse. A bounded character on the weighted group algebra therefore has |chi(t)|=1. Every unitary group character extends by absolute convergence because w>=1. Hermitian character values yield spectrum(x*x)={|s(x)|²} within the relevant algebra. This requires neither semisimplicity nor ambient character extension/spectral equality.
- **Full/stable lift and units:** e=[kE]/|E| has norm one and unit e in its factor. J([k])=1-e is the unit in J(B); the full product unit maps to 1. D on the stable coordinate space is bounded linear, not multiplicative. Multiplicativity of J follows from the central idempotent splitting. Disjoint supports give ||Jx||=||x||+|D(x)|. The specified full coordinate span is exactly Ce+J(B).
- **Proper-span F8 module:** its coefficient cubic is irreducible, and all seven ordinary nonidentity group elements have nonzero unipotent coefficient. Every actual C2 restriction is free, whereas every induced-endotrivial coordinate has a nonfree ordinary cyclic restriction. The centralizer is the local algebra F8[J] and dimension two excludes projectivity over kC2³. Hence the module is a missing indecomposable coordinate; its distance from the full closed span is exactly two. The shifted direction z(g1-1)+(g2-1) acts by zero, so this does not contradict a shifted-cyclic projectivity criterion. The witness is not a non-Hermitian species.

Rank-one, p=2, trivial-group exclusion, negative syzygies, arbitrary module-field extensions, countable support in potentially uncountable index sets, and factor identities were included in these checks.

## Primary-source scope

Benson arXiv:2008.13155v2, printed/PDF page 69, was visually checked against the local source image. Proposition 4.4.6, Lemma 4.4.7, and Theorem 4.4.8 give the credited elementary-abelian classification and endotrivial growth input. Chapter 4 states arbitrary characteristic-p fields, and Corollary 4.3.8 supplies gamma invariance under field extension. The relevant H are nontrivial p-groups, so p divides their orders.

The Benson–Symonds primary preprint introduction likewise permits arbitrary k; its Theorem 7.5 on printed page 12 was visually checked and corroborates the endotrivial gamma result. Its Proposition 7.4 credits Dade and its Theorem 7.1 credits Carlson. Carlson–Thévenaz 2005 pages 823–824 corroborate unique cores and Dade's noncyclic abelian classification; that paper explicitly moves to algebraic closure after asserting scalar-extension injectivity on T(G). It is not silently treated as a direct arbitrary-field original proof.

Dade 1978 and Carlson 1981 original proofs were not directly inspected, nor was the final 2024 publisher edition. The inherited result is an explicitly credited theorem from accessible primary mathematical texts. This qualification must remain. Nothing in Turn 5 requires pretending these inputs were independently re-proved.

## Review and fresh replay of the parent controls

The parent `independent_controls.py` was read after the independent reconstruction. A fresh invocation exited successfully with the recorded **176,934 exact assertions**. No implementation defect or incorrect mathematical label requiring repair was found.

The actual syzygy weights are justified by tensoring the cyclic minimal resolutions: beta_n=binomial(n+r-1,r-1), d_0=1, d_(n+1)=p^r beta_n-d_n, with negative dimensions supplied by duality. For rank one, the class labels collapse to 0 for C2 and to parity for odd p; restriction of ordinary syzygies gives precisely these stable class maps. For rank at least two, the classification input supports the Z-coordinate interpretation. The dimension and divisibility checks are finite evidence for those consequences, not numerical classification proofs.

The RREF enumeration, closed Möbius formula, normalized indices, signed rational block bounds, finite-support inverse identities, sampled fourth-root unitary species, dimension normalization, actual rank-two induced matrices, and cyclic Jordan tensor ranks are implemented consistently with their stated scope. In particular:

- `weighted_completed_block_bounds` and `weighted_completed_inverse` contain finite-support rational calculations. Their names refer to formulas used in the completion proof; the code itself does not construct or quantify over all infinite-support elements. The report already states the completed-range proof is written separately.
- `full_stable_norm` checks the exact norm expression and triangle bound. It does not itself test the full Green multiplication or J multiplicativity. The report does not claim it does.
- `exact_unitary_species` samples the permitted finite-root characters. The all-character classification is the analytical argument, not this sample.
- The separate F8 controls use x³+x²+1, explicitly distinguished from exact candidate replay. If beta is this alternative cubic's root, alpha=beta inverse satisfies alpha³+alpha+1=0. The two coefficient triples are F2 bases related by an invertible change of the group generators; the all-subgroups induced family is preserved. The parent report correctly calls this a separate F8 construction.
- The F64 check establishes the explicitly constructed field extension and embeds the nonzero coefficient values. It is a finite field-extension check, not evidence covering every field extension. The arbitrary-field theorem is proved independently.

Retain the report's current scope paragraph and source qualifications. Optional naming changes to distinguish finite-support controls would improve readability, but none is necessary to repair the theorem or the existing qualified report.

## Additional exact control

`full_split_controls.py` imports no author or parent-control code and passes **54 assertions**. It independently computes all nilpotent-power ranks of the tensor square of the (p-1)-dimensional cyclic Jordan core for p=3,5,7, giving U tensor U = k plus (p-2) copies of kC. On the resulting actual full Green multiplication it checks e²=e, J(k)²=J(k), J(k)J(U)=J(U), J(U)²=J(k), eJ(k)=eJ(U)=0, e+J(k)=1, J multiplicativity on signed rational inputs, and the exact J norm. This specifically covers the multiplicativity/factor-unit boundary not directly exercised by the parent's norm-only controls. The receipt is `FULL_SPLIT_CONTROLS.json`.

## Strongest verified result and exact gap

The strongest verified result remains intrinsic symmetry of the actual induced-endotrivial stable coordinate span for every nontrivial elementary abelian p-group over every characteristic-p field, with explicit bounded completed Möbius decomposition, together with intrinsic symmetry of its full/projective extension. The F8 witness verifies that the family can be proper.

The exact original gap is the behavior of bounded species on the other actual indecomposable coordinates. Hermitian restriction to this proper subalgebra does not force ambient Hermitian behavior. No ambient nonsymmetric example, universal symmetry proof, novelty certificate, new author turn, or merge-readiness claim follows.

Completion estimate: **100% of this assigned adversarial checkpoint; 0% additional completion certified for the original universal discovery goal.**
