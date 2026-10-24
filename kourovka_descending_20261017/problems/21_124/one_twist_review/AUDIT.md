# Independent adversarial review: one-twist cubulation

Review UTC: 2026-10-24 22:35. Reviewer: `/root/p21124_one_twist_adversary`, which did not author the candidate proof. Review completion: **100%**. Estimated completion of full Kourovka 21.124 remains **3%**, following the candidate's estimate; this audit does not establish a resolution of either part.

**Verdict: PASS for the explicitly restricted supporting lemma.** No substantive mathematical objection remains to the reviewed hash. The conclusions are a compact NPC square-complex model for the specified one-twist groups, an index-two subgroup with a compact NPC VH model, and the stated free-by-cyclic envelope and retraction. Neither virtual specialness nor originality is certified.

Reviewed proof SHA256:

`6bc52038fe8e168a3d88ca6b7d9d8f883c0394ab276b892ebf2e1ecd9816b00a`

Reviewed author script SHA256:

`59078a09566c4ad844e626dc70d0cf5b7478bd998467a390ef76d1abd6b2902d`

The reviewed artifacts are `positive_hierarchy/ONE_TWIST_CUBULATION.md`, `check_one_twist.py`, and `one_twist_certificate.json`. No author file was changed in this review.

## Exact statement and boundary conditions

The group is

\[
 G(w)=\langle F(a_1,\ldots,a_r),t,c\mid [t,a_i]=1,
 c^{-1}tc=tw\rangle,
\]

where the **fixed** free factor has finite rank \(r\geq1\). The proof assumes \(w\) has nonzero image in \(F^{ab}\). The case \(w=1\) is separately a RAAG. No conclusion is asserted for nontrivial \(w\in[F,F]\), for which the proposed positive integer \(k\) would be zero. There is no hidden primitivity or non-proper-power hypothesis on \(w\).

