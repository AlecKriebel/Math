# Independent adversarial spectral review: PR1142 / problem30002112 / OWR-12005-004

## Outcome and exact scope

No spectral, multiplicity, indexing, scaling, asymptotic, or source-scope defect was found in the pinned current proof. The reviewed mechanism establishes the full negative additive estimate for each fixed integer m >= 2, conditional on the stated established hypersurface-existence and approximation theorems. Those theorem statements and their cited construction were checked against primary sources. This review does not establish historical novelty, external peer review, or a formal machine proof.

The strongest independently checked claim is this: if, for every positive integer q, a smooth compact connected embedded H_q inside B(0,1/2) has area q and first positive eigenvalue greater than T_q=q(q+m-1), then the connected smooth domains obtained by removing its bounded cavity from the unit ball satisfy

    F_q / D_q -> +infinity,
    F_q = lambda_{k_q}(boundary Omega_q) (q+rho_m)^(2/m),
    D_q = I(Omega_q)^(1+2/m) + k_q^(2/m),
    k_q = C(q+m-1,m) + C(q+m-2,m) + 2.

The pinned proof supplies that premise through its Lemma 2. I found no gap when checking its metric-comparison/smoothing steps against the primary theorem statements. No remaining spectral/counting/asymptotic gap was identified. The unreproved background dependencies are the established existence, Nash-Kuiper, smooth-approximation, and separation theorems; the finite computations do not replace these theorems. No actual smooth H_q was numerically constructed.

The domains themselves are connected and have two boundary components. This review asserts nothing about connected boundaries, dimension m=1, one fixed domain as q varies, or constants uniform over changing dimension m.

## Independence, exposure order, and pinned target

The source reviewed was `inputs/PROOF.md`, SHA256 `c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658`, 10412 bytes. The parent assignment identifies head `c29139d2c2a98f1a0284d0dc794c88f51c680a0c`; that head label was supplied by the parent and was not independently fetched in this read-only shard.

The parent assignment disclosed the construction, intended formulas, and adversarial targets. Thus this is an independent reconstruction and falsification attempt relative to prior reports, not a blind discovery exercise. The first source read was the current PROOF after a restricted filename inventory of `inputs/`. Its internal-audit endorsement was visible and explicitly excluded from evidence. I wrote `INDEPENDENT_CORE.md` at 2026-10-17T23:15:05.987844+00:00 before opening primary sources or running the exact computations.

I then read the PDF skill, queried only the two identified primary PDFs through the web tool, fetched four primary PDFs into this shard's private source directory, extracted relevant passages, rendered and visually inspected the relevant theorem/question pages, and built independent exact checks. No content of old AUDIT, ACCEPTANCE, STATUS, MANIFEST, README, SOURCE_METADATA, SOURCE_DEPENDENCIES, parent/root acceptance reports, or concurrent reviewer reports was opened. Their filenames alone appeared in the initial inventory. No outside individual was contacted. No subagent, Git write, tracker, PR, release, or Zenodo operation was performed.

`INPUT_RECEIPTS.json` records all nonself file sources and their hashes, including the skill instructions. `ARTIFACT_SHA256.json` records own artifacts without hashing itself; its detached SHA sidecar anchors that manifest without a circular self-pin. Source renderings/text are private derivatives and their hashes are also listed there.

## Independent derivation of the harmonic count

Put n=m+1, the ambient dimension. The number of monomials of homogeneous degree ell in n variables is C(ell+m,m). To verify the trace subtraction without assuming the desired endpoint count, give polynomial monomials the Fischer inner product

    <x^alpha,x^beta> = alpha! if alpha=beta, and 0 otherwise.

Multiplication by |x|^2 is the adjoint of the Euclidean Laplacian between the degree-(ell-2) and degree-ell polynomial spaces. Multiplication by |x|^2 is injective, so its adjoint is surjective in finite dimensions. The harmonic kernel therefore has dimension

    d_{m,ell} = C(ell+m,m) - C(ell+m-2,m),

with the second term zero at ell=0,1. Polar coordinates show that restricting a homogeneous harmonic polynomial to the sphere gives an eigenfunction with eigenvalue ell(ell+m-1). The orthogonal decomposition into harmonic polynomials and |x|^2 times lower-degree polynomials, together with density of polynomial restrictions, makes these modes complete. Distinct nonnegative degrees give distinct eigenvalues because consecutive levels differ by 2ell+m>0.

