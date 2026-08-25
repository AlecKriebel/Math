# Fresh adversarial mathematical review of the 2026-08-24 K2P-SAME package

Date: 2026-08-25  
Reviewer role: independent mathematical referee subreview  
Submission root reviewed: `/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/isolated/k2p_principal_d_plus_submission_referee`  
Final checkpoint: mathematical subreview 100% complete (best estimate)

## 1. Mathematical verdict

**Mathematics: PASS.** I found no counterexample, invalid implication, hidden use
of the revoked rooted tree/sunlet oracle, or unresolved mathematical quantifier
gap in the revised theorem architecture. In particular, the previously invalid
quartet-coordinate claim has been replaced consistently in the article and
current quartet semantics, and the replacement is correct by a fresh symbolic
derivation.

My confidence in the mathematical verdict is **0.94**. The remaining uncertainty
is concentrated in the millions-of-record finite exhaustiveness claim, which is
inherently computational and is not converted into a hand proof by this review.
I checked the finite universe theorem, its certificate semantics, and several
independent representatives, but—by assignment—did not run the full replay
suite. A separate computational audit must establish exhaustive row coverage,
canonicalization, and transport completeness.

There is one real **authority-consistency defect** in the package: an artifact
named as current C02 authority contains pre-reclassification restoration counts
that disagree with the revised article and current restoration forest. This does
not alter a mathematical predicate or defeat the theorem, but it prevents the
theorem-to-artifact crosswalk from being literally mutually consistent until the
artifact is regenerated or its scope is narrowed and the affected seals are
updated. Details are in Finding 1.

No prior review verdict, stored PASS label, replay report, certificate count, or
frozen hash was used as a mathematical premise.

## 2. Materials read and source/PDF consistency

I read the complete current sources:

- `proof_compression_submission/article/main.tex` (1,866 lines);
- `proof_compression_submission/supplement/supplement.tex` (954 lines);
- `proof_compression_submission/supplement/certificate_appendix.tex` (285 lines);
- `proof_compression_submission/supplement/compression_tables.tex` (69 lines);
- `proof_compression_submission/article/references.bib` (202 lines);
- the theorem/artifact crosswalk in both Markdown and JSON form;
- the promoted proof manuscript and the domain, quartet, bridge/marginal,
  global, cycle, theta2, canonicalizer, probe, rank-upper, restoration,
  triangle, genericity, reconstruction, and weak-sharpness proof narratives.

The five declared source hashes I obtained were:

| Source | SHA-256 |
|---|---|
| `article/main.tex` | `ca6dd8d750768b0c47121c8bd60c5c9c3223af194139f5f578cb8bbf5fd5c3f1` |
| `supplement/supplement.tex` | `57275e1e5e1058306607a98583ac31e98383952ef2284515fea01f1c47ce95bd` |
| `supplement/certificate_appendix.tex` | `f2444f0308ab2dcccc45dec0704e98b147fffe4bb11fef9ef19cb7f34e688af5` |
| `supplement/compression_tables.tex` | `1ce2ef60784c1a240cdd639cd845710934c9587e4c341ad293394c8e1f758e9b` |
| `article/references.bib` | `14dbb4901d924b068c8cc2d050e73bae3cf996a72863a22ade90d6f8e6b4057c` |

I rendered and visually inspected all 26 article pages and all 24 supplement
pages. The PDF hashes were:

| PDF | Pages | SHA-256 |
|---|---:|---|
| article | 26 | `2c4433d53c33c337d4ed028c2843cf0b5631263d7bf4a0a42106727985daa3a8` |
| reader supplement | 24 | `9b10797d7503e6940d80a95bc90302b3b32a9ea34cb9f63a54bee3f12f3c06e1` |

The corrected quartet formulas render correctly on article PDF p. 6; the
triangle blocks and determinants render on p. 17; the genericity,
reconstruction, continuous-time, and weak-sharpness arguments render on pp.
19–24. I saw no clipped formula, missing generated table, or visible mismatch
between those pages and the source. Formal clean-build and byte-provenance
questions belong to the reproducibility audit, not this mathematical subreview.

