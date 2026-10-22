# Centered-arc Hilbert series: a category obstruction and a normal-surface converse

Problem 30005416 / OWR-12697689-012. Prose edition dated 11 October 2026.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made. The historical question’s intended category and worldwide current status are not certified.

## 1. Conclusions and scope

Write

\[
 C(q)=\frac{1}{(1-q)^3}\prod_{i\ge2}\frac{1}{(1-q^i)^2}.
\]

The following distinctions are essential.

1. **Unrestricted pointed affine schemes, and even geometrically integral surface germs: the converse is false.** The surface \(xy=0\) at the origin has series \(C\), but is a nonnormal, nonisolated crossing. This particular obstruction is already contained in Bruschek–Mourtada–Schepers [BMS], Proposition 3.9, and is not a new result. More strongly, the pinch point \(x^2-y^2z=0\) has series \(C\) over every characteristic-zero field. It is geometrically integral and its completed local ring is a domain, but it is nonnormal and has a one-dimensional singular locus. A complete proof is given below. Priority for this pinch-point observation has not been established.
2. **Normal finite-type surface germs: there is a positive converse.** Over an algebraically closed characteristic-zero field, a normal surface germ has series \(C\) if and only if it is a rational double point. Over an arbitrary characteristic-zero field, with a rational center, the conclusion is geometric ADE after extension to an algebraic closure, not a particular split equation over the original field. The full argument below uses an explicit infinite graded regular-sequence criterion and Mustaţă’s jet-scheme theorem. This is a restricted theorem, not a silent change to the broad source question; its novelty is uncertain. The independent internal mathematical audit in AUDIT.md accepts the theorem with precisely these restrictions.
3. Neither result distinguishes the Dynkin types. All ADE types already have the same series. The existence of the crossing formula in the foundational paper is strong reason to avoid advertising a new solution to the historic question merely from that example. The author’s intended extra category restriction is not explicitly settled by the short OWR formulation.

No reduction of the arc scheme or alternative grading is used anywhere.

## 2. Source question, history, and current bounded literature status

The official OWR 6/2023 contribution by Mourtada, PDF pages 45–47, printed pages 371–373, sets up a characteristic-zero field, a closed point on an affine singularity, the scheme of arcs centered there, and the grading from reparametrization. Its Theorem 1 gives \(C\) for ADE; Question 2 asks for characterization. The contribution then discusses nonreduced examples. It contains no explicit restriction of Question 2 to normal, reduced, or isolated surfaces.

The retained author manuscript *Jet schemes of rational double point singularities*, dated 31 January 2013, page 13, has the same question as Question 4.5 after Proposition 4.4. Section 2 begins with an algebraically closed field; Section 3 lists the ADE equations over \(\mathbb C\); Section 4.1 resets its Hilbert-series definitions for an affine scheme over a field. This is a historic restatement, not a new 2023 problem. Another author-hosted version, `JetSchemes-ValuationTheory.pdf`, has different numbering: the Hilbert-series question is 4.4. Searches for Question 4.5 therefore also return the separate question about numbers of jet components; that question must not be substituted here.

[BMS], arXiv:1101.4950v2 (7 February 2011), explicitly permits nonreduced and reducible schemes in Section 3. It proves finite-weight stabilization in Proposition 3.2, analytic invariance in Proposition 3.3, the ADE formula in Corollary 3.8, and the crossing formula in Proposition 3.9. Setting its dimension parameter \(d=2\) and component count \(e=2\) gives exactly \(C\). The two formulas appear together on page 9.

A historical catalog record described the problem as open based on a literature check dated 22 August 2026. The 2013 scholarly restatement predates the 2023 question. A catalog status and bounded absence of further located results do not determine mathematical novelty, priority, or the author’s intended category.

A fresh bounded web search found [AGPM], arXiv:2601.12048v1 (17 January 2026), which uses the known \(A_r\) series to prove partition identities and proposes a separate initial-ideal conjecture. Its introductory and theorem passages do not resolve this converse. The 2020 author HDR, mathematical Section 8 passages around printed pages 43–45, discusses the invariant and a forward canonical-hypersurface formula, without supplying the converse in the passages inspected. No exhaustive literature search or complete audit of these papers is claimed.

## 3. Exact ring, grading, and stabilization

Let \(k\) be a field and \(O\) the origin in a closed affine subscheme of \(\mathbb A^e_k\), defined by \(g_1,\ldots,g_r\). Put

\[
 u_a(t)=\sum_{i\ge1}u_{a,i}t^i,\qquad
 S=k[u_{a,i}:1\le a\le e,\ i\ge1],\qquad \deg u_{a,i}=i.
\]

