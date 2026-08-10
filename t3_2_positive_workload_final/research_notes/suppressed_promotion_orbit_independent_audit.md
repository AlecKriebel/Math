# Independent audit of the suppressed four-pair orbit

## Verdict and scope

**PASS**, restricted to the four support pairs and 28 affine-feasible failed
incidences selected by `src/suppressed_promotion_orbit_certificate.py`.
The proof audited is `research_notes/suppressed_promotion_orbit_full_proof.md`.
This verdict supports the pair-level arithmetic

\[
 (1839,187)\longmapsto(1835,187),
\]

but makes no global T3-2 claim.

## Checks replayed

1. **Cleaned macro endpoints.**  Starting from
   \((I,U,V)=(0,M,D)\), the top shell satisfies
   \((I,U,V)=(i,M-i,D+i)\).  Applying each of the six lower edges with
   source in \(\{0,I+U\}\), and then using only the top invariant to return
   to \(I=0\), gives exactly the six endpoints and factorial rewards in
   (2.6).  The calculation is independent of the transient value \(i\).

2. **Killed-shell occupation.**  The birth--death rates in (3.3) give
   Poisson domination with mean at most \(\alpha M/(\mu D)\).  The
   coordinate martingale identity yields (3.6); its deterministic errors
   are \(o_{L^1}(1)\), while the scaled martingale variance is
   \(O(M/D)=o(1)\).  Compensation by
   \(I(M-I)\), \(I\), or \((I)_2\) preserves a uniform exponential moment
   for the transient \(I\)-population.  No moment is claimed or needed for
   the full populations \(U,V\).

3. **All-clock physical cleanup.**  When \(D/M\to\infty\), top death has
   rate at least \(cDI\), versus \(CMI+C(1+I^2)\) for lower interference.
   The displayed endpoint and occupation bounds make the exceptional
   positive factorial cost uniformly integrable.  The bounded-\(M\)
   one-active rows are handled separately: after a zero-source target,
   \(I\le4\), \(U=O(1)\), cleanup fails with probability \(O(D^{-1})\),
   and its positive cost is \(O(D^{-1}\log D)\).

4. **Whole-top equality profile.**  For \(M\asymp D\), the proof now stops
   at the first successful \(I+U\)-source reaction rather than imposing an
   invalid cleanup race against another order-\(N\) clock.  The transient
   shell cost is \(O(1+i\log(i+1))\), the successful direct reward is
   \(-\log N+O(1+\log(i+1))\), and the transient exponential moment gives
   expected drift \(-p\log N+O(1)\).

5. **Balanced cut hazard and extreme ratios.**  Strong connectivity of the
   lower linkage forces a directed edge from
   \(\{0,I+U\}\) to \(\{I,2I\}\).  Conditional Poisson-clock calculus and
   the occupation lemma give the uniform lower bound in (5.7), without an
   independence assumption.  In the \(R\to0\) regime the only positive
   reset contributes \(O(R\log(1/R))\); in the \(R\to\infty\) regime the
   zero-source and degree-one/two exceptional hazards vanish while every
   \(I+U\)-target has a diverging negative factorial reward.

6. **Global potential and classwise conclusion.**  The condition
   \(\ell_I+\ell_V-\ell_U=\log(\mu/\alpha)\) supplies one fixed proper
   corrected factorial potential for the pair.  A fixed linear correction
   does not change a strict logarithmic source-tier exit on every passing
   descriptor.  The failed-descriptor episodes have sufficient duration
   and endpoint integrability for the common-entropy stopping lemma.
   Population-increasing reactions have source molecularity at most one,
   so nonexplosion follows from a linear total-population bound.  Restriction
   to each closed irreducible class then gives positive recurrence.

## Executable replay

The exact orbit, descriptor table, macro displacements, reward signs, and
disjointness were replayed with
`tests/test_suppressed_promotion_orbit_certificate.py` and
`tests/test_two_active_promotion_obstruction.py`: all six focused tests
passed.  The analytic and global flags were left unchanged during this
audit; promotion is a separate release-status action.