## 3. Independent exact attacks

All scratch work is under
`/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/math`.
None of these scripts imports a submitted classifier, canonicalizer, certificate
verifier, expected classification table, or model-map implementation.

### 3.1 Main independent algebra/graph attack

Command:

```text
.venv/bin/python -B independent_checks/math/fresh_exact_checks.py
```

The script SHA-256 is
`6e31a7a28e59921d874eece125ae980b80ef50b373433d2463f5a7b0315667a5`;
the JSON output SHA-256 is
`aedc640f928ecd0b2336289c19a743bbf09b88a0ca55345e6505d8e6ec6f8a1f`.
It exited 0 in 1.19 s with peak resident memory 84,934,656 bytes.

It independently did all of the following.

1. Rebuilt the quartet tree Fourier monomials from splits and obtained
   
   \[
   \begin{array}{c|ccc}
    &12|34&13|24&14|23\\ \hline
   q_{CCCC}-q_{CCTT}&0&P(1-g_I)&P(1-g_I)\\
   q_{CCCC}-q_{CCTT}+q_{CTCT}-q_{CTTC}&0&2P(1-g_I)&0,
   \end{array}
   \]
   
   where \(P=s_1s_2s_3s_4>0\). This exactly matches article source
   lines 415–461 (PDF p. 6).
2. Factored the whole-map three-sunlet polynomial as
   
   \[
   -a_s^2b_s^2a_gb_gc_g^2f_s^2\delta(1-\delta)d_ge_g(1-f_g)^2,
   \]
   
   matching article lines 474–527 and supplement lines 400–413.
3. Rebuilt the ordinary-triangle witness from its map, obtained the six
   \(1/12\) and three \(1/48\) nonconstant coordinates, found full Jacobian
   rank nine, and independently reproduced
   \(\det J_0=-1/2\) and \(\det J_\perp=-1/4\). These are the exact blocks at
   article lines 1232–1272 (PDF p. 17), not a sampled-rank argument.
4. Rebuilt the weak-sharpness maps from the literal arcs. Exact symbolic
   elimination gave rank nine for each map, the two normalized tensors printed
   in the weak audit, and exact equality after the stated pendant factors.
5. Suppressed the two weak witnesses to literal mixed graphs and independently
   enumerated all ordinary-edge orientations. The censuses are
   \((5,2,3)\) and \((7,2,5)\) for
   (admissible, tree-child, non-tree-child) rootings. The labelled mixed graphs
   are nonisomorphic, each has exactly one ordinary triangle, and they remain
   nonisomorphic after forgetting the head flags on those triangle edges.
6. Recomputed the cherry determinant
   \(4u_su_g/(v_sv_g)\), with value \(2464/675\) at the printed physical
   witness.
7. Recomputed \(C(4,1)=831\),
   \(C(4,0)=C(5,1)=1,983\), and \(C(5,0)=4,155\) directly from the binomial
   formula.
8. Checked exact rational points arbitrarily close to the \(D_+\) and
   continuous-time boundaries against every transition-probability inequality;
   no floating-point sign decision was used.

### 3.2 Independent primitive-core and repair enumeration

Command:

```text
.venv/bin/python -B independent_checks/math/primitive_core_enumeration.py
```

Final script SHA-256:
`183d340ee52364abc15e0e48167de2e28f553dde8b54d2960b6465f8b80c712f`.
Output SHA-256:
`eb6ba17f6a46a9f1d7125086098f66432e944af36c76ebddf6e42637918fca96`.
It exited 0 in 0.08 s with peak resident memory 20,086,784 bytes.

This starts only from three abstract pole-to-pole paths. It places one real
incoming source and two reticulation events, tries every segment orientation,
enforces the binary local degrees, reachability, acyclicity, and literal
directed-multigraph isomorphism, and then tests every occupied-segment subset
against graph simplicity and the no-omnian incidence condition. It found:

- 66 raw valid oriented placements;
- exactly four isomorphism classes, one each of
  \(\theta_0,\theta_1,\theta_2,\theta_3\);
