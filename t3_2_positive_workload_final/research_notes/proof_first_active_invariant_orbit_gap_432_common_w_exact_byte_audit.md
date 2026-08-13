# Exact-byte audit of the 432-pair population-Foster theorem

**Hostile proof-first audit, 2026-08-12 PDT.** This note records an
independent strict audit of

~~~text
research_notes/proof_first_active_invariant_orbit_gap_432_common_w_theorem.md
SHA-256 7edab78daabbf7e492851efe5326ccc228adfcb57f02cd5ff55eaa7056e034c8
395 lines / 15,939 bytes
~~~

The verdict is **STRICT PASS** for the theorem's literal pair-level claim.
The proof is global on each fixed population class and does not use the
invalid inference that a terminal strongly connected component of chart
exits must contain a drift start.

## 1. Exact finite scope replay

The audit rehashed and replayed the authoritative support-only certificate:

~~~text
src/active_invariant_orbit_gap_432_certificate.py
SHA-256 31fa24a20e18546e9c623d3aaf6d3b845c1708d5782f86333c02417fa366cd53

tests/test_active_invariant_orbit_gap_432_certificate.py
SHA-256 09c434fc162ff33f51e331e298ec2e35407a8e0501f1a3b8d771bf33c2fe708b
~~~

All nine dedicated tests pass. The replay verifies the disjoint identity

\[
 432=174\ \text{deficiency zero}
       +234\ \text{non-DZ with no feasible corrected-cut failure}
       +24\ \text{exceptional}.                       \tag{1.1}
\]

The corresponding fingerprints are, respectively,

~~~text
all 432
5516d6071b2b9d07b0e4e02613b9caee217ba3ebb0082e21f2bc664e6247ea36
DZ 174
d894c296de7c24e3c855f116228b852ef940b15ac913556ffea9c87e6655a974
non-DZ / no feasible failure 234
4c6420ad47c2ee57736484b213595dde69c3734ce20d19ff4f97aeb31ab77d6a
exceptional 24
051a641f3987ec93b129ad044d96292a97e536e9ef3d2724234dc4af9bfdef69
~~~

Every pair has rank two and a unique primitive nonnegative normal with one
zero and two strictly positive entries. The zero coordinate occurs 144
times in each position. Every one of the 192 feasible failure rows has its
unique active coordinate equal to that invariant-zero coordinate. The
invariant and alignment fingerprints are

~~~text
9dec8108276e9d439c18aacda1ec35d9bac08e097f8833e3446c50b40d8148ca
a9368dd934b7ac6135c3df4866e2322700d3a607dd58f8327aeb709065880ab2
~~~

After removing the 48 deficiency-zero failures, the 24 non-DZ failures are
exactly two 12-pair orbits under species permutations and linkage reversal:

\[
 \begin{array}{c|c|c|c}
 &L_1&L_2&\text{invariant}\\ \hline
 \mathrm I&\{A,A+B\}&\{2A,2C,A+C\}&A+C,\\
 \mathrm {II}&\{A,A+B\}&\{C,2A,B+C\}&A+2C.
 \end{array}                                          \tag{1.2}
\]

Their orbit fingerprints are

~~~text
50804d58a48bb1a2683014442a436761ec0ba0df34f3ef3ac0d1939fe850886
cc76d3c7bcc7942f956f1efc8cf0f718ad1e6e08d911f8f8127ebc3cf8c5002f
~~~

The executable certificate has `recurrence_claim=False`; it enumerates no
orientation, rate, population, or stochastic history.

## 2. Common population potential and nonexplosion

For

\[
 G(x)=K+\sum_i\log(x_i!),\qquad W(x)=G(x)^4,
\]

the choice \(K>1\) makes \(W\ge0\), and a diverging population sequence has
at least one diverging factorial term, so \(W\) is proper on
\(\mathbb N_0^3\). A bounded reaction has
\(|\Delta G|=O(\log(2+|x|))\), and the fourth-power identity in the target is
exact.

Nonexplosion is independent of the Foster argument. A quadratic-source
reaction cannot increase total molecularity in the binary complex universe.
All increasing hazards therefore have degree at most one and bounded jumps.
A linear immigration/Yule comparison bounds total population on finite
physical intervals; bounded total-population sublevels are finite and have
bounded aggregate hazards.

## 3. The bounded-depth Foster lemma

The repaired episode index is exact. If \(N\) is the first positive episode
count whose completed segment visits \(K_0\), then
\(\{j\le N\}\) is measurable at the start of episode \(j\). Every charged
episode starts outside \(K_0\), including the completed hit episode.
Conditional summation therefore gives

\[
 \mathbb E V(X_{\sigma_{N\wedge n}})
 +\mathbb E\sigma_{N\wedge n}
 +\mathbb E(N\wedge n)\le V(x).                      \tag{3.1}
\]

If \(N=\infty\), the episodes contain infinitely many actual jumps. Their
bounded expected accumulated time and monotonicity would give a finite
accumulation time, contradicting nonexplosion. Thus the finite set is hit
in finite mean time.

