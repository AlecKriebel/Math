# Scoped acceptance: triangle stripe family, target 5500058

Date: 2026-10-11 UTC. Disposition: ACCEPT_PARTIAL_FULL_PLANE_CONTINUUM_CONSTRUCTION.

## Review and distribution status

AI-assisted and unrefereed, with an independent internal AI mathematical audit.
Acceptance is scoped to the stated partial theorem; it is not external human
peer review or formal proof-assistant certification. This is not a computational
reproduction package. The proof is self-contained. Programs, raw expanded cases,
datasets, copied source documents and source-derived images are not distributed.
Source hashes authenticate bytes, not correctness, novelty, or current status.
Editorial preparation performed no new mathematical program runs, scholarly
source-body inspection, or literature survey.

## Accepted result

The full sufficient criterion in PROOF.md is accepted. In particular, the single
whole-plane coloring c(X,Y)=floor(400Y/77) mod 3 avoids every congruent copy,
including every reflected copy, of every normalized triangle
A=(0,0), B=(1,0), C=(x,y) in the closed real rectangle
849/1000 <= x <= 851/1000 and 349/1000 <= y <= 351/1000.
The shape family has positive area and is uncountable. Stripe boundaries,
negative coordinates, all translations, rotations and both isometry determinants
are included. This is not a finite grid or almost-everywhere result.

## Why the acceptance is checkable

PROOF.md retains the general four-condition sufficient criterion, half-open
stripe separation, area/diameter lower bound on projection width, exhaustive
same-color stripe placements, six-vertex closed hexagon, and strict unit-disk
contradiction. It gives all six exact rectangle maxima, the center certificate,
and the exact negative isometry witness. AUDIT.md independently checks each
argument, endpoint equality, reflection, continuum maximization, source
comparison and negative-control scope.

The independent audit historically reproduced the six rectangle bounds and
center norms, checked six rational negative witnesses with determinant +1 and
-1 isometries, and matched 13 noncollinear decisions by an independently authored
rational projection-polygon method. The polygon corner checks are regression
evidence only; the analytic endpoint-convexity argument proves the continuum.
These historical calculations were not rerun during publication preparation.
The deterministic proof does not depend on those programs or retained outputs.

## Correction and identities

Before acceptance, the original proof's wording about an arbitrary containing
strip was corrected from equality to an upper bound: its area is at most
ell*w/2. Equality is appropriate for actual projection span. The accepted proof
is 7,242 bytes, SHA-256
35340484a8258b1587538fbb8d07515c709df8829629f04121c3547d65243012.
The original independent audit is 14,239 bytes, SHA-256
b14cfe2d8ee8ee89122516dc81b599b6e1cb7049a5dd17b036d3bc7197967a01.

The public proof and audit preserve all mathematical arguments while adding
review/distribution context, making historical verification wording explicit,
and removing private file dependencies. ACCEPTANCE.json binds the distributed
proof, audit and this report. MANIFEST.json binds the seven other public files;
the separately reviewed publication payload pins the manifest itself.

The creator's 42-member inventory and independent audit's 14-member inventory
were authenticated. The creator explicitly excluded generated __pycache__
directories. That qualified inventory claim must not be read as authentication
of all regular files. Inventory authentication verifies bytes and retained scope;
it does not confer permission to redistribute excluded source material.

## Unresolved full target and prior work

The original question is: for every fixed Euclidean triangle T, does some
three-coloring c_T of every point of R^2 avoid all monochromatic congruent copies
of T? This edition neither proves nor disproves that universal statement. A
failure of one stripe width is not an obstruction to all three-colorings.

Novelty is unestablished. The center is outside the two specified three-color
criteria of Aichholzer and Perz (EuroCG 2019), but that is not a novelty claim.
Mundinger et al. (ICML 2025) announce additional stripe regions; overlap appears
plausible from their Figure 4. Neither exact containment of this rectangle nor
identity of the constructions is certified. Their published statement that
separate papers were in preparation is historical, not a certification of their
present publication status. Figure 8's numerical conflict threshold is not an
all-points proof or a counterexample. The December 2025 status discussion is
version-pinned context, not an exhaustive October 2026 status search.

No novelty, general solution, global optimal stripe width, blanket validation of
cited papers, external human review, or formal proof-assistant result is claimed.