- zero valid placements with both poles reticulate;
- minimal repair profiles respectively
  two size-two repairs, two size-two repairs, four size-two repairs, and two
  size-one repairs;
- the two cycle repairs \(\{0\}\) and \(\{1\}\);
- for the exceptional two-boundary \(K_4-e\), exactly 25 admissible
  lowest-stable-ancestor rootings and zero tree-child rootings.

Thus the hand reduction and repair table at article lines 878–1003 are
independently supported from primitive incidence data rather than topology
names.

### 3.3 Independent direct-certificate replay

Command:

```text
.venv/bin/python -B independent_checks/math/direct_certificate_check.py
```

Script SHA-256:
`b85fd57b863ea3ffdc8684d1615b30619ca1e39ce3606f73c9f08a86dc928014`.
Output SHA-256:
`ec59f819aa93536e20c8e06f53b92358e7f8f63faae0a889e7762f3708c14994`.
It exited 0 in 0.34 s with peak resident memory 64,897,024 bytes.

I transcribed the two literal graphs bound to corrected raw row 1849, source
descriptor
`ffa19a908a552bb362e0c840df91c95a7db974f700f8ebc7fcce4ac2e5f55cd0`,
target descriptor
`7d9d43468513d406e3ea0bbea704f91b9f5c1a8dc58e2651aa8af96079478325`,
and port permutation `(0,1,3,2)`. A separate four-switch symbolic expansion
gave, for printed template R4Q-03,

\[
q_{10}q_{20}-q_{12}q_{18},
\]

an identically zero target pullback and a nonzero 44-term source pullback. The
independent `srepr` hash of that source polynomial is
`5632d4b85551dbe62afb95f5bc6eca42692c13215da7ed858461092d747a794e`.
This reproduces the worked path at supplement certificate appendix lines
168–181 using neither the submitted map generator nor its certificate replay.

## 4. Mathematical claim matrix

