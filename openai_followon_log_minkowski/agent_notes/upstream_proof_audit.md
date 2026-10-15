# Independent upstream proof audit

Audit started 2026-10-06 (America/Los_Angeles); initial report 2026-10-06 21:12 PDT / 2026-10-07 04:12 UTC.

## Assignment and scope actually reviewed

The original follow-on targets are smooth even existence and uniqueness of
`h^(1-p) det(∇²h+hI)=f` in every ambient dimension `n>=2`, `0<=p<1`, and
uniqueness of arbitrary full-dimensional origin-symmetric bodies having equal
`L_p` surface-area measure for `0<p<1`. This audit scrutinizes the upstream
logarithmic Brunn--Minkowski input. It does **not** certify the follow-on
transfer theorem, existence/regularity inputs, novelty, or publication package.

Read-only source: `/Users/alec/Desktop/math`, HEAD
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Read repository README,
manuscript-specific README and citation, `lean/README.md`, comparator README,
`lean/docs/091.md`, formalization catalogue entry, all manuscript analytic proof
sections (`introduction`, `reduction`, `moment`, `identities`, `density`,
`tensor`, `variance`), the `L_p` corollary proof in `measure.tex`, and selected
relevant sections of the **actual** 24,491-line Lean source. The later
measure-theoretic applications in `measure.tex` are not dependencies of the
present follow-on targets and were not certified by this audit.

No source-clone files were written. No Git mutations or external human contact
were performed. Reproducible local checks below belong solely to this folder.

## Pinned source and correction check

Source directory:
`preprints/The-logarithmic-Brunn-Minkowski-conjecture-September-23-2026/build/`.

| File | SHA-256 |
|---|---|
| main.tex | d356923b220ebffb27178c2ea84163502bd09794c6244b529e5d0c4db7dbfe13 |
| introduction.tex | 212126ab7376cc1d303373ea41942c66166b0b2f62977a6cd4a9cb26b9bdaa1f |
| reduction.tex | f2c39bb83b42fd63d4fa1189d9f0d120d4490317d5fe117995f68458f44a5688 |
| moment.tex | 7e145c98d83124dcd250cad6b530c7e457a672249d76cab7ab7ba9e297049755 |
| identities.tex | 3726a4ff74c31c15f33f60f53ef2e6cf23ab1a38758e01886e8fb78c520c762c |
| density.tex | 507e24c5c22c15d537875ce39e9777b91a3e9c8a51776622521b86c2adeb4e2c |
| tensor.tex | a4ff83463ed8aac5409de660da013161c12144cf8b431626c3ed2363112bd798 |
| variance.tex | b3fd5c3b6a11895c2b3ceb26566869fb67b96966b4705700e80326b71a69a2e1 |

`lean/OAI/Geometry/LogVolume/BrunnMinkowski.lean` SHA-256:
`bb798d24c3506422bc6ebdf064b71e3a1cf0f5f77835dd1985da2ff18a2c43a5`.
`lean/docs/091.md` SHA-256:
`acbcff0c78fd7c308009732bb529fc5b5c6f48e39aea0fb84d07fc2d84951177`.

Read-only GitHub API searches for the latest commit touching the manuscript
directory and actual Lean proof returned the pinned commit in both cases,
timestamp `2026-10-06T21:58:50Z`, message `Initial commit`. Thus no later
correction was observed. September 23 in the manuscript is an internal
manuscript date; this repository evidence puts public commit disclosure on
October 6, 2026. It does not establish that no earlier disclosure exists.

## Exact pivotal statement

Upstream `introduction.tex:21--31` claims: for every `n>=1`, compact convex
bodies with nonempty interior `K=-K`, `L=-L`, and `0<=t<=1`,

`|W[h_K^(1-t) h_L^t]| >= |K|^(1-t) |L|^t`.

The support function is restricted to the Euclidean unit sphere, and Wulff
intersection is essential; the geometric mean need not itself be a support
function. Bodies are full-dimensional, hence the symmetric support functions
are strictly positive. No smoothness, common normal fan, or unconditionality
assumption is present. The dimensional convention is ambient `R^n`, sphere
`S^(n-1)`. The one-dimensional case is proved separately as exact interval
equality.

