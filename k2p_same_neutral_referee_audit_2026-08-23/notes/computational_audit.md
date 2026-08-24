# Independent computational and finite-classification audit

Completed 2026-08-23. This report concerns the isolated project at
`isolated_handoff/materials/k2p_principal_d_plus_submission_referee`.
No file below `isolated_handoff/` was edited. Independent scripts are in
`scripts/computational/`; generated records and the disposable mutation copy
are in `outputs/computational/`.

## Bottom line

**Computational evidence: FAIL.** The high-volume finite ledgers have the
claimed sizes and satisfy their declared row, parent, transport, and ordering
contracts, but a load-bearing printed displayed-quartet lemma is false under
the article's declared Fourier convention. The release gate called an “exact
quartet replay” never evaluates the printed polynomial. Two semantic
mutations of the spectrum/coordinate convention leave that gate byte-for-byte
unchanged and returning PASS.

This is a false printed lemma and a missing algebraic replay, not presently a
counterexample to the uniformly relabelled central theorem. Replacing the
printed G/T coordinates by the equal C/T sector gives exactly the claimed
tree zero/sign pattern. The corrected theorem therefore remains plausible,
but the current proof and computational release do not validate it.

The independently reproduced census is a **ledger/domain/contract census**.
It rebuilds the literal primitive completion domains and raw-ID Cartesian
order, then streams and checks every submitted row. It does **not**
independently recompute every analytic classification predicate. Thus exact
counts below PASS as counts; the semantic exhaustiveness of the partition is
FAIL for quartet terminals and otherwise only as strong as the separately
listed certificate replays.

## Layer status

| Layer | Status | Strongest evidence | Exact remaining gap |
|---|---|---|---|
| Primitive core encodings and completion grammar | PASS relative to the declared five cores | Literal edge templates independently regenerated; source counts 2/6/4 and target counts 1120/2814/6138; every raw ID and lexicographic port permutation checked | The mathematical theorem that these five cores exhaust the claimed network class is a proof-layer premise, not independently reproved here |
| Raw generation and finite census | PASS as census/contract | Independent streaming replay of all 405,216 raw4, 2,946,240 theta2, 13,440 cycle-base, 536,364 cycle-full, 36,824 restoration, and 574,535 probe rows/parents | Analytic category predicates are not all independently regenerated |
| Canonicalization and graph equality | UNVERIFIED globally | Fresh incidence-graph replay passes all 196 feasible direct relation presentations: raw4 80, cycle-base 24, theta2 80, cycle-full 12 | No all-universe pairwise merge/split partition; not every restoration/probe graph transport was rebuilt by this audit |
| K2P map and printed polynomial coordinates | **FAIL** | Independent symbolic pullback, exact rational witness, and direct comparison with the low-level atlas | Printed G/T quartet separators contradict declared `(0,C,G,T)`, `(1,s,g,s)` convention |
| Symbolic rank upper bounds | PASS for symbolic-vs-sampled question | Code is coefficientwise polynomial/syzygy based; raw ID 97 independently rebuilt with exact source rank 13 and target rank 10 and both stored determinants | No second engine replay of all 4,379 upper-bound descriptors |
| Other direct polynomial certificates | UNVERIFIED independently | Submitted exact cubic/quartic/quintic and mutation replays inspected and quick suite passed | This audit did not independently recompute every polynomial family; quartet family is specifically FAIL |
| Restoration forest structure | PASS structurally; quartet sublayer FAIL | 997 canonical parents, 2,540 member roots, every child/parent/hash/transport reference, depth two, and exact census checked; 13 mutations freshly rejected | 36,006 quartet-labelled restoration children require corrected algebraic rebinding; all 4,986 target transports were not independently graph-matched here |
| Probe inventory/coherence | PASS structurally; quartet sublayer FAIL | All sites and Cartesian products checked; fresh 15-case semantic suite; submitted separate primitive-graph audit inspected | 539,024 quartet-labelled probe rows require corrected algebraic rebinding; this audit did not reconstruct all 67,741 exact graph transports itself |
| Weak-class sharpness | PASS | Independent audit reproduces graph/rooting properties, tensor equality, ranks 9/9, cherry determinant, and `4n-3` extension | None found in the claimed exact scope |
| Mutation coverage | **FAIL** | Broad raw/restoration/probe/domain suites freshly run; coordinate-convention mutation survives | Source↔target reversal, graph-parent reversal/complement pairing, sampled-engine substitution, and global canonicalizer collision attacks remain unrun |
| Release harness | Operational PASS; semantic **FAIL** | 21 commands actually invoked; nonzero exits stop PASS; optimized mode forbidden; fresh quick ledger PASS | Harness invokes the quartet-blind gate, so a false printed lemma can coexist with overall PASS |

