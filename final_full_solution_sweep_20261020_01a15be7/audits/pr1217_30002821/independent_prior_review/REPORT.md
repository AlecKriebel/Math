# Independent adversarial existing-publication review: PR1217

Verdict: **PASS for the exact target as a credited existing result.** No substantive mathematical gap or theorem-changing repair was identified in Alper Ferudun's version 1.1 or the pinned eight-file reconstruction. Record the existing version DOI; do not create another publication. This is an internal AI-assisted review, not external human peer review or formal verification.

Audit completed 22 October 2026 UTC. This audit family is 100% complete once the accompanying seal is written; the parent sweep's overall completion estimate remains 79%. Nothing in this report claims worldwide first priority or independent discovery by this project.

## Exact target and authentication

The original question is Jim Propp and Richard Kenyon's Problem 7, collected by Günter Rote in Oberwolfach Report 13/2015, printed page 722, PDF page 62, DOI `10.4171/OWR/2015/13`. The complete relevant page was freshly fetched, read, rendered, and visually inspected. It explicitly places the two unit-disk centers at `(±1,1)` and asks for maximum total area of infinitely many nonoverlapping disks touching the x-axis in their bounded curved triangle. All 70 report pages were fetched, but only page 62 is certified as read and visually inspected here.

The accepted existing result is **Alper Ferudun, The Ford-Circle Packing Has Maximum Area: An Answer to a Question of Propp and Kenyon, version 1.1, 30 September 2026**, version DOI `10.5281/zenodo.23049959`. The entire twelve-page manuscript was freshly read in text and visually inspected. The fresh original-report PDF has 4,345,044 bytes and SHA-256 `e3ba6ef5fc327cfe1ca2c3c52a30d8107fbe487f832ae799f6ccd3e8e3da25ca`. The current proof PDF has 150,937 bytes and SHA-256 `85af3e938d3e1be3fff87541f231f02bdb16e1c1f18e062d6aa0ca65fafec9bc`, exactly matching the candidate pin. Public API and DataCite metadata were also freshly read. A web-preview failure was bypassed with successful read-only public API requests; the final DOI resolved with HTTP 200 to the intended Zenodo record.

All eight changed candidate blobs were independently materialized with `git show` from head `31b93de3925e425bbd65506b86911352e40ef0d8`, relative to base `4b27092a448d53b61408355ce44ec38d103a1ce4`. Each was read completely. `PINNED_BINDINGS.json` records Git blob IDs, byte lengths, and SHA-256 values. The live draft PR body identifies the same head/base and pins all eight correct byte lengths and hashes. The manifest validates its seven non-self entries. The actual comparison has eight paths and no QUEUE path. The pinned `PROOF.md` is 26,239 bytes, SHA-256 `812823624ded0d1b8fafde07b89732d3b4f473e0ae95eab8c52c8f1adad8e533`.

Success here means a universal upper bound for every admissible countable packing, together with a complete admissible greedy family attaining that bound. The boundary disks are excluded from the objective. Boundary tangencies are allowed. No uniqueness, arbitrary-weight, non-line-tangent, or nontangent-boundary claim is certified.

## Independent mathematical reconstruction and attempts to falsify it

### Geometry, countability, and the actual greedy family

Write a disk as `(x,s)`, with center `(x,s²)` and radius `s²`. Subtracting the squared radii in the center-distance condition gives exactly `|x-y| >= 2st`. With tangent boundaries of positive sizes `a,b` separated by `2ab`, an internal disk satisfies `x-x_A >= 2as` and `x_B-x >= 2bs`, so `s <= ab/(a+b)`; equality fixes its base point and gives the unique greedy insertion. These are necessary and sufficient interior-disjointness conditions, not just necessary radius estimates.

For the unit gap, the lower arcs have height `β(u)=1-sqrt(1-(1-|u|)²)`. The bounded open region `|u|<1, 0<v<β(u)` is a connected component of the open upper half-plane with the two closed boundary disks removed: its relative boundary lies on those disks and `β` tends to zero at the two base endpoints. An algebraic gap disk has connected interior in that complement and contains a point `(x,ε)` of this component. Thus it stays in the intended bounded region. This excludes the possible relaxation to an unbounded component above the boundary disks.

