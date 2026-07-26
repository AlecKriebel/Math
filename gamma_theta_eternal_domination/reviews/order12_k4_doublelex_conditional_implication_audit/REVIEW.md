# Independent conditional implication audit for the order-12 DoubleLex lane

## Verdict

**`VALID_CONDITIONAL_CONNECTED_EXCLUSION_ONLY`.**

Let \(D\) be the exact DIMACS file
`instances/order12_k4_connected_doublelex/instance.cnf`, with

\[
\begin{aligned}
\operatorname{SHA256}(D)
  &=\texttt{14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7},\\
|D|&=4{,}030{,}657\text{ bytes},\\
(v,c,\ell)&=(18{,}381,\ 115{,}507,\ 1{,}190{,}774).
\end{aligned}
\]

If a strict, independently accepted certificate establishes that these
exact bytes are UNSAT, then the accepted claims C-037 and C-045 imply:

> There is no **connected** finite simple graph \(G\) of order \(12\) with
> \(\gamma(G)=\gamma^\infty(G)=4<\theta(G)\).

That conclusion is the complete connected \((n,k)=(12,4)\) exclusion.  It
does not, by itself, exclude disconnected order-12 parameter-four graphs,
establish an all-parameter order-12 frontier, or resolve the universal
\(\gamma\)--\(\theta\) conjecture.

No solver return code, raw proof, converted proof, report, or other pending
certificate artifact is a premise of this audit.  This review neither
accepts nor rejects any currently pending solver or proof-production output.

Audit date: 2026-07-26 PDT.  Snapshot branch: `main`.  Snapshot HEAD:
`9df3a414e6ba9f631ff68bff69d5ab0a37048f5e`.

## 1. Meaning of the strict certificate premise

The mathematical premise needed below is simply that \(D\) is UNSAT.
For campaign promotion, a “strict certificate for
`14284db1...a976e7`” must establish that premise rather than merely report
it.  At minimum, the accepted package must:

1. recompute the exact formula SHA-256 and parse the declared and actual
   DIMACS census;
2. bind the refutation to those exact formula bytes;
3. replay the refutation with a sound checker in a fail-closed,
   warning-fatal run;
4. record exact proof, checker, and replay-result bindings; and
5. receive an independent audit or replay rather than relying on the
   producing solver's exit status.

The implication proved here is conditional on that gate being completed.
It does not assert that any extant candidate package satisfies the gate.

## 2. Exact parent and DoubleLex binding

Write \(F\) for
`instances/order12_k4_connected_parent/instance.cnf`.  The exact audited
artifacts are:

| formula | bytes | variables | clauses | literals | SHA-256 |
|---|---:|---:|---:|---:|---|
| connected parent \(F\) | 3,992,947 | 18,381 | 114,742 | 1,180,016 | `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac` |
| DoubleLex \(D\) | 4,030,657 | 18,381 | 115,507 | 1,190,774 | `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7` |

An independent parse reproduced both declared censuses, both actual clause
counts, both literal counts, and maximum variable 18,381.  After omitting
the two different DIMACS headers, all 114,742 parent clause lines are
byte-for-byte the first 114,742 clause lines of \(D\).  The remaining 765
clause lines have 10,758 literals and SHA-256

`328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0`.

This agrees with the two manifests and the accepted C-045 hostile review.
C-045 proves the exact semantic relation

\[
F\text{ is satisfiable}\quad\Longleftrightarrow\quad
D\text{ is satisfiable}.
\tag{2.1}
\]

It is an equisatisfiability theorem.  It supplies no SAT or UNSAT outcome.

## 3. What exact DoubleLex UNSAT would prove

### Conditional theorem: connected order-12 parameter four

**Theorem.**  Assume a strict certificate establishes that the exact
formula \(D\) above is UNSAT.  Then no connected finite simple graph \(G\)
on 12 vertices satisfies

\[
\gamma(G)=\gamma^\infty(G)=4<\theta(G).
\tag{3.1}
\]

**Proof.**  The strict premise gives that \(D\) is not satisfiable.
Equation (2.1), the accepted DoubleLex equivalence C-045, then gives that
the exact parent \(F\) is not satisfiable.

