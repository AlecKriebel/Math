# Independent adversarial audit of the rank-five character certificate

**Verdict: PASS for the explicit finite-subgroup claims.** Review completed
2026-10-24 21:55 UTC; completion estimate is **100% of this limited review**,
not of the Hydra virtual-specialness problem. No mathematical objection to the
index-1024 construction or the subsequently requested index-512 improvement
was found. Neither result resolves virtual specialness or virtual RFRS.

## Inputs and independence

The original review input is `FINITE_COVER_HOMOLOGY.md` together with the
15-file package listed by `FROZEN_INPUTS.json`. Every frozen file has its
advertised byte count and SHA-256 hash. The manifest itself has SHA-256
`8af60a6b0c4f99952ed1cd52728e3e477ec1bd1392541766aaf1e806f4f74e7d`.

At the parent researcher's subsequent request, this review also checked
`INDEX512_DELTA.md` and `rank5_cocycle_certificate_index512.json`. These are
explicitly a separate delta, not part of the original frozen manifest. Their
SHA-256 hashes are respectively
`ee08e29df2c0bfb0652cfccd0b909cfd216b9e0c62bc049e97a48fcdb46cdb76` and
`f76017a86b8255f64fc7d521651c088685b860bc369090efbc79419dbc5284fc`.

The new verifier `independent_cocycle_audit.py` neither imports nor runs any
author program. I did not read the author verifier before implementing the
independent check. Its graph is constructed directly from the six epsilon
entries in the prose, and its target words are generated independently from
the declared generators and left-associated commutators. Signed paths use
explicit inverse permutations and subtract the weight of the traversed
positive edge. The substitution is exactly
`theta(a1)=a1`, `theta(ai)=ai*a(i-1)`, with inverse letters mapped by inverse
words; this matches `t^-1*ai*t=theta(ai)`.

## Exact computational checks

| Check | Frozen r=16 | Delta r=8 |
|---|---:|---:|
| Connected fiber-cover vertices | 64 | 64 |
| Transitive full Hydra action points | 1024 | 512 |
| Defining-relator action checks | 5120 | 2560 |
| Integral cochains | 9 | 9 |
| Edge-cell identities | 2880 | 2880 |
| Actual signed target-lift evaluations | 19 | 19 |
| Distinct target words | 18 | 18 |
| Character value on a1 squared | 1 | 1 |

Each recorded generator permutation is bijective and equals the compact
epsilon specification. The independently generated theta^16 positive word
lengths are 1,17,137,697,2517. Direct traversal of every image edge at each
of the 64 vertices verifies that both theta^8 and theta^16 lift with vertex map
equal to the identity.

As a separate check on index and conjugation convention, I constructed a right
permutation action on `(q,v)` with `q` modulo r and v one of the 64 graph
vertices. Generator ai acts on v by the word theta^q(ai); t sends q to q-1.
For every point and each i the action satisfies `t^-1*ai*t=ai*a(i-1)` (or ai
for i=1). Each action is transitive. This check uses all original Hydra
relations, rather than a homology rank calculation.

All nine cochains and all vertex potentials are integers. For every positive
edge v--ai-->w the verifier checks

    integral(theta^r(edge)) - integral(edge) = beta(w) - beta(v).

It also verifies each target's exact first closing power and its stated
nonzero evaluation, and separately evaluates the entire theta^r-substituted
target loop. The standard-generator closing powers are 2,4,2,2,2. All ten
elementary commutators and all four recorded left-associated commutators close
without taking a further power. The first nested commutator duplicates
`[a1,a2]`; hence 19 entries represent 18 distinct target words, exactly as
claimed. In particular the construction detects a2 to the fourth power, not
an asserted closed a2 squared.

Eight synthetic corruptions were each rejected: a changed graph permutation,
a changed edge weight, a changed vertex potential, a changed signed target
word, a changed closing power, an incorrect evaluation, an incorrect character
assignment, and a nonintegral edge weight. Original inputs were never mutated.
Their rejection reasons are recorded in `adversarial_mutation_receipt.json`.

## Why the finite checks prove the stated group claim

The connected 64-sheeted rose cover defines a subgroup L of index 64 in F5.
The verified image-edge endpoint condition supplies a based lift of theta^r
with all vertices fixed. Thus theta^r(L) is contained in L. Since theta is an
automorphism and both subgroups have index 64, the containment is equality.
Consequently `K_r=<L,t^r>` is the stated semidirect product and has index 64r.

An integral graph cochain evaluates additively on based loops; cancellation of
an edge with its reverse contributes zero. It therefore defines a homomorphism
phi:L->Z. On a loop, the verified differences of vertex potentials telescope
to zero. Hence phi(theta^r(l))=phi(l), and phi extends to K_r by assigning
t^r the value zero. This respects the displayed stable-letter conjugation
relation; no invariance under theta itself is required.

The character indexed 63 evaluates the actual closed lift a1^2 to1. Therefore
the extension is surjective and `x |-> (a1^2)^(lambda(x))` is a retraction onto
the infinite cyclic subgroup generated by a1^2. The same argument for each
nonzero recorded target evaluation proves rational-homology visibility of
that target's recorded power. One such finite-index subgroup and nonzero
evaluation suffice to refute persistent rational-homology invisibility for
each of these candidates.

## Smaller powers and a potential logical trap

Failure to lift theta^k with the identity vertex map would by itself **not**
exclude a lift permuting vertices while fixing the basepoint. I checked the
unique possible rooted lift determined by images of spanning-tree paths.
Actual based-subgroup invariance fails for k=1,2,4. Explicit witnesses, using
vertex encoding v+32s and basepoint 0, are:

| Exponent k | Word closed in L | Endpoint of its theta^k image |
|---:|---|---:|
| 1 | a4^2 | 32 |
| 2 | a4^2 | 32 |
| 4 | a4*a5^2*a4^-1 | 32 |

For k=8 and 16 the rooted lift exists and is the identity. These explicit
closed-loop witnesses independently justify the delta's lower-power
statement. They establish no minimal-index claim for other finite covers.

## Precise objections and boundaries

There are **no blocking mathematical objections** to either audited
construction. The originally frozen index 1024 claim remains correct; the
separate index 512 delta is stronger. The delta should remain identified as a
separate input unless the package is deliberately refrozen.

The word commutator convention here is `xyx^-1y^-1`, which the certificate
explicitly encodes. The inference to a retraction uses the value 1 on a1^2;
nonzero values on the other targets prove visibility, not automatically
retractions onto those exact cyclic subgroups. The prose currently makes
this distinction correctly.

The RFRS implication in the document is sound: a nontrivial element of an
RFRS group eventually exits its residual chain, and its rational homology
class in the preceding term cannot vanish. Passing first to a nonzero power
handles the virtually RFRS case. Detecting a finite list of words in one cover
does not supply such a residual chain or settle all cyclic subgroups. The
document's central conclusion respects that boundary.

This review does not independently certify the auxiliary matrix ranks in the
characteristic-cover tables, the random-search provenance, or the literature
and priority assertions. Their hashes were checked, but the central result
needs none of them. No input from the separate rank-six auxiliary search was
used. No external communication or publication was performed, and all review
artifacts were written inside `homology/review/`.

## Reproduction

From the homology directory:

    python3 review/independent_cocycle_audit.py --output review/independent_cocycle_receipt.json
    python3 review/independent_cocycle_audit.py --certificate rank5_cocycle_certificate_index512.json --output review/independent_cocycle_receipt_index512.json
    python3 review/adversarial_mutation_checks.py

The timestamped JSON receipts record the input and verifier hashes, exact
counts, lower-power witnesses, and every target evaluation.