| Claim layer | Status | Proof locations | Fresh adversarial conclusion | Exact remaining gap |
|---|---|---|---|---|
| Standard fixed mixed graph; admissible rootings; weak/strong tree-child | PASS | article 206–299 (PDF pp. 4–5) | Definitions are quantified correctly. The no-omnian criterion is valid under the binary fixed-graph convention. Weak witnesses independently have both TC and non-TC rootings. | None mathematical. |
| Fourier map, inverse probabilities, \(D_+\), subdivision, root movement | PASS | article 303–413 (PDF pp. 5–6) | Inverse Fourier inequalities give exactly \(0<s,g<1,\ g>2s-1\). Choosing \(r>\max\{s,g,2s-g\}\) proves subdivision. The reticulation-adjacent root case is handled switching-by-switching; no parent complement is silently introduced. | None. |
| Quartet and whole-map tree/sunlet separation | PASS | article 415–527 (PDF pp. 6–7); quartet proof narrative | Corrected equal sector is \(\{C,T\}\). Fresh pullbacks give the printed table and exhaust all seven displayed-set cases. The \(\mathcal T_i\) factor has a fixed strict sign on every interior point. | Finding 1 concerns stale restoration counts in a C02 authority artifact, not these formulas. |
| Tree of blobs and decoration | PASS | article 464–527 | Quartet marginals force the labelled tree of blobs pointwise; \(\mathcal T_i\) distinguishes an ordinary degree-three tree component from a three-cycle. Strong theta supports require at least four physical ports. | Attribution checked; no revoked rooted oracle is used. |
| Complete two-sector bridge fibre | PASS | article 535–691 (PDF pp. 8–10) | All-zero normalization fixes sector 0; positivity and rank-one uniqueness give cut scales; \(C/T\) invariance forces equality of paired scales; \(G\) remains independent. The degree-two stabilizer is real but excluded: fresh \(K_4-e\) census is 25/0. Pair-anchor determinant is \(-2\); peeling a tree leaves no holonomy. | None. |
| Physical local product and simultaneous gluing | PASS | article 642–662, 1277–1330 | Serial three-edge splitting realizes the incidence orbit in the physical cone locally. The explicit small-\(s\) choices make original and both transformed bridge pairs strict. The proof does not claim arbitrary normalized tensors are physical. | None. |
| Paired marginals and parameter transport | PASS | article 693–778 | Products preserve \(D_+\); the displayed \(r^{m-1}\) bound gives surjectivity and analytic sections. Visible signatures justify paired \((S_E,G_E)\) products. Inheritance is complemented only when an actual stored graph transport reverses parent order. | Exhaustiveness of every stored transport is computational. |
| Semialgebraic localization and no remote compensation | PASS | article 780–846 | The finite-cover step correctly selects a fixed target type on a source-open germ. Intrinsic bridge extraction prevents a remote factor from cancelling a local multihomogeneous/rank obstruction. Restoration is explicitly fixed-full and uses source marginal openness only; it never lifts an abstract marginal relation or inverts a target deletion. | All-child coverage is computational. |
| Cycle/theta core and repair universe | PASS | article 848–1039 (PDF pp. 11–14) | Degree excess gives cycle or theta. The pole/sink case split is exhaustive; fresh brute force gives exactly the four orientations and the printed repair profiles, including zero two-reticulate-pole cases. Completion arithmetic is independently exact. | Literal record generation/canonicalization remains computational. |
| Finite certificate semantics | PASS (semantics) / UNVERIFIED here (all rows) | article 1041–1164; supplement 232–440 and generated appendix | Quartet/\(\mathcal T_i\), directed rank, polynomial, restoration, isomorphism, and triangle terminal semantics are logically sufficient and direction-safe. A source minor plus symbolic target upper bound excludes containment; a target-zero/source-nonzero polynomial excludes a source-open analytic relation. R4Q-03 was independently replayed. | This subreview did not independently replay every one of the millions of rows or all 997 parents. |
| PC-PARTIAL boundary | PASS | article 1166–1202; crosswalk 30–45 | The manuscript explicitly retains the 75 exceptional rank representatives, 997 restoration parents, and full probe ledgers. It does not infer graph orbit equivalence from literal polynomial-body equality. | None. |
| Ordinary-triangle common germ | PASS | article 1204–1330 (PDF pp. 17–18) | Exact \(4\times4\) and \(5\times5\) determinants give rank nine. The proof uses the submersion theorem, not a false square inverse. The contextual constant-rank section is correctly composed, and several disjoint triangle factors are handled in one product rank choice. | None. |
| Global equivalence and no one-way containment | PASS | article 1332–1363 (PDF p. 18) | Necessity uses pointwise topology, bridge-local factor extraction, finite local classification, and coherent probes. Sufficiency uses contextual triangle submersions and physical bridge gluing. A common full-dimensional germ with sections gives both directed relations. No circular use of genericity occurs. | Depends computationally on bounded/probe completeness. |
| Generic identifiability | PASS | article 1365–1478 (PDF pp. 19–20) | Complex image closure is irreducible and \(d_N\) equals generic complex rank because the physical domain is Euclidean open. The tree-child path argument proves \(r\le n-1\) and \(|V|\le4n-3\), hence finitely many topologies. Total source rank-drop images have dimension \(\le d_N-1\). A full-dimensional physical competitor intersection yields a target analytic section and contradicts the main theorem. Every component of \(E_N\) is therefore proper. | None. |
| Exact reconstruction | PASS | article 1480–1538 (PDF pp. 20–21) | Exact-input assumptions are explicit. R5 retains every unexcluded local support; R8 uses exact semialgebraic membership and returns a triangle class. No pointwise misuse of a generic rank certificate remains. Finiteness and depth-two restoration prove termination. | No bit-complexity, stability, or finite-sample guarantee is claimed. |
| Strict continuous-time transfer | PASS | article 1540–1588 (PDF p. 21) | \(D_{CT}=\{0<s<1,s^2<g<1\}\) is open in \(D_+\). Positive coordinate roots give subdivisions/marginal sections. The rank-nine triangle witness is strict CT. The explicit \(L,U\) bridge inequalities make all three bridge pairs CT. Polynomial nonvanishing persists on the open cone. | None. |
| Weak-class \(4n-3\) sharpness | PASS | article 1590–1799 (PDF pp. 21–24); supplement 444–560 | Literal graphs, root censuses, nonisomorphism, non-triangle-equivalence, exact common tensor, exact rank nine, physical CT parameters, tensor-observable cherry inverse, determinant, and pruning induction all check. A cherry adds exactly four dimensions, giving \(4n-3\). | My fresh script establishes exact rank nine but does not duplicate the package's specifically named two 9-by-9 minor values; the independent rank result is equivalent for the theorem. |

