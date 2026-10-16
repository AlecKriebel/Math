# Acceptance report: KP-4.104 / 2980

## Disposition

Accept the authored partial results with the separately preserved source-completeness correction. The original and audit freezes are retained verbatim. The current report is `audit/public/REPORT.corrected.md`, reconstructed exactly from `original/public/REPORT.md` and `audit/public/SOURCE_COMPLETENESS.patch`. Auditing and publication add no substantive mathematical attempts: **5/5; unsolved**.

The target concerns nonsingular complex curves properly embedded in the standard four-ball, with one transverse boundary link type and one smooth isotopy class, yet distinct complex isotopy classes; stronger symplectic separation and infinitely many examples are also requested. None of those three clauses is resolved here. Marked boundary/collar problems must not be silently substituted for the unmarked transverse-link convention.

## Accepted mathematical content and limitations

1. The stationary-collar symplectic-isotopy extension argument is valid. A prescribed first jet of a Hamiltonian produces the symplectic-normal velocity, and a cutoff gives support away from the stationary collar. This local argument cannot supply a globally positive interpolation. The two exact endpoint forms and their degenerating midpoint demonstrate that exactness and cohomological agreement do not suffice.
2. The tempting two-Hurwitz-orbit braid example loses its proposed distinction after simultaneous conjugation. Direct braid relations establish factor-by-factor conjugacy; the independent integer-matrix calculation corroborates it. The calculation does not establish complex isotopy or classify all geometrically allowed presentation changes. Three-braid finiteness is not finiteness over arbitrary stabilized representatives.
3. The known annulus family cannot supply the desired smooth-class counterexample: its double branched covers have varying first homology. The universal integral relation-matrix reduction gives the rectangular diagonal form with entries 1, 1, n and a zero row. Distinct positive odd parameters yield different group orders. Even parameters belong to a disconnected-surface subfamily. Matching selected invariants would not by itself prove smooth isotopy.
4. The Stokes obstruction for a symplectic surface whose actual geometric boundary remains Legendrian is valid, without an exactness assumption on the original Lagrangian. The source-completeness correction is necessary: known CGHS conversion results already supply moved-boundary symplectic surfaces and complex representatives, retaining the unmarked smooth class through tracked smooth isotopies. Their existence must be credited. They do not transfer Hamiltonian non-equivalence to symplectic or complex non-isotopy. Prescribed extra boundary markings still require control. The degree-four capping consistency test is conditional on the standard unmarked capped setting.
5. The standard capping/adjunction calculation and the fixed-ball transversality wall are valid with their stated hypotheses. The Golla–Starkston labeled incidence convention is retained. The imported Siebert–Tian degree-at-most-17 result and the standard capping correspondence do not produce an arbitrary boundary-fixed isotopy or a complex path through a fixed ball. Smooth algebraic curves can cross the real boundary-transversality wall without reaching the complex discriminant.

These are accepted obstructions, reductions, and exact calculations. They are not actual target examples, an impossibility theorem, an infinite-family construction in one smooth class, or a novelty determination. Imported geometric theorems remain external inputs rather than machine-certified facts.

## Exact correction and immutability

Original report: 25,467 bytes; SHA-256 `b05408b043af27f7ad7ca28e737bfd3f92a47a37badceaaad7b1a3d3662fe7b5`.

Corrected report: 26,685 bytes; SHA-256 `1372f3c3de364d04472a17c67085324041ee6f7dbfc30e1fd2c1abbcd98910a0`.

Two-hunk correction: 5,556 bytes; SHA-256 `ba36649ad1875f9ee1305274f4899e90410bbd3f8ddadc9667e861e7dafe4c9d`.

The patch alters only the Section 4 conversion discussion/exact gap and adds the CGHS reference. It does not alter the Stokes lemma, checker, five-approach count, or unresolved disposition. Historical `RESULT.json` is preserved, so its compressed conversion-gap phrase is interpreted through this correction, not as the current gap formulation.

## Verification boundary

The portable publication layer authenticates every member, both archive inventories, the frozen manifests, the exact patch reconstruction, all result types, and complete original and independent outputs. Genuine UID/EUID 1000 read-only tests cover normal, `-O`, and `-OO`; the original checker, independent checker, and native harness have zero `assert` statements. Each native harness invocation reproduces 6 successful baselines and 30 deliberate mathematical failures across all three optimization modes. Validation uses explicit checks that survive optimization. The complete native receipt is compared with the preserved receipt, with only runtime Python version normalization.

Publication controls additionally test trusted-bootstrap substitution defenses, exact inventory, duplicate/nonfinite JSON, boolean-versus-integer and float-versus-integer confusion, altered manifest schemas, self-consistent repinning attacks, patch corruption, symlinked roots/ancestors/members, special files, and hostile-working-directory relocation. These checks establish artifact integrity and bounded arithmetic reproducibility; none decides a geometric isotopy question.

Fresh public-source and corpus bindings: **NOT_RUN**. The prior independent audit rechecked the nine original PDF byte/hash pins and separately pinned CGHS; its retrieval and inspection metadata remain historical evidence. No source bodies are shipped. Current-source inspection or a new exhaustive literature search is not implied by a portable PASS.

## Public references

- Cao, Gallup, Hayden, Sabloff, *Topologically distinct Lagrangian and symplectic fillings*, MRL 21 (2014), 85–99: https://arxiv.org/abs/1307.7998 and https://doi.org/10.4310/MRL.2014.v21.n1.a7.
- Casals–Gao, *Infinitely many Lagrangian fillings*: https://arxiv.org/abs/2001.01334.
- Baykur–Van Horn-Morris, *Fillings of genus-1 open books and 4-braids*: https://arxiv.org/abs/1604.02945.
- Orevkov, corrected quasipositive three-braid factorization manuscript: https://arxiv.org/abs/1409.4726v3.
- Golla–Starkston, *The symplectic isotopy problem for rational cuspidal curves*: https://arxiv.org/abs/1907.06787.
- Siebert–Tian, *On the holomorphicity of genus two Lefschetz fibrations*: https://annals.math.princeton.edu/2005/161-2/p09.

## Repository scope

The publication is limited to this source-free attempt directory and the existing complete `unsolved_math_prioritization/QUEUE.md`, changing only rank 1052 / 2980's Status, Turns, and Findings cells. All other queue bytes, notes, and chat links are preserved. No merges, releases, or external outreach are part of this publication.
