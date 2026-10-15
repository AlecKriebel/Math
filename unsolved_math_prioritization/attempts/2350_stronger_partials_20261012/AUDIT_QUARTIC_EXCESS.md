# Independent acceptance: forced unpaired quartic excess

Date: 12 October 2026 (UTC). Erdős 864 / problem 2350 / queue row 1741.

## Verdict and exact accepted source

**ACCEPTED as a necessary-condition partial result.** No correction is required to the finite identities, continuum theorem, endpoint constants, localized alignment bounds, centered Fourier transfer, or claimed endpoint phase threshold. This is not a proof that the endpoint profile is impossible and does not improve the unrestricted leading constant or settle Erdős 864.

The audit reviewed the original quartic proof and accepted its mathematics with the wording refinement below. The complete corrected proof is QUARTIC_EXCESS_PROOF.md. [Editorial redaction: unpublished input, manifest and provenance identity listings are omitted; no mathematical review is removed.] Original inputs were independently checked without editing them. No remote action or publication occurred during that audit.

There is one **nonblocking wording refinement**. Theorem 2's heading says “necessary positive residual phase,” while its parameterized formula is stated throughout the larger geometric cutoff range. Its right side is positive precisely for `0<b<3/(2A0)`, where `A0=7−2√2`. For the full parameterized family, “necessary residual phase bound” would be a more precise heading; alternatively qualify “positive” by that smaller range. The actual endpoint `b=1−√(2/3)` lies in the positive range, and all endpoint assertions are correct without this refinement. The separately frozen `QUARTIC_EXCESS_PROOF.md` makes exactly this heading change and adds the explicit sign-range qualification after (16). `QUARTIC_CORRECTION_MAP.json` records both exact replacements at original byte offsets, with their exact mathematical wording; distributed-file identities are supplied by the public manifest. No inequality, endpoint, constant, proof, or scope statement was changed. The original mathematical content is accepted with this wording qualification; reuse the corrected edition to avoid carrying the overbroad heading forward.

## 1. Finite arithmetic audit

Suppose two distinct representations of a nonzero difference satisfy `a−b=c−e=d`. Then `a+e=b+c`, and the two unordered sum representations are distinct: equality of the unordered pairs would force either `d=0` or identical difference representations. Therefore their common sum is the sole exceptional sum `T`. All four endpoints belong to the reflected core. Fixing one representation uniquely determines the other as `(T−b,T−a)`, so every nonzero difference has at most two representations and every difference involving an unpaired point is unique.

For a core difference, the reflection involution fixes `(a,b)` exactly when `a+b=T`. At a given nonzero `d`, that fixed representation is unique when it exists. Thus, with `p(d)` its indicator,

    2c(d)=r_C(d)+p(d),
    sum_{d≠0} p(d) ≤ |C|.

This accounts exactly for self-reflected differences and for possible midpoint elements; no even/odd exception has been discarded. Mapping `(a,b)` to the unordered sum `{a,T−b}` gives precisely the unique core representation of `T+d`, including diagonal representations. Hence its count is `c(d)`.

The two mixed-difference orientations become `m(d)` and `m(−d)` by reflecting the core endpoint. These cannot meet each other, a core difference, or a U-difference at a nonzero site. This proves

    c+r+m(d)+m(−d)≤1.

Nonexceptional unordered sum uniqueness separately proves `c+m(d)+q≤1`. All four counts are binary; also `q(0)=0` because `U∩(T−U)=∅`. These facts prove

    qr=[q+c+m+r−1]_+

without any missing case. If either `c` or `m` is one, both `q` and `r` vanish; otherwise this is the binary identity `qr=[q+r−1]_+`.

For each fixed `d`, there are exactly `2q(d)−δ(d)` ordered first-pair choices. The second pair is the unique representation of `u4−u3=d` when `r(d)=1`. Consequently

    P_T(U)=2∑_{d≠0}q(d)r(d)−∑_{d≠0}δ(d)r(d).

Every unpaired point contributes to at most one diagonal term, giving an error in `[0,|U|]`. The use of ordered quadruples, including all repeated entries, is correct. The weight inequality follows pointwise from `[s]_+≥φs` for `0≤φ≤1`; the coarse-block inequality follows from `∑[s]_+≥[∑s]_+`. Both are valid on arbitrary disjoint finite blocks, not only intervals.

The cardinality bound used later is elementary here: summing the at-most-two representations over the `2(N−1)` nonzero differences gives `|A|(|A|−1)≤4(N−1)`. Thus all retained diagonal and midpoint errors are `O(√N)`.

## 2. Weak-limit audit

The centered supports stay in a fixed bounded interval. In total variation, the occupation measure for `c`, normalized by `1/N`, differs from half the core difference convolution by `O(|C|/N)`: the errors are the fixed-reflection representations and the omitted zero atom. The unordered U-sum measure differs from half the ordered sum convolution by `O(|U|/N)`. Omitting the U-difference zero atom has the same order. The mixed sum count is already a convolution; its zero count is zero.

