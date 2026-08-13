# Neutral-face classification and the missing service estimate for the 336 family

**Hostile proof-first structural audit, 2026-08-12 PDT.**  This note isolates
what follows symbolically from the level-set hypotheses

\[
 h\cdot y=2s\quad(y\in T),\qquad
 R=\{0\}\cup U,\quad h\cdot u=s\quad(u\in U),
\]

with \(h>0\), \(\operatorname{rank}\operatorname{span}(T-T)=2\), and
strongly connected orientations on \(T\) and \(R\).  It proves an exact
classification of neutral \(T\)-faces and qualitative access to an
\(R\)-death.  It also gives two explicit networks showing that neither the
next workload event nor the number of neutral reactions has a uniform
one-step bound.  No recurrence conclusion is asserted.

## 1. Proper coordinate faces

For a set of species \(P\), let

\[
 {\cal F}_P=\{x:x_i=0\text{ for }i\notin P\},\qquad
 T_P=\{y\in T:\operatorname{supp}y\subseteq P\}.
\]

At a relative-interior population of this face with every present
coordinate at least two, the enabled \(T\)-sources are exactly \(T_P\).

> **Lemma 1.1 (dead-or-leaking face).**  If \(P\) is a proper subset of the
> three species, then exactly one of the following holds:
>
> 1. \(T_P=\varnothing\), and every \(T\)-clock is disabled on the relative
>    interior of \({\cal F}_P\);
> 2. \(T_P\ne\varnothing\), and a \(T\)-reaction accessible from the face
>    produces a species outside \(P\).
>
> In particular, no proper face supports an active forward-invariant
> \(T\)-network.

### Proof

If \(T_P\) is nonempty and proper, choose \(y\in T_P\) and
\(z\in T\) with \(z\notin T_P\).  A directed path from \(y\) to \(z\) exists by
strong connectivity.  The first edge on this path which leaves \(T_P\) has
an enabled source supported in \(P\) and a target containing a species
outside \(P\).

It remains to rule out \(T_P=T\).  If every complex of \(T\) were supported
in the proper set \(P\), every difference \(y-z\) would lie both in the
coordinate subspace on \(P\) and in the hyperplane \(h\cdot v=0\).  Since
\(|P|\le2\) and the restriction of \(h\) to \(P\) is strictly positive,
this intersection has dimension at most \(|P|-1\le1\), contradicting the
rank-two hypothesis. \(\square\)

For a padded boundary phase, a source supported in \(P\) can still be
disabled because a pure quadratic needs two copies.  Those exceptional
low-count phases belong to the dead alternative after replacing \(T_P\) by
the set of sources enabled at that phase.  Along an escaping dead ray, all
large mass is consequently carried by species which do not by themselves
enable a unary or pure-quadratic \(T\)-source; every possible activation
needs one of finitely many bounded tokens.

There are two useful exact corollaries for the 336 weights.

* For \(h=(1,1,1)\), fix a species \(i\).  The complexes supported on the
  opposite face are \(\{2j,j+k,2k\}\).  If none belongs to \(T\), then
  \(T\subseteq\{2i,i+j,i+k\}\); rank two forces equality.  Hence
  \[
                         T=\{2i,i+j,i+k\}                 \tag{1.1}
  \]
  is the unique support shape for which the whole face \(x_i=0\) is
  \(T\)-dead.
* For \(h=(1,1,2)\), the lower linkage is
  \(R=\{0,A,B\}\) and
  \(T\subseteq\{2A,A+B,2B,C\}\).  The face \(x_A=0\) contains the possible
  \(T\)-sources \(2B,C\).  If both were absent, \(T\) would lie in
  \(\{2A,A+B\}\) and have rank at most one.  Thus every \(A\)-death face
  leaks; the same argument applies to \(B\).  On the pure \(C\)-ray,
  either \(C\in T\) is a unary activation source, or \(C\notin T\) and the
  \(C\)-coordinate is an exact full-network invariant, because \(C\notin R\).

## 2. Qualitative access to a death

Let

\[
 D=\{u\in U:\text{some labelled edge }u\to0\text{ is present}\}.
\]

The set \(D\) is nonempty: take the last edge of a directed \(R\)-path from
any unary vertex to zero.

Fix \(d\in D\).  On the face \(x_d=0\), Lemma 1.1 gives an exact
dichotomy.

1. If a \(T\)-source is enabled, a finite directed \(T\)-path has a first
   edge which creates \(d\).
2. If no \(T\)-source is enabled, strong connectivity of \(R\) supplies a
   finite path

   \[
                         0\longrightarrow\cdots\longrightarrow d
                         \longrightarrow0.
   \]

   The first edge is a constant-source birth and the intervening unary
   targets carry the token needed for the next edge.

Thus every population has a finite positive-probability physical path to a
death event, unless the death is already enabled.  This is only
**qualitative access**.  Competing \(T\)-clocks can make the probability of
a specified label word vanish, and its neutral reaction count need not be
uniformly integrable.  Consequently this face lemma does not supply the
rate-weighted service estimate required for recurrence.

## 3. Immediate upward workload is possible

Take \(h=(1,1,1)\), \(s=1\), and

\[
 R=\{0,A,C\},\qquad
 T=\{A+B,B+C,A+C\}.
\]

Orient \(R\) as

\[
                         0\to C\to A\to0
\]

and orient \(T\) by any directed three-cycle.  The complexes of \(T\) all
have \(H\)-level two and their affine differences have rank two.  At

\[
                         x=(0,n,0)
\]

no \(T\)-source and no death source is enabled.  The next
population-changing reaction is therefore certainly \(0\to C\), so

\[
                         H(X_{\tau_1})-H(x)=+1.
\]

This refutes any proposed theorem saying that the next \(H\)-changing event
has uniformly negative drift at high workload.  A valid stopped theorem
must include the constant-source activation prelude.

## 4. Neutral reaction depth can diverge

Again take \(h=(1,1,1)\), orient \(R=\{0,A,C\}\) by
\(0\to C\to A\to0\), and let \(A\to0\) be the chosen death edge.  Put

\[
                         T=\{2B,A+B,A+C\}
\]

and include the strongly connected labelled edges

\[
 2B\to A+B,\qquad A+B\to2B,\qquad
 A+B\to A+C,\qquad A+C\to2B.
\]

Starting from \((0,n,0)\), the \(2B\)-source has rate of order \(n^2\).
Fix a sufficiently small \(c>0\).  During the first \(cn\) reactions, any
binary displacement changes \(B\) by at most two, so \(B\ge n/2\) on every
path consisting only of \(T\)-reactions.  The \(2B\)-clock alone then keeps
the aggregate \(T\)-rate above \(c_1n^2\).  The aggregate \(R\)-rate is at
most \(c_2n\), since \(R\) has only a constant source and unary sources and
the total workload is still \(n\).  Conditional at each of the first
\(cn\) steps,

