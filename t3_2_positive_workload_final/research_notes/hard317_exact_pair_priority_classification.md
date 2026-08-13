# Exact-proper bases that require the priority trace

**Proof-only classification, 2026-08-11 PDT.**  This note extends the
\(w_a,m_a\) construction of
*hard317_source_zero_priority_macro.md* to all seventeen exact proper pairs

\[
                         L_+=\{aU,V+I\},\qquad a=0,1,2.             \tag{1.1}
\]

It identifies structurally which bases have a singular pure renewal and
therefore require the priority trace.  No orientation enumeration is used.
The support list is finite bookkeeping; every probabilistic conclusion is
derived from the common invariant.

This is not a certification of the completed stopped theorem.  It only
classifies its necessary scope.

## 1. Universal exact-pair identity

For a lower complex \(y=(c_y,b_y)\), define

\[
 w_a(y)=c_y+a b_y,\qquad
 m_a(u)=\min\{b_y:y\in L_0,\ w_a(y)\le u\}.                        \tag{1.2}
\]

The proper pair preserves \(U+aI\).  A lower firing \(y\to z\), followed
by proper cleanup to \(I=0\), maps

\[
 u'=u-w_a(y)+w_a(z),\qquad
 \Delta V=b_y-b_z.                                                \tag{1.3}
\]

On the first lower time scale, its source has
\(b_y=m_a(u)\).  Therefore

