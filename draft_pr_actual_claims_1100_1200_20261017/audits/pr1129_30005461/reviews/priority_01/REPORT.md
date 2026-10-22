# Priority audit: PR 1129 / problem 30005461 / OWR-12697710-007

Verdict: **VERIFIED_PRIOR_FULL_CONSEQUENCE**.

Audit date: 17 October 2026 (UTC). Frozen candidate head supplied by coordinator: `26fed29c1130e539ba018a37200f133870f0e036`. The pinned proof and optional appendix hashes match (`BRIDGE_CHECKS.json`).

The mixed-exponent clause is already a credited published theorem. The entire Motzkin-threshold clause follows from **Baldi–Blekherman–Kozhasov–Plaumann–Reznick–Sinn, _Stubborn Polynomials_, arXiv:2602.01191v1**, together with the elementary, uniform local calculation below. This February 2026 source is an earlier **public preprint**, not an identified journal publication. The audit does **not** claim that its authors explicitly wrote the limit formula or recognized this particular consequence. It verifies the full implication and finds no remaining central mathematical problem in applying their theorem to the exact target family.

Accordingly the priority condition for a new solution is not met under a process that counts earlier full mathematical consequences. Recommended root disposition: **strict SKIP; leave the PR, manuscript, comments, closure/merge state, DOI/Zenodo, and tracker untouched**. This audit itself makes no such mutations.

## Exact target and success criterion