\[
 {\mathbb P}\{\text{the next reaction belongs to }R\}
 \le {C\over n}.
\]

Consequently the probability that the first \(cn\) reactions all belong to
\(T\) is at least \((1-C/n)^{cn}\), which stays bounded away from zero
(after reducing \(c\) if necessary).  On this event no death has occurred
and the neutral reaction count is order \(n\).  Those \(cn\) reactions have
physical duration of order \(1/n\), because their hazards are order
\(n^2\).  Thus the number of \(T\)-reactions before service has no uniform
geometric tail even though the corresponding physical time is short.

## 5. Exact averaging for the exceptional common-catalyst support

The exceptional support singled out by a dead coordinate face has an exact
finite-state reduction.  Let

\[
                  T=\{2i,i+j,i+k\},\qquad h=(1,1,1).
\]

On the active region \(x_i\ge1\), set

\[
                  z_i=x_i-1,\qquad z_j=x_j,\qquad z_k=x_k.
\]

Every \(T\)-source propensity has the common catalyst factor \(x_i\):

\[
 (x)_{2i}=x_i z_i,\qquad
 (x)_{i+j}=x_i z_j,\qquad
 (x)_{i+k}=x_i z_k.                                      \tag{5.1}
\]

After removing that factor, an edge between two complexes of \(T\) is
exactly a unary conversion between the corresponding vertices
\(\{i,j,k\}\).  Thus

\[
                            {\cal L}_T=x_i{\cal L}_{\rm lin}, \tag{5.2}
\]

where \({\cal L}_{\rm lin}\) is the generator of \(N-1\) independent
particles moving on the strongly connected three-vertex labelled graph
inherited from \(T\).  The last \(i\)-particle is a persistent catalyst for
the \(T\)-dynamics.

Let \(\pi\) be the strictly positive invariant law of one particle and let
\(\mu_N\) be the multinomial law with \(N-1\) trials and cell probabilities
\(\pi\).  The invariant law of the physical \(T\)-chain is not quite
\(\mu_N\), because (5.2) is a state-dependent time change.  It is exactly

\[
 \nu_N(z)={1\over Z_N}\,{\mu_N(z)\over1+z_i},\qquad
 Z_N=\sum_z{\mu_N(z)\over1+z_i}.                            \tag{5.3}
\]

Indeed, \(\nu_N(z)(1+z_i)=Z_N^{-1}\mu_N(z)\), so stationarity follows
immediately from that of \(\mu_N\) for \({\cal L}_{\rm lin}\).

Multinomial concentration shows that, with probability
\(1-e^{-cN}\), every \(z_\ell\) lies between fixed positive multiples of
\(N\).  On this event \((1+z_i)^{-1}\) is also between fixed multiples of
\(N^{-1}\), while the exceptional-event contribution to (5.3) is at most
exponentially small.  Consequently

\[
                  {\mathbb E}_{\nu_N}x_\ell=\Theta(N)
                  \qquad(\ell=i,j,k).                       \tag{5.4}
\]

Thus every possible \(R\)-death species has linear stationary exposure in
the active neutral class, for every strong orientation and positive rate
vector.  On the face \(x_i=0\), \(T\) is dead.  If \(i\notin U\), that face
is \(T\)-invariant and the open linear \(R\)-subsystem acts on \(U\); if
\(i\in U\), a strong \(R\)-path from zero supplies a constant-source
activation of the catalyst.

Equations (5.1)--(5.4) solve the frozen-\(H\) invariant-law part of the
exceptional face.  They do not alone justify replacing the evolving
full-network phase by \(\nu_N\): a stopped proof still has to control the
pre-mixing interval and the \(R\)-events occurring during it.

## 6. Exact missing theorem

The symbolic hypotheses prove death accessibility but not its
rate-weighted use.  A classwise same-\(H\) closure needs a stopped
activation/service theorem of the following strength.

> For every arbitrary positive labelled rate vector and every closed fixed
> class of a level-set network, construct physical stopping times which
> retain the complete constant-birth activation and the possibly
> unbounded-count \(H\)-neutral \(T\)-phase, and prove a proper
> single-workload Foster inequality outside a finite set.  Equivalently,
> prove a uniform lower estimate on accumulated death hazard after
> contracting each finite-\(H\) neutral class, with an error strictly
> dominated by the constant \(0\)-source birth intensity.

A stationary finite-state averaging lemma would have to be quantitative,
not merely qualitative.  At minimum it must show that every active closed
\(T\)-class on workload level \(N\) exposes a death species at a rate
tending to infinity with \(N\), and it must separately control activation
from the \(T\)-dead strata.  Because the neutral mixing reaction count can
grow with \(N\), a proof must work in physical time or by an exact
source-layer Green contraction.

The common-catalyst calculation in Section 5 supplies this invariant-law
estimate for its exceptional active class, but not yet the required stopped
full-network estimate.  Until such a theorem is proved, the global 336 branch remains a
load-bearing classwise gap.  The dead-or-leaking face lemma rules out a
structural siphon obstruction, but it does not close the stochastic
rate-weighted interface.

## 7. A valid quadratic corrector, and what it does not prove

There is a useful pointwise estimate behind a proposed global repair.  Fix a
unary \(d\in D\), and let

\[
 \delta_d=\sum_{d\to0}\kappa_{d0}>0,
 \qquad V_\epsilon(x)=H(x)^2-\epsilon x_d .             \tag{7.1}
\]

An additive constant makes \(V_\epsilon\) nonnegative, and it is proper for
every fixed sufficiently small \(\epsilon>0\), because
\(x_d\le H/s\).  The correction is deliberately only linear in \(x_d\).
Every \(T\)-reaction preserves \(H\), and every \(T\)-edge which decreases
\(x_d\) has a binary source containing \(d\).  Consequently

\[
                    -{\cal L}_T x_d\le C_Tx_d(1+H),      \tag{7.2}
\]

for a constant depending only on the fixed labelled network.  In particular,
the possibly quadratic neutral clock contributes at most

\[
                    {\cal L}_TV_\epsilon
                    \le\epsilon C_Tx_d(1+H).             \tag{7.3}
\]

The \(d\to0\) reactions have the exact increment

\[
 V_\epsilon(x-d)-V_\epsilon(x)
       =-2sH+s^2+\epsilon.                               \tag{7.4}
\]

All zero-source births together cost at most \(2s\beta_0H+C\), where
\(\beta_0\) is their aggregate rate.  Unary transfers preserve \(H\) and
their adverse correction is \(O(\epsilon x_d)\); deaths of other unary
species are favorable apart from a bounded lower-order term.  Hence

\[
 {\cal L}V_\epsilon(x)
 \le 2s\beta_0H+C
      -\bigl(2s\delta_d-\epsilon C_T\bigr)Hx_d+C'x_d .   \tag{7.5}
\]

Choose first \(\epsilon<s\delta_d/C_T\), with the evident interpretation
when \(C_T=0\), and then a fixed integer \(K\) large enough.  Equation
(7.5) proves