For the classwise promotion, the target now correctly chooses
\(o,c\in K_0\cap\Gamma\). This intersection is nonempty by the hit result.
There are finitely many prescribed path states and finitely many possible
first-competitor endpoints. Hence exact path following has a uniform
positive probability, and the competitor-return costs have a uniform finite
mean. Geometric retry proves finite mean return to \(o\).

## 4. The 174 and 234 analytic branches

For the 174 deficiency-zero pairs, strong connectivity of both linkage
graphs gives weak reversibility of the full network. Full-network
deficiency zero supplies a positive complex-balanced vector for every
positive rate vector. The class-restricted stochastic product form is
normalizable by the full-lattice product-Poisson sum. Together with
nonexplosion, this gives positive recurrence on every closed irreducible
class.

For a non-DZ/no-failure pair, suppose that the population-generator bound
failed outside every finite class subset. Properness gives a divergent bad
sequence in one fixed affine class. Exact descriptor completeness and the
necessity half of affine feasibility make its descriptor feasible. Since
the pair has no feasible corrected-cut failure, the corrected superlevel cut
forces, for the actual arbitrary strong orientation, a D-descending reaction
sourced in the literal global top S-tier.

The frozen quantitative entropy calculation gives, with \(A_n\) the maximal
enabled source propensity and \(g_n\to\infty\) its certified D-gap,

\[
 {\cal L}G(x_n)\le-cA_ng_n,
 \quad\sum_ra_r(x_n)\le CA_n,
 \quad |\Delta_rG(x_n)|\le C\log R_n.                \tag{4.1}
\]

Here \(A_n\) is bounded below by a positive labelled rate because a maximal
source is enabled. Also \(G(x_n)\asymp R_n\log R_n\). In the exact
fourth-power expansion, the largest positive remainder divided by the
negative leading term is at most

\[
 {C(\log R_n)^2\over G(x_n)g_n}\longrightarrow0.     \tag{4.2}
\]

Thus \({\cal L}W(x_n)\to-\infty\), contradicting the bad sequence. This is
a statewise generator bound, not a chart-local drift-or-exit assertion.

The exact analytic dependency bytes replay as

~~~text
research_notes/s_tier_superlevel_cut_and_affine151_corrected.md
d91f369d34cadfb28ddb872df8fb9f6d17799ec207da29933037f55ae95f0407
research_notes/stoichiometric_gate_feasibility.md
27b40b61903ae6c2e223d007ec08323ec9aec10e9198deb99d2d7c60d878d007
research_notes/universal_fourth_power_one_active_interface.md
9d4239f4fc6b45a9522b94b09523c9f98ac7a3b089c919bd9594f12409c78cc2
~~~

## 5. The two exceptional service families

In type II, fix \(M=A+2C>0\). Strong connectivity forces an
\(A+B\)-sourced edge to \(A\), and every nonself edge out of \(B+C\) lands
at \(C\) or \(2A\). Hence the aggregate B-removal rate is

\[
 B(\delta_1A+\delta_2C)\ge c_MB.                    \tag{5.1}
\]

All B-creating sources are among the classwise bounded populations
\(A,C,2A\). B-neutral hazards and their factorial increments are likewise
bounded classwise. A removal changes \(G\) by
\(-\log B+O_M(1)\), so

\[
 {\cal L}W\le-c_MB G^3\log B+O_M(G^3\log B)
 \longrightarrow-\infty.                            \tag{5.2}
\]

There is no activation wait in this branch.

In type I, fix \(M=A+C\). Whenever \(A>0\), the forced arrow
\(A+B\to A\) has rate \(\delta AB\), whereas the reverse birth and the
entire A/C phase have bounded classwise rates. Dividing its generator
bound by the all-clock hazard proves a one-jump reward of order
\(-G^3\log B\).

At \(A=0\), the cases \(M=0\) and \(M=1,C=1\) are absorbing singletons. If
\(M\ge2\), the only enabled source is \(2C\), and every actual nonself edge
from it lands at \(2A\) or \(A+C\). This first jump leaves B fixed, costs at
most \(O_M(G^3)\), and activates \(A>0\). Appending the next ordinary
all-clock jump yields

\[
 \mathbb E[\Delta W+\tau]
 \le C_MG^3-c'_MG^3\log B+C_M\le-1                 \tag{5.3}
\]

for large B. Both endpoint and duration are integrable; the rule has depth
one or two and retains every clock. Since A and C range over a finite
invariant phase, bounded B is a finite class subset. Lemma 3.1 applies.

## 6. Verdict and claim boundary

The three branches in (1.1) are disjoint and exhaustive. Each proves
nonexplosion and positive recurrence for arbitrary strongly connected
labelled orientations and arbitrary fixed positive rates on every closed
irreducible population class. **STRICT PASS** applies to exactly this
pair-level theorem and its pinned finite identity.

The result does not itself certify the final union of all global support
branches. That later composition must pin the authoritative 432 certificate
and prove the intended precedence/set union. No such global-union claim is
used in this verdict.
