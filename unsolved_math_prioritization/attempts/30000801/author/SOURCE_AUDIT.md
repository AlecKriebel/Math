# Source and literature audit

Checked 2026-10-06 UTC. No full resolution of the exact target was verified in
this search. This is a bounded literature search, not a proof that none exists.
No external communication or remote repository mutation was performed.

## Exact original source

Michael Struwe's contribution, “Quantization for a fourth order equation with
critical exponential growth,” appears on pp. 2071–2073 of Oberwolfach Report
35/2007, *Partielle Differentialgleichungen*, workshop July 22–28, 2007.
The equation, positive constant λ_k, energy, Navier conditions, bubble scaling
96, and quantum 16π² were inspected in the official PDF. Page 2071 was also
visually inspected to avoid superscript/OCR errors. The question is on p. 2072.

- Report: https://doi.org/10.4171/owr/2007/35
- Official PDF: https://ems.press/content/serial-article-files/46122
- Catalog page: https://www.unsolvedmath.com/problems/30000801

The catalog page could not be read live (HTTP 403 / web internal error). The
complete previously supplied corpus record was reviewed instead, together with
the original PDF. Its corrected statement matches the target equation. Its
legacy original statement and background contain incompatible nonlinearities;
those were not used. The report was held in 2007; a bibliographic display of 2008
must not be interpreted as a different workshop or problem.

The source's selected-center index I is not explicitly the cardinality of the
set of distinct limit locations. Relative-scale separation does not imply
separation of those limits. This distinction is retained in PROOF.md.

## Nearby results and scope checks

1. **Struwe (2007), Math. Z. 256, 397–424.** Theorem 1.2 proves integer energy
   quantization for the exact positive Navier equation. It does not prove L=I;
   the introduction explicitly raises the stronger question. The inspected
   author PDF is dated September 5, 2006. The publication DOI is
   https://doi.org/10.1007/s00209-006-0081-4 and the author PDF is
   https://people.math.ethz.ch/~struwe/CV/papers/ConcEner.pdf.
   An ETH repository request for the publisher-layout PDF returned HTTP 429;
   that version was not downloaded or treated as byte-inspected.

2. **Robert (2007), Proc. Roy. Soc. Edinburgh A 137, 531–553.** The inspected
   author version is dated January 6, 2006, revised June 12, 2006. Its Theorem 1.2
   concerns Δ²v_k=V_k e^(4v_k), V_k→1 locally uniformly, bounded nonlinear mass,
   a global L¹ bound on the negative part of its sign-convention Laplacian, and
   a local L¹ bound on that Laplacian. Its atoms have positive integer
   multiplicities; they need not all be one. Robert uses Δ=-Σ∂²; this reverses
   the second-order sign relative to PROOF.md, not Δ². This theorem cannot be
   transplanted by replacing v with u²/2 (APPROACHES.md, route 2).
   https://doi.org/10.1017/S0308210506000096
   https://iecl.univ-lorraine.fr/wp-content/uploads/2021/04/RobertExpQuanti.pdf
   https://arxiv.org/abs/math/0512148 (v1 submitted December 7, 2005; earlier
   arXiv version, not assumed identical to the inspected revised author PDF).

3. **Martinazzi–Struwe (2012), Math. Z. 270, 453–487 per arXiv metadata.**
   Theorem 2 proves integer quantization for order 2m with clamped Dirichlet
   data u=∂_n u=…=∂_n^(m−1)u=0. It is not the Navier condition. The inspected
   January 25, 2010 author version separately identifies simplicity, isolation,
   and boundary exclusion as open issues for its critical squared exponential.
   Its discussion of Wei's simpler exponential equation adds convexity in the
   Navier case; no arbitrary-domain transfer is made here.
   https://arxiv.org/abs/1003.1329 (v1, March 5, 2010)
   https://doi.org/10.1007/s00209-010-0807-1
   https://people.math.ethz.ch/~struwe/CV/papers/Quantization-2m.pdf

4. **Druet–Thizy (2020), JEMS 22, 4025–4096.** The 2017 preprint's Theorem 1.2
   is a two-dimensional, second-order theorem. Its coefficients converge in C¹,
   have uniformly bounded second derivatives, and have a positive limit.
   The detailed planar concentration result does not settle order four in R⁴.
   https://arxiv.org/abs/1710.08811
   https://arxiv.org/pdf/1710.08811

5. **Chen–Deng (2026), arXiv:2608.03321.** The primary abstract states a
   nonlocal Choquard exponential equation on C⁶ domains with positive C⁴
   coefficient K. It constructs solutions from stable critical configurations
   and makes local uniqueness/index assertions under nondegeneracy. Its
   equation and mass 8π²(8−α) differ from the target, and its arXiv page lists
   no journal reference. Only the abstract and version metadata were inspected;
   this is not an audited proof and not a resolution of the present problem.
   https://arxiv.org/abs/2608.03321 (v1, August 4, 2026)

The appearance of “strong energy quantization” in work on biharmonic maps also
has a different meaning (a Lorentz-space/no-neck property for a manifold-valued
problem). It does not by its title establish one bubble for this scalar equation.
No conclusion here relies on that adjacent literature.

## Prior actual work

Read-only GitHub code and PR searches for the numeric ID, problem code, Navier,
and quantization returned no actual attempt. The current attempts directory
listed 65 children and no target child; public history, assessment history, and
state files had no target match. The current queue row remained queued, 0/5.
The related-target grouping did not include this ID. Complete corpus review
found an absent report, represented by {}, and verified the catalog's review
hash and statement hash. These are evidence of no *found* prior substantive
attempt, not a claim that every branch or private record was searched. Desk
review and catalog inclusion alone were not used to skip the problem.