\[
             {\cal L}V_\epsilon(x)\le-cH
             \quad\hbox{when }H\text{ is large and }x_d\ge K. \tag{7.6}
\]

Thus the proposed corrector is not the obstruction: it gives a clean common
physical-time generator branch above a fixed service threshold, including
all \(R\)- and \(T\)-clocks.

What remains is not merely to *hit* that threshold.  A constant-source birth
has

\[
                    \Delta H^2=2sH+s^2,                 \tag{7.7}
\]

whereas reaching \(x_d=K\) changes the correction in (7.1) by only
\(-\epsilon K=O(1)\).  Therefore a prelude which stops upon first hitting
\(K\) cannot by that fact alone pay even one activation birth at scale \(H\).
After establishment it must retain enough occupation above the threshold,
or enough actual \(d\to0\) deaths, to offset every preceding birth.  A
sufficient quantitative output would be a stopped estimate of the form

\[
 {\mathbb E}_x\!\int_0^\tau H(X_t)x_d(t)\,dt
       \ge \theta H(x)\,{\mathbb E}_x B_\tau+\theta_0H(x), \tag{7.8}
\]

up to controlled shell errors, or the equivalent negative macroincrement
for \(V_\epsilon\).  Here \(B_\tau\) counts all zero-source births.  Merely
giving a positive probability of hitting \(K\) is weaker than (7.8), since
\(T\) can immediately move mass out of \(d\).

Nor may the fixed-\(K\) estimate be justified by a prescribed bounded label
word.  For example, take

\[
 h=(1,1,1),\qquad T=\{2A,2B,2C\},
\]

with a strong orientation containing \(2B\to2C\) and \(2C\to2A\), and
start at \((0,n,0)\).  After the prescribed first edge \(2B\to2C\), the
\(2C\)-source has order-one propensity while the still-enabled \(2B\)-source
has order \(n^2\).  The conditional probability that the prescribed
\(2C\to2A\) label fires next is therefore \(O(n^{-2})\).  Activation may
still occur through an aggregate avalanche, but no uniform fixed-word
probability follows from strong connectivity.

The exact remaining repair is consequently an aggregate stopped
establishment-and-service lemma: it must contract fast neutral competitors
or use a dyadic/physical-time argument, retain repeated extinction and
reseeding attempts, count all births and deaths, and yield (7.8) or an
equivalent Foster decrement.  Equations (7.1)--(7.6) then provide a valid
common potential for the handoff; they do not replace that lemma.

## 8. Nonenumerative reduction of the missing activation theorem

The finite support family admits a much smaller symbolic reduction than 336
separate cases.  This reduction does not prove the stopped estimates, but it
identifies their exact universal kernels.

### 8.1 The homogeneous shell

Take \(h=(1,1,1)\), and examine a dormant pure-\(X\) ray.  Write the other
species as \(Y,Z\).  If \(2X\in T\), the ray already enables a quadratic
\(T\)-source and is not dormant.  Suppose therefore that \(2X\notin T\).
Rank two forces at least one of \(XY,XZ\) to belong to \(T\): otherwise
\(T\subseteq\{2Y,YZ,2Z\}\), whose affine rank is at most one.

Up to exchanging \(Y,Z\), exactly one of the following three symbolic
geometries occurs.

1. **Two carriers:** \(XY,XZ\in T\).  Regard these two complexes as carrier
   types \(Y,Z\).  Kill the two-state carrier graph on its first edge into
   the pure-mutant set \(\{2Y,YZ,2Z\}\).  No nonempty carrier subset can be
   closed, by strong connectivity of \(T\), so its killed generator \(Q\)
   is transient.  As in the standard killed-carrier construction, put
   \(g=(-Q)^{-1}{\bf1}\) and choose
   \(v_i=1-\rho g_i>0\) for sufficiently small \(\rho>0\).  Then
   \[
                    R=v_YY+v_ZZ
   \]
   has a fixed positive rate-weighted reward at either carrier source.
   Pure-mutant sources have total rate \(O((Y+Z)^2)\).  Hence, while
   \(Y+Z\le\eta X\),
   \[
                  {\cal L}_T R\ge cXR-C R^2 .          \tag{8.1}
   \]
   An \(R\)-linkage reaction sourced at the bulk \(X\) either lowers \(H\)
   or creates transverse mass, while every adverse \(R\)-linkage
   contribution is sourced in \(Y,Z\) and is \(O(1+R)\).  Thus (8.1) is
   the exact two-carrier PF wedge, with all lower clocks retained.

2. **One carrier and the opposite pure double:** \(XY\in T\),
   \(XZ\notin T\), and \(2Z\in T\).  Put
   \[
                             R=2Y+Z.                   \tag{8.2}
   \]
   The minimum-height source class is exactly
   \(\{XY,2Z\}\); the only possible higher sources are \(YZ,2Y\).
   On a dyadic band \(K\le R\asymp r\le\eta H\),
   \[
   \lambda_{\min}\ge
       c\{XY+Z(Z-1)\}\ge cr^2,                         \tag{8.3}
   \]
   whereas the aggregate higher-source and adverse lower rate divided by
   \(\lambda_{\min}\) is at most
   \[
                             C(\eta+K^{-1}).           \tag{8.4}
   \]
   If one minimum vertex has no direct edge to the higher class, every
   reaction from it goes to the other minimum vertex.  Nonnegativity of
   \(Y,Z\) then gives the same two pathwise source-balance inequalities as
   the dyadic compound-activation lemma: after an \(O(r)\) debit, a fixed
   fraction of minimum-source firings comes from a direct-cut source.
   Conditional on such a firing, the cut probability is a fixed positive
   rate ratio.  Thus the already isolated aggregate-source argument, not a
   bounded label word, is the exact analytic kernel required here.

3. **One carrier and no opposite pure double:** \(XY\in T\),
   \(XZ,2Z\notin T\).  The only remaining possible vertices are
   \(XY,YZ,2Y\), and rank two forces the exact equality
   \[
                              T=\{XY,YZ,2Y\}.           \tag{8.5}
   \]
   This is the common-catalyst support with catalyst \(Y\).  On \(Y\ge1\),
   set \(z_Y=Y-1,z_X=X,z_Z=Z\).  The three source propensities factor as
   \[
   (x)_{XY}=Yz_X,\qquad (x)_{YZ}=Yz_Z,\qquad
   (x)_{2Y}=Yz_Y,                                      \tag{8.6}
   \]
   so \({\cal L}_T=Y{\cal L}_{\rm lin}\) for \(H-1\) independent particles
   on the strong three-vertex unary graph.  On \(Y=0\), \(T\) is dead.  If
   \(Y\) is absent from the lower unary support, that face is a full-network
   invariant and the fixed class reduces to an open linear subsystem; if it
   is present, the lower graph supplies the physical catalyst seed.

