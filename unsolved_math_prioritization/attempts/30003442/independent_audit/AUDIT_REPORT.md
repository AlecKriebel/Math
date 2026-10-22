# Independent adversarial audit: problem 30003442

## Verdict: PASS, within the stated partial scope

The frozen packet correctly proves the largest mixed-characteristic-root comparison for all positive integers **m,d with min(m,d) ≤ 3**. No mathematical correction is required for that theorem. Its two exact counterexamples to invalid averaging/flow arguments are correct. The packet does **not** prove or refute the unrestricted conjecture, establish general flow monotonicity, or establish novelty. The audit does not upgrade any of those statuses.

The result is an independent mathematical review plus reproducible exact computation, not a formal proof-assistant certification. Author code was read and replayed, but no author functions were imported into the independent verifier. The independent implementation shares SymPy as an exact arithmetic dependency; it uses a separately implemented Sturm sequence and dyadic isolation routine instead of the author's `Poly.intervals` routine.

One nonblocking integrity-hardening issue was found: the author's package checker does not reject a symlink specifically at `MANIFEST.json`. The actual frozen manifest is a regular file, the ZIP is pinned, every archived member matches the actual safe directory, and the independent checker rejects that substitution. This does not affect the frozen mathematical result or its present safe boundary. An optional patch is supplied separately without changing the freeze.

## Frozen inputs

- Author ZIP: `STABLE_ROOTS_30003442_AUTHOR_PACKET.zip`
- Size: 24,172 bytes
- SHA-256: `388e9f7d81f3c5f13dac355b43721a65bd408cfa5b25c0d61b356c96c8a094ff`
- Author manifest SHA-256: `bbc539d32efaccd64ea3918b44e79270cb586a153062643b50d6e8d8024bdf11`
- Eleven flat, safe files; all examined. ZIP contents, individual hashes and byte counts agree with the manifest and receipt.
- The author directory and archive were not modified. No remote write was performed.

## 1. Primary statement and source scope

The normalized target matches Conjecture 1 on printed p. 825 of Petter Brändén's contribution to [Oberwolfach Report 14/2017](https://doi.org/10.4171/OWR/2017/14). The printed gradient requirement is d/m; the polynomial is real, homogeneous and stable. The operator is the product of the distinct factors 1−∂i, followed by diagonal substitution. The reference is the dth power of the variable average.

Printed p. 826 announces a symmetric-subclass theorem and defers its proof. It does not furnish a proof for general inputs. Visual inspection confirms the displayed flow sign and monotonicity direction described in the packet. The exact small example below diagnoses those displayed formulas; it does not contradict the extremal conjecture.