## Finding C-1 — wrong Fourier character pair in the quartet separator

**Severity: proof-blocking and computational-completeness-blocking.**

The article declares order `(0,C,G,T)` and edge spectrum `(1,s,g,s)` at
`proof_compression_submission/article/main.tex:302-307`. Hence C and T are
the equal K2P sector. Nevertheless, `main.tex:416-450` defines

```text
F_A = q_GGGG - q_GGTT
G_B = q_GGGG - q_GGTT - q_GTTG + q_GTGT
```

and asserts both vanish on `A=12|34`, with the stated crossing-tree signs.
Direct use of the article's tree Fourier formula gives on `12|34`

```text
F_A = g1*g2*(g3*g4 - s3*s4),
```

which is not an identity. At the exact point `s=3/4`, `g=3/5` on all five
edges, all of `0<s<1`, `0<g<1`, `g>2s-1`, and `g>s^2` hold. The
inverse-transition entries are
`(f(0),f(C),f(G),f(T))=(31/40,1/10,1/40,1/10)`, so the witness is strictly
physical and strictly continuous-time. Exact values are:

| Tree | printed F | printed G | corrected F | corrected G |
|---|---:|---:|---:|---:|
| `12|34` | `-729/10000` | `-729/10000` | 0 | 0 |
| `13|24` | `-891/40000` | `567/20000` | `81/640` | `81/320` |
| `14|23` | `-891/40000` | `-729/10000` | `81/640` | 0 |

The corrected equal-sector formulas are

```text
q_CCCC - q_CCTT
q_CCCC - q_CCTT - q_CTTC + q_CTCT.
```

Their symbolic pullbacks have exactly the asserted zero/sign sets.

The executable low-level map agrees with the article's declared convention,
not the printed quartet formula:

- `package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py:206-209`
  swaps C=1 and T=3 and fixes G=2;
- `k2p_atlas_core.py:252-257` assigns XOR value 2 to the g sector and values
  1/3 to the s sector;
- the descriptor/evaluation code at `k2p_atlas_core.py:268-349` uses that
  dispatcher.

The nominal quartet replay is not algebraic.
`work/quartet_separation_closure/verify_quartet_logic.py:25-68` assumes the
abstract F/G zero sets and checks only the 21 unordered pairs of seven
nonempty topology subsets. Its `PROOF.md:8-29` repeats the false coordinate
formulas. Likewise,
`work/corrected_composite_ledgers/verify_corrected_composites_independent.py:122-169`
recomputes split sets and invariant names but no Fourier coordinate or
polynomial pullback. That verifier also loads the submitted atlas near
`:112-119`, so it is not independent of the decisive graph/map compiler.

The fresh semantic mutation record proves the blind spot. Changing the
declared spectrum or changing the printed polynomial labels leaves the
quartet verifier and certificate unchanged; both variants exit 0 with stdout
SHA-256
`646d2e0a881888c2e9a63f8a8f724c85b74f535c2737ce858ed354a0ef46c066`.
Mutation report:
`outputs/computational/quartet_gate_mutation/quartet_gate_blindness.json`,
SHA-256 `72a033e22826014cf260ae7e0d9766eb5feaab8406cf05fd2f1437dd9fbc76c0`,
payload `227b03cde7c2bcf746a3dc198122c324a0f4b7d8fe1a898632b2c1658d08a64b`.

