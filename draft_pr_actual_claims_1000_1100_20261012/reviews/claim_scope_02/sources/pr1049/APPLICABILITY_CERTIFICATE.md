# Hayman Littlewood root count prior resolution certificate

**Target:** 2304015 / AMR-022-4015, Hayman Problem 4.15.

**Checked:** 9 October 2026.

**Conclusion:** The exact almost-all, half-root-count question is covered by Oren Yakir's published result. The transfer from the cited theorem to the requested polynomial family is verified below. This is a prior-resolution applicability certificate, not a new solution or an independent audit of Yakir's complete proof.

## The question being certified

For each positive integer $n$, put

$$
\Omega_n=\{-1,1\}^n,\qquad
H_{\varepsilon}(z)=\sum_{k=1}^{n}\varepsilon_k z^k,
\qquad D=\{z\in\mathbb C:|z|<1\}.
$$

Let $N_D(f)$ count the zeros of $f$ in this **open** disc, with algebraic multiplicity. The target asks whether, among the $2^n$ distinct polynomials $H_\varepsilon$, all but $o(2^n)$ have $n/2+o(n)$ such zeros. This is the question on printed p.76, PDF p.77, of Hayman and Lingham's arXiv:1809.07200v2, Problem 4.15. The same page's historical update records no reported progress as of that 2018 edition; it is not a current-status assertion. [H]

A precise sufficient meaning of the two little-oh terms is: there exist numbers $r_n\ge0$ and exceptional sets $E_n\subseteq\Omega_n$ such that

$$
\frac{r_n}{n}\longrightarrow0,\qquad
\frac{|E_n|}{2^n}\longrightarrow0,\qquad
|N_D(H_\varepsilon)-n/2|<r_n\quad(\varepsilon\notin E_n).
$$

The same $r_n$ must work for every nonexceptional sign vector at size $n$. The conclusion is not required for every polynomial or only along a subsequence.

## The cited result and its model

In Theorem 1 on p.1 of arXiv:2011.06234v2, Yakir takes

$$
Q_n(z)=\sum_{j=0}^{n-1}X_jz^j,
\qquad
\mathbb P(X_j=1)=\mathbb P(X_j=-1)=\tfrac12,
$$

with independent coefficients, and establishes

$$
a_n:=\mathbb P\!\left(
\left|N_D(Q_n)-\frac n2\right|\ge n^{9/10}
\right)\longrightarrow0.
\tag{Y}
$$

The rendered theorem was inspected to verify both the absolute value and the non-strict exceptional-event threshold. The model is uniform on all $2^n$ real-sign coefficient vectors; its degree is exactly $n-1$. The paper expressly identifies Hayman Problem 4.15 as the problem answered. [Y, p.1]

Here the zero count is in the complex plane. Real Rademacher coefficients do not mean that only real zeros are counted, and they are not complex random phases or Gaussian coefficients. No conditioning on the leading coefficient, irreducibility, simple roots, or a parity class of $n$ occurs in the theorem.

## Exact transfer to Hayman's indexing

For a sign vector $\varepsilon\in\Omega_n$, define

$$
Q_\varepsilon(z)=\sum_{j=0}^{n-1}\varepsilon_{j+1}z^j.
$$

This is precisely Yakir's coefficient law when $\varepsilon$ is uniform on $\Omega_n$. There is a bijection between the two coefficient families, and

$$
H_\varepsilon(z)=zQ_\varepsilon(z).
\tag{1}
$$

Because $Q_\varepsilon(0)=\varepsilon_1\ne0$, equation (1) adds **exactly one simple zero at the origin**. Every nonzero zero retains its multiplicity. Since $0\in D$, for every sign vector, without any probabilistic qualification,

$$
N_D(H_\varepsilon)=N_D(Q_\varepsilon)+1.
\tag{2}
$$

Let

$$
B_n=\{\varepsilon\in\Omega_n:
|N_D(Q_\varepsilon)-n/2|\ge n^{9/10}\}.
$$

Independence and equal sign probabilities give each sign vector probability $2^{-n}$. Therefore (Y) gives the exact probability-to-cardinality identity

$$
|B_n|=2^n a_n=o(2^n).
\tag{3}
$$

For every $\varepsilon\notin B_n$, equation (2) and the triangle inequality give

$$
|N_D(H_\varepsilon)-n/2|
\le |N_D(Q_\varepsilon)-n/2|+1
< n^{9/10}+1.
\tag{4}
$$

Thus one may take $E_n=B_n$ and the explicit deterministic tolerance

$$
r_n=n^{9/10}+1,
\qquad r_n/n=n^{-1/10}+n^{-1}\longrightarrow0.
\tag{5}
$$

Equivalently, the number of Hayman polynomials for which
$|N_D(H_\varepsilon)-n/2|\ge n^{9/10}+1$
is at most $2^n a_n=o(2^n)$. This proves the precise target formulation from the cited theorem. The proof of this transfer is elementary and complete; the nontrivial probabilistic assertion (Y) is credited to Yakir.

## Degree and asymptotic quantifiers

