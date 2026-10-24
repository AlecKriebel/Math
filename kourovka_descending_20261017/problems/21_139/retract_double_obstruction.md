# Retracts and the failed conjugate-double mechanism

Checkpoint: 2026-10-24T16:32:22.520827+00:00. Discovery estimate for full21.139: **12%**. This is a known lemma and a restricted construction obstruction, not a solution or novelty claim.

Let G be torsion-free hyperbolic and let r:G→A be a retraction. Then A is malnormal: A∩gAg⁻¹=1 for g∉A.

For nontrivial x∈A, the centralizer C_G(x)=〈c〉 is infinite cyclic. Write x=c^m with m≠0. Since r(c)^m=r(x)=x=c^m, unique roots imply r(c)=c. Thus C_G(x)≤A. For arbitrary g write g=n r(g), where n∈ker r. Since r(g) normalizes A, gAg⁻¹=nAn⁻¹. If x=nyn⁻¹ is nontrivial and x,y∈A, applying r gives x=y, so n centralizes x. Hence n∈C_G(x)≤A, and n∈A∩ker r=1. Therefore g∈A, proving the assertion.

This exact theorem is already Lemma4.4 in MarcoLinton, *Embedding finitely generated free-by-cyclic groups in {finitely generated free}-by-cyclic groups*, arXiv2510.10178v2 (22Apr2026), IMRN2026,rnag020. Primary source: https://arxiv.org/abs/2510.10178 ; the displayed lemma/proof is also at https://academic.oup.com/imrn/article/2026/4/rnag020/8494558 . An older statement is Corollary20, p.70 of Myasnikov's *Combinatorics over free groups* author-hosted teaching monograph. No new lemma is claimed.

An abstract double A∗_{〈w〉}A with w homologically zero in both vertex copies can carry a two-class by Mayer–Vietoris. However, two distinct conjugates of this retract A in its chosen torsion-free hyperbolic retraction host have trivial intersection. They cannot realize that nontrivial cyclic amalgamation inside this host. This obstruction does not apply to different nonconjugate copies, or to conjugators outside the finite-index retraction host in a larger original ambient group. It also does not preclude arbitrary other embeddings of the abstract double.

The valid direction for virtual Betti numbers is vb₂(A)≤vb₂(G), by finite-index retraction pullbacks. Unbounded vb₂ of a hyperbolic finite-rank-free-by-cyclic overgroup does not force unbounded vb₂ of its retract. Linton's quasiconvex retract embedding therefore supplies a controlled host, rather than a solution of the zero-vb₂ freeness remainder.