Suppose for contradiction that a connected graph \(G\) satisfies (3.1).
The accepted parameter chain and equality collapse C-001--C-002 give

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=4<\theta(G).
\]

The exact graph-to-formula theorem C-037 says that, after relabeling one
maximum independent four-set as the anchor and sorting the eight outer
labels, \(G\) extends to a satisfying assignment of \(F\).  This
contradicts UNSAT of \(F\).  \(\square\)

The converse direction embedded in C-037 is also why this is a complete
connected-lane exclusion: no connected parameter-four counterexample is
lost through anchoring, outer sorting, the complete coloring bank, or the
one-guard encoding.

### Role of C-043 and C-044

C-043 and C-044 are consistent with, but not needed for, the short
whole-formula implication above:

- C-043 proves that all eight `1***` parent cubes are logically UNSAT.
- C-044 proves that parent satisfiability is represented, up to the accepted
  anchor/outer action, by the four canonical leaves `0000`, `0001`, `0011`,
  and `0111`.  The other four `0***` leaves are orbit-redundant, not
  individually certified UNSAT by C-044.
- C-045 selects the same four possible first rows while additionally sorting
  the complete anchor columns.

A strict refutation of the whole exact DoubleLex formula would therefore
remove the need for four separate leaf certificates.  After (2.1) transfers
UNSAT back to \(F\), every parent cube is semantically UNSAT as a consequence.
This does not retroactively turn pending leaf-production records into
individually checked certificates.

## 4. Exact disconnected parameter-four bookkeeping

The connected conclusion does not automatically cover disconnected graphs.
The missing case has a particularly narrow exact form.

**Lemma.**  A disconnected 12-vertex graph \(G\) satisfies

\[
\gamma(G)=\gamma^\infty(G)=4<\theta(G)
\tag{4.1}
\]

if and only if

\[
G=Q\mathbin{\dot\cup}K_t
\tag{4.2}
\]

for some \(t\geq1\), where \(Q\) is a connected counterexample of order
\(12-t\) with

\[
\gamma(Q)=\gamma^\infty(Q)=3<\theta(Q).
\tag{4.3}
\]

**Proof.**  Let the components of \(G\) be \(G_i\), and put
\(a_i=\gamma(G_i)\), \(b_i=\gamma^\infty(G_i)\), and
\(c_i=\theta(G_i)\).  C-003 gives additivity of all three parameters.
Since \(a_i\leq b_i\) termwise and
\(\sum_i a_i=\sum_i b_i=4\), every component has \(a_i=b_i\).  Since
\(\sum_i c_i>4\), some component \(Q\) has
\(a_Q=b_Q<c_Q\).  It is a connected counterexample, so C-006 gives
\(a_Q\geq3\).

If \(a_Q=4\), no domination budget remains for another nonempty component,
contrary to disconnectedness.  Hence \(a_Q=3\).  All remaining components
together have domination number one, so there is exactly one of them, say
\(R\), and \(\gamma(R)=\gamma^\infty(R)=1\).  Equality collapse gives
\(\alpha(R)=1\), so the nonempty simple graph \(R\) is complete:
\(R=K_t\).  This proves (4.2)--(4.3).

Conversely, \(\gamma(K_t)=\gamma^\infty(K_t)=\theta(K_t)=1\).
Additivity applied to (4.2)--(4.3) gives (4.1).  \(\square\)

Thus the minimal extra evidence needed to extend the conditional connected
result to the complete order-12 parameter-four slice is:

> exclusion of connected parameter-three counterexamples on every order at
> most 11.

The campaign already has independently certified complete connected
coverage through order 9 (C-011 and C-016).  Relative to that accepted
coverage, the only still-needed cases are connected \((10,3)\) and
\((11,3)\).  A strict exhaustive certificate for those two cases, or a
mathematical theorem implying their absence, is sufficient.

### Published result versus campaign certificate

MacGillivray--Mynhardt--Virgile (2022) explicitly report, after their
computer search, that there is no counterexample of order at most 11.  If
that published exhaustive-computation result is accepted as a premise, it
is stronger than the two missing parameter-three exclusions and therefore,
together with the conditional theorem in Section 3, yields:

> No finite simple graph \(G\) of order 12, connected or disconnected,
> satisfies \(\gamma(G)=\gamma^\infty(G)=4<\theta(G)\).

