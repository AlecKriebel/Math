# Independent adversarial audit: rational Hilbert-modular Lyapunov exponents

Date: 2026-10-05. Target metadata: rank 723, ID 30002533, OWR-12870-003.

## Verdict

**PASS, scoped to the original report's existential new-exponent question.** The frozen deduction supports `already_solved` by credited prior results. No fatal mathematical implication was found. This is an independent AI-assisted mathematical audit using published theorems, not a formal proof certificate or an independently named new fraction.

The accepted conclusion is that actual individual primitive Gothic Teichmüller components have rational, nonuniformizing Hilbert-modular exponents outside `{1, 1/2, 1/3, 1/5, 1/7}`. In a sequence of distinct components the Prym exponents approach `3/13`; eventually they lie in `(14/65, 16/65)`. Neither attainment of `3/13` nor a component-specific fraction is established. A fixed Hilbert surface, an effective discriminant threshold, and classification are outside this conclusion.

The proof genuinely needs its orbit-closure and invariant-subbundle arguments. A discriminant-specific volume ratio alone would fail this audit.

## Binding and scope

The audited author manifest has SHA-256

`e4a387aec4351158d9b723f72122831696b4901ee4f721f94239bff5a4bde7fe`.

All nine declared payloads were independently hashed, size-checked, and matched against the actual file set before and after testing. The external digest is essential: a checker that merely trusts its adjacent manifest cannot detect a coordinated change to both proof and manifest. The controls explicitly demonstrate this distinction. `BINDING.json` records the exact file identities.

The original publisher PDF was independently retrieved and its complete relevant contribution on printed pp. 563-564 was inspected in text and rendered images. It asks for other rational exponents of immersed Kobayashi curves, without prescribing a particular fraction or a fixed discriminant. Thus a noneffective existence deduction from an explicitly constructed family addresses its literal mathematical obstruction. It does not provide an individually identified example should a different task require one. [O]

The live problem URL independently returned HTTP 403. Its current wording was not seen. The numeric ID/label/rank association remains supplied catalogue metadata; no raw statement or AI-report corpus was available to recompute that binding. The contribution title, content, DOI and old-value set agree with the proposed original-source target. Do not promote this scoped result into verification of unseen live-page requirements.

## Independently checked source inputs

Six PDFs were fetched anew from the listed publisher/author URLs. Every independently obtained byte count and SHA-256 matched the frozen public metadata. Relevant statements, definitions and proofs were then inspected; selected mathematical pages were also rendered and visually checked. Files and images are excluded from this audit package. `SOURCE_AUDIT.json` records retrieval and inspection metadata only.

- [G]: Gothic local geometry, proper real multiplication, finite curve loci, nonsquare primitivity, and an actual infinite family; especially Theorems 1.4, 1.6-1.10, Corollary 1.11, and §§5, 8. Theorem 5.2 supplies the local tangent sheet rather than merely a dimension count.
- [A]: Theorem 1.4 supplies symplecticity of the absolute tangent image. The real tangent convention preceding it and the flat-subbundle terminology were checked.
- [E]: Definition 1.1, the self-intersection discussion, Theorems 2.2-2.3, and Corollary 2.5 supply the precise measure and orbit-closure framework, including no loss of probability mass.
- [B]: Theorems 2.6, 2.8-2.9, the uniform integrability discussion, and the proof in §5 support restriction to invariant subbundles and exterior powers, not only the sorted full spectrum.
- [T]: §§3-4 and §6 identify the Prym realization and arithmetic quotient. Theorem 11.2 gives the generic Prym value; printed pp. 1206-1207 distinguish the disconnected average from the individual curve degree ratio. Proposition 4.3 explicitly discusses commensurable arithmetic groups.
- [O]: The primary contribution supplies the target and normalization. Its earlier congruence assumption belongs to the separate twisting-volume theorem.

[T] is published in Geometry & Topology 24 (2020), 1149-1210; its PDF records publication on 30 September 2020. The inspected [B] is the 2017 author version; its Astérisque 415 (2020), 157-180 publication was independently confirmed on the SMF page. The inspected [A] is arXiv v2; its Crelle 732 (2017), 1-20 publication was independently confirmed. No claim of typesetting-byte identity between author and journal versions is made.

