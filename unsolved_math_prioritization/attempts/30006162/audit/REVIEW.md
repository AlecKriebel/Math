# Independent adversarial audit: exceptional-surface generic points

**Verdict: PASS_SCOPED_PARTIAL_RESULTS. No mandatory mathematical correction. Both original questions remain unresolved; retain unsolved, 5/5 approaches used.**

This is a fresh, separate AI audit, not human peer review, formal verification, a novelty assessment, or a claim of complete literature coverage. The author freeze was preserved. The audit accepts only the stated necessary conditions and restriction lemma, not a positive or negative answer about either surface group.

## Frozen target and record binding

The reviewed author ZIP has 21,689 bytes and SHA-256 `5981aaf13469525d7984ca3a3f48be5993c2767488773139f18ba48cf464c287`. Its externally pinned manifest has SHA-256 `34cd470aa7970f2ab7414623cb880bedc62c3be665ff050d1afb319f4ed47ccf`. The archive has exactly twelve regular, flat members. Every extracted member was compared to the frozen source and manifest before replay.

The complete original catalog, problem, and research-result datasets were independently hashed. The matched problem is ID 30006162, rank 829, OWR-14299082-004. The statement fingerprint matches. Recomputing the review fingerprint from the entire problem record and the absent-report fallback `{}`, using Python's default JSON serialization with sorted keys, gives `789e495c517ffce08c19dc75da7ce5a50e96969671b3b52b105dea02c6d4b878`. Dataset contents are not included here.