The intermediary variance proposition is `reduction.tex:9--23`: for
`V=ε|x|²/2 + Σ_i ψ_i`, `ψ_i=(p_i·x/h_i)^q`, even integer `q>=2`, `ε>0`,
`p_i!=0`, `h_i>0`, probability `dμ=Z^-1 exp(-V)dx`,

`Var_μ(Σ_i b_i ψ_i) <= Σ_i b_i² E_μ ψ_i` for all real `b_i`.

Spanning is required only when interpreting the limiting slabs as bounded
polytopes. All Gaussian-regularized polynomial moments exist even without it.

## Independent checks of the mathematical mechanism

1. **Reduction to finite slabs.** Differentiating the partition integral
   yields `d² log Z/dt² = Var(dot V)-E(ddot V)`. Geometric slab interpolation
   has `dot V=Σb_iψ_i`, `ddot V=Σb_i²ψ_i`, with
   `b_i=-q log(h_i^1/h_i^0)`. This gives log-concavity from the variance
   proposition with the correct signs and constants. Gaussian domination
   permits even `q->∞`; only finitely many hyperplanes are exceptional.
   Monotone convergence as `ε->0` yields volume. Nested finite directions
   containing a basis give bounded outer approximations and continuity of
   measure from above. Positivity prevents degeneration. Endpoints and `n=1`
   match the stated quantifiers.

2. **Moment-coordinate construction.** The truncated target on `B_R` is even,
   smooth and positive on its closure, centered, with
   `D²(V+log Z_R)>=εI`. Berman--Berndtsson's compact theorem and Klartag's
   uniform `4/ε` Hessian cap apply. Reflecting the unique translated minimum
   yields an even potential. The supporting-plane estimate
   `g_R(y)>=g_R(z)+|∇φ_R(z)·y|-∇φ_R(z)·z`, integrated with
   `E[z·∇φ_R]=n`, gives a coercive lower bound uniform in `R`; it does not
   misuse an unproved lower Hessian cap. Together with the global upper cap,
   the moment equation bounds the determinant away from zero on compact sets,
   hence gives local uniform ellipticity. Interior regularity and bootstrapping
   provide a smooth subsequential limit. The common exponential bound justifies
   passage of total mass and pushforward. Dense gradient image plus supporting
   planes makes every tilted potential coercive, proving surjectivity; positive
   Hessian gives injectivity. This is more than merely invoking the abstract
   moment-measure theorem.

3. **Adjoints and range identity.** In source coordinates `∂*_k=x_k-∂_k`;
   in target coordinates negative weighted divergence gives
   `δ_μτ=x` and `Af=x·∇f-τ:D²f`. For compact `f`,
   `B=τD²fτ`, `W=δ_μB=τ∇_x(A-1)f`,
   `u=δ_μW=A(A-1)f`. Direct expansion of the third derivative of `φ`
   confirms the gradient identity and symmetry of `D_zW`. Double adjunction
   gives both `E[uF]=E[W·∇F]` and `E[uF]=E[B:D²F]`. Compact support in source
   coordinates follows from the actual global inverse homeomorphism.

4. **Density with no global lower cap.** Orthogonality gives the fourth-order
   elliptic distribution equation `A(A-1)g=0`. Local positive definiteness,
   not a global positive lower bound, suffices for interior smoothness.
   Expanding `(A-1)(η_r^4g)` verifies the coefficients `4,-12,-8` in
   `density.tex`. The two cutoff estimates bound both `Ag` and the Dirichlet
   energy. The split `w=g-Ag`, `v=Ag` yields `Aw=0`, `Av=v` in `L²`.
   Cutoffs force `w` constant. Approximation of `v` by `η_rv` in graph norm,
   together with
   `E||τ^(1/2)D²fτ^(1/2)||²=||Af||²-E[fAf]`, forces `v` linear.
   Thus only affine obstructions remain. Evenness removes linear modes and
   centering removes constants. No hidden spectral-gap assumption is inserted.

