# Exact logarithmic and additive integration audit

Authored for row 1793, shared mathematical pass 1/5, 2026-10-16. Scope: the fixed complex SE(2) pair in CONTRACT.md. This report audits and supplies classical algebraic-integration tools; it makes no novelty claim.

## Result in brief

1. A logarithmic multiple is decidable by finite exact algebraic operations for algebraic-number coefficients, and more generally for coefficients in an explicitly presented finitely generated characteristic-zero field. It does not require a Mordell–Weil rank computation or numerical period recognition.
2. Rational residues alone are insufficient. After clearing residue denominators, the residue divisor must be torsion; even then a residual holomorphic differential must vanish.
3. Torsion testing has a terminating bound: spread a model over a normal finite-type integral Z-base and use two smooth reductions in distinct residue characteristics. A completely explicit, very inefficient annihilator follows from the Weil bound without calculating Jacobian equations or its exact point counts.
4. Once a finite cover is fixed, exactness of a differential is finite linear algebra in an explicitly bounded Riemann–Roch space. Further finite covers cannot repair failed exactness, by trace.
5. Finite multiplicative monodromy is equivalent to the logarithmic condition only with the at-most-simple-pole condition included. Trivial monodromy alone permits essential singularities.

## 1. Notation and coefficient model

Let D/C be a smooth projective connected curve with meromorphic differential ω. For the signature construction the preferred differential is

ω = (i du/v − du/u)/2,

not merely η = i du/v. The companion forms are ρ = du/(2v) and σ = du/(2uv).

The mathematical statements below apply over C. An exact decision algorithm needs a representation of the coefficients. A sufficient representation is an explicitly presented finitely generated field k of characteristic zero, embedded in C, with:

- a declared algebraically independent transcendence basis T over Q;
- a finite algebraic extension of Q(T), given by exact polynomial equations and a chosen component/embedding;
- exact representations of the input coefficients in that field.

The case k a number field, in particular all input coefficients algebraic numbers, is simpler. Finite algebraic extensions of k may be taken during normalization, splitting polar supports, and constructing a cover. This preserves the model. We may include i in k and enlarge k so D is geometrically connected and all points supporting relevant divisors are k-rational. Such enlargement is finite because each finite support consists of algebraic closed points.

Every finite collection of actual complex coefficients generates a finitely generated Q-field, so a field of definition exists for every complex input. This existence does not provide an algorithm which discovers the algebraic relations among arbitrary complex-number names or numerical approximations. The algorithm claim is conditional on the explicit exact representation just stated. Risch's original account makes the same explicit-transcendence-basis distinction (1970, p.606).

All curve calculations are relative to k: d kills k. Pole orders and residues are computed on the smooth projective normalization, including infinity. A residue is tested for membership in Q, not just in the constant field k. For finitely generated presentations this is decidable, for example by eliminating to find the algebraic relation of the residue over Q: if it is transcendental there is none; if algebraic, its minimal polynomial and exact representation decide whether its degree is one. Equivalently one can first test vanishing of the extended partial derivations with respect to T, then perform algebraic-number calculations on the constant algebraic subfield.

## 2. Intrinsic logarithmic test and exact exponent

Say ω is torsion-logarithmic if nω = df/f for some positive integer n and f∈C(D)*.

First reject if ω has a pole of order at least two or a nonrational residue. If all poles are simple and all residues rational, let m be their least common positive denominator (m=1 when there are no poles), and form the integral degree-zero divisor

A = Σ_P m Res_P(ω) P.

The residue theorem gives deg A=0. Let [A]∈Pic^0(D)=J(D)(C).

**Proposition.** The differential ω is torsion-logarithmic exactly when:

(a) [A] is torsion, of some order t≥1; and
(b) for a function f with div(f)=tA, the holomorphic differential

H = mtω − df/f

is zero.

If these conditions hold, the smallest logarithmic exponent is n=mt. The choice of f up to a nonzero constant does not affect H.

**Proof.** For any nω=dg/g, comparison of residues says m divides n and div(g)=(n/m)A. Therefore t divides n/m. Conversely if tA is principal, H has no poles: the residues cancel and both summands have at most simple poles. If n is any multiple of mt and div(g)=(n/m)A, then g/f^(n/(mt)) has divisor zero, hence is constant. Consequently nω−dg/g = (n/(mt))H. Thus another larger exponent cannot fix a nonzero H, and when H=0 the least possible exponent is mt. This also covers A=0: t=m=1 and ω must be zero. ∎

This identifies the repair needed in the imported report's proposed algorithm: testing whether A itself is principal is too strong; its divisor class may have nontrivial torsion order. Testing only whether A is torsion is too weak because H may be a nonzero holomorphic differential.

## 3. A finite, input-derived torsion annihilator

This subsection makes the preceding torsion predicate finite. Its arithmetic mechanism is classical; Risch 1970, pp.607–608, explicitly uses two good reductions in different residue characteristics.

