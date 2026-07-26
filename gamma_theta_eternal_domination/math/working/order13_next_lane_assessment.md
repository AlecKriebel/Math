# Post-`hole7` lane assessment for the order-13 frontier

> **Portfolio note, 2026-07-26 13:17 PDT.**  This memo ranks only the
> computational fallback lanes.  Checkpoint 048 supersedes its immediate
> launch recommendation: the accepted `hole7` input was frozen before any
> solver run, and the campaign now prioritizes a universal
> minimum-counterexample proof before any further order-13 production or move
> to order 14.  If the finite lane resumes, the relative ranking and stop
> gates below remain the current evidence-based recommendation.

## Scope and evidence labels

This is a bounded research-design memo, not a mathematical claim, a solver
result, or a coverage certificate.  The repository snapshot inspected was
`HEAD b9b74a38415dac6ef11bb7cbc55badf224affadd`.

The labels below have the following meanings.

- **PROVED**: a consequence of accepted campaign mathematics.
- **CERTIFIED-FINITE**: backed by an accepted finite certificate.
- **OBSERVED**: measured from retained artifacts or the current machine.
- **ESTIMATE**: an extrapolation or arithmetic ceiling, not a generated
  catalog or a coverage result.
- **RECOMMENDATION**: a portfolio decision, not a theorem.

At the time of this audit, `instances/order13_k3_hole7/` contained an exact
constructor package, but no terminal `hole7` solver result or production tree
was visible.  The ranking should therefore be updated with the terminal
`hole7` time and proof-volume measurements when they exist.

## Executive decision

**RECOMMENDATION.**  After the current `hole7` attempt, take the order-13
`hole5` lane next, but do not run the unstrengthened formula in monolithic
proof-production mode.  First port and independently audit the accepted
order-12 free-vertex signature sorter.  Its first kill test is a single
60-second, proofless, seed-zero solve of the exact audited strengthened
formula.  If that test is not terminal, stop the monolithic lane and
partition it by an exhaustive prefix of the lexicographically least free
signature.

The ranking is:

1. order-13 \(k=3\), `hole5`, with an audited \(S_7\) signature sorter;
2. C-056 \(k=5\) kernel-and-attachment enumeration;
3. the whole order-13 \(k=4\) anchored DoubleLex parent.

The principal reason is payoff per new trust surface.  If `hole7` receives an
accepted UNSAT certificate, `hole5` is the only remaining branch in the
accepted order-13 \(k=3\) cover: C-053 already excludes `hole11`, and C-057
certifies `hole9` UNSAT.  The `hole5` core and production machinery are much
smaller and more mature than either alternative.  The order-12 history also
gives a concrete mechanism, rather than a generic hope, for making this
specific hard branch tractable.

The recommendation is conditional in two ways:

1. a SAT result immediately becomes a candidate-verification emergency; and
2. if `hole7` exposes proof growth or a runner defect relevant to `hole5`,
   that evidence must be incorporated before launch.

## Comparison at a glance

| lane | exact or bounded search object | preparation gap | decisive payoff | dominant risk |
|---|---|---|---|---|
| \(k=3\), `hole5` | 9,802 variables; 40,726 clauses; 493,820 literals; 1,805,539-byte unstrengthened proposed formula | prove/audit \(S_7\) covariance; produce and independently reconstruct a symmetry-derived package; authorize its production intake | with accepted `hole7`, closes the complete order-13 \(k=3\) slice | the plain analog was solver-hard; the order-13 sorter has not yet been proved or audited |
| \(k=5\), C-056 kernels | ten-vertex \(Q\), then attachment-mask orbits; 233,002 raw unordered mask pairs per kernel before structural filters | no kernel catalog, canonical attachment generator, orbit manifest, or independent coverage checker exists | could close the entire order-13 \(k=5\) slice without a monolithic SAT proof | a naive kernel-by-mask product is billions of cases; coverage engineering is substantial |
| \(k=4\), whole parent | 29,393 variables; 343,117 full DoubleLex clauses; 5,109,628 literals | new order-13 encoder, independent reconstruction, new \(S_9\times S_4\) covariance audit, runner/package work | one exact UNSAT certificate would close the order-13 \(k=4\) slice | roughly four times the coloring bank and 4.29 times the literals of the order-12 formula; proof expansion may approach or exceed the practical disk cap |

