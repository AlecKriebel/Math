# Source gate: row 1835, ID 30000859, OWR-1731-004

**Finding: already solved in the literature for the intended nondegenerate model.** No new proof or new open problem is claimed. Inspection date: 2026-10-21 UTC.

## Original question

Jakob Erik Björnberg, “Open problem: Is there a RSW theorem for anisotropic percolation?”, Arbeitsgemeinschaft: Percolation, Oberwolfach Report 48/2007, pp. 2888–2889. [Official report](https://publications.mfo.de/bitstream/handle/mfo/3034/OWR_2007_48.pdf?isAllowed=y&sequence=1); [EMS article](https://ems.press/journals/owr/articles/1731), DOI 10.4171/OWR/2007/48.

The model is independent nearest-neighbor bond percolation on the square lattice, with fixed horizontal/vertical opening probabilities p_h,p_v and p_h+p_v=1 (critical and self-dual). Write H(a,b) for horizontal crossing of [0,a]×[0,b]. The question requests a positive scale-independent lower bound for P(H(n,n)), and corresponding bounds for P(H(kn,n)) for each fixed integer k. The conditional rectangle-extension step was already known; the missing square bound was the issue. Alternative formulations ask for shapes supporting both ingredients, or improvements to a function f with simultaneous lower bounds for H(n,f(n)) and H(f(n),n), particularly a nonzero finite limiting ratio n/f(n).

## Exact resolution and matching

Geoffrey R. Grimmett and Ioan Manolescu, *Inhomogeneous bond percolation on square, triangular and hexagonal lattices*, Annals of Probability 41(4) (2013), 2990–3025, DOI [10.1214/11-AOP729](https://doi.org/10.1214/11-AOP729). [Author-hosted published PDF](https://www.statslab.cam.ac.uk/~grg/papers/AOP729.pdf); [2011 preprint record](https://arxiv.org/abs/1105.5535).

Equation (1.1), p. 2993, gives κ_square(p)=p_h+p_v−1. Theorem 1.3(a), p. 2995, establishes the box-crossing property whenever p∈(0,1)^2 and κ_square(p)=0. Definition 1.2, p. 2994, supplies a positive lower bound for both crossings of every fixed-aspect-ratio box at all sufficiently large scales. Section 1.2 identifies exactly the same independent orientation-dependent square-lattice model. The introduction, p. 2991, cites the earlier problem, and reference [4], p. 3024, explicitly identifies Björnberg's contribution.

**Our deduction:** setting aspect ratio k proves the requested rectangle bounds; aspect ratio 1 gives the square bound. The finitely many smaller integer scales have strictly positive probabilities and can be absorbed by reducing the constant. Taking f(n)=n meets the final formulation, with n/f(n)=1. Constants may depend on the fixed parameters and aspect ratio.

## Scope safeguards

The open endpoints (p_h,p_v)=(0,1),(1,0) are excluded: one crossing direction is then impossible. This is necessary nondegeneracy, not an unresolved exception. The original prose does not explicitly list that restriction, so literal inclusion of endpoints would make its desired conclusion false. The resolution concerns RSW, not Cardy's formula, conformal invariance, or existence of critical exponents. No uniform positive constant over all anisotropies is asserted.

## Inspection and provenance

The original report and the published resolution were retrieved and inspected on 2026-10-21 UTC. The original question (MFO p. 2888) and resolution theorem (p. 2995) were visually inspected using local PDF renderings after web PDF screenshots failed with cache-miss errors. The official MFO copy prints the question at pp. 2888–2889; the EMS-served PDF prints it at pp. 2828–2829. This pagination difference does not change the mathematical question.

SOURCE_METADATA.json records the public URLs, byte counts and SHA-256 hashes of the three inspected PDFs. This package contains no copied PDFs, extracted source text or source page images. The mathematical account above is an authored summary and deduction, not a reproduction of those sources.
