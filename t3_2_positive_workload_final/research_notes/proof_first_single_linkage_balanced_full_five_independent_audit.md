# Independent audit of the balanced full-five carrier theorem

**Audit date:** 2026-08-12 PDT  
**Verdict:** **MATHEMATICAL PASS (strictly local scope).**

The audited theorem is Theorem 5.1 of
`proof_first_single_linkage_structural_reduction_and_mesoscopic_gap.md`,
frozen as part of the exact target bytes

```text
266d7dccfc0157d7ebb6ac2ae6ad5c4e0d5feb82bca5591472e44dc8e4f94c83
    research_notes/proof_first_single_linkage_structural_reduction_and_mesoscopic_gap.md
```

After this audit, the sole byte-level repair moved `\tag{5.3}` from the
last row of the inner `aligned` environment to the surrounding display.  The
header-identical derivative is frozen at

```text
8a34f9934f9ffdd078850070de561aa3cf3f734a9fbeb2e4f08bc68c5e106262
    research_notes/proof_first_single_linkage_structural_reduction_and_mesoscopic_gap.md
```

A direct diff against the audited bytes contains only that tag relocation.
The old target reproduces the standard `amsmath` error `\tag not allowed
here`; the derivative compiles successfully to a ten-page PDF with Tectonic.
The theorem statement, proof text, and every mathematical symbol are
otherwise identical.  The mathematical PASS therefore applies verbatim to
the derivative hash.

The theorem is valid for every strongly connected labelled orientation of

\[
                    \{0,C,2C,A+C,B+C\},
\tag{A.1}
\]

every positive fixed rate vector, every fixed closed irreducible class, and
every balanced cofactor-free entrance.  Its stopping rule retains all
physical clocks, includes the causing terminal reaction on every branch,
has the stated endpoint and duration moments, is independent of the fixed
linear correction \(\ell\), and gives the claimed common
factorial-linear fourth-power drift.  The proof in the target is compressed
but complete; the estimates below supply an independent replay of every
compressed step.

No support, orientation, population box, or reaction-word list is used.
The same proof works for every sub-support in the theorem's displayed
interval whenever its hypotheses are nonvacuous.  The full-five support
(A.1) is the only non-deficiency-zero balanced support and is the case
needed by the final one-linkage composition.

## 1. Frozen and invariant alternatives

Write

\[
 q_A=A+C,\qquad q_B=B+C,\qquad
 \mathcal K=\{q_A,q_B\},\qquad
 \mathcal P=\mathcal C\cap\{C,2C\}.
\tag{A.2}
\]

At a state \(x=(a,b,0)\), no source except \(0\) can be enabled.  If
\(0\notin\mathcal C\), the state is therefore absorbing and its class is a
singleton.  If \(0\in\mathcal C\) but
\(\mathcal P=\varnothing\), the linear functional

\[
                              H=A+B-C
\tag{A.3}
\]

has value zero on every complex in \(\{0,q_A,q_B\}\), so it is an exact
stoichiometric invariant.  On \(C=0\), \(H=a+b=N\).  One fixed class can
therefore contain at most one such value of \(N\), contrary to the
theorem's premise of arbitrarily large balanced entrances.  Thus the only
nonvacuous case has \(0\in\mathcal C\) and
\(\mathcal P\ne\varnothing\).  In the full-five support both conditions
hold.

## 2. Exact clean population ledger

At \(C=0\), retain the actual first \(0\)-sourced reaction.  Call it a
**pure launch** if its target is in \(\mathcal P\), and a **mixed launch**
if its target is in \(\mathcal K\).  While \(C>0\), temporarily use only
\(\mathcal K\)-sourced reactions to define the clean skeleton.

Every internal \(\mathcal K\)-reaction \(q_i\to q_j\), when that labelled
edge is present, preserves both \(C\) and \(A+B\).  Every exit

\[
               q_i\longrightarrow z,qquad
               z\in\{0,C,2C\},
\tag{A.4}
\]

