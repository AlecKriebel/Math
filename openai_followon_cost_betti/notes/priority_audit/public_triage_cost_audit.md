# Rapid triage: physics, quantum information, operator algebras, topology (#260–321)

Checkpoint: 2026-10-06 20:57 America/Los_Angeles. Triage completion estimate: 85%; proof completion is 0%, as requested. Read catalogue for all 62 families. Exact TeX, Lean scope document, and comparator inspected for #273. Follow-ons below assume the claimed #273 theorem is valid; no Lean rebuild or proof audit performed. ComparatorChallenges files contain `sorry` by design and are statement comparators, not proof verification evidence.

## Ranked launch candidates

### 1. Exact bosonic optical communication trade-off regions (highest confidence)

**Target.** Make unconditional the full quantum dynamic capacity region of the pure-loss channel for transmissivity eta in [1/2,1] under a finite mean input photon constraint N; also the public/private/secret-key dynamic region. The claim covers arbitrary entanglement across channel uses, with the standard net resource-generation/consumption conventions. This is substantially richer than the already-known single-resource quantum/private capacities.

**Mechanism.** Result #273, vacuum second port, is exactly the strong multimode minimum-output-entropy premise in the converse by Wilde, Hayden and Guha, *Quantum trade-off coding for bosonic communication*, PRA 86 062306 (2012), Sections III.G and III.H. Their achievability remains intact. A newer independent presentation is De Palma, arXiv:1805.12469, Theorem 11 and Corollary 12.

**Checkable target equations.** With g(x)=(x+1)log(x+1)-x log x and lambda in [0,1], quantum region is the closed union of
C+2Q <= g(lambda N)+g(eta N)-g((1-eta)lambda N),
Q+E <= g(eta lambda N)-g((1-eta)lambda N),
C+Q+E <= g(eta N)-g((1-eta)lambda N).
The public/private/key region follows the parallel existing conditional theorem. Keep log units consistent (bits vs nats).

**Exact remaining work.** Match #273 finite-energy assumptions with energy-constrained code ensembles, insert the theorem into the existing multi-letter converse, verify average-energy conventions and closure/endpoints, and audit the coding theorem's infinite-dimensional reduction. No new central inequality is apparent. Plausible short-paper timescale: days, not a promised deadline.

**Novelty risk.** These regions and their conditional derivations are already published; contribution is removal of the outstanding hypothesis with careful scope, not new formulas. Do not claim first discovery of ordinary pure-loss quantum/private capacities: they were already established without EPnI. The corpus has no dynamic-capacity/trade-off theorem; its #273 broadcast corollary explicitly restricts scope.

Primary sources:
- https://www.markwilde.com/publications/PhysRevA.86.062306.pdf (Sections III.G–H, pp. 9–11; explicitly says Strong Conjecture 2 follows from EPnI)
- https://arxiv.org/pdf/1805.12469 (Theorem 11; Corollary 12)

### 2. Exact confidential-message bosonic broadcast capacity, with arbitrary preshared-key rate (very high confidence)

**Target.** Remove the minimum-output-entropy assumption from Pereg–Ferrara–Bloch, arXiv:2105.04033, Theorem 6: exact common/confidential rate region for a pure-loss bosonic broadcast channel with eta in [1/2,1], for any key-assistance rate R_K, including zero, under the source’s strong-secrecy criterion and its Section II-C coherent-encoder convention. Distinct from corpus #273's two independent ordinary classical messages.

**Mechanism.** Their Conjecture 1 is exactly S(E_eta^tensor-n(rho)) >= n g(eta g^-1(S(rho)/n)), the vacuum specialization of #273. Theorem 6 has a complete conditional converse and achievability. For eta>=1/2 and beta in [0,1], target region is
R0 <= g((1-eta)N)-g((1-eta)beta N),
R1 <= min{g(eta beta N), g(eta beta N)-g((1-eta)beta N)+R_K}.
Do not promote the eta<1/2 formula: the independent arithmetic audit found its common-message bound inconsistent at eta=0 when Bob must decode the common message. This candidate is restricted to eta>=1/2.

**Gap/checks.** Retain the source’s Section II-C coherent-encoder convention and strong-secrecy criterion. An extension to unrestricted encoders requires a separate converse audit and is not claimed. Audit key accounting, finite-energy ensembles and endpoints against #273. No new central analytic step is apparent within the restricted scope, but the source’s eta<1/2 inconsistency increases the importance of checking its converse directly. The title/abstract may appear unconditional; full text explicitly states the conjecture in Theorem 6 and discussion. Three-user layered secrecy is NOT promoted: the source’s Theorem 10 only displays an inner-bound inclusion despite surrounding suggestive prose.

**Novelty risk.** Conditional formula already known. Unconditional implication is a direct theorem combination; publish with attribution rather than claiming a novel formula. Corpus-wide relevant-keyword search found no such result.

Primary source: https://arxiv.org/pdf/2105.04033 (Conjecture 1 and Theorem 6, p. 11; Section VI.B notes ordinary wiretap capacity was already unconditional).

### 3. Sharp multimode Gaussian additive-noise entropy minimization (very high mechanism confidence; moderate headline impact)

**Target.** For every finite n, noise variance nu>0 and finite-energy n-mode input rho of entropy ns, prove the exact constrained minimum
min S(N_nu^tensor-n(rho))/n = g(g^-1(s)+nu),
attained by a product thermal input. The nontrivial new range is 0<nu<1: nu>=1 is entanglement-breaking and was already settled.

