# Exact audit certificate for W4/2 < 0.19

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and explicitly retained classical dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete seven-section mathematical reconstruction and exact rational certificate proof are retained, including all corrections, analytic formulas, rational endpoints, necessary finite examples, assumptions and limitations. Executable code, raw calculation outputs or coefficient arrays, datasets, copied source documents or text, source images and private coordination material are not distributed. Hashes authenticate bytes; they do not prove mathematical correctness.

Retrieval, inspection and numerical-execution statements describe the original audit of October 11, 2026 UTC and its authenticated earlier source inspection. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. References to code, receipts and their execution describe historical private verification; those artifacts are not distributed in this edition.

This is independently authored audit work. It does not use, execute, or transplant either author's numerical program, certificate, or Lean proof.

## Mathematical input

rho(u)=1/((floor(1/u)+1)u), 0<u<=1. For r=1,...,4, J_r is 1/r! times the integral of product rho(u_j) on u_j>0, sum u_j<=1. W4=1-J1+J2-J3+J4.

Take N=8192 and cells I_i=((i-1)/N,i/N], 1<=i<=N. Let m_i=integral_{I_i}rho.

## Exact cell bounds

Since floor(1/u)+1<=1/u+1, rho(u)>=1/(1+u), while rho(u)<=1. Thus on I_1,

1/(N+1)<=m_1<=1/N.

For i>=2 there are finitely many reciprocal-integer breakpoints in I_i. Split it at all of them using exact rational numbers. On every resulting interval (a,b), the integer h=floor(1/u) is constant away from endpoints, so the integral is log(b/a)/(h+1). Its endpoint ratio is at most i/(i-1)<=2.

For any rational x in [1,2], let z=(x-1)/(x+1), so 0<=z<=1/3. The identity

log x = 2 sum_{k>=0} z^(2k+1)/(2k+1)

follows by integrating the geometric series for 2/(1-z^2). With t=18 terms the exact positive remainder obeys

0<=log x-2 sum_{k=0}^{t-1} z^(2k+1)/(2k+1)
 <= 2 z^(2t+1)/((2t+1)(1-z^2)).

All endpoints and partial sums are Python Fraction rational numbers. Add the exact lower/upper pieces to enclose m_i. Set Q=10^15, a_i=floor(Q*lower_i), and b_i=ceil(Q*upper_i). Then a_i/Q<=m_i<=b_i/Q with all coefficients nonnegative. Exact runtime conditions verify interval order, branch containment and cell upper bound 1/N. They are explicit exceptions, not assert statements.

## Simplex bounds and exact convolution

Let P_a(X)=sum_{i=1}^N a_i X^i, and define P_b similarly. Their rth powers have coefficients A_{r,s}, B_{r,s}. A product of cells is fully within the simplex if sum i_j<=N. If it intersects the simplex then sum(i_j-1)<=N, so sum i_j<=N+r. Thus

sum_{s<=N} A_{r,s}/(r! Q^r) <= J_r
 <= sum_{s<=N+r} B_{r,s}/(r! Q^r).

The upper limit deliberately permits an extra boundary layer and is safe; the lower bound also safely discards straddling cells. There is no heuristic quadrature or unbounded discretization error: these are exact set containments. The r=1 upper polynomial degree is N, so the upper limit is capped at rN.

To multiply the integer polynomials, encode X as B=2^256 and place each nonnegative coefficient in a 32-byte little-endian limb. The program verifies sum b_i<2Q and (2Q)^4<B. Every coefficient of every power r<=4 is bounded by (sum b_i)^r<(2Q)^4<B. Therefore no coefficient creates a carry into its neighbor, and ordinary arbitrary-precision integer multiplication gives exactly the polynomial coefficients. Decoding fixed-width limbs and summing the desired range is exact. This also proves that the limb padding is sufficient, rather than assuming it from observed output.

## Result

The output receipt stores exact rational endpoints. The resulting upper endpoint for W4/2 is

9107579506388801169233743962217281937113174719967397591655029
/
48000000000000000000000000000000000000000000000000000000000000.

Exact cross multiplication proves this is less than 19/100. For readable outward bounds it is less than 0.189741239716434, and the gap below 0.19 is greater than 0.000258760283566. The program verifies the exact comparison, not a decimal string comparison. Decimal conversions occur only after exact proof arithmetic, for human-readable output.

Normal, -O and -OO runs produce identical receipt bytes. The calculation uses only Python's standard library (fractions, integer arithmetic, JSON, hashes, and decimal for display). It imports no numerical library. The code and receipts are retained in the original private audit records. They are not distributed in this edition; VERIFICATION.json records their byte identities and the historical execution scope. No numerical program was rerun during editorial preparation.

This certificate establishes the strict integral threshold; it does not independently establish the author's tighter 0.1897123371 bound or any explicit finite n threshold for the game theorem.
