# Consolidated independent cross-review of group 2

Checkpoint: 2026-10-10 14:11 PDT. Completion estimate for the assigned 14-record metadata cross-review: **100%**. **All 14 proposals PASS; no corrections requested.** Remote metadata-only application and post-edit DOI/version/file invariance checks remain the root workflow's responsibility.

The reviewing team independently read every exact deposited PDF text in this group, including bibliographies, assumptions, boundary cases and disclosures. The parent reviewer read the final four manuscripts and separately reread the full bosonic manuscript; the independent subagent read the first ten. Every proposed tag, changed field and citation/dependency relation was compared with the existing metadata and deposited content. This evaluates discovery metadata alignment, not independent mathematical certification or proof of novelty.

All 14 proposal JSON files parse; their unique keyword arrays have 14–18 terms. English is added only where missing. Existing citations are retained. No title, creator, DOI, reserved DOI, version, file, publication date, license or access change is proposed. All 14 source PDF MD5 bindings again match the deposited-PDF catalog. Review acceptance is bound to current patch SHA-256 values in `CROSS_REVIEW_GROUP_2_VALIDATION.json`.

The only description change is on 23203100: one §1-supported sentence states transmissivity range, forward/no-free-feedback resource scope and average-energy convention. A direct string check confirms removing that sentence reproduces the entire old description verbatim. Both reviewers independently checked the false literal consumed-key target versus the positive corrected generated-secret theorem, and all existing external-EPnI, priority, AI, unrefereed and Lean-build caveats remain intact.

New structured links on 23204176 (three) and 23203143 (five) reproduce already cited manuscript sources with modest `references` semantics; they do not assert coauthorship, new priority or formal certification.

| Record | Verdict | Evidence report |
|---|---|---|
| 23204176 | PASS | `CROSS_REVIEW_GROUP_2_A.md` |
| 23203732 | PASS | `CROSS_REVIEW_GROUP_2_A.md` |
| 23203334 | PASS | `CROSS_REVIEW_GROUP_2_A.md` |
| 23203323 | PASS | `CROSS_REVIEW_GROUP_2_A.md` |
| 23203270 | PASS | `CROSS_REVIEW_GROUP_2_A.md` |
| 23203143 | PASS | `CROSS_REVIEW_GROUP_2_B.md` |
| 23203100 | PASS | `CROSS_REVIEW_GROUP_2_B.md` |
| 23203081 | PASS | `CROSS_REVIEW_GROUP_2_B.md` |
| 23202994 | PASS | `CROSS_REVIEW_GROUP_2_B.md` |
| 23202966 | PASS | `CROSS_REVIEW_GROUP_2_B.md` |
| 23196750 | PASS | `CROSS_REVIEW_GROUP_2_C.md` |
| 23191301 | PASS | `CROSS_REVIEW_GROUP_2_C.md` |
| 23191247 | PASS | `CROSS_REVIEW_GROUP_2_C.md` |
| 23181280 | PASS | `CROSS_REVIEW_GROUP_2_C.md` |


# Independent cross-review: GROUP_2 first five metadata patches

Checkpoint: 2026-10-10 14:10 PDT (21:10 UTC). Completion estimate for these five content/patch cross-reviews: **100%**. Conclusion: **PASS for all five**, with no correction requested. Application and final remote invariance checks remain outstanding in the parent workflow.

I read the complete exact deposited-PDF text for each of the five records below, including bibliography and scope/disclosure sections, and compared every proposed metadata field and keyword with the old metadata. The catalog records local PDF checksum matches. The longer Vlasov–Maxwell output was reread across the output-truncation boundary. This is an independent metadata alignment check, not certification of the mathematics or upstream external proofs. No patch, remote record, code, DOI, version, file or git state was modified.

## 23204176 — Rational Hodge classes on mixed products of K3 moduli spaces — PASS

