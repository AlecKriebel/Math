# PR209 / 5100015 — independent meromorphic adversary

Frozen author head: `fd09a95b479f376234835a4494693bb1316c85ec`. Reviewed submitted PROOF SHA-256: `4f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2`.

**Verdict: no mathematical blocker found for the source-defined noncircular, nondegenerate confocal ellipse pair.** The argument covers both odd periods and periods congruent to two modulo four, all primitive star winding classes, and justified repetitions. An independently reconstructed direct-area divisor proof confirms the conclusion without using the submitted edge-vector reduction or dn-area trace as its central mechanism. This is a theorem/proof audit, not a whole-preprint, historical priority, or release authorization.

## Exact hypothesis and success criteria

For E: x²/a²+y²/b²=1, a>b>0, and a fixed strictly interior confocal ellipse C with positive axes, let P be an ordered billiard trajectory. Let R_i be intersections of the E tangents at successive P_i,P_(i+1), and Q_i the origin's perpendicular foot on the E tangent at P_i. The target is constancy of signed shoelace area(R) times signed shoelace area(Q), for listed N not divisible by four. A proof must hold for every phase, include odd and twice-odd primitive period, preserve star ordering, and justify repetitions. No finite computation can discharge this universal criterion.

The imported pinned statement says “confocal caustic” without spelling out its conic type. The actual source introduction explicitly defines the EB here using two confocal ellipses. The author likewise states this narrower domain. No transfer to hyperbolic/focal caustics is proved; interpreting the imported wording as all confocal conics would leave a scope gap. The separate source-domain audit should resolve how the final catalog wording records that distinction.

## Independence and route tracking

I first read only INTAKE and the pinned problem/report. At 04:37:20 UTC I froze Jacobi q/f formulas, pole locations, real subgroup period, the potential complementary-divisor mechanism, and explicit falsification plans in `INDEPENDENT_FREEZE.md`. I then read the author's PROOF/SOURCES and, after writing/running my own independent program, the author verifier and inherited review. The inherited PASS is a hypothesis, not evidence counted here.

| Family | Mechanism | Evidence/status | Exact remaining gap |
|---|---|---|---|
| Independent direct area divisor | Ordered areas are even, anti-periodic elliptic functions with complementary simple-pole classes on the reduced real quotient. Adjacent foot double poles cancel because their singular directions are parallel isotropic vectors. | Complete derivation in `INDEPENDENT_PROOF.md`; exact addition algebra and direct complex geometric checks support it. | No gap in genuine elliptic domain found. Classical canonical parametrization remains a cited input. |
| Submitted edge-vector/dn trace | Center pedal is a fixed linear image of an edge-vector polygon. Both areas reduce to phase-shifted dn traces. Odd-order trace product is holomorphic elliptic. | All substantive steps independently re-derived below; full chain survives falsification. | No gap found in exact stated domain. |
| Hyperbolic or degenerate extension | Would require a different canonical domain or a justified continuation/limit with controlled orbit and area definitions. | Not established and not used. | This cannot be inferred from the elliptic proof or numerical limits alone. |
| Wrong-foot numerical control | Replace tangent-side feet by original billiard-chord feet. | Non-discriminating at sampled odd N=5: product is also constant numerically. | Product-only tests do not verify the intended geometry. Direct incidence/projection formulas are needed. |

No route is reopened by merely assuming the target or an equivalent invariant. No outside input was requested or prepared.

## Submitted proof audit

1. **Canonical theorem, parameters and normalization.** Stachel's published Theorem 4.3/(4.9), pp.1614–1615, explicitly gives vertices (−a sn u,b cn u), modulus equal to caustic eccentricity, step 2v, v=2tau K/N, and a=alpha dn(v)/cn(v), b=beta/cn(v). For primitive gcd(tau,N)=1 with 0<tau<N/2, v lies strictly between 0 and K. Thus cn(v), sn(v), dn(v), cn(K−v), alpha,beta and all displayed real denominators are nonzero. Reversing traversal negates both signed areas. No circularity, period-factor mismatch, or modulus/parameter confusion was found.

2. **Area identities (6)–(8).** Expanding Jacobi addition in the endpoint determinant gives (6), including sign in the author's reflected-x convention. Pairwise dn summation yields (7). Bilinear determinant expansion gives area(D)=2area(P)−(1/2)sum det(P_i,P_(i+2)); application of the same pointwise identity at offset 2v proves (8). It does not require that the skip-two graph form a single cycle. The proof performs cyclic sums rather than dividing by an area.

3. **Outer polygon (9)–(10).** Polarity is checkable by substitution: E_0 C_0^−1 B_i satisfies both endpoint tangent equations. Its fixed diagonal scale and midpoint phase give the coefficient in (10). Parallel endpoint tangents require antipodal points; their chord crosses the center and cannot touch a strictly interior confocal ellipse. Therefore no finite real phase is dropped.

4. **Center foot (11)–(15).** Projection on n·X=1 is exactly n/(n·n), with denominator at least b² after the displayed normalization. Quarter-period formulas give dn(K−v)=b/a and a positive cn(K−v). The addition-formula pair sum followed by L=diag(b/a,1)/(2cn(K−v)) equals the actual foot coordinate by coordinate. The 2K antipodal shift turns the sum into a difference of successive shifted vertices. Multiplication by a global minus sign preserves two-dimensional signed area. The determinant factor b/(4a cn²(K−v)) is correct. Thus the phase and coefficient in (15) are correct; no alternative pedal construction is silently substituted.

