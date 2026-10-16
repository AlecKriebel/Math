# Independent cross-review of Group 3 metadata patches

Checkpoint: 2026-10-10 21:14 UTC / 14:14 PDT. Assigned cross-review: 100% complete. Parent application and remote identity/read-back checks remain outside this subtask. No Zenodo mutation, patch edit, external outreach or Git operation was performed.

## Judgment and scope

**All 14 patches pass this independent content and preservation review. No required metadata correction was identified.** The additions identify actual objects, source problems, standard synonyms and proof mechanisms; they do not promote conditional, inherited or asymptotic claims into stronger results. All 14 existing descriptions are already explicit and remain unchanged.

I read the exact deposited-paper extracts identified in `group_3_records.json`, including the statements, arguments, assumptions, boundaries and bibliographies; compared the original metadata and proposed patches; and reviewed `GROUP_3_REVIEW.md` and `GROUP_3_LINK_VALIDATION.json`. These are the checksum-matched extracts supplied by the parent catalog, not a substitution of a current repository draft. This review checks metadata fidelity to the submitted scholarly claims. It does not newly certify the proofs, historical priority, unread source editions or mathematical foundations imported by the papers.

Structural checks on every patch confirmed:

- Fields are restricted to `keywords`, previously absent `language`, and, in five records, `related_identifiers`. No title, description, creator, DOI, concept identifier, version, publication date, access, license or file field appears in a patch.
- Every existing keyword and related-identifier object is preserved. Lists contain 13–17 distinct tags, without promotional claims or invented MSC classifications.
- Language is absent in all 14 original records; all 14 patches add `eng`. The manuscripts are in English.
- The 14 new scholarly identifiers all use `references`. They are citations in the deposited bibliographies, not alternate identifiers for these papers, new versions, provenance replacements or claims that an inaccessible source was fully read.

## Record-by-record content challenges

### 23180194 — Measure-only preserving Markov transports characterize mass-stationarity

**Pass.** Theorem 1, p. 2, concerns a locally compact second-countable Hausdorff Abelian group, a jointly measurable action on an arbitrary measurable ambient space, sigma-finite Q and a nonzero covariant locally finite Radon random measure. The invariant test kernels preserve that measure and depend measurably on it alone. Sections 2–3 construct Campbell reversal through local symmetric gates and closed-period-subgroup transports. Palm distributions, Campbell measures, Haar measure, stationary random measures, measure-preserving kernels and Last–Thorisson Problem 7.3 therefore have direct content evidence; probability theory and stochastic geometry are justified subject categories.

The tags do not suggest a non-Abelian theorem or a deterministic allocation result. The unchanged description retains the narrower unresolved intensity-erased/Cox-allocation converse, absence of finite-intensity/standard-Borel/marginal-sigma-finiteness assumptions, credited classical equivalences and bounded priority findings. No reference was added.

Source: [mass_stationarity_markov.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23180194/mass_stationarity_markov.txt), Theorem 1 and §§2–4.

### 23174283 — Exact chordal separation of spherical Fibonacci points

**Pass.** Theorem 1 specifies the rational, unshifted configuration with q=F_n, n≥3, and exact minimum Euclidean chord 2/√q, uniquely at the pole/first-latitude pair. Sections 2–3 use dual Fibonacci lattice/product separation and a unimodular basis; the Zaremba index is a credited classical arithmetic input. The new discrete-geometry, sphere-point-set, minimum-distance, chordal-distance and Fibonacci tags identify this theorem. `hyperbolic-cross product separation` names the lattice product mechanism rather than a claim about hyperbolic geometry.

No packing-optimality, discrepancy, midpoint-height, irrational-angle or arbitrary-cardinality tag is added. The original description retains those exclusions and the construction/arithmetic attribution. The new Zaremba reference exactly matches bibliography [3]; the existing OWR problem source and discrepancy reference remain.

Source: [spherical_fibonacci_separation.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23174283/spherical_fibonacci_separation.txt), Theorem 1, arithmetic argument and bibliography [3].

### 23174156 — An explicit SU(5) lens-space counterexample to the printed Guadagnini-Pilo conjecture

**Pass.** Theorem 1 fixes ordinary full SU(5), WZW k=5 and shifted r=10, compares L(5,1) and L(5,2), and uses S³-normalized squared magnitudes 3475+1550√5 and 4025+1800√5 despite fundamental group Z/5. The A4 lattice and Hansen–Takata surgery formula are explicit in §2; cyclotomic certificates are §4. Quantum topology, RT, Wess–Zumino–Witten, 3-manifold invariants and fundamental group are direct search terminology.

