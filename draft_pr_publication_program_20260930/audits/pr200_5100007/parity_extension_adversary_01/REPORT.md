# Independent adversarial report

UTC: 2026-10-16 04:50:11. Narrow audit completion estimate: 100%.

**Verdict: the proposed primitive parity iff is proved by the paired-torus mechanism, with the odd-period implication supplied explicitly.** No counterexample or unresolved parity gap was found. This is a mathematical verification report, not a novelty, priority, or publication-approval determination.

## Exact strongest result

For a noncircular real ellipse with a fixed proper nested nondegenerate confocal elliptical caustic and primitive least billiard period N≥3, the ordinary product of distances from the consecutive-boundary-tangent intersections to either fixed focus is phase independent **if and only if 4|N**. Every admissible coprime star winding is covered. Repetition raises the strictly positive primitive product to an integer power and cannot restore constancy.

The proof uses the published canonical billiard parametrization already stated in the permitted original proof and standard Jacobi analytic facts checked against DLMF. It does not claim a new derivation of that established dynamics input. The subsequent algebra, torus order, all relevant divisor multiplicities/collisions, real-phase analytic implication, and the exceptional N=4 case are checked in `DERIVATION.md`.

## Decisive necessity argument

On T=ℂ/(2Kℤ+2iK'ℤ), let p=iK', let δ=4Kτ/N be the primitive step, and let G=⟨δ⟩ have order L=N/gcd(N,2). For δ≠K, the paired squared-distance function H has divisor

    2[p+K]+[p+K+δ]+[p+K-δ]-4[p].

Its cyclic norm F=∏_{j=0}^{L-1}H(u+jδ) therefore has divisor

    div(F)=4∑_{g∈G}[p+K+g]-4∑_{g∈G}[p+g].

The two cosets coincide exactly when L is even, equivalently 4|N. In the other parity classes they are disjoint, so the norm has genuine poles and zeros of order four and is nonconstant.

For ordinary real one-focus products, P_-(u)=P_+(u+2K), and

    P_+(u)² P_-(u)²=F(u)^(N/L).

Constancy of either single-focus product would force the other and this paired norm power to be constant on the real phase circle. The identity theorem then forces a constant meromorphic function, contradicting the displayed nonzero divisor. **For odd N, the phase shift 2K moves to a different orbit; no within-orbit antipodal pairing or identification of the paired norm with a single-focus product is made.**

When δ=K, primitivity forces N=4 and the divisor drops to 2[p+K]-2[p]. Its order-two cyclic norm cancels, as required for sufficiency. For general 4|N the antipodal point really is in the orbit, so the original positive-direction pairing applies.

## Finite validation and falsification attempts

`check.py` and `CHECK_RESULTS.json` provide reproducible controls:

- Exact symbolic factorization residual: zero.
- Exact rational divisor checks: 1,521 primitive admissible winding cases with 3≤N≤100, including the N=4 degree drop. Divisor vanishing occurred exactly for 4|N.
- Direct geometric controls: 117 families, all coprime windings for 3≤N≤16 at k=0.3, 0.8, 0.97, using 100 decimal digits and 13 real phases. Each Q was computed by solving the original pair of boundary-tangent equations; both foci were tested.
- Every odd or 2 mod 4 control showed a nonconstant product. The smallest sampled relative range was approximately 1.49×10⁻¹⁶. At k=0.8, examples were N=3, τ=1: 0.1316576; N=5, τ=2: 0.00801662; N=6, τ=1: 0.00404740; N=10, τ=3: 0.0000162926.
- Every 4|N control was constant to numerical precision: maximum sampled relative range 2.29×10⁻⁹⁹. The largest relative residual in the tangent-intersection formula was 1.65×10⁻⁹⁹. The focus-swap phase identity had maximum log-product error 2.74×10⁻⁹⁹.

These finite checks support the derivation and would expose many sign, winding, or exceptional-case errors. They are not the proof of universal constancy/nonconstancy. In particular, small observed variation near the circular limit must not be mistaken for an invariant.

Run from this directory with:

    /opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P check.py

The script loads only the explicitly permitted shared third-party runtime packages (mpmath 1.3.0, SymPy 1.14.0), and does not read that family's authored work.

## Scope, independence, and remaining gaps

The circle is excluded and would invalidate the necessity statement, since both foci then coincide at the center. Hyperbolic/degenerate caustics, separatrices, and N=2 are excluded and remain unclassified here. They are outside the exact claim, rather than gaps in its proof. No unresolved mathematical gap remains in the claimed parity extension once the cited standard canonical parametrization is taken as input.

The initial challenge and approach were frozen before reading the permitted original proof. That proof was the only authored neighboring result read; no sibling verdicts, favorable reviews, or priority conclusions were read. The first disk write failed with ENOSPC, so the initial freeze was first preserved in the tool transcript and parent message, then persisted when allocation resumed. All authored artifacts are confined to the assigned directory. No local Git/ref/PR/publication action, external outreach, or release was performed.

`SHA256SUMS.txt` hashes the frozen input proof and all audit artifacts except the manifest itself; names are relative, files were required to be regular non-symlinks, and no recursive directory scan was used.