These cases and their coordinate swaps are exhaustive.  They reduce the
homogeneous stopped theorem to the already recognizable PF wedge, dyadic
two-minimum balance, and common-catalyst kernels.  What is still required
for a global theorem is their common birth/death ledger and common-potential
endpoint, not another support or orientation table.

### 8.2 The anisotropic shell

After a coordinate permutation, the only other weight is
\(h=(1,1,2)\).  Write the species as \(A,B,C\).  The level-two shell is
\[
                         \{2A,A+B,2B,C\}.              \tag{8.7}
\]
All quadratic vertices lie on an affine line.  Therefore rank two is
equivalent to
\[
               T=\{C\}\cup Q,\qquad
               Q\subseteq\{2A,A+B,2B\},\quad |Q|\ge2,  \tag{8.8}
\]
and the lower support is exactly \(\{0,A,B\}\).

There is an elementary first activation layer.  Put
\[
                     S=A+B,\qquad H=S+2C.
\]
Every \(C\)-sourced reaction raises \(S\) by two, every
quadratic-to-\(C\) reaction lowers it by two, and quadratic-shell
reactions preserve it.  Since \(C\) has a positive outgoing rate,
\[
            {\cal L}S\ge a(H-S)-KS^2-K_RS.             \tag{8.9}
\]
In particular, for sufficiently small fixed \(\eta>0\),
\({\cal L}S\ge cH\) on \(S\le\eta\sqrt H\), for large \(H\).  Applying the
generator to \(e^{-\theta S}\), rather than using positive drift alone,
gives the corresponding stopped ascent to the \(\sqrt H\) scale: the
upward \(C\)-clock has order \(H\), the quadratic downward clock is at most
\(K\eta^2H\), and adverse lower clocks are \(O(\sqrt H)\).

The second layer, exposure of a specified death species, contains the
remaining anisotropic obstruction.  Let the death be \(A\).  When \(A\) is
small, the zero-\(A\) complex class is
\[
                         P=\{C\}\cup(\{2B\}\cap T).     \tag{8.10}
\]
Strong connectivity guarantees an edge path from \(P\) to an
\(A\)-containing complex, but it does **not** give a pointwise lower bound
on the cut clock.  For instance, the only cut may be sourced at \(C\).
Starting with \(C=0\) and \(B\asymp H\), a \(2B\to C\) clock then has order
\(H^2\), while the first newly created \(C\)-clock has only order one.
The probability of taking that cut on the next reaction can vanish.

The required replacement is a two-reservoir killed-transfer lemma for the
source propensities
\[
                              C,\qquad B(B-1).          \tag{8.11}
\]
If \(C\) has no direct cut, every \(C\)-reaction goes to \(2B\); if \(2B\)
has no direct cut, every \(2B\)-reaction goes to \(C\); at least one of the
two sources has a direct cut.  Internal firings transfer exactly one
\(C\)-token against two \(B\)-tokens.  A valid proof must use this population
balance or its killed-resolvent equivalent over the whole conversion block.
It must allow order-\(H\) neutral firings when the initial reservoir is on
the wrong side, whose physical duration is nevertheless small, and must
retain all \(A\)-sourced losses and lower clocks.  The desired conclusion is
stopped ascent to \(A\ge\delta\sqrt H\), or an already favorable workload
death, with a complete birth/death ledger.

Thus (8.9) closes the first anisotropic layer, but the two-reservoir lemma
for (8.11) is load-bearing.  Any proof which replaces it by a fixed path or
by “strong connectivity gives an order-\(H\) exit” repeats the exact
fixed-word error from Section 7.

## 9. A common marked potential on the all-active chart

There is a separate way to remove the **all-active** \(H\)-versus-factorial
potential switch.  It does not close the dormant boundary prelude, but it
does show that no averaging theorem is needed inside the all-active chart.

Carry the actual target mark \(t\), and use the exact marked factorial
\[
                 F(x,t)=\sum_i\log((x_i-t_i)!).
\]
Let \(\Lambda(x)\) be the total labelled hazard.  The one-jump identity gives
\[
                         {\cal L}F(x,t)=\Lambda(x)D(x,t),
 \qquad D(x,t)\le C_F.                                  \tag{9.1}
\]
Fix a unary \(d\) having a labelled edge to zero, and put
\[
                         V_\epsilon(x,t)=H(x)^2+\epsilon F(x,t). \tag{9.2}
\]
This is one proper function on the marked space.

The lower linkage changes \(H\) only at zero-source births and unary deaths.
Consequently
\[
                         {\cal L}H^2\le C H-cHx_d+C.     \tag{9.3}
\]
Fix a large constant \(M\).  On the region
\[
                         \Lambda\le M Hx_d,             \tag{9.4}
\]
equations (9.1)--(9.3) give
\[
 {\cal L}V_\epsilon
       \le CH-\{c-\epsilon C_FM\}Hx_d+C.                \tag{9.5}
\]
Choose \(\epsilon<c/(2C_FM)\).  Along an all-active escaping sequence,
\(x_d\to\infty\), so (9.5) tends to minus infinity.

It remains to treat
\[
                         \Lambda>MHx_d.                 \tag{9.6}
\]
The upper linkage \(T\) contains a complex involving \(d\).  Otherwise all
of \(T\) would be supported on the other two species and, because it lies on
one positive \(h\)-level, its affine rank would be at most one.  Fix one
such complex \(c_T\).  In the lower linkage fix \(c_R=d\).  Their source
rates obey
\[
       \lambda_{c_T}(x)\le C Hx_d,\qquad
       \lambda_{c_R}(x)\le Cx_d.                       \tag{9.7}
\]
Strong connectivity supplies a simple directed path from every actual
target mark in either linkage to the corresponding \(c_T\) or \(c_R\).
Thus (9.6)--(9.7) place both marked target paths in the quantitative
available regime:
\[
                  p_{c_T}\le C/M,\qquad p_{c_R}\le C/(MH). \tag{9.8}
\]

The finite all-clock Bellman recursion has the following immediate
quantitative consequence.  If a terminal source probability is at most
\(\delta\), the supremum of its expected \(F\)-reward over the finite path
menu is at most \(-A(\delta)\), where
\[
                              A(\delta)\longrightarrow\infty
                              \quad(\delta\downarrow0).  \tag{9.9}
\]
Indeed, failure of (9.9) would give a sequence with terminal probability
tending to zero but Bellman reward bounded below, contradicting the exact
first-vanishing-source recursion.  This is compactness over a finite path
menu, not an orientation or population enumeration.

