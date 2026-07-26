# Hostile coverage review of the order-12, parameter-three exclusion chain

## Verdict

**`ACCEPT_COMPLETE_ORDER12_K3_EXCLUSION`.**

The proof in `math/lemmas/order12_k3_exclusion.md` correctly establishes
\[
  \nexists G,\ |V(G)|=12,\quad
  \gamma(G)=\gamma^\infty(G)=3<\theta(G).
\]
Its final premise \(P_5\) is certified unsatisfiability of the exact
\(F_5\land S\) CNF with SHA-256
`c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`.

No mathematical gap was found in the equality collapse, disconnected
reduction, SPGT split, hub-free and length reductions, branch composition,
or graph-to-\(F_5\land S\) implication.

The independent clean-room post-run review now has the exact activating
primary verdict

`ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`

and is backed by a deterministic probe and canonical log.  Therefore
\(P_5\) is active, the C5 branch is certified empty, and composition with
C-017, C-028, C-030, C-031, and C-033 certifies the complete order-12,
parameter-three slice.

This review assigns `CERTIFIED-FINITE`, not `PROVED`, because the decisive
branch exclusions use exact finite proof certificates.

The reviewed theorem-note bytes have SHA-256
`b6010d6f365a62845e24666603f6417d87f14c37876e3406dc2a7c6b6ee91ae4`.

Review date: 2026-07-25 PDT.

## 1. Frozen premise and artifact audit

### Exact Git roles

The source/run gate and the artifact freeze are different commits and are
not interchangeable:

| Role | Commit | Audit meaning |
|---|---|---|
| source/run gate | `6f3ef0a0970b7214c34018fe32ea1ceeb5764d17` | exact audited runner/runtime-source revision named by `run_config.json`; it reports `runtime_sources_match_head=true` |
| provisional artifact freeze | `dff45f4239e4acabc461533a0a213beec18ec56d` | later commit that freezes the 12 run artifacts byte-for-byte |

Direct Git-object reads at the artifact-freeze commit reproduce outcome
SHA-256
`ea2ea36321a786aa40aff1e68587474bbdba5402abc800b1a0816d65b6df8df4`
and addition-only proof SHA-256
`c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3`.
A direct Git-object read of the production source at the source/run-gate
commit gives SHA-256
`02e8a13d806593017071ca0ad89680ece8c947e0c24d7579e6a779bc25ba044f`.

The later artifact-freeze commit is not falsely described as the revision
under which the solver executed.  Conversely, the source/run-gate commit
does not contain the later proof artifacts.  Neither commit relation is used
as a logical proof of UNSAT; it is provenance that the independent post-run
auditor must bind.

### Accepted mathematical dependencies

Fresh SHA-256 calculations give:

| Premise | Artifact | SHA-256 | Audit result |
|---|---|---|---|
| parameter chain, additivity, minimum parameter | `math/reductions.md` | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` | accepted |
| odd-wheel obstruction and order-12 split, C-014 | `math/lemmas/k3_structural_day1.md` | `00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e` | accepted |
| C-014 hostile review | `reviews/k3_structural_hostile_review.md` | `f2b0ce3d551576d5050bb03c7e8699bdffdb3ae35fbf5d3cf4b28c4e4ab270bc` | `ACCEPT` |
| antihole elimination, C-017 | `math/lemmas/k3_antihole_elimination.md` | `9e572203c09e082c3cbdfc0cdae8e4166007af3f909b73f7d8d2e196f04ddc4f` | accepted |
| C-017 hostile review | `reviews/k3_antihole_hostile_review.md` | `7837fb360328533ea58a31d1a0eb60ef279a67d1e610144eb5206661ef38f5e3` | `ACCEPT without correction` |
| C-028 graph implication | `math/lemmas/hole9_template_exclusion.md` | `4305dcfc170f665d0c97b5d4601c3dd226099b61e11a2ad28a15fc66ee36c1f2` | accepted |
| C-028 acceptance record | `results/synthesis_k3_hole9_orphan_recovery_acceptance.json` | `ebede11b90e6e0b73d75f57c7706ba2e62e699281fcd8c15a208886dd53db291` | accepted |
| C-028 hostile graph review | `reviews/hole9_template_exclusion_hostile_review.md` | `e17707945f3420c4ba2ecb6b3056b14789e2648e12e4c641772dfb7cee6452b7` | `ACCEPT without reservation` |
| C-030 exact-CNF/proof review | `reviews/hole7_addition_only_hostile_review.md` | `b904fcec9df16eff06640f36241a7589e1686777a57b7f32f9825832a8cecaa2` | `ACCEPT ... without mathematical reservation` |
| signature theorem, C-031 | `math/lemmas/hole5_signature_symmetry.md` | `8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8` | accepted |
| C-031 mathematical hostile review | `reviews/hole5_signature_symmetry_hostile_review.md` | `169b99e083fe2079b3957de3095591142162aca76a10b42f9bb61266775ef223` | accepts equisatisfiability |
| C-031 implementation binding addendum | `reviews/hole5_signature_symmetry_implementation_binding_addendum.md` | `0dd77b3d9012cbed92f402224f6f6f737f5464f16ca39856df74a97fc65d3cc0` | accepts exact committed bytes |
| exact signature-package review | `reviews/hole5_signature_package_hostile_review.md` | `b675ed1ba1e83a37069af4f3f526a98b3c627d1133300b1e5764fe933fa7b5ed` | accepts formula infrastructure |
| conditional C5 realization, C-033 | `math/lemmas/hole5_template_exclusion_conditional.md` | `dee226088d17c2564da406f4e675a71f2d160cc678805e360e2ef51398b7e26b` | proved conditional |
| C-033 hostile review | `reviews/hole5_template_exclusion_conditional_hostile_review.md` | `c63613befffa7bd506691d6e8cdc48bd5dd72d3de947cec5834cdbf484b62405` | `ACCEPT_CONDITIONAL_REALIZATION_ONLY` |

The Strong Perfect Graph Theorem is the one external theorem used by the
structural split.  Both C-014 and C-017 state this dependence explicitly.
No unproved graph-class restriction is used.

### Already accepted finite branch certificates

For C-028 (`hole9`), the decisive exact formula has SHA-256
`2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d`
and the addition-only RUP proof has SHA-256
`24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab`.
The acceptance record and two hostile reviews above bind the formula,
proof, graph implication, and standalone replay.  The historical CEGAR
checkpoint remains nonterminal and is not used.

For C-030 (`hole7`), fresh hashes are:

| Artifact | SHA-256 |
|---|---|
| exact 6,886-variable, 21,718-clause CNF | `6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7` |
| v2 certificate record | `c38002e16190065ed13453f9013a294f013846b5ed3651fde64aaa927e2f888e` |
| 284,317-addition RUP proof | `e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9` |

The C-030 hostile audit reports two pinned, strict, warning-free
`-I -f -W -U` replays, exit zero, exactly one `s VERIFIED`, and zero RAT
lemmas.  It separately audits graph-to-CNF coverage.  Therefore the C7 and
C9 branches need no new premise here.

### Exact certified C5 bytes

The certified C5 stack hashes as follows:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| exact \(F_5\land S\) CNF | 754,323 | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |
| raw binary proof | 12,524,020 | `c17ed1ee2782270ed861462ae7bdd94420a2079edf419a7d778d7096a67d1be4` |
| addition-only binary proof | 6,337,621 | `c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3` |
| runner-generated certificate record | 4,200 | `f54d7bf8a50f24e3a5084442d84f07548a60401faca8ec18bfd07f24f0e337e8` |
| runner-generated outcome | — | `ea2ea36321a786aa40aff1e68587474bbdba5402abc800b1a0816d65b6df8df4` |
| parser transcript | — | `435ac813fbc0a345816256397bccf9a3f0dc662f3e4a338cc3cc31bd25c19fe1` |
| checker stdout | 482 | `582074fe80efc122bef5586bc9768e32dfbb3a7bb5758f04b5fe23d0862b6515` |
| checker stderr | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| run configuration | — | `6d899e212d2f349b48eefad5037ea007981a331b7e581966165ae861c741221b` |
| pinned DRAT-trim binary | — | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |

The parser transcript reports:

- 247,981 additions and 245,439 deletions in the raw proof;
- preservation of every addition byte and its order;
- 247,981 records and no deletions in the addition-only proof;
- maximum variable 6,886;
- exactly one empty addition, at final record 247,981; and
- 4,372,774 addition literals.

The installed checker transcript says that binary forward verification read
the exact 6,337,621-byte proof against a formula with 6,886 variables and
23,968 clauses, used 10,912,555 resolution steps, reported zero RAT lemmas,
and ended with `s VERIFIED`; stderr is empty.

These runner-generated facts did not by themselves establish \(P_5\).  The
certificate file itself says `NO_STANDALONE_MATHEMATICAL_CLAIM`.  The
independent post-run audit below rehashed and reparsed the bytes and reran the
checker rather than trusting those records.

## 2. Exact activation test for \(P_5\): passed

The final post-run hostile stack is:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `reviews/hole5_binary_production_postrun_hostile_probe.py` | 61,778 | `e480f7a27b5e5424b6ba7507a85a57144949f974b37351ee0872cca1ba8a7937` |
| `reviews/hole5_binary_production_postrun_hostile_probe_log.json` | 24,943 | `bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5` |
| `reviews/hole5_binary_production_postrun_hostile_review.md` | 11,140 | `060c65bbc5b08f562289dcf43e36924d34a0ae90ae2cc72c895c59b7eaf916a3` |

Every required activation check passed:

1. The three hostile artifacts above are frozen and hash-bound.
2. The independent probe imports neither the production runner nor its
   parsing or transition core as proof evidence.
3. It reconstructs or independently checks the DIMACS header and body and
   binds the exact CNF SHA-256
   `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`.
4. It canonically parses the raw and addition-only binary streams, checks the
   counts above, and confirms that the latter is exactly the raw addition
   stream in order with every deletion removed.
5. It independently reruns the pinned checker on the exact CNF and
   addition-only proof using binary input, forward verification,
   warning-fatal mode, and RUP-only mode.
6. The rerun exits zero, has empty stderr, emits exactly one `s VERIFIED`,
   and reports zero RAT lemmas.  Formula, proof, and checker hashes remain
   unchanged before and after the rerun.
7. The review's primary verdict is exactly
   `ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`, and it expressly accepts the
   certificate as filling the missing premise in C-033 rather than merely
   accepting runner engineering.

The probe ran twice after normalizing a randomized temporary output path;
both final full runs, including fresh checker replay, produced byte-identical
canonical JSON.  The earlier nondeterministic draft log was deleted and is
not bound here.  No proof, formula, parser result, or checker result changed.

No case manifest is needed because this is one exact parent formula, not a
collection of cubes; the C-031 \(S_6\) theorem supplies the semantic coverage
of the strengthened parent.

## 3. Hostile audit of the mathematical implication

### Parameter normalization

The target hypothesis is
\(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\), not merely
well-coveredness or \(\alpha=\gamma^\infty\).  The accepted parameter chain
forces \(i(G)=\alpha(G)=3\).  Thus for \(H=\overline G\),
\[
 \omega(H)=3<\chi(H)=\theta(G).
\]
The complement and clique-cover directions are correct.

### No disconnectedness gap

Additivity gives equality
\(\gamma(G_j)=\gamma^\infty(G_j)\) on every component and a strict
\(\gamma^\infty(G_q)<\theta(G_q)\) on at least one component \(G_q\).
Thus \(G_q\) is a counterexample.  Its parameter is at least three by the
accepted minimum-parameter theorem.  Since all component domination numbers
are positive and sum to three, \(G_q\) is the only component.

This proves that every parameter-three counterexample is connected.  It is
not enough merely to cite “some connected counterexample exists,” because
that component might a priori have smaller order.  The domination-budget
argument closes exactly that gap and shows the original 12-vertex graph
itself is connected.

### Exhaustive structural split

SPGT applies to \(H\) because \(H\) itself has
\(\omega(H)<\chi(H)\).  C-017 excludes an induced
\(\overline{C_7}\) by induced-subgraph monotonicity and the proved
\(\gamma^\infty(C_7)=4\); a five-antihole is \(C_5\).  Hence \(H\) has an
odd hole.

C-014 forbids an outside hub, since a hub plus the odd hole is an induced
odd wheel.  The pair-common-neighbor property follows from
\(\gamma(G)=3\): a nondominating pair in \(G\) has an outside vertex
adjacent to neither endpoint in \(G\), hence to both in \(H\).  A rim edge
has no common rim neighbor.  If the hole had only one outside vertex, that
vertex would serve every rim edge and would be a hub.  Thus at least two
vertices are outside, and at order 12 the only possible odd-hole lengths are
5, 7, and 9.

The branches need not be disjoint.  Exhaustiveness plus an exclusion of each
branch is sufficient; overlap creates no omitted case and no double-counting
obligation.

### Branch scopes match

C-028 and C-030 each quantify connected 12-vertex graphs satisfying
\(\gamma=\alpha=\gamma^\infty=3<\theta\) and containing the respective
hub-free complement cycle.  Equality collapse supplies the displayed
\(\alpha=3\), and the preceding argument supplies connectedness and
hub-freeness.  Their universes therefore match the C9 and C7 branches
exactly.

For C5, C-033 has the slightly leaner hypothesis
\(\gamma=\gamma^\infty=3<\theta\), plus connectedness and the hub-free
induced \(C_5\).  It constructs a model of the retained \(F_5\), including
the nonempty family, domination, every unoccupied attack, one moving guard,
the legal \(G\)-edge, and the selected successor.  C-031 then transports the
entire assignment—not only graph-edge variables—under the outer \(S_6\)
action to a model of \(F_5\land S\).

The exact formula named by C-031 and C-033 has the same SHA-256 as the CNF
named in \(P_5\).  There is therefore no parent/leaf, strengthened/base,
ASCII/binary, or \(G/\overline G\) mismatch.

## 4. Variant, sign, and quantifier audit

- Attacks are quantified only over \(r\notin D\).
- A true move variable selects one \(u\in D\), replaces only \(u\) by \(r\),
  and requires \(ur\in E(G)\).
- Since edge variables encode \(H=\overline G\), the legal-move clause uses
  a negative \(H\)-edge literal.
- Every selected family state dominates, and every selected successor is
  another family state.
- The family-nonempty clause prevents a vacuous all-false strategy.
- Clique partitions of \(G\) are proper colorings of \(H\), so
  \(\theta(G)>3\) means \(\chi(H)>3\), which is the sign used by every
  coloring-bank clause.
- No all-guards-move, occupied-attack, total-domination, connected-eternal,
  or complement-coloring variant is imported.

## 5. Claim boundary

The passed activation test in Section 2 makes this chain support:

> **`CERTIFIED-FINITE`.**  No 12-vertex graph satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).

It does not support:

- no counterexample through order 12;
- exclusion of the order-12 \(k\ge4\) slices;
- exclusion at any larger order;
- a universal proof;
- a counterexample; or
- resolution of the \(\gamma\)--\(\theta\) conjecture.

No certificate or mathematical premise remains pending for this precisely
delimited finite slice.
