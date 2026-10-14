# An inclusion induced interface between spherical state sum TQFTs

## Conclusion and meaning of the question

Kawahigashi Problem 9.4 asks how the three-dimensional state-sum TQFT associated with fusion data is related to the theory built from a fusion-rule subalgebra with restricted 6j-symbols. It does not specify a comparison arrow or require equality, an equivalence, a state-space inclusion or a numerical quotient. The relevant source is Ohtsuki, printed page 510, with the model on pages 506–509. [Primary source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf#page=138).

Here is a precise inclusion-dependent relation. For a full fusion-subcategory inclusion \(\iota:\mathcal D\hookrightarrow\mathcal C\) over \(\mathbb C\), with the spherical pivotal structure on \(\mathcal D\) inherited from \(\mathcal C\), use the ambient category as a bimodule:
\[
\mathcal M_\iota={}_{\mathcal D}\mathcal C_{\mathcal C},\qquad
 d\triangleright m\triangleleft c=\iota(d)\otimes m\otimes c.
\]
Its inherited spherical trace makes it an admissible topological surface defect in the published Carqueville–Müller construction. That construction yields a full oriented \((3,2)\) defect TQFT whose two bulk restrictions are monoidally naturally isomorphic to the original, separately normalized TVBW theories.

The proof audit accepts this relation for complete finite spherical Barrett–Westbury data and compatible restrictions of their simple-label bases. The conclusion uses existing general theorems, with their hypotheses checked explicitly. No new general defect theorem or mathematical novelty is claimed. [Detailed construction](pass1_interface/INTERFACE_CONSTRUCTION.md) · [Independent audit](pass1_audit/INDEPENDENT_AUDIT.md).

## Complete data and the source interpretation

The historical text describes labels, fusion multiplicity spaces, recoupling data, dimensions and a normalized tetrahedral state sum. Its introductory discussion names symmetry, unitarity and pentagon equations, but is not a complete categorical axiom list. The interpretation used here retains complete spherical state-sum data: unitors, duality maps satisfying the snake identities, pivotal data, spherical traces and the specified normalization are included alongside the associator.

For an explicit reconstruction, let \(I\) be the finite simple-label set, with multiplicity spaces \(H_{ij}^k\). Objects are finite \(I\)-graded vector spaces, and
\[
 (X\otimes Y)_k=\bigoplus_{i,j} X_i\otimes Y_j\otimes H_{ij}^k.
\]
The supplied recoupling matrices define the associator; their coherence equations and the supplied unit, duality and pivotal data give a spherical fusion category. The construction preserves the original data and gauges. It does not choose a different categorification of the fusion ring.

Retain a subset \(J\subseteq I\) containing the tensor unit, closed under duals, and closed under every simple summand occurring in products. Retain the entire multiplicity spaces and all restricted structural maps. Objects supported on \(J\) form a full spherical fusion subcategory. Conversely a replete full fusion subcategory with inherited structure has precisely this form. Every intermediate label in a product of retained labels remains in \(J\), so the associator restrictions have no missing summands.

An arbitrary linear subalgebra is different. In \(\mathbb C[\mathbb Z/3]\), the span of \(1\) and \(g+g^2\) is a subalgebra, since \((g+g^2)^2=2+g+g^2\). It is not spanned by a subset of the original simples. Relabelling \(g\oplus g^2\) as a simple would change its endomorphism algebra. Such a subspace is not the based restriction studied here.

This makes the coverage explicit without imposing unitarity, positivity, pseudo-unitarity or braiding. It does not establish reconstruction from bare arrays satisfying an unspecified subset of the historical equations. [Full model proof](pass1_model/MODEL_AND_ALPHA_AUDIT.md).

## Why the restricted regular bimodule has the required trace

All module associators and unit constraints are inherited from \(\mathcal C\); their coherence follows from its pentagon and triangle. Set
\[
 t_m(f)=\operatorname{tr}_{\mathcal C}(f).
\]
For a decomposition \(m\cong\bigoplus_s s\otimes V_s\), this is
\[
 t_m(f)=\sum_s d_s\operatorname{Tr}(f_s),\qquad d_s=\dim_{\mathcal C}(s).
\]
Each simple dimension is nonzero: the tensor unit appears once in \(s^*\otimes s\), and evaluation and opposite coevaluation are nonzero projection and inclusion maps for that unique summand. Their composite cannot vanish. Consequently the pairing \((f,g)\mapsto t_m(gf)\) is a direct sum of nonzero multiples of ordinary rectangular-matrix trace pairings. It is nondegenerate on every Hom pair, and matrix trace cyclicity gives \(t_m(gf)=t_n(fg)\).

The left partial-trace identity follows by closing the \(\iota(d)\) strand first:
\[
 t_{\iota(d)\otimes m}(F)=t_m\bigl(\operatorname{ptr}^{L}_d(F)\bigr).
\]
It uses exactly the \(\mathcal D\)-duality maps because that structure is inherited. Closing a right \(c\) strand gives
\[
 t_{m\otimes c}(G)=t_m\bigl(\operatorname{ptr}^{R}_c(G)\bigr).
\]
Sphericity identifies both total closures with the same trace. Applying these to the two outer factors in \(\iota(d)\otimes m\otimes c\) gives the simultaneous compatibility; interchange and coherence identify the closure orders. These are identities for arbitrary endomorphisms, not merely dimension identities for identity maps. The scale is fixed by \(t_1(1)=1\).

The inherited pivotal structure is essential. For the identity inclusion of the underlying tensor category \(\mathrm{Vec}_{\mathbb Z/2}\), put the sign spherical structure on the left and the standard structure on the right. The two module axioms force \(t_g=-t_1\) and \(t_g=t_1\), respectively. Only the zero trace can satisfy both, contradicting nondegeneracy. This example lies outside the theorem's hypotheses.

Thus the particular restricted regular bimodule meets CM Definition 5.16. No blanket assertion that every spherical module category has a trace is needed. [Trace proof and conventions](pass1_interface/INTERFACE_CONSTRUCTION.md).

## The published theorem supplies a full defect functor

Carqueville–Müller, *Orbifold Completion of 3-Categories*, CMP 407, article 8 (2026), uses an algebraically closed characteristic-zero field. Proposition 5.17 and Theorem 5.18 place spherical fusion categories and traced bimodules in the relevant orbifold completion. Theorem 6.4 constructs the symmetric monoidal defect bordism functor; Example 6.5 identifies its single-bulk restrictions with TVBW. The complete published version was inspected. [Published source](https://doi.org/10.1007/s00220-025-05434-y).

For a compatible triangulation of a decorated closed surface, one first has a pre-state space. A triangulated cylinder acts as an idempotent. The actual state space is its image, or equivalently the colimit over triangulations. Decorated bordisms act on these state spaces, with identities, sewing, diffeomorphism invariance and disjoint union supplied by the theorem.

The distinguished wall remembers the supplied inclusion: right-\(\mathcal C\)-module endofunctors of the regular module are left tensoring functors. Evaluation at the tensor unit identifies their category with \(\mathcal C\), and the left action recovers \(d\mapsto\iota(d)\), including its tensor constraints. This is an inclusion-specific construction, not an unrelated common property of two theories.

In CM's categorical arrow convention, a \((\mathcal D,\mathcal C)\)-bimodule points from \(\mathcal D\) to \(\mathcal C\). A geometric positive-normal convention must be stated separately. Reversal uses the specified opposite/adjoint label with exchanged action sides. No cancellation with the reversed wall is assumed.

The theorem concerns a full \((3,2)\) defect theory. It does not establish a fully extended oriented theory down to points. It also does not identify every defect amplitude with Meusburger's fixed-boundary state-sum model; CM explicitly leaves a detailed comparison for further work. [Full functor audit](pass1_defect/RESULT.md).

## Exact bulk and boundary normalization

Write \(\Delta_{\mathcal A}=\sum_s d_s^2\) for \(\mathcal A=\mathcal D,\mathcal C\). Each is nonzero over \(\mathbb C\). The vertex normalization is \(\Delta_{\mathcal A}^{-v}\) for that bulk's own label system. In particular,
\[
 \operatorname{TVBW}_{\mathcal A}(S^3)=\Delta_{\mathcal A}^{-1}.
\]
The restricted-label part of the ambient sum, retaining the ambient vertex factor, is generally not the subcategory invariant.

For nonempty boundary, the bulk comparison is not equality of raw matrices. Carqueville–Runkel–Schaumann, Theorem 4.5 and equation (4.70), gives a diagonal rescaling on colored boundary pre-spaces. Its entry for a colored graph \((\Sigma,\Gamma;c)\) is
\[
 f_{\mathcal A}(\Sigma,\Gamma;c)
 =\Delta_{\mathcal A}^{|\Sigma\setminus\Gamma|/2}
   \prod_{e\in\Gamma_1}d_{c(e)}^{-1/2}.
\]
The number in the exponent counts complementary regions. Roots are chosen consistently with the orbifold presentation. This factor depends on the coloring. With the corresponding diagonal operators,
\[
 Z_{\mathrm{orb}}(Y^t)=F_{\mathrm{out}}^{-1}p_{\mathrm{TV}}(Y^t)F_{\mathrm{in}}.
\]
The operators conjugate cylinder projectors and induce the monoidal natural isomorphisms on actual state spaces. Each bulk is treated separately. The formula does not purport to normalize all mixed-phase raw matrices. The auxiliary CRS comparison was inspected in arXiv v2, not a newly retrieved publisher PDF. [Inspected theorem and equation](https://arxiv.org/pdf/1809.01483v2#page=41).

For standard untwisted \(\mathrm{Vec}_G\), a spanning-tree gauge fixing counts \(|G|^{v-1}|\operatorname{Hom}(\pi_1M,G)|\) flat edge assignments on a connected manifold. The vertex factor gives
\[
 \operatorname{TVBW}_{\mathrm{Vec}_G}(M)
 =\frac{|\operatorname{Hom}(\pi_1M,G)|}{|G|}
 =\sum_{[\rho]}\frac1{|C_G(\operatorname{im}\rho)|}.
\]
This is groupoid cardinality, not the unweighted number of conjugacy classes. The distinction records a narrow convention discrepancy between the source's displayed equation (48) and its adjacent prose example. It does not invalidate the source question or license a paper-wide error claim.

## What the finite examples establish

The inclusion \(\mathrm{Vec}_{C_3}\subset\mathrm{Vec}_{S_3}\) has sphere values \(1/3\) and \(1/6\), respectively. Its torus state-space dimensions are \(9\) and \(8\). The validation constructs the full rational gauge-average cylinder projector on commuting pairs, checks idempotency and computes its rank by exact elimination. Orbit enumeration, Burnside averaging and the closed-cylinder trace independently give the same ranks.

The commuting-pair groupoid mass is \(3\) in both examples; it is not the surface-space dimension. The normalized values on \(S^3,S^2\times S^1,L(2,1),L(3,1),T^3\) have subcategory-to-ambient ratios \(2,1,1/2,2,9/8\), so there is no manifold-independent quotient.

A five-vertex sphere and its six-vertex 1–4 subdivision have \(81\) and \(243\) flat \(C_3\)-labelings. Correct normalization gives \(1/3\) twice. The incorrect ambient \(S_3\) factor gives \(1/96\) and \(1/192\). This directly detects the normalization error.

The unequal torus dimensions exclude universal injectivity in the subcategory-to-ambient direction. Unequal sphere values exclude a monoidal natural transformation between these ordinary normalized bulk theories in either direction: naturality at the closed bordism \(S^3:\varnothing\to\varnothing\), with an invertible monoidal unit component, would force equality of those scalars. These facts do not obstruct the wall in a decorated theory.

Matrix-unit tests also cover both partial traces, mixed off-diagonal terms, rectangular cyclicity, an inherited sign-pivotal example and incompatible pivots. Each of normal, optimized and double-optimized Python completes 17,857 explicit checks with identical output. These are finite consistency tests, not a computational proof of the general published TQFT theorem. [Validation and exact outputs](pass1_validation/VALIDATION_REPORT.md).

## The actual alpha induction inclusions

In BEK's type III subfactor setting, the canonical Q-system is the additional algebraic object. The genuine inclusions are between the full, chiral, ambichiral and specified subsystem categories. Their standard spherical structures restrict correctly. The α-induction functor itself need not be fully faithful, so it is not renamed an inclusion. BEK Theorems 3.9 and 4.6 already allow degenerate braiding; their product-description corollaries impose further nondegeneracy assumptions. [BEK preprint](https://arxiv.org/pdf/math/0002154v1).

The nonunitary categorical branch uses Kirillov–Ostrik's finite semisimple ribbon category \(\mathcal B\), with a connected commutative rigid algebra \(A\), nondegenerate algebra pairing, nonzero categorical dimension and trivial twist. Under their stated hypotheses, the genuine full spherical inclusion is
\[
 \operatorname{Rep}^0(A)\subset\operatorname{Rep}(A),\qquad
 \dim_{\operatorname{Rep}(A)}(X)=\dim_{\mathcal B}(X)/\dim_{\mathcal B}(A).
\]
These conclusions precede the extra modularity assumptions. Neither the forgetful functor to \(\mathcal B\) nor the free-module functor from it is substituted for this inclusion. [KO preprint](https://arxiv.org/pdf/math/0101219v3).

Once the actual inherited spherical inclusion is established, a singular S-matrix creates no new trace obstruction. The interface does not calculate all quantum doubles, construct a minimal modular extension, or remove hypotheses from BEK's or Sato's stronger formulas. [Detailed coverage and limits](pass1_model/MODEL_AND_ALPHA_AUDIT.md).

## Supplementary relative center description

With endofunctor tensor product defined by composition, the wall endomorphism category is
\[
 E_\iota=\operatorname{Fun}_{\mathcal D|\mathcal C}(\mathcal M_\iota,\mathcal M_\iota)
 \simeq Z_{\mathcal D}(\mathcal C).
\]
A relative central object has a half-braiding only against \(\iota(\mathcal D)\). The two bulks have underlying tensor functors \(Z(\mathcal D)\to E_\iota\leftarrow Z(\mathcal C)\). Their central lifts have the braided product domain \(\overline{Z(\mathcal D)}\boxtimes Z(\mathcal C)\), where the bar reverses the braiding. Kong–Zheng's theorem gives the corresponding braided equivalence with \(Z(E_\iota)\). It does not identify the two bulk centers with one another.

The relative center need not itself be braided. The untraced wall remembers the inclusion up to inner conjugacy, with the two bulk labels fixed; a unit marking sharpens this to monoidal natural isomorphism. Preservation of the selected spherical trace imposes the separate condition \(\dim(u)=1\) on the conjugating invertible object. The center statements alone neither recover a selected trace nor prove a ribbon-compatible or oriented-TQFT comparison.

At the underlying bimodule level the distinguished wall is invertible exactly when \(\iota\) is a tensor equivalence. The detailed report checks composition order, braiding reversal and the difference between untraced algebra and normalized physical defect data. [Supplementary proof and sources](pass1_center/RELATIVE_CENTER_INTERFACE.md).

## Reading the acceptance

The accepted outcome is a concrete inclusion-induced interface, not an unconditional claim about every possible reading of a historical axiom sketch. It covers the complete spherical based interpretation and the specified α-induction instances without a modularity restriction. The source question does not require an artificial stronger target to remain open after this relation has been established. No novelty or exhaustive present-day literature claim is made. The full proofs, independent audit, source metadata and reproducibility instructions remain available through the [results index](RESULTS_INDEX.md).