Evidence: `papers/23204176/paper.txt`, all 177 lines / 4 PDF pages. Theorem 1 and §1 specify projective complex K3 bases, smooth projective Gieseker-stable twisted-sheaf or eligible generic Bridgeland-stable moduli, and arbitrary mixed/repeated bases. Proposition 2 and §2 explicitly use rational algebraic correspondences, Tate-twisted Chow-motive splittings and cycle-class pull-push. §3 explicitly withholds arbitrary deformations, singular/semistable or abelian-surface moduli, integral/generalized Hodge and finite-dimensional motives.

Every keyword is supported:

- `rational Hodge conjecture`, `K3 surfaces`, `moduli spaces`, `Hilbert schemes`, `Gieseker-stable sheaves`, `twisted sheaves`, `Bridgeland stability`, `moduli spaces of sheaves`, `mixed products`: exact Theorem 1 objects and quantifiers.
- `Chow motives`, `Hodge classes`, `algebraic cycles`, `Tate twists`, `algebraic correspondences`: definitions and Proposition 2's explicit transfer mechanism.
- `Kuga–Satake`: §1's dependency/provenance account and §3's sharply limited Lean-scope disclosure; the term names a discussed input, not a new theorem by this author.
- `complex algebraic geometry`: the entire complex projective setting.

Added `language: eng` agrees with the deposited manuscript. The title and description are unchanged. Their smoothness/projectivity/stability, inherited-source, mixed-product, no-priority/novelty, AI/unrefereed and no-formalization caveats remain intact.

All three added related links use `references`, which is appropriately modest: Bülles DOI `10.1007/s00229-018-1086-0` is bibliography [3] and the exact motive-splitting input; Arapura DOI `10.1016/j.aim.2006.01.005` is bibliography [2] and credited prior Hodge transfers; pinned OpenAI commit URL exactly matches the existing reference [4] and §1's principal snapshot. They neither attribute coauthorship nor assert formal verification. The old record has no related-identifiers array, so no preexisting relations are dropped. The existing free-text references are untouched.

## 23203732 — L2-acyclicity and cost for a rank-100 amalgam — PASS

Evidence: `papers/23203732/paper.txt`, all 298 lines / 6 PDF pages. §2 gives the rank-100 amalgam and Bernoulli/finite-height actions. Lemma 2 and Proposition 3 give the direct regular-tree convolution, cellular boundary, finite two-dimensional classifying space and all-degree L2-acyclicity independently of cost. §§4–6 clearly retain the upstream positive Bernoulli-cost input and distinguish action cost from group infimum cost.

Every keyword is supported:

- `cost`, `fixed price`, `orbit equivalence`, `measured group theory`, `probability-measure-preserving equivalence relations`: §1 definitions and the relation-level versus group-infimum distinctions.
- `L2-Betti numbers`, `L2-acyclicity`, `asphericity`, `classifying spaces`, `von Neumann dimension`, `regular trees`: Lemma 2/Proposition 3 and Theorem 5.
- `amalgamated free products`, `Bernoulli actions`: exact §2 group/action construction.
- `Fox derivatives`: explicit completed cellular boundary computation in §3, credited to Fox.

English addition is correct. No title or description changes. The existing description retains the independent all-degree invariant calculation, inherited positive-cost proof, intermediate-source warning, prior triage/classical implication, no independent discovery/firstness and AI/unrefereed/nonformal caveats.

