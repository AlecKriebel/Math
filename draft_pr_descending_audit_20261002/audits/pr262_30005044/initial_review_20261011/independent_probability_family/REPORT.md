# PR262 / problem30005044: independent probability-family audit

**Disposition:** the two specified mathematical claims are validated for the stated minimal finite-path graphical process. No substantive defect was found in the submitted probability proof. This report does **not** clear source interpretation, novelty, or priority.

**Audit completed:** 2026-10-12 UTC. **Family:** independent probability construction, adaptive exploration, simultaneous infection, and quenched quantifiers.

## 1. Audited claim, assumptions, and evidence boundary

Let a rooted Galton–Watson tree have iid offspring counts with

\[
\mathbb P(\xi\ge m)=m^{-1/4},\qquad m=1,2,\ldots.
\]

Only the root is infected at time zero. Each ordered edge carries an independent rate-\(\lambda\) Poisson arrow process, and each vertex an independent rate-one recovery process. All these clocks are independent of the tree. Fitness is \(F\equiv1\). A vertex is infected at time \(t\) precisely when a **finite** time-ordered graphical infection path reaches it from the initial root without crossing a recovery mark. This is also the increasing union of the processes in finite balls, coupled using the same clocks.

The exact claims are:

1. For every \(\lambda>0\), with \(\tau=1/(2\lambda)\),
   \[
   \mathbb P(|X_\tau|=\infty)\ge\frac7{30}e^{-3/(2\lambda)}.
   \]
2. There is a single probability-one set of trees such that, for every tree in that set and **every** \(\lambda>0\), the quenched probability of an infinite infected set at some finite time is positive.

The probability in claim 1 averages over both tree and clocks. Claim 2 need not have a uniform probability or time. The hypotheses do not ask whether all infinite-mean offspring laws explode, whether every deterministic tree explodes, or whether explosion has quenched probability one.

The offspring law is a genuine probability law: the masses \(m^{-1/4}-(m+1)^{-1/4}\) are nonnegative and telescope to one. Since its tail tends to zero, the count is finite almost surely. Since its tail at one is one, there are no leaves. Every generation and every finite-radius ball is finite almost surely, by induction and countability. Its mean is infinite because \(\sum_{m\ge1}m^{-1/4}\) diverges.

This audit read the entire submitted `PROOF.md`, but only **after** completing and hashing `INDEPENDENT_DERIVATION.md`. The submission's SHA256 is `8f2010e4aa303e260546faf72c507d53c30b43025be7ad2e99019631eac7b2bd`. The frozen pre-comparison independent derivation's SHA256 is `549a991ed3fe6af3902c5cf2b3e16464bcda85f9e14a8d5dd399dada3b427f3b`. `INPUT_MANIFEST.json` gives the exact input path and evidence limits. No other reviewer's output or cited external source body was read. No external communication, publication, Git operation, or provider mutation was performed.

## 2. Independent construction before reading the submission

The independent mechanism uses the thresholds

\[
k_n=256^{2^n},\quad s_n=\tau(1-2^{-n}),\quad
I_n=(s_{n-1},s_n],\quad n\ge1.
\]

First require at least \(256\) children at the root; this costs probability \(1/4\). At stage \(n\), inspect only the first \(k_{n-1}\) children of the previously selected vertex. A child passes if it has at least \(k_n\) children and receives a downward arrow in \(I_n\). Select the first passing child. This is done without inspecting recoveries.

The conditional pass probability of one fresh child is

\[
p_n=k_n^{-1/4}\left(1-e^{-2^{-(n+1)}}\right).
\]

For \(0\le x\le1/4\), \(1-e^{-x}\ge x-x^2/2\ge(3/4)x\). Therefore

\[
k_{n-1}p_n\ge a_n:=\frac34 2^{4\cdot2^{n-1}-n-1}.
\]

Here \(a_1=3\), and \(a_{n+1}/a_n\ge8\), so \(a_n\ge3n\). Conditional failure at stage \(n\) is at most \(e^{-3n}\). The first-failure union bound gives conditional all-stage success at least

\[
1-\sum_{n\ge1}e^{-3n}=1-\frac1{e^3-1}>\frac{14}{15}.
\]

The last inequality follows without a decimal approximation from \(e^3>1+3+9/2+27/6+81/24=131/8>16\). Thus an infinite selected forward ray has probability at least \(7/30\).

On that ray, require root recovery-free on \([0,\tau]\), and its \(n\)-th descendant recovery-free on \([s_{n-1},\tau]\). The total required recovery-free exposure is

\[
\tau+\sum_{n\ge1}(\tau-s_{n-1})=3\tau.
\]

Because the vertices are distinct and recovery clocks were never inspected, the conditional probability is exactly \(e^{-3\tau}\). Each fixed ray vertex is infected at \(\tau\) through its own finite graphical path. This proves the exact annealed bound independently.

