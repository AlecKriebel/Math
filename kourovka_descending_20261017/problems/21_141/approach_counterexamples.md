# Counterexample approaches to Kourovka 21.141

Research checkpoint: **2026-10-17 21:24 UTC**. Overall discovery estimate **11%**; scoped negative-route audit complete. No complete counterexample has been found. The problem is not marked solved, and no novelty claim is made for the elementary deductions below. Independent adversarial verification of the shear, normal-edge and image-factor claims passed; see `counterexamples/review_collapse.md`. Fresh root-level review is still required before promotion.

The exact negative target is a pro-p pushout \(G=A\amalg_H B\), with coherent pro-p vertices and a polycyclic pro-p edge, together with a **closed topologically finitely generated** subgroup \(S\leq G\) for which \(\dim_{\mathbb F_p}H^2(S,\mathbb F_p)=\infty\). An abstract incoherent dense subgroup, a finite quotient with many relations, or a noninjective vertex map alone does not meet this target.

## Approach families and current gaps

| Family | Mechanism | Evidence and status | Exact remaining gap |
|---|---|---|---|
| Induced-subgraph pro-p RAAG amalgams | Place an induced cycle, hence a finitely generated non-finitely-presented Bestvina–Brady subgroup, across the amalgam | Blocked in the standard full-subgraph construction. Polycyclic full RAAG edge must be a clique; clique-sums of chordal graphs remain chordal. Independent report: `counterexample_raag/RAAG_ROUTE.md`. | A materially different, nonstandard embedding would be needed; replacing the edge by a free pro-p group violates the hypothesis. |
| Kernels of maps to \(\mathbb Z_p\), and then abelian quotients | Construct a topologically finitely generated infinite-relator fiber kernel | A finite-orbit cohomology argument and a zero-edge quotient obstruction rule this out for proper amalgams. Independent derivation and proof: `counterexample_raag/FIBER_OBSTRUCTION.md`. | Arbitrary finitely generated closed subgroups need not be fibers or lie in finitely generated fibers. |
| Nonproperness and incompatible local actions | Make vertex images collapse to an incoherent quotient | Explicit rank-two shear amalgam collapses the whole edge and becomes a free pro-p group, hence is coherent. The general normal-edge case is positive by an elementary extension argument below. | A counterexample would require nonnormal edge behavior and rigorous incoherence of the resulting image vertex or another closed subgroup. |
| Inverse limits and finite p-quotients | Seek bounded generator rank but unbounded relation ranks in finite approximations | Finite examples can suggest candidates but cannot by themselves certify a finitely generated non-finitely-presented inverse limit. A persistence requirement is identified below. | Need a compatible inverse system and infinitely many independent classes surviving continuous inflation, or an independent infinite cohomology calculation. |

## 1. A complete nonproper shear calculation

Let \(H=\mathbb Z_p^2\), written additively with column-vector coordinates. Define

\[
U^t=\begin{pmatrix}1&t\\0&1\end{pmatrix},\qquad
L^t=\begin{pmatrix}1&0\\t&1\end{pmatrix}\quad(t\in\mathbb Z_p),
\]

and form \(A=H\rtimes_U\mathbb Z_p\), \(B=H\rtimes_L\mathbb Z_p\). Both are three-dimensional nilpotent pro-p groups, with a finite closed subnormal series having factors \(\mathbb Z_p\). Every closed subgroup of either vertex is polycyclic and finitely presented, by the elementary induction in Section 2. Thus the vertices are coherent and the edge is polycyclic in the required topological sense.

**Claim.** The pro-p pushout \(G=A\amalg_H B\) is \(\mathbb Z_p\amalg\mathbb Z_p\); the entire common \(H\) maps to 1.

**Proof.** Let \(M\) be the image of \(H\) in \(G\). It is a closed, normal, finitely generated abelian subgroup: it is normal in both image vertices and these topologically generate G. The epimorphism

\[
H/pH\longrightarrow M/pM
\]

has a kernel invariant under both U and L. The only common invariant subspaces of \(\mathbb F_p^2\) are 0 and the whole space. Indeed, U has only one invariant line, \(\langle(1,0)\rangle\), and L does not preserve it. Therefore \(M/pM\) is either zero or isomorphic to \(\mathbb F_p^2\).

In the second case conjugation gives a continuous homomorphism from the pro-p group G into \(\operatorname{GL}_2(\mathbb F_p)\) whose image contains U and L, so that image must be a finite p-group. This is impossible. For odd p,

\[
UL^{-1}U=\begin{pmatrix}0&1\\-1&0\end{pmatrix}
\]

has order 4. For p=2,

\[
UL^{-1}=\begin{pmatrix}0&1\\1&1\end{pmatrix}
\]

has order 3. Hence \(M/pM=0\). Since M is a finitely generated abelian pro-p group, Nakayama's lemma (or the classification of finitely generated \(\mathbb Z_p\)-modules) gives M=0. Killing H leaves precisely the two free procyclic generators. The universal property supplies mutually inverse maps between G and \(\mathbb Z_p\amalg\mathbb Z_p\). QED.

