# Substantive turn 1: exact harmonic martingales and reduction to existence

2026-10-01 06:19–06:23 UTC. Model: **unit initial edge counts**, rate-one independent vertex clocks, alpha=1 on Z, with e_i=(i,i+1). Unreviewed partial theorem; the convergence conjecture remains unresolved. Completion estimate: 20%. The source's initial-condition omission is retained in SOURCE_SCOPE.md.

Write N_i(t) for the counts, S_i=N_i+N_{i+1}, and

    h(n)=sum_{r=1}^{n-1} 1/r,    h(1)=0.

The instantaneous birth rate of N_i is

    lambda_i=N_i/S_{i-1}+N_i/S_i.

## Exact martingale and growth bounds

**Lemma.** For every i,

    M_i(t)=h(N_i(t))- integral_0^t (1/S_{i-1}(s)+1/S_i(s)) ds

is an L^2-bounded martingale. It converges almost surely and in L^2 to a finite limit. Moreover almost surely, simultaneously for every i,

    liminf log N_i(t)/log t >= 2/3,
    limsup N_i(t)/t <= 2.

Proof. Each increment of N_i from n to n+1 changes h by 1/n. Compensating that jump process gives the displayed drift exactly. Its actual squared jumps sum to at most sum_{n>=1}1/n^2. Consequently the expectation of its predictable quadratic variation, and hence its second moment, is uniformly bounded by pi^2/6. The martingale convergence theorem applies. This does not assume linear growth or convergence of N_i/t.

Let P_j(t) count clock rings at vertex j. Pathwise N_i<=1+P_i+P_{i+1}, hence the Poisson strong law gives limsup N_i/t<=2. Also

    S_i(t)<=2+P_i(t)+P_{i+1}(t)+P_{i+2}(t),

because each ring in those three vertices contributes at most one count to the two-edge sum. Thus limsup S_i/t<=3. For every epsilon>0, both reciprocal terms in the harmonic drift are eventually at least 1/((3+epsilon)t). Boundedness of the convergent M_i and h(n)=log n+O(1) give liminf log N_i/log t>=2/(3+epsilon). Let epsilon decrease to zero. Countable intersections make the assertions simultaneous over all edges. No nonadapted stopping-time coupling is used.

In particular every edge grows to infinity at a polynomial rate. This does **not** imply that N_i/t stays away from zero.

## Every existing pointwise limit has alternating form, including possible zeros

Suppose on a sample path all limits x_i=lim N_i(t)/t exist. They are in [0,2]. We first show that adjacent limiting zeros are impossible. If x_i=x_{i+1}=0 then S_i(t)/t->0. For every A>0 eventually 1/S_i(t)>=A/t. The harmonic martingale formula would force liminf h(N_i(t))/log t>=A, contradicting N_i(t)<=O(t). Thus every adjacent sum x_i+x_{i+1} is positive.

If x_i>0, then h(N_i(t))/log t->1. The harmonic drift and logarithmic Cesaro averaging yield

    1/(x_{i-1}+x_i) + 1/(x_i+x_{i+1}) = 1.       (*)

If x_i=0, the same drift gives a logarithmic growth exponent

    lim log N_i(t)/log t = 1/x_{i-1}+1/x_{i+1}.

The upper bound by one, together with 0<x_{i-1},x_{i+1}<=2, forces x_{i-1}=x_{i+1}=2. Equation (*) at either neighboring edge then forces the next edge to be zero. A zero therefore propagates an alternating (0,2) pattern through the whole line.

If all x_i are positive, put a_i=1/(x_i+x_{i+1}). Equation (*) says a_{i-1}+a_i=1, so a_i and the neighboring sums are two-periodic. Hence for each parity x_{i+2}-x_i is a constant increment. Boundedness along the two-sided infinite line forces that increment to vanish. All neighboring sums equal two, and x_i alternates between a and 2-a for some a in (0,2).

Combining the two cases, **any existing full pointwise limit has the form (a,2-a,a,2-a,...) with a in [0,2]**. No separate strict-positivity assumption on the limit is needed.

## Unit-initialized conditional homogenization

**Theorem.** If the unit-initialized critical WARM has almost-sure pointwise limits on all edges, those limits are almost surely all one.

The usual bounded-degree graphical construction is a translation-covariant measurable function of the iid family of marked rate-one vertex Poisson processes. This iid family is ergodic under translation by two. In the alternating limit just established, x_0 is invariant under that translation, so it is almost surely a deterministic constant a. Translation invariance of the unit-initialized law also identifies the distribution of x_0 and x_1, giving a=2-a, hence a=1. This uses an actual almost-sure limit, not a weak subsequential limit: ergodicity need not survive passage to a weak limit of laws.

The event that all pointwise limits exist is itself translation-invariant, hence has probability zero or one. The theorem does not establish that its probability is one. Proving existence of the limits is the remaining central difficulty.

## Exact gap and next mechanisms

The harmonic martingales eliminate one possible ambiguity: no random alternating limiting phase can survive in an actual unit-initialized limit, and boundary zero limits cause no extra family. But they do not prove convergence, a uniform positive linear rate, or the interchange of spatial and temporal limits. The finite-cycle result cannot be transferred by interchanging infinite volume with infinite time without a bound. Next routes should attack the missing temporal convergence, for example through the staggered monotone coupling, local dissipation, or a controlled finite-volume approximation. These are routes to test, not established conclusions.
