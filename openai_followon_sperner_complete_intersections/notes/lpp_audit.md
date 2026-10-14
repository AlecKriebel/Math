# Independent audit of the Artinian lex-plus-powers paper

Audit checkpoint: 2026-10-06 22:16:57 America/Los_Angeles (2026-10-07 05:16:57 UTC).

Auditor: independent LPP branch. No findings from the companion-proof audit were used. Copied upstream sources were read, never edited. No external individual was contacted. This branch performed no commit, push, or publication.

Completion estimate for this scoped audit: **100%**. This means that the LPP reduction, its dependency interface, and local auxiliary arguments have been reviewed and finite falsification tests recorded. It does not certify the imported construction or completion of the project's mathematical goal.

## Verdict and strongest verified statement

**Conditional validation with an exact upstream dependency.** No incorrect inference was found in the LPP paper's reduction from its stated commuting-form theorem to one Hilbert-matching monomial ideal containing the prescribed powers. Its transferred-resolution and filtered-Koszul arguments also pass this local proof review. The paper imports its foundational commuting-form theorem from the companion; the deep division-algebra construction is not certified by this audit.

The strongest verified result is:

> If a full homogeneous regular sequence over C admits the commuting forms, triangular identities, and full left-division-algebra basis stated in `01-forms.tex`, every homogeneous ideal containing that sequence has a Hilbert-matching monomial replacement containing the corresponding pure powers. Those same hypotheses also imply the claimed Betti domination by that monomial replacement.

This conditional implication has a short, checkable graded-module proof. A central unresolved gap in the companion construction would remain central here. Conversely, an isolated defect in a later Betti-only step would not destroy the HF reduction: monomial extraction and established pure-power Hilbert compression suffice.

## Exact claim and source interface

Write S=C[x_1,...,x_n], 2<=a_1<=...<=a_n, P=(x_1^{a_1},...,x_n^{a_n}), and let a homogeneous I contain a full regular sequence f_i of degrees a_i. The target HF claim is existence of **one** monomial M containing P such that

\[
\dim_{\mathbb C}(S/M)_d=\dim_{\mathbb C}(S/I)_d\qquad\text{for every }d.
\]

The LPP paper states this with Betti domination in `build/sections/03-monomial.tex`, lines 93–108, label `mono:bound`. Its proof imports the construction at lines 112–124.

The interface, `build/sections/01-forms.tex`, lines 10–33, label `thm:forms`, requires a genuine finite-dimensional central **division** algebra Delta over k/C; commuting degree-one t_i in Delta[x]; identities

\[
t_h^{a_h}=c_hf_h+\sum_{\ell<h}B_{h\ell}f_\ell+\sum_{\ell>h}C_{h\ell}t_\ell,
\qquad c_h\ne0;
\]

and a left-Delta basis {t^alpha:alpha in N^n} of the **entire** algebra Delta[x]. A basis only of its complete-intersection quotient would not justify the proof. The strengthening is explicit at `01-forms.tex`, lines 35–40. It is also explicitly stated in the companion's `01-introduction.tex`, lines 31–61. No mismatch between the cited theorem and the used interface was found.

## Reconstructed HF proof

Put N=Delta[x], m=dim_k Delta, and let T=k[y_1,...,y_n] act on the **right** by y_i->t_i. The full basis gives N=Delta tensor_k T as a right-T module. Set W=IN. The original complex-coefficient polynomials are central, so W is a two-sided ideal; in particular it is right-T linear and left-Delta linear.

Within each degree order exponent positions by increasing lex order of (alpha_n,...,alpha_1). At alpha, let V_alpha be the possible coefficients of elements of W with zero earlier coefficients. Left multiplication by Delta makes V_alpha a left ideal, hence either zero or all Delta (`03-monomial.tex`, lines 136–147). Right multiplication by t_i translates every exponent by e_i. Thus nonzero positions are upward closed and define a single ordinary monomial M (lines 149–163).

The triangular identities put

\[
t_h^{a_h}-\sum_{\ell>h}C_{h\ell}t_\ell\in W.
\]

Every exponent in the second summand has a positive coordinate of index greater than h, so it is strictly after a_h e_h. The coefficient at that first position is exactly 1, with no possible cancellation. Hence x_h^{a_h} belongs to M (lines 165–178).

Finite elimination, equivalently the filtration in `02-filtered.tex`, lines 155–171, gives equality of dimensions for N/W and its leading-position quotient. These are respectively m dim_C(S/I)_d and m dim_C(S/M)_d. Cancelling the positive integer m gives the HF equality in every degree (`03-monomial.tex`, lines 180–197). No Betti comparison is used in this argument.

