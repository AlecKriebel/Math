# Independent audit: strong selection and low order

Scope: the disposable package at
`work/package`.  All manuscript and certificate assertions are treated as
hypotheses.  No delivered program has been executed in this audit.  Scratch
algebra and direct reading of the cited source are independent checks.

## 2026-08-22T19:30:50Z — checkpoint 1 (completion estimate: 35%)

### Strongest verified result

The complete-directed-support expansion in Theorem 2 / equations (2.10),
(5.4)–(5.16) is correct for each fixed positive weighting and every `n >= 3`.
Writing `epsilon=1/r` and

`a_uv=(d_v^- - w_uv)/w_uv`,

direct first-step differentiation gives

`q_{ij}=epsilon(a_ij+a_ji)/[n(n-2)] + O(epsilon^2)`

and

`q_i=1/n + epsilon [O_i+(O_i+I_i)/(n-2)]/n^2
      + O(epsilon^2)`.

Uniform averaging therefore gives

`rho(W,r)=(n-1)/n-T_dir/[n^2(n-2)r]+O(r^-2)`.

The complete baseline has the same formula with
`T_dir=n(n-1)(n-2)`.  For a target column containing `m=n-1`
positive weights `x_1,...,x_m`,

`(sum x_i)(sum 1/x_i)-m^2
 = sum_{i<j}(x_i-x_j)^2/(x_i x_j)`.

This proves `T_dir-n(n-1)(n-2)=E_dir`, including the stated coefficient.
The summands are unchanged by a positive rescaling of any incoming column,
and vanish exactly when that column is constant.  After normalization this is
exactly `P=J_n`; raw column constants cancel from every parent competition, so
equality is equality of the full chains, not only of the asymptotics.

Locations: compiled PDF p. 6 (statement) and pp. 12–14 (proof); source
`sections/02_model_results.tex`, lines 85–111, and
`sections/05_strong_selection.tex`, lines 42–126.

### Citation check in progress

The cited Tkadlec–Pavlogiannis–Chatterjee–Nowak source uses the same edge
orientation (`u -> v` means that `u` can replace dead target `v`), uniform
initialization, no self-loops, advantageous fitness, and allows directed and
weighted graphs.  Its main-text Theorem 1 states eventual strict suppression
for every fixed noncomplete graph; its model restricts attention to strongly
connected graphs.  Thus the manuscript invokes it only inside its actual
hypothesis range.  I am checking the source proof and the manuscript's separate
reducible closure before marking this item complete.

### Exact open gap at this checkpoint

Triangle elimination/factorization, both weighted-K4 certificates, their
boundary extensions, monotonicity, and all endpoint cases remain to be
independently reconstructed.  The cited theorem's proof, rather than only its
statement, also remains to be checked.

## 2026-08-22T19:44:55Z — checkpoint 2 (completion estimate: 80%)

### Cited noncomplete-support theorem: verified against the source

The citation is substantively correct.  The published article's model (main
PDF pp. 3–4) has no self-loops, uniform singleton initialization, target-first
death uniformly at random, and source `u` chosen at dead target `v`
proportionally to `fitness(u) w_{u,v}`.  It allows asymmetric directed weighted
graphs and restricts its fixation/extinction discussion to strongly connected
graphs.  Main-text Theorem 1 on p. 7 says: for a fixed noncomplete graph,
possibly directed and/or weighted, some `r* > 1` makes fixation strictly less
than that on `K_N` for every `r > r*` (indeed `r*=2N^2` is allowed).  These are
exactly the hypotheses used at manuscript p. 14 / `sections/05_strong_selection.tex`
lines 128–132.  Arbitrary finite raw weights cause no mismatch with the
source's `[0,1]` convention because a common positive scaling puts them in that
range without changing any competition.

The cited proof was also rechecked from its 12-page supplement, Section 4.1,
pp. 5–7.  From a singleton at `u`, extinction before the first gain has
probability at least `1/(1+N p_+(u))`.  Two Jensen steps give

`rho_dB(G,r) <= d r/(d r+d+r-1)`,

