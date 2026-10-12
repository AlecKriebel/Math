# PR463: verified mathematics, classical original-target disposition

Selected problem: 6000016 / AMR-059-0016, Stability of Hessian Metrics.
Original eligible draft head: `982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649`.
Original QUEUE status: exactly `claimed_solved`, attempt accounting `1/5`.
This document proposes a priority correction while that eligible status remains
unchanged. A separate final root acceptance gate and live exact-head check are
required before any correction. No paper or publication package is proposed.

## Exact target and strongest mathematical result

The original item 5(b), printed p. 126, Furuhata–Matsuzoe–Urakawa (1998),
[DOI 10.4036/iis.1998.125](https://doi.org/10.4036/iis.1998.125), asks whether
every sufficiently small affine deformation of a compact positive Hessian
manifold admits some positive Hessian metric. It separately records the
hyperbolic affirmative case and imposes no fixed-holonomy restriction.

On the fixed torus, D_t=D_0+t dx⊗dx⊗∂y is a smooth complete flat torsion-free
affine family preserving dx∧dy. At zero, dx²+dy² is locally Hessian. For any
smooth positive Hessian metric with periodic coefficients A,B,C, Codazzi gives
B_x−A_y=tC, and the global one-form α=A dx+B dy satisfies dα=tC dx∧dy.
Stokes and C>0 force t=0. Every nonzero parameter, however small, therefore
admits no positive Hessian metric at all. The cover/deck-cocycle proof gives
a materially distinct verification. No invariance, parallelism, global torus
potential or continuous parameter-dependent metric is assumed. The result
does not exclude indefinite metrics, noncompact local metrics or semidefinite
tensors and does not address fixed holonomy or the hyperbolic subclass.

Three independent mathematical families and the root's reconstruction pass.
All 14 original files and all 25 supplied historical reference bindings are
checkable and unchanged. Author 41/audit 61 named results reproduce byte-exactly
normally and optimized, including optimized nested subprocesses. Independent
families supply 691, 140 and 43 exact controls with actual negative-entrypoint
checks. Counts supplement the analytic proof; they do not certify its universal
quantifiers. Exact report hashes and positive output checks are in
MATHEMATICAL_FAMILY_READBACK.json. Zero new original proof-search attempts.

## Priority mechanism and application

The exact developing map F_t(x,y)=(x,y+t x²/2) is classical. The root and
independent reviewers visually inspected [Baues–Goldman v1](https://arxiv.org/pdf/math/0401257v1),
printed pp. 24–25. The [official version record](https://arxiv.org/abs/math/0401257v1)
dates publication on 20 January 2004 at 16:47:28 UTC. The familiar v2 passage is
printed p. 20 and dated 14 June 2005. The normalized cube-root period is continuous;
t=s³ makes it smooth as well. Ordinary connection/chart smoothness is direct.

Knownness of that family alone does not settle priority of the all-metric
obstruction. The decisive historical mechanism is a fully checkable older
theorem application, authored explicitly in reviews/priority/APPLICABILITY_CHAIN.md:

1. Suppose any positive Hessian metric exists on a nonzero shear torus.
   Delanoë (1989), Théorème 3, printed p. 67,
   [primary paper](https://doi.org/10.18910/7541), supplies another positive
   Hessian metric whose determinant is a positive constant times the square
   of the prescribed parallel area density.
2. The developing cover is the entire affine plane. Twice applying Poincaré
   integration to the lifted Codazzi tensor yields a global smooth strictly
   convex potential on that plane, with constant Hessian determinant.
   Rescaling makes the determinant 1. No global torus potential is asserted.
3. Jörgens (1954), Satz 1, printed p. 130, bounds derivatives of the two diagonal
   Hessian coefficients at any disk center by constants times R^−2. The
   fixed entire smooth solution permits arbitrary radii R. Sending R to
   infinity forces all third derivatives to vanish, hence a constant positive
   Hessian matrix H. The original estimate was visually inspected in the
   official two-page publisher preview; its full proof was not retrieved.
4. Deck invariance requires S_tᵀHS_t=H with S_t=[[1,0],[t,1]]. The off-diagonal
   equality gives t H_22=0, impossible for t≠0 and H_22>0.

This chain excludes all positive Hessian candidates, rather than assuming
Hessian metrics are parallel. Its published components and this exact family
were available by 20 January 2004. The unrestricted original target is thus a
routine negative consequence of documented classical results. This is an
inference from those components. An earlier publication explicitly naming
item 5(b) as solved and the first author to recognize the application were not
established; neither is claimed.

Shima (2007), Corollary 8.6, and Fox (2013) corroborate the replacement-metric route.
Shima's readable p. 164 image and the full Cheng–Yau (1982) chapter were not
obtained; official snippets are weaker evidence. They are supplementary,
conditional attribution checks, not the decisive foundation. Inaccessible
Yagi classification pages likewise carry no disposition burden. A stronger
recent summary claiming the *given* metric is already parallel is excluded:
(1+ε cos(2πx))dx²+dy², 0<ε<1, is positive Hessian on the standard affine torus
with parallel dx∧dy, but has nonzero D_0g. Foreign sources remain private.

## Proposed exact action and stop boundary

Recommend correcting only this PR branch's selected QUEUE Status to
`already_solved` and Findings to a precise linked account of the older theorem
chain and the unestablished explicit-answer/first-solver attribution. Preserve
the original 14 artifacts, the `1/5` count, blank DOI, every other cell and row,
and every other Git path. Do not invent a new open problem to rescue the
publication classification. The short elementary proof may be useful exposition;
that does not justify framing it as a newly solved previously open problem.

The conditional repair helper is `draft_pr_claimed_solved_400_500_20261011/repair_pr463_status.py`.
It defaults to read-only preflight and requires a final accepted priority gate,
six distinct reviewed families, bound final evidence/helper bytes, and live
original open-draft/head/ref/repository/base plus exact claimed_solved QUEUE.
The first operational review found missing actual report/result bindings and
an insufficiently strict immutable-link check. That failed review and its
original helper/synthesis are preserved. The corrected contract requires each
family's canonical final REPORT and RESULT/DECISION with unique SHA256/size
bindings, all 14 frozen source objects and the reviewed source/synthesis/application
inputs. It parses the actual final result objects, checking exact identity and
scope-specific counts; labels with fabricated zero counts do not suffice.
The candidate's raw publication blocker 1 and classification change 1 remain
faithfully bound, alongside its zero unresolved proposed-disposition counters.
Those findings motivate this alternate accepted action, rather than disappearing.
The newest disposition reviewer must be a fresh numbered agent with no unresolved
operational or mathematical correction and must bind the exact final helper and
synthesis bytes. The first failed reviewer cannot supply final acceptance.
The synthesis URL must use the full 40-hex commit SHA and exact repository/audit
path without query or fragment. Before any Git mutation, the helper downloads
that immutable published synthesis and compares its complete bytes and accepted
digest with the local reviewed document. Existing operation receipts block
repeated apply attempts before dispatch.
Its applied commit changes one file and exactly the selected Status/Findings,
uses a nonforced branch update and verifies immutable QUEUE and ref readbacks.
The Git-data API is not an atomic expected-old-SHA CAS; nonforced ancestry
and immediate original-ref checks protect ordinary concurrent advancement.
After any uncertain ref update, inspect saved operation/readbacks without
repeating the write.

Once the readback shows `already_solved`, immediately exclude this PR under
the user's rule. No subsequent review, repair, paper, Zenodo/DOI, spreadsheet
row, ready/merge, close or comment. Keep it open and draft. Publish the completed
authored disposition evidence on main and proceed descending to the next fresh
exact-claimed_solved draft. This disposition is a reviewable proposal, not an
assertion that the action has happened. The sealed priority and candidate
reviews support its rationale. A NEW clean complete disposition/helper review,
genuine root acceptance gate and live eligibility remain required for execution.