Choose \(M\) so that the right side of (9.9), with
\(\delta=C/M\), is strictly negative.  Along a designated path of bounded
length from an all-active state, every coordinate changes by \(O(1)\);
therefore all enabled falling factorials, \(\Lambda\), \(H\), and \(x_d\)
change by relative \(1+o(1)\).  The only positive change of \(H^2\) is a
zero-source birth.  At every path stage its expected contribution is
\[
             (2sH+O(1))p_0\le {CH\over\Lambda}
                         \le {C\over Mx_d}=o(1).        \tag{9.10}
\]
The episode has bounded depth.  Equations (9.8)--(9.10) therefore give
\[
             {\mathbb E}\{V_\epsilon(X_\tau,T_\tau)
                         -V_\epsilon(x,t)\}\le
                    -\tfrac12\epsilon A(C/M)<0          \tag{9.11}
\]
outside a finite subset of the all-active chart, unless a designated
physical jump records a chart exit.  Every competing clock is included by
the marked Bellman identity.

Equations (9.5) and (9.11) prove a common-\(V_\epsilon\)
negative-or-exit theorem on the whole all-active level-set chart.  The
argument is sequentially exhaustive: the ratio
\(\Lambda/(Hx_d)\) is either at most the fixed \(M\), or it is in (9.6).

This does **not** by itself complete the global chart cover.  On an
escaping dormant face it is possible that \(\Lambda=O(1)\).  One
constant-source activation then costs \(O(H)\) in the \(H^2\) part, while
the immediate marked reward is only logarithmic.  The boundary macro must
either be a fixed-class invariant reduction or retain enough subsequent
deaths to repay that activation birth.  Sections 7--8 identify exactly that
remaining stopped ledger.  What Section 9 establishes is that the original
all-active linear-\(H\) theorem may be replaced by the same marked
potential used at its eventual boundary endpoint; there is no independent
weighted seam inside the all-active branch.

## 10. A slow compact-shell entrance is not a service obstruction

The anisotropic service window after a compact entrance has physical scale
\(H^{-1/2}\), but the entrance itself need not have that scale.  The following
example is a useful hostile diagnostic, but it is **not** a recurrence or
fixed-service counterexample.  Consider
\[
 T=\{C,A+B,2A\},\qquad R=\{0,A,B\},                    \tag{10.1}
\]
with a strong top graph containing both directions on
\(C\leftrightarrows A+B\) and \(A+B\leftrightarrows2A\), and the lower
cycle
\[
                              0\to B\to A\to0.          \tag{10.2}
\]
Choose the \(A+B\to C\) rate larger than the \(A+B\to2A\) rate, and start
from
\[
                              (A,B,C)=(0,N,0).          \tag{10.3}
\]

At large \(B\), the lower reaction \(B\to A\) seeds an \(A\)-carrier at
rate of order \(B\).  An \(A+B\)-reaction then occurs at order \(AB\).
With the displayed rate choice, a carrier can make many dominant
\(A+B\to C\) returns before the smaller reproduction route builds a
mesoscopic \(A\)-population.  Thus a proof is not entitled to assert that
the compact set \(A,B=\Theta(\sqrt N), C=\Theta(N)\) is reached in physical
time \(O(N^{-1/2})\).  In the usual fast-carrier approximation the
\(B\)-reservoir can drain multiplicatively, making a logarithmic entrance
time plausible.  This observation alone is enough to invalidate a proof
which simply postulates the faster entrance scale.

It does **not** invalidate a fixed-horizon net-service theorem.  The
reverse \(C\to A+B\) clock has order \(C\).  Balancing it against the
dominant \(A+B\to C\) clock gives the diagnostic relation
\[
                              A\asymp {C\over B}.       \tag{10.4}
\]
Hence, as \(B\) drains and \(C\) accumulates, service exposure grows; near
\(B\asymp\sqrt N,C\asymp N\), it is already of order \(\sqrt N\).  In
particular the tempting inference that the total \(A\)-death count must be
only \(O(\log N)\) is false.  A sufficiently large fixed physical horizon
may accumulate an arbitrarily prescribed mean service while its
constant-source birth cost grows only linearly in that horizon.

The exact pathwise ledger makes clear what a proof has to retain.  Write
\(m_1,m_2,m_3,m_4\) for the reaction counts
\[
 C\to A+B,\quad A+B\to C,\quad A+B\to2A,\quad
 2A\to A+B,
\]
and \(b,u,d\) for \(0\to B,B\to A,A\to0\).  For the displayed edges,
\[
\begin{aligned}
 A_t-A_0&=m_1-m_2+m_3-m_4+u-d,\\
 B_t-B_0&=m_1-m_2-m_3+m_4+b-u,\\
 C_t-C_0&=-m_1+m_2.
\end{aligned}                                         \tag{10.5}
\]
Additional labelled edges are inserted with their literal stoichiometric
increments.  Dominant \(C\leftrightarrows A+B\) backtracks therefore cancel
in the ledger; every uncompensated route through \(2A\), every lower seed,
every birth, and every death remains visible.  Any valid arbitrary-
orientation proof must obtain service from these balances or from the
equivalent killed-reservoir resolvent, not from a prescribed next label.

Once \(B=O(\sqrt N)\) and \(C=\Theta(N)\), the anisotropic scaling
\[
        a={A\over\sqrt N},\qquad b={B\over\sqrt N},
        \qquad c={C\over N},\qquad \sigma=t\sqrt N       \tag{10.6}
\]
turns the top dynamics into the full-rank strong two-species
single-linkage system on \(\{0\}\cup Q\), with the zero-source rates
multiplied by \(c\).  A fixed \(\sigma\)-window gives a fixed mean number of
physical \(A\)-deaths and \(o(1)\) births.  Such a window is a valid
post-entrance tool, but it is not the only possible service clock.

A stronger and cleaner repair would stop after a fixed physical horizon
(or an earlier favorable workload drop) and prove directly that the
complete accumulated \(A\)-death compensator dominates the constant-source
birth count.  This formulation permits a slow compact-shell entrance and
charges all service accumulated during it.

Therefore the load-bearing anisotropic theorem is a **two-reservoir
occupation lemma**, not a uniform entrance-time lemma: for every fixed
strong orientation and positive rate vector it must combine the exact
source balances, repeated carrier creation and extinction, and the
post-entrance scaled window to give a net birth/death inequality over one
physical all-clock stopping rule.  The example above warns against the
wrong time scale but supplies no counterexample to that corrected theorem.

## 11. Exact killed-linear ascent in the no-\(2B\) support

The no-\(2B\) anisotropic support has an exact rate-weighted ascent
functional.  This removes one possible source of the gap, although an
occupation/service handoff is still required.

> **Lemma 11.1 (killed-complex linear functional).**  Let
> \[
>                         T=\{C,A+B,2A\}
> \]
> carry an arbitrary fixed strongly connected labelled graph with positive
> rates.  There are \(v\in{\mathbb R}^3\) and constants
> \(c,C>0\), depending only on that graph and its rates, such that
> \(v_A>v_B\) and
> \[
> {\cal L}_T(v\cdot x)
>   \ge c\{(x)_C+(x)_{A+B}\}-C(x)_{2A}.                \tag{11.1}
> \]

### Proof

