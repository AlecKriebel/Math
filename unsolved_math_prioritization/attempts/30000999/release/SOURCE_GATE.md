# Source and prior-work gate

Checked 3 October 2026 for problem 30000999 / OWR-2042-008.

## Exact source

The direct problem URL, https://www.unsolvedmath.com/problems/30000999, was attempted first and was unavailable through the web tool. A pinned local catalogue record supplied the provisional statement and source pointer. It was not treated as an independent mathematical authority. No matching record was found in the separate cached research-results map.

The official [Oberwolfach Report 31/2008](https://ems.press/content/serial-article-files/46174) was then independently retrieved and its relevant pages read. The PDF's title page gives *Calculus of Variations*, 6–12 July 2008; the report occupies printed pp. 1707–1770. Benjamin K. Stephens's contribution, “Measuring the Geodesic Radon Transform with Mass Transport,” begins on p. 1762, states the transform, distance and reverse question on p. 1763, and ends with references on p. 1764. DOI: https://doi.org/10.4171/OWR/2008/31.

Printed p. 1763 was also rendered and visually inspected. The official PDF SHA-256 was 15854a33755fcaae9620944f730823932f48c32f6a56b9ce057c0b1b5862e54f. The source PDF and its full extraction are not part of the release payload.

The source defines the measure operator as the dual of normalized equator averaging, uses intrinsic spherical transport distance, and gives 1 <= p < infinity. It discusses a forward contraction estimate and then asks for a uniform inverse bound. There is no evenness or support restriction in this passage. The contraction formula assumes the usual n >= 3 setting; the elementary normalized two-point equator construction also defines R for n = 2. The case n = 1 is undefined. The main negative theorem covers every dimension in the source setting.

The source really contains the reverse question. The catalogue's claim that the available extract was merely an incomplete fragment misses the question at the bottom of p. 1763. Its source-citation label “(2009)” conflicts with the report's 2008 title/date. Neither mismatch affects the source-verified mathematical formulation.

## Literature and novelty limits

The loss of the odd part is classical. [Michael Quellmalz (2020), DOI 10.1007/s13324-020-00383-2](https://doi.org/10.1007/s13324-020-00383-2), Sections 2.2.2 and 4, treats the normalized equatorial Funk transform and its odd nullspace. Its introduction and Section 6 discuss the classical Sobolev smoothing degree (n-2)/2 and credit earlier work. These facts explain both the elementary antipodal failure and the high-frequency even-density obstruction.

The finite-order Wasserstein estimate in PROOF.md is derived directly, using classical harmonic moments and an explicit smooth transport flow. This investigation did not locate an exact prior published statement of that strengthened theorem. The search was bounded, so historical novelty and priority remain unverified. No first-resolution claim should be attached to this note. In particular, Theorem 1 is an immediate application of the well-known parity obstruction, not a new injectivity theorem.

## Bounded same-problem duplicate check

- The retrieved main-branch QUEUE.md row 499 remained queued, 0/5, with no linked attempt or DOI. Its returned file blob was c87c275c638939b8008fd58db80657491d14971e.
- GitHub PR searches scoped to AlecKriebel/Math for the problem ID returned no result. Searches for Radon and Wasserstein returned unrelated work, including signed-measure Euclidean Cramer–Wold extensions, Crofton metrics, and a Markov-generator convergence question.
- Default-branch code searches for the ID and Wasserstein returned no indexed hits; that negative index result is not itself proof of absence.
- A scan of the local pinned problem catalogue found only this entry matching both the relevant spherical/equatorial transform and the Wasserstein inverse question. Available local campaign paths and queue projections supplied no same-problem prior attempt.

No genuine mathematically identical prior attempt was found in these checks. This is a bounded duplicate screen, not a guarantee about every repository branch, private conversation or unpublished work. It does not justify claiming literature novelty.
