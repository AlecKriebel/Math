# Scope clarification after independent audit

Date: 2026-10-05 UTC. Target: 2306086 / Function Theory 6.86.

## Controlling disposition

The independent audit found no blocking defect in the qualitative fixed-point theorem. The current publication disposition is `claimed_solved`, `5/5`, **only for the literal qualitative improvement question**: for each fixed nonreal z there is a strictly smaller centered disk radius that works uniformly for every normalized real-coefficient univalent function. The classical radius is sharp at nonzero real z. The displayed expression at z=0 is identically zero.

The primary wording does not explicitly demand a sharp or numerical formula. Therefore the earlier statement that the overall target is left unresolved must not be read as denying the proved qualitative theorem. The historical labels in `author/README.md`, `author/LIMITATIONS.md`, `author/PROOF_PARTIALS.md`, `author/APPROACH_LOG.md` and `author/FROZEN_MANIFEST.json` remain unchanged as an audit trail. This note and the full independent audit supersede their pending-audit/scope-review labels. The quantitative meaning of “partial” remains correct.

An explicit positive gap, the best radius M(z), extremizers at general nonreal points, and the full variability region remain undetermined. Novelty and present literature status have not been established. No claim is made that all quantitative questions are solved or that the qualitative proof is new. Numerical Loewner values are non-certified evidence, not interval-certified strict lower bounds or a global extremal theorem.

## Two presentation corrections

1. In the conformal comparison in Section 3 of the frozen proof, “quotient” means **inverse composition**, not pointwise division. If g and f map the disk conformally onto the same slit complement, g^{-1} composed with f is a disk automorphism fixing zero. For g=4|c|k_+ or 4|c|k_-, its derivative at zero is 1/(4|c|), whose modulus must be 1. Hence |c|=1/4, and normalization identifies f with the appropriate real Koebe map.
2. For the vanishing-gap obstruction in Section 4, use **delta(z)=|Im z|/|1-z^2| tending to zero**, for example along a sequence approaching an interior point of the real diameter. Euclidean imaginary part tending to zero near the boundary endpoints +1 or -1 does not alone imply delta tends to zero. There is also a separate obstruction as delta tends to 1/2, for example z=i t with t tending to 1.

These clarify wording and scope; they introduce no new proof-search turn or change to the frozen theorem. The exact lower bounds and numerical limitations remain as audited.
