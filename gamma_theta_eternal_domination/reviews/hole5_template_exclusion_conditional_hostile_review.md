# Hostile coverage review: conditional order-12 `hole5` exclusion layer

## Verdict

**`ACCEPT_CONDITIONAL_REALIZATION_ONLY`.**

The theorem in
`math/lemmas/hole5_template_exclusion_conditional.md` correctly proves:

\[
\begin{gathered}
\text{connected order-12 counterexample with }
\gamma=\gamma^\infty=3\\
\text{and a hub-free induced }C_5\text{ in }\overline G
\end{gathered}
\quad\Longrightarrow\quad
F_5,\ F_5\land S,\ \text{and }F_5\land S\land T
\text{ are satisfiable}.
\]

The separate premise that an accepted certificate refutes either exact
strengthened formula remains unfilled. Therefore this review makes **no**
`hole5` exclusion, no finite-slice claim, and no SAT/UNSAT claim. No solver
or proof checker was run for this review.

The reviewed theorem-note SHA-256 is
`dee226088d17c2564da406f4e675a71f2d160cc678805e360e2ef51398b7e26b`.

## Frozen dependencies checked

The audit read and hash-checked the mathematical and executable layers
separately:

| Dependency | SHA-256 |
|---|---|
| `math/reductions.md` | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| `math/lemmas/complement_k3_dictionary.md` | `54d7cafdc7047d75ed58739f6a773344a2f780aaecd0eafde8ed01a0692c6256` |
| `math/lemmas/maximum_independent_states.md` | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| `math/lemmas/k3_structural_day1.md` | `00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e` |
| `math/synthesis_k3_cegar_design.md` | `57d82b9dabdc9c8f66950a3f9c483f3cb58e35a11e243a8880c173b5724a09b8` |
| `src/synthesis_k3/encoding.py` | `fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6` |
| `math/lemmas/template_coloring_bank.md` | `abc9568d70eee6b792e4220b58c12f5e7c069a13e37dbd3265025abe02cd6f50` |
| `src/synthesis_k3/template_color_bank.py` | `dc69687f01e85bea643b73f713b1afca51b3911b3fee4a857da3fb07cc979838` |
| `math/lemmas/hole5_signature_symmetry.md` | `8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8` |
| accepted \(S_6\) implementation-binding log | `615c46de94578b7e5d4f62a509b03993065e0976ccc316db53a34c3c86f13a73` |
| accepted rim-reflection coverage log | `a5808f2f8485fe462b308e7f1fa9c023fb6d8ab3d5c7aad871fa6516f4569dbc` |

The exact retained inputs are:

| Artifact | SHA-256 |
|---|---|
| complete-bank `hole5` CNF | `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7` |
| 3,645-row coloring bank | `b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00` |
| complete-bank manifest | `99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402` |

## 1. Hypothesis normalization

The theorem assumes
\[
\gamma(G)=\gamma^\infty(G)=3<\theta(G).
\]
The one-guard parameter chain puts every intervening parameter at three, in
particular \(\alpha(G)=3\). For \(H=\overline G\), independent sets of \(G\)
are cliques of \(H\), while clique partitions of \(G\) are proper colorings
of \(H\). Thus
\[
\omega(H)=3<\chi(H).
\]
The directions are correct: the formula's positive \(e_{uv}\) means an edge
of \(H\), not of \(G\).

No dominating pair exists in \(G\). A pair fails to dominate precisely when
some outside vertex is adjacent in \(H\) to both endpoints. Therefore every
pair of \(H\) has a common neighbor. This implication does not assume
well-coveredness and does not replace eternal closure by a static condition.

Connectedness is a stated hypothesis of this conditional theorem. The
encoded cut clauses contain negative \(H\)-edge literals, so they require a
crossing edge of \(G\), which is the correct complement direction.

## 2. Template relabeling

Choose the assumed hub-free induced \(C_5\), orient it, and label its rim
\(0,1,2,3,4\). Adjacent rim vertices \(0,1\) have no common neighbor on an
induced cycle of length five. The pair-common-neighbor property therefore
supplies an external vertex, which can be labeled \(5\), adjacent in \(H\)
to both \(0\) and \(1\).

Hub-freeness applies to every outside vertex, including the chosen vertex
5. Hence each of vertices \(5,\ldots,11\) satisfies the exact five-literal
no-hub clause. The remaining six labels are arbitrary. This establishes all
and only the template requirements:

- five positive rim-edge units;
- five negative rim-chord units;
- seven no-external-hub clauses; and
- the two positive units \(e_{05},e_{15}\).

No automorphism of the input graph is presumed. The operation is ordinary
relabeling after selecting a witnessed induced subgraph. The broader SPGT
split is used only to locate the \(C_5\) branch in the campaign: this theorem
does not claim that all parameter-three counterexamples contain a \(C_5\).

## 3. Exact base-formula realization

The independent clause accounting is:

| Clause family | Count | Why the target assignment satisfies it |
|---|---:|---|
| no \(K_4\) | 495 | \(\omega(H)=3\) |
| witness existence | 66 | choose one common neighbor per pair |
| witness implications | 1,320 | the chosen witness has both required \(H\)-edges |
| `hole5` template | 19 | the relabeling above |
| connected cuts | 2,047 | each proper cut has a crossing \(G\)-edge, hence an \(H\)-nonedge |
| selected-state domination | 1,980 | every family state dominates \(G\) |
| family nonempty | 1 | an eternal family is nonempty by definition |
| move implications | 11,880 | a chosen guard uses a \(G\)-edge and reaches a selected successor |
| attack-response clauses | 1,980 | choose one response for every selected state and unoccupied attack |
| triangle-to-family strengthening | 220 | every \(H\)-triangle is a maximum independent triple of \(G\) |
| **total** | **20,008** | |