\[
 \Delta\{V+m_a(U)\}=m_a(u')-b_z\le0,                              \tag{1.4}
\]

because \(u'\ge w_a(z)\).  This proves the same priority coboundary for
\(a=0,1,2\).

At base \(u\), a pure opening is enabled exactly when \(u\ge a\).  A
genuine lower escape of cofactor order zero is enabled exactly when

\[
 \exists\,y\in L_0:\quad b_y=0,\quad c_y\le u.                    \tag{1.5}
\]

If (1.5) holds, it competes on the base time scale.  The pure renewal has
the polynomial bound used by the ordinary exact-pair proof.  If (1.5)
fails, then \(m_a(u)>0\): the first lower macro occurs only after order
\(n^{m_a(u)}\) pure attempts, and treating it as a small perturbation is
false.  These and only these bases require the priority trace.

Thus the classification criterion is

\[
                 u\ge a\quad\hbox{and}\quad m_a(u)>0.              \tag{1.6}
\]

It depends on the enabled lower face at the actual base, not merely the
maximal source degree somewhere in the support.

## 2. Source zero

For \(a=0\), the pure opening is enabled at every base.  The six lower
supports give:

| lower support | bases satisfying (1.6) | \(m_0(u)\) |
|---|---|---|
| \(\{I,2U,2I,U+I\}\) | \(u=0,1\) | \(1\) |
| \(\{U,2U,2I,U+I\}\) | \(u=0\) | \(2\) |
| \(\{U,I,2I,U+I\}\) | \(u=0\) | \(1\) |
| \(\{U,I,2U,2I,U+I\}\) | \(u=0\) | \(1\) |
| \(\{U,I,2U,2I\}\) | \(u=0\) | \(1\) |
| \(\{U,I,2U,U+I\}\) | \(u=0\) | \(1\) |

Every source-zero support therefore has a finite singular base set.  These
are precisely the bases repaired by the source-zero priority theorem.

## 3. Source one

Four of the five \(a=1\) lower supports contain \(0\):

\[
\begin{gathered}
\{0,2U,2I,U+I\},\quad
\{0,I,2U,2I,U+I\},\\
\{0,I,2U,2I\},\quad
\{0,I,2U,U+I\}.
\end{gathered}                                                     \tag{3.1}
\]

The zero-source lower clock is enabled at every base, so \(m_1(u)=0\)
and (1.6) never holds.

The remaining support is

\[
                         L_0=\{I,2U,2I,U+I\}.                      \tag{3.2}
\]

At the smallest proper-enabled base \(u=1\), no cofactor-free lower source
is enabled and \(m_1(1)=1\).  At \(u\ge2\), \(2U\) is enabled and
\(m_1(u)=0\).  Hence the unique source-one priority base is

\[
       L_+=\{U,V+I\},\quad L_0=\{I,2U,2I,U+I\},\quad u=1.          \tag{3.3}
\]

The base \(u=0\) has no proper opening.  Moreover its face is isolated:
every complex in (3.3) has \(U+I\ge1\), so a reachable state at
\(U=I=0\) began there and has \(D_V=0\).  It is outside the
historical-positive-debt local scope.

## 4. Source two

Five of the six \(a=2\) lower supports contain \(0\):

\[
\begin{gathered}
\{0,I,2I,U+I\},\quad
\{0,U,2I,U+I\},\quad
\{0,U,I,2I,U+I\},\\
\{0,U,I,2I\},\quad
\{0,U,I,U+I\}.
\end{gathered}                                                     \tag{4.1}
\]

Again \(m_2(u)=0\) for every \(u\), so no proper-enabled base is singular.

The last support is

\[
                         L_0=\{U,I,2I,U+I\}.                       \tag{4.2}
\]

The pure opening requires \(u\ge2\).  But at every such base the
cofactor-free lower source \(U\) is enabled, so \(m_2(u)=0\).  At \(u=0,1\)
the pure opening is disabled.  Consequently:

\[
             \boxed{\text{No source-two exact-pair base needs priority.}} \tag{4.3}
\]

This explains why the exceptional \(\{2U,V+I\}/\{0,I,2I,U+I\}\) row has
a delicate interrupted-return correction but no enabled-base renewal
singularity: its degree-zero lower clock is always present.

## 5. Complete structural classification

Among all seventeen exact base-open supports, the priority trace is needed
exactly on:

- the finite singular bases of all six \(a=0\) supports; and
- the single \(a=1\) support (3.3) at \(u=1\).

No \(a=2\) base needs it.  Outside these bases, either:

1. the proper opening is disabled (\(u<a\)); or
2. an enabled cofactor-free lower source competes on the base scale
   (\(m_a(u)=0\)).

In the second case the ordinary killed one-species trace has a genuine
enabled escape clock.  If the escape has lower source degree \(e\), while
the pure opening has degree \(a\), then

\[
                 (1-Z^{\rm pure}(u))^{-1}
                    \le C(1+u)^{(a-e)^+}.                          \tag{5.1}
\]

This is the exact enabled-base version of the renewal estimate: compare the
two physical base clocks before opening, and use the strong cut if the
proper two-node block is not closed.  Since \(0\le a,e\le2\), the loss is
at most quadratic and is already included in the ordinary polynomial Green
weights.  In the first case there is no pure renewal to sum.

The criterion (1.6) is the proof-level replacement for the false rule based
only on the maximal lower source degree \(d\).  It is orientation-independent
and remains valid for arbitrary fixed positive rates.

## 6. Ordinary enabled-base renewal theorem

The nonsingular alternative can be proved without referring to the
seventeen-row list.

### Theorem 6.1 (enabled escape after exact-pair renewal)

Let

\[
 L_+=\{aU,V+I\},\qquad a\in\{0,1,2\},                             \tag{6.1}
\]

with both proper directions present, and let the lower linkage be a finite
strong digraph of binary complexes containing no \(V\).  Start from a
no-fast base \(x=(u,n,0)\), where \(a\le u<L_n\), and stop, including the
boundary-causing reaction, before \(V<n/2\) or
\(U\vee I\vee |V-n|\ge L_n\).  Suppose an \(I\)-free lower source

\[
                         eU\in L_0,\qquad e\le u                   \tag{6.2}
\]

is enabled.  Put

\[
 e_*(u)=\max\{e:eU\in L_0,\ e\le u\}.                             \tag{6.3}
\]

Let \(Z_x^{\rm pure}\) be the probability of one exact physical return
using only \(aU\to V+I\) and \(V+I\to aU\), before any lower firing or
physical boundary.  Then, uniformly in \(n\),

\[
 {1\over1-Z_x^{\rm pure}}
       \le C(1+u)^{(a-e_*(u))^+}.                                 \tag{6.4}
\]

Separate the two nonpure kernels before renewing.  Put in \(Q_0\) every
stopped path whose first base reaction is an enabled lower reaction.  Put in
\(K^{\rm int}\) only a path whose first base reaction is the proper opening
and for which a lower reaction interrupts the ensuing proper excursion
before its pure return.  Finally, let \(B^{\rm pure}\) contain a
proper-only excursion that hits the included physical boundary before
returning.  These three events are disjoint, and the complete renewed exit
kernel is

\[
     (I-Z^{\rm pure})^{-1}(Q_0+K^{\rm int}+B^{\rm pure}).          \tag{6.5}
\]

The ordinary kernel \(Q_0\) may have order-one mass and is **not** subject
to an \(n^{-1}\) estimate.  Its actual no-fast, service, upward, or boundary
endpoint instead obeys, for every fixed \(p,q\),

\[
 \begin{aligned}
 (I-Z^{\rm pure})^{-1}Q_0w_p
     &\le C_p(1+u)^{p+C_p},\\
 (I-Z^{\rm pure})^{-1}Q_0H_{\theta'}
     &\le C_{\theta',\theta}(1+u)^{C_{\theta',\theta}}H_\theta(u),\\
 (I-Z^{\rm pure})^{-1}Q_0\!\left[(1+T)^q w_p\right]
     &\le C_{p,q}(1+u)^{p+C_{p,q}} .                              \tag{6.6}
 \end{aligned}
\]

Only the interrupted-proper kernel is small.  Including its same four
actual endpoint types, it satisfies

\[
 \begin{aligned}
 (I-Z^{\rm pure})^{-1}K^{\rm int}w_p(u)
   &\le {C_p(1+u)^{p+2+(a-e_*)^+}\over n},\\
 (I-Z^{\rm pure})^{-1}K^{\rm int}
       H_{\theta'}(u)
   &\le {C_{\theta',\theta}(1+u)^{2+(a-e_*)^+}\over n}
          H_\theta(u),                                            \tag{6.7}
 \end{aligned}
\]

where \(w_p(u)=(1+u)^p\),
\(H_\theta(u)=\exp\{\theta u\log(u+e)\}\), and
\(0<\theta'<\theta<1/2\).  Every fixed physical holding-time reward obeys
the same \(n^{-1}\) bound in (6.7), with a larger polynomial power of
\(1+u\).  The renewed \(B^{\rm pure}\) term is superpolynomially small
under each reward in (6.6)--(6.7).  Here \(T\) is physical elapsed time,
never reaction count.

#### Proof of the renewal bound

At the base, the pure opening clock is

\[
                         \lambda_{\rm p}
                         =\alpha(u)_{\underline a}.                \tag{6.8}
\]

Let \(\lambda_{\rm esc}\) be the total clock of **all** enabled lower
reactions at the base.  The enabled source \(e_*U\) has at least one
outgoing edge by strong connectivity, so for some fixed \(\gamma>0\)

\[
 \lambda_{\rm esc}\ge\gamma(u)_{\underline{e_*}}>0.               \tag{6.9}
\]

Every such firing terminates the pure trial.  If its target is \(I\)-free,
it is already a nonself base exit; if its target contains \(I\), the path
has used a lower edge and can never again belong to the word class defining
\(Z^{\rm pure}\).  There are no other base clocks: at \(I=0\), the reverse
proper and every \(I\)-sourced lower reaction are disabled.  Consequently
the first base race has total rate \(\lambda_{\rm p}+\lambda_{\rm esc}\),
and

\[
 1-Z_x^{\rm pure}
 \ge{\lambda_{\rm esc}\over\lambda_{\rm p}+\lambda_{\rm esc}}
 \ge {\gamma(u)_{\underline{e_*}}
        \over \alpha(u)_{\underline a}+\gamma(u)_{\underline{e_*}}}
 \ge c\,{(1+u)^{e_*}\over(1+u)^a+(1+u)^{e_*}}.                  \tag{6.10}
\]

The middle inequality uses monotonicity of
\(t\mapsto t/(\lambda_{\rm p}+t)\): any additional escape clock, including
a degree-two clock, raises rather than lowers the quotient.  Hence no
unlisted term may be placed only in the denominator.  The final comparison
uses \(u\ge a,e_*\) and the binary falling-factorial bounds.  It yields

\[
 1-Z_x^{\rm pure}\ge c(1+u)^{-(a-e_*)^+},                        \tag{6.11}
\]

which is (6.4).  On the finitely many values at which a falling factorial
differs from its power comparison, (6.2) makes the escape clock strictly
positive and enlarging \(C\) completes the bound.

Notice what the proof does not use: a maximal lower degree whose source is
disabled at \(u\).  The clock in (6.9) is physically enabled at the actual
base.  This is exactly why Theorem 6.1 avoids the source-zero obstruction.

#### Proof of the endpoint bounds

First consider \(Q_0\).  If \(f\) is an enabled base lower edge with clock
\(\lambda_f\), (6.10) gives the exact cancellation

\[
 {1\over1-Z_x^{\rm pure}}
 {\lambda_f\over\lambda_{\rm p}+\lambda_{\rm esc}}
 \le {\lambda_f\over\lambda_{\rm esc}},\qquad
 \sum_{f\ {\mathrm{base\ lower}}}{\lambda_f\over\lambda_{\rm esc}}=1.
                                                                    \tag{6.12}
\]

Thus the renewed \(Q_0\) is a convex mixture of ordinary traces launched by
one actual lower firing.  Its mass can be order one, but no renewal power is
left uncancelled.  The launching reaction changes each slow coordinate by
at most two.  If it lands at \(I=0\), the trace has already stopped.  If it
lands at \(I>0\), then below the boundary

\[
 {\lambda_{\rm slow}\over\lambda_{\rm fast}+\lambda_{\rm slow}}
       \le q_n:={CL_n^2\over n}.                                  \tag{6.13}
\]

A path with \(k\) later slow firings has at most \(k+1\) fast firings before
its included endpoint: apart from a possible terminal service, each fast
firing must spend reserve created by a later proper opening.  Summing the
fast choices between successive slow firings therefore costs only \(C^k\),
so all \(k\ge0\) are controlled by a convergent geometric race series.
The source/target telescoping and the same reserve pairing show that its
positive \(U\)-increment is at most \(2k+C\), where the fixed \(C\le4\)
also covers the launching target and a terminal service.  Consequently its weighted
series has ratio at most

\[
       Cq_nL_n^{2\theta'}
       ={CL_n^{2+2\theta'}\over n}=o(1),                           \tag{6.14}
\]

because \(\theta'<1/2\).  A fixed initial jump is absorbed by the strict
gap \(\theta-\theta'\).  The same series with
\((1+u+Ck)^p\) proves the polynomial line of (6.6), while the part
\(k>L_n\) is superpolynomially small even after multiplication by the
stopped endpoint weight.  This proves all endpoint claims for \(Q_0\)
without a finite interruption cutoff.

Now condition on a proper opening.  At the opened state, the sum of all
lower clocks is at most \(C(1+U+I)^2\), while the fast clock is at least
\(cnI\).  Before the first lower firing, the proper cloud has the
birth--death product

\[
 {\mathbb P(I=i+1\mid\hbox{pure cloud})\over
  \mathbb P(I=i\mid\hbox{pure cloud})}
 \le {C(1+u)^a\over n(i+1)}.                                     \tag{6.15}
\]

A proper-only boundary path must make order \(L_n\) nested openings: along
that path \(R=I\), while proper openings never increase \(U\).  Iterating
(6.15) therefore bounds its probability by a factorial product with ratio
at most \(CL_n^2/n\).  After multiplication by (6.4), by any fixed time or
polynomial reward, and by \(H_{\theta'}(L_n+C)\), it is
\(O(n^{-M})H_\theta(u)\) for every fixed \(M\).  This proves the asserted
bound for \(B^{\rm pure}\) and also shows why it cannot simply be omitted
from the path partition.

Size bias by a binary lower propensity preserves every fixed moment.
Compensating the first lower clock against \(cnI\) therefore gives

\[
 \mathbb E\!\left[
  (1+U_T+I_T+R_T)^p;\hbox{a lower firing before pure return}
  \,\middle|\,\hbox{opened}\right]
 \le {C_p(1+u)^{p+2}\over n}.                                    \tag{6.16}
\]

After that first lower firing, (6.13)--(6.14) sum every later slow
interruption.  For completeness, if there are \(k\) post-interruption slow
firings and the final \(U\)-increment is positive, pairing every proper
target \(V+I\) with the fast reaction that spends its reserve gives an
increment at most \(2k+C\); unpaired proper targets have \(U\)-degree zero.
This is the all-order source/target argument and does not impose a maximum
on \(k\).  Multiplying (6.16) by (6.4), and using the strict gap
\(\theta-\theta'\) to absorb the fixed power
\((a-e_*)^+\le2\), proves both lines of (6.7).

#### Proof of the time bounds

A raw base wait has every fixed moment bounded by a polynomial in \(1+u\).
The number of pure attempts is geometric with moments controlled by
(6.4).  Every open holding time is dominated by an exponential variable
of mean \(C/n\).  After a lower interruption, augment the asymmetric
race recursion by the binomial expansion of accumulated holding times.
The \(k\)-th term acquires only a fixed polynomial in \(k\), so the geometric
series (6.13)--(6.14) remains summable.  Summing the pure block first changes
only the polynomial exponent supplied by (6.4).  This proves (6.6)--(6.7)
for physical elapsed time, not reaction count.
\(\square\)

### Corollary 6.2 (ordinary versus priority trace)

For an exact pair (1.1), Theorem 6.1 applies at every proper-enabled base
outside the set (1.6).  On (1.6), its premise (6.2) fails and the
\(w_a,m_a\) priority trace is necessary.  Hence, after adjoining the
lower-only case \(u<a\), the two analytic kernels are disjoint and exhaustive:

\[
\begin{array}{c|c}
\text{ordinary kernel}&u<a\ \text{or}\ m_a(u)=0,\\
\text{priority kernel}&u\ge a\ \text{and}\ m_a(u)>0.
\end{array}                                                       \tag{6.17}
\]

The case \(u<a\) has no pure opening and is included in the ordinary
lower-only trace without renewal.

## 7. Publication boundary

The classification establishes where the priority theorem must be inserted
into the hard-317 kernel, and Theorem 6.1 supplies the ordinary-side renewal
and all-order bounds.  It does not by itself prove the corresponding
priority-side dirty-macro control, boundary payment, duration moments, or
the common fourth-power drift.  Those are the separate audit obligations
stated in the frozen source-zero priority note.

All analytic, pair-level, and global certification flags remain false.
