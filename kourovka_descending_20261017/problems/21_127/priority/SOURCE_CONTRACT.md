# Source contract — Kourovka 21.127

Prepared 2026-10-24 UTC for a future candidate. Audit/source preparation only; no independent original-solution effort begun.

Official source: https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf
Edition/update: 21st edition, official website advertises October 20, 2026 update.
Locator: printed p.198, problem 21.127; PDF page index 197.
Proposer: I. Soroko.
SHA-256: f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118

Exact mathematical target: for every right-angled Artin group \(G=A(\Gamma)\) and every \(g\in[G, G]\), is \(\operatorname{scl}_G(g)\in\mathbb Q\)? The source mentions Calegari’s free-group Rationality Theorem and directs the reader to 18.40 for the definition.

Definition source: same official PDF, printed p.129, problem 18.40; PDF page index 128. \(\operatorname{cl}_G(g)\) is the minimum number of commutators in a product representing \(g\), and
\[
\operatorname{scl}_G(g)=\lim_{n\to\infty}\frac{\operatorname{cl}_G(g^n)}{n}.
\]
The domain is the commutator subgroup, so the convention assigning infinity to elements outside rational homological boundaries is irrelevant here. The identity has value zero.

Graph scope: problem 21.127 itself does not explicitly say finite graph, and a Notebook-wide finite-RAAG convention was not located in the searched text. Do not add a restriction silently. It is immaterial for this elementwise question: if a word for g uses a finite set S of vertices, the full induced subgraph inclusion A(Γ[S])→A(Γ) has a retraction killing other generators. Both maps send g to itself. Commutator length cannot increase under a homomorphism, so for every n the two commutator lengths of g^n are equal. Retraction also places g in the smaller commutator subgroup. Hence its scl is equal in the two groups. This is an elementary scope check, not original progress on rationality.

A positive solution must prove this assertion for arbitrary finite defining graphs and arbitrary commutator-subgroup elements. A negative solution must exhibit such a group/element with a rigorously irrational value. An exact algorithm is stronger additional information; a spectral gap, rational values of selected chains, complexity lower bound, or approximation algorithm alone does not answer the question.