where `d` is average positive support degree.  A noncomplete directed support
has `d <= N-1-1/N`; comparison with the exact complete baseline yields strict
suppression for all sufficiently large `r`, and the source's displayed
quadratic check proves the advertised `2N^2` threshold.  (The supplement has
an internal theorem-numbering typo in its results list, calling transience
Theorem 2, while its proof and the published main paper call it Theorem 1.  The
manuscript's citation to the published theorem is nevertheless unambiguous.)

### Reducible closure and undirected limit: verified

For the support orientation used here, a source SCC has no incoming parent
edge from another SCC.  With at least two source SCCs, a singleton leaves one
of them all-resident forever.  With a unique source SCC `C != V`, a singleton
outside `C` cannot enter it.  From `i in C`, before the first gain the competing
state-changing hazards are death of `i`, of rate `1/n`, and gains at its
`s_i^+` positive out-neighbors, of rates `p_iv(r)/n` with `p_iv(r)<=1`.
Consequently

`Pr(first gain before extinction)
 = sum_v p_iv(r)/(1+sum_v p_iv(r)) <= s_i^+/(s_i^++1)`.

Uniform initialization and `|C|<=n-1`, `s_i^+<=n-1`, give (5.17),
`rho <= (n-1)^2/n^2`, strictly below the limiting complete value
`(n-1)/n`.  No ancestry direction is reversed and no absorption assumption is
silently used.

For a connected undirected support, a singleton at `i` has, at `r=infinity`,
one extinction hazard and one certain-gain hazard for each of its `s_i`
neighbors.  Thus it reaches an adjacent pair first with probability
`s_i/(s_i+1)`.  From an adjacent pair the mutant set stays connected, losses
are impossible in the limiting chain, and a boundary vertex is eventually
added almost surely until fixation.  The finite embedded chain has finite
fundamental matrix and finite-`r` leakage is `O(1/r)`.  This proves (2.11).
The termwise subtraction in (2.12) is correct:

`(n-1)/n^2 - s_i/[n(s_i+1)]
 = (n-1-s_i)/[n^2(s_i+1)]`.

Locations: manuscript Proposition 4, PDF p. 6; proof pp. 14–15;
`sections/05_strong_selection.tex` lines 128–163.

### Weighted triangle: exact independent reconstruction passed

I reconstructed the literal six transient states independently.  From
singleton `i`, target `j` gives the pair with probability
`u_ij=r w_ij/(r w_ij+w_jk)`; from unique-resident state `G_i`, loss of mutant
target `j` has probability `v_ij=w_ij/(r w_jk+w_ij)`.  This gives exactly
(6.2)–(6.3).  The coefficient matrix is `D(I-Q)` with positive diagonal `D`
and substochastic `Q` of row sums strictly below one; hence it is a nonsingular
M-matrix and its determinant is positive.

An independent SymPy 1.14 derivation solved these equations, separately built
the full subset chain, and verified exactly

`rho(W,r)-rho(J_3,r) = -r(r-1) H_r/[3(r+1) P_r]`,

with `P_r=L det(M)/3`, as well as every identity in (6.7)–(6.8).  The
independent full-chain route agreed at three nonsymmetric exact-rational test
points.  Positivity is decisive: `A,D,E>=0`; if weights are nonuniform then
`U>0`, so `E=4s_2(3s_2 U+V)>0` and `H_r>0` for `r>1`.  Conversely equality
forces `U=0`, hence `a=b=c`.  The denominator is positive for all positive
weights and `r>0`.

Locations: Theorem 5, PDF p. 6; proof PDF p. 15;
`sections/06_low_order.tex` lines 7–68.  Independent artifact:
`work/independent_scratch/triangle_rederive.py`; logged run
`independent_triangle_rederive_v2`, exit 0.

### Both symmetric weighted-K4 families: exact independent reconstruction passed

For a two-class graph I regenerated every transition directly.  A resident
target in the size-`p` class sees mutant weight `i alpha+j gamma` and resident
weight `(p-i-1)alpha+(q-j)gamma`; analogous counting yields all four lines of
(B.1).  Thus mutant counts `(i,j)` are a strong lumping.  I then built the
`1+3` and `2+2` systems without importing delivered code and separately
cross-checked them against literal 14-transient-state chains at exact-rational
nonsymmetric points.

For `G_13`, exact elimination reproduced (B.2) and every displayed term of
`F_13` and `P_13`.  Both polynomials are positive on `x>0,r>0`; for `r>1` the
only equality is `x=1`.

For `G_22`, the raw holding-deleted 7-state matrix regenerated

`P_22=128 L_22 det(M_22)`

as a polynomial with exactly 123 monomials, all positive integers.  This
identifies the matrix convention and verifies (B.4), not merely denominator
sign.  Solving the lumped chain regenerated (B.3), a symmetric polynomial
`H_22`, and after changing variables
`g=sqrt(xy)`, `d=(sqrt(x)-sqrt(y))^2`, `t=r-1`, reproduced every coefficient
`C_0,...,C_4` in (B.5) exactly.  For `g,t>0`, the only apparently negative
coefficient is inside

`g^4+4g^3-2g^2+4g+1=(g^2-1)^2+4g(g^2+1)>0`.

Hence `C_j>0` for `j>=1`, while `C_0>=0`; if `d>0`, `H_22>0`, and if `d=0`
then `H_22=C_0=0` exactly when `g=1`, i.e. `x=y=1`.  The parameterization is
complete: every `x,y>0` gives `g>0,d>=0`, and conversely every such `(g,d)`
comes from positive square roots with product `g` and squared difference `d`.

Locations: Appendix B, PDF pp. 27–28;
`appendices/B_k4_certificate.tex` lines 1–154.  Independent artifact:
`work/independent_scratch/k4_rederive.py`; logged run
`independent_k4_rederive`, exit 0.

### Exact open gap at this checkpoint

The remaining work is an adversarial consolidation of monotonicity and all
endpoints (`n=2`, absent `n=3` symmetric sector, zero-support limits, `r=1`),
plus a final counterexample search and severity assessment.

## 2026-08-22T19:49:02Z — final checkpoint (completion estimate: 100%)

### Monotonicity and boundary audit

**Fitness monotonicity.**  The manuscript's Lemma 12 (PDF p. 16;
`sections/07_implications_reproducibility.tex` lines 8–29) is correct.  For
`f_r(x)=rx/[1+(r-1)x]`,