The order-13 formula counts in this table are exact combinatorial counts for
the proposed encodings recorded in `math/lemmas/order13_strategy.md`.  They
are not solver outcomes.

## Lane 1: order-13 `hole5`

### Exact size and reuse

**OBSERVED.**  The accepted order-13 \(k=3\) constructor architecture already
supports the four hole templates without runtime monkeypatching.  The current
`hole7` package demonstrates the production-scale census:

\[
 9{,}802\text{ variables},\quad
 34{,}903\text{ clauses},\quad
 349{,}248\text{ literals},\quad
 1{,}372{,}338\text{ bytes}.
\]

Its manifest explicitly records no heuristic symmetry breaker.

**PROVED/COUNTED FOR THE PROPOSED ENCODING.**  The corresponding unstrengthened
`hole5` formula has:

\[
\begin{aligned}
&9{,}802 &&\text{variables},\\
&29{,}791 &&\text{base clauses},\\
&10{,}935 &&\text{complete coloring rows},\\
&40{,}726 &&\text{full clauses},\\
&493{,}820 &&\text{full literals},\\
&1{,}805{,}539 &&\text{DIMACS bytes}.
\end{aligned}
\]

The proposed sorter fixes the six-vertex core consisting of the \(C_5\) rim
and its named common neighbor, and sorts the seven remaining vertices by
their six-bit \(H\)-adjacency signatures.  Six adjacent six-bit comparators
add no variables and exactly

\[
 6(2^6-1)=378\text{ clauses},\qquad 6(642)=3{,}852\text{ literals}.
\]

Thus the strengthened census should be 41,104 clauses and 497,672 literals,
with the same 9,802 variables.  These last totals are exact arithmetic for
the proposed suffix, not frozen output bytes.

The reusable trust base is unusually strong:

- the order-13 constructor, complete coloring-bank generation, package audit,
  and six-phase production runner already exist;
- the order-12 `hole5` signature theorem, auxiliary-free comparator
  generator, clean-room truth-table audit, and binary-proof pipeline were
  accepted;
- the order-13 core has the same signature width, six bits.  Only the free
  action grows from \(S_6\) to \(S_7\).

There is no exact transfer of the accepted order-12 formula hash or proof.
The reusable object is the symmetry mechanism and its audit design.

### Measured hardness and the relevant mechanism

**OBSERVED.**  On the order-12 unstrengthened `hole5` parent, retained trials
gave:

- a 600-second proofless `UNKNOWN`;
- a 300-second UNSAT-preset proofless `UNKNOWN`; and
- a proof-producing run terminated after 153.478 seconds at the
  536,870,912-byte file limit, without a solver result.

Peak RSS remained only about 65--71 MiB.  This was proof/search hardness, not
memory exhaustion.

**OBSERVED.**  After appending the accepted order-12 \(S_6\) signature sorter,
the formula had 6,886 variables, 23,968 clauses, 192,169 literals, and 754,323
bytes.  CaDiCaL returned UNSAT in 6.151 seconds at 59.66 MiB peak RSS.  The
raw binary proof was 12,524,020 bytes and its deletion-free stream was
6,337,621 bytes; the accepted checker chain verified it.

**INTERPRETATION.**  This is strong evidence that sorting attacks the actual
`hole5` symmetry bottleneck.  It is not a performance theorem for order 13,
so the port still receives a hard time gate.

### Mandatory soundness and package prerequisites

No proof-producing launch is authorized until all of the following are
complete.

1. Write the \(S_7\) covariance proof for the exact order-13 formula.  It
   must transport edge, common-neighbor witness, family, one-guard move, and
   complete coloring-bank variables.  Edge-only covariance is insufficient.