The corresponding literal count is 114,601. The variable allocation is
66 edge, 660 common-neighbor witness, 220 family, and 5,940 move variables,
for 6,886 total.

The note's proposed assignment is complete, not merely an edge assignment:

1. set edge variables from \(H\);
2. select one real common neighbor for each pair and set only that witness
   variable true;
3. set \(f_D\) exactly for the members of a chosen eternal three-family;
4. for every selected \(D\) and every \(r\notin D\), select one responding
   guard supplied by eternal closure and set only that response variable
   true; and
5. set every other move variable false.

This assignment satisfies implications from false auxiliary variables
vacuously and verifies every implication from a true auxiliary variable by
an actual graph or family witness.

### One-guard model audit

The attack quantifier is exactly \(r\notin D\), so no occupied-vertex attack
is introduced. A true \(m_{D,r,u}\) names one old guard \(u\), and the
successor is exactly \((D-\{u\})\cup\{r\}\). Its legal-edge clause is
\(\neg m_{D,r,u}\vee\neg e_{ur}\). Since \(e\) describes \(H\), the negative
literal means \(ur\notin E(H)\), equivalently \(ur\in E(G)\). No other guard
moves.

The nonempty-family clause prevents the all-false \(f\) assignment. Every
selected configuration has its own domination clauses, and every selected
successor is therefore also dominating. There is no hidden
\(\gamma_m^\infty\), \(\gamma_{\rm all}^\infty\), occupied-attack, stationary,
or nondominating-successor convention.

### Triangle strengthening audit

An \(H\)-triangle is an independent three-set of \(G\), and
\(\alpha(G)=3\). In any eternal three-family, attack the unoccupied vertices
of that independent set successively. A guard already on another vertex of
the set cannot respond along a \(G\)-edge, so each response increases the
number of guards on the set. The final configuration is that triangle.
Thus every \(H\)-triangle really has \(f_D=1\), and the redundant
triangle-to-family clauses do not overconstrain a target.

## 4. Complete coloring-bank audit

Only positive forced \(H\)-edges constrain a proper coloring. They contain
the triangle \(0,1,5\), so every compatible coloring uses all three colors.
The number of labeled compatible rows is
\[
(2^5-2)3^6=21,870.
\]
The free action of the six color-name permutations leaves exactly 3,645
first-use representatives.

For each representative \(c\), the formula appends the positive clause
\[
\bigvee_{c_u=c_v} e_{uv}.
\]
It is false exactly when \(c\) is a proper coloring of \(H\). Conversely,
canonicalizing the color names of any proper three-coloring produces a bank
row with the same color blocks. Thus, relative to the template units, the
bank conjunction is equivalent to \(\chi(H)>3\).

The target has \(\chi(H)=\theta(G)>3\), so it satisfies every bank clause.
There is no sign reversal: a same-color pair must be a nonedge for a proper
coloring of \(H\); the positive disjunction says that at least one such pair
is instead an \(H\)-edge.

The retained suffix contains exactly the independently reconstructed 3,645
clauses, with 74,358 literals. Base plus bank therefore gives the exact
23,653-clause, 188,959-literal \(F_5\).

## 5. Symmetry-coverage audit

The accepted \(S_6\) audit maps all 6,886 variables, not only the 66 graph
variables. It proves that permutations of vertices \(6,\ldots,11\) preserve
the full complete-bank clause multiset. Its exact 315-clause comparator
stream has SHA-256
`ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`,
and exhaustive truth tables show it accepts exactly nondecreasing adjacent
six-bit signatures. Therefore every \(F_5\) model has an orbit representative
satisfying \(S\).

The accepted residual reflection audit reconstructs the full semantic action
of
\[
\rho=(0\ 1)(2\ 4)
\]
and verifies exact base, bank, and full covariance. It swaps variables
\(e_{25}=24\) and \(e_{45}=39\). If \(T=(-24,39)\) fails, reflection makes it
true. Subsequent outer sorting fixes vertices \(0,\ldots,5\), hence preserves
both variables and \(T\). This proves coverage of \(F_5\land S\land T\).

Neither \(S\) nor \(T\) is asserted to be a logical consequence of \(F_5\).
Their use is the correct equisatisfiable orbit-representative argument.

The exact strengthened formula bindings checked here are:

| Formula | Variables | Clauses | Literals | Bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| \(F_5\land S\) | 6,886 | 23,968 | 192,169 | 754,323 | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |
| \(F_5\land S\land T\) | 6,886 | 23,969 | 192,171 | 754,332 | `441e54c28fdf6005f0f17fb951bf37c7ff46e222f3e605b7e715fabeec8f64d4` |

## 6. Conditional-logic and publication boundary

The established implication is
\[
\boxed{\text{counterexample satisfying the \(C_5\) premise}
\ \Longrightarrow\ F_5\land S\land T\text{ is SAT}.}
\]

To infer exclusion, a separate accepted fact would be required:
\[
\boxed{F_5\land S\land T\text{ is UNSAT by an independently checked
certificate}.}
\]

The second box is not supplied by the theorem note or by this review. A
timeout, solver output, unchecked DRAT file, partial cube set, or proof for
different bytes cannot fill it. A future accepted certificate must bind the
exact formula, proof, checker and version, successful checker transcript,
and any case-coverage manifest.

Subject to that explicit missing premise, no mathematical gap was found in
the complement dictionary, template relabeling, exact base realization,
one-guard family encoding, complete coloring-bank equivalence, or
\(S_6\)/reflection coverage.