`partial_r f_r=x(1-x)/[1+(r-1)x]^2 >= 0`,
`partial_x f_r=r/[1+(r-1)x]^2 > 0`.

Using the same dead target and uniform threshold preserves set inclusion when
both fitness and the current mutant set are increased.  Reaching the full set
in the lower chain therefore forces simultaneous fixation in the upper chain.
This proves nondecreasing, not generally strictly increasing, fixation.  The
lack of strictness is real: `n=2` and directed cycles with one incoming parent
per target are fitness-independent.

**`n=2`.**  There is only one loopless row-stochastic kernel.  With one mutant,
the next state-changing death is the mutant or resident with equal probability,
so every admissible positive raw weighting has fixation `1/2` for every
`r>0`.  Formula (2.4) reduces to `1/2`, and the manuscript correctly excludes
`n=2` from the singular `1/(n-2)` expansion while stating the exact tie in
Theorem 1.  A zero support entry is incompatible with positive incoming degree
at this order.

**Absent symmetric sector at `n=3`.**  Its dimension in (4.10) is
`n(n-3)/2=0`; directly, symmetric off-diagonal variables `(a,b,c)` with row
sums `a+b=a+c=b+c=0` all vanish.  Thus Theorem 6 correctly starts symmetric
positivity at `n=4`, the `n=3` table entry is `---`, and the local proof at
`n=3` needs only the standard and antisymmetric sectors.  There is no endpoint
gap.  Locations: PDF pp. 11–12; `sections/04_local_hessian.tex` lines 62–111
and 134–148.

**Zero support.**  The complete-support expansion deliberately requires every
off-diagonal weight positive; its ratio defect is undefined at a zero and the
fixed-`W` expansion is not uniform as a positive weight tends to zero.  This is
not a coverage gap: a strongly connected support with any missing edge is in
the cited theorem, and a reducible support is in (5.17).  Connected undirected
graphs with missing edges are explicitly allowed by Proposition 4.  If a zero
creates a target of incoming degree zero, it leaves the paper's model.