The campaign's present stronger certificate standard does not independently
reproduce the published coverage at orders 10 and 11.  Its C-007 check
recomputes all parameters for the 56 graph strings listed in MMV Table 9 and
finds no counterexample among them.  It does **not** independently prove
that the published search omitted no other graph.  The literature audit
likewise records that no source-code archive, raw case manifest, solver log,
or proof certificate for the original exhaustive run was found.  Therefore:

- the published theorem can be used if a paper-level computational premise
  is allowed;
- C-007 alone cannot be upgraded into exhaustive order-10/11 coverage; and
- a strictly campaign-certified disconnected \((12,4)\) result still needs
  the two missing connected parameter-three cases above.

## 5. What is required for an order-12 frontier

For a connected order-12 counterexample with common parameter \(k\):

- C-006 gives \(k\geq3\);
- C-036 gives \(12\geq2k+1\), hence \(k\leq5\);
- C-035 excludes \(k=3\);
- the strict DoubleLex premise would exclude \(k=4\); and
- connected \(k=5\) remains open.

Consequently, even after strict DoubleLex UNSAT, an all-parameter
order-12 claim requires a sound exclusion of the connected \((12,5)\)
lane.

Disconnected order-12 counterexamples require a separate lower-order
premise via C-003.  There are two evidentiary versions:

1. If the published MMV no-counterexample-through-11 result is accepted,
   it excludes every disconnected order-12 counterexample component.  In
   that setting, after strict DoubleLex UNSAT, only the connected
   \((12,5)\) exclusion is additionally needed for an exact-order-12 (and
   hence through-order-12) frontier.
2. For a strictly campaign-certified frontier, complete connected coverage
   is currently certified only through order 9.  In addition to the
   connected \((12,5)\) exclusion, strict lower-order evidence is needed at
   orders 10 and 11.  Using C-006 and C-036, the potentially relevant
   missing lanes are
   \[
   (10,3),\ (10,4),\ (11,3),\ (11,4),\ (11,5).
   \]
   Exhaustive all-parameter coverage of connected graphs at orders 10 and
   11 is an equivalent, simpler gate.

No implication in this review addresses order 13 or higher.

## 6. Reusable conditional statements with no scope inflation

### Connected statement

> Let \(D\) be the exact 18,381-variable, 115,507-clause DIMACS formula
> with SHA-256
> `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`.
> If an independently accepted strict refutation proves \(D\) UNSAT, then
> there is no connected finite simple graph \(G\) on 12 vertices satisfying
> \(\gamma(G)=\gamma^\infty(G)=4<\theta(G)\).

### All-graph parameter-four statement

> Under the same strict UNSAT premise, and additionally assuming that no
> connected parameter-three counterexample has order at most 11, there is
> no finite simple graph \(G\) on 12 vertices satisfying
> \(\gamma(G)=\gamma^\infty(G)=4<\theta(G)\).

### Order-12 frontier statement

> Under the same strict UNSAT premise, additionally assuming (i) no
> counterexample has order at most 11 and (ii) no connected order-12
> counterexample has common parameter five, no finite simple graph of order
> at most 12 is a counterexample to the \(\gamma\)--\(\theta\) conjecture.

The lower-order premise in the last statement may be supplied either by
explicit acceptance of the published MMV computation or by a new
campaign-standard strict coverage package; those are different evidentiary
claims and should be labeled accordingly.

## 7. Exact byte ledger

The audit used the following exact accepted or status-recording bytes.

