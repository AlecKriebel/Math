# Research log

Actual model: gpt-6-astra, reasoning effort xhigh. All timestamps are UTC on 2026-09-30. Research ceiling: 11:06–13:06; at most five substantive approaches.

## Source gate, 11:06–11:13

Read repository policy, queue, exact pinned record and full original Achenjang report. The original definition is broader than several later uses of “stacky curve”: it permits non-Deligne–Mumford tame inertia and nontrivial generic stabilizers, and defines the cohomological Brauer group. No earlier problem-specific attempt, branch, PR or duplicate was found. The source-code-keyed upstream report is null. The local desk assessment only suggested Leray and possible existing coverage. Completion estimate: 5%.

The full current Achenjang and Bishop papers were retrieved and their relevant hypotheses and proofs read. The later Bishop–Newman nodal paper and Lopez classifying-stack paper were checked for scope. Neither was silently promoted to a full solution of the original arbitrary-stack target.

## Approach 1: local stabilizers and coarse-space Leray, 11:13–11:16

For a dense schematic open, all positive higher direct-image sheaves have finite support. Achenjang's connected-inertia local Picard contribution is p-primary, while its target finite-group H² is prime-to-p torsion; the connecting map must vanish. Combined with the known curve cohomology vanishing, this gives a direct sum of the étale stabilizer quotients' Schur multipliers. The proof is saved in PARTIAL.md. It does not cover generic inertia. Completion estimate: 20% of the full target.

## Approach 2: global gerbe dependence, 11:16–11:19

Computed two smooth proper tame Deligne–Mumford curves over the same coarse P¹ with the same μℓ² stabilizer everywhere. The neutral product has Brauer group Z/ℓ; the product of the O(1) root gerbe with Bμℓ has Brauer group zero. The Picard weight sequence and Kummer sequence identify the difference. This does not refute the original problem; it rules out discarding the global gerbe class. No general transgression/extension formula was obtained. Completion estimate: 20%.

## Approach 3: connected generic inertia, 11:19–11:20

Applied Achenjang's classifying-stack theorem to A¹×Bμp in characteristic p. Artin–Schreier gives an infinite p-primary group, with an explicit normal form indexed by positive exponents prime to p. This is a credited special-case computation and an elementary normal-form deduction, not a full classification. It records why tame does not mean prime-to-characteristic inertia outside the Deligne–Mumford case. Completion estimate: 20%.

## Checkpoint

The full target remains unresolved after three approaches. The polished partial proof is saved; executable finite controls and separate review remain pending. The unresolved part is the actual computation of generic-inertia sheaves, transgressions and extension data, not just naming a spectral sequence. No fourth or fifth approach has been used.

## Frozen verification, 11:28 UTC

All 77,458 exact finite controls pass. The mathematical text and checker are frozen for separate adversarial review. The remaining generic-inertia problem is not resolved, and no fourth or fifth approach will be pursued without a materially new mechanism. Completion estimate remains 20%.

## 2026-09-30 11:41 UTC — Independent review completed

Separate adversarial AI review passed the frozen partial claims without a mandatory correction. All 77,458 author controls reproduce byte-identically and 40,882 independent exact controls pass. The full original computation remains unsolved, 3/5; completion estimate remains 20%. No new proof attempt or novelty claim is added.