The WZW-level tag is correct and does not confuse k=5 with r=10. The root-lattice tag does not change the invariant into a restricted/projective/spin category: §1 explicitly retains all 126 full-category labels. The unchanged description retains dependence on established modular-category and RT/surgery inputs and unresolved Kuriya priority, with no first-counterexample or historical-resolution claim. No reference was added.

Source: [pr95_note.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23174156/pr95_note.txt), Theorem 1 and §§1–5.

### 23171212 — The mixed point spectrum of a matrix contraction on its closed unit ball

**Pass.** Theorem 1 treats any finite-dimensional complex normed space and norm contraction, acting on all continuous complex functions on the closed unit ball. Lemmas 2–3 give the contractive peripheral projection and unimodular eigenfunction factorization; §3 uses Stone–Weierstrass, and §5 explicitly identifies the classical JdLG mechanism. Operator theory, dynamical systems, composition operators, peripheral spectrum and spectral projection are supported. `nonnormal contractions` is a legitimate included matrix class: neither normality nor diagonalizability is assumed.

The description continues to distinguish the missing mixed-case exclusion from earlier disk/peripheral/nilpotent facts and the immediate full-disk consequence. No holomorphic-observable, invariant-measure or new-general-decomposition claim is introduced. No reference was added.

Source: [pr91_note.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23171212/pr91_note.txt), Theorem 1, Lemmas 2–3, §§3–5.

### 23157237 — Consistent spectral recovery of smooth reversible diffusion tensors at a fixed lag

**Pass.** The model in §1 fixes a known smooth bounded connected domain, d≥2, smooth unknown tensor/density, stationary exact positions at one known positive lag, conormal reflection and known ellipticity/density bounds. Theorem 2 gives almost-sure local uniform tensor and separately fitted divergence convergence; the clipped tensor has a global L² limit. The dependent-data smoothing, spectral-jet excitation, ridge fit and continuous functional calculus appear in Lemmas 1/3, equation (11), Proposition 4 and equations (19)–(22).

`low-frequency observations`, `nonparametric diffusion estimation`, `anisotropic diffusion` and `inverse problems` are justified mathematical/statistical descriptions. The tags do not promise rates, minimax or computational efficiency, nonreversible/rough/noisy inference, global divergence recovery or a numerical implementation. The unchanged description retains these limits and credit for prior spectral fitting and eigenvalue-power weighting. No reference was added.

Source: [spectral_tensor_consistency.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23157237/spectral_tensor_consistency.txt), model (1)–(3), Theorem 2 and §§2–5.

### 23153134 — A complete negatively curved observation Gramian with two-state ambiguity

**Pass.** Theorem 1 and §2 construct a connected genus-three surface, zero dynamics, a hyperbolic double cover and a Nash output into R17. The actual differential observation Gramian is Tπ* g with curvature −1/T for each fixed T>0; histories are locally injective and exactly two-to-one globally. Double covers, genus-three surface, state indistinguishability, differential observation metric and Riemannian geometry are precise. Nonlinear control is the source subject even though the construction deliberately uses zero dynamics.

The unchanged description retains the fixed coherent coordinate normalization, fixed-time interpretation, manifold formulation and exclusion of a strengthened global-Euclidean-domain question. It credits classical constructions and retains the finite-verifier/global-topology distinction. No reference was added.

Source: [negative_gramian_cover.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23153134/negative_gramian_cover.txt), Theorem 1 and §§1–3.

### 23149775 — Focal pedal area ratios of closed elliptic billiards

**Pass.** Theorem 1 proves B±(w)=C0 A±(w), with positive C0 independent of phase and common to both foci, for the specified primitive convex/star orbits and elliptical caustics. It does not prove phase constancy of A+/A−; §5 gives an exact counterexample. Sections 2–4 explicitly use Jacobi functions, common compact-torus poles and residue matching. `Liouville theorem` is supported by the holomorphic compact-torus/constant step, not a different geometric or number-theoretic theorem. Planar geometry and pedal/Poncelet terminology are appropriate.

All exclusions, signed supporting-line area convention, older positive/negative cases and established-method attribution remain in the original description. No reference was added.

Source: [focal-pedal-ratios-note.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23149775/focal-pedal-ratios-note.txt), Theorem 1 and §§2–6.

### 23147866 — Asymptotic LOCC dense coding with the symmetric four-qubit W state

