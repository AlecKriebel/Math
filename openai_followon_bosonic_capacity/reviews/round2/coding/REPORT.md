# Independent adversarial audit: finite generated-secret coding

Date (UTC): 2026-10-07T04:35:15.563012+00:00

This is a narrow, fresh audit for the second complete-package reviewer. I read the current manuscript and direct coding supplement themselves, without reading prior favorable review reports. No source edits, external communications, publication operations, or Git operations were performed. The audit below is mathematical checking, not formal machine verification.

## Exact reviewed versions

- `manuscript/main.tex`: SHA-256 `eda0b20fb843fda3b7b70203b63628e36ebf5d4a1b6c817624d3a5810f9beaab`
- `notes/coding_repair/DIRECT_CODING.md`: SHA-256 `48f64a4071ccb6d93e5ddda2b69c8d10354c3c50601fe2929aefc2df2ed15adf`

## Verdict and scope

No substantive error was found in the finite-cq generated-message achievability proof, its soft-covering estimate, sequential decoder, bounded-average-cost selection, and expurgation. The cone and generated-secret resource conversions are correct under the expressly stated finite-gross net-resource convention. The finite proof does not establish the stronger literal consumed-key secrecy criterion; it correctly disclaims that criterion. This audit does not certify the upstream EPnI or quantum-father theorem, priority, PDF packaging, remote publication, or the full private converse; those are outside this delegated check.

## Checks actually performed

1. **Conditional spectral projectors.** For each fixed finite ensemble, positive eigenvalues have bounded surprisal. Grouping positions by x or (x,y), the law of large numbers gives the displayed rank, restricted eigenvalue and retained-mass properties. Uniformity over sufficiently narrowly typical x-sequences follows from positive type frequencies bounded below. Zero-probability letters and zero spectral eigenvalues are correctly excluded. The projectors Q commute with the sampled conditional state; P need not commute with Q.

2. **Packing algebra.** For Gamma_t=P Q_t P and distinct sampled t,l, conditional independence gives E Tr(Gamma_t sigma_l)=E Tr(Q_t P sigma_x P). Its bound is the P-restricted operator norm times rank Q_t, exactly 2^{-n(b-2 delta)}. Own-word acceptance follows by applying gentleness to P, comparing with Q_l acceptance, then Jensen. Hayashi–Nagaoka applied to each deterministic realization gives the stated average error. The same independence argument gives the public HSW random-code expectation; it does not presuppose existence of a different public code.

3. **Noncommuting soft covering.** With tau=P Q sigma Q P, positivity and Q sigma Q <= A Q imply tau <= A P and Tr tau <=1. The two truncation errors obey

   ||sigma-P Q sigma Q P||_1 <= ||sigma-P sigma P||_1 + ||P(sigma-Q sigma Q)P||_1,

   hence the stated average bound 4 sqrt(epsilon). For independent centered Hermitian random matrices, the cross terms of E Tr[(K^{-1}sum tau-bar tau)^2] vanish by independence and entrywise expectation even when the matrices do not commute. Tr tau^2<=A Tr tau<=A gives A/K. The rank-D trace/Hilbert–Schmidt inequality then gives sqrt(DA/K), with exponent c=H(E|X)-H(E|XY). Comparing each sampled state and the mean with their truncated versions gives the stated 8 sqrt(epsilon) remainder. No operator Chernoff theorem or exponentially large union bound is needed for uniform-message average trace secrecy.

4. **Public/private decoding composition.** The public POVM depends only on cloud centers. Averaging satellites therefore produces precisely the ensemble on which the outer packing error was estimated. The private decoder may depend on the selected key and codebook; no false independence of these decoders is required. Gentleness applies pointwise to the subnormalized correct-public branch. Comparing its acceptance with the private decoder on the original state gives w_n+2 sqrt(v_n) after averaging, including the outer failure probability.

5. **Secrecy target.** For each (j,m), key averaging gives zeta_jm. The block-diagonal trace norm is exactly the displayed average distance to the code-dependent target sigma_x(j). This yields secrecy with an arbitrary legitimate J-E target. If the manuscript's criterion uses the actual J-E marginal, trace contraction plus triangle inequality changes the bound by at most a factor two, which still vanishes. Neither derivation reveals or jointly protects the consumed key. The public codebook and actual public label can be disclosed to Eve.