2. Prove that every \(S_7\) orbit has a representative whose seven six-bit
   signatures are nondecreasing.  The forced rim, named common neighbor, and
   their labels must remain fixed.
3. Independently regenerate the six comparators, exhaust their truth tables,
   and compare the clause multiset.  A direct audit has
   \(6\cdot2^{12}=24{,}576\) comparator assignments.
4. Create a deterministic derived package or an explicit audited constructor
   mode, then obtain byte-identical clean-room reconstruction.  The current
   base constructor advertises no heuristic breaker and must not be silently
   altered.
5. Audit production-runner intake for the new package schema and exact source
   closure.  Reusing the runner algorithm does not by itself authorize a new
   package type.

### First bounded kill test and stop gate

**RECOMMENDATION.**

1. After the prerequisites above, run exactly one seed-zero CaDiCaL child,
   proofless, on the exact strengthened formula.
2. Wall limit: 60 seconds.  RSS limit: 2 GiB.  One solver process only.
3. If SAT, freeze the assignment and graph immediately and invoke two
   independent semantic verifiers.
4. If UNSAT, authorize certificate production with the resource envelope
   below.
5. If `UNKNOWN`, timeout, or resource refusal occurs, do **not** start an
   unpartitioned proof-producing run.  Partition by a proved exhaustive
   Boolean prefix of the lexicographically minimum free-vertex signature and
   pilot the resulting cubes separately.

For certificate production, use one child at a time, a 2 GiB RSS cap, a
30-minute limit per child phase, a 1 GiB maximum individual proof file, and
an 8 GiB free-disk reserve.  Stop and refine the partition if any proof
reaches its cap or if the conservative five-live-file preflight cannot
preserve the reserve.

This is deliberately stricter than the runner's 2 GiB default file cap.
With only about 17 GiB currently free, a five-file preflight at 2 GiB per
file plus the 8 GiB reserve cannot pass; at 1 GiB it requires about
13.1 GiB and remains feasible.

## Lane 2: C-056 \(k=5\) kernel enumeration

### What is already proved

**PROVED.**  C-056 reduces every order-13, parameter-five counterexample to
a degree-two root \(v\), its nonadjacent neighbors \(a,b\), a ten-vertex
kernel

\[
 Q=G-N[v]
\]

with all four parameters equal to four, and two attachment masks
\(A,B\subseteq V(Q)\).  The residual

\[
 R=Q-(A\cup B)
\]

has all four parameters equal to three.  The accepted reduction also
supplies:

- the full independent-anchor projection hierarchy;
- \(\Delta(Q)\leq6\) and at least three nonsimplicial vertices;
- an exact clique-insertion test;
- exactly 707 possible domination tests before early rejection;
- forced-state one-guard response filters; and
- \(|A|=|B|=6\Rightarrow A=B\), with
  \(Q[R]\cong K_2+2K_1\).

This is a complete coverage design, not an exclusion.

### Static endpoint-collapse simplification

**PROVED, WITH AN EXPLICIT PRECONDITION.**  For any graph \(F\), once
independent exact checks certify both

\[
 \gamma(F)=t\quad\text{and}\quad\theta(F)=t,
\]

the parameter chain gives

\[
 \gamma(F)=i(F)=\alpha(F)=\gamma^\infty(F)=\theta(F)=t.
\]

Therefore the kernel generator does not need to execute an eternal
fixed-point computation on \(Q\), \(R\), or a required projection after
both endpoint equalities for that graph have been independently certified.
The same endpoint check also yields well-coveredness because
\(i(F)=\alpha(F)\).

This shortcut must not be used after checking only one endpoint, after a
heuristic coloring attempt, or on the reconstructed 13-vertex \(G\), where
the desired endpoints differ.  Final \(G\) survivors still require both
independent exact one-guard evaluators.

