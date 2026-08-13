# Common-fourth-power completion of the exact-cloud trace

**Proof-first completion note, 2026-08-11 PDT.  Audit status: pending.**  This note completes the
analytic exact-pair trace built in
*hard317_exact_pair_cloud_averaging.md*, using the independently audited
ordered-Green estimates in *proof_first_exact_cloud_ordered_green.md*.
It treats the seventeen exact proper pairs only.  The remaining hard
templates and pair/global composition are outside this note.

All reaction orientations are strong and all positive rate constants are
arbitrary but fixed.  Constants may depend on these fixed data and on a
requested moment order.  No finite orientation enumeration is a proof
input.

## 1. Scope and stopping rule

Fix one reachable reflected-debt class, a reference \((x^\circ,0)\), and a
historically reachable no-fast base

\[
                         x=(u,n,0),qquad D_V>0,qquad u=n^{o(1)}. \tag{1.1}
\]

The proper linkage is \(\{aU,V+I\}\), \(a\in\{0,1,2\}\), and the lower
linkage is one of the seventeen supports in the cloud note.  The trace is
defined at every state in scope.  Here is the structural proof, which is
also needed for the duration estimate.  If \(u\ge a\), the proper opening
is enabled.  In every source-zero support a lower source has
\(w_0\le u\); in the exceptional source-one support
\(\{I,2U,2I,U+I\}\), the source \(I\) has \(w_1(I)=1\le u\); and in the
exceptional source-two support \(\{U,I,2I,U+I\}\), the source \(U\) has
\(w_2(U)=1\le u\).  Every other source-one or source-two support contains
\(0\).  Thus a proper-enabled base always has a feasible lower source.  If
\(u<a\) and no lower source is feasible, every reaction source is disabled,
so the physical state is static.  Such a face cannot carry historically
reachable positive reflected \(V\)-debt from \((x^\circ,0)\).  This
excludes precisely the otherwise undefined alternative.

Use

\[
 L_n=\left\lfloor {n^{1/3}\over\log(n+e)}\right\rfloor.          \tag{1.2}
\]

Contract completed proper excursions in level-zero local time.  Select the
first lower edge with its exact killed effective rate.  A macro is
**leading clean** when its source minimizes the cofactor degree among
feasible sources and no second lower reaction occurs before cleanup.  Let
\(H_a(U,V)=V+m_a(U)\) be the cofactor-envelope proof corrector.

The physical block stops, including the last reaction, at the first of the
following disjoint, path-labelled alternatives.  If one reaction has more
than one label, use the displayed order:

- \(D\): a leading-clean physical firing first reaches \(V<n\);
- \(E\): a nonleading source or a second lower firing during cleanup,
  whether or not that same firing also services \(V\) or crosses a cutoff;
- \(B\): in the absence of \(D\) or \(E\), \(U\), \(I\), or \(|V-n|\)
  first reaches \(L_n\).

Every boundary first crossed while an excursion is open remains the
auxiliary event \(B\).  Only a direct outer-base crossing whose included
endpoint has \(I=0\) and \(V=n\) is the path-labelled promotion endpoint.

## 2. Ideal leading trace and service

For a leading clean edge \(y\to z\), exact carrier cancellation gives

