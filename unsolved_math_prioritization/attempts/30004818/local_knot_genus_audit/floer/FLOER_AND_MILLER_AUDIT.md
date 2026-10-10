# Independent audit: the local Floer bound and Miller's torsion family

## Verdict

**Accept the mathematical claims audited here.** The argument proves

\[
|\tau(K)|\le g_{M\times I}(K)\le g_4(K)
\]

for every classical knot placed in a ball in a closed connected oriented smooth three-manifold \(M\). No rational-homology-sphere hypothesis, restriction on the surface's fundamental-group image, or vanishing of its capped absolute homology class is needed. Consequently \(|\tau(K)|=g_4(K)\) implies equality of the two genera for every such \(M\).

Miller's cited family really has smooth concordance order exactly two and arbitrarily large **topological**, hence smooth, four-genus. Its stable smooth four-genus and classical \(\tau\) are zero.

No mathematical correction to these claims is required. Three useful clarifications are to give an explicit reference for general Floer nonvanishing, specify coefficients/basepoint conventions, and spell out the orientation convention when reversing the surface. The discussion below provides precise language.

This audit covers the Floer-theoretic and Miller portions of Approach 5. It does not independently certify the preceding group-norm construction or the other four approaches.

## 1. Relative adjunction: exact theorem and hypotheses

The inspected Hedden–Raoux source is *Knot Floer homology and relative adjunction inequalities*, arXiv:2009.05462v2 (6 August 2021). Theorem 1 is on manuscript page 2; the fully normalized statement is **Theorem 4.1, page 24**, with the independence-of-normalization calculation on page 26.

Take a compact oriented smooth cobordism \(W:Y_1\to Y_2\), so \(\partial W=-Y_1\sqcup Y_2\). Let the boundary knots be rationally null-homologous, let \(\mathfrak t\in\operatorname{Spin}^c(W)\), and suppose the associated hat map sends a class \(\alpha\) to \(\beta\ne0\). For an oriented properly embedded surface \(\Sigma\) with boundary \(-K_1\sqcup K_2\), Theorem 4.1 gives

\[
\langle c_1(\mathfrak t),A\rangle+A^2+
2\bigl(\tau_\beta(Y_2,[S_2],K_2)-\tau_\alpha(Y_1,[S_1],K_1)\bigr)
\le 2g(\Sigma),
\]

where the chosen rational Seifert surfaces fix the lift

\[
A=[q_1^{-1}S_1+\Sigma-q_2^{-1}S_2]\in H_2(W;\mathbb Q).
\]

For the local knots in the manuscript, \(q_1=q_2=1\), and the class is integral. No definiteness condition on \(W\), no positive-genus condition on \(\Sigma\), and no condition \(A=0\) appear. The theorem concerns the genus of the original boundary-bearing surface, not the genus after attaching its Seifert caps. Thus the constants and signs used in Approach 5 are correct.

A useful explicit cap convention for the application \(U\to K\) is

\[
A=[D_U+\Sigma-S_K],
\]

where \(D_U\) and \(S_K\) are the local disk and local Seifert surface used to normalize the two filtrations.

The theorem is directly applicable to a genus-zero surface as well. Its proof on page 24 also permits disconnected surfaces, interpreting genus as the sum, though the application here can use a connected surface throughout.

## 2. Coefficients, nonvanishing, and conjugation

Use \(\mathbb F_2\) coefficients, as in Hedden–Raoux, Section 2.1, page 6. This avoids integer orientation-system choices and makes all stated tensor-product formulas literal vector-space formulas.

An explicit reference for the manuscript's general nonvanishing input is:

- A. Alishahi and R. Lipshitz, *Bordered Floer homology and incompressible surfaces*, Ann. Inst. Fourier **69** (2019), 1525–1573, **Theorem 1.2, page 1526**; proof **pages 1542–1543**. It states that \(\widehat{HF}(Y)\ne0\) for every closed oriented three-manifold. The proof produces nonzero rational rank; the universal-coefficient theorem therefore supplies nonvanishing over \(\mathbb F_2\). The nonvanishing of the standard \(S^1\times S^2\) summand and the connected-sum formula handle those prime summands.