Kill the fixed complex graph on first hitting \(2A\), and let \(Q\) be its
subgenerator on \(P=\{C,A+B\}\).  Strong connectivity makes \(Q\)
transient.  Hence
\[
                         g=(-Q)^{-1}{\bf1}>0.
\]
For sufficiently small \(\rho>0\), prescribe complex values
\[
 r(2A)=1,\qquad r(y)=1-\rho g_y\quad(y\in P).          \tag{11.2}
\]
If \(k\) is the vector of rates from \(P\) to \(2A\), then
\(Q{\bf1}+k=0\) and \(Qg=-{\bf1}\).  Therefore the full labelled
complex-graph generator satisfies
\[
             {\cal Q}r(y)=\rho\quad(y=C,A+B).          \tag{11.3}
\]
Its value at \(2A\) is bounded below by a fixed negative constant.

The three complexes are affinely independent in the plane
\(A+B+2C=2\).  More explicitly, the assignment (11.2) is induced by the
species-linear functional
\[
 v_C=r(C),\qquad
 v_A={1\over2},\qquad
 v_B=r(A+B)-{1\over2}.                                \tag{11.4}
\]
Indeed \(v\cdot C=r(C)\), \(v\cdot(A+B)=r(A+B)\), and
\(v\cdot2A=1\).  Moreover
\[
                    v_A-v_B=1-r(A+B)=\rho g_{A+B}>0. \tag{11.5}
\]
Multiplying (11.3) and the bounded \(2A\)-source reward by the literal
falling-factorial source propensities gives (11.1). \(\square\)

There is a useful full-network corollary.  Suppose \(A\to0\) is a death
edge in the lower linkage and \(B\) has no edge to zero.  Every
\(B\)-sourced lower edge then targets \(A\), so (11.5) makes its
contribution favorable.  The zero-source contribution is bounded and every
\(A\)-sourced lower contribution is \(O(A)\).  Thus
\[
 {\cal L}(v\cdot x)
 \ge c\{C+AB+B\}-C\{A(A-1)+A+1\}.                    \tag{11.6}
\]
If \(B\to0\) exists instead, \(B\) itself is already a service species and
the large-\(B\) branch is favorable.

On a workload shell \(H=A+B+2C\asymp N\), choose a sufficiently small
fixed \(\eta>0\).  Since \(B+2C=N-A\), (11.6) gives
\[
             {\cal L}(v\cdot x)\ge c_0N
             \quad\text{on }A\le\eta\sqrt N           \tag{11.7}
\]
for all large \(N\).  The functional \(v\cdot x\) has oscillation \(O(N)\)
on the localized shell.  Dynkin's formula therefore gives a uniformly
bounded mean time, and by block restart a geometric physical-time tail, to
one of
\[
 A>\eta\sqrt N,\qquad H\notin[N/2,2N].                \tag{11.8}
\]
The second alternative is a literal population-shell endpoint; no clock is
deleted.

Lemma 11.1 is stronger than qualitative access and uses no orientation or
population enumeration.  It also explains why a dominant
\(C\leftrightarrows A+B\) backtrack cannot create a closed low-\(A\)
phase: the killed resolvent charges the fixed positive leakage through
\(2A\).  What it does **not** prove is the final net-service statement.
An \(A=\Theta(\sqrt N)\) first hit may still have \(B\gg\sqrt N\), and the
fast \(A+B\) clock can immediately redistribute the new carriers.  The
remaining lemma must retain those repeated excursions until either
\(B=O(\sqrt N)\), enough \(A\)-death compensator has accumulated, or a
favorable workload-shell exit occurs.  That is the precise occupation seam
left after (11.7).

## 12. The scaled marked potential fails the existing global interface

There is a tempting common-potential normalization which makes the
pointwise birth toll small.  Put
\[
 W_\epsilon(x,t)
   =H(x)+{\epsilon\over H(x)+1}
      F(x,t),\qquad
 F(x,t)=\sum_i\log((x_i-t_i)!).                       \tag{12.1}
\]
It is nonnegative and proper because \(H\) is proper and \(F\ge0\).
The coarse upper estimate \(F(x,t)\le C H\log(2+H)\) will be used below.

Every top reaction preserves \(H\).  Hence an all-top marked episode has
exact reward
\[
       {\epsilon\over H+1}\{F(X_\tau,T_\tau)-F(x,t)\}. \tag{12.2}
\]
For a lower jump, \(|\Delta H|\le s\), \(|\Delta F|\le C\log(2+H)\),
and the denominator change gives
\[
\left|
 {F+\Delta F\over H+\Delta H+1}-{F\over H+1}
\right|
\le {C\log(2+H)\over H+1}.                           \tag{12.3}
\]
Thus the only order-one part of a lower jump is its literal workload
increment \(\Delta H\); the scaled factorial toll is lower order.

In the anisotropic family the total hazard has the uniform shell lower
bound
\[
 \Lambda(x)\ge c\{C+A+B\}\ge c'H.                    \tag{12.4}
\]
Indeed \(C\) has a fixed positive outgoing rate in the upper linkage, and
each lower unary vertex has positive aggregate outgoing rate.  Therefore a
zero-source birth occurs at the next all-clock jump with probability
\[
                              p_0(x)\le {C\over H}.   \tag{12.5}
\]
Although a physical birth changes the first term of (12.1) by \(s\), its
expected one-step cost is only \(O(H^{-1})\).

Now suppose a bounded-depth marked Bellman path reaches a source of
probability at most \(\delta\).  The exact factorial recursion gives
expected \(F\)-reward at most \(-A(\delta)\), where
\(A(\delta)\to\infty\) as \(\delta\downarrow0\).  Equations
(12.2)--(12.5) consequently give a negative \(W_\epsilon\)-episode once
\(A(\delta)\) exceeds the fixed birth and denominator-change constants.
This is the correct comparison:
\[
       -{\epsilon A(\delta)\over H}+O(H^{-1}),        \tag{12.6}
\]
not a comparison with the \(O(H)\) activation cost of the quadratic
potential \(H^2\).

This normalization removes the artificial need to repay one birth by an
order-\(H\) correction in a **single expected episode comparison**.  It
does not close balanced reservoir states.  If
all same-linkage terminal source probabilities along the finite path menu
stay bounded away from zero, \(A(\delta)\) is only a fixed number and may
not dominate arbitrary rate-dependent birth cost.  In precisely that
region the rate balance says that the service species has nonnegligible
occupation, and one needs the two-reservoir net-service lemma.  Its natural
target is now only
\[
 {\mathbb E}\{B_\tau-D_\tau\}\le-a<0                 \tag{12.7}
\]
with appropriate moments and actual endpoints, rather than the
workload-weighted estimate (7.8).  Here \(B_\tau,D_\tau\) are literal lower
birth and workload-death counts retained by the all-clock episode.