### Downstream quartet-labelled layers

| Layer | Records using displayed-quartet terminal semantics |
|---|---:|
| Raw4 composite | 360,408 |
| Theta2 composite | 2,942,592 |
| Cycle full | 535,920 |
| Theta2 dummy closure | 760 = 504 + 256 |
| Global restoration | 36,006 = 35,758 + 248 |
| Probe one/two port | 539,024 = 27,758 + 511,266 |
| **Total across distinct layers** | **4,414,710** |

These rows feed the corrected-universe release, theorem-artifact item C02,
tree-of-blobs/topology direction, proper-containment exclusion,
reconstruction/genericity, and continuous-time transfer. Their graph counts
need not change if the uniform C/T correction is proved, but every algebraic
binding must be replayed and resealed.

## Finding C-2 — global canonicalizer exhaustiveness is not independently established

**Severity: computational-completeness gap, not an observed false merge.**

The submitted exact helper at `k2p_atlas_core.py:933-957` enumerates every
underlying graph triangle and forgets all three edge-head flags; it does not
itself test that the triangle has exactly two singly headed edges into one
common reticulation. Probe transport verification does check that ordinary
pattern at
`work/probe_coherence_corrected/verify_probe_coherence_corrected.py:95-123`.

The independent graph audit deliberately used the stricter predicate and
passed every direct claimed relation presentation available in the finite
layers:

- raw4: 80 presentations, comprising 26 isomorphic and 54 triangle
  presentations, covering all 55 graph terminal classes (20 isomorphism, 35
  triangle classes);
- cycle base: 24 presentations (8 isomorphism, 16 triangle);
- theta2: all 80 labelled-isomorphism presentations;
- cycle full: all 12 restored isomorphism presentations.

Thus 196 direct presentations PASS. This is not an exhaustive collision or
splitting audit over every graph pair in the millions of nonterminal rows,
nor a fresh graph reconstruction of every restoration/probe equality
transport. Global merge/split correctness remains UNVERIFIED.

Independent artifact:
`outputs/computational/independent_graph_relation_audit.json`, script SHA-256
`2380957fc742cf4186f8099e4c37a703c026fc1d9ab98543001d90879a46904e`,
output SHA-256
`a431ac1627b00dce9808333ca69037e603bc60e74d52224fdf41f0dd279f194e`,
payload `fd101d38cece24bff7ca843f9ceadc03be5c2fe31ad7dd0a35e465c0cf95327b`.

## Audit of the eleven code questions

1. **Primitive encodings, not topology names: PASS relative to the core list.**
   `k2p_atlas_core.py:9-41` gives literal arc/reticulation/sink/repair tuples;
   `:65-110` builds and validates directed graphs. Generation does not call
   the revoked rooted tree/sunlet oracle. The asserted core-completeness
   theorem remains mathematical input.

2. **Generate every raw relation exactly once before canonicalization: PASS as
   a Cartesian-domain statement.** The independent audit rebuilt all source,
   target, weak-composition, repair, sink-mask, and lexicographic permutation
   domains and checked raw IDs `0..N-1` with no omission/duplication. A fresh
   raw mutation suite rejected both an omitted and a duplicated row.

3. **Direction, dummy/incoming roles, ports, parents, boundaries: PASS for
   stored row contracts; UNVERIFIED for inheritance-complement semantics.**
   Every raw ID decodes to its stored source/target/permutation; every stored
   permutation is the exact expected lexicographic permutation. Restoration
   and probe parent/reference/order contracts pass. No explicit independent
   mutation reversed reticulation parent order with/without the corresponding
   inheritance complement.

4. **Canonicalizer merge/split: UNVERIFIED globally.** The 196 direct
   relation presentations pass a fresh stricter matcher. There is no
   exhaustive whole-universe collision/splitting partition. See C-2.