This substantially lowers per-kernel cost: domination and clique cover on
at most ten vertices can be checked with small subset and exact-coloring
searches, while the 1,287-state \(k=5\) one-guard fixed point is deferred to
the final survivors.

### Catalog arithmetic and its boundary

**OBSERVED FROM THE PUBLISHED MMV TABLE.**  The locally archived 2022 source
reports 11,716,571 connected unlabeled graphs of order 10, of which 23,394
satisfy \(\gamma=\gamma^\infty=\theta\), across all common parameter values.
The repository contains the table and the 56 near-miss Graph6 records, but it
does not contain a Graph6 catalog of these 23,394 equality graphs.

**ESTIMATE, NOT A CATALOG OR COVERAGE RESULT.**  Component additivity shows
that an admissible \(Q\) has at most four components and every component has
equal additive parameters.  Using the published connected equality counts

\[
 (c_5,\ldots,c_{10})=(5,22,67,358,2265,23394)
\]

and deliberately overestimating \(c_1,\ldots,c_4\) by the total connected
graph counts \((1,1,2,6)\), the multiset-component arithmetic ceiling is

\[
 \sum_{\substack{\lambda\vdash10\\\ell(\lambda)\leq4}}
 \prod_s {c_s+m_s(\lambda)-1\choose m_s(\lambda)}
 =27{,}018.
\]

This number is conditional on the published counts and ignores the required
common value four, the projection hierarchy, \(\Delta(Q)\leq6\), and the
nonsimplicial filter.  It is only an upper estimate for planning.  It neither
constructs the graphs nor proves that an orbit is covered.

### Attachment scale and correct generation order

**PROVED/COUNTED.**  Before quotienting by \(\operatorname{Aut}(Q)\), C-056
leaves exactly 233,002 unordered mask pairs with

\[
 1\leq|A|,|B|\leq6,\qquad |Q-(A\cup B)|\geq3.
\]

Multiplying the 27,018 planning ceiling by 233,002 gives about 6.295 billion
raw pairs.  That product is an **ESTIMATE** and demonstrates only that a
Cartesian kernel-by-mask loop is unacceptable.

The implementation should instead:

1. generate or assemble \(Q\) from connected equality-component catalogs;
2. filter the exact \(Q\) hierarchy and degree/nonsimplicial conditions;
3. enumerate \(R\subseteq Q\) first and certify the parameter-three endpoint
   hierarchy;
4. generate only covers \(A\cup B=Q-R\) compatible with mask sizes and
   Lemma 9/Theorem 10;
5. quotient online by
   \(\operatorname{Aut}(Q)\times\langle A\leftrightarrow B\rangle\);
6. apply clique insertion, the 707 domination checks, and forced-state tests;
   and
7. invoke the two one-guard evaluators only on reconstructed survivors.

No exact transfer from the order-12 \(k=4\) UNSAT certificate supplies this
catalog: \(Q\) has \(\theta(Q)=4\), can be disconnected, and is not an
order-12 counterexample target.

### First bounded kill test

Before committing to full coverage engineering, implement a checkpointed
static kernel filter and run one deterministic \(1/256\) nauty shard of
connected order-10 graphs with the sound \(\Delta\leq6\) generator
restriction.  Record staged survivor counts after endpoint collapse, local
hierarchy, and nonsimplicial tests.  Use one process, at most 1 GiB RSS, and a
10-minute wall budget.

Stop and redesign around a constructive fixed-independent-four-set generator
if the measured full-stream extrapolation exceeds 12 CPU-hours.  If the
kernel rate is acceptable, run an \(R\)-first/aut-orbit attachment pilot on
at most the first 100 canonical kernels; do not extrapolate from the raw
233,002-pair ceiling without recording every filter stage.

This is the preferred second lane because it has a proved finite normal form
and avoids large proof files.  It is not first because its catalog and
coverage checker do not yet exist.

## Lane 3: exact order-13 \(k=4\) parent

### Exact formula scale

**PROVED/COUNTED FOR THE PROPOSED ENCODING.**  The whole anchored order-13
DoubleLex target has:

\[
\begin{aligned}
&715 &&\text{family states},\\
&25{,}740 &&\text{move variables},\\
&29{,}393 &&\text{total variables},\\
&79{,}320 &&\text{base clauses},\\
&262{,}144 &&\text{complete coloring clauses},\\
&343{,}117 &&\text{full DoubleLex clauses},\\
&5{,}109{,}628 &&\text{full literals}.
\end{aligned}
\]

The first sorted outer row has exactly four exhaustive forms:

```text
0000  0001  0011  0111
```

These are a ready-made resumable partition after a whole-formula pilot.

### Reuse and lack of exact transfer

**OBSERVED.**  The accepted order-12 formula had 18,381 variables, 115,507
clauses, 1,190,774 literals, and 4,030,657 bytes.  Its solver retained a
32,987,136-byte raw binary proof; normalization produced 15,783,377 bytes,
and LRAT conversion produced 228,381,671 bytes.  The forward RUP replay took
about 437 seconds and 125 MiB RSS; LRAT conversion took about 225 seconds and
245 MiB RSS.

The order-12 encoder and DoubleLex appender are intentionally frozen to
\(n=12\).  Most loop structure and the mathematical \(S_8\times S_4\)
argument are reusable, but the following are new proof obligations:

- a separate order-13 module and schema;
- exact independent reconstruction of 29,393 variables and all clause
  families;
- \(S_9\times S_4\) covariance of the complete formula;
- fresh row and nine-bit column comparator audits;
- any C-051 strengthening, if used, with a separate semantic proof and
  small-order differential tests; and
- a new production/package audit.

C-047's order-12 UNSAT result has no upward transfer: adding a thirteenth
vertex creates genuinely new graphs and game states.

### Storage estimate and first kill test

**ESTIMATE.**  Scaling the order-12 DIMACS bytes per literal gives an
order-13 input of about 17.30 MB (16.49 MiB).  Linear scaling of the retained
order-12 proof sizes by literal count would give roughly 142 MB raw binary
DRAT and 980 MB LRAT.  Solver and proof growth need not be linear, so these
figures are planning estimates, not promises or upper bounds.

After the new encoder and covariance audits, run a 60-second proofless
whole-formula pilot with one process and a 2 GiB RSS cap.  If it is not
terminal, pilot each of the four exhaustive first-row cubes for 60 seconds.
Do not enter certificate production unless at least one branch gives measured
evidence compatible with a 1 GiB individual-file cap and the 8 GiB disk
reserve.  Otherwise keep this lane at formula-construction readiness and
return effort to the C-056 generator.

This lane ranks third because its trust surface is larger than `hole5`, it
has no structural shrink comparable to C-056, and its likely LRAT working set
is close to the present conservative file ceiling.

## Laptop budget

**OBSERVED.**  The machine reports:

- Apple M1 Pro;
- 10 physical/logical CPU cores;
- 16 GiB physical RAM; and
- about 17 GiB free on a 97%-used data volume at the audit snapshot.

No solver or other campaign-heavy process was visible during the snapshot,
but the desktop applications were active and one renderer used about 1 GiB
RSS.

For all three lanes:

- use one heavy child only;
- cap a solver at 2 GiB RSS and a static enumeration child at 1 GiB;
- retain at least 2 GiB reclaimable-memory margin;
- preserve an 8 GiB disk reserve;
- use deterministic shards/cubes and atomic checkpoints;
- never retain a raw graph stream when a hash, count ledger, and survivor
  catalog suffice; and
- suspend proof production if free disk falls below the runner's conservative
  preflight requirement.

More CPU would accelerate the independent nauty shards in the C-056 lane, but
the present immediate bottleneck is free disk and proof/certificate working
volume, not RAM or solver parallelism.

## Exact provenance

The following hashes bind the sources used for the assessment.

