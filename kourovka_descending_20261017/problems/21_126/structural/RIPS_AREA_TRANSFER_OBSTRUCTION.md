# Why quotient area and fibre-product conjugacy do not transfer to intrinsic area

Prepared October 24, 2026 UTC. This is a rigorously justified obstruction to a tempting positive route, not a result resolving 21.126.

## A countermodel to an unrestricted transfer inequality

There are groups Q of type F3 with undecidable word problem. Bridson2013, *On the subgroups of right-angled Artin groups and mapping class groups*, proof of Theorem3.4, explicitly invokes the Collins–Miller examples with these properties. His Theorems3.1 and3.2 state the 1–2–3 theorem and virtually special Rips construction. They give an extension

1→N→G→Q→1,

where G is virtually special hyperbolic, N is finitely generated, and the symmetric fibre product P≤G×G is finitely presented. Intersecting with a finite-index RAAG-embeddable subgroup of G×G gives a finitely presented finite-index subgroup P_0 of P embedded in a RAAG.

The word problem in P is decidable: substitute words into the two G coordinates and use the hyperbolic word problem. The same is true for P_0, or follows directly from its RAAG embedding. Thus δ_P and δ_{P_0} have recursive upper bounds. This standard equivalence follows by enumerating the finitely many words of length ≤n, deciding which are null, and searching in parallel for diagrams for those null words. Conversely, a recursive Dehn upper bound decides the word problem by finite enumeration of diagrams of bounded area and boundary length (equivalently the bounded-noise lemma).

But δ_Q has no recursive upper bound, because Q has undecidable word problem. Therefore **no general inequality δ_Q≼δ_P** can hold for all such fibre products. Otherwise the coarse constants could be fixed for this example, and the recursive upper bound for δ_P would give a recursive upper bound for δ_Q, a contradiction. This remains a contradiction even though the inequality need not be uniform in Q.

The issue is intrinsic area, not finite presentability or embedding: both P and its finite-index RAAG subgroup are finitely presented. The Rips kernel N is merely finitely generated. One cannot replace it by a finite presentation without proof.

## Scope of the recent quantitative theorem

The cached current primary version is Bridson, *Conjugacy in fibre products, distortion, and the geometry of cyclic subgroups*, [arXiv2507.17598v2](https://arxiv.org/abs/2507.17598v2), dated July10,2026. Printed pp2–3 explicitly state:

- TheoremB: δ_Q≼CL_P≼CL_P^{G×G}≼δ_Q^c under the stated torsion-free hyperbolic hypotheses, with further cyclic-control comparisons.
- TheoremE: Dist_P^{G×G}≃δ_Q for a fibre product of a hyperbolic group over Q.
- TheoremF: very large conjugator length functions can be realized by finitely presented subgroups of virtually special products.

Here CL is a **conjugator length function**, Dist is **extrinsic subgroup distortion**, and δ_Q^c is the **rel-cyclics Dehn function of the quotient**. None of these symbols denotes δ_P. TheoremE therefore makes the countermodel sharper: P can have non-recursively bounded ambient distortion while its intrinsic Dehn function is recursively bounded. TheoremB similarly allows nonrecursive conjugator length. An undecidable conjugacy problem in a finitely presented RAAG subgroup is compatible with its decidable word problem and recursive intrinsic Dehn function.

No inference from a recursive word-problem algorithm to a polynomial or exponential intrinsic Dehn upper bound is made here. Recursiveness is enough to falsify the unrestricted transfer, but does not settle either growth branch of 21.126. Likewise this does not rule out a carefully proved transfer theorem with additional hypotheses and explicit hard null words. It identifies what such a new theorem must actually control.

## Exact unresolved step for a positive fibre-product construction

One needs explicit short null words in a finitely presented RAAG subgroup P and a certificate that **every intrinsic filling** has super-exponential area, or a matched superpolynomial subexponential lower/upper pair. The quotient-area, distortion, and conjugacy statements above do not supply these intrinsic null-word certificates. Merely assigning a quotient Q with very large Dehn function transfers the central unproved step to an invalid unrestricted inequality.
