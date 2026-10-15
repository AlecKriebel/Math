# Question 8.2: the literal additive-distortion condition is affirmative

**Status:** Credited known-result consequence, with a self-contained verification. Independent review pending. No new-discovery or human-peer-review claim.

## 1. Exact question and attribution

Calegari's *Problems in foliations and laminations of 3-manifolds* (2002), Question 8.2, p. 16, asks whether the leaf-line action can be topologically conjugated so that, for each group element (g), there is a finite constant (C(g)>0) satisfying
\[
 \bigl|\,|g(u)-g(v)|-|u-v|\,\bigr|\le C(g)
 \qquad(u,v\in\mathbb R).                                      \tag{1}
\]
Here and below (g) in this display denotes the action **after one common conjugacy**. The constant may depend on (g); there is no bound uniform over the entire group, and the conjugacy is not required to be a quasi-isometry for a previously chosen metric.

For finitely generated orientation-preserving actions, a stronger published conclusion is available: Deroin–Kleptsyn–Navas–Parwani, *Symmetric random walks on Homeo\(^+(\mathbb R)\)*, Ann. Probab. **41** (2013), 2066–2089, Theorem 8.5, gives a conjugacy to Lipschitz homeomorphisms having bounded displacement for each element. Its stated irreducibility hypothesis can be removed for this application by adjoining two translations with irrationally related translation lengths, applying the theorem to the enlarged finitely generated group, and restricting the conjugacy. Thus (1) is a consequence of credited existing work. We do not assert that those authors explicitly framed their theorem as an answer to Calegari's question.

The earlier source, Calegari's *The Geometry of R-covered foliations* (2000), Question 5.3.19, p. 511, asks precisely the per-element inequality. Its §1.1, p. 461, assumes a closed orientable manifold and a co-orientable foliation, so the group is finitely generated and the action preserves orientation. The elementary argument below proves the needed weaker conclusion directly. A second argument covers arbitrary countable line actions, including orientation reversal, so compactness or a co-orientation omission in the 2002 wording does not create a gap under the usual second-countability convention for manifolds.

## 2. Finite generators: a dominating homeomorphism

**Proposition 1.** Let (G\le\operatorname{Homeo}_+(\mathbb R)) have a finite symmetric generating set (S). There is an increasing homeomorphism (h:\mathbb R\to\mathbb R) such that
\[
 \sup_u|hsh^{-1}(u)-u|\le1\quad(s\in S).
                                                               \tag{2}
\]
Consequently every (g\in G) satisfies (1), with (C(g)=2|g|_S+1).

**Proof.** Define
\[
 F(x)=\max\bigl(\{x+1\}\cup\{s(x):s\in S\}\bigr).
\]
A maximum of finitely many continuous strictly increasing functions is continuous and strictly increasing: a function attaining the maximum at (x) strictly increases at every (y>x). Every function in this finite family tends to each end of the line at the corresponding end, so (F) is onto. Hence it is a homeomorphism, and (F(x)\ge x+1).

Put (a_n=F^n(0)) for (n\in\mathbb Z). These points strictly increase and tend to the two ends. Choose any increasing homeomorphism (h_0:[a_0,a_1]\to[0,1]), and on ([a_n,a_{n+1}]) set
\[
 h(x)=n+h_0(F^{-n}(x)).
\]
The definitions agree at endpoints. They define an increasing homeomorphism of the entire line satisfying (hFh^{-1}(u)=u+1).

For (s\in S), we have (s(x)\le F(x)). Symmetry gives (s^{-1}(y)\le F(y)); putting (y=s(x)) yields (F^{-1}(x)\le s(x)). Applying (h) to both bounds proves (2).

Displacement bounds add under composition: if (|a(u)-u|\le A) and (|b(u)-u|\le B), then (|a(b(u))-u|\le A+B). Thus (|hgh^{-1}(u)-u|\le|g|_S). The reverse triangle inequality gives (1) with bound (2|g|_S); adding one makes (C) positive also at the identity. \(\square\)

No invariant measure, absence of fixed points, or foliation-specific property was used. This proof does not establish the extra Lipschitz regularity in the cited theorem.

## 3. Countable families and orientation reversal

**Proposition 2.** For any countable family ((f_j)_{j\ge1}\subset\operatorname{Homeo}(\mathbb R)), there is a single increasing homeomorphism (h) such that, writing (epsilon_j=1) or (-1) for the orientation of (f_j),
\[
 B_j:=\sup_{u\in\mathbb R}|hf_jh^{-1}(u)-\epsilon_j u|<\infty.
                                                               \tag{3}
\]
Every (f_j) therefore obeys (1), with (C(f_j)=2B_j+1).

**Proof.** Set (r_0=0,r_1=1). Recursively choose (r_{n+1}>r_n+1) so large that, for every (j\le n),
\[
 f_j([-r_n,r_n])\ \cup\ f_j^{-1}([-r_n,r_n])
                 \subset(-r_{n+1},r_{n+1}).                    \tag{4}
\]
This is possible because there are only finitely many compact sets at each step. Define the odd piecewise-affine increasing homeomorphism (h) by (h(r_n)=n) for all (n\ge0).

