# Source gate: extremality-testing complexity

Checked 20 October 2026. Queue row 1827; ID 30002723; OWR-13353-006.

## Initial literature-gate verdict

This report predates the authored proof in this package. Its open-for-research verdict concerns the bounded literature search, not the later manuscript review; see ../ACCEPTANCE_REPORT.md for the current package disposition.

**Source identity recovered; no verified resolution found. Retain the problem as open for research, not solved.** This is the single-row, rational-data, piecewise-linear extremality-testing complexity question. Decidability and a bound polynomial in a numerical denominator are already known. Neither the newer grid-free methods inspected nor the 2025 two-dimensional result establishes a polynomial bound in the binary encoding length for this target.

This is a literature/source gate only. No proof attempt, queue change, publication, or claim of new mathematics was made. The conclusion that no resolution was found is a bounded search finding, not a proof that none exists.

## Original source and chronology

The source is Matthias Köppe's contribution, “The Gomory–Johnson infinite group problem: A 42-year update,” pp. 2898–2901, in *Combinatorial Optimization*, Oberwolfach Reports 11 (2014), no. 4, pp. 2873–2932, DOI 10.4171/OWR/2014/51. The workshop ran 9–15 November 2014; EMS records publication on 29 October 2015. Thus the record's 2014 proposed year and 2015 publication wording are compatible.

On printed p. 2899, within the **single-row** discussion, the report asks whether the pseudo-polynomial running time of the first extremality algorithms is optimal. Its reference [2] is the Basu–Hildebrand–Köppe one-dimensional paper. The adjacent continuous-function oversampling theorem is a separate statement, not a restriction silently imposed on the preceding complexity question. Page 2899 was also visually inspected in the downloaded PDF.

