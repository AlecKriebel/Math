# Independent adversarial audit: Problem 6200061

## Verdict

**ACCEPTED_PARTIAL_NOT_SOLVED.** The frozen package's marked-realization obstruction is mathematically valid under its stated proper-geodesic hyperbolic model convention. No mathematical correction is required. All five proposed routes were reviewed; none resolves the general equality or the existential attainment question. This is acceptance of the stated partial result, not a resolution or an originality determination.

The distinction is indispensable: a specific marked Ahlfors-regular minimizing metric need not be equivariantly bilipschitz to a visual boundary, while some other minimizing metric can be visual. For the surface groups in this example, the ordinary Fuchsian model already supplies that other metric.

## Frozen identity and complete target review

The audited input is `KLEINIAN_BOUNDARY_6200061_AUTHOR_SAFE_FREEZE.zip`, exactly 30,172 bytes, with SHA-256 `9d404dd597724c207e50afe80f97ec7f4b66e8c957193972fe2011c8853563d8`. Its nine-member roster matches the external receipt. Its manifest SHA-256 is `fc47e35e492d41ab4b1b1a49e3ed43bf4d5a275861e1f90e3028691b9d099f03`. The archive and receipt were not modified.

The complete target record and complete associated report were read. Independently recomputing default `json.dumps([record, reports.get(problem_number,{})], sort_keys=True).encode()` gives `19d550c8dd1630a33ab9f57396a75f3ff318fe849cdf8d4a4ad32469fe9fb258`. It matches both the catalog and author identity file. The target is ID 6200061, number AMR-061-0061, rank 810. All three complete input corpus byte counts, hashes and record counts match the frozen metadata; the statement hash also matches. Only verification metadata, not corpus records, is included here.

The earlier repository search remains bounded evidence. Its reported failed recursive reads prevent an exhaustive history claim. This audit did not repeat a remote repository search and did not mutate any remote resource.

## Mathematical audit

### 1. Visual metrics and the group action

For a visual metric with one comparison constant C valid for every boundary pair, changing the basepoint from o to g^{-1}o changes the boundary Gromov product by at most D = d(o,g^{-1}o), up to the fixed convention-dependent hyperbolicity error. The resulting distortion is bounded above by C² exp(epsilon D), with the reciprocal lower bound. This is a genuine global bilipschitz bound for each fixed isometry g. Uniformity over all g is unnecessary and is not claimed.

If F is an equivariant L-bilipschitz identification from the proposed boundary metric into a visual boundary, the given group element is Lipschitz with constant at most L² C² exp(epsilon D). Thus one non-Lipschitz group element obstructs every such identification, including realization after a bilipschitz change of the marked metric.

### 2. Actual surface-group element

A nonidentity element of a torsion-free cocompact Fuchsian group is hyperbolic. A Möbius conjugacy can place its fixed points at -1 and infinity; inversion of the element if necessary makes its multiplier a greater than 1. It then acts as x ↦ ax + b with b = a - 1 > 0. The construction therefore works for an actual element of every closed orientable hyperbolic surface group. It does not require the multiplier 2.

The conjugacy is chosen before defining the metric and fixes the chosen marked group action for the rest of the argument. The separate calculation at a = 2 is correctly labelled illustrative rather than a claim about every lattice.

### 3. Quasisymmetric gauge, including infinity

For h(x) = x|x|, direct sign cases give

(1/2)|x-y|(|x|+|y|) ≤ |h(x)-h(y)| ≤ |x-y|(|x|+|y|).

Consequently the Euclidean image-distance ratio is at most 2t(2+t) when the original ratio is at most t. This controls opposite-sign pairs as well as same-sign pairs. In the infinity coordinate u = 1/x, the map is again u ↦ u|u|. Chordal distance is bilipschitz comparable to coordinate distance on suitably bounded coordinate neighborhoods; away from 0 and infinity the map and inverse are locally Lipschitz.

The compactness step is sound. A finite chart cover supplies a common positive Lebesgue radius r. For 0 < t ≤ 1, triples whose denominator distance is below r lie in a single controlled chart; for the remaining triples the image denominator has a positive lower bound and uniform continuity makes the numerator tend to zero with t. For fixed t > 1 use cutoff r/t. These bounds give a finite distortion function tending to zero at zero, with an increasing homeomorphism majorant. Thus the chordal-circle map h is globally quasisymmetric. The identity from q to the pulled-back metric d = h* q has exactly that distortion.

### 4. Ahlfors regularity and optimality

The map h is an isometry from the pulled-back metric circle onto the chordal circle. Pull back normalized circle arclength to obtain the measure. One can make the constants explicit: for chordal diameter 1 and 0 < r ≤ 1, a ball has normalized measure 2 arcsin(r)/π, between (2/π)r and r. The same bounds hold for d-balls. Hence d is Ahlfors 1-regular.

The compatible topology is the circle topology, so Hausdorff dimension is at least its topological dimension 1. The displayed Ahlfors-regular metric has dimension 1. Therefore it attains the Ahlfors-regular conformal dimension. No invariance of this measure under the original group action is needed.

### 5. Non-Lipschitz calculation and marking

For b = a - 1 > 0 and positive t tending to zero, the squared source distance is t⁴/(1+t⁴). The image distance is

(2ab t + a²t²) / [sqrt(1+b⁴) sqrt(1+(b+at)⁴)].

If R(t) is the image/source distance ratio, then

t R(t) → 2ab/(1+b⁴) > 0.

Thus R(t) is unbounded. The author's explicit lower bound is also correct. This establishes the obstruction without relying on finitely many samples. The abstract metric circle is round by the isometry h, but that isometry does not conjugate the fixed action to maps induced by model isometries with this round visual metric. Changing the marking changes the realization question. Meanwhile the original standard visual metric q proves both numerical equality and existential attainment for this group.

