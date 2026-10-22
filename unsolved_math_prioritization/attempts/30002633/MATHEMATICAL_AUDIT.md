# Independent mathematical audit: canonical-family reduction for the sharp κ estimate

Target: 30002633 / OWR-13106-006. Audit date: 10 October 2026 UTC.

## Decision

**Accept the mathematics as a partial result, first substantive attempt (1/5). The exact whole-section metric-scope clarification required by this audit is applied in §7.1 of the distributed report identified below.** The reduction to a canonical connected-sum family, the stable-slope equivalences, and the stated obstruction to smooth compactness are mathematically valid consequences of the imported results. They do not prove the proposed universal estimate or construct a counterexample. No additional proof-search turn is represented by this audit.

For each fixed integer m≥2, set d=2^m, B_m=(K3)^m with A-hat(K3)=2, and X_{m,p}=#^p B_m. The accepted principal conclusion is the equivalence between:

1. |A-hat(M)|≤d κ(M) for all closed spin 4m-manifolds;
2. the same inequality for connected simply connected closed spin 4m-manifolds;
3. κ(X_{m,p})=p for every positive integer p;
4. that equality for an unbounded set of p;
5. lim_{p→∞} κ(X_{m,p})/p=1.

The last three statements remain unproved in this packet. An equivalence with them is not a resolution of the original question.

## 1. Exact question and primary-source scope

The original question is the open question immediately after Theorem 4 on printed p.2006 of Oberwolfach Report 36/2014. The coefficient to be improved is 2^(2m−1), and the proposed coefficient is 2^m. The question has no simple-connectivity hypothesis. The source's spectral convention starts at eigenvalue μ_0 and includes multiplicities. The attempted report preserves these conventions. The case m=1 is already covered by the old theorem; κ=∞ makes the inequality vacuous. [Original report](https://doi.org/10.4171/owr/2014/36).

The principal imported source is Bär–Dahl, *Small eigenvalues of the conformal Laplacian*, author manuscript arXiv:math/0204200v3, dated 3 December 2002, corresponding to Geom. Funct. Anal. 13 (2003), 483–508. The manuscript itself, rather than an abstract or search excerpt, was checked. Its relevant statements have exactly the required scopes:

- Equation (3), p.2: finite-disjoint-union additivity of κ. Orientation reversal leaves κ unchanged.
- Proposition 1.2, p.2: κ=0 is equivalent to the existence of a positive-scalar-curvature metric; a connected scalar-flat manifold has κ≤1.
- Theorem 2.4, p.8: the existing A-hat estimate has coefficient 2^(2m−1).
- Theorem 3.1, p.10: codimension-at-least-three surgery can approximate any prescribed **whole ordered initial eigenvalue block**, for Δ+c Scal with fixed c>0.
- Corollary 3.2, p.10: κ does not increase in the permitted surgery direction.
- Lemma 3.4, pp.10–11: each finite eigenvalue block is continuous in the C¹ topology on **smooth positive-definite metrics**.
- The normalization on p.4 is α=A-hat in dimensions divisible by eight and α=A-hat/2 in dimensions congruent to four modulo eight.
- Remark 4.3, p.18: simply connected spin manifolds of the **same dimension at least five** and the same α have equal κ.

In particular, Remark 4.3 is not a statement about multiplication by a Bott manifold. It follows the spin-bordism argument of Proposition 4.2 and invokes Stolz's theorem through that argument. The attempted report is entitled to import this published result without reproving Stolz. Theorem 5.1, p.20, concerns dimensions changed by Bott products; it is neither needed nor used in the canonical-family proof. [Bär–Dahl author manuscript](https://arxiv.org/abs/math/0204200v3).

