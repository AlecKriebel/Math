# Heegner divisors versus all effective divisors

**OWR-15582-004 · ID 30003570 · reviewed 6 October 2026**

## Outcome and scope

This bounded investigation does **not** establish equality or strict inclusion for the K3 moduli spaces in the question. Five approaches were examined. The deliverable is a source-grounded status assessment and elementary, fully proved reductions identifying exactly what a solution must still supply. These reductions are not claimed to be novel or to solve any previously open case.

No earlier substantive attempt was found in the supplied complete problem/report pair or the bounded repository-history searches. The inherited report was empty; the accompanying dated literature paragraph was only triage. Provenance checks matched all supplied hashes. This gate is bounded negative evidence, not an exhaustive theorem about historical absence.

## Setting

Fix a positive integer d. Write

\[
 X_d=\mathcal F_{2d}=\widetilde O^+(\Lambda_{2d})\backslash\mathcal D_{\Lambda_{2d}},
 \qquad
 \Lambda_{2d}=U^{\oplus2}\oplus E_8(-1)^{\oplus2}\oplus\langle-2d\rangle.
\]

Here the polarization is primitive, big and nef. Set

\[
 V_d=\operatorname{Pic}(X_d)\otimes\mathbb R,
 \quad C_d=\operatorname{cone}_{\mathbb R_{\ge0}}\{[P]:P\text{ primitive Heegner}\},
 \quad K_d=\overline{\operatorname{cone}_{\mathbb R_{\ge0}}\{[D]:D\text{ effective}\}}.
\]

Closure is in the finite-dimensional real vector space V_d, with classes modulo linear equivalence. Thus C_d is contained in K_d. Positive multiplicities in conventions for Heegner divisors do not change their rays. One must not replace X_d by the ample-polarization locus or use numerical equivalence on an unspecified compactification without justification.

### Approach 1: exact source and later-literature verification

The original question is on p. 2439 of Möller's contribution, joint with Bruinier, in Oberwolfach Report 39/2017 [A]. The workshop dates were 27 August–2 September 2017; the broad catalog citation's 2018 date is not the workshop year.

Bruinier–Möller [B, Theorem 1.1] proves that C_d is rational polyhedral. Its introduction distinguishes this statement from equality with K_d. Picard-space generation establishes full dimension, not positivity of coefficients. The Hodge class λ lies in the interior of C_d; see [B, §§3–4] and [D, introduction].

Barros–Flapan–Zuffetti [C, v2, §1.3] reports that equality is not known for any K3 degree. Corollary 1.7 concerns a different modular variety associated to U²⊕A₁(−1)⊕A₁(−3), parametrizing a generalized-Kummer-fourfold case. It is not a solution for X_d. The public arXiv history showed v2 dated 8 December 2025.

The published paper [D] separates finite generation, computation of generators, and equality as three questions; it addresses computation. The February 2026 preprint [E] proves finite generation of the K3 rational Picard **vector space** and provides a degree-two slope bound discussed below. Neither result supplies the missing positivity assertion. Targeted searches found no later resolution, which is not proof that none exists.

### Approach 2: modular relations and Hodge twisting

A tempting route is to express arbitrary classes using Heegner divisors and remove any negative coefficients using positive Hodge relations. The following calculation pinpoints the obstruction.

**Lemma 1 (exact twisting threshold).** Let C be a full-dimensional closed polyhedral cone in a real vector space V, with a finite nonzero supporting description

\[
 C=\{v:\ell_j(v)\ge0\text{ for }1\le j\le r\}.
\]

For h in the interior of C, and any v in V, define

\[
 t_0(v)=\max\left(0,\max_j\frac{-\ell_j(v)}{\ell_j(h)}\right).
\]

For t≥0, one has v+th∈C exactly when t≥t₀(v).

*Proof.* Every nonzero supporting functional is strictly positive at h: otherwise a small displacement from h in a direction on which the functional is negative would contradict interiority. Each defining inequality for v+th is equivalent to t≥−ℓ_j(v)/ℓ_j(h). Taking their maximum proves the assertion. ∎

Applied to C_d and h=λ, this proves that any class, even a class outside K_d, becomes an NL-cone class after adding enough λ. It cannot prove that an effective class already lies in C_d. For example, in the first quadrant of R², v=(−1,1) and h=(1,1) satisfy v+h∈C but v∉C. Subtracting the Hodge contribution is precisely the unjustified step. No uniform positivity argument for t₀([D])=0 on all effective D was obtained.

### Approach 3: extremality and low-dimensional geometry

Proving some Heegner rays extremal in K_d does not generally identify K_d. Even proving every extremal ray of C_d remains extremal is insufficient in dimensions at least three.

