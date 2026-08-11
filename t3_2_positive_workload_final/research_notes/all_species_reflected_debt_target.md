# The all-species reflected-debt target

## 1. Purpose and claim boundary

This note records an abstract target construction for the physical-time
repair.  It does not prove the remaining one-active service theorem and it
does not certify T3-2.  Its point is to remove two unnecessary obligations
from that theorem:

1. a local episode need not produce a surplus reaction when its active debt
   is zero; and
2. no inactive-coordinate box is needed to make the final target finite.

The construction marks every physical species, not merely the species which
is active in the current source-rate chart.

## 2. The deterministic reflected marks

Let \(X\) be a population CTMC on a closed irreducible class
\(\Gamma\subseteq\mathbb N_0^d\).  Fix a reference state
\(x^\circ\in\Gamma\), start \(D(0)=0\), and update the mark after every
physical jump \(x\mapsto x+\zeta\) by

\[
 D_i^+=(D_i+\zeta_i)^+,
 \qquad i=1,\ldots,d.                                \tag{2.1}
\]

This definition also covers jumps of size two.  Put

\[
 H_i=X_i-D_i.                                        \tag{2.2}
\]

> **Lemma 2.1 (pathwise reflected target).**  On every reachable marked
> state,
> \[
>  0\le D_i\le X_i,
>  \qquad H_i(t)\le H_i(0)=x_i^\circ .               \tag{2.3}
> \]
> In fact every \(H_i\) is pathwise nonincreasing.  Consequently
> \[
>  \widehat K_{x^\circ}
>  :=\{(x,d):d=0,\ x\in\Gamma\}
>  \subseteq
>  \{(x,0):0\le x_i\le x_i^\circ\ \hbox{for all }i\} \tag{2.4}
> \]
> is finite.

### Proof

Assume \(0\le D_i\le X_i\) before one jump.  If
\(D_i+\zeta_i\ge0\), then

\[
 D_i^+=D_i+\zeta_i\le X_i+\zeta_i=X_i^+,
 \qquad H_i^+=X_i^+-D_i^+=H_i.
\]

If \(D_i+\zeta_i<0\), then \(D_i^+=0\le X_i^+\) and

\[
 H_i^+=X_i+\zeta_i<X_i-D_i=H_i.
\]

Induction proves (2.3).  At \(D=0\), \(X=H\le x^\circ\)
coordinatewise, which proves (2.4).  \(\square\)

The marked process is still a nonexplosive CTMC whenever the physical
process is: its mark is a deterministic function of the previous mark and
the selected physical reaction.  Moreover a proper population function is
proper on the reachable marked space, because a fixed population \(x\) has
only \(\prod_i(x_i+1)\) possible marks satisfying \(0\le d\le x\).

## 3. Exact gluing statement

Write \(\widehat\Gamma_{x^\circ}\) for the marked states reachable from
\((x^\circ,0)\).  Let \(W:\Gamma\to[0,\infty)\) be proper.  Split the
marked states outside a finite set \(K\supseteq\widehat K_{x^\circ}\) into
a generator-good set \(G\) and finitely many bad-tube sets \(B_j\).

Assume that:

1. for some \(a>0\),
   \[
    {\cal L}W(x)\le-a,
    \qquad (x,d)\in G;                               \tag{3.1}
   \]
2. every marked state in \(\bigcup_jB_j\setminus K\) has positive debt in
   at least one coordinate selected by that tube; and
3. there are \(\eta\in(0,a]\) and \(\delta>0\) such that every
   \((x,d)\in B_j\setminus K\) admits a physical strong-Markov stopping
   rule \(\tau_{x,d}>0\), with all reactions retained, for which
   \[
    \mathbb E_{x,d}\!\left[
       W(X_{\tau_{x,d}})-W(x)+\eta\tau_{x,d}
    \right]\le-\delta .                              \tag{3.2}
   \]
   The endpoint and duration are uniformly integrable to the extent needed
   to remove the localization used in (3.1)--(3.2).

> **Theorem 3.1 (all-debt finite-target gluing).**  Under these hypotheses,
> the marked chain hits \(K\) in finite mean physical time from every state
> reachable from \((x^\circ,0)\).  In particular the physical population
> chain is positive recurrent on \(\Gamma\).

### Proof

On the marked space use \(\widehat W(x,d)=W(x)\).  It is proper by the
observation following Lemma 2.1.  Equations (3.1)--(3.2) are exactly the
common-potential hypotheses of the physical-time gluing theorem: run
localized generator-good motion until \(B\cup K\), append the selected
bad-tube episode, and telescope.  This gives finite mean hit of \(K\).

The projection of \(K\) to \(\Gamma\) is finite.  To see the positive-return
step explicitly, first dispose of the trivial case in which the class is an
absorbing singleton.  Otherwise, start at any marked \(k\in K\), take one
ordinary physical jump, and apply the theorem from its marked successor to
return to \(K\).  Every state has finitely many marked successors and a
finite mean holding time.  Maximizing over the finite set \(K\) therefore
gives a finite mean positive marked return to \(K\).  Its physical
projection is a finite set with finite mean positive return.  Irreducibility
of the physical class then promotes one state, and hence every state, to
positive recurrence.
\(\square\)

The sequence form used by the atlas is equivalent.  If every divergent
sequence in one \(B_j\) has a subsequence on which (3.2) holds with the same
\(\eta,\delta\), properness gives a finite-exception conclusion by the
usual bad-sequence contradiction.  No exact finite phase is inferred from
tightness.

## 4. What a one-active tube now has to prove

Suppose species \(i\) is the unique divergent coordinate in a fixed-width
statewise bad tube.  If \(D_i=0\), then

\[
 X_i=H_i\le x_i^\circ .                              \tag{4.1}
\]

The other coordinates are tube-bounded, so such states form a finite
class-dependent exception.  Therefore the local theorem is needed only
when \(D_i>0\).  Its successful physical word need only lower this existing
debt; it need not cross \(D_i=0\) and create a surplus exit.

This distinction is important for the remaining kinetic regression.  A
word which lowers \(D_i=1\) to zero can require one fewer slow-before-fast
contest than a word which continues to a surplus.  The latter is not the
correct recurrence target.

A support-specific tube theorem may close (3.2) in either of two ways.

1. **Bounded-time amplified drift.**  In one bounded physical attempt, a
   debt-reducing endpoint has probability of order \(N^{-m}\), whereas a
   new unresolved entry has order \(N^{-m-1}\).  A common sufficiently
   high factorial-entropy power supplies a uniform negative margin, provided
   all neutral endpoint curvature and promoted tails are controlled at the
   same scale.
2. **Shell-adapted descent.**  Repeat the retained-reaction attempt until
   debt falls by one, prove finite level-dependent duration and endpoint
   moments, and apply the shell-adapted trace scalarization.  Promotion
   exits must be charged by the same population potential; they cannot be
   called finite-box failures.

Neither alternative follows from a finite reaction word alone.  The
remaining analytic obligations are:

* an arbitrary-strong-orientation proof of the kinetic separation;
* a full-reaction stopped kernel realizing it;
* moment bounds for countable open phases and promotion exits; and
* one common-potential composition with the already certified
  multi-active generator regions.

## 5. Claim status

Lemma 2.1 and Theorem 3.1 are abstract Markov-chain statements.  They
repair the finite-target interface and show why surplus service at zero
debt is unnecessary.  They do not certify any of the remaining support
pairs.  The universal one-active theorem and global T3-2 flag remain open.