5. **Rank upper certificates are symbolic: PASS.**
   `work/rank_upper_certificates/syzygy_upper.py:1-20,53-112,153-169`
   constructs coefficientwise polynomial vector-field systems and exact
   ranks. `work/raw_ledger_audit/rank_upper_binding.py:186-346` binds all
   4,379 descriptors, including 75 exceptional representatives and their
   port transports. No sampled-point rank is used as a global upper bound.

6. **Polynomial coordinates match the printed Fourier maps: FAIL.** The
   implemented model map is internally consistent, but the printed quartet
   polynomial is not. See C-1.

7. **All 997 restoration obligations: PASS structurally.** Exactly 997
   canonical parents and 2,540 physical roots were distinguished; all
   36,568 first children, 256 second children, 36,824 edges, and 36,792 leaves
   have valid row hashes, parent references, Cartesian insertion sets, and
   terminal statuses. The forest has depth two and no missing continuation.
   The quartet-labelled subset still inherits C-1.

8. **Every probe site/relation: PASS structurally.** All 176 anchors, 2,206
   source and 2,206 target sites, 29,964 one-port rows, 2,107 equality
   survivors, 2,107 two-port parents, 544,571 two-port rows, 67,741 exact
   transports, and 4,379 parent restrictions were checked. Every registry
   reference resolves and every ordinary-triangle witness has the required
   headed-edge pattern. Independent graph replay of all transports was not
   repeated by this audit.

9. **Independent replayers: mixed result.** The submitted probe full audit
   implements a separate primitive-graph path and was freshly executed by the
   quick release. The corrected-composite verifier imports the same atlas.
   The quartet gate is purely abstract and misses the decisive algebra. This
   audit added separate literal generators, incidence matching, Fourier/Jacobian
   code, and exact pullbacks, but did not replay every analytic family.

10. **Authoritative/historical/revoked distinction: PASS operationally.**
    The release common code and mutation suite quarantine historical artifacts,
    reject rooted-oracle reintroduction, and bind promoted replacements.

11. **Optimized/stale/missing inputs cannot create PASS: operational PASS,
    semantic FAIL.** The outer harness forbids optimized mode and fails on
    any nonzero component; outer hash and generated-TeX omission mutations
    pass. Nevertheless, a semantically false quartet formula reaches PASS
    because no invoked gate evaluates it.

## Exact finite censuses

### Primitive completion domains

| Port count | Incoming selected | Incoming marginalized | Total |
|---:|---:|---:|---:|
| 3 | 289 | 831 | 1,120 |
| 4 | 831 | 1,983 | 2,814 |
| 5 | 1,983 | 4,155 | 6,138 |

Source supports are cycle 2, raw4 theta 6, and theta2 4. These independently
give `C(4,1)=831`, `C(4,0)=C(5,1)=1983`, and `C(5,0)=4155`.

### Four-port theta universe

| Category | Count |
|---|---:|
| Displayed quartet | 360,408 |
| Whole-map sign | 16,974 |
| Rank | 23,822 |
| Direct terminal presentations | 1,472 |
| Restoration member presentations | 2,540 |
| **Total** | **405,216** |

The 1,472 presentations reduce to 934 terminal classes: 839 quadratics, 36
higher-degree direct classes, 4 hard bindings, 20 isomorphisms, and 35
ordinary triangles. The 36 split into 22 quintics, 12 quartics, and 2 cubics.
There are 997 restoration-parent classes. Raw ledger gzip SHA-256 is
`431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96`;
uncompressed SHA-256 is
`f3fa7f6568551e1f5daa5aa0fbeb7cfd5773c8fd1277588efed3f98a7c8f4033`
over 391,559,514 bytes.

### Five-port theta2 universe

| Category | Count |
|---|---:|
| Displayed quartet | 2,942,592 |
| Whole-map sign | 2,528 |
| Rank | 800 |
| Quadratic | 240 |
| Isomorphism | 80 |
| **Total** | **2,946,240** |

