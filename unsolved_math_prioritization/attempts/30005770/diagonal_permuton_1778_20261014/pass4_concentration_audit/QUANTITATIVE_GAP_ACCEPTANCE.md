# Independent analytic acceptance of the quantitative window-gap certificate

Shared PASS4, 14 October 2026.

## Verdict and corrected final input

**Accepted.** `pass4_window_gaps/QUANTITATIVE_WINDOW_GAPS.md`, 8193 bytes, SHA-256 `c66d6b4bd17ec313e0df0989f0bdc7aee6db46007fde953569aa61e9e771e29b`.

The submitted earlier version cited the superseded provisional three-point rerooting file as an accepted input. At review, the author replaced it with the independently accepted one-point proof and sharpened the prefactor to A_eta lambda(n+1)^(K+1). The final version also clarifies that zero-padding a fixed vector leaves its score unchanged, whereas enlarging the allowed positive dimension lowers the minimax value. These corrections are incorporated in the pinned version.

The exact recurrence, all-size count, fixed-K growth gap and exponential-in-K comparison bounds are valid. They are a lower certificate for the true gap, not an equality with that gap and not an upper bound on it.

## 1. Branches, monotonicity and the minimax identity

For p>0, R_eta(p,q)=eta q-E(p,q) is continuous at q=0 with value zero, has derivative eta-log(1+p/q), and strictly positive second derivative p/[q(p+q)]. It first decreases and then increases to infinity. Thus the positive level d>0 has exactly one positive root, and its sublevel set is precisely the interval from zero to that root. The p=0 case is q<=d/eta.

Increasing p lowers R at every fixed positive q, so the positive root Q_eta(p,d) is nondecreasing in p. Homogeneity gives Q_eta(dp,d)=d Q_eta(p,1), for d>0. These are the correct directions for the induction; no unwanted decreasing branch is used.

For any normalized nonnegative vector, the first positive entry has zero predecessor and strictly positive local penalty. Hence its maximum d is positive. The induction x_j<=d y_j follows from the root comparison, including coordinates equal to zero. Summing yields d>=1/sum y_j. The positive normalized vector proportional to y makes every local penalty equal to that reciprocal sum. This proves the minimax identity exactly.

The derivative in q at the positive level-one root is strictly positive. Finite iteration of the implicit equation therefore gives continuity of each y_j and kappa_K in eta>0. This justifies taking eta up to gamma only after the fixed-K asymptotic step.

## 2. The count retains the exact rotation multiplicity

For a fixed complete cell-size vector, choose one maximizing positive penalty. It corresponds to a real nonempty cell: trailing zeros have penalty zero and cannot be selected. For the first cell use the absolute first-cell bound directly. For a later cell use the accepted marked-pair count

    (n+1) binom(p+q,p) F_(n+1)(q).

The removed incoming shuffle remains in the binomial factor. The uniform frontier bound and homogeneity of entropy then give A_eta lambda(n+1)lambda^n exp(-n kappa_K(eta)) for this vector. The fact that rotation does not preserve the full size vector causes no difficulty: it is an ambient upper count for that vector's source set, not a proposed law on its images.

At most (n+1)^K padded vectors are possible. The resulting finite inequality holds for every n,K. For fixed K the polynomial factor disappears after division by n, and continuity in eta yields g_K<=lambda exp(-kappa_K(gamma)). The argument does not need a ratio limit for a_n.

For varying K the same displayed finite inequality remains true, but its factor (n+1)^K cannot be ignored. Nor can lambda^n/a_n be assumed bounded. The note correctly makes no arbitrary growing-K probability claim.

## 3. Tangent bounds and their signs

The function H(t)=(1+t)log(1+t)-t log t increases from zero to infinity and is strictly concave. Its unique root H(t_eta)=eta satisfies t_eta<1/2 in the application eta<=gamma<=log2, so R=1/t_eta>2.

At a positive recurrence value, eta-H(y_(j-1)/y_j)>0, hence y_j>R y_(j-1). This gives the upper bound for kappa_K through a lower geometric bound on the y_j.

The tangent inequality has the correct orientation:

    E(p,q)<=d p+log(1+t_eta)q,
    eta q-E(p,q)>=c q-d p,

where d=log(1+1/t_eta) and c=t_eta d=eta-log(1+t_eta)>0. Evaluating at the level-one root yields y_j<=R y_(j-1)+1/c. Its iterated sum gives the lower bound for kappa_K, with denominator [R^(K+1)-(K+1)R+K]/(R-1)^2. The K=1 boundary agrees with y_1=1/eta and causes no exception.

The two bounds have the same exponential order in K at fixed eta. The separate geometric test vector also correctly gives kappa_K(eta)<=eta/(2^K-1). This is an upper bound on the capability of this particular certificate, not on log(lambda/g_K).

## Scope

The certificate is positive for each fixed K but summable in K. Neither this summability nor the geometric test vector proves that the true gap sequence is summable. Actual adaptive-window sufficiency remains a separate question. No finite enumeration or coefficient extrapolation is used to establish any radius or growth limit here.
