# Turn 5: the actual sphere norm for quadratic networks

Fifth and final substantive author turn. The original arbitrary-activation robustness question remains unresolved. This turn proves a log-free spherical lower order for all quadratic-on-the-sphere networks, with hidden biases and arbitrary width permitted. It makes the radial-constant ambiguity explicit: the operator norm of a quadratic form alone cannot lower-bound its sphere Lipschitz norm, because a multiple of ||x||² is constant on the sphere. The original BLN polynomial/tensor and spectral-proxy results are credited; this turn supplies a direct sphere-norm argument for the quadratic subclass, not a priority claim or the general conjecture.

## 1. Statement and activation scope

Let d≥2, n≥8d. Let x_i be independent uniform on S^{d-1}, and y_i independent fair signs. With probability at least

    1-2exp(-n/32)-2exp(-d)-2exp(-6d),                    (1)

the following holds simultaneously for every k≥1 and every function

    f(x)=x^T A x+b·x+c,    A symmetric, rank(A)≤k,

having empirical squared error at most1/256:

    Lip_{S^{d-1}}(f) ≥ (1/8192)sqrt(n/k).                (2)

In particular this applies to f(x)=c_0+sum_{j≤k}a_j(w_j·x+β_j)², for which A=sum a_jw_jw_j^T has rank at most k. The representation can have arbitrary real coefficients and biases, chosen after seeing the data.

The polynomial activation t² is not globally Lipschitz, so this is first a polynomial subclass result of the kind separately studied in the primary source. To connect it precisely to a fixed globally Lipschitz activation, set

    ψ(t)=t² for |t|≤1, and ψ(t)=2|t|-1 for |t|>1.

This ψ is globally2-Lipschitz. Any quadratic-neuron representation above can be implemented on the sphere with this one ψ by replacing each (w_j,β_j) by (w_j/R_j,β_j/R_j), where R_j≥max(1,||w_j||+|β_j|), and replacing a_j by a_jR_j². Every sphere argument then stays in the quadratic core. Thus(2) also applies to these quadratic-core realizations for a fixed Lipschitz activation. It is NOT a result for arbitrary ψ-networks whose units cross out of that core.

## 2. Exact deterministic sphere-norm information

For q(x)=x^T A x on the unit sphere,

    Lip_S(q)=λ_max(A)-λ_min(A)=:s(A).                    (3)

To prove the upper bound, subtract mI with m=(λ_max+λ_min)/2. Since ||x||=||y||=1,

    q(x)-q(y)=(x+y)^T(A-mI)(x-y),

and ||A-mI||_op=s(A)/2, ||x+y||≤2. For the reverse inequality, use a unit-speed great circle in the plane of extreme eigenvectors. At the vector halfway between those eigenvectors, the derivative of q along the tangent has magnitude s(A). Chord distance divided by arc distance tends to1. This proves(3), including the case s(A)=0.

For L=Lip_S(f), the even and odd antipodal parts each have Lipschitz constant at most L. Therefore

    s(A)≤L,              ||b||≤L.                       (4)

If rank(A)<d, zero is an eigenvalue, so ||A||_op≤s(A) and ||A||_*≤rank(A)L. At full rank this fails for scalar matrices, but

    ||A-mI||_*≤dL/2                                    (5)

always holds. We will pair A only with a trace-zero random matrix, so the scalar shift in(5) is harmless.

## 3. Balanced signs and two uniform concentration bounds

With failure probability at most2exp(-n/32), both labels occur at least3n/8 times. Conditional on the entire label sequence, take the same number m of each sign (for example the first m of each), where m is the smaller label count. This selects N=2m≥3n/4≥d independent spherical points and fixed balanced signs. Define on this subset

    Ω=sum_i y_i x_i x_i^T,       V=sum_i y_i x_i.

The crucial exact identity is trace(Ω)=sum_i y_i=0. We establish

    ||Ω||_op≤512sqrt(N/d),      ||V||≤8sqrt(N)            (6)