More seriously, it does not lift the already frozen marked episodes into
the existing terminal Green--Foster theorem.  Those episodes give a fixed
margin such as
\[
                         {\mathbb E}\Delta F\le-2.     \tag{12.8}
\]
After quotienting, this is only
\[
                         {\mathbb E}\Delta W_\epsilon
                              \le-{2\epsilon\over H}+o(H^{-1}), \tag{12.9}
\]
which tends to zero.  Even a polynomially rare source has
\(A(\delta_H)=O(\log H)\), so its quotient reward is only
\(O(\log H/H)\).  A uniform negative episode margin would require
\(A(\delta_H)=\Omega(H)\), equivalently an exponentially rare terminal
source, which binary mass-action ratios do not generally supply.

The global lower bound \(\Lambda\ge cH\) makes a bounded-jump episode last
only \(O(H^{-1})\) in mean, but the terminal Green contradiction drops the
nonnegative duration term and still requires a uniform embedded episode
margin.  Thus fast physical time does not convert (12.9) into the current
contract.  A new hazard-weighted or source-layer Green theorem could in
principle normalize the episode count by \(H^{-1}\), but no frozen
composition theorem supplies that interface.

The denominator must also be evaluated at the actual post-jump workload and the
actual target mark.  Treating it as fixed across a lower jump would discard
the error in (12.3).  Even with that proviso, (12.1) is only a local
comparison device.  It does **not** presently compose the rare-source
Bellman episodes, balanced service episodes, and lower-dimensional
handoffs.  The minimal repair remains either a uniform net-service episode
under a potential with a uniform margin, or a separately proved
hazard-weighted Green duality theorem together with its charged seams.

## 13. Minimal balanced service theorem still required

The preceding reductions isolate a statement which is both sufficient and
strictly weaker than an orientation/history enumeration.

> **Balanced level-set service lemma.**  Fix one level-set pair, one
> arbitrary strongly connected labelled graph on each linkage, one positive
> rate vector, one closed irreducible class, and a chosen lower unary death
> species \(d\).  Suppose a localized boundary state has workload
> \(N\to\infty\) and lies in the complement of:
>
> 1. the common-\(H\) pointwise region \(x_d\ge K\);
> 2. a marked rare-source Bellman region with a uniform negative episode
>    margin under the chosen global scalar;
> 3. a finite or invariant face; and
> 4. a named population/active-set/chart exit.
>
> Then there is a physical all-clock stopping time \(\tau\), using only the
> fixed network data and the current localized state, such that:
>
> \[
> \begin{split}
> &{\mathbb E}_x\{B_\tau-D_\tau\}\le-a<0,\\
> &\sup_x{\mathbb E}_x e^{\theta(B_\tau+D_\tau)}<\infty,\\
> &\sup_x{\mathbb E}_x\tau^p<\infty,\qquad
> \sup_x{\mathbb E}_x[(H(X_\tau)-H(x))^+]^p<\infty
> \end{split}                                           \tag{13.1}
> \]
> for some \(a,\theta>0,p>1\), or else \(\tau\) records one of the named
> favorable exits with the endpoint charged under the same scalar.
> Here \(B_\tau\) and \(D_\tau\) count every lower workload birth and death
> exactly once; all neutral top reactions and lower transfers remain in the
> physical path.

If the final global scalar is a powered population/factorial envelope, the
first line of (13.1), its exponential moment, and the exact endpoint
identity give a uniform stopped Foster decrement by the same Taylor
calculation as the audited rank-two stopped-service theorem.  If a
different scalar is chosen, the theorem must state its literal endpoint
inequality rather than infer it from (13.1).

For \(h=(1,1,1)\), the analytic proof of (13.1) may split only into the
three symbolic kernels in Section 8.1:

* killed two-carrier PF ascent;
* dyadic two-minimum source balance; and
* exact common-catalyst linear-chain averaging.

After reaching a compact normalized activation shell, the strong
single-linkage top ODE has no invariant service-free subset except the
already isolated dormant vertices.  Infinite service integral and
compactness then give a fixed density-time window with arbitrarily large
mean death compensator.  The required proof must show that its activation
trial count, birth count, downward/upward shell exits, and endpoint moments
obey (13.1), uniformly over the finitely many dormant vertices of the fixed
support.  Constants may depend on the fixed orientation and rates.  This is
orientation-uniform in scope, not rate-uniform in constants.

For \(h=(1,1,2)\), supports with \(2B\) use the exact two-reservoir
\(\{C,2B\}\) source balance, while the sole no-\(2B\) support
\(\{C,A+B,2A\}\) uses Lemma 11.1 followed by the occupation/service
handoff.  A proof may stop at a fixed physical horizon or at a favorable
shell exit; it need not assert a false \(O(N^{-1/2})\) entrance from every
boundary state.

The lemma must be paired with a **single global interface**.  Under the
currently frozen terminal Green theorem, every retained episode needs a
uniform negative scalar margin and a uniform positive endpoint moment.
An \(H\)-dependent margin such as \(H^{-1}\) is not sufficient.  Any
replacement by a source-layer or hazard-weighted normalization is itself a
new load-bearing theorem and must prove its own nonoverlap, boundary-entry
uniform integrability, and charged-seam condition.

## 14. A physical-time supermartingale can accept vanishing jump margins

The last sentence of Section 13 applies to the currently frozen
**embedded-Green** theorem.  There is a different physical-time route which
can accept the \(H^{-1}\) jump margin of Section 12.

> **Lemma 14.1 (episode-time Foster lemma).**  Let \(Y=(X,T)\) be a
> nonexplosive marked CTMC, \(K\) a finite set, and \(V\ge0\) one proper
> function on the whole marked state space.  Suppose that, until hitting
> \(K\), state-selected physical episodes tile the trajectory at stopping
> times
> \[
>              0=S_0<S_1<S_2<\cdots,                 \tag{14.1}
> \]
> every episode contains at least one actual jump, and for some fixed
> \(\eta>0\),
> \[
> {\mathbb E}\!\left[
>   V(Y_{S_{n+1}})-V(Y_{S_n})+\eta(S_{n+1}-S_n)
>       \,\middle|\,{\cal F}_{S_n}\right]\le0.         \tag{14.2}
> \]
> Assume the positive endpoint increments are uniformly integrable under
> the localization used below.  Then the first hitting time
> \(\tau_K\) satisfies
> \[
>                         {\mathbb E}_y\tau_K
>                                  \le {V(y)\over\eta}. \tag{14.3}
> \]

### Proof

Stop at the first episode endpoint which hits \(K\), and also at the first
endpoint outside a finite \(V\)-sublevel.  Conditional summation of
(14.2), justified by the stated positive-part uniform integrability, gives
\[
             \eta\,{\mathbb E}S_{n\wedge N\wedge\sigma_R}
                    \le V(y).                         \tag{14.4}
\]
First let \(R\to\infty\), then \(n\to\infty\), using Fatou or monotone
convergence for the time term.  On the event that \(K\) is never hit, the
episode endpoints contain an infinite subsequence of actual jump times.
Nonexplosion therefore forces \(S_n\to\infty\).  Equation (14.4) then
would give infinite expected limiting time on a positive-probability
no-hit event, a contradiction.  Hence \(K\) is hit almost surely, and
monotone convergence yields (14.3). \(\square\)