Let \(G_{b,j}\) be the coefficient of \(t^j\) in \(g_b(u(t))\). Then the **scheme-theoretic** centered-arc coordinate ring is

\[
 B=S/(G_{b,j}:b=1,\ldots,r,\ j\ge1).
\]

Each \(G_{b,j}\) is homogeneous of weight \(j\), and all variables have strictly positive weight. The centered \(m\)-jet ring is

\[
 B_m=k[u_{a,i}:1\le i\le m]/(G_{b,j}:1\le j\le m).
\]

For every \(h\le m\), the natural map \((B_m)_h\longrightarrow B_h\) is an isomorphism. Indeed, a monomial of weight \(h\) uses no variable of weight greater than \(h\). In a homogeneous expression for an ideal element of weight \(h\), only equations of weights at most \(h\) and coefficient polynomials of nonnegative weight can occur. Every such variable and equation is already in \(B_m\). This proves stabilization directly, without asserting injectivity of whole truncation-ring maps.

Consequently, if two defining power series agree modulo \((u_1,\ldots,u_e)^{N+1}\), their centered-arc rings have identical graded pieces through weight \(N\). Every monomial in the difference has at least \(N+1\) factors, each contributing positive \(t\)-order, so its coefficient of \(t^j\) vanishes for \(j\le N\).

These statements hold for completed local presentations as well. For any test \(k\)-algebra \(A\), a centered jet sends the maximal ideal into \((t)\subset A[t]/(t^{m+1})\), so it extends uniquely to the completed local ring. A centered arc extends by \(t\)-adic convergence into \(A[[t]]\). Coordinate changes at the formal origin yield weight-preserving changes on coefficient rings: the coefficient of \(t^i\) always has weight \(i\). This is a scheme/functor statement for all \(A\), not only for field-valued arcs.

In particular, an infinite equation cannot remove a lower-weight class. Replacing the coordinate ring by its radical is a different operation and need not preserve the series.

## 4. The crossing: an independent proof of the already-known obstruction

Let \(X=\operatorname{Spec} k[x,y,z]/(xy)\) and \(O=(0,0,0)\). Write

\[
 F_j=\sum_{a=1}^{j-1}x_a y_{j-a},\qquad
 S_m=k[x_i,y_i,z_i:1\le i\le m],\qquad I_m=(F_2,\ldots,F_m).
\]

We prove that this displayed sequence is regular. Dimensions may be computed after extension to an algebraic closure, which does not change heights. For a truncated series, assign order \(m+1\) when it is zero. The geometric vanishing set of \(I_m\) consists exactly of pairs whose orders satisfy

\[
 \operatorname{ord}x(t)+\operatorname{ord}y(t)\ge m+1.
\]

It is therefore the union, for \(1\le a\le m\), of the linear spaces

\[
 L_a=V(x_1,\ldots,x_{a-1},\ y_1,\ldots,y_{m-a}).
\]

Every \(L_a\) has codimension \(m-1\) in \(\mathbb A^{3m}\). Thus \(\operatorname{ht}I_m=m-1\). The same argument gives the expected height for each prefix. Inductively, a preceding regular-sequence quotient of a polynomial ring is Cohen–Macaulay and unmixed; the next \(F_j\) cannot lie in a minimal associated prime, because the prefix height increases by one. Hence it is a nonzerodivisor. This proves regularity without replacing the ideal by its radical in the ring being counted.

The usual exact sequence for multiplication by a homogeneous nonzerodivisor now gives

\[
 H_{B_m}(q)=\frac{\prod_{j=2}^{m}(1-q^j)}{\prod_{i=1}^{m}(1-q^i)^3}.
\]

Weightwise stabilization gives \(H_B=C\). The argument actually works over any field, though the task’s scope is characteristic zero. The surface is reduced, but reducible and nonnormal, with singular line \(x=y=0\), so it is not ADE.

A useful scheme-structure check is the class \(x_1y_2\). It is nonzero in weight 3: the only mixed two-factor relation there is \(x_1y_2+x_2y_1\). Yet

\[
 (x_1y_2)^2=-(x_1y_1)(x_2y_2)=0.
\]

Thus the centered arc ring itself is not reduced. Its reduced ring would instead have the relations \(x_i y_j=0\) for every \(i,j\). If \(H(q)=\prod_{i\ge1}(1-q^i)^{-1}\), its series would be \(2H(q)^2-H(q)\), whose weight-3 coefficient is 17, whereas \([q^3]C=18\). Counting only reduced arcs gives the wrong answer here.

