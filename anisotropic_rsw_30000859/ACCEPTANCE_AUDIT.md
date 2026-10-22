# Acceptance audit: anisotropic square-lattice RSW

- Dataset row: 1835; problem ID: 30000859; source key: OWR1731-004.
- Disposition: **already_solved**; turns: **1/5**.
- Scope: literature resolution of the nondegenerate problem, not a new proof claim.
- Audit date: 2026-10-21.

## Original problem and primary sources

Jakob Erik Björnberg's 2007 question concerns independent bond percolation with fixed horizontal/vertical parameters satisfying ph + pv = 1. Writing H(a,b) for a horizontal open crossing of [0,a] × [0,b], it asks for a scale-independent positive square-crossing bound and extension to fixed-aspect rectangles. Its final formulation asks whether an auxiliary f(n), giving positive bounds for both H(n,f(n)) and H(f(n),n), can have n/f(n) tending to a nonzero finite limit. The report already explains that the conditional rectangle extension is available; the missing input was an a-priori square bound.

Primary original: [Oberwolfach Report 48/2007](https://publications.mfo.de/bitstream/handle/mfo/3034/OWR_2007_48.pdf?isAllowed=y&sequence=1), pp. 2888–2889; [EMS record](https://ems.press/journals/owr/articles/1731), DOI 10.4171/OWR/2007/48. The MFO and EMS copies have different printed pagination; these locators refer to MFO.

Resolution: Geoffrey R. Grimmett and Ioan Manolescu, *Inhomogeneous bond percolation on square, triangular and hexagonal lattices*, Annals of Probability 41(4) (2013), 2990–3025, [DOI](https://doi.org/10.1214/11-AOP729), [published author-hosted PDF](https://www.statslab.cam.ac.uk/~grg/papers/AOP729.pdf), [preprint record](https://arxiv.org/abs/1105.5535).

## Exact theorem match

Equation (1.1), p. 2993, defines the square-lattice critical expression as ph + pv − 1. Theorem 1.3(a), p. 2995, establishes box-crossing for every p in (0,1)^2 where this expression vanishes. Definition 1.2, p. 2994, means that for each fixed positive aspect ratio there is a positive bound, uniform over sufficiently large integer scales and all translated/rotated boxes, for crossings in both directions. The embedding is the ordinary square lattice Z². The introduction, p. 2991, identifies this previously open question; reference [4], p. 3024, explicitly names Björnberg's report. This is not merely a title match.

## Theorem-to-question deduction

Fix ph,pv in (0,1), ph+pv=1. Apply the theorem with aspect ratio 1. Each square has an open horizontal crossing with probability at least δ(p)>0 for all sufficiently large integer n. For the finitely many omitted n, the event that a specified horizontal row is open has probability ph^n>0. Taking the minimum of these finitely many positive probabilities and δ gives an all-n constant c1(p)>0.

For every fixed integer k≥1, use aspect ratio k and repeat the finite-scale argument. This gives ck(p)>0 with P(H(kn,n))≥ck(p) for all n≥1, without assuming rotational invariance of the anisotropic measure. Vertical crossings follow from the same box-crossing definition, not by falsely identifying a rotated law with the original law.

Now take f(n)=n. Both events in the report's final formulation become H(n,n), and n/f(n)=1 identically. Thus the requested nontrivial limiting aspect ratio is obtained exactly. Squares and fixed-aspect rectangles already supply the requested class of shapes; no elongated-diamond theorem is needed.

## Dual crossings and the optional upper bound

The original question asks for positive lower bounds. The usual two-sided version also follows. Declare a dual edge open precisely when its crossing primal edge is closed. A horizontal dual edge crosses a vertical primal edge, so the dual parameters, in horizontal/vertical order, are (1−pv,1−ph)=(ph,pv). The dual lattice is a translate of Z². Consequently it has the same box-crossing property.

Here is an explicit boundary-safe argument for H(m,n), with m=kn. A dual top-to-bottom crossing confined to [1/2,m−1/2] × [−1/2,n+1/2] blocks every primal left-to-right crossing in [0,m] × [0,n]. For large n, this dual strip contains a box of height N=n+1 and width (k/2)N, with its top and bottom at those same heights. Definition 1.2 gives a uniformly positive probability for a vertical dual crossing of this narrower box. Therefore P(H(kn,n))≤1−η(p,k) for large n. At finitely many remaining scales, closing every horizontal edge across a fixed vertical cut has positive probability, so the upper bound extends to all n. The vertical version interchanges coordinates and parameters. No unsupported exact complement identity for identically sized primal/dual rectangles is used.

## Limitations checked

- Constants depend on the fixed parameter pair and aspect ratio. This is not uniform over anisotropies approaching the endpoints, nor over aspect ratios tending to zero or infinity.
- The original report does not explicitly exclude (0,1) and (1,0). The nondegenerate interpretation is necessary: at ph=0 every positive-width horizontal crossing fails; at ph=1 horizontal crossings are deterministic and vertical crossings fail. These deterministic endpoints do not support two-direction/two-sided RSW.
- For example, P(H(1,1))=1−(1−ph)^2 tends to zero as ph tends to zero. Hence a single positive all-scale lower bound over the entire open critical segment cannot be inferred.
- The theorem's definition is a sufficiently-large-scale assertion for arbitrary translated/rotated boxes. The all-n upgrade above is only asserted for the lattice-aligned integer rectangles in the original question.
- This audit does not claim Cardy's formula, convergence of crossing probabilities, conformal invariance, an effective formula for the constants, or a new mathematical proof.

**Acceptance:** the intended fixed, nondegenerate anisotropic RSW problem is resolved by the cited published theorem. The correct queue disposition is already_solved, 1/5, with the endpoint and parameter-dependence qualifications retained.
