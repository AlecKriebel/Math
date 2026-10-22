# Approach 2: Baker separation from a small residue

**Result:** the desired entropy size for a restricted seed class, with a bounded-denominator rational-neighborhood extension. This reconstructs the classical logarithmic-form strategy; no novelty is claimed.

We use the established Baker–Wüstholz consequence (see BLMV, Theorem 4.3): for fixed multiplicatively independent a,b>1 there are c0,D>0 such that
|u log a+v log b| >= c0(1+|u|+|v|)^(-D)
for every nonzero integer pair (u,v). When u=0 or v=0 the bound also follows by reducing c0. We use this theorem as an external input, not as an original proof.

## Small-seed theorem
Fix 0<theta<=1. There are M,N,s0 depending only on a,b,theta such that, for s>=s0 and any real x with 1/s<=x<=s^(-theta),
C({a^n b^k x mod 1: 0<=n,k<=M log s}, (log s)^(-N)) >= c_theta log s.
Thus its logarithm is at least (1/2)log log s for sufficiently large s. Here c_theta>0 also depends on a,b.

Proof. Put Y=log(1/(2x)). For s large, theta log s-log 2<=Y<=log s. For each integer
0<=k<=floor(Y/(2 log b)),
put n_k=floor((Y-k log b)/log a). These exponents are nonnegative and bounded by a constant times log s. The numbers
 y_k=x a^(n_k)b^k
belong to (1/(2a),1/2]. Distinct k give distinct exponent pairs and distinct values. All coefficient differences n_k-n_j and k-j are bounded by C log s. Therefore Baker–Wüstholz gives
|log y_k-log y_j|>=c1(log s)^(-D).
Since the exponential has derivative at least 1/(2a) on the logarithmic interval in question, the mean value theorem gives
|y_k-y_j|>=c1/(2a) (log s)^(-D).
Choose any integer N>D. For sufficiently large s this exceeds (log s)^(-N). No interval of that length covers two of the y_k. Their number is at least c_theta log s. Taking logarithms proves the conclusion. All estimates are uniform in x in the indicated range. QED.

The same result holds for x in [1-s^(-theta),1-1/s] by reflection on the circle.

## A forward-small-residue criterion
Suppose an orbit point z=a^(n0)b^(k0)r/s mod 1 satisfies 0<||z||<=s^(-theta), with n0,k0<=C log s. Coprimality implies ||z||>=1/s. Apply the theorem to ||z|| and include the original exponents in the total cutoff. The desired covering lower bound holds for A_{floor(M' log s)}(r,s), where M' depends on a,b,theta,C. Reflection and changing from circle arcs to intervals in [0,1] lose at most a fixed factor. In particular, the conclusion holds for reduced representatives 1<=r<=s^(1-theta), and for their reflections.

This is an independently specified, proved restricted condition. It is not a silent correction of the report's printed condition |s|<r^(1-theta).

## Extension near a fixed rational
Fix Q>=1 and 0<theta<=1. Suppose r/s differs modulo 1 from u/q by a signed nonzero epsilon, where 1<=q<=Q, gcd(q,ab)=1, and |epsilon|<=s^(-theta). For sufficiently large s the desired conclusion again holds, with constants depending on a,b,Q,theta.

Choose h=lcm(ord_q(a),ord_q(b)); for q=1 take h=1. Then a^h and b^h are multiplicatively independent and both fix u/q modulo 1. Hence their orbit of r/s equals u/q plus their orbit of epsilon. The nonzero difference of two rationals with denominators s and q has |epsilon|>=1/(qs)>=1/(Qs). Apply the preceding proof with S=Qs, bases a^h,b^h, and exponent theta/2, which is valid for large s because s^(-theta)<=(Qs)^(-theta/2). The final exponents in a,b are multiplied by h. Since there are only finitely many q<=Q, all constants can be chosen uniformly. The produced points occupy a translated/reflected arc of length less than 1/2; their circle separation is unchanged. Splitting a wrapping arc does not weaken the lower bound on interval covering. QED.

## Remaining gap
No argument here guarantees a power-small residue, or a power-close approximation to one of these bounded-denominator rationals, within O(log s) steps for every numerator. Pigeonholing only O((log s)^2) points gives inverse-polylogarithmic closeness, not s^(-theta). Replacing one by the other would be an invalid quantifier/scale upgrade.