Section 7.2 of [Marcus–Spielman–Srivastava, Interlacing Families II](https://annals.math.princeton.edu/2015/182-1/p08) is an extremal conjecture for a matrix subclass. [Zackrisson's 2017 thesis](https://www.diva-portal.org/smash/get/diva2%3A1106332/FULLTEXT02) reports failure of a stronger root-majorization assertion and separately leaves the largest-root question open. The audit confirms this distinction as historical source attribution; it does not claim an independent reproduction of the thesis's large numerical example.

Both full pinned public corpora were independently rehashed. The target ID has a unique matching problem-number record. The prior-report corpus lacks the `OWR-15219-012` key. No corpus contents or source text are included in this audit packet. Public-source sizes, hashes, inspection details and match results are in `SOURCE_AUDIT.json`.

A fresh bounded public search found no verified unrestricted resolution. This is not an exhaustive literature theorem. Historical repository-search observations in the author log were not promoted into an exhaustive repository-content claim, and this audit did not repeat the entire repository search. The subjective progress percentage in that log is not a mathematical finding.

## 2. Universal proof review

### 2.1 Normalization and coefficient signs

Euler's identity is applicable because d is positive and P is homogeneous. Summing the given derivatives yields dP(1)=d, so P(1)=1. This is not an extra normalization assumption.

For a positive real vector a, a zero P(a)=0 would imply P(ia)=i^dP(a)=0, contrary to stability. Thus P has no positive-orthant zero. Connectedness and P(1)=1 make P positive on that orthant.

For a fixed positive a, the one-variable slice P(a+te_i) is a nonzero real-rooted polynomial, by real specialization. It is positive for t≥0. Its roots are strictly negative, so it has nonnegative coefficients, including its linear coefficient ∂iP(a). Any nonzero derivative is again homogeneous and stable, and its nonnegativity makes it positive on the positive orthant by the same nonvanishing argument. Induction therefore covers every iterated partial derivative. Evaluating at the origin by continuity gives D^αP(0)=α! [x^α]P≥0. Constant derivatives cause no difficulty.

The closure facts used here are valid. For fixed upper-half-plane values of the other variables, each zero of a nonconstant univariate slice lies outside the upper half-plane, so the imaginary part of its logarithmic derivative is strictly negative there. Hence 1−c∂i preserves stability for positive c. Derivative closure follows by taking the limit of (1−c∂i)P/(−c) as c tends to infinity; real specialization follows from Hurwitz. The zero-polynomial alternative is harmless in derivative steps and is ruled out for normalized marginal slices.

### 2.2 Marginal Bernoulli representation

Nonnegative coefficients and P(1)=1 define a probability distribution on nonnegative integer vectors with sum d. Differentiating its generating function yields EX_i=d/m.

Each marginal has real nonpositive roots and positive value at 1, so it factors into terms 1−θ+θz with 0≤θ≤1. Zero roots correspond to θ=1; absent degree corresponds to padded θ=0. Padding to d factors is legitimate. The marginal sum of parameters is d/m, hence each parameter is at most min(1,d/m). Only one-coordinate marginal distributions are factorized; the proof never requires mutual independence of coordinates X_i.

### 2.3 Mixed-characteristic coefficients and real roots

Square-free mixed differentiation gives C_k=Σ_{|S|=k}∂_SP(1)=E e_k(X). Homogeneity gives the exact expansion with coefficient (−1)^k C_k at t^(d−k). Its leading coefficient is 1, C_1=d, and C_k vanishes for k>min(m,d).

Successive applications of 1−∂i preserve multivariate stability, and diagonal substitution preserves upper-half-plane nonvanishing. Real coefficients then force every univariate zero to be real. The top homogeneous part is unchanged, so the polynomial cannot vanish identically or lose degree.

For the reference, differentiating distinct variables gives C_k=binom(m,k)(d)_k/m^k. In particular, when m<d the factor t^(d−m) is retained. The proof neither changes the operator to 1−Σ∂i nor differentiates an already diagonalized polynomial.

### 2.4 Moment identities

Let a=1/m, μ=d/m. The md parameters have total sum d. Expanding the centered square and cube gives

Δ2=Σθ²−d/m=Σ(θ−a)²,

Δ3=Σθ³−d/m²=Σ(θ−a)²(θ+2a).

Consequently 0≤Δ3≤[min(1,d/m)+2/m]Δ2, including parameters equal to 0 or 1. The second and third Bernoulli-sum moments, substituted into Newton's identities using ΣX_i=d, give

C2−C2,∞=Δ2/2,

C3−C3,∞=(d/2−d/m−1)Δ2+(2/3)Δ3.

Both identities were independently derived symbolically through factorial cumulants and reconstructed on every example. No joint-independence assumption is hidden in the argument.

### 2.5 Linear and quadratic cases

For d=1, the polynomial is t−1. For m=1, it is t^(d−1)(t−d). For min(m,d)=2, increasing C2 by Δ2/2 decreases the quadratic discriminant by 2Δ2. Real-rootedness ensures the new discriminant remains nonnegative. The largest quadratic root is positive because the root sum is d>0; removed zero factors cannot alter that maximum. Thus the comparison has the correct direction, including repeated-root equality limits.

### 2.6 Cubic cases

After removing t^(d−3), write q−q0=(Δ2/2)(t−B), where B=2(C3−C3,∞)/Δ2. The case Δ2=0 is separated before division and gives identical cubics.

If m=3 and d≥3, the marginal bound gives B≤d/3+2/9. The exact centered reference cubic is u³−(d/3)u−2d/27. At u=2/9 its value is 8/729−4d/27<0.

If d=3 and m≥3, the bound θ≤3/m is essential and correctly used: B≤1+2/(3m). The centered reference cubic is u³−3u/m−2/m². At u=2/(3m) it is 8/(27m³)−4/m²<0.

In either case, the comparison point is strictly below the largest reference root L. This inference needs only that a monic real-rooted polynomial is positive to the right of its largest root. Thus B<L. The largest reference root is positive because its root sum is d. For Δ2>0, q(L)>0 and, for t>L, q'(t)=q0'(t)+Δ2/2>0. There are no roots at or above L. Repeated roots of q0 do not invalidate this reasoning, because strict positivity of q0' is needed only to the right of L. Extra zeros of the full polynomial are smaller than L.

**Conclusion:** this is a universal proof over the stated infinite parameter ranges, not an extrapolation of the finite checks. Equality classification of the underlying multivariate input is neither needed nor claimed.

## 3. Auxiliary obstructions and corrected flow

### Permutation averaging

The polynomial P=(x+y)²(z+w)²/16 is a normalized homogeneous stable input with all four derivatives equal to 1. Independent averaging over all 24 permutations reduces to the three displayed pairings. The specialization x=t,y=−1,z=0,w=1 is exactly (t²+1)/24. Its nonreal roots disprove stability of the averaged polynomial.

Direct mixed differentiation gives χP=χQ=(t²−2t+1/2)². Thus unchanged mixed-characteristic real-rootedness is not a test for multivariate stability. This is an obstruction to that averaging proof route, not a counterexample to the largest-root conjecture.

### Flow

For m=d=2 and P=xy, the printed positive-time flow gives 2xy−(x+y)²/4 at s=log 2. Its mixed characteristic is t²−2t+3/2, which has no real roots. The corrected flow yields half xy plus half the reference, with largest mixed-characteristic root 3/2 instead of 1. Both the printed sign and decreasing direction are therefore incompatible with this admissible symmetric example.

The corrected substitution with r=e^(−s/d) is sound: its generator is (1/d)Σ_i(x̄−x_i)∂i=T−I. The substitutions compose by multiplying r, preserve the upper half-plane, preserve the uniform gradient, and tend to the reference. These facts do not prove largest-root monotonicity.

The operator identity also has a direct universal coefficient derivation:

C_k(TP)=[m(d−k)C_k(P)+(m−k+1)(d−k+1)C_(k−1)(P)]/(md).

It yields the reported χ(TP) formula. Implicit differentiation at a simple largest root yields the reported velocity. Dividing by f' at repeated roots would be invalid; both verifiers omit the two sampled repeated-root cases. For a monic real-rooted polynomial at a simple largest root, f'>0. Therefore the sign of the independently bounded quantity t f''−(mt−m+d−1)f' gives the velocity sign there.

The JSON label `flow_numerator_interval` in the author output refers to that **scaled** numerator, which is f' times the numerator displayed in the prose. Its sign interpretation is valid; renaming the field would make the scale explicit.

## 4. Computational and adversarial coverage

All listed outputs passed with the final scripts:

- Author normal replay and optimized replay reproduce the frozen 58-example JSON exactly.
- Author four false-claim controls and fourteen package-corruption controls pass, including under optimization.
- Independent reconstruction of all 58 examples: 22 by direct symbolic polynomial construction/differentiation and 36 by partial-matching dynamic programming from the recorded permutation matrices.
- Independently implemented rational Sturm chains count real roots with multiplicities through square-free decomposition, isolate the largest root, and certify every author's reported interval.
- Every largest-root comparison is strictly below the reference in these 58 samples.
- Thirty-four sampled flow velocities have exact positive bounds. Two repeated-largest-root cases are omitted from division by f'.
- Nine universal symbolic identities, four additional sets of operator/generator/composition/endpoint checks, and twenty-one boundary/reference checks pass.
- Fourteen independent mathematical negative controls reject invalid normalization, gradient, homogeneity, coefficient signs, operator order, missing cross derivatives, incorrect stability/flow implications, sign errors and lost multiplicities.
- Nineteen independent package controls reject damaged files, changed manifests, missing proof, extra/hidden/nested inputs, symlinks, traversal metadata and a self-consistent altered proof with rehashed manifest.
- Independent normal, optimized and relocated executions produce identical results. Critical checks use explicit conditional raises and remain active under `python -O`.

The controls validate implementations and individual examples. They do not turn the product-polynomial subclass, an empirical velocity observation, or a finite parameter list into a universal proof.

## 5. Corrections and release boundary

**Required mathematical corrections: none.** No revision to the retained theorem, normalization, moment bounds, root direction or exact counterexamples is needed.

Optional improvements for a later author revision:

1. Reject a symlinked `MANIFEST.json` before reading it. `OPTIONAL_HARDENING.patch` contains a minimal change. `MANIFEST_SYMLINK_CONTROL.json` records the reproduced distinction between the author and independent validators. The current frozen ZIP is unaffected.
2. Rename the sampled-flow JSON field to `scaled_velocity_numerator_interval`, or explain its positive f' scaling.
3. A future exposition could spell out derivative closure using the limit argument in §2.1 above. The standard closure fact already used by the proof is correct.

Keep the unrestricted conjecture marked unresolved by this work. Do not label the theorem new without separate literature review. Do not attach PDFs, extracts, screenshots, raw corpora, source matrices or private coordination to a public package. This audit contains only original reasoning and computations, public metadata and safe replay results. It authorizes no publication or remote changes. The PASS attaches to the exact frozen archive above; applying even the optional hardening patch requires a new author manifest/freeze and corresponding replays.
