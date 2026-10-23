# Independent public-package acceptance: subcategory TQFT interface

**Target:** Kawahigashi Problem 9.4, record 1787, 10400168 / AMR-103-0168.  
**Review date:** 14 October 2026 UTC.  
**Verdict:** **ACCEPT the sealed public reader at its declared mathematical scope.**

The reviewed archive is `SUBCATEGORY_TQFT_1787_INTERFACE_PUBLIC.tar.gz`, 104,130 bytes, SHA-256 `2ac0a8a5cbad9cbdcac77df2eefa989908403137a6d82235627cdf7770737307`. Its root `MANIFEST.json` is 8,849 bytes, SHA-256 `43245422144e64a0d17ed963847cbcb70d1e6b3139232d09bc48db82e0c53504`. Acceptance was issued after the archive was sealed and independently restored, inspected, and tested. It applies to these exact bytes.

This review checks mathematical claim fidelity, evidence bindings, public-content boundaries, archive integrity, and executable finite validation. It adds no mathematical research pass and does not represent external journal peer review. It neither certifies novelty nor establishes present-day openness of stronger formulations.

## 1. Mathematical claim fidelity

### Inclusion-dependent interface and trace

The reader correctly states the accepted input: a full strong monoidal fusion-subcategory inclusion `i: D → C` over the complex numbers with inherited spherical pivotal structure. The wall is the ambient category with restricted left action and regular right action, `_D C_C`, carrying `t_m(f)=tr_C(f)`.

The retained proof verifies finite semisimplicity, coherence, cyclicity and nondegeneracy on all Hom pairs, both partial-trace identities, and compatibility of the combined actions. Evaluation at the tensor unit recovers the supplied monoidal inclusion from its left action on the regular right module. The reader does not substitute an unrelated common property of the two bulks or a general trace-existence assertion for this concrete construction. The inherited-pivotal requirement remains explicit, including its incompatible-pivot countercheck.

### Full functor and exact normalization

The claim is a full oriented `(3,2)` defect functor on the cited compatible stratified bordism category, with cylinder-projector state spaces, sewing, diffeomorphism invariance, and disjoint union. The two constant-bulk restrictions are monoidally naturally isomorphic to their own normalized TVBW theories. A fully extended oriented theory down to points, and equality with Meusburger's entire defect model, are not claimed. The attribution to Carqueville–Müller Definitions/Theorems 5.16–5.18 and 6.4, Example 6.5, is retained. [Published source](https://doi.org/10.1007/s00220-025-05434-y).

Each bulk uses its own nonzero spherical global dimension. The boundary comparison is precisely the coloring-dependent diagonal operator with entries

`f_A(Σ,Γ;c) = Dim(A)^(|Σ minus Γ|/2) product_e d_(c(e))^(-1/2)`.