Every positive-radius disk interior contains a rational point; disjoint interiors admit an injective assignment of such points. Therefore every admissible family is at most countable without a local-finiteness assumption. Countable boundaries have total area zero, so the sum of disk areas agrees with the area of the union.

For a positive primitive pair `(m,n)`, define `s=(m/a+n/b)^(-1)` and `x=x_A+2ans`. Direct cancellation gives

`x_(m',n')-x_(m,n) = 2(mn'-m'n) s_(m,n) s_(m',n')`.

Distinct primitive positive pairs cannot be proportional, so their determinant is a nonzero integer and the disks really have disjoint interiors. The endpoint pairs `(1,0),(0,1)` give the boundary disks and put every positive-pair base point strictly inside the base interval. Determinant-one mediants give exactly the local greedy insertion. Conversely, the subtractive Euclidean algorithm for positive coordinates in a unimodular cone reaches `(1,1)`, proving every primitive pair is generated, with uniqueness from the disjoint child cones. This is a genuine packing and a complete family, not merely a collection with the desired radius distribution.

In the unit case put `q=m+n`, `p=n`. The disks have radius `1/q²` and base point `2p/q-1` for every reduced `0<p<q`. Completeness is material: a succession that forever ignores a recursive gap is not the complete maximizing family. The original question's usual full recursive interpretation is the one certified.

### Arithmetic and all-degree analytic step

Set `w(0)=0`, `w(s)=1/(exp(1/s)-1)` for `s>0`. It is continuous at zero and strictly increasing. Its positive exponential expansion and the unique gcd decomposition `(M,N)=d(m,n)` give exactly

`Σ_G w(s_D) = Σ_(M,N>=1) exp(-M/a-N/b) = w(a)w(b)`.

For `G_p=Σ_primitive(m/a+n/b)^(-p)`, comparison with the unit case gives convergence precisely when `p>2`. An elementary independent proof of divergence at `p=2` uses the divergent unrestricted double sum `Σ_(q>=2)(q-1)/q²=ζ(2)G_2` in the extended nonnegative sense. For smaller positive `p`, comparison suffices; for nonpositive `p`, infinitely many sizes tending to zero give divergence. The divisor identity `Σ_(d|n)φ(d)=n`, applied in absolutely convergent series for `p>2`, gives `G_p(1,1)=ζ(p-1)/ζ(p)-1`. In particular the asserted area is exactly `π(ζ(3)/ζ(4)-1)`.

The universal analytic obligation is log-convexity of `1+w(exp(λ)-ρ)+w(ρ)` on `λ>log ρ` for every `ρ>0`. Direct differentiation, independently checked as a rational-function identity, reduces its log-curvature to a strictly positive factor times `Ω(q,x)`, with `q=1/s`, `x=1/ρ`. The source's four exponential polynomials `U1,...,U4` give

`Ω=x(exp(x)-1)U1+(exp(x)-1)U2+xU3+U4`.

This identity alone would not establish positivity, since `U2` has a negative low-degree coefficient. Combining by x-degree is essential. In the expansion `Σ ω_n(q)x^n/n!`, `ω_0=U4`, `ω_1=U2+U3`, and `ω_n=nU1+U2` for `n>=2`. For every degree `m>=2`, the normalized coefficients of `U1,U2,U3` are respectively

`(m-2)2^(m-1)+1`, `m((m-5)2^(m-2)+2)`, `(m-2)2^(m-1)+2`.

`U4` has zero degree-two coefficient and normalized coefficient `m((m-5)2^(m-2)+4)` for `m>=3`; all four have zero coefficients in degrees zero and one. Thus `ω_0` vanishes through degree four and is positive from degree five; `ω_1` has normalized coefficient `(m+1)((m-4)2^(m-2)+2)`, zero at degrees two and three and positive thereafter. For `n>=2`, use nonnegativity of `U1` and reduce to `n=2`: the coefficient is `2^(m-2)(m²-m-8)+2(m+1)`, zero at `m=2`, equal to four at `m=3`, positive for all `m>=4`. These formulas cover every integer degree analytically. Because the expressions are entire, the series converge at all positive arguments, and `Ω(q,x)>=q^5/6>0`. No finite grid is promoted into the universal proof.

