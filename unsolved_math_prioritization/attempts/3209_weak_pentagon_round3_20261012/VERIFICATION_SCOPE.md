# Verification scope and reproduction limits

This prose edition preserves the complete proof and audit arguments, plus all important aggregate counts and scope qualifications. It is not an executable reproduction bundle. Original programs, source data, generated streams, raw certificates, manifests, and machine receipts are excluded. Mathematical deductions can be read here, and the two literal graphs and displayed maps can be independently reconstructed. The original exact seeded streams and every catalog witness cannot be replayed using this edition alone.

## What establishes which claim

The universal 1+4 theorem rests on the elementary argument: distinct demand magnitudes, a slot-count degree-list bound, a strict surplus in every nontrivial boundary component, the injection into free demand orientations for isolated empty-list candidates, and greedy completion with at most six forbidden colors out of eight. No signed choosability theorem is used.

The universal degree-four boundary theorem rests on the exact signed reduction and its end-block argument, together with the expressly retained Schweser–Stiebitz Theorem 2.1(a),(c),(e) and Lemma 2.4. The application uses original palettes only at non-cut vertices, retains opposite-sign multiplicity, establishes original-graph component closure, excludes degree-eight bricks by an unbalanced triangle or 20=3|N|, and excludes degree-four bricks by nonsymmetric lists or a negative triangle.

The two impossibility claims are elementary finite constructions, with ordinary signed degrees (5,5,5,5,8) on the 18-vertex graph and a full-palette doubled K₅ obstruction. The completion preserves the old obstruction. Neither conclusion comes from a timeout, a bare solver UNSAT flag, catalog completeness, or random sampling.

## Exact explicit-graph computations

For the 18-vertex graph, all 131,072 normalized cuts were examined. Equal ports have maximum 21 attained 30 times; unequal ports have maximum 22 attained 7 times. Each port relation in the ten-new-vertex gadget has 1,024 assignments. Equal ports give gadget maximum 14 attained once; unequal ports give 13 attained six times. Hence the cubic maximum is max(21+14,22+13)=35, attained 30·1+7·6=72 times.

The mixed audit additionally enumerated all 134,217,728 normalized cuts of the 28-vertex graph, returning 35 and 72, with direct edge-sum checks at 1,344 points including the final state and five known-small-graph controls. The 18-vertex maximum is 22 with count 7. The two displayed maximum masks are 85338 and 16517114. The cut sizes 20 and 34 fail global optimality by the gain-one switch {0,2,10}. They are nevertheless strict single-vertex local maxima.

The second audit checked graph identity against those exhaustive-enumeration inputs, then directly validated all 7 and 72 distinct normalized maximum-cut witnesses from the tester. Distinctness, exact maximum size, and equality with the exhaustive count prove that all maxima of these two graphs extend. This is not a universal maximum-cut theorem. The first audit alone checked one prescribed maximum per graph; its original narrower wording is retained in the complete report.

Additional mixed-graph finite checks: 1,170 same-parity cube tuples of lengths zero through three; 4,681 boundary-role tuples of lengths zero through four; 2,048 mixed-list assignments with zero colorings; 32,768 full-palette doubled-K₅ assignments with zero colorings; 32,768 ordinary-graph full-palette assignments with 2,880 colorings; 65,536 orientation/list-assignment checks. The two explicit graphs, both signed reductions, unrestricted and displayed maximum maps, switches, and factorized maxima were independently reconstructed.

## Catalog target coverage

The supplied catalogs have 8,738 records at orders 6,8,…,18. The independent audit examined 1,049,918,752 normalized cuts and found 106,875 matching-complement targets with four or five demands. Every target had a directly validated positive witness:

- 2+2: 64,221 local nonglobal cuts and 9,426 global cuts.
- 4+1: 33,201 local nonglobal cuts and 27 global cuts.
- Total: 97,422 local nonglobal and 9,453 global cuts.

The complete per-order table is retained in FINITE_VERIFICATION_REPORT.md. This targets local cuts as well as global maxima, rather than merely repeating an earlier unrestricted global-maxima screen. The independent checker validates graph structure and computes the target set before comparing supplied witnesses. It rejects omitted, duplicated, malformed, extra, and non-target records. Exact supplied-record coverage is a checked fact; provider completeness and nonisomorphism are not independently proved.

## Generated and constructive checks

Seven batches contain 520,000 distinct labeled graphs with designated cuts and directly checked extensions. Their exact dimensions, counts, seeds, and software versions are in SOURCES.md. Their designated cuts are strict single-vertex local maxima because the graphs are cubic with matching complements; global optimality was not computed. The samples' failure to encounter the explicit cubic 1+7 obstruction is a concrete warning against extrapolating a universal theorem from random positive results.

