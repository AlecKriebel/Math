# Follow-up gate: concrete prior classification and N13 numerical closure

**PASS.** Root's `FINAL_PRIORITY_DISPOSITION.md`, recorded 2026-10-12T21:29:46Z, supports `already_solved` for the literal original target through a checked application of Frank-Manibo's prior results. The independently reviewed N13 certificate closes this review's target-relevant strict-numerical gap. Current mathematical classification blockers: 0; required repairs: 0; unresolved mathematical gaps for this classification: 0. The separate queue transaction remains pending its own operational review.

The earlier review is preserved. Its REPORT/RESULT correctly recorded one local uncertified-integral gap at that historical checkpoint. All nine files in its positive hash manifest remain byte for byte unchanged. This follow-up supersedes that gap for the final classification; it does not edit the old record or pretend that the original midpoint replay was certified.

## Concrete evidence inspected

I read the complete root disposition; numerical producer REPORT, RESULT, SEAL, certificate JSON, and all 391 lines of the controlling code; fresh numerical adversary REPORT/RESULT, analytic obligations, independent Gram implementation/raw results, and execution summary; root replay records; and the parent custody inventory. The controlling hash is

    027dc38ea76f1a4e69d8976a4845caefc4429e48b551afa7c327dc243b3dac20.

It matches the producer's pre-peer seal, the fresh numerical adversary's result, and the actual controlling file. All 24 positive entries in the parent-produced adversary custody inventory match actual byte sizes and SHA-256 hashes. This is a parent-produced inventory and is not represented here as an independently generated final reviewer seal. The initial numerical adversary's source checkpoint and its independent Gram mechanism provide distinct independence evidence.

My newly captured direct execution runs only the controlling certificate, with N=13, M=65536, precision 100 bits, from `/tmp`. It does not invoke an old runner or overwrite peer raw records. It exited 0 and matched every stable field in the producer's saved N13 certificate. The command, actual start/end times, stdout, stderr, exit status, and exact code hash are in `FOLLOWUP_CHECKS.json`. This execution corroborates the read analytic mechanism; success printing alone is not the mathematical premise.

## Why the certificate closes exactly the needed gap

The code reconstructs the source-forward product B(x)B(2x)...B(2^12 x) using exact Gaussian polynomial coefficients. The modular convolution has sufficient zero padding and a unique signed lift under the checked modulus/root assumptions. The numerical adversary independently checked all 16,383 Fourier coefficients through the exact Gram recurrence, rather than accepting agreement at sampled points. Its common coefficient digest is

    3d3550f4233ca4f00b26cb86befd13f54aeff043e46b099fff5bad3a47bbb5f4.

For torus cells centered at j/M, the exact average of the positive squared Frobenius norm is the Fourier sum with sinc(pi k/M) multipliers. The determinant supplies positivity. The interval sinc inputs, certified positive-sign roots, and upward propagated FFT error enclose these means. Concavity of log then bounds the true integral by the average of logarithms of cell means. The outward logarithm arithmetic uses those mean upper endpoints. It does not mistake point sampling or apparent grid convergence for a quadrature enclosure. I checked the error recurrence includes both input errors, twiddle error and its interaction with input error, and multiplication rounding, and that the exact partial-transform amplitude is bounded by the coefficient L1 norm.

The logarithm normalization keeps its argument at least 1 and its exponent nonnegative. Positive atanh-series terms and the explicit remainder upper bound give the upper logarithms; downward positive partial sums give a lower log2. Fixed-point endpoints use Python arbitrary-precision integer arithmetic. The strict result depends on the immutable reviewed implementation and this analytic derivation. As the numerical adversary explains, the actual sampling mutant passes internal guards yet violates the cell-mean premise; arbitrary altered code is not certified by a status string. Root's concrete disposition preserves that distinction and the failed inactive-fault history accurately.

Let R=2^100, U=736627539868258100115635444363832284, and L=878668439483319573618263538022. I independently checked

    65536*13*L - U = 11969853181466710380769305597695012 > 0.

The exact certified chain is

    I13 <= U/(65536*13*R) < L/R <= log(2).

The source's exponent upper bound is one half of I13, because I13 uses log(norm_F squared). Thus

    lambda <= I13/2 < log(2)/2 = log(sqrt(2)),

which is exactly Proposition 14's threshold for two digits. This checks the essential factor of two and N normalization. Existence of one such finite N suffices. No separate acceptance of N12, no reproduction of its printed 0.688005 last digits, and no two-sided certificate for the whole historical table are needed. The exact chi3 reflection and the unitary transpose gauge verified in the structural audit transfer this same bound to every character sector used by the positive weighting.

## Root synthesis and scope check

The concrete disposition retains the verified primitive power-4 substitution and the noncircular fixed-ray aperiodicity argument. It correctly withdraws the unsupported simple standard-Rudin-Shapiro renaming. It relies on a continuous lookup factor of the actual physical comb, with support phase retained, and its constant-roof R suspension; it does not infer the physical-hull spectrum solely from an unobserved labelled extension. Periodizing the singular fundamental diffraction preserves singularity on R.

The positive real values (4,1,2,5) are injective. Their finite lookup recovers the squared spin observable and hence its absolutely continuous dynamics. The constant, chi1, and chi3 invariant sectors give singular physical diffraction. Root explicitly identifies this positive formula as a checked deduction from earlier general results rather than a formula printed in the prior paper. It claims neither earliest priority nor an express prior-paper answer to van Enter's named conjecture. It preserves the valid submitted unweighted planar construction and does not certify novelty of that strengthening.

The reviewed synthesis consequently has no material mathematical overstatement requiring repair. `already_solved` here means the literal original target was resolvable by those earlier results, with its exact physical-hull application now checked. It does not declare a narrower unweighted one-dimensional target settled. The certificate itself remains a reproducible finite computation under explicit exact-integer semantics and accepted spectral theorems, not a formal verification of Python or the whole source theory.

The requested QUEUE-only change, preservation of 1/5/blank DOI/frozen files, immediate exclusion after success, and absence of downstream paper/DOI/PR communication match this mathematical disposition. This report does not approve or execute the transaction helper; its concurrency, exact-head, remote-write, and byte-preservation controls belong to the separate operational gate. Original proof-search attempts added: 0. No Git, PR, status, source, paper, DOI, or external communication action was performed.
