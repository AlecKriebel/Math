# Mixed odd SOS powers and the Motzkin threshold limit

Problem 30005461 / OWR-12697710-007. **Full two-clause target accepted.**

1. For arbitrary real polynomials p,q and nonnegative integers i,j, if p^(2i+1) and q^(2j+1) are sums of squares, then (p+q)^(2i+2j+1) is a sum of squares. This is the previously published Blekherman–Kozhasov–Reznick theorem, with the truncated-binomial ingredient credited to Iosif Pinelis. The complete credited proof and both display corrections are included.
2. For f_c(x,y)=x^4*y^2+x^2*y^4+1-c*x^2*y^2, every fixed real c<3 has all sufficiently large odd powers SOS. Consequently the thresholds defined by {c: f_c^(2k+1) is SOS}=(-infinity,c_k] satisfy **lim c_k=3**.

## Main mechanism

On the integral singular cubic surface ABC=D³, q_c=A²+B²+C²−cD² is strictly positive at every real projective point when c<3. Scheiderer's published Corollary 4.2 gives an odd SOS power of this section. Projective-space cohomology lifts its square roots to homogeneous polynomials. Substituting (A,B,C,D)=(x²y,xy²,z³,xyz) gives the exact homogeneous Motzkin power, and z=1 gives the target affine family. The limit follows from eventual admissibility of every c<3 and f_c(1,1)=3−c.

There is no essential preprint dependency. The optional appendix separately verifies real delta(M_c)=6 for 0<c<3 using the definition in *Stubborn Polynomials*. Its conclusion and source status are kept separate from the principal proof.

## Contents

- [PROOF.md](PROOF.md): full principal limit proof
- [CREDITED_MIXED_EXPONENT_PROOF.md](CREDITED_MIXED_EXPONENT_PROOF.md): complete credited first-clause proof, both source corrections, homogenization and edge cases
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): full substantive independent acceptance and reconstruction
- [REAL_DELTA_APPENDIX.md](REAL_DELTA_APPENDIX.md): unchanged optional direct local calculation
- [ACCEPTANCE.json](ACCEPTANCE.json): exact distributed proof/audit/appendix identities and scope
- [STATUS.json](STATUS.json): accepted full resolution, credit and limits
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): source roles, corrections and inspection limits
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source/PDF identities and historical verification metadata
- [MANIFEST.json](MANIFEST.json): exact ten-file inventory, hashing the other nine members

## Credit and limits

The first clause is [Blekherman–Kozhasov–Reznick, Theorem 5.3](https://doi.org/10.1017/fms.2026.10221), with Pinelis's ingredient. The threshold derivation imports [Scheiderer, Corollary 4.2](https://doi.org/10.1007/s00229-011-0484-3) and [Stacks Project, Lemma 30.8.1](https://stacks.math.columbia.edu/tag/01XS). No historical novelty or priority is claimed. No explicit exponent, square-root certificate, convergence rate, uniform exponent for all c<3 or affirmative SOS conclusion at c=3 is supplied.

The independent mathematical audit requires no material correction and leaves no unresolved residual in the two stated clauses. This AI-assisted manuscript and audit are unrefereed. Acceptance does not mean external human peer review, journal acceptance or formal proof-assistant certification.

The full mathematics and substantive audit findings are preserved. Programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination are excluded. Historical checks are supplementary; no omitted software is needed for the written proofs. Edition preparation rechecked frozen byte identities and publication integrity without new scholarly retrieval, source-text inspection, literature search or mathematical-computation reruns. QUEUE.md and unrelated repository content are unchanged. No merge, release, DOI, journal submission or outreach is implied.