5. **Odd trace lemma.** [DLMF 22.4](https://dlmf.nist.gov/22.4) verifies the needed period/sign/pole data. For odd q, H={2Kj/q} excludes K, and U(z)=sum_H dn(z+h) has at most simple poles. At c=K+iK', dn(c+t)=−dn(c−t), by evenness and the combined half-period sign. No summand of U(c) is singular. Opposite subgroup elements cancel, including h=0, so U(c)=0. Every possible pole p of U shifts by K to a finite zero of U. The two pole sets do not overlap because q is odd. Consequently U(z)U(z+K) has every possible pole removable and is holomorphic on a compact nondegenerate torus. Constancy follows. Real dn>0 ensures nonzero real trace; the proof does not require proving individual polygon-area nonvanishing.

6. **Finite lattice and parity (18)–(21).** The order of 2v=4tau K/N modulo 2K is q=N/gcd(N,2); gcd(tau,N)=1 is essential and present. Every subgroup element occurs r=N/q times, yielding T=rU rather than accidentally dropping r² in the product. q is odd exactly for N odd or twice odd. The period 2v shifts T(u+K−v) to T(u+K+v), producing the required K-separated product. All winding classes are covered by subgroup equality rather than convexity assumptions.

7. **Repeated and limiting cases.** Repetition multiplies both signed area sums by the repeat count. A primitive divisor of N not divisible by four cannot itself be divisible by four. No admissible nondegenerate N=2 trajectory exists in this domain. The circle must be handled by rigid rotational symmetry; the complex torus argument itself cannot simply be specialized to k=0. The author gives the valid separate symmetry argument. Hyperbolic/focal/zero-axis cases are neither proved nor invoked. Noncentral feet and filled unsigned star-lobe areas are outside the theorem.

Stachel's nearby printed dn real-shift sign is erroneous; this is not imported into the proof. The DLMF sign used here and by the author is correct. No result from k203,a, k303,a, or an unproved area-product theorem is a premise.

## Independent program and controls

Run `check_independent.py` with the pre-existing scientific Python runtime and `-B`; it imports no inherited research code and writes only `CHECK_RESULTS.json` in this folder. SymPy 1.14 and mpmath 1.3 are the existing environment dependencies. Exact symbolic checks reduce additions modulo the defining sn/cn/dn algebraic relations. Numerical diagnostics use 85 decimal digits and are uncertified; no intervals or universal numerical certificate are claimed.

The final receipt records nine symbolic assertions (including a sign mutation that must fail), eleven direct geometric families, seven odd trace orders, three local complex pole/zero probes, and 1,819 finite winding/order arithmetic cases. Families include N=3,5,6,7,9,10,14,18,31 and primitive stars up to winding 15/31, with moduli 0.2,0.7,0.97. Outer vertices are independently obtained from two tangent equations and center feet from direct perpendicular projection. The q-formula is separately checked against tangent incidence. Evenness and the imaginary anti-period are tested on the actual geometric area sums, not assumed from a trace formula.

Products at three phases agree to roughly 85 digits. Excluded N=4,8,12 show relative phase variation approximately 1.86e−2, 4.08e−5, and 2.19e−8, respectively. A noncentral foot at the sampled odd 5-star varies by 2.88e−4. Even trace orders q=2,4,6 vary as well. These discriminate the parity and center hypotheses. The wrong-original-chord-foot variant at odd N=5 does **not** discriminate: its relative spread is about 3e−86. That observation is recorded as a failed negative control, not asserted as a new theorem or counted as successful target verification.

One development run failed because the N=12 negative-control detection threshold 1e−7 exceeded its true variation 2.19e−8. The threshold was tightened to 1e−20, still far above the 85-digit numerical floor. This changed the diagnostic criterion, not the mathematical argument. No author file or source was altered or executed.

## Source-passage coverage

| Primary source | Read location and supported use | Limitation |
|---|---|---|
| Reznik–Garcia–Koiller, arXiv v11 | Local immutable text: introduction (two confocal ellipses), signed-area convention, Table 4 row k303,b, §3.4. | Table/extraction gives target, not proof. No independent broad novelty audit here. |
| Published *Fifty New Invariants* | Local immutable text: p.342 introduction/area convention, p.346 Table 4 and §3.4. [Primary PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). | Source-domain visual audit is handled separately; no PDFs or copied extracts included here. |
| Stachel, published *On the motion of billiards in ellipses* | Local immutable text pp.1613–1615, especially Theorem 4.3/(4.9). [DOI](https://doi.org/10.1007/s40879-021-00524-2). | Explicit elliptic caustic theorem; adjacent sign typo avoided using DLMF. |
| NIST DLMF | Live primary pages [22.4](https://dlmf.nist.gov/22.4), [22.8](https://dlmf.nist.gov/22.8), accessed 2026-10-16 UTC. | Standard analytic inputs only; no prior cyclic product theorem assumed. |

## Strongest verified result and disposition

The strongest verified result is the universal constant-product theorem in the source-defined genuine confocal ellipse domain, for every phase, primitive admissible star, and admissible repeated traversal. The author's complete chain is checkable and survives this independent attack; an independently frozen divisor mechanism provides a second derivation. No mandatory mathematical correction has been identified. Broader conic scope, historical novelty, metadata changes, immutable publication, and release/merge actions require the coordinator's separate decisions. This subagent performed no Git, remote, tracker, provider, or outside-contact mutation.
