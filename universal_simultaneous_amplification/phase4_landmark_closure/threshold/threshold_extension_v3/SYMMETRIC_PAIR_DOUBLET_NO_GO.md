# Symmetric portal-linked pair doublets do not cross the hybrid tangent

Date: 2026-08-08 (America/Los_Angeles)

No literature search and no external communication were used.

## 1. Scope and result

Let

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1
\]

and let `R_hyb` be its unique root in `(3/2,151/100)`.  Consider the
separated dilute hybrid construction, but permit a satellite to be a
**correlated doublet** of two strong `K_2` modules.  The two fast pairs have
the same internal scale `sigma`, the same total weak load to the large
clique center, and an arbitrary positive symmetric weak edge bundle between
them.  The pair--pair bundle and the pair--center bundles vanish on the same
time scale.  Ordinary hub leaves may be added, and arbitrary populations of
doublets with different `sigma` and correlation strengths may be mixed.

At fitness `R_hyb`, every such doublet has nonpositive leaf-eliminated
tangent separator

\[
                 F_{dB}+(R_{\rm hyb}-1)F_{Bd}\le 0.       \tag{1}
\]

Equality holds only when the pair--pair weak load is zero and
`sigma=sigma_*`, the already known uncoupled-pair tangency.  Since an
ordinary leaf has separator exactly zero, mixtures preserve (1).

Consequently no fixed nonzero symmetric pair correlation can raise the
proved threshold at first order.  This is a rigorous tangent-cone class
obstruction, not a universal upper bound for `R_sim`: a parameter sequence
approaching the equality boundary can only be decided by a second-order
calculation.

## 2. Trace derived from the update rules

Take a unit clique center of order `C`.  Each fast pair has internal edge
weight `C/sigma`.  A pair--center edge has weak weight proportional to
`epsilon`; a pair--pair edge has weak weight proportional to `epsilon C`,
so both kinds of successful macro event have order `epsilon`.  First send
`epsilon` to zero at fixed finite counts and then send `C` to infinity.
The fast classes are exactly the states in which the center and each strong
pair are monomorphic.  The finite-state Schur complement therefore gives
the trace obtained by one weak introduction followed by exact local
absorption.

For one mutant pair against the resident center, write `A` for successful
center establishment and `D` for recovery of the pair by the center.  For
one mutant and one resident pair, write `m` for infection of the resident
pair and `q` for recovery of the mutant pair.  After deleting a common
positive time factor, direct event summation gives

\[
\begin{array}{c|cccc}
 &A&D&m&q\\ \hline
 Bd&2\sigma(r-1)x&2x/(r+1)&4r^2\sigma y/(r+1)&4\sigma y/(r+1)\\[1mm]
 dB&2(r-1)x&\sigma x/r&2r\sigma y&2\sigma y/r.
\end{array}                                                \tag{2}
\]

Here `x` is the common total core load and `y` is the total inter-pair load
in the normalization above.  The factors in (2) follow directly as follows.

* Under Bd, a mutant pair supplies two reproducing sources.  Dividing the
  weak target load by internal degree `C/sigma`, then multiplying by the
  exact `K_2` fixation probabilities `r/(r+1)` and `1/(r+1)`, gives the Bd
  row.
* Under dB, the internal degree of the target pair supplies `sigma`; the
  exact dB fixation probability from a mixed `K_2` is `1/2` for either
  relative fitness.  This gives the dB row.
* A mutant introduced into the large center fixes with probability
  `p=1-1/r`; this is already included in `A`.

In both rows

\[
                              {m\over q}=r^2.              \tag{3}
\]

Let `H_1` and `H_2` be center-establishment probabilities from one and two
mutant pairs.  Their exact first-step equations are

\[
 (A+D+q+m)H_1=A+mH_2,\qquad
 (A+D)H_2=A+DH_1.
\]

Solving gives

\[
 H_1={A(A+D+m)\over(A+D)(A+D+q)+mA}.                    \tag{4}
\]

Put

\[
 H(z,\theta)=
 {z(z+1+r^2\theta)\over
  (z+1)^2+\theta\{1+(1+r^2)z\}}.                        \tag{5}
\]

With `u=2y/x`, equations (2)--(4) become

\[
 H_{Bd}=H\bigl(\sigma(r^2-1),\sigma u\bigr),\qquad
 H_{dB}=H\bigl(2r(r-1)/\sigma,u\bigr).                  \tag{6}
\]

## 3. Full singleton correction

A singleton first fixes its own fast pair with probability `r/(r+1)` under
Bd and `1/2` under dB.  There are four satellite vertices, and the four core
vertices they replace each have limiting fixation `p`.  Thus the exact
leading corrections are

\[
 F_{Bd}=4\left\{{rH_{Bd}\over(r+1)p}-1\right\},\qquad
 F_{dB}=4\left\{{H_{dB}\over2p}-1\right\}.              \tag{7}
\]

The subtractions in (7) are the complete uniform-singleton far-field terms.
They are not optional local-gadget normalizations.

Dividing the separator in (1) by four gives

\[
 S(r,\sigma,u)=
 {rH_{dB}\over2(r-1)}+{r^2H_{Bd}\over r+1}-r.           \tag{8}
\]

