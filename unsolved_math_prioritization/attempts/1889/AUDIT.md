# Independent audit: finite affine residue patterns

10 October 2026. Target: corpus ID 1889, singleton Erdős problem 25.

**Review scope.** This is an unrefereed, AI-assisted authored note and an independent internal AI audit. “Accepted” refers only to the stated partial mathematical scope. No external human peer review, journal acceptance of these authored documents, formal proof-assistant certification, novelty assessment, or current worldwide openness certification is claimed. The audit reports checks of the reviewed local materials; executable checkers, detailed test outputs, source documents, extracted text, and page images are not distributed in this prose edition. No new scholarly-source retrieval or inspection occurred during edition preparation.

## Decision

**ACCEPT as a partial positive theorem, with no mandatory mathematical correction.** Theorem 1, Lemmas 2–5, Corollary 6, and the explicit example are valid on the stated hypotheses. This is an independent mathematical review, not a formal proof certificate or a novelty assessment. The unrestricted singleton problem remains unresolved by this work.

The reviewed note is *Logarithmic density for finitely many affine residue patterns*, 15,022 bytes, SHA-256 `bd97cb7fdf168742d082866c553f48705c571b90895011087031ad3fa7710174`. Its containing inventory has 32 members, 7,501 bytes, SHA-256 `b052842d8907e035d3fe0cd7ddec885fc5073f8b7b2de8337f74d692cc207e29`. No alteration of that note is needed for this acceptance.

## Exact proposition accepted

There is one canonical residue `0 <= a_i < n_i` per strictly increasing positive integer modulus `n_i`. An integer is excluded by modulus `n_i` only when `m >= n_i`. Outside a family whose reciprocal moduli sum converges, the residue data satisfy one of finitely many fixed identities

\[
q a_i=p n_i+c,\qquad q\ge1,\quad p,c\in\mathbb Z.
\]

On these hypotheses the surviving integers have logarithmic density equal to the decreasing limit of the natural densities of the finite sieves. Pairwise coprimality, disjointness of progressions, bounded residues, and convergence of the reciprocal sum over the patterned family are unnecessary. Natural density of the infinite survivor set is not asserted.

When every modulus is patterned, every modulus may instead have its own arbitrary finite positive activation threshold. The resulting logarithmic density is the same finite-periodic limit. This threshold-invariance statement is not extended to arbitrary summable exceptions.

The inclusive activation and singleton formulation agree with Erdős's section I.4, visually checked in the full original PDF. [Erdős 1995](https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf)

## Dependency and proof audit

### 1. Davenport–Erdős is used at the correct strength

