# Independent finite-quotient scope audit

**Verdict: pass.** `../root_structure/FINITE_QUOTIENT_SCOPE.md` correctly separates the current whole-group profinite theorem from Kourovka21.129. This is a source/scope check, not a reproof of the finite-group classifications or a novelty claim.

The actual [arXiv2609.27171v2 abstract/version record](https://arxiv.org/abs/2609.27171v2) gives first submission23September2026 and revision16October2026. [TheoremC](https://arxiv.org/html/2609.27171v2) states that isomorphic profinite completions of two irreducible spherical Artin groups force the groups to be isomorphic. Section11 proves that statement by whole-group finite-quotient and cohomological data. It does not assume quasi-isometry, virtual isomorphism, or isomorphic open subgroups, and supplies no implication from those conditions to its hypothesis.

The cached v2 PDF hash independently matches the source manifest:

`625f2c4038631751bfefeb421a20e013e45104e88624c7c4937db2488861cce8` (867013bytes).

Exact audited file hashes and timestamp are in `FINITE_QUOTIENT_AUDIT_MANIFEST.json`.

The explicit barrier works for **all n≥2**, including n=2. In an Artin relation of odd length2r+1, abelianization equates its two endpoint generators; an even length2r relation has identical exponent sums on both sides and gives no relation. Therefore the abelianization is free abelian on components of the odd-edge subgraph. For A_n that graph is connected; for B_n its unique4-edge separates it into two components. Consequently

\[
A[A_n]^{ab}=\mathbb Z,\qquad A[B_n]^{ab}=\mathbb Z^2.
\]

The B_n group surjects onto \((\mathbb Z/2)^2\) by reducing its two independent exponent coordinates modulo2. No map from A_n onto that group can be surjective, since every map to an abelian group factors through its cyclic abelianization. These are different whole-group finite-quotient sets. Yet [Cumplido–Paris Theorem2.4(1)](https://ems.press/content/serial-article-files/39000?nt=1) makes the pair abstractly commensurable, hence quasi-isometric. Thus equality of the whole finite-quotient sets is neither a necessary consequence of quasi-isometry nor a necessary condition for abstract commensurability in the target class.

There is no low-rank omission: B1 is outside the displayed n≥2 statement; rank2 is exactly the A2/B2 example. This barrier does not challenge TheoremC, because its stronger hypothesis fails on the A/B pair.

Abstractly commensurable groups do give isomorphic open subgroups of their profinite completions, by completing the common finite-index subgroups. The converse inference to discrete commensurability requires an additional rigidity theorem; TheoremC cannot simply be applied to those finite-index subgroups because they need not themselves be irreducible spherical Artin groups. No such bridge is proved in the audited source note or cited theorem. The four residual quasi-isometry implications therefore remain unchanged.
