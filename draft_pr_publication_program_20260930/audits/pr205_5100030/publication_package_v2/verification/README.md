# Portable focal-distance invariant calibration

Requires Python 3.10+ and mpmath 1.3.0, the sole dependency listed in requirements.txt. No repository, archived audit, network access, external file or private runtime path is needed by verify.py.

With that dependency available, run:

```sh
python3 -B verify.py > results_normal.json
python3 -B -O verify.py > results_optimized.json
```

Both commands must exit zero and report PASS. All validation uses explicit exceptions and remains active under -O. The default has eight proper confocal configurations, 70 validated positive-calibration traversals and 25 required rejection controls. For more precision, use --digits 90; the default is 60 requested digits plus 40 working guard digits. Requested digits must be between 50 and 160.

These are finite, arbitrary-precision, **noninterval diagnostics**, not a universal proof or a novelty claim. The theorem depends on the written geometric bridge and classical Landen/Fourier identities. The value formula is shared audited mathematical input; this implementation does not claim independent discovery of it.

## Physical quantity and numerical construction

The outer ellipse has axes a>=b>0 and the caustic axes alpha,beta satisfy a²-alpha²=b²-beta²=lambda with 0<lambda<b². The noncircular theorem has a>b and alpha>beta; a=b is used separately as a circular boundary calibration. The foci are F±=(±sqrt(a²-b²),0).

For every ORIGINAL physical chord, q± is ordinary Euclidean distance from F± to its COMPLETE supporting line. The measured quantity is

    I = (sum q+)(sum q-).

The program shoots for the caustic using accumulated ordinary ellipse angle. Initial tangents come from affine circle tangency. It propagates the forward line/outer-ellipse intersection and reflects the unit direction about the ellipse gradient normal. It does not choose physical vertices from a Jacobi parameterization or project points back onto a conic. Every orbit must pass closure, winding, boundary, caustic tangency, reconstructed specular reflection and q+q-=beta² checks. Primitive cases also reject every shorter return.

All coprime windings for N=3,5,7 are checked at a/b=2, together with two aspect-ratio controls. Each fixed pair is tested at three phases in both directions. Actual repeated traversals r=3 and r=5 are checked against r²I; these are labelled repetitions rather than new primitive periods. Formula evaluation continues to use the original primitive N.

## Shared classical normalization

The parameter is m=c²/alpha²=k², with 0<m<1. Write K=K(m), and define

    D_N(u) = sum_j dn(u+4Kj/N | m),
    C_N(u) = sum_j cn(u+4Kj/N | m).

For odd primitive N, set

    q = exp(-pi K(1-m)/K(m)), Q=q^N,
    M = [theta_2(0,Q)/theta_3(0,Q)]^4,
    K_M = (pi/2) theta_3(0,Q)^2,
    gamma = K/(N K_M).

The common Landen/Fourier value is

    D_N(u)^2 - m C_N(u)^2 = (1-M)/gamma²,
    I = alpha² (1-M)/gamma²
      = beta² [sum_j 1/dn(4Kj/N | m)]².

The implementation checks the physical I against both value forms and checks the normalized trace at three real phases. It separately verifies gamma=1/sum_j dn(2Kj/N). The 2K and 4K dn grids are permutations for odd N because dn has period 2K. The cn trace must use the 4K grid; the wrong 2K grid is an explicit rejection control. Do not conflate cn/dn amplitudes or the parameter m with the modulus k.

Classical antecedents include Khare–Sukhatme, *Generalized Landen Transformation Formulas for Jacobi Elliptic Functions*, arXiv:math-ph/0312074v1, particularly the odd-order formulas, and the Fourier/theta normalizations in DLMF 22.11 and 22.2. The package's audited normalization supplied the exact formula above. This verifier is an application/calibration of that shared formula, with no claim of firstness or current openness.

For m=0, use I=N²beta² directly. The program checks circular N=3 and N=5 stars physically in both directions. The degenerate endpoint m=1 is excluded.

## Exact even-period counterexample

Take outer axes a=sqrt(3/2), b=sqrt(3)/2 and lambda=1/2. The caustic axes are alpha=1, beta=1/2, with common c=sqrt(3)/2. The four-period axis diamond with vertices (±a,0),(0,±b) has each focal sum 2sqrt(2), so

    I = 8.

In the SAME confocal pair, the axis-aligned rectangle with vertices (±1,±1/2) has each focal sum 3, so

    I = 9.

Its initial ellipse angle is atan(1/sqrt(2)). Both trajectories pass the physical checks. The rectangle lies on the outer ellipse, its four support lines are tangent to the caustic, and the outer gradient at (1,1/2) is (2/3,2/3), giving specular reflection at the right-angle corner. Their unequal exact values show why the odd-period restriction matters.

## Fail-closed controls and result interpretation

Every scalar is checked for real finiteness before sums/maxima or comparisons; JSON output also forbids nonfinite values. Controls require rejection of NaN/Inf, complex scalars, bad geometry/period/parameter inputs, a wrong finite identity, the wrong cn grid, segment distances substituted for complete lines, and a corrupted physical orbit. A negative control passing silently makes the program fail.

The JSON tolerance is 10^(-requested_digits+20). Physical closure is max(position discrepancy/a,direction discrepancy). Tangency and focal-product residuals are divided by a²; boundary, reflection and winding residuals are dimensionless. Value-comparison errors use max(1,abs(expected)) scaling. These are observed residuals, not certified error bounds.

results_normal.json and results_optimized.json record actual complete executions. RUN_SUMMARY.json records their equality after removing the optimization flag, source identity and the portable command lines. Python 3.10 syntax is checked; the actual executions used Python 3.14.6. No dependencies were installed or copied to produce these results.