## 5. Detailed logical scrutiny

### 5.1 Definitions and physical domains

The standard semi-directed construction at article lines 219–229 is genuinely
one-step root suppression: it forbids loops, parallel edges, and loss of a
reticulation arrowhead. Later restriction cleanup is explicitly separated from
the admissible-rooting relation. Thus “strongly tree-child” at lines 240–244
means every admissible rooting, not existence of a favorable rooting.

For spectrum \((1,s,g,s)\), inverse Fourier transformation gives

\[
\frac{1+2s+g}{4},\quad \frac{1-g}{4},\quad
\frac{1-2s+g}{4},\quad\frac{1-g}{4}.
\]

On the positive-eigenvalue component their strict positivity is exactly
\(D_+\). For subdivision, write \(r=1-\varepsilon\). The sufficient and
necessary strict bounds for the residual pair used in the proof are met once

\[
r>\max\{s,g,2s-g,0\},
\]

which is possible because the original pair is interior. This confirms the
article's continuity proof and avoids the false unrestricted square-root claim.

The continuous-time formula is also correct: positive K2P rates give
\(s=e^{-2(\alpha+\beta)t}\), \(g=e^{-4\beta t}\), so \(\alpha,\beta>0\) is
equivalent to \(s^2<g<1\). Since
\(s^2-(2s-1)=(1-s)^2>0\), the strict CT cone is contained in \(D_+\).

### 5.2 Corrected quartet layer

The Englander et al. version-4 paper uses a different naming of the repeated
K2P character sector in its displayed formulas. The revised submission no
longer copies those character names literally. Article lines 433–450 explicitly
state that the present spectrum has equal sector \(\{C,T\}\), give the complete
pullback table, and identify the formulas as the current-coordinate versions of
the literature result. This is exactly the needed correction.

I searched the package for the revoked literal `q_GGGG-q_GGTT`. Its only
remaining occurrence is an intentional mutation designed to be rejected. The
current semantics specification declares character order `(0,C,G,T)`, spectrum
`(1,s,g,s)`, equal sector `{C,T}`, singleton sector `G`, and literal coordinates
`CCCC,CCTT,CTCT,CTTC`. Thus the mathematical article, the current formula
registry, and the mutation target agree.

The mixture argument is pointwise, not generic. Positive inheritance weights
make any topology-specific strict sign survive. Singleton-vs-other displayed
sets use an \(F_t\) witness; two-or-more-vs-two-or-more sets use a membership
\(J_t\) witness for a topology present on only one side. This covers all 21
unordered unequal pairs of the seven nonempty displayed subsets.

### 5.3 Bridge fibres, marginals, and localization

The potential degree-two paired-sector gauge is not waved away. For two
unmarked incidences, \((\rho_1,\rho_2)=(t,t^{-1})\) is a genuine stabilizer.
The retained strong class excludes the only simple reduced two-boundary theta;
my independent \(K_4-e\) enumeration found 25 admissible LSA rootings and no
tree-child rooting. For degree at least three, the equations
\(\rho_e\rho_f=1\) for all pairs and positivity force every \(\rho_e=1\).

The physical product statement is local and correctly weaker than an ambient
tensor claim. Endpoint serial factors near the identity vary the four incidence
directions while the residual bridge stays in \(D_+\). This supplies physical
saturation after shrinking to a constant-rank chart.

