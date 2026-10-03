# Independent adversarial audit: Martingale for practical purposes

## Verdict

**PASS for the stated finite-horizon partial results and the disposition “unsolved, 5/5 attempts.” No mathematical correction is required.** This is an independent AI-assisted review of a frozen author packet, not human peer review, a formal proof verification, or a claim that the broad research problem is solved.

Problem: **9700001 / AMR-096-0001**, David Aldous, *Martingale, for practical purposes*.

Audit date: **2026-10-03 UTC**.

The author manifest SHA-256 is:

`b6d9927303b07c183e311b6b1f8a944d16147671b0c6b5f09b686acb9fc5cd62`

All **12 manifested files** match that manifest. The author packet was not modified. Its deterministic receipt reproduces byte-for-byte: **109,255 exact-rational assertions**. An independently written checker adds **35,318 exact-rational finite controls**, all passing. These counts describe controls, not independent proofs or a probability of correctness.

## 1. Exact source and scope

I read the complete [Aldous primary problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/fields.html), the complete [maintained problem index](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html), and section 3 of the author's [related conceptual discussion](https://www.stat.berkeley.edu/~aldous/Real_World/words_paradox.html).

The primary page presents a definitional program concerning practically discoverable stopping advantages. Its separate discrete-time question asks whether polynomially many stopping equalities can define a useful tractable class. It does not require such a class to equal the exact martingales. The source leaves the access model, encoding, tolerances, and computational resources unspecified. Accordingly, a fixed-library obstruction to exact characterization cannot settle the main question.

The index explicitly places this topic at 0.5 on its conceptual-to-technical scale and warns that updates may omit relevant work. Those facts support a cautious scope reading; they are not evidence that no later solution exists. The packet correctly makes neither a historical novelty claim nor an exhaustive literature-status claim.

The continuous-time motivation is not imported as an unrestricted optional-stopping theorem. Every proof under review is finite-horizon, with integrability or boundedness stated where needed. The five numbered attempts are five substantive approaches in one investigation, not five independent replications.

## 2. Claim-by-claim mathematical review

### Attempt 1: finite observation filtrations

**Accepted.** The stopping map that continues one step on an atom of the time-t observation sigma-field and otherwise stops at t is adapted. Its expectation differs from the initial mean by the deterministic-time deviation plus the atom's increment moment. The included deterministic tests therefore remove the baseline term exactly.

The optional-projection step is valid even when the price process is not adapted to the smaller observation filtration. Nesting of the observation sigma-fields gives

`E[E[X_(t+1) | G_(t+1)] | G_t] = E[X_(t+1) | G_t]`.

Thus zero atom moments are equivalent to the projected process being a martingale. Null atoms impose no restriction and do not invalidate any expectation identity. Separately conditioning on the stopping events proves equality of the price and projected-price stopping expectations.

The telescoping identity holds pathwise at a finite horizon. Each survival event is measurable at its corresponding time, so atomwise cancellation establishes fairness for every permitted stopping time. The stated absolute drift bound and its sharper positive/negative-part version follow without assuming that arbitrary collections of atoms can form one stopping rule. The factor-one-half local witness bound is correct even when the two candidate expectation deviations have opposite signs.

The coarse-filtration counterexample has the stated gain of 1/2 under natural price information. This is a genuine limitation of the positive result, not a failure of it.

The polynomial-time statement is relative to explicit rational tables or supplied exact moments. It is not a polynomial-in-horizon algorithm for an exponentially large input table. The rational-polytope sentence is read under the paragraph's explicit rational-path-value hypothesis; arbitrary irrational fixed prices would only imply a polytope, not necessarily a rational one.

### Attempt 2: feature approximation

**Accepted.** Splitting each survival indicator into an approximant and residual, then applying the triangle inequality, gives exactly the displayed coefficient-weighted moment error plus increment-weighted approximation error. Deterministic coefficient signs and signed features cause no hidden sign reversal. Stated integrability is sufficient because there are finitely many terms.

The bounded-increment specialization follows directly from the pointwise bound on the increment magnitude. Uncontrolled coefficient norms could amplify small moment errors, and the packet explicitly retains their cost.

