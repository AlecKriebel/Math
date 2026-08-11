# A stopped Perron--Frobenius activation wedge for the seven mixed-profile rank-two pairs

## 1. Scope

This note proves a local stopped activation-wedge estimate for the seven
mixed-profile pairs in the exact twenty-pair rank-two linear-workload
family.  It does **not** prove pair recurrence.  The estimate is awaiting
independent replay, and the interior-to-\(C\)-service seam in Section 6 is
open.  All executable recurrence and global flags remain false.

The seven-pair fingerprint is

~~~text
93717536ce82eceefe6909c62568afab31e06695dada8b69defb93335d576957
~~~

There are 40 one-active failed incidences, no two-active failed incidence,
and seven all-active failed incidences.  The one-active incidence
fingerprint is

~~~text
8c5502bb4bc4b29fbb5c89512fbf4e796001735316b41b60f82d3c0add4dff72
~~~

## 2. Exact normalized geometry

Relabel a one-active row so that \(X\) is active and \(A,B\) are inactive.
Every row has lower linkage

\[
             L_-=\{0,A\}
\tag{2.1}
\]

and its other linkage is one of

\[
\begin{split}
T\in\{&
\{2A,2B,AB,A+X,B+X\},\\
&\{2A,2B,A+X,B+X\},\\
&\{2A,AB,A+X,B+X\},\\
&\{2B,AB,A+X,B+X\}\}.
\end{split}                                             \tag{2.2}
\]

Each menu occurs in ten physical incidences.  The exact inactive caps
\((0,0),(1,0),(2,0),(0,1),(0,2)\) each occur eight times.  All 40 rows are
Family-I origin-service rows of resistance zero in the already proved
arbitrary-orientation graph theorem.

The important extra structure is that the two carrier complexes

\[
                 A+X,\qquad B+X                         \tag{2.3}
\]

are always present, while every other top-linkage complex is an inactive
quadratic in

\[
                 \{2A,AB,2B\}.                          \tag{2.4}
\]

## 3. The killed carrier matrix

Fix an arbitrary strongly connected orientation of \(T\) and arbitrary
positive rates.  Regard \(A+X\) and \(B+X\) as carrier types \(A,B\).
For \(i\ne j\), let \(q_{ij}\) be the total rate of carrier edges
\(i+X\to j+X\), and let

\[
 r_i=\sum_{\substack{i+X\to y\\y\in\{2A,AB,2B\}}}
             \kappa_{i+X,y}.                            \tag{3.1}
\]

Make every split edge in (3.1) absorbing and write

\[
 (Qf)_i=\sum_{j\ne i}q_{ij}(f_j-f_i)-r_i f_i.           \tag{3.2}
\]

No nonempty carrier set can be closed under carrier edges while having
zero \(r_i\) throughout: it would be a closed vertex set in the full
strongly connected graph \(T\).  Hence the killed two-state chain is
transient, \(-Q\) is a nonsingular \(M\)-matrix, and

\[
             h=(-Q)^{-1}{\bf1}>0.                       \tag{3.3}
\]

Choose \(\epsilon>0\) small and put

\[
             v_i=1-\epsilon h_i>0.                      \tag{3.4}
\]

For a carrier source define its rate-weighted inactive-mass reward

\[
\begin{split}
b_i(v)={}&
\sum_{i+X\to j+X}\kappa_{i+X,j+X}(v_j-v_i)\\
&+\sum_{\substack{i+X\to y\\y\ {\rm inactive\ quadratic}}}
       \kappa_{i+X,y}(v\mathbin\cdot y-v_i).             \tag{3.5}
\end{split}
\]

At \(\epsilon=0\), (3.5) equals \(r_i\).  If \(r_i=0\), the
second sum is absent and (3.2)--(3.3) give

\[
        b_i(v)=-\epsilon(Qh)_i=\epsilon.                 \tag{3.6}
\]

If \(r_i>0\), then \(b_i(v)=r_i+O(\epsilon)\), so a smaller common
\(\epsilon\) gives \(b_i(v)\ge r_i/2\).  Therefore

\[
                b_*:=\min_i b_i(v)>0.                   \tag{3.7}
\]

This is the orientation- and rate-uniform-in-state Perron--Frobenius
margin.  Its numerical value may depend on the fixed orientation and rate
vector, as allowed.

## 4. Physical generator bound

Set

\[
       R=v_AA+v_BB,\qquad H=X+A+B.                       \tag{4.1}
\]

Every top reaction preserves \(H\).  Carrier-source propensities are
\(XA\) and \(XB\).  The total absolute contribution from inactive
quadratic sources is at most \(K(A+B)^2\).  Equations (3.5)--(3.7) and
comparability of \(R\) with \(A+B\) therefore give

\[
          \mathcal L_T R\ge cXR-KR^2.                   \tag{4.2}
\]

Write the rates on (2.1) as \(\alpha\) for \(0\to A\) and \(\delta\)
for \(A\to0\).  Then

\[
          \mathcal L_-R=v_A(\alpha-\delta A)
             \ge-K_0(1+R).                              \tag{4.3}
\]

Choose \(\eta>0\) small enough in terms of (4.2), then choose \(h_*\).
For \(h=1+H\ge h_*\),

