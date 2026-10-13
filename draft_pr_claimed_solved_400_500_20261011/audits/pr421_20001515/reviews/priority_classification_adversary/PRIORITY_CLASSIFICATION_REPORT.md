# Independent priority/classification adversary — exact PR421 / 20001515

Recorded UTC: 2026-10-12T23:08:52.189679+00:00.
Completion: 100% of the bounded classification audit. This is not 100% confidence in absolute historical novelty.

## Verdict

**The presently assembled old-tools chain does not, by itself, certify that AIM 5.2 was historically already solved. Do not change this record to `already_solved` on that reason alone.** Subject to the accepted mathematical gate, an affirmative paper is defensible as a compact explicit construction and a current short application/identification using established tools. Do not claim the first answer, absolute novelty, or that earlier tools could not answer it.

This conclusion is conditional on a precise meaning of `already_solved`: a prior established answer (explicit, equivalent, or genuinely directly covered by a known theorem). If the project deliberately uses that field to mean *deducible today from pre-existing general results without a new theorem*, the chain meets that broader label once all group-specific checks pass. That is a different editorial taxonomy and must be declared rather than silently treated as historical priority.

I have read no peer reports. Applicable root AGENTS were read; there are no nested AGENTS in my path. No Git, PR, sheet, status, source-snapshot, Zenodo, or external communication changes were made. The finite model's accepted validity is an input, not re-proved here. The initial sealed criteria contained an inaccurate approximate future timestamp; `CHRONOLOGY_CORRECTION.json` preserves the original bytes and records actual mtime 2026-10-12T23:04:40.553195Z. The substance was sealed before primary theorem inspection.

## Exact claim and source boundaries

The claim is geometric action of the exact group

\[
G=\langle a,b,c,t\mid [a,t]=1,\quad tbt^{-1}=ab,\quad tct^{-1}=bcb\rangle
\]

on a CAT(0) cube complex. The final `b` in `bcb` is positive. The canonical catalog identifies the target as AIM Problem 5.2, attributed to Rylee Lyman. The workshop summary instead discusses `b` mapping to `aba`, with `c` mapping to `bcb`; its candidate cubulation therefore is not evidence for this exact group. The summary's candidate was described with cocompactness still hoped for. [AIM workshop summary](https://aimath.org/pastworkshops/freebycyclicrep.pdf)

The parent reports fresh 2026 and archived 2024 unchanged AIM entries. I did not independently authenticate those two snapshots. Direct retrieval of the live AIM page failed in this bounded audit (web timeout / certificate mismatch); those failures are recorded. A persistent question entry is positive evidence about that record, not a guarantee that no answer exists elsewhere.

## Primary theorem scope independently checked