**Pass.** Sections 1–4 use independent Pauli codebooks, the A1B1:A2B2 receiver cut, a complete Bell measurement at receiver 1 and a cq multiple-access output local to receiver 2 after forwarding. Winter's theorem gives R1<3/2, R2<3/2, R1+R2<3/2+h2(1/4), so the sum-rate lower bound is approximately 2.311278 bits per resource copy and (9/8,9/8) is strictly interior. This is the exact achieved region, not a sum-rate-three claim.

The LOCC expansion, cqMAC acronym, multipartite-entanglement, Bell/Pauli, achievable-rate-region and quantum-Shannon/asymptotic terms are supported. None says optimal capacity or one-copy advantage. The unchanged description retains asymptotic uniform-average-error conditions and the original ownership/routing model, as well as credited Bell/coding ingredients. No reference was added.

Source: [w4_locc_dense_coding.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23147866/w4_locc_dense_coding.txt), Theorem 1 and §§1–5.

### 23146753 — Closedness and attractive approximation of binary MTP2 edge models

**Pass.** Theorem 1 concerns finite nonnegative unary/original-edge factors on the same fixed finite graph and the pointwise closure of positive attractive Ising distributions. Sections 2–3 explicitly handle lattice supports, pins, equalities and implications and use max-flow/min-cut residual reparameterization with nonvanishing normalizers. MTP2's expanded name, log-supermodularity, Markov random fields and algebraic statistics are standard supported categories/synonyms, including distributions with zeros.

The patch does not conflate finite factors with a generic toric closure or introduce hidden variables/edges. The unchanged description retains empty/isolated-vertex conventions, the classical frameworks and Gandolfi–Lenarda attribution for the separate earlier counterexample. No reference was added.

Source: [mtp2-edge-closure-note.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23146753/mtp2-edge-closure-note.txt), Theorem 1, Lemmas 2–3 and §§4–5.

### 23137834 — Full 5-torsion of the regular-pentagon quintic pencil

**Pass.** Theorem 1 and §§2–4 compute the genus-one normalization outside three excluded parameters, all 25 geometric 5-torsion points, the Tate twist, degree-ten residual polynomial and full division field of degree 4 or 20 with explicit Galois action. Birational normalization, quadratic twists, division polynomials, Kummer extensions, Galois representations, Weil pairing and the full level-5 modular cover are concrete objects/methods. Arithmetic geometry and genus-one curves are justified categories.

The original description retains credit to Fisher/Verdure/Morton and the known infinity subgroup, the allowed cuspidal plane member, no firstness/universal radical-solver claim and the excluded nonregular/star/Tate–Shafarevich variants. The added Morton v4 is the operative version expressly identified in bibliography [4]. Existing v1 and journal DOI remain, so the earlier residual-table/radical provenance and the operative-version distinction survive.

Source: [pentagonal-torsion-note.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23137834/pentagonal-torsion-note.txt), Theorem 1, §§2–5 and bibliography [4].

### 23133607 — A counterexample to Takao's self-duality question

**Pass.** Theorem 1 and §§2–3 construct p-torsion finite flat schemes of rank p^(2n), p>3 and n≥3, over the stated Witt-ring base; the explicit six-dimensional cyclic-word module has unequal image-intersection invariants under duality and a finite Honda complement. Supersingular elliptic p-torsion filtration, mixed characteristic, Witt vectors, contravariant Dieudonne theory and Cartier duality are actual content. Arithmetic geometry is an appropriate subject.

The exact base remains `W(closure of F_p)` in the original description; plain-text extraction loses overbars and is not grounds to replace it with W(F_p). No every-perfect-field descent, principally polarized Jacobian or surrounding Coleman-conjecture resolution is introduced. Added Hoshi revised and Pries–Ulmer publication URLs exactly match bibliography [2]/[4], as detailed below.

Source: [qss-self-duality-note.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23133607/qss-self-duality-note.txt), Theorem 1, §§2–3 and bibliography [2]/[4].

### 23131374 — Integer endpoint discontinuity of normalized uniformization for positively curved surfaces

**Pass.** Theorem 1 constructs a separate smooth complete positive-curvature sequence for every fixed finite integer r≥0 on plane and sphere: compact-open C^r convergence fails to induce compact-open C^(r+1) convergence of the actual normalized uniformization factors. Sections 3–6 use a radial twist, logarithmic perturbations and, only at r=1, the nonlinear curvature correction. The differential/Riemannian/conformal/quasiconformal terminology and exact topology/method tags are supported.

The unchanged description retains normalized parametrization rather than abstract-homeomorphism scope, smooth objects despite finite topology, exclusions of RP2/smooth/noninteger-Hölder conclusions, classical endpoint attribution and bounded priority. No reference was added.

