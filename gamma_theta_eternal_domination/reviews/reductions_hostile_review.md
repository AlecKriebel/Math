# Independent hostile review of the core reductions

**Review date:** 2026-07-25 13:24 PDT  
**Files reviewed:** `math/reductions.md`, `math/reductions_audit.md`,
and `math/class_restrictions_pending.md`  
**Verdict:** **ACCEPT** every numbered mathematical result in
`math/reductions.md`, with the explicitly stated dependence on the Strong
Perfect Graph Theorem where applicable.  No critical, high-severity, or
medium-severity mathematical defect was found.  The only findings are
low-severity dependency-ledger and exposition corrections.  The
citation-pending graph-class restrictions are accepted only as a quarantine
mechanism; they are not accepted as established search filters.

## 1. Model audited

I used exactly the family definition

\[
 \forall D\in\mathcal F\ \forall r\in V(G)\setminus D\
 \exists u\in D\cap N_G(r):
 (D-\{u\})\cup\{r\}\in\mathcal F,
\]

where every member of the nonempty family \(\mathcal F\) is a dominating
\(k\)-subset.  Thus the attacked vertex is unoccupied, one guard is removed,
that guard is adjacent to the attacked vertex, and the attacked vertex is
inserted.  I did not use an all-guards-move, occupied-attack, total-domination,
or non-family formulation.

## 2. Severity-ranked findings

### Critical, high, and medium severity

None.

### Low severity L1: the dependency ledger combines two results with
different dependencies

In `math/reductions_audit.md`, the row

> Component additivity and connected reduction | None

is not an exact dependency record.  Proposition 5 (additivity) is proved from
the definitions, but Corollary 6 (connected reduction) additionally uses the
componentwise inequalities
\(\gamma(G_j)\leq\gamma^\infty(G_j)\leq\theta(G_j)\) from Theorem 2.

**Exact correction:** split the row into

| Result | Nondefinitional dependency | Current proof status |
|---|---|---|
| Component additivity | None | Complete |
| Connected reduction | Component additivity and the parameter chain | Complete |

Likewise, the imperfection-obstruction row should list **equality collapse and
SPGT**, not only SPGT, because Proposition 7 uses
\(\alpha(G)=\gamma^\infty(G)\) from Corollary 3.  These omissions do not affect
either proof.

### Low severity L2: the proof of \(\alpha\leq\gamma^\infty\) has one
unnecessarily compressed sentence

Theorem 2, item 3, is correct.  However, the sentence

> Equivalently, the step-by-step argument gives
> \(k\geq |I|=\alpha(G)\).

compresses the final contradiction into wording that can sound as though
Lemma 1 alone literally returns \(|I|\) guards when \(|I|>k\).

**Exact replacement:**

> If \(|I|>k\), Lemma 1 reaches a configuration whose \(k\) guards all lie in
> \(I\).  Choose \(r\in I-D\).  Since \(I\) is independent,
> \(D\cap N(r)=\varnothing\), contradicting the required response to the
> unoccupied attack at \(r\).  Hence \(k\geq |I|=\alpha(G)\).

The existing preceding sentence already makes this argument, so this is an
expository correction only.

### Low severity L3: the perfect-graph row asks for an unnecessary
class-specific eternal-domination theorem

The perfect-graph exclusion in `math/class_restrictions_pending.md` is
mathematically valid without locating a separate theorem asserting a
one-guard bound or equality on perfect graphs.  If \(G\) is perfect, closure
of perfect graphs under complementation gives

\[
 \theta(G)=\chi(\overline G)=\omega(\overline G)=\alpha(G).
\]

The already proved chain
\(\alpha(G)\leq\gamma^\infty(G)\leq\theta(G)\) then gives
\(\gamma^\infty(G)=\theta(G)\).

**Exact correction to the “source statement still required” cell:** replace
the request for a “primary source for the standard one-guard bound/equality”
by a primary citation for complement closure/perfect-graph identity (or use
SPGT, already invoked in the reductions).  No graph-class-specific eternal
domination result is needed.

### Optional clarity improvement, not a finding

In the final step of Lemma 9, one may add that both candidate moves are edges
of \(A_n\): both \(0\) and \(n-4\) are at cyclic distance \(2\) from \(n-2\).
The proof is already sound without this sentence—an illegal candidate would
also fail to be a valid response—but stating legality makes the attack audit
maximally explicit.

## 3. Accept/reject decisions