The independently developed quenched route differs from the submission. Define \(h_r(S)\) as a subtree's probability of an infinite infected set at \(1/(2r)\). Its annealed expectation is positive, so a fresh subtree has positive probability \(\rho_r\) of satisfying \(h_r>0\). Generation sizes \(Z_n\) increase to infinity almost surely: if the nondecreasing integer sequence were bounded, it would eventually stay at some \(k\), requiring all offspring counts in infinitely many size-\(k\) generations to be one. Conditional probabilities \(\mathbb P(\xi=1)^{kj}\) tend to zero. Independent generation-\(n\) subtrees then yield

\[
\mathbb P(\text{no favorable subtree at generation }n)
=\mathbb E(1-\rho_r)^{Z_n}\longrightarrow0.
\]

Almost every tree has a favorable descendant. A finite positive-probability access path puts an infection at that descendant at time one, and independent future marks give explosion at \(1+1/(2r)\). Intersecting the full-measure sets for \(r=1/m\) and adding arrows extends this to every positive rate. Full details are preserved in the frozen independent derivation.

## 3. Comparison with the submitted ray estimates

The submitted proof's §§3–4 (lines 46–133) uses smaller, exponentially growing thresholds:

\[
D_n=16^{n+2}=2^{4n+8},\qquad
\ell_n=\frac{2^{-n-2}}{\lambda},\qquad
s_n=\frac{1-2^{-n}}{2\lambda},\quad n\ge0.
\]

The root threshold is again \(D_0=256\), costing \(1/4\). The time windows are \([s_n,s_{n+1})\). A candidate child at stage \(n\) passes with probability

\[
p_n=D_{n+1}^{-1/4}(1-e^{-\lambda\ell_n})
=2^{-n-3}(1-e^{-2^{-n-2}}).
\]

The factor \(2^{-n-3}\) is correct: \(D_{n+1}=2^{4n+12}\). Using \(1-e^{-x}\ge x/2\) for \(0\le x\le1\) gives

\[
p_n\ge2^{-2n-6},\quad D_np_n\ge2^{2n+2}=4^{n+1}.
\]

Conditional stage failure is consequently at most

\[
(1-p_n)^{D_n}\le e^{-D_np_n}\le e^{-4^{n+1}}
\le2^{-4(n+1)}.
\]

The final inequality follows from \(4^{n+1}\ge4(n+1)\) and \(e>2\), including the boundary stage \(n=0\). These bounds are correct for every stage. Their infinite sum is exactly

\[
\sum_{n\ge0}2^{-4(n+1)}=\frac1{15}.
\]

If \(F_n\) is first failure at stage \(n\), then its conditional probability given root qualification is bounded by the stated stage bound multiplied by the probability of reaching that stage, hence by the bound itself. Summing the disjoint first-failure events proves all-stage success at least \(14/15\), and multiplying by root qualification proves \(\mathbb P(G)\ge7/30\). Independence between different stage-success events is neither true in general nor required.

The submitted thresholds are more economical than those in the independent derivation. This is a harmless improvement, not an unresolved dependence issue.

## 4. Adaptive conditioning: why the product law is valid

The principal conditioning hazard is to select a child because it has many offspring, then incorrectly call its selected degree unconditioned. The submission does not make that mistake.

At stage \(n-1\), selection of \(v_n\) uses its own offspring count and its incoming edge's arrow marks in the previous deterministic interval. It may bias that count substantially. At the next stage, only a lower bound \(\xi_{v_n}\ge D_n\) is used. The first \(D_n\) children's own offspring counts and the directed arrows from \(v_n\) to those children have never been examined. They are independent of the previously revealed data and of each other.

One can formalize this by assigning iid offspring variables to the countable Ulam–Harris word set before exploring the tree, and independent arrow processes to potential ordered edges. The vertex selected at each finite step is a measurable function of finitely many revealed offspring and arrow variables. The new child variables are in disjoint coordinates outside this history. The first-passing-child rule gives a random coordinate, but does not inspect that child's children's counts or its outgoing arrows. Unused sibling branches similarly expose no variables in the next selected generation.

This establishes the **annealed** conditional child product law given the exploration history. It does not assert such a law after conditioning on the entire tree; after fixing the tree, the degrees are of course fixed. The later recovery computation legitimately conditions on the entire tree and all arrows because recoveries form a separate independent family. These are distinct conditioning steps, consistently used.

## 5. Infinite recovery product and common-time infection

The submitted survival event is exactly the one independently derived:

\[
R_0=\{v_0\text{ has no recovery in }[0,\tau]\},\quad
R_n=\{v_n\text{ has no recovery in }[s_{n-1},\tau]\},\ n\ge1.
\]