Ledger gzip SHA-256 is
`805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659`;
uncompressed SHA-256 is
`550e8c2d9d7f683d79e8955b91629f1fc527fc8b72a1f592e85d6ecc74642bb7`
over 2,766,984,898 bytes. The dummy forest has 56 roots (40 one-dummy, 16
two-dummy), 576 six-port children (504 quartet, 72 isomorphism), 32
continuations, 288 seven-port children (256 quartet, 32 isomorphism), 864
descendants, and 832 leaves.

### Cycle layer

Base: 13,440 = 7,452 sign + 5,964 restoration roots + 16 triangles + 8
isomorphisms. Root dummy multiplicities are 324/1, 1,896/2, 2,784/3, and
960/4. Full: 536,364 = 535,920 quartet + 132 directional quadratic + 300
sign + 12 isomorphism. Base/full gzip SHA-256 values are
`d6209dc605c9f3a3459c129d741c6b788f26dcf989afe828d8a720833bfd49da`
and `cc73d0eaf3f39939c255c8f86915093e58159eca37c147ae2854d430f1fcb2f7`.

### Restoration and probes

Restoration: 997 canonical parents, 2,540 physical roots, role multiplicity
histogram `{1:568,2:1260,3:712}`, 36,568 first children, 256 second children,
36,824 edges, 36,792 leaves, depth two, 42 source transport classes, and
4,986 target transport classes. File SHA-256:
`43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8`.

Probes: 176 anchors; all 2,206 source and target sites; 29,964 one-port rows
partitioned as 27,758 quartet, 99 sign, 1,915 isomorphic, 192 triangle; 2,107
equalities; 544,571 two-port rows partitioned as 511,266 quartet, 576 sign,
30,969 isomorphic, 1,760 triangle; 32,729 equalities; 67,741 exact transports,
3,745 triangle transports, and 4,379 restrictions.

Independent census artifact:
`outputs/computational/independent_finite_census_audit.json`, script SHA-256
`50ee021da20e1f337e4463e1075345081305b5946badff2f912264376eb22a1c`,
output SHA-256
`8f38e03b8caedabfaf738fd084a21ed73ec69efed33188bc8de593ce51672319`,
payload `93f67aed4a71d1c93f695042d34070cd9bb4847b83c66f90eba8d756dfa88b2e`.
Runtime is intentionally excluded from the JSON to keep it deterministic.

## Independent rank replay

Raw ID 97 was reconstructed as
`((source=0)*2814 + target=4)*24 + permutation=1`. A self-contained
four-switch Fourier/Jacobian engine, importing no atlas/classifier/rank
verifier, reproduced:

- source descriptor
  `ffa19a908a552bb362e0c840df91c95a7db974f700f8ebc7fcce4ac2e5f55cd0`,
  rank 13, determinant
  `-478706839714566624614441380748865169471530201053/149787609539704268948588236421804522318836095761928116995023175680000000`;
- target descriptor
  `3085ce46031358d1cd879afdc62343b79dc0e00916df48421d73d5c105821dee`,
  rank 10, determinant
  `85344059259921/425095072120832000000000`.

Artifact SHA-256:
`647b330b985fd635dce772162e4686fea092f59cd8f638d9ae79a3d1866a6370`;
script SHA-256:
`349f8a9f30816e6c8a8033eb3a5949f1c1b4224c4d3bcfb39ace690659c45170`;
payload `d0d614fa619d4e9c98927a8e4e0611cb3f323407ad4cb6c50009bcc736d08f37`.

## Mutation coverage matrix

“Fresh” means a mutation was actually injected and replayed during this audit,
not merely read from a stored PASS report.

