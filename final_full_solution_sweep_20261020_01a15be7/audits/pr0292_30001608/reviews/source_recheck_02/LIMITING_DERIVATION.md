# Distinct stochastic boundary challenge

This note was developed independently of the candidate checker. It is a local limiting calculation, with a finite-horizon justification, and is not a second proof of positive recurrence.

Put alpha=lambda/2. Start the exact permanent-seed chain at

    (A,B,X,Y) = (floor(rho R), b, n, R),

where rho>=0, b,n are fixed and R tends to infinity. For any fixed finite time horizon, center A and Y at their initial values. The locally limiting generator has these events:

| event | rate |
|---|---|
| centered A increases by 1 | alpha |
| B increases by 1 | alpha |
| centered A decreases by 1 and X increases by 1 | rho(X+1) |
| B decreases by 1 and centered Y increases by 1 | B |
| X decreases by 1 | X |
| centered Y decreases by 1 | X+1 |

The limiting X and B are independent. X is a linear birth/death process with immigration rho; B is immigration/death with immigration alpha and individual death rate 1. The permanent seed contributes both the immigration term rho in X and the baseline departure rate 1 in Y. Deleting the seed changes the limiting mechanism.

## Finite-horizon justification

Here is a compact-containment and moment argument rather than a stationary substitution. Let P_A,P_B be the external arrival counts, and stop when Y<R/2 or P_A>R. Before that stopping time,

    A <= floor(rho R)+P_A <= (rho+1)R,
    r_A = A(X+1)/(X+Y+1) <= 2(rho+1)(X+1).

Thus X and its birth count are bounded by a linear pure-birth process U with births 2(rho+1)(U+1). For fixed time T, U_T and its counting process have moments of every order. B and the number of B-to-Y transitions are bounded by b+P_B(T). The Y departure intensity is always at most X+1, so its stopped count is bounded by a counting process with integrated intensity at most the integral of U+1. This count also has moments of every fixed order on [0,T].

Reaching Y<R/2 requires at least order R departures, while reaching P_A>R requires order R external arrivals. Markov bounds of arbitrarily high order therefore give

    P(stop <= T) <= C(k,T,rho,b,n) R^(-k)

for each fixed k. The constants are independent of R, but are allowed to depend on the fixed parameters and horizon. Off this event the centered coordinates and jump counts have the preceding R-independent bounds. On the event, the global pathwise bounds

    X <= n+floor(rho R)+P_A,
    -floor(rho R) <= A-floor(rho R) <= P_A,
    -R <= Y-R <= b+P_B,
    B <= b+P_B

and sufficiently high-order stopping estimates give uniform integrability of every fixed moment. Stopped rates converge uniformly on every finite set of centered states to the displayed generator. The limiting chain is nonexplosive by its linear rates. Standard finite-state localization, followed by these compact-containment bounds, identifies the finite-horizon process limit and allows passage of the first moments. This argument does not interchange the infinite-time and R limits.

## Exact limiting first moments

Let k=rho-1 and M(t)=E X(t). Then

    M'(t)=rho+(rho-1)M(t),   M(0)=n,
    E B(t)=alpha+(b-alpha)e^(-t).

For rho=1, M(t)=n+t. For rho!=1,

    M(t)=n e^(kt)+rho(e^(kt)-1)/k.

The limiting centered Y mean is

    E[Y(t)-R] = alpha t+(b-alpha)(1-e^(-t))
                - t - integral_0^t M(s) ds.

Since both X and Y departures remove one peer, while first downloads only transfer peers between classes,

    E[N(t)-N(0)] = (lambda-1)t - 2 integral_0^t M(s) ds,
    N=A+B+X+Y.

At rho=1 this specializes to

    E[A(t)-R]=(alpha-n-1)t-t^2/2,
    E[Y(t)-R]=(alpha-n-1)t-t^2/2+(b-alpha)(1-e^(-t)),
    E[N(t)-N(0)]=(lambda-2n-1)t-t^2.

For rho=1 the generator also gives

    Var X(t)=(2n+1)t+t^2,
    Cov(X(s),X(t))=Var X(s),  0<=s<=t.

Conditional on X, the Y departure count is Poisson with integrated intensity integral(X+1), and is independent of the B departure count. With p=1-e^(-t),

    Var[Y(t)-R] = b p(1-p)+alpha(t-p)
                 +(n+1)t+t^2/2+(2n+1)t^3/3+t^4/6.

These formulas predict the mean and variance of the retained, reproducible finite-horizon Monte Carlo diagnostic at initial (10^6,5,0,10^6), lambda=10. It observes mean Y increments 3.4874 at t=1 (predicted 3.5, estimated standard error 0.0320) and -10.9484 at t=10 (predicted -10, estimated standard error 0.6650). This is a numerical check of the finite-horizon calculation, with no equilibrium or recurrence inference.

## Falsification of the population-drift shortcut

At rho=0,n=0, limiting X remains zero and A is pure immigration. Therefore

    E[N(t)-N(0)] = (lambda-1)t

for every fixed finite t. For lambda>1 it is strictly positive, however large that fixed t is. The exact finite-R initial generator value at (0,b,0,R) is lambda-R/(R+1), consistent with this limit. Consequently no fixed physical-time skeleton of unweighted total population can have negative expected drift uniformly outside a finite set at lambda>1. This refutes that proposed shortcut, not positive recurrence of the chain.

Even with rho=1/2,n=0, M(t)=1-e^(-t/2)<=1, so lambda=10 gives E delta N>=7t>0 on every fixed horizon. The obstruction is not confined to an exactly empty waiting room. The restored balance in the rho=1 calculation cannot be extended uniformly to all ratios by using the same raw population function.

The full candidate's global V includes a workload and cohort-imbalance correction as well as a finite birth/death corrector. It can decrease while N grows. Its pointwise Foster argument therefore survives these boundary challenges. The local limiting route remains blocked as a global recurrence proof: closing it would require a new function or a state-dependent horizon with uniformly controlled costs, which would carry the central difficulty rather than resolve it.