The primary question was independently read and visually inspected on printed p.91, PDF p.17, of [Oberwolfach Report 2/2025](https://ems.press/content/serial-article-files/51347). It asks about Homeo₀(S²) and Homeo₀(RP²), not the related question about a particular chain flow or generic conjugacy classes. The compact-Hausdorff, jointly continuous flow convention is retained.

## Structural results and their hypotheses

[Basso–Zucker v2](https://arxiv.org/abs/2412.05659v2), Theorem 7.7, was checked in the text and visually on PDF p.57. Its first-countability condition is existence of a point of first countability, contrary to the negative wording in the abstract. The hypothesis is a minimal G-extremally-disconnected flow of a Polish group. Application to the universal minimal flow is legitimate; application to an arbitrary minimal flow would not be.

Corollary 7.11 requires a closed presyndetic extremely amenable subgroup. Theorem 7.12 instead characterizes metrizability using a closed co-precompact extremely amenable subgroup. Propositions 7.2, 7.4, 7.15 and 7.16 supply the intermediate-subgroup, composition and inheritance statements used by the author. Their factor orders agree with the report: FUH for presyndeticity, UFH for co-precompactness. These orders must not be interchanged.

[Gutman–Tsankov–Zucker](https://arxiv.org/abs/1910.12220), Theorem 1.1, applies because disk-supported isotopies give local transitivity. It establishes nonmetrizability for both target universal minimal flows. Nonmetrizability alone does not exclude a comeagre orbit or a first-countability point. There is also no zero-dimensionality shortcut here. A connected group acts trivially on a zero-dimensional compact Hausdorff space, since each orbit is a connected image of the group. Each target has a nontrivial transitive compact surface action. Consequently its universal minimal flow cannot be replaced by a zero-dimensional universal flow without a separate, valid theorem. A zero-dimensional auxiliary flow and a metrizable universal flow are different assertions.

## Independent verification of Proposition 1

Write K=G_p. Evaluation is onto: finitely many coordinate-disk isotopies move p along a path to any point. It has continuous local sections, as constructed in [Dirbák, Lemma 5.29](https://link.springer.com/article/10.1007/s00209-025-03918-0). That lemma has no negative-Euler-characteristic assumption. Translating a section gives sections at all points and proves openness of evaluation.

For each open identity neighborhood U, compactness of X applied to the open cover {fUp} gives G=FUK. Separately, compactness applied to {Uy:y in X} gives G=UF'K. The latter are open because evaluation at every y is open. This is a valid proof of both properties, with potentially different finite sets.

K is closed and Polish. The cited inheritance results give GPP(K) iff GPP(G), and metrizable M(K) would imply metrizable M(G), contradicting the credited manifold theorem. If K were extremely amenable, its co-precompactness would already give that contradiction. No claim that compactness of G/K makes K extremely amenable is made.

## Independent verification of Proposition 2

Let A contain at least two distinct points and let delta be its minimum separation. The chosen U depends on A only, not on the eventual finite set F. Uniform displacement less than delta/4 gives separation greater than delta/2 for every pair in uA. For each f in a nonempty finite F, the compact set of pairs with separation at least delta/2 is disjoint from the diagonal. Injectivity and continuity of f therefore give a positive minimum eta_f of image separation. Taking the minimum over F remains positive.

If H preserves A setwise, every element fuh sends A to f(uA), so its pairwise separation is at least eta. The surface group is transitive on ordered pairs of distinct points: after moving the first point, the second can be moved in the connected punctured surface by disk-supported isotopies that fix the first. Thus some element sends two chosen members of A to distinct points closer than eta. That element is outside FUH. An empty F fails trivially. The quantifiers are exactly one U defeating every finite F. H need not be closed.

This also explains the configuration-space hazard. The distinct-point configuration space is noncompact. Its natural compactification admits collisions. The proof does not incorrectly assert a fixed positive separation on that whole compactification; it only obtains one on each fixed finite union of the small-displacement images fUA. The target configuration approaching the diagonal is precisely what defeats that union. Extreme amenability cannot be applied directly to a noncompact distinct-configuration space.

## Independent verification of Corollary 3

Extreme amenability of a candidate H supplies at least one fixed point in the compact surface. Two fixed points, or another finite orbit together with that point, would give a finite invariant set with at least two points, which Proposition 2 excludes. Hence the common fixed point is unique and there are no other finite orbits.

The candidate lies strictly inside K, since K is not extremely amenable. Closedness and intermediate presyndeticity are available. Co-precompactness in G contradicts the known nonmetrizability; co-precompactness in K, composed with that of K in G, produces the same contradiction.

The nonnormality argument is valid. If H were normal in K, the quotient map is open and sends presyndetic covers to finite-left-translate covers of every identity neighborhood in K/H. Inversion, with inverse neighborhoods, supplies finite-right-translate covers. Pulling those covers back gives K=UFH, hence co-precompactness of H in K, a contradiction. Normality in G would imply normality in K. The conclusion is specifically non-co-precompactness in both groups, and nonnormality in both; it is not a classification of all possible certificates.

## Independent verification of Proposition 4 and the newer preprint

Continuity of q at the identity gives a neighborhood U on which |q| is bounded by 1. Presyndeticity supplies a finite F with G=FUH. Two defect inequalities give a bound on |q| over all G whenever its restriction to H is bounded. Applying that bound to g^n and using homogeneity forces q(g)=0. A difference of homogeneous continuous quasimorphisms has the same properties, proving injectivity of restriction. No amenability hypothesis is needed for this lemma; even continuity can be weakened to boundedness on some identity neighborhood.

[Böke v2](https://arxiv.org/abs/2602.10707v2) is dated September 29, 2026, and strengthens the main statement to an infinite-dimensional space of homogeneous quasimorphisms on the projective-plane identity component. Theorem 1.1 and Remark 4.12 support the existence and credited continuity inputs. The latter points to the [Bowden–Hensel–Webb appendix](https://pure.manchester.ac.uk/ws/portalfiles/portal/190304731/quasi_morphisms_on_surface_diffeomorphism_groups.pdf). The homeomorphism continuity mechanism is local boundedness from fragmentation followed by the homogeneous-power estimate. The source metadata distinguish the downloaded arXiv bytes from the separately viewed accepted manuscript.

Restrictions of these functions remain continuous in the subspace topology, and injectivity preserves linear independence. Thus every presyndetic subgroup of the projective-plane group carries infinitely many such restrictions. This conclusion is accepted with its credited preprint input. It is not a negative answer to GPP.

In particular, topological extreme amenability of an arbitrary inherited-topology subgroup must not be substituted for amenability of the underlying discrete group. The usual discrete averaging argument needs an applicable mean and a valid function space. A pointwise compact closure of translates does not by itself make the topological group action jointly continuous. Neither the author nor this audit establishes the missing vanishing result in that generality. This is a stated gap rather than a hidden deduction.

## Transfers, chains and cohomology

The sphere's orientation-preserving subgroup is its identity component and has index two; the projective plane has trivial mapping class group. The report correctly avoids orientation language for RP². Finite index gives presyndeticity, so the full-sphere and identity-component GPP questions are equivalent by the credited theorem.

The antipodal lift argument is sound. Antipodal degree on S² is -1. Of the two commuting lifts of a projective-plane homeomorphism, precisely one is orientation preserving, giving a homomorphism inverse to descent from the closed centralizer. Descent is a continuous bijective homomorphism of Polish groups and is open. It is not descent from every sphere homeomorphism. No unproved inheritance from arbitrary closed subgroups is used.

[BCV v3](https://arxiv.org/abs/2403.08667v3), its definitions, Theorem 1.2, Question 1.4, Proposition 6.13 and relevant parts of Section 7 were checked. The two exceptional surfaces are explicitly left open. Chains are maximal chains of nonempty subcontinua with the double-Vietoris topology. Neither a dense chain orbit, turbulent points alone, nor finite off-by-one amalgamation tests answer the generic-orbit question. The Rosendal condition retains its universal neighborhood/open-set quantifiers and all open refinements.

For clarity, every embedded circle in a closed surface has a local arc separating a sufficiently small coordinate disk, including a globally one-sided circle in RP². Also, that essential one-sided circle has no planar open neighborhood. The report's stated failure of the planar-open-set sufficient hypothesis is therefore correct; global one-sidedness does not remove the local-separation issue.

[Dirbák's surface counterflow theorem](https://link.springer.com/article/10.1007/s00209-025-03918-0) requires negative Euler characteristic, and its construction uses a non-nullhomotopic circle-valued map. Neither target has nonzero integral H¹. For RP², its first homology is Z/2, whose homomorphisms into Z are zero; torsion does not supply the required H¹ class. This excludes that particular specialization, not every possible cocycle.

The adjacent work was fetched at exact commit `91ddfb046912817229202f5478487cf91fcb3e36`: [partial report](https://github.com/AlecKriebel/Math/blob/91ddfb046912817229202f5478487cf91fcb3e36/unsolved_math_prioritization/attempts/30006161/PARTIAL_RESULT.md) and [separate review](https://github.com/AlecKriebel/Math/blob/91ddfb046912817229202f5478487cf91fcb3e36/unsolved_math_prioritization/attempts/30006161/review/REVIEW.md). PR 158 had this head and remained an open draft when checked. Residual thinness and the circular-cover fundamental-group obstruction belong to ID 30006161. They are properly credited, not counted as a new solution or a new approach for that older ID.

## Reproduction and acceptance limits

The frozen author's 2,108 finite diagnostics replayed normally and with optimization, from unrelated working directories and relocated archive extractions. Its 28 integrity rejection controls were independently rerun. A separate checker exhaustively tests finite factor-order and two-defect examples, exact separation inequalities, homogeneity bounds, and torsion controls. Counts and machine results are in the accompanying JSON files.

The audit verifier checks an external manifest pin, exact regular-file inventory, payload sizes and hashes, and executes the already hash-verified checker source in an isolated interpreter. Normal, optimized, relocation and negative controls were run. It neither trusts a cached receipt as mathematical evidence nor imports unchecked local bytecode. These controls establish packet integrity and finite examples only. The infinite topological conclusions depend on the proofs and credited source hypotheses, not on their finite check counts.

No mandatory patch was found. Optional clarity about local separation and the distinction between universal and auxiliary flows is supplied above without modifying the author freeze. Both target answers remain unresolved, and all five authorized approaches remain recorded as used.
