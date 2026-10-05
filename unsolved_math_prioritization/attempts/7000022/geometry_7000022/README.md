# Surface area of convex hulls of closed space curves

Problem 7000022 / AMR-069-0022, rank 749. Research date: 2026-10-05.

## Result

**The full problem remains unresolved in this investigation.** Five proof routes were examined. The package provides rigorous bounds, a complete four-vertex special case, and exact counterexamples to two proposed reductions. It contains no claim of a new solution or of novelty for its partial results.

The target is the following mathematical assertion. For every continuous rectifiable closed parametrized curve `gamma` in Euclidean three-space with length `L`, let `K = conv(gamma)`. Define `A(K)` as the ordinary boundary area if `K` has dimension three, twice its planar area if it has dimension two, and zero if its dimension is at most one. Prove

`A(K) <= L^2/(2*pi)`.

A circle attains equality. The source does not impose simplicity, smoothness, a knot type, or containment of the curve in the boundary of its hull. Finite length supplies the rectifiable interpretation; repeated traversals count toward length. Nothing here substitutes area of a spanning surface, volume, or a projected signed area for `A(K)`.

The exact named item is **Area of the convex hull of closed curves**, Problem 5.3 on printed page 14 of [Mohammad Ghomi's 2019 problem collection](https://ghomi.math.gatech.edu/Papers/op.pdf). Its formulation and the doubled-disk convention were checked against a rendered page. Ghomi restated the equivalent polytope-tour problem in [October 2024](https://mathoverflow.net/questions/480430/shortest-loop-through-vertices-of-a-convex-polytope), including the warning that shortest tours need not stay on the hull boundary. No subsequent resolution was found in the targeted primary-source search through 2026-10-05; that negative search is not a proof of current openness.

## Verified partial conclusions

1. The conjecture for all closed curves is equivalent to its polygonal version. A normalized maximizer exists, but compactness alone does not establish its shape.
2. If the hull has at most four vertices, the stronger sharp estimate `A <= L^2/8` holds. The limiting equality example is a square with its hull counted twice.
3. Cauchy's projection formula and planar isoperimetry yield `A <= 2*L^2/(3*pi)`. An exact second-moment calculation exposes the reversed-Jensen error in a prior desk route.
4. Mean width and the classical Minkowski inequality yield the better universal estimate `A <= pi*L^2/16`, about 23.37% above the requested coefficient. An explicit sufficient condition in terms of mean-width slack is recorded.
5. For a concrete flattened octahedron, the shortest closed Euclidean tour is strictly shorter than every closed tour restricted to the hull boundary. This blocks a length-nonincreasing boundary replacement argument.
6. A closed walk on a three-arm tree has a positive-area tetrahedral hull but a zero-area Lipschitz spanning disk. Thus an estimate based only on the least area of a spanning disk cannot control the hull area.

The known hull-boundary case is explicitly attributed to Zalgaller and Ghomi. The four-vertex calculation and the explicit controls are separately scoped, not promoted to a full resolution.

## Files and replay

- `PROOFS.md`: definitions, proofs, exact examples, and the remaining gap
- `RESEARCH_LOG.md`: five substantive approach families and their outcomes
- `SOURCE_VERIFICATION.json`: public source metadata, byte verification, inspection limits, and repository checks
- `verify.py`: dependency-free exact arithmetic controls
- `CHECK_RESULTS.json`: saved result of those controls
- `AUTHOR_MANIFEST.json`: exact file inventory and SHA-256 hashes

Run `python3 verify.py` from this directory. It writes the deterministic `CHECK_RESULTS.json` and uses rational interval arithmetic for radicals and pi. The script checks exact examples and finite tour enumeration; it does not prove the conjecture or mechanically certify every analytic proof.

## Status and release boundary

Five of five substantive approaches were used. Recommended mathematical disposition: **exhausted, with partial bounds and verified obstructions**, not solved. The exact full target has no verified completion percentage beyond 0%; the bounded investigation and its deliverable are complete. A fresh uninvolved audit is required before publication. No remote changes were made during authorship.

Only authored mathematics, authored code, computed verification results, and public-source verification metadata belong to this package. Source PDFs, extracts, dataset contents, and private coordination material are excluded.
