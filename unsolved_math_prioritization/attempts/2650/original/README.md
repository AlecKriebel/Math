# Coherence with polycyclic pro-p amalgamation: scoped results and obstructions

**Target:** numeric ID 2650, Kourovka Notebook Problem 21.141 (P. A. Zalesskii).
**Status:** unresolved after five substantive attempts; no full solution,
refutation, or novelty claim. Date: 3 October 2026.

The question asks whether every proper free pro-p amalgam of coherent
pro-p groups over a polycyclic subgroup is coherent. A coherent pro-p group
has all its finitely generated closed subgroups finitely presented in the
pro-p category.

This package preserves proofs of positive special cases and failed routes.
They are provisional AI-assisted research notes for independent expert
scrutiny, not an accepted resolution of the Notebook problem.

## Mathematical contents

1. `turn_01.md`: finite subgroup-decomposition criterion, explicit
   generator/relation bounds, and the missing pro-p subgroup-structure step.
2. `turn_02.md`: extension and quotient permanence; coherence when the edge
   has an open procyclic subgroup, including finite-edge amalgamation.
3. `turn_03.md`: lifting coherence through a polycyclic normal kernel; the
   common-normal-kernel reduction includes arbitrary-rank central and normal
   amalgamation.
4. `turn_04.md`: explicit two-generator, arbitrarily long, reduced proper
   graphs with rank-two abelian edge groups; faithful finite-edge quotients
   show why a rank-only uniform accessibility estimate is unavailable.
   All groups in this family are coherent.
5. `turn_05.md`: the natural inverse limit of the preceding chain family is
   free pro-p; an arbitrary set of two-generator pure-power commutation
   relators has a finite minimal exponent frontier. Neither route gives a
   counterexample.

`SOURCE_GATE.md` records exact target identity, credited prior work, dated
literature limits, and unsuccessful access to the exact catalogue page.
`RESEARCH_LOG.md` records the five-turn budget and completion estimates.
`status.json` states the unresolved exhausted status in machine-readable form.

## Prior work and remaining gap

Chatzidakis–Zalesskii's procyclic-edge decomposition theorem and
Castellano–Zalesskii's malnormal analytic-edge coherence theorem are credited
inputs. The elementary deductions here do not establish historical novelty.
The full problem remains at the finite subgroup-structure/accessibility
step for a general higher-rank, core-free polycyclic edge with no
acylindricity hypothesis.

## Reproduce the finite checks

Run from this directory with Python 3 and its standard library:

    python chain_obstruction.py
    python power_commutator_frontier.py
    python verify_artifacts.py

The checks cover 128 chain parameters, 15 enumerated finite lattice systems,
65,536 exponent-frontier subsets and 64 exponent-cover parameters. They
verify the encoded finite algebra and combinatorics. They do not replace
the written universal arguments or certify the original open problem.

Source PDFs, screenshots, raw catalogue/research corpora and private
retrieval receipts are excluded. No contact with outside researchers,
GitHub release, Zenodo deposition or claim of peer review is part of this
package.
