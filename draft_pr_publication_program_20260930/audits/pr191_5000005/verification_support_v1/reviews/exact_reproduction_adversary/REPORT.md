# Exact reproduction and adversarial geometry report — PR191 / 5000005

Verdict: **REPRODUCED_FINITE_CHECKS; PARITY_REPAIRED_RULE_SURVIVES; BARE_A0_SHORTHAND_FALSE.**

The submitted author and independent checkers reproduce exactly, in ordinary Python and with optimization. Independent exact physical billiard calculations found no counterexample to the candidate's parity-selected reconstruction for the sampled n=3,4,5,6,8 directions. A direct pentagon calculation falsifies the imported bare A0 shorthand. This report does not certify the all-n theorem or historical novelty.

## Source-first independence and scope

I independently read the pinned Fuchs PDF before the candidate or any author/reviewer code, and sealed SOURCE_FIRST_ASSESSMENT.md (SHA256 295d8855973c39079707f4618cb7e4ae7d3bbe4deb35ef98c408c47d13d54677). Source prose pp.501–505 and 510–512 was read; Figure8's terminal supplement, Figure9's diagonal types, both pp.504–505 tables, and p.511 tables were visually inspected before that seal. Additional visual checks of pp.510/512 followed later. The old review opinions were read only after sealing INDEPENDENT_JUDGMENT.md (SHA256 43fd8c80bc0e8d332703ab648220f4351d1bb33fb6b948e92696919f33c4fa33). PDF SHA256: 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d. Private source derivatives and third-party code copies are excluded from the publication allowlist.

Chronology correction: the source-first note's manually typed 04:22Z header is inaccurate. Its filesystem creation/modification epoch is 1792037844, namely **2026-10-15T04:17:24Z**. The tool sequence independently records that seal before candidate/code inspection. Execution records use machine-generated UTC timestamps. The sealed note was preserved unchanged and this correction is explicit.

The source-derived model uses a=n alpha/pi in [0,n−2], b=n beta/pi in [2,n]. The physical terminal interior angle is pi−beta. If q is the number of straight segments, q odd selects the sum d=(b+a)/2 and k=n−1−d modulo n−2; q even selects the difference d=(b−a)/2 and k=d−1. Direct X0Xj has a=n−j−1,b=n−j+1 and q=1, yielding k=j−1. Preserving parity resolves numerical overlaps at special directions.

## Exact reproduction

| Program | Ordinary / optimized exit | Check count | stdout SHA256, identical in both modes |
|---|---:|---:|---|
| Author verify.py, unchanged private copy | 0 / 0 | 3,276,822 | 9b79444776c09d7d5ae97fcb0bba3568d0d193982276308cffaf41499512645c |
| Original independent check_independent.py, unchanged private copy | 0 / 0 | 441,920 | cc880ca26ea697ed7464a6774d1220776e3ee7eee7f56e785fcba9457fbd23d5 |

Author script SHA256: 14f5b3d8e69fccee88a933413da13f9b97dd400f986fe52194c9396f8b750669. Independent script SHA256: 20f99541d2702d34209100544d376f6a8e18f7cd15aa62f328e2f526ee2bd112. Frozen candidate SHA256: 6d406380552758f7b4292759d62c12cbf2fe7f4c03e358086d6fac938ed10260.

Code was inspected before execution. Both checkers use explicit if/raise guards; neither contains an AST assert statement. They need no optimization hardening. Deliberately injecting false conditions into their guards, and the three new physical checkers' guards, gives ten expected nonzero exits across ordinary/-O modes. No false result silently becomes PASS under optimization. All execution receipts preserve actual argv, UTC, exit, script/input and output hashes, counters and limitations. Original files were never modified or executed in place; the author's output write is confined to its own private copy.

The author count includes 2,765,952 checks of common-shift invariance/transport identities after defining the shift and reflection matching. These are correct algebraic sanity controls. They do not independently establish the geometric common-shift premise or endpoint reflection. Formal endpoint-angle tuples are also not certificates of actual long trajectories. The old independent program expands source boundary and angular-lift controls, but likewise does not replace the global geometric argument.

## Independent exact physical checks

The new programs start from polygon coordinates and the real reflection formula d_new=2e<d,e>/<e,e>−d. Each step computes all positive ray-edge intersections exactly, takes the first, treats collinear boundary edges, and stops only at an exact vertex. Type comes from final incoming direction relative to the terminal outgoing polygon edge and the actual segment parity. No cone-label or asserted endpoint matching computes a traced type.

