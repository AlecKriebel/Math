# Five-approach research log

Problem 2303022 / AMR-022-3022. Date: 4 October 2026, UTC.
Started at 08:18 UTC; source checks and the five mathematical approaches were
interleaved. The numbered entries are the five substantive proof approaches;
individual tool calls, source searches, and later checks are not extra turns.
This log records outcomes rather than inventing separately timed sessions.

## Readiness checkpoint, 08:18--08:27 UTC

- Requested catalogue page was inaccessible through the web tool.
- Read the exact statement and update in Hayman--Lingham (2018), page 67.
- Read the immutable catalogue record and prior report. They say OPEN-TRIAGE;
  the prior work contains a statement check and unsuccessful literature search,
  not a claimed proof or a mathematical attempt artifact.
- Live queue row: rank 572, queued, 0/5. No target-number PR, branch, code-search
  result, or target attempt directory was found. Broader issue search for Fuchs
  also returned no matches. Related-target group file contained no target ID.
- Read the repository and queue research instructions. No remote writes were
  made during this attempt.
- Found the important scope distinction: the connected continuum problem has
  a published answer; Betsakos explicitly asks about two curves. The full
  arbitrary-closed-set target is not certified already solved.

Completion estimate toward a new sharp resolution at this stage: 0--5%.
Source triage and admissibility checks were complete enough to proceed.

## Turn 1/5: topological reduction and radial selectors

**Proposed mechanism.** Reduce arbitrary radial-covering obstacles to a compact
one-point-per-radius selector, or connect components and apply a known theorem.

**Work and proved outcome.** Proved that every compact exactly-one-point-per-ray
selector is a Jordan separator, with escape probability zero. Proved objective
monotonicity under adding obstacle points. Constructed two complementary
semicircular obstacles and showed that adding two radial connectors produces a
Jordan barrier; Turn 4 quantitatively proves positive escape before adding them.

**Why the full route fails.** Connecting components moves the escape probability
in the wrong direction for the desired universal upper bound. A measurable
radial selector need not be compact. The claimed lossless topological reduction
is unavailable and, in its naive form, explicitly false.

**Artifact.** proof.md, Section 2.
**Full resolution:** no. Completion estimate: 5%.

## Turn 2/5: connected extremal metric and conformal rectangle

**Proposed mechanism.** Transfer the known connected quadratic-differential
extremal configuration to the unrestricted target.

**Work and proved outcome.** Matched the literature's actual connected-set
hypothesis; derived the rectangular separation-of-variables series rather than
copying the published decimal. Exact rational arithmetic encloses the short-side
probability and checks that complementing it gives the connected hitting constant.
The geometric connected-set theorem remains explicitly cited, not independently
reproved. No claimed extension to disconnected obstacles was found.

**Why the full route fails.** There is no admissible theorem identifying a
multiply connected obstacle domain with the same single-rectangle extremal
problem. A correct connected constant does not supply the missing comparison.
The older update must not be misread as a resolution of the full target.

**Artifact.** proof.md, Section 3; controls/verify.py.
**Full resolution:** no. Completion estimate remains 5%.

## Turn 3/5: Green-potential dual certificate

**Proposed mechanism.** Lift angular measure onto E, divide by its Green value at
0, and bound the resulting potential uniformly. A sharp optimal certificate
could force the desired extremal constant.

**Work and proved outcome.** Established a three-region pointwise kernel bound,
including the logarithmic singularity, then integrated the majorants. Used the
full inverse image under z -> z^n to place compact obstacles near the unit circle
without assuming a false radial-shove inequality. Exhaustion handles relatively
closed obstacles. This proves h(E)>=1/16, hence q(E)<=15/16, uniformly.

**Why the full route fails.** The envelopes use loose inequalities and different
pointwise maximizing regimes. No matching obstacle can be inferred, and no
optimality or duality theorem identifies the bound with the true supremum.
This is a non-sharp Hall-type partial, with no novelty/improvement claim.

**Artifact.** proof.md, Section 4; exact coefficient controls in verify.py.
**Full resolution:** no. Completion estimate: roughly 10%, highly subjective.

## Turn 4/5: Brownian stopping, Harnack chains, and component overlap

**Proposed mechanism.** Assemble known single-component estimates using the
strong Markov property, or establish a maximizing disconnected construction.

**Work and proved outcome.** Gave a 31-link explicit Harnack chain for the two
semicircles, with all clearance estimates and an annulus terminal probability.
This proves q(E)>1/(2*3^31). Separately proved the finite-component lower estimate
h(E)>=C_conn/k from event counting and the published connected theorem.
Demonstrated that disjoint angular projections still allow positive probability
of hitting both obstacles before T, so hitting probabilities are not additive.

**Why the full route fails.** The quantitative construction is not extremal.
The finite-k bound degenerates as k increases, and the joint hitting-event
intersections are not controlled sharply. Even the two-curve infimum is not
identified by these arguments.

**Artifact.** proof.md, Sections 5--6; exact chain/count controls.
**Full resolution:** no. Completion estimate remains roughly 10%.

## Turn 5/5: logarithmic-coordinate PDE experiment

**Proposed mechanism.** Use explicit circular arcs to reduce the PDE to a cylinder
with aligned slit boundaries, search for an exact pattern, and test a possible
extremizing construction.

**Work and outcome.** Implemented the cylinder finite-difference model with
periodic angular coordinate and a finite reflecting inner truncation. Ran three
meshes (4,030; 16,254; 65,278 unknowns) and empty/full-circle controls. The two-arc
values were about 0.003634, 0.004216, and 0.004514. The values did not suggest a
closed-form sharp candidate; endpoint discretization is visibly material.

**Why the full route fails.** There is no certified continuum discretization or
truncation error and no global optimization argument. Small matrix residuals
are not continuum proof certificates. These values cannot justify a conjectured
sharp constant, let alone resolve the target.

**Artifact.** controls/explore_two_arcs.py; controls/two_arcs_results.json;
proof.md, Section 7.
**Full resolution:** no. Five-turn budget is exhausted.

## Frozen conclusion

Recommended status: **unsolved, 5/5**. The sharp universal supremum is not found.
The complete proofs above are proofs of partial statements only. This checkpoint
does not claim priority, a literature improvement, or independent verification
of the full published connected-set theorem. Mathematical completion estimate:
roughly 10%; dossier/reproducibility completion: 100% before independent audit.

A fresh independent audit is required before any public repository write. Any
subsequent audit is verification of this frozen work, not an extra search turn.