Let k be a finitely generated subfield of C over which D and A are defined. Choose a normal integral affine scheme B of finite type over Z with function field k, and after shrinking B spread D to a smooth projective family C→B with geometrically connected fibers of genus g. Its relative Jacobian J→B is an abelian scheme. Choose closed points b1,b2∈B with finite residue fields F_(q1), F_(q2) of distinct characteristics p1≠p2.

These are finite algebraic choices; they can be found in the exact presentation model. The image of nonempty B in Spec Z contains a nonempty open set (the generic fiber is nonempty and the image is constructible), so there are closed points above infinitely many primes. A closed point over a finite field has a finite residue field. Consequently an enumeration of finite fields and solutions of the equations of B eventually finds the required pair. The normal base and smooth family can be obtained by normalization, generic spreading out and localization away from their computable bad loci. No numerical approximation of the given complex embedding is used.

**Specialization lemma.** For any closed b of residue characteristic p, prime-to-p torsion in J(k) injects into J_b(κ(b)).

**Proof.** Suppose a k-rational point T has order N prime to p. Over the normal connected base B[1/N], the N-torsion group scheme J[N] is finite étale. The generic rational section T extends uniquely to a section over B[1/N]: its closure is a finite birational component over a normal base and hence is isomorphic to the base. Two sections of a finite étale separated scheme which agree at one point agree on an open-and-closed locus. Since the base is connected, a torsion section specializing to zero is the zero section. This applies also to the difference of two torsion sections, proving injectivity. ∎

Put M_i=#J_bi(F_(qi)). If T has order r=p1^a s with gcd(s,p1)=1, then s divides M_1, while p1^a divides M_2 since p1≠p2. In particular r divides M_1 M_2. Thus B0=M_1 M_2 annihilates J(k)_tors. This is an annihilator, not a bound requiring a search through all positive integers.

There is no need to compute either M_i. The Weil bound gives

M_i ≤ (1+sqrt(q_i))^(2g) ≤ (q_i+1)^(2g).

Define the explicit integer

H0 = max((q1+1)^(2g), (q2+1)^(2g)),    B0 = H0!.

Then s and p1^a individually divide H0!, and they are coprime; hence r divides H0!. Therefore this very large B0 also annihilates all torsion in J(k). In genus zero, take B0=1 immediately.

The use of k-rational torsion is sufficient even though the geometric theorem is over C. The explicit divisor A defines a k-rational class. If nA becomes principal after extending k to C, then the corresponding line bundle has a nonzero global section over C. Global sections commute with extension of the ground field; thus its Riemann–Roch space over k is already nonzero and nA is principal over k. Equivalently the k-point [A] becomes zero after extension only when it was zero. There is no need to bound all of J(C)_tors, which of course has unbounded exponent.

## 4. Finite log test with no unbounded order search

Once B0 is known, set N=m B0.

1. Test whether B0 A is principal. Concretely compute L(−B0 A). Since this divisor has degree zero, any nonzero f in this space has div(f)=B0 A. If the space is zero, reject: A is not torsion.
2. If f exists, test the exact identity Nω=df/f in the one-dimensional function-field differential module.
3. If this fails, reject: no larger multiplier works, by the proposition above.
4. If it holds, N and f are a successful logarithmic certificate.

This already produces a bounded Kummer cover, though it need not be minimal or connected before a component is selected. To obtain the minimal exponent, factor the finite integer B0 and compute t=ord[A] by repeatedly removing prime factors from B0 whenever the corresponding smaller multiple of A remains principal. Equivalently test the finitely many positive divisors of B0. Then n=mt, obtain f_min with div(f_min)=tA, and verify nω=df_min/f_min. This constructs the preferred minimal connected cover used in the canonical-cover theorem.

All these tests use exact finite linear algebra and field operations. They require no recognition of numerical periods, no unsolved rank bound, no uniform torsion conjecture, and no potentially nonterminating search for an unknown cover.

A principal-divisor test in a Riemann–Roch space is completely algebraic. The conventional sign is worth recording: L(E)={h: div(h)+E≥0}; therefore to find div(f)=B0 A, use E=−B0 A, not E=B0 A (or invert the function returned from the latter).

## 5. Exactness on a fixed curve is finite linear algebra

Let C be a smooth projective connected curve in characteristic zero and let α be a meromorphic one-form. At a pole P with pole order r≥1, any meromorphic primitive z satisfying dz=α has a pole of order exactly r−1 if r≥2. A meromorphic derivative cannot have a simple pole. Away from poles of α, a primitive has no pole.

Indeed if z=c t^(−h)+higher terms with h≥1 and c≠0, then dz=−hc t^(−h−1)dt+…, and the leading coefficient is nonzero in characteristic zero. Define the effective divisor

E_α = Σ_P max(−ord_P(α)−1,0) P.

Then

α is exact ⇔ there exists z∈L(E_α) with dz=α.

The forward implication follows from the local calculation; the reverse is immediate. Choose a finite basis f1,…,fr of L(E_α) and solve Σ c_j df_j=α over the exact coefficient field. Differentials can be compared after expressing them in one separating differential dx over the function field. This gives a finite linear system. A successful solution is a primitive certificate. A failed rank test is an exact rejection certificate. No integration along cycles is needed.