The [original Reznick contribution](https://ems.press/content/serial-article-files/47007), printed p.780 / physical PDF p.40, has the following two clauses:

1. For arbitrary real polynomials `p,q` and integers `i,j >= 0`, odd SOS powers `p^(2i+1)` and `q^(2j+1)` imply that `(p+q)^(2i+2j+1)` is SOS.
2. For `f_c=x^4 y^2+x^2 y^4+1-c x^2 y^2`, with `{c:f_c^(2k+1) is SOS}=(-infinity,c_k]`, determine the limit of `c_k`.

The candidate answers the second clause by `lim c_k=3` and, more strongly, an odd SOS power for every real `c<3`, hence every sufficiently large odd power for each fixed `c`. Those are the claims audited. A different family `M+epsilon(x^2+y^2+z^2)^3` also occurs on the original page; its known positive-definite argument alone does not settle this target.

## Prior sources and status checked now

| Source | Exact version / locator | Verified role and status |
|---|---|---|
| Reznick, _The Odd Powers of the Motzkin Polynomial, etc._ | OWR 14/2023, pp.778–780; original PDF SHA256 `5a9bdc9f9daa12ef35185ceae208c0f2f75e191875827f78b7b6ad0f5cdbf240` | Exact original family and questions; physical p.40 visually inspected. |
| Blekherman–Kozhasov–Reznick (BKR) | [arXiv:2407.21779v1](https://arxiv.org/abs/2407.21779v1), submitted 31 July 2024, Theorems 44 and 47; [publisher version](https://doi.org/10.1017/fms.2026.10221), Theorems 5.3 and 6.3 | Forum of Mathematics, Sigma 14 (2026), e65, online 27 April 2026. Mixed clause and threshold intervals. Publisher PDF SHA256 `f4058ac7b54e498c5b639eb21bf54973b421a9fc7b5ed301b1053e0e594078bb` (666704 bytes). |
| Baldi–Blekherman–Kozhasov–Plaumann–Reznick–Sinn | [arXiv:2602.01191v1](https://arxiv.org/abs/2602.01191v1), submitted 1 February 2026; PDF dated 3 February; Theorem 1.2, Definition 6.3, Theorem 6.4 | Current arXiv history contains v1 only. PDF SHA256 `c91b217bbe413cb934822be9c5f364c75739b38b7bdf178bbf2b764af6ecd0b9`, 648190 bytes. Preprint status corroborated by current author pages. |
| Scheiderer | [author manuscript](https://www.math.uni-konstanz.de/~scheider/preprints/ppss.pdf), Corollary 4.2; [publisher DOI](https://doi.org/10.1007/s00229-011-0484-3) | General projective Positivstellensatz, published online 2011 / journal 2012. The older theorem is an imported ingredient; its age alone does not show that the candidate's cubic-surface application had previously been made. |
| Pinelis | [original MathOverflow answer](https://mathoverflow.net/questions/444079/are-truncated-even-degree-binomial-polynomials-psd), 3 April 2023 | Truncated-binomial positivity ingredient, expressly credited in BKR. |

Current publication-status evidence for _Stubborn Polynomials_: [Blekherman's page](https://sites.google.com/site/grrigg/) lists it as submitted for publication; [Sinn's page](https://wwwuser.gwdguser.de/~sinn3/research.html) labels it a 2026 preprint; [Baldi's research list](https://lorenzobaldi.github.io/pub/) places it under Preprints. The arXiv record/API carries no journal reference or journal DOI. These positive status labels support calling it a preprint; this audit does not infer nonpublication merely from an empty search.

The current arXiv HTML for the stubborn preprint displays an internal date of 24 August 2026, whereas the independently retrieved fixed v1 PDF explicitly says 3 February 2026. The theorem was verified in that fixed PDF, not dated from the later HTML rendering. The submission history still lists only v1; a changed rendering date is not treated as a new arXiv version.

The BKR arXiv PDF remains the 2024 v1 (SHA256 `24de6d87101b210f717e050a82d87e3a29a30b02213cf88899b7872e4b6f490d`). The current publisher version is materially later: its Section 6 acknowledges the 2026 classification, while p.24 still asks whether `lim c_k=3`. Both passages were inspected. The surviving question is evidence about the text, not a logical exception to a theorem that implies its answer. No reliance is placed on abstracts, search snippets, or that unresolved sentence to establish novelty.

## The complete target bridge from the earlier preprint

### Imported theorem

Theorem 6.4 of arXiv:2602.01191v1 says, in paraphrase: a nonnegative ternary sextic which is not SOS and has total real delta invariant at most eight has some odd SOS power. Definition 6.3 computes the local invariant by adding `m(m-1)/2` at the current multiplicity-`m` center and recursing over real infinitely near points of the strict transform. The theorem statement has no extra smoothness, ordinary-node, or general-position hypothesis. Theorem 1.2 summarizes its classification counterpart. The relevant full pages 19–21 and the introductory theorem were read; p.20 was visually inspected.

### Exact family, nonnegativity, and complete real zero set

Fix any `0<c<3` and homogenize:

\[
M_c=x^4y^2+x^2y^4+z^6-cx^2y^2z^2.
\]

AM–GM applied to the first three monomials gives

\[
M_c\ge (3-c)x^2y^2z^2\ge0.
\]

At a real projective zero, `xyz=0`. If `z!=0`, either `x=0` or `y=0` leaves the positive term `z^6`, impossible. If `z=0`, the equation becomes `x^2 y^2(x^2+y^2)=0`. Thus the complete real projective zero set is exactly

\[
P=[1:0:0],\qquad Q=[0:1:0].
\]

This treats all signs and all projective points. It also explains why replacing the original family by a positive-definite perturbation would be an error.

### Non-SOS hypothesis

If `M_c` were SOS, its square roots could be homogeneous cubics. On `y=0`, their squared sum equals `z^6`; viewing each root at `z=1` as a polynomial in `x`, the highest-degree coefficient argument forces each root to be independent of `x`. Thus the terms `x^3,x^2z,xz^2` vanish in every root. Restricting to `x=0` similarly eliminates `y^3,y^2z,yz^2`.

Every cubic root is consequently a linear combination of

\[
x^2y,\quad xy^2,\quad xyz,\quad z^3.
\]

In the sum of their squares the coefficient of `x^2 y^2 z^2` is precisely the sum of the squares of the `xyz` coefficients, hence nonnegative. In `M_c` it is `-c<0`, a contradiction. There is no unsupported Newton-polytope assertion in this argument.

### Uniform real delta calculation, including both blowup charts

At `P`, put `x=1,u=y,v=z`. Start with

\[
F_0=u^2+u^4+v^6-cu^2v^2.
\]

It has multiplicity two, tangent cone `u^2`. Successively use the vertical charts `u=a v`, then `a=b v`, then `b=t v`, each time dividing by the exceptional factor `v^2`. The resulting strict transforms are

\[
\begin{aligned}
F_1(a,v)&=a^2+a^4v^2+v^4-ca^2v^2,\\
F_2(b,v)&=b^2+b^4v^4+v^2-cb^2v^2,\\
F_3(t,v)&=1+t^2+t^4v^6-ct^2v^2.
\end{aligned}
\]

The first exceptional restriction is `a^2`, so its only real point is the origin; the next restriction is `b^2`, again with only the origin. Their multiplicities are two. The tangent cone of `F_2` is `b^2+v^2`. The final restriction is `1+t^2`, which has no real zero.

For completeness, the complementary charts give these strict transforms:

| Center | Complementary substitution and strict transform | Exceptional restriction |
|---|---|---|
| `F_0` | `v=s u`: `1+u^2+s^6u^4-cs^2u^2` | `1` |
| `F_1` | `v=s a`: `1+s^2a^4+(s^4-cs^2)a^2` | `1` |
| `F_2` | `v=s b`: `1+s^2+s^4b^6-cs^2b^2` | `1+s^2` |

Both charts of each blowup therefore cover every real exceptional direction. No real infinitely near point is omitted, including directions associated with older exceptional curves. There are exactly three multiplicity-two centers at `P`, so

\[
\delta_P^{\mathbb R}(M_c)=1+1+1=3.
\]

Symmetry gives the same result at `Q`, hence

\[
\boxed{\delta^{\mathbb R}(M_c)=6<9\quad\text{for every }0<c<3.}
\]

All displayed identities are polynomial identities over `Z[c]`: the argument is uniform in the parameter and is not extrapolation from `c=1`. The preprint itself explicitly discusses `M_1` and its two local invariants equal to three (p.19); the extension to the whole interval is the new application calculation supplied by this audit, not attributed as an explicit source statement.

### Odd powers, all real parameters below three, and the limit

All hypotheses of Theorem 6.4 now hold for each fixed `0<c<3`. Therefore `M_c^m` is SOS for some odd positive integer `m`. Setting `z=1` gives an SOS identity for the exact affine `f_c^m`, with no multiplier or denominator. If `m' >= m` is odd, then

\[
f_c^{m'}=(f_c^{(m'-m)/2})^2 f_c^m
\]

is SOS as well. For `c<=0`, `M_c` itself is the SOS

\[
(x^2y)^2+(xy^2)^2+(z^3)^2+(-c)(xyz)^2.
\]

Thus every real `c<3` has the property required by the candidate. For every such fixed `c`, eventually `c_k>=c`. Conversely, `c>3` gives `f_c(1,1)=3-c<0`, so an odd power cannot be SOS and `c_k<=3`. It follows that

\[
\liminf c_k\ge c\ (c<3),\qquad\limsup c_k\le3,
\qquad\boxed{\lim c_k=3}.
\]

No uniform exponent as `c` approaches three is needed. At `c=3` extra real zeros appear, so the zero-set calculation is deliberately not extended to that endpoint. The argument proves neither a convergence rate nor strict increase of the thresholds, neither of which is the audited conclusion.

## Mixed-exponent clause and its existing credit

BKR's published Theorem 5.3 is the claimed mixed-exponent rule with `a=2i+1,b=2j+1` and exponent `a+b-1`. Its binary-form proof is valid after substituting arbitrary polynomials, so equal degrees or homogeneity of `p,q` are unnecessary. The cases `i=0` or `j=0`, constant polynomials, and the zero polynomial are included. BKR identifies Pinelis's truncated-binomial positivity as its ingredient; the original 2023 MathOverflow answer and the later publication link were independently read. No new authorship is warranted for this clause.

## Priority interpretation, exact gap, and limits of the audit

**Strongest verified finding:** the complete two-clause answer is a direct consequence of earlier mathematical work: the 2024 BKR mixed theorem, subsequently journal-published in April 2026, and the February 2026 sextic classification preprint. The full target-specific bridge is provided above. The central theorem guaranteeing an odd SOS power is prior work; the added AM–GM, coefficient check, six chart substitutions, and liminf argument leave no equivalent or stronger unsupported claim. They are routine finite checks of the earlier criterion.

**What was newly done here:** checking that exact criterion uniformly for this family and drawing the threshold conclusion. This is not evidence that the preprint explicitly stated this application, that the authors knew it, or that no useful alternative proof can be contributed. The candidate's cubic-surface proof may be an independently useful derivation from a published theorem; that does not restore novelty to its final discovery claim. Its generic no-novelty disclaimer is not full credit for the prior classification consequence.

**Exact remaining mathematical gap in the priority bridge:** none, relative to the correctness of the imported Theorem 6.4. This audit independently verifies the application, not the entire unrefereed paper's Del Pezzo theory and all cited foundations. Journal peer review is not asserted for that preprint. No explicit earlier full-answer paragraph was identified in the inspected sources; the positive verdict is consequence-based and does not depend on an inference from search absence.

**Coverage:** the original contribution; BKR v1 relevant complete Sections 5–6 and current published counterparts, including the update and final question; _Stubborn Polynomials_ introductory theorem and complete pp.18–21; Scheiderer Corollary 4.2; current arXiv histories; current three author status lists; Crossref metadata for BKR; the original Pinelis discussion and the 2011 Reznick/Ottem examples. The related 2024 surfaces preprint's overview/main theorem statements were checked as a citation lead; its arbitrary multipliers do not by themselves give an odd power of the same polynomial. Its full proof was not audited. Search coverage and exclusions are recorded in `QUERY_LEDGER.json`; searches are not a completeness certificate for all literature through the audit date.

**Reproducibility and handling:** `verify_bridge.py` passes 20 exact symbolic/pin checks (`BRIDGE_CHECKS.json`). It checks all six chart substitutions, exceptional restrictions, multiplicities, permitted cubic supports and the negative coefficient, uniformly in `c`; it is supplementary rather than formal theorem certification. Full third-party PDFs, text, HTML, rendered pages, and raw API data are confined to ignored `sources/private/`. Only authored analysis, metadata, query/inspection ledgers, scripts, and receipts are public. No human outreach or other-shard communication occurred. Only the parent coordinator received internal findings.