For the compactness consequence, Futaki's Corollary 2 applies to connected closed manifolds with finite fundamental group and spin universal cover: the existence of a nonnegative-scalar-curvature metric entails |π₁(M)| |A-hat(M)|≤2^(dim M/4). The simply connected spin special case used in the report is therefore valid. The preprint's statement is on PDF p.4/printed p.2, and its proof is on PDF p.9/printed p.7. The historical comment about the then-unknown existence of compact Spin(7) examples is not used as a present-day claim. [Futaki author preprint MPI 92-57](https://archive.mpim-bonn.mpg.de/1159/1/preprint_1992_57.pdf).

The Gromov–Lawson proof of Theorem B, printed pp.431–432, corroborates the spin-bordism/codimension-three surgery mechanism. It is not being cited as a replacement for the later Stolz input or as a claim that α alone classifies all spin bordism classes. [Gromov–Lawson](https://annals.math.princeton.edu/1980/111-3/p02).

## 2. Disjoint unions and spectral normalization

The disjoint-union identity is an explicitly stated source result. It also has a direct verification that is worth recording because the disconnected case is part of the target.

For the upper inequality, take normalized κ-witnesses on each component with all preceding eigenvalues of absolute value below ε<1. The union has the sum of those numbers of small eigenvalues and its next eigenvalue is exactly one. For the reverse inequality, suppose a disjoint union has a finite witness number k. Along witnesses with ε tending to zero, pass to a subsequence on which the allocation of its first k eigenvalues between the finitely many components is constant, say k_i on component i. The next eigenvalue on every component is at least one. Scaling each component by its own next eigenvalue normalizes that eigenvalue to one and can only reduce the absolute values of the preceding eigenvalues. Thus κ(M_i)≤k_i, and summing gives Σκ(M_i)≤k. This also handles the possibility of infinite κ by contraposition. No cancellation of negative eigenvalues is used.

The report's surgery normalization has the correct scaling direction. If μ_k(h)=λ>0, the rescaled metric λh has eigenvalues μ_i(h)/λ. With η=min(1/4, ε/4), the finite surgery sequence leaves μ_k(h)>1−η and |μ_i(h)|<2η for i<k. Hence the normalized preceding block is bounded by 2η/(1−η)<ε. Negative eigenvalues stay negative where appropriate; their absolute values are controlled. Multiplicities are included because the imported theorem compares ordered lists, not chosen eigenvectors.

The total error budget is legitimate for finitely many surgeries, and no infinite surgery process is used. For k=0 the preceding block is empty; one may invoke the theorem with at least one eigenvalue requested and retain its μ_0 conclusion, regardless of the convention for whether 0 belongs to N.

## 3. Spin surgery and the fundamental-group reduction

The circle-surgery lemma passes all of the needed topological checks.

- A closed smooth manifold has a finite CW model, so its fundamental group has a finite generating family.
- In dimensions n≥5 those loop classes have pairwise disjoint embedded circle representatives. Based generators can be represented by free embedded loops with paths to the basepoint; killing their normal closures still kills the group.
- Each circle's oriented normal bundle is trivial. Its rank is n−1≥4, and the two homotopy classes of oriented framings differ by the nontrivial element of π₁(SO(n−1)).
- Twisting by that element switches the induced spin structure on the circle. One choice is the bounding spin structure, so the ambient spin structure extends over the index-two handle in the surgery trace. The construction supplies a spin bordism, not just an oriented bordism with an unexamined framing.
- Removing the circle's tube preserves the fundamental group: maps of loops and of their homotopies can avoid its core by general position. Van Kampen identifies the result of the surgery with the quotient by the normal closure of that loop. The attached D²×S^(n−2) is simply connected. Connectivity is preserved.
- After finitely many such surgeries the manifold N is simply connected, spin, and has α(N)=α(M). For dimension 4m the A-hat characteristic number is preserved as well.
- The surgery codimension is n−1≥4. Therefore the spectral theorem gives κ(N)≤κ(M), the direction needed to preserve a hypothetical violation.

There is no use of a converse surgery inequality. The inverse circle surgery has codimension two, outside the imported theorem. When m≥2, the entire reduction stays in dimension 4m≥8, safely within the topological and spectral hypotheses.

If the proposed inequality holds on simply connected manifolds, applying it to N gives |A-hat(M)|=|A-hat(N)|≤dκ(N)≤dκ(M). For a finite disjoint union, additivity of κ and the triangle inequality for A-hat finish the reduction. Thus arbitrary π₁ and disconnected manifolds really are covered by the equivalence.

## 4. Canonical family and amplification

A scalar-flat product metric on B_m gives κ(B_m)≤1. Its A-hat genus is 2^m≠0, excluding positive scalar curvature and hence κ=0. Consequently κ(B_m)=1.

An oriented connected sum is an S⁰ surgery on a disjoint union. A compatible spin one-handle exists, the surgery codimension is n≥3, and therefore

κ(M₁#M₂)≤κ(M₁)+κ(M₂).

This establishes κ(X_{m,p})≤p. The inherited lower bound is exactly ceil(p/2^(m−1)); it is correctly identified as the old Bär–Dahl estimate after substitution, not an improvement.

The reverse implication in the principal theorem is the critical arithmetic step. Assume κ(X_{m,p})=p for every p. Given a connected spin M with finite κ(M)=k and nonzero A-hat, reverse its orientation if necessary and put A=A-hat(M)>0. The spin index ensures A is an integer. Form Y=#^d M, where d=2^m is a number of copies. Then κ(Y)≤dk and A-hat(Y)=dA. Kill π₁ by spin circle surgery, obtaining N with κ(N)≤dk and the same A-hat genus.

N and X_{m,A} now have the same dimension, are simply connected and spin, and have equal A-hat=dA. The same-dimensional α normalization gives α(N)=α(X_{m,A}) in both dimension classes modulo eight. Remark 4.3 gives

A=κ(X_{m,A})=κ(N)≤dk.

This is the desired estimate. The parity constraint on A in dimension 8ℓ+4 causes no problem; it makes A even but does not prevent using it as the positive integer index of the canonical family. The argument does not require every integer to occur as the original A-hat genus.

Conversely, the universal estimate applied to X_{m,p} supplies κ(X_{m,p})≥p and hence equality. A hypothetical violation A>dk produces the concrete canonical-family defect κ(X_{m,A})≤dk≤A−1. All inequalities are in the proper direction.

## 5. Defect propagation and stable slope

For a(p)=κ(X_{m,p}) and the artificial value a(0)=0, connected-sum subadditivity gives a(p+q)≤a(p)+a(q). If a(p₀)=p₀−δ with δ≥1, write p=qp₀+r, 0≤r<p₀. Then

a(p)≤q a(p₀)+a(r)≤p−qδ.

For every p≥p₀, q≥1, so equality a(p)=p is impossible. This is stronger than showing defects only at multiples of p₀. The handling of r=0 uses a(0)=0 merely as a numerical convention and requires no zero-fold connected-sum manifold.

The given elementary subadditivity argument proves

lim a(p)/p=inf a(p)/p,

with value in [2^(1−m),1]. A slope of one forces every ratio to be at least one, while the construction forces every ratio to be at most one. Conversely, equality for all p gives slope one. An unbounded equality set excludes any finite first defect by the propagation inequality. These conclusions correctly prove the equivalence of items 3–5 without computing the slope.

The integer model b_N(p)=p−floor(p/N) is a valid barrier to the claimed numerical inference: it has all the listed subadditive and lower/upper-bound properties, agrees with p before N, and has slope 1−1/N. It is expressly not a geometric counterexample. Finite tests and the listed numerical properties alone cannot establish the missing infinite family of equalities.

## 6. Audit of the analytic obstruction claims

### The one-chirality shortcut

For the flat torus T^(4m) with trivial spin structure, both complex chiral harmonic-spinor spaces have dimension 2^(2m−1). Lichnerowicz identifies harmonic and parallel spinors for the flat metric, and the parallel spaces have those ranks. Its scalar Laplacian has a one-dimensional kernel; scaling this same flat metric gives an exact κ≤1 witness. Thus the proposed uniform replacement h⁺≤2^mκ fails for m≥2, while h⁺−h⁻=0. The ordinary index inequality has not been refuted. The stronger fact κ(T^(4m))=1 is already cited in Bär–Dahl, but is unnecessary for this counterexample to the shortcut.

A metric-scope qualification is important: the h⁺ in the Bär–Dahl proof is evaluated for a specially chosen metric meeting its spectral-gap hypothesis. It is not claimed there that every metric on M has h⁺ bounded by 2^(2m−1)κ(M). The torus argument refutes the uniform one-chirality substitution and its application to the exact-flat witnessing sequence. It does not prohibit every possible argument using a different choice of metrics. This distinction does not affect the canonical-family theorem.

### Smooth-limit obstruction

Lemma 3.4 applies precisely to the report's convergence hypothesis: after diffeomorphism pullback there is C¹ convergence to a smooth positive-definite metric on the same manifold. Pullbacks leave the scalar spectrum unchanged. Continuity forces zero to be the lowest eigenvalue with multiplicity k. A scalar Schrödinger operator on a connected closed manifold has simple ground state with a strictly positive eigenfunction, so k=1. Conformal covariance then converts its positive zero eigenfunction f into a scalar-flat metric f^(4/(4m−2))g∞. Futaki supplies |A-hat(M)|≤2^m.

Nonzero A-hat gives the index obstruction needed to exclude positive scalar curvature and supplies harmonic spinors in the scalar-flat case. In a holonomy explanation, zero-index factors, such as G₂ factors or odd-complex-dimensional Calabi–Yau factors, cannot occur in a product with nonzero total A-hat. The remaining irreducible factors have the stated genus values, whose products satisfy the bound.

The κ definition provides none of the compactness hypotheses. The proposition excludes this kind of smooth limit for every k>1 witnessing sequence; it supplies neither a limiting decomposition into k scalar-flat components nor a means to rule out degeneration. It therefore cannot be promoted to a universal proof.

### Reverse surgery and product spectra

The inverse of the S⁰ connected-sum surgery is a surgery on S^(n−1), of codimension one. Neither it nor inverse circle surgery is covered by the codimension-three theorem. The stated inability to deduce a lower bound by simply undoing the construction is correct.

For a product with a Ricci-flat d-dimensional factor, the coefficient difference is

c_(n+d)−c_n = d/[4(n−1)(n+d−1)] > 0.

The additional scalar-curvature multiplication operator is not controlled by a κ witness on the first factor. A-hat multiplicativity does not supply a conformal-Laplacian product law or a κ product inequality. The report correctly makes no such claim.

## 7. Verification, acceptance boundary, and exact gap

The audit also independently inspected source pixels for Bär–Dahl PDF pages 2, 4, 10, and 18; OWR PDF page 16/printed p.2006; and Futaki PDF pages 4 and 9. Further relevant passages were read from the retained full-text extractions. The arXiv version record and Futaki's public preprint were also reopened. A fresh OWR DOI web retrieval failed; the retained hashed full PDF and its statement page were available and were used, so this failure does not create a statement-verification gap.

Accepted source-byte identities:

- Bär–Dahl: 217733 bytes; SHA-256 cbc78fc33b701b2cc4f3e50855db1cabd0658715032eafa12163e90a4b7d138a.
- OWR 36/2014: 509561 bytes; SHA-256 fe95c0a5e2d9f3c84d1903c276aaf91fd0f3f7b6599fb8aacfa7f215f7c2b954.
- Futaki MPI 92-57: 357811 bytes; SHA-256 b9bee3a9b56fd3f4c5a2b1e59315c56e054019313983a6d85a41d85e3f42c564.
- Gromov–Lawson: 842699 bytes; SHA-256 4a4dc75afe0a7743c668653349f32f3d526b953c2d8054e14392b3220ebda69b.

The exact mathematical gap is unchanged:

κ(#^p((K3)^m))≥p for every m≥2 and p≥2,

or, equivalently, stable slope one in every such fixed dimension. A refutation instead requires a genuine manifold/metric construction witnessing some κ(X_{m,p})<p with the required entire small-eigenvalue block. Neither side is supplied.

The acceptance is for the stated consequences of the cited theorems. It is not a broad novelty certification, a formal proof certificate, or a certification of current openness throughout the literature. The bounded source screen and this review did not establish a later full resolution.

## Distributed authored-version scope

The accepted report in this proof-only edition is [PROOF_SEARCH_REPORT.md](PROOF_SEARCH_REPORT.md), 22746 bytes, SHA-256 4cd7c49be6d21533e45aaceb94973d450b0d1cb100250811f0c9eaadb0a0294d. Its §7.1 applies the exact whole-section clarification required by the audit. The Bär–Dahl opening is explicitly metric-specific: the estimate concerns its selected spectral-gap metric, not a uniform bound for every metric. The torus conclusion is limited to the blanket one-chirality inequality, leaving other justified metric-selection arguments possible. No new theorem or missing proof is asserted by this clarification.

The complete canonical-family equivalence, spin framings, signed full-block normalization, same-dimensional α comparison, stable-slope and defect-propagation proofs, compactness and product barriers, and the symbolic b_N example are preserved. The numerical example is not a manifold counterexample. Supplementary computational verification accounts and undistributed artifact identities are omitted from this proof-only edition. Mathematical acceptance applies to the stated consequences of the cited theorems, with the source/version/access limits retained above.

This AI-assisted audit is unrefereed. Acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. Any subsequent revision requires review of its changed passages and a new distributed-version identity.
