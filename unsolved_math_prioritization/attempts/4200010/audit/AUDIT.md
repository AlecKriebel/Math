# Independent adversarial audit: Knill item 10

Problem 4200010 / AMR-041-0010. Audit date: 4 October 2026.

## Verdict

**PASS for the explicit unrestricted smooth-symplectic, Koopman almost-periodic statement.** No fatal mathematical error or required correction was found in the frozen candidate. The construction supplies a compact connected autonomous Hamiltonian system with an invariant open band of full four-dimensional Liouville measure 1/4, zero exponents in every tangent direction, and no positive-measure almost-periodic invariant subregion. Its individual energy components already fail almost periodicity.

This is an independent AI-assisted adversarial audit, not a formal proof certification, human peer review, historical-priority determination, or resolution of an unstated stronger problem. Retain the manuscript designation `claimed_solved`, AI-assisted and unrefereed, with no novelty claim. The author's later terminology gives additional support for the spectral reading; the 2000 problem itself does not contain a formal definition of almost periodicity.

## Exact frozen input

- Inventory: 12 regular files, 37,232 bytes; no extra files or symlinks.
- Candidate manifest SHA-256: `0e82b3cd57b31613728a1c61cc2eef4c911651b805dbea6ad56dab40736869ad`.
- Candidate proof SHA-256: `541bc3c95d8f04b1d89cac3d2af21815ab331c7eeff9d79ff3591ba8f53eabd1`.
- The proof is 12,628 bytes. `AUDITED_INPUTS.json` binds every input, including the candidate manifest itself.
- Every release file was read. No original file was edited. The input hashes were checked again after all replays and mutation tests.

## Source and interpretation audit

The author's [2000 HTML list](https://people.math.harvard.edu/~knill/seminars/intr/) and the [primary two-page PDF](https://people.math.harvard.edu/~knill/seminars/bozeman/intr-l.pdf), page 2, agree on the target. It is an existence question about positive Liouville measure outside the almost-periodic region and the positive-exponent region. The text does not impose a Euclidean ambient manifold, an exact symplectic form, analyticity, natural mechanics, contact type, genericity, or weak mixing. The subsequent weak-mixing speculation is separately identified as a guess. Other entries discuss discrete spectrum and ergodic invariant measures, supporting the spectral context without furnishing a precise definition for this entry.

