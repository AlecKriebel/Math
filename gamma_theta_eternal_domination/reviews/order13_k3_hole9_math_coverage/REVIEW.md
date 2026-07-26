# Hostile mathematical coverage audit of the order-13 `hole9` certificate

**Audit date:** 2026-07-26  
**Verdict:** `ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION`

## Exact accepted result

Relative to C-050 and the accepted inputs of C-055, there is no order-13
counterexample with common parameter three whose complement contains a
hub-free induced \(C_9\).

Combining this certificate-backed branch exclusion with the accepted C-053
near-spanning-hole theorem reduces the live order-13, parameter-three cover
from

\[
 C_5,\ C_7,\ C_9
\]

to the two overlapping branches

\[
 C_5,\ C_7.
\]

The theorem and its exact bytes are accepted as written in
`math/lemmas/order13_k3_hole9_certificate_exclusion.md`, 7,351 bytes,
SHA-256
`372f1595dc224232095eb9cf9523eb1d1d992502391d6fc58f3e818d41769937`.

This is a certified finite **template exclusion**. It is not a complete
order-13 parameter-three exclusion, because `hole5` and `hole7` remain live.
It says nothing decisive about the order-13 parameter-four or parameter-five
slices. It does not exclude all order-13 counterexamples, raise the global
counterexample lower bound to 14, or resolve the universal conjecture.

## Certificate acceptance

The exact formula has:

| field | value |
|---|---:|
| variables | 9,802 |
| clauses | 32,108 |
| literal occurrences | 281,028 |
| bytes | 1,168,197 |
| SHA-256 | `3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea` |

The independently written verifier B, exact SHA-256
`4adf3691f438c03b230ff323ea5f7c180db9b5c8cd895b6f31327f5e154a97ee`,
was freshly replayed during this audit. Its output was byte-identical to the
15,105-byte retained evidence with SHA-256
`3de45d16b906e52c3960e4b2e75604908c8cacf356b84d7337db721f4fa49af8`.
All seven focused tests passed.

The verifier independently establishes that the certificate formula and the
accepted constructor formula are byte-identical. It parses the normalized
binary proof as 45,281 additions, consisting of 45,280 nonempty additions
and one unique final empty addition, with no deletions and no post-empty
data. The exact proof has SHA-256
`af216ef2d7698db2b1d1c55411bc05025bfe25f10c16f2e85c5301f7a88bdd5f`.

A private warning-fatal `drat-trim` run in RUP-only forward mode returned
exit zero, empty stderr, one exact `s VERIFIED`, and zero RAT lemmas in the
core. A separate `lrat-check` replay against the exact 8,546,664-byte LRAT,
SHA-256
`f6ef614f2acee4cf43aa3b75372b354912c50248a13c3f863479cdc49b061805`,
returned exit zero, empty stderr, and one exact `c VERIFIED`.

The final external exact-byte code audit was also independently replayed
during this review. Its exact artifacts are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| external `REVIEW.md` | 9,578 | `aef1543f799666fd32842dd2aaa454d7ae65c9556374cbf6d5d4f5f6bbb18c4a` |
| external `evidence.json` | 8,482 | `97aad1ec54552aca510d511063ccca74de702dc4f9f1796dbbc2333f4c42ecd9` |
| external `replay.py` | 21,785 | `e7627c21fa588ec4b1efd2438d6666acf6f437bbed6dcff7ebe5b592fe38e66f` |

That audit returned
`ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER`, rejected all 24 hostile
corruptions, rebuilt both retained checkers from the retained C sources,
obtained byte-identical executables, and replayed both proofs. It caught and
repaired two stale hashes in supporting source-build provenance. The
corrected final provenance has SHA-256
`95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275`.
The defective provenance values were never used by the decisive verifier;
the exact proof, formula, checker binaries, and successful checker runs did
not change.

The verifier's retained verdict ends with
`PENDING_HOSTILE_ACCEPTANCE`. That wording is an intentional claim boundary,
not a remaining blocker. The external code audit accepts the exact-CNF
verification, and this review supplies the separately requested hostile
mathematical integration acceptance.

## Independent formula reconstruction

The read-only audit in this directory imports no campaign module and launches
no solver or proof checker. It independently allocates all 9,802 variables
and reconstructs every clause from the mathematical specification:

| clause family | clauses |
|---|---:|
| no \(K_4\) in \(H\) | 715 |
| pair common-neighbor choice | 78 |
| pair common-neighbor implications | 1,716 |
| induced \(C_9\) | 36 |
| selected-hole hub-free clauses | 4 |
| named rim-edge common neighbor | 2 |
| connected cuts in \(G\) | 4,095 |
| selected-state domination | 2,860 |
| nonempty eternal family | 1 |
| move uses a \(G\)-edge | 8,580 |
| successor remains in the family | 8,580 |
| selected attack has a response | 2,860 |
| every \(H\)-triangle is selected | 286 |
| complete coloring obstruction | 2,295 |

The independently reconstructed ordered DIMACS stream is byte-identical to
the exact certified formula, not merely equal in census or clause multiset.
This also proves that the certified bytes contain no extra signature sort,
rim reflection, DoubleLex clause, unrelated independent anchor, or other
heuristic graph-symmetry breaker.

For the coloring bank, the audit enumerates all

\[
 3^{13}=1{,}594{,}323
\]

named color rows independently. Exactly 13,770 are proper on the forced
positive template edges. Their first-use canonical quotients are exactly the
2,295 retained rows:

\[
 13{,}770=(2^9-2)3^3=6\cdot2{,}295.
\]

The fixed \(H\)-triangle \(\{0,1,9\}\) makes the color-name action free.
Thus the bank removes only the six names of three colors. It is complete and
does not impose a vertex symmetry.