The independent checker differentiates using its own sparse rational-function algebra in `(q,x,E,X)`, with `dE/dq=E`; it derives the derivative and `Ψ/Ω` identities before checking the coefficient forms against the direct exponential-polynomial expansion. This is supplementary verification of the written all-degree proof.

### Chain induction, degeneracies, and deformation endpoints

For a k-chain, cumulative consecutive tangencies give `Σ_(l=0)^k s_l s_(l+1)=ab`, and every nonconsecutive pair except the fixed endpoint pair satisfies `Σ_(l=i)^(j-1)s_l s_(l+1)>=s_i s_j`. The chain value used algebraically is the sum of internal weights plus consecutive products. The proof does not require assuming that arbitrary independently filled subgaps already constitute a globally feasible packing.

Induct on `k`, for all positive boundary sizes simultaneously. At `k=1`, the Farey identity `w(c)(1+w(a)+w(b))=w(a)w(b)` gives equality. An extra contact `(i,j)` splits a chain into an inner chain with `j-i-1` and an outer chain with `k-j+i+1` internal disks. Both parameters lie in `[1,k-1]` precisely because the fixed endpoint pair was excluded. The exact accounting subtracts the new product `w(s_i)w(s_j)` once. Positions do not change, so the split chains inherit every required geometric inequality. There is no unsupported induction with zero or unchanged parameter.

For a nondegenerate chain with `k>=2`, keep indices `0,3,...` fixed, preserve `L=s0*s1+s1*s2+s2*s3`, put `K=L+s0*s3`, and vary

`s1=exp(θ)-s3`, `s2=K exp(-θ)-s0`.

Both sizes are positive precisely on `I=(log s3,log(K/s0))`; all constraints with endpoints avoiding indices 1 and 2 stay constant. The feasible set is relatively closed. At the left parameter boundary, constraint `(0,2)` tends to `-s0*L/s3<0`; at the right boundary, `(1,3)` tends to `-s3*L/s0<0`. Both constraints are present even for `k=2`. Consequently the feasible set is compact away from both boundaries. The original point has a feasible neighborhood because there are finitely many strict inequalities. Its connected component is a nontrivial closed interval. Each endpoint has an additional contact, or continuity would extend that component. This argument uses only the one component; it does not assume the full feasible set is connected or convex.

The varying objective equals

`(1+w(s1)+w(s3))(1+w(s2)+w(s0))-(1+w(s0))(1+w(s3))`

plus an unchanged constant. The two positive factors are log-convex under affine parameter changes, so their product is convex. Keeping the subtracted constant is necessary. The objective at the original point is bounded by one of the two degenerate endpoint values. This completes the chain induction independently of the packing-cardinality induction.

As an exact k=2 control, take the unit gap and `y=exp(θ)`. Then `s1=y-1`, `s2=2/y-1`, and the two nonconsecutive slacks are `3-4/y` and `3-2y`. The feasible interval is exactly `[4/3,3/2]`, with positive-size degenerate endpoints. This catches an incorrect loss of constraints at the lowest nontrivial chain length.

### Finite optimization and the infinite limit

For at most `n` disks, allow labelled zero-size entries in the compact box `[x_A,x_B]×[0,ab/(a+b)]`, retaining the closed boundary and pair inequalities. The objective is continuous and zero entries contribute zero; padding at `x_A` proves this compact maximum equals the desired finite supremum. Any positive entries have distinct base points and form an actual admissible packing.

In a maximizing configuration, suppose a disk has no tangent disk to its right, counting boundary B. The finitely many rightward slacks have a positive minimum η. If S is the largest size among all disks and both boundaries, shifting right by `δ<η/2` and increasing size by `δ/(2S)` preserves all leftward inequalities because separation increases by δ while the required separation increases by at most δ. Rightward slacks remain at least `η-2δ>0`. The new weight increases, a contradiction. Reflection gives the corresponding left contact. Crucially, neither argument assumes the contact is with the immediately adjacent base point.

