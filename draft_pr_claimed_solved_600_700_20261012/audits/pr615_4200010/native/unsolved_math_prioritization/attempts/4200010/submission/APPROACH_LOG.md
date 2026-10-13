# Substantive approach log

The five-approach budget is an upper limit. A complete candidate was obtained on the second distinct approach; no artificial extra proof searches were added after completion. Verification afterward checks the frozen candidate and is not further open-ended search.

## Approach 1: weakly-mixing disk-map suspension

Time: 2026-10-04 15:26-15:28 UTC. Completion estimate at checkpoint: 55%.

Mechanism: start with a classical smooth area-preserving weakly-mixing zero-entropy disk map and realize it by a periodic Hamiltonian. The extended autonomous Hamiltonian `p+K(t,x)` would yield a positive-volume energy band. The literature search found primary-author descriptions of the relevant disk-map constructions. Zero entropy alone must not be confused with a proof of zero exponents without the surface/Pesin argument or a derivative-rigidity hypothesis.

Outcome: promising but unused. Rather than import this existence theorem and its boundary, isotopy, exponent, and compactification details, move to an explicit skew-shift model. No claim based on this route is part of the final theorem.

## Approach 2: explicit skew shift and compact symplectic mapping torus

Time: 2026-10-04 15:27-15:33 UTC. Completion estimate at checkpoint: 100% of the candidate proof, with independent audit and priority review outstanding.

Mechanism: `F(x,y)=(x+sqrt(2),y+x)` has an elementary Fourier ergodicity proof, an orthogonal orbit that prevents almost periodicity, and a unipotent derivative. Its mapping torus crossed with a circle has symplectic form `beta+tau wedge dE`. A genuine periodic real Hamiltonian equals the local coordinate on an energy interval.

Outcome: `FULL_PROOF.md` gives a complete compact autonomous construction with volume-1/4 invariant band, zero exponents in every phase-space direction, and no positive-volume almost-periodic invariant subregion. The proof explicitly includes measurable invariant subsets, not only the full band. Exact finite algebra and failure controls passed.

## Validation focus and rejected shortcuts

An isolated horocycle-type energy surface would not by itself establish positive full phase volume. The original skew shift need not be Hamiltonian on its own torus; the four-dimensional suspended flow is Hamiltonian by direct contraction. A global formula `H=E` on a circle would be invalid; the cutoff fixes it. Ergodicity alone would not exclude almost periodicity; the orthogonal orbit does. Clock eigenfunctions do not imply that the full system is almost periodic. No novel-research or prior-resolution certificate is inferred from the construction.
