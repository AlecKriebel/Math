# Source gate: next-most-probable Galois groups

Checked: 2026-10-21. Queue row 1852; ID 30005647.

## Verdict

**Recovered, but the source-status rationale needs correction.** The fixed-degree, large-box next-group question is a genuine remaining asymptotic question. It is not equivalent to the already proved order-of-magnitude version of van der Waerden's conjecture. Nor should its status depend on the separate Odlyzko–Poonen conjecture. No new mathematical result is claimed by this gate.

## Original source and extraction boundary

Lior Bary-Soroker, *Past and Present of Probabilistic Galois Theory: A Comprehensive Overview*, in Oberwolfach Report 42/2023, pp. 2468–2469, DOI [10.4171/OWR/2023/42](https://doi.org/10.4171/OWR/2023/42). The workshop ran 24–29 September 2023; the PDF was produced in March 2024. A publication-year label must not change the workshop year.

The report's first paragraph concerns independent uniform coefficients on a growing interval, with degree fixed. The second paragraph explicitly switches to a fixed coefficient distribution and growing degree. The curated original extraction crosses this boundary. The supplied clean statement stays in the first model, but its literature assessment incorrectly combines the two.

The report is an overview, not a fully quantified problem statement: it does not specify monicity or the interval endpoints in this paragraph. The centered monic model below is a literature-supported precise normalization, not a verbatim hypothesis claimed to appear in the overview. The printed page was visually inspected; a grammatical “of” where “or” is intended does not define a third candidate group.

Primary PDF: https://ems.press/content/serial-article-files/47479

## Strict working target

For a fixed integer n >= 5 and positive integer H, choose

f(X) = X^n + a_1 X^(n-1) + ... + a_n,

with all n free coefficients independently uniform on the integers in [-H,H]. Let H tend to infinity, keeping n fixed. The sample space has (2H+1)^n elements. For a separable f, regard its splitting-field Galois group over Q as a permutation group on its n roots, up to conjugacy, not merely as an abstract group.

The strong target is

P_H(G_f is the standard point stabilizer S_(n-1)) / P_H(G_f != S_n) -> 1.

The point-stabilizer event means a rational root together with the full symmetric action on the remaining roots. It is intransitive. This is an **unconditional sample**, allowing reducible polynomials; it is not conditioned on irreducibility, nonzero constant coefficient, or a non-symmetric Galois group. The ratio can equivalently be read as a conditional probability given failure of S_n, but the sampling model itself is unchanged. Conditioning on irreducibility would remove the point-stabilizer candidate and create a different problem.

For a fully robust counting implementation, define the named permutation-group events only on separable polynomials and place every nonseparable polynomial in the exceptional complement; explicitly account for that residual rather than assuming n distinct roots. Do not silently change to sampling irreducibles. The source formula below supplies the cleanest quantitative target for n >= 10; smaller degrees require their appropriate error estimates rather than copying that error term.

## What is proved, and what remains

[Bhargava, Annals of Mathematics 201 (2025), 339–377](https://annals.math.princeton.edu/2025/201-2/p01), proves that the exceptional count E_n(H) is O_n(H^(n-1)). This gives an O_n(H^-1) probability, with the matching lower-order scale supplied by reducible polynomials. The paper was already available as a preprint before the 2023 workshop. Its [expanded arXiv version](https://arxiv.org/abs/2111.06507), v3 dated 28 September 2024, was downloaded and its introductory theorems inspected. The result is an order bound, not an asymptotic equivalence with a specified leading constant or a proof that alternating groups have negligible contribution. The [2024 expository article](https://arxiv.org/abs/2410.03792) also states the order-bound theorem, not a resolution of that remaining distinction.

[Bary-Soroker, Ben-Porath and Matei, *Probabilistic Galois Theory – The Square Discriminant Case*](https://arxiv.org/abs/2207.12493), v2 (1 April 2024), pp. 1–3, makes the distinction explicit. For n > 2 the point-stabilizer probability is asymptotic to c_n/H, c_n > 0. For n >= 10 it records

P(G_f != S_n) = P(G_f = S_(n-1)) + P(G_f = A_n) + O_n(H^-2).

Consequently, the remaining obstruction in this range is P(G_f = A_n) = o_n(H^-1). Its Conjecture 1.1 proposes, for n >= 4, H^(-n/2) << P(G_f=A_n) << H^(-n/2+epsilon). That sharper exponent is conjectural, not proved by the paper's lower-bound constructions. Square nonzero discriminant only forces G_f to lie inside A_n; it does not force equality. Thus an imprimitive square-discriminant family is not automatically an alternating-group family. The paper reports the strong next-group statement known in degrees 3 and 4; these should not be presented as unresolved instances.

A later primary confirmation is David Hokken's contribution, *The Galois group of random reciprocal polynomials*, [OWR 52/2025, p. 2776](https://ems.press/content/serial-article-files/52436). Its background discussion expressly identifies the same O(H^-1) versus o(H^-1) alternating-group gap. Its illustrative coefficient box is [1,H], so this is corroborating status evidence, not a license to identify every interval model or its constants.

Searches through 2026-10-21 found no primary resolution of the general fixed-degree alternating-group gap. This is a bounded literature check, not a proof that no newer result exists. Related reciprocal-family results and the hybrid regime where degree and box size both grow do not settle this fixed-degree target.

## Separate model: a recent status change

The classical Odlyzko–Poonen question chooses f = 1 + sum_(j=1)^(n-1) a_j X^j + X^n, independently uniform a_j in {0,1}, and sends n to infinity. [Breuillard–Varju (2019)](https://arxiv.org/abs/1810.13360) proved a conditional irreducibility result under the Riemann hypothesis for Dedekind zeta functions.

[Constantin Kogler, arXiv:2609.26771v2](https://arxiv.org/abs/2609.26771v2), submitted 22 September and revised 14 October 2026, now states an unconditional proof in this {0,1} model. The PDF's Theorem 1.1 was inspected. This gate records a **current posted theorem claim**, not an independently audited proof or verified journal acceptance. It does not establish the corresponding assertion for every fixed coefficient distribution, and it has no bearing on the fixed-n next-group ratio above. The older blanket status rationale is therefore both model-mismatched and stale.

## Gate outcome and publication boundary

Proceed only with the precise fixed-n large-box residual, preferably explicitly scoped to n >= 10 when using the displayed O(H^-2) decomposition. Do not claim to solve the row by reproving Bhargava's order bound, substituting degree-growth irreducibility, or counting square discriminants without the full-group condition. The full conjectural exponent is a stronger optional target, not a known theorem.

This authored gate and public bibliographic/hash metadata are distinct from copied PDFs, extracted text, images, and private corpus records. Copied source material remains outside the publication set. No repository publication action was performed.
