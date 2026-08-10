# Mandatory counterexamples for the physical-time repair

These examples invalidate tempting recurrence interfaces. They are not
counterexamples to T3-2.

## 1. Strict shellwise drift can still be null recurrent

On \(\mathbb N_0\), let \(P(0,1)=1\) and, for \(n\ge1\),

\[
 P(n,n+1)=\frac{n}{2n+1},\qquad
 P(n,n-1)=\frac{n+1}{2n+1}.
\]

The drift is strictly negative at every positive state:

\[
 \mathbb E[X_{k+1}-X_k\mid X_k=n]=-
 \frac{1}{2n+1}.
\]

An unnormalised reversible measure is

\[
 m_0=1,\qquad
 m_n=\frac{2n+1}{n(n+1)}=\frac1n+\frac1{n+1},\quad n\ge1.
\]

Its mass diverges. The edge resistance
\(1/(m_nP(n,n+1))=n+1\) also has divergent sum, so the chain is recurrent
but not positive recurrent. Hence \(\mathbb E_1T_0=\infty\). A pointwise
inequality \(p_n>a_n\) on every shell does not replace an excursion-wide
uniform margin or a valid variable-drift cost theorem.

## 2. Naive lexicographic descent can hide infinite lower-level cost

Use CTMC states \(s_k=(1,k)\), \(t_k=(0,k)\), \(k\ge1\), and \(t_0\). From
\(s_k\), jump to \(s_{k+1}\) at rate \(k\) and to \(t_k\) at rate one. From
\(t_k\), jump to \(t_{k-1}\) at rate one, and let \(t_0\to s_1\) have rate
one.

The switch time from every \(s_k\) has finite mean and strictly lowers the
first lexicographic component. One jump from every \(t_k\) lowers the second.
Starting from \(s_n\), however, the switch level \(M\) satisfies

\[
 \mathbb P_n(M=m)=\frac{n}{m(m+1)},\qquad
 \mathbb P_n(M\ge m)=\frac{n}{m},\qquad m\ge n.
\]

The expected switch duration is

\[
 \sum_{m=n}^{\infty}\frac{n}{m}\frac1{m+1}=1,
\]

but \(\mathbb E_nM=\infty\). The subsequent unit-rate drain from \(t_M\) to
\(t_0\) therefore has infinite mean. Finite joint shells and bounded jumps do
not imply positive recurrence without integrability of every lower-level seam
and reset cost.

## 3. Tight environment with infinite support

The weakly reversible immigration-death network

\[
 0\rightleftarrows E
\]

has a Poisson stationary distribution with parameter equal to the birth-rate
to death-rate ratio. The law is tight, but every value \(E=n\) has positive
stationary probability. No one fixed finite phase can record the exact
environment. A repaired proof must include \(E\) in a proper workload, prove a
uniform truncation error, or use a genuine countable-environment theorem.

## 4. Fast neutral jumps are not physical-time cost

Consider the three-species, two-linkage weakly reversible CRN

\[
 A\rightleftarrows B,
 \qquad
 0\rightleftarrows C.
\]

Give both fast reactions rate constant \(R>0\), give \(0\to C\) rate
\(\lambda>0\), start with \(A+B=N,C=0\), and stop at the first \(0\to C\)
reaction. Before stopping, the aggregate fast propensity is exactly \(RN\),
while the trace hazard is exactly \(\lambda\). Thus

\[
 \mathbb E\tau=\frac1\lambda,
 \qquad
 \mathbb EJ=\frac{RN}{\lambda},
\]

where \(J\) is the number of neutral \(A\rightleftarrows B\) reactions before
\(\tau\). The physical mean is independent of \(N\), while the embedded cost
is arbitrarily large. A physical-time trace must skip these jumps rather than
charge them as elapsed time.

## 5. Signed service is not proper-workload descent

In the exceptional atlas architecture

\[
 \{C,2C\}\quad\&\quad\{0,A,2A,B+C\},
\]

the certified signed quantity \(W=B-C\) falls when \(C\to2C\). Every positive
scalar workload rises on that reaction. Consequently, the signed service
certificate does not by itself satisfy proper-workload descent. A combined
episode or a globally proper seam-compatible Lyapunov function is still
required.