- Hayman's family has $n$ signs and degree $n$; Yakir's family has $n$ signs and degree $n-1$. The same $n$ is the number of signs in both families. Substituting $n+1$ into the theorem is unnecessary and would change the number of polynomials.
- The theorem is centered at $n/2$, as printed, not at $(n-1)/2$. The added zero shifts the exact count by one, absorbed explicitly by (4). No assertion of an exact mean or an exact half of the degree is needed.
- The limit holds as integer $n\to\infty$, with no even-only or odd-only restriction. Omitting finitely many small degrees has no effect.
- For every fixed $\delta>0$, equation (5) eventually gives $r_n<\delta n$. Hence the fraction of Hayman polynomials with $|N_D(H_\varepsilon)/n-1/2|\ge\delta$ tends to zero.
- The theorem supplies an $n^{9/10}$ deviation tolerance with exceptional probability tending to zero. This certificate does not claim a numerically effective cutoff, an optimal deviation scale, a central limit theorem, or almost-sure convergence under a coupling across degrees.

## Multiplicity and the unit circle

The zero-counting measure on Yakir's p.1 is used with Jensen's formula in §2, equations (2.3)–(2.4), pp.3–4. This is the algebraic-multiplicity zero count: repeated roots contribute their multiplicities. The notation is not a distinct-root count, and no square-free hypothesis is being added. [Y]

The certificate uses $D=\{|z|<1\}$. Zeros on $|z|=1$ do not contribute to $N_D$. Multiplication by $z$ leaves every unit-circle zero and its multiplicity unchanged, so equation (2) is valid even for a polynomial with boundary roots. It does not assume that boundary roots are impossible.

Yakir separates the boundary from the disc in the remark on p.5 and records

$$
\mathbb P\bigl(Q_n\text{ has a zero on }\{|z|=1\}\bigr)\longrightarrow0
\tag{6}
$$

as equation (2.6), citing Konyagin and Schlag. Thus even if a reader were to assign a closed-disc convention to the unqualified word “disk,” the manuscript's stated boundary result lets one discard a further $o(2^n)$ coefficient vectors and obtain the same open-disc conclusion. This convention check does not independently audit the cited boundary theorem. The main transfer (1)–(5) uses the open-disc theorem and does not need an assumption of boundary-free polynomials. [Y, p.5]

## Publication status and credit

The official Institute of Mathematics of the Polish Academy of Sciences record identifies:

Oren Yakir, *Approximately half of the roots of a random Littlewood polynomial are inside the disk*, **Studia Mathematica 261 (2021), 227–240**, DOI **10.4064/sm201117-28-1**, published online **31 May 2021**. The publisher's abstract gives the same almost-all conclusion for the $n$-coefficient family and attributes the original question to Hayman's 1967 book. [P]

The arXiv history has v1 on 12 November 2020 and v2 on 24 January 2022. The later revision date does not turn the published 2021 result into an unpublished 2022 claim. The technical statement inspected here is the version-pinned arXiv v2. The publisher record independently confirms journal publication and the matching conclusion; the publisher's typeset PDF was not obtained or compared byte-for-byte with arXiv. [A, P]

Credit for the solution belongs to Yakir. The coefficient relabeling, added-zero calculation, and conversion of probability to a count in this certificate explain applicability and are not claimed as a new research result.

## Scope of verification

Verified here: exact target and source locations; coefficient distribution; number of sign choices; degree/indexing shift; open-disc and multiplicity conventions; quantitative threshold transfer; uniform little-oh quantifiers; and public publication metadata. Fresh downloads of both version-pinned primary PDFs match the previously inspected bytes; hashes and inspection scope are recorded separately.

Not certified here: every estimate or dependency in Yakir's 14-page proof, the independent validity of the cited Konyagin–Schlag result, or identity of the arXiv and journal typeset texts. During the boundary inspection, apparent proof-text issues were noticed on Yakir's p.5: the displayed upper-tail conversion has a plus-sign error allowance, and the reciprocal-polynomial definition writes its new symbol on both sides. These observations are preserved for any future independent proof audit. No correction is asserted or attempted here. They do not alter the source theorem's statement or the exact implication (1)–(5).

**Disposition:** Record this target as resolved in prior published work, with applicability verified and complete-proof audit outside the certificate's scope.

## Public primary references

- **[H]** W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, 21 September 2018, Problem 4.15, printed p.76 / PDF p.77. [Version record](https://arxiv.org/abs/1809.07200v2), [PDF](https://arxiv.org/pdf/1809.07200v2).
- **[Y]** Oren Yakir, *Approximately half of the roots of a random Littlewood polynomial are inside the disk*, arXiv:2011.06234v2, 24 January 2022, Theorem 1 and model on p.1; Jensen count in §2, pp.3–4; boundary remark and (2.6), p.5. [Version record](https://arxiv.org/abs/2011.06234v2), [PDF](https://arxiv.org/pdf/2011.06234v2).
- **[A]** [arXiv publication and submission history](https://arxiv.org/abs/2011.06234).
- **[P]** [Official Studia Mathematica article record](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/261/2/114055/approximately-half-of-the-roots-of-a-random-littlewood-polynomial-are-inside-the-disk), [DOI](https://doi.org/10.4064/sm201117-28-1).
