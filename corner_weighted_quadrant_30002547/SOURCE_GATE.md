# Source/status gate: Growth Rate of Quadrant Loops

Checked 2026-10-20 UTC. Problem ID 30002547; catalog identifier OWR-12872-018.
Scope: source/status recovery performed before the accompanying authored proofs.
This document distinguishes the recovered historical target from the partial results in this package.

## Decision

**Exact target recovered. No resolution of the full parameter range was verified.**

This is a corner-weighted, origin-returning, nonnegative-quadrant model, including negative real weights. It is not the ordinary unweighted quadrant-walk enumeration problem. The radius has a conjectured change of formula at a = −1/2. General positive step-weight theorems, an unrestricted endpoint count, or a related permutation growth theorem cannot be substituted for the requested result.

The historical primary sources inspected present the target as a conjecture. This bounded search is not a certification of present-day openness. The source-recovery review itself makes no new proof or disproof claim.

## Original source and identity

Mireille Bousquet-Mélou's contribution **“Corners in square lattice loops”** is on printed p. 711 of *Enumerative Combinatorics*, Oberwolfach Reports 11 (2014), no. 1, 635–720. It appears in the problem session edited by Svante Linusson. The meeting was March 2–8, 2014; EMS records publication on December 10, 2014.

- [Official bibliographic record](https://ems.press/journals/owr/articles/12872)
- [Official PDF, p. 711](https://ems.press/content/serial-article-files/46502?nt=1#page=77)
- [DOI 10.4171/OWR/2014/12](https://doi.org/10.4171/OWR/2014/12)

The contribution has two conjectures. Its first is positivity in powers of a+1; its second is the present growth/radius question. The second predicts equality of the quadrant and unconfined loop radii for every fixed real a ≥ −1. The algebraic value is supplied by its Albert–Bousquet-Mélou reference.

OWR-12872-018 is a catalog identifier, not a printed problem number. The problem ID, title, DOI and mathematical model were checked against the source.

## Exact model and quantifiers

This is a formal transcription of the recovered model, not a proof attempt.

Let S = {N=(0,1), S=(0,−1), E=(1,0), W=(−1,0)}. Let L_n be the finite set of words w=s_1…s_{2n} on S whose partial sums all lie in Z_{≥0}² and whose final sum is (0,0). Define

    c(w) = #{j : 1 ≤ j < 2n and (s_j,s_{j+1}) is (N,W) or (E,S)},
    Q_n(a) = sum over w in L_n of a^{c(w)},
    Q(a,u) = sum over n ≥ 0 of Q_n(a) u^n,    Q_0(a)=1.

Only adjacent pairs in the linear word are counted: there is no added last-step/first-step junction. The same linear-word convention must be retained for the unconfined comparison. The two letters NW describe a North step followed by a West step, not a northwestern diagonal step. Likewise ES is ordered. Other turns do not automatically receive the weight a. Boundaries are allowed. Paths may revisit vertices and edges and may return to the origin before their final step. There is no self-avoidance, primitiveness, translation quotient, or rotation quotient. The walk is a rooted step sequence.

The quantifier is **for each fixed real a ≥ −1**, with n tending to infinity. It is not an assertion uniform in varying a=a_n, and it does not cover complex a or a<−1.

For the comparison series W(a,u), keep the same origin, endpoint, corner statistic and half-length marking, but remove all intermediate quadrant constraints. An “unconfined loop” is still closed; it is not an arbitrary-endpoint walk.

## Radius, exponential constants, and already established cases

The explicit statement is Conjecture 11, equation (7), in Michael Albert and Mireille Bousquet-Mélou, [*Permutations sortable by two stacks in parallel and quarter plane walks*](https://arxiv.org/abs/1312.4487), European Journal of Combinatorics 43 (2015), 131–164, [DOI](https://doi.org/10.1016/j.ejc.2014.08.024). [Inspected v3 text](https://arxiv.org/html/1312.4487v3), §4, pp. 12–16 and §§4.3–4.4.

    ρ_Q(a) = 1 / (2 + sqrt(2+2a))²,      a ≥ −1/2;
             −a / [2(a−1)²],            −1 ≤ a ≤ −1/2.

Writing μ(a)=ρ_Q(a)^{−1}, the conjectured half-length growth factors are

    μ(a) = (2 + sqrt(2+2a))²,            a ≥ −1/2;
           −2(a−1)²/a,                  −1 ≤ a ≤ −1/2.

Both branches give ρ=1/9 at a=−1/2. At a=−1 and a=1, the radii 1/8 and 1/16 are already proved (Proposition 17). That proposition also gives

    Q_n(−1) ~ (8/π) 8^n n^{−3},
    Q_n(1)  ~ (4/π) 16^n n^{−3}.

Propositions 21 and 22 establish the displayed radius for unrestricted loops and upper-half-plane loops, respectively. Proposition 17 gives the displayed first-branch radius as a lower bound for quadrant loops when a≥0, not a general equality. Beyond a=1, this search did not verify a later theorem establishing equality for every nonnegative a; this is a search limitation, not an assertion that no such theorem exists.

## Interpretation controls for later work

The following are logical safeguards and normalization checks, not new results on the conjecture.

1. **Half-length versus length.** u marks n for a 2n-step loop. An exponential factor per individual step is sqrt(μ), not μ. Using all lengths without accounting for impossible odd-length returns creates spurious zero subsequences.
2. **Radius versus ordinary limit.** The universally valid coefficient characterization is ρ_Q(a)^{−1}=limsup_n |Q_n(a)|^{1/n}. Replacing this with an ordinary limit, or a ratio limit Q_n/Q_{n−1}, needs an additional argument. The primary radius formulation is the safest exact target.
3. **Negative weights.** For −1≤a<0 the polynomial is evaluated as a signed sum. It is not the total absolute weight, not a probability, and not Q_n(|a|). Set inclusion alone no longer compares weighted sums. The separate (a+1)-positivity conjecture must not be assumed as a proved input.
4. **Loops, excursions and bridges.** “Excursion” may name these confined return paths, provided it allows boundary contacts and intermediate returns. “Bridge” may mean merely a fixed-endpoint path with no cone constraint; terminology alone does not identify the same object. “Primitive excursion” would be a different restriction.
5. **Quarter-plane versus half-plane.** The relevant easier half-plane model imposes y≥0 only. A diagonal half-plane model, a wedge of another angle, and an arbitrary starting point are not the same statement.
6. **Endpoint extraction matters.** The arbitrary-endpoint walk series in ABM Proposition 21 has full-length radius 1/(2+sqrt(2+2a)); its square is not the loop radius on −1≤a<−1/2. Thus a proof of the unrestricted-walk growth constant cannot settle the entire loop conjecture. In particular, cancellation can invalidate positive-weight intuition in that interval.
7. **No full-asymptotic claim.** Equality of radii does not determine a prefactor, power-law exponent, logarithmic correction, or a complete asymptotic expansion. The OWR question asks only exponential growth/radius. The general expression Q_n(a)~κ(a)μ(a)^n n^{γ(a)} and convergence of a derivative at the radius are stronger issues, not part of the recovered question. Known formulas at a=±1 must not be promoted to all a.
8. **Weights on corners versus steps.** These weights depend on two consecutive steps. A theorem for products of fixed nonnegative single-step weights is not a direct match, even when its step alphabet and endpoint happen to agree.

## Later literature screened and nonmatches

- William Kuszmaul, [*Signed Enumeration of Upper-Right Corners in Path Shuffles*](https://arxiv.org/abs/1510.00777), [inspected v2 text](https://arxiv.org/html/1510.00777v2), resolves the fixed-projection parity conjecture (ABM (P1)) and proves positivity for a different signed-peak statistic. Its introduction explicitly identifies the solved conjecture; §4 retains further positivity questions. This provides a combinatorial explanation relevant to a=−1, not a proof of the radius formula for every a≥−1. A search result saying that an Albert–Bousquet-Mélou conjecture was solved is insufficient without checking which one.
- Andrew Elvey Price, [*Permutations sortable by deques and two stacks in parallel share the same growth rate*](https://arxiv.org/abs/1912.00056), [inspected text](https://arxiv.org/html/1912.00056v1), proves equality of two permutation-class growth rates (Theorem 2.11). The introduction explicitly says the three ABM quarter-plane conjectures were not proved by that work. Its differently constrained eager/standard walk encodings do not identify the present Q. This is a genuine related resolution, but not this queue item.
- Elvey Price–Guttmann, [*Permutations sortable by deques and by two stacks in parallel*](https://doi.org/10.1016/j.ejc.2016.08.002), reports numerical evidence for the radius and exponents, not a full-range proof. A public publisher search extraction was available; the DOI full-page retrieval failed. It was not treated as fully inspected evidence.
- Dreyfus–Elvey Price–Raschel, [*Enumeration of weighted quadrant walks: criteria for algebraicity and D-finiteness*](https://arxiv.org/abs/2409.12806), [inspected model and main-results section](https://arxiv.org/html/2409.12806v1), uses nonnegative weights assigned to individual steps and studies algebraicity/D-finiteness. That model and theorem goal do not directly resolve the signed corner-weight radius problem. The arXiv record has a September 2024 submission; an August 2026 date displayed by the HTML was not used as proof of a new revision or new resolution.

Searches covered the exact source/catalog titles, quadrant/quarter-plane loops, NW/ES corner weights, ABM Conjecture 11, the piecewise radius, and later work on the identified authors' related models. No inspected primary source supplied a matching theorem over the full interval a≥−1. This is a bounded negative literature finding, not an exhaustive bibliographic certificate.

## Evidence and limitations

The OWR PDF was downloaded, text-extracted, and p. 711 visually inspected. ABM v3 was downloaded and text-extracted; its p. 12 radius formula was visually checked. The other two downloaded preprints were text-extracted; pertinent statements were cross-checked against their primary arXiv HTML.

- OWR PDF: 940719 bytes; SHA-256 dfced400ffd721c7ff977cc9973e493599aba3ddea0741f4c0e2b17b365f2baf.
- ABM v3 PDF: 528344 bytes; SHA-256 ab0a664bd67b1a5e015e2eb6cb2af25c365e455ba024dc8f4b068680b669ce1d.
- Elvey Price v1 PDF: 392211 bytes; SHA-256 20a795dd516ef96566fccbd1b125ffd5001e183392dfbd8dcc4d63380d61aa46.
- Kuszmaul v2 PDF: 235057 bytes; SHA-256 ca5f0ce68f525a5de3d27c05bb46bb4227f0c261f3bd071be021e8e55f575802.

This source/status gate includes authored mathematical transcription, public citations and verification metadata only. No source PDFs, source extractions, page images, dataset records, or private coordination material are included in the publication package. Retrieval and inspection descriptions above record checks made before the accompanying proof attempts; they are not a guarantee of exhaustive literature coverage.
