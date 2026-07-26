# Hostile review: recursive online-kernel certificates and the K3 measurement

Date: 2026-07-25 17:33 PDT

## Verdict

**ACCEPTED.**

The recursive failure/survival certificate theorem, the forced
maximum-independent-state obstruction, the strict \(K_2/K_3\) example on
\(C_{15}\), and the finite measurement on the recorded edge-toggle family
are correct under the stated one-guard-moves model.

An independent verifier imported no campaign module, used frozensets rather
than the author's bit masks, replayed all 518 recursive failure trees, and
recomputed the complete kernel profile of every one of the 8,587 source
targets.  It reproduced every population distribution and compared all
64,893 selected configuration ranks with the earlier third-audit trace.

Severity census:

| Severity | Count | Disposition |
|---|---:|---|
| Critical | 0 | none |
| High | 0 | none |
| Medium | 0 | none |
| Low | 1 | auxiliary self-reparser scope note below |

The low finding does not affect the frozen evidence: the independent hostile
verifier supplies the omitted cross-file coverage checks.

## Frozen hashes

| Artifact | SHA-256 |
|---|---|
| `src/search/three_step_kernel.py` | `e65102358dbfb5a7ab4e5cfe55907e6c583def32c95ed10e50efa49c5271b6fd` |
| `tests/test_three_step_kernel.py` | `76044cc09946098abd00467a5efc2f19c802836bea3511cd51587d798476205a` |
| `results/three_step_kernel_measurement.json` | `1369c38a696b9d1d1c5c4c0aefdf823ae0bda143c25c30ebe7335ab263b41c12` |
| `certificates/k3_three_step_edge_toggle.ndjson` | `74d20dd736cf8b962b79e235b1fff77df1f065df8d698913c4811d1cd18b349b` |
| `certificates/c15_k2_not_k3.json` | `e89df4aaf127f8f3069c40d6a7dc56830cb36c16fd0417e52a9e48162fdfba41` |
| `math/lemmas/three_step_forced_obstruction.md` | `a0fa3a28269a30a4cf8930d3c72ccb83b8d04890fa8695d45d56de59cec14fed` |
| input edge-toggle ledger | `a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319` |
| input third-audit trace | `b31eee468a8a45e0534fece7b54cb142ff126fb1f9155db5bbea98acaa948435` |
| independent hostile probe | `5e54ed829ffd83702cfa16d419d15da6776db5d766f3e04c7e78903e88a5ff56` |
| hostile probe log | `51c6ce83f16b57bab77990399541256d14ba9124e92349787eee0328d5564167` |

All six author-artifact hashes matched the audit assignment before any
inspection or execution.  The author artifacts were not edited.

## Mathematical audit

### Kernel indexing and online quantifiers

Let \(\mathcal C_k\) be the dominating \(k\)-sets and let

\[
\Phi(\mathcal X)=\{D\in\mathcal C_k:
  \forall r\notin D\ \exists u\in D\cap N(r),\
  D-u+r\in\mathcal X\}.
\]

With \(\mathcal K_0=\mathcal C_k\) and
\(\mathcal K_{h+1}=\Phi(\mathcal K_h)\), membership in \(\mathcal K_h\)
means survival of the next \(h\) adaptively revealed attacks:

\[
\forall r_1\exists u_1\;\forall r_2\exists u_2\;\cdots\;
\forall r_h\exists u_h.
\]

The indexing in the note, code, certificates, and result is consistent:

- \(K_0\) tests only domination;
- \(K_1\) tests one attack and response;
- \(K_2\) tests two online plies; and
- deletion rank \(h\) is the least \(h\) for which a state is absent from
  \(K_h\).

The operator is monotone.  Since \(K_1\subseteq K_0\), induction gives
\(K_{h+1}\subseteq K_h\).  On a finite configuration space the sequence
stabilizes, and its stable value is the greatest eternal \(k\)-family.  No
offline choice of an earlier guard after seeing a later attack occurs.

### Recursive certificates

For a dominating root at positive horizon, nonmembership has the exact dual
form

\[
D\notin K_h
\iff
\exists r\notin D\ \forall u\in D\cap N(r):
D-u+r\notin K_{h-1}.
\]

Thus a failure node must name one unoccupied attack and contain a child for
every adjacent occupied guard.  The child is the configuration obtained by
removing that guard and adding the attacked vertex, at horizon one less.  A
non-dominating child may terminate early with a vertex missed by its closed
neighborhood.  At horizon zero, such a terminal is exactly a proof of
nonmembership in \(K_0\).