Consequently the modes strictly below T_q are precisely degrees 0 through q-1. In the sum of their dimensions, all polynomial-dimension terms cancel except the final two:

    N_q = C(q+m-1,m) + C(q+m-2,m).

At q=1 the result is N_1=1; no generalized binomial coefficient with negative top entry is being used. At q=2, N_2=m+2. For m=2, d_{2,ell}=2ell+1 and N_q=q^2. For m=3, d_{3,ell}=(ell+1)^2 and N_q=q(q+1)(2q+1)/6. These provide useful independently recognizable special cases.

The exact code also enumerates monomials and builds the actual integer Laplacian matrices for m=2,3,4 and ell=0,...,6. Gaussian elimination over rational numbers independently verifies each harmonic kernel dimension and surjectivity. This is finite corroboration of the general argument, not its replacement.

## Disjoint union, both zeros, and exact index

For a disjoint union of two closed Riemannian manifolds, the Hilbert spaces and Dirichlet forms split as direct sums. Its Laplacian spectrum is therefore the union of the two spectral multisets. On each connected component, an eigenfunction of eigenvalue zero has zero Dirichlet energy and is constant; there is exactly one zero per component. The reversed normal orientation of a cavity component changes neither its induced metric nor its intrinsic Laplacian.

The sphere contributes N_q modes strictly below T_q, including its zero. The connected cavity contributes exactly one mode below T_q, its own zero. Thus the entire boundary has exactly N_q+1 modes below T_q. The next mode is a sphere mode at T_q:

    lambda_{N_q+2}(S^m disjoint-union H_q) = T_q.

Indeed the entire T_q cluster runs from N_q+2 through N_q+1+d_{m,q}. Strict cavity gap excludes an additional tie at T_q, although a weak gap >=T_q would already suffice for the first-index identity. q=1 gives two zeros followed by lambda_3=m, exactly as required.

The first positive boundary eigenvalue is lambda_3=m for this family. It is not the first positive eigenvalue of the cavity. For q>1 the target T_q occurs later. In particular, transferring the cavity's large first positive eigenvalue directly to boundary lambda_2 or lambda_3 would be wrong; the proof does not do this.

## Exact size bound and asymptotic contradiction

For q>=m>=2, each of the two binomial coefficients is at most (q+m)^m. Hence

    k_q <= 2(q+m)^m+2 <= 2^(m+2) q^m,
    k_q^(2/m) <= C_m q^2,  C_m=2^(2+4/m).

All quantities being raised to positive powers are positive. An equivalent integer check is

    k_q^2 <= 2^(2m+4) q^(2m).

Write A=q+rho_m, V=|Omega_q|, alpha=(m+2)/m, gamma=(m+2)/(m+1), and v=omega_{m+1}(1-2^(-(m+1))). The geometric containment gives 0<v<=V<=omega_{m+1}. Direct algebra, with the volume power retained, gives

    I^alpha = A^(1+2/m) / V^gamma <= K A^(1+2/m),
    K = v^(-gamma).

Since T_q>=q^2 and F_q=T_q A^(2/m),

    0 < D_q/F_q
      <= K A/q^2 + C_m/A^(2/m)
      -> 0

for each fixed m. Therefore F_q/D_q -> +infinity. The first upper-bound term decays like q^-1, and the second like q^(-2/m); m=2 remains valid because both decay. q<m is irrelevant to the limit, and the exact counting identity remains valid there.

For every finite real pair a,b, set M=max(0,a,b). Both target terms X=I^alpha and Y=k_q^(2/m) are positive, so aX+bY<=M(X+Y). When F_q/(X+Y)>M, the desired bound fails strictly. This includes zero, negative, mixed-sign, and arbitrarily large finite coefficients; no division by a nonpositive proposed right side occurs.

Under ambient rescaling by a factor t>0, lambda scales as t^-2, area as t^m, and volume as t^(m+1). Thus the normalized eigenvalue, isoperimetric ratio, its target power, and the index term all remain invariant. Replacing the correct volume exponent gamma by alpha would give a nonzero scaling exponent and is explicitly rejected by an exact negative control.