The paired serial marginal map is onto. Given \((S,G)\), choosing
\(r^{m-1}>\max\{S,G,2S-G,0\}\) makes the last factor
\((S/r^{m-1},G/r^{m-1})\) strict. The two differential rows have disjoint
nonzero supports. The complete visible-signature proposition correctly treats
\((s,g)\) as a pair and forgets an inheritance parameter only when both choices
are tensor-identical after all other choices are fixed. A complement is licensed
only by a stored parent-order reversal.

The localization proof does not assume that a target type is fixed globally in
advance. It covers the source box by finitely many semialgebraic realization
sets and selects one containing a source-open subgerm. Because the projective
local factor is analytically extractable from the global bridge contraction,
remote parameters cannot cancel a local polynomial or rank obstruction.

Restoration has the required fixed-full quantifiers: start with actual fixed
networks and their full analytic relation, then marginalize that same relation
at the actual source/target attachments. Source marginal openness supplies the
child source germ. There is no inference from an abstract selected relation and
no inverse of an arbitrary target deletion map.

### 5.4 Finite proof semantics and PC-PARTIAL

The hand universe proof is now sufficient to explain why cycle and theta cores
are the only inputs, why the four theta event placements are exhaustive, and why
the displayed repair table is the list of minimal transversals. My independent
event enumeration agrees exactly up to segment renaming.

The completion formula counts repair-tagged directed descriptors, not
isomorphism classes. A named zero-character repair leaf is inserted only when a
required segment's physical word is empty, consumes no selected physical label,
and remains part of the raw descriptor. This makes the stars-and-bars formula
and all four printed values correct.

The six terminal mechanisms are logically adequate:

1. a pointwise strict sign separates complete physical images;
2. if a source germ factored through a target, its rank could not exceed the
   target's maximal rank, so a nonzero exact source minor exceeding a symbolic
   target upper bound excludes the direction;
3. a target-identically-zero polynomial with nonzero source pullback cannot
   vanish on a source-open analytic neighborhood;
4. fixed-full restoration reduces a parent to one of its exhaustive physical
   children;
5. a labelled mixed-graph isomorphism transports all physical parameters;
6. an ordinary triangle has the separately proved rank-nine common germ.

The article correctly refuses to treat equal polynomial bodies as graph-orbit
equivalence. The 75 exceptional rank representatives, all 997 parent
assignments, 36,824 restoration edges, 29,964 one-port rows, 544,571 two-port
rows, exact transports, and parent restrictions remain part of the proof. This
is an honest computer-assisted theorem rather than a falsely compressed hand
classification.

### 5.5 Triangle context, global theorem, and genericity

At the common symmetric CT point, each triangle orientation map is a
submersion onto the nine-dimensional normalized three-leaf K2P tensor space.
No square inverse of the full parameter map is asserted. In context, the map
\(\mathcal H:Q\times C\to Y\) is restricted to a generic constant-rank chart;
its local section is composed with each triangle's physical section. Hence the
same contextual image germ is regular and full-dimensional for every
orientation. For several triangle factors the product submersion is formed
first and the generic context is chosen once, avoiding an invalid induction on
generic contexts.

The proof dependency is acyclic:

```text
pointwise topology + bridge localization + finite classification
    -> necessity of K2P-SAME
triangle submersion + physical gluing
    -> sufficiency of K2P-SAME
K2P-SAME + semialgebraic dimension
    -> generic identifiability
generic identifiability + finite decks + exact membership
    -> reconstruction
```

In particular, genericity is not used to prove the main equivalence. The
genericity proof handles the total source rank-drop image before extracting a
target section. If a competing physical intersection had dimension \(d_N\), a
constant-rank incidence stratum would project with rank \(d_N\), giving exactly
the physical analytic target section forbidden by K2P-SAME. Real
semialgebraic/Zariski and complex dimensions are compared only after that step.

Reconstruction now retains every locally unresolved support until global
assembly. A generic-rank certificate is not misused as a pointwise test. Exact
semialgebraic model membership selects the unique triangle class off \(E_N\).

### 5.6 Weak sharpness