**Mechanism.** Use #273's thermal-attenuator corollary with eta tending to 1 and N_B=nu/(1-eta). The resulting channels converge to additive Gaussian displacement noise; the lower bound tends to the displayed formula. Output energies stay bounded for each fixed finite-energy rho even though bath energy diverges, allowing the needed entropy continuity. Thermal input attains the limit.

**Gap/checks.** Establish channel convergence and energy-constrained entropy continuity rigorously, using the exact variance normalization. Handle s=0, nu=0 limiting identity, n=1 consistency. Do not silently extend to arbitrary finite-entropy but infinite-energy inputs: the continuity argument requires further work there.

**Novelty risk.** The corpus explicitly disclaims additive-noise channels in #273's introduction, line 63. The old conjecture includes this case (De Palma arXiv:1805.12469, Conjecture 1, Eq. 18); Corollary 5 already covers nu>=1. Whole-corpus text search found no other quantum additive-noise result. A direct limiting corollary is likely too small alone for a headline paper; bundle with the capacity results.

Primary source: https://arxiv.org/pdf/1805.12469 (Conjecture 1; Corollary 5).

### 4. Thermal-noise and multi-receiver degraded bosonic broadcast capacity (promising, needs model audit)

**Target.** Unconditional coherent-state superposition capacity region for the degraded finite-receiver bosonic broadcast models with additive thermal noise treated in Guha's thesis, beyond the corpus's two-receiver pure-loss case.

**Mechanism.** The thesis supplies a conditional multi-receiver theorem; its strong noisy minimum-output premise is #273's thermal-attenuator corollary. Iterate the entropy comparison along the degradation chain and use existing superposition coding.

**Gap/checks.** Need exact model matching: degrading channels must be identical tensor powers of a thermal attenuator at each stage, independent environments, finite average energy. Do not extrapolate to general nondegraded/MIMO networks or thermal-channel quantum capacity. This has a larger scope-verification burden than candidates 1–3.

Primary source: https://dspace.mit.edu/entities/publication/55006e49-04c0-405f-b897-c13f02ccbe2f (Guha thesis, abstract explicitly describes arbitrary receivers and additive thermal noise); PDF https://dspace.mit.edu/bitstream/handle/1721.1/41840/1/Saikat%20Guha-TR723.pdf (Chapters 3 and 5).

## Local evidence and exclusions

- Exact input theorem and thermal consequence: `/Users/alec/Desktop/math/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/00-introduction.tex`, lines 10–63.
- Ordinary broadcast paper explicitly excludes noisy broadcast, amplifier, wiretap, quantum capacity, feedback and receiver cooperation: same directory `sections/06-broadcast.tex`, final paragraph around lines 301–305.
- Lean scope `/Users/alec/Desktop/math/lean/docs/273.md`: the selected finite-energy EPnI only; capacity consequences not formalized there.
- Whole-corpus TeX search for dynamic capacity, quantum trade-off, key assistance, layered secrecy and quantum additive-noise statements found no duplication. Search absence is evidence, not proof of global novelty.
- Obvious applications already in corpus: #273 pure-loss two-user ordinary broadcast; #280 local extension correspondence; #288 universal hyperreflexivity; #302 zero-mean-dimension iff SBP/Z-stability/finite nuclear dimension; #287 entropy-dimension consequences in its companion sections.
- Do not infer efficient ground-state computation from #265 polynomial PEPS existence: contraction/optimization still central difficulty.
- Do not infer diffusive/ballistic Anderson transport from #261 absolutely continuous spectrum alone.
- Do not infer torus/topological Laughlin gap, Coulomb-to-pseudopotential gapped interpolation, or an AKLT-to-Heisenberg uniformly gapped path from the stated sphere/endpoint gap alone.
- Do not infer Kaplansky's group-ring zero-divisor conjecture from the reduced-C*-projection counterexample; the algebraic bridge is unsupported.
- Broad operator algebra/topology consequences mostly either already recorded in companion articles, immediate low-novelty reformulations, or require a central extra mechanism. No sufficiently justified high-impact quick target there was promoted in this rapid pass.

## Independent adversarial check of #259 cost proposal

Checkpoint: 2026-10-06 21:00 America/Los_Angeles. Review completion estimate: 100% of the implication check; 0% of foundational proof audit.

The algebra/groups agent's relation-level consequence passes. The source `A-group-without-fixed-price-October-5-2026/build/introduction.tex` explicitly defines a surjection Gamma -> Z, so Gamma is infinite; X and all Y_M are free pmp. Its theorem provides Cost(Y_M)<=1+99/M for every M>100, and Cost(X)>=1+eta with eta>0. Since beta0^(2)(Gamma)=0, Gaboriau's inequality and invariance for free pmp actions give 0<=beta1^(2)(Gamma)<=99/M for all M, hence beta1=0. The Bernoulli orbit relation R_X therefore has Cost(R_X)-1>beta1(R_X)-beta0(R_X). The exact relation-level question is stated in Gaboriau's own FAQ https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/FAQ.pdf, page 1 (Cost vs L2-Betti Numbers Problem). No ergodicity assertion about Y_M is needed. Group cost defined as infimum over free actions is exactly one here, so this does NOT disprove the infimum-group-cost equality. The inference is very short; novelty should be framed as an explicit negative answer to the distinct relation-level question, conditional on the released fixed-price counterexample.

Correction checkpoint: 2026-10-06, following independent arithmetic audit. Candidate 2 is narrowed to eta>=1/2, strong secrecy, and the source’s Section II-C coherent-encoder convention. The eta<1/2 claim and an unrestricted-encoder interpretation are withdrawn. Scope-triage completion estimate remains 85%; the new source inconsistency is an unresolved converse-validation risk.