6. **Code selection and energy.** Before conditioning on a good code, all symbols are drawn i.i.d. by position with a shared center per position. Thus the entire codebook-letter collection at position i is independent of the collection at a different position. Its averaged cost V_i is bounded in [0,H] and has the correct mean. Scalar Hoeffding is therefore valid even when message cardinalities are one. The high-probability low-cost event intersects the Markov high-probability low-error/low-leakage event. This proof estimates the bounded cutoff observable, not an unbounded number operator by trace norm. At zero ensemble cost, nonnegativity forces all sampled letter costs to vanish.

7. **Expurgation.** Removing public rows with row mean greater than F^{1/2}, then private entries with conditional defect greater than F^{1/4}, retains respectively fractions at least 1-F^{1/2} and 1-F^{1/4}. Equalizing private sizes by further deletions preserves those lower bounds. The remaining decoder can keep discarded outcomes as failure; pointwise correct acceptance is unchanged. The key remains uniformly averaged. Nonnegative average costs grow by at most the reciprocal retained fraction, covered by the original strict cost slack. Expurgation does not secretly impose joint consumed-key secrecy.

8. **Pure-loss support.** A photon-number cutoff input is supported on levels 0 through K. The beam-splitter isometry maps each input level q to pairs (q-j,j), so both B and E remain within the same finite support. The finite-dimensional coding lemma thus applies to the bosonic cutoff without an unsupported infinite-output concentration step. A general finite-input channel with infinite outputs would require a separate approximation, correctly disclaimed in the supplement.

9. **Rate cone.** For corner (a,b,-c) and conversion vectors v_1=(1,-1,0), v_2=(0,-1,1), v_3=(-1,1,-1), the unique coefficients are

   x_1=b-c-(P+S), x_2=a+b-(R+P), x_3=a+b-c-(R+P+S).

   They are nonnegative exactly when the three asserted inequalities hold. This establishes the algebraic region. Negative net rates can require finite gross streams or seeds; their allowed cancellation is an explicit operational convention, not proved by the algebra alone.

10. **Generated-key/OTP composition.** The joint generated-secret promise protects all generated private/key registers together, with a uniform product ideal independent of Eve and public data. Revealing one private subset to use it as public communication leaves the remaining subsets decoupled in that ideal. Relabeling a uniform transmitted private subset as shared key is legitimate by correctness. A new independent uniform message T encrypted with a joint-decoupled generated key S gives L=T xor S; tracing the consumed S leaves T and every other surviving generated-secret subset uniformly decoupled from L and Eve. This can be checked exactly on the ideal product state, then transferred to the approximate state by trace contraction. Every consumed-key register must be discarded from the final protection target, as the manuscript states. Returning a used OTP key together with its plaintext would fail and is not asserted. Fixed finite sequential compositions add their errors. If a resource cycle is used, its required seed and a final unused regenerated resource must be accounted as the stated finite gross input/output; unlimited or uncharged superlinear catalysts are not justified.

## Boundary and limitation checks

- At a=0 or b=0, one public cloud or one private message removes the corresponding strict-rate requirement without affecting the other bounds.
- At c=0, arbitrarily small key rates and closure suffice; finite-ensemble zero conditional Holevo information in fact makes the relevant Eve states identical on the support.
- Average cost is over public/private messages and consumed key. No peak cost for each key or codeword follows, and none is claimed.
- The theorem's uniform generated-message promise is not silently strengthened to secrecy jointly with consumed key, security after key revelation, or a full arbitrary correlated-input channel simulation.
- The manuscript's compact description of pasting scalar inner codes is compatible with the supplement's equivalent conditional-table proof. The latter alone provides a checkable finite-alphabet construction.

## Nonblocking presentation observation

The supplement writes its trace-secrecy target using a code-dependent ideal J-E marginal, whereas main.tex uses the actual J-E marginal. A one-line triangle/contraction argument supplies the factor-two conversion noted in check 5. This is not a mathematical gap because both errors vanish; no package amendment is required for validity.