This supplies some \(\mathfrak s\) and \(0\ne\alpha\in\widehat{HF}(M,\mathfrak s;\mathbb F_2)\). It does **not** assert that every Spin\(^c\) summand is nonzero. Approach 5 only needs one such summand and does not assume more.

Ozsváth–Szabó, *Holomorphic disks and three-manifold invariants: properties and applications*, **Theorem 2.4, published page 1167**, states the isomorphism

\[
\widehat{HF}(M,\mathfrak s)\cong\widehat{HF}(M,\overline{\mathfrak s}).
\]

Its proof keeps the orientation of \(M\) fixed. Thus a nonzero conjugate class exists in the **same oriented** manifold, and \(c_1(\overline{\mathfrak s})=-c_1(\mathfrak s)\). No orientation-reversal duality is being substituted for conjugation. The two product Spin\(^c\) structures are the extensions of \(\mathfrak s\) and \(\overline{\mathfrak s}\) under the product identification.

No assertion that conjugation preserves a general knot's Alexander filtration is needed. The local calculation below computes the needed value separately in both summands.

## 3. The local filtered-complex calculation

Hedden–Raoux **Proposition 2.6, page 9**, gives additivity of \(\tau\) for any pair of nonzero homology classes under the hat connected-sum isomorphism. **Remark 2.7, pages 9–10**, specifies the boundary-connected-sum Seifert surface convention in the null-homologous case.

Choose the local unknot diagram by placing its two basepoints in the same complementary region of an ordinary pointed diagram for \(M\). The local disk normalization puts every generator in Alexander grading zero. Hence the entire hat complex of \((M,U)\) has filtration zero, and

\[
\tau_\alpha(M,[D_U],U)=0
\]

for every nonzero class in any supporting Spin\(^c\) summand.