The two base graphs satisfy the binary degrees and level-two condition. My
literal root enumeration agrees with the printed 5/2/3 and 7/2/5 censuses. The
mixed-incidence comparison rules out labelled isomorphism and, after erasing
the only triangle's head flags on both sides, ordinary-triangle equivalence.

All stated internal, pendant, and cherry edge pairs lie strictly in the CT
cone. The exact common base tensor has six two-nonzero coordinates
\(\delta^2\), three all-nonzero coordinates \((4/5)\delta^3\), and full rank
nine on both sides. For a cherry, the ratios and products

\[
(u_s/v_s,u_sv_s,u_g/v_g,u_gv_g)
\]

are tensor observables, have the printed nonzero determinant, and admit the
positive analytic square-root inverse. After recovering the four edge
coordinates, division by a nonzero cherry factor recovers each old tensor
coordinate. This proves both the lower and upper four-dimension increment.
Pruning the newest labelled cherry recovers the base graphs and preserves the
weak-not-strong and non-equivalence properties.

## 6. Numbered findings

### Finding 1 — Current C02 authority contains stale restoration counts

**Classification:** authority-consistency / reproducibility defect; no
mathematical theorem failure.

The theorem/artifact crosswalk
`proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md`, row C02
at line 17, names
`work/adversarial_proof_review/topology_direction_certificate.json` as an
**Authority** for the quartet/tree-of-blobs layer.

That JSON currently asserts:

- `published_ledgers.restoration_quartet = 35758`;
- `published_ledgers.restoration_tree_sunlet = 646`;
- `restoration_topology_binding.displayed_quartet_mismatch = 35758`;
- `restoration_topology_binding.strict_tree_sunlet = 646`;
- `restoration_topology_binding.raw_children = 36568`.

The associated narrative
`work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md`, lines 125–131,
likewise says 646 restoration tree/sunlet children and 36,404 topology-terminal
children.

Those figures are not the revised forest partition. The current authoritative
forest
`work/restoration_sign_reclassification/corrected_restoration_forest.json`
states:

- `census.first_proof_counts.displayed_quartet_mismatch = 35758`;
- `census.first_proof_counts.full_map_Ti_zero_strict_sign = 606`;
- `census.first_proof_counts.exact_multihomogeneous_quadratic = 148`;
- `census.first_proof_counts.inherited_exact_F_2_112_quartic = 24`;
- `census.first_proof_counts.restore_remaining_physical_role = 32`;
- `census.second_proof_counts.displayed_quartet_mismatch = 248`;
- `census.second_proof_counts.full_map_Ti_zero_strict_sign = 8`.

The revised article agrees with the latter at `article/main.tex` lines
1127–1133 (article PDF p. 15), and the supplement agrees at
`supplement/supplement.tex` lines 310–326 (supplement PDF p. 6). Thus the
current total number of topology-sign terminal leaves in the restoration
forest is

\[
35758+606+248+8=36620,
\]

not 36,404. The 646 value is a pre-reclassification aggregate and no longer
describes the current first-/second-layer proof partition.

**Logical effect.** This does **not** invalidate the corrected quartet
predicate, the raw four-port counts 360,408 and 16,974, the fixed-full
restoration lemma, or the current restoration forest. The article's proof uses
the correct current partition, and crosswalk C08 points to the current forest.
The stale C02 artifact is therefore not a counterexample and does not change
the mathematical PASS. It is nevertheless a real inconsistency because the
crosswalk labels the artifact as present authority rather than historical
evidence.

**Smallest adequate remedy.** Either:

1. regenerate the topology-direction certificate and narrative from the
   current first- and second-layer forest, preserving the corrected
   `full_map_Ti_zero_strict_sign` terminology; or
2. formally narrow C02's scope to the raw-four-port quartet/\(\mathcal T_i\)
   predicates and remove the stale restoration fields and claims.

Because the artifact is named in the theorem crosswalk and frozen release
inputs, the crosswalk, source/content manifests, release lock, PDFs if their
printed crosswalk changes, and outer handoff seal require resealing. If option 2
changes only machine scope outside the PDFs, the build inputs need not change,
but every manifest that binds the edited bytes still must.

