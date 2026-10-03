# Delone cluster groups: source and prior-attempt gate

Checked 3 October 2026. Numeric ID 20001782, AIM-GEOMETRY-0120, queue rank 458.

## Exact target and conventions

For every fixed dimension d >= 4, does there exist h(d) such that every
2R-regular Delone set X in R^d satisfies |S_x(2R)| <= h(d), independently of R/r?
Here r is the exact packing radius, R is the exact covering radius, distinct
points have distance at least 2r, and closed R-balls centered on X cover R^d.
The closed cluster is C_x(t) = X intersect B_x(t). Its group S_x(t) consists
of ambient isometries fixing x and preserving C_x(t). Cluster equivalence
must carry the marked center to the marked center. This centered convention
is essential. Element order and group cardinality are distinct quantities.

The catalogue title describes a previous machine-generated partial report,
not the original question. Neither an element-order reduction nor a
conditional short-span estimate resolves the target.

## Sources actually checked

1. Exact catalogue URL: <https://www.unsolvedmath.com/problems/20001782>.
   Web retrieval failed; the cloud browser displayed HTTP 403 Forbidden and
   “This request was blocked.” No successful current rendering is claimed.
   The supplied catalogue snapshot was checked against its recorded SHA-256
   hashes. Its statement and complete partial report were read locally.
2. Original AIM item: <http://aimpl.org/softpack/3/>, item 3.2. Direct retrieval
   failed. The accessible official [workshop report](https://aimath.org/pastworkshops/softpackrep.pdf),
   page 3, Problem 1, independently confirms the dimension-only group-order
   target and the sharp values 12 and 48 in dimensions two and three.
3. N. Dolbilin, A. Garber, E. Schulte, M. Senechal,
   [Bounds for the Regularity Radius of Delone Sets](https://doi.org/10.1007/s00454-024-00666-6),
   Discrete & Computational Geometry 74 (2025), 78–94, published online 2024.
   Section 2 supplies the marked-center conventions; Problem 5.1 is exactly
   the target. Conjecture 5.2 proposes 2^d d! for sufficiently large d.
   Proposition 3.2 treats full-dimensional nearest-neighbor clusters.
4. E. Schulte, [Bounding the Regularity Radius of Delone Sets](https://www2.cms.math.ca/Events/winter25/abs/pdf/rpi-es.pdf),
   Canadian Mathematical Society Winter 2025 abstract, still presents
   conjectures with verified special classes, not a general resolution.
5. P. Müller, [A note about Jordan's bound on the size of finite linear groups](https://arxiv.org/abs/2603.15813),
   March 2026 preprint, supplies a self-contained Jordan bound 25^(d^2).
   We can instead use the abstract classical Jordan constant throughout.

Targeted current searches for the exact problem, 2R-regular cluster groups,
group-order bounds, and 2025–2026 developments found no general resolution.
This is a bounded literature check, not proof of completeness or novelty.

## Prior-attempt gate

The live main-branch row was queued at 0/5. Searches of PRs for the numeric ID,
code and Delone title, branches for the numeric ID and Delone, repository code
for the ID, and commit messages for the ID returned no earlier target attempt.
The related-target-groups file contains no exact-ID entry. The prior imported
report is explicitly PARTIAL-PROGRESS and ends with the general target open.
It is background, not a completed campaign attempt or a literature certificate.

Five substantive proof attempts are available. Source retrieval, independent
review, and packaging do not count as attempts. Success requires either a
dimension-only bound with all hypotheses proved or a fixed-dimensional family
of 2R-regular Delone sets with unbounded cluster-group order.

No source PDFs, screenshots, or corpus files are included in this package.