Source: [integer_endpoint_discontinuity.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23131374/integer_endpoint_discontinuity.txt), Theorem 1 and §§1–6.

### 23131001 — An even-strand Markov calculus for classical and virtual links

**Pass.** Theorem 1 gives four reversible schemes for ordinary oriented unframed classical closures of tagged even-strand braid words and four extra virtual exchanges. The proof positively pads odd vertices of an unrestricted Markov chain and lifts relations, conjugation, stabilization and exchange. The entire keyword list is justified, including Artin relations and ordinary closure. `Markov theorem` identifies the imported classical/virtual calculus, without asserting a new unrestricted theorem or an algorithm for finding a chain.

All six added identifiers are bibliography [1]–[4], [8], [9]. The exact arXiv v1/v3 sources are respected. `references` is appropriate for Nencka and Fiedler despite limited full-text access: it says these are cited sources, not verified replacements for the current record. The description's explicit incomplete-priority paragraph and unread Nencka1998/1999/CPT96 qualifications remain verbatim. No historical-new-resolution, plat-closure, minimality, locality or search-algorithm claim is added.

Source: [even_strand_markov.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23131001/even_strand_markov.txt), Theorem 1, positive-padding proof, priority section and bibliography.

### 23130727 — An alternating antimorphic Fine-Wilf theorem

**Pass.** The exact alternating-prefix definition, Theorem 1 and §§1–2 support theta-periods, antimorphic involutions, reflected extension theta(w)w, ordinary periods 2p/2q, central reflection and the gcd threshold p+q−gcd(p,q). `generalized Fine-Wilf theorem`, `free monoids`, `periodic words` and `word reversal` identify the actual context. The uniform one-unit obstruction does not imply pairwise optimality; the original description preserves that qualification and the unrestricted fixed-letter convention.

The four added DOI references match bibliography [1], [2], [4], [5]. The OWR identifier is the 2010 workshop volume even though its publication is 2011. Kari–Seki publisher metadata identifies the cited article, without claiming the manuscript's inaccessible publisher-final body was read. The existing access/version disclosures survive verbatim.

Source: [alternating-antimorphic-fine-wilf.txt](/Users/alec/Documents/Math/zenodo_discoverability_20261010/papers/23130727/alternating-antimorphic-fine-wilf.txt), definition, Theorem 1, related-results section and bibliography.

## Added scholarly identifiers: independent source comparison

Each row is newly added, using `references`; no existing reference is removed. Exact DOI strings may differ in case from publisher registration because DOIs are case-insensitive. The drafter's live primary-source identity receipts are in [GROUP_3_LINK_VALIDATION.json](/Users/alec/Documents/Math/zenodo_discoverability_20261010/reviews/GROUP_3_LINK_VALIDATION.json); I independently checked every addition against the exact deposited bibliography and its use in the paper.

| Record | Added identifier | Exact source and qualification | Judgment |
|---|---|---|---|
| 23174283 | `https://www.fq.math.ca/Scanned/8-2/zaremba.pdf` | Zaremba original, bibliography [3]; classical Fibonacci product index, credited rather than newly claimed | Pass |
| 23137834 | `https://arxiv.org/abs/1612.06268v4` | Morton [4], operative v4 dated 11 June 2018; v1 remains for earlier table/radical | Pass |
| 23133607 | `https://www.kurims.kyoto-u.ac.jp/~yuichiro/rims1911revised.pdf` | Hoshi [2], exact revised author manuscript, March 2021 | Pass |
| 23133607 | `https://nyjm.albany.edu/j/2021/27-27v.pdf` | Pries–Ulmer [4], On BT1 group schemes and Fermat curves, NYJM27 (2021), 705–739 | Pass |
| 23131001 | `10.4064/bc103-0-1` | Fenn–Ilyutko–Kauffman–Manturov survey [1], source Problem42 | Pass |
| 23131001 | `10.1112/blms.12761` | Gorsky–Kivinen–Simental [2], classical Markov foundations; Wiley metadata matches after Crossref429 | Pass |
| 23131001 | `https://arxiv.org/abs/math/0008092v1` | Kamada [3], precise v1 virtual braid/Markov source | Pass |
| 23131001 | `https://arxiv.org/abs/math/0507035v3` | Kauffman–Lambropoulou [4], precise v3 virtual exchange formulation | Pass |
| 23131001 | `10.1090/conm/233/03432` | Nencka [8], identified 1999 chapter whose full text remains unavailable | Pass: citation identity, not a read-proof claim |
| 23131001 | `10.1142/S0218216503002561` | Fiedler [9], Markov Moves Cannot be Replaced by Double Markov Moves; limited preview/abstract comparison retained | Pass: citation identity, not proof certification |
| 23130727 | `10.1090/S0002-9939-1965-0174934-9` | Fine–Wilf [1], Uniqueness theorems for periodic functions, 1965 | Pass |
| 23130727 | `10.4171/OWR/2010/37` | Nowotka/Bischoff workshop contribution [2], printed pp.2219–2222; report year2010/publication2011 | Pass |
| 23130727 | `10.1016/j.tcs.2009.09.037` | Czeizler–Kari–Seki [4], On a special class of primitive words, TCS411 (2010), 617–630 | Pass |
| 23130727 | `10.3233/FI-2010-285` | Kari–Seki [5], FI101 (2010), 215–236; author-version/final-body comparison limits retained | Pass |

