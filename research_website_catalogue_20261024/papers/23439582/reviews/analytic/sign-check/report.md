# Closed independent bounded algebra lane

Closed 2026-11-15 04:42:16 UTC. Completion estimate for this bounded lane: 100%.

The exact checker passed **131,095 equality comparisons** across F2, F3 and
F5, including nine comparisons with the predicted negative-control residuals.
The run was 2026-11-15 04:42:07.541483–04:42:08.632399 UTC (1.090711 seconds).
There were no failures of the unmutated formulas.

| Field | Equality comparisons | Status |
|---|---:|---|
| F2 | 44,339 | PASS |
| F3 | 43,378 | PASS |
| F5 | 43,378 | PASS |

The model is the infinite free associative graded Hopf algebra k<e,o>, with e
even and o odd, as derived in `reconstruction.md`. Words and all intermediate
products retain their full lengths. Unary tests use every word of length <=6
(127 H words, 254 B basis elements); binary tests use every separate input
of length <=4 (31 H words or 62 B elements each); associativity uses every
separate B input of length <=3 (30 elements each, 27,000 triples per field).
Actual binary outputs reached word length 8 and triple outputs length 9.

Per field the B checks comprise 3,844 coproduct multiplicativity identities,
27,000 associativity identities, 254 coassociativity identities, 254 left and
254 right counit identities, 254 left and 254 right antipode identities,
3,844 counit multiplicativity identities, 3,844 antipode antimultiplicativity
identities, and 254 unit identities on each side. The H implementation is
also checked for graded coproduct multiplicativity, coassociativity, counits,
antipodes and graded antipode antimultiplicativity. In F2 an additional 961
identities confirm ordinary coproduct multiplicativity after forgetting the
grading, as used in the primary's characteristic-two branch.

A second internal construction expands Delta from the three generator
equations and S by reversing generator products. Each is compared with the
closed formula on all 254 B inputs per field. This algorithm avoids the
unshuffle sign count and the closed antipode exponent respectively, while
sharing B multiplication. It is additional implementation evidence within
the same mathematical model, rather than wholly separate software or model
verification.

The negative control omits |v| from the left group exponent of Delta_B. On
x=o#1 the multiplicativity residual, left minus right, is

    -2 (o#1) tensor (o#1).

It has coefficient 1 in F3 and 3 in F5, so both odd-characteristic tests fail
as intended. It vanishes in F2, exactly as predicted before execution. With
the original antipode retained, both mutated antipode convolutions on x
instead give the nonzero residual

    (o#1) + (o#g)

in all three fields. The F2 behavior therefore records both the collapse of
odd signs and a separate structural failure of the mutated formula.

## Independence, reproduction and exact gap

Read exposure: root `/Users/alec/Documents/Math/AGENTS.md` and only the
permitted primary `source-resume-20261115/published-source/main.tex`, using
its algebra section at lines 44–95 and a text locator search. No native
verification source was read, before or after implementation. No earlier or
current review, triage, result, or opinion files were read. The parent later
reported its own native-code reading, but communicated no native mechanisms
or results to this lane. No external human contact, Git operation, source
mutation, source build, or wider programme campaign occurred.

Reproduce in this directory with Python 3 (standard library only):

    python3 check_bosonization.py > rerun-results.json

Execution timestamps and elapsed time will differ. All mathematical results
and counts should agree. The checked source file and all completed artifacts
are hashed in `manifest.json`, sealed by `SEAL.sha256`.

The strongest verified result is that these finite exact comparisons support
the displayed parity-bosonization conventions on a noncommutative infinite
free-word model with a nonzero odd square. They do not prove the infinite
Hopf-algebra ideal theorem, universality for every graded Hopf algebra, any
topological import, or the paper's main theorem. The requested bounded lane
has no outstanding task; those larger claims remain outside its scope.
