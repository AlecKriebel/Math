# Source and scope audit

Checked October 3, 2026. All mathematical sources below are primary papers or the official report. Search-result snippets were used for discovery, followed by inspection of full local source texts where theorems are used. Source PDFs and complete extracted texts are excluded from the publication packet.

## Problem and model

- [Designated problem page](https://www.unsolvedmath.com/problems/30002320): attempted first; HTTP 403. A preexisting pinned catalog record supplied the fallback title and formula. It is not independent mathematical evidence.
- [Official MFO report](https://publications.mfo.de/handle/mfo/3349), DOI [10.4171/OWR/2013/18](https://doi.org/10.4171/OWR/2013/18): Amin Coja-Oghlan, “Random graph coloring,” pp.1097–1099. Formula (1), p.1098, and Conjecture 4, p.1099, are decisive. The rendered formula places the nth root inside E. The report uses G(n,m) and average degree; our fixed-density floor convention is stated explicitly. The report belongs to 2013 and was published in 2014. Its unrelated contributions are not reproduced.

## Existing results and exact limits of use

1. Victor Bapst, Amin Coja-Oghlan, Samuel Hetterich, Felicia Rassmann, Dan Vilenchik, [The condensation phase transition in random graph coloring](https://arxiv.org/abs/1404.5513). Inspected arXiv v1, April 19, 2014, especially Section 2.1 and its footnotes, Theorem 2.1, and Section 4.1. Its precise condensation result has k≥k_0, not every k≥3. It explicitly treats the expected nth root and flags threshold convergence as a consequence of an all-density solution.

2. Amin Coja-Oghlan, Florent Krzakala, Will Perkins, Lenka Zdeborová, [Information-theoretic thresholds from the cavity method](https://arxiv.org/abs/1611.00814v4), Advances in Mathematics 333 (2018), 694–795, DOI [10.1016/j.aim.2018.05.029](https://doi.org/10.1016/j.aim.2018.05.029). Inspected Theorem 1.2 and Section 4.3. It gives the below-condensation formula for every q≥3 and an above-condensation deficit. Neither the boundary nor the all-density expected-root limit is asserted. Section 4.3 expressly handles the obstacle from zero interaction weights rather than importing the positive-weight theorem unmodified.

3. Mohsen Bayati, David Gamarnik, Prasad Tetali, [Combinatorial approach to the interpolation method and scaling limits in sparse random graphs](https://arxiv.org/abs/0912.2444), Annals of Probability 41 (2013), 4080–4115, DOI [10.1214/12-AOP816](https://doi.org/10.1214/12-AOP816). Inspected Section 2's model conventions, Theorems 1–2, and Remark 3. The pressure theorem uses finite λ, and its zero-temperature coloring optimization counts satisfied edges. Their auxiliary with-replacement model is not silently substituted for a loop-free simple graph when discussing exact coloring counts.

4. Dimitris Achlioptas and Ehud Friedgut, [A sharp threshold for k-colorability](https://cgi.di.uoa.gr/~optas/papers/k-col-threshold.pdf), Random Structures & Algorithms 14 (1999), 63–70. Theorem 1.1 is about a sharp sequence for each k≥3. It does not prove that the sequence itself converges. Our proof uses only its separated, one-sided high-probability assertions.

5. Peter Ayre, Amin Coja-Oghlan, Catherine Greenhill, [Lower bounds on the chromatic number of random graphs](https://arxiv.org/abs/1812.09691), Combinatorica 42 (2022), 617–658. Inspected the [authors' paper](https://web.maths.unsw.edu.au/~csg/papers/ACG-interpolation.pdf), especially Theorem 1.3 and Section 2. These are non-colorability bounds and soft-partition-function tools, not an all-density formula for the hard-coloring count.

## Prior-attempt and publication checks

The live main queue was fetched and its rank-503 entry was queued, 0/5. Repository PR/issue searches by problem ID and PR searches by problem number and title phrase found no genuine same-problem attempt. A repository code search by ID returned no matches; this negative indexed search is not treated as proof that every branch was searched. No duplicate was identified from the inspected records.

The substantive public claims are bounded accordingly: no all-density solution was found in the sources checked. This is not a guarantee of exhaustive literature coverage. No remote write, branch, commit, PR, queue mutation, or queue-generation command was used by the author stage.
