Corrected assembly note (2026-10-06): verified barrier for the one-positive-kernel dynamics route only. The complete frozen family body below is retained literally as a credited proof input, SHA256 f7e021af1dfaaf29d04b5582acd5f7e94860dafa2c190e44286fba76ac0b30d1, 2,406 bytes. Its original candidate/pending-review language is historical and is superseded by the exact scoped adversarial credits in independent_review/SCOPED_REVIEW_CREDITS.json. The C-family phrase about replacing original B concerns its strict repair target; in this corrected author tree B is retained as a separately scoped intensity-background theorem. No global review or full non-discrete allocation conclusion is inferred.

---

# Why one positive reversible dynamics is insufficient

This is an exact counterexample to an attempted invariant-law-uniqueness shortcut. It is NOT a counterexample satisfying all count-only Cox tests, and its transport is NOT asserted to be Cox-derived.

On Z set a_n=2^(-|n|) and

    h_n = 1-2^(-n-1) for n>=0,
          2^(n-1)   for n<0.

Thus 0<h_n<1, h_-n=1-h_n, sum a_n=3 and sum a_n h_n=3/2. Define

    F_n = (3/2)2^-n -(1/2)4^-n for n>=0,
          3*2^n -2*4^n        for n<0,
    J_n=2-F_n,
    B_n=J_n/(h_(n+1)-h_n).

The formula F_n=3 sum_(k<=n) a_k(1/2-h_k) is an exact geometric tail identity. In particular 1<=J_n<2 and B_n>0. For distinct n,m define symmetric conductances

    C_nm = a_n a_m + 1_{|n-m|=1} B_min(n,m),
    mu_n = 1+B_(n-1)+B_n+a_n(3-a_n).

Every C_nm is strictly positive, every mu_n is finite. Let p_nm=C_nm/mu_n for m!=n, and p_nn=1/mu_n. Then p has row sum one and is reversible for mu. It has positive transitions between every two distinct states, so positivity, irreducibility and even the Kolmogorov cycle condition hold.

Nevertheless q_n=mu_n h_n is an infinite sigma-finite invariant measure, because

    B_n(h_(n+1)-h_n)-B_(n-1)(h_n-h_(n-1))
      +3a_n(1/2-h_n)=0,

and hence sum_m q_m p_mn=q_n by the exact rank-one tail sum. It is nonreversible: q_n p_nm=h_n C_nm differs from h_m C_nm whenever n!=m. No truncation or ignored boundary current appears in this construction.

Embed it in the canonical orbit of alpha=sum_n mu_n delta_n. Alpha is nonzero locally finite and aperiodic (mu_n grows at both ends). On its countable Borel translation orbit define the spatial transport by the displayed p, covariantly; use identity outside that invariant orbit. It is a genuine invariant alpha-preserving Markov transport with strictly positive jump density on all alpha-supported target locations. The canonical law sum_n q_n delta_(theta_n alpha) is sigma-finite and invariant for that transport, but is not mass-stationary: Mecke between two root indices requires q_n/mu_n=q_m/mu_m, whereas h_n!=h_m.

This blocks inferring Mecke from one positive symmetric kernel on infinite laws. The discrete Cox displacement tests evade it because their conductance c<=e^-2/2 forces every invariant signed current to vanish. On this example those tests cannot all preserve q. Full source repair requires genuine count-only families beyond the discrete current mechanism.
