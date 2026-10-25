# Independent adversarial review — Zenodo 22729545

**Conclusion: no substantive defect found in the reviewed version, within its stated strict domain.** This is an independent AI mathematical/source review with exact supporting calculations. It is not human peer review, a mechanized proof, a novelty certification, or evidence that the inverse is practical with noisy finite data.

Paper: *Raw Strongly Tree-Child Level-2 Species Networks from Metric Genealogy Laws under the NMSC: Signed pair co-occupancy, rooted graph reconstruction, and demographic fibers*, v1.0.0, manuscript dated 5 September 2026, [Zenodo record](https://zenodo.org/records/22729545).

## Immutable scope and independence

Read every page of the main paper (21 pages) and supplement (11 pages). The fresh public PDFs agree with the supplied original hashes; fresh extracted text is byte-identical to the original complete text read. Bindings:

- Main PDF SHA-256: `2b5ddc6da8cf02d084ae034a2d23328f6633b1cb91e6dd809df6cd6863e4e33e`.
- Supplement PDF SHA-256: `9bfb1431b2cd84a000ba820ef30e18e3e10b4d83475380066a0b042c80062560`.
- Source ZIP SHA-256: `61a605db1ad090498fb26e26a63768c0aad4a1ea5ce2849c62b865a45feb2da8`.
- Reproducibility ZIP SHA-256: `90ea0c85320a110d0766956e35739cd165adadda7a5b67dab491f9aad6aa89be`.

`source-bindings.json` and `source-receipt.json` bind this review to the fresh acquisition. No prior or sibling B reviewer verdicts were consulted. The previously completed independent A review supplied only checked mathematical imports, explicitly separated below. Published mathematical code and expected finite check outputs were examined and replayed; their favorable results were not treated as proof of the universal claim. Fresh controls import no published code.

## Exact claim assessed

On finite rooted binary **strongly tree-child** networks of level at most two per undirected blob, with known surjective sample-to-taxon map, positive finite rates, finite piecewise-constant demographic words, interior independent Bernoulli inheritance, contemporaneous samples, and **distinct absolute ages of all distinct internal biological events**, equality of the normalized complete rooted metric-genealogy law is equivalent to the declared Q1–Q8 raw quotient. Every taxon is sampled, but its sample count may be one or larger. The ancestral root population has a positive constant final tail, ensuring complete coalescence.

The quotient retains exposed incidences, event ages, rate words and typed inheritance weights while removing the specified unary data, parent presentation, equal-rate subdivisions and bi-unary sister direction with donor-word transfer. All indexed pair/triple marginals on the original label set suffice. This is not recovery of an arbitrary raw graph without quotienting. It is not a generic-only result or a claim that one selected triple suffices.

## Proof audit and attempted falsification

### Observation to current grouping

Main Section 3 and supplement Sections 1–3 correctly use *unnormalized* survival mass. On a boundary-free interval, pair survival is a finite positive mixture of exponentials plus a constant separated-lineage mass. Analytic uniqueness and positivity distinguish exponent zero even when positive rates coincide. Comparing two models away from the union of their finite boundary sets avoids assuming that hidden boundaries are already observed. The triple formula correctly has initial total rate `3λ` for an all-together triple, a specified first-merger factor `λ`, and post-merger pair survival `exp(-λw)`. Taking the long frozen continuation limit removes the all-together contribution and integrates the desired present grouping. The continuation is an exact-law identifiability device, not a claim that the physical network stops changing.

Sampling consistency is appropriate for independent block routing and the Kingman coalescent. No historical-route projector is silently assumed. In particular, supplement Example 6.5 correctly explains why a historical selector need not descend to a quotient of future behavior; the current proof uses observable current masses instead.

### Signed jumps and global graph

At a tree join, all pair co-occupancy jumps are nonnegative with cross-child support; at a reticulation they are `-2γ(1-γ)` times the surviving child-pair mass. No merger atom occurs at a prescribed biological time. Strict positivity prevents loss of feasible supports; temporal separation is needed to read distinct events without cancellation.

The tree-only witness argument gives nonnested clusters for incomparable vertices. Distinct reticulation clusters are strictly different; incomparable reticulations sharing descendants would force a third reticulation into a common undirected cycle, violating level two. Thus clusters plus observed chronological order recover the reachability poset, including equal-cluster comparable vertices. Transitive reduction alone loses shortcuts, but the positive support at a deficient tree tail recovers the target cluster except for the stated two-singleton pendant sister triangle. The proof explicitly distinguishes that ambiguity from a singleton terminal whose outside-parent incidence is already a cover.

I checked the potentially difficult comparable-reticulation case: if the lower reticulation's sole child edge were in its level-two blob, a path avoiding that reticulation would first reenter its descendant set at a third reticulation. This supports the bridge fact used later. Fresh graph and exact probability controls below also exercise nested/multiple blobs and this case.

### Incidence-linked demographic words

An ordinary-arc tree-only witness occupies that arc deterministically, giving `λ=f/q` where exposure is positive. For a reticulation with parents at `a1<a2`, the earlier parent's ordinary-side witness is disjoint until `a1`, and the longer arm is inaccessible to side entry until `a2`. This makes the oriented anchor jump equal to `γ`.

The triple first/second merger construction in main Lemma 5.3 selects the earlier parent arm by the support of its second merger, not by an unobserved route tag. Its initial mass is taken from its own selected triple. Dividing the ordered-merger density recovers `g1=λ1 exp(-Λ1)`; integration gives its strictly positive survival and then its rate. The pair density recovers the other arm. Equal rates and inheritance one-half do not defeat this ordered-merger separation.

For the longer arm, I specifically attacked omitted bypass histories and circular inversion through another reticulation. With no prior reticulation in its blob, the initial known-chain mass is the observed co-occupancy minus the isolated-arm mass, so bypass is included; later tree-join increments belong to that chain. When an earlier reticulation lies in the same blob, the lower child bridge forces the sampled descendants through the lower reticulation; forward propagation uses already recovered ancestor parameters. The longer arm remains inaccessible, so its isolated surviving mass is the positive remainder. The proof's ancestor-first ordering is sufficient and does not use the unknown longer-arm rate to compute the subtractand.

### Quotient, small marginals, and core enumeration

Q8 is necessary: a singleton reticulation's hidden clock and unary rates affect no selected merger before its two typed parent exits. Q6 is valid only with transfer of the **entire** exposed donor word; a single donor-rate value does not suffice. For an exposed side, the split-pair positive constant atom distinguishes its local germ from an unsplit positive-rate single population. The strong-fan stopping argument prevents an arbitrary hidden routing network from being smuggled into the two-outlet macro. The deterministic normalization permits compound Q6–Q8 macros without claiming a distinguished hidden biological clock.

All indexed small marginals refer to one fixed original labelled sample set. The pair laws first fix one common graph and age coordinate; later triples identify parameters on that graph. This avoids independently choosing incompatible triple carriers. Main Theorem 7.3 and its eight-lineage corollary therefore do not assert a minimal bound or a single-query bound.

The five-core/twelve-minimum-repair result has a separate binary cyclomatic-number argument and bounded exact enumeration. It is not used to extrapolate arbitrary decorated graph identifiability from a finite table. I checked that the universal inverse instead uses the cluster/support argument. No defect was found in the stated core scope or its relation to the global proof.

## Reproduced support and fresh controls

`replay-full.json` reports integrity verification of all 64 indexed files and eight successful replay groups in a temporary copy confined to this review folder:

1. 96 exact raw numerical identities.
2. 628 minimum-core signed-support rows and two Q6 comparisons.
3. 504 additional-port rows at the stated finite domain.
4. Balanced-word, bypass/tree-join and upper-reticulation formulas with rejected wrong formulas.
5. 12 worked-inverse symbolic identities and four rejected wrong formulas.
6. Semantic verification of the finite literal-cylinder certificate.
7. 90 canonical exact tests, including 13 exposure-loss tests.
8. 57 killed executable mutation records in 56 conceptual groups.

Fresh `independent_controls.py` generates 160 seeded binary tree-child networks with 3–8 taxa, up to four attempted reticulation insertions, and level at most two per blob. It excludes a root directly parented to a reticulation to avoid conflating root-suppression conventions in this extra check. Random one/two samples per taxon are used. Thirty-nine networks have more than two reticulations overall. No published code is imported. Rational killed-pair propagation checks 3,791 pair laws and 36,743 biological transitions against the signed-support formulas; graph checks cover 16,122 cluster comparisons, 206 reticulation-cluster comparisons, 168 shortcut completions and 50 lower-sink bridge instances. Eighty repeated-rate frozen-germ controls recover the zero-exponent mass. A wrong donor-word simplification is rejected. Results and the exact generated graphs are saved.

Fresh `triple_controls.py` propagates the actual no-merger three-lineage state distribution, applies the specified first merger operator, then propagates and applies the second merger operator. It checks 302 ordered-density/two-arm recoveries across 151 exposed reticulations, using unequal half-epoch demographic words and equal/nonbalanced inheritance cases. It also checks 151 oriented inheritance anchors and 1,097 longer-arm subtractions. Of those reticulations, 17 require known ancestor-reticulation propagation and 134 use the chain method with bypass allowed. All probabilities are rational; rates are integer multiples of `4 log(2)`, so quarter-grid survival calculations are exact. These finite experiments corroborate the proof and are not exhaustive in graphs or parameters.

Environment for the canonical suite and fresh controls: Python 3.14.6, SymPy 1.14.0, NetworkX 3.2.1, mpmath 1.3.0. Canonical package dependency versions match the published requirements. The optional separately specified twelve-job Tier-0 runtime was **not** executed, and no claim of that fresh coverage is made. PDF byte reconstruction from TeX was not attempted; both public PDF bytes and the supplied source archive are hash-bound.

## Primary imports and scope checks

- [Hellmuth, Schaller and Stadler, *Clustering systems of phylogenetic networks*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10564800/), Lemma 33 and Corollary 13: checked the original statement and argument for nonnested incomparable tree-child clusters and the cluster/comparability property. These agree with the narrower use in B; uniqueness of arbitrary shortcut-containing graphs is not imported from this source.
- [Yang and Flouri (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9087891/) and [Thawornwattana et al. (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10439365/): checked the two-singleton sister-direction ambiguity and distinction from richer sampling. These provide context, not a substitute for B's graph theorem. Their bidirectional/simultaneous model switches are not silently added to B's temporally separated class.
- Companion A, [Zenodo 22729537](https://zenodo.org/records/22729537): the earlier independent review read all 37 main and 27 supplement pages and checked the exact reversible all-indexed-locus-law ↔ normalized metric-genealogy-law bridge, plus compact-semianalytic finite determination. B's Corollary 1.2 and Section 11 import exactly those qualified claims. B does not prove a new effective locus-length bound or an arbitrary substitution-model inverse.

Other bibliography items give comparisons; this review is not an exhaustive priority/novelty search and does not certify their every historical assertion.

## Strongest supported result and remaining limits

The complete proof chain appears sound for the stated positive, temporally separated, strong-tree-child level≤2 class. I found no counterexample, unsupported central reduction, or numerical-to-proof substitution requiring a defect hold. No mathematical repair was undertaken.

Important boundaries remain: zero inheritance, zero/infinite rates, coincident distinct biological events, absent taxa, level-three blobs, general non-tree-child networks, within-locus recombination, unknown locus boundaries, and unsupported substitution classes are outside the theorem. Analytic continuation and divisions by positive but potentially tiny masses give no stability guarantee. In particular, the informative early-arm triple density scales as `q3 γ²`; it can be arbitrarily weak near the domain boundary. The paper explicitly disclaims practical finite-data reconstruction, and this is not a defect in its exact-law result. Human specialist review and independent novelty assessment remain desirable before making journal or originality claims, without any outreach prepared or initiated here.