The mapping-torus convention is correct: the relation implies \(tct^{-1}=cw\), because \(t\) commutes with \(w\). A cyclic conjugation \(w'=v^{-1}wv\) can be undone by applying the inner automorphism \(g\mapsto vgv^{-1}\) to the free vertex factor and fixing \(t,c\). Thus reducing to a cyclically reduced nonempty representative does not alter the abstract problem.

## Finite-index vertex marking and the actual group of the complex

Set \(k=\gcd(e_1(w),\ldots,e_r(w))>0\) and choose an integral character \(\chi\) with \(\chi(w)=k\). In \(A=F\times\langle z\rangle\), write pairs as \((g,n)\). The proposed map is

\[
 i(g,t^m)=(g,km-\chi(g)).
\]

Projection to \(F\), followed by the central coordinate, proves injectivity. Its image is exactly

\[
 B=\{(g,n): n+\chi(g)\equiv0\pmod{k}\}.
\]

Indeed any such pair is \((g,-\chi(g))(1,k)^{(n+\chi(g))/k}\). The quotient map to \(\mathbb Z/k\) is surjective on \(z\), so the index is exactly \(k\), including \(k=1\).

The two edge groups in the ambient HNN extension are entirely contained in \(B\):

\[
 i(t)=z^k,\qquad i(tw)=z^k w(a_i z^{-\chi_i})=w(a_i).
\]

Consequently their full inverse images under \(i\) are exactly \(\langle t\rangle\) and \(\langle tw\rangle\). A reduced HNN word over the original vertex group cannot gain an ambient pinch. Britton's normal-form lemma therefore applies in the claimed direction. There is no unsupported assertion that an arbitrary HNN map induced by a vertex injection is injective.

More importantly, the direct model \(Y_w\) itself has the right group. Its vertex space has group \(B\), and its selected annulus imposes \(c^{-1}z^k c=w(a)\). Under the displayed isomorphism from \(F\times\langle t\rangle\) to \(B\), this is exactly the original relation. This verifies both injectivity and surjectivity of the presentation marking onto \(\pi_1(Y_w)\). The proof does not infer cocompact CAT(0) geometry from an arbitrary subgroup of a CAT(0) group.

## Cubical geometry, including wrap corners

Give each basis circle of the rose \(k\) unit edges and the central circle \(L=|w|\) unit edges. Both attaching paths then have length \(kL\). The central path traverses its circle \(k\) times; the free path traverses the cyclically reduced word with each letter subdivided into \(k\) edges. Both maps are combinatorial local isometries: their incoming and outgoing directions are distinct and lie in one factor of the product link.

At each old vertex the link is complete bipartite. Every oriented transversal annulus-edge direction adds a new link vertex adjacent only to the two old directions at the corresponding boundary position. These two neighbours are distinct and lie in the same part of the old link. There are no edges between new link vertices. It follows directly that no link loop, double edge, or triangle is introduced. This argument includes the wrap from the last square back to the first, negative letters, repeated visits to an old vertex, proper powers, and a transversal edge whose endpoints coincide. In the latter case its two oriented germs are separate link vertices. A unit circle and a one-square annulus are legitimate cubical CW complexes under the usual definition.

The finite cover of the vertex product has precisely the same local links. Its two selected attaching loops close because their elements are in \(B\); no claim about arbitrary other vertex covers is needed. Attaching that one annulus repeats the preceding link argument. Compactness follows from the finite vertex cover and finitely many annulus squares.

The natural map \(Y_w\to X_k\) has injective links. Old links are mapped isomorphically by the vertex covering. If a selected transversal direction is present, its two incident corners are both present. Every other ambient corner involving only old directions is already supplied by the product squares. Thus the link image is full. The local-isometry assertion, as well as the separate Britton injection, is valid.

## The parity cover really is VH

Sending \(c\) to \(1\in\mathbb Z/2\) and the vertex group to zero respects the relations and is surjective. The corresponding connected cover therefore has degree exactly two. Each annulus runs between its central boundary in one vertex copy and its free boundary in the other.

In copy zero, free edges are horizontal and central edges vertical; in copy one, those assignments are reversed. The transversal edges of the annulus leaving copy zero are horizontal, and those leaving copy one vertical. Both boundary paths of a given annulus consequently have the same color, opposite to its transversal edges. All squares alternate colors. Covers preserve the already verified links and NPC property.

This proves a VH model, not a clean or special model. It supplies no finite-cover argument eliminating the remaining hyperplane pathologies.

## Independent presentation check of the free fiber and retraction

The free-by-cyclic computation can be checked without relying solely on the Bass–Serre rank count. Take a free group on \(x_i,C_0,\ldots,C_{k-1}\) and the automorphism

\[
 x_i\mapsto x_i,\quad C_j\mapsto C_{j+1}\ (j<k-1),\quad
 C_{k-1}\mapsto C_0w(x).
\]

An explicit inverse sends \(C_0\) to \(C_{k-1}w(x)^{-1}\), sends \(C_j\) to \(C_{j-1}\) for \(j>0\), and fixes the \(x_i\). Form its semidirect product with generator \(z\). Set \(a_i=x_i z^{\chi_i}\), \(c=C_0\). Then \([z,a_i]=1\), \(w(a)=w(x)z^k\), and

\[
 c^{-1}z^k c=w(x)z^k=w(a).
\]

These assignments give inverse presentation maps to the claimed \(H_k\), using \(x_i=a_i z^{-\chi_i}\) and \(C_j=z^j c z^{-j}\) in the reverse direction. Thus its fiber is actually free of rank \(r+k\), not just a group with the same Euler characteristic. Its height character is the stated \(\eta\).

The \(k\)-th power of this automorphism fixes each \(x_i\) and sends **every** \(C_j\) to \(C_jw(x)\). On the index-\(k\) subgroup with stable generator \(u=z^k\), identifying all \(C_j\) with \(C_0\) commutes with the monodromy and gives the stated retraction. Replacing the other free generators by \(D_j=C_jC_0^{-1}\) is a Nielsen basis change, and each \(D_j\) is fixed. This is a claim only about this explicit envelope; it proves no preservation theorem for arbitrary free-by-cyclic envelopes.

## Reproducibility and the extent of the tests

The author script was rerun from a temporary copy, with the original proof and certificate untouched. All fields other than the timestamp reproduce exactly: **370 cases**, including all qualifying rank-two cyclically reduced words of length at most five. See `author_rerun.json`.

The separate `independent_check.py` does not import the author script. It directly constructs the voltage product cover and its selected annulus, then directly constructs the two-copy parity model. It checks every vertex link, connectedness, Euler characteristic, fullness and injectivity of the local-isometry links, square colors, and exact free-word monodromy inverse/power/retraction formulas. It reproduces all author cell counts and checks **282 further cases**, for **652 total**, across fixed ranks one through six and gcd values through twelve. Extra tests include negative words, proper powers, higher ranks, and four nondefault character choices satisfying \(\chi(w)=k\). See `independent_results.json`.

These finite checks support implementation reproducibility; the general arguments above carry the quantifiers. No computation tests virtual specialness, and none is described as doing so.

## Primary-source and priority scope

[Haglund–Wise, *Special cube complexes*](https://www.imo.universite-paris-saclay.fr/~frederic.haglund/special%28corrected%29.pdf), Definitions 2.1 and 2.9 and Lemma 2.11, use the flag-link condition and full-link formulation of local isometry employed here. Their Section 5 requires extra cleanliness hypotheses for its VH specialness conclusions; the present proof has not verified those hypotheses. This supports the strict separation of NPC/VH from specialness.

[Delage, arXiv:2602.08759v3](https://arxiv.org/html/2602.08759v3), Theorem 1.2(1) and Proposition 3.1, proves the prior CAT(0) assertion when the fixed free factor has rank two and the twisting word has nonzero abelianization. The candidate's acknowledgement of this prior result and of the corrected Samuelson statement is accurate. This review does not perform a comprehensive priority audit of explicit cubulations in arbitrary rank and makes no novelty claim.

## Scope of acceptance and remaining gap

Accept this as a reviewed supporting deduction for the stated family. Do not mark Kourovka 21.124 as solved, solved_verified, or published on its strength. The proof establishes no RAAG embedding for a finite-index subgroup in the generic nonprimitive case, no general special-combination theorem, and no general CAT(0)-preserving envelope result. A hypothetical vertex-cover cleanup of the word \(w\) must still satisfy all HNN covering compatibility conditions; this audit does not supply such an extension.

No independent human peer review or formal proof certification has occurred.
