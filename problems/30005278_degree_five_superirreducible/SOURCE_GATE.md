# Source/prior-attempt gate: 30005278 / OWR-11695860-018

2 October 2026. Rank 369. This gate consumes zero substantive author turns. No prior campaign attempt was recovered. The mathematical target below is eligible for a fresh five-turn attempt.

## Exact source and conventions

The full source is Trevor Wooley's Question 9, attributed to J. Bober, D. Fretwell, G. Kopp, L. Du and T. Wooley, in *Analytic Number Theory*, OWR 50/2022, printed p.2945 (PDF page 51). Primary PDF: https://ems.press/content/serial-article-files/46986 ; publisher https://ems.press/journals/owr/articles/11695860 ; DOI https://doi.org/10.4171/OWR/2022/50 . Report citation: Oberwolfach Reports 19(2022), no.4, pp.2895–2960. Publication was 27 July 2023, so the imported 2023 citation and 2022 report year refer to different valid dates. The whole problem was read and the exact printed page visually inspected.

The printed shorthand asks whether a degree-five integer polynomial remains irreducible under every integer-polynomial substitution of degree at most two. Its omission of “positive degree” is resolved by the same authors' explicit later definition: degrees one and two, with irreducibility tested over the fraction field Q. Constants and content factors are not counterexamples to the intended problem. The published finite-field paper's first page explicitly defines weak k-superirreducibility over a domain using irreducibility over its fraction field. This is stronger source evidence than inferring an artificial negative answer from the shorthand.

Accordingly the target is: find f in Z[x], degree five, such that f(g(x)) is irreducible in Q[x] for every g in Z[x] with 1 <= degree(g) <= 2. Integer g and rational g are different quantifier classes; a rational-substitution counterexample need not settle the integral question. Nonzero scalar factors of f do not matter under this convention.

The requested UnsolvedMath page was attempted but inaccessible. The complete pinned imported record was read. Its August 2026 literature triage is credited background, not a prior attempted proof; the separate research-results entry is null.

## Current primary literature and credited inputs

- Lara Du, *2-superirreducibility of univariate polynomials over Q and Z*, https://arxiv.org/abs/2409.16206v2 , posted 17 June 2025 (PDF front-page date June 18). The introduction and complete Section 6 were read, together with the composition criterion. The paper leaves odd degree unresolved and proves that x^(2k+1)+2x+1, k>=2, remains irreducible after substitutions ax²+c with a,c integers and a nonzero. That is a prior theorem, not a new result here. Its use of “weakly” in Section 6 differs from the finite-field paper's definition; the explicit substitution class will always be stated.
- J. W. Bober, L. Du, D. Fretwell, G. S. Kopp and T. D. Wooley, *On 2-superirreducible polynomials over finite fields*, Indagationes Mathematicae 36(3)(2025), 753–763, DOI https://doi.org/10.1016/j.indag.2024.08.005 , https://arxiv.org/abs/2309.15304 . Author PDF https://www.math.purdue.edu/~twooley/publ/20230927superirred.pdf . The definition, Lemmas 2.2–2.3 (credited to Capelli), odd-degree finite-field obstruction and p-adic discussion were read. No finite-field or p-adic 2-superirreducible polynomial exists in the relevant odd-degree setting; this does not give the integral answer.
- The exact Capelli criterion is: for irreducible f with root theta, f(g) is irreducible over Q iff g(x)-theta is irreducible over Q(theta). For g=ax²+bx+c, the obstruction is whether b²−4ac+4a theta is a square in that root field. The field is Q(theta), not the full splitting field. Du's Section 6 occasionally says “splitting field” while representing elements in the power basis of theta; any use here is explicitly in the root field, with a direct local proof of denominators when needed.
- Du's polynomial irreducibility input is credited to Perron's criterion. A self-contained specialized verification may be supplied for reproducibility, without claiming novelty. Published even-degree examples and Schinzel's degree-minus-one obstruction do not resolve degree five with quadratic substitutions.

Bounded current exact-code/title/topic searches and primary author publication checks recovered no later full resolution. This is not a global proof that none exists. The accessible v2 primary manuscript, rather than secondary bibliographic dates, fixes the exact credited theorem used here.

## Campaign prior gate

Fresh recovered-head artifact scans examined 374 remote refs for the ID, source code, superirreducible and superirreducibility aliases: no target artifacts or matching branch names. The all-ref commit-message scan also returned none. Four live all-state PR searches (ID, source code, superirreducible, superirreducibility) each returned zero. The recovered related-target-groups file has no matching group. These checks do not exclude possible uncommitted or unindexed work. Source imports and upstream literature are not Alec/campaign attempts.

Raw primary PDFs, extracted source text/images, imported records and retrieval logs remain local-only. Public artifacts may contain proofs, exact controls, source links and hashes.
