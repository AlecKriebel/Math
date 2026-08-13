# Open-phase Green bound for the separated carrier

**Independent proof audit, 2026-08-12 PDT.**  This note checks only the
phase-corrector table and the resulting open-state Green bound in
`proof_first_separated_completed_return_ledger.md`.  It does not assume or
prove the base-return Green estimate, the duration estimate, localization,
or the final Foster theorem.

**Verdict for the stated open-phase claim: PASS.**  After the phase is
augmented as below, a lower phase has corrected one-step row mass
(O(\delta^\theta)).  A (q)-phase has an (O(1)) exit to a lower phase
and only (O(\delta^{1-\theta})) recurrent mass.  Hence the corrected
payoff accumulated up to the first base return, service, or included
boundary is (O(\delta^\theta)) from a lower phase and (O(1)) from a
(q)-phase.  In particular, only one (q)-sourced exit can be free before
a small factor is incurred.

## 1. Localized open states and corrected weight

Let

\[
 q=A+C,
 \qquad
 {cal C}\subseteq\{0,B,2B,C,2C,B+C,q\},
\]

and fix an open state (x) with (A,C\ge1).  Assume throughout the open
domain that (A\asymp a) and

\[
 {1+B^p\over a}+{C\over a}\le\delta,
 \qquad \delta=o(1),
 \qquad 0<\theta<1.                                      \tag{1.1}
\]

For a complex (v), put (M_x(v)=\prod_i(x_i+1)^{v_i}) and
(r_v=M_x(v)/M_x(q)).  Every lower complex then satisfies

\[
                         r_v\le C\delta.                    \tag{1.2}
\]

The reason is direct: the possible ratios have scales
(1/(AC),B/(AC),B^2/(AC),1/A,C/A,B/A), with harmless (+1)
corrections.  These are bounded by (1.1).  Since the graph is fixed and
strong, (q) has an outgoing edge of positive fixed rate; hence its
aggregate propensity bounds the total denominator below by (cM_x(q)).

Attach a phase (s) to each open state.  If the latest reaction has lower
target (z), set (s=z); if its target is (q), set (s=q).  Define

\[
             \Psi_\theta(x,s)
               ={\exp\{\theta G_\ell(x)\}\over M_x(s)^\theta}. \tag{1.3}
\]

