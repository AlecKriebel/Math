# Exact scope and success test

## Identification and verified primary statement

The public descriptor catalog associates numeric ID 30002507 with OWR-12866-017, the title *A Dirichlet Series with Exactly One Zero*, and DOI https://doi.org/10.4171/OWR/2014/06. The associated primary source is *Dirichlet Series and Function Theory in Polydiscs*, Oberwolfach Report 06/2014, printed page 390, section 8, Michel Balazard's first question. The downloaded publisher PDF has 60 physical pages; physical page 56 was rendered and visually inspected.

In mathematical form, the source asks whether there exist complex coefficients (a_n), a real alpha, and rho with Re(rho)>alpha such that the ordinary series

f(s)=sum_{n=1}^infinity a_n n^{-s}

converges for every s in H_alpha={Re(s)>alpha}, and its zero set within H_alpha is exactly {rho}.

This is a paraphrase and mathematical formalization, not an imported source-text reproduction. The source does not prescribe multiplicity. A simple-zero example would satisfy both the distinct-point and multiplicity-one readings; the retained conditional constructions explicitly check simplicity. The identically zero function and zero-free monomials do not satisfy the target.

## Hypotheses that may not be added or replaced

- The bases are positive rational integers n. A general series sum a_k x_k^{-s} with arbitrary real x_k tending to infinity is a different class.
- Actual convergence of the displayed ordinary series is required in the half-plane containing the zero. Meromorphic or holomorphic continuation into that half-plane is not enough.
- The source says some open half-plane. It does not require uniqueness in the maximal convergence half-plane, which is a stronger variant used in later papers.
- A zero on the convergence boundary alone does not count. The open half-plane must contain the zero.
- There is no stated sign, reality, boundedness, integrality, multiplicativity, or nonzero-everywhere restriction on the coefficients.
- Entire continuation, finite order, exponential type, global boundedness, and uniform convergence on the whole half-plane are not source hypotheses.
- The zero need not be real unless a separately chosen real-coefficient construction and conjugation symmetry force it.
- A finite-height zero count or a compact-exhaustion argument with a different function at each stage is not a single all-height construction.

## Required completion artifact

A positive solution must specify or prove existence of one ordinary coefficient sequence, an open right half-plane, convergence of that sequence there, and the exact nonempty singleton zero set there. A negative solution must rule out every coefficient sequence allowed by the source, including conditionally convergent series and arbitrary growth. Neither artifact has been obtained.

## Access and provenance limits

The exact https://www.unsolvedmath.com/problems/30002507 route failed through web retrieval and returned HTTP403 through a direct read. No access-control bypass was attempted. The descriptor catalog, not the inaccessible live page, supplies the title/ID/DOI linkage. The complete upstream raw statement and prior AI report were unavailable and uninspected; the descriptor's hashes are identity metadata, not evidence that those missing bytes were read.

Repository observations found no earlier target-specific attempt in the inspected PR/branch searches, main attempt listing, main history, and path-filtered commit history. These are bounded observations, not a proof that no deleted, renamed, inaccessible, or unindexed work exists. The main queue's queued 0/5 entry alone was not treated as absence evidence.
