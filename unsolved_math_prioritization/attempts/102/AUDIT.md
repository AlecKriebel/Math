# GREEN-012 / ID102: independent proof, source, and computation audit

Audit date: 10 October 2026.

## Decision and exact scope

**Accepted as a computer-assisted partial result. No mathematical correction is required. The unrestricted problem is not resolved.**

The audited manuscript proves the exact inequality
\[
T_G(A)\geq \alpha^{15}|G|^{10}
\]
for every finite abelian group and subset of density \(\alpha\geq20/23\). Its stronger, exact scalar criterion \(F((1-\alpha)/\alpha)\leq5\), subject to the stated \(0<\alpha<1\) and \((1-\alpha)/\alpha\leq1\), is also valid. The approximate density endpoint \(0.86946194679\) is descriptive, not a separately certified universal decimal cutoff.

The coset and complement-of-coset cases, quotient/product closure, and exhaustive finite result for all abelian groups of order at most 16 are accepted. No full-target solution, global literature-status assertion, or novelty-priority assertion is made.

The inspected proof is 12,452 bytes, SHA-256 `41b3304c35a5b5e371f3e9abe7735564d639ce6f5965f30f88d9f0218a940dde`. The four-file public candidate and its underlying validation files were authenticated against the 4,917-byte author inventory with SHA-256 `9ead37bb8b154b1342499a25d458543bbb428b3ef1c23f4ef634cfc584f7987d`. All 23 inventoried files matched and the file set was exact. The audit did not change those files.

A separate typesetting-only patch repairs malformed inline mathematical delimiters in the proof and result summary. It changes no mathematical text, displayed equation, scope, or conclusion. The acceptance above concerns the mathematical contents of the pinned original, with that presentation issue explicitly recorded.

## 1. Target and source authentication

The target has five left and five right labeled vertices. The edge condition is \((j-i)\bmod5\in\{0,1,2\}\), giving 15 distinct edges. All ten tuple coordinates are ordered and may coincide. The count is exact at every finite group order; there is no asymptotic term, prime-order assumption, cyclic-group restriction, Fourier-uniformity assumption, or injectivity requirement.

The original 23-file source inventory matched the prescribed SHA-256 `87dd9dca3e167ab01f7c8dd5ba22ffeaaed72553860f654443dc9a48e6e5e0e3`. All its individual byte counts and hashes were independently checked.

