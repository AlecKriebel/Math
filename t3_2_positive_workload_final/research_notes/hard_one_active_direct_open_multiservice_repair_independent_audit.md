# Independent hostile audit of the direct/open multi-service repair

**Verdict (2026-08-12 PDT): STRICT PASS at the stated 105-incidence local
scope.**  The multi-service construction repairs the arbitrary-subpower
inactive-cloud gap.  The direct mechanism has a background-uniform service
minorization in active time; the open mechanism has an autonomous
\((B,C)\) stopping rule and hence preserves the exact conditional
immigration--death law of \(A\).  The resulting defect and boundary bounds
remain valid after every fixed polynomial endpoint size bias, and the exact
fourth-power remainder is lower order.  This verdict does not certify the
other 999 one-active incidences, a hard pair, or T3-2.

The frozen target is

```text
note  fbd9f42815b08a2030d931482b70ff10aca9a92df3c080e2533f275fa6733c2a
```

No orientation, history, or population box was enumerated.  The finite
replay was restricted to the support predicates: 99 incidences have a
linkage containing \(C\) and an active-free complex, and six incidences have
the normalized supports

\[
             \{C,A+C\},\qquad \{0,B,2B,B+C\},\qquad B_0=0.
\]

## 1. Direct service minorization is uniform in the background

Fix a simple directed path in the \(C\)-linkage from \(C\) to its first
active-free vertex.  Before its terminal edge, all vertices have active
degree one and, after removal of the common \(C\), belong to
\(\{0,A,B\}\).  In active time \(ds=C_tdt\), a \(C\)-sourced top edge is a
constant-rate immigration clock and every \((C+I)\)-sourced top edge gives
each labelled particle of type \(I\) an independent constant-rate clock.
This is an exact graphical representation: a top source contains at most
one inactive molecule, so there is no particle--particle interaction to
invalidate the labels.

If the path has length one, its edge itself is a constant-rate service
clock in active time.  Otherwise, require one immigration on the first path
edge in a prescribed subinterval, label that immigrant, and in subsequent
subintervals require its prescribed path clocks before its other clocks.
This event has probability \(\eta>0\) in a fixed interval of length \(T\).
Neither number nor types of background particles enter \(\eta\).  A
background service before the tag finishes is already a success, while
background top-to-top reactions cannot move the labelled particle.  Thus,
from every post-service background state,

\[
 \mathbb P\{\hbox{a service during }[s,s+T]\mid\mathcal F_s\}\ge\eta.
\]

Applying this conditional minorization successively shows that the active
time \(S_K\) to \(K\) services is dominated by \(T\) times a sum of \(K\)
geometric variables of parameter \(\eta\).  Hence

\[
 \mathbb E S_K^r\le C_rK^r,
 \qquad
 \mathbb P\{S_K>C K+y\}\le C e^{-cy}.
\]

This proves the claimed service estimate without prescribing a word for
the whole system and without a bounded-background hypothesis.

## 2. Direct defect, endpoint, and moving-boundary estimates

Let \(M_s\) be total inactive mass and \(N_s\) the service count in the
defect-free top process.  Top conversions and deaths do not increase
\(M\), top births are dominated by a fixed-rate Poisson process \(\Pi\),
and one service increases inactive mass by at most two.  Pathwise,

\[
                         M_s\le u+\Pi_s+2N_s.
\]

The preceding negative-binomial tail and the Poisson exponential martingale
therefore give every fixed moment of
\(S_K+\sup_{s\le S_K}M_s\) as a fixed polynomial in \(1+u+K\).

Before the \(K\)-th clean service, \(C\ge n-K\).  The total propensity of
all active-free sources is at most \(C_0(1+M)^2\), so its active-time
intensity is at most

\[
                         {C_0(1+M_s)^2\over n-K}.
\]

For any fixed polynomial post-jump weight \(F\), the compensator formula,
with the bounded causing jump included, gives

\[
 \mathbb E[F;E]
 \le {C\over n-K}\,
      \mathbb E\int_0^{S_K}(1+M_s)^2F^+_s\,ds
 \le {C_F\over n}(1+u+K)^{d_F}.
\]

Thus iteration to \(K=u+1\), rather than one service, does not lose the
factor \(n^{-1}\); it costs only a fixed polynomial in the subpower
quantity \(u+K\).