## Independent rational quantitative envelope

A new checkable bound avoids evaluating pi, sphere volumes, or irrational powers numerically. For n=m+1, cube inclusions give

    (2/n)^n <= omega_n <= 2^n.

Let

    R=n*2^n >= rho_m,
    b=(2/n)^n*(1-2^-n) <= v,
    J=max(1,b^-2) >= K.

The last inequality uses 1<gamma<2. Also C_m<=16 for every m>=2. For q>=max(m,R), A<=2q and A>=q, so

    D_q/F_q <= 2J/q + 16/q^(2/m)
             <= (2J+16)/q^(2/m),
    F_q/D_q >= q^(2/m)/(2J+16).

This proves an explicit divergent lower bound with only rational dimension-dependent constants. On q=t^m, any integer t satisfying t^m>=max(m,R) and t^2>(2J+16)M certifies strict violation for a given finite pair a,b with M=max(0,a,b). The code computes these exact sufficient thresholds for 35 sample dimension/coefficient choices, including both coefficients negative and coefficients as large as 10^100. The thresholds certify the analytic envelope; they are not evaluated spectra or geometric reconstructions.

## Geometry assumptions actually used

The spectral argument needs H_q smooth, compact, embedded, connected, contained in the half ball, with the stated area and gap. Compact embedded codimension-one separation provides its bounded complementary region U_q. Every point outside the closed half ball can be joined to infinity without meeting H_q, so U_q lies in the half ball. This proves the volume bound and keeps the two boundary components positively separated.

The exterior of H_q is a connected open subset of Euclidean space, hence path connected. For any point in that exterior inside radius 3/4, take a path to outside the unit ball and stop it at its first radius-3/4 encounter. The stopped path stays inside the outer ball. Points already outside radius 3/4 lie in the full connected annulus outside the half ball. This establishes connectedness of Omega_q regardless of knotting or genus of the cavity. No convexity, uniform curvature, injectivity radius, uniform Weyl remainder, or fixed topology in dimension two is used.

The metric lemma compares Dirichlet energies by c^(+/- (1+m/2)) and L2 norms by c^(+/-m/2), hence Rayleigh quotients by c^(+/- (m+1)). Min-max over the full common H1 space includes zero modes automatically and avoids a changing mean-zero subspace. The C1 isometric embedding has the prescribed smooth metric; its smooth approximants induce smooth metrics converging uniformly to that smooth metric. No spectral theory on a singular final boundary is required. Exact area restoration changes eigenvalues by a factor tending to one and keeps the surface inside the prescribed ball.

## Primary-source scope and pins

