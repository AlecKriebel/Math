# The move-then-hold tracking bridge cannot close the full game

Status: a precise impossibility result for one reference/correction/certificate architecture. It is not a Devil-winning strategy against unrestricted Angels. In particular, the conclusions do not apply to controllers that are free to leave the stated tracking envelope, to a different reference process, or to a different probability accounting method.

## 1. Reference and finite-block attack

Use the accepted reference from the hidden-block construction. In a block [S,T] of length L=T−S, draw D uniformly from [−L,L]². In each coordinate, move by its sign during the first |D_coordinate| steps and then stay. Its endpoint displacement is D.

Let R be a fixed nonnegative integer, and put M=(4R+1)². Assume M≤L. At round u=T−M, after observing the actual Angel position Y_u, the Devil fixes the square

Y_u+[−2R,2R]².

It has exactly M lattice points. In rounds u,u+1,...,T−1, announce these M points, one per round, all with detonation time T. This is a legal adaptive schedule; the first target is chosen only after the observed position Y_u, and every announcement is made strictly before T. Its individual leads lie between one and M.

Consider the reference pause event

P={||D||_infinity≤L−M}.

On P, both coordinate motions have finished by u, so X_u=X_T. If the actual path is within R of the reference at both u and T, then

||Y_T−Y_u||_infinity≤2R.

Every such endpoint Y_T is bombed. Therefore, on P, the Angel either dies by T or violates radius-R tracking at one of the two observed endpoints. No assumption about the controller's correction algorithm or its independence is needed for this geometric implication.

The pause event has exact probability

p(L,R)=[2(L−M)+1]²/(2L+1)².

Thus the probability of both survival and radius-R tracking at these two times is at most 1−p(L,R). If R²=o(L), then M/L tends to zero and p(L,R) tends to one.

## 2. Repeated blocks and arbitrary deterministic radius profiles

Now use independent reference draws in blocks j, with L_j tending to infinity. Let r(t) be any deterministic nonnegative integer envelope, and put

R_j=max{r(t): S_j≤t≤S_(j+1)}.

Whenever M_j=(4R_j+1)²≤L_j, execute the preceding attack during the last M_j rounds of that block, targeting T_j=S_(j+1). In all other rounds make ineffective current-time announcements. Attack intervals of distinct blocks are disjoint, so the one-announcement-per-round budget is obeyed globally.

Every attack announcement is short in the precise sense of the transfer criterion: its announcement lies in block j and its target S_(j+1) is strictly before S_(j+2).

Let P_j be the pause event for attacked block j, with probability p_j=p(L_j,R_j). These events depend only on independent D_j and are therefore mutually independent, despite the adaptive spatial centers of the attacks.

If Y both survives and satisfies the envelope for all times, none of the P_j can occur. Hence

P[global survival and tracking]≤product_(attacked j)(1−p_j).

In particular, this probability is zero whenever sum_(attacked j)p_j diverges. If for some fixed eta<1 there are infinitely many blocks with M_j≤eta L_j, then p_j≥(1−eta)² on those blocks and the sum diverges.

It follows that a positive-probability global event of short-threat avoidance and tracking against every Devil requires

liminf_(j→infinity) R_j/sqrt(L_j)≥1/4.

Indeed, if the liminf were smaller, infinitely many R_j would be at most c sqrt(L_j) for some c<1/4. On those blocks,

M_j/L_j≤16c²+8c/sqrt(L_j)+1/L_j,

which is eventually at most a fixed eta<1. The repeated attack would then make the desired event have probability zero.

This necessary condition is for a deterministic radius envelope around this particular reference. It is not a lower bound on the displacement of every full-game winning Angel.

## 3. The geometric repair union series then diverges

Assume additionally that consecutive block lengths are asymptotically comparable:

L_(j+1)/L_j tends to 1.

Both accepted schedules, L_j=3j²+3j+1 and L_j=j(1+floor(log₂j))², have this property. For the logarithmic schedule, the only extra length jumps multiply by ((b+1)/b)² with b tending to infinity, so their ratios also tend to one.

Suppose the good-event hypotheses of COUPLING_TRANSFER.md hold for this reference with epsilon<1. The repeated short-only attack above forces liminf R_j/sqrt(L_j)≥1/4. In particular, for all sufficiently large j,

R_j≥sqrt(L_j)/8.

Choose a time t_j in the closed block [S_j,S_(j+1)] at which r(t_j)=R_j. For every announcement round n in block j−2, this target time is long, since t_j≥S_j=S_((j−2)+2). The completed fresh reference blocks between n and t_j are among j−1 and j, so

L*(n,t_j)≤max(L_(j−1),L_j)≤2L_j

for sufficiently large j. The geometric repair bound used in the transfer criterion consequently satisfies

q_n≥min{1,(2R_j+1)²/(2L*(n,t_j)+1)²}

≥1/(400L_j).

For the last inequality, use (2R_j+1)²≥4R_j²≥L_j/16 and (2L*+1)²≤(4L_j+1)²≤25L_j². The lower bound remains valid if the expression inside the minimum exceeds one.

There are L_(j−2) announcement rounds in block j−2. Their aggregate contribution to the series is at least L_(j−2)/(400L_j), which is eventually at least 1/800. Distinct values of j correspond to distinct announcement blocks. Thus

sum_(n≥1)q_n=infinity.

Choosing a tighter error only at block endpoints does not evade this argument: the worst-case target can be the interior time t_j where the envelope reaches its block maximum.

## 4. Exact conclusion

For the accepted move-then-hold reference and either accepted block schedule, no deterministic tracking envelope can make the sufficient conditions of COUPLING_TRANSFER.md hold:

- If its maxima are too small on infinitely many blocks, a legal short-lead attack destroys every positive-probability global short-safe tracking event.
- If the good event can retain positive probability against all such attacks, the generic geometric repair-factor union series diverges.

Divergence of this upper-bound accounting is not an actual loss theorem for the corrected path. A controller could exploit correlations between targets and corrections that this worst-case summation discards. Other references, local resetting schemes, nonuniform event charges, or genuinely history-sensitive block strategies are not excluded.
