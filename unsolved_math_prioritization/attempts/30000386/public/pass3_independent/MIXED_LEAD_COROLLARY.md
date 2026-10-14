# Genuine coupling of short leads through fifteen and distant adaptive threats

Status: authored PASS3 partial theorem, submitted for independent audit. This remains a proper restriction of the original Time-Bomb game. No novelty claim.

Dependency: BOUNDED_TRACKING.md, SHA256 f3aaf3404d9dcadd917ad9c027e284cf54c79cf05c0bf173b19ba30d6430887d. The deterministic extraction uses the already accepted finite-horizon safety-game/compactness argument, with absolute time included in the state.

## 1. Exact admissible announcement class

Set

    E=161^2=25921,
    K=3,000,000,  A=200K=600,000,000,
    b(j)=1+floor(log_2 j),  ell_j=j b(j)^2,
    M_j=K ell_j,  L_j=200 M_j=A ell_j,
    S_1=1,  S_(j+1)=S_j+L_j.

For S_j<=n<S_(j+1), allow the Devil's round-n announcement (p_n,t_n) to be any of:

- Ineffective: t_n<=n.
- Short: 1<=t_n-n<=15.
- Long: t_n>=S_(j+2).

The Devil may mix these types in any adaptive order, choose arbitrary positions, and assign many bombs the same target time. Its only per-round restriction is the original one-announcement budget plus the displayed lead restriction.

**Theorem.** The Angel has a deterministic infinite winning strategy against every such Devil.

## 2. Independent reference path and online tracking

Put z_0=z_1=0. At the beginning of block j select D_j independently and uniformly from the integer square [-M_j,M_j]^2. The draw may be sampled just after the Angel has reached time S_j; it is used only for subsequent reference increments. On this block define

    z_(S_j+k)=z_(S_j)+(k/L_j) D_j,  0<=k<=L_j.

Thus the reference block has total displacement D_j, its endpoint is again integral, and each increment has Euclidean norm at most sqrt(2)/200<1/100. Reference motion is entirely independent of Devil announcements. Future block draws are not consulted before their blocks start.

Use the online controller of BOUNDED_TRACKING.md. It consults all short bombs, ignores long bombs, and has error ||a_t-z_t||_2<80 at every time. It never collides with a short bomb. Continue the hypothetical controlled path after a long collision, extending the Devil's rule by any legal nonanticipating rule. This continuation is only for probability bookkeeping; before the first collision it is exactly the randomized legal play. No argument conditions on having survived.

## 3. One long announcement

Fix a round n in block j. Condition on the observed history through the Angel move and on the Devil's round-n choice. If the announcement is long, p_n,t_n are fixed and t_n>=S_(j+2). The independent displacement D_(j+1) has not started and is still uniform. Its entire block has finished by t_n, so

    z_(t_n)=D_(j+1)+Z,

where Z is independent of D_(j+1) conditional on that history. This uses only the independent reference construction, not any independence property of tracking errors or future Devil actions.

If a_(t_n)=p_n, then ||z_(t_n)-p_n||_infinity<80. For every fixed Z, an interval of length 160 in each coordinate contains at most 161 possible integer coordinate values for D_(j+1). Hence

    P[a_(t_n)=p_n | the round-n history and choice]
       <= E/(2M_(j+1)+1)^2.                      (1)

The tracking error can depend on the fresh displacement, the entire later reference path, and later short bombs. None of that affects the pointwise implication used in (1). If the round-n announcement is not long, set its long-collision event to be empty.

## 4. Summation and deterministic extraction

There are L_j announcement rounds in block j. By the countable union bound, the probability of any long collision is at most

    Q = sum_j L_j E/(2M_(j+1)+1)^2
      < (50E/K) sum_j ell_j/ell_(j+1)^2
      <= (50E/K) sum_j 1/ell_j
      <= 100E/K
       = 25921/30000 <1.                         (2)

The second inequality uses monotonicity of ell_j. For the last summation bound, on 2^r<=j<2^(r+1) one has b(j)=r+1, and the group's sum of 1/[j b(j)^2] is at most 1/(r+1)^2. Summing these groups gives at most 2.

No short collision occurs, so the randomized online controller has probability greater than 4079/30000 of infinite survival against every admissible adaptive Devil.

If some finite horizon were losing, finite perfect-information backward induction would supply an admissible Devil strategy forcing a collision by that horizon against every realization of the randomized controller, contradicting the positive probability just proved. Every finite horizon is therefore winning. The accepted nested finite-action extraction then supplies one deterministic infinite online strategy. This is an online randomized-strategy argument followed by exact extraction; it is not an offline path selected after the schedule.

## 5. A more familiar sufficient long-lead bound

The exact long-lead threshold is

    g(n)=S_(j+2)-n  when S_j<=n<S_(j+1).

The same elementary dyadic calculation as the accepted logarithmic-delay theorem gives, for j>=2,

    n >= A j^2 b(j)^2/20,
    g(n) <= (9/2) A j b(j)^2
         < 21 sqrt(A) sqrt(n) [1+log_2 n].

For j=1, g(n)<=9A. Thus the simpler restriction that every effective announcement have either lead at most 15 or lead at least

    ceil(max(9A, 21 sqrt(A) sqrt(n) [1+log_2 n]))

also gives deterministic infinite survival. Here A=600,000,000. The constants are deliberately conservative and not optimized. The long threshold has order sqrt(n) log(n+1), while the theorem also permits arbitrary simultaneous short threats through lead fifteen.

## 6. Remaining gap

Announcements with intermediate leads can violate the two-layer budget m_n+b_n<=15 while also arriving too late for the fresh completed reference block. They are excluded by this corollary. No argument here handles them, removes the bound fifteen, or resolves the original unrestricted conjecture.