## Graph-to-formula implication

Assume that \(G\) is an order-13 counterexample with

\[
 \gamma(G)=\gamma^\infty(G)=3<\theta(G)
\]

and that \(H=\overline G\) contains a hub-free induced \(C_9\).

The accepted parameter chain gives

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=3.
\]

In particular, no pair dominates \(G\). For every pair \(a,b\), there is
therefore a vertex outside the pair nonadjacent in \(G\) to both, equivalently
an external common \(H\)-neighbor of \(a,b\). This complement sign is
correct.

Choose the stated \(C_9\), either orientation, and any starting rim edge.
Label the rim \(0,1,\ldots,8\). The endpoints of rim edge \(01\) have a
common \(H\)-neighbor. It cannot lie on the induced rim, so label one such
outside vertex 9 and label the three remaining vertices arbitrarily. This is
a relabeling of the whole graph, not an automorphism assumption. It loses no
target regardless of how many admissible holes, rim edges, or common
neighbors the graph has.

The forced edges \(01,09,19\) make \(\{0,1,9\}\) an \(H\)-triangle and
therefore an independent triple in \(G\). Since \(\alpha(G)=3\), it is
maximum. The accepted maximum-independent-state lemma puts every such triple
in every eternal family of triples, so the triangle-to-family strengthening
is sound.

Relative to C-050, the graph is connected: otherwise component additivity
would put equality in every component and the clique-cover gap in a component
of order at most 12, contradicting the accepted lower-order frontier.
C-050 itself remains explicitly relative to MacGillivray--Mynhardt--Virgile's
published through-order-11 computation; this audit does not relabel that
premise as a campaign-only enumeration.

All remaining graph-to-CNF signs and quantifiers are exact:

- \(e_{uv}=1\) means \(uv\in E(H)\), so a guard edge in \(G\) is
  \(\neg e_{uv}\).
- Witness variables range only over vertices outside the named pair.
- Domination clauses cover exactly the unoccupied vertices of each selected
  state; occupied vertices dominate themselves.
- Attack-response variables exist only for \(r\notin D\).
- Each response names one guard \(u\), traverses one \(G\)-edge, and selects
  exactly \(D-u+r\).
- Several true response variables are alternative existential witnesses;
  decoding chooses one. They do not encode simultaneous guard movement.
- Every selected successor is subject to the domination clauses.
- Every proper cut has a negative \(H\)-edge, exactly a crossing \(G\)-edge.
- The complete coloring bank makes \(\chi(H)>3\), equivalently
  \(\theta(G)>3\).

Thus Theorem 4 of C-055 maps the relabeled graph and a genuine one-guard
eternal family to a satisfying assignment of the exact formula. The
independently certified UNSAT proof contradicts that assignment. Therefore
the hub-free \(C_9\) branch is empty.

There is no circular use of the gamma--theta conjecture. The strict
clique-cover gap is a counterexample hypothesis and is encoded directly as
non-three-colorability of \(H\). Equality with \(\alpha\) comes from the
parameter chain, not from well-coveredness alone.

## Coverage after the branch exclusion

The accepted C-055 coverage proof starts from
\(\omega(H)=3<\chi(H)\). The Strong Perfect Graph Theorem gives an odd hole
or odd antihole. Accepted C-017 removes the only additional
\(\overline{C_7}\) antihole case, and accepted C-014 makes every induced odd
hole hub-free. Pair/common-neighbor forcing gives at least two outside
vertices, yielding the four overlapping order-13 lengths

\[
 5,\ 7,\ 9,\ 11.
\]

C-053 strengthens the outside-vertex bound to three for parameter-three
equality graphs and therefore removes \(C_{11}\). The exact certificate
accepted here removes \(C_9\). Hence every remaining order-13,
parameter-three counterexample would lie in at least one of the \(C_5\) or
\(C_7\) branches.

The branches are an overlapping cover, not a partition. No graph is assigned
a unique hole. Excluding a branch means that no target can possess any
admissible occurrence of that hole, because any chosen occurrence can be
relabelled into the formula. No inclusion--exclusion or orbit-counting
argument is required.

## Claim boundary and caveats

The following are **not** established:

1. the complete order-13, parameter-three slice;
2. either the `hole5` or `hole7` branch;
3. the order-13 parameter-four or parameter-five slice;
4. absence of every order-13 counterexample;
5. a counterexample lower bound of 14;
6. a universal proof or counterexample; or
7. novelty or priority.

The external code audit records three nonblocking caveats: the focused unit
test contains 18 base mutations while the complete replay contains all 24;
runtime source authentication comes from the external exact-byte binding,
not the verifier's self-observation; and exact compiler-output equality is
platform-specific. None affects the accepted exact-CNF proof on the audited
machine.

Blocking mathematical defects: **0**.  
Blocking formula-coverage defects: **0**.  
Blocking certificate or binding defects: **0**.  
Blocking scope defects: **0**.

## Reproduction

From the campaign directory:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
python3 -W error reviews/order13_k3_hole9_math_coverage/audit.py |
cmp - reviews/order13_k3_hole9_math_coverage/evidence.json
```

The audit enumerates all named colorings, independently reconstructs the
formula byte for byte, independently recounts the binary proof, and checks
all accepted dependency and verifier verdicts. It is read-only and normally
takes about one second on the campaign MacBook.

The exact audit artifacts are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `audit.py` | 37,142 | `d98cb928f1616710f1cb52b0a174d37ab1ae86568e778aab1e2ebdd1186f8f44` |
| `evidence.json` | 13,539 | `511de162e1d3a94adf495896d638d943b179a3007b6dfc72fd0316e2ef37a47d` |