Products of finite weakly convergent measures on these common compact supports converge. It follows that the four *linear* occupation measures have the stated convolution limits. Applying the finite weighted inequality to a continuous compactly supported test function in `[0,1]` and using a lattice Riemann sum gives

    liminf P_T(U)/N ≥ 2∫φ(t)J(t)dt.

The compactly supported L² densities make all convolutions continuous; `J=−1` outside a compact set. Supremizing over these test functions yields exactly `2∫[J]_+`. This proof never asserts convergence of `q(d)r(d)`, or of any other product of occupation indicators. It passes a linear lower bound before taking the weak limit. The feared microscopic-product shortcut is absent.

## 3. Endpoint profile and all constants

For `0≤t≤min(b,(1−b)/2)`, direct overlaps give

    (g*g)/2=1−b−2t,
    g*v=√2 t,
    v*v=b−t,
    J(t)=b/2−(A0/2)t.

Thus the positive triangle has radius `b/A0` and contributes `b²/A0` after the theorem's outer factor of two. The condition that it fit in the short range is `b≤A0/(A0+2)`; the other requirement `b/A0≤b` is automatic because `A0>1`.

At the relevant endpoint, `b<(1−b)/2`, so the short formula covers `|t|≤b`. The source's reference to earlier difference domination correctly excludes further positive mass for `|t|≥b`. A direct self-contained check is also available. With `I=[−1/2,1/2]`, `V=[−b/2,b/2]`, `H=1_I*1_V`, and `W=1_V*1_V`, expansion of `1_E=1_I−1_V` gives

    J(t)=(1−|t|)_+ +(√2−2)H(t)+(5/2−√2)W(t)−1.

For `|t|≥b`, `W=0`, while `H≥0` and `√2−2<0`; hence `J≤0`. Therefore the reported positive-part functional is exactly the full functional, not just one contribution.

Independent symbolic simplification and 60-digit evaluation give:

    b = 0.1835034190722739672675719750980362026780175064477766…
    b/A0 = 0.0439890239388684100107264915145809695925624217270201…
    b²/A0 = 0.0080721362944344615043523533672156289644797723096996…
    (2/3)b³ = 0.0041194688433363644318426057951996065462650157612317…
    excess = 0.0039526674510980970725097475720160224182147565484679…
    residual fourth energy = 0.0632275407790928379717786279302785374991383433632081…
    residual phase threshold = 0.0625149642449023979620979936369563727043081800190199…

All rounded source values are consistent. In particular the exact threshold strictly exceeds `0.0625149`.

## 4. New localized result

Fix `0<δ≤b/A0`. The exact localized version of the quartic identity has a diagonal error at most `|U|`. Integrating the positive linear score on `|t|≤δ` gives

    liminf P_N(δ)/N ≥ 2bδ−A0δ².

Every nonzero U-difference has at most one representation, so the local quartic count is at most the number `S_N(δ)` of ordered U-sums in that band. The sum-convolution limit is absolutely continuous and puts no mass at its interval endpoints or at zero; therefore

    S_N(δ)/N → 2bδ−δ².

This proves both sides of (10a). Dividing by `2δ`, then letting `δ` decrease to zero after the N-limits, proves both limits in (10b) equal `b`. Moreover

    limsup (S_N(δ)−P_N(δ))/N ≤ (A0−1)δ²,

which gives the claimed failed-alignment proportion. This statement uses **iterated limits**; it does not assert control for every arbitrarily shrinking band `δ_N`.

The four-variable mixing prediction integrates `(b−|t|)²` over the band, yielding `2b²δ−2bδ²+(2/3)δ³` and local density `b²`. The proven density is `b`, so the enhancement is exactly `1/b=3+√6`. Maximizing `2bδ−A0δ²` at `δ=b/A0` recovers the global bound. No mixing upper bound is proved or assumed in the established lower bound.

## 5. Fourier transfer and parity

Every centered frequency lies in `Z−T/2`. For odd T, F, G, and R may be antiperiodic, but every monomial in a fourth-degree expression has an integer exponent. In particular the exponent in `F³ conjugate(F)` is `u1+u2+u3−u4−T`, so orthogonality gives the claimed count without a factor-of-two or period error.

The symmetric lattice interval defining G is invariant under negation for both parities, so G is real. Its `M=bN+O(1)` consecutive points have exact energy `(2M³+M)/3`; the normalization `N^{-1/2}` on each Fourier coefficient gives `((2/3)b³+o(1))N`.