For any positive-integer divisor set `D`, the required input is not merely existence of the logarithmic density of `M(D)`. It is equality with the increasing finite-union limit. The 1936 paper defines its constant on printed page 147 from the densities added by consecutive divisors; Theorem 1(a), printed pages 149–150, gives logarithmic density equal to this constant. No coprimality, reciprocal summability, or natural-density hypothesis occurs. Finite or empty `D` is covered directly by periodicity. [Davenport–Erdős 1936](https://users.renyi.hu/~p_erdos/1936-04.pdf)

Consequently, for fixed `K`, the nested difference `M(D) \ M(D_K)` has logarithmic density equal to the difference of their logarithmic densities, and these differences tend to zero. This uses subtraction of two existing limits for nested sets, not countable additivity of density.

All five pages of the original paper were read and visually inspected. Its classical Tauberian input is taken as an established theorem; no new formal verification of that theorem is claimed.

### 2. Primitive sets and bounded chain height

If `P` is primitive and `x` is an element of `P` exceeding `K`, then no element of `P_K` divides `x`: such a divisor would be a distinct element of `P`. Hence

\[
P\setminus[1,K]\subseteq M(P)\setminus M(P_K).
\]

The preceding tail theorem bounds its upper logarithmic density by a quantity tending to zero. No prior existence of the logarithmic density of `P` is assumed. For a set of strict divisibility-chain height at most `h`, rank each element by the longest chain ending at it. Each rank is well defined because an integer has finitely many positive divisors. Comparable distinct elements have different ranks. Thus there are at most `h` primitive layers, and a finite union bound proves the claim.

### 3. Affine pullback

For the injective map `t=bm-c`, after deleting finitely many small positive `m`,

\[
\frac1m=\frac{b}{t+c}=\frac b t+O_{b,c}(t^{-2}).
\]

The error sum is bounded independently of the chosen subset of positive `t`. Summing to `bX+|c|` and dividing by `log X` proves the claimed upper-logarithmic-density inequality. Positive, zero, and negative `c` cause no difficulty; positivity of the affine image is essential and is correctly restricted to all sufficiently large `m`. The argument never asserts that intersecting an arbitrary logarithmically dense set with a residue class preserves existence of density.

### 4. Restricted multiples and valuation strata

Let `g=gcd(p,q)>0`. The equivalence `k congruent p mod q` iff `k=g j` with `j congruent p/g mod q/g` gives exactly

\[
V_{p,q}(D)=gV_{p/g,q/g}(D).
\]

There is no scaling of `D`. Negative `p` is harmless because congruences depend on its residue class. For `p=0`, `g=q` and the reduced quotient modulus is one. Scaling a set by `g` multiplies upper logarithmic density by `1/g`, since its harmonic sum up to `X` is exactly `1/g` times the original sum up to `X/g`.

In the coprime case, decompose `x=s u` with `s` supported on the primes dividing `q` and `gcd(u,q)=1`. A divisor `d` giving quotient congruent to the unit `p` has the same exact valuations as `x` at every prime dividing `q`. Thus `d=s v`. On the stratum `u congruent r mod q`, the remaining conditions are exactly `v|u` and `v congruent r p^{-1} mod q`. Using the full supported factor rather than `gcd(x,q)` is indispensable. The inverse is `p^{-1}`, not `p`.

For `D_K`, the new bound is `v <= K/s`, exactly as written. Restricting the residual multiples difference to the unit class can only decrease its upper logarithmic density; scaling by `s` supplies the factor `1/s`. This is sufficient even though no separate theorem on residue-class intersections was cited.

For each fixed valuation cap `L`, only finitely many supported factors and unit residues occur. The omitted integers lie in the finite union of `ell^L N` over primes `ell|q`, whose upper logarithmic density is at most the sum of `ell^{-L}`. First take `K` to infinity for this finite collection, then `L` to infinity. No exchange of infinite unions and density is used. For `q=1`, there is one stratum (`s=1`, the sole residue class), and the omitted union is empty; no inverse modulo a nontrivial ring is needed.

### 5. Translation of the affine residue family

For a fixed valid triple, writing `m=a_n+n z` gives

\[
qm-c=n(p+qz).
\]

When `qm-c>0`, the quotient on the right is a positive integer congruent to `p` modulo `q`. Conversely, `qm-c=n k` with `k congruent p mod q` implies `m-a_n=n(k-p)/q`. These are exact integer identities. The finite initial region where the affine image is nonpositive depends only on the fixed triple, not on the choice of modulus or on the truncation parameter. The restricted-multiple approximation therefore transfers to the untruncated residue union `U`.

### 6. Activation, including the optional chain proof

For every fixed finite modulus bound `K`, `U_K \ B_K` is finite. The displayed inclusion

\[
B\setminus B_K\subseteq (U\setminus U_K)\cup(U_K\setminus B_K)
\]

therefore proves the needed approximation without removing activation as an assumption. This is the shortest route to Theorem 1.

The additional proof of Lemma 5 is also sound. After excluding finitely many small affine images, every `t` in the defect has a representation `t=n k` with positive `k congruent p mod q`. If `t_2=h t_1`, `h congruent 1 mod q`, and `h>=2q`, the same `n` witnesses the congruence at `m_2`, and

\[
m_2\ge(2q t_1-|c|)/q\ge t_1\ge n.
\]

This contradicts defect membership. On a fixed supported-factor/unit-residue stratum, a comparable pair has quotient `1 mod q`, even when `p` is not a unit. A chain with `ceil(log_2(2q))+1` elements has endpoint quotient at least `2q`. The resulting height bound, primitive-layer argument, and finite-stratum tail estimate prove zero upper logarithmic density. The indexing counts elements, not links; the stated bound is correct. For `q=1` the height bound is one.

### 7. Arbitrary finite thresholds

For arbitrary finite positive `T_n`, the same finite-defect argument works: each `U_K \ (B_T)_K` is finite, although its size can grow without bound with `K`. The order of limits is crucial and correct: fix `K`, let `X` tend to infinity, and only afterward let `K` increase.

There is an additional short way to see full threshold invariance:

\[
U\setminus B_T\subseteq(U\setminus U_K)\cup(U_K\setminus(B_T)_K).
\]

Thus the whole removed-activation defect is logarithmically null. This directly proves the conclusion of Lemma 5 and Corollary 6 from the approximation already established for `U`. It is an optional simplification, not a repair.

### 8. Exceptional family and final union

For a canonical residue, the activated progression consists of `a+n j` with `j>=1`, including the zero-residue case. Its count up to `X` is `max(0,floor((X-a)/n))`, at most `X/n`. Summing this pointwise count bound over exceptional moduli above `K` gives an upper natural-density bound by their reciprocal tail. Partial summation gives the same upper logarithmic-density bound. This is a uniform counting argument, not an invalid general countable-union inequality for upper density.

Assigning each nonexceptional modulus to any one valid triple gives finitely many families. Their residual errors are controlled by a finite union bound regardless of overlap. Each complete finite approximation is eventually periodic. The monotone approximation principle then identifies the limit, and taking complements gives exactly formula (2).

### 9. Example and boundary

For odd prime `ell`, `n=2ell` and `a=ell` exclude exactly the odd multiples `ell k` with odd `k>=3`. Every odd composite has such a divisor with `ell<=m/3`. Hence the survivor set is precisely the even integers, the odd primes, and 1, with natural and logarithmic densities `1/2`. The reciprocal sum diverges, all moduli share a factor two, and residues and complementary residues are unbounded. The finite six-prime version was independently checked exactly.

Do not extend threshold invariance to arbitrary summable exceptions. An explicit scope control is `n_i=2^{i+2}`, `a_i=i`, `i>=1`. The reciprocal sum is `1/4`; with the original activation the survivor density is at least `3/4`. With all thresholds set to 1 the untruncated union contains every integer `i` via its own residue, so the survivor set is empty. Its density differs from the finite-periodic limit, which remains at least `3/4`. This only rejects an unstated extension; it is not a counterexample to the actual Erdős target or to the accepted theorem.

## Source boundaries and computation

Araújo's dissertation, section 3.2, Theorems 3.24 and 3.26 (printed pages 40 and 42), was checked from the full PDF. It distinguishes the untruncated-sieve issue from the activated summable theorem. The source uses overloaded notation for the number of residue classes; the candidate's one-residue counting argument is explicit and does not depend on that notation. [Araújo dissertation](https://digital.ub.uni-paderborn.de/hs/download/pdf/8306542)

Chojecki's full note was checked beyond its abstract: the positive-case statements, first-kill setup, Conjecture 5.1, and conditional Theorem 5.4 are clearly distinguished. Its missing estimate is not imported as a theorem here. [Chojecki note](https://www.ulam.ai/research/erdos25.pdf)

Wang's full retained PDF, Theorem 1.1 and section 5, and the public full-text page distinguish the multiple-residue proposed construction from singleton EP25. The proposal's proof and Lean claims were not audited. The direct remote PDF request failed during this audit, while the public HTML and the authenticated local PDF supported the scope check. [Wang full-text page](https://multiscalar.ai/results/erdos-486/)

The candidate's exact checker was rerun under ordinary Python, `-O`, and `-OO`, reproducing its retained output byte for byte. An independently implemented suite additionally checks negative and zero quotient residues, modulus one, large signed offsets, valuation tails, cutoff-chain ranks, thresholds both below and far above their moduli, exceptional counts, and an exact six-prime density. All checks use explicit failures rather than disabled assertions. Finite tests support the algebra and edge cases; the infinite conclusions depend on the proof above and the classical theorem.

No novelty claim, global current-openness certification, or source redistribution is part of this audit.
