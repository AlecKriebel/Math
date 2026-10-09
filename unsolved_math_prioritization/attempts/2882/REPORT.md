# KP 4.6 exotic fillings and the turn 3 detector obstruction

## Recovery status and conclusion

Problem reference: 2882 / KP-4.6. Status retained: **UNSOLVED, 3/5 turns**.

This is a reconstruction of the same turn 3 approach, dated 2026-10-09. It is not a fourth approach and is not a byte-for-byte restoration of a missing artifact. The mathematical inputs below have been freshly inspected. The reconstructed input received a fresh independent audit on 2026-10-09, accepted for the partial result below. This proof-only edition updates the review state, makes the elementary Cartan arithmetic explicit, and distinguishes omitted supplementary computation from the written proof. It does not inherit acceptance or a file hash from a missing historical version. See AUDIT.md and PROVENANCE.md for the precise input and editorial boundary. Turns 1 and 2 are outside this report.

The original target is the universal **absolute, orientable exotic-pair** question: for each prescribed closed orientable smooth 3-manifold, which may be disconnected, find two compact connected orientable smooth 4-manifolds that are homeomorphic but not diffeomorphic and whose entire boundaries are the prescribed 3-manifold. The non-diffeomorphism is absolute: a potential diffeomorphism is not required to fix the boundary. Neither infinitely many smooth structures nor simple connectivity is required.

The detector obstruction below uses only a particular class of **connected rational-homology-sphere boundaries**. That restriction belongs to the test family and its proofs, not to the original universal target. This report establishes an obstruction to particular ordinary invariants and a proposed connected-sum proof method. It neither supplies the required exotic pair for every boundary nor identifies a 3-manifold with no exotic filling.

For the explicit boundary

\[
Y=P\#9(-O),
\]

where \(P=\partial(-E_8)\) and \(O=\partial(-E_7)\), the recovered conclusion is:

1. Every smooth oriented filling of either \(Y\) or \(-Y\) is indefinite, without a hypothesis on its first Betti number or fundamental group.
2. \(Y\) is an **integral** L-space. Any smooth oriented closed 4-manifold obtained by gluing any filling and any cap along \(Y\), with any orientation-compatible boundary identification, has zero ordinary integral Ozsváth–Szabó invariant in every individual Spin\(^c\) structure, with all ordinary \(U\)- and \(H_1/\mathrm{torsion}\)-insertions.
3. If \(W\) fills \(Y\) and \(E\) is a smooth closed oriented 4-manifold with \(b_2^+(E)>0\), then the full integral mixed map of \((W\#E)\setminus B^4:S^3\to Y\) is zero. Every capped transplant \((W\#E)\cup_f C\) also has zero ordinary Seiberg–Witten invariant in every Spin\(^c\) structure and with all ordinary insertions.

The zero conclusions do not imply that two transplants are diffeomorphic. They show that these ordinary detectors cannot establish their exoticness in this example.

## 1 Conventions and exact source inputs

For the detector propositions in this report, a filling means a smooth compact connected oriented 4-manifold whose entire boundary is the specified connected rational homology sphere. This connected-boundary convention is local to these propositions; the original target permits a disconnected prescribed boundary. A cap \(C\) for a filling of \(Y\) has \(\partial C=-Y\). A gluing map \(f:\partial W\to\partial C\) reverses the induced boundary orientations. The resulting closed manifold is given the compatible orientation. Closed extra components are not included in the words filling or cap.

For a compact 4-manifold, \(b_2^+\) and \(b_2^-\) refer to the positive and negative indices of its real intersection pairing. All Heegaard Floer groups and maps used in the assertions are ordinary untwisted groups over \(\mathbb Z\), unless explicitly stated otherwise. Choices of homology orientation and overall signs cannot affect a zero conclusion. An ordinary insertion is an element of

\[
\mathbb Z[U]\otimes\Lambda^*(H_1(-;\mathbb Z)/\mathrm{torsion}).
\]

The source inputs are these, with exact locations and freshly retrieved PDF metadata in the accompanying source records:

- **DLM:** Aliakbar Daemi, Tye Lidman and Mike Miller Eismeier, *3-Manifolds without any embedding in symplectic 4-manifolds*, Geometry & Topology 28 (2024), 3357–3372. Theorem 2, printed page 3357, gives the no-definite-filling family \(mP\#k(-O)\), \(m\geq1\), \(k>8m\). The theorem imposes no \(b_1\) or \(\pi_1\) restriction on fillings. Its introduction fixes the plumbing orientations. The proof of Proposition 2.1 explicitly removes rational first homology by surgery; that is a step of the proof, not an extra hypothesis. [Publisher PDF](https://msp.org/gt/2024/28-7/gt-v28-n7-p09-s.pdf)
- **OS L-spaces:** Peter Ozsváth and Zoltán Szabó, *On knot Floer homology and lens space surgeries*, arXiv:math/0303017v2. Definition 1.1, page 2, uses free abelian \(\widehat{HF}\); Section 2, page 9, supplies orientation and connected-sum closure and the reduced-group characterization; Proposition 2.3, page 11, includes elliptic 3-manifolds. [Versioned PDF](https://arxiv.org/pdf/math/0303017v2)
- **OS four-manifolds:** Ozsváth and Szabó, *Holomorphic triangles and invariants for smooth four-manifolds*, arXiv:math/0110169v2. Lemma 8.2 and Definition 8.3, page 66; Theorem 8.5, page 67; Section 9, page 70; and Theorem 10.1, page 71, give the infinity-map vanishing, mixed-map construction, cut independence and closed invariant. The mixed-map domain explicitly includes the exterior algebra of ordinary first-homology insertions. [Versioned PDF](https://arxiv.org/pdf/math/0110169v2)
- **Mukherjee:** Anubhav Mukherjee, *A note on embeddings of 3-manifolds in symplectic 4-manifolds*, Algebraic & Geometric Topology 25 (2025), 3251–3270. Lemmas 2.6 and 2.9, and Remarks 2.7–2.8, printed page 3259, independently restate the admissible-cut mechanism. This is corroboration, not the justification for changing coefficients to \(\mathbb Z\). [Publisher PDF](https://msp.org/agt/2025/25-6/agt-v25-n6-p03-p.pdf)
- **KM:** Peter Kronheimer and Tomasz Mrowka, *Monopoles and Three-Manifolds*, Cambridge University Press, 2007. Proposition 3.5.2 and Theorem 3.5.3, page 64; Proposition 9.7.1, page 152; Proposition 23.2.2, page 457; Definitions 27.1.6–27.1.7, page 555; Sections 27.2–27.3, pages 556–565; and Proposition 27.4.1, page 566, are used for the ordinary monopole invariant with insertions. [University-hosted book PDF](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/kronmrowka.pdf)
- **EMM:** John B. Etnyre, Hyunki Min and Anubhav Mukherjee, *On 3-manifolds that are boundaries of exotic 4-manifolds*, arXiv:1901.07964v3. Remark 1.8, page 3, already discusses connected-sum transplantation and its stabilization and ordinary-invariant difficulties. The construction idea and general warning are therefore credited to EMM, not presented here as new. [Versioned PDF](https://arxiv.org/pdf/1901.07964v3)

## 2 A nonvacuous family of obstructing boundaries

Write

\[
Y_{m,k}=\mathbin{\#}^{m}P\ \#\ \mathbin{\#}^{k}(-O),
\qquad m\geq1,\quad k>8m.
\]

Let \(V_8\) and \(V_7\) be the negative-definite simply connected plumbing 4-manifolds with forms \(-E_8\) and \(-E_7\), with boundaries \(P\) and \(O\), respectively. Their boundary-connected sum

\[
W_{m,k}=(\mathbin{\natural}^{m}V_8)\natural
(\mathbin{\natural}^{k}(-V_7))
\]

is a smooth filling of \(Y_{m,k}\), with

\[
Q_{W_{m,k}}=(-E_8)^{\oplus m}\oplus E_7^{\oplus k},
\qquad (b_2^+,b_2^-)=(7k,8m).
\]

Thus no assertion concerns an empty collection of fillings. The standard Cartan matrices have determinants \(\det E_8=1\) and \(\det E_7=2\). The plumbing homology sequence identifies boundary first homology with the cokernel of the intersection matrix: it is trivial for \(P\) and \(\mathbb Z/2\) for \(O\). Connected-sum homology gives

\[
H_1(Y_{m,k};\mathbb Z)\cong(\mathbb Z/2)^k.
\]

In particular, the smallest convenient member \(Y=Y_{1,9}\) has a filling with form \(-E_8\oplus9E_7\), positive index 63, negative index 8, rank 71, and boundary first homology \((\mathbb Z/2)^9\). For a written verification of the Cartan arithmetic, let \(A_\ell\) be the chain matrix with diagonal entries 2 and adjacent entries \(-1\). Its leading determinants satisfy \(D_0=1\), \(D_1=2\), and \(D_\ell=2D_{\ell-1}-D_{\ell-2}\), so \(D_\ell=\ell+1\). Thus \(A_\ell\) is positive definite, and its inverse entry at an endpoint is \(\ell/(\ell+1)\), by the cofactor formula. The \(E_n\) tree, for \(n=7,8\), has three arms of lengths \(1,2,n-4\) attached to its central vertex. Eliminating the positive-definite arm blocks gives the central Schur complement

\[
2-\frac12-\frac23-\frac{n-4}{n-3}
=\frac{9-n}{6(n-3)}>0.
\]

Consequently \(E_n\) is positive definite and

\[
\det E_n=2\cdot3\cdot(n-3)\frac{9-n}{6(n-3)}=9-n.
\]

This proves the determinants 2 and 1, and hence the asserted boundary cokernels (a group of order 2 is cyclic). The indices of the displayed direct sum and its absolute determinant \(2^9=512\) now follow directly. Supplementary exact-arithmetic programs were run during reconstruction and the independent audit, as recorded historically in AUDIT.md and VERIFICATION.md. They are not distributed in this edition, are not needed for this derivation, and do not compute Floer groups or prove DLM's theorem.

## 3 Why every filling and every cap is indefinite

**Proposition 1.** If \(A\) fills \(Y_{m,k}\) or \(-Y_{m,k}\), then \(b_2^+(A)\geq1\) and \(b_2^-(A)\geq1\).

**Proof.** These boundaries are rational homology spheres. The long exact sequence of \((A,\partial A)\), over \(\mathbb R\), contains

\[
0=H_2(\partial A;\mathbb R)\longrightarrow H_2(A;\mathbb R)
\longrightarrow H_2(A,\partial A;\mathbb R)
\longrightarrow H_1(\partial A;\mathbb R)=0.
\]

The middle map is an isomorphism. Poincaré–Lefschetz duality therefore makes the intersection form on \(H_2(A;\mathbb R)\) nondegenerate. No assumption on \(H_1(A)\) was used.

If the rank is positive and either index vanishes, the form is definite, contradicting DLM Theorem 2. For boundary \(-Y_{m,k}\), reverse \(A\)'s orientation to apply that theorem. To avoid any convention about whether the rank-zero form counts as definite, suppose separately that \(b_2(A)=0\). Then \(A\#\mathbb{CP}^2\) has the same boundary and a nonzero positive-definite form, again impossible. Consequently both indices are positive. \(\square\)

**Proposition 2.** For fillings \(A\) of \(Y_{m,k}\), caps \(C\) with boundary \(-Y_{m,k}\), and every allowed gluing \(f\),

\[
Q_{A\cup_f C}\cong Q_A\oplus Q_C\quad\text{over }\mathbb R,
\qquad b_2^\pm(A\cup_f C)=b_2^\pm(A)+b_2^\pm(C)\geq2.
\]

**Proof.** Real Mayer–Vietoris has zero terms \(H_2(Y_{m,k};\mathbb R)\) and \(H_1(Y_{m,k};\mathbb R)\), so the inclusion maps induce an isomorphism on second homology from the direct sum of the two pieces. Classes can be represented away from the gluing collar; representatives from different pieces have intersection zero. Proposition 1 gives the inequalities. The reasoning is unaffected by the boundary identification. \(\square\)

An added cap cannot remove the positive index of a filling. In particular, changing the cap cannot turn a positive-positive connected-sum decomposition into a definite one.

## 4 The integral L-space input and the Spin c issue

The manifolds \(P\) and \(O\) are elliptic. Apply OS L-spaces Proposition 2.3, orientation invariance, and connected-sum closure. Definition 1.1 is explicitly integral and torsion-free. Hence, for each \(Y_{m,k}\),

\[
\widehat{HF}(Y_{m,k};\mathbb Z)\cong\mathbb Z^{2^k},
\qquad HF^+_{\mathrm{red}}(Y_{m,k};\mathbb Z)=0.
\]

The reduced minus group also vanishes, by its canonical identification with the reduced plus group. The same conclusions hold after orientation reversal and hold in each Spin\(^c\) summand. This does **not** infer integral vanishing from a computation over \(\mathbb F_2\).

A rational homology sphere need not have zero integral first homology: our example has substantial 2-torsion. What is needed for Spin\(^c\) gluing is instead

\[
H^1(Y_{m,k};\mathbb Z)
\cong\operatorname{Hom}(H_1(Y_{m,k};\mathbb Z),\mathbb Z)=0.
\]

In integral cohomological Mayer–Vietoris, this makes

\[
H^2(A\cup_f C;\mathbb Z)\longrightarrow
H^2(A;\mathbb Z)\oplus H^2(C;\mathbb Z)
\]

injective. Since Spin\(^c\) structures form a torsor for \(H^2\), two global Spin\(^c\) structures with the same restrictions coincide. We use uniqueness for restrictions of an already existing global structure, not an assertion that every arbitrary pair of boundary data glues. Thus no torsion ambiguity allows cancellation among distinct extensions to masquerade as individual vanishing.

## 5 Direct connected sum transplantation has zero mixed map

**Proposition 3.** Let \(W\) fill \(Y_{m,k}\), and let \(E\) be any smooth closed connected oriented 4-manifold with \(b_2^+(E)>0\). Set \(T=W\#E\). Then, for every Spin\(^c\) structure \(\mathfrak s\),

\[
F^{\mathrm{mix}}_{T\setminus B^4,\mathfrak s}:
HF^-(S^3;\mathbb Z)\otimes
\Lambda^*(H_1(T;\mathbb Z)/\mathrm{torsion})
\longrightarrow HF^+(Y_{m,k},\mathfrak s|_Y;\mathbb Z)
\]

is identically zero.

**Proof.** Place the removed ball in the \(E\) region. The internal connected-sum sphere decomposes the cobordism into \(E\) minus two balls, from \(S^3\) to \(S^3\), followed by \(W\) minus a ball, from \(S^3\) to \(Y_{m,k}\). Both pieces have positive \(b_2^+\), the second by Proposition 1. Their common \(S^3\) has \(H^1(S^3;\mathbb Z)=0\), so it is an admissible cut, and the total positive index is at least two.

The OS mixed construction factors through \(HF_{\mathrm{red}}(S^3;\mathbb Z)=0\). Cut independence identifies that zero construction with the mixed map of the whole cobordism. Its stated domain includes all ordinary exterior insertions; \(U\)-multiples are already included in \(HF^-\). One can also distribute every exterior monomial between the two pieces using the integral first-homology direct sum at an \(S^3\) connected sum. Hence the claim is about the full mixed map, not one test vector or a Spin\(^c\)-sum. \(\square\)

The same internal-sphere argument applies to any \(W\) with positive \(b_2^+\), even without an L-space boundary. Here Proposition 1 makes this hypothesis unavoidable for every possible initial filling.

## 6 Every closure along this boundary has zero closed OS invariant

**Proposition 4.** Let \(A,C,f\) be as in Proposition 2 and \(X=A\cup_f C\). Then, for each \(\mathfrak s\in\operatorname{Spin}^c(X)\),

\[
\Phi_{X,\mathfrak s}(a)=0
\quad\text{for every }a\in
\mathbb Z[U]\otimes\Lambda^*(H_1(X;\mathbb Z)/\mathrm{torsion}).
\]

**Proof.** Remove one ball from each piece. The intervening \(Y_{m,k}\) is a positive-positive cut by Proposition 1, and is admissible because its integral \(H^1\) is zero. Its integral reduced Floer group is zero by Section 4. The punctured mixed map therefore vanishes, and the closed invariant is the prescribed coefficient of that zero map. Equivalently, apply OS Theorem 10.1 directly. The conclusion is for an individual global Spin\(^c\) structure; Section 4 also explicitly explains why an extension sum is not an issue.

For insertion bookkeeping, integral Mayer–Vietoris shows that \(H_1(A)\oplus H_1(C)\to H_1(X)\) is surjective: the next \(H_0\) map is injective because the three spaces are connected. Its kernel comes from the finite group \(H_1(Y)\), hence is torsion. It induces an isomorphism on the quotients by torsion. Ordinary exterior monomials thus come from sums of products of classes on the two pieces. The mixed construction with these classes still factors through the zero reduced group. \(\square\)

This assertion is stronger than Proposition 3 in a different direction: \(A\) need not be a connected-sum transplant. It covers every filling, every cap and every gluing along this boundary, for the stated closed OS invariant.

## 7 Seiberg Witten vanishing for capped transplants

The next assertion is deliberately restricted to **capped connected-sum transplants**. No corresponding all-fillings Seiberg–Witten statement is inferred here from the Heegaard Floer calculation.

**Proposition 5.** With \(W,E\) as in Proposition 3, let \(C\) be any cap and \(f\) any allowed gluing. For

\[
X=(W\#E)\cup_f C\cong E\#N,
\qquad N=W\cup_f C,
\]

the ordinary Seiberg–Witten invariant is zero in every individual Spin\(^c\) structure, for every ordinary \(U\)- and \(H_1/\mathrm{torsion}\)-insertion, without imposing \(b_1(W)=b_1(C)=b_1(E)=0\).

**Proof.** Choose the connected-sum ball in the interior of \(W\), away from its boundary, to obtain the displayed diffeomorphism. Proposition 2 gives \(b_2^+(N)\geq2\), while \(b_2^+(E)\geq1\).

Here is a source-level proof that retains insertions and individual Spin\(^c\) structures. Denote the ordinary monopole Floer variants by \(\overline{HM},\widehat{HM},\check{HM}\), and the mixed map by \(\overrightarrow{HM}\). KM Proposition 3.5.2 makes the bar map zero for a positive-index cobordism. For a cobordism from \(S^3\) to \(S^3\), the exact triangle then makes the check map zero, since \(i_*:\overline{HM}(S^3)\to\check{HM}(S^3)\) is surjective. The analogous hat map also vanishes. This applies to the twice-punctured \(E\).

Factor the twice-punctured \(X\) with the twice-punctured \(N\) first and the twice-punctured \(E\) second. Since the former has positive index at least two, KM Theorem 3.5.3 applies in its stated invariant range and gives

\[
\overrightarrow{HM}(X^{\circ\circ})
=\check{HM}(E^{\circ\circ})\circ
\overrightarrow{HM}(N^{\circ\circ})=0.
\]

This use of \(b_2^+(N)\geq2\) avoids needing to call a stand-alone mixed map for a positive-index-one piece canonical.

We must not stop with a sum of Spin\(^c\) invariants. Fix \(\mathfrak s\) on \(X\), and let \(\mathfrak s_E,\mathfrak s_N\) be its restrictions. On the disjoint union of configuration spaces \(\mathcal B^\sigma(E^{\circ\circ})\), use the degree-zero class \(e_{\mathfrak s_E}\) that is 1 on that Spin\(^c\) component and 0 on all others; similarly use \(e_{\mathfrak s_N}\). These are ordinary cohomology classes, not exponential weights depending only on real first Chern classes. Their pullback product is exactly \(e_{\mathfrak s}\), because Spin\(^c\) gluing across \(S^3\) is unique. Torsion-distinct Spin\(^c\) structures are consequently separated as well.

KM Proposition 23.2.2 formulates composition for arbitrary cohomology classes on these disjoint unions. Sections 27.2–27.3 construct the mixed map and its corresponding composition with such classes. The positive-index bar-map vanishing still applies after the selectors are inserted: the underlying reducible moduli spaces are empty, by Proposition 27.2.4, before any cohomological evaluation is taken. Thus the check map of the selected \(E\) component is zero by the same exact-triangle argument.

Finally, \(H_1(X;\mathbb Z)\cong H_1(E;\mathbb Z)\oplus H_1(N;\mathbb Z)\). Any ordinary insertion is a sum of products of insertions pulled back from the two pieces; place a power of \(U\) on either piece. Apply the class-decorated composition to each such product together with the two selectors. Every term is zero. Definitions 27.1.6–27.1.7 and Proposition 27.4.1 identify its evaluation with the ordinary Seiberg–Witten invariant in the chosen \(\mathfrak s\). This proves the claimed individual, all-insertion vanishing and uses no first-Betti-number restriction. \(\square\)

## 8 Ordinary plus and minus maps are a separate statement

For an ordinary positive-index cobordism \(V:L_0\to L_1\) between integral L-spaces, the undecorated \(F^\infty_{V,\mathfrak s}\) is zero. Naturality of the exact sequence gives:

- \(F^+_{V,\mathfrak s}=0\), because \(HF^\infty(L_0)\to HF^+(L_0)\) is surjective;
- \(F^-_{V,\mathfrak s}=0\), because \(HF^-(L_1)\to HF^\infty(L_1)\) is injective.

These are consequences for the ordinary plus/minus cobordism maps. They are not a definition of the mixed map. In particular, this reasoning is not a claim about \(\widehat{HF}\) cobordism maps, twisted or local-coefficient invariants, stable cohomotopy, families invariants, or other refined detectors. None is identified with the maps that were proved zero.

## 9 Exact surviving gap

The connected-sum idea is to choose a connected filling \(W\) of a prescribed boundary and closed exotic donors \(E_0,E_1\), then try to prove that \(W\#E_0\) and \(W\#E_1\) form an absolutely exotic pair. EMM Remark 1.8 considers the stronger aim of an infinite family and already points out both stabilization and ordinary-invariant obstacles. The present deduction makes the ordinary-detector problem unavoidable for the above explicit connected boundary family and supplies an all-caps, all-gluings closed OS statement in that family.

What is missing for the original target is an exotic pair of compact connected orientable fillings, with the entire prescribed boundary, for every closed orientable 3-manifold, including disconnected ones. A transplantation proof would have to specify the donors and resulting homeomorphisms, and prove that at least two resulting fillings are non-diffeomorphic even when boundary identifications are allowed to vary. An infinite family would be stronger than required. Neither an exotic pair nor that stronger conclusion follows from the equal zero invariants here. For a different construction, this report supplies neither a candidate pair nor its distinguishing argument.

The family \(Y_{m,k}\) is not asserted to lack exotic fillings. No two candidate transplants are proved diffeomorphic, and no stable or refined invariant is ruled out. There is no claimed new theorem on the current literature-wide status beyond the explicit source inputs. The original problem therefore remains **UNSOLVED at 3/5**, with the reconstructed third-turn obstruction independently audited as a partial result and presented here in a proof-only editorial edition.
