# An explicit even-strand Markov formulation

**Complete candidate for the literal source question, pending independent review.** The result below gives a finite list of algebraic move schemes for ordinary closures of even-strand classical braids, and a second list for ordinary closures of even-strand virtual braids. It is an elementary consequence of the established Markov theorems. Historical novelty, a minimal list, and a stronger bounded-support locality property are not claimed.

## 1. Exact scope

Problem42 on p.34 of [Fenn–Ilyutko–Kauffman–Manturov, arXiv1409.2823](https://arxiv.org/abs/1409.2823) asks whether Markov's theorem can be reformulated so that only braids with an even number of strands participate. It imposes no additional locality or minimality condition. The same item occurs on p.37 of the [published survey](https://www.impan.pl/shop/publication/transaction/download/product/86155).

We retain **ordinary braid closure**, not plat closure. The links are unframed and oriented, as in the classical and virtual Markov theorems used below. This is not a transverse or framed Markov theorem. The survey includes both classical and virtual problems and does not qualify “braids” in this item; both versions are therefore supplied.

The allowed states and every endpoint of every replacement are even-strand braids. Moves are given by explicit word patterns, not by a rule that permits an unspecified path through odd-strand braids. Odd-strand braids appear only in the proof that the finite list is complete, as auxiliary objects in the already established unrestricted Markov theorem.

## 2. Word conventions and the even-only move list

A state is a tagged pair \((N,w)\), where N is even, \(N\ge2\), and w is a braid word on N strands. The tag matters: the same empty word on two and four strands has different ordinary closures.

Write \(\sigma_i^{\pm1}\) for classical generators and \(v_i\) for virtual generators, with \(v_i^{-1}=v_i\). Define \(W_N(k)\) to mean words in the alphabet with indices \(1\le i\le k\), regarded throughout as words on the stated **even** number N of strands. The empty word is allowed, including when \(k=0\). In the classical version, omit all v's. Thus the support restrictions below are syntactic restrictions on words in an even-strand group; they do not create odd-strand objects in the move category.

For a word a, \(s(a)\) increases every generator index by one and preserves generator types and signs. Concatenation is multiplication, and inverses reverse the word and invert each letter. For virtual words set
\(G_i=\{\sigma_i,\sigma_i^{-1},v_i\}\); for classical words set
\(G_i=\{\sigma_i,\sigma_i^{-1}\}\).

All arrows below are reversible. Ordinary braid relations in the appropriate even-strand group are always allowed, without changing N.

### C. Conjugation at an even level

For \(a,b\in W_N(N-1)\),

\[
(N,b)\ \longleftrightarrow\ (N,aba^{-1}).
\tag{C}
\]

### BC. Conjugation with a terminal positive crossing retained

For \(a,b\in W_N(N-2)\),

\[
(N,b\sigma_{N-1})\ \longleftrightarrow\
(N,aba^{-1}\sigma_{N-1}).
\tag{BC}
\]

### T. Replacement of a terminal stabilizing crossing

For \(b\in W_N(N-2)\) and \(g\in G_{N-1}\),

\[
(N,b\sigma_{N-1})\ \longleftrightarrow\ (N,bg).
\tag{T}
\]

The choice \(g=\sigma_{N-1}\) is the identity and may be omitted.

### D. Two-strand stabilization

For \(b\in W_N(N-1)\) and \(g\in G_N\),

\[
(N,b)\ \longleftrightarrow\
(N+2,bg\sigma_{N+1}).
\tag{D}
\]

The old word b is put on the first N of the N+2 strands, so the operation adds two strands at once. There is no allowed N+1-strand state in this replacement.

**The classical list ends here.** The virtual list additionally contains the following four exchange patterns; dropping them is not justified by the classical theorem.

### R and L. Right and left virtual exchange at an even level

For \(a,b\in W_N(N-2)\),

\[
(N,a\sigma_{N-1}^{-1}b\sigma_{N-1})
\ \longleftrightarrow\
(N,av_{N-1}bv_{N-1}),
\tag{R}
\]

\[
(N,s(a)\sigma_1^{-1}s(b)\sigma_1)
\ \longleftrightarrow\
(N,s(a)v_1s(b)v_1).
\tag{L}
\]

### BR and BL. Virtual exchange with a terminal positive crossing retained

For even \(N\ge4\) and \(a,b\in W_N(N-3)\),

\[
(N,a\sigma_{N-2}^{-1}b\sigma_{N-2}\sigma_{N-1})
\ \longleftrightarrow\
(N,av_{N-2}bv_{N-2}\sigma_{N-1}),
\tag{BR}
\]

\[
(N,s(a)\sigma_1^{-1}s(b)\sigma_1\sigma_{N-1})
\ \longleftrightarrow\
(N,s(a)v_1s(b)v_1\sigma_{N-1}).
\tag{BL}
\]

Every displayed index lies between1 and N-1 at an N-strand endpoint. In particular, the shifted blocks in BL have indices at most N-2; the last crossing has index N-1.

This is a finite list of **four classical or eight virtual algebraic schemes**, besides the standard finite families of braid relations. Word parameters are arbitrary finite blocks, as in the ordinary conjugation/exchange formulation. If desired, a in C and BC can be restricted to one generator or its inverse: successive conjugations generate the version with an arbitrary a. No bound on block length is asserted, and no unproved equivalence test is used as a move-applicability condition.

## 3. The two even-strand theorems

**Classical theorem.** Every nonempty oriented classical link is the ordinary closure of an even-strand classical braid. Two such braids have isotopic oriented closures if and only if they are connected by braid relations at even levels and a finite sequence of C, BC, T and D, using only classical generators.

**Virtual theorem.** Every nonempty oriented virtual link is the ordinary closure of an even-strand virtual braid. Two such braids have equivalent oriented virtual closures if and only if they are connected by virtual braid relations at even levels and a finite sequence of C, BC, T, D, R, L, BR and BL.

The empty link may be included separately as the isolated zero-strand empty state. No positive-strand ordinary closure is empty, so this convention creates no further moves.

## 4. Established unrestricted input

The classical Alexander and Markov theorems give braid representatives and say that ordinary closure equivalence is generated by braid relations, conjugation at a fixed strand count, and right stabilizations
\((m,b)\leftrightarrow(m+1,b\sigma_m^{\pm1})\).

For virtual braids we use [Kamada, Theorem3.2](https://arxiv.org/abs/math/0008092), together with his Proposition3.1. His moves are braid relations, conjugation, right stabilization by \(\sigma_m\), \(\sigma_m^{-1}\) or \(v_m\), and **both** right and left virtual exchanges. Their algebraic forms are also stated explicitly in [Kauffman–Lambropoulou, Section5](https://arxiv.org/abs/math/0507035): at strand count m+1 they are

\[
a\sigma_m^{-1}b\sigma_m\leftrightarrow av_mbv_m,
\quad
s(a)\sigma_1^{-1}s(b)\sigma_1\leftrightarrow s(a)v_1s(b)v_1,
\tag{15}
\]

where the blocks use indices at most m-1. These are established theorems, not conclusions of this note. In particular, virtual exchange moves must not be discarded merely because their classical analogues follow from ordinary Markov moves.

## 5. Soundness: every listed move preserves the ordinary closure

C is conjugation. In BC, each endpoint has the same oriented closure as the word preceding its terminal crossing, and those preceding words are conjugate. In T, every permitted terminal crossing is a right stabilization of the same preceding word. In D, the closure is unchanged by two consecutive stabilizations, the second chosen positive.

R and L are precisely the established virtual exchanges (15). In BR and BL, the two words preceding the final positive crossing are related by a virtual exchange; applying the same positive stabilization at both ends therefore gives equivalent closures.

This verifies each algebraic pattern without assuming the completeness conclusion. The references to lower strand counts in this *verification* are not allowed intermediate states: the move relation itself was explicitly and independently defined in Section2 by the displayed even-endpoint substitutions. A proof may use the older unrestricted theorem without putting its auxiliary braids in the new object category.

Thus every finite chain of the stated even moves preserves closure equivalence.

## 6. Completeness: lifting every unrestricted Markov edge

For the proof only, define an even representative of an arbitrary tagged braid by

\[
P(m,b)=
\begin{cases}
(m,b),&m\text{ even},\\
(m+1,b\sigma_m),&m\text{ odd}.
\end{cases}
\tag{16}
\]

Its closure agrees with that of \((m,b)\). Given an unrestricted classical or virtual Markov chain, apply P to every vertex. The original endpoints, if even, are fixed exactly, including their strand tags. We now check **every** edge type.

1. **Braid relation at count m.** If m is even, apply the same relation. If m is odd, apply it inside b while retaining the terminal \(\sigma_m\) at the even count m+1. All involved generator indices remain valid.
2. **Conjugation at count m.** When m is even, its image is C. When m is odd, its image is BC at N=m+1, with both blocks supported on indices at most N-2. If conjugation is decomposed into single-generator conjugations, each of these is one such even move.
3. **Right stabilization from an even count m.** The original edge is \((m,b)\leftrightarrow(m+1,bg)\), with \(g\in G_m\). Its image is
   \[
   (m,b)\leftrightarrow(m+2,bg\sigma_{m+1}),
   \]
   exactly D.
4. **Right stabilization from an odd count m.** Its image is
   \[
   (m+1,b\sigma_m)\leftrightarrow(m+1,bg),
   \]
   exactly T, or an identity when g is positive. Stabilization inverses are covered by the reversed arrows in items3–4.
5. **Right virtual exchange at an even total count m.** Its image is R at N=m. At an odd total count m, P retains a terminal \(\sigma_m\), and the image is BR at N=m+1. The exchange blocks have indices at most m-2=N-3 in the latter case.
6. **Left virtual exchange at an even total count m.** Its image is L at N=m. At an odd total count m, its image is BL at N=m+1. Again the unshifted blocks have support at most N-3, so their shifted versions and the terminal crossing satisfy the displayed support requirements.

Identical successive images can be removed. The resulting sequence is a finite chain in the **even-only category**, connecting exactly the original even endpoints. In the classical setting the input chain has no virtual letters or virtual exchanges, so it uses only C, BC, T and D.

This proves completeness in both directions. It also proves the representation statement: start with any Alexander braid representative and apply P once. If an unrestricted certificate never exceeds M strands, its even image never exceeds \(2\lceil M/2\rceil\), with no further intermediate strand counts. This is a certificate-conversion observation, not a complexity bound for finding a certificate.

## 7. Why this is more than an unspecified compressed path relation

A rule saying “two even braids are related whenever some odd-intermediate Markov path connects them” would merely restate closure equivalence. No such rule is used here. There are finitely many explicit word-pattern types; their support restrictions are stated in the even ambient group; and each usual generator of Markov equivalence is converted to a single named type (or to elementary braid relations). An application of a move is certified by its displayed word data, without searching for a hidden path or solving a link-equivalence problem.

The list is an algebraic block-move formulation. It is not claimed to be the smallest list, or to satisfy an additional requirement that every modification lie in a disk meeting a bounded number of strands independently of the word blocks. The original item does not state either demand. If one adds such a stronger geometric-locality requirement, that becomes a different problem and is not resolved by the present theorem.

## 8. Verification and attribution boundary

The checker constructs tagged classical and virtual words, applies the padding map, and verifies that every sampled unrestricted edge matches the corresponding explicit even pattern exactly. It also checks index ranges, endpoint parity, reversibility, the sharp rounding bound for certificate height, and preservation of the permutation-cycle count of the ordinary closure. The latter is only a necessary sanity check for link equivalence.

The finite diagnostics do not prove the unrestricted Markov theorems or replace the symbolic edge-by-edge argument. No braid word-problem solver or exhaustive knot search is claimed. The foundational Markov, virtual Markov, Alexander and exchange results are prior work. The bounded literature audit did not establish historical priority for this padding reformulation, and no novelty claim is made.