### 6. Auxiliary results and all five routes

- The additive-defect supremum construction is a valid finite, positive, symmetric, left-invariant metric satisfying d0 ≤ D ≤ d0 + K. Taking a supremum preserves the triangle upper bound. The Gromov-product error bound 3K/2 is valid. Properness, geodesicity and an appropriate geometric model do not follow from this lemma alone, as the package correctly warns.
- The direct filling route supplies a quasi-isometric model, not automatically an isometric geometric action preserving the supplied boundary metric. The marked obstruction closes exactly that unjustified stronger route.
- The entropy/visual-parameter rescaling calculation is consistent: transforming both parameters leaves their quotient unchanged. Admissibility of a fixed parameter cannot be silently preserved under all rescalings.
- Tree cylinder measures and their regularity ratios are correct. Arbitrary positive visual parameters give A = E = 0 for nonabelian free groups. Compact Ahlfors 0-regularity would force uniformly positive singleton masses and is impossible on the infinite boundary. Real-hyperbolic uniform lattices have A = E = n - 1, attained, by the round visual metric and the topological lower bound.
- The Poincaré-profile route does not supply the missing reverse realization implication. A profile bound expressed using A instead of E does not establish A = E.

The general missing step remains a geometric action whose visual dimension is arbitrarily close to A(G), and, for the attainment clause, an exact minimizing geometric model when the gauge minimum exists.

## Independent executable checks

`independent_checks.py` uses only the standard library and does not import the author's verifier. It pins the external archive identity before extraction, checks the exact roster and manifest identity, reconstructs the Bernstein polynomial in the reverse direction, checks a separate degree-six identity, derives chordal-distance ratios directly, and recomputes every stored cylinder and finite supremum example.

Results, recorded in `CHECK_RESULTS.json`:

- Frozen author verifier: normal and optimized Python pass in relocated temporary directories from unrelated working directory `/`.
- Author suite: all 12 negative cases, 24 mode-specific rejection runs, pass.
- Independent suite: 22 rejection cases, each under normal and optimized Python, give 44 expected rejections. Coverage includes missing/extra files, symlinks, duplicate/nonfinite JSON, rehashed identity/scope changes, false polynomial/sample/cylinder/supremum data, noncanonical rational data, and source-inclusion declarations.
- Seven positive Bernstein coefficients, seven exact degree-six identity evaluations, 80 exact dyadic ratios, 84 cylinder records and the order-five supremum metric agree.
- An additional 155 general-multiplier rational checks and 4,080 sign-spanning power-map triple checks pass. These are regression checks; the geometric proofs above and in the frozen text carry the universal conclusions.
- The independent harness itself was relocated and run under normal and optimized Python. Both return identical core results, as recorded in `HARNESS_RELOCATION.json`.

### Important verifier limitation

Three deliberate rehashed mutations still pass the *standalone author verifier*: changing mathematical prose, replacing a plausible corpus hash, and replacing a source title. These are outside its symbolic/declared-scope checks. The same three mutated archives are rejected by the independent external identity pin under both normal and optimized Python. This is not a flaw in the frozen mathematical result, but a concrete reason never to describe the author's executable as a proof assistant or a fresh source-verification service. The frozen external receipt and human mathematical/source audit remain essential.

## Primary-source verification

- [Kapovich's survey](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf): independently read the surrounding definitions and Problem 61 on PDF/printed page 17, and rendered that exact local PDF page for visual inspection. Its front-page date is October 24, 2007; the collection originated in a 2005 workshop. The statement has separate equality and conditional existential-attainment content.
- [Hume–Mackay–Tessera author version](https://people.maths.bris.ac.uk/~jm13806/pdf/Poincare-sep.pdf): independently read and rendered page 46, Definitions 12.4–12.5 and the subsequent conjecture discussion. Its front-page date is May 29, 2019. The [publisher record](https://ems.press/journals/rmi/articles/16795) confirms publication in 2020, volume 36(6), pages 1835–1886. The 2018 reference label used elsewhere is not the publication year.
- [Hume–Mackay–Tessera 2022](https://link.springer.com/article/10.1007/s00039-022-00617-4): independently inspected Remark 1.15 and Section 5.3. These remove the equivariant-dimension hypothesis from profile bounds; the discussion still allows a possible gap between the two dimensions.
- [Coornaert 1993](https://msp.org/pjm/1993/159-2/pjm-v159-n2-p03-p.pdf): inspected the introductory hypotheses and Sections 3 and 7, particularly Proposition 7.4 and Corollary 7.6. These support visual distortion and regularity/dimension background in the proper-geodesic, cocompact setting.
- [Hume–Mackay 2025](https://arxiv.org/abs/2511.10469): submission history confirms the 2025 preprint status. Questions 1.4–1.5 and Theorems 1.6–1.7 concern a profile critical exponent rather than the equivariant conformal dimension. No geometric-action realization theorem is supplied by those results.
- Bonk–Schramm is credited for standard filling/boundary correspondence; its full original article was not independently inspected in this audit. The obstruction proof does not rely on an unverified claim that such a filling is equivariant.

Retained PDF hashes and sizes match the author metadata. Current primary web pages were checked independently; the audit does not claim a fresh byte-for-byte download of every source. A renewed targeted public search found no full resolution. Neither that search nor this report establishes exhaustive absence of later work. Retrieval and inspection details are in `SOURCE_CHECKS.json`.

## Distribution and preservation

This audit archive contains only authored mathematical review, authored checking code/results, and public verification metadata. It contains no third-party PDF, extracted source text, corpus contents, private source, or coordination material. No correction patch is supplied because no correction to the frozen partial result was necessary. No remote mutation, publication or outreach occurred.