| Result | Decision | Hostile-check summary |
|---|---|---|
| Lemma 1 (independent-set forcing) | **ACCEPT** | For every response supplied by family closure, the moved guard lies outside \(I\), because \(r\in I\) is unoccupied and \(I\) is independent.  Hence \(|D\cap I|\) increases by exactly one.  If \(|I|>k\), the next unoccupied attack in \(I\) has no adjacent guard. |
| Theorem 2 (parameter chain) | **ACCEPT** | Maximal independent sets are precisely independent dominating sets; the forcing argument proves \(\alpha\leq\gamma^\infty\); the clique-partition strategy moves only the one guard assigned to the attacked clique. |
| Corollary 3 (equality collapse) | **ACCEPT** | Immediate squeeze between equal endpoints of the proved chain. |
| Corollary 4 (well-coveredness) | **ACCEPT** | \(i=\alpha\) forces every maximal independent set to have the common size \(\alpha\). |
| Converse warnings after Corollary 4 | **ACCEPT** | \(K_{3,3}\) is well-covered but has \(\gamma=2<3=\alpha\).  \(C_5\) is well-covered with \(\gamma=\alpha=2<3=\gamma^\infty\).  No converse is smuggled into the search target. |
| Proposition 5 (component additivity) | **ACCEPT** | A one-guard move cannot change a component-count vector.  Each nonempty count-vector sector is closed.  Projecting a fixed sector gives a dominating closed family in each component; the product construction proves the reverse inequality. |
| Corollary 6 (connected reduction) | **ACCEPT** | Nonnegative component gaps \(\gamma^\infty-\gamma\) sum to zero, so every component has equality; a positive summed \(\theta-\gamma^\infty\) gap occurs in at least one component. |
| Proposition 7 (imperfection obstruction) | **ACCEPT relative to SPGT** | For \(H=\overline G\), equality collapse gives \(\omega(H)=\alpha(G)=k<\theta(G)=\chi(H)\).  SPGT applies to \(H\), and complementation interchanges induced holes and antiholes on the same vertex set. |
| Lemma 8 (induced-subgraph monotonicity) | **ACCEPT** | The maximum-\(|D\cap W|\) choice repairs the failure of naive projection.  For \(S=D\cap W\) and \(r\in W-S\), closure gives a response.  A responding guard outside \(W\) would produce a family member with \(m+1\) guards in \(W\), contradicting maximality; therefore the witness lies in \(S\), the successor remains in the maximum slice, and the projected family both dominates and is closed. |
| Lemma 9 (odd antiholes) | **ACCEPT** | In \(\overline{C_n}\), a two-set is nondominating exactly at cyclic distance \(2\).  Lemma 1 forces \(\{0,1\}\).  Each attack at \(d+2\) invalidates the move from \(0\) and forces \(d\mapsto d+2\).  The final attack at \(n-2\) makes both possible successors nondominating.  The \(n=5\) case is a valid direct final step.  The upper bound is the one-guard clique-partition bound with \(\theta(\overline{C_n})=\chi(C_n)=3\). |
| Theorem 10 (\(\alpha=\gamma^\infty=2\)) | **ACCEPT relative to SPGT** | The complement has \(\omega=2<\chi\).  An induced odd hole in the complement gives an induced odd antihole in \(G\), contradicting Lemmas 8–9.  An induced odd antihole of length at least \(7\) gives an induced odd cycle in \(G\) with an independent 3-set; length \(5\) again contradicts Lemmas 8–9. |
| Corollary 11 (minimum parameter) | **ACCEPT relative to SPGT** | \(k=1\) forces a complete graph; \(k=2\) is excluded by Theorem 10. |
| Section 7 search target | **ACCEPT as necessary conditions only** | Connectedness, all parameter equalities, \(k\geq3\), the clique-cover gap, and an induced odd hole/antihole all follow.  The note correctly refuses to treat them as sufficient. |

## 4. Detailed audit of the two highest-risk proofs

### Lemma 8: quantifiers and maximum-occupancy projection

The proof correctly handles the order of quantifiers.  For each
\(S\in\mathcal P\), choose a representing \(D\in\mathcal F^\star\).  For each
\(r\in W-S\), one also has \(r\notin D\), so the global family axiom applies.
Its existential response cannot use \(u\notin W\), since that particular
successor belongs to \(\mathcal F\) and would have \(m+1\) guards in \(W\).
Thus the existential witness supplied by closure lies in \(W\), hence in
\(S\).  Its successor has exactly \(m\) guards in \(W\), so it lies back in
\(\mathcal F^\star\).  This proves the projected closure with the correct
\(\forall S\,\forall r\,\exists u\) order.

The proof does **not** need \(\mathcal F^\star\) to be globally closed against
attacks outside \(W\), and it does not claim that.  The same local response
also proves domination of \(H\).  If \(m=0\), nonemptiness of \(W\) supplies an
attack whose response would raise the occupancy to \(1\), a contradiction.