## 1. The rel-zero condition and classification of proper orbit closures

This is a valid argument, but **rank two by itself is not enough**.

On a Gothic sheet the tangent is the relative-cohomology realization of the absolute cohomology of the abelian quotient C. The relative kernel is in the involution's positive eigenspace: the involution fixes the zeros. The Gothic tangent is in its negative eigenspace and hence meets that kernel trivially. Thus absolute projection is injective on the entire Gothic tangent and on every sub-tangent. This verifies rel zero, rather than assuming it from terminology.

For an affine invariant submanifold N contained in that sheet, write V for its real period tangent. The independent geometric input [A] makes p(V) symplectic. Consequently

`dim_C N = dim_R V = dim_R p(V)`

is even. A nonzero translation surface contributes at least the two-dimensional complex scaling/orbit cone. A proper submanifold of the four-dimensional Gothic manifold can therefore only have complex dimension two. Without injectivity, rank-one/rel-one dimension three would remain possible; without symplecticity, parity would not follow. Both hypotheses are actually available here.

There is a minor precision point in reading the frozen proof's connected-manifold shorthand: Gothic loci can be immersed and have several local sheets. Work on their smooth orbifold sheets or normalization. A linear tangent lying in a finite union of linear sheets lies in one of them. A closed affine subvariety of equal dimension cannot be a proper full-dimensional piece of the irreducible Gothic variety. This uses local analytic structure and irreducibility, not the false general assertion that every closed subset containing some open set equals a connected space.

For complex dimension two, the area-one locus has real dimension three. The SL(2,R) action has discrete stabilizers, so every orbit is open there. On a connected affine component it is the only orbit. The finite invariant probability measure makes this a finite-volume closed orbit, hence a Teichmüller curve. A proper connected affine submanifold cannot hold infinitely many distinct such orbits.

**Result:** the specific classification used in the packet is proved by its stated inputs. No classification theorem for arbitrary rank-two manifolds is silently required.

## 2. Distinctness, primitivity and equidistribution

Select actual distinct closed orbits, not an enumeration of discriminant labels or marked copies. [G] supplies infinitely many nonsquare, geometrically primitive components; its field-realization result is a further check that this is a genuine infinite family. The proper-action requirement in its definition also prevents freely relabeling one action by arbitrary suborders. There are finitely many auxiliary choices of the elliptic data at a fixed surface. A finite cover or repeated marking is not counted as a new orbit.

For each chosen orbit use its normalized ergodic probability measure on the area-one stratum H(2,2,2). The three regular fixed points used in the construction only involve finite markings; they do not introduce a relative deformation parameter into the unmarked stratum.

Any subsequential affine limit has support contained in the closed Gothic locus. If that support were proper, the previous section makes it a single closed orbit (or finitely many such components before selecting the ergodic one). Eventual containment from [E] would then contradict pairwise distinctness. Every subsequential limit must therefore be the Gothic affine measure. Compactness in [E] gives a probability limit rather than a subprobability measure. No additional cusp estimate or assumption that the curves stay in a fixed compact set is being made.

This is an argument about individual ergodic curve measures. Their volumes, the number of components at a given discriminant, and weights used in disconnected unions do not enter it. Geometric primitivity is sourced independently, not deduced from measure convergence or from a finite cover of the parameter curve.

## 3. The Prym block, finite markings and continuity

Let W be the real rank-four Prym local system. On an immersed Gothic sheet it is also `p(T_R M)`. Its flat structure is visible in period coordinates; it is a continuous invariant subbundle of the Hodge bundle. The quotient C used in [G] and the dual Prym used in [T] describe this same rational Hodge factor up to isogeny. An isogeny changes the integral lattice, not the Lyapunov spectrum of the real local system.

