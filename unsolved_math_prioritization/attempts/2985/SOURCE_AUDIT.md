# Source, scope and attribution audit

Checked 2026-09-30.

## Original question

The full original Problem 4.109 and both remarks were read on printed p.281
of [*K3: A New Problem List in Low-Dimensional Topology*, author-hosted
preliminary version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
The page was inspected visually. The prescribed data are a symplectic
surface in a closed symplectic four-manifold with surface class Poincaré
dual to an integer multiple of the symplectic class. The question asks
whether that complement supports a Weinstein structure.

The statement does not explicitly add connectedness, integrality of the
unscaled symplectic class, simple connectivity of the ambient manifold,
or a large-degree hypothesis. The candidate uses a connected ambient
manifold and a connected surface, and its symplectic class has integral
periods. It therefore does not rely on the possible omission of a
connectedness condition.

The source's first remark singles out the projective-plane case. Its second
remark concerns existence of *some* suitable surface for large degree and
asks about effective degree bounds. A bad prescribed surface of degree one
does not imply that every degree-one representative is bad. The candidate
keeps these quantifiers separate. The ambient manifold in the construction
is not asserted to be the projective plane.

## Published ingredients

Emmanuel Giroux, *Remarks on Donaldson's symplectic submanifolds*,
Pure and Applied Mathematics Quarterly 13(3) (2017), 369–388,
[DOI 10.4310/PAMQ.2017.v13.n3.a1](https://doi.org/10.4310/PAMQ.2017.v13.n3.a1),
[full author manuscript, arXiv:1803.05929v1](https://arxiv.org/abs/1803.05929v1).

The introduction, precise definitions, Theorems 1–2, and the full relevant
Section A were read. Proposition 9 attributes disconnected examples in
the standard four-torus to Auroux. Its explicit construction uses two
orthogonal integral symplectic classes and symplectic smoothing of affine
torus pairs. These are established ingredients, not discoveries of this
attempt. Proposition 5 supplies a Liouville compactification of an integral
symplectic hyperplane-section complement. Theorem 2 supplies Weinstein
complements for suitably chosen sufficiently large-degree sections; its
existential quantifier does not apply to every representative.

The candidate checks explicit offsets making the two nodal unions disjoint,
and proves its required local smoothing in coordinates. Thus it does not
depend on the overly broad assertion in the displayed construction that
arbitrary unequal translation parameters ensure disjointness. The proposed
additional step is the specified free affine involution exchanging the
smoothed components. The connected quotient is then obstructed using
ordinary third homology in its connected double cover.

The basic Weinstein Morse-index bound is stated in Giroux's introduction:
critical indices in real dimension four are at most two. The homology
obstruction uses the standard oriented Thom isomorphism, exactness of the
pair sequence, and finite-cover transfer. These ingredients do not depend
on a particular Liouville primitive or completion convention.

## Literature and novelty limits

Current searches included the exact Kirby number and statement, connected
symplectic hyperplane sections, non-Weinstein complements, free quotients,
and finite-cover obstructions. They located the published disconnected
construction and higher-dimensional related examples, but did not establish
whether this connected four-dimensional quotient construction has appeared
before. No historical-priority claim follows from a limited search.

The pinned dataset's open or partial classification is triage, not proof of
current open status. The authoritative target was taken from the full K3
text, not inferred from that classification. No outside contact was made.

## Data provenance

The source record is preserved in [source_record.json](source_record.json),
from [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath)
at revision `37e53eabe540fb458758e198be61634bd02ee008`, under its CC-BY-4.0
attribution. No exact `KP-4.109` entry was present in the pinned separate
research-results dictionary. Source PDF hashes and inspected locations are
recorded in [source_manifest.json](source_manifest.json). The PDFs themselves
are not part of the public research package.