## 5. An integral and formally irreducible counterexample: the pinch point

Let

\[
 P=\operatorname{Spec}k[x,y,z]/(x^2-y^2z),\qquad O=(0,0,0),\quad \operatorname{char}k=0.
\]

For \(n\ge4\), consider

\[
 D_n:\quad x^2-y^2z-z^{n-1}=0.
\]

After renaming coordinates this is precisely the \(D_n\) equation in the 2013 source. After algebraic closure it is an ADE singularity, hence has series \(C\) by [BMS], Corollary 3.8 (or Mourtada’s Proposition 4.4). The coordinate equations are defined over \(k\), and tensoring their finite-dimensional graded pieces with an extension field preserves their dimensions; therefore the same series holds over every characteristic-zero \(k\).

Fix an arbitrary weight bound \(N\). Choose \(n\ge4\) with \(n-1>N\). The equations of \(D_n\) and \(P\) differ by an element of \((x,y,z)^{N+1}\). Section 3 gives

\[
 [q^h]\operatorname{AHP}_{P,O}=[q^h]\operatorname{AHP}_{D_n,O}=[q^h]C
 \quad\text{for every }0\le h\le N.
\]

Since \(N\) was arbitrary, \(\operatorname{AHP}_{P,O}=C\) as formal power series. This uses each finite-weight equality and the positivity of the grading; it does not exchange unjustified analytic limits or discard nilpotents.

The polynomial and completed local quotient rings are domains even after algebraic closure. For the completion, substitute

\[
 y=u,\quad z=v^2,\quad x=uv
\]

in \(k[[u,v]]\). Each residue class has a unique representative
\(a(y,z)+x b(y,z)\). Its image is \(a(u,v^2)+uv b(u,v^2)\). The first summand has even \(v\)-exponents and the second odd \(v\)-exponents, so their sum vanishes only when both \(a,b\) vanish. This gives an injection into a domain; the polynomial argument is identical. The same proof works over any field extension.

Nevertheless, the Jacobian derivatives are \(2x,-2yz,-y^2\), and their vanishing set is the line \(x=y=0\). The germ is not isolated. It is also nonnormal: \(x/y\) in its fraction field is integral, satisfying \(T^2-z=0\), but is not in the local ring. Otherwise \(x h=y g\) with \(h\) a unit at \(O\); reducing modulo \(y\) in \(k[x,z]_{(x,z)}/(x^2)\) would make \(x\) times a unit vanish, which is impossible. The completed-local argument is the same. It follows that \(P\) is not a rational double point.

The arc scheme has retained its nonreduced structure: its weight-2 equation is \(x_1^2=0\), while its weight-1 class \(x_1\) is nonzero.

Thus integrality, geometric integrality, and formal irreducibility alone do not repair the broad characterization. Normality or an appropriate isolatedness hypothesis really matters. This pinch-point argument is an authored deduction from the known \(D_n\) formula; no claim of first discovery is made.

## 6. Infinite regular-sequence criterion

Let \(S=\bigoplus_{h\ge0}S_h\) be a nonnegatively graded \(k\)-algebra with finite-dimensional graded pieces. Let homogeneous elements \(f_j\) have positive degrees \(d_j\) tending to infinity, with only finitely many \(d_j\) below any bound. Set

\[
 R_0=S,\quad R_j=S/(f_1,\ldots,f_j),\quad
 K_j=(0:_{R_{j-1}}f_j),\quad
 P_j=\prod_{i=1}^{j}(1-q^{d_i}).
\]

An element \(f_j=0\) is allowed, with its prescribed degree; then \(K_j=R_{j-1}\). The multiplication exact sequence gives

\[
 H_{R_j}=(1-q^{d_j})H_{R_{j-1}}+q^{d_j}H_{K_j}.
\]

Dividing by the unit \(P_j\) and telescoping gives

\[
 \frac{H_{R_j}}{P_j}=H_S+\sum_{i=1}^{j}\frac{q^{d_i}H_{K_i}}{P_i}.
 \tag{*}
\]

Every coefficient of each summand on the right is nonnegative: \(H_{K_i}\) has nonnegative coefficients, and each inverse factor \((1-q^{d})^{-1}\) does too. The limits and sum are coefficientwise well-defined, because the \(d_i\) tend to infinity and every homogeneous ideal piece stabilizes. For \(B=S/(f_i:i\ge1)\), let \(P=\prod_i(1-q^{d_i})\). Taking limits in (*) proves

\[
 H_B=H_SP\quad\Longleftrightarrow\quad K_i=0\text{ for every }i.
 \tag{**}
\]

