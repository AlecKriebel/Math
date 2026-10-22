# Turn 3 — Geometric positivity and phase alignment

Checkpoint: 2026-10-05 06:44 UTC. Mechanism: use the positive-real-part structure of the logarithmic derivative, rather than quadratic energy. Outcome: sharp proper-subclass theorem, including zero-Hayman-index examples, with no full-class extension. Best-guess progress toward full resolution: 10%.

## 1. Coefficient lemma proved directly

If p(z)=1+sum_{n>=1}p_n z^n is holomorphic in D and Re p(z)>0, then |p_n|<=2. For 0<rho<1 and n>=1, Fourier orthogonality gives

    p_n rho^n = (1/pi) integral_0^(2pi)
                            Re p(rho e^(it)) e^(-int) dt.

Taking absolute values and using the mean-value property yields |p_n|rho^n<=2 Re p(0)=2. Let rho increase to 1. This proof uses positivity of the real part, not a pointwise modulus bound.

## 2. Starlike functions of order sigma

Suppose f in S satisfies Re(zf'(z)/f(z))>sigma, where 0<=sigma<1 and the value at zero is understood removably. Define

    p(z)=(zf'(z)/f(z)-sigma)/(1-sigma).

Then p(0)=1 and Re p>0. Since zf'/f=1+2sum n gamma_n z^n, the lemma implies

    |n gamma_n| <= 1-sigma,
    A_f(r) <= (1-sigma)r/(1-r).                          (1)

For sigma=0 these are the familiar starlike bounds. The estimate is attained by

    f_sigma(z)=z(1-z)^(-2(1-sigma)),

using the analytic branch equal to 1 at zero. Indeed its logarithmic coefficients are gamma_n=(1-sigma)/n, and its logarithmic derivative has real part greater than sigma. The standard starlike criterion makes this normalized function univalent. For 0<sigma<1 its Hayman index is zero, because

    (1-r)^2 M(r,f_sigma) <= r(1-r)^(2sigma) -> 0.

Thus the difficult residual zero-index class in TURN_4 is not being described as entirely untouched; (1) already covers this explicit part of it.

## 3. Another cancellation-free case

If gamma_n=e^(in theta)u_n for some fixed theta and all u_n>=0, then

    A_f(r)=H(r e^(-i theta)).

The signed growth bound recorded with the original problem therefore proves the required order for such a fixed function directly. Having real coefficients alone is insufficient for this reduction: changing signs can cancel. No arbitrary function in S has been shown to admit the required positivity or phase alignment.

## 4. Why the extension fails

General univalence does not imply Re(zf'/f)>0. Replacing the full class S by a starlike class changes the problem. Nor does the universal bound on H imply positive real part after one fixed rotation. A proof that assumes this sign control has assumed an extra geometric hypothesis. This turn stops at that exact hypothesis rather than presenting (1) as a full answer.