lowers \(A+B\) by exactly one.  A pure launch raises \(A+B\) by zero,
whereas a mixed launch raises it by one.  It follows pathwise that:

* a pure launch followed by the first mixed exit stops with
  \(A+B=N-1\);
* a mixed launch whose first mixed exit lands in \(0\) returns to \(C=0\)
  with \(A+B=N\), and is a neutral attempt;
* a mixed launch whose first exit lands in \(C\) or \(2C\), followed by
  one more mixed exit, stops with \(A+B=N-1\).

There are at most two mixed exits before service or neutral return.  Mixed
internal transitions preserve \(C\), and the above launch/exit list gives

\[
                         1\le C\le3
\tag{A.5}
\]

throughout every open window and at every clean service endpoint.  In
particular, the terminal state is a real post-reaction state and not a
contracted return.  A neutral attempt need not return to the identical
\((a,b,0)\), because internal transitions may transfer population between
\(A\) and \(B\); it returns with the exact total \(A+B=N\).  The
localization below controls this harmless redistribution.

## 3. Uniform clean exits for every strong orientation

Let \(L_N=\lfloor N^{1/4}\rfloor\), and stop at and include the reaction
which first makes the sum of the number of internal mixed transitions and
neutral attempts equal to \(L_N\).  Before this cutoff, every reaction has
bounded increment, so for all sufficiently large \(N\),

\[
                  A\wedge B\ge \epsilon N/2.
\tag{A.6}
\]

At an open state, the aggregate mixed-source rate is

\[
 C\bigl(\kappa_A^{\rm out}A+\kappa_B^{\rm out}B\bigr)
       \ge c_\epsilon NC,
\tag{A.7}
\]

where the two aggregate outgoing constants are positive by strong
connectivity.  Because \(\mathcal K\) is a nonempty proper vertex block,
strong connectivity gives an edge from \(\mathcal K\) to its complement.
Its source population is at least \(\epsilon N/2\), and the denominator in
(A.7) is at most \(CNC\).  Hence at every exposed mixed race the chance of
leaving \(\mathcal K\) is bounded below by a fixed \(\delta>0\).  The
number of internal mixed transitions before an exit therefore has a
geometric tail, uniformly over the balanced cone before localization.

There is also a fixed service probability per attempt.  If an outgoing
\(0\)-edge lands in \(\mathcal P\), that launch has fixed positive
probability and its subsequent mixed exit is a service.  If no such edge
exists, every outgoing \(0\)-edge lands in \(\mathcal K\).  Take a directed
path from \(0\) to \(\mathcal P\), which exists by strong connectivity,
and inspect its first entrance into \(\mathcal P\).  Because no
\(0\)-edge enters \(\mathcal P\), this first entrance is an edge
\(\mathcal K\to\mathcal P\).  The chance that this particular edge wins
the first mixed race is bounded below by a fixed constant using (A.6)--
(A.7); after that landing, a second mixed exit occurs geometrically and
completes a service.

Thus the number of neutral attempts has a geometric tail.  A geometric sum
of the geometric mixed-block lengths has an exponential tail: if \(R\) is
the total number of exposed mixed races and neutral attempts in the clean
skeleton, then for constants depending only on the fixed graph, rates, and
\(\epsilon\),

\[
             \mathbb P\{R\ge r\}\le Ce^{-cr},
             \qquad \mathbb E(1+R)^p\le C_p.
\tag{A.8}
\]

This proves the localization estimate
\(\mathbb P\{R\ge L_N\}\le Ce^{-cL_N}\), which is smaller than every
power of \(N\).  The argument uses only directed cuts and conditional
mass-action races, so it is uniform over an arbitrary fixed strong
orientation and arbitrary fixed positive rates.

## 4. Restoration of every physical clock