| artifact | SHA-256 |
|---|---|
| `CLAIMS.md` | `57b9953b668ab60ec89389f77b2ff6a225750e86d2641b4ea23397bb23f321ef` |
| `math/reductions.md` | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| `reviews/reductions_hostile_review.md` | `6798b33ad14adc660b69792ee74ed31be4afeb5c2bab4659b29d7b650090c159` |
| `math/lemmas/half_order_exclusion.md` | `5d5e054305d97bf8e40f84073abd5236c6d726d66205b5e309ccfe39dd7d5f50` |
| `reviews/half_order_exclusion_hostile_review.md` | `41d76e6d5295db5924d3bc2b0181ac42519c4592fa6b071dbdd8c28c817b5aa2` |
| `math/lemmas/order12_k3_exclusion.md` | `b6010d6f365a62845e24666603f6417d87f14c37876e3406dc2a7c6b6ee91ae4` |
| `results/order12_k3_exclusion_acceptance.json` | `f6224392eed348519ab898eaccfe96d223f874b280165cc49d48d3f587dbf2a3` |
| `math/lemmas/order12_k4_synthesis_target.md` | `5421357c5095113ac598afa22fa5a4e3623ef19d3c3a7a348b6c6c9a29945671` |
| `reviews/order12_k4_synthesis_target_hostile_review.md` | `119b9038b160cf9e85f56056578a3b33decf08c83cd40df071e89f35be1fea35` |
| `math/lemmas/order12_k4_minimum_signature.md` | `d87e2d3feffb5d93aa0a132289adb166bee27ef6f92526701a28cc988aaf215a` |
| `reviews/order12_k4_minimum_signature_hostile_review.md` | `00292a202b3290f03640f0409caccc02ec8f4dacbe49d273879146fbf271f2a0` |
| `math/lemmas/order12_k4_anchor_signature_symmetry.md` | `11d6fe9790083dcaecb196f1f175712b02e2bdfde5003454509ab3c6ee369acc` |
| `reviews/order12_k4_anchor_signature_symmetry_hostile_review.md` | `20e7168cfafe5da38d03c1ce31ecaa9618a90d2262c17f3c755e50bf27fc04c4` |
| `math/lemmas/order12_k4_doublelex.md` | `d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76` |
| `reviews/order12_k4_doublelex_hostile_review.md` | `4cf3c5012a8b0ecfdcbad82c0fd2c283c2aebbd3396eaba9b232902956f86d8f` |
| parent `instance.cnf` | `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac` |
| parent `manifest.json` | `621a0878c117dc8b4d6dbd0ba14c8402a8c24e8339d2f85cb23d61ffd74fbb61` |
| DoubleLex `instance.cnf` | `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7` |
| DoubleLex `manifest.json` | `4ca0b1d43c145acf35f7545b7a85e5d0aafa62e7279c120212455985312cba96` |
| `literature/sources/mmv2022.pdf` | `e1a5c6bb4fb4767c3d91a5e848872d26d97d3f0df284142a1b885ad720a20edf` |
| `literature/sources/mmv2022_src/EternalDomination.tex` | `e77618dcf06b4e65d6b622e993eed4307238de49d4f395da920044bb6dfd9a45` |
| `literature/status.md` | `61ae2e2a67991bef928894a09ee452196d2834035934456b262cc983f75ba9c4` |
| `results/mmv2022_summary.md` | `0c91027e7a013a532732ffcd4d9b0cd96d765e25e13e7b203df5cbacabe19cc5` |
| `instances/mmv2022_table9.csv` | `801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d` |
| `results/mmv2022_parameters.csv` | `ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6` |
| C-016 aggregate `results/logs/unlabeled-n09-all.json` | `547594bf981c627a969f7661d695af9cd2121e8e71ed3ca42833ce898b2b1021` |

The C-011 order-1-through-8 log hashes, in order, are:

```text
n01 6964f0cbd6017f49412520257ed0fac15fd43619f5ea9ebf897bf3903fb53420
n02 b1a31245382db8f30092fd9b77c8e816ae378c02a64c4627bf0cd099e84c5c54
n03 e82cf1d70708ac022ba4a9c3d1c0dabb2c048ab22b4fa4fc666e4331dfcb8264
n04 315dd975ed95ed2201e7d62f286fec6b36bf153912949ae3a0304500dd3eac26
n05 83a4b531479ea631e0afdff21ae3ccee38440c3f0ec7085ec6a871439fe93dc9
n06 ff702b81288e28d149b3ea0701f01bc994dd3c7930966d0784de7739e4a79b36
n07 8fcdccdcdc016b4ff24abe9f6d0d6122143187c4cf69a99ee213072335a02183
n08 7da35f567387feed750c6fbce63aeb4a5bfcf88b511bbe83928c2162a26e6ad2
```

These hashes identify the evidence inspected for this implication audit.
They do not incorporate or endorse any pending DoubleLex proof artifact.
