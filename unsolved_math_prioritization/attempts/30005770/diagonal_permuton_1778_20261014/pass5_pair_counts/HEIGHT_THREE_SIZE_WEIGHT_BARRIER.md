# Exact height-three states and a sharp size-weight barrier

Final shared PASS5, row1778 /30005770, 14 October 2026. This companion extends the low-chain run investigation to all normalized213-avoiding states of LIS at most3. It proves a restricted-path growth upper bound and an exact obstruction to improving that bound using a pure exponential size weight. It does not prove the global1324 pair estimate.

## 1. State generating functions

Let H_h contain the empty permutation and all213-avoiders of LIS at most h, and write F_h(x) for its ordinary size generating function. The unique minimum decomposition L,1,R has every L value greater than every R value, L in H_h, and R in H_(h-1). Thus

    F_0(x)=1,       F_h(x)=1/[1-x F_(h-1)(x)].              (1)

In particular,

    F_1=(1-x)^(-1),
    F_2=(1-x)/(1-2x),
    F_3=(1-2x)/(1-3x+x^2).                                 (2)

Put kappa=(3+sqrt5)/2 and sigma=(3-sqrt5)/2. Then

    F_3(x)=A/(1-kappa*x)+B/(1-sigma*x),
    A=(kappa-2)/(kappa-sigma)>0,
    B=(2-sigma)/(kappa-sigma)>0.                            (3)

Here A+B=1 and A*kappa+B*sigma=1. For c>=1, the number s_c of nonempty H_3 states of size c obeys

    s_c=A*kappa^c+B*sigma^c <= kappa^(c-1),                 (4)

since division by kappa^(c-1) gives A*kappa+B*sigma*(sigma/kappa)^(c-1)<=1.

## 2. A rigorous growth bound for arbitrary-length height-three paths

Restrict the actual directed canonical kernel K to nonempty H_3 states. For 0<z<=1/(4*kappa), choose t=C(kappa*z), so 1<t<=2, (1-kappa*z*t)^(-1)=t. With f_A=t^|A| and the binary-shuffle upper bound,

    (T_z f)_A
      <=sum_(c>=1) kappa^(c-1) binom(|A|+c,c)(zt)^c
      =[t^(|A|+1)-1]/kappa
      <=(t/kappa)f_A.                                     (5)

Since t/kappa<=2/kappa<1, this is a positive weighted-supremum contraction even at the displayed endpoint. The starting sum is at most

    sum_(a>=1) kappa^(a-1)(zt)^a = zt/(1-kappa*zt)=zt^2.

It follows that the total-size restricted-path generating function is finite at z=1/(4*kappa). In particular, if b_m^(3) counts actual canonical paths all of whose states have LIS<=3, then

    limsup_m (b_m^(3))^(1/m) <=4*kappa=6+2sqrt5.             (6)

This is about10.472136. It exceeds the rigorous lower bound10.271012 in Theorem16 of the inspected primary staircase paper. Those two inspected bounds therefore do not imply a positive restricted-versus-full growth gap. No claim about the latest optimal lower bound is needed here.

## 3. An exact family of actual kernel rows

For p>=2 let A_p=1 direct-sum J_(p-1). For any nonempty C in Av(213), let d(C) be the size of its first skew-indecomposable block. Every such first block has the form1 direct-sum R: in the minimum decomposition, all preceding points form an earlier skew component. Hence C_1=|C|-d(C)+1. The lower pattern S(C) has its maximum in position d(C).

We claim the following exact actual-kernel formula, with q=|C|:

    K(A_p,C)=binom(p+q-1,q)-binom(p+d(C)-2,d(C)-1).          (7)

The upper increasing pairs all start at its first point. Greediness places the lower maximum after that point and before a later upper point. If any lower point preceded the first upper point, it and that greedy witness would make1324. Thus every admissible word begins U.