For \(L=n^{1/16}\), put
\(m=L-u-2K-2\sim L\).  If the top process crosses \(L\) before \(S_K\),
then \(\Pi_{S_K}\ge m\).  Splitting at a deterministic time proportional
to \(m\) gives

\[
 \mathbb P\{\Pi_{S_K}\ge m\}
 \le \mathbb P\{S_K>c_1m\}
     +\mathbb P\{\Pi_{c_1m}\ge m\}
 \le e^{-c_2m}.
\]

The same split after multiplication by fixed powers of \(S_K\), \(M\),
and the included post-jump endpoint remains \(O(n^{-M_0})\) for every
fixed \(M_0\).  On clean completion, \(C=n-K\), physical time is at most
\(S_K/(n-K)\), and the endpoint inactive entropy is
\(O((u+K)\log(2+u+K))\) in expectation.  This proves all direct estimates
claimed in (1.6)--(1.12).

## 3. The open stopping rule really is autonomous

In the open support, the first linkage preserves \((B,C)\), and every rate
in the second linkage depends only on \((B,C)\).  The unlocalized completion
or defect time \(\tau^\circ\) can therefore be constructed from the
second-linkage driving clocks alone.  It is independent of the clocks
driving \(A\).  Conditional on the entire \((B,C)\)-path, the operational
horizon \(S^\circ=\int_0^{\tau^\circ}C_tdt\) is deterministic, and the
standard independent-particle construction gives exactly

\[
 A_{\tau^\circ}\ \stackrel d=\
 \operatorname{Bin}(u,e^{-\beta S^\circ})
 +\operatorname{Pois}\!\left({\alpha\over\beta}
                  (1-e^{-\beta S^\circ})\right).
\]

In particular this is not an application of a terminal-time formula after
conditioning on an \(A\)-dependent stop.  Uniformly in the conditioned
path, \(A_{\tau^\circ}\) is dominated by \(u+P\), where
\(P\) is Poisson with fixed mean.  It follows that it has every fixed
moment and expected factorial entropy \(O(1+u\log(2+u))\).

## 4. Arbitrary strong orientation gives a positive launch parameter

Write \(T=B+C\).  At \(b>0\), the total \(T\)-exit rate is
\(\kappa mb\), \(\kappa>0\), while all active-free-source rates sum to at
most \(C(1+b^2)\).  Therefore the exact relevant-clock race has defect
probability at most \(C(1+b)/m\).

At \(b=0\), the outgoing zero-complex rate \(\lambda_0\) is positive.
An attempt progresses directly if \(0\) jumps to \(B\) or \(2B\), or if
\(0\) jumps to \(T\) and the first \(T\)-exit lands at \(B\) or \(2B\).
The sum of these two probabilities is the displayed \(p_*\).  If
\(p_*=0\), every zero exit lands at \(T\) and every \(T\)-exit lands at
zero.  Then \(\{0,T\}\) is a closed proper subset of the four-vertex
reaction graph, contradicting strong connectivity.  Thus \(p_*>0\) for
every fixed strong orientation and positive rate vector.

Conditional on no competing lower-source firing, neutral returns to
\(b=0\) are geometric with parameter at least \(p_*\).  Each attempt has
one constant-rate zero-source wait and at most two \(T\)-exit races.  The
intermediate \(B\)-population is at most two before the final service, so
all size-biased defect estimates for one macrocycle are \(O(n^{-1})\), and
all duration moments are finite.

For precision, the zero-complex jump deliberately used to launch an
attempt at \(b=0\) is an allowed macrocycle reaction, not a defect.  In the
target note, “first lower-source defect” in Section 4 means the first
*competing* active-free-source reaction outside this designated launch.
Sections 4.1--4.2 make this construction unambiguous.  The publication copy
should make that qualifier explicit, but it does not change the stopping
rule or any estimate.

## 5. Iterating the open kernel retains the \(n^{-1}\) margin

After the \(j\)-th clean net service, \(B_j\le j+3\).  Before completion,
the active population is at least \(n-K\).  Summing the relevant-clock
bound over the \(K\) macrocycles yields

\[
 \mathbb P(E)\le {C\over n-K}\sum_{j<K}(1+j)
               \le {C K^2\over n-K}=n^{-1+o(1)}.
\]