**Example 2.** In R³ let

\[
 C=\operatorname{cone}(e_1,e_2,e_3),\qquad
 K=\operatorname{cone}(e_1,e_2,e_3,(-1,1,1)).
\]

Then C⊊K, both cones are closed and pointed, and all three extremal rays of C remain extremal in K.

*Proof.* The added generator lies outside C. The functional x+y+z is 1 on each of the four generators, so the finitely generated cone K is pointed. The nonnegative functionals y+z, x+2z and x+2y on K expose respectively the rays through e₁,e₂,e₃: direct evaluation on the four generators shows the indicated ray is their entire zero set. ∎

There is an important rank-two exception. If C⊂K are full-dimensional closed pointed cones in a two-dimensional space and both boundary rays of C are extremal rays of K, then C=K. Indeed, intersect K with an affine line defined by a strictly positive functional. The result is a closed segment; its two endpoints are exactly its extremal rays after normalization. Both are already the normalized boundary generators of C.

For d=1, [D, Table 1, p. 32] gives two NL rays, represented in its sign convention by P_{−1,0} and P_{−1/4,ℓ_*}, and Picard dimension two. The second ray is unigonal. The simple sufficient test in [C, Theorem 1.1] gives 1/2<1 for the unigonal case (h,a,d)=(1,1,1), whereas for the nodal case (0,0,1) it gives 4<1, which fails. This failure proves neither non-extremality nor strict inclusion. The required second extremality proof was not obtained.

### Approach 4: finite separating certificates and boundary-safe curves

**Lemma 3 (finite certificate reduction).** Use any finite supporting description C_d={v:ℓ_j(v)≥0 for all j}. Then:

1. C_d=K_d if and only if every ℓ_j is nonnegative on every prime effective divisor class.
2. If C_d⊊K_d, there is an actual prime effective divisor E and an index j with ℓ_j([E])<0.

*Proof.* The forward implication in (1) is immediate. Conversely, primewise nonnegativity extends to finite effective real sums and then to their closure by continuity; hence K_d⊂C_d. For (2), choose x∈K_d\C_d. Some ℓ_j(x)<0. By definition of K_d, an effective real divisor class sufficiently close to x has negative ℓ_j. At least one of its finitely many prime components then has negative ℓ_j. ∎

Thus a counterexample cannot consist solely of a formal vector in V_d outside C_d: its effectiveness must be established. Nor does checking finitely many known effective classes settle equality.

The compactification issue can be handled explicitly. Let \bar X be a normal projective Q-factorial compactification of a normal Q-factorial X, and let B_i be the prime divisors of \bar X\X. Assume the real Picard spaces used here are finite dimensional. Restriction r satisfies

\[
 \operatorname{Pic}(\bar X)_{\mathbb R}
   \twoheadrightarrow\operatorname{Pic}(X)_{\mathbb R},
 \qquad \ker r=\operatorname{span}_{\mathbb R}\{[B_i]\}.
\]

To see this, take closures of Weil divisors on X and use Q-factoriality. If a divisor restricts to a principal divisor, subtract the divisor of the same rational function on \bar X; the remainder is boundary-supported. Tensoring the resulting rational exact sequence with R preserves exactness.

Writing K for the corresponding closed effective cones, one always has

\[
 K_X=\overline{r(K_{\bar X})}.
\]

Indeed r(Eff(\bar X))=Eff(X), because effective divisors lift by closure. Continuity gives r(K_{\bar X})⊂K_X, while the equality for effective cones gives the reverse inclusion after taking closure. The unclosed image must not silently replace its closure.

For a normal compactification with boundary of codimension at least two, closure instead directly identifies **Weil class groups**. This does not assert that its Cartier Picard group or its numerical divisor space agrees with V_d. In the K3 Baily–Borel model the boundary has dimension at most one [C, proof of Corollary 3.3]; on a resolution or toroidal model there can be divisorial boundary.

**Lemma 4 (sufficient curve certificate for a supporting functional).** In the compactification setting above, let C⊂Pic(X)_R be generated by designated effective prime divisor classes. Let ℓ be nonnegative on C. Suppose a numerical curve class γ on \bar X:

- annihilates every B_i;
- induces ℓ under the restriction quotient, meaning γ·L=ℓ(r(L)) for every divisor class L on \bar X;
- is represented by complete integral curves of constant numerical class in an algebraic family whose union is dense in the closure of one designated prime divisor S.

Then ℓ is nonnegative on every effective divisor on X.