The five reference arrays retain all pre-existing objects. References do not establish novelty, endorse an unread claim, imply identical editions or redefine the paper as a version of the cited work. No `isNewVersionOf`, `isIdenticalTo` or provenance relation was added.

## Broad terminology adversarial check

No required removals. The broad additions are ordinary disciplines appropriate to their manuscripts: probability/stochastic geometry, discrete geometry, quantum topology, operator theory/dynamical systems, inverse problems, nonlinear control, planar geometry, quantum information/Shannon theory, algebraic statistics, arithmetic geometry, differential geometry and knot theory. They are paired with narrower object and method tags rather than used as standalone evidence of a claim. Deliberately challenged near-boundary tags were `nonnormal contractions` (included by the norm-general theorem), `low-frequency observations` (fixed positive lag), `nonlinear control` (the observability problem's discipline despite zero dynamics), `Liouville theorem` (explicit compact-torus analytic step), `Galois representations` (displayed action matrices), `mixed characteristic` (Witt-ring lift) and `hyperbolic-cross product separation` (Fibonacci dual-lattice product). All have checkable support.

## Preserved gaps and application boundary

There is no unresolved metadata-content objection in this group. Manuscript scientific/priority limits remain: inherited category/coding/classical frameworks; finite diagnostics rather than universal proof certificates; no human refereeing; bounded priority audits; unread final editions and historical sources, especially Kuriya and Nencka; model/domain/topology/asymptotic exclusions. These must remain in the applied descriptions exactly as they are in the originals.

The parent still must apply through a metadata-only workflow and verify the same published record DOI/concept DOI/version, files, creators and preserved descriptions after read-back. This local cross-review cannot itself certify that a later API operation avoids a version bump or new DOI; it verifies that these patch contents contain no such requested mutation.

## Reviewed patch receipts

The following SHA-256 values bind this judgment to the exact local patch bytes at review time. Any later modification requires checking the relevant changed content again.


| Record | SHA-256 |
|---|---|
| 23180194 | `ff3489f12c8d24c28fb88fd66860cd98eec03d19e35f6b4d3f559a1599c36b28` |
| 23174283 | `aa4a05549ae5670d1cbee1934d6fef1f1c602e6a88fb080beb3d0b9b14811e8a` |
| 23174156 | `2ccd492860cdb963c2ae69a0f87364f68dd9bbda31883335c0989e4d8b199e3c` |
| 23171212 | `4ed29053ada45849a669703d6f0b124e9f4ded2e279816a3b40a2dd216ea3b49` |
| 23157237 | `1319dd3373b27b583d02016621a5dacb7bcb79cb8a8180b029e46977e5126fc4` |
| 23153134 | `65494d5e235bd6f02c66e3e1f9d460b686dc1439a37064402d828b4f44559b64` |
| 23149775 | `d5c2b0e12d9c6b2191fe2250948e54627840f602241e89726dc5d2a6e4d15864` |
| 23147866 | `f3742e3a46c13bafbaeca78283fbfa24ee93ee019b0b7eaa41bdd4d1b221bb34` |
| 23146753 | `35843473a15e213f67b0ccbb355dc4d6450cfe2b76a8ba9d3922517557bd1b72` |
| 23137834 | `e3be3a13f28f5424eadfd03c30f8cdadd7b5094815b8d4824613cb521769c45f` |
| 23133607 | `69893f6002e0dc8215d3c7b470767e592453f26722dbd9fd0f476103ad5823d1` |
| 23131374 | `785341f866bb6f89bf2454a309fae1e032c029aa7c001f10c6469430f24330f8` |
| 23131001 | `3b37646562d9542a54859862f970c3d30036de2e6a27b29f7589063f62935992` |
| 23130727 | `a291ae73a78271c13d942c156fad4a2d62a3c18cbb532d2884fe64bde1155c21` |