- [EMS article and publication dates](https://ems.press/journals/owr/articles/13353)
- [Original report PDF, p. 2899](https://ems.press/content/serial-article-files/46541)

## Mathematical target and input representation

The underlying relaxation is

\[
R_f(\mathbb R,\mathbb Z)=\operatorname{conv}\{y:\mathbb R\to\mathbb Z_{\ge0}:\operatorname{supp}(y)\text{ finite},\ \sum_r r y(r)\in f+\mathbb Z\}.
\]

A nonnegative valid function \(\pi\) gives \(\sum_r\pi(r)y(r)\ge1\). Minimality excludes a different valid function pointwise below it. Extremality asks whether \(\pi=(\pi^++\pi^-)/2\), with valid \(\pi^\pm\), forces equality. The competing functions are **not** assumed to share the input's breakpoints or be piecewise linear. The usual minimality conditions are periodicity modulo 1, \(\pi(0)=0\), nonnegativity, subadditivity, and \(\pi(x)+\pi(f-x)=1\). [Part VII, §§1.2–1.4](https://ojmo.centre-mersenne.org/item/10.5802/ojmo.16.pdf)

For a concrete bit-complexity formulation, use rational \(f\in(0,1)\), a finite sorted list \(0=b_0<\cdots<b_n=1\), and the rational point values and left/right limits at the breakpoints. Interpolate affinely on each open interval and extend periodically. Endpoint data must be compatible with periodicity. The promise is that \(\pi\) is minimal valid. Discontinuities, including two-sided discontinuity at zero, are permitted. This finite representation agrees with the data model explained in [Part V, §3](https://arxiv.org/html/1609.04982v2).

**Encoding qualification:** the OWR paragraph does not itself specify a formal language or bit encoding. The all-rational sparse-list formulation above makes explicit the rational-data complexity question in the cited literature; it is not a verbatim extra hypothesis from OWR. It must be fixed before a hardness or polynomial-time claim is assessed.

## Existing theorem versus the unresolved complexity target

Basu–Hildebrand–Köppe, Part I, Theorem 1.3, permits piecewise-linear minimal valid functions with rational breakpoints, including discontinuous ones. With \(q\) the least common denominator of those breakpoints, its bound is polynomial in \(q\) **elementary operations over the reals**. This is not stated as a polynomial bit-time theorem. The introductory complexity discussion then explicitly restricts to all-rational input and asks about polynomial or strongly polynomial algorithms. Weak NP-hardness is conjectured there, not established.

For the explicit representation above, let \(L\) be the total binary length of the breakpoint, value/limit, and right-hand-side data. The unresolved efficient-algorithm target is \(\operatorname{poly}(L)\), rather than \(\operatorname{poly}(q)\). Replacing the sparse input by all \(q\) grid entries can enlarge it exponentially and changes the complexity question. Strong polynomiality is a distinct, stronger target; it should not be confused with ordinary polynomial bit complexity.

- [Part I, Theorem 1.3 and introductory complexity discussion, pp. 5–8 of arXiv v2](https://arxiv.org/html/1206.2079v2)
- [Survey, §7.2, Theorem 7.1 and Open Question 7.2](https://arxiv.org/pdf/1410.8584v2)

## Later results checked and why they do not close this row

1. **Continuous oversampling.** OWR p. 2899 and the survey describe reduction to a finite grid with fixed oversampling factor \(m\ge3\), with \(f\) and the breakpoints on the \(1/q\) grid. This yields a finite test for continuous input, but its grid size still depends on the numerical value of \(q\). It is neither a solution of the binary-size question nor permission to discard discontinuous inputs. [Survey, §8](https://arxiv.org/pdf/1410.8584v2)

2. **Grid-free software.** Hong–Köppe–Zhou, Part V, describes a practical grid-free tester and empirical weak dependence on \(q\). The inspected paper does not provide a worst-case polynomial-in-\(L\) guarantee. Good behavior for huge denominators is not that guarantee. [Part V, introduction and §7](https://arxiv.org/html/1609.04982v2)

3. **Inverse-semigroup theory.** The published 2022 Part VII gives finite presentation of the rational moves closure in Theorem 72, with a finiteness argument rather than a polynomial bit-size bound. Its perturbation-decomposition results impose one-sided continuity at the origin, and §12.2 explains the two-sided-discontinuous obstruction. Section 12.1 and reference [15] describe Part VIII as a forthcoming computational companion/manuscript. No verified public Part VIII resolution of the complexity question was found. [Published Part VII, Theorem 72, §10.1, §12](https://ojmo.centre-mersenne.org/item/10.5802/ojmo.16.pdf)

4. **Two-dimensional progress.** Hildebrand–Köppe–Xu's 2025 preprint, Theorem 7.1, handles continuous piecewise-linear minimal functions on the specified standard unimodular triangulation \(\mathcal P_q\) of \(\mathbb R^2\), with \(f\in q^{-1}\mathbb Z^2\). The concluding paragraph explicitly discusses time polynomial in \(q\). It removes the earlier diagonal-constrained restriction, but is not an arbitrary-dimensional result and does not solve this one-row bit-complexity question. The arXiv record inspected lists v1, submitted 9 January 2025. [Part IV](https://arxiv.org/abs/2501.05582), [full text](https://arxiv.org/html/2501.05582v1).

## Audit boundaries and provenance

The recovered local corpus contains exactly one matching problem record and no matching research-result record. Both dataset copies were freshly hashed; this was not a fresh upstream dataset fetch. The queue's ID, source key, title, and row number agree. Raw dataset extracts, downloaded PDFs, text extraction, and the page image remain separate from this authored report.

Targeted searches included extremality with polynomial-time, pseudo-polynomial, weak NP-hardness, bit complexity, grid-free Part VIII, and 2024–2026 date terms. The current author research page and the 2025 paper's recent-literature discussion were checked. No claimed general polynomial-bit-time algorithm or verified weak-NP-hardness proof for the exact one-row target was located. [Author research index](https://www.math.ucdavis.edu/~mkoeppe/art/infinite-group/)

**Scope requirements:** preserve the rational sparse-list encoding, minimality promise, possible discontinuities, and unrestricted valid-function competitors. Any result only for a fixed grid, continuous subclass, algebraic-irrational representation, or higher-dimensional triangulation must be labeled as such rather than accepted as a solution to this row.