5. **Tensor estimate: pivotal algebra checked independently.** Weighted
   vector Bochner gives
   `Eu²=E(W^THW)+E tr((D_xW)²)`. The manuscript correctly keeps a matrix
   square instead of silently replacing it by a Hilbert--Schmidt square.
   `D_zW=B+R` has symmetric `R`, so its final term
   `tr(MRMR)` is nonnegative. With `Q=hτh`, `h=D_x²f`, twice differentiating
   the moment equation and integrating the divergence gives exactly the
   signs in `tensor.tex:100--120`. A constant dual-coordinate change
   `z=Tz'`, `x'=T^Tx` normalizes `τ` at one point, without differentiating a
   moving frame. Every derivative index then pairs covariantly against a
   contravariant index, so the relevant scalars are invariant.

   At `τ=I`, `S_ijk=f_ijk`, `J_ijk=h_ia C_ajk`. Direct contraction yields
   `cross=||S||²+<S,J>`,
   `qder=2<S,J>+<J,J^(12)>`, `cubic=||J||²`. Because `J` is symmetric in
   its last two slots,
   `||SymJ||²=(||J||²+2<J,J^(12)>)/3`. Therefore the remainder is exactly

   `2||S+SymJ||² + (1/6)||J-J^(12)||² >=0`.

   The factor `1/6` and the cross coefficients agree. The accompanying
   standalone Python certificate checks these contractions and the final
   identity in exact rational arithmetic, dimensions 1--5, including
   arbitrary indefinite symmetric `h`. This is a falsification check; the
   above algebra supplies the general argument.

6. **Homogeneous variance completion.** `H_ix=(q-1)∇ψ_i` and the Stein
   identity give `m_i=E tr(τH_i)=q Eψ_i`. Matrix Cauchy--Schwarz yields
   `d_i²<=m_i E tr(MBH_iB)` even for indefinite `B`.
   Form Cauchy--Schwarz gives
   `E W^TH_iW >= (q-1)d_i²/m_i`. Adding the two bounds and using the tensor
   estimate gives `Eu²>=Σd_i²/Eψ_i`. The Gaussian terms dropped are
   nonnegative. Density and polynomial `L²` continuity extend it to every
   centered even test. A final scalar Cauchy--Schwarz supplies the original
   variance inequality. Division by `Eψ_i` is justified by positive density
   and nonzero `p_i`.

7. **`L_p` volume consequence.** The unit-volume normalizations
   `K_0=|K|^(-1/n)K`, `L_0=|L|^(-1/n)L`, scalar
   `c=((1-t)|K|^(p/n)+t|L|^(p/n))^(1/p)` and reweighting
   `θ=t|L|^(p/n)/c^p` are correct. Power-mean domination of the geometric
   mean and monotonicity/homogeneity of the Wulff intersection give the
   additive volume-power inequality for every `0<p<1`. The corollary does
   not claim a strictness/equality classification, so that classification
   must be supplied independently for general-body uniqueness.

## Primary external dependencies checked here