Indicator features correspond to differences of actual stopping expectations. General signed features do not automatically correspond to one stopping time, and the packet does not treat them as such.

The four equiprobable price histories give zero adjacent current-state drift while preserving a full-history stopping gain of 1/4. In the two histories that meet at price zero, the previous price distinguishes the sign of the last increment. The proposed stopping event is therefore available in the natural filtration but absent from the current-state sigma-field. All signs and expectations are correct.

### Attempt 3: fixed-library obstruction

**Accepted, with precisely the packet's fixed-map scope.** There are `D = 2^n - 1` nonterminal nodes. For each node, its predictable jump process has conditional one-step drift one at that node and zero at every other node. Consequently the node-drift functionals are independent and the martingale space has codimension D.

A fixed stopping equality is one linear functional on the adapted-process space. Its value on a node-jump process is the node probability multiplied by the stopping map's survival indicator at that node. Survival is constant on the node's atom. Fewer than D equations therefore leave a nonzero drift direction.

The sparse construction uses only m+1 selected nodes. A rational null vector exists even with repeated tests, dependent rows, or zero rows. The minor argument provides polynomial bit size: rank-r minors of a zero-one matrix have magnitude at most r!, so the integer kernel entries have O(r log r) bits. Multiplication by inverse node probabilities adds at most n bits. After normalization, the denominator is a sum of at most m+1 such integers, adding only logarithmically many further bits. Polynomial-time exact elimination is available; computing minors need not use factorial-time determinant expansion.

Normalization makes the predictable perturbation uniformly bounded by one. Adding it with the stated small scale to the encoded fair-bit martingale preserves every fixed test, yet leaves a nonzero conditional drift. The price at time t is within one eighth of an integer after the specified rescaling, so exact nearest-integer rounding uniquely recovers the entire revealed prefix. Thus the natural price filtration really equals the original bit filtration; the construction does not exploit inaccessible extra information.

The process starts at zero, is rational and adapted, and is uniformly bounded, so integrability and bounded stopping are automatic. Its sparse description and exact evaluation have polynomial size and cost in n and m. Retrieving a survival decision may require replaying the stopping algorithm along the prefix; this is still polynomial when the supplied algorithms are efficiently executable. There is no promise of efficient access to arbitrary opaque stopping maps.

For a node with nonzero drift, either the deterministic-time mean already differs from zero or the corresponding one-step cylinder rule does. The rule is executable from prices through the same exact decoder. Its advantage may be exponentially small, and no robustness to measurement noise is proved.

Most importantly, fixed sample-space maps are not the same thing as fixed programs that receive prices or inspect the process law. Changing the process can change the stopping map implemented by a fixed program. The packet expressly excludes this stronger interpretation, adaptive queries, general computational hardness, and approximate characterization. None can be inferred from this theorem.

### Attempt 4: explicit fully observed Markov model

**Accepted.** The essential identity is conditional on the entire observed state history, using the actual Markov hypothesis. It cannot be inferred merely from adjacent price-state mean tests. Multiplication by the state probability correctly removes restrictions at unreachable states.

The stopping tests are legitimate full-history stopping rules even though the sigma-fields generated by the current state alone need not be nested. The full-history deviation bound follows by conditioning each survival-weighted increment on the full history and bounding its predictable drift.

Both backward recursions are valid. Conditional induction bounds arbitrary history-dependent policies, and the constructed Markov stop regions attain the bounds. A random initial state is observed at time zero, so the expectation of the initial-state value function is the correct optimum. Stopping at zero places the initial expectation between the extrema. Independent external randomization cannot improve a linear expectation over mixtures of deterministic policies.

Polynomial complexity is in the explicit time-indexed transition/reward table's total bit length. A common denominator can be taken as the product of the denominators in that table: each time-indexed transition is used at most once along a path. The exponentially many possible paths do not force exponentially many denominator bits. Value magnitudes are bounded by the largest reward magnitude, also controlling numerator size. The number of arithmetic operations is polynomial in the explicit state-transition description.

The algorithm presupposes an observed state. If the state is hidden, an optimal full-state stopping policy need not be executable from prices alone. This limitation is explicitly retained.

The method is classical backward induction/Snell-envelope optimal stopping, credited as such. The packet supplies the finite proof, so correctness does not depend on importing an unread external theorem.

