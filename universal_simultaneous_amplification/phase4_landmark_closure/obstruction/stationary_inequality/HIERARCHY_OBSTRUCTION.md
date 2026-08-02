# Why the singleton and first-moment balances do not prove (62)

Date: 2026-08-02 (America/Los_Angeles)

Status: **EXACTLY COMPUTED DIAGNOSTIC.**  This note does not disprove the
stationary inequality (62).  It proves that the currently available
singleton equations and stationary size balance are logically insufficient
to prove it: an exchangeable probability law can satisfy all of those
equations exactly while violating (62).

Take the dB geometric-union dual at `r=3/2` and use the transition matrix of
the unit-weight complete graph `K_7`, so `P_ij=1/6` for `i != j`.  Consider
the following *putative* exchangeable law on nonempty subsets.  Its total
mass on levels 1, 2, and 3 is

\[
 p_1=\frac{12}{67},\qquad
 p_2=\frac{15}{67},\qquad
 p_3=\frac{40}{67},
\]

and every other level has mass zero.  Within a level the mass is uniform.
This is a probability law, but it is not claimed to be stationary for the
full dual chain.

For `r=3/2`, put

\[
 \ell(x)=\frac{x}{r-(r-1)x}.
\]

Here `ell(1/6)=2/17`.  If `q_i` and `q_ij` denote the exact singleton and
doubleton masses of the putative law, then

\[
 q_i=\frac{p_1}{7}=\frac{12}{469},\qquad
 q_{ij}=\frac{p_2}{\binom72}=\frac5{469}.
\]

Consequently every exact stationary singleton equation holds:

\[
 q_i
 =\sum_{j\ne i}\ell(P_{ji})(q_j+q_{ij})
 =6\frac2{17}\frac{17}{469}
 =\frac{12}{469}.
\]

The exact dB stationary size balance can be written

\[
 E\{C(A)+(r-1)R_2(A)\}
 =\left(1-\frac1r\right)E|A|.
\]

On a `k`-set of `K_7`, its left-hand integrand is

\[
 T_k
 =\frac{k(k-1)}6+\frac{k(7-k)}{78}.
\]

Thus `T_1=1/13`, `T_2=6/13`, and `T_3=15/13`.  Direct substitution gives

\[
 ET=\frac{54}{67}
 =\frac13 E|A|,
 \qquad E|A|=\frac{162}{67}.
\]

Hence the normalization, every singleton equation, and the first-moment
stationarity equation all hold exactly.

Nevertheless the normalized margin in (62) is negative.  Because `K_7` is
regular, the inverse-degree weighted singleton term divided by `H` is
`p_1/7`, and therefore

\[
 \frac1{r^2H}\sum_i\frac{q_i}{d_i}
 -\left\{\frac{E|A|}{7}-\frac13\right\}
 =\frac{p_1}{7r^2}
  -\left\{\frac{E|A|}{7}-\frac13\right\}
 =-\frac1{1407}.
\]

So a proof of (62) must use a genuinely higher-order stationarity constraint
(at least information not implied by the singleton equations and the size
balance).  In particular, pairing the two orientations in the exact
singleton equation and then substituting the exact first-moment balance
cannot close the argument by itself.

The companion verifier performs every calculation with `Fraction`
arithmetic.

## The second factorial-moment equation is still insufficient

For a state `A` of size `k`, let

\[
 b_v=\sum_{u\notin A}h_r(P_{vu})
\]

and

\[
 s_v=\sum_{\{u,z\}\subseteq V\setminus A}
 \{h_r(P_{vu})+h_r(P_{vz})-h_r(P_{vu}+P_{vz})\}.
\]

If `J_v` is the number of distinct outside vertices in the geometric burst
at `v`, then `b_v=EJ_v` and `s_v=E binom(J_v,2)`.  Since the new size is
`k-1+J_v`, direct use of Vandermonde's identity gives the exact generator
formula

\[
 \mathcal L\binom{k}{2}
 =\sum_{v\in A}\{(k-1)(b_v-1)+s_v\}.
\tag{1}
\]

The preceding `K_7` law does not satisfy (1).  Adding (1), however, still
does not close the hierarchy.  On `K_9` at `r=3/2`, take the exchangeable
putative law

\[
 p_3=\frac{112}{115},\qquad p_8=\frac3{115},
\]

with all other level masses zero.  Its singleton equations hold trivially.
For a `k`-set, the generators of `k` and `binom(k,2)` at levels 3 and 8 are

\[
 (\mathcal Lk,\mathcal L\binom{k}{2})=
 \begin{cases}
 (3/17,21/17),&k=3,\\
 (-112/17,-784/17),&k=8.
 \end{cases}
\]

Both stationary moment equations therefore hold exactly.  Nevertheless,
`p_1=0`, `E|A|=72/23`, and the normalized (62) margin is

\[
 -\left(\frac{E|A|}{9}-\frac13\right)=-\frac1{69}.
\]

Thus even the singleton equations together with the first two exact
factorial-moment equations do not imply (62).  A successful moment proof
must use at least a third-order constraint, or a graph-sensitive weighted
pair observable containing information not present in the cardinality
moments.