The cited [1998 spectral paper](https://people.math.harvard.edu/~knill/publications/knill_singularcontinuous1.pdf) does discuss Koopman operators and spectral measures. It is contextual support, not a proof of the candidate construction or an explicit definition of the 2000 target.

Additional primary evidence located during this audit: Knill's [Differential Equations on Graphs](https://people.math.harvard.edu/~knill/pde/pde.pdf), dated Summer 2016, section 4, PDF page 8, explicitly uses almost periodicity of an invariant-measure system to mean pure discrete Koopman spectrum. This later usage corroborates the candidate's stated convention; it is not a retroactive formal amendment to the older problem.

The source's KAM remark would be misleading if one interpreted every continuum of varying torus frequencies as one discrete-spectrum Liouville system. The candidate avoids exploiting that ambiguity: each energy component in its band is itself ergodic and non-almost-periodic. An independent orbitwise check below also rules out Bohr almost-periodic trajectories. None of this identifies almost periodicity with mere uniform recurrence; that weaker topological convention is different and is not established as the source's meaning.

Source inspection provenance: primary URLs were independently opened with the web retrieval tool; the primary PDF was also visually checked by independently rendering its hash-verified local bytes. The three previously retained primary-source files match their stated sizes and hashes. A fresh direct raw-byte download attempt returned HTTP 403 for each of those three URLs, so no independent second network-byte acquisition is claimed. The 2016 source was inspected through web PDF retrieval, without a locally verified raw-byte hash. No source PDF, source text extract, corpus record, or private coordination file is included in this audit release. `SOURCE_CHECKS.json` records the distinctions.

## Mathematical falsification checks

### 1. Does the skew shift define the claimed torus system?

Yes. Changing a lift by `(r,s)` in `Z^2` changes the image by `(r,s+r)`, so it descends. Its inverse and determinant-one derivative are correct. For every integer `n`, the lift is

`(x+n*a, y+n*x+a*n*(n-1)/2)`.

The expression satisfies both the forward and backward recursion. Thus it covers negative iterates, not just positive powers. The area form descends, and the Fourier pullback sends `(k,l)` to `(k+l,l)` with scalar phase `exp(2*pi*i*k*a)`.

For an invariant square-integrable function, coefficients along a nonzero-`l` chain have equal magnitudes. Such a chain is infinite, so its coefficients vanish by square summability. For `l=0`, irrationality eliminates all coefficients except the constant. This is an ergodicity proof. It does not infer non-almost-periodicity from ergodicity: that separate conclusion follows from the explicitly orthogonal translates of `exp(2*pi*i*y)`.

### 2. Is the suspension genuinely global and symplectic?

Yes. The deck action shifts `t` by an integer and is free and properly discontinuous. It preserves `dx wedge dy`, `dt`, and the product orientation. Therefore the two-form `beta` and one-form `tau` are globally defined and closed on the compact mapping torus. On its product with the energy circle,

`omega = beta + tau wedge dE`,

and `omega^2/2 = beta wedge tau wedge dE` is nowhere zero. It integrates to one. The notation uses global one-forms on circles, not nonexistent real-valued circle coordinates. The original torus map need not be Hamiltonian or isotopic to the identity on its own torus; neither condition is used by this construction.

This four-manifold has an explicitly nonexact symplectic form: its integral on a torus fiber is one. Consequently the construction must not be silently advertised as taking place in a prescribed exact cotangent or standard Euclidean symplectic manifold. That is a real scope distinction, already acknowledged by the candidate, rather than a flaw in the printed unrestricted claim.

### 3. Is the Hamiltonian a real periodic function, with positive full phase volume?

Yes. The denominator in the smooth step `q` is everywhere positive. The standard flatness of `exp(-1/r)` at zero makes `q` smooth at both break points. The two cutoff factors make `h` identically zero on neighborhoods of both endpoints of the chosen circle chart. Its periodic extension is therefore a global smooth real function. Both factors are one on `[1/8,3/8]`, so on the open band `h'=1` and `h''=0`.

The contraction convention gives `X_H=h'(E)*partial_t`. In the band the flow is exactly the unit-speed suspension, and the energy coordinate is fixed. The band measure is the interval length 1/4 times the normalized mapping-torus measure. It is not an isolated hypersurface of ambient measure zero.

Each `N x {E}` in the band is a connected component of its energy level and is regular along that component. The candidate correctly says regular locally: possible components elsewhere at the same Hamiltonian value need not enter this conclusion. On the band `mu=nu*dE` and `H=E`, so the normalized conditional measure is exactly `nu`.

### 4. Are all exponents zero, including the energy direction and seam crossings?

Yes. The frame `V1=partial_x-t*partial_y`, `V2=partial_y`, `V3=partial_t`, `V4=partial_E` is deck-equivariant. In particular the minus sign is essential. The metric making it orthonormal is a legitimate global smooth metric on a compact manifold.

In this frame, at arbitrary real time `s` on the band, the derivative is the identity with the single extra entry `(2,1)=s`. This holds across seams: in a fundamental domain, with `k=floor(t+s)` and `t'=t+s-k`, the coordinate derivative has shear `k`, and changing source and target frames gives shear `s`, not `k`. Exact boundary and negative-time cases were separately tested.

Writing this matrix as `I+sN`, with `N^2=0` and `||N||=1`, yields both the forward and inverse bounds `1+|s|`. The two-sided bound on every nonzero vector proves a limit of zero, not merely a nonpositive upper exponent. Compactness transfers the result to every smooth metric. The transverse derivative is the identity because `h''=0` on the band.

An additional check outside the claimed band gives derivative entries `(2,1)=s*h'(E)` and `(3,4)=s*h''(E)` in the same frame. These are still only linear in time; in fact the same reasoning proves zero exponents globally for this particular Hamiltonian. This strengthening is not needed by the candidate and is not used to enlarge its published claim.

### 5. Does continuous-time ergodicity really hold?

Yes. Invariance under all flow times forces a locally integrable function to have zero distributional derivative in the `t` direction inside each product chart. It is therefore independent of `t` almost everywhere. The seam condition makes the resulting torus function `F`-invariant, hence constant.

The time-one map alone is not ergodic on the suspension: it preserves the clock coordinate. The candidate does not make that substitution. Its small-time argument is necessary and sufficient. Strong continuity of the Koopman group follows first for continuous functions by uniform continuity on compact `N`, then for all `L2` functions by density and unitarity.

### 6. Could a positive invariant subregion evade the orthogonality witness?

No. For each rational time, invariance of the indicator holds almost everywhere. Fubini followed by a countable intersection leaves almost every energy section invariant at every rational time. Strong continuity upgrades that section to full real-time invariance. Suspension ergodicity makes its indicator either zero or one almost everywhere. The measurable section mass then identifies the region, modulo null sets, with `N x J` for a measurable energy set `J`.

The fundamental-domain function `G=exp(2*pi*i*y)` is a valid measurable `L2` function despite its seam discontinuity. At integer times, different translates have nonzero integral Fourier frequency `n-m` in `x`. Their cross inner products vanish, and their squared norms on `N x J` equal `Leb(J)`. Normalization produces an infinite set at pairwise distance `sqrt(2)`, so no positive invariant subregion has a precompact Koopman orbit for every observable.

The argument does not mistake an eigenfunction, an almost-periodic factor, a single orbit, or a zero-measure fiber for an almost-periodic positive-measure region.

### 7. Is the final measure decomposition legitimate?

Yes. Restriction to an invariant measurable subset is an intertwining bounded projection, hence preserves orbit precompactness. If a good region met the band in positive measure, its intersection would contradict the preceding result. The band contains no positive-exponent point. Thus it is disjoint from both kinds of region modulo null sets.

For completeness, a maximal almost-periodic measurable region exists modulo null sets under the stated definition. Almost periodicity passes to invariant subsets and to countable disjoint unions: approximate an `L2` vector by finitely many summands and use the invariant small tail norm. Let `a` be the supremum of measures of almost-periodic regions and take a sequence with measures approaching `a`. Its countable union is almost periodic and has measure `a`; adding any other such region changes it only by a null set. Thus use of a maximal good region creates no uncountable-union loophole.

## Independent orbitwise falsification test

Even if one asks about Bohr almost-periodic trajectories, the same example survives. Fix any point and sample its suspension orbit at integer times. These points all lie in one embedded torus slice. The continuous circle-valued function `exp(2*pi*i*y)` on that slice gives the sequence

`u_n = exp(2*pi*i*(y+n*x+a*n*(n-1)/2))`.

For two distinct integer shifts `k,j`, the phase of `u_(n+k)/u_(n+j)` is

`(k-j)*x + a*((k-j)*n + (k*(k-1)-j*(j-1))/2)`.

Its slope in `n` is the irrational number `(k-j)*a`. Density of irrational rotation implies that the supremum distance between the two shifted scalar sequences is exactly 2. Their translates are therefore not precompact in the uniform norm. A Bohr almost-periodic continuous trajectory would give precompact sampled translates, and composition with the uniformly continuous function on the compact slice would preserve that property. Contradiction. This applies to every point of the band.

This is an additional auditor-derived check, not a substitute for the written invariant-measure proof or a claim about the distinct notion of uniform recurrence.

## Executable replay and attempted breakages

`python3 run_audit.py ../submission` verifies the exact input hashes, reruns both candidate scripts, compares the author output with its recorded JSON, runs independent checks without importing candidate code, tests deliberately damaged temporary copies, and rechecks all original bytes.

Results:

- 3,248 original exact checks passed; all six original controls passed.
- 2,460 additional exact checks passed, including exact arithmetic in `Q(sqrt(2))`, torus representative changes, negative and fractional flow times, seam hits, group laws, derivative/inverse/symplectic identities, exact positive-semidefinite norm bounds, transverse energy terms, and orbitwise phase differences.
- Eight supplementary algebra controls passed. They distinguish fixed zero-speed motion, integer-time invariance from flow invariance, the wrong return sign, an omitted transverse term, a single energy from a positive-length band, off-plateau disintegration weights, clock factors from full systems, and translation without shear.
- Four actual manifest mutations were rejected: edited proof bytes, an extra file, a missing file, and a same-content symlink.
- Every original candidate byte remained unchanged.

Counts are coverage metadata, not a measure of proof strength. The finite programs do not establish irrationality, smooth flatness, Fourier completeness, infinite-chain square summability, quotient smoothness, disintegration, strong continuity, or infinite-time limits. Those points were checked in the written mathematical audit above.

## Remaining limits and publication recommendation

No mandatory proof edit is requested. The 2016 terminology reference and the orbitwise check may be useful editorial additions, but are not prerequisites for the stated theorem. If the candidate is changed, bind and review the changed bytes rather than describing this audit as applying automatically.

Keep the exact ambient category and almost-periodicity definition visible. Do not upgrade the claim to weak mixing, standard Euclidean phase space, a prescribed cotangent bundle, analyticity, natural mechanics, robustness, genericity, or historical novelty. The bounded literature search found corroborating context, not an authoritative prior exact resolution; it cannot certify priority. Repository duplicate checks and corpus provenance in the author's packet were not independently repeated against remotes, in accordance with the audit's no-remote scope.

Only the audit directory is a portable authored deliverable. The candidate and audit manifests are separate and jointly identify the material examined. No remote publication, repository change, external communication, or helper delegation was performed by this audit.