| Requested mechanism | Fresh/inspected/unrun | Observed intended mechanism | Status |
|---|---|---|---|
| Omitted raw row | Fresh raw 7-case suite; independent dense scan | Rejected by raw count/dense-ID gate | PASS |
| Duplicated raw row | Fresh raw 7-case suite; independent uniqueness scan | Rejected by duplicate raw-ID gate | PASS |
| Incorrect classifier precedence | Fresh probe 15-case disposable suite | `CORRECTED_PROBE_REPLAY_FAIL:classifier order` | PASS |
| False canonical merge | Fresh theta2 suite has one false-isomorphism mutation; fresh 196-presentation graph audit | Single injected false relation rejected, but no global collision partition | PARTIAL/UNVERIFIED globally |
| Source↔target reversal | Verifier direction fields inspected | No explicit fresh reversal attack | UNRUN |
| Reversed parent order | Reverse marginal-class mutation is fresh but is not reticulation-parent order | No graph-parent reversal mutation | UNRUN |
| Illicit inheritance complement | Descriptor action code inspected | No complement-without-certified-parent-reversal attack | UNRUN |
| Sampled rank substituted for symbolic upper | Fresh false-rank/upper-binding corruption; symbolic code inspected | No literal sampled-engine substitution | UNRUN as mutation; symbolic mechanism PASS statically |
| Missing restoration child | Fresh restoration 13-case disposable suite | First/second omissions rejected by coverage length | PASS |
| Wrong restoration parent | Fresh restoration 13-case suite | Wrong parent rejected by complete acyclic parent forest | PASS |
| Restoration cycle | Fresh restoration 13-case suite | Nonforest attempt rejected by abstract-parent gate | PASS |
| Broken restriction/transport | Fresh restoration and probe suites | Rejected by semantic parent/registry/self-hash replays | PASS |
| Missing probe site | Fresh root-suppressed-site mutation; all site formulas scanned | Rejected by candidate-profile formula | PASS for tested site; other site-type injections inspected only |
| Invented/inconsistent triangle | Fresh probe mutation plus strict direct graph replay | Global triangle hash rejected; all direct triangles satisfy ordinary pattern | PASS for direct/tested cases; all probe graph relations not rebuilt here |
| Altered D_plus witness/facet | Fresh restoration and 12-case analytic suites | `s=2` rejected; exact `g=2s-1` facet rejected | PASS |
| Reassigned quadratic/cubic/quartic/quintic | Fresh release suites | Certificate ID/pullback binding failures | PASS |
| Optimized Python | Fresh outer/raw/restoration/probe/release suites | Explicit forbidden-mode diagnostics | PASS |
| Stale hash/generic missing outer file | Fresh outer handoff mutations | Wrong hash and omission rejected | PASS |
| Missing generated TeX inputs | Fresh five-source build | Both generated supplement inputs rejected | PASS |
| Missing bibliography specifically | Generic outer verifier logic inspected | This track did not inject bibliography-specific omission | UNRUN here; provenance track to reconcile |
| Spectrum or quartet-coordinate label altered | **Fresh independent mutation** | Both mutations still return identical quartet PASS | **FAIL: survivor** |

Fresh disposable restoration report:
`outputs/computational/mutation_disposable/project/work/restoration_sign_reclassification/corrected_restoration_mutation_certificate.json`,
13/13 rejected, file SHA-256
`79645c56cc0b4689eafcd7abc5f78f7854dac694e32a5915c905f557e7f1e6c0`,
payload `ff2d7203e32664c286e231628c933be1a4337c3e560ea51994f41d786d997c07`.

Fresh disposable probe report:
`outputs/computational/mutation_disposable/project/work/probe_coherence_corrected/probe_coherence_mutation_certificate.json`,
15/15 rejected, file SHA-256
`517138a25e210faa33caaef2dec6ae6b9a4b27ec5b61c268f4589181a86541b5`,
payload `ea6e8e554c8216ac9fa97b7402449d861abad3f3b5dde4ce3eafd5f68d162a17`.

Fresh disposable analytic report:
`outputs/computational/mutation_disposable/project/work/adversarial_proof_review/mutation_certificate.json`,
12/12 rejected, file SHA-256
`390976c38c6a1e00ca2490d5ef341f17cc9a13e72892dcb27a1d19cea315d172`,
payload `0dce2bf3a48a05f50826ffcb9c49ebbf6e78e79c135030549d708a25d31ff76c`.

## Release-harness audit

Outer `run_all_verifiers.py:27-53` declares 21 quick commands plus one
full-only primitive-regeneration command. Lines `78-99` forbid optimized
Python and require a new output directory; `102-133` starts every subprocess,
captures its log, and stops on failure unless diagnostic `--keep-going` is
explicit; `134-155` returns PASS only when every expected command ran with
exit status zero.