At an open state, every source outside \(\mathcal K\) belongs to
\(\{0,C,2C\}\).  By (A.5), the sum \(q_{\rm pure}\) of all such physical
propensities is bounded above by a constant.  Together with (A.7), the
exact exponential race gives

\[
 \mathbb P\{\text{a pure-source clock wins the next open race}
                 \mid\mathcal F\}
       ={q_{\rm pure}\over q_{\rm pure}+q_{\rm mixed}}
       \le {C\over N}.
\tag{A.9}
\]

Use the clean skeleton only to index these races.  In the physical chain,
stop at and include the first pure-source winner and label it \(E\).
Conditional on a clean history of length \(R\), the union bound in (A.9)
is \(CR/N\).  Before that included reaction, every population displacement
is bounded by a constant times \(R\), and the causing reaction is binary.
Multiplying the conditional union bound by any fixed polynomial of the
history and using (A.8) yields

\[
 \mathbb E\!\left[
   (1+|X_\tau-x|)^p;E\right]\le {C_p\over N}.
\tag{A.10}
\]

Label by \(B\) the actual reaction which first reaches the localization
threshold, with priority given to \(E\) if it is simultaneously a pure
competitor.  Then \(B\) implies that the clean skeleton reaches
\(L_N\), and its centered endpoint displacement is at most a fixed
multiple of \(L_N\).  Equation (A.8) gives, for every fixed \(p,M\),

\[
 \mathbb E[(1+|X_\tau-x|)^p;B]\le C_{p,M}N^{-M}.
\tag{A.11}
\]

On the remaining event \(D\), the exact ledger of Section 2 gives

\[
                 A_\tau+B_\tau=N-1,\qquad C_\tau\le3.
\tag{A.12}
\]

Equations (A.8)--(A.12) give the endpoint and probability parts of (5.3),
including \(\mathbb P(D^c)\le C/N+C_MN^{-M}\).  Every reaction clock has
been retained: the \(0\)-clock at \(C=0\) is the designated physical
launch; every mixed clock is part of the skeleton; and the first firing of
any other clock is the included physical endpoint \(E\).

## 5. Physical duration

At each neutral visit to \(C=0\), the holding time is exponential with the
fixed aggregate outgoing \(0\)-rate \(\lambda_0>0\).  By (A.8), the number
of such visits is geometrically dominated.  Every open holding time has
total rate at least \(c_\epsilon N\) by (A.7); adding pure clocks only makes
it shorter.  Geometric-sum moment bounds therefore give

\[
                         \mathbb E(1+\tau)^p\le C_p.
\tag{A.13}
\]

The same conditioning used in (A.10), now with polynomial moments of the
preceding exponential holding times, proves

\[
 \mathbb E[(1+|X_\tau-x|+\tau)^p;E]\le C_p/N.
\tag{A.14}
\]

On \(B\), at most \(O(L_N)\) empty-face waits and faster open waits occur.
Their conditional polynomial moments grow at most polynomially in \(L_N\),
while (A.8) is exponential.  Thus

\[
 \mathbb E[(1+|X_\tau-x|+\tau)^p;B]\le C_{p,M}N^{-M}.
\tag{A.15}
\]

Together with the clean geometric moments, these equations prove every
duration assertion in (5.3).  In particular, the time used in the drift is
the actual elapsed CTMC time, not the number of retained transitions.

## 6. Factorial-linear entropy decrement

Fix \(\ell\in\mathbb R^3\), choose \(K_\ell\) so that

\[
 G_\ell(z)=K_\ell+sum_i\log(z_i!)+\ell\cdot z\ge1,
 \qquad W_\ell=G_\ell^4,
\tag{A.16}
\]

and note that the stopping rule above does not depend on \(\ell\).  On
\(D\), write \(u=A_\tau-a\) and \(v=B_\tau-b\).  By (A.12),
\(u+v=-1\).  Before localization, \(|u|+|v|=O(L_N)=o(N)\), and
\(a,b\ge\epsilon N\).  The uniform factorial finite-difference expansion
therefore gives