This is a proper infinite-group deduction, not an inference from finite computations. The finite-matrix script `counterexamples/shear_checks.py` checks the local algebra and supplies reproducible examples; the preceding argument works for every prime.

**Consequence.** The standard incompatible-shear nonproperness example is a false counterexample: it loses its edge and its surviving group is coherent.

## 2. A positive theorem excluding all normal-edge collapse gadgets

**Proposition (elementary).** If H is polycyclic pro-p and normal in both coherent pro-p vertices A and B, then their pro-p pushout is coherent, even if it is not proper.

The following elementary facts make the proof checkable.

1. Closed subgroups and continuous quotients of a polycyclic pro-p group are polycyclic. Intersect a finite closed subnormal procyclic series with the subgroup, or take its images in the quotient. Each resulting factor is a closed subgroup or quotient of a procyclic pro-p group.
2. Polycyclic pro-p groups are topologically finitely generated and finitely presented. The procyclic cases have presentations \(\langle x\mid\ \rangle\) or \(\langle x\mid x^{p^a}\rangle\). Finite generation and finite presentation are preserved by extensions. For the latter, take finite presentations for kernel and quotient, lifts of quotient generators, finitely many conjugation rules in both directions, and one lifted kernel word for each quotient relator. These relations give the extension by the normal form map to the prescribed kernel and quotient.
3. If C is coherent and K is a closed topologically finitely generated normal subgroup, then C/K is coherent. For a finitely generated closed subgroup D of C/K, its preimage P is generated by finitely many lifts together with a finite generating set of K. Hence P is finitely presented. Presenting D=P/K adds only finitely many normal relators.
4. A pro-p extension with coherent quotient and polycyclic kernel is coherent. For a finitely generated closed subgroup S of the extension, the kernel S intersected with the polycyclic subgroup is finitely generated and finitely presented, and the image of S is finitely presented by coherence. Apply extension finite presentability.
5. Free pro-p products of coherent groups are coherent, by the Kurosh theorem for topologically finitely generated closed subgroups: such a subgroup is a finite free pro-p product of a finitely generated free pro-p group and finitely many finitely generated intersections with conjugates of the vertex factors. The restriction to finitely generated subgroups matters; an unrestricted naive Kurosh statement for all closed subgroups must not be substituted. The exact primary theorem read by the adversarial reviewer is Haran, *On closed subgroups of free products of profinite groups*, Proc. London Math. Soc. (3) 55 (1987), 266–298, **Theorem 9.7, p.298**, [author PDF](https://www.tau.ac.il/~haran/Papers/closed_subgroups.pdf), [DOI](https://doi.org/10.1093/plms/s3-55_2.266). Its separability hypothesis applies to finitely generated pro-p groups. Arbitrarily many nontrivial Kurosh factors would give arbitrarily large Frattini-quotient dimension; hence only finitely many occur, and each is a finitely generated retract. The earlier Herfort–Ribes paper [DOI](https://doi.org/10.1017/S0305004100066548) also treats the finitely generated case, but its full text was not needed here.

To prove the proposition, let M be the common image of H in G. It is closed, polycyclic and normal. By the universal property,

\[
G/M\simeq (A/H)\amalg(B/H).
\]

Both quotients on the right are coherent by fact 3. Their free pro-p product is coherent by fact 5. Fact 4, applied to the polycyclic kernel M, proves coherence of G. QED.

## 3. Category and image-factor audit

For an arbitrary pro-p pushout, let \(\bar A,\bar B,\bar H\) be the actual closed images of the factors and edge in G. A compatible pair of continuous maps from \(\bar A,\bar B\) agreeing on \(\bar H\) lifts to a compatible pair from A,B, hence extends uniquely to G. It follows directly that

\[
G\simeq\bar A\amalg_{\bar H}\bar B
\]

is a proper pushout of the **image** factors. This does not prove the original vertices embed, nor does it show their quotient images are coherent. Coherence passes to a quotient with a finitely generated normal kernel by fact 3, but arbitrary kernels are not covered.

There is also an independently checked direct proof of \(\bar A\cap\bar B=\bar H\), avoiding any Bass–Serre citation. Put \(W=\mathbb F_p[[G/\bar H]]\), and let m be the basis vector at the edge coset. The pro-p semidirect product \(W\rtimes G\) admits compatible maps

\[
a\longmapsto(a\cdot m-m,a),\qquad b\longmapsto(0,b)
\]

from \(\bar A\) and \(\bar B\). Compatibility holds because every element of \(\bar H\) fixes m. If \(x\in\bar A\cap\bar B\), the extended homomorphism from G must send x to both displayed values, so \(x\cdot m=m\). The stabilizer of m is exactly \(\bar H\): distinct coset vectors are separated in some finite permutation module \(\mathbb F_p[G/\bar H U]\). Thus x lies in \(\bar H\). All groups, maps and completed modules are continuous; the finite module semidirect products are finite p-groups.

A current primary preprint, Peng–Yang, [arXiv:2608.02193v2](https://arxiv.org/abs/2608.02193v2), Theorem 4.1, establishes a related image-factor pushout for pro-p completions of abstract amalgams. Its accompanying assertion that closure of the original edge may be smaller than the image-factor intersection has not been adopted here: the same universal-property proof appears to work with that edge closure, and the discrepancy needs resolution before relying on the narrative claim. The theorem over the actual intersection is not being claimed false.

For procyclic edges the original amalgam is always proper: Quadrelli–Snopce–Vannacci, [arXiv:1906.04789v2](https://arxiv.org/abs/1906.04789v2), text immediately after Proposition 5.21, explicitly recalls this standard fact. Hence cyclic-edge candidates cannot obtain a negative answer merely by vertex collapse.

**Unsupported kernel reduction.** Let \(K=\ker(H\to G)\) and \(N_i=\overline{\langle\!\langle K\rangle\!\rangle}_{G_i}\). One can check \(N_i\cap H=K\), because \(N_i\subseteq\ker(G_i\to G)\), and G is the same pushout of \(G_i/N_i\) over \(H/K\). It does not follow from this calculation that the new vertices embed in G. That would require a separate theorem saying that an injective final edge map forces injective final vertex maps. No such theorem is used here. Furthermore, even equality \(N_i=\ker(G_i\to G)\) would only give finitely many **normal generators** for the vertex kernels; it would not imply that those kernels are topologically finitely generated as groups. Fact 3 cannot be applied on the basis of normal generation. These are two distinct gaps, so Noetherian stabilization of subgroups of H alone does not settle nonproper amalgams.

## 4. What finite quotient searches would have to certify

Finite p-groups are themselves finitely presented. Unbounded relation ranks among finite quotients of an inverse limit do not establish non-finite-presentability of the limit: for example, free pro-p groups have very complicated finite p-quotients while having no defining relations. In cohomology,

\[
H^2(S,\mathbb F_p)=\varinjlim_U H^2(S/U,\mathbb F_p),
\]

with the appropriate continuous inflation maps. Finite-level classes may die under later inflation. A valid computational certificate therefore needs a compatible system and arbitrarily large linearly independent sets whose classes survive all sufficiently deep refinements, or an independent proof of infinite continuous second cohomology. Generator bounds in unrelated finite approximations also do not supply the missing closed subgroup of a fixed amalgam.

The finite matrix checks in this route are deliberately used only for their local algebraic claims. They do not certify the sought incoherent subgroup.

## 5. Attempt to extend the fiber obstruction to arbitrary normal subgroups

Root requested the possible strengthening: for a finitely generated closed normal \(N\triangleleft G\), either N is contained in the edge core, or NH is open in G. If true in the needed generality, the finite-orbit argument would show finite presentability of N. This statement is **not proved here** and no abstract normal-subgroup theorem is being imported into the pro-p category.

The primary lead Zalesskii, *Normal subgroups of free constructions of profinite groups and the congruence kernel in the case of positive characteristic*, Izv. Math. 59 (1995), 499–516, [MathNet primary entry](https://www.mathnet.ru/eng/im22), **Theorem B, p.500**, gives a graph-of-profinite-groups description for closed normal subgroups and says its conclusions also hold in the pro-C category. Its underlying graph is profinite; the statement does not assert it finite. The source therefore does not by itself give the desired openness of NH. The primary PDF was indexed and its theorem statement retrieved, but direct local download repeatedly timed out; no full-paper verification is claimed.

The finite-quotient reduction produces virtually free pro-p approximants with finitely generated normal images. Their rank/Euler-characteristic inequalities retain the order of the finite image of \(N\cap H\), which can grow without bound. They consequently do not furnish a uniform bound on the number of N-edge orbits. A finite-rank edge has bounded generator rank, not bounded orders of finite quotients. This is the exact obstruction in the attempted estimate.

For abelian G/N, the hyperplane argument in the independent fiber report does prove NH open whenever N is finitely generated. For a general nonabelian quotient, there need not be a continuous character to \(\mathbb Z_p\) killing the edge image. Quotients whose open subgroups all have finite abelianization make that character argument unavailable. This marks an unsupported route, not a counterexample.

## Checkpoints

- Opening checkpoint (before the first clock-verified timestamp, 2026-10-17 21:17 UTC): started an independent negative family audit; discovery estimate **5%**. Opened RAAG/fiber and nonproperness approaches separately from the affirmative homology route.
- 2026-10-17 21:17 UTC: explicit infinite shear pushout determined; discovery estimate **9%**. Normal-edge extension argument identified. Complete counterexample still absent.
- Intermediate checkpoint (between 2026-10-17 21:17 and 21:24 UTC): standard RAAG and cyclic fiber routes have rigorous obstructions; discovery estimate **11%**. Independent adversarial review requested for image-factor, normal-edge, and shear claims. Exact remaining general gap: arbitrary finitely generated closed subgroups with potentially infinite quotient graph.
- 2026-10-17 21:24 UTC: independent review passed for three elementary claims; abelian-quotient fiber corollary completed. Discovery estimate remains **11%**. General normal-subgroup strengthening still lacks the needed finite-orbit theorem; kernel-normal-generation and topological-generation gaps separated. No repository operations, external contact, solved-status change or publication performed by this route.