## Falsification of a tempting weakened coefficient-space lemma

A finite-dimensional central simple algebra cannot replace the division algebra in the **local coefficient-space step**. The following is an explicit counterexample to that weakened step, not to the paper's actual hypothesis or full theorem.

Let D=Mat_2(k) and

\[
t_1=E_{11}x_1+E_{22}x_2,\qquad
t_2=E_{11}x_2+E_{22}x_1.
\]

These t_i commute. In each degree their ordered monomials form a full left-D basis: right multiplication of a left coefficient by E_11 and E_22 separates its two column spaces, and exponents are interchanged only in the second column space. The change of basis is invertible.

Take I=(x_1,x_2^2), which contains the scalar regular sequence (x_1^2,x_2^2). In degree one, W_1=Dx_1. Since

\[
x_1=E_{11}t_1+E_{22}t_2,
\]

the coefficient space at t_1, the paper's first position, is exactly DE_11. Its k-dimension is 2, rather than zero or dim_k D=4. The step at `03-monomial.tex`, lines 141–147, therefore fails for matrix coefficients. This example tests that local step; these t_i are not claimed to satisfy all the paper's triangular identities. A split matrix representation by itself cannot support the given HF proof. An upstream division gap would need a separate replacement argument, not just a Betti repair.

## Local adversarial checks

* **Resolution transfer**, `03-monomial.tex`, lines 37–87: N is left-S free and right-T free with degree-zero generators. Tensoring preserves exactness, and positive-degree differential entries become positive-degree T entries, so minimality is preserved. No coefficientwise commutation with arbitrary elements of Delta is silently assumed.
* **Filtered Betti comparison**, `02-filtered.tex`, lines 173–224: adding the exterior exponent 1_sigma gives a common internal-degree filtration. Associated graded maps are V/V_alpha -> V/V_(alpha+e_i); ranks can drop, giving the correct Betti inequality direction.
* **Root-of-unity stabilization**, `04-stabilization.tex`, lines 67–138 and 157–216: nested-factor ratios are polynomials; the unitriangular maps intertwine the complexes. The strict-prefix coefficient is nonzero because 0<u_ell<a_ell. The degree ordering a_h<=a_ell is explicitly used to preserve P.
* **Stable box compression**, `05-boxes.tex`, label `box:inequalities`: the zero-slice tail filling respects all capacities, reflected-complement stability has the correct direction, and the shadow count follows by an allowed last-variable transfer. Independent finite enumeration checked **63,319 stable sets**, **2,138 degree boxes**, and **205 bound tuples**, including **1,558 unsorted-bound boxes**. No counterexample; no test-domain boxes skipped. Largest degree-box size 70. Script/result: `notes/lpp_box_tests.py`, `notes/lpp_box_tests.json`; explanatory audit: `notes/lpp_box_tests.md`. Bounded tests corroborate the proof review, but are not arbitrary-size certification.
* **Koszul endpoints**, `06-tor.tex`: reduction H/zH preserves the minimal resolution because z is injective on H. Middle coefficient components are annihilated by all earlier variables. Koszul ranks decrease under submodule or quotient, and the endpoint inclusions have the required directions.
* **Boundary cases**: I=S, empty/full degree boxes, n=1, negative internal degrees, and outside-range Koszul positions are explicitly covered.
* **Fields**, `08-characteristic-zero.tex`: for the project's full-length Artinian target, only coefficient descent is needed. A finitely generated coefficient field F_0/Q embeds in C; faithful flatness descends regularity and field extension preserves HF and monomial exponents. The whole original field need not embed in C. The paper's shorter-sequence Artinian reduction is dispensable for this target.

## Prior theorem and exact remaining gap

The pure-power monomial comparison is independent prior work: [Mermin–Murai, The Lex-Plus-Powers Conjecture holds for pure powers](https://math.okstate.edu/people/mermin/papers/the_lex_plus_powers_conjecture_holds_for_pure_powers.pdf), Theorem 3.1, covers characteristic-zero ideals containing a monomial regular sequence. I checked the primary theorem statement. Its HF component is already a consequence of Clements–Lindström; this dependency does not run through the 2026 papers.

Accordingly, a Betti-only failure in LPP Sections 4–6 would leave the HF conclusion intact once `mono:bound` is supplied. A failure of the imported division construction or full ordered-basis hypothesis would leave that conclusion unproved by this route.

**Exact remaining dependency:** independently validate existence of k,Delta,A,t_1,...,t_n in the companion's commuting-form theorem for every full regular sequence. No alternative construction for arbitrary regular sequences was obtained here. This audit must not be promoted to unconditional certification of EGH or of the project's Sperner conclusion before that dependency is resolved.