\[
 u'=u-w_a(y)+w_a(z),\qquad
 \Delta V=b_y-b_z,qquad
 \Delta H_a=m_a(u')-b_z\le0.                                   \tag{2.1}
\]

The equality set is a proper subset of the strong lower linkage in every
one of the seventeen actual supports.  Let \(Q_n(u,du')\) be the exact
leading-clean contracted kernel restricted to \(\Delta H_a=0\), with all
strict drops, defects, and included boundaries killed.  The maximal
feasible \(I\)-free source supplies the large-\(U\)
descending-or-killed cut, and all positive equality transitions have one
smaller source degree.  Consequently, for \(0<\theta<1/2\),

\[
 (I-Q_n)^{-1}F_\theta(u)\le C_\theta F_\theta(u),
 \qquad
 (I-Q_n)^{-1}(1+U)^p\le C_p(1+u)^{p+c_p},                       \tag{2.2}
\]

where \(F_\theta(u)=e^{\theta u\log(u+e)}\).  For completeness, the two
parts of this Green estimate are as follows.  Outside a fixed compact set,
the normalized contribution of every positive edge is \(O(u^{-1})\),
whereas a descending or killed edge from the unique maximal-degree source
has probability bounded below.  A bounded positive jump \(j\le2\) costs
only \(O(u^{\theta j})\), and hence

\[
 {Q_nF_\theta(u)\over F_\theta(u)}
 \le C u^{-\theta}+C u^{-1+2\theta}+o(1)<1.                    \tag{2.2a}
\]

On the remaining finite set, normalize the exact effective hazards by
their smallest feasible cofactor power.  The resulting matrices converge,
uniformly when the active coordinate is \(n+O(L_n)\), to finite
substochastic matrices carrying the same positive strong-cut paths.  No
equality-only class is closed.  Therefore some fixed number of steps has
killing probability at least \(\eta>0\), uniformly for all large \(n\).
This finite strong-cut minorization, joined to (2.2a) by a bounded
corrector, proves (2.2).  Applying the same drift to polynomial weights,
and then to the usual marked kernels, gives every fixed moment of the
killed macro count.

After

\[
                           q=m_a(u)+1\le3                        \tag{2.3}
\]

strict \(H_a\)-drops,

\[
 V_q+m_a(U_q)\le n+m_a(u)-q\le n-1.                             \tag{2.4}
\]

Thus the raw physical path has already crossed \(V=n-1\), and its first
such crossing is \(D\).  This proves strict old-debt service for the ideal
trace; the proof corrector is not added to the physical Lyapunov function.

## 3. Weighted defects and boundary

The ordered-Green theorem gives, at each occupied base and for every fixed
\(p\),

\[
 \mathbb E[(1+U_E+I_E+|V_E-n|)^p;E\mid U=u_b]
 \le {C_p(1+u_b)^{p+3}\over n}.                                 \tag{3.1}
\]

Integrating (3.1) through at most three killed equality Green episodes by
(2.2) yields

\[
 \mathbb E[(1+U_E+I_E+|V_E-n|)^p;E]
 \le {C_p(1+u)^{c_p}\over n}=n^{-1+o(1)}.                       \tag{3.2}
\]

The proper carrier product, the factorial equality Green bound, and the
worst \(n^2\) level-zero trial amplification give, for
\(0<\theta'<\theta<1/2\),

\[
 \mathbb P(B)
 \le C{F_\theta(u)\over F_{\theta'}(L_n-C)}
 +Cn^2(1+u)^C
   \sum_{j\ge L_n-C}{[C(1+L_n)^a/n]^j\over j!}.                 \tag{3.3}
\]

This is \(O(n^{-M})\) for every fixed \(M\).  Equations (2.4), (3.2), and
(3.3) therefore imply

\[
                           \mathbb P(D)=1-n^{-1+o(1)}.           \tag{3.4}
\]

Every endpoint in (3.2)--(3.3) includes its boundary-causing reaction.

## 4. Physical duration and endpoint moments

Per unit level-zero local time, the next lower macro is exponential with
the sum of the exact killed effective rates.  At every nonstatic base the
structural argument in Section 1 supplies a feasible source with
cofactor degree at most two.  The exact product and the ordered-Green
relative error therefore give

\[
             \sum_e\widehat A_e(u,v)\ge c n^{-2},
 \qquad
             \mathbb E_u T_0^p\le C_p n^{2p},                  \tag{4.1}
\]

where \(T_0\) is the level-zero local time accumulated before the next
lower macro.  A completed proper excursion, conditional on its opening,
has physical-time moments at most \(C_p n^{-p}(1+u)^{c_p}\): its death
clock is at least \(cni\), while its birth/death ratio below the cutoff is
\(o(1)\).  Openings form a Poisson process of rate at most
\(C(1+u)^a\) in level-zero local time.  The compound-Poisson moment formula
applied conditionally on \(T_0\) consequently gives, for the duration
\(\eta\) of one fully contracted macro,

\[
 b_p(u):=\mathbb E_u\eta^p\le C_pn^{2p}(1+u)^{c_p}.             \tag{4.2}
\]

It remains to sum physical time over the whole killed equality trace; a
first-moment occupation bound alone would not justify this step.  Define

\[
 M_jf(u)=\mathbb E_u[\eta^j f(U');\ \Delta H_a=0]
\]

for one leading-clean macro, and let \(m_p(u)\) be the \(p\)-th moment of
the duration until its first strict drop.  Bounded macro displacement,
the preceding compound-Poisson estimate, and the carrier factorial tail
give, for every polynomial weight \(w_r(u)=(1+u)^r\),

\[
                         M_jw_r(u)
 \le C_{j,r}n^{2j}w_{r+c_{j,r}}(u).                             \tag{4.3}
\]

Expanding \((\eta+\sigma'\mathbf1_{\{\Delta H_a=0\}})^p\) gives the exact
additive-functional recursion

\[
 (I-Q_n)m_p
 =b_p+
   \sum_{j=1}^{p-1}{p\choose j}M_jm_{p-j}.                     \tag{4.4}
\]

Starting with \(p=1\), induction in \(p\), (4.2)--(4.3), and the
polynomial Green bound (2.2) prove

\[
 \mathbb E_u\sigma_{\mathrm{drop}}^p
 \le C_pn^{2p}(1+u)^{c_p}.                                    \tag{4.5}
\]

There are at most three strict-drop episodes.  Their starting endpoints
have polynomial moments by the same Green recursion, so the strong Markov
property and (4.5) yield

\[
 \mathbb E\sigma^p\le C_pn^{2p}(1+u)^{c_p}=n^{2p+o(1)}.         \tag{4.6}
\]

For later use we record the endpoint form carefully.  On the ideal event
\(D\), the polynomial Green bound and the carrier factorial tail give
polynomial moments in \(1+u\).  On \(E\), the corresponding
event-weighted moments are (3.2).  At the first included boundary firing,

\[
 U_B+I_B+|V_B-n|\le3L_n+C,                                    \tag{4.7}
\]

because all reaction vectors are bounded.  Combining (3.2)--(3.3) with
these three alternatives proves, for every fixed \(p\),

\[
 \mathbb E(1+U_\sigma+I_\sigma+|V_\sigma-n|)^p
 \le C_p(1+u)^{c_p}.                                           \tag{4.8}
\]

## 5. Entropy of the actual service endpoint

Fix the common chart vector \(\ell\) and put

\[
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                                      \tag{5.1}
\]

For the spectator factorial component
\(B_\ell(u)=\log(u!)+\ell_Uu\), we retain the actual strict-drop endpoint.
Let \(Q\) be one episode's equality continuation kernel and \(S\) its
strict-drop kernel.  Put

\[
                 h_C(u)=B_\ell(u)+C\log(u+e).                   \tag{5.2}
\]

For sufficiently large \(C\), the maximal-degree cut used in (2.2) gives

\[
                    Qh_C(u)+SB_\ell(u)-h_C(u)<0                 \tag{5.3}
\]

outside a finite set.  To see the sign without hiding the terminal cost,
let \(d\) be the maximal feasible source degree.  If a degree-\(d\)
strict-drop edge is present, its bounded spectator jump costs at most
\(j_*\log(u+e)+O(1)\) in \(B_\ell\), while termination omits the
\(C\log(u+e)\) part of \(h_C\); choose \(C>j_*\).  If there is no such
edge, the strong cut supplies a degree-\(d\) descending continuation, whose
factorial increment is \(-c\log(u+e)+O(1)\).  Every positive edge has
degree at most \(d-1\), so its total normalized contribution is only
\(O(u^{-1}\log(u+e))\).  The case \(d=0\) has no positive lower-degree
edge.  These alternatives prove (5.3).

Let

\[
 g(u)=[Qh_C(u)+SB_\ell(u)-h_C(u)]_+,
 \qquad \chi=(I-Q)^{-1}g.                                     \tag{5.4}
\]

The support of \(g\) is finite, and the uniform compact minorization in
Section 2 makes \(\chi\) bounded.  Therefore

\[
 Q(h_C+\chi)+SB_\ell-(h_C+\chi)\le0.                           \tag{5.5}
\]

Iteration, followed by at most three strong-Markov restarts, yields

\[
 \mathbb E[B_\ell(U_D)-B_\ell(u);D]
 \le C\log(u+e)+C+o(\log n).                                  \tag{5.6}
\]

The final term accounts for defects and boundaries and is justified below;
it is not placed inside the ideal \(Q/S\) corrector.  Thus (5.6) retains
the actual physical endpoints and asserts no pathwise entropy descent.

On \(D\), the first crossing has \(V=n-1\), so the old-active factorial
increment is exactly \(-\log n\).  The carrier size-biased factorial law
gives

\[
 \mathbb E[\log(I_D!)+|\ell_I|I_D;D]
 \le C+n^{-1+o(1)}.                                            \tag{5.7}
\]

Since \(\log u=o(\log n)\), (5.6)--(5.7) make every non-active mean cost
on \(D\) equal to \(o(\log n)\).  On \(E\), the elementary bound

\[
 |\Delta G_\ell|^r
 \le C_r\log^r(n+L_n+e)
       (1+U_E+I_E+|V_E-n|)^{2r}                                \tag{5.8}
\]

and (3.2), used with moment order \(2r\), give

\[
                         \mathbb E[|\Delta G_\ell|^r;E]
 \le n^{-1+o(1)}.                                              \tag{5.9}
\]

On \(B\), the deterministic first-crossing cap (4.7) and the
superpolynomial estimate (3.3) give, for every prescribed \(M\),

\[
                         \mathbb E[|\Delta G_\ell|^r;B]
 \le C_r(L_n\log n)^{2r}\mathbb P(B)=O(n^{-M}).                \tag{5.10}
\]

Taking \(r=1\) in (5.9)--(5.10) proves the deferred
\(o(\log n)\) term in (5.6).  Consequently

\[
 \mathbb E[\Delta G_\ell+{\bf1}_D\log n]\le o(\log n),
 \qquad
 \mathbb E\Delta G_\ell\le-\log n+o(\log n).                 \tag{5.11}
\]

On the ideal part of \(D\), the polynomial equality Green bound and the
carrier factorial law show that every fixed moment of the spectator and
cofactor factorial increments is \(n^{o(1)}\); also
\(|\log((n+j)!/n!)|\le C(1+|j|)\log(n+|j|+e)\).  Combining this with
(5.9)--(5.10), for every fixed \(r\), gives

\[
                       \mathbb E|\Delta G_\ell|^r=n^{o(1)}.    \tag{5.12}
\]

The signs in (5.11) are inequalities: additional spectator descent only
helps.

## 6. Common fourth-power drift

At the starting base, \(G_\ell(x)=\Theta(n\log n)\).  The exact expansion

\[
 \Delta W_\ell
 =4G_\ell^3\Delta G_\ell+6G_\ell^2(\Delta G_\ell)^2
  +4G_\ell(\Delta G_\ell)^3+(\Delta G_\ell)^4                  \tag{6.1}
\]

and (5.11)--(5.12) show that the final three terms are
\(o(G_\ell^3\log n)\).  The physical-time reward in (4.6) is
\(n^{2+o(1)}=o(G_\ell^3\log n)\).  Therefore

\[
 \mathbb E_x[W_\ell(X_\sigma)-W_\ell(x)+\sigma]
 \le-cG_\ell(x)^3\log n                                      \tag{6.2}
\]

for all large \(n\).

### Exact-pair stopped-block theorem

For all seventeen exact proper-pair supports, every strong orientation,
every fixed positive rate vector, every fixed common \(\ell\), and every
historically reachable positive-\(D_V\) start (1.1), the physical stopping
rule of Section 1 has:

- strict old-active service with probability \(1-n^{-1+o(1)}\);
- arbitrary fixed endpoint moments;
- physical duration \(n^{2+o(1)}\);
- superpolynomial included-boundary probability;
- the actual-endpoint entropy estimate (5.11); and
- the common-fourth-power Foster estimate (6.2).

The theorem is local to the seventeen exact pairs.  It changes no pair or
global certification flag until independently audited and composed with the
remaining hard templates under the path-labelled marked interface.
