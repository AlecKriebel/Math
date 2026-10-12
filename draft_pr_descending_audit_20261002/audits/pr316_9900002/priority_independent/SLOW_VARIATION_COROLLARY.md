# Slowly varying tails and the exact all-scale obstruction

Prepared independently in the PR316 historical-priority audit, 2026-10-04. This is a current checkable deduction from a classical premise, not evidence that an earlier author explicitly stated a solution to Thorisson Problem 1.2. The stronger conditional conclusion was independently falsification-tested by the fresh, history-free slow_tail_adversary; its report is preserved in that subdirectory.

## Setup and historical premise

Let X_1,X_2,... be independent copies of an almost surely finite strictly positive random variable. Put S_0=0, S_n=sum_{j=1}^n X_j, N(t)=inf{n>=1:S_n>t}, and D_t=X_{N(t)}, the full interval length covering t under intervals [S_{n-1},S_n). Let r(x)=P(X_1>x) and U(t)=sum_{n>=0}P(S_n<=t).

Assume r is eventually positive, slowly varying, tends to zero, and

\[
U(t)r(t)\longrightarrow1. \tag{P}
\]

The historical premise (P) follows from K. B. Erickson, *Strong renewal theorems with infinite mean*, Transactions AMS 151 (September 1970), 263–291, Theorem 5 at printed p.265 and equation (2.2) at p.266, including its explicit alpha=0 convention. In that source m(t)=integral_0^t r(s)ds, r(t)=t^{-alpha}L(t), and

\[
U(t)\sim[\Gamma(\alpha+1)\Gamma(2-\alpha)]^{-1}t/m(t).
\]

At alpha=0, equation (2.2) says U(t)~1/L(t)=1/r(t). Source identity: DOI https://doi.org/10.1090/S0002-9947-1970-0268976-9 . Official AMS endpoints returned403/internal access errors. The preserved original article scan came from a public mirror, not a primary hosting institution; its title page, copyright, printed page numbers and Theorem5/equation(2.2) were visually inspected. This provenance limitation remains explicit. The general all-scale statement below is our deduction, not a quotation from that article.

The explicit continuous example later in this note establishes (P) by an independent elementary proof, so its negative answer does not depend on trusting the mirrored theorem.

## Well-definedness and exact total-life tail

Strict positivity implies S_n->infinity almost surely: some epsilon>0 has P(X>=epsilon)>0, and independence gives infinitely many such increments. For any lambda>0, q=E exp(-lambda X)<1 and

\[
U(t)\le e^{\lambda t}\sum_{n\ge0}q^n<\infty.
\]

For every x>=t>=0,

\[
\boxed{\ P(D_t>x)=r(x)U(t).\ } \tag{1}
\]

To prove this, decompose by the covering interval. The events
{S_n<=t<S_n+X_{n+1}, X_{n+1}>x}
are disjoint. Since x>=t, the last inequality and S_n>=0 already imply S_n+X_{n+1}>t. Independence therefore turns the sum into sum_n P(S_n<=t)P(X_{n+1}>x). This includes x=t, possible atoms in the increment law, and renewal epochs exactly at t. It is not an identity for residual life alone.

By (P), (1), and slow variation, for each fixed K>=1,

\[
P(D_t>Kt)=U(t)r(t)\,\frac{r(Kt)}{r(t)}\longrightarrow1.
\]

Monotonicity extends escape to all positive K. Thus D_t/t->infinity in probability.

## Every asymptotically tight positive scale converges to zero

Let phi(t) be any deterministic finite positive value at every sufficiently large t. No monotonicity or regularity in t is required. Suppose Y_t=D_t/phi(t) is asymptotically tight.

If phi(t)/t did not tend to infinity, there would be t_j->infinity and finite C>0 with phi(t_j)<=Ct_j. For every fixed M>0,

\[
P(Y_{t_j}>M)\ge P(D_{t_j}>MCt_j)\longrightarrow1,
\]

contradicting tightness. Therefore phi(t)/t->infinity, and phi(t)->infinity.

For fixed a,b>0, both a phi(t) and b phi(t) eventually exceed t. Write p_t(a)=P(Y_t>a). Equation (1) and slow variation give

\[
|p_t(a)-p_t(b)|
\le p_t(b)\left|\frac{r(a\phi(t))}{r(b\phi(t))}-1\right|
\longrightarrow0. \tag{2}
\]