This applies to each of α=aρ and β=a^(−1)σ on the explicit Kummer normalization. It remains valid at branch points, singularities of a plane presentation, and infinity because valuations and differentials are computed on the normalization. It also handles holomorphic nonzero forms correctly: E=0, L(E) consists of constants, and exactness fails.

## 6. Finite covers cannot repair failed exactness

For any finite separable extension of function fields M/L of degree d, trace commutes with derivation:

Tr_(M/L)(dz)=d Tr_(M/L)(z).

Here the d on the right denotes exterior differentiation; in particular, if α∈Ω_L and α=dz in M, then

α = d(Tr_(M/L)(z)/[M:L])

already in L. Conversely an exact form remains exact after pullback. Thus exactness is unchanged by passing to further finite covers in characteristic zero.

For the preferred cover L=K(a), da/a=ω, one can also descend primitive solvability directly to the two base-field equations

dA+ω A=ρ,    dB−ω B=σ.

For example, if dz=aρ in a finite extension M containing L, then z/a solves d(z/a)+ω(z/a)=ρ. Taking normalized trace from M to K (on z/a, with coefficients of ω,ρ in K) gives a rational solution A∈K. The same argument applies to w/a^(−1)=wa. Conversely A gives z=aA. The differential-equation report supplies direct finite pole bounds for these rational equations; the bounded Riemann–Roch primitive test above is an independent fallback once L is fixed.

## 7. Finite multiplicative monodromy: exact logical boundary

On U=D minus the poles of ω, a local nonzero solution of da/a=ω has monodromy χ:π1(U)→C*. Torsion-logarithmic ω gives finite χ, since a^n=f locally. It also forces all poles of ω to be simple.

Conversely assume all poles are simple and χ has finite image, of exponent n. Then a^n is single-valued on U. Near a pole with local coordinate t, write ω=r dt/t+dh with h holomorphic. Finite local monodromy makes nr an integer, and a^n=c t^(nr) exp(nh) extends meromorphically. Hence a^n is a meromorphic function f on compact D and nω=df/f.

Without the simple-pole condition, the converse is false: ω=d(1/t)=−dt/t² on P¹ has trivial multiplicative monodromy, but exp(1/t) has an essential singularity. It is not algebraic and no nω is a logarithmic differential. Thus any theorem phrased only as “finite monodromy” must either include regular singularity or replace the phrase by the algebraic logarithmic-multiple condition.

## 8. Classical-source audit and limits

### Fully inspected primary mathematical paper

Robert H. Risch, “The solution of the problem of integration in finite terms,” Bulletin of the American Mathematical Society 76 (1970), 605–608, DOI https://doi.org/10.1090/S0002-9904-1970-12454-5 . Full original paper inspected at the academic mirror https://www.cs.ru.nl/~freek/courses/mfocs-2012/risch/S0002-9904-1970-12454-5.pdf .

- Page 606 explicitly requires a transcendence-basis representation to avoid unresolved questions about named transcendental constants.
- Pages 607–608 connect algebraic integration to torsion divisor classes over finitely generated Q-fields and bound this torsion through two good reductions in different residue characteristics.
- This is direct prior art for the effectivity mechanism. The present specialized proof is an application, not a claimed new integration algorithm.

### Checked author exposition of the standard arithmetic ingredients

J.S. Milne, Abelian Varieties, course notes v1.1 (27 July 1998), https://www.jmilne.org/math/CourseNotes/AV110.pdf . Theorem 14.1, printed p.54 (PDF page 56), gives finite-field point counts from Frobenius and the square-root bound on roots. The discussion of Theorem 23.5, printed pp.89–90 (PDF pages 91–92), states the prime-to-residue-characteristic torsion reduction property. These are established ingredients; the self-contained specialization lemma above addresses the finite-type base actually used here.

### Additional checked primary context

Chad Schoen, “Specialization of the torsion subgroup of the Chow group,” arXiv:math/0403550, https://arxiv.org/pdf/math/0403550 . The opening and the proposition on PDF pages 1–3 cover prime-to-characteristic specialization injectivity for divisor classes over finite-type regular integral Z-bases. Its higher-codimension counterexamples do not contradict the divisor-class use here.

### Identified but not used as a verified theorem source

Barry M. Trager, Integration of algebraic functions, MIT Ph.D. thesis (1984), official repository https://dspace.mit.edu/entities/publication/514a5c61-b41a-47da-b846-f5a95ca6c515 . Repository metadata inspected; PDF download through the web reader failed, so no particular theorem in the thesis is relied on here.

The available prior signature report's norm/trace argument for a logarithmic necessary obstruction is sound on the main stratum, but its “directly computable” wording needs the coefficient-model caveat and its proposed denominator-principality step needs the torsion repair above. This report does not independently establish all of that prior report's source geometry, its homogeneous-line classification, or the final fixed-pair realization theorem; those are established in the companion canonical-cover, differential-equation, example and degeneracy reports. No unqualified AIM resolution or novelty assertion follows from the classical integration facts alone.