| Source and date | Actual conclusion relevant to this route | What remains target-specific |
|---|---|---|
| Minasyan–Osin, first preprint 2013; journal 2015; checked corrected v6, 20 December 2017, Corollary 4.3 | A tree-hyperbolic element with finite stabilizer of an axis segment is WPD. | Verify the claimed segment for `bx`; the conclusion is not cubulation. [Corrected source](https://arxiv.org/pdf/1310.6289v6) |
| DGO, first preprint 2011; checked v5, 2 December 2014; journal 2017, Theorem 6.8 / Corollary 2.9 | Loxodromic WPD elements give hyperbolically embedded maximal virtually cyclic subgroups. | Apply to the one given element in the correct tree action. [Source](https://arxiv.org/pdf/1111.7048v5) |
| Sisto, preprint 29 October 2013; journal 2016, Theorem 1 | An infinite-order element in such a subgroup of a finitely generated group is Morse, hence word-metric quasiconvex. | Match that metric to the base cube complex's combinatorial metric. [Source](https://arxiv.org/pdf/1310.7753v1) |
| Ben-Zvi–Kropholler–Lyman, preprint 10 November 2020; online 28 October 2021; issue July 2022, Theorems 1.1 / 5.1 | A finite graph realizing a subgroup quasiconvex for the cube-complex edge generating set has a finite local-isometry completion. | Supply finite NPC `K`, cyclic inclusion, and the metric check. This does not itself conclude the HNN extension is cubulated. [Preprint](https://arxiv.org/pdf/2011.05374v1), [publication](https://doi.org/10.1017/S0305004121000645) |
| Hagen–Wise, checked v3, 13 August 2025, Remark 3.7 | Compatible cubulations, cocompact vertex actions and convex edge subcomplexes give free cocompact cubulation by standard local-isometry gluing. | Supply compatibility, here through one finite domain and its symmetry-related map. [Current source](https://arxiv.org/pdf/1605.07879v3) |

The same current Hagen–Wise paper's Corollary 7.2 only gives a free action for fast automorphisms. Its definition does not require metric properness or cocompactness, and Question 1.3 asks the stronger questions. Lyman's CAT(0) 2-complex theorem likewise cannot be promoted to a cubic action; Question 1 explicitly asks about cocompact cubulation. [Lyman v3](https://arxiv.org/pdf/1909.03097v3)

The chronology above establishes dates for ingredients and statements. It does not establish the date of this exact assembled deduction. Using the 2020 completion theorem with standard gluing suggests that the described toolkit sufficed before the current effort, but no first availability date for the *assembled answer* follows from that observation. The explicit gluing formulation I checked is from 2025; I did not date the earlier standard argument by independent full-text comparison.

## Why the chain is an application, and what is routine in it

The supplied route starts with

\[
H=\langle x,y,b\mid [x,y]=1,\ bxb^{-1}=y\rangle,\qquad g=bx.
\]

After old results give a finite local-isometry completion `j` of the `bx` circle, the cubical symmetry `lambda(x)=y`, `lambda(y)=x`, `lambda(b)=b^{-1}` supplies a second map on the **same** finite domain. A mapping cylinder then supplies

\[
\langle H,z\mid z^{-1}(bx)z=b^{-1}y\rangle.
\]

The target identification uses `t=x`, `a=xy^{-1}`, `c=(zx)^{-1}`. These target-specific steps were provided in the assignment and are not claimed as my independent mathematical verification.

All the abstract mechanisms are old. The extra insight is the application that finds this base model and symmetry, uses finite completion to satisfy geometric gluing, and identifies the resulting group with the exact AIM presentation. The completion's compactness is a direct specialization of an old theorem; the final existence conclusion is obtained by combining that specialization with the symmetry and gluing. A manuscript must describe that dependence candidly.

Counting citations or saying the calculation is short cannot decide priority. Equally, the fact that all statements imply a claim in the closure of mathematical deduction cannot date that claim's discovery. A general prior theorem for **these symmetric cyclic HNN extensions** would directly subsume the application once the hypotheses are checked. An earlier source already building the two compatible local-isometry maps, or asserting geometric cubulation for this equivalent HNN presentation, would also defeat existence novelty. No such source was identified in this bounded audit.

## Adversarial tests of both hypotheses

For **historically already solved**, the strongest evidence is that no new abstract theorem is needed: the final proof can be short and follows from established machinery. The exact missing evidence is a dated establishing source, or a prior general theorem that already carries the final geometric conclusion for this class without this effort supplying the intermediate compatible construction. An exact group name is unnecessary if that general theorem exists. Existing free cubulation, quasicubical, or CAT(0)-space results are insufficient.

For **present contribution**, the strongest evidence is the accepted explicit finite model, together with a present application that bridges the geometric matching issue. The exact missing evidence for a stronger historical claim is a convincing search closure and any earlier public/unpublished-to-us record of the equivalent construction. This audit cannot prove absence. Unchanged AIM entries alone do not fill that gap. A small explicit model may contribute independently of old existence priority, but it is not certified here as the smallest, lowest-dimensional, first, or structurally unique model.

These hypotheses need not be mutually exclusive at every level: an old existence theorem could coexist with a new explicit model. If a prior affirmative answer is later found, correctly mark the problem `already_solved` under the user's workflow and assess the explicit model separately. The construction does not rescue a false claim to first existence priority.

## Positive claim allowlist and proposed framing

Allowed, conditional on the accepted mathematical gate:

- The displayed exact group acts geometrically on a CAT(0) cube complex.
- The paper gives a finite NPC cube complex with that fundamental group, with the checked cell vector `(1,7,8,2)`.
- This gives an affirmative answer to the displayed AIM Question 5.2.
- The existence conclusion also follows from a short present combination of the cited earlier tools with the explicit symmetry and group identification, once its hypotheses are checked.
- The cube complex is an explicit construction; its finite data and verification can be reproduced.
- No prior recorded affirmative answer was located in the specifically enumerated sources and queries checked, with the bounded search date stated.

Withhold: first answer, newly solved since a particular year, universally still open before this effort, absolute novelty, minimal cells/dimension, virtual specialness, and a historical `already_solved` conclusion drawn solely from the ingredient dates.

A safe title is **A compact cubulation for a quadratic free-by-cyclic group**. A safe abstract opening is: “We construct a finite nonpositively curved cube complex with fundamental group the mapping torus of `a` mapping to `a`, `b` mapping to `ab`, and `c` mapping to `bcb`. Its universal cover gives a geometric cubulation, answering AIM Question 5.2 affirmatively.” The introduction should then credit the alternative existence route and distinguish the explicit finite model from the general tools.

## Bounded search and exact remaining uncertainty

This reviewer independently retrieved the primary MO, DGO, Sisto, Ben-Zvi–Kropholler–Lyman and current Hagen–Wise papers; both the 2020 and published completion theorem statements agree at the relevant scope. Lyman v3 was read at the scope stated above. Source bodies and hashes are in `../../private_sources/priority_classification_adversary/`; receipt files preserve retrieval time and failures. Web queries are recorded in `SEARCH_BOUNDARY.json`. No result in the checked sources supplies a prior final affirmative answer for the exact `ab,bcb` group. This is bounded absence evidence, not an extensive independent literature closure or a novelty certificate; the parent's broader priority audit is still material.

An earlier written record of the exact compatible construction could change the historical conclusion. That possible outside input is recorded here; no outreach is prepared or initiated, under the independent-research policy.