Following a left contact strictly decreases base points and must end at A; following right contacts ends at B. The two paths form a positive-length tangent chain selected from the finite packing. Every residual disk's base point lies in exactly one consecutive chain interval, where it is an admissible disk of that tangent gap. There are at most `n-k<n` residual disks. Cardinality induction, simultaneous over all positive boundary sizes, bounds their weights by the products in the chain value. The already independently proved chain inequality completes this second induction. Thus no circular assumption of global optimality is used.

For any infinite packing, take finite subfamilies and use the definition of a nonnegative series as the supremum of finite subsums. No saturatedness, rational-base-point assumption, infinite compactness theorem, optimizer for countably many disks, or unproved exchange of conditional series is required.

Finally scale the whole geometry by `1/t²`; sizes scale by `1/t`. Integrating the resulting weight inequality against `t^(p-1)dt` gives the positive finite factor `Γ(p)ζ(p)` and the upper bound `G_p(a,b)` when `p>2`. The one-weight integral exists already for `p>1`, but the product integral at `t=0` behaves as `ab*t^(p-3)` and requires `p>2`, consistent with the exact series threshold. Taking `p=2α` proves every radius power `α>1`; taking `p=4` proves area. The complete greedy packing attains the value, so this is a maximum rather than merely a supremum estimate.

For a positive Borel measure μ on `(0,∞)`, countable sums of nonnegative measurable functions commute with integration by monotone convergence, which requires no σ-finiteness assumption. Thus the source's scale-superposition corollary is valid as an extended-value statement. More strongly, since every kernel is everywhere positive, finiteness of even one such weighted integral would force μ to be σ-finite by its positive level sets; a genuinely nonsigma-finite measure makes the nonempty-packing comparison trivially infinite. The reconstruction's MCT explanation supplies a valid justification of the source's loose use of the word Tonelli, with no change to its theorem.

The four equal-size disks at base points `-1/3,-1/9,1/9,1/3` provide an exact counterexample to arbitrary nondecreasing weights, while the complete greedy family has only three disks of size at least `1/3`. The source and candidate explicitly exclude that extension. Strict local curvature also does not imply uniqueness of an arbitrary infinite maximizer, and no such conclusion is used.

## Existing-publication family and support package

The fresh Zenodo versions list has exactly the observed releases v1.0, record/DOI `23049225`, and v1.1, record/DOI `23049959`. Concept DOI `10.5281/zenodo.23049224` resolves through the API to current v1.1; the current record's latest endpoint also returns v1.1. DataCite independently gives the same author, title, version and `IsVersionOf` relation; its concept record lists both version DOIs. The v1.1 DOI registration is `2026-09-30T01:46:06Z`, and the concept registration is `2026-09-30T00:25:28Z`. These establish existing recorded publication, not the time of first discovery or every possible historical public disclosure. No exhaustive prior-literature claim was adopted or attempted.

All three v1.1 payloads were freshly downloaded and matched the API's sizes and MD5 digests; their SHA-256 values are:

- PDF: `85af3e938d3e1be3fff87541f231f02bdb16e1c1f18e062d6aa0ca65fafec9bc` (150,937 bytes).
- Source ZIP: `8963b0bb9ffc342c3047ff0d14376023d99960c26556a077a42bab0f61d6ec19` (129,209 bytes).
- Verification report: `f1942bbfb327893f091fcdb05c5ab1d7655bc979535e712d00c3fc21b2f8bdab` (25,714 bytes).

The ZIP has 102 entries: nine directories and 93 files, 299,269 uncompressed bytes. Every file was read for SHA-256 and UTF-8 validation, and all CRCs pass. The archive report and standalone report are byte-identical. Its `main.tex`, bibliography, license, reproducibility README and verification report were inspected. All 45 Python source members were parsed statically, with imports, function names, assertions and I/O calls recorded in `SOURCE_STATIC_REVIEW.json`. Numerical warning/error records were read. This is a complete archive inventory and static support audit; it does not certify every program line or reproduce the author's stored executions. No author program was executed or imported.