Conversely, once the first letter is U, no cross1324 can occur: a two-upper/two-lower1324 would require a lower point before the first point of an increasing upper pair, and the other possible color distributions are excluded by the upper Av(213) and lower Av(132) conditions. Such a word is greedy exactly when some later U follows the lower maximum.

There are binom(p+q-1,q) words beginning U. The nongreedy ones have all p-1 remaining uppers before the d(C)th lower; their prefix interleaves those uppers with the first d(C)-1 lowers in binom(p+d(C)-2,d(C)-1) ways, after which all remaining letters are lower. This proves (7), including d(C)=1 and q=1.

## 4. Summing the exact rows at height three

Define

    W_p(x)=sum_(C nonempty in H_3) K(A_p,C)x^|C|.

A first skew block of size d consists of1 followed by an H_2 state of size d-1. The remaining skew suffix is an arbitrary H_3 state. Using (7), (3), and [x^r]F_2=2^(r-1) for r>=1 gives the exact identity

    W_p(x)= A(1-kappa*x)^(-p)+B(1-sigma*x)^(-p)-1
       -(x F_3(x)/2)[1+(1-2x)^(-p)].                       (8)

This holds formally coefficientwise, and as a convergent numerical identity for 0<x<1/kappa. The first three terms sum the first binomial in (7); the subtracted expression is

    x F_3(x) sum_(r>=0) [x^r]F_2(x) binom(p+r-1,r) x^r,

where the coefficient notation refers only to the scalar coefficient sequence of F_2. That sum equals [1+(1-2x)^(-p)]/2.

For fixed 0<x<1/kappa, kappa>2>sigma and A>0 imply

    lim_(p->infinity) W_p(x)^(1/p)=(1-kappa*x)^(-1).         (9)

Indeed the positive A term has strictly larger exponential base than every other term in (8), and its coefficient is nonzero.

## 5. Exact limitation of exponential size weights

Consider the actual H_3 transition T_z on the weighted supremum space with weight f_A=t^|A|, for any fixed t>0. Its norm is at least

    sup_(p>=2) W_p(zt)/t^p.                                (10)

If zt>=1/kappa, even a single row is infinite: (7), or the witness construction, gives K(A_p,C)>=1, so its row dominates F_3(zt)-1.

If zt<1/kappa, (9) gives

    lim_(p->infinity) [W_p(zt)/t^p]^(1/p)
       =1/[t(1-kappa*z*t)].                               (11)

When z>1/(4*kappa), the quadratic kappa*z*t^2-t+1 is strictly positive for every t. Thus the right side of (11) exceeds1, so (10) is infinite. We have proved:

**Size-weight obstruction.** For every z>1/(6+2sqrt5) and every t>0, the actual restricted H_3 transition fails to be a bounded operator on the pure exponential size-weighted supremum space with weight t^|A|.

Together with (5), the threshold1/(6+2sqrt5) is exact for this family of positive exponential size-weight certificates. The exact state constants and the greedy subtraction in (8) cannot move it. This is stronger than a failed crude upper estimate, because the obstruction uses genuine kernel rows.

It does not bound the actual restricted-path growth from below. It does not preclude shape-dependent weights, another Banach space, direct path counting, or a stronger independently verified full-class growth lower bound. In particular it does not disprove the desired1324 weak limit.

## Dependencies and finite-test scope

The exact canonical kernel convention is the accepted PASS2 convention. The height-two companion is LOW_CHAIN_RUN_THEOREM.md, SHA256 cc9008beda1563339e9f308a2fb1987d38835c1af2c521fb87e7ebb5b7c715fa. The public primary growth source is Bevan--Brignall--Elvey Price--Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Theorems9 and16, https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf, reopened and inspected14 October2026. Its exact lower bounds are only used for the stated comparison; no conjectured value of lambda is assumed.

All thresholds above follow from the displayed all-size identities and inequalities. Finite regression checks do not supply an asymptotic growth inference.
