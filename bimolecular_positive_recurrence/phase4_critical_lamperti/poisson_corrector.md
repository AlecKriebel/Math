# Exact Poisson corrector

For a finite irreducible stochastic matrix \(P_0\) and deterministic or
conditional macroreward \(r(i,j)\), define

\[
d_0(i)=\sum_jP_0(i,j)r(i,j),\qquad
b_0=\pi d_0.
\]

The normalized finite Poisson system is

\[
(I-P_0)h=d_0-b_0,\qquad h(i_*)=0.
\]

For

\[
Y=N+h(\phi)
\]

the leading corrected conditional mean is the state-independent value
\(b_0\).  If

\[
P_N=P_0+N^{-1}P_1+O(N^{-2}),
\]

then, in the critical case \(b_0=0\),

\[
a_i=\sum_j(P_1)_{ij}
      [r(i,j)+h(j)-h(i)]
\]

(with the analogous reward-expansion term when present), and

\[
v_i=\sum_j(P_0)_{ij}
      [r(i,j)+h(j)-h(i)]^2.
\]

Averaging with \(\pi\) gives \(a,v\) and \(\Xi=2a+v\).  The exact arithmetic
is implemented in `src/poisson_corrector.py` and
`src/corrected_variance.py`.

For the reaction-network classes in the theorem, the complete-credit
construction makes every recurrent limiting reward nonpositive.  Therefore
\(b_0=0\) forces every corrected increment to vanish and hence \(v=0\).
The code still implements the general formula so that this structural
collapse can be checked independently on calibration macrochains.
