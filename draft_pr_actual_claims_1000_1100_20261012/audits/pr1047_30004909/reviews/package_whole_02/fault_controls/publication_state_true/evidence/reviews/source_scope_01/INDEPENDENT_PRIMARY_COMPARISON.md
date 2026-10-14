# Independent primary comparison, recorded before earlier audit bodies

Audit subject: PR 1047, problem 30004909 / OWR-8415356-020, submitted head `56b3a35182e5cb04b05e41f5017e47caf50582c1`.

The nine submitted files and original `SUBMITTED_PINS.json` were frozen and hash checked first. Only the submitted `REPORT.md` body has been read. The earlier `SOURCE_AUDIT.md`, `ACCEPTANCE.md`, provenance, status, README, and manifest bodies have not yet been read. This document records the independent conclusions before that comparison. Retrieval metadata and SHA-256 values are in `SOURCES_RETRIEVAL.json`; originals, full extraction, and rendered pages are local ignored materials under `sources/raw/`.

## Source passage and mathematical target

The official EMS report [DOI 10.4171/OWR/2021/53](https://doi.org/10.4171/OWR/2021/53), [full PDF](https://ems.press/content/serial-article-files/46931), has 62 PDF pages. The complete Végh item occupies the upper part of printed page 2946, PDF page 54 (zero-based 53), ending before the next item. The preceding page and following item supply no additional conditions. The target page was both extracted and visually inspected at 1800-pixel resolution.

The passage requires a nonnegative monotone submodular function on `2^V`, zero at the empty set and one on every singleton. It asks for a constant positive factor and one matroid rank with domain `2^V`. Its display is exactly

\[
\frac{r(S)}{\alpha}\le f(S)\le\alpha r(S)\qquad(\forall S\subseteq V).
\]

The left denominator is visibly `alpha`. The text labels the approximating map `f` and the display labels it `r`; this is a local notation inconsistency, resolved by the explicit rank description and display. No weights, scalar multiplier, sum of ranks, larger ground set, or oracle restriction occur in this item. An ordinary rank on `V` is therefore directly supported.

The item does not write an independent universal quantifier over finite `V`. Dimension independence is the conventional reading of its constant-factor question, not a verbatim quantifier. That qualification is essential. Nothing here establishes a different unprinted intention.

## Exact quantifiers under review

Let \(\mathcal F(V)\) comprise all functions satisfying those normalization, monotonicity, and submodularity conditions. The submitted report disproves

\[
\exists\alpha>0\ \forall\text{ finite }V\ \forall f\in\mathcal F(V)\ \exists M\text{ on }V\ \forall S\subseteq V:
\quad r_M(S)/\alpha\le f(S)\le\alpha r_M(S).
\tag{U}
\]

The source's domain and rank class match (U); the placement of `forall finite V` makes the uniform interpretation explicit. The proof remains relevant if “non-integer” is read as an exclusion of integer-valued inputs: use `n >= 2` for the square-root family and `m >= 2` for the rational family. The `n=1` and `m=1` cases simply test boundaries.

The incorrect left comparison `r(S) <= f(S)` is not what the source prints. Replacing the display by that inequality changes the approximation requirement. Rescaling the map to \(\widehat f=r/\alpha\) would yield \(\widehat f\le f\le\alpha^2\widehat f\), but \(\widehat f\) is generally not an ordinary matroid rank. One cannot discard the denominator while retaining the same approximant class and factor.

## Falsification attempt: could the question mean fixed dimension?

For any nonempty `S`, the stated hypotheses imply

\[
1\le f(S)\le |S|.
\]

The lower bound follows from a singleton and monotonicity. Enumerate the elements of `S`; each marginal is at most its singleton value by diminishing returns, giving the upper bound. For fixed nonempty `V` of size `n`, the free matroid rank `r(S)=|S|` and factor `alpha=n` satisfy both comparisons for every normalized input. Thus a factor allowed to depend on dimension is immediate. This is independent mathematical evidence supporting the usual reading of “constant” as uniform over dimensions. It does not turn the omitted source quantifier into an explicit one.

The empty ground set is harmless: the only value is zero and rank zero works for every positive factor. It cannot rescue (U), which fails on arbitrarily large nonempty ground sets.

## Independent proof and hostile checks

For an ordinary finite matroid, rank is maximum cardinality of an independent subset. At a maximum independent subset `B`, put `R=r(V)=|B|`; then `r(B)=R`. No representability, simplicity, graph structure, or symmetry of the approximant is assumed. Singleton comparison forces every element to be a nonloop, hence `R >= 1` and `alpha >= 1`. These conclusions justify every later division.

For \(f_n(S)=\sqrt{|S|}\), normalization and monotonicity are immediate. Its discrete increments

\[
d_k=\sqrt{k+1}-\sqrt{k}=\frac1{\sqrt{k+1}+\sqrt k}
\]

decrease. For `t=|A intersect C|`, `a=|A minus C|`, and `c=|C minus A|`, compare \(\sum_{j=0}^{a-1}d_{t+j}\) with \(\sum_{j=0}^{a-1}d_{t+c+j}\). This proves the full submodular inequality even when one or more parts are empty. The basis and full set respectively force

\[
R/\alpha\le\sqrt R\ \Longrightarrow\ R\le\alpha^2,
\qquad
\sqrt n\le\alpha R\le\alpha^3.
\]

Therefore \(\alpha\ge n^{1/6}\). The dependence of the basis on the approximant causes no circularity: the display applies to every subset, so that particular basis is an allowed test. The full-set comparison uses the same `R`. Arbitrarily many parallel classes do not evade the argument. For each candidate universal positive `alpha`, an integer `n > alpha^6` defeats it; if `alpha < 1`, a singleton already defeats it.

For \(g_m(0)=0\) and \(g_m(k)=1+(k-1)/m\) for `k >= 1`, its increments are `1,1/m,1/m,...`, nonnegative and decreasing when `m >= 1`. The same summation proves submodularity without reliance on the sum-of-ranks characterization. For `n=m^2`, the basis and full-set comparisons give

\[
m\le\alpha+\alpha(m-1)/R,
\qquad
m+1-1/m\le\alpha R,
\qquad R\ge m/\alpha.
\]

Consequently \(m\le\alpha+\alpha^2(m-1)/m\le\alpha+\alpha^2\). Hence

\[
\alpha\ge(\sqrt{1+4m}-1)/2,
\qquad\alpha\ge\sqrt{m/2}=n^{1/4}/\sqrt2.
\]

The `m=1` boundary gives `g_1(S)=|S|`, with the free matroid and factor one. The proof avoids division by `m-alpha`, so there is no missing sign case at `alpha=m` or beyond. The last bound uses `alpha >= 1`. The zero set imposes `0 <= 0 <= 0`. All mathematical bounds in the submitted report survive these tests.

## General mechanism and the intermediate-set challenge

For any nondecreasing discretely concave cardinality function \(\phi\) with \(\phi(0)=0,\phi(1)=1\), a matroid of total rank `R` necessarily needs

\[
\alpha\ge\max\{R/\phi(R),\phi(n)/R\}.
\tag{C}
\]

The uniform matroid of rank `R` attains precisely this factor. Indeed, concavity makes `phi(k)/k` nonincreasing and at most one. For `k <= R`, `k/phi(k)` is bounded above by `R/phi(R)` and `phi(k)/k <= 1`. For `k >= R`, monotonicity bounds `R/phi(k)` by `R/phi(R)` and `phi(k)/R` by `phi(n)/R`. The maximum in (C) is at least one. Thus no overlooked intermediate set defeats the submitted sharpness assertion; no symmetry assumption is needed for the lower bound on arbitrary matroids.

For the square-root family this yields \(\max\{\sqrt R,\sqrt n/R\}\). Minimize over integer `1 <= R <= n`; when `n=m^3`, `R=m` attains `n^(1/6)` exactly. This verifies the claimed family-specific sharpness, without asserting sharpness over all normalized submodular functions.

## Primary crosschecks and comparison to related work

[Goemans's MIT lecture 8](https://math.mit.edu/~goemans/18438F09/lec8.pdf), dated 8 October 2009, PDF page 1 (printed 8-1), gives the basis terminology, maximum-independent-cardinality rank, and equality of basis size to full rank. PDF page 4 (8-4), Definition 5 and Observation 2, gives the rank axioms and diminishing-returns equivalence. Both pages were visually checked. Together with `f(S) <= |S|`, its rank axioms verify the integer-valued observation in the original problem. These are definitions and elementary facts, not claims of research priority.

The entire ten-page [Goemans-Harvey-Iwata-Mirrokni paper](https://www.cs.ubc.ca/~nickhar/papers/SubmodularEverywhere/SubmodularEverywhere.pdf) was read, including body sections 2-7 and references. Problem 1 (PDF 2) asks for an approximant after polynomially many value queries. Section 3 (PDF 5-6, Figure 1) constructs \(\widehat f(S)=\sqrt{\sum_{i\in S}p_i}\); Section 4 (PDF 6) treats a matroid rank as the input. Section 5, Lemma 5 (PDF 7), explicitly uses concave cardinality submodularity. Section 6 (PDF 8-9) proves lower bounds through indistinguishability of rank inputs, rather than nonexistence of a rank approximant. These body locators establish the distinction; the abstract alone is insufficient.

An independent check shows why the related results cannot automatically supply this obstruction. Every monotone hard input constructed in that Section 6 is itself a rank, so if its identity were known it would have a rank approximant with factor one. Its oracle hardness therefore cannot imply an existential obstruction like (U). Conversely the present square-root input is exactly a square-root-of-modular function with all `p_i=1`, so it is already in the related paper's approximant class. The function is not being claimed new. The report's existence question and its elementary proof require no algorithm and no query budget.

This checks the named related paper's formulation and mechanism. It is not an exhaustive priority audit, does not establish absence of other implicit antecedents, and does not exclude derivations from other papers. The primary-source and mathematical decisions are independent of any unresolved priority question.

## Pre-comparison decision

PASS for correctness of the submitted mathematical obstruction to (U), including the stronger rational bound and the square-root family's exact optimum. PASS for the ordinary same-ground-set rank class and displayed denominator. PASS WITH EXPLICIT INTERPRETIVE QUALIFICATION for uniformity over all finite dimensions: the source does not separately quantify `V`, and the report says so. No supported inference about an unknown alternative intended question, and no priority certification.

The only visible source blemish is the source's `f`/`r` naming inconsistency; the submitted display handles it correctly. Earlier record comparison remains to be done after this checkpoint.