On the tree-and-arrow event \(G\), the selected vertices are distinct. Conditional on all tree and arrow data, the recovery marks at these vertices remain independent rate-one clocks. For the first \(N\) descendants the conditional probability of the no-recovery event is

\[
\exp\left[-\tau-\sum_{n=1}^N(\tau-s_{n-1})\right]
=\exp[-(3-2^{1-N})\tau].
\]

These finite survival events decrease to the countable event \(R\). Continuity from above yields \(\mathbb P(R\mid\text{tree, arrows})=e^{-3\tau}\) on \(G\). The infinite product is positive because its exponent is a finite sum. There is no independence claim about infection states along the ray.

For each finite \(n\), the selected incoming arrow of \(v_n\) lies in \([s_{n-1},s_n)\). Its required no-recovery interval begins at \(s_{n-1}\), so it cannot lose that infection before \(\tau\). Its parent is infected by \(s_{n-1}\) and remains infected thereafter. Starting with the root proves inductively that every \(v_n\) is infected at the **same** time \(\tau\).

For each \(n\) this proof uses exactly \(n\) downward arrows and finitely many vertical segments, all within the radius-\(n\) ball. Thus it certifies membership in the explicitly specified minimal finite-path process. It does not treat an infinite-jump path as a legal infection path, import an infection from infinity, or assume a process restart at an explosion time. Deterministic endpoints have probability zero of carrying any mark in these countably many finite-rate clocks, so the open/closed endpoint convention does not change the probability.

Combining the tree-and-arrow success probability and conditional recovery probability is legitimate:

\[
\mathbb P(G\cap R)=\mathbb E[1_G\mathbb P(R\mid\text{tree, arrows})]
=e^{-3\tau}\mathbb P(G)\ge\frac7{30}e^{-3\tau}.
\]

## 6. Submitted quenched argument and all-rate quantifiers

The submission's §5 (lines 135–155) proves a stronger fixed-rate propagation statement by a clean inherited-property argument. Fix \(\lambda>0\), and call a deterministic rooted tree good if its root-started graphical process has positive probability of an infinite configuration at at least one of the countable times \(\tau+m\), \(m\ge0\). Let \(q\) be the Galton–Watson probability of this tree property. The annealed bound implies \(q>0\).

A good child subtree makes its parent tree good. On a fixed tree, keep parent and child recovery-free in \([0,1]\), and require a downward arrow in \([0,1/2]\). This event has probability

\[
e^{-2}(1-e^{-\lambda/2})>0.
\]

The child is then infected at time one. Marks after time one are independent of this access event. Choose a time \(\tau+m\) at which the child's root-started subtree process has positive probability of an infinite configuration; such an \(m\) exists by countability. Every one of that subtree event's finite infection paths can be concatenated with the finite access path. The parent tree therefore has an infinite configuration with positive probability at \(\tau+(m+1)\).

No Markov property at an explosion time is needed: the shift time is the fixed deterministic time one. Extra paths from infections outside the subtree cannot invalidate any concatenated path.

Given the root offspring count, its descendant subtrees are iid copies of the whole Galton–Watson tree. A bad parent must have only bad children, so

\[
1-q\le\mathbb E[(1-q)^\xi].
\]

If \(0<q<1\), putting \(z=1-q\in(0,1)\) gives \(z^\xi\le z\) almost surely and strict inequality on \(\{\xi\ge2\}\), an event of positive probability. Hence \(\mathbb E z^\xi<z\), contradicting the previous inequality. Therefore \(q=1\). This uses no finite-mean assumption.

For each positive rational rate the good-tree property has full measure. The intersection over those countably many rates still has full measure. For any positive real rate, choose a smaller positive rational rate and superpose extra arrows, using the same recoveries. Every finite path at the lower rate remains available at the higher rate. An infinite infected set at a finite lower-rate time therefore has at least the same positive probability at the higher rate. This proves the order of quantifiers claimed in the statement; it does not intersect uncountably many probability-one sets.

The original annealed result alone would not establish this quenched assertion. The submitted inheritance argument and the independently derived generation-growth argument both close that otherwise real gap.

## 7. Measurability and graphical coupling

All possible vertices and finite vertex sequences are countable. Random-tree membership of a finite word is determined by finitely many ancestral offspring counts. A finite path's validity over a bounded interval is a measurable function of finitely many clocks. For a fixed endpoint and time, graphical reachability is a countable union over finite paths; on each finite ball it also agrees with the ordinary finite-state graphical process. Taking the increasing union over balls gives the specified minimal process.

An infinite infected set at a fixed time is measurable because the vertex set is countable; for example, enumerate all potential vertices and use the event that its membership-indicator sum diverges. Its graphical probability as a function of the tree is measurable by integration. Countable unions over \(\tau+m\) and finite child scans preserve measurability. This makes the good-tree probability \(q\) and the independent \(h_r\)-subtree amplification well defined.