The survival certificate is the dual:

- the root and every recursively retained successor dominate;
- every unoccupied attack occurs exactly once; and
- one occupied adjacent guard and one exact successor are supplied for each
  attack.

Induction on \(h\) proves both soundness and completeness.  Universal
branching is not merely asserted: both the author checker and the independent
checker reconstruct the complete set \(D\cap N(r)\) and require exact equality
with the branch guards.

Every move checked in the frozen artifacts therefore:

1. attacks an unoccupied vertex;
2. removes exactly one occupied guard;
3. moves that guard along an edge to the attacked vertex; and
4. either reaches the required lower-horizon certificate or exposes a
   genuinely non-dominating successor.

### Forced maximum independent state

Suppose an eternal family has \(k\) guards and \(S\) is an independent
\(k\)-set.  Starting at any family state, attack an unoccupied vertex of
\(S\).  A guard already on \(S\) cannot respond because \(S\) is independent,
so every response moves a guard from outside \(S\) into \(S\).  The quantity
\(|D\cap S|\) increases by exactly one.  Repeating reaches \(S\), which must
therefore belong to every eternal \(k\)-family.

When \(\alpha(G)=k\), a finite failure certificate rooted at one maximum
independent \(S\) rules out every eternal \(k\)-family.  Together with
\(\alpha(G)\leq\gamma^\infty(G)\), this gives
\(\gamma^\infty(G)\geq k+1\).  This proves Theorem 2 without assuming the
conjecture or any equivalent statement.

## Independent replay

`reviews/three_step_kernel_hostile_probe.py` imports no campaign Python
module.  It uses:

- tuple-of-frozenset adjacency rather than adjacency bit rows;
- frozenset guard configurations rather than integer masks;
- a fresh graph6 parser;
- fresh domination, independence, clique-partition, and kernel routines; and
- fresh recursive JSON checkers for failure and survival trees.

The replay completed in 13.095 seconds.  It rejected immediately on any
hash, schema, quantifier, move, witness, coverage, or count discrepancy.

### \(C_{15}\) strictness

The hostile parser reconstructed the stored graph as the labeled 15-cycle.
It independently obtained:

\[
\alpha(C_{15})=7,\qquad
(|K_0|,|K_1|,|K_2|,|K_3|)=(765,120,15,0).
\]

The 15 maximum independent states are exactly the 15 rotations of
\(\{0,2,4,6,8,10,12\}\).  All 15 lie in \(K_2\), and none lies in \(K_3\).

The positive \(K_2\) tree has 73 nodes and 64 horizon-zero leaves and gives
one legal response for every first and second attack.  The negative \(K_3\)
tree has eight nodes and four non-domination leaves.  Independent replay
confirmed the readable branch description in the note, including attack
\(1\), the complete guards \(0,2\), and the subsequent attacks \(7,3,11\).
Consequently failure at the third ply is strictly stronger than failure at
the second ply.

### Complete source-population recomputation

The input ledger contains 19,136 unique graph6 records.  Exactly 8,587 rows
have both stored evaluators reporting

\[
\gamma=\alpha=3,\qquad\gamma^\infty=\theta=4.
\]

For every one of these 8,587 rows, the hostile probe independently checked
connectedness, order, size, \(\gamma=3\), \(\alpha=3\), \(\theta=4\), and
empty stable three-guard kernel.  Hence their stored
\(\gamma^\infty=4\) also follows independently from the empty three-kernel
and the clique-cover upper bound.

The earliest forced-state deletion ranks over the full target population
were:

| Earliest rank | Graphs |
|---:|---:|
| 1 | 4,169 |
| 2 | 3,892 |
| 3 | 518 |
| 5 | 7 |
| 6 | 1 |

Thus exactly 526 rows survive \(K_2\).  On those 526 rows the complete
distributions were reproduced:

| Statistic | Distribution |
|---|---|
| earliest forced rank | \(3:518,\ 5:7,\ 6:1\) |
| latest forced rank | \(3:225,\ 4:291,\ 5:2,\ 6:7,\ 7:1\) |
| all 6,375 forced triples | \(3:5283,\ 4:1012,\ 5:19,\ 6:55,\ 7:6\) |
| first empty full-kernel level | \(3:185,\ 4:331,\ 5:2,\ 6:7,\ 7:1\) |

