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
