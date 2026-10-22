# Independent adversarial audit: rank 585 / problem 2306063

Audit date: 2026-10-04 UTC. Target: Function Theory 6.63, AMR-022-6063.

## Verdict

**PASS AS AN UNSOLVED, FIVE-APPROACH PACKAGE OF RESTRICTED RESULTS.**

No fatal mathematical error or mandatory correction was found in the frozen package. The original fine-C0 openness problem is not solved, and the package does not claim otherwise. It is suitable to proceed to the separate publication gate with status **unsolved, 5/5**, preserving its restrictions, negative applicability findings, source-provenance caveats, and non-novelty statements. This verdict is not a solution certificate or an exhaustive literature-status determination.

The independent audit read all twelve public files, checked the principal arguments separately, inspected the relevant primary-source text and page images, and replayed the controls. No helper was used, no frozen public file was changed, and no remote write was performed during this audit.

## Frozen identity and mechanical reproduction

The reviewed directory is the package's `public` directory. The two anchors supplied at handoff match exactly:

- SHA256SUMS.json: f9a155e07ffa4391de564c59d147c26071b0dfb7de5b37ee127c27e8b99fa0ed
- PROOF.md: d020ba52a186b8384c651311e86c5860eb77c39256c25be87cced7759f503272

The manifest contains eleven file records, plus the manifest itself, giving exactly twelve public files. Every length and hash matches; no additional file is present. The public inventory contains Markdown, JSON, and Python only. The six privately downloaded PDFs match their listed source hashes and byte counts. Those checks establish byte consistency with the author manifest, not by themselves independent provenance of each download.

Both author verification commands pass. Running verify.py reproduces CHECKS.json **byte for byte**, including all 1,718 assertions and the floating-point error figures. The code uses exact rational arithmetic for its algebraic controls and explicitly labels its floating-point diagnostics. Neither program tests an infinite conformal end. The artifact accurately disclaims formal proof verification and numerical certification of end type.

A separate read-only replay script and its output accompany this report. It rechecks the frozen hashes, inventory, source-file consistency, selected-record tolerance correction, and unsolved/5-of-5 disposition. The mathematical audit remains the prose assessment here, not an inference from assertion counts.

## 1. Target and quantifiers

