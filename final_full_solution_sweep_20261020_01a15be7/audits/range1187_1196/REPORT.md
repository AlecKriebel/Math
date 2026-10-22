# Independent bounded eligibility audit: PR1187–1196

## Decision

The ten recorded classifications withstand this independent scope challenge: eight restricted/conditional attempts and two complete prior answers. No previously unpublished full-original-question claim was found in this range. This is an eligibility and attribution conclusion, not a second complete correctness or priority certification of every partial theorem.

Two accounting matters must remain visible before final sweep reconciliation:

1. **PR1194 is a complete prior published answer.** Existing DOI `10.1007/s00493-024-00127-x` must be reconciled with the spreadsheet, with a fresh duplicate check. Root already tracks this as pending; this review does not authorize an unchecked append and made no write.
2. **PR1189 has a related original subsidiary-answer accounting lead.** Erdős's 1992 printed p.43 separately conjectures a finite cardinality ceiling of `n/2+O(1)` and an upper-density ceiling of `1/2`. Freud's already published finite `19/36` construction refutes the former; the accepted corrected infinite extension supplies the latter counterexample. A stronger published finite construction is Coppersmith–Phillips, DOI `10.1137/S0895480193244139`. The readable SIAM primary abstract and Crossref record authenticate its `13n/24−O(1)` construction and bibliography; direct DOI/PDF requests returned403, and this review did not obtain the five-page proof. Resolve this existing-publication lead explicitly, without presenting it as a solution of the distinct lower/logarithmic-density questions on p.42 or creating a new upload. See `COPPERSMITH_ACCOUNTING_LEAD.json` and its access limitations.

No mathematical reclassification of the eight principal partial targets is required. In particular, missing finite certificates are reproduction limits, not the central reason for excluding their restricted results. Conversely, PR1190's formal replay limitations do not erase its conventional complete prior-solution claim.

## Independent evidence and limits

`PINS.json` and `FINAL_PINS.json` independently bind all ten fresh GitHub PR heads, bases and complete bodies, all80 changed path/blob/status entries, and30 freshly fetched immutable text blobs. Initial and final immutable inputs agree. All PRs were open, draft and unmerged at those observations. All eight files per PR are additions; none changes `QUEUE.md`. `BINDING_CROSSCHECK.json` verifies that the locally read source copies also match the freshly fetched GitHub blobs. Complete paths were checked through the immutable base-to-head comparison, not accepted merely from the preliminary live file-list endpoint.

All ten bodies' mathematical text, all acceptance documents, primary outcome/theorem/definition and gap sections, and relevant reduction/construction/repair arguments were read. `READ_SCOPE.json` gives the exact boundary: not every line of every partial proof was independently audited. The complete fresh17246-byte Blair prior proof was read. Candidate programs, historical auditors, Lean/Lake and other mathematical implementations were neither imported nor executed. Five independent exact scope sanity checks are in `SCOPE_CONTROLS.json`; they do not certify asymptotic theorems by finite extrapolation.

Eleven fresh primary-source retrievals are pinned in `PRIMARY_RETRIEVALS.json`, including the exact cited versions of the original questions and the external Blair proof. Fresh PDF bytes match the corresponding PR source identities. Original-source text inspection covered the relevant target pages. Erdős1992 printed42–43 and the complete four-page Freud1993 article were also visually inspected; Erdős–Rosenfeld printed355 was visually inspected to disambiguate the universal quantifier. Full source PDFs, extraction and render artifacts remain private. Historical source-inspection and program-run assertions in the PRs were not silently recertified.

