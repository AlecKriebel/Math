# Independent complete-package review 01

Reviewer: independent automated adversarial reviewer `/root/complete_review_01`.
Review completed 2026-10-06 PDT / 2026-10-07 UTC. Assignment completion estimate: 100%; this is an accounting estimate, not a confidence probability or publication receipt. No external individual was contacted. Upstream and candidate sources were read only. This reviewer made no Git, upload, publication, or tracker operation.

## Verdict and exact scope

**No substantive mathematical or package blocker was found in the exact candidate below.** The claimed smooth theorem for every ambient `n>=2`, `0<=p<1`, and positive even smooth density, and the arbitrary full-dimensional origin-symmetric equal-measure theorem for `0<p<1`, follow from the inspected analytic logarithmic Brunn--Minkowski proof and the established existence/regularity inputs. The nonsmooth `p=0` uniqueness assertion is explicitly excluded and falsified by the correct box calculation.

This is a favorable automated complete-package review of a consequence note, not human peer review, an exhaustive novelty certificate, a reproduced Lean certificate, or evidence of publication. It does not certify unrelated upstream measure/B-conjecture applications. Adding final reviews/response records and updating package status must be followed by a final inventory/reproduction pass on those additions; this report does not pretend to hash itself or a later archive containing itself.

Exact reviewed uploads:

| File | Bytes | SHA-256 |
|---|---:|---|
| `publication/upload-kit/paper.pdf` | 79067 | `18622046e8c5b52559520b8b08c43ee35a3ebcead202038990e9dcda49473fbc` |
| `publication/upload-kit/source-and-verification.zip` | 89248 | `9e5ecfa16b50b9838d1b20650af2015f6f71a57f5f877497dae99a7cbbcdb7cc` |
| `publication/upload-kit/README.md` | 6229 | `386d94cd217b609a1509bc6b3015bc583e3c7470d86a999fa6cbb5dcc930dac6` |

`main.tex` SHA-256: `d7e44a54c1e55f423e147edcaf70ec82d8c8142f58390f8b487d6f1790a4173e`.
`zenodo-deposit.json` SHA-256: `e07287fadc017b6fd4f0a3db4853dadfbafa978fa23eb1e2934e3af77fd0ec91`.
Upstream pin: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

The initial inspected ZIP was `4318eb97016e8bb9787b1afd25350de9c6687a01f4821f6896fa1cf1e4f34c38`. A minor reconstruction-documentation observation was fixed. Independent comparison confirmed that only `verification/REPRODUCIBILITY.md` and its enclosing `PACKAGE_CONTENTS.json` changed to produce the latest ZIP. The paper, proofs, metadata, programs and other evidence remained byte-identical.

## Actual inspection and independent mathematical checks

I began with `main.tex`, then read the actual upstream `introduction.tex`, `reduction.tex`, `moment.tex`, `identities.tex`, `density.tex`, `tensor.tex`, and `variance.tex`, plus the positive-p volume corollary. I subsequently read all analytic/priority/formal-scope reports, dependency ledger, exact current theorem statements, root validation, research log, approach table, code, inventories and intended metadata. Favorable report verdicts were not used in place of checking the argument.

### Upstream analytic input

The upstream introduction, lines 21--29, has precisely the symmetric full-dimensional all-body Wulff inequality needed by `main.tex:39--45`. The reduction at `reduction.tex:44--119` is valid: differentiating the Gaussian-regularized partition integral gives variance minus expected second potential derivative; the signs and coefficients agree with geometric widths. Gaussian domination justifies the even-power limit. Spanning slab normals provide bounded full-dimensional outer approximations, and continuity of measure from above supplies every direction. Dimension one is separately treated; there is no smoothness or unconditionality restriction hidden in this reduction.