Related identifiers are unchanged. Their `references` relations fit bibliography [5] (pinned OpenAI rank-100 cost input), [2] (Gaboriau action invariance), [6] (Popa–Shlyakhtenko–Vaes known implication), and [9] (author's public preliminary triage). The relations do not claim that the new independent cellular proof is inherited from the cost input.

## 23203334 — Finite multispecies relativistic Vlasov–Maxwell — PASS

Evidence: `papers/23203334/paper.txt`, all 595 lines / 10 PDF pages. Theorem 1.1 and §1 specify fixed finite species, strictly positive masses, arbitrary charges, nonnegative compact smooth phase data and compatible `C_b^∞ ∩ L2` fields. They expressly impose no smallness, symmetry or neutrality. §§2–5 keep positive mass-weighted energy, signed source/receiver coefficients and the simultaneous support bootstrap. §6 proves local theory/continuation and §7 states the no-massless/no-noncompact-tail limits.

Every keyword is supported:

- `relativistic Vlasov-Maxwell`, `multispecies`, `global classical solutions`, `kinetic theory`, `partial differential equations`, `collisionless plasma`, `global existence`, `large initial data`, `Cauchy problem`: the exact equation, theorem and no-smallness statement; collisions are explicitly excluded.
- `signed impulse estimates`, `angular occupation`: §§3–5's substantive transfer argument.
- `momentum support`, `continuation criterion`: Theorem 1.1 and §§5–6's finite-time support/continuation mechanism.
- `mass normalization`, `charge-to-mass ratio`: equation (1.1) and §1's distinction between equal-ratio inherited cases and distinct-ratio transfer.
- `energy estimates`: §2's mass-weighted positive spatial/cone budgets.

English addition is correct. Title and description unchanged. Large-data/global terminology does not erase the explicit compact-support, positive-mass, fixed-species and bounded-field-derivative assumptions in the description. The description keeps inherited universal cancellation, distinct-ratio coefficient transfer, source attribution, AI/unrefereed/no-firstness and no formalization.

The unchanged pinned OpenAI snapshot with `isDerivedFrom` is consistent with §1/[1]'s exact one-species analytic dependency. No link implies that the fixed finite-species coefficient transfer was already in that source.

## 23203323 — A priori estimates across the subcritical Lane–Emden hyperbola — PASS

Evidence: `papers/23203323/paper.txt`, all 225 lines / 5 PDF pages. Theorem 1 requires n≥3, p,q>1 and the strict subcritical hyperbola for the unweighted classical system. Its conclusions include proper-domain/gradient/exterior estimates, zero-Dirichlet half-space nonexistence and fixed bounded C2-domain strong compactness in precisely stated spaces. §§2–4 reconstruct the inherited doubling and boundary blow-up machinery and prove strong compactness using Sobolev and Schauder estimates; §5 explicitly withholds critical/supercritical, weighted, weak-solution and parabolic claims.

Every keyword is supported:

- `Lane–Emden system`, `elliptic systems`, `subcritical Lane–Emden hyperbola`, `semilinear elliptic equations`: equations (1)–(2) and exact strict scope.
- `a priori estimates`, `Liouville theorems`, `gradient estimates`, `exterior decay`: Theorem 1 and §§2–3.
- `Dirichlet problem`, `half-space nonexistence`, `boundary blow-up`, `doubling lemma`: exact established reductions discussed in §§2–4.
- `strong compactness`, `Sobolev estimates`, `Schauder estimates`: exact function-space conclusions and §4's norm-convergence proof.

Removing the generic original `consequence note` keyword does not remove its status from the unchanged description. English addition is correct. The title/description retain strict exponent/dimension scope, inherited Liouville and reduction inputs, no first-priority or independent-solution claim, exact spaces, Lean rebuild limits and AI/unrefereed status.

Existing relations are unchanged: the source manuscript is `isDerivedFrom` and PQS/Quittner–Souplet links are `references`, matching [1]–[3] and their distinct roles. The arXiv DOI targets an existing cited source; the patch adds no stronger semantic relationship.

## 23203270 — Explicit complex polynomial retract in five variables — PASS

Evidence: `papers/23203270/paper.txt`, all 292 lines / 6 PDF pages. Theorem 1 and §§2–3 supply split complex-algebra homomorphisms, a five-component idempotent polynomial endomorphism and a smooth integral transcendence-degree-four image. The nonpolynomiality is an explicitly external cancellation theorem. §1 and the dependency account discuss locally nilpotent derivations; §4 separates exact symbolic identities from written nonpolynomiality and unreproduced Lean build. Ambient dimension four is expressly not settled.

Every keyword is supported:

- `Costa retract question`, `polynomial retracts`, `algebra retracts`, `retracts of polynomial rings`, `split algebra homomorphisms`: §1's definition and Theorem 1's split maps.
- `affine-space cancellation`, `Zariski cancellation problem`, `polynomial cylinder`: the stated inherited cancellation problem and `A[w] ≅ C[5]` input. Zariski cancellation is the standard name for this precise affine-space cancellation problem.
- `complex affine geometry`, `complex affine five-space`, `smooth affine varieties`, `idempotent polynomial map`: exact complex ambient space and image conclusion; direct smoothness proof and zero-fiber computation in §3.
- `locally nilpotent derivations`: §1's pivotal input mechanism and §2's cylinder-coordinate exponential derivation.
- `exact symbolic verification`: §4's polynomial-identity certificates, correctly distinct from proof of nonpolynomiality.

English addition is correct. Title/description unchanged, including the inherited nonpolynomiality and classical Nagamine implication, five-variable limitation, no four-variable solution, priority audit limits, AI/unrefereed/no complete formal-verification and original-versus-third-party licensing disclosures.

Related links unchanged: `isDerivedFrom` for the pinned explicit cancellation input, and `cites` for Nagamine's prior classical cylinder-to-retract implication, agree with bibliography [6] and [2]. No relation confuses newly written transport formulas with the upstream construction.

## Overall conclusion

All five patches are content-aligned and preserve mathematical scope and attribution. Every tag names an actual theorem object, method, problem synonym or explicitly discussed dependency; no tag advertises an excluded extension. Only 23204176 adds related links, all already documented in its deposited bibliography and existing metadata references. No genuine issue found. **PASS**.


---

# Independent cross-review: GROUP_2 middle five metadata patches

Checkpoint: 2026-10-10 14:10 PDT (21:10 UTC). Completion estimate for these five content/patch cross-reviews: **100%**. Conclusion: **PASS for all five**, with no correction requested. Remote application/invariance verification remains outstanding in the parent workflow.

I read the full exact deposited PDF text for each record, including proof, bibliography, boundary cases and disclosure, then compared all proposed metadata fields and every keyword with the original metadata. I independently evaluated the bosonic description without relying on the separate reviewer's conclusion. JSON validation confirmed allowed fields, unique 16–17-tag arrays, appropriate English additions and no dropped existing related identifiers. No patches, remote data, code or git state were edited. This assesses discovery metadata/content consistency, not independent certification of the upstream mathematics.

## 23203143 — Wreath products and planar triangle bounds — PASS

Evidence: `papers/23203143/preprint.txt`, all 398 lines / 8 PDF pages. §1 identifies Kourovka 21.22's standard restricted regular wreath question and a separate planar triangle Fourier problem. Theorems 1–2 give finitely generated Hopfian lamp/acting groups whose wreath is non-Hopfian, with explicit split epimorphism and kernel; the general reduction and external direct-finiteness counterexample are credited. §§3–4 define real Schwartz two-/three-point programs, prove triangular-lattice Poisson lower bounds and use the established product-program comparison and the external sharp planar certificate for `L2=2/√3`, `P2=4/3`. They expressly distinguish an infimum comparison from optimizer attainment or literal product feasibility.

Every keyword is supported:

- `Hopfian groups`, `restricted regular wreath products`, `direct finiteness`, `group algebras`, `non-Hopfian groups`, `split epimorphisms`, `Kourovka Notebook Problem 21.22`: §1 and Theorems 1–2, including the finite-support lamp and regular-action requirement.
- `Cohn-Elkies bounds`, `planar circle packing`, `triangle three-point bounds`, `sphere packing`, `Fourier analysis`, `Poisson summation`, `linear programming bounds`, `Schwartz functions`, `triangular lattice`, `positive definite kernels`: exact definitions, Poisson/product proof and external certificate in §§3–4. General sphere-packing terminology names the established framework; it does not advertise another-dimensional equality.

All five added `references` links are exact deposited bibliography entries: pinned direct-finiteness PDF [7], pinned planar Fourier certificate [8], Bradford–Fournier-Facio DOI `10.1007/s00209-024-03589-3` [4], Cohn–de Laat–Salmon `arXiv:2206.15373v1` [10], and Cohn–Elkies DOI `10.4007/annals.2003.157.689` [13]. `references` does not overstate coauthorship, originality or formal verification. The original record had no related-identifiers array, so none are removed.

Title and description unchanged. The existing English field is preserved. The generic verification keyword is dropped while verification content remains in the description. The unchanged description retains independent/inherited distinctions, source attribution, no first-priority claim, planar-only/nonattainment caveats, AI/unrefereed/no-endorsement and unrelated-Lean-artifact limitations. PASS.

## 23203100 — Bosonic dynamic capacities and consumed-key secrecy — PASS

Evidence: `papers/23203100/paper.txt`, all 345 lines / 7 PDF pages. §1 explicitly restricts the capacity discussion to the one-mode pure-loss channel, vacuum environment and `η∈[1/2,1]`, states the average photon constraint over messages/shared key/encoder randomness, permits arbitrary internal multimode entanglement, and uses signed forward finite-gross-resource rates with no free feedback. §2 derives multimode entropy transfer from external EPnI; Theorem 3 gives the inherited classical/quantum/entanglement capacity region. §§4–5 carefully separate a false literal joint-consumed-key secrecy model from the repaired positive theorem.

Independent sentence-by-sentence description audit:

1. **Original sentence retained verbatim**: external finite-energy multimode EPnI supplies the previously conditional classical/quantum/entanglement capacity premise, with arbitrary entanglement across uses. Supported by abstract and §§1–3. It does not claim a new EPnI proof.
2. **Only added sentence**: one-mode channel with `1/2 ≤ η ≤ 1`, forward accounting without free feedback, average constraint over messages/key/randomness rather than peak/per-codeword. Every clause is explicit in §1. The sentence supplies genuine missing scope and makes no new theorem claim.
3. **Original operational-defect sentence retained verbatim**: the printed catalytic criterion protects consumed key jointly with generated secrets and excludes the one-time pad. §4, equation (10), uses uniform `U=(M,T_A,J,S_B)` independent of public/environmental `Z`; it demands mutual independence of all private registers.
4. **Original zero-energy-counterexample sentence retained verbatim**: Proposition 4 forces a trivial generated register as reliability/secrecy errors vanish under the literal model, even with consumed resources. Yet the displayed N=0 region includes `(-1,1,-1)` for a one-time pad; its joint-consumed-key trace distance is `2(1-1/d)`. The description correctly presents this as a refutation of the literal region, not failure of EPnI.
5. **Original repaired-private-region sentence retained verbatim**: §5 equation (11) protects only generated `W=(M,T_A)` jointly from public transcript/Eve. Consumed `V=(J,S_B)` may correlate and is not delivered to Eve as an extra side channel. Theorem 5 gives the closed public/private/key union under this stated correction, with explicit converse accounting and key-assisted coding. The sentence does not equate the corrected convention with the literal one.
6. **Original inherited-formulas/no-independent-proof/no-false-unchanged-target sentence retained verbatim**: §1 and §7 expressly preserve inherited formulas/coding machinery and refutation of the unchanged target.
7. **Original upstream-unrefereed-audit/unreproduced-Lean sentence retained verbatim**: §§2 and 7 retain the external proof dependency and build limitations.
8. **Original AI-use sentence retained verbatim**: disclosure confirms extensive AI research/drafting/verification.
9. **Original no-human-peer-review/refereeing sentence retained verbatim**: disclosure and original metadata agree.

A direct string check verified that deleting the single added scope sentence from the new description reproduces the entire old description exactly. No previous sentence, caveat or attribution was changed or shortened.

Every keyword is supported:

- `bosonic channels`, `pure-loss bosonic channel`, `multimode bosonic systems`, `average photon constraint`, `quantum information theory`: exact §1–2 setting and energy model.
- `dynamic capacity`, `capacity regions`, `classical-quantum-entanglement trade-off`, `entanglement-assisted communication`: §3's theorem and father/noiseless conversions.
- `entropy photon-number inequality`, `EPnI`: explicitly credited external entropy theorem and transfer.
- `consumed secret key`, `public-private-secret-key trade-off`, `trace-norm secrecy`, `one-time pad`: the §4 refutation and §5 corrected model; no tag asserts secrecy after revealing consumed key or semantic security for arbitrary messages.
- `degradable channels`: §2's degradation and §5's pure-refinement converse, valid in the expressly stated transmissivity interval.
- `Gaussian ensembles`: §3 thermal displacement and §5 coherent Gaussian construction, with §6 finite approximation.

English addition is correct. All related identifiers are unchanged: Wilde–Hayden–Guha DOI `10.1103/PhysRevA.86.062306` is [2] (`references`); the pinned EPnI source is [1] (`references`); the author's package is appropriately `isSupplementedBy`. Scope remains one-mode pure-loss capacity, average energy, finite gross resources, no free feedback/stronger energy/semantic-security/thermal-channel/amplifier/two-way extension. PASS.

## 23203081 — Even Minkowski uniqueness — PASS

Evidence: `papers/23203081/paper.txt`, all 268 lines / 5 PDF pages. Theorem 1 distinguishes smooth strictly positive even density uniqueness for `0≤p<1`, n≥2, from arbitrary full-dimensional symmetric-body measure uniqueness only for `0<p<1`. §1 defines support functions, Lp surface-area/cone-volume measures and Wulff shapes; §2 gives nonsmooth first variation/mixed-volume rigidity; §3 the smooth p=0 transfer; §4 supplies credited existence/regularity and an equal-volume-box counterexample to arbitrary-measure p=0 uniqueness.

Every keyword is supported:

- `convex geometry`, `logarithmic Brunn-Minkowski inequality`, `log-Minkowski problem`, `Lp-Minkowski problem`, `origin symmetry`, `uniqueness`, `even Minkowski problem`, `smooth uniqueness`: exact theorem/source/target and parity restrictions.
- `surface-area measures`, `cone-volume measure`, `support functions`, `Monge–Ampère equation on the sphere`, `positive Gauss curvature`: §1 definitions and equation (2) with its positive curvature matrix, Theorem 1 and §4 regularity.
- `Wulff shapes`, `mixed volumes`, `first variation`: explicit W[a] construction, Lemma 2 and Proposition 3's mechanism.

Only keywords change; existing language/title/description are preserved. The detailed description keeps the nonarbitrary p=0 scope, box counterexample, existence/regularity attribution, inherited logarithmic inequality, no first-announcement claim and AI/unrefereed/Lean-build caveats.

Related links unchanged: pinned logarithmic Brunn–Minkowski source [1] and He–Liu `arXiv:2510.21530v1` [4] both use `references`, correctly naming substantive input and established endpoint transfer. PASS.

## 23202994 — Hypersingular Riesz-energy constants on surfaces — PASS

Evidence: `papers/23202994/paper.txt`, all 267 lines / 5 PDF pages. Theorem 1 gives the ordered-pair d=2 hypersingular constant for every real s>2, covolume-one triangular-lattice Epstein sum, ambient Euclidean distance and positive-area smooth compact embedded surfaces including smooth boundary. §2 proves centered-disk periodic limits and positive-gap periodization; §3 lattice crop upper bound; §4 applies the corrected rectifiable-manifold universality theorem. §1 explicitly withholds microscopic crystallization, finite-minimizer uniqueness, s≤2, other dimensions and second-order terms.

Every keyword is supported:

- `Riesz energy`, `hypersingular energy`, `minimal discrete energy`, `surface asymptotics`, `smooth embedded surfaces`, `ordered-pair energy`: definitions and Theorem 1.
- `triangular lattice`, `universal optimality`, `Epstein zeta function`, `covolume normalization`: actual substantive external input and exact Z_s normalization.
- `rectifiable manifolds`: the established universality theorem used in §4, whose exact smooth-surface application is stated. This term names a genuine cited method class and adds no rough-set extension to the conclusion.
- `sphere energy`, `chordal distance`: explicit unit-sphere specialization.
- `periodic configurations`, `gap periodization`: Lemma 2/Proposition 3's exact transfer, with prescribed limit order.
- `Brauchart–Hardin–Saff conjecture`: §1 identifies only its d=2, s>2 part as the target.

English addition is correct. Title/description unchanged; all pair/density/dimension/exponent/distance conventions, inherited reductions/attributions, exclusions and review/formalization limitations remain intact.

Existing `isDerivedFrom` for the pinned universal-optimality PDF agrees with bibliography [7] and the principal theorem input. `references` links agree with [2] (Hardin–Saff manifolds; DOI `10.1016/j.aim.2004.05.006` in old metadata), [5] (periodic energy; `10.1063/1.4903975`) and [6] (thermodynamic hypersingular energy; `10.1007/s00365-018-9431-9`). None were altered. PASS.

## 23202966 — Binary relation-liveness automata — PASS

Evidence: `papers/23202966/paper.txt`, all 284 lines / 6 PDF pages. §2 defines strict h² adjacency-block binary coding, malformed-word rejection and exact one-way source sizes, with an h³ fooling set. §3 constructs sh²-state target pullback. Theorem 4 applies the two external growing-alphabet obstructions to fixed-binary deterministic simulation and full-universe nondeterministic complement, giving `2^Ω(h)=2^Ω(n^(1/3))`. Endmarkers, stays, partial transitions, loops and zero-/positive-step acceptance are explicit. §4 withholds `2^Ω(n)` and L≠NL/uniform-small-table implications.

Every keyword is supported:

- `two-way finite automata`, `Sakoda-Sipser`, `binary alphabet`, `state complexity`, `one-way nondeterministic finite automata (1NFA)`, `two-way deterministic finite automata (2DFA)`, `two-way nondeterministic finite automata (2NFA)`: exact source/target models and §1 provenance.
- `nondeterministic complementation`, `deterministic simulation`, `state lower bounds`, `relation liveness`, `read-only automata`: exact two target obstructions, explicitly unlike rewriting 1-limited automata.
- `adjacency-bit encoding`, `fixed-length coding`, `fooling sets`: explicit Sections 2–3 mechanisms and witnesses.
- `stretched exponential lower bounds`: precisely the exponent measured against cubic binary source size; it usefully avoids suggesting a linear-in-source-size exponent.

English addition is correct. Title/description unchanged, retaining exact endmarked/ordinary state counts, full-complement semantics, inherited obstructions and coding machinery, cubic source size and all AI/unrefereed/Lean-build caveats.

Both unchanged `isDerivedFrom` links exactly name bibliography [2] and [3]'s separate deterministic-liveness and nondeterministic-complementation inputs. No new relation merges or enlarges these scopes. PASS.

## Overall conclusion

All five patches are content-aligned and retain the required boundaries and provenance. Wreath/triangle adds five already-cited references. The only description edit, on bosonic capacity, is a single correct scope sentence with the entire original text preserved verbatim. Every keyword was checked, with no excluded extension or unsupported priority/formalization advertised. No genuine issue found. **PASS**.


---

# Independent group-2 cross-review: final four records

Checkpoint: 2026-10-10 14:08 PDT. Completion estimate for this four-record content cross-review: 100%. All four exact deposited-PDF text extracts were read in full, and current metadata was compared with each proposed changed-fields-only patch. No patches were edited or applied.

## 23196750 — Fixed moment separator: PASS

Reviewed `papers/23196750/fixed_moment_separator.txt` (all 5 PDF pages), existing record metadata and `patches/23196750.json`.

All 18 keyword terms are supported: the truncated moment problem/fixed separator/normalization/unit ball are the question and Theorem 1; sum of squares, rational/SOS certificates, Scheiderer quartic and rational sums of squares are the exact field-dependent construction; quadratic and Archimedean modules are defined in §§1–2; the Putinar Positivstellensatz and real algebraic geometry/polynomial optimization occur in the rational strict-positivity discussion and cited Powers/Nie applications; the Galois obstruction is proved in Lemma 1; representing measures and the non-PSD moment matrix are explicitly treated; Gram spectrahedra is a directly cited predecessor used to explain rational factors versus rational PSD Gram data. Topic keywords do not suggest that the presented moment matrix is PSD: the unchanged description expressly says it is not.

The patch adds English and replaces keywords only. No title, description, related identifier, author, DOI, version, file, publication date, rights or access change. The preserved description retains the exact rational-square-factor convention, arbitrary finite multiplier degrees, minimum-one boundary, different rationally certifiable separator, positive rational rescalings, strict-margin exclusion, prior quartic/local/SDP mechanisms, bounded priority search and AI/unrefereed/no formal certification. No substantive caveat is lost.

## 23191301 — Fixed odd-power SOS nonconvexity: PASS

Reviewed `papers/23191301/odd_power_sos_nonconvexity.txt` (all 6 PDF pages), existing record metadata and `patches/23191301.json`.

All 17 keywords match the actual claim and proof: sum-of-squares cones/odd powers/nonconvexity/nonnegative and sextic forms/fixed-exponent convexity/Reznick question are §1's fixed-power sets and result; modified coefficient-1 Motzkin polynomial is §3's credited seed; truncated functionals/pseudoexpectations/tensor product moment matrices are the finite product-positivity mechanism in Lemmas 1–2; SOS separation is classical finite-dimensional separation; Schur complements and exact rational certificates are Proposition 1's 220-by-220 local matrix certificate. Polynomial positivity and real algebraic geometry describe the subject rather than an unstated broader theorem.

The patch adds English and replaces keywords only. Existing description remains exact: explicit sufficient dimension 3*10^62 at q=3, a q-dependent finite dimension for every odd q>=3, no ternary/minimal/uniform-dimension/classification conclusion, credited seed and product/counting tools, analytical product/general-q proof, bounded priority, extensive AI use and unrefereed/no formal certificate. It does not confuse convexity of the union over exponents with convexity at a fixed exponent. No actionable issue.

## 23191247 — Focal antipedal sum equality, k603: PASS

Reviewed `papers/23191247/focal_antipedal_sum.txt` (all 4 PDF pages), existing record metadata and `patches/23191247.json`.

All 15 keywords identify the actual elliptic billiard/Poncelet/confocal-antipedal geometry, focal ordinary Euclidean distance sums, telescoping mechanism, source label k603, admitted odd primitive periods and star polygons. “Billiard dynamics” and “plane geometry” accurately describe the model; “Poncelet families” is an explicit consequence. No keyword claims either individual sum is invariant. §§1–3 establish equality via a per-edge norm difference proportional to vertical displacement, then closure; caustic-on-left orientation is made consistent and reversal/repetition are included.

The patch adds English and replaces keywords only. The preserved description explicitly restricts strictly nested elliptical caustics and excludes hyperbolic/degenerate cases; it preserves original-polygon scope, odd periods, stars, reversal/repeated traversal and no separate-sum constancy. Existing AI/unrefereed/priority qualifications and known focal-height/central-symmetry/telescoping attribution remain. No actionable issue.

## 23181280 — Aggregate root-dependent spanning-tree cost: PASS

Reviewed `papers/23181280/root_dependent_spanning_trees.txt` (all 4 PDF pages), existing record metadata and `patches/23181280.json`.

All 15 keywords are supported. Spanning trees/arborescences/rooted orientations/root-dependent costs/all-root cost/whole-tree arc costs identify §1's exact common-tree objective. Strong NP-completeness and bounded integer costs are Theorem 1 and Corollary 1: costs {0,1,2} and shifted {1,2,3}. The 3-SAT/satisfiability reduction with at-most-three literal clauses is §2. Extended formulations and spanning-tree polytope are the Kaibel/Martin motivation in §1; the manuscript carefully distinguishes integral projection from a fully integral joint lift. Combinatorial optimization/computational complexity and Kaibel's arborescence problem are appropriate subject/problem terms.

The patch adds English and replaces keywords only. Description remains precise about independently supplied costs for every whole root orientation of the same undirected tree, bounded costs, Problem 1/report chronology, finite checks, bounded priority and AI/no human refereeing. The patch neither claims a standard minimum-spanning-tree problem is hard nor extends to the neighboring Problem 2. No actionable issue.

## Scope and remaining work

The four source/patch comparisons pass. No new link or description requires repair for these four records. This cross-review assesses metadata alignment, not novelty certification or a new mathematical proof audit. Final metadata-only remote edit/readback remains the parent workflow's responsibility.
