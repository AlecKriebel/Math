# Credited source certificate: Kourovka 21.134

Checked 2026-10-03 UTC. Upstream identifier: [2643 / KOU-21.134](https://www.unsolvedmath.com/problems/2643).

## 1. Exact target and authoritative resolution

For a finite group \(X\), write \(t_X(n)=|\{x\in X:x^n=1\}|\) for every positive integer \(n\). Problem 21.134 asks whether equality of these functions preserves triviality of the solvable radical, and whether it forces a group to be isomorphic to an almost simple group with that function.

The editors' [October 2026 revision](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf), printed page 197, marks 21.134 with a star and records that **both answers are negative**, crediting J. G. Thompson. The update cites Li–Shi (below) and a letter from the problem's proposer A. V. Vasil'ev dated 18 May 2026. The maintained revision is linked from the editors' [30 September announcement](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/).

This target concerns finite-group power-equation counts. It is distinct from 21.137, which concerns power subgroups of finite prime-power groups.

## 2. Published counterexample and exact numerical input

Yu Li and Wujie Shi, *A note on Thompson problem*, Ricerche di Matematica **74** (2025), 559–563, [DOI 10.1007/s11587-023-00835-4](https://doi.org/10.1007/s11587-023-00835-4); author preprint [arXiv:2303.09460v1](https://arxiv.org/abs/2303.09460v1), submitted 15 March 2023.

The preprint's second page attributes the nonisomorphic equal-type pair to Thompson. Its Theorem 9, on the fourth PDF page, records the pair \(H=L_3(4):2_2\) and \(G=2^4:A_7\), and gives the following numbers \(a_X(d)\) of elements of **exact order** \(d\) for each group:

| \(d\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| \(a_H(d)=a_G(d)\) | 1 | 435 | 2240 | 6300 | 8064 | 6720 | 5760 | 5040 | 5760 |

All other exact-order counts are zero. The article reports a MAGMA computation for this table. That computation is a **credited published input** here: this package has not independently enumerated the groups. Their indicated structures, including the specified ATLAS outer involution, are likewise the groups identified in that source.

The table contains more information than merely equality of the groups' orders and sets of element orders. Those weaker data must not be substituted for the target's type function.

## 3. Why this settles the full target

The following elementary deductions spell out how the credited example applies; they carry no novelty claim.

### Equality for every positive integer

Every element of a finite group has one exact order, and \(x^n=1\) if and only if that order divides \(n\). Consequently

\[
t_X(n)=\sum_{d\mid n}a_X(d).
\]

Equality of the published exact-order counts therefore implies \(t_H(n)=t_G(n)\) for **all** positive integers, including those larger than the group order. No bounded verification is being used to replace that quantifier. Both table totals are 40,320. Its exponent is 840, so these functions can alternatively be written using \(\gcd(n,840)\).

### The radical of \(G\)

Let \(V\cong C_2^4\) be the indicated normal elementary abelian subgroup of \(G=2^4:A_7\). Because \(V\) is solvable and normal, \(V\le R(G)\). The image of \(R(G)\) in \(G/V\cong A_7\) is a solvable normal subgroup. The alternating group \(A_7\) is nonabelian simple, so that image is trivial. Hence \(R(G)\le V\), and

\[
R(G)=V,\qquad |R(G)|=16.
\]

### The radical of \(H\)

Let \(S=L_3(4)=\operatorname{PSL}_3(4)\). This is a nonabelian simple group, and the specified extension satisfies \(S\le H\le\operatorname{Aut}(S)\). Thus \(H\) is almost simple. Set \(N=R(H)\). Then \(N\cap S\) is solvable and normal in \(S\), so it is trivial. Normality gives \([N,S]\le N\cap S=1\), and therefore \(N\le C_H(S)\).

The centralizer of the inner automorphism group of a centerless group \(S\) in \(\operatorname{Aut}(S)\) is trivial: if an automorphism \(\alpha\) commutes with every inner automorphism \(c_s\), then \(c_{\alpha(s)}=\alpha c_s\alpha^{-1}=c_s\), whence \(\alpha(s)=s\) because \(Z(S)=1\). It follows that \(C_H(S)=1\), so

\[
R(H)=1.
\]

Therefore \(G\) has the same type as radical-free \(H\), while having nontrivial radical: part (a) is false. Also \(H\) is almost simple, but \(G\not\cong H\) since the solvable radical is an isomorphism invariant: part (b) is false. The single pair settles both questions simultaneously. Both groups are nonsolvable, so this certificate makes no assertion about a solvable-versus-nonsolvable equal-type pair or the separate original Thompson problem.

## 4. Verification and provenance limits

- The Notebook page and the preprint's attribution and Theorem 9 were inspected as text and as rendered pages. The fresh Notebook PDF has SHA-256 `31baec1b36ec3a956e787355eccfffa2e89df5b1fe31b22a3123377d8103baab`; the versioned arXiv PDF has SHA-256 `a2bb1359b9f184f0faab173fc9a18178191d8b70841f7cd98e9179ecfc7e7068`.
- The journal bibliographic citation is recorded by the Notebook. The detailed theorem was read in the authors' public preprint; the paywalled journal text was not independently inspected.
- The exact catalogue page could not be read live: the web fetch failed and a direct request returned HTTP 403. Its stale cached open label is superseded for this disposition by the editors' explicit resolution and cited counterexample. No claim is made that the live catalogue has been corrected.
- `verify_counts.py` checks the published table's sum, element-order divisibility conditions, exponent, divisor-sum transform and Möbius inversion. These are internal arithmetic consistency checks, **not** a group-enumeration certificate or a replacement for Li–Shi's result.
- Primary source PDFs and screenshots are retained only as local reading inputs and are not part of this publication package.
- Source retrieval, arithmetic validation, exposition and review consume zero substantive proof-attempt turns. There is no residual part of 21.134 left open by this certificate and no claim to a new research contribution.
