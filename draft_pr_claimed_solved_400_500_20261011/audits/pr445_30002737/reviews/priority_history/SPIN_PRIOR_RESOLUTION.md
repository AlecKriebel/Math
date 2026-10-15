# Affirmative antecedent checkpoint: faithful scalar spin weighting

Authored 12 October2026 after the independently sealed initial non-finding. This records a material change of judgment. Completion estimate90% of the bounded history audit; the central antecedent comparison is established from primary text, with the historical numerical bound's stated error acknowledged below.

## Primary evidence

Frank–Mañibo, *Spectral theory of spin substitutions*, arXiv:2108.08642v1, submitted19 August2021 12:13:42UTC; downloaded PDF1279519bytes, SHA-256 `e150c1be6c0883c6bfc2d28f4189e008e91c31737d1cd5defd3b154a735eefc2`. The PDF header is dated20 August2021. Full examples Section5 pp29–33, the character theorems pp13–14, observable diffraction pp22–23, and singularity criterion pp25–29 were read. Pages32–33 were rendered and visually inspected. [Primary preprint](https://arxiv.org/pdf/2108.08642v1).

The official publisher confirms publication online8 August2022, DCDS42(11),5399–5435, DOI10.3934/dcds.2022105, and reproduces Table1 and its stated numerical error bound. Downloaded publisher HTML169501bytes, SHA-256 `2d42c3262ca47f427a79fcdb390b899a446b2d90316bbbb6626e18666cdce520`. Direct journal PDF retrieval returned403/404; no journal PDF body is represented as inspected. [Official publisher](https://www.aimsciences.org/article/doi/10.3934/dcds.2022105).

## Earlier construction and resolution mechanism

Example5.4, p32, has Q=2, D={0,1}, G=C4={1,i,−1,−i}, and spin matrix W=[[1,i],[1,−1]]. Characters are χn(g)=g^n. It states that χ2(W)/sqrt2 is unitary, so the χ2 sector is Lebesgue, whereas the χ1 and χ3 sectors are singular by Proposition4.20. Unlike an equal-weight invisible-colour example, χ1 is **faithful**: kerχ1={1}, and its scalar weights distinguish every spin.

Let ω1 be the paper's scalar weighted comb using χ1. Its actual physical-comb hull is the unit suspension of the spin-factor subshift; no digit data need be retained externally. Theorem4.1 and Example4.4 identify its diffraction with the spectral measure of Fχ1=sum_d fdχ1. Proposition4.20 and Example5.4 give singularity of that measure. Passing from the fundamental torus measure to the periodic real-line diffraction preserves singularity, since a countable union of translates of a torus-null support is real-line null.

The **same scalar comb** determines ω2 by replacing each coefficient z in {1,i,−1,−i} with z². This is a finite-alphabet local factor on the actual comb hull: all coefficients are nonzero, the lattice support is retained, and the scalar coefficient at each lattice point determines its square. Corollary4.5 says the χ2 comb has Lebesgue diffraction. Its diffraction subspace embeds into its own translation representation by the standard Dworkin argument, and this factor representation embeds into that of ω1. Thus the actual ω1 hull has nonzero AC dynamics while ω1's physical diffraction is singular. Equivalently, the square-of-spin observable already lives in the χ1 comb's state space.

The real-line action is essential: either apply the real-line factor/diffraction embedding, or suspend the square observable; the latter has a nonzero sinc-squared Lebesgue density. This is an equivalence check of the paper's existing one-dimensional construction, not a new proof-search construction. Full digit-forgetting conjugacy is unnecessary: the AC square observable depends only on the retained scalar spin.

This supplies an earlier central counterexample to the **original unrestricted translation-bounded conjecture**, which permits complex scalar weights. It does not establish the same additive row-column construction or an earlier unweighted Meyer strengthening. Requiring an earlier unweighted Meyer construction to recognize prior resolution of the original target would wrongly narrow that target.

## Numerical qualification

The χ1 singularity proof uses the cocycle Bχ1(k)=[[1,i],[exp(2πik),−exp(2πik)]], Proposition4.20, and an integrated Frobenius norm upper bound. Table1 reports2f(12)=0.688005 and2f(13)=0.682035, with all numerical errors below10^−3. Even adding10^−3 leaves either value strictly below log2≈0.693147, hence f(N)<log sqrt2 with room. The table and error assertion occur in the preprint and official publisher page. This family has verified the displayed arithmetic and the exact factor mechanism; it has **not independently reproduced a rigorous quadrature certificate** for the historical error assertion. Treat the old source's published validated-numerical assertion as the source of that bound, not as a new audit-produced certificate.

## Scoped finding

Affirmative earlier central-resolution evidence is now found. Proposed recommendation: `already_solved` for the original unrestricted problem, with the numerical-source qualification explicit. Direct same-construction evidence remains unconfirmed. The submitted unweighted Meyer theorem may remain a stronger independently checkable contribution, but novelty of that strengthening is not established by this audit. No mathematical failure of the submitted proof is alleged.