On `|α|≤K/N`, weak convergence and uniformly bounded first derivatives in the scaled variable imply `sup|R(α)|=o_K(√N)`, while `G=O(√N)`. Each mixed absolute fourth-degree integral there is `o_K(N)`. Strong Sidonicity gives `∫|F|⁴=2|U|²−|U|=O(N)` and hence `∫|R|⁴=O(N)`. The interval geometric-series bound gives

    ∫_{|α|>K/N}|G|⁴=O(NK^{-3}).

Hölder therefore bounds the j-residual mixed integral outside the short arc by `O(NK^{-3(4−j)/4})` for `j=1,2,3`. Taking N to infinity first and then K to infinity proves every asserted mixed term is `o(N)`. The pure residual is intentionally retained.

Expansion now proves

    E_N/N → 2b²−(2/3)b³ >0,
    P_T(U)/N = (2/3)b³ + Re∫R³conjugate(R)/N + o(1).

Division by the positive limiting energy gives exactly

    liminf Ψ_N ≥ [1/A0−(2/3)b]/[2−(2/3)b].

This is a necessary signed-phase requirement. The elementary bound `|Ψ_N|≤1` does not contradict the required approximately 0.062515. Neither a nonpositive phase theorem nor negligible residual phase follows from weak convergence, and neither has been smuggled into the proof.

## 6. Countercontrols and sharpness

The seven-element centered integer control has exactly one repeated unordered sum, zero. Its unpaired set is `{1,2,4}` and has precisely the three ordered solutions obtained by permuting the first three entries of `(1,1,2,4)`. Translation by 26 transforms T to 52 and preserves the equation and admissibility.

Modulo 7, the six unordered sums of `{1,2,4}` are exactly the six nonzero residues, as are its six ordered nonzero differences. There are no reflected pairs. Direct enumeration gives exactly nine ordered quartic solutions. The source correctly limits this example to microscopic finite-group compatibility; it is not an integer interval construction.

For the one-site coupling, the five category masses sum to one and are nonnegative on the stated short range. The positive sum can use the negative-mixed category, holes, or the difference category; the negative sum has the reversed mixed category and the same two shared categories. The common hole and difference categories may support both sum orientations under the stated capacities. Filling each orientation's available mixed category and holes first yields intersection `[q−m−h]_+` with the difference category. Since `q≤r≤r+m+h`, this allocation is feasible simultaneously for both orientations. Thus the positive-part bound is sharp for precisely this abstract paired-site model. It is not a claim that all its couplings can be realized arithmetically.

## 7. Independent computational evidence and limits

The independent finite diagnostic is an independently implemented check, with explicit exceptions rather than assert statements. It imports no code from the authored packet. Its finite representation fibers are stored as actual pair lists, and it enumerates each subset of `[1,18]` once. In addition to actual exceptional sums, strong Sidon inputs with maximum at most 8 are checked against every designated T from −1 through twice their maximum plus 3, covering empty-core, empty-U, midpoint, no-exception, odd-T, and exterior-sum cases. A separate larger integer countercontrol is also tested.

The independent run reports:

- 262,144 subsets considered; 8,559 designated-core inputs checked
- 290,598 exact site checks
- 10,161 occupied sum-only sites beyond the difference span
- 153,858 localized checks at every relevant integer cutoff
- 25,677 noncontiguous coarse-block and rational-weight checks
- 3,748 midpoint cases and 2,646 odd-T cases
- 707 cases with nonzero quartics and diagonal corrections
- 5,100 exact rational interval-overlap checks
- all 13 feasible binary paired-orientation patterns
- 246 independent linear-program checks of simultaneous one-site sharpness

The LP evaluations and decimals are diagnostics. The finite identities and the continuum/Fourier conclusions rest on the proofs above, not on finite enumeration or floating-point optimization.

The independent exact Fourier diagnostic separately uses exact rational Laurent coefficients and verifies 264 residual quartic expansions, including 120 antiperiodic cases. It checks exact interval energy, centered integer orthogonality, both mixed expansions, and the scalar phase norm bound. All integrals are constant-coefficient extractions from proven periodic quartics; no approximate quadrature is used.

The author's verifier was also rerun. Its output matches the supplied normal-mode JSON byte-for-byte. Independent verifiers were run normally and with optimization enabled; their agreement is reported only as aggregate verification here. The supplementary `AUDIT_QUARTIC_CONTINUUM_FOURIER.md` records a separate review of Sections 2–4 with the same verdict.

## Accepted scope and stopping point

Accepted: a proved necessary global quartic excess, a proved short-band near-total alignment requirement, and an exact positive residual-phase threshold at the specified endpoint profile.

Not established: realization or impossibility of the profile; an upper phase or mixing bound; elimination of all other asymptotic profiles; improvement to the unrestricted leading constant; a solution of Erdős 864; novelty or current-literature status.

The next mathematical ingredient would have to restrict arithmetic configurations across sites or control the signed residual phase beyond the scalar norm bounds. This audit does not claim that such an ingredient has been found.

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
