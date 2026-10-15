# Reproduction and evidential limits

ROOT replay of the packaged files: 11 October 2026, Python 3.14,
standard-library execution, no external numerical libraries.

The core exact checker completed 21,508 explicit checks with rational
arithmetic and arithmetic in Q(sqrt(8/15)). For periods 3 through 101 it
checked both focal signs for every coprime positive rotation with
0 < tau < n/2: 1,053 odd primitive pairs, 255 primitive pairs of period
2 modulo 4, and 263 primitive pairs of period 0 modulo 4. Repeat
multiplicities 2, 3 and 4 preserve the divisor criterion in every sampled
case. The checker also verifies the exact confocal triangle geometry,
its focal products and the doubled six-event difference 180 sqrt(30);
a physical primitive four-period control gives products 4 and 64/25
on the same ellipse/caustic pair.

The exact checker also passed under optimized Python, because its checks
use explicit exceptions rather than removable assert statements.
The recorded normal-run JSON is verification/exact_results.json.

The two separately authored theta diagnostic scripts were replayed from
a fresh scratch copy of the package scripts. The only changes to the
independent scripts for this package were explicit rejection of optimized
Python and redirection of proof references to the accompanying manuscript. Their main computations and tolerance tests are retained.

check_divisor.py passed 1,053 odd-half-period positive cases, including
1,003 star-turn cases, and 1,036 disjoint even-half-period divisor
controls, with 30 sampled theta cases. Observed maximum normalized
norm disagreement was approximately 1.22e-15 and zero-location residual
approximately 2.30e-13. These are observed residuals, not rigorous error
bounds. Physical n=4 and doubled n=3 negative controls vary as expected.

check_classification.py passed the same 1,053/255/263 full-sn-torus
primitive-pair counts, both foci, plus 33 sampled numerical cases and
their repeated traversals. Some analytically nonconstant cases show
variation below floating-point resolution; the output reports that
limitation rather than calling them constant.

The manuscript's universal proof independently establishes the analytic
Jacobi factors and complete divisor for every admissible primitive
period, then uses compactness and the identity theorem. Neither finite
enumeration nor unvalidated theta diagnostics prove that universal claim.
No interval certification or proof-assistant formalization is supplied.

The source assumptions are strict nested nondegenerate confocal
elliptical caustics. Circles have a direct constant-radius argument;
hyperbolic or degenerate caustics are not covered. Repeated return
length is distinguished from primitive least period throughout.