| Family | Arithmetic | Terminated trace invocations | Admissible transformed-pair comparisons | Longest trace |
|---|---|---:|---:|---:|
| Triangle, square, hexagon | Rational coordinates with rational metric | 890 | 646 | 40 segments |
| Pentagon | Q(sqrt5), exact metric and sign ordering | 200 | 172 | 4 segments |
| Octagon | Q(sqrt2), exact sign ordering | 538 | 462 | 7 segments |
| Total | Exact intersections, reflections and unwrapped sector checks | 1,628 | 1,280 | 40 segments |

These are invocation counts with repeated directions, not 1,628 distinct saddle connections. Seeds for pentagon/octagon calculations include sheared polygon chords; seed termination is not presumed from the shear formula, because each physical ray is actually traced and its first endpoint recomputed. All three programs give byte-identical scientific outputs under ordinary and optimized execution.

The octagon samples probe the noncrystallographic even case with two vertex classes; all 462 transformed pairs preserve the source even/odd class. The checks cover all Figure9 direct chords for each tested n, both edge directions, zero-direction rejection, terminal supplements, admissible unwrapped sectors, and odd-ell rejection for even n. In n=3/4/6 with even ell, the wrong sign of ell can be invisible modulo n−2; pentagon/octagon samples distinguish it.

False controls have actual geometric witnesses. For n=8, an initial exact direction with raw coordinates (−2−sqrt2/2,1+sqrt2/2) has k=0 and two segments. With epsilon=−1,ell=2 its transformed first hit has k'=4 and five segments. The wrong plus-ell rule predicts 2 modulo6. For n=5, a sampled direction has k=1 and epsilon=−1,ell=1 yields k'=1; using the wrong epsilon or ell sign yields a different residue. The full exact coordinates and receipts remain private; the authored scripts reproduce them. A terminal-supplement control on n=6, X0X2, changes correct k=1 to incorrect k=3 if beta is replaced by the physical interior angle pi−beta.

A full 2pi wrap leaves a physical ray unchanged but changes the unwrapped expression; explicit guards reject that substitution. No modulo-angle shortcut broadens the conjecture's initial vertex sector.

## Exact scope counterexample and required repair

The authenticated upstream target includes the bare assertion that A0 is characterized by beta−alpha=2pi/n. The source makes this same shorthand, although Figure9 and the preceding parity selector require qualification. For a pentagon:

- X0X2: (a,b)=(2,4), one segment, correct type A1.
- X0X3: (a,b)=(1,3), one segment, correct type A2.

Both have b−a=2. Under the bare shorthand both would be A0. Their allowed transformation is epsilon=+1,ell=−1, so the signed law would require the second to be A1. The literal shorthand and law are therefore inconsistent. Under the parity-selected reconstruction the correct relation is 2=1−(−1) modulo3 and the contradiction disappears.

Required repair: explicitly scope the result to the full parity-selected source convention and document why the imported shorthand is invalid. Do not claim an unchanged exact dataset statement, or an unqualified literal four-row union, was proved. This distinction is mathematical, not a numerical discrepancy.

## Remaining analytic gap and route status

No new internal algebraic counterexample to candidate Lemmas1–4 was found. The unrestricted result still requires analytic verification of: (i) the two-polygon surface model and every germ's physical identification; (ii) synchronized common affine shift across both even cones, using the involution commutation argument; (iii) exhaustion of model germs by chords; and (iv) the imported lattice/cusp reduction for the actual two-polygon surface. Finite checkers cannot establish these for all n or all short directions. The coordinator's independent geometric and external-source families are responsible for those checks; this report does not duplicate their source retrieval or adopt their eventual verdict.

The old review agrees that parity must be retained and discusses those analytic obligations. It was consulted after independent judgment and is not counted as a second new proof. Its conclusion cannot repair the literal target without documenting the scope change.

Status of the computation family: COMPLETE within assigned reproduction/falsification scope. The bare-classifier route is BLOCKED by an exact counterexample and may be reopened only after a materially explicit convention repair. The parity-repaired route survives the finite checks. Overall discovery percentage is not inferred from a test count; audit completion is 100% for this family's bounded task. Historical author effort remains 2/5. No novelty, priority, acceptance or all-n certification is asserted.