Self-intersections need not create an unproved global choice of W. The self-intersection set is a finite union of lower-dimensional affine submanifolds by [E]. Here those are closed orbits. Delete those finitely many possible members from the chosen sequence. On the remaining locus the tangent sheet, hence W, is unambiguous. The limiting Gothic measure gives the deleted set mass zero. Compact subsets avoiding it capture arbitrarily high limiting mass, so the projective-bundle compactness argument is unaffected. Alternatively one can use the usual finite orbifold markings/immersed-manifold domain. No assumption of connected discriminant loci is needed.

Theorem 2.8 in [B] is phrased for Hodge exponents, but its proof is more informative than that shorthand. The following application follows its actual mechanism:

1. Restrict the cocycle to W. The ambient uniform logarithmic-integrability bound restricts to W, and to its exterior powers up to a fixed multiplicative factor.
2. Choose the semisimple decomposition adapted to this invariant summand. Its strongly irreducible constituents are continuous by the regularity input used in [B]. W itself need not be strongly irreducible on every curve.
3. Apply the projective top-exponent argument to these constituents. Taking their finite maximum gives continuity of the top exponent of W and of exterior powers of W.
4. In particular, the largest exponent of `wedge^2 W` is `1 + lambda_P`, because the four exponents of W are `1, lambda_P, -lambda_P, -1`. Subtracting the fixed tautological exponent 1 preserves the Prym label.

Thus the needed convergence is `lambda_P(C_n) -> 3/13`. It is not inferred by assigning a position in the sorted genus-four spectrum. Finite marking/level covers preserve time parametrization and normalized exponents; no re-scaling of the flow is introduced.

## 4. Exact exclusion and rationality

The independently computed distances from `3/13` to the old values are respectively

`10/13, 7/26, 4/39, 2/65, 8/91`.

Half of the minimum separation is `1/65`. Convergence therefore puts every sufficiently late individual exponent in `(14/65,16/65)`, disjoint from the old set.

Rationality is not inferred from a numerical approximation or from rationality of the limit. For each individual Hilbert-modular curve the two relevant degrees are rational orbifold/parabolic degrees of algebraic automorphic line bundles. After a suitable finite level and cusp-unipotent cover they can instead be calculated as integral degrees divided by common finite-cover factors. The uniformizing degree is positive: it is proportional to the logarithmic hyperbolic cotangent degree. Their quotient is therefore a well-defined rational number.

The report and Gothic article reverse the names of the two foliation classes. Label by geometric role: the uniformizing degree is the denominator, the other is the numerator. The known examples and the normalization at most one select that convention. Merely inverting `3/13` would yield `13/3` and fail it.

## 5. Standard Hilbert quotient and common-cover transfer

The nonprincipal polarization is real and must not be erased. The Gothic arithmetic group stabilizes a full lattice of the form `b + O_D^dual` in K², whereas the original quotient uses `SL_2(O_D)`. Both are determinant-one stabilizers of commensurable full lattices in the same K-vector space.

Here is an elementary justification of the finite-index claim independent of any polarization identification. Choose an integer m with

`m L_0 subset L_1 subset (1/m) L_0`.

An element of the stabilizer of L_0 congruent to the identity modulo m² has `(g-I)L_1 subset m L_0 subset L_1`; its inverse satisfies the same relation. It therefore stabilizes L_1. The congruence kernel has finite index. Reverse the roles to obtain commensurability in both directions. This remains valid for nonmaximal quadratic orders.

Use the group intersection, acting on the same H×H, for the common cover. These covering maps are induced by the identity on the universal domain; no conjugation of potentially mixed determinant sign is necessary. Pull back an individual Gothic curve, choose a component, map to the standard quotient, and normalize its image. The graph parametrization survives, and the image is an algebraic immersed Kobayashi curve. Interior orbifold stabilizers and cusps can be handled after a common neat/unipotent level.

If the upstairs curve has degrees `(a,b)` and maps with degrees d and e to the two curve realizations, their degree pairs are `(a/d,b/d)` and `(a/e,b/e)`. Both ratios are a/b. The two covering degrees need not agree. Isogeny of the abelian factor, finite covering of the base curve, and equality of polarizations are three different issues; only the first two are used.

## 6. Rejected implications and computational controls

The audit explicitly rejects these tempting replacements for the proof:

- A new disconnected average implies a new individual exponent. Counterexample: weights `3/8,5/8` on old values `1/3,1/5` give `1/4`.
- Even an average limit of `3/13` rules out all-old components. Weights `3/13,10/13` on the same two old values give exactly that limit.
- Convergence implies attainment of `3/13`, supplies an effective threshold, or fixes the discriminant.
- Continuity of a sorted full spectrum identifies the Prym summand without additional bundle information.
- Rank two alone, or rel zero alone without tangent symplecticity, proves the required classification.
- Different labels, markings, or covering multiplicities imply different closed orbits.
- Changing polarization silently identifies the two Hilbert modular quotients.
- Passing arithmetic checks or matching PDF bytes verifies the deep theorems.
- Source-free execution is a source-verification pass.

`independent_checks.py` supplies 20 independent exact abstract controls and 11 disposable-copy mutation controls. It does not import the author's arithmetic function. The original checker was separately replayed: math-only exited 0; the source-free run exited 2 with `NOT_RUN_MISSING_SOURCES`; the run with all six independently retrieved PDFs exited 0. Same-size proof/PDF corruption, missing and renamed files, unexpected files, and symlinks were detected. Coordinated proof/manifest alteration was rejected by external binding even though the self-referential author integrity stage accepts it. This is the expected distinction, not a theorem-verification result.

## 7. Residual limits and disposition

No mathematical correction to the frozen conclusion is required. For exposition, retain the sheet/normalization convention and the subbundle/exterior-power explanation above whenever summarizing why the component gap is closed. They must not be replaced by the average formula or by an unqualified appeal to full-spectrum continuity.

The appropriate resolution is credited prior mathematics, with one author literature-verification approach. The primary original-source question is answered in the stated existential scope. The live-page text, raw catalogue/AI-report hashes, comprehensive repository history, a named new component fraction, and any stronger fixed-surface statement remain unverified or unclaimed. The audit did not redo the author's bounded repository-history search and makes no claim of exhaustive absence of earlier attempts.

The original freeze was not changed. No helper agent, external repository write, comment, PR, queue edit, merge or release was used. The safe audit contains authored analysis/code and public verification metadata only. Source PDFs, extracted text, rendered images, dataset records, and private coordination material are excluded.

## Public references

- [O] Martin Möller, contribution with Christian Weiss, *Twisted Teichmüller curves*, OWR 10/2014, pp. 563-564. DOI: https://doi.org/10.4171/owr/2014/10 . Publisher PDF: https://ems.press/content/serial-article-files/46498
- [G] McMullen, Mukamel, Wright, *Cubic curves and totally geodesic subvarieties of moduli space*, Annals of Mathematics 185 (2017), 957-990. https://doi.org/10.4007/annals.2017.185.3.6
- [A] Avila, Eskin, Möller, *Symplectic and isometric SL(2,R)-invariant subbundles of the Hodge bundle*, Crelle 732 (2017), 1-20. https://doi.org/10.1515/crelle-2014-0142 . Inspected version: https://arxiv.org/pdf/1209.2854
- [E] Eskin, Mirzakhani, Mohammadi, *Isolation, equidistribution, and orbit closures for the SL(2,R) action on moduli space*, Annals of Mathematics 182 (2015), 673-721. https://doi.org/10.4007/annals.2015.182.2.7
- [B] Bonatti, Eskin, Wilkinson, *Projective cocycles over SL(2,R) actions: measures invariant under the upper triangular group*, Astérisque 415 (2020), 157-180. https://doi.org/10.24033/ast.1103 . Inspected version: https://www.math.uchicago.edu/~wilkinso/papers/BEW28July2017.pdf . Publication verification: https://smf.emath.fr/publications/cocycles-projectifs-au-dessus-dactions-de-sl2-mathbb-r-mesures-invariantes-au-dessus
- [T] Möller, Torres-Teigell, *Euler characteristics of Gothic Teichmüller curves*, Geometry & Topology 24 (2020), 1149-1210. https://doi.org/10.2140/gt.2020.24.1149 . Publisher PDF: https://msp.org/gt/2020/24-3/gt-v24-n3-p02-s.pdf