### Attempt 5: statistical access

**Accepted.** The sample paths must be independent copies from the same process law, as used explicitly by the proof. Dependence among rules evaluated on the same path is harmless because the argument first controls each rule across independent paths, then takes a union bound. The library is fixed independently of the evaluation sample.

The increment in stopped reward lies in `[-2B, 2B]`, so its range width is 4B. The supplied exponential-moment proof gives two-sided tail probability `2 exp(-K r^2 / (8 B^2))`; substituting the displayed radius and union-bounding over m rules gives the claimed confidence. The tilted-variance bound, including its integration for negative tilts, is valid for bounded random variables.

All strict and non-strict threshold signs are correct. The acceptance branch can be empty when the requested tolerance is below the radius; the packet says so. A true advantage exceeding tolerance plus twice the radius guarantees detection on the simultaneous event. These conclusions apply only to the specified library, not every computationally efficient stopping rule.

For the rare-event pair, the null sample law is concentrated at the all-zero sample. Its total variation distance from the alternative is exactly the alternative's probability of seeing at least one success, bounded above by K times the rare-event probability. A test with both success probabilities at least two thirds must separate the laws by at least one third. Randomization and a bounded adaptive sample budget do not defeat the argument, because one can average over random seeds and pad the sample sequence.

This rules out a uniform bounded-sample exact-zero decision over arbitrarily small nonzero deviations. It does not make the one-step stopping map hard to write down, and the packet correctly distinguishes those tasks. The standard concentration argument retains Hoeffding's credit.

## 3. Independent computational controls

The author verifier was inspected before execution. Its manifest checker passed, and its regenerated JSON matched the supplied receipt byte-for-byte.

The separate `independent_checks.py` does not import or call the author's mathematical checking functions. It uses the Python standard library and exact `fractions.Fraction` arithmetic, with a recorded deterministic seed. Its additional coverage includes:

- Four nested observation structures: full, delayed, trivial, and an intermediate coarsening; random nonuniform laws with zero-probability outcomes; nonzero initial prices; and deliberately generated martingales.
- Four-way certificate equivalence, optional projection at every enumerated stopping time, the sharper drift bound, local witnesses, and signed rational feature approximants.
- Independently selected nodes on one- through six-bit trees, repeated or degenerate stopping tests, rank-zero nullspaces, actual natural-price injectivity, exact prefix decoding, all node drifts, and explicit missed witnesses.
- An exact identity-matrix test for the node-drift basis, and full stopping-constraint matrix rank D for horizons one through four.
- Exhaustive history-policy enumeration for small Markov chains with random initial states, rational transitions, null/unreachable states, constructed extrema policies, and positive and negative reward values.
- Direct enumeration of Bernoulli sample laws, randomized test functions, exact total variation, and 5,000 rational checks of the statistical decision thresholds.

Final receipts:

| Suite | Assertions | Result |
|---|---:|---|
| Frozen author controls | 109,255 | PASS; byte-identical replay |
| Independent audit controls | 35,318 | PASS |

The independent audit does not claim to computationally prove the analytic universal statements, the Hoeffding exponential-moment inequality, asymptotic bit-complexity bounds, or the absence of later literature. Those were assessed through the proof and scope review above.

## 4. Reproduction and integrity

With the audit directory and frozen `public` packet as siblings, use Python 3.9 or newer:

```text
python verify_audit.py ../public
```

The wrapper verifies this audit's manifested files, the exact author-manifest identity and all its files, the byte-identical author receipt, and the independent receipt. It reads the frozen packet and writes no files there. Paths are configurable through the packet argument.

The audit manifest covers the report, structured verdict, verifier scripts, and receipts. The manifest itself is excluded from its own file list in the usual way.

## 5. Publication recommendation

Retain **unsolved, 5/5 attempts**, all explicit observation/access assumptions, the fixed-map versus process-dependent distinction, finite-input bit complexity, the potentially tiny advantage, and classical attribution. The packet supports its advertised special-case results and limitations. It does not provide a canonical general MPP definition, certify practical discovery for arbitrary succinct laws, or resolve the original conceptual program.

No required revision, unresolved mathematical blocker, or remote change resulted from this audit.
