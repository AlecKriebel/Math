# Version 1.1 mathematical audit: closure, rate limit, and ACK Example 4.1

**Audit date:** 10 August 2026
**Scope:** the proposed lifted state-cycle lemma and its state-space
consequences; the rate-dependence calculation; and the exact
comparison with Anderson, Cappelletti, and Kim (2020), Example 4.1.  The
load-bearing marked-target recurrence proof was not reopened.

## Verdict

**Verdict: the state-space strengthening is valid.**  The lifted state-cycle
lemma is valid.  Every reachability set of a weakly reversible stochastic
reaction network is a closed communicating class.  This conclusion needs
neither a single linkage class nor the bimolecular assumption.

The fixed-state limit in the rate-dependence example is

\[
 D_0(m,A)\longrightarrow a_m(1+p_m)>0
 \qquad (\kappa_2\downarrow0),
\]

and the fixed-rate large-\(m\) coefficient remains exactly
\(-\kappa_2/(\kappa_1+\kappa_2)\).

The ACK Example 4.1 comparison also survives exact audit.  A short
complete target-following episode has reward
\(-\alpha\log n+O(1)\) with an explicit \(\alpha>0\), so the comparison is
certified for its inclusion in the manuscript.

## 1. Lifted state-cycle lemma

Let a genuine reaction channel \(y\to y'\) be enabled at
\(x=r+y\), where \(r=x-y\in\mathbb N_0^d\).  Weak reversibility places this
edge on a directed complex cycle, so there is a directed path

\[
 y'=z_0\longrightarrow z_1\longrightarrow\cdots
 \longrightarrow z_m=y.
\]

At the population state \(r+z_i\), the source \(z_i\) is present because
\(r\ge0\).  Thus the \(i\)-th reaction is enabled, and its successor is

\[
 (r+z_i)-z_i+z_{i+1}=r+z_{i+1}.
\]

Starting from the post-jump state \(x'=r+y'=r+z_0\), these enabled
transitions lift the complex path and end at \(r+y=x\).  Each specified
finite channel sequence has positive probability under positive mass-action
rate constants.  This proves that every enabled genuine population
transition has a population return path.

### State-space consequences

Write \(x\leadsto y\) for population accessibility.

1. If \(x=x_0\to x_1\to\cdots\to x_k=y\), reverse each one-step edge by its
   lifted return path, in reverse order.  Concatenation gives
   \(y\leadsto x\).  Hence accessibility is symmetric.
2. The reachability set
   \(\Gamma(x)=\{y:x\leadsto y\}\) is communicating: every member returns to
   \(x\), and two members communicate through \(x\).
3. It is closed: if \(z\in\Gamma(x)\) and \(z\to w\), then
   \(x\leadsto z\to w\), so \(w\in\Gamma(x)\).
4. Since accessibility is an equivalence relation, every communicating
   class is one such \(\Gamma(x)\), and every communicating class is closed.
5. Therefore an arbitrary initial state already lies in one closed
   irreducible component.  There is no separate entrance problem; the
   relevant entrance time is zero.

The conclusion is graph-theoretic.  The one-linkage and bimolecular
hypotheses enter the positive-recurrence proof later, not this lemma.

### Adversarial edge-case audit

- **Zero complex.** If a source or intermediate complex is zero, it is
  enabled at every \(r+0=r\).  The algebra above is unchanged.
- **Boundary states.** Enabledness of the first reaction gives
  \(r=x-y\ge0\).  Every lifted state is \(r+z_i\ge z_i\), so the return path
  never requests a missing reactant.
- **Parity and lattice restrictions.** The lifted path uses actual reaction
  displacements and returns to its starting state.  It stays in the same
  stoichiometric lattice coset and does not assert communication between
  distinct parity or conservation classes.
- **Multiple linkage classes.** A fired edge and its return path lie in the
  same weakly reversible linkage class.  No path between linkage classes is
  needed.
- **Parallel channels.** Choose the actual fired labelled channel.  Its
  target has a return path.  Aggregating exact parallel channels does not
  change the population accessibility relation.
- **Identical population displacements.** The proof never infers a source or
  target from the displacement; it selects one actual enabled channel that
  realizes the edge.  Distinct channels with the same displacement therefore
  cause no ambiguity.
- **Absorbing singletons.** A state with no genuine enabled transition has
  reachability set \(\{x\}\).  Conversely, under the symmetry result, a
  singleton communicating class cannot have a genuine outgoing transition,
  because its successor would communicate with it.  Its stationary law is
  the point mass.
- **Null self-channels.** A formal \(y\to y\) changes no population state and
  may be deleted from the generator.  The lemma concerns genuine one-step
  population transitions.

### Prior literature

Paulevé, Craciun, and Koeppl, *Dynamical Properties of Discrete Reaction
Networks*, Journal of Mathematical Biology **69** (2014), 55--72,
doi:10.1007/s00285-013-0686-2, Lemmas 4.5--4.6, record precisely this return
property.  They call it “recurrence” of a discrete reaction network: every
enabled transition can return.  That terminology must be distinguished from
positive recurrence of a Markov chain.  Their Lemma 4.6 proves that every
weakly reversible reaction network has this discrete return property.
Anderson, Cappelletti, and Kim (2020) also invoke that lemma near their own
Lemma 3.2.  The manuscript should retain the elementary proof above and cite
Paulevé--Craciun--Koeppl for precedent.

## 2. Corrected rate-dependence calculation

For

\[
 0\xrightarrow{\kappa_0}A
 \xrightarrow{\kappa_1}A+B
 \xrightarrow{\kappa_2}0,
\]

the exact recursion is

\[
 D_0(m,A)=a_m+p_m(b_m+q_mc_m),
\]

where

\[
\begin{aligned}
 a_m&=\frac{\kappa_0\log m}{\kappa_0+\kappa_1m},
&p_m&=\frac{\kappa_1m}{\kappa_0+\kappa_1m},\\
 b_m&=\frac{\kappa_0\log m}
 {\kappa_0+(\kappa_1+\kappa_2)m},
&q_m&=\frac{\kappa_2m}
 {\kappa_0+(\kappa_1+\kappa_2)m},\\
 c_m&=-\frac{\kappa_1(m-1)}
 {\kappa_0+\kappa_1(m-1)}\log(m-1).
\end{aligned}
\]

For fixed \(m\), \(\kappa_0\), and \(\kappa_1\), as
\(\kappa_2\downarrow0\),

\[
 b_m\to a_m,\qquad q_m\to0,
\]

while \(a_m,p_m,c_m\) do not depend on \(\kappa_2\).  Therefore

\[
 D_0(m,A)\to a_m+p_ma_m=a_m(1+p_m)>0.
\]

For fixed positive rates and \(m\to\infty\),

\[
 a_m,b_m=O\!\left(\frac{\log m}{m}\right),\quad
 p_m=1+O(m^{-1}),\quad
 q_m=\frac{\kappa_2}{\kappa_1+\kappa_2}+O(m^{-1}),
\]

and

\[
 c_m=-\log m+O\!\left(\frac{\log m}{m}\right).
\]

Hence

\[
 D_0(m,A)=
 -\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
 +O\!\left(\frac{\log m}{m}\right).
\]

Thus the qualitative conclusion about the absence of a bound on the location
or diameter of \(K\), uniform over all positive rate vectors and depending
only on species and complex counts, remains valid.

## 3. Exact ACK Example 4.1 comparison

Use the rate-labelled directed cycle

\[
 A\xrightarrow{\kappa_1}A+B
 \xrightarrow{\kappa_2}A+C
 \xrightarrow{\kappa_3}C
 \xrightarrow{\kappa_4}2B
 \xrightarrow{\kappa_5}A.
\]

### Unshifted entropy drift

At \(x_n=(n,1,0)\), only the first two reactions are enabled.  For ACK's
unshifted entropy-like function, the first reaction changes the \(B\) term
from its value at one molecule to its value at two molecules, an increment
\(2\log2-1\).  The second reaction replaces one \(B\) by one \(C\) and has
zero increment.  Therefore

\[
 \mathcal A V(x_n)=\kappa_1n(2\log2-1)\longrightarrow+\infty,
\]

exactly as in ACK Example 4.1.

### Reachable carried target and path

Start ACK's population chain at \((1,0,0)\).  For \(n\ge2\), repeating the
reaction word

\[
 (A\to A+B),(A\to A+B),(2B\to A)
\]

\(n-2\) times reaches \((n-1,0,0)\).  Three further firings of
\(A\to A+B\) reach \((n-1,3,0)\), and a firing of \(2B\to A\) reaches
\((n,1,0)\) with carried target \(A\).  Thus
\(((n,1,0),A)\) is an explicitly reachable marked state.

Take the fixed target-following path

\[
 A\longrightarrow A+B\longrightarrow A+C\longrightarrow C
\]

and use \(C\) as the terminal complex.  The lifted phase populations are

\[
 (n,1,0),\quad(n,2,0),\quad(n,1,1),\quad(n-1,1,1).
\]

Put \(S=\kappa_1+\kappa_2+\kappa_3\) and

\[
 L_1=n(\kappa_1+2\kappa_2)+2\kappa_5,
 \quad L_2=nS+\kappa_4,
 \quad L_3=(n-1)S+\kappa_4.
\]

The exact one-step rewards at the four phases and continuation probabilities
are

\[
\begin{aligned}
 d_A&=0,
&p_0&=\frac{\kappa_1}{\kappa_1+\kappa_2},\\
 d_{A+B}&=\frac{\kappa_1n}{L_1}\log2
          +\frac{2\kappa_5}{L_1}\log n,
&p_1&=\frac{2\kappa_2n}{L_1},\\
 d_{A+C}&=\frac{\kappa_4}{L_2}\log n,
&p_2&=\frac{\kappa_3n}{L_2},\\
 d_C&=-\frac{(n-1)S}{L_3}\log(n-1).&&
\end{aligned}
\]

Each source has one outgoing channel, so the conditional designated-edge
factors are one.  The complete marked-target episode reward is therefore

\[
 J_n=p_0\bigl[d_{A+B}+p_1(d_{A+C}+p_2d_C)\bigr].
\]

This is an exact formula, not a floating-point estimate.  Since

\[
 p_1\to\frac{2\kappa_2}{\kappa_1+2\kappa_2},\qquad
 p_2\to\frac{\kappa_3}{S},\qquad
 d_C=-\log n+o(\log n),
\]

while \(d_{A+B}=O(1)\) and \(d_{A+C}=o(1)\),

\[
 J_n=-\alpha\log n+O(1),
\]

where

\[
 \alpha=
 \frac{\kappa_1}{\kappa_1+\kappa_2}
 \frac{2\kappa_2}{\kappa_1+2\kappa_2}
 \frac{\kappa_3}{\kappa_1+\kappa_2+\kappa_3}>0.
\]

This calculation isolates the target augmentation cleanly: on the same
sequence where ACK's unshifted one-step entropy drift tends to positive
infinity, the complete carried-target episode has strictly negative
logarithmic drift.

## 4. Deterministic verification added

Version 1.1 adds exact standard-library checks for:

- lifted return cycles with the zero complex and boundary states;
- multiple weakly reversible linkage classes;
- parallel channels and distinct channels with identical displacement;
- symmetry and closure of finite reachability sets with parity restrictions;
- an absorbing singleton;
- the corrected fixed-\(m\), \(\kappa_2\downarrow0\) limit;
- the exact coefficient \(-\kappa_2/(\kappa_1+\kappa_2)\);
- scalar-envelope monotonicity on an additional exact rational grid;
- ACK's unshifted generator drift;
- explicit reachability of the carried target in ACK Example 4.1;
- the complete ACK episode formula, checked against the generic
  falling-factorial identity through exact rational prime-exponent
  signatures; and
- normalized regenerative occupation and stationary flux on a finite
  three-state CTMC cycle.

These checks are deterministic and use no floating point.  They calibrate
finite algebraic interfaces only: no finite atlas proves the universal
theorem, no random test proves recurrence, \(K\) is not enumerated, and no
useful rate-uniform bound on \(K\) is certified.  The universal theorem
remains analytic.