Fresh GWS CLI inspection used workbook `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, numeric sheet1254632077, title `Math Puzzles`, exact GRID metadata and all43 columns. The initial05:10:48UTC view had182 rows; a later focused05:15:16UTC view had183. This is a concurrent-state observation, not a write by this reviewer. `LEDGER_CHECK.json` and `COPPERSMITH_LEDGER_CHECK.json` retain aggregate leads and hashes, without publishing private raw rows.

The fresh lead rows were semantically distinguished:

- Row60's numeric substring `3000017` belongs to problem30000170, a prox-regularity result, DOI23306332.
- Row83's `2503` comes from arXiv2503.08553, a harmonic-sphere result, DOI23356680.
- Rows147/148 are problem3000016 general directed reachability and3000018 simple directed halting, DOI23431676/23431716. Neither answers general Eulerian-multigraph halting.
- No exact balanced-permutation DOI/title/author/PR/problem lead was found in the bounded182-row search. No Coppersmith/Phillips/Freud/subsequence-sum/target-DOI lead was found in the later183-row search. Fresh semantic duplicate checks remain necessary before action.

The read-only verifier `verify_readonly.py` performs no filesystem writes or provider mutations. Root should read its exact source before replay. An initial run failed because this reviewer assumed an `ACCEPTANCE.json` for1189, whose actual acceptance is Markdown. The assumption was corrected in this review's verifier; the failed stderr is preserved privately. The subsequent and final runs passed. No failure was represented as a passed audit.

## Per-PR findings

### PR1187 /2150, alias2304007: disk covering

The original [Erdős1961 printed246](https://users.renyi.hu/~p_erdos/1961-22.pdf) asks for a universal radius-sum bound2 for monic polynomials. The cited connected-case2 result and general2.59 result are explicitly prior. The PR's component-partition formula retains the endpoint and covers the closed region, so this is not an exclusion based on a mistaken open/closed or finite/countable distinction.

Its exact translated-binomial-family formula has a maximum strictly below2, but no argument extends it to arbitrary monic polynomials. The quartic is a useful obstruction to separate component covers: exact rational comparisons give `19/16<b<6/5`, so the separate cost exceeds `9/4` while a common disk costs less than `6/5`. It is therefore not a counterexample to the original target. Fixed-polynomial compactness would turn all estimates `2+ε` into an attained2, but the missing universal estimates are not supplied. **Partial classification sustained.**

### PR1188 /2249, EP677: equal interval LCMs

[Erdős1979 printed78](https://users.renyi.hu/~p_erdos/1979-23.pdf) asks for unequal complete LCMs of equal-length blocks with inclusive disjointness `m≥n+k`. The source separates this from prime-support and unequal-length questions. The PR preserves full prime-power LCMs and the inclusive boundary.

Its starting point `n` is unbounded, but `k≤20` and `k≤d≤256` remain bounded. The exact ratio/root and cross-difference reductions do not rule out arbitrary length and gap. The product ratio is monotone; no LCM monotonicity follows. As a semantic control, blocks `{3,4}` and `{8,9}` have identical prime support `{2,3}` but LCMs12 and72. Omitting three million numerical certificates limits replay of the finite corollary; it does not change the more decisive quantifier gap. **Partial classification sustained.**

### PR1189 /2334, EP839: separated blocks and Freud repair

Fresh text and images of [Erdős1992 printed42–43](https://hrj.episciences.org/125/pdf) distinguish three matters. Printed42 asks whether every admissible infinite sequence has lower natural density0, and whether its reciprocal mass divided by `log x` tends to0. Printed43 separately proposes an upper-density/finite-count ceiling near1/2. Upper and lower density must not be interchanged.

The PR's main theorem assumes prefix-sum separation and a bounded block-width ratio. Avoidance alone has not been shown to imply that architecture. Its explicit constructions satisfy both printed42 conclusions, so neither is an original-problem counterexample. This preserves the principal **partial classification**.

The printed extension error is substantive and was independently confirmed against [Freud1993 printed6202](https://webhomes.maths.ed.ac.uk/cook/iss_no60.PDF). The last interval begins at `8x−8y+3T+1`, which becomes `4L+3T+1`. The surviving new C-neighbor sum `4L+3T` lies one below that endpoint for the stated divisible-by4 case. The PR supplies a one-integer repair for all prefix totals `T≥3`, distinguishes the `T=4` boundary wording, and retains the complete prior upper-density19/36 conclusion. This is neither an unresolved numerical observation nor a full answer to the printed42 questions.

The finite Freud construction already refutes the separate printed43 finite ceiling independently of the infinite-extension issue. The later stronger [Coppersmith–Phillips publication](https://epubs.siam.org/doi/10.1137/S0895480193244139) is an accounting lead for that subsidiary question. Its bibliography is SIAM Journal on Discrete Mathematics9(2)(1996),173–177, Don Coppersmith and Steven Phillips. The1996 print issue must not be confused with its2006 online date. This review's primary access stops at the publisher abstract and Crossref metadata; no full-paper proof acceptance is asserted. **Preserve the prior subsidiary answer and resolve the publication-accounting lead; no new-upload recommendation.**

### PR1190 /2283, EP730: central-binomial prime supports

The [original1975 printed91](https://www.renyi.hu/~p_erdos/1975-27.pdf) asks for infinitely many distinct positive indices whose central binomial coefficients have the same prime-divisor sets. It does not require equal valuations or coefficient values.

The freshly retrieved [Blair proof at commitf297d710018270c66b296082766334974260bcbc](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/ErdosProblems/Erdos730/compute/full_density/proof.md) has the exact17246-byte SHA recorded by the PR. It states and conventionally proves a stronger positive-parameter-density consecutive-pair result, with classical Kummer/Mertens/fixed-modulus PNT inputs. The positive strictly increasing quadratic makes the terminal bridge genuinely infinite and injective. Density is in the parameter, not in `n` or all pairs.

The author manifest freshly matches11258 bytes and SHA2ee9620b…; it attributes antecedent roles to Price and Tomodovodoo and reconstruction/formalization to Blair. No new original-question theorem is claimed by the PR. Failure to replay Lean or certify the elaborated axiom footprint must not turn this complete conventional prior claim into a partial one. This bounded review does not certify the entire analytic or formal proof anew. The sole DOI in that manifest is Lindström's unrelated EP154 background, `10.1006/jnth.1997.2212`; it is not an EP730 publication DOI. A limited search found no authenticated EP730 DOI, which is not a worldwide absence claim. **Complete-prior classification sustained; preserve exact public-source provenance and unknown DOI status.**

### PR1191 /2291, EP757: strong-Sidon seed extensions

[Ma–Tang2602.23282v2](https://arxiv.org/pdf/2602.23282v2), pp1–2, separately defines the solved weak-Sidon problem and Erdős's unsolved optimal constant for `(4,5)`-sets. Its Lemma5.1 on p13 identifies the exact14-point seed and maximum8. Those are distinct mathematical targets.

The PR's all-real argument covers0,1 or2 additions to that fixed affine seed, including irrational additions. That universal quantifier is genuine and should be preserved. Nevertheless it neither classifies arbitrary16-point sets nor improves/determines the original universal constant. The finite candidate families and maximum-subset avoidance premises are explicit but omitted from the edition. The general AP and normalization reductions do not remove the seed restriction. **Partial classification sustained.**

### PR1192 /2364, EP885: factor-difference obstructions

Fresh text and the image of [Erdős–Rosenfeld1997 printed355](https://matwbn.icm.edu.pl/ksiazki/aa/aa79/aa7944.pdf) show that Conjecture1 quantifies over every positive integer `k`, with `k` distinct integers sharing at least `k` differences. Proposition3.1 supplies a finite fixed-pair reduction, not the universal existence conclusion.

The PR gives a transposed fixed-seed `k=4` configuration and exact fixed-scale support exclusions. The latter allow arbitrary positive integers in the tested neighborhoods, so an independent `N` cutoff is not the gap. The missing cases are unrestricted `k=5`, arbitrary seed differences/scales, and arbitrary `k`. The rational-square rectangle equivalence transfers the task to constructing a missing6-by5 rectangle; it does not supply that rectangle. T-pair supports of size5 are explicitly permitted, so the correct exclusion requires triple intersections. **Partial classification sustained.**

### PR1193 /2503, EP1122: additive rigidity

[Erdős1946](https://users.renyi.hu/~p_erdos/1946-06.pdf), p1, defines ordinary additivity on coprime inputs; p3 states density-one nondecrease as a conjectural sufficient condition for exact logarithmic behavior. It is separate from the neighboring density-one small-successive-difference question.

The PR proves exact rigidity only with a further fixed-slope periodically approximable residual, or a summable prime-tail condition. Its absolute-vanishing-error lifting lemma is a sufficient bridge that the original assumptions have not been shown to supply. A normalized error relative to a growing variance scale need not be absolute `o(1)`. The parity/valuation examples have positive decrease density, and the slowly varying scalar example is not an additive counterexample. Higher prime-power values remain arbitrary finite reals; complete additivity is not imposed. **Conditional partial classification sustained.**

### PR1194 /3100034: balanced permutations

The immutable PR body/primary text/acceptance consistently record the complete Beniamini–Lavee–Linial prior finite classification, including endpoints, low-order residue classes and nonexistence for all `n≥k≥4`. Arbitrary increasing index sets, not contiguous substrings or approximate uniformity, define the target. The omitted19 witnesses limit this exposition's reproduction, not the published theorem's full scope. Endpoint and chamber/odd-centre derivations are explanatory completions rather than a new contrary theorem.

**Complete-prior classification sustained.** Existing DOI `10.1007/s00493-024-00127-x` requires spreadsheet reconciliation. The final state observation still lists the required existing-publication reconciliation; it must not disappear merely because the upward numerical cursor has advanced. A separate dedicated primary review is in progress; this range audit does not substitute for it or claim to have independently rechecked all19 witnesses. No new upload is appropriate.

### PR1195 /2440, EP1016: outerplanar pancyclic excess

[Erdős1971 Problem10, printed101](https://www.renyi.hu/~p_erdos/1971-25.pdf) asks for divergence beyond the logarithmic lower bound for the unrestricted pancyclic minimum. It does not restrict to outerplanar graphs or explicitly demand the stronger modern coefficient-one log-star estimate.

The PR proves the divergence only for outerplanar graphs through degree-constrained integer weighted trees. Since the unrestricted minimum is at most the subclass minimum, a divergent subclass lower bound does not prove the required unrestricted lower bound. Removing crossing chords can destroy pancyclicity. The corrected `k²+4` substitution and exact star-dual construction preserve useful restricted results; the `k=3` bounds13,13,13,12 check correctly. None closes the graph-class gap. **Partial classification sustained.**

### PR1196 /3000017: weighted directed-cycle cactus halting

Fresh [Hujter–Kiss–Tóthmérész1507.03209v4](https://arxiv.org/pdf/1507.03209v4) states the broad halting question with multiple edges in Problem22 on p13. Its Theorem11 instead decides prescribed-endpoint reachability; it does not solve the halting endpoint-existence question.

The PR's compressed algorithm is restricted to directed-cycle block cacti with independent positive binary block weights. The bidirected triangle is a connected loopless Eulerian graph outside that exact class. Its unit-weight cycle `(2,1,0)→(0,2,1)→(1,0,2)→(2,1,0)` was independently checked; a same-total stable vector `(1,1,1)` does not supply Laplacian equivalence because images of `3I−J` have equal coordinates mod3. This demonstrates the missing lattice information without proving general hardness or excluding another general algorithm. Signed stable certificates are not represented as reachable endpoints. **Restricted partial classification sustained.**

## Handoff

The bounded review is complete at100%; overall sweep estimate remains79%. Keep PR1194's accounting requirement pending until verified execution/readback. Preserve the related PR1189 original-subsidiary-publication lead with its exact scope/access limits. The other eight principal partial targets need no publication action under the full-solution rule. This review made no provider, spreadsheet, Git, index, branch, PR or release mutation, and contacted no outside individual or other agent.