\[
 \log\frac{(a+u)!(b+v)!}{a!b!}
   =u\log a+v\log b
      +O_\epsilon\!\left(1+\frac{u^2+v^2}{N}\right).
\tag{A.17}
\]

Since \(a/N,b/N\in[\epsilon,1]\),

\[
 u\log a+v\log b
  =-\log N+u\log(a/N)+v\log(b/N)
  \le-\log N+C_\epsilon(|u|+|v|).
\tag{A.18}
\]

The clean history has exponential moments by (A.8), so the expectation of
the remainder in (A.17)--(A.18) is \(O_{\epsilon}(1)\).  The terminal
\(C\)-factorial is bounded by (A.12), and the fixed linear correction has
increment \(O_\ell(1+|u|+|v|)\).  Thus the clean contribution is
\(-\log N+O_{\epsilon,\ell}(1)\).

On \(E\), the state remains within \(O(L_N)\) bounded jumps of the balanced
entrance, so

\[
 |G_\ell(X_\tau)-G_\ell(x)|
       \le C_\ell(1+|X_\tau-x|)\log(N+2).
\tag{A.19}
\]

Equations (A.14) and (A.19) show that the absolute \(p\)-th moment of this
increment on \(E\) is \(O(N^{-1}\log^p N)\).  Equation (A.15) makes the
boundary contribution smaller than every power of \(N\).  Since
\(\mathbb P(D)=1-O(N^{-1})\), these estimates prove

\[
 \mathbb E\,[G_\ell(X_\tau)-G_\ell(x)]
       \le-\log N+O_{\epsilon,\ell}(1),
 \qquad
 \mathbb E|G_\ell(X_\tau)-G_\ell(x)|^p
       \le C_{p,\epsilon,\ell}\log^p N.
\tag{A.20}
\]

This is exactly (5.4) and the moment estimate (5.12) for the actual endpoint.

## 7. Common fourth-power drift

At the balanced entrance,

\[
                         G_\ell(x)\asymp_\epsilon N\log N.
\tag{A.21}
\]

Put \(G=G_\ell(x)\) and \(Z=G_\ell(X_\tau)-G_\ell(x)\).  The exact identity

\[
 (G+Z)^4-G^4=4G^3Z+6G^2Z^2+4GZ^3+Z^4
\tag{A.22}
\]

and (A.20) give

\[
\begin{aligned}
 \mathbb E[W_\ell(X_\tau)-W_\ell(x)]
 &\le -4G^3\log N+O(G^3)\\
 &\quad+O(G^2\log^2N+G\log^3N+\log^4N).
\end{aligned}
\tag{A.23}
\]

By (A.21), every term on the second line is
\(o(G^3\log N)\).  The physical duration has bounded mean by (A.13), so it
is lower order as well.  Therefore, for every fixed \(\ell\) and all large
balanced entrances,

\[
 \mathbb E_x[W_\ell(X_\tau)-W_\ell(x)+\tau]
       \le-c_{\epsilon,\ell}G_\ell(x)^3\log N.
\tag{A.24}
\]

The same physical stopping rule was used throughout; only constants in the
entropy estimates depend on \(\ell\).  This proves the common-potential
quantifier in (5.5), not merely a Lyapunov function selected after observing
the path.

## 8. Certification boundary

The balanced theorem is a complete local proof, not a heuristic or a finite
verification.  Its only inputs are the exact launch/exit ledger, strong
connectivity, fixed positive rates, exponential-clock races, and elementary
factorial estimates.  It is uniform over arbitrary strong orientations in
the theorem's sense: constants may depend on the fixed graph and rates but
not on \(a,b,N\).

This PASS certifies only Theorem 5.1 at the frozen target hash.  It does not
certify the separated-scale theorem, the complete one-linkage composition,
or the global T3-2 result.  Those conclusions require their own frozen
composition and independent audits.