Because all complexes have degree at most two, if (x'=x+z-y), then

\[
 M_{x'}(z)\asymp M_x(z)                                  \tag{1.4}
\]

uniformly, including at coordinate boundaries.  The use of (x_i+1) is
important here.

## 2. Exact transition table

For an enabled reaction (y\to z), stochastic mass action and the
factorial quotient give

\[
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 \le C{M_x(y)\over M_x(q)},
 \qquad
 e^{\theta(G_\ell(x')-G_\ell(x))}
 \le C\left({M_x(z)\over M_x(y)}\right)^\theta.      \tag{2.1}
\]

If (y\ne q), substitution of (1.3)--(1.4) yields

\[
\begin{split}
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 {\Psi_\theta(x',z)\over\Psi_\theta(x,s)}
 &\le C {M_x(y)\over M_x(q)}
       \left({M_x(z)\over M_x(y)}\right)^\theta
       {M_x(s)^\theta\over M_{x'}(z)^\theta}\\
 &\le C r_y^{1-\theta}r_s^\theta.                  \tag{2.2}
\end{split}
\]

The target monomial cancels.  If (y=q), its embedded probability is at
most a fixed constant and the same calculation gives

\[
 {\lambda_{qz}(x)\over\lambda_{\rm tot}(x)}
 {\Psi_\theta(x',z)\over\Psi_\theta(x,s)}
             \le C r_s^\theta.                      \tag{2.3}
\]

Thus (2.2)--(2.3) give precisely the three rows claimed in the ledger:

\[
\begin{array}{c|c}
 y\ne q&C r_y^{1-\theta}r_s^\theta\\
 y=q,\ s\ne q&C r_s^\theta\\
 y=q,\ s=q&C.
\end{array}                                                \tag{2.4}
\]

The constants absorb the finitely many outgoing edges and their fixed
positive rates.  Formal (q\to q) self-reactions, if allowed in a network
presentation, are literal physical self-loops and are contracted; all
genuine (q)-sourced reactions have lower target.

## 3. Two-phase row bounds

Let (L) denote the collection of lower phases and (Q) the phase (q).
Split the corrected open kernel into its (L,Q) blocks and let (E) be
the corrected exit kernel to a base return, service, or included
localization boundary.

If (s\in L), both (r_s) and every lower-source (r_y) are
(O(\delta)).  Therefore (2.2)--(2.3) give

\[
 \|K_{LL}\|+\|K_{LQ}\|+\|E_L\|
       \le C(\delta+\delta^\theta)
       \le C\delta^\theta.                            \tag{3.1}
\]

If (s=q), every (q)-sourced firing either exits or sets a lower phase.
Its corrected mass is (O(1)).  A lower-source competitor has corrected
mass (O(\delta^{1-\theta})); only a competitor whose target is (q)
can leave the phase equal to (q).  Hence

\[
 \|K_{QQ}\|\le C\delta^{1-\theta},
 \qquad
 \|K_{QL}\|+\|E_Q\|\le C.                         \tag{3.2}
\]

This is the precise meaning of "one free (q)-exit."  Arbitrarily many
lower-to-(q) firings may occur before it, but each such recurrent firing
has the small corrected factor in (3.2).

Let (H_L,H_Q) be the row norms of the corrected terminal-payoff kernel,
starting in the two phase types.  The first-step equations and
(3.1)--(3.2) imply

\[
 H_L\le\varepsilon(1+H_L+H_Q),
 \qquad
 H_Q\le C(1+H_L)+\varepsilon_QH_Q,                  \tag{3.3}
\]

where (arepsilon=C\delta^\theta) and
(arepsilon_Q=C\delta^{1-\theta}).  For sufficiently small (delta),
absorption in (3.3) gives

\[
                         H_L\le C\delta^\theta,
 \qquad                  H_Q\le C.                 \tag{3.4}
\]

Equivalently, the two-phase open resolvent is bounded in the corrected
weight.  A first marked open lower-source firing carries
(O(\delta^{1-\theta})) from phase (q) and (O(\delta)) from a lower
phase; the strong Markov property and (3.4) preserve that small factor
through all subsequent open branching.

## 4. Terminal reset at (C=0)

At a cofactor-free base, reset the artificial phase to (dB), where (d)
is the largest degree of a present pure-(B) complex.  If an open reaction
lands at (C=0), its target is (cB\in{cal F}), so (c\le d).  Since
the reaction changes (B) by at most two,

\[
                {M_x(cB)\over M_{x'}(dB)}\le C.       \tag{4.1}
\]

Replacing the post-jump target divisor by the base divisor therefore only
adds a fixed factor to (2.2)--(2.3).  This applies equally when the return
is declared a service.  For (d=0), both base monomials equal one.

An included boundary reached while (C>0) keeps the actual post-jump
target phase, so no reset factor is needed.  The estimates use the
pre-jump localized state; bounded reaction increments make them valid for
the included crossing endpoint.

## 5. Scope boundary

The phase correction repairs the divergent incomplete prefix
(0\to q\to B+C\to q): its later (q\)-exit is the sole free exit, while
the lower-to-(q) recurrence already carries a small monomial ratio.  No
counterexample to the phase table, its normalization, or the terminal
base reset was found.

This audit deliberately does not certify the separate base-return kernel.
In particular, it does not prove that the base Green operator is transient,
that negative active displacement is reached, or that the physical
duration and localization terms have the moments needed for a common
fourth-power Foster episode.