| role | path | SHA-256 or exact embedded hash |
|---|---|---|
| order-13 census and lane design | `math/lemmas/order13_strategy.md` | `5b59d8c9fcbf1eb2a3e20157fcef02b4faa02a48e62c6fbda7b9c1fc12e7d6c6` |
| accepted order-12 sorter theorem | `math/lemmas/hole5_signature_symmetry.md` | `8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8` |
| accepted order-12 sorter generator | `src/synthesis_k3/hole5_signature_breaker.py` | `cc1dc4249dc20f78e8eff4de14ffdca632da1e9455a381000786faa28c950c77` |
| unstrengthened order-12 hardness ledger | `results/logs/hole5-full-bank-trials-20260725.json` | `6c173adcceecc601b1e0314142b76574e37d8de8932154b9b858ed5746bfcdfa` |
| order-12 sorter validation ledger | `results/logs/hole5-signature-breaker-validation.json` | `dafe1cdfe66bac034e71faaa0ba3f157fc88b21a317cbd6cba5f62e598f6d442` |
| order-12 strengthened terminal outcome | `results/synthesis_k3_hole5_signature_seed0_600s_binary/outcome.json` | `ea2ea36321a786aa40aff1e68587474bbdba5402abc800b1a0816d65b6df8df4` |
| current order-13 constructor core | `src/search/order13_k3/encoding.py` | `da06a797a29fcefff1eadbea4aa1535fb2ef14c0c64d84236bb3bf9241e1d47d` |
| current order-13 package generator | `src/search/order13_k3/generate.py` | `35c78ecc4802667514c6294ac00558b83c9cfc83a37f9854533aedb9ca1bf1d0` |
| current order-13 production runner | `src/search/order13_k3/production.py` | `7223e9c789b50aa021371f07670af9ee1a2406fd649e1d84713ed4b566a7f11e` |
| exact `hole7` package manifest | `instances/order13_k3_hole7/constructor-manifest.json` | `a218a21b761754bfaef520d8e98d10963c97a1178966cbfbb68054005ac53bf9` |
| order-12 \(k=4\) parent manifest | `instances/order12_k4_connected_parent/manifest.json` | `621a0878c117dc8b4d6dbd0ba14c8402a8c24e8339d2f85cb23d61ffd74fbb61` |
| order-12 \(k=4\) DoubleLex manifest | `instances/order12_k4_connected_doublelex/manifest.json` | `4ca0b1d43c145acf35f7545b7a85e5d0aafa62e7279c120212455985312cba96` |
| C-056 structural normal form | `math/working/order13_k5_structural.md` | `34c29d4b14e0955bd1ea0968f138a991cdd2a595ff3dd26891b74c1218af0a11` |
| C-056 follow-up and 233,002-pair count | `math/working/order13_k5_followup/RESULT.md` | `14d44f8b69acdec27783559794f6096c77c9c3f63cc2e219d59728eaf1e4a88b` |
| C-056 acceptance binding | `results/order13_k5_structural_acceptance.json` | `d0fb174d1493d4175c4f42c09f67723e6157537041ef056e8f15262b7013bd52` |
| MMV connected-graph/equality counts | `literature/sources/mmv2022_src/EternalDomination.tex` | `e77618dcf06b4e65d6b622e993eed4307238de49d4f395da920044bb6dfd9a45` |

The exact order-13 `hole7` CNF hash embedded in its manifest is
`3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340`.
The exact order-12 \(k=4\) DoubleLex CNF hash embedded in its manifest is
`14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`.

## Bottom line

**RECOMMENDATION.**  Spend the next bounded sprint on the audited order-13
`hole5` signature transfer and its 60-second kill test.  It has the smallest
new proof surface, the strongest directly relevant historical mechanism, and
the highest near-term chance of converting the current frontier into a
complete \(k=3\) slice.  Prepare the C-056 static kernel filter as the next
lane if the monolithic `hole5` pilot misses its stop gate.  Keep the order-13
\(k=4\) parent at design readiness until either `hole5` closes or the C-056
kernel census shows that its coverage engineering is larger than projected.