As stronger, unstated checks, the low-order certificates extend without a new
equality to their connected zero-support faces.  With exactly one zero edge,
the triangle has `s_3=0`, `V=s_2^2>0`, so its numerator is strict and its
M-matrix denominator stays positive.  In (B.2), setting `x=0` leaves positive
`F_13,P_13`; this is the star.  In (B.3) the unit cross edges keep the graph
connected for all `x,y>=0`, `L_22>0`, and the `(g,d,t)` certificate is strict
when one or both internal weights vanish.  Exact subset-chain checks at a
weighted path, `G_13(0)`, `G_22(0,3)`, and `G_22(0,0)` all passed.

**`r=1`.**  On each strongly connected structure, the neutral process's
eventual ancestor has some probability distribution over vertices; averaging
a uniformly placed singleton over that distribution gives fixation `1/n`.
The complete formula explicitly takes this continuous value.  Equations
(6.5), (B.2), and (B.3) all have a factor `r-1`, so every weighting ties at
neutrality; their strict equality classifications are correctly restricted to
`r>1`.  Monotonicity itself is stated on `r>0` and covers `r=1`.

### Counterexample search

No counterexample was found.  Besides the general derivations, literal exact
subset chains gave the following independent adversarial checks:

- nonsymmetric complete directed examples at `n=3` and `n=4` reproduced the
  coefficient `E_dir/[n^2(n-2)]` exactly (values `17657/20790` and
  `123367/192192`);
- a strongly connected directed 3-cycle gave fitness-independent fixation
  `1/3`, strictly below the complete baseline for `r>1`, as the cited theorem
  predicts;
- nonsymmetric triangle and both K4 families agreed between orbit-reduced and
  literal subset chains at exact-rational parameter points;
- the connected zero-support and neutral endpoints listed above agreed with
  their claimed or limiting behavior.

Independent artifacts and every executed command, version, output summary,
exit status, and SHA-256 are recorded in
`records/strong_selection_low_order_commands.log`.  No delivered code was run.

### Validation table and severity assessment

| Claim | Location | Independent status |
|---|---|---|
| Complete-support `1/r` expansion and coefficient | Theorem 2, PDF p. 6; (5.4)–(5.16), pp. 13–14 | **Verified** by general first-step derivation and exact `n=3,4` chains |
| Raw/normalized identity, scale invariance, equality class | (2.9)–(2.10), p. 6; (5.15)–(5.16), p. 14 | **Verified** exactly |
| Strongly connected noncomplete-support obstruction | Tkadlec et al. main Theorem 1, p. 7; manuscript p. 14 | **Verified against source and source proof** |
| Reducible source-component closure | (5.17), PDF pp. 14–15 | **Verified** |
| Undirected support limit and deficit | Proposition 4, p. 6; proof p. 15 | **Verified** |
| Weighted-triangle global inequality and equality | Theorem 5, p. 6; (6.1)–(6.8), p. 15 | **Verified** by independent symbolic elimination, SOS, and literal chain |
| `G_13` lumping/certificate/domain/equality | (B.1)–(B.2), PDF p. 27 | **Verified** |
| `G_22` lumping/determinant/123-term certificate/domain/equality | (B.1), (B.3)–(B.6), PDF pp. 27–28 | **Verified** |
| Fitness monotonicity | Lemma 12, PDF p. 16 | **Verified** by order-preserving coupling |
| `n=2`, `n=3` missing sector, zero support, `r=1` | pp. 6, 11–16, 27–28 | **Verified; no endpoint gap** |

I found **no mathematical defect, omitted domain case, incorrect equality
class, or citation-hypothesis mismatch** in the assigned strong-selection and
low-order slice.  The cited supplement's theorem-numbering inconsistency is in
the external source and does not make the manuscript citation ambiguous.  No
correction is required on the basis of this slice.

### Strongest verified result and exact remaining gaps

The strongest verified result is the full assigned chain of claims: every
fixed positive complete-support structure has the stated sharp sum-of-squares
strong-selection deficit; all other supports are eventually strictly
suppressing unless dynamically equal to `J_n`; and the positive weighted
triangle plus both stated symmetric weighted-K4 slices satisfy global strict
complete-graph maximality for all `r>1`, with precisely the stated equality
classes.

There is **no remaining mathematical gap within this sub-audit's scope**.
Package-integrity, fitness-two dual/Hessian claims beyond the `n=3` endpoint,
delivered-code inspection, and full replay are intentionally assigned to the
other referee workstreams and are not certified here.
