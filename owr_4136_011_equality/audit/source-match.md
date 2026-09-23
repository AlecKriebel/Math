# Exact source match

Checked 2026-09-23 UTC. Mathematical-source matching complete (100%).

1. The live [UnsolvedMath entry OWR-4136-011](https://www.unsolvedmath.com/problems/OWR-4136-011), titled *Simplex Equality Cases in Convex Geometric Inequalities*, was read through the in-app browser. Initial web-tool retrieval failed and a direct HTTP request returned 429; ordinary browser access succeeded. The live page states n>2, the condition that all extreme points have norm at least r, the centroid g_K, the normalized second moment C2, and exactly the bound in this manuscript. Its question is whether equality forces a simplex with all vertices on the radius-r sphere. The page labels the problem Open, cites statement review v1.7, and dates its literature triage 2026-08-21. This catalogue status is evidence of the catalogue contents, not independent proof of novelty.
2. [Fradelizi's Oberwolfach report, joint work with Paouris and Schütt](https://doi.org/10.4171/OWR/2009/53), *Simplices in the Euclidean ball*, printed pp. 2907–2909: Theorem 1 and the paragraph following it on p. 2908 give the same inequality, polytope equality class, and conjecture for general bodies. The following paragraph accidentally refers back to Theorem 1.1, the journal numbering. This does not change the target.
3. [Fradelizi–Paouris–Schütt, Canadian Mathematical Bulletin 55 (2012), 498–508](https://doi.org/10.4153/CMB-2011-142-1): Theorem 1.1 and its following paragraph, p. 499, give the same conjecture. The exact simplex moment identity is Lemma 3.2, p. 502; the polytope equality proof is on pp. 503–504. The paper was published electronically 8 July 2011.

## Scope corrections and boundaries

- The paper explicitly uses norm >=r. The historical prose says “greater than r” (three quoted words), although its equality statement and Lemma 3.2 require and use the non-strict interpretation. If all norms are strictly greater than r, the deficit is strictly positive.
- The catalogue restricts n>2; the sources start with n>=2. The submitted proof also covers n=1, so covers the entire catalogue problem.
- No origin-inside-body, smoothness, or closedness of the extreme-point set is assumed.
- For the displayed bound including the centroid term, every inscribed nondegenerate simplex is an equality case, including nonregular triangles. The weaker bound C2>=r²/(n+2) requires centroid zero in addition; only for that version is the dimension-two equality triangle necessarily equilateral. The original paper discusses the latter distinction on p. 503.
- This work claims resolution of the equality conjecture following Theorem 1.1, not a new inequality and not other questions concerning John or Löwner position.

The user-supplied argument matches and resolves the full mathematical scope of the linked problem, subject to proof verification documented separately. The primary sources are stored locally for inspection but are not redistributed in the public package.