The final release verifier similarly treats a nonzero status or missing PASS
marker as failure and checks expected-failure mutations. It does not collect
peak memory itself. The shared fresh quick run completed all 21 commands in
778.85 s and produced ledger SHA-256
`76236eebb4900c2aa3b616470d5a15fd9de9228c3fe0a5cdc43bd472bc9ef2cd`.
That operational PASS is valid but cannot cure C-1: its
`quartet_sign_logic` stage completed in 0.034 s with the same abstract-gate
stdout hash as the semantic mutations.

## Execution ledger for independent/fresh attacks

| Command or check | Exit | Wall | Peak RSS | Output SHA-256 / payload |
|---|---:|---:|---:|---|
| `check_quartet_coordinate_semantics.py` | 0 | 0.43 s | 81,543,168 B | `c6517e...` / `924508d6...` |
| `test_quartet_gate_blindness.py` | 0 | 0.13 s | 24,510,464 B | `72a033e2...` / `227b03cd...` |
| `independent_finite_census_audit.py` | 0 | 30.45 s | 172,212,224 B | `8f38e03b...` / `93f67aed...` |
| `independent_graph_relation_audit.py` | 0 | 6.19 s | 125,763,584 B | `a431ac16...` / `fd101d38...` |
| `independent_rank_replay.py` | 0 | 0.22 s | 52,330,496 B | `647b330b...` / `d0d614fa...` |
| weak-sharpness independent audit in disposable copy | 0 | 0.25 s | 43,302,912 B | `cfd8d3a2...` / `848cc69e...` |
| restoration 13-case suite in disposable copy | 0 | 66.46 s | 569,540,608 B | `79645c56...` / `ff2d7203...` |
| probe 15-case suite in disposable copy | 0 | 172.97 s | 72,531,968 B | `517138a2...` / `ea6e8e55...` |
| analytic/domain 12-case suite in disposable copy | 0 | 0.06 s | 26,116,096 B | `390976c3...` / `0dce2bf3...` |
| shared `run_all_verifiers.py --quick` | 0 | 778.85 s | not recorded | ledger `76236eeb...` |

Full hashes, exact commands, determinants, and row-level records are in the
named JSON artifacts. Peak RSS is from `/usr/bin/time -l` where shown.

## Submitted producer/verifier registry inspected

