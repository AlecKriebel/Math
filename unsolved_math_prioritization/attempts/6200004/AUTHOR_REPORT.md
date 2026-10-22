# Frozen author report: Davis's dimension-ratio problem (6200004)

## Verdict proposed for independent review

**Partial results; original unresolved. Five substantive author turns used.**

No example of a nontrivial torsion-free Gromov-hyperbolic group G with

    cd_Q(G) / cd_Z(G) < 2/3

has been constructed. No proof that all such groups obey the opposite inequality has been obtained. The source's equality examples (2,3), a compactum without a certified group-boundary realization, and conformal-dimension growth do not answer the question.

This packet is frozen for independent review. It does not authorize a solved label. There is no sixth search turn. Final publication and shared-queue changes remain outside this author checkpoint.

## Recovery and provenance

- Repository: AlecKriebel/Math; authorized per-problem branch: dot/math-6200004.
- Recovered commit: fd707b73b09f2ea4ef325b7993f75ebb10e758e8, whose message records turn 4.
- All 33 attempt files were recovered through the connected GitHub reader. Every one of the 32 SHA-256 entries in TURN_4_MANIFEST.json matches, and the manifest's Git blob is separately recorded in RECOVERY.json.
- All 10 primary PDFs were independently downloaded to the local review workspace and match the byte hashes in the original source manifests. Those PDFs and extracted text are review inputs only, not proposed repository uploads.
- On 2026-10-03, all-state PR searches for the exact ID, branch head, and Davis returned no PR. The branch head was still the recorded turn-4 commit. This supplements, rather than replaces, the original broader duplicate gate.

## Exact source and credit

Kapovich's author-hosted *Problems on Boundaries of Groups and Kleinian Groups*, dated October 24, 2007, printed page 3, Problem 4 (Mike Davis), gives the exact strict ratio question. See SOURCE_NORMALIZATION.md for the original AIM workshop context and definitions. The question concerns projective dimension over group rings, quantified over all modules.

Foundational input is credited to Bestvina–Mess (boundary dimension and existing examples), Davis and related Coxeter compact-support formulas, Dicks–Leary (prime-field detection), Dranishnikov (Z-boundary cohomology and Markov compacta), Bowditch and the accessibility/boundary results he cites, and Arora–Martínez-Pedroza (finitely presented subgroups in rational dimension two). The recent fibering and conformal-dimension papers are only used in their stated scopes. No originality claim is made for the derived exclusions.

## Strongest retained partial results

1. Every putative witness has rational dimension q>=2 and integral dimension d>=floor(3q/2)+1. The first possible pair is (2,4). In boundary dimensions r=q-1 and n=d-1, the target is 3r+1<2n, retaining the essential shift.
2. For finite-type groups in this setting, a coefficient drop forces top integral group-ring cohomology to be nonzero bounded-exponent torsion, detected by some F_p. Only finitely many primes can exceed the rational dimension. This does not impose the desired ratio by itself.
3. Closed connected PL manifold nerves give (n+1,n+1) in the orientable case and (n,n+1) in the nonorientable case. Their torsion-free finite-index Coxeter groups therefore cannot beat 2/3. Barycentric flagification alone does not ensure hyperbolicity.
4. Clique inflation, coning, and full-simplex clique sums cannot improve the ratio from those seed families. Joins of two infinite factors violate hyperbolicity, and products do not improve the ratio under the proved hypotheses.
5. A witness can be reduced to a one-ended torsion-free hyperbolic group with the same d and no larger q. A finite cyclic splitting retains a high-dimensional violating vertex. This is not an absolute-rigidity theorem for arbitrary iterated JSJ operations.
6. A finitely presented nonhyperbolic subgroup forces q>=3. This excludes the cited integral-dimension-three and -four F2-but-not-F3 fiber-kernel examples as answers; it does not exclude all higher-dimensional algebraically fibered groups.
7. The final turn excludes the unsymmetrized simplex-seeded Section 3 Markov towers: their relative mod-p dimension is n, but global top Čech cohomology vanishes. Hyperbolic-group boundaries cannot have that discrepancy. A sphere seed passes this one test, and no blanket nonrealizability theorem is asserted.

All claims, hypotheses, proofs, and limitations are in TURN_1.md through TURN_5.md. These statements are an author submission for review, not an independent review verdict.

## Exact remaining gap

Either construct a torsion-free Gromov-hyperbolic G and rigorously determine q,d with 3q<2d, or prove 3q>=2d for every admissible G. The unexplored general singular no-square-nerve and genuine boundary-realization problems remain central. Converting an algebraic or compactum dimension profile into an appropriate proper cocompact hyperbolic action has not been achieved. The present exclusions do not establish a universal lower bound.

## Verification

All five deterministic Python checkers run with the standard library only. Earlier outputs match the saved checkpoint exactly: 8,218 + 680 + 81,584 + 2,818 assertions. Turn 5 adds 4,945 assertions, totaling 98,245. Assertion counts measure finite controls, not mathematical coverage or proof probability. These computations do not construct the missing group.

Run python reproduce_checks.py from this directory. It compares every JSON result with the saved output and verifies the recovered file/source hashes. It leaves historical outputs unchanged. FREEZE_MANIFEST.json binds all proposed author/checkpoint files; local primary-source hashes are listed separately.

## Completion estimate

The bounded author attempt is 100% complete (five of five turns). Best-guess completion toward resolving the original research goal is 15%, a heuristic progress estimate required by repository practice, not a calibrated probability. The original remains unsolved by this work.