The README openly records two early sampler exceptions, finite-difference sign noise at tiny curvature, and small optimizer excesses at constraint-tolerance violations. Those are not successful universal certificates. The manuscript says the written proof is independent of all computations. The independent 600-digit calculation also reconciles the most delicate README example: at the actual grid value `s=10^(-2.5),ρ=.001`, log-curvature is `7.96125670782684...e-133`; at rounded `s=.0032`, it is `3.21476344885055...e-131`. Exponential sensitivity explains the rounded prose. At `s=ρ=.001`, the positive value is about `2.02734e-428`, well below the resolution of the old finite differences. None of those noisy diagnostics refutes the exact all-degree proof.

The manuscript and public metadata explicitly disclose unrefereed status and AI-assisted research, computation, proof development and preparation. Its author verification narrative and claimed historical referee independence are not premises of acceptance, nor are they a claim of conventional human peer review.

## Independent checks, ledger decision, and boundaries

The independently written and source-read `independent_checker.py` passed **702,059 checks** in each of ordinary, `-O`, and `-OO` modes; the outputs are byte-identical. Coverage includes exact rational-function derivative/Ω identities, all coefficient positions `0<=m,n<=256` by direct exponential-polynomial expansion, 323 primitive disks plus both boundaries in each of six rational gaps, 52,650 pair comparisons per gap, split bookkeeping and parameter reduction through k=13, k=2 endpoint controls, the additive objective constant, the threshold-weight counterexample, and six 600-digit finite-difference checks from tiny to very large scales. Five deliberately false variants/predicates are rejected. These are bounded diagnostics, not the proof of the universal theorem or a proof-assistant certificate. The original 242,391 historical check count was not relied on or replayed.

Before any mathematical review, a fresh GWS CLI numeric `getByDataFilter` read selected sheetId `1254632077` in spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, all 43 columns, with no row limit. The allocated grid has 1,178 rows; 191 populated row records were returned. The raw reply is private, SHA-256 `26aadd1c217ebf0142460ae845b3d5be0467eef71b71665d9bfb204145961772`. Exact problem/PR identifiers and the version/concept/earlier-version DOI aliases yield no existing target row. A shared-source lead exists at row 81: the same EMS report URL, but explicitly Sanyal's Grassmann orbitopes on pp.708–709, catalogue `30002816/OWR-13498-004`, PR1031, DOI `10.5281/zenodo.23353160`. This is not Propp–Kenyon's Problem 7 on p.722. Another 27 broad semantic leads are unrelated rows, mainly other Ferudun citations and other circle/billiard questions; each is classified in the proposal. A shared author name, report URL, or different disk problem is not a target duplicate. A final fresh duplicate check remains necessary immediately before any future tracker mutation.

`TRACKER_PROPOSAL.json` contains exactly one four-cell A:D proposal with B genuinely empty, the version DOI in C, all source/problem/PR/family aliases, and explicit Ferudun attribution. It is a proposal only. This agent performed no spreadsheet write, upload, release, Git mutation, or external communication. The correct operational outcome is existing publication verified; pending parent-controlled recording, with no duplicate Zenodo upload.

All `PRIVATE_*` source/workbook data, PDF text/renderings, metadata responses and the local pinned source copies are evidence-only and not public package contents. Only authored report/checker/compact manifests may be considered for public distribution after the parent applies its release boundary. Raw source bytes are not authorized for automatic publication by their local presence.

One CLI incident is preserved separately: the shared GWS prerequisite file was missing in the installed skill path. `gws generate-skills --help` unexpectedly ran generation and rewrote the pre-existing root `skills/` tree and `docs/skills.md`. No pre-call bytes were captured, so no claim of byte changes or unchangedness is made. `GWS_GENERATION_OBSERVATION.json` records the 96 observed file paths, sizes, SHA-256 values and mtimes, the exact command, and the absence of restoration/deletion/staging. The parent was informed immediately; all subsequent audit outputs stayed in this folder. This local side effect did not make any service write or affect the mathematical source pins.

**Strongest verified result:** every admissible countable line-tangent packing in the original unit gap has area at most `π(ζ(3)/ζ(4)-1)`, attained by the complete primitive Ford family; the same proof covers tangent positive-radius boundary disks and radius powers `α>1`, plus the stated positive scale superpositions.

**Exact remaining mathematical gap:** none identified for that scope. Independent discovery, worldwide priority, uniqueness, conventional human peer review, and correctness of unrelated exploratory claims remain uncertified and are not required for recording the credited existing result.