The attempt counts have geometric tails and the endpoint changes per race
are bounded.  Multiplying by any fixed polynomial of attempt count,
\(A\), \(B\), duration, or post-jump population changes the numerator only
to another fixed polynomial in \(1+u+K\).  This proves (4.11), not merely
an unweighted union bound.  Constant-rate zero-source waits occur only at
\(b=0\); their geometric sums give
\(\mathbb E(\tau^\circ)^r\le C_rK^r\).  Every neutral launch/exit pair has
net \(C\)-increment zero and every completed macrocycle has one final
unpaired \(T\)-exit, so \(C_{\tau^\circ}=n-K\) on clean completion.

## 6. The open factorial upcrossing is superpolynomially rare

Only after constructing \(\tau^\circ\) is the \(A\)-cutoff imposed.  In
operational time, label the \(u\) initial particles; their contribution is
always at most \(u\).  The immigrant subsystem starts at zero and at every
deterministic time is Poisson with mean at most \(\alpha/\beta\).  Given a
deterministic horizon \(S\), an upcrossing of \(L\) requires an immigration
birth while the immigrant subsystem contains at least \(L-u-1\) particles.
Consequently

\[
 \mathbb P\{\sup_{s\le S}A_s\ge L\}
 \le \alpha S\,
    \mathbb P\{\operatorname{Pois}(\alpha/\beta)\ge L-u-1\}.
\]

Before the stop, \(C\le n+1\), so
\(\mathbb E(1+S^\circ)^r\le C_rn^r(1+K)^r\).  Since
\(L-u-1\sim n^{1/16}\), the Poisson factorial tail beats that polynomial
and every additional fixed polynomial endpoint or horizon bias.  Thus the
included upcrossing endpoint has \(O(n^{-M})\) weighted mass for every
fixed \(M\).  On the complement the terminal law from Section 3 applies;
on the completion event its nonnegative factorial entropy is bounded above
by its unlocalized expectation.  This validates the order of conditioning
and localization in the target note.

## 7. Arbitrary correction and exact fourth-power expansion

On clean completion,

\[
 \log{(n-K)!\over n!}
 =-K\log n+O(K^2/n).
\]

The complete inactive factorial-linear endpoint cost, including an
arbitrary fixed \(\ell\), is at most
\(C_\ell(1+u+K)\log(2+u+K)\) in expectation.  The correction is exactly
\(\ell\cdot(X_\tau-X_0)\); it is not the sum of absolute corrections over
the fast internal jumps.  Since \(K=u+1\) and \(\log K=o(\log n)\),

\[
 \mathbb E\Delta G_\ell
 \le-K\log n+O_\ell(K\log(2+K))
     +n^{-1+o(1)}K\log n
 \le-cK\log n.
\]

The weighted defect and boundary estimates imply, for each fixed \(r\),

\[
                 \mathbb E|\Delta G_\ell|^r
                    \le n^{o(1)}(\log n)^r.
\]

At the entrance, \(G_\ell(X_0)\asymp n\log n\).  In the exact identity

\[
 \Delta(G_\ell^4)=4G_0^3\Delta G_\ell
 +6G_0^2(\Delta G_\ell)^2
 +4G_0(\Delta G_\ell)^3+(\Delta G_\ell)^4,
\]

each of the last three expectations is \(n^{-1+o(1)}\) relative to
\(G_0^3K\log n\).  Direct duration is \(n^{-1+o(1)}\), open duration is
\(n^{o(1)}\), and both are lower order than the same margin.  Hence the
claimed \(W_\ell\) estimate follows for arbitrary fixed \(\ell\), with no
hidden bounded-start substitution.

## 8. Reflected debt and actual endpoints

For direct rows, top-to-top reactions preserve \(C\), and each service has
\(\Delta C=-1\).  It first lowers positive reflected debt; after that debt
is zero, further services lower the historical residual \(H=C-D\), exactly
as the reflected-mark lemma permits.

For open rows, a neutral attempt \(0\to T\to0\) first raises and then lowers
the reflected \(C\)-mark.  An attempt through \(B\) or \(2B\) has one final
unpaired \(T\)-exit.  Thus each complete macrocycle changes both physical
\(C\) and the reflected accounting by net \(-1\): it lowers incoming debt
when positive and becomes a valid surplus service after reflection reaches
zero.  No identity of an individual active molecule is required.

Every completion, competing defect, and cutoff crossing includes its
causing physical reaction.  Splitting the already controlled boundary
union into inherited \(P/B\) labels cannot enlarge either endpoint-weighted
estimate.  Therefore the frozen note proves Theorem 6.1 at exactly its
stated local scope.