| Layer | File | SHA-256 |
|---|---|---|
| Primitive/model/canonicalizer | `package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py` | `5b9e03653cc6960bf341fcbe7e63ffd10226d0f6a56441012212c6e3b2a26483` |
| Raw producer | `work/raw_ledger_audit/generate_raw_ledger.py` | `91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44` |
| Raw verifier | `work/raw_ledger_audit/verify_raw_ledger.py` | `745ece3309128b0b0a5bb824e9811be946c40bee744cd99ebdc7d709f714e371` |
| Composite producer | `work/corrected_composite_ledgers/generate_corrected_composites.py` | `a117923e7b5cf90f0a13630fd21a6c454139f7e6e9c3c7bf84276229351a58ce` |
| Composite verifier | `work/corrected_composite_ledgers/verify_corrected_composites_independent.py` | `67ddf315b400a0a96f4a5901e6a340a158d9d4fd1111e8ee17193de5d78b5690` |
| Terminal-registry producer | `work/corrected_composite_ledgers/build_terminal_registry.py` | `e4a0576a6340e41ed2e9818d8971032f429418aa7782b6502a421ce3f407c119` |
| Rank syzygy engine | `work/rank_upper_certificates/syzygy_upper.py` | `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e` |
| Rank verifier | `work/rank_upper_certificates/verify_rank_upper_certificates.py` | `a0ec39eda9b36f1c32b4fa3c67414fddd5cd68e4cf02659dd9d5182ce0c298af` |
| Rank binding | `work/raw_ledger_audit/rank_upper_binding.py` | `4ed999fbcd4527908c2e4ba82d0c32651ec97feb9c94ca9a4452f44c951a635d` |
| Direct polynomial verifier | `package/referee/k2p_offline_sweep_portable/proofs/verify_four_port_direct_residual_closure.py` | `e8437ecea238ac87add6ebcfadc21a2f1a5cc22b9f1cac1300dac7339a43529a` |
| Quartet gate | `work/quartet_separation_closure/verify_quartet_logic.py` | `edd0e42ffe14a4dbc30c685ad20dcb0d766547fe0dcefdd6a7ff51cc998c8ae1` |
| Restoration producer/verifier | `work/restoration_sign_reclassification/build_corrected_restoration_forest.py`; `verify_corrected_restoration_forest.py` | `55e7196b840b98334327e81b2583ab2105a8107ee9be308781b41187c9c7de6d`; `e4cef28f156e1c300ed7b7cc48bb1a96f3a7686d92e2c748ec8dfa156d236f9e` |
| Probe producer/verifier | `work/probe_coherence_corrected/build_probe_coherence_corrected.py`; `verify_probe_coherence_corrected.py` | `f0176e1759771a01ffa3da9e8d2b8967fc9189d3f93b30c6d06554bba9a77ddf`; `3facc1b51c133aa953f4a0cba86782672c86e78990d72ef2fc2aaa16a6f2a1bd` |
| Probe partition verifier | `work/probe_coherence_corrected/verify_site_transport_partition.py` | `eec1206761682ed7e1f5f276b3e8e6128c037b9d156aeb631ecc44ca8938f722` |
| Separate probe graph replay | `work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py` | `51e2de1e8b1fe753a5b0605b3995ea02cfc7db4c3f83d7a3d39da51a116bba44` |
| Outer/final harness | `run_all_verifiers.py`; `work/final_theorem_release/verify_final_theorem_release.py`; `run_release_mutations.py` | `cea2d4a4b478080216d4db170c15bd6331431bd63a343196bccf69980f4227cb`; `1f197bf6e5d3704e6a9d25832f21454125a0fa5d4d0898fbc42db317dab8dd2d`; `88fb0020271ee68465bfdd5420d3f35bb4a64f53478c34da606798e6be0fd262` |
| Release shared enforcement | `work/final_theorem_release/release_common.py` | `66b417a42684e59e6f99c5ac655699e03eeb76295bafcd5e38565390351798e8` |

## Track-local unverified gates

- exhaustive pairwise canonicalizer merge/split testing over all finite
  universe graphs;
- an alternate-engine replay of all 4,379 rank upper bindings;
- independent recomputation of every non-quartet cubic/quartic/quintic and
  sign predicate;
- independent graph reconstruction of all 67,741 probe transports and every
  restoration transport;
- explicit source↔target reversal and reticulation-parent-order/inheritance-
  complement mutations;
- literal sampled-rank-engine substitution for the symbolic upper prover;
- bibliography-specific omission mutation (generic omission and generated-TeX
  omissions were tested);
- the top-level `--full` primitive-regeneration run was not run by this track;
  the root referee must reconcile any shared full execution separately.

## Minimal adequate remedy

1. Correct the quartet coordinates uniformly to the equal C/T sector (or,
   less desirably, change every declared/implemented spectrum convention
   coherently).
2. Add an exact symbolic verifier that derives the printed quartet pullbacks
   from the declared character order and checks the strict physical sign
   factors. It must fail under either semantic mutation above.
3. Rebind and replay all quartet-labelled raw, cycle, restoration, and probe
   terminal families; regenerate theorem-artifact C02 and the release ledger.
4. Rebuild article/supplement PDFs and reseal every affected manifest/report.
5. Before claiming exhaustive canonicalizer independence, either add a full
   collision/splitting replay with the strict ordinary-triangle predicate or
   narrow the claim to the directly replayed relation presentations.

No evidence from this audit requires changing the central architecture or
starting a mixed-sign or unrelated extension. The demonstrated repair is a
uniform coordinate correction plus a missing exact semantic gate.
