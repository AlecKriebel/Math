# Construction gates for Kourovka 21.138

Independent route audit, 2026-10-24 17:03:48 UTC. Exact target: an **infinite finitely presented** group all of whose arbitrary infinite-index subgroups are free. This note supplies exclusions and obstruction proofs, not a resolution. Estimated completion toward the full problem: **5%**. No counterexample satisfying every hypothesis has been found.

## 1. A finite-presentation obstruction to embedding monsters

Write IF for the stated infinite-index subgroup property. A finitely presented IF group is coherent: a finitely generated subgroup of infinite index is a finite-rank free group, whereas a finite-index subgroup is finitely presented by Reidemeister–Schreier. Consequently a finitely generated group which is not finitely presented cannot embed into any finitely presented IF group. Its image would have to be finitely presented in either index case.

Thus a Higman embedding of a recursively presented torsion-free monster into a finitely presented overgroup cannot preserve IF. An embedding theorem, without a new control mechanism for all overgroup subgroups, does not remove the finite-presentation obstruction. This conclusion does not depend on whether the monster image is proper.

An infinite IF group is torsion-free: a nontrivial finite cyclic subgroup would have infinite index and would not be free. Prime-exponent Tarski monsters therefore fail immediately. Torsion-free Tarski monsters do satisfy IF, since every proper nontrivial subgroup is infinite cyclic; their known finite-presentation failures matter essentially.

## 2. Two precise finite-presentation gates for recent monsters

Let a fixed finitely generated group map epimorphically through a sequence \(G_i\), with direct limit \(M\). If \(M\) is finitely presented, the kernel from the free group on the fixed generators is finitely normally generated. Each of those finitely many relators vanishes at some stage. At a common later stage the kernel is already the full limit kernel, so the sequence stabilizes to \(M\).