with conditional failure probability at most2exp(-d)+2exp(-6d). These constants are uniform in the particular balanced sign sequence, so the conditioning is legitimate even though the selected subset depends on labels.

For completeness, a scalar-moment proof of the first bound avoids an unquantified matrix concentration citation. For any unit u, put Z=d(u·x)². The spherical identity gives EZ=1 and E Z^h≤(2h-1)!!≤2^h h!. Hence, for integer h≥2,

    E|Z-1|^h≤2^{h-1}(EZ^h+1)≤4^h h!.

For |λ|≤1/8, expanding the centered exponential and bounding absolute moments gives

    Eexp(λ(Z-1))≤1+sum_{h≥2}(4|λ|)^h
                  ≤exp(32λ²).

Independence, also with the fixed signs, and exponential Markov yield

    P(|u^TΩu|>t)
      ≤2exp[-min(d²t²/(128N),dt/32)].                  (7)

Indeed optimize with λ=dt/(64N) until that reaches1/16; for larger t choose λ=1/16. In the latter case dt≥4N and -dt/16+N/8≤-dt/32. Balanced signs remove the deterministic sum y_i/d before this argument.

Choose t=128(sqrt(N/d)+1). Each exponent in(7) is at least4d. A1/4-net with at most9^d points, and the general symmetric-matrix estimate ||Ω||≤2max_net|u^TΩu|, give failure at most2exp[-(4-log9)d]≤2exp(-d). Thus ||Ω||≤256(sqrt(N/d)+1)≤512sqrt(N/d), since N≥d.

For the vector bound, the same spherical even-moment identity gives Eexp(λ u·x)≤exp(λ²/(2d)). Hence for every unit u,

    P(|u·V|>t)≤2exp[-dt²/(2N)].

A1/2-net has at most5^d points and controls ||V|| by twice the maximum linear form. With t=4sqrt(N), the failure probability is at most2exp[-(8-log5)d]≤2exp(-6d), yielding the second bound in(6). The nets are fixed before the data are observed, and(6) controls every subsequently chosen A and b.

## 4. Interpolation correlation and rank split

On the label event, restrict the empirical errors e_i=f(x_i)-y_i to the selected N observations. Cauchy–Schwarz and the original full-sample error bound give

    sum_selected y_i f(x_i)
       =N+sum_selected y_i e_i
       ≥N-sqrt(Nn)/16≥N/2.                             (8)

The last inequality follows from N≥3n/4. Since the selected signs sum to zero, the constant term cancels and the left side of(8) equals

    trace(AΩ)+b·V.

At least one of the two terms has absolute value at least N/4. If it is the linear term, (4) and(6) give L≥sqrt(N)/32, stronger than(2) for every k≥1.

If it is the quadratic term and k<d, use rank(A)≤k, (4), and(6):

    N/4≤kL·512sqrt(N/d),
    L≥sqrt(Nd)/(2048k)≥sqrt(N/k)/2048.                 (9)

If k≥d, use trace(Ω)=0, shift A by mI, and apply(5):

    N/4≤(dL/2)·512sqrt(N/d),
    L≥sqrt(N/d)/1024≥sqrt(N/k)/1024.                  (10)

Finally N≥3n/4 converts all three cases into the weaker constant(2). The same event controls every k and all data-dependent coefficients. No restriction on parameter magnitudes or conditioning was imposed.

## 5. What this closes and what remains

This closes the source lower order on the actual sphere norm for the stated quadratic subclass, including biases and overcomplete widths. Unlike an operator-norm proxy, the proof correctly ignores radial constants through the trace-zero signed matrix. It does not handle arbitrary Lipschitz activations or general piecewise-linear networks with dependent biased units. Combining it with the first four turns still leaves the original unrestricted high-dimensional lower-bound conjecture unresolved5/5.

The final exact controls check spectral-spread identities in rational two-dimensional cases, antipodal cancellation, scalar-shift trace cancellation, moment bounds and all numerical implications. They supplement the analytic proof and do not certify an infinite probability statement by finite testing. Author search stops at this fifth turn; a separate complete independent review is required before publication disposition.