The direction is `Z_orb(Y)=F_out^(-1) p_TV(Y) F_in`, hence `J_out Z_orb(Y)=TVBW_A(Y) J_in`. It conjugates cylinder projectors and is multiplicative under disjoint union. It is neither a coloring-independent scalar nor a claimed formula for all mixed-phase raw boundary amplitudes. Consistent root choices and the separate normalization of each bulk remain explicit. The reviewer independently checked the retained source text and page image for the incoming/outgoing ratio in CRS equation (4.70). [Inspected arXiv v2, p. 41](https://arxiv.org/pdf/1809.01483v2#page=41).

### Historical model and α-induction

Coverage is stated for complete finite spherical Barrett–Westbury data and compatible based restrictions, retaining the unit, duals, all simple tensor summands, full multiplicity spaces, and the supplied associator, duality, pivotal, and normalization data. The source's abbreviated numerical axiom sketch is not advertised as a reconstruction theorem for bare arrays or arbitrary linear subalgebras. No positivity, unitarity, pseudo-unitarity, braiding, modularity, or S-invertibility restriction has been silently imposed on the general categorical construction.

The actual BEK ambichiral/chiral/full/ambient and subsystem inclusions are distinguished from α-induction itself, which need not be fully faithful. The KO local-module inclusion into all modules retains its finite ribbon, connected commutative rigid-algebra, nonzero-dimension, and trivial-twist hypotheses. The free-module and forgetful functors are not substituted for that inclusion. The reader preserves the further hypotheses of BEK's product corollaries and Sato's conditional formulas. It does not claim a universal singular-S product formula. [BEK](https://arxiv.org/pdf/math/0002154v1), [Kirillov–Ostrik](https://arxiv.org/pdf/math/0101219v3).

The disclosed finite-group normalization distinction is retained: the displayed normalized state sum gives representation-groupoid cardinality rather than an unweighted conjugacy-class count. This is presented as a narrow convention discrepancy, not a paper-wide allegation. [Historical source, pp. 509–510](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf#page=137).

### Ordinary-map, center, and equivalence limits

Wall cylinders supply decorated comparison maps, without asserted naturality against all undecorated topology-changing bordisms. Unequal sphere values and torus dimensions in the finite examples are used only to exclude stronger ordinary-map, equivalence, universal-injectivity, and constant-ratio conclusions. They are not manufactured as additional requirements of the qualitative source question.

The relative-center report preserves composition as the endofunctor tensor convention and the braided central action `overline{Z(D)} ⊠ Z(C) → Z(E_i)`. The overline reverses the braiding, not arrows or the tensor product. The reviewer independently checked the retained Kong–Zheng page image for this convention. The report does not make the relative center itself braided or identify the two bulk centers. The cited braided equivalence is not promoted to an unverified pivotal/ribbon or oriented-amplitude comparison. [Kong–Zheng, p. 13](https://arxiv.org/pdf/1507.00503v3#page=13).

Untraced wall equivalence is qualified by fixed bulk labels and inner conjugacy; a unit marking recovers the inclusion up to monoidal natural isomorphism. Literal preservation of the selected trace additionally requires `dim_C(u)=1`. The distinction from possible Euler-completed defect equivalences remains explicit. The underlying restricted regular wall is invertible only when the inclusion is a tensor equivalence. Algebraic reversal and relative tensor products are not presented as automatically normalized physical cancellation rules.

### Acceptance and novelty wording

The final source-scope acceptance supports the existing-result answer under the documented complete spherical-BW/based-subsystem interpretation. Historical source-only reports remain clearly identified as earlier stages. The current reader does not leave the accepted interpretation unresolved merely because stronger outputs were neither required nor obtained. The construction is consistently described as an application of existing theory, with no novelty certificate.

## 2. Exact identities and public-content boundaries

The independent review verified all **33 original/public identity records** against the actual authored originals and shipped bytes. **31 are byte-for-byte copies.** The two limited public editions are:

- `CONSTRUCTION_CONTRACT.md`: operational/archival directions are replaced by a historical-status explanation; the substantive source contract is preserved.
- `pass1_scope/SOURCE_SCOPE_ACCEPTANCE.md`: queue-administration recommendations are replaced by a public disposition paragraph; the mathematical acceptance, explanations, limitations, and citations are preserved.

All **16 acceptance/input bindings** match. The final mathematical-audit manifest is pinned at `ae7d65b3fda8741dc740e177b97af2a4d1edd6fab7f341cffcaba22b8433c4ad`. The original source-scope acceptance is pinned at `ef7b9d186ae4a0f526ae1fadc1a39547d5fdf5b918a467cc1a919847070cef41`; its adapted public edition is 8,126 bytes, SHA-256 `9c787bc527769af0d61e4d3d1e759100f2e07f5682be3b90a0995d0e4e7dd2a4`.

The nested original-input manifests and the source disposition's original-report hash are accurately explained in `REPRODUCIBILITY.md`. The root manifest, identity ledger, and bindings identify the different public edition without pretending it has the original hash.

The archive contains only authored Markdown, JSON verification material, and Python checks. No source PDFs, source-page images, extracted source text, external dataset records, or private coordination material are included. Generated finite-example results are authored validation outputs, not copied external datasets. Source-file metadata were checked against **14 distinct retained PDF identities across 37 records**; this is local byte verification, not a fresh download or renewed inspection of every cited proof. Preprint-versus-publisher inspection limits remain disclosed.

All **55 relative Markdown links** resolve inside the public package. Public scholarly links remain source references; this review does not certify their future availability.

## 3. Archive integrity and reproducibility

The archive contains exactly **48 regular files**, matching the root manifest's 47 payload entries plus the manifest itself. Every archived file matches the public tree byte-for-byte. There are no duplicate or unsafe member names, symlinks, hard links, or nonregular objects. Paths are sorted under `public/`; ownership and timestamps are normalized, file mode is `0444`, and the gzip timestamp is zero. Two independent in-memory reconstructions were byte-identical to each other and to the sealed archive.

All **five public Python scripts** were inspected and exercised from restored disposable copies. The root replay wrapper passed under normal, optimized, and double-optimized Python. Across those wrapper runs:

- **18 successful finite executions**, each with **17,857 explicit checks**
- Every finite output exactly matched the retained 52,503-byte result, SHA-256 `698e921b5b199738d7d6af5d1b98b73c81ee2830740e0cb86ccbe92f0a3b454f`
- **18 intentionally false guard probes** rejected
- No optimization-sensitive Python `assert` statements in the five scripts
- Original orchestration scripts and regenerated output/receipt comparisons exercised in disposable copies

The 15 packaged integrity mutations were each rejected under all three verifier modes, giving **45 rejection checks**. These cover byte changes, missing/extra files and directories, symlinks, a FIFO, unsafe/duplicate/self-referential manifest paths, wrong sizes/hashes, noncanonical JSON, duplicate JSON keys, and a wrong external manifest pin.

The reviewer also introduced three independent semantic mutations: a wrong torus-dimension expectation, a wrong sphere-value expectation, and an incorrect pivotal-constraint matrix. Each failed with the expected diagnostic in all three modes, giving **9 additional negative controls**.

The restored package and sealed public files remained unchanged. These checks validate the finite computations and integrity machinery; they do not computationally prove the general defect-TQFT theorem. Authentication still requires a trusted external archive or manifest pin.

## 4. Final disposition

**Accepted for use as the sealed public research reader and verification package.** No unresolved public-package defect was found. The accepted mathematical answer remains the inclusion-dependent interface under the explicit complete spherical-BW/based-subsystem interpretation, with all stated qualifications intact.

This reviewer performed no repository edits, publication, or new mathematical pass. Any later payload change requires a new manifest/archive identity and a corresponding review; this acceptance does not extend automatically to changed bytes.
