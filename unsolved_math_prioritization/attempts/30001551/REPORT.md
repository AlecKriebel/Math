# Independent word equations: one bounded research attempt

**Target:** problem 30001551 / OWR-4425-006.

**Outcome:** unresolved. No independent triple with a common nonperiodic solution was constructed, and no complete nonexistence proof was obtained. The output is an attributed erasing-witness reduction and a reproducible finite search. It is not an improvement of the known upper bound and is not claimed to be new literature.

## Exact question

Does there exist a system of exactly three independent, constant-free equations on `X,Y,Z`, with nonempty variable words on both sides, interpreted over a finite-alphabet free monoid, that has one common nonperiodic solution? Images may be empty. Deleting each equation must enlarge the complete solution set. Individual nonperiodic solutions of separate equations do not suffice.

## What was established

The accompanying `PROOF.md` gives a complete elementary proof of the following restricted statement, with prior ingredients identified:

- A hypothetical target triple has at most one equation admitting an erasing deletion witness.
- If it has a common erasing nonperiodic solution, all deletion witnesses are nonerasing.
- More generally, a balanced system with a common nonperiodic solution and a member equivalent to pairwise commutation has an equivalent subsystem of at most two members.

The key two-erasure argument is already present in Holub–Žemlička (2015), Lemmas 15–16. Finding this prior result prevented an unsupported novelty claim. The reduction is useful for certificate design but leaves the core difficult cases open.

## Bounded constructive search

The erasing-common-solution branch was tested. Up to renaming variables, any equation solved by a nonperiodic morphism erasing `Z` has identical left and right words after deletion of `Z`. Therefore `[a,b,epsilon]` is a valid common nonperiodic solution for the entire searched equation family.

Two explicitly bounded searches were completed:

1. All 157,800 unordered distinct equation pairs `U,V` with `1 <= |U|=|V| <= 8` and `pi_Z(U)=pi_Z(V)`; deletion witnesses drawn from the 216 nonerasing morphisms whose three images are binary words of lengths 1–2. The equations induce five distinct solution subsets on this finite pool. All 10 triples of distinct subsets fail the three-witness independence condition.
2. All 28,216 such equations with side length at most 7; deletion witnesses drawn from the 2,744 nonerasing morphisms whose images are binary words of lengths 1–3. They induce 15 distinct solution subsets. All 455 triples of distinct subsets fail the condition.

Repeated solution subsets cannot participate in an independent triple on the pool. Thus checking triples of distinct subsets is sufficient for the stated finite claim. The independence test requires, for solution subsets `A,B,C`, that each of `(B intersect C) minus A`, `(A intersect C) minus B`, and `(A intersect B) minus C` be nonempty.

An independently written verifier uses a different equation generator (binary skeletons with compositions of inserted `Z` letters), exact base-3 integer evaluation in place of string substitution, and set differences in place of the searcher's bit operations. It rechecks counts, every signature, and every triple of distinct signatures. No randomized or floating-point equality is used.

These computations do **not** rule out an independent triple of the searched equation lengths with longer or nonbinary witnesses. They do not rule out longer equations, or systems whose common nonperiodic solutions are all nonerasing. The search bounds are computational restrictions, not universal bounds.

## Source and interpretation checks

The exact original contribution and both complete prior author manuscripts were read: Nowotka–Saarela (2022) and Saarela (2024). A further primary source, Holub–Žemlička (2015), was retrieved and its erasing-solution and balanced-system results inspected.

The 2022 upper bound is 17 under the common-nonperiodic-solution condition, while 18 concerns systems without that requirement. Its conclusion leaves the sharp nonperiodic bound between 2 and 17. The 2024 classification concerns entire systems and unbalanced equations. It does not assert redundancy of arbitrary balanced finite subsystems. A bounded literature search on 10 October 2026 located no later resolution; this is not an exhaustive absence claim.

The following plausible shortcuts remain invalid:

- Requiring witnesses to be nonerasing before proving a reduction that permits that restriction
- Treating pairwise independence as three-equation independence
- Giving a separate nonperiodic solution for each equation in place of a common one
- Substituting free-semigroup conventions for the stated free-monoid problem
- Treating a finite failed search as universal nonexistence
- Treating a one-equation presentation of an entire system as a statement about all its finite subsystems

## Stopping point

The obstruction obtained here is a restricted structural result. The finite searches provide no witness. Further progress would require a method controlling nonerasing deletion witnesses beyond these finite pools, or an explicit independently verifiable triple. The exact target remains unresolved by this attempt.