### Finding 2 — Historical pre-closure narratives are not visibly quarantined

**Classification:** nonblocking presentation/status ambiguity.

- `work/adversarial_proof_review/PROBE_INPUT_CONTRACT.md` lines 5–11 says the
  global theorem “remains blocked” pending corrected probe closure.
- `work/global_theorem_closure/GLOBAL_PROOF.md` lines 3–8 says promotion still
  requires restoration, cycle, probe, and release gates.

Those sentences accurately describe their historical stage, and the promoted
manuscript, current probe proof, article, and release lock close the listed
gates. Neither file is the C11 promoted authority. Nevertheless, a fresh reader
asked to read “authoritative proof narratives” can reasonably mistake these
unbannered stage documents for current status.

**Effect:** none on a theorem predicate or current certificate.  
**Remedy:** add a conspicuous “historical pre-closure input; current status is
in …” banner, or classify these paths as historical in the machine crosswalk.
Any byte edit requires resealing the manifests that bind the files, but no
mathematical replay is required.

## 7. Literature and scope audit

I checked the cited topology claims rather than treating citations as proof of
the new K2P theorem.

- Huber et al., *When Are Quarnets Sufficient to Reconstruct Semi-Directed
  Phylogenetic Networks?*, Lemma 4.2 and Figure 8, supplies the two underlying
  semi-directed level-two generator shapes and proves the broader quarnet/blob
  statements. The publisher's primary page is
  <https://doi.org/10.1007/s11538-025-01510-5>.
- Englander et al., bioRxiv version 4, Propositions 2.9–2.10, Theorem 2.11,
  and Corollary 2.12, supplies displayed-quartet separation and tree-of-blobs
  recovery for JC/K2P. I inspected a current v4 rendition (31 pages, SHA-256
  `69f04a54d7deb5e12485ba566b50bdcffddf5cd1d80c6c7cfb0c656bc504e40d`)
  and verified the cited statements. The article correctly performs the
  one-time character-sector relabel required by its own spectrum convention.
  DOI: <https://doi.org/10.1101/2025.04.18.649493>.
- Brits et al. proves level-one full identifiability modulo triangles under
  JC/K2P/K3P, not the present level-two theorem:
  <https://arxiv.org/abs/2607.12919>.

The four directed incoming-source placements, fixed-port repair grammar,
two-sector K2P bridge analysis, finite directed classification, contextual
triangle gluing, and weak-sharpness construction are proved or certified in
the present package rather than attributed to those papers.

A limited current search found no earlier work stating the same complete
principal-domain strong level-two K2P equivalence. This is search evidence, not
an exhaustive priority guarantee.

The scope exclusions are stated accurately at article lines 1801–1820 (PDF p.
25) and promoted manuscript Appendix B. The theorem does **not** claim:

- a mixed-sign K2P classification;
- stochastic-boundary, singular-edge, or inheritance-boundary results;
- level greater than two or merely weak-tree-child identifiability;
- equality of complete stochastic images;
- individual bridge-parameter identifiability inside the gauge fibre;
- numerical conditioning, bit complexity, finite-sample inference, or model
  selection guarantees.

The weak theorem is correctly presented only as sharpness of the word
“strongly,” not as a classification of all weak networks.

## 8. Unrun gates and handoff to the main referee

By explicit assignment I did not run `run_all_verifiers.py --full`, regenerate
the full raw ledgers, or independently replay every restoration/probe row.
Consequently the following are not certified by this mathematical subreview
alone:

- exactly-once generation of all 405,216 and 2,946,240 raw directions;
- every symbolic rank-upper certificate and all exceptional orbit transports;
- all 997 restoration parents and 36,824 restriction edges;
- all 29,964 one-port and 544,571 two-port rows and 67,741 exact transports;
- fail-closed behavior of the full release harness, ledgers, archive, and
  mutation suites.

Those are computational/reproducibility gates for the other referee tracks.
Subject to their successful independent replay, the revised mathematical
argument supports ACCEPT. Finding 1 must still be resolved or explicitly
classified by the main referee when assigning the package-level
reproducibility status.

