# Structural family report — Kourovka21.126

October24,2026 UTC. **Outcome: unsolved.** Family discovery estimate:7%. No complete super-exponential witness, no superpolynomial subexponential witness, and no full negative answer. Publication and tracker gates remain closed. All assertions below are scoped partial results; originality of the derived lemmas is not established.

## Strongest mathematical findings

1. Every finitely presented **normal** subgroup of a RAAG has δ≼exp. The proof removes non-full join factors injectively, then combines the known finite-by-abelian quotient theorem with the known exponential upper bound for finitely presented coabelian kernels of automatic groups. Finite-index passage handles the finite commutator quotient. It leaves the intermediate branch and arbitrary nonnormal subgroups open.
2. For a finite graph-of-groups subgroup J≤A with polynomially filling vertex groups and free-abelian edge groups satisfying |x|_E≤Cτ_A(x), original-interval tracking in Britton reductions gives an intrinsic polynomial area bound. With vertex degree≤d≥2, the deliberately conservative bound is δ_J≼n^{2d+1}. Ambient RAAGs supply the edge condition by undistortion of their abelian subgroups. Finite generation and presentation of subgroup vertex stabilizers were proved directly, rather than inherited without justification. This gives a clique-amalgam closure of polynomial subgroup exclusions.
3. The house RAAG A(C4)*_{Z²}Z³ has only polynomially filling finitely presented subgroups, with the derived upper bound n^5.
4. Combining this house case with established two-dimensional, coherent-RAAG, and three-limit-factor theorems and a complete five-vertex graph census gives **δ_H≼n^{18} for every finitely presented subgroup of every RAAG defined by at most five vertices**. This is a partial ambient-size exclusion, not a restriction of the Notebook's quantifiers. The exact proof is SMALL_GRAPH_SYNTHESIS.md.

## Established results found during original route development

- Huang–Osajda2019 Corollary1.3 excludes both requested rates in every triangle-free ambient RAAG by a genuine finitely presented subgroup theorem. It supersedes our independently developed forest-only compact-core argument.
- Casals-Ruiz–Duncan–Kazachkov2023 Lemma9.5 gives geometric coherence of coherent/chordal RAAG Salvetti complexes, so their finitely generated subgroups are CAT(0) and have quadratic upper bounds. This supersedes our potential independent chordal consequence and is fully credited.
- Ascari et al.2406.19860v2 TheoremA gives degree9 for finitely presented subgroups of three free factors; Corollary4.8 gives degree18 for at most three **limit** factors. The distinction matters for F2×(Z²*Z), the fifth leftover five-vertex graph.

None of these facts supplies a full answer to21.126. They are prior inputs or derived exclusions, not new complete resolutions.

## Routes attempted and precise gaps

- **Direct normal-kernel construction:** the exponential bound blocks a super-exponential witness normal in an actual RAAG. It does not apply to a kernel normal only in an arbitrary virtually special subgroup. At-most-exponential does not rule out the intermediate branch.
- **Repeated same-height cyclic fibre products:** the exact group is N^m⋊Z, and taking another symmetric same-height product merely adds kernel copies. If the hyperbolic source has a finitely presented kernel, the known polynomial kernel-filling bound and our direct area estimate keep all these groups at most exponential. Polynomially growing monodromy gives a polynomial bound by a separate collection proof that does not confuse reduced iterate length with raw substitution length. No exponential lower bound is asserted from monodromy alone.
- **Large-Dehn quotient in a special Rips fibre product:** a general transfer δ_Q≼δ_P is false. Choose a known type-F3 quotient Q with undecidable word problem; its fibre product P is finitely presented and virtually embeds in a RAAG but has decidable word problem and recursively bounded intrinsic Dehn function. Quotient δ_Q has no recursive upper bound. Bridson2507.17598v2 transfers δ_Q to distortion and conjugator length, and does not transfer it to δ_P. The missing positive ingredient is a lower bound on every intrinsic filling of actual short null words in P.
- **Clique/abelian-edge filling:** the new mechanism closes graph-of-groups routes only when the vertex subgroup filling bounds are independently known. Assuming such bounds for arbitrary larger indecomposable RAAG blocks would merely relocate the original difficulty. That route is blocked at the arbitrary vertex case without a new mechanism.
- **Small ambient search:** exact finite combinatorics identifies all five-vertex exceptions to the first closure criterion and then eliminates each mathematically. This is not an exhaustive search over finitely presented subgroups of larger RAAGs.

## Verification and reproducibility

The fresh adversarial subagent authored no proof and actively tested the normality reductions, source hypotheses, polynomial collection costs, finite-index central-Z argument, compact-core geometry, graph grammar, interval tracking, finite vertex presentations, and house amalgam. Exact receipts and independent standard-library graph enumerators are in review/. Author graph scripts and certificates are at this folder's top level. Run:

    python3 graph_census.py
    python3 dimension_two_census.py
    python3 review/independent_graph_census.py
    python3 review/independent_dimension_two_census.py
    python3 review/independent_small_graph_classification.py

These computations certify only finite graph classifications; the mathematical subgroup filling claims are proved in the notes and reviewed separately. All material conclusions remain supported by explicit arguments and named external theorems.

Raw primary PDFs and extracted bodies are local under sources/ with provenance hashes. The original Scott1973 and Baudisch1981 PDFs were inaccessible; that limitation is disclosed in FORESTS_AND_CLOSURE.md, and their role is now unnecessary for the stronger triangle-free and small-graph synthesis. The independent source checks do not amount to human peer review. AI tools were used throughout this research and verification.

No external communication, git operation, preprint preparation, Zenodo action, journal submission, or Google Sheets mutation was performed by this family.
