# Independent acceptance: the nonnegative-potential Hardy–Rellich supplement

14 October 2026. Additional audit within the same shared PASS1; the earlier two-proof acceptance remains separately pinned.

**PASS for the exact supplementary artifact pinned in `NONNEGATIVE_RELLICH_AUDIT_MANIFEST.json`.** For the proposed solution-free core, strict positive \(C^2\) leading weight, \(Q\ge4\), \(W\ge0\), and \(S_Q[V]\ge0\), the core implies a positive coefficient-one Bessel solution on the entire fixed \((0,R)\), with no additional endpoint condition. The proof needs only radial tests, which are finite-energy original spatial tests even on the axis.

## Independently checked gates

1. The exact radial integration-by-parts identity cancels the complete \((Q-1)(V/r^2-V'/r)\) correction and leaves \(\mathfrak q[v']\ge0\). Derivatives of compact radial tests are precisely compact smooth functions with zero ordinary integral. The proof neither drops this constraint nor changes its measure.
2. With \(t=\log r\), \(U(t)=r^{-2}V(r)\), the exact transformed side condition is \(U''\le(Q-1)U\). Reversing the parameter from an arbitrary fixed interior point and applying variation of constants yields
   \[
   V(r)\le C r^{2-\sqrt{Q-1}}
   \]
   near zero. The integral kernel has the required sign. Every formula is evaluated over a finite interval before taking the bound; no unproved limiting value of \(U\) is assumed.
3. A unit-ordinary-integral bump \(\eta_\delta(r)=\delta^{-1}\eta(r/\delta)\) has leading derivative cost at most
   \[
   C_\eta\delta^{Q-2-\sqrt{Q-1}}.
   \]
   The exponent is strictly positive for every integer \(Q\ge4\).
4. The sign \(W\ge0\) gives the correct one-sided estimate \(\mathfrak q[\eta_\delta]\le C_\eta\delta^\beta\). No estimate on the absolute potential energy, two-sided convergence of the form, or form-norm density statement is asserted or needed.
5. For any fixed compact test \(h\), the bump can be supported disjointly near zero. Thus \(h-(\int h)\eta_\delta\) is an admissible zero-mean test with no cross terms. Its nonnegative form and the one-sided bump estimate imply \(\mathfrak q[h]\ge0\) by taking \(\delta\downarrow0\).
6. The separately pinned Hardy positivity lemma then gives a strictly positive flux-classical solution on the full interval at coefficient one. It does not impose endpoint values or shrink the interval.

The stated local extension is also accepted: it is enough that the sign \(W\ge0\) and the side condition hold on some neighborhood of zero. Real \(W\) elsewhere is permitted because the correction eventually lies in that neighborhood.

This supplement also proves necessity for any well-defined stronger inequality with an additional nonnegative independent-function remainder under these same hypotheses, simply by dropping that remainder. It does not identify the chosen independent function with the positive solution.

## Scope boundary

The exponent used here is negative when \(Q=3\), so this proof makes no historical-dimensional claim. The result does not contradict the separately audited real-potential counterexample, whose potential is negative near zero. The source's literal remainder already contains an assumed positive solution and remains logically distinct from the proposed solution-free core. The original informal source question is not promoted to a single fully resolved theorem by this acceptance.

The only analytical dependency is the exact pinned Hardy proof. Relevant source formulas are GJR v3 Theorem 1.3, [versioned primary PDF](https://arxiv.org/pdf/2404.05510v3). The supplement's elementary argument is self-contained apart from that already audited positivity lemma.
