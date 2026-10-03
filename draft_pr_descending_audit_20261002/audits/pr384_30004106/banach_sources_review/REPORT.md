# Independent source, Banach-algebra, and turns 1–2 audit

**Disposition: PASS for the audited scoped claims. No mandatory correction found. The original universal question remains unsolved, 5/5 author turns. No novelty certification.**

Frozen PR384 head: `682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6`. All 52 frozen file lengths and SHA256 hashes match `snapshot_manifest.json`. This audit changed only its own folder. It performed no Git/index/queue/PR/service writes and no outside communication. Source reconstruction and proof mechanisms were recorded in `INDEPENDENT_RECONSTRUCTION.md` before the previous review was read. The prior verdict was subsequently compared and agrees for this assigned scope; it was not evidence for the verdict.

## Exact target and source binding

The primary source is Benson's contribution on printed pp847–849 of [OWR14/2019](https://ems.press/journals/owr/articles/16776), with the question on p849/PDF9. A fresh download matches the frozen source hash. That page was independently rendered and visually inspected: the conjugation bars are present in both character formulas. EMS records publication on 27 February 2020, despite the volume year 2019.

The modules are finite-dimensional representations over an arbitrary characteristic-p field k. The algebra is the complexification of the **split** Green ring, with indecomposable isomorphism classes as a free basis, completed in the norm

`||sum c_M[M]|| = sum |c_M| dim_k M`,

and involution `sum c_M[M] -> sum conjugate(c_M)[M*]`. Complex scalars for the Banach algebra do not change the characteristic of the module field. The exact universal claim is that `Spec(x*x)` lies in `[0,infinity)` for every element x of this completion, equivalently every bounded complex character is a *-character. The modular unresolved regime has p dividing |G|. Ordinary characters, positive tensor-growth identities, stable/projective quotients, maximal quotients, semisimplicity, and further C*-completions are different objects or weaker conclusions.

Fresh full-text sources:

- [Benson arXiv2008.13155v2](https://arxiv.org/abs/2008.13155v2), 30 April 2022, 120-page accepted manuscript. The exact involution and symmetry equivalences are in Proposition2.9.10; Proposition3.4.2 translates them to Green rings; Question5.15.2 on printed/PDF111 still asks for full symmetry.
- The author's `banach-book.pdf` independently matches the frozen hash. PDF metadata gives 11 June 2020 and 123 pages. It must not be described as a newer edition.
- The 2024 Memoirs publication is identifiable as volume298, number1488, DOI10.1090/memo/1488. The official full publisher PDF was not retrieved (official AMS retrieval returned403). No byte identity, theorem-number identity, or unchanged-problem assertion about that inaccessible edition is inferred.
- [Kua–Lim arXiv2603.11533v3](https://arxiv.org/abs/2603.11533v3), 24 August 2026, is restricted to the symmetric group on p letters over an algebraically closed characteristic-p field. Its inspected introduction and scope concern tensor products modulo projectives and module-growth invariants; they supply no universal full-completion theorem.
- [He arXiv2408.04196v2](https://arxiv.org/abs/2408.04196v2), 4 February 2025, studies the number of indecomposable summands over an algebraically closed field, including faithful-module asymptotics. This is distinct from all bounded Green-ring characters. Its current arXiv metadata now has journal reference Ark.Mat.64(2026),91–120; the downloaded v2 PDF is still the precise frozen referenced version. Updating that bibliographic fact is optional and does not alter the mathematics.

All five frozen primary source hashes matched independent fresh retrievals. Source receipts also bind a sixth retrieved source, the primary Benson–Symonds author manuscript, used to cross-check the credited growth dependency. Raw PDFs, text extractions, and the visual page stay inside the ignored `raw_sources/` directory and are not part of the report whitelist. The search was bounded; the review does not prove that no prior resolution exists.

## Turn 1: field extension and local species

### Algebraic scalar extension

The written finite-degree argument is sufficient. Extension E is a unital ring homomorphism and commutes with duality. Restriction R need only be additive. For a finite extension of degree d, positivity of decomposition multiplicities and preservation of total vector-space dimension give

`||Ex|| <= ||x||`, `||Ry|| <= d||y||`, and `RE=d id`.

Applying them to complex virtual combinations forces equality of norms. It permits splitting, repeated summands, and cancellation; assuming an indecomposable stays indecomposable would be wrong. No separability, normality, perfection, or algebraic-closure assumption is hidden.

The infinite algebraic-extension argument also works. The finitely many matrices defining a finite list of decompositions and repeated-type isomorphisms descend into one finite subextension. A summand indecomposable over the larger field is indecomposable there; summands distinct over the larger field cannot become isomorphic over the subextension. All deliberately repeated types were already identified using descended isomorphisms. Thus the finite-support norm is computed exactly at that finite stage, before extending by density. The completed image is closed because the map is isometric and the domain complete.

An independent collision argument confirms the mechanism without an unquoted Noether–Deuring hypothesis. For distinct indecomposables U,V of a finite-dimensional algebra, every composite `U -> V -> U` belongs to the nilpotent radical of the local algebra End(U); otherwise U splits off V and hence equals V. Finite-dimensional Hom spaces commute with any field extension. If KU and KV shared a nonzero summand, inclusion and projection would yield a nonzero idempotent composite in `K tensor rad End(U)`, which is a nilpotent ideal, contradiction. This proves disjointness of scalar-extended supports even for arbitrary field extensions and independently verifies the author’s narrower algebraic-extension theorem. It is not a novelty claim or evidence from finite replay.

Symmetry descends by equality of the norms of every power, hence equality of spectral radii for x and x*x. The commutative symmetric-radius criterion then applies inside the smaller algebra. The manuscript correctly avoids assuming every character of a Banach subalgebra extends to its ambient algebra or that arbitrary subalgebras are inverse-closed. No equality of arbitrary spectra is needed.

### Countable closure and compactness

The tensor products `M^a tensor (M*)^b` contain finitely many indecomposable summands each, and the countable union is closed under duals and product summands. Its weighted coordinate span is a closed unital *-subalgebra. Symmetry of the ambient algebra implies symmetry there by the same power-norm argument. Conversely, an ambient character restricts to each one-module subalgebra; respecting duality on every basis element implies respecting it on the dense finite span and then the whole completion. This proves the stated equivalence.

If z,w are the character values on M,M*, the imaginary parts of the two selfadjoint witnesses `M+M*` and `i(M-M*)` are respectively `Im z+Im w` and `Re z-Re w`. Both vanish exactly when `w=conjugate(z)`. Therefore a non-Hermitian species has a finite selfadjoint witness even though its tensor closure can be infinite. The second witness usually is not an actual module; signed/complex elements remain necessary.

For a countable tensor-closed basis, the disk product `prod_i {|z_i|<=dim M_i}` is compact. Unit and multiplication equations define closed subsets and each uses finitely many coordinates. Their simultaneous solutions are precisely contractive characters: the disk estimates control every finite linear combination and allow continuous completion. The fixed closed defect condition `|z_(M*)-conjugate(z_M)|>=epsilon` has the necessary positive epsilon. Compactness gives the finite-intersection criterion with the correct universal quantifiers over finite subsystems and rational epsilon. Integer multiplication/dimension data become finite real polynomial constraints. No effective enumeration over arbitrary fields is assumed.

This reformulation supplies no general finite exclusion or actual non-Hermitian species. As a route to settling the central question, it is **blocked** until there is a materially new character-exclusion mechanism or a compatible infinite construction.

The deliberately nonstandard involution on l1(Z) is an accurate negative control outside the Green-ring axioms. It is not an actual-group counterexample. It demonstrates why positive radius identities alone do not establish full symmetry.

## Turn 2: endotrivial growth, characters, and p-group splitting

### Precise credited dependency and access limit

In Benson v2, Chapter4 takes k to be an arbitrary field of characteristic p. Theorem4.4.8 states the endotrivial `gamma_G(M)=1` result for kG-modules without an algebraic-closure restriction. The chain is explicit: Theorem4.4.2 cites Carlson1981 Theorem3.7 for a uniform core-dimension bound; Theorem4.4.4 takes nth roots to detect gamma on elementary abelian subgroups; Proposition4.4.6 cites Dade1978 I/II for elementary abelian endotrivial syzygies; Lemma4.4.7 uses polynomial growth of ordinary syzygies, with p dividing |G|; these imply Theorem4.4.8. These hypotheses cover the packet’s use.

The independently retrieved primary [Benson–Symonds author manuscript](https://personalpages.manchester.ac.uk/staff/peter.symonds/preprints/bs1.pdf) has arbitrary k in its introduction, field-extension invariance in Lemma2.11, the same Carlson/Dade chain in Section7, and the endotrivial theorem7.5. It supplies an additional direct source check, not an independent proof of the classified inputs.

The [official Dade I page](https://annals.math.princeton.edu/1978/107-3/p06) confirms Ann.Math.107(1978),459–494, DOI10.2307/1971125; it provides no full article PDF here. The official Dade II endpoint and attempts to retrieve Carlson1981’s original full text did not yield those originals. Those original proofs were therefore **not** independently reread or certified. They remain credited classical inputs through the controlling retrieved theorem. This is an access limitation, not a missing hypothesis or a reason to replace the theorem with finite evidence.

### Weighted stable group algebra

When p divides |G|, k is a nonzero indecomposable stable unit. Tensoring by a stable invertible object preserves indecomposability. Krull–Schmidt and removal of projective summands therefore yield one unique nonprojective indecomposable representative E_t for every stable endotrivial class t. Inverses are duals and multiplication of cores is the group law. This reasoning is valid over arbitrary k and does not assume finite generation of the endotrivial group.

The stable coordinate norm gives exactly `l1(T,w)` with `w(t)=dim E_t`, not a replacement norm. It satisfies `w(1)=1`, `w(t)>=1`, `w(t^-1)=w(t)`, and `w(st)<=w(s)w(t)`. The credited gamma theorem supplies `lim w(t^n)^(1/n)=1` for each t and its inverse.

A character’s nonzero values lambda(t) form a homomorphism to C*. Applying the norm bound to every power gives `|lambda(t)|<=1`; using the inverse gives the reverse bound. Hence the character is unitary. Conversely every unitary group homomorphism defines a bounded multiplicative Fourier sum, with absolute convergence controlling products. The complete character space and spectrum formula follow. Thus all elements, including infinite sums and complex combinations, lie in a symmetric stable sector. Restriction of an ambient character suffices; character extension is never assumed.

The twisting-defect formula is correct: multiplication by an endotrivial factor multiplies the defect by its inverse unitary value. It preserves the defect’s absolute value for that character. It does not constrain an unrelated species on other modules.

### Actual full/stable p-group algebra

For a nontrivial p-group over every characteristic-p field, kG is local and every finite projective is free. The regular projective P is the unique indecomposable projective. The diagonal tensor identity `P tensor M = (dim M)P` and self-duality give the central selfadjoint idempotent `e=P/|G|`, with norm1. The orthogonal idempotent f=1-e has norm2. The projective ideal is Ce, so the full algebra splits as `Ce x fA`, with factor units e and f. The stable quotient identifies with fA.

For the canonical nonprojective representative of a stable element x, let D(x) be its coordinate dimension sum. The lift is `J(x)=x-D(x)e`. Projective and nonprojective supports are disjoint, so exactly

`||J(x)|| = ||x||_st + |D(x)|`,

and consequently `||x||_st <= ||J(x)|| <= 2||x||_st`.

J is multiplicative because it uses the central idempotent projection, not because D is multiplicative on the stable quotient. That latter statement is false and the packet correctly disclaims it. Taking nth roots of the two-sided power bounds gives spectral-radius equality with the stable factor. Full spectra are the union of the scalar-factor spectrum and the stable-factor spectrum; inverses exist precisely when both components are invertible. The distinct factor units matter.

The closed coordinate span of P and all E_t is a unital *-subalgebra, because tensor products give another E_t plus a free projective summand. It is the product of Ce and J of the symmetric stable weighted algebra, so it is symmetric. The trivial p-group/semisimple boundary has no nonzero stable unit and is handled separately by the ordinary scalar algebra. The argument is not transported to general finite groups with several indecomposable projectives.

The equivalence “full p-group symmetry iff entire stable symmetry” transfers the central difficulty to an equivalent unsupported claim. It is **blocked as a universal resolution**. The proper endotrivial/projective sector theorem is verified, but no positivity theorem on arbitrary additional indecomposables follows.

## Reproducible independent controls and negative boundaries

`independent_controls.py` has no author imports, uses the standard library, and passed **85,360 exact assertions**. The receipt distinguishes finite checks from proofs of infinite statements. The materially distinct controls are:

1. Actual characteristic3 C3 Jordan tensor products, derived from finite-field matrix ranks of the diagonal group action.
2. Actual characteristic3 C3 x C4 modules over F3 and F9: the irreducible two-dimensional F3[C4] module splits into its two exact F9 eigenlines. This yields the nine-to-twelve indecomposable scalar-extension pattern in a genuinely modular example. Tensor compatibility, inverse duality, restriction/extension, signed isometry, and Gaussian-integer complex norms are checked. No arbitrary-field theorem is inferred from this example.
3. The actual full C3 Green algebra `V^2=1+P`, `VP=2P`, `P^2=3P`, with its three characters. Exact Gaussian-rational products, star compatibility, 294 explicit complex inverses, orthogonal factor units, and the exact lift norm bound are checked. The dimension sum fails stable multiplicativity (`D(V)^2=4`, `D(V^2_st)=1`), and f has scalar component zero so cannot be treated as the full unit.
4. Polynomially weighted Z truncations admit rational nonunitary values with defects tending to zero while satisfying every constraint in that finite range. This catches the invalid inference from finite feasibility or from an unspecified positive defect to a compatible infinite species. The fixed epsilon compactness argument is a written proof, not a replay result.
5. The exponential symmetric weight `w(n)=2^|n|` admits evaluation `u->2`, with dual value1/2, so dropping subexponential growth breaks symmetry. It also embeds injectively by Fourier sums into C(S1) as a *-algebra, showing why an injective continuous map into a C*-algebra alone does not ensure spectral invariance. The selfadjoint `i(u-u^-1)` has character value3i/2 at this evaluation. This is an abstract boundary, not a Green-ring counterexample.
6. The two selfadjoint witness imaginary parts have squared sum exactly equal to the squared duality defect, detecting omitted conjugation or an incorrect witness formula.

Before replay, both frozen author scripts were inspected in full. Only own-folder copies were executed with Python `-B`. Turn1’s23,589 assertions and Turn2’s61,260 assertions reproduce their frozen JSON receipts byte-for-byte (84,849 author assertions total). Author Turn2 explicitly labels its dimension-weighted p-group-type model as abstract; this audit’s actual C3 and C12 controls supplement it. Neither collection is used as evidence for a universal infinite theorem.

## Final gap and required disposition

The strongest verified result in this assigned scope is symmetry of the complete stable endotrivial weighted algebra and its full projective/endotrivial p-group lift, with exact character and norm descriptions. The source problem still requires a proof that every bounded species on all remaining actual indecomposable directions respects duality, or an actual finite-group/module-field counterexample carrying a complete non-Hermitian character or nonreal selfadjoint spectral certificate. Algebraic closure reduction, countable compactness, scalar/projective splitting, and checks on positive module classes do not supply that result.

The proper-family results and precisely labeled blocked routes warrant the scoped PASS. Keep the original status **unsolved,5/5**. No sixth author turn, novelty claim, universal solution, or external outreach is authorized or warranted by this audit. No mandatory issue or reasonable mathematical correction was found in the source scope and turns1–2 at the frozen head.
