# PR 37 recurrence/orientation family audit

**Verdict: PASS_SCOPED_KNOWN_THEOREM_CONSEQUENCE. No mandatory mathematical
correction found in the frozen recurrence/orientation reduction. The full
KP-5.2 target remains unsolved.**

This audit concerns numeric 3009, original head
`84bb43d21b36e4d97229806e2518fbc135bee786`, base
`c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. The frozen PARTIAL.md hash is
`c24cf9578f26202c2af4e25d017a5e44d7047ad32e7f35ebac0604275399f00f`.
The original 13/14 diff is frozen; the original substantive accounting remains
1/5, proposed outcome unsolved; audit accounting is 0. No new proof search or
repair to the frozen package was undertaken. All authored outputs belong to
this family's directory. Root owns integration and any publication.

## Independent evidence and exposure

The complete literal source record was read first and sealed in
SOURCE_FIRST_SEAL.json at 2026-10-02T07:38:04Z. PARTIAL.md was then read. The
complete operative Kolev–Pérouème v3 PDF, K3 printed pages 302–303, and rendered
operative theorem/target pages were inspected. SEALED_PROOF.md was sealed at
2026-10-02T07:48:21Z before historical reviews and root/sibling interpretations.
Its SHA-256 is
`91a6e5e2df7c3bfff92657586f3d3f0ec5988a20876cfafa6cbaaecdb5fc012a`.
Historical review content and the root's source-dependency observation were
read only afterward. No sibling interpretation was read. The sealed proof
remains byte unchanged.

The strongest verified deduction is the stated low-dimensional identity
consequence, conditional on the accurately cited established planar theorems.
No novelty, priority, exhaustive literature, self-contained reconstruction of
prime-end theory, or complete higher-dimensional solution is certified.

## Findings

| Audited mechanism | Result | Exact boundary |
|---|---|---|
| Full-orbit diameter versus displacement | Same constant D, for every integer exponent, by rebasing at the second orbit point | One-step displacement and individually bounded orbits do not suffice |
| Orientation | Straight-line homotopy is uniformly proper and extends jointly over infinity; degree stays +1 | The intermediate maps need not be homeomorphisms |
| Sphere recurrence | Chordal factor 2 and both denominator estimates are correct; radius precedes recurrence index in the epsilon argument | This is not global Euclidean uniform convergence |
| Kolev–Pérouème Theorem 1.1 | Exact required scope: recurrent, orientation preserving, nonidentity S^2 homeomorphism; two fixed points | The theorem does not assert the same fixed-point count for S^3 or arbitrary dimension |
| Line case | Global bound excludes decreasing maps; increasing motion contradicts positive-exponent recurrence at the moved point | Reflection is a recurrent control failing the global bound |
| Closed ball extension | Boundary agreement and the similarly pasted inverse give a homeomorphism; recurrence and diameter <=2 extend | Boundary fixation does not ensure a smooth seam |
| Strong smooth case | The low-dimensional homeomorphism conclusion applies to smooth maps with the stated returns | No derivative estimates or higher-dimensional smooth theorem are proved |
| Local/manifold remarks | No theorem for these variants is claimed by frozen PARTIAL | A precise quantitative smallness formulation is needed; the naive finite-D annulus version is false |
| Equicontinuity, compact closure, periodicity, locally compact action | None is substituted into the actual planar proof | A returning sequence supplies none of these as a proved extra hypothesis |

The filled-continuum construction also meets the stated Cartwright–Littlewood
hypotheses: it is nonempty, compact, connected, invariant, and nonseparating,
and contains a disk. The two fixed-point regions are disjoint when their
centers are more than 6D apart. Infinity supplies the third sphere fixed point.
This family did not reread Brown's historical primary proof and does not
pretend that finite algebra checks verify that theorem.

## Imported theorem proof dependency

Kolev–Pérouème v3 Lemma 3.1 asserts that the relevant component of an
intersection of Jordan domains is a Jordan domain, citing Newman Theorem
16.3. The exact cited book theorem was not independently inspected here. The
paper additionally relies on the prime-end results of Epstein/Mather,
Brouwer translation arcs, and Brown–Kister invariance. Reading v3 checks what
the published theorem asserts and how it is used; it is not a self-contained
verification of every foundational import. No actual counterexample to the
Jordan-component step or theorem has been verified by this family. This is a
documented dependency/validation limit, not presently a fatal error in a
package explicitly importing the established Theorem 1.1. The annulus-lift
normalization was independently explained in the sealed proof.

The operative v3 has manuscript date 12 August 1996 and arXiv revision date
2 March 2009; arXiv records the 1998 journal publication. The journal PDF was
not obtained. Both successfully fetched primary PDFs have exactly the hashes
recorded in frozen provenance. Fetch/render receipts and failures are retained.

## Actual replays and counter-controls

The authored replay helper copies exact frozen scripts into ignored isolated
directories, executes each by absolute path, records the interpreter, cwd,
hashes, actual return code, stdout/stderr, and output hashes, and compares
fresh results with the saved originals. It does not run a frozen script in
place or alter its saved result.

| Actual replay | Observed result |
|---|---|
| Exact check_controls.py | 31 assertions pass; saved JSON matches byte and structure |
| Exact historical independent_checks.py, read after seal | 8,462 assertions pass; saved JSON matches byte and structure |
| Delete factor 4 in squared chordal identity | Nonzero exit at chordal_metric_identity |
| Multiply tail formula by R^4 | Nonzero exit at tail_bound_derivative |
| Replace 7D center separation by 6D | Nonzero exit at two_fixed_point_regions_disjoint |

The independent checker passes six separately identified calculation and
construction groups and rejects 11 explicit false inferences. Its evidence
includes exact rational boundary/metric tests, signed-exponent rebasing,
Pell-return irrational rotations, a radial smooth-seam failure, an annulus
scope counterexample, an S^3 fixed-circle control, and an explicit recurrent
non-equicontinuous compact-space homeomorphism. The last control is not a
manifold or KP-5.2 counterexample. Its analytic tail and separation estimates
hold for the entire infinite construction; the finite calculations are replay
controls, not the proof of the infinite claims. It also disproves a general
compact-cyclic-closure inference, but does not independently certify a
non-locally-compact closure example.

The bundled and system runtimes initially lacked SymPy. The initial replay
therefore failed with ModuleNotFoundError, and all corresponding failure
receipts remain in original_replay_attempts.json and family_execution_receipts.json.
The expected-mutant guards correctly did not count dependency failures as
successful rejection. Pinned SymPy 1.14.0 was installed only inside ignored
tmp/replay_env. The rerun then passed baseline comparisons and produced the
intended assertion failures in the actual altered scripts.

## Remaining gap and disposition

There is no verified higher-dimensional mechanism under precisely global
bounded full orbits and compact-open recurrence, including the ball and stronger
smooth variants. The informal local/manifold extension also needs its own
well-typed quantitative hypotheses. Substituting a compact or locally compact
cyclic closure transfers the central difficulty to an unsupported claim.
Promote only the credited low-dimensional consequence with the full target
unsolved and no novelty claim. This audit provides no reason to change the
frozen substantive count or to open a new proof-search response.

No other individual was contacted. No canonical research, shared integration,
Git, remote, PR, or release write was made by this family. Foreign reference
bytes, copied replay scripts/results, and dependencies remain only in ignored
tmp. The authored_manifest.json is an exact authored-file allowlist; its
verification receipt checks the seal and final directory inventory.