- [Ben Green, *100 Open Problems*, page 9](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf): the complete retained PDF was authenticated, the relevant text read, and the page image independently viewed. Problem 12 supplies the finite-abelian tuple question and graph description. The inspected PDF does not explicitly print the modulo-5 convention. PDF: 839,479 bytes; SHA-256 `e06971245914947f152550dee59bbb29fe0e798f0c51b2bc2557f824c2f9a44a`.
- [Lean community discussion, 6 February 2026](https://leanprover-community.github.io/archive/stream/252551-graph-theory/topic/Sidorenko%27s.20Conjecture.20and.20Green%27s.20Open.20Problem.2012.html): independently opened during this audit. Kevin Buzzard's public report supplies Green's modulo-5 clarification. This is a publicly reported author clarification, not independently held private correspondence or an amended-PDF claim.
- [László Lovász, *Subgraph densities in signed graphons and the local Sidorenko conjecture*, Lemma 2.3](https://arxiv.org/abs/1004.3026): the source identity and retained complete PDF were checked; the relevant lemma was read. It states the variable-overlap version of Cauchy–Schwarz cited by the manuscript. The manuscript proves its needed three-factor case directly, so no stronger result from that paper is an unproved dependency. PDF: 213,905 bytes; SHA-256 `1b58de48cb8a3365016bb1eb16073c770c29bae5ffd48429e14ec61df923143b`.
- [Deng, Tidor, and Zhao, *Uniform sets with few progressions via colourings*](https://doi.org/10.1017/S0305004125000106): the complete retained published PDF was authenticated and its first two pages read. The subject is Fourier-uniform arithmetic-progression counts. On Green's page 9, the relevant discussion is visibly under Problem 13, not Problem 12. It gives no negative solution of the present target. PDF: 292,100 bytes; SHA-256 `ebae91fe58aadece6bcd55c9ca32631be4959b21c7dd993051116086b5852829`.

No source contents or dataset contents accompany this public audit.

## 2. Analytic proof audit

### Arbitrary finite abelian groups and complex characters

All expectations are normalized. For real \(g=1_A-\alpha\), write \(\widehat g(\chi)=\mathbb E_xg(x)\overline{\chi(x)}\) and \(q_\chi=|\widehat g(\chi)|^2\). Reality gives \(q_{\bar\chi}=q_\chi\), without requiring real characters or a symmetric subset. The trivial coefficient is zero, Parseval gives \(S=\alpha(1-\alpha)\), and the complement indicator gives \(q_\chi\leq(1-\alpha)^2\).

For the normalized operator with symmetric real kernel \(U(x,y)=g(x+y)\),
\[
U\chi=\widehat g(\bar\chi)\bar\chi,\qquad U^2\chi=q_\chi\chi.
\]
Consequently \(t(C_{2k},U)=\operatorname{tr}(U^{2k})=\sum_\chi q_\chi^k\). This validates the normalization and handles complex characters and every finite abelian group, including those with 2-torsion.

With \(E=\sum q_\chi^2\), Cauchy–Schwarz gives \(M_6S\geq E^2\), and the coefficient bound gives \(E\leq(1-\alpha)^2S\). These are universal exact inequalities.

For \(C(x,x')=\mathbb E_yU(x,y)U(x',y)\), the Fourier coefficients are the nonnegative \(q_\chi\). Therefore
\[
L=\mathbb E C^3=\sum_{\chi\psi\omega=1}q_\chi q_\psi q_\omega\geq0.
\]
The pointwise bound \(|C|\leq S\) implies \(L\leq SE\). Since a nonzero summand requires \(\chi\psi\ne1\), replacing its third coefficient by \(\beta^2\) gives
\[
L\leq\beta^2\sum_{\chi\psi\ne1}q_\chi q_\psi
=\beta^2(S^2-E),\qquad\beta=1-\alpha.
\]
The subtraction of \(E\), and not some different diagonal quantity, is correct because \(q_{\bar\chi}=q_\chi\).

### Graph estimates

For the three selected same-side stars, integrate their centers first. No remaining variable appears in all three functions. After bounding other edges by \(\alpha\), apply the three-factor Cauchy–Schwarz inequality to the absolute values of the star functions. Degree-2 and degree-3 star norms squared are respectively \(E\) and \(L\). This proves the manuscript's bound for each certified degree sum \(D\); no independence between shared variables is incorrectly assumed.

For the seven-edge graph formed by two squares sharing an edge,
\[
t(\Theta_{1,3,3},U)=\mathbb E_{u,v}U(u,v)(U^3(u,v))^2
\geq-\alpha M_6.
\]
Here \(\mathbb E(U^3)^2=\operatorname{tr}(U^6)\), using symmetry. Both the edge exponent and sign are correct.

Every reflection witness partitions the active vertices into exchanged sets and fixed vertices, has no edges across the exchanged sets or within the fixed set, and pairs the remaining factors by an involutory graph automorphism. Conditioning on fixed labels therefore produces a square. This argument remains valid when the automorphism exchanges the graph's original bipartition, since the kernel is symmetric.

### Expansion coefficients and optimization

The expansion has one term per edge subset, with coefficient \(\alpha^{15-e}\). Degree-1 terms vanish. The five theta terms consume only \(5\alpha^9M_6\) of the positive \(15\alpha^9M_6\). The remaining cycle and disjoint-square contributions give precisely
\[
\frac{T_G(A)}{\alpha^{15}N^{10}}
\geq1+z^2\bigl[5-zD(s)+(5+10/r)z^2\bigr].
\]
There is no missing multiplicity or power of \(N\) or \(\alpha\).

For \(r=\beta/\alpha\), \(z=\sqrt E/\alpha^2\), and \(s=L/(\alpha^2E)\), the valid domain is
\[
0<z\leq r^{3/2},\qquad0\leq s\leq\min\{r,r^4/z^2-r^2\}.
\]
For \(0<r\leq1\), the two branches meet at \(z_*=r^{3/2}/\sqrt{1+r}\). The first lower-bound branch decreases because its derivative is at most \(-140\sqrt r-180r-111r^{3/2}\). On the second branch each \(zs^{k/2}\), \(k=1,2,3\), is nonincreasing, while the positive quadratic term increases. The global lower bound is thus \(5-F(r)\) at the joining point. All radicals have nonnegative arguments on the stated domain.

The displayed factorization of \(F\) has positive increasing factors for \(r>0\); its bracket has positive derivative. Also \(F(0+)=0\) and \(F(r)\to\infty\). Thus its positive root at height 5 exists and is unique. Independent high-precision evaluation agrees with the quoted approximation; the accepted exact claims remain the scalar criterion and rational endpoint.

At \(r=3/20\), the independently checked rational radical bounds give
\[
F(3/20)<\frac{19693179}{3946064}
=5-\frac{37141}{3946064}<5.
\]
Monotonicity proves the whole range \(\alpha\geq20/23\). The proof separately handles \(\alpha=1\). When \(E=0\), Fourier inversion gives \(g=0\), so dividing by \(E\) is never used improperly.

## 3. Load-bearing finite classification

A separately written checker reconstructed the graph from the modular membership rule, checked all 32,768 subsets, and independently validated every supplied witness. It imported no author checking code. Exact coverage has 624 nonempty edge subsets without degree-1 vertices:

| Assigned class | Count |
|---|---:|
| Single cycles of lengths 4, 6, 8, 10 | 5, 15, 25, 8 |
| Disjoint cycles of lengths (4,4), (4,6) | 5, 5 |
| Two squares sharing an edge | 5 |
| Reflection squares | 95 |
| Three stars of degree sums 7, 8, 9 | 160, 180, 121 |

The assignments are disjoint as certificate rows, even where a graph could admit more than one kind of useful witness. Every row occurs exactly once; no leaf-free subset is omitted. The independent theta test used the union of two induced four-cycles sharing one edge. Every reflection's involution, active-vertex partition, edge pairing, and forbidden-edge conditions were checked. Every star triple's bipartition, distinctness, degrees, overlap multiplicity, and degree sum were checked.

**This classification is a substantive computer-assisted dependency of the high-density theorem.** The analytic argument alone is not being represented as a hand classification of all cases. Code and witness contents are excluded from the present publication scope; publishing only prose and hashes does not make those materials publicly reproducible. This audit records local independent verification, rather than claiming that the restricted public packet contains a standalone machine-checkable proof.

Both the author verifier and independent structural verifier accepted the valid certificate in ordinary Python, `-O`, and `-OO`. The original nine corruption tests were independently rerun in all three modes, giving 27 rejections. Thirteen independently designed corruptions were rejected in all three modes, giving another 39 rejections. These controls check missing/extra/duplicate rows, graph changes, bad stars, bad reflections, false graph classes, and altered polynomial data. The mathematical justification is the exhaustive witness verification; the corruption tests are additional checker controls.

## 4. Special cases and exact finite counting

The quotient statement has exactly \(|\ker\pi|^{10}\) lifts per quotient tuple, and direct products multiply both normalized counts and densities. For a subgroup coset the connected graph forces one free quotient label, yielding normalized density \(\alpha^9\). For its complement, replacing right quotient labels by their complements to the coset representative turns the constraints into proper colorings.

The chromatic polynomial was independently recomputed by inclusion–exclusion over all edge subsets. Its ascending coefficients are
\[
(0,-573,2175,-3710,3825,-2663,1305,-450,105,-15,1).
\]
The positive coefficient list for \(q^5P_H(q)-(q-1)^{15}\) after \(q=u+2\) was independently checked exactly. Direct enumeration of proper 2- and 3-colorings also gave 2 and 306, matching the polynomial. Consequently the complement-coset conclusion holds for every integer index \(q\geq2\); \(q=1\) is the empty set.

A separate enumerator generated all invariant-factor chains of product at most 16, obtaining exactly 25 abelian isomorphism types. It checked **all 398,350 subsets directly, without translation-orbit pruning**, and compared \(T_G(A)N^5\) with \(|A|^{15}\) in 128-bit integer arithmetic. It rooted a left coordinate and independently counted right-coordinate choices. No violation occurred. Every cardinality minimum and its first minimizing bit mask agreed with the author's retained results.

Additional finite controls:

- Literal enumeration of all ten coordinates agreed in all 46 subset cases over the groups of order at most 4.
- An independent Burnside calculation gave 26,300 subset-translation orbits, agreeing with the author's optimized coverage.
- Recompiling and rerunning the author's complete enumerator reproduced its output byte for byte.
- The author's unsigned-64-bit comparison is safe: both sides and all nonnegative partial sums are bounded by \(16^{15}=2^{60}\). The independent code used a wider comparison type anyway.
- An undefined-behavior-sanitized independent run through order 8 matched the corresponding full-run output.
- Independent exact rational checks of the moment inequalities passed in 2,191 cases. Complex-character and normalized-operator identities were also numerically cross-checked in those cases, including 1,701 with a genuinely nonreal Fourier coefficient; the maximum residual was below \(4\times10^{-16}\). These floating-point identities are controls only, not premises of the universal proof.

The finite enumeration establishes its stated bounded-order special case. It supplies no inference from order 16 to arbitrary order. The universal high-density argument instead rests on the exact analytic bounds and finite graph classification audited above.

## 5. Remaining boundary

The general low-density, arbitrary-subset problem remains untreated by this result. The reported modulo-5 clarification must stay qualified, and the adjacent Problem 13 discussion must not be repurposed as a resolution of Problem 12. Subject to those limits and the acknowledged computer-assisted dependency, the audited mathematical claims are accepted.