Indeed, in the forward direction the sum in (*) must vanish, so each nonnegative summand vanishes. Equivalently, if any defect exists, let \(h\) be the smallest \(d_i+\min\{a:(K_i)_a\ne0\}\). At weight \(h\), the normalized difference has a strictly positive coefficient. Later equations, even when also zero divisors, cannot cancel it. This answers explicitly the possible cancellation objection.

The reverse direction is the usual successive nonzerodivisor formula. The proof does not assume that the quotients are reduced, Noetherian, or domains. It applies to the countable positively weighted polynomial ring used for arcs.

## 7. Normal-surface converse, with all restrictions exposed

**Theorem.** Let \(k\) be algebraically closed of characteristic zero, let \(X\) be a finite-type normal surface in a neighborhood of a closed point \(O\), and use the scheme-theoretic centered-arc ring with natural jet weights. Then

\[
 \operatorname{AHP}_{X,O}(q)=C(q)
 \quad\Longleftrightarrow\quad (X,O)\text{ is a rational double point.}
\]

**Proof.** The reverse implication is [BMS], Corollary 3.8. For the forward implication, the coefficient of \(q\) in the arc series is the embedding dimension at \(O\): in a minimal completed-local presentation all equations have order at least two, so there are no weight-1 relations. Since \([q]C=3\), this embedding dimension is three.

The local ring is excellent, and completion preserves normality. Thus its completion is a two-dimensional complete normal local domain with a minimal Cohen presentation

\[
 \widehat{\mathcal O}_{X,O}=k[[x,y,z]]/(f),\qquad f\in(x,y,z)^2.
\]

To justify that the kernel is principal: it is a height-one prime in the regular local unique-factorization domain \(k[[x,y,z]]\). Hence it is generated by one nonzero element. The hypersurface property descends from completion, so after shrinking around \(O\), \(X\) is locally a complete intersection. Normality in dimension two makes the singular locus zero-dimensional; shrinking further leaves \(O\) as its only possible singular point.

Write \(F_j=[t^j]f(x(t),y(t),z(t))\). These are homogeneous of weight \(j\) in
\(S=k[x_i,y_i,z_i:i\ge1]\). The completion-invariance argument in Section 3 identifies the actual centered-arc ring with \(S/(F_2,F_3,\ldots)\). Also

\[
 H_S=\prod_{i\ge1}(1-q^i)^{-3},\qquad
 C=H_S\prod_{j\ge2}(1-q^j).
\]

Criterion (**) therefore says that every \(F_j\) is a nonzerodivisor modulo its predecessors. In particular \(F_2\ne0\), so \(f\) has multiplicity two. Equivalently, the weight-2 polynomial space has dimension 9 whereas \([q^2]C=8\), forcing a nonzero quadratic equation.

For every \(m\), the regularity of \(F_2,\ldots,F_m\) descends to \(S_m=k[x_i,y_i,z_i:1\le i\le m]\): the infinite polynomial extension is faithfully flat, so a nonzero annihilator in the finite quotient could not disappear. The centered \(m\)-jet scheme thus has dimension

\[
 3m-(m-1)=2m+1.
\]

Now \(\pi_m^{-1}(X_{\mathrm{sing}})=\pi_m^{-1}(O)\) has dimension \(2m+1<2(m+1)\). Mustaţă [M], Proposition 1.4, says for an lci integral variety that this strict inequality is equivalent to irreducibility of \(X_m\). One can also see it directly: every component of the lci jet scheme has dimension at least \(2(m+1)\), while the inverse image of the smooth locus is an irreducible affine bundle of exactly that dimension; no additional component can be supported over \(O\).

All \(X_m\) are therefore irreducible. Mustaţă’s Theorem 0.1 gives rational singularities. The local ring is a hypersurface and therefore Gorenstein. A rational Gorenstein surface singularity is a rational double point (equivalently, a canonical surface singularity, of ADE type). This is the standard characteristic-zero characterization used by Mourtada in Section 3. The embedding dimension three excludes a smooth point. This completes the proof. \(\square\)

**Audit-supported citation supplement.** In the final arXiv revision [M5], Theorem 4.4 on PDF page 19 states the surface-specific equivalence between irreducibility of all jet schemes and rational double points in characteristic zero. Once the preceding argument establishes jet irreducibility, that theorem provides a direct alternative for the last classification step. The independent audit inspected the theorem and its proof; its deeper motivic-integration input was not re-proved. The original v4 citations and their original read scope remain separately recorded.

