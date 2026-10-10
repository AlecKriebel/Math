# Exact minor correction to the preserved author freeze

Severity: minor proof wording. Proposition 3 is true with its existing hypotheses; no change of result or mathematical disposition is required.

Target: `PROOF.md`, Section 4, Proposition 3 proof, the covering paragraph. Apply these three local wording edits together.

First old clause:

    cover A by sets U_i of positive diameter d_i<1/(2j), with Σ_i d_i^κ arbitrarily small.

Replace with:

    cover A by sets U_i of diameters 0≤d_i<1/(2j), with Σ_i d_i^κ arbitrarily small.

Second old clause:

    For each U_i meeting A∩E_j choose x_i in that intersection.

Replace with:

    For each positive-diameter U_i meeting A∩E_j choose x_i in that intersection.

Third old sentence:

    Singleton members can be replaced by arbitrarily small positive-diameter balls; the growth estimate rules out atoms on E_j.

Replace with:

    Any zero-diameter cover member meeting A∩E_j is a singleton {x} with x∈E_j, and ν({x})≤j r^κ for every 0<r<1/j, so ν({x})=0. There are at most countably many such members. Discard their zero-mass contribution and apply the preceding estimate to the positive-diameter members.

Reason: isolated points in a general metric space need not admit arbitrarily small positive-diameter balls. The atom estimate already available supplies the complete repair. No measurability of E_j is needed, since the argument uses outer measure.

The old sentence is preserved in `author_freeze/PROOF.md` so the original review binding remains exact. This correction has been audited as written; it has not been applied to the frozen manuscript.

Optional explanatory refinement, not an error: the cited 2010 paper sets up automorphisms. Proposition 1's explicit isometry proof establishes the noninvertible version independently. If revising the literature paragraph, making that attribution boundary explicit would help readers.