A nearby false argument was explicitly tested: arbitrary projection does not
work.  In \(P_3\), the two-guard eternal family contains
\(\{0,1\}\); projecting this configuration onto the induced subgraph on the
two endpoints gives the singleton \(\{0\}\), which does not dominate the two
isolated endpoints.  Taking the maximum-occupancy slice instead selects the
configuration occupying both endpoints, exactly as Lemma 8 requires.

### Lemma 9: every attack and successor

For a two-set \(\{x,y\}\) in \(A_n=\overline{C_n}\), an outside vertex \(z\)
is undominated precisely when \(z\) is a cycle-neighbor of both \(x\) and
\(y\).  For \(n\geq5\), this happens precisely when \(x,y\) are the two
cycle-neighbors of some \(z\), equivalently when their cyclic distance is
\(2\).

For odd \(d\) with \(1\leq d\leq n-6\), the attacked vertex \(d+2\) is not in
\(\{0,d\}\).  The move \(d\mapsto d+2\) is an \(A_n\)-edge because its cycle
distance is \(2\).  The other successor, if considered, is
\(\{d,d+2\}\), a nondominating pair, so family closure forces
\(\{0,d+2\}\).  At the last configuration \(\{0,n-4\}\), the attack \(n-2\)
is unoccupied, and the two successors \(\{0,n-2\}\) and
\(\{n-4,n-2\}\) both have cycle distance \(2\).  For \(n=5\), these are
exactly the two successors from the initial forced configuration
\(\{0,1\}\).  There is no occupied attack, no stationary guard response, and
no simultaneous move in the argument.

## 5. Independent computational falsification attempts

These checks are supporting evidence, not substitutes for the proofs.

- With verifier A, and separately with the structurally independent verifier
  B, I checked every nonempty induced-subgraph pair of every labeled graph
  of orders \(1\) through \(5\): **32,767 pairs per verifier**.  No violation of
  \(\gamma^\infty(G[W])\leq\gamma^\infty(G)\) occurred.
- Both verifiers returned
  \(\gamma^\infty(\overline{C_n})=3\) independently for
  \(n=5,7,9,11,13,15\).
- Verifier A checked the full parameter chain and component additivity on all
  **1,099 labeled graphs of orders \(1\) through \(5\)**; no violation
  occurred.

## 6. Review of `class_restrictions_pending.md`

The file's logical firewall is **ACCEPTED**.  In particular, it correctly
distinguishes the implication
\(\gamma=\gamma^\infty\Rightarrow\gamma=\theta\) from an unconditional
\(\gamma^\infty=\theta\) theorem, flags the one-guard/all-guards model hazard,
and refuses to blur subgraph-\(C_4\)-free with induced-\(C_4\)-free.

The substantive status decisions are:

| Proposed class restriction | Review decision |
|---|---|
| Perfect graphs | **ACCEPT mathematically**, using \(\alpha=\theta\) for perfect graphs and the parameter chain; citation attribution remains to be recorded. |
| Circular-arc graphs | **WITHHOLD / PENDING** exactly as the file says. |
| Series-parallel or \(K_4\)-minor-free graphs | **WITHHOLD / PENDING** exactly as the file says. |
| Outerplanar graphs | **WITHHOLD / PENDING** exactly as the file says. |
| Subcubic graphs | **WITHHOLD / PENDING** exactly as the file says. |
| Triangle-free graphs | **WITHHOLD / PENDING** exactly as the file says. |
| \(C_4\)-free graphs | **WITHHOLD / PENDING** exactly as the file says. |
| Planar graphs | **WITHHOLD / PENDING** exactly as the file says. |

Therefore the filters “nonplanar,”
\(\Delta\geq4\), “contains a triangle,” and “contains a \(4\)-cycle” must not
yet enter any coverage certificate.  The conditional combination in the file
is logically valid once the exact primary theorems and their conventions are
verified.

## 7. Final audit conclusion

No numbered reduction should be rejected or demoted on mathematical grounds.
In particular:

1. \(\alpha\leq\gamma^\infty\) uses only unoccupied attacks and one-guard
   moves.
2. Eternal domination is additive over components under the stated family
   definition.
3. The maximum-occupancy projection proves the claimed induced-subgraph
   monotonicity; the tempting naive projection is false, but is not used.
4. The odd-antihole attack sequence is complete for every odd \(n\geq5\).
5. The SPGT complement translation and the \(\alpha=2\) exclusion are sound.
6. The note never infers \(\gamma=\alpha\) from well-coveredness and explicitly
   supplies counterexamples to both tempting converses.

The proof document is ready to serve as a sound basis for search restrictions
once the external graph-class rows are separately source-audited.
