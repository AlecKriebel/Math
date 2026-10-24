# Central quotients and stabilization: an obstruction to a construction route

Status: derived algebraic consequences of published theorems; no counterexample to Kourovka 21.129 and no novelty claim. Prepared 24 October 2026. The algebraic statements below are unconditional given the cited Cumplido–Paris results. The quasi-isometry extension states its additional geometric input explicitly.

## Exact question and source inputs

Could one start with products of irreducible spherical Artin groups, add rank-one factors, or identify central generators diagonally, and thereby obtain quasi-isometric but noncommensurable groups which are both spherical Artin groups?

Use the following notation. Let \(A_\Gamma\) be a spherical Artin group. Suppose \(\Gamma\) has \(p\) connected components, of which \(k\) have at least two vertices and \(a=p-k\) are singletons. Write \(T_1,\ldots,T_k\) for the nonsingleton types and
\[
 Q_i=P_{T_i}/Z(P_{T_i}),
\]
where \(P_T\) is the pure Artin subgroup. Products indexed by the empty set mean the trivial group.

[Cumplido–Paris, *Commensurability in Artin groups of spherical type*](https://doi.org/10.4171/RMI/1282), Proposition 3.1 and Corollary 3.2, give a finite-index subgroup
\[
 P_\Gamma\cong \left(\prod_{i=1}^k Q_i\right)\times\mathbb Z^p.
 \tag{1}
\]
Each \(Q_i\) and every finite-index subgroup of \(Q_i\) have trivial center; Lemma 4.1 gives the stronger trivial-centralizer statement. Theorem 2.2 says that spherical Artin products are commensurable exactly when their lists of irreducible components can be matched by commensurability. A singleton component is \(A_1\cong\mathbb Z\); it cannot match a nonsingleton because the latter has cohomological dimension at least two (Proposition 2.1), or because its center quotient has a nontrivial finite-index centerless factor.

The primary paper is cached in the priority audit at `../../priority/sources/cumplido_paris_2022.pdf`; text locations were inspected directly. These inputs are existing theorems, not conclusions of this probe.

## Lemma 1: central lattices only consume abelian directions

**Claim.** If \(C\le Z(A_\Gamma)\) is free abelian of rank \(r\), \(0\le r\le p\), then
\[
 A_\Gamma/C\quad\text{is virtually isomorphic to}\quad
 \left(\prod_{i=1}^k Q_i\right)\times\mathbb Z^{p-r}.
 \tag{2}
\]
In particular,
\[
 (A_\Gamma/C)\times\mathbb Z^r\sim_{\rm comm}A_\Gamma.
 \tag{3}
\]

**Proof.** The center of a direct product is the product of the centers, so the center of \(A_\Gamma\) is \(\mathbb Z^p\). Set \(L=C\cap P_\Gamma\). As \(P_\Gamma\) has finite index, \([C:L]<\infty\), hence \(L\) has rank \(r\). Also \(L\le Z(P_\Gamma)\). In the splitting (1), the center is exactly the displayed \(\mathbb Z^p\), since the \(Q_i\)'s have trivial center. Therefore
\[
 P_\Gamma/L\cong
 \left(\prod_iQ_i\right)\times(\mathbb Z^p/L).
\]
The map from \(P_\Gamma\) to \(A_\Gamma/C\) has kernel precisely \(L\), and its image has finite index. Hence \(P_\Gamma/L\) embeds as that finite-index image. Smith normal form yields
\[
 \mathbb Z^p/L\cong\mathbb Z^{p-r}\times F
\]
for a finite abelian group \(F\). The subgroup obtained by setting the \(F\) coordinate equal to its identity has finite index. This proves (2); taking its product with \(\mathbb Z^r\) and using (1) proves (3). No primitivity assumption on \(L\), or on \(C\), was used. ∎

**Boundary cases.** If \(r=0\), nothing is removed. If \(r=p\), the remaining free abelian factor is trivial. If \(k=0\), this is the ordinary quotient of \(\mathbb Z^p\) by a sublattice; it is virtually \(\mathbb Z^{p-r}\). If \(p=k=r\), the central quotient is virtually \(\prod_iQ_i\), and this is not commensurable with a nontrivial spherical Artin group. If the empty diagram is admitted, it represents the trivial group; finite groups are commensurable with it through their trivial finite-index subgroup. Thus \(k=0,r=p\) is consistent with the empty case.

**Nonprimitive examples.** With \(A_\Gamma=\mathbb Z^2\) and \(C=\langle(2,2)\rangle\), the quotient is \(\mathbb Z\times\mathbb Z/2\); its torsion-free finite-index subgroup is \(\mathbb Z\). With primitive \(C=\langle(1,1)\rangle\), the quotient is already \(\mathbb Z\). Diagonal slope and lattice divisibility affect the finite torsion part, but not (2).

Primitivity in \(Z(A_\Gamma)\) does not assert that the whole quotient \(A_\Gamma/C\) is torsion-free: an element outside the center may have a nontrivial power in \(C\). The proof needs only the displayed finite-index subgroup, and its finite torsion factor comes specifically from \(Z(P_\Gamma)/L\). It makes no assertion that all torsion in the entire quotient is central.

## Proposition 2: exact algebraic eligibility criterion

**Claim.** Allowing the empty diagram to represent the trivial group, for \(C\) as in Lemma 1, \(A_\Gamma/C\) is commensurable with a spherical Artin group if and only if
\[
 r\le a=p-k.
 \tag{4}
\]
When (4) holds, it is commensurable with the Artin group obtained from \(\Gamma\) by deleting any \(r\) singleton components. Moreover every spherical Artin group commensurable with this quotient has exactly \(k\) nonsingleton components, matched up to commensurability with the \(T_i\)'s, and exactly \(a-r\) singleton components. If only nonempty diagrams are admitted, the finite case \(k=0,r=p\) is excluded from this claim; finite groups cannot be commensurable with a nonempty spherical Artin group, since the latter is torsion-free and infinite.

**Proof of sufficiency.** Deleting \(r\) singleton components leaves a diagram with the same \(Q_i\)'s and \(p-r\) components. Equation (1) for that diagram agrees with (2).

**Proof of necessity and the stronger classification.** Suppose \(A_\Gamma/C\sim_{\rm comm}A_\Omega\), and let \(q\) be the number of components of \(\Omega\). Products preserve commensurability, so (3) gives
\[
 A_\Gamma\sim_{\rm comm}A_\Omega\times\mathbb Z^r
 =A_{\Omega\sqcup rA_1}.
\]
Apply Cumplido–Paris Theorem 2.2. The right-hand diagram has \(r\) explicit singleton components, all of which must match singletons of \(\Gamma\). Thus \(r\le a\), \(q=p-r\), and all remaining irreducible components match as claimed. This argument does not invoke any unproved cancellation theorem for arbitrary groups. ∎

A diagonal central product of two nonsingleton irreducible spherical Artin groups has \(p=k=2,r=1\). It therefore fails (4). Such a group is not commensurable with any spherical Artin group. Adding a singleton before quotienting changes \(a\) from zero to one and makes the quotient eligible, but then it is already commensurable with the original product of the two nonsingleton groups.

More generally, if one also appends \(s\) new rank-one factors after quotienting, then
\[
 (A_\Gamma/C)\times\mathbb Z^s
 \sim_{\rm comm}
 \left(\prod_iQ_i\right)\times\mathbb Z^{p-r+s}.
\]
This is commensurable with a spherical Artin group exactly when \(p-r+s\ge k\), with the same empty-diagram convention as above. In the eligible case it has the same nonsingleton components and \(a-r+s\) singleton components up to commensurability. For a full necessity argument, put \(u=p-r+s\), \(U=(\prod_iQ_i)\times\mathbb Z^u\), and \(B=\prod_iA_{T_i}\). If \(U\sim_{\rm comm}A_\Omega\), then
\[
 A_\Omega\times\mathbb Z^k\sim_{\rm comm}U\times\mathbb Z^k
 \sim_{\rm comm}B\times\mathbb Z^u.
\]
Theorem 2.2 forces \(\Omega\) to have \(k\) nonsingleton components and \(u-k\) singletons. Thus \(u\ge k\).

## Proposition 3: cyclic stabilization cannot hide a commensurability mismatch

For spherical Artin groups \(A_\Gamma,A_\Omega\) and integers \(s,t\ge0\),
\[
 A_\Gamma\times\mathbb Z^s\sim_{\rm comm}
 A_\Omega\times\mathbb Z^t
\]
if and only if their nonsingleton components match up to commensurability and their total numbers of components satisfy
\[
 p_\Gamma+s=p_\Omega+t.
\]
This is Theorem 2.2 applied to \(\Gamma\sqcup sA_1\) and \(\Omega\sqcup tA_1\). In particular, taking \(s=t\) proves cancellation within this class:
\[
 A_\Gamma\times\mathbb Z^s\sim_{\rm comm}
 A_\Omega\times\mathbb Z^s
 \iff A_\Gamma\sim_{\rm comm}A_\Omega.
\]
Allowing unequal stabilizations can compensate only for a different number of singleton components. It cannot turn a noncommensurable pair of nonsingleton irreducible factors into a commensurable pair.

The independent auditor also supplied a direct general lemma: if the virtual centers of \(G\) and \(H\) are trivial, then \(G\times\mathbb Z^s\sim_{\rm comm}H\times\mathbb Z^t\) if and only if \(G\sim_{\rm comm}H\) and \(s=t\). For a finite-index subgroup \(K\le G\times\mathbb Z^s\), one has \(Z(K)=K\cap\mathbb Z^s\) and \(K/Z(K)\cong\operatorname{pr}_G(K)\le_{fi}G\); a finite-index isomorphism preserves both this quotient and the rank of the center. The full proof, an independent factor-matching argument, and an example showing why mere centerlessness is insufficient are in [the audit](cancellation_audit/audit.txt).

## Quasi-isometry extension: exact cited geometric input

The algebraic propositions above need no geometric claim. For the broader quasi-isometry obstruction, use the following published input explicitly:

- [Kapovich–Kleiner–Leeb, *Quasi-isometries and the de Rham decomposition*](https://math.nyu.edu/~bkleiner/kkl.pdf), Theorem B (author-hosted manuscript pp. 2–3): for geodesic products whose distinguished factors have all asymptotic cones homeomorphic to Euclidean spaces and whose remaining factors have coarse type I or II, a quasi-isometry preserves the Euclidean dimension and number of remaining factors and matches the latter up to quasi-isometry. Remark 1.4 allows shearing in Euclidean directions; a full product-map assertion is not needed here.
- Cumplido–Paris Remark 5.2 (published pp. 514–515) states that the \(Q_i\)'s in (1) are of coarse type I, citing their references [9], [38], and KKL Proposition 4.2. The remark explicitly uses Theorem B for this decomposition. This probe has checked the statement and its use, but has not independently reproduced the coarse-type-I verification from those three inputs.

With this input, if \((\prod_iQ_i)\times\mathbb Z^u\) is quasi-isometric to a spherical Artin group with \(q\) components and \(\ell\) nonsingleton components, then KKL gives \(u=q\) and \(k=\ell\). Since \(q\ge\ell\), necessarily \(u\ge k\). Conversely \(u\ge k\) makes the model commensurable, hence quasi-isometric, to an eligible product having the same nonsingleton types and \(u-k\) singletons. Therefore a central quotient in Proposition 2 with \(r>a\) cannot even be quasi-isometric to an eligible spherical Artin group, on the cited coarse-type-I input.

The same input shows that cyclic stabilization adds no new irreducible quasi-isometry comparisons. For irreducible nonsingleton \(A_T,A_U\),
\[
 A_T\times\mathbb Z^s\simeq_{qi}A_U\times\mathbb Z^t
\]
forces \(s=t\) and \(Q_T\simeq_{qi}Q_U\), hence \(A_T\simeq_{qi}A_U\) by multiplying by \(\mathbb Z\). This is a reduction, not a proof that the matched irreducibles are commensurable.

## What is established and what remains open

The central-lattice construction family is blocked as a way to introduce new eligible product geometry: admissible central quotients merely consume singleton factors up to commensurability; inadmissible quotients cannot be quasi-isometric to spherical Artin groups on the cited product-rigidity input. Equal cyclic stabilization cancels for commensurability, and stable quasi-isometry of irreducible factors reduces to their original quasi-isometry comparison.

The central difficulty remains unchanged: establish quasi-isometry or a separating quasi-isometry invariant for the unresolved same-rank irreducible comparisons, and then verify commensurability or noncommensurability for the same pair. No result here supplies either missing implication for an exceptional pair. Reopening this route would require a mechanism that changes a noncentral irreducible factor rather than merely identifying central directions, or a verified failure of the cited product-rigidity hypotheses.

Independent audit: `cancellation_audit/audit.txt` endorsed the algebraic proofs, checked arbitrary finite-index subgroups without assuming they split, and checked primitive/nonprimitive lattices and empty/full-rank boundaries. Its requested kernel/image wording correction was incorporated. The geometric extension was not independently audited in that subtask.
