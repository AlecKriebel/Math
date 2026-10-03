# Attempt 1: finite observation filtrations

All results here are finite-horizon statements, not a proposed canonical solution of Aldous's unrestricted question. Fix an integer n >= 1, an integrable real process X_0,...,X_n adapted to F, and a specified subfiltration G_t contained in F_t. Each G_t has a finite partition A_t of atoms (null atoms may be retained). Write m_t=|A_t|.

For t<n and A in A_t define the G-stopping time

T(t,A) = t+1 on A, and t otherwise.

Let L contain these sum_{t<n} m_t times and the n-1 deterministic times 1,...,n-1. The deterministic time 0 is implicit. Duplicate times may be removed.

## Theorem 1: a finite stopping certificate

The following are equivalent:

1. E X_T = E X_0 for every T in L.
2. q(t,A):=E[1_A(X_{t+1}-X_t)]=0 for every t<n and A in A_t.
3. Y_t:=E[X_t|G_t] is a G-martingale.
4. E X_T = E X_0 for every G-stopping time T taking values in {0,...,n}.

Proof. Put b_t=E X_t-E X_0. Directly,

E X_{T(t,A)}-E X_0 = b_t+q(t,A).                 (1)

The deterministic tests set b_t=0 for 1<=t<n, and b_0=0 automatically, so 1 implies 2. Conversely 2 implies E(X_{t+1}-X_t)=sum_A q(t,A)=0, hence all b_t=0 and (1) proves 1. Conditional expectation onto G_t is zero exactly when its integrals over the finitely many atoms are zero. The tower property therefore identifies 2 with E[Y_{t+1}|G_t]=Y_t, proving 2 iff 3, including null atoms.

For any G-stopping T the event {T>t} belongs to G_t and

X_T-X_0 = sum_{t=0}^{n-1} 1_{T>t}(X_{t+1}-X_t). (2)

Taking expectations proves 2 implies 4, because each survival event is a union of atoms. Finally L consists of G-stopping times, so 4 implies 1. This proof does not require X_t to be G_t-measurable. Equivalently E X_T=E Y_T follows by conditioning separately on {T=t}. QED.

## Quantitative version and witness

Define V_G(X)=sum_{t,A}|q(t,A)|. Equation (2) gives

sup_{T G-stopping} |E X_T-E X_0| <= V_G(X).       (3)

Indeed a survival event selects some atoms at each time. A slightly sharper bound is max(sum q_+,sum q_-), where the sums are over all time-atom pairs; no assertion that every such selection is a stopping policy is needed.

If an atom has q(t,A) != 0, at least one of deterministic t and T(t,A) has nonzero expectation deviation, by (1). More quantitatively their maximum absolute deviation is at least |q(t,A)|/2. The t=0 candidate has zero deviation but the other then has magnitude |q|. Once the rational moments are available, this is a constructive certificate.

## Tractability and its exact scope

If N=sum_{t<n}m_t is polynomial in n, the displayed stopping library is polynomial-size. Given an explicit finite probability table and explicit rational path values and partition memberships, all its moments and witnesses are computed in polynomial time in the total table bit length. Given the moment list itself, only polynomially many rational operations are needed. For a fixed finite outcome space, values, and partitions, the tests are linear equalities in the outcome probabilities; their intersection with the probability simplex is a rational polytope.

This is not a claim of polynomial time in n when the supplied table has exponentially many rows. An arbitrary succinct sampler does not supply exact expectations for free. A polynomial number of constraints is not itself a polynomial-time membership algorithm.

The observation restriction is essential. Let B be a fair sign and X=(0,B,2B). For the trivial G_t all mean constraints hold. The natural filtration of X knows B at time 1, and T=2 on {B=1}, T=1 otherwise has E X_T=1/2. Thus a coarse observer can regard a process as fair while an observer of the actual price finds a simple advantage. Requiring G to include all observed prices may itself destroy the small-atom bound.

## Outcome

A fully proved polynomial stopping-certificate class exists relative to a prescribed polynomial-size nested observation structure and explicit moment access. This does not identify which observations or information/computation model should be called practical in the source problem. The unresolved part motivates Attempt 2.