- [OWR 33/2012](https://ems.press/content/serial-article-files/46403), PDF pages 22-24, printed 2034-2036: Theorem 3 addresses bounded smooth Euclidean domains. Its following open question asks for the additive version with dimension-only constants. No connected-boundary restriction appears. PDF SHA256 `20d5708e6ab0ccee4e8944d8e11c514221c2642a4e15c878067eed34405bc8e9`, 1024557 bytes.
- [CEG author preprint](https://arxiv.org/pdf/1007.0826), PDF pages 1-2 and 14: indexing begins at lambda_1=0, Theorem 1.1 has the bounded-domain smooth-boundary scope, and Example 3.1 explicitly treats a disconnected two-component boundary with two zero modes. This resolves a potential convention objection. PDF SHA256 `68238e41cde092efed54e5743e4af35fd512e7913c6d557ec7809a1a43d74888`, 230881 bytes. The downloaded artifact displays the v2 arXiv label and a different body date; the byte pin, rather than an inferred release date, identifies what was checked.
- [CDE author preprint](https://arxiv.org/pdf/0909.5346), PDF pages 1,6,14-15: Theorem 1.4 gives the required unbounded normalized first positive eigenvalue for embedded surfaces, and for fixed abstract type in dimension at least three. Section 5 uses C1 isometric embeddings and smooth approximation. Their zero-based indexing places the first positive eigenvalue at lambda_1. PDF SHA256 `a2bc60b7f1b00009ef39ac1260ee6b9cb4a3464d3617f0f3944a9aee5fa6bb35`, 216749 bytes.
- [De Lellis-Szekelyhidi](https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/contr_vol_Nash_11.pdf), Definition 1.1 / Theorem 1.2, printed pages 3-4: a smooth short embedding into dimension at least m+1 has C0-close C1 isometric embeddings. The embedding conclusion is part of the statement, so immersion alone is not being substituted. PDF SHA256 `22ca78b5750848189dee869f3fc8895c0b935c4af5316450132164aba87e0ddc`, 429804 bytes.

These are primary sources. No secondary source or previous acceptance verdict is used. The separation and approximation background was not independently re-proved from its original publications; CDE explicitly documents the approximation step used here.

## Exact computation and adversarial diagnostics

`verify_spectral.py` uses integer and Fraction arithmetic, explicit `require` checks, and no runtime assertions. Final runs in normal Python and Python -O produced byte-identical complete result payloads:

    bytes each: 1,922,366
    SHA256: 89195b25d6faed83eb78fcd1c80b4f22e49550acbf9893b28d975e6f8c9b074f

All result fields and negative diagnostic strings are retained in `results.normal.json` and `results.optimized.json`; `RUN_RECEIPTS.json` records interpreter and invocation details. Coverage consists of 21 exact Laplacian ranks, 3989 count/power-bound cases (m=2,...,32 and selected m=64,128,256, including q=1, q=m-1,m,m+1, and q=10^6), 144 multiset index cases, 63 scaling cases, 14 rational envelope cases, 35 coefficient thresholds, 15 negative rejections, and one positive cavity-tie control.

For the concrete m=2,q=2 spectral controls, the correct N=4, T=6, first target index=6, and last target index=10. The synthetic cavity has one zero and next value 13. The checking functions receive each actual wrong alternative:

| Wrong alternative | Candidate index / actual result | Diagnostic |
| --- | --- | --- |
| Omit the cavity zero in indexing | 5 / eigenvalue 2 | Rejects target identity |
| Count sphere levels <=T in N | 11 / eigenvalue 12 | Rejects target identity |
| Count distinct levels, dropping multiplicities | 4 / eigenvalue 2 | Rejects target identity |
| Omit the second endpoint binomial | 5 / eigenvalue 2 | Rejects target identity |
| Add a cavity eigenvalue 5<T | 6 / eigenvalue 5 | Rejects target identity |
| Give cavity two zeros | 6 / eigenvalue 2 | Rejects target identity |
| Substitute boundary lambda_2 for cavity's first positive mode | 2 / eigenvalue 0 | Rejects target identity |
| Substitute boundary's first positive mode for T at q=2 | 3 / eigenvalue 2 | Rejects target identity |
| Shift index to 7 while claiming it is the first T mode | 7 / eigenvalue 6 | Identity passes; independent first-index check rejects |
| Omit harmonic trace subtraction at m=2,ell=2 | claimed dimension 6 / exact kernel 5 | Rejects multiplicity |
| Use alpha as volume exponent | m=2 scaling exponent -2 | Rejects scale invariance |

Four further controls reject inputs outside m>=2,q>=1; these are scope checks, not evidence that an out-of-scope mathematical statement is false. The positive tie control adds three cavity modes exactly at T and confirms the first index stays 6 while multiplicity increases. These tests are explicit counterexample/sanity controls, not general algorithm mutation coverage. Synthetic spectra check bookkeeping only; their values are not claimed to be realized by a smooth hypersurface.

## Limits, recommendation, and completion

A fixed-domain Weyl law permits its onset and remainder to depend on the domain. Here both domain and index vary, and the large cavity gap postpones its contribution below T_q. Thus a nonuniform Weyl limit cannot disprove this construction, and the construction does not refute any fixed-domain Weyl statement. The known multiplicative estimate is also compatible: at this index its product of the two target factors has substantially larger order than the asserted additive estimate.

No repair is required in the current proof's spectral argument. A useful optional exposition change would be to include the direct D_q/F_q bound and the M=max(0,a,b) observation when stating failure for arbitrary finite real constants; the positive-constant argument already suffices for the usual question. This is not a condition for accepting the mathematical mechanism.

Review completion estimate: 100% of this assigned independent spectral/counting/asymptotic validation. This percentage describes the review task, not a probability of novelty, publication acceptance, or correctness of all mathematics in the repository. Final UTC is recorded in RESEARCH_LOG.md and the artifact receipt.
