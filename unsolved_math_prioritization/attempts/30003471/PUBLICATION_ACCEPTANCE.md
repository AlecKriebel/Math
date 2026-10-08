# Acceptance of the frozen three-dimensional dihedral comparison argument

Date: 2026-10-08 UTC. Target 30003471 / OWR-15427-013, queue rank 999.
Disposition: **claimed_solved, 1/5 substantive author approaches**.

The complete frozen author proof and both complete independent mathematical audits
were read before this acceptance. Both audits accept the unchanged mathematical
argument, including arbitrary nonsimple vertices, and identify no mandatory
mathematical correction. Their optional presentation suggestions do not alter the
accepted proof. The accepted proof SHA-256 is
`6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`.

For compact, full-dimensional convex polytopes in Euclidean three-space with a
fixed face-lattice correspondence, weak dominance of all corresponding interior
dihedral angles forces equality of the **complete facet-normal Gram matrix**.
Reversing the two polytopes rules out all-strict dominance and proves the original
one-edge weak-comparison target. This is a dimension-three result. Equality of
normals' Gram matrices does not assert support-number, edge-length, or full metric
rigidity. Smooth corner equivalence is not assumed, including at nonsimple vertices.

The proof constructs compatible target-normal boundary data on smooth inner
approximations of the source polytope, with logarithmic vertex cutoffs. Its critical
boundary L2 estimate, uniform H1-to-L4 trace bound, smooth-boundary index/energy
argument, nonvanishing constant limit, and Clifford intertwining conclusion were
all covered by each mathematical audit. Finite diagnostics support bookkeeping;
they do not establish these infinite-dimensional analytic conclusions.

The specialized dependency is Brendle's published smooth-domain result, inspected
in arXiv:2301.05087v4, Section 2, Propositions 2.9, 2.14 and 2.15. Publication metadata
were verified; the inspected proof text was the author manuscript, not the publisher
PDF. The smoothing strategy is credited to Bi's arXiv:2608.06320v1. Wang-Xie-Yu's
arXiv:2606.30130v1 states a related stronger comparison and is relevant prior work;
its full singular-index proof is neither audited here nor used as a black box.
No journal acceptance of those recent manuscripts was verified. No novelty,
absolute priority, formal proof, conventional human peer review, or journal
acceptance of this argument is claimed.

## Preserved history and replay

`public/` is the exact ten-file candidate freeze. Its earlier pending-audit flags
and candidate wording are historical, intentionally unchanged. The later controlling
publication disposition is this report and `ACCEPTANCE.json`, supported by the two
complete frozen audits in `audit_a/` and `audit_b/`. The mathematical text is unchanged.
The second audit's ZIP is excluded; every manifest-bound member is included.

The original second-audit diagnostic program remains byte-identical. Its original
local path and mandatory source-PDF assumptions are preserved as history. The
explicit `PORTABLE_CONTROLS.patch` changes only input-location selection and optional
source hashing in `PORTABLE_INDEPENDENT.py`. Every mathematical computation is
unchanged. Portable runs replay 4,137 checks and explicitly report that nine PDF-hash
checks were NOT_RUN. Separately supplying the nine matching PDFs restores all 4,146
checks. Neither PDFs nor source extracts nor dataset contents are distributed.

The strict publication wrapper authenticates fixed inner manifests, exact directory
and regular-file inventories, strict JSON types, duplicate keys, filesystem modes,
and absence of symbolic links. It replays controls in normal, -O, and -OO modes,
enforces read-only fixtures using actual denied write probes, and checks unchanged
input bytes. External-bootstrap mutation tests authenticate the wrapper before
running it, separately from the publication-manifest anchor. These are integrity
and diagnostic checks, not a formal mathematical verifier.

## Primary references

- [Original OWR problem, printed p.1198, question 4](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1)
- [Akopyan-Karasev, Conjecture 5.1](https://arxiv.org/abs/1505.05263v2)
- [Brendle, inspected version](https://arxiv.org/abs/2301.05087v4); [published record](https://doi.org/10.1007/s00222-023-01229-x)
- [Bi, credited smoothing strategy](https://arxiv.org/abs/2608.06320v1)
- [Wang-Xie-Yu, relevant recent claim](https://arxiv.org/abs/2606.30130v1)
- [Bar-Hanke-Schick, version-specific caution](https://arxiv.org/abs/2202.05180v2)