Given eta>0, tightness supplies a fixed b with limsup p_t(b)<=eta. For each a>0, (2) gives limsup p_t(a)<=eta. Since eta is arbitrary, Y_t->0 in probability.

A proper finite weak limit implies asymptotic tightness. Consequently every proper finite weak limit of D_t/phi(t) is delta_0; no nondegenerate limit is possible. This covers positive constants, finite mixed laws with an atom at zero, and arbitrarily oscillating scales. Survival at zero is never compared, since zero need not be a continuity point of the limit.

A sharp equivalent criterion is

\[
D_t/\phi(t)\text{ is asymptotically tight}
\quad\Longleftrightarrow\quad
D_t/\phi(t)\to0\text{ in probability}
\quad\Longleftrightarrow\quad
r(\phi(t))/r(t)\to0.
\]

For the final reverse implication, r(phi(t))/r(t)->0 forces phi(t)/t->infinity: any bounded subsequence would contradict monotonicity and r(Ct)/r(t)->1. Then (1) and slow variation apply to every positive threshold. This criterion is stronger than required for the exact source problem.

## Explicit admissible continuous law, with an elementary proof of (P)

Take

\[
r(x)=
\begin{cases}
1,&0\le x<1,\\
(1+\log x)^{-1},&x\ge1.
\end{cases}
\]

This is the continuous survival of a probability density f(x)=1/[x(1+log x)^2] on x>1. Integrating with u=log x gives total mass one. The law is strictly positive, finite almost surely, and non-lattice because it has a density. Its mean is infinite, since integral_1^infinity r(x)dx = integral_0^infinity e^u/(1+u)du = infinity. It is slowly varying by direct substitution.

For t>1, define J_t=inf{k>=1:X_k>t}, L_t=sum_{j<J_t}X_j, and M(t)=E[X1_{X<=t}]. A geometric-series calculation gives

\[
E L_t=\frac{M(t)}{r(t)}.
\]

Here M(t)=integral_1^t [1+log x]^{-2}dx. Splitting at sqrt(t) gives

\[
M(t)\le\sqrt t+\frac{t}{(1+\tfrac12\log t)^2},
\qquad
\frac{M(t)}{t\,r(t)}\longrightarrow0. \tag{3}
\]

On {L_t<=t}, the first increment exceeding t is precisely the interval covering t, so D_t>t. Markov's inequality, (1), and (3) yield

\[
1-\frac{M(t)}{t r(t)}
\le P(L_t\le t)
\le P(D_t>t)=U(t)r(t)\le1.
\]

Hence (P) holds for this law without a renewal asymptotic theorem. The preceding all-scale argument supplies a fully elementary counterexample satisfying Thorisson's source assumptions.

The suggested m(t)=E[min(X,t)] satisfies m(t)/t->0 by bounded convergence, because min(X,t)/t->0 almost surely and is at most1. Since D_t/t->infinity, D_t/m(t)->infinity in probability along the full t limit. Thus the same simple law rejects both questions.

Properness is essential. For phi(t)=t^c, c>1, (1) gives P(D_t/phi(t)>a)->1/c for every a>0; this is not tight on the real line. On the compactified half-line the limiting law is (1-1/c)delta_0+(1/c)delta_infinity. For phi(t)=exp((log t)^2), the normalized total life tends to0, a permitted degenerate limit.

## Historical and candidate boundary

This proof shows the exact negative existence claim is an elementary consequence of a classical index-zero renewal asymptotic, and even admits the independent elementary example above. It does not demonstrate when someone first drew or published the all-scale inference or explicitly answered Thorisson's later Problem1.2.

The submitted lacunary mixture is outside regular variation. With p_n=2^{-2^n}, a_n=2^{4^n}, and r the mixture's survival,

\[
r(a_n/2)=q_n,\quad r(a_n)=q_{n+1},\quad
r(a_n)/r(a_n/2)\longrightarrow0,
\]

because q_n~p_n and q_{n+1}~p_n^2. No finite regular-variation index has this doubling ratio. Its one-atom dominance at selected times, P(D_{a_n/2}=a_n)->1, is a distinct mechanism. That construction may have mathematical or expository value even though the universal negative answer has this classical route. Priority of the precise construction remains unverified.