\[
\begin{cases}
\mathcal LR\ge c_1hR,&0<R\le\eta h,\\
\mathcal LR=\alpha v_A>0,&R=0.
\end{cases}                                             \tag{4.4}
\]

Thus the apparently dormant active axis is not neutral after the physical
birth is retained: the birth creates the first carrier, and the strong top
graph amplifies that carrier at order \(H\).

## 5. One proper stopped-wedge function

Fix an integer \(p\ge2\), and choose \(a>0\) so that
\(av_A>2p\).  Define on the whole state space

\[
       V_p(x)=h^p\exp\{-aR/h\},\qquad h=1+H.             \tag{5.1}
\]

Because \(0\le R\le v_{\max}H\),

\[
 e^{-av_{\max}}h^p\le V_p(x)\le h^p,                   \tag{5.2}
\]

so \(V_p\) is proper.

At \(R=0\), the only enabled reaction is \(0\to A\), and its exact
multiplicative increment is

\[
 {V_p(H+1,v_A)\over V_p(H,0)}
 =\left(1+{1\over h}\right)^p
    \exp\left\{-{av_A\over h+1}\right\}<1               \tag{5.3}
\]

for all sufficiently large \(h\).  Moreover the decrement in (5.3) is at
least \(c h^{p-1}\).

For \(0<R\le\eta h\), a top jump leaves \(h\) fixed and changes \(R\) by
a bounded amount \(d\).  The uniform expansion

\[
 e^{-ad/h}-1=-{ad\over h}+O(h^{-2}d^2)                 \tag{5.4}
\]

and (4.2) give

\[
\begin{split}
\mathcal L_TV_p
 &\le-{aV_p\over h}\mathcal L_TR
   +{CV_p\over h^2}\sum_{r\in T}\lambda_r(\Delta_rR)^2\\
 &\le-cV_pR+{C\over h}V_pR.                            \tag{5.5}
\end{split}
\]

Here the top intensity is at most \(C\{H(A+B)+(A+B)^2\}\le ChR\)
inside the wedge.  The lower birth/death contribution has absolute value
at most

\[
             C h^{p-1}(1+R).                            \tag{5.6}
\]

For \(R>0\), the negative term in (5.5) has order \(h^pR\) and absorbs
(5.6); \(R=0\) is handled by (5.3).  After enlarging \(h_*\),

\[
       \mathcal LV_p\le-c_ph^{p-1}
       \quad\text{on}\quad
       \{h\ge h_*,\ R\le\eta h\}.                       \tag{5.7}
\]

This is a pointwise physical-time bound for the full generator.  No lower
reaction was deleted and no inactive coordinate was put in a fixed box.

For an exact stopped contract, fix \(M>2\), start with \(h_0\ge Mh_*\),
and stop at

\[
\tau=\inf\left\{t:
 R_t>\eta h_t\ \text{or}\
 h_t<h_0/M\ \text{or}\
 h_t>Mh_0\right\}.                                     \tag{5.8}
\]

Localization and (5.7) give

\[
 \mathbb E_x\!\left[
   V_p(X_\tau)-V_p(x)
   +c_p(h_0/M)^{p-1}\tau
 \right]\le0.                                           \tag{5.9}
\]

In particular,

\[
 \mathbb E_x\tau\le C_{p,M}h_0.                         \tag{5.10}
\]

The same bound holds uniformly after every pre-\(\tau\) stopping time.
Markov's inequality and the strong Markov property therefore give an
exponential tail on scale \(h_0\), and hence

\[
             \mathbb E_x\tau^m\le C_{m,p,M}h_0^m
             \quad(m\ge1).                              \tag{5.11}
\]

The stopped shell itself gives deterministic polynomial endpoint bounds.
Finally, (5.2) and (5.9) imply

\[
 \mathbb P_x\{h_\tau\ge Mh_0\}
       \le e^{av_{\max}}M^{-p}.                         \tag{5.12}
\]

Thus the proved endpoint alternatives are:

1. activation, \(R_\tau>\eta h_\tau\);
2. workload descent, \(h_\tau<h_0/M\); or
3. an upward shell exit whose probability has the tunable bound (5.12).

## 6. What is still open

The estimate does not identify \(R\) with the service species.  At an
activation endpoint \(R\ge\eta h\), most inactive mass could be \(B\)
rather than the physical outflow species \(A\) in the normalized chart.
A complete seven-pair theorem must prove, uniformly from that endpoint,
one of:

1. access to a region with enough \(A\)-occupation that repeated
   \(A\to0\) reactions decrease \(H\);
2. a second stopped corrector which converts the \(R\)-mass into physical
   \(A\)-service; or
3. a common scalar whose top-shell correction remains controlled outside
   the activation wedge.

It must then compose the service episode with (5.8)--(5.12), including the
upward shell endpoint, and prove a negative increment for one proper
function.  None of those assertions follows from the PF wedge alone.
Accordingly the seven pair-recurrence flag remains false.

## 7. Reproduction

Run

~~~text
PYTHONPATH=src python3 -B src/rank_two_mixed_profile_7.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_rank_two_mixed_profile_7.py -v
~~~

The executable freezes the seven pairs, 40 one-active rows, 20 normalized
profiles, four carrier menus, cap histogram, all-active workloads, and
claim-neutral arithmetic.  It records the independent audit as pending and
keeps every recurrence flag false.