The functional tolerance is correct. The primary statement asks for a positive continuous function on (0,infinity) and imposes the inequality at every positive x. This is verified in [Hayman and Lingham, Problem 6.63, printed pages 140-141](https://arxiv.org/pdf/1809.07200v2), whose two relevant pages were visually inspected. The following update says that the editors had received no progress report. The date-limited update does not establish the present global literature status.

The selected recovered problem record agrees with that statement. The separately recovered prior research report abbreviates the question using a scalar epsilon. The package correctly identifies and rejects that abbreviation. A scalar uniform tolerance, compact-open approximation, C1 control, or a fixed quasiconformal distortion bound cannot silently replace the original quantifier.

The distinction between a hyperbolic annular end and generic hyperbolicity of an entire Riemann surface is also preserved. The use of finite versus infinite annular modulus is appropriate after selecting an ordinary compact inner collar.

The original unrestricted welding class does not automatically provide differentiability, uniqueness, local quasisymmetry, or removable seams. These hypotheses are asserted only for restricted results that need them. In the singular route the package specifically does not infer an admissible, globally coherent sewing from the construction of a boundary homeomorphism alone.

## 2. Theorem 1: affine classification

**Accepted.** Both branches give actual end uniformizations, rather than a numerical type guess.

For a=1, division by b+i and exponentiation identifies exactly integer translates by b+i. Two interior strip points cannot differ by a nonzero such translate because their imaginary coordinates differ by less than one. The computed logarithmic radius has the correct sign. Choosing a representative with imaginary part in [0,1) shows that all sufficiently large radii are attained and that their representatives lie in the half-strip. The resulting end is a puncture after inversion, including the b=0 case.

For a different from one, translation by c=(b+i)/(a-1) changes the sewing to multiplication by a. The stated shifted boundary heights are correct. For a>1, a small positive-angle ray crosses the two boundaries over a radial ratio a. For a<1, both heights are negative, the angle is negative, and the radial ratio is 1/a. In both cases the absolute logarithmic radial width is one period. Equal values of the exponential can only come from that radial periodicity; in the interior of a fundamental segment there is no duplication. The angle-to-radius conversion is monotone and tends to radius one at the end. Thus a nondegenerate finite annulus is obtained in both dilation cases.

The role of b is only a finite real displacement of the cutoff. The claim of openness is deliberately confined to the affine parameter family. It does not answer the ambient fine-topology question.

## 3. Theorem 2 and Lemma 2A: quasiconformal transport

**Accepted with the stated regularity restrictions.**

The map h=beta composed with alpha inverse is defined on the whole positive half-line under the theorem's zero-endpoint assumptions. Each horizontal interpolation between x and h(x) is increasing, onto, and proper. The identity h(alpha(x))=beta(x) is exactly the seam compatibility needed for descent. The map sends the distinguished infinite end to the corresponding infinite end.

The derivative matrix, positive Jacobian bound, and Frobenius-norm bound are correct. In two real dimensions the singular-value ratio is the square of the largest singular value divided by the determinant, so the displayed K0 is a valid, possibly non-sharp global upper bound.

The seam argument must not be used for arbitrary Jordan arcs. Here local bi-Lipschitz boundary identifications do furnish the standard locally quasiconformal sewing charts and local quasiarcs. Straightening and ACL gluing establishes local quasiconformality of the descended map. Such seams have area zero. Conformal changes of coordinate preserve interior dilatation, so after extension across the seams the original almost-everywhere K0 bound remains valid. There is no unjustified multiplication of infinitely many local constants in this argument. The resulting finite quasiconformal bound preserves finiteness versus infinitude of annular modulus.

For Lemma 2A, the intervals are disjoint and locally finite, and their lengths can satisfy the positive minimum of epsilon on each relevant compact interval, no matter how rapidly epsilon decays. The two slopes s_n and 2-s_n match the two endpoints. Their positive lower bounds are only local, which is enough for a locally bi-Lipschitz admissible sewing but not for uniform quasisymmetry. The equal-adjacent-interval ratio diverges. On positive-area regions near the upper edge the interpolation has p at most 2s_n and a largest singular value at least one, giving the claimed unbounded distortion.

Crucially, this proves failure of a particular uniform-distortion route, not a change of end type and not failure of every possible comparison method. The text observes that limitation.

## 4. Theorem 3: invariant form and finite energy

**Accepted.** This is a restricted, correctly attributed version of the classical method.

The orbit intervals exhaust the tail: in the expanding case their successive gaps grow at least geometrically; in the stated generalization escape is assumed expressly. Transporting q0 by inverse derivative gives mass one on each interval, local smoothness at the orbit endpoints, and q(f(x))f'(x)=q(x). Hence theta(f(x))-theta(x) is constant and equals one.

The circle-valued theta therefore descends. Its degree on the finite boundary core is one, since its variation along the unmatched upper segment is one and its variation along the vertical segment is zero. A nearby interior core has the same degree. This is the topological step needed for the nonzero period; positivity of q alone would not supply it.

The local seam potentials have matching traces. The real-analytic case supplies regular conformal charts directly: near a paired point, use the original coordinate on one side and the holomorphic local inverse of f(z)+i on the other. The more general assertion separately assumes C1 chart and inverse extensions with nonzero derivative. This is a genuine restriction and is not inferred merely from the smoothness of a boundary homeomorphism.

With those charts the glued potentials are locally Lipschitz, and a standard admissible representative of their differential norm gives length at least one on every separating core. For complete pointwise clarity one may use the continuous piecewise-C1 representative described in the optional clarification below, or assign an infinite density on the area-zero seam. The energy remains the strip-interior integral. The orbitwise substitution and Tonelli calculation produce exactly the stated sum of reciprocal iterate derivatives. Under uniform expansion it is bounded by a convergent geometric series. Since E is positive and finite, the essential-loop extremal length is at least 1/E, equivalently the annular modulus is at most E.

The polynomial affine density calibration integrates to one, its square integrates to 6/(5 L0), and the stated energy bound follows. It is correctly called an upper bound, not the exact modulus.

The hypotheses on [Jenkins's theorem, pages 427-430](https://doi.org/10.4153/CJM-1959-043-7) were independently read; page 430 was visually checked. The original theorem explicitly assumes the relevant chart and inverse boundary regularity and gives the derivative-product sufficient criterion. The package neither conceals these hypotheses nor claims Jenkins supplies arbitrary value-only stability.

## 5. Theorem 4: parabolic tail surgery

**Accepted.** The two affine pieces agree at R, have positive slopes, and give a locally bi-Lipschitz sewing onto the required endpoint interval. Its far tail is exactly a translation. Deleting the compact kink region does not change the infinite end, so Theorem 1 supplies parabolicity.

Agreement on every prescribed compact interval eventually becomes exact. However, the tail error equals (a-1)(x-R), which grows without bound. The constant positive tolerance one rejects every member. The package correctly concludes only failure of compact-open stability and of finite-window type tests; it explicitly does not claim a counterexample to the actual question or even to uniform-norm stability.

## 6. Lemmas 5A-5C: compactification and capacity

**Accepted as reduction, approximation, and obstruction statements.** No full counterexample results.

The map exp(-2 pi z) sends the two half-strips to the two half-disks with the signs stated. The artificial middle cut is the negative real radius and retains the identity identification. The positive-side map and its two-sided germ are correct. A nonzero alpha(0) changes the finite neighborhood size, not the germ at zero.

Taking logarithms proves the exact equivalence between the original additive tube and the variable multiplicative tube for tau. This conversion is especially important when epsilon becomes small rapidly. Replacing it by an arbitrary fixed additive neighborhood at zero would be invalid.

In Lemma 5B, delta is positive and continuous on each compact subinterval of (0,1). A compact exhaustion and finite refinements supply a locally finite partition whose image oscillations are smaller than the required local delta. Every increasing map with the specified endpoint values then stays inside the tube. Endpoint limits follow from the partition values and monotonicity. The local log-singular maps can be joined while including the countable endpoints in the exceptional set. Countable unions of logarithmic-capacity-zero Borel sets remain capacity zero, giving the positive-side log-singularity asserted.

[Bishop, Remark 9 on page 620](https://annals.math.princeton.edu/2007/166-3/p01) explicitly provides the interval construction used here. That page, and Theorem 25 on page 640, were visually inspected. The author correctly treats this construction as an external published theorem dependency.

The fixed negative side prevents the resulting whole germ from being log-singular: if E is capacity zero, removing it from any nondegenerate compact negative interval leaves a set of positive capacity. Its image is itself. Therefore the image of the complement cannot have capacity zero. This argument needs only the zero-capacity ideal property, not an unjustified numerical capacity subtraction formula.

Bishop's global log-singular circle theorem therefore has an unmet hypothesis in this application. The package does not infer global welding through zero from local existence, and does not infer parabolicity from singularity alone. This is the correct stopping point for this route.

## 7. Source-direction and literature checks

[Huber's 1986 paper](https://www.math.purdue.edu/~eremenko/Pdf/huber1.pdf) was read on all three pages, with the concluding page also rendered for inspection. Its fine approximation theorem produces a hyperbolic singular end while the other side is held fixed under its regularity hypothesis. The earlier two-sided approximation assertion leading to admissibility through the singular point is explicitly left open in that paper. The package describes this direction correctly. Density of hyperbolic examples does not logically imply hyperbolic openness or fine parabolic approximation.

[Vainio 1989](https://www.acadsci.fi/mathematica/Vol14/vol14pp161-167.pdf) explicitly sets local quasisymmetry off zero as a uniqueness/existence framework and develops more regular type criteria. [Vainio 1995](https://www.acadsci.fi/mathematica/Vol20/vainio.pdf) separately addresses continuation with uniqueness assumptions and a restricted derivative-based hyperbolicity theorem. Those caveats are important and are retained. The selected source passages do not provide the original unrestricted stability theorem.

The official indexed [Preciso dissertation abstract](https://www.research.unipd.it/handle/11577/3425905) corroborates the Schauder/Roumieu perturbation setting. The package appropriately claims abstract-level inspection only. The 1977 [Anderson-Barth-Brannan listing](https://doi.org/10.1112/blms/9.2.129) is corroborated by an indexed scholarly full-text copy containing Problem 6.63; no stronger full-article inspection claim is made. Direct DOI and dissertation-page fetches were unavailable to the auditor, while indexed evidence was accessible.

These are checks of the cited dependencies and their applicability. They are not a new unrestricted research attempt or an exhaustive search of later literature. The original package's cautious claim that its targeted searches found no exact resolution is the strongest justified formulation. Its 2018 source update must not be turned into a proof that the problem remains globally open in 2026.

## 8. Corrections and optional clarifications

### Mandatory corrections

None identified. No corrected replacement of a frozen public file is supplied or required by this audit.

### Optional non-blocking clarification: metric values on seams

In Theorem 3 the statement about all rectifiable loops can be made completely explicit by specifying the metric representative on the seam. Under the stated C1 chart assumptions, the two gradient traces agree: the tangential derivatives agree by theta(f(x))=theta(x)+1, and both normal derivatives vanish because theta in each strip coordinate depends only on x. Thus the potentials have a C1-compatible differential at the seam. Alternatively, setting the density to infinity on the area-zero seam leaves the energy unchanged and provides a standard admissible representative. This is an expositional strengthening, not a new hypothesis or a failure of the restricted theorem.

### Optional non-blocking clarification: sequence indexing

Lemma 2A may explicitly say n=1,2,... when defining t_n=3n. The proof and verifier already use this indexing. Starting at n=0 would put a window at the excluded endpoint, so making the convention explicit avoids a purely notational distraction.

## 9. Publication boundary

The separate publication gate must still recheck the live base head and duplicates before any repository write. This audit does not certify current remote state. The recorded recovered-problems corpus mismatch is disclosed and must remain disclosed; the primary target was independently checked despite that mismatch. The historical research-results hash and earlier repository-read summaries are provenance records, not a substitute for the publication-time check.

Keep the original disposition unsolved, 5/5. Do not promote the restricted results, the 1,718 finite assertions, or this audit to a general solution, a novelty claim, or proof-assistant verification. Retain all regularity and admissibility restrictions. Do not distribute downloaded PDFs, source page images, raw corpus or raw connector/coordination records. No mandatory new public artifact is imposed by this audit; its safe prose and check metadata may accompany a release if the parent publication gate chooses.