The joint distribution also matched exactly:

\[
(3,3,3):185,\ (3,3,4):40,\ (3,4,4):291,\ (3,5,5):2,\
(5,6,6):7,\ (6,7,7):1.
\]

The probe streamed all 19,136 rows of the independent third-audit trace and
verified its row-stream digest
`fc929585dd5b9096dc9dca262093d2fc4f02e5784fc66f0e8ab39ec5f23336a3`.
For the 526 selected rows, all 64,893 dominating-triple deletion ranks
matched the fresh kernel profiles.

### Recursive-certificate population

All 518 serialized \(K_3\)-failure trees were strictly parsed and replayed.
For every row the hostile checker independently verified:

- the graph and ledger-row identity;
- exact \(\alpha=3\);
- a maximum independent root that survives \(K_2\) and first fails at
  \(K_3\);
- exact root horizon and guard count;
- every attack, every adjacent-guard branch, every successor, and every
  terminal witness; and
- the stored node and leaf counts.

The totals were 5,540 nodes, 3,174 leaves, and at most 17 nodes in one
certificate.  The row-stream digest was
`f5f876ebe26dcac0bd14af57f74921e4d95d82753f94a567844de18ecab25468`.

The 518 certificate indices and eight deep-row indices are disjoint and
their union is exactly the independently recomputed 526-row \(K_2\)
survivor set.  The eight retained rows have the stated seven rank-five and
one rank-six earliest losses.  The deepest graph `Kun_w{vRrblV` has kernel
sizes

\[
147,143,136,128,119,93,28,0.
\]

This closes the coverage loop for the delimited derived family.  It does not
turn that family into an enumeration of all graphs of order 11 or 12.

## Source, regeneration, and tamper audit

All seven author tests passed in 0.146 seconds.  Their exhaustive small-graph
test compares the recursive finder and checker against direct kernels for
every labeled graph through order four, every positive guard count, every
state, and horizons zero through three.

The production program was rerun with temporary output paths.  It
deterministically regenerated both decisive artifacts byte for byte:

- recursive stream:
  `74d20dd736cf8b962b79e235b1fff77df1f065df8d698913c4811d1cd18b349b`;
- \(C_{15}\) witness:
  `e89df4aaf127f8f3069c40d6a7dc56830cb36c16fd0417e52a9e48162fdfba41`.

The hostile checker submitted 14 decisive malformed/tampered cases,
including Boolean guard counts, nonmaximum roots, wrong horizons, occupied
attacks, omitted universal branches, malformed guards, incorrect
successors, false undominated witnesses, extra fields, duplicate JSON keys,
missing survival attacks, and illegal survival responses.  All 14 were
rejected.

The measurement binds the source, input ledger, earlier trace, recursive
stream, and \(C_{15}\) witness by SHA-256.  The hostile verifier checks each
binding against the actual bytes before mathematical replay.

### Low finding: scope of the author's internal stream reparser

The private author helper `_verify_recursive_file` validates each graph and
recursive tree and validates the header/trailer digests, but by itself it
does not reopen the ledger to check that `ledger_row_index` names the stored
graph.  It also does not explicitly equate each row certificate's guard
count and horizon to the header values.  This means that helper is a
same-run serialization check, not a complete cross-artifact coverage
auditor.

There is no defect in the frozen stream: the independent hostile verifier
does reopen the ledger, enforces the row/header equalities, checks the
518-plus-8 partition, and rejects those mismatches.  The recommendation is
to retain the hostile verifier as part of the published verification path
(or later harden the private helper if it is promoted as a standalone
checker).

## Scope and overclaim audit

The note expressly says:

- no general novelty claim is made for finite-horizon kernels;
- the 518 certificates concern only the recorded edge-toggle-derived
  population;
- eight deeper rows remain;
- the result is not exhaustive at order 11 or 12;
- no global lower bound is raised; and
- the \(\gamma\)--\(\theta\) conjecture is not resolved.

Those limitations match the evidence.  The universal content is confined to
the elementary recursive-certificate equivalence and forced-state theorem;
the numerical content is correctly delimited as a certificate-backed finite
measurement.

## Final assessment

No critical, high, or medium issue remains.  The proof and frozen
certificates are mathematically sound, the population is independently
covered, and the claims are appropriately scoped.  **ACCEPTED.**