Adding arrows pathwise preserves finite-path membership, at every time. Suppressing edges produces a subset of paths. These two direct graphical facts justify both rate monotonicity and subtree restart domination, including after an infinite infected configuration has become possible.

The additional submitted fitness statement is mathematically valid when every assigned \(F_v\) is finite and at least one, and the graphical clocks are sampled conditionally on that assignment. On each ordered edge add independent rate \(\lambda(F_uF_v-1)\) arrows. Each rate is finite, the edge set is countable, and every old finite path remains valid. No uniform fitness bound is required. Whether the original source permits the specific constant fitness choice is a source-interpretation matter that this family has not checked.

## 8. Adversarial attacks, edge cases, and blocked shortcuts

| Attack or boundary case | Audit finding |
|---|---|
| Selected vertex has a conditioned high degree | Valid: only its lower bound is used; fresh grandchildren and outgoing arrows retain their product law. |
| Treat stage-success events as independent | That shortcut is unjustified; the submitted first-failure sum does not use it. |
| Condition on the whole tree while using iid child degrees | That shortcut is invalid; the stage estimate conditions only on revealed exploration history. Whole-tree conditioning is used later only for independent recoveries. |
| Require every ray vertex recovery-free on all of \([0,\tau]\) | This would cost probability zero. The submitted shrinking windows have total exposure \(3\tau\). |
| Show only summable passage times / an infinite first-passage ray | This alone does not certify simultaneous infections in a recovery process. The survival windows certify every vertex at one final time. |
| Permit an infection path with infinitely many arrows to an endpoint at infinity | Such a path is unnecessary and is not used. Each listed infected vertex has a finite witness in a finite ball. |
| Use positive annealed probability to claim almost every tree explodes | Invalid without amplification. The inherited-good-subtree argument closes this gap. |
| Swap almost-every-tree and every-real-rate quantifiers | Avoided by a countable rational-rate intersection and explicit arrow superposition. |
| Restart using a stopping time equal to explosion | No such restart is used. The access and future subtree argument uses fixed time one. |
| Very small positive \(\lambda\) | The final time is large and the recovery probability can be extremely small, but it remains positive and the time-window arrow probabilities retain the same scaled values. |
| Very large positive \(\lambda\) | The final time shrinks, but all stage estimates remain valid because the arrow-window products \(\lambda\ell_n\) are unchanged. |
| \(\lambda=0\) | Excluded; no infection spreads. The theorem does not claim an extension to this boundary. |
| Degree-one infinite ray as a deterministic tree | A counterexample to any every-tree claim: even the no-recovery infection process takes a sum of iid positive exponential waits to reach arbitrarily far, hence cannot explode. This tree has Galton–Watson probability zero under the stated law. |
| Offspring allowed to be infinite | Not allowed or needed. The specified tail tends to zero. |
| Other infinite-mean offspring laws | Not classified. Infinite mean alone is not asserted as a sufficient condition by this proof. |

No genuinely new unresolved mathematical gap resulted from these attacks. The incorrect shortcut routes above are blocked; they are not substitutes for the verified mechanism.

## 9. Reproducible checks and deliverables

`audit_checks.py` uses only Python's standard library. It verifies exact stage algebra for a finite range, the exact infinite geometric failure sum, the exact \(7/30\) prefactor, the recovery partial sum \((3-2^{1-N})\tau\), and the independent threshold lower bounds. The all-stage proofs are analytical and given above; finite checks are not presented as proofs of conditional independence or infinite limits. `CHECK_RESULTS.json` records a passing result and labels floating diagnostic quantities as non-proof evidence. No random simulation was used.

Run it with:

```text
python3 audit_checks.py
```

All outputs are confined to this audit family's assigned folder. The folder also includes the frozen pre-comparison derivation, timestamped research log, inspected-input manifest, and final authored-output manifest with SHA256 hashes.

## 10. Strongest verified result and exact remaining scope

**Strongest verified mathematical result:** both the exact annealed lower bound and the almost-every-tree, every-positive-rate quenched explosion statement follow rigorously for the explicitly specified finite-path process and offspring law. The proof also survives any finite fitness assignment bounded below by one under the usual conditional graphical construction. The full submitted probability argument is consistent with the independent derivation; no proof repair is required for these claims.

**Exact remaining scope:** this family has not verified what the original cited question means, whether its allowed fitness distributions include the proposed specialization, whether the external papers use precisely the cited definitions and page numbers, or whether the result has already appeared elsewhere. The submitted external citations are claims in an inspected document, not independently verified source evidence here. No novelty or priority conclusion should be attributed to this report. The parent mathematical audit should receive a separate adversarial checkpoint before promoting the candidate.

Best-guess completion of this family's assigned mathematical audit: **100%**. Completion of novelty/priority clearance: **not assessed**.