I checked the compact-target assumptions and exact statements of Berman--Berndtsson Theorem 1.1, Klartag Proposition 3.1/Remark 3.5, Wang's journal Corollary 2.3, and the interior Schauder statements in the saved primary texts. The first supplies the ball-target moment potential for centered positive smooth weight; the second supplies the radius-independent `4/epsilon` upper Hessian cap. Wang's corollary is explicitly a real `Sym(n)` uniformly elliptic estimate, despite the surrounding paper's complex-geometry title. The smooth truncated potentials meet the Schauder a priori regularity class. The distributional elliptic step was checked against [Dyatlov's primary notes, Theorem 14.2](https://math.mit.edu/~dyatlov/18.155/155-notes.pdf).

At `moment.tex:78--104`, the supporting-plane/expectation argument gives uniform linear coercivity and normalization bounds without assuming a global lower Hessian bound. Determinant positivity plus the upper cap gives local ellipticity at lines 106--136. Smooth subsequential convergence, common-tail dominated convergence, and the finite supporting-plane tilted coercivity argument at lines 156--185 give an actual global gradient diffeomorphism, rather than only dense image.

For density, I independently checked the fourth-order local ellipticity, product-rule coefficients `4,-12,-8`, the estimates controlling `Ag` in `L2`, and the cutoff/graph-norm argument showing the only obstructions are affine (`density.tex:35--150`). No unsupported spectral-gap assumption is introduced. For the tensor step I checked the adjoint signs, the gradient identity making `D_z W` symmetric, the vector Bochner **matrix-square** trace, the twice-differentiated moment equation, and constant dual-coordinate normalization. At `tensor.tex:159--211`, the contracted remainder is exactly

    2||S+Sym J||² + (1/6)||J-J^(12)||².

The full symmetrization formula uses last-two-index symmetry, so its coefficients give the displayed identity in every dimension and for indefinite test Hessians. The two Cauchy--Schwarz bounds and `m_i=q E psi_i` in `variance.tex:21--89` supply the required variance inequality, including positive denominators and legitimate polynomial cutoff limits. The exact finite programs support this algebra, but the argument above is not inferred from finite cases.

### Follow-on deductions and boundary cases

`main.tex:74--88`: the nonsmooth Wulff variation is sound. Boundary contact plus the almost-everywhere unique normal gives `h_W=a` with respect to `S_W`. Applying classical Minkowski first inequality in both orders produces the displayed root-volume sandwich. Uniform difference quotients and weak surface-area convergence identify both limits, with reversed bounds for negative parameter. No assumption that a geometric mean is a support function is inserted.

`main.tex:106--123`: strict Jensen gives support ratio constancy only `S_K`-almost everywhere. Equality in both intermediate bounds fixes that ratio to `(V(L)/V(K))^(1/n)`. This is exactly enough to make classical mixed volume attain equality, recovering homothetic translates. Origin symmetry eliminates the translation. Equal prescribed measures give `Vp(K,L)=V(L)` and the reverse identity, and `n-p>0` forces equal volume and scale. Atomic surface-area measures are permitted throughout.

`main.tex:127--159`: each smooth endpoint candidate is a global minimizer of the scale-invariant functional because its normalized cone-volume density is `f/M`. Equal endpoint volumes and energies make the logarithmic integral along the local geometric-support path constant. Positive curvature is open on the compact sphere; only this local path is needed. Log-BM and global minimality force constant path volume. Arbitrary even smooth perturbations yield the pointwise PDE with multiplier exactly one. I independently differentiated it: with tangent dimension `m=n-1`,

    Q(hw²)=2wQ(hw)-w²Q+2h dw⊗dw,
    tr(Q^(-1)Q(hw))=-w,
    0=-tr((Q^(-1)Q(hw))²)-(m+2)w²+2h Q^(-1)(dw,dw).

Thus `n+1` is the correct coefficient. Similarity to a real symmetric matrix makes the trace-square nonnegative. At both extrema the gradient vanishes, forcing both extrema to zero. This works for `n=2`. Right differentiation is legitimate because the explicit smooth path extends across zero. He--Liu's actual Theorem 4 and Section 3 were read; the local account correctly avoids its global-path regularity step and dimensional/algebra slips. Their transfer is credited.

`main.tex:163--167`: BBCY Theorem 1.7 and Proposition 7.3 preserve `G={I,-I}` and provide full-dimensional existence. Symmetry makes the origin interior, eliminating zero support. CW Proposition 1.2, its positive-support strict-convexity input, and BBC Theorem 1.1(i),(iv) then give the stated regularity. The positive determinant upgrades the smooth semidefinite curvature matrix to definite; smooth elliptic bootstrapping follows. The planar distributional equation gives the same result directly. Scaling is `c^(n-p)`, and unnormalized `p=0` data fix volume `M/n`. Each signed box facet has area `V/(2a_i)`, so the `L0` atom is `V/2` and the cone-volume atom is `V/(2n)`.

A supplemental independently tasked adversarial checker also read these deductions directly and rederived the endpoint coefficient; it found no counterexample or substantive gap. Its narrow check supplemented rather than replaced this complete review.

## Priority, formal scope, metadata and package

The consequence framing in `main.tex:23,45--47,170`, the README and deposit description matches the actual division of credit. I directly verified the earlier announcement in [Stancu's 2018 primary report, pp.3263--3264](https://ems.press/content/serial-article-files/46776): it announces smooth cone-volume uniqueness and the all-body logarithmic inequality while deferring flow asymptotics. I read He--Liu's primary theorem and proof. The audited literature search and its inaccessible Stancu2022 full-text limitation are explicitly recorded; neither a firstness claim nor a proof of exhaustive absence of duplication is made. The priority report's earlier abbreviated CW existence paragraph was corrected before the frozen candidate and now matches the explicit BBCY-to-CW chain.

I inspected the actual Lean definitions and final declaration at upstream lines 24468--24486, rather than the comparator's intentional `sorry`. The all-body statement matches the analytic theorem and contains no extra assumed analytic conclusion. Static scans and pinned source hashes agree. I did not rebuild the 24,490-line development or extract its imported axioms; all package locations accurately disclose this limitation. The excerpt retains the substantive formal limitations, and the derivation's basis is the manually checked analytic argument. No certification of the follow-on theorem by Lean is claimed.

I inspected the intended Zenodo metadata and three-file set. Title, Alec Kriebel/ORCID, date, CC BY 4.0 owned-contribution scope, theorem quantifiers, endpoint exclusion, source relation and AI/human-review disclosures agree with the actual paper and README. No reserved identifier is presented as an already published DOI. Production and tracker operations are still future state and are not certified by this review.

I inspected every ZIP entry and every actual uploaded file. The archive contains exactly 29 listed payloads plus `PACKAGE_CONTENTS.json`; paths are safe unique regular files with fixed timestamps. Every byte-size/SHA-256/MD5 entry matches both the external package inventory and the actual owned working file. No downloaded article, upstream source copy, Lean dependency, cache, binary preview, private key or credential token was found. Only third-party source identifiers/hashes and owned audit text/code are included. The public formal excerpt's provenance and scope are explicit.

Fresh extraction under `reviews/review_01_extract` passed internal hashes, 23 read-only upstream file hashes, 450 exact tensor cases, 200 endpoint cases, 7 box cases and 28 scaling cases, followed by a clean standalone Tectonic 0.16.9 PDF build. The latest archive was then freshly extracted under `reviews/review_01_extract_final`, all entry hashes were checked again, and the same reproduction/build was rerun. Receipts are `reviews/review_01_inventory_final.json` and `reviews/review_01_clean_results_final.json`. These are finite/reproduction checks, not proof or formal certification. The author-workspace builder `--check` also reproduced the initially frozen uploads byte for byte.

Using the PDF skill for read-only review, I rendered and visually inspected **all five pages of the exact uploaded PDF**. Equations, proof transitions, bibliography, title, author, ORCID, date, margins and page numbers are legible without clipping/overlap or missing glyphs. Poppler metadata gives the matching title/author, five letter-size pages, no encryption, forms or JavaScript; all 22 fonts are embedded. No layout repair is required. Rebuilt PDF bytes can differ through creation timestamps, which is correctly disclosed.

## Observations and remaining limits

1. **Resolved minor documentation observation:** the archived builder alone cannot reconstruct the complete upload kit because the original formal report and separately exported PDF are intentionally omitted, and the external package inventory is separate. The latest `verification/REPRODUCIBILITY.md` now explicitly distinguishes full-author-workspace archive reconstruction from extracted-archive tests/PDF compilation/upstream checks. I verified the revised text in the exact latest ZIP.
2. **Nonblocking wording observation, `main.tex:165`:** positive bounded Monge--Ampère density alone does not force local strict convexity for arbitrary local convex functions. Here the sentence is supported by the global convex-body/interior-origin structure and the expressly cited BBC Theorem 1.1(i),(iv), so there is no missing assumption in the theorem. A future revision may state that body-level dependency more directly.
3. **Recorded limitations, not unresolved defects in this consequence note:** Lean kernel/axiom/Comparator reproduction remains incomplete; the later Stancu article's full text was inaccessible; no human peer review or exhaustive novelty certification has occurred. The candidate does not claim any of these. Later final-package additions and actual production/DOI/tracker state require their own verification.

No substantive unresolved concern remains within this reviewed mathematical and exact-candidate package scope.
