# Parent analytical reproduction — PR838 / 10000036

Date: 2026-10-15 UTC. Mathematical verdict: **PASS** for the exact ordinary finite-energy theorem. The frozen author proof is 16,299 bytes, SHA-256 `c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d`, at head `ed2de7249953ba0c1afad253adca9b820d7297c5`. This is an analytical proof reproduction, not a simulation or a formal certificate. Priority and submission readiness are separate gates.

## Exact assertion and imported input

For each integer d≥2, the claimed law is a nearest-neighbor **bond** subgraph of Z^d, invariant under every graph automorphism and mixing under translations. Both single-edge conditional probabilities, given every other output edge, are strictly positive almost surely. Almost surely it has a unique infinite component C, and quenched Bernoulli bond and site thresholds of both X and C equal one. A uniform energy bound, or failure of every such marginal bound, is not claimed. Neither all-vertex percolation, positive association, finite dependence nor finitary coding is part of the assertion.

The imported connected one-ended spanning tree is Timár's exact inspected arXiv1805.10690v1 Theorem1/Corollary2. Its factor convention is checked against Definition6 in1712.08210v1. The rooted deterministic lattice is ergodic; summation over displacement vectors verifies the mass-transport identity. Independent uniformly shifted finite box partitions give invariant amenability with boundary density tending to zero. Outside a sufficiently large box the lattice is connected for d≥2, verifying one-endedness. The factor is equivariant under every graph isomorphism, supplying full automorphism invariance, not just translations. The exact final journal body was not retrieved and is not asserted identical to v1. This audit checks the theorem's stated hypotheses and subsequent use, rather than claiming an independent reproof of the classical input.

Pemantle supplies an optional older UST input for2≤d≤4. His high-dimensional disconnected forest is not substituted: the proposed non-tree-edge path may not exist between different forest components. The all-dimensional proof uses Timár.

## Deterministic finite-past geometry and the kernel

Let G be countably infinite, connected and simple with degree bound Δ, and let T be a connected one-ended spanning tree. Deleting an edge t has exactly one finite component S(t). Indeed two infinite components would each contain a ray by local finiteness and give two ends; two finite components cannot cover T. Thus s(t)=|S(t)| is a positive integer.

Along the unique ray from any v, write its edges t_n. Their finite sides S_n contain v and increase strictly, since the next ray vertex enters the next finite side. Hence their sizes s_n are distinct positive integers. In fact S_n exhaust all vertices, by coalescence of rays. For a non-tree edge e, its finite connecting tree path P_T(e) exists, and M(e)=max_{t∈P_T(e)}s(t) is finite and positive. If e crosses S(t), its path uses t, and M(e)≥s(t). At most Δs(t) ambient edges cross S(t).

Given T, independent edge uniforms retain t∈T with probability1−2^{-s(t)} and include e∉T with probability2^{-M(e)}. Every parameter is in(0,1). The finite-side/path functions are Borel by countable unions over finite connected sets and finite paths; each finite set has finite incident boundary. The good connected one-ended-tree domain is Borel and automorphism invariant; assigning rates1/2 on its null complement gives a globally measurable equivariant kernel. An enumeration can describe this measurability without becoming a geometric choice in the law.

## Bypasses, summability and all vertices

For each fixed good T and v, let B_n mean that t_n is deleted or at least one non-tree boundary edge of S_n is included. A union bound gives

    P(B_n | T) ≤ (1+Δs_n)2^{-s_n},
    Σ_n P(B_n | T) ≤ Σ_{m≥1}(1+Δm)2^{-m} = 1+2Δ.

The first Borel–Cantelli lemma, requiring no independence between B_n, proves eventual retention of every ray edge and the exact identity ∂_X S_n={t_n}. All possible crossing edges are controlled, so a path composed of many inserted edges cannot evade this boundary statement. Neither connectivity of S_n in X nor independence of cut events is assumed. Countability of vertices gives one conditional probability-one event valid for every v, then integration gives one joint probability-one event for(T,X).

## Percolation, uniqueness and quenched thresholds

Retained ray tails prove percolation of R=X∩T. Any two such tails coalesce and their common late tail is retained. Every infinite R-component contains a ray, so there is exactly one, C_R. Any infinite X-component starting at v must exit every finite S_n. At all late cuts it crosses t_n, whose endpoints lie in C_R. Consequently every infinite X-component meets C_R, and X has one infinite component C. This also rules out a separate infinite component assembled only from inserted edges joining finite retained-tree pieces.

Fix a good pair(T,X) before any thinning. For a given v, an infinite bond-thinned path must retain arbitrarily many distinct fixed t_n. Its probability is at most p^k for every k, hence zero for p<1. Countability excludes every infinite thinned component. The good event does not depend on p: the deterministic argument applies to every real p<1 on the same graph. At p=1, C exists. Restricting late cuts to C gives ∂_C(S_n∩C)={t_n} because both endpoints of t_n lie in C_R⊂C. Thus p_c(X)=p_c(C)=1. For site thinning, the infinitely many distinct consecutive ray vertices must be retained, giving the same bound.

These witness conclusions transfer to the output marginal without a non-Borel projection assumption. For bond thinning one can use the Borel graph-only certificate: for every v and k there are finite sets F_i containing v with singleton X-boundaries whose boundary edges are pairwise distinct. This uses countably many finite witnesses. For bond and site thresholds, connection probabilities at fixed rational p and v are decreasing limits of measurable finite-ball connection polynomials. Their vanishing for countably many p,v is Borel; monotonicity supplies every real p<1. No measurable selection of T from X is required.

## Marginal energy, symmetry and mixing

Let F_e=σ(X_f:f≠e) and H_e=σ(T,U_f:f≠e). Then F_e⊂H_e, U_e is independent of H_e, and r_T(e) is H_e-measurable. Consequently

    P(X_e=1 | F_e)=E[r_T(e) | F_e],
    P(X_e=0 | F_e)=E[1−r_T(e) | F_e].

Conditional expectations of strictly positive integrable variables are strictly positive almost surely: otherwise integration over their measurable zero set contradicts strict positivity. This proves both states positive after forgetting T; merely checking conditional-on-T rates would not suffice. Countably many edges allow a common exceptional null set. Conditional versions can be set to1/2 on excluded conditioning configurations. Conversely small hidden-tree rates alone do not prove failure of uniform marginal energy, and no such inference is made.

The finite-past/path rules commute with every automorphism. The full-equivariant iid tree input and independent iid edge marks therefore give full symmetry. Their joint translation action is mixing: approximate measurable events by finite-coordinate cylinders, separate translated finite supports, then let approximation errors tend to zero. Measurable equivariant factors inherit this mixing; no finite coding radius or quantitative decay rate is assumed.

## Artifact and literature boundaries

The parent read the complete frozen author proof, approach and scope documents, both earlier complete mathematical audit reports, and all three fresh family reports. Root primary reading extents/pins and additional HM/PT/factor-definition reading are separately recorded. Fresh source-scope checks confirm the historical BHS/BT ordinary-energy bond convention; uniform energy would be a different claim.

The independent static checker verifies all27 frozen regular files and Git blob identities, the closed26-entry publication inventory, all3 archives/15 members and unpacked copies, and acceptance bindings. It passes normally and with optimization, rejecting11 parser/path controls. No source member was executed. The historical21-control checker was not distributed and is not claimed reproduced. These integrity checks do not prove the mathematical theorem.

No required mathematical repair was found. Original proof effort remains3/5, with no additional central proof-search attempt. Mathematical validity does not establish novelty or historical priority. In particular the fresh planar HM implication must be integrated honestly before preprint promotion.