The elementary constructor passed 163,228 tests in each of normal Python, -O, and -OO: 33,228 catalog 4+1 cuts, 120,000 generated 4+1 cases, and 10,000 deterministic subcubic edge-deletion variants retaining the unique minority demand and allowing zero through four opposite demands. Independent supplementary tests covered 48,231 cases from every labeled simple triangle-free subcubic graph on two through six vertices and every eligible normalized cut. Among these, 27,128 are disconnected and 21,668 have isolated vertices. Three additional relabeled/complemented cases exercised four potentially empty isolated boundary lists simultaneously.

Finite template checks cover exactly six local third-neighbor slot types, 75,265 orientation-injection templates, and 588,768 degree-list templates in the declared universes. The independent template checker uses MRV backtracking rather than the source's rooted-tree greedy procedure and also checks 1,170 cube tuples. Their applicability to arbitrary graphs follows from the written proof, not extrapolation from the finite totals.

The finite catalog diagnostic has 213 distinct degree/touch signatures among the 33,228 five-demand cuts, including 226 cuts with four deficient boundary pairs all of auxiliary degree six. This disproves the tempting simplification that all boundary pairs automatically satisfy the degree-four condition; it is not a premise of the elementary lemma.

## Negative controls and optimization safety

The mixed audit ran twenty independent rejection controls and seven upstream inventory rejection controls in each Python mode. They cover missing and extra files or directories, append and same-length payload mutations, changed manifests, manifest and payload symlinks, recomputed internal hashes against a fixed external pin, graph or demand mutations, inconsistent boundary orientations, wrong or out-of-range maps, unrestricted maps falsely claimed as prescribed, deleted signed constraints, and false maximum values or counts. The source graph builder was compared against the pinned graphs. All mutation copies were disposable; frozen originals were rechecked.

The testing packet had sixteen mutation/control tests for wrong maxima, bad witnesses, missing or duplicated cuts, coordinated input truncation, missing or extra records, wrong prescribed cuts, removed obstruction constraints, and corrupted ordinary or unrestricted witnesses. Complete replay and optional byte-for-byte regeneration were recorded by its author. The independent audit inspected the terminal author logs and checked their receipt identities without redundantly rerunning random generation; it independently validated every positive certificate. The stated C++ standard-library dependence remains.

The 1+4 audit ran 155 hostile controls per Python mode with byte-identical outputs. Every one of the 99 source payloads, including all catalogs and certificates, was mutated and rejected. Further controls cover a changed manifest, added file, same-byte symlink, false maxima, wrong and out-of-range labels, negative certificate flags, nonnormalized cuts, missing or duplicated targets, missing or extra records, coordinated catalog/certificate truncation, trailing fields, duplicate generated edges or graphs, wrong designated cuts, removed negative constraints, corrupt unrestricted and maximum witnesses, and an omitted global maximum. Positive and restored-inventory controls pass. Both original and new checkers reject corresponding mutations.

The independently packaged final replay subsequently completed successfully, with both source and audit freezes unchanged. Its complete-certificate, three-mode, 155-control, proof-edge-case, and all-79-witness checks reached terminal success. This is a recorded original replay result, not a runnable-public-bundle claim.

All acceptance decisions use explicit runtime checks; Python optimization does not remove them. The complete construction, templates, negative examples, independent diagnostics, inventories, and hostile controls were checked in normal Python, -O, and -OO. The source main freeze covers 99 payloads plus one manifest; its separate lemma freeze covers a 16-file subset, not a second closed directory. The mixed audit covers 27 payloads and the 1+4 audit covers 52 payloads, each with its own closed inventory and external pin. These historical inventory counts are verification scope, not identities of undistributed artifacts.

## Edition preservation and final limits

Six complete authored source documents have reversible editorial maps. Only operational identities, byte counts of excluded artifacts, misleading public replay directions, and final companion-status references were editorially changed; no mathematical proof is abridged. Public source identities and mathematical counts are preserved. Preparation validates the actual public examples and vectors, closed payload inventory, scope boundaries, source metadata, and exact reversible preservation. It does not rerun the billion-cut catalog audit or claim human review.

The original Weak pentagon target, the proposed universal fixed-global-maximum strengthening, and the mixed 2+2 four-demand case remain unresolved in this round. No later-round result is included. The third-round count is confirmed; earlier lifetime work totals remain unknown.