**General characteristic-zero field.** For a \(k\)-rational center, all finite jet presentations and their homogeneous pieces commute with field extension. The Hilbert series is unchanged by \(k\subset\bar k\). Normality is geometrically preserved over a perfect field; near the lifted rational point one takes the normal irreducible component containing it. Applying the theorem over \(\bar k\) proves the same equivalence with *geometric* ADE. No split normal form, rational exceptional curves over \(k\), or particular Dynkin form over \(k\) is asserted.

**Nonrational closed points.** Under the literal OWR convention \(\dim_k B_h\), the degree-zero piece is \(\kappa(O)\). Since \([q^0]C=1\), equality with \(C\) forces \([\kappa(O):k]=1\); finite type and closedness make this a finite extension. If instead one defines the series over \(\kappa(O)\), as in [BMS] Definition 3.1, the theorem must be restated over that residue field. These conventions should not be silently interchanged.

This theorem addresses a declared normal-surface variant. It does not prove that an arbitrary finite-type pointed scheme with series \(C\) is normal, isolated, or a surface; Sections 4–5 show why normality cannot be inferred in the broad category.

## 8. Computational controls, limitations, and disposition

The proof is symbolic and does not depend on a finite calculation. As a check only, the original computational study used exact rational sparse Gaussian elimination. Its program and raw outputs are not distributed in this prose edition. It enumerates all monomials and all equation multiples in weights 0 through 8. It compares the resulting graded dimensions for \(xy\), the pinch point, \(A_1\), and \(D_4\) against a separately expanded Euler product. The smooth three-space and doubled-plane examples are negative controls. A separate coefficient test checks that adding \(z^{N+1}\) is invisible through weight \(N\), whereas adding \(z^N\) is not. No floating-point arithmetic, probabilistic ranks, source-author code, or theorem inference from the finite bound is used. The stored results and reruns specify every tested case.

The initial control draft was interrupted before its result was relied on because a naive high-power expansion enumerated unnecessary terms. The retained version bounds compositions by total weight. There is no silent omission or successful-result claim for the interrupted draft.

Recommended mathematical disposition: **category clarification with an already-known broad obstruction, a proved pinch-point deduction, and a fully argued normal-surface converse accepted by the independent internal audit**. Do not mark this as a novel unrestricted solution on the strength of the crossing alone. Do not conflate a bibliography search with a prior-proof audit. No worldwide priority determination has been made for the pinch-point observation or the normal-surface derivation.

## References

- [OWR] H. Mourtada, *Commutative Algebra and Integer Partitions*, in *Resolutions in Local Algebra and Singularity Theory*, Oberwolfach Reports 6/2023, printed pp. 371–373. https://ems.press/content/serial-article-files/47000 . DOI 10.4171/OWR/2023/6.
- [M13] H. Mourtada, *Jet schemes of rational double point singularities*, author manuscript dated 31 January 2013, Section 4.1, Proposition 4.4 and Question 4.5, p. 13; later published in *Valuation Theory in Interaction* (2014), pp. 373–388. https://webusers.imj-prg.fr/~hussein.mourtada/PointDouble30Sept.pdf .
- [BMS] C. Bruschek, H. Mourtada, J. Schepers, *Arc Spaces and Rogers-Ramanujan Identities*, arXiv:1101.4950v2, 7 February 2011, especially Section 3, pp. 5–9; published in *The Ramanujan Journal* 30 (2013), pp. 9–38. https://arxiv.org/pdf/1101.4950v2 . DOI 10.1007/s11139-012-9401-y.
- [M] M. Mustaţă, *Jet Schemes of Locally Complete Intersection Canonical Singularities*, arXiv:math/0008002v4, 22 February 2001, Theorem 0.1, p. 1, and Proposition 1.4, pp. 6–7; published in *Inventiones Mathematicae* 145 (2001), pp. 397–424. https://arxiv.org/pdf/math/0008002v4 .
- [M5] M. Mustaţă, *Jet Schemes of Locally Complete Intersection Canonical Singularities*, arXiv:math/0008002v5, 9 April 2001, Theorem 4.4, PDF p. 19, as independently inspected in the audit; deeper motivic-integration input imported. https://arxiv.org/pdf/math/0008002v5 .
- [AGPM] P. Afsharijoo, P. D. González Pérez, H. Mourtada, *Partition identities associated with Ar Surface singularities*, arXiv:2601.12048v1, 17 January 2026, introduction and Section 2, pp. 1–5. https://arxiv.org/pdf/2601.12048v1 .

All source-byte identities, retrieval receipts, and actual read scopes are listed separately in `SOURCES.json`; whole-file retrieval is not a whole-proof audit.