The local knot is represented as \((M,U)\#(S^3,K)\). Since \(\widehat{HF}(S^3;\mathbb F_2)\) is one-dimensional, every class in the connected sum corresponds to \(\alpha\otimes\theta\), with \(\theta\) its unique nonzero generator. Proposition 2.6 and the local Seifert surface give

\[
\tau_{\alpha\otimes\theta}(M,K)=0+\tau_\theta(S^3,K)=\tau(K).
\]

This calculation proves the required statement for **all nonzero classes**, not merely selected generators or classes in the image of a tower. Changing the ambient Spin\(^c\) structure to its conjugate does not change the classical knot factor or the disk normalization.

## 4. Product maps and the harmless basepoint convention

Hedden–Raoux explicitly suppresses basepoints and paths, while noting their relevance: **Section 2, page 6; Remark 3.3, page 13**. The opening of **Section 5.1, page 27**, states that the product cobordism induces the identity.

The manuscript's identity statement is correct with the standard product basepoint path and the standard identifications of the two ends. It should not be interpreted as claiming identity for every nontrivial point-pushing path in the product. A surface-selected path can instead induce a basepoint-moving isomorphism. This does not endanger the proof: one may set \(\beta=F_{W,\mathfrak t}(\alpha)\ne0\), and the local calculation gives \(\tau_\beta(M,K)=\tau(K)\) just as it does for \(\alpha\). The same holds in the conjugate structure.

Accordingly, either of these conventions is sufficient:

1. Explicitly use the standard product path when invoking the identity; or
2. Use the appropriate product/basepoint-moving isomorphism and refrain from requiring \(\beta=\alpha\).

No nontriviality assumption on the fundamental-group image of the surface is introduced by this observation.

## 5. Cap class, Chern pairing, and reversed orientation

Puncturing the bounding surface and extending the new trivial boundary to the other product end gives a surface \(\Sigma:U\to K\) of the same genus \(g\). Its chosen cap class \(A\) need not vanish.

The absolute intersection form of \(M\times I\) is zero: every absolute two-dimensional class comes from a slice \(M\times\{t\}\), and its representatives can be displaced in the interval direction. Equivalently, the boundary-to-absolute map on \(H_2\) is surjective, so the absolute-to-relative map is zero. In particular \(A^2=0\), even when \(A\ne0\).

Put \(c=\langle c_1(\mathfrak s),A\rangle\). The two applications of Theorem 4.1 give

\[
c+2\tau(K)\le2g,\qquad -c+2\tau(K)\le2g.
\]

Adding gives \(\tau(K)\le g\), with no unproved assumption about \(c\).

For full orientation precision, retain the usual ambient orientation of \(M\times I\), define \(R(x,t)=(x,1-t)\), and use the oriented surface

\[
\Sigma^{\mathrm{rev}}=-R(\Sigma).
\]

Its boundary is \(-K\) at the incoming end and \(U\) at the outgoing end, so it is the required cobordism \(K\to U\) in the same oriented product. With reversed local caps its class is \(A^{\mathrm{rev}}=-R_*A\). The two inequalities now have \(\tau\)-difference \(-\tau(K)\); conjugation cancels the Chern pairing again and gives \(-\tau(K)\le g\). Therefore \(|\tau(K)|\le g\).

This explicitly justifies the manuscript's phrase “reverse the surface cobordism.” Merely changing which end is called incoming without managing orientations would be ambiguous, but the required surface exists by the construction above.

The upper bound follows by putting a classical four-ball surface in the local ball product. Together these prove the claimed inequality and its equality cases, including sums of equally handed trefoils.

## 6. Miller's family

The inspected manuscript is A. N. Miller, *Amphichiral knots with large 4-genus*, arXiv:2011.09346v1 (18 November 2020). On **page 1, Theorem 1.1** gives, for every \(g>0\), a strongly negative amphichiral knot with topological four-genus strictly larger than \(g\). **Corollary 1.2, on the same page**, explicitly records two-torsion knots of arbitrarily large four-genus. The paragraph between them explains the negative-amphichiral/order-two consequence. **Proposition 2.7, page 6**, strengthens this to infinite families generating \((\mathbb Z_2)^\infty\).

The publisher record confirms publication in *Bulletin of the London Mathematical Society* **54** (2022), 624–634, DOI 10.1112/blms.12588, and its abstract explicitly states the same topological-genus obstruction and smooth two-torsion conclusion.

Because these knots are not even topologically slice, they are not smoothly slice. Their smooth concordance order is therefore **exactly** two, not merely a divisor of two. Their smooth genus satisfies

\[
g_4^{\mathrm{smooth}}(K)\ge g_4^{\mathrm{top}}(K)>g.
\]

For an order-two knot, even multiples are smoothly slice and odd multiples are concordant to \(K\). Hence \(g_{4,\mathrm{st}}(K)=0\). Additivity and integer-valuedness give \(2\tau(K)=0\), hence \(\tau(K)=0\). These implications are valid and show why real-valued additive concordance invariants cannot recover ordinary four-genus on this family.

Neither Miller's theorem nor these algebraic consequences supply a genus-saving surface in an oriented product. Approach 5 correctly labels the family as a testing family rather than a counterexample.

## Sources and inspection record

- Hedden–Raoux, inspected local PDF/text and visually inspected Theorem 4.1 on manuscript page 24: https://arxiv.org/abs/2009.05462 ; https://doi.org/10.1007/s00029-022-00810-1 .
- Ozsváth–Szabó, inspected local PDF/text and visually inspected conjugation Theorem 2.4 on published page 1167: https://annals.math.princeton.edu/wp-content/uploads/annals-v159-n3-p04.pdf .
- Alishahi–Lipshitz, downloaded and inspected the publisher-hosted PDF/text, including Theorem 1.2 and its proof: https://www.numdam.org/item/10.5802/aif.3276.pdf ; https://doi.org/10.5802/aif.3276 .
- Miller, inspected local manuscript PDF/text and checked the publisher record: https://arxiv.org/abs/2011.09346 ; https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.12588 .

All source page/theorem locations above distinguish manuscript pagination from journal pagination. The original Approach 5 file and its original sources were not edited.