*Proof.* For a prime E≠S, density of the family in \bar S supplies a member not contained in \bar E: otherwise \bar S⊂\bar E, impossible for distinct prime divisors. A positive Cartier multiple of the effective Q-Cartier divisor \bar E restricts to a nonzero section on the normalization of that complete curve. Its zero divisor has nonnegative degree. Thus ℓ([E])=γ·\bar E≥0. For E=S use [S]∈C and the assumed nonnegativity of ℓ. Extend by linearity to effective sums. ∎

Producing such witnesses for every ℓ_j would prove equality by Lemma 3. Boundary annihilation guarantees that changing a lift by boundary does not alter the intersection. Complete curves avoiding the boundary provide a sufficient way to achieve this. Existing negative-self-intersection arguments aim to prove extremality of a divisor; they do not automatically give these globally nonnegative supporting functionals. No complete set of the needed witnesses was constructed.

### Approach 5: exact degree-two slope reduction

Put X=X₁, let u be the reduced unigonal class, and let p be a positive representative of the other NL ray. The literature inputs are: dim Pic(X)_R=2 and C=cone(u,p) [D, Table 1]; u is extremal in K [C, Example 1.2; E, §4.1]; and p=Aλ−Bu with A,B>0 and A/B=150/57 [E, Proposition 4.4 and proof]. Normalization of p does not affect the ratio.

Define the slope of an effective class v=aλ−bu as a/b when a,b>0, and infinity otherwise. Let s be the infimum of these slopes.

**Proposition 5.** Under these literature inputs,

\[
 C=K\quad\Longleftrightarrow\quad s=150/57.
\]

Moreover, strict inclusion would be witnessed by a prime effective divisor of finite slope strictly less than 150/57.

*Proof.* The nonzero ray R_{≥0}u is extremal in the full-dimensional closed two-dimensional cone K. Consequently K is pointed and this ray lies on a supporting line. That line is a=0 in the basis (λ,u). Since λ∈C and λ is not proportional to u, K lies in a≥0 and K∩{a=0}=R_{≥0}u.

Set q=A/B. From p=Aλ−Bu,

\[
 a\lambda-bu=(a/A)p+(aB/A-b)u.
\]

For a>0, this belongs to C exactly when aB/A−b≥0. If b≤0 this is automatic. If b>0 it is exactly a/b≥q. Classes in K with a=0 already lie on the u-ray. Since p is effective with slope q, the infimum satisfies s≤q. Thus s=q precisely when every effective class is in C; closedness of C then yields K=C. Conversely K=C forces all finite slopes to be at least q. If inclusion is strict, Lemma 3 gives a prime effective class outside C, and the preceding coefficient test shows its slope is finite and less than q. ∎

The bound proved in [E, Proposition 4.4] is

\[
 1/1984\le s\le150/57.
\]

It leaves the necessary endpoint undecided. The displayed lower constant is reported from that preprint; its modular-form computation was not independently rerun here. No divisor with slope below the upper endpoint was constructed, and no matching lower bound was proved.

## Final assessment

The original K3 equality-versus-strictness question remains **unresolved by this investigation**. The available statements establish finite NL geometry and selected extremal rays, while the missing condition is positivity against all prime effective divisors. The degree-two reduction isolates a concrete unanswered endpoint rather than resolving it.

No theorem of mathematical openness is asserted. No existing software was executed for cone calculations, no finite search is substituted for a proof, and no independent computational certification of the cited papers is claimed. The authored lemmas above are elementary reductions with complete proofs, conditional only where their stated geometric or literature inputs require it.

## References

[A] Martin Möller, joint with Jan H. Bruinier, “Cones of Heegner divisors,” *Komplexe Analysis*, Oberwolfach Report 39/2017, pp. 2439–2440. https://doi.org/10.4171/owr/2017/39

[B] Jan Hendrik Bruinier and Martin Möller, *Cones of Heegner divisors*, J. Algebraic Geom. 28 (2019), 497–517. https://doi.org/10.1090/jag/734

[C] Ignacio Barros, Laure Flapan and Riccardo Zuffetti, *Extremal divisors on moduli spaces of K3 surfaces*, arXiv:2504.16730v2 (8 December 2025). https://arxiv.org/html/2504.16730v2

[D] Ignacio Barros, Pietro Beri, Laure Flapan and Brandon Williams, *Cones of Noether–Lefschetz divisors and moduli spaces of hyperkähler manifolds*, Math. Ann. 394, article 27 (2026). https://doi.org/10.1007/s00208-026-03372-1

[E] Ignacio Barros, Shi He and Paul Kiefer, *Finite generation of Noether–Lefschetz divisors and the slope of the moduli space of cubic fourfolds*, arXiv:2602.08463v1 (9 February 2026). https://arxiv.org/html/2602.08463v1