- [Berman--Berndtsson, Theorem 1.1](https://numdam.org/item/10.5802/afst.1386.pdf):
  a positive smooth weight on a compact convex target containing zero has a
  smooth moment potential with a gradient diffeomorphism precisely when the
  weighted barycenter is zero; uniqueness is up to source translation. Its
  statement and the `g=e^-V/Z_R` substitution were checked from the paper.
- [Klartag, 1309.2767v1, Proposition 3.1 and Remark 3.5](https://arxiv.org/pdf/1309.2767v1):
  assumptions include a bounded smooth positively curved target and smooth
  bounded convex density potential and derivatives; Hessian lower bound
  `εI` gives the explicit moment-Hessian upper bound `4/ε`. Truncated balls
  meet these assumptions, uniformly in the value of this bound.
- [Wang 2012, Corollary 2.3](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806604056548241409-1806604056548241409-2398ebf5172d5f2f7f2c3b729bc59588.pdf):
  after an initial HTTP403 at the old publisher URL, the parallel dependency
  auditor retrieved the journal PDF; I independently read its exact statement
  in the saved text. It is expressly for general concave uniformly elliptic
  `F` on real symmetric matrices and `C²` solutions with a `C^α` right-hand
  side. It provides a smaller positive Hölder exponent and a bound depending
  only on dimension, ellipticity, exponent, `|F(0)|`, and the local norms of
  `f,u`. The smooth spectral scalar extension in the manuscript meets it.
  Local PDF SHA-256:
  `ffd3deef72830c77efe1f8cf08db8d238ac47ca01ef3449cd8c6db28e52ff542`.
- The uses of standard local Schauder and distributional elliptic regularity
  are structurally correct. Their precise primary-source citations should
  remain recorded in the parallel dependency audit.

## Actual formalization versus comparator

`lean/ComparatorChallenges/LogBrunnMinkowski.lean` intentionally ends its
target theorem with `sorry`; it is a challenge statement and was not treated
as a proof. The actual file is
`lean/OAI/Geometry/LogVolume/BrunnMinkowski.lean`, whose declared dependency
is `Mathlib`. Relevant genuine declarations include:

| Declaration | Pinned line | Semantic scope inspected |
|---|---:|---|
| `CompactMomentVariational.C11_to_C2` | 8715 | upgrades the actual convex moment pushforward under locally elliptic coefficients |
| `CompactMomentVariational.C2_positive_MA` | 8742 | pointwise positivity and moment equation |
| `IntegratedTensor.tensor_estimate` | 17558 | integrated trace inequality from smooth moment equation |
| `FullTensor.tensor_energy` | 17707 | target-measure Bochner and tensor energy |
| `LogBrunnMinkowski.SoftVarianceStatement` | 20144 | correct Gaussian slab variance quantifiers |
| `LogBrunnMinkowski.main_of_softVariance` | 20208 | all-body reduction with separate one-dimensional case |
| `CompactMomentVariational.C2_to_smooth` | 24019 | regularity bootstrap |
| `ActualMoment.coordinates` | 24370 | actual diffeomorphism and Gaussian slab probability pushforward |
| `LogBrunnMinkowski.softVariance` | 24468 | obtains moment coordinates rather than assuming them |
| `LogBrunnMinkowski.main` | 24481 | literal full-body theorem, matching sphere Wulff semantics |

The final `main` takes only dimension, compactness, convexity, nonempty
interior, origin symmetry, and interpolation-range hypotheses. Its definitions
`support`, `wulff`, `logCombination`, `IsConvexBody`, `OriginSymmetric`
match the manuscript mathematically. `ENNReal` volume powers carry the same
geometric-mean meaning for these positive finite body volumes. Selected
intermediary `potential`, `law`, variance, and reduction definitions also
agree. Searches found no literal `sorry`, `admit`, `axiom`, or `unsafe`, and
no `native_decide`/`sorryAx` shortcuts in the actual file. **This audit did not
compile it or kernel-check dependencies.** That must be reported separately
by the dedicated formal-verification audit; source inspection alone is not
formal certification. The follow-on Minkowski theorem is not formalized by
this declaration.

## Verdict and remaining gap

No substantive error was found in the upstream analytic argument actually
needed here. The tensor estimate, dense-range construction and slab reduction
survived independent algebraic and boundary scrutiny. The strongest result
independently verified in this audit is the validity of their stated
mathematical deduction chain under the checked compact moment/Hessian inputs
and standard local elliptic regularity. The audit's exact remaining evidentiary
gap is reproduction of the actual Lean build/axiom check and confirmation of
the precise remaining Schauder and distributional regularity citations in the
parallel dependency audit. The pivotal Evans--Krylov source was checked above.

There is no basis here for promoting the follow-on target before the separate
He--Liu transfer, general-body strictness/equality, existence, priority, and
complete-package audits pass. Attribution must remain: OpenAI supplies the
new logarithmic inequality, established authors supply their reductions, and
the follow-on note is a newly available consequence rather than a new proof
of logarithmic Brunn--Minkowski.

## Reproduction

Run:

`python3 agent_notes/upstream_audit_tensor_certificate.py`

Python version used: 3.14.6; standard library only. Expected result:
`PASS: 200 exact rational tensor checks; dimensions 1--5; seed 20261006.`
