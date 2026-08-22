# Provisional independent assessment before author-record comparison

**Manuscript:** *Positive Recurrence for Single-Linkage Bimolecular Weakly
Reversible Stochastic Reaction Networks*  
**Assessment frozen:** 2026-08-21 22:38 PDT  
**Purpose:** record the merged blind conclusion before opening any existing
author audit, preservation record, validation summary, reviewer checklist,
research/revision log, or committed expected verification report.

## Independence record

The three separated preliminary reports were completed before their
conclusions were merged:

| Track | Preliminary report SHA-256 | Information barrier |
|---|---|---|
| Analytic proof | `b4980e653ea89752164966a13019d25c84f6de9c3c020d779fd529dc249a03ff` | Manuscript/PDF/TeX/bibliography only; no code or author records |
| Software static | `8a149263eaefcf785f24e74f52bb158b5c033fc0cb9895796e0858975b84e0e6` | Manuscript and complete implementation/tests/tooling; no execution, golden output, or author records |
| Adversarial | `44c254a4a820df5fd6f45d3a3699b7a8d2f4960ec096fceec25ab7bc684f9daf` | Manuscript/PDF/TeX/bibliography and public primary sources; no code or author records |

The main referee separately read all 16 manuscript pages, reconstructed the
proof, and read all 1,846 source-module lines and all 868 test lines before this
merge. The reports were not used to steer one another.

## Exact result assessed

For a finite labelled stochastic mass-action network on
`N_0^d`, with strictly positive channel rates, molecularity at most two at
every source and target complex, and a weakly reversible complex graph with
one linkage class, the set reachable from any initial population is a single
closed communicating class. Each nonabsorbing reachable class supports a
nonexplosive minimal CTMC and has finite expected positive physical return time
to every state. An absorbing reachable class is a singleton. Consequently
each reachable class has a unique stationary probability law.

## Blind analytic conclusion

All three mathematical reconstructions, including the main referee's, found
all twelve requested load-bearing implications valid:

1. return paths lift with a fixed nonnegative residual and make reachability
   symmetric and closed;
2. the labelled-target augmentation is Markov and irreducible and has an
   autonomous ordinary-population projection;
3. the shifted log-factorial potential is proper and its increment is exactly
   `log((x)_t/(x)_s)`;
4. target-following episodes include every deviation and obey the displayed
   recursion, including zero-length paths;
5. both scalar-envelope branches, monotonicity, and finite backward
   propagation of negative divergence are correct;
6. compactification retains divergent coordinates whose normalized weight is
   zero and gives the asserted factorial asymptotics;
7. the A/B/C bimolecular top-complex split is exhaustive, including unary,
   repeated-species, bounded-companion, and exact-invariant branches;
8. the exceptional Foster set is finite and nonempty;
9. deterministic finite-horizon bounds discharge integrability, so the
   stopped supermartingale and monotone-convergence argument are valid;
10. the finite trace-chain return is correctly converted to original jump
    count, and marked return projects to population return;
11. recurrent visits to one state rule out explosion, the uniform positive
    lower rate converts jump count to physical time, and the regenerative
    occupation law is valid; and
12. irreducibility supplies uniqueness, while absorbing singletons have their
    point masses.

No counterexample was found among zero complexes, self/parallel channels,
equal displacements, boundary faces, parity classes, `2S_i`, absent species,
zero-weight divergent coordinates, zero-length target paths, extreme but
positive rate ratios, finite shells, or absorbing states. Multiple linkage
classes and molecularity three were confirmed to be excluded rather than
silently covered.

Independent, production-free scratch checks supplied additional falsification
evidence: one track checked 136,020 exact factorial identities and 56,728
three-species top configurations; another checked 5,238 factorial cases,
58,044 two-/three-species top configurations, an independently enumerated
episode recursion, and both scalar branches. These finite checks do not replace
the proof.

## Blind static software conclusion

The canonical report is genuinely recomputed twice and compared byte-for-byte
with a committed expected report. Its strongest finite checks are exact
factorial and entropy identities, lifted return paths, a cross-interface ACK
episode calculation, a 98,261-case three-species certificate atlas, and 5,000
fixed-seed four-species stress cases. Exact rational arithmetic and canonical
sorting avoid floating-point or nondeterministic-output concerns.

The software does not implement most universal probabilistic implications:
general augmented irreducibility, properness, arbitrary episode recursion,
compactification, the exceptional set, stopped-process integrability, trace
conversion, nonexplosion, or regeneration. The manuscript and software README
accurately describe the computation as finite falsification and
reproducibility evidence, not a proof.

Minor static coverage limitations are the unsupported all-self-channel
reduction in the helper data model, a scalar-envelope test narrower than the
displayed lemma, and edge-case labels that do not fully exercise the
zero-length final jump or unrestricted face successors. These do not affect
the analytic theorem and are correctly outside the verifier's stated universal
claim.

## Primary-source and novelty comparison

The checked primary/official sources support the manuscript's material
comparisons: Anderson--Kim formulated the conjecture; Anderson--Cappelletti--
Kim proved the binary one-linkage case with the additional pure-species
condition and used the described boundary branch; Pauleve--Craciun--Koeppl's
``recurrence'' is combinatorial reachability; Xu v2 proves bimolecular weakly
reversible nonexplosion while still recording positive recurrence as open; and
official 2022/2025 programs plus the ConStRAINeD page describe the broader
two-species result as announced/complete with its manuscript still in
preparation. Exact-title and topic searches found no public duplicate of the
present arbitrary-species, one-linkage binary theorem. This is time-bounded
evidence, not proof of absolute priority.

## Provisional finding and disposition

The sole common concrete defect is artifact provenance: the copied packet has
no internal Git metadata, the exact claimed public
`bimolecular-positive-recurrence-v1.2.4` tag is absent from the configured
remote, and both exact manuscript GitHub links return 404. Matching public
tags stop at v1.2.3. The packet bytes can still be audited and reproduced, but
the manuscript's present-tense tagged-release claim cannot currently be
verified. The narrow repair is to publish the exact tag and confirm its target,
or revise the availability wording to describe the standalone packet.

Subject to the still-pending canonical replay, mutation tests, artifact byte
rebuild, and comparison with author-generated records:

- **Provisional mathematical status:** CORE RESULT SOUND, REVISION REQUIRED.
- **Provisional journal recommendation:** minor revision.
- **Reason:** the theorem and proof are affirmatively verified; the required
  correction is a noncentral but reproducible release-availability claim.

This assessment is now frozen as the pre-author-record baseline.