The strict inequality in (14.1) is load-bearing.  A chart classifier,
Bellman/Flat0 top-access declaration, or endpoint reclassification can
have zero physical duration.  Such declarations must be concatenated into
the next rule until at least one ordinary jump is taken.  Because the chart
and mark menus are finite, one must prove that this zero-time
reclassification cannot cycle.  Nonexplosion says nothing about an
artificial infinite sequence of zero-time chart handoffs.

Likewise, a structural-exit alternative is not a terminal outcome of the
global tiling.  The exit-causing jump belongs to the old episode exactly
once; its actual endpoint and mark select the next rule.  Every endpoint
must use the same \(V\), or else the potential reset becomes an omitted
seam charge.

For the scaled potential (12.1), a bounded-depth rare-source episode has
\[
       {\mathbb E}\Delta V\le-{A\over H},\qquad
       {\mathbb E}\tau\le{C\over H}                   \tag{14.5}
\]
whenever the total hazard remains comparable to \(H\) along its bounded
prefix and the quotient errors are absorbed.  Choosing
\(\eta<A/C\) makes (14.2) valid despite the vanishing embedded margin.
This is a genuine way around the objection in (12.9).

It is not automatic for all frozen local episodes.  One must verify:

1. the \(C/H\) duration bound at every stage, including a finite Flat0
   prelude whose degree-zero phases can have only \(O(1)\) hazard;
2. that any such slow prelude has a fixed negative \(V\)-reward large
   enough to pay \(\eta{\mathbb E}\tau\), or is a finite-class/exit branch;
3. quotient errors at every actual \(H\)-changing endpoint;
4. a finite zero-time handoff closure; and
5. the positive endpoint uniform integrability needed in (14.4).

In particular the h112 global lower bound \(\Lambda\ge cH\) resolves item
1 for ordinary jumps in that family.  It does not automatically resolve a
projected h111 branch whose lower support omits the large coordinate and
whose active top sources are disabled.  Thus Lemma 14.1 is an exact
candidate composition theorem, not yet a blanket lift of every frozen
AA/Q/B/B/B-F0 theorem.

## 15. The \(H\)-alone architecture and its exact missing occupation bound

For the level-set family, no marked potential is needed if one proves the
right occupation estimate on the direct-death boundary.  Let
\[
 \beta=\sum_{0\to u}\kappa_{0u},\qquad
 \delta_d=\sum_{d\to0}\kappa_{d0},\qquad
 D=\{d:\delta_d>0\}.
\]
Strong connectivity of the lower linkage makes \(D\ne\varnothing\).  The
exact global identity is
\[
                    {\cal L}H=s\beta
                         -s\sum_{d\in D}\delta_d x_d. \tag{15.1}
\]
All top reactions and lower unary transfers disappear literally.

Choose fixed \(\eta>0\), then \(K\) so large that
\[
 s\beta-s\delta_*K\le-2\eta,\qquad
 \delta_*=\min_{d\in D}\delta_d,                      \tag{15.2}
\]
and put
\[
                 {\cal D}_K=\{x:x_d<K\text{ for every }d\in D\}. \tag{15.3}
\]
At a state outside \({\cal D}_K\), stop at the next ordinary physical
jump.  If \(\Lambda(x)\) is the total hazard, then
\[
 {\mathbb E}_x\{\Delta H+\eta\tau\}
             ={ {\cal L}H(x)+\eta\over\Lambda(x)}\le0. \tag{15.4}
\]
The margin may vanish when \(\Lambda\) is large; Lemma 14.1 was designed
precisely for this physical-time normalization.

The only missing stochastic statement is therefore the following.

> **Direct-death occupation lemma.**  There are a finite \(H\)-sublevel
> \(K_0\), constants \(a>0,\eta>0\), and, from every
> \(x\in{\cal D}_K\setminus K_0\), an integrable all-clock stopping time
> \(\tau\) containing at least one actual jump, such that
> \[
>       {\mathbb E}_x\{H(X_\tau)-H(x)+\eta\tau\}\le-a. \tag{15.5}
> \]
> The rule is state selected, retains every top reaction, birth, transfer,
> and death, and stops at its actual physical endpoint.

This is equivalent to a literal occupation surplus.  In compensator form,
a sufficient exact statement is
\[
 {\mathbb E}_x\int_0^\tau
       \sum_{d\in D}\delta_dX_d(t)\,dt
 \ge\left(\beta+{\eta\over s}\right){\mathbb E}_x\tau
                         +{a\over s}.                 \tag{15.6}
\]
In reaction-count form it is
\[
             s\,{\mathbb E}_x(D_\tau-B_\tau)
                    \ge a+\eta{\mathbb E}_x\tau,       \tag{15.7}
\]
where all zero-source workload births and all direct workload deaths are
counted once.

Equations (15.4)--(15.5) tile the full trajectory under the one proper
function \(H\).  Conditional summation and Lemma 14.1 give
\[
                         {\mathbb E}_x\tau_{K_0}
                                  \le {H(x)\over\eta}. \tag{15.8}
\]
The extra constant \(a\) is convenient but unnecessary; the
\(\eta\tau\) term already forces finite physical time.

No polynomial or exponential endpoint moment is needed for (15.8).
Pathwise,
\[
                         H(X_\tau)\le H(x)+sB_\tau,    \tag{15.9}
\]
because births are the only workload-increasing reactions.  Their aggregate
clock has the constant intensity \(\beta\).  For an integrable stopping
time, localization of its counting-process martingale gives
\[
                         {\mathbb E}B_\tau=\beta{\mathbb E}\tau. \tag{15.10}
\]
Thus \(H(X_\tau)\) is integrable automatically.  Nonnegativity of \(H\)
and Fatou handle the negative part in the episode summation.

There is no hidden chart seam: \(H\) is the same physical function on every
face, and a chart-exit jump simply becomes the endpoint of the current
macro and the start of the next state-selected rule.  Zero-time
reclassifications must still be folded into a rule which takes an actual
jump.

The only fixed-class exceptions are exact reductions, not stochastic
loopholes.  A zero-active class is a singleton.  If a \(T\)-dead face
cannot be seeded because its common catalyst is absent from the lower
unary support, that catalyst coordinate is a full-network invariant; after
fixing the class it cannot carry escape.  The remaining open unary linkage
has finite phase access to a direct death and satisfies the same occupation
contract.  More generally, any coordinate invariant is removed before the
level-set theorem is invoked.  Strong connectivity of \(R\) leaves no
closed active lower phase from which every direct-death vertex is
inaccessible.

Consequently (15.6), not a common factorial estimate or an embedded seam
charge, is the minimal load-bearing theorem for global classwise closure of
the 336 family.  Sections 8.1 and 8.2 give its finite symbolic analytic
kernels.