All denominators in (5)--(8) are positive for `r>1`, `sigma>0`, and
`u>=0`.

## 4. Exact endpoint certificate

Clearing the positive denominator in (8) yields

\[
 S(r,\sigma,u)=
 {-r\{Q_0(r,\sigma)+uQ_1(r,\sigma)+u^2Q_2(r,\sigma)\}
  \over \operatorname{Den}(r,\sigma,u)}.                 \tag{9}
\]

The constant coefficient factors as

\[
 Q_0=(r+1)(2r^2-2r+\sigma)\{1+(r^2-1)\sigma\}F_r(\sigma),\tag{10}
\]

where

\[
 F_r(\sigma)=(r-1)\sigma^2+(r^3-4r^2+3r+1)\sigma+r(2r-3).
\]

The sextic identity is

\[
 4(r-1)F_r(\sigma)
 -\{2(r-1)\sigma+r^3-4r^2+3r+1\}^2=-P(r).               \tag{11}
\]

Therefore at `r=R_hyb`, `Q_0>=0`, with equality exactly at

\[
 \sigma_*={-R_{\rm hyb}^3+4R_{\rm hyb}^2-3R_{\rm hyb}-1
             \over2(R_{\rm hyb}-1)}.                    \tag{12}
\]

The remaining coefficients have the form

\[
 Q_1=\sigma(c_{13}\sigma^3+c_{12}\sigma^2+c_{11}\sigma+c_{10}),
 \quad
 Q_2=\sigma^2(c_{22}\sigma^2+c_{21}\sigma+c_{20}),      \tag{13}
\]

with

\[
\begin{aligned}
c_{13}&=2r^4+r^3-2r^2-r,\\
c_{12}&=r^8-3r^7+3r^6+3r^5-7r^4-2r^3+5r^2+3r-1,\\
c_{11}&=2r^8-2r^7-2r^6-6r^5+8r^4+8r^3-9r^2+1,\\
c_{10}&=6r^5-7r^4-5r^3+6r^2-2r,\\
c_{22}&=r^4+r^3-r-1,\\
c_{21}&=r^8-r^7-2r^5-r^4+r^3+3r+1,\\
c_{20}&=2r^5-r^4-r^3-2r.
\end{aligned}                                           \tag{14}
\]

At every `r` in `(3/2,151/100)`, `c_10,c_12,c_13,c_20,c_22` are positive.
The discriminants

\[
 \Delta_1=c_{11}^2-4c_{10}c_{12},\qquad
 \Delta_2=c_{21}^2-4c_{20}c_{22}                         \tag{15}
\]

are strictly negative throughout the same interval.  Exact Sturm sequences
prove these sign statements: none of the relevant polynomials has a root in
the rational isolating interval, while at `r=3/2`

\[
 \Delta_1=-{806975\over16384},\qquad
 \Delta_2=-{5311175\over65536}.                          \tag{16}
\]

Hence the quadratic part of `Q_1` is positive, its cubic term is positive,
and `Q_2` is a positive quadratic.  Thus

\[
 Q_1(R_{\rm hyb},\sigma)>0,qquad
 Q_2(R_{\rm hyb},\sigma)>0qquad(\sigma>0).              \tag{17}
\]

Equations (9)--(17) prove (1), with the stated equality class.

## 5. Mixtures and the exact remaining escape

In the dilute trace, corrections from independently attached doublets add.
Ordinary hub leaves contribute `(1/(r-1),-1)`, whose separator is zero.
Arbitrary mixtures of symmetric doublets and uncoupled pairs therefore
still obey (1).  Nonuniform portal loads on the two vertices of an isolated
`K_2` do not change its trace, because both local singleton fixation values
and both internal degrees are equal.

This closes the following proposed extension mechanisms at first order:

* heterogeneous mixtures of uncoupled strong pairs;
* arbitrary ordinary-leaf compensation;
* fixed nonzero symmetric pair--pair correlation on the portal scale;
* arbitrary mixtures of such symmetric doublets.

The precise unresolved modes are now narrower.  A construction within this
architecture must either

1. take `sigma->sigma_*` and `u->0` and obtain a positive **second-order**
   term at the zero tangent;
2. use a genuinely asymmetric portal-edge network (unequal pair scales or
   unequal core loads) whose separator is not an average of symmetric
   doublets; or
3. make the correlated gadget rank grow, or leave the separated trace
   regime altogether.

The numerical searches in `HOSTILE_SEARCH.md` found no lead in (2), but that
statement remains numerical.  Modes (1)--(3) remain open for unrestricted
`R_sim`.

## 6. Replay

Run `replay.sh`.  The independent exact verifier:

1. independently reconstructs every event coefficient in (2), including the
   finite-center dB count recurrence;
2. solves the three-state macro chain;
3. reconstructs (5)--(9);
4. verifies the sextic square identity;
5. proves every interval sign in (14)--(17) by exact Sturm arithmetic; and
6. checks the equality class.

Classification:

* symmetric-doublet trace and separator: **PROVED**;
* endpoint nonpositivity and equality class: **EXACTLY CERTIFIED**;
* extension of the global lower bound beyond `R_hyb`: **NOT FOUND**;
* exact unrestricted `R_sim`: **OPEN**.