Fix (j). Suppose (r_n\le|x|\le r_{n+1}), where (n\ge j+1). Applying (4) at index (n+1) gives (|f_j(x)|<r_{n+2}). Applying its inverse-image part at index (n-1\ge j) gives (|f_j(x)|\ge r_{n-1}): otherwise (x\in f_j^{-1}([-r_{n-1},r_{n-1}])\subset(-r_n,r_n)), a contradiction. Consequently
\[
 n\le |h(x)|\le n+1,\qquad
 n-1\le |h(f_j(x))|\le n+2.                                   \tag{5}
\]
Also (4) at index (j) implies (|f_j^{-1}(0)|<r_{j+1}\le|x|). Monotonicity now gives
(operatorname{sign}f_j(x)=\epsilon_j\operatorname{sign}x).
The signed difference in (3), evaluated at (u=h(x)), has absolute value at most (2) by (5).

On the remaining compact interval (|x|\le r_{j+1}), continuity already suffices. More explicitly, (4) at (j+1) gives (|h(f_j(x))|\le j+2) and (|h(x)|\le j+1), so (B_j\le2j+3). Finally
\[
 \bigl|\,|hf_jh^{-1}(u)-hf_jh^{-1}(v)|-|u-v|\,\bigr|
 \le |hf_jh^{-1}(u)-\epsilon_j u|
     +|hf_jh^{-1}(v)-\epsilon_j v|
 \le2B_j.
\]
This proves the claim. \(\square\)

The enumeration is fixed once, and the same (h) works for all its members. It is not a separate conjugacy chosen for each element. The construction also works for a finite family by repeating its entries.

## 4. Application to the exact leaf-line action

A connected second-countable 3-manifold has countable fundamental group. For instance, a countable triangulation gives a countable 1-skeleton, whose finite edge loops surject onto the fundamental group. For the closed smooth manifolds in the earlier source, a finite triangulation gives finite generation directly.

Choose one initial homeomorphism from the leaf space to (mathbb R). Enumerate the image of the holonomy representation and apply Proposition 2; composing the initial coordinate with (h) gives (1) for every element of (pi_1(M)). Nonfaithfulness is harmless, and the bound can be assigned through the image. Hence the displayed condition in Question 8.2 is affirmative. In the original closed co-oriented setting, Proposition 1 alone suffices, as does the stronger published theorem.

Atoroidality is not needed for this topological, per-element formulation. The result makes no assertion about the ambient Hausdorff distance between leaves, the quality of (h) relative to a geometric transverse metric, uniformity of (C) across group elements, or simultaneous Lipschitz regularity in the countable-family argument.

## 5. Historical warning and controls

The 2002 Remark (2) says that toroidal examples can fail the preceding condition. That cannot serve as an obstruction to the **literal topological-conjugacy/per-element bound** proved here. We retain the mismatch explicitly rather than silently strengthening the target. We have not determined an additional geometric restriction that would recover the intended historical distinction. The queue correction concerns the displayed statement, not an inferred stronger question.

Two useful controls make the quantifiers concrete:

1. For the cyclic dilation (x\mapsto2x), the original Euclidean additive distortion is unbounded. In the coordinate (h(x)=\operatorname{sign}(x)\log(1+|x|)), its (k)-th power has displacement at most (|k|\log2). Thus expansion in the old coordinate does not obstruct the permitted arbitrary topological reparameterization.
2. In this same coordinate, for (k>0) and (u\ge0), the conjugated map is (u\mapsto\log(1+2^k(e^u-1))). It fixes (0), while its displacement tends to (k\log2) as (u\to\infty). The additive-distortion constants for these powers in this chosen coordinate cannot be bounded uniformly in (k). The conclusion proved is genuinely per-element; it does not produce a group-uniform constant.

`verify.py` checks finite rational piecewise-affine instances of the common-coordinate exhaustion, both orientations, endpoint and inverse-image inequalities, and the exact reduction from signed displacement to two-point distortion. These are diagnostics for the proof, not exhaustive tests of arbitrary homeomorphisms.

## References

- D. Calegari, *Problems in foliations and laminations of 3-manifolds*, 2002, version 0.78, Question 8.2 and Remarks, p. 16. [arXiv:math/0209081v1](https://arxiv.org/abs/math/0209081v1).
- D. Calegari, *The Geometry of R-covered foliations*, Geom. Topol. **4** (2000), 457–515; §1.1, p. 461, and Question 5.3.19, p. 511. [Published full text](https://msp.org/gt/2000/4-1/gt-v4-n1-p17-p.pdf).
- B. Deroin, V. Kleptsyn, A. Navas, K. Parwani, *Symmetric random walks on Homeo\(^+(\mathbb R)\)*, Ann. Probab. **41** (2013), 2066–2089; Proposition 8.4 and Theorem 8.5. [DOI](https://doi.org/10.1214/12-AOP784); [arXiv:1103.1650v3](https://arxiv.org/abs/1103.1650v3), reprint pp. 22–23.