Coulon–Fournier-Facio–Ho [2508.21244v3](https://arxiv.org/html/2508.21244v3), §7.3, construct their torsion-free monsters by epimorphisms through non-elementary hyperbolic groups. Such stages cannot be monsters: non-elementary hyperbolic groups contain nonabelian free subgroups, which themselves have proper noncyclic subgroups. Hence these limits are not finitely presented. The lacunary-hyperbolic criterion in Ol’shanskii–Osin–Sapir, [*Geometry & Topology* 13 (2009)](https://msp.org/gt/2009/13-4/gt-v13-n4-p06-p.pdf), Theorem 8.1, independently gives the same gate: finitely presented lacunary hyperbolic groups are hyperbolic.

The higher-dimensional constructions in Fournier-Facio–Sun [2503.01987v3, 10 April 2025](https://arxiv.org/html/2503.01987v3), Remarks 4.4–4.5, have an even stronger obstruction. In their notation let \(W_i=T_0\vee\bigvee_{j=1}^iY'_j\), with \(m_j=|X_j|\). Then \(b_1(W_i)\leq2+\sum m_j\), and \(T_i\) attaches \(\sum(m_j+2)\) two-cells. The pair exact sequence implies \(b_2(T_i)\geq2i-2\). Wedges followed by two-cell attachments preserve the previously existing \(H_2\). Thus \(H_2(T;\mathbb Q)\), and its image in \(H_2(M;\mathbb Q)\), have infinite dimension. A resolution finite through degree two over \(\mathbb QM\), after tensoring with \(\mathbb Q\), has finite-dimensional degree-two chain space; its homology is finite-dimensional. Hence these monsters are not \(FP_2(\mathbb Q)\), and in particular are not finitely presented. The same source explicitly records the missing finitely presented torsion-free Tarski-monster case. This statement concerns that construction route, not all possible IF groups.

## 3. An explicit infinite-index subgroup excludes every group containing BS(1,2)

Consider
\[
B=\langle x,s\mid s^{-1}xs=x^2\rangle.
\]
Set \(x_n=s^nxs^{-n}\), for \(n\geq0\). The relations give \(x_{n+1}^2=x_n\), so
\[
A=\bigcup_{n\geq0}\langle x_n\rangle
\]
is an increasing union of cyclic groups. The affine representation \(x(u)=u+1, s(u)=u/2\) proves that every \(x_n\) has infinite order. It identifies this union, faithfully, with the additive group \(\mathbb Z[1/2]\). The group \(A\) is abelian and noncyclic, hence is not free. The height homomorphism \(B\to\mathbb Z\), \(x\mapsto0, s\mapsto1\), kills \(A\), so \([B:A]=\infty\). Therefore \([G:A]=\infty\) in **every** overgroup \(G\geq B\), and no such \(G\) has IF. This argument also works for \(BS(1,m)\), \(|m|\geq2\).

This rules out the following familiar finite presentations, with actual offending subgroups rather than an inference from finite quotients:

* **Higman’s group.** Adjacent generators embed as \(BS(1,2)\); see Martin, [*On the cubical geometry of Higman’s group*](https://pure.hw.ac.uk/ws/files/15846513/Martin_Higman_Cubical_Duke_Revised_2.pdf), *Duke Math. J.* 166 (2017), 707–738, DOI [10.1215/00127094-3715913](https://doi.org/10.1215/00127094-3715913), introduction and its square-of-groups construction. A vertex stabilizer is an actual embedded \(BS(1,2)\). The dyadic subgroup above is consequently an infinite-index nonfree subgroup of Higman’s group, despite that group having no nontrivial finite quotients.
* **Baumslag–Gersten’s group.** The one-relator group \(\langle x,t\mid x^{x^t}=x^2\rangle\), with \(u^v=v^{-1}uv\), rewrites as
  \[
  \langle x,s,t\mid s^{-1}xs=x^2,\ t^{-1}xt=s\rangle.
  \]
  This is an HNN extension of \(B\) identifying the infinite cyclic subgroups \(\langle x\rangle\) and \(\langle s\rangle\). Both have infinite order (use the affine representation and height map), so Britton’s lemma embeds \(B\). Again \(A\cong\mathbb Z[1/2]\) is the required infinite-index nonfree subgroup. The original paper is Baumslag, [*A non-cyclic one-relator group all of whose finite quotients are cyclic*](https://doi.org/10.1017/S1446788700007783), *J. Austral. Math. Soc.* 10 (1969), 497–498. “All finite quotients cyclic” must not be confused with having no finite quotients.

These exclusions require the displayed subgroup embeddings. Merely mapping onto a group containing a bad subgroup would not suffice.

## 4. The finitely presented simple left-orderable examples also fail IF

Hyde–Lodha’s \(Q_n\), \(n\geq2\), are genuinely finitely presented torsion-free infinite simple groups. Nevertheless, [2302.04805v3](https://arxiv.org/html/2302.04805v3), proof of Proposition 3.4, explicitly puts the 1-periodic copy of \(F_{n(n+1)}'\) inside \(Q_n\).

Choose two disjoint subintervals \(I,J\subset(0,1)\) with suitable \(n(n+1)\)-adic endpoints. The rigid stabilizer of either interval contains a copy of \(F_{n(n+1)}\), so choose a nontrivial commutator supported in each interval. They lie in \(F_{n(n+1)}'\); their periodic extensions \(f,g\in Q_n\) have disjoint supports \(I+\mathbb Z,J+\mathbb Z\). They commute and generate \(\mathbb Z^2\): restricting \(f^ag^b=1\) to each support forces \(a=b=0\), because an orientation-preserving homeomorphism of the line has infinite order unless trivial.

The subgroup \(\langle f,g\rangle\) is proper because \(Q_n\) is nonabelian simple. Every proper subgroup of an infinite simple group has infinite index: otherwise its finite coset action would be faithful, embedding the whole infinite group in a finite symmetric group. Thus this is an infinite-index \(\mathbb Z^2\), contradicting IF. Simplicity and absence of finite quotients do not establish the required subgroup property.

## Outcome and precise remaining gap

No finite-presentation upgrade of the examined monster mechanisms survives the coherence or homology gates. Higman, Baumslag–Gersten, and the checked Hyde–Lodha family fail IF by explicit infinite-index nonfree subgroups. A putative finitely presented torsion-free simple group satisfying IF remains a possible counterexample mechanism, but none has been constructed here. Asserting its existence would transfer the central difficulty to an unsupported stronger claim. This route is therefore **blocked pending a materially new construction**, not a solution of 21.138.

Checkpoint 2026-10-24 17:03:48 UTC: complete local construction-gate audit; full-problem estimate remains **5%**. Mathematical deductions above are written for independent review. No publication, DOI, or external communication is warranted by this partial record.
