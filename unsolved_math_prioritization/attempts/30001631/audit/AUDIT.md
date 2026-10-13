# Independent adversarial audit: 30001631 / OWR-4535-006

Audit date: 2026-10-05 UTC. Catalog rank supplied for this investigation: 699.

## Verdict

**PASS WITH CONTROLLING CLARIFICATIONS, for an unsolved 5/5 investigation only.**

The frozen packet contains five substantive approaches and correct partial mathematical statements. None proves any curvature sign for an actual positive-dimensional finite-type Takhtajan–Zograf (TZ) metric. No actual TZ counterexample, complete prior resolution, or novelty claim has been verified. The justified outcome is **NO RESOLUTION / exhausted five attempted approach families**. This does not mean every possible method or every paper has been exhausted.

No substantive mathematical error was found in the stated partial propositions. Two wording clarifications below control the interpretation of Approach 1. They do not repair a claimed proof of negativity, because no such proof is claimed or used. All frozen bytes remain unchanged. This audit is a separate object and does not silently change the frozen `independent_audit_status: pending` field.

## 1. Exact object binding and independence

The independently verified input is the ten-file public directory, together with its ZIP:

- Original `MANIFEST.json`: 1,508 bytes; SHA-256 `793eff4aec0c86808289fa1ce17d32d95f52c03dd09219d13538a6fa6527d5cd`
- Original public ZIP: 21,262 bytes; SHA-256 `c9a370d76b6ef5cb98214f49098e812eb9c470adfa9e3a694bcbea4bd006298f`
- Original `RESEARCH.md`: 23,297 bytes; SHA-256 `b6f10bdce68153be76cb8afdef6a08b2f150bafe21dfb9b19777698e4033546c`
- Original control result: SHA-256 `beecfadff13471436484aaf671da8e7242fefc17a8f3e777efb0050e4cb7d86a`

Every one of the nine manifest-listed payload files was hashed independently. The externally supplied manifest digest supplies its otherwise omitted self-binding. The ten ZIP entries are unique, have exactly the directory allowlist, and each decompressed member equals its corresponding original file byte-for-byte. No directories or symlinks occur in the input public directory. Original controls were replayed, with all eleven passing and their result bytes identical to the recorded result. Input bytes were re-read and compared at the end of the independent run.

This audit independently reads the proofs and primary sources; replay is not substituted for mathematical review. No repository, branch, PR, website, or other remote object was written. All changes are new local audit files outside the input directory. The separate public audit contains authored analysis, test code/results, and verification metadata only. Source PDFs, source extracts, rendered source pages, dataset records, and private coordination material are excluded.

## 2. Controlling clarifications and affected dependencies

Line references below are to the exact `RESEARCH.md` digest above.

### C1. Tangent linearity, mixed pairing, and the Gram-frame obstruction

Locations: lines 35–45 (definition and polarization), 71–80 (Gram lemma, attempted identification, and obstruction); Approach 1 in `APPROACH_LOG.md`.

For a fixed surface and fixed cusp normalization, the assignment from a tangent Beltrami differential to its holomorphic quadratic differential, defined by `mu = y^2 conjugate(q)`, is **complex-antilinear**. Thus, if `q_mu` has coefficients `a_m` and `q_nu` has coefficients `b_m`, the mixed pairing for the declared convention linear in its first argument is

    g_a(mu,nu) = C0 sum_m conjugate(a_m) b_m / m^5,
    C0 = 3/(128 pi^5).

The complex-linear isometry into an ordinary sequence Hilbert space is

    J_a(mu)_m = sqrt(C0) conjugate(a_m) / m^(5/2).

It identifies the finite-dimensional tangent space with **its image**, not with the whole infinite-dimensional sequence space. Equivalently one can use the holomorphic q-coefficients with the conjugate complex structure. Replacing `mu` by `c mu` replaces `q` and its coefficients by `conjugate(c)` times their old values, which gives the required first-slot linearity of the displayed pairing.

This fiberwise statement does not imply that the sections `J_a(e_i)` obtained from a holomorphic tangent frame depend holomorphically, in Hilbert norm, on the moduli parameters. Cusp charts, the uniformizing group, and harmonic projection vary. The q-coefficient assignment itself must not be promoted to a complex-linear holomorphic tangent embedding. Even coordinatewise holomorphy would require adequate Hilbert-norm control before one could invoke the infinite-dimensional Gram lemma.

**Dependency check:** no proof in the frozen packet actually makes that promotion. Proposition 1 uses only a fixed fiber, Tonelli, and Parseval. Lemma 2 assumes a genuinely holomorphic Gram frame and proves a general conditional statement. The attempted application is explicitly stopped at lines 78–80 and is never used as an established sign input to Proposition 3 or any later approach. The other four approach families, the norm coefficient, and the unsolved outcome are unaffected. The correct controlling reading of the proposed application is “if the conjugated-coefficient tangent embeddings formed a holomorphic Hilbert Gram frame.” This assumption remains unproved.

### C2. Cofinite/finite-type, not finite groups

Location: `RESEARCH.md` line 82, phrase referring to “finite-group Bers maps.”

Read this as **Bers maps for nontrivial Fuchsian groups in the finite-type/cofinite setting**. A cofinite Fuchsian uniformizing group here is generally infinite; finite-dimensional Teichmüller space does not make the group finite. Teo's Remark 5.3 distinguishes the special universal parabolic Bers isomorphism from the Bers isomorphisms for nontrivial groups. His subsequent discussion proposes studying how universal curvature information could bear on cofinite surfaces. It is not a completed finite-type negativity theorem.

**Dependency check:** the imprecise adjective affects the source description only. The paper's special universal metric identity, the absence of a verified holomorphic isometric application with controlled curvature, and the five-family unresolved outcome are unchanged. No inference about a finite group is used in any calculation.

No original file is edited to incorporate either clarification. Any later synopsis or promotion of these results must retain them.

## 3. Source, definition, and target audit

### Primary question

The original Obitsu contribution in OWR 53/2010 was independently retrieved and its printed pp. 3128–3130 read. Printed p. 3130, PDF page 46, was also visually inspected. Its third open problem asks about TZ curvature negativity without naming sectional, holomorphic sectional, bisectional, or Ricci curvature. The fourth item conditionally proposes studying the negative Ricci form; it is a separate item. The mathematical target in the packet preserves that distinction. [OWR](https://ems.press/content/serial-article-files/46312)

The live selected problem webpage independently returned HTTP 403. Neither its current text nor the missing selected raw statement/AI-report corpus was used as evidence. The compact catalog rank, ID/code association, and recorded raw-source hashes are supplied provenance labels, not newly recomputed raw-corpus matches. The audit verifies the independently inspected OWR mathematical target; it does not certify byte identity of an unavailable dataset statement.

### Surface and moduli assumptions

The working hypotheses are consistent: `n>0`, `2g-2+n>0`, and `d=3g-3+n>0`. The first supplies a nonzero cuspidal sum, the second a finite-area complete hyperbolic fiber of curvature −1, and the third nonzero tangent directions. A torsion-free cofinite Fuchsian uniformization is understood for a smooth punctured Riemann surface. The excluded three-punctured sphere has no tested tangent directions. The `n=0` zero sum must not be called a positive TZ metric.

The fiber metric is `y^-2|dz|^2`; its area is `y^-2 dxdy`. A chosen primitive parabolic generator is normalized to translation by one, after choosing its orientation. The Eisenstein series has unit coefficient of `y^2` in its own normalized cusp. Residual real translations only change Fourier phases, leaving the squared norm invariant. Conjugating another cusp to infinity requires pulling back the Beltrami tensor, including its unimodular derivative factor; the normalized representative in Proposition 1 already does this.

OTW §1.1 and PTT §2.1.2 independently confirm the harmonic tangent representatives, the weighted cusp integral, the sum over cusps, and Kählerness of each summand. Individual summands require labels or a cusp-preserving quotient; their sum is invariant under cusp permutations. Local orbifold uniformizing charts carry the same curvature tensors as Teichmüller space. There is no claim of an ordinary tangent metric at a singular coarse-space point. [OTW](https://www3.math.kyushu-u.ac.jp/~weng/otw.pdf), [PTT](https://arxiv.org/abs/1508.02102)

### Curvature convention

For the row-vector metric convention `G=(G_(i bar j))`, the contracted inverse term is `b G^-1 b*`. In indexed formulas the inverse contraction `G^(p bar q)` denotes the tensor with coefficient `(G^-1)_(q p)` in ordinary matrix indexing. This resolves a possible transpose ambiguity; the independent complex-Hermitian tests use this convention and conjugate transpose, not ordinary transpose.

The declared curvature tensor is the negative second derivative plus the inverse-metric quadratic term. For a one-dimensional coefficient `lambda`, this gives

    R = -lambda * partial_z partial_bar_z log(lambda),
    H = R/lambda^2,
    K = -(1/(2lambda)) Delta_0 log(lambda) = 2H.

Independent hyperbolic and round-sphere controls give Gaussian curvatures −1 and +1. Constant positive scaling preserves signs and leaves `-partial partial_bar log det G` unchanged. Nonpositive bisectional curvature implies nonpositive holomorphic sectional curvature and Ricci; strict bisectional negativity gives strictness. A statement concerning arbitrary real two-planes is a distinct target in dimensions greater than one. In dimension one these sign questions coincide.

## 4. Full analytic audit of the Fourier norm and conditional Gram lemma

### Cusp behavior and convergence

An integrable holomorphic quadratic differential has at most a simple pole in the puncture coordinate `u=exp(2 pi i z)`. Because `du/dz=2 pi i u`, its coefficient in the upper-half-plane coordinate is `O(u)`. It follows that `q(z)=O(exp(-2 pi y))` and the harmonic representative is `O(y^2 exp(-2 pi y))`. The same reasoning holds at every cusp after normalization. A fixed-surface Eisenstein series at `s=2` is smooth on the compact core and has at most quadratic cusp growth. Consequently its weighted `|mu|^2 dA` integral is finite: exponential decay dominates all the displayed polynomial factors.

The norm unfolding uses a nonnegative series, so Tonelli applies before finiteness is known. Absolute values of invariant Beltrami coefficients are scalar invariant under the group, since the tensor's transformation factor has modulus one. Hyperbolic area is invariant. Coset-translated fundamental domains tile the quotient by the cusp subgroup up to null sets. In a normalized cusp, the factor `y^2` from the Eisenstein summand cancels the `y^-2` in area. The resulting integral is precisely the Euclidean strip integral over `0<x<1`, `y>0`.

There is no need for a cusp asymptotic uniformly valid as `y` approaches zero in the unfolded strip. The original finite-area quotient supplies global finiteness, and the nonnegative unfolding transfers it. This distinction is important because the entire unfolded strip is not a single embedded cusp neighborhood of the original surface.

Periodicity identifies `q` with a holomorphic function on the punctured unit disk, extending holomorphically with zero value at its center. Its Taylor/Fourier series therefore converges uniformly on every circle of radius `exp(-2 pi y)<1`. Parseval is legitimate for each fixed `y>0`. After integration in `x`, all terms are nonnegative, so the second interchange of summation and integration follows from Tonelli without uniform convergence near `y=0`. The coefficient moment is

    integral_0^infinity y^4 exp(-4 pi m y) dy
      = Gamma(5)/(4 pi m)^5
      = 3/(128 pi^5 m^5).

The vanishing zero mode is essential; a nonzero constant q would produce a divergent integral at infinity. A norm of zero forces all Fourier coefficients to vanish, hence the differential is zero by holomorphy. The mixed pairing is finite by Cauchy–Schwarz and is precisely the formula in C1. These steps prove the full weighted sequence identity, not just a finite truncation. Teo 2024 Proposition 6.2 independently states the matching normalized identity. It is not a new result. [Teo 2024](https://arxiv.org/abs/2401.12260)

The width control is consistent. For an unscaled cusp width `w`, the normalized Eisenstein leading term is `(y/w)^2`, the unfolded measure is `dxdy/w^2`, and the Fourier frequency is `2 pi m/w`. The resulting coefficient is `C0*w^4`. On replacing the coordinate by width one, the quadratic differential coefficients multiply by `w^2`, giving the same norm. Using unnormalized `y^2` instead would introduce an extra `w^2` and change the stated convention. Likewise using `mu=-2y^2 conjugate(q)` multiplies the norm expression in those q-coefficients by four.

### Conditional Hilbert-space curvature

Assume genuinely Hilbert-norm holomorphic vectors `u_i` in a single fixed Hilbert space, with positive Gram matrix and the Kähler tangent-metric condition stated in the packet. For `D=sum_(i,k) v_i w_k partial_k u_i`, differentiating the Gram matrix gives a second derivative term `||D||^2`, while the inverse-Gram term equals `||PD||^2`, where `P` is the orthogonal projection onto the frame span. Hence

    R(v,bar v,w,bar w) = -||D||^2 + ||PD||^2 = -||(1-P)D||^2.

This is a valid conditional general lemma. The finite set of frame and derivative vectors makes its projection algebra finite-dimensional once the strong holomorphic maps are given. It does not prove their existence. Strict negativity requires a nonzero normal component for every tested nonzero pair. Smooth norm-preserving fiber maps do not suffice: the positive scalar metric `exp(-|z|^2)` has reduced tensor value +1 at zero while admitting the smooth one-vector realization by its square root. That countermodel correctly identifies the missing holomorphic hypothesis.

**Approach 1 outcome:** a rigorous actual TZ norm identity and a valid conditional sign criterion, with no established holomorphic variation or ambient sign application. It remains unsolved.

## 5. Curvature of a sum

For positive Hermitian cusp matrices `G_a`, put `G=sum_a G_a`, `b=sum_a b_a`, and `c=bG^-1`. Expanding the proposed weighted squares gives

    sum_a (b_a-cG_a)G_a^-1(b_a-cG_a)*
      = sum_a b_aG_a^-1b_a* - bG^-1b*.

Indeed the two cross terms total `-bc* - cb*` and the last terms total `cGc*=bc*=cb*`. Each quadratic form is nonnegative. Equality occurs exactly when every `b_a=cG_a`. The second derivatives of a sum add, so the combined curvature equals the sum of the individual tensors **minus** this defect. No common normal-coordinate assumption is needed. The proof is valid for complex matrices; the independent control uses nonreal off-diagonal entries and obtains positive defect `2529/574`, with exact zero in the common-connection equality case.

If each reduced holomorphic sectional curvature has an upper bound `-kappa_a`, with `kappa_a>0`, then for `x_a=G_a(v,bar v)>0`,

    H_G(v) <= -sum_a kappa_a*x_a^2/(sum_a x_a)^2
            <= -1/(sum_a 1/kappa_a).

The second inequality is precisely weighted Cauchy–Schwarz; its direction is correct after multiplication by a negative sign. Equality in that estimate is possible at `x_a` proportional to `1/kappa_a`, independently of whether the geometric defect vanishes. The scalar local-metric control independently differentiates two metrics and obtains total tensor `-9/2` from individual values `-1`, confirming the minus-defect direction.

**Approach 2 outcome:** the sum lemma really applies to the actual cuspidal decomposition, but no cusp curvature bound or domination estimate for a possibly positive part is provided. Neither the Gram lemma nor a Ricci statement supplies it. This is a sufficient conditional reduction, not a solution or equivalent reformulation of all possible target meanings.

## 6. Potential criterion and the line-bundle distinction

Set `G=C Psi` with `Psi=partial partial_bar psi`, positive and smooth. In the curvature formula the second derivative contributes `-C` times the fourth derivative of psi, and the quadratic term contributes `C` times the third-derivative inverse-Hessian contraction. Its contraction on a pair of vectors is nonnegative. Thus strict bisectional negativity is equivalent to the indicated fourth-order contraction strictly exceeding that quadratic term for each nonzero pair. In holomorphic normal coordinates at the tested point, `partial G=0`, so the quadratic term disappears there. No global normal coordinate or simultaneous normalization of several metrics is assumed.

For `psi=sum |z_i|^2+a|z_1|^4`, the metric is diagonal with first entry `1+4a|z_1|^2`. It is positive in a sufficiently small neighborhood for every real a, and its first metric derivatives vanish at the origin. Therefore `R_(1 bar1 1 bar1)(0)=-4a`. In complex dimension one the full Gaussian formula is `-8a/(1+4a|z|^2)^3`, agreeing with `K=2H`. The metric `h=exp(-psi)` on a holomorphic line bundle has positive Chern form proportional to `i partial partial_bar psi` regardless of the sign of a. These facts prove the claimed failure of the implication from positive line curvature to negative tangent-metric curvature.

PTT's explicit §4 potential formulas have stated moduli-space and sign conventions, including their genus-zero setting; they must not be read as a computed full fourth-order curvature tensor in every genus. General local existence of Kähler potentials also supplies no fourth-jet bound. [PTT](https://arxiv.org/abs/1508.02102)

**Approach 3 outcome:** the criterion and countermodel are correct. Positivity of determinant/tautological line-bundle Chern forms does not resolve the metric Riemann-curvature question. The required fourth-order inequalities for actual TZ potentials remain unproved.

## 7. Degeneration, oscillation, and completeness

For `lambda=C/(r^2 L^p)`, `L=-log r`, radial differentiation gives `Delta_0 F(L)=F''(L)/r^2`. Since `log lambda=log C+2L-p log L`, its L-second derivative is `p/L^2`. This proves Gaussian curvature `-p L^(p-2)/(2C)`. Radial length is `sqrt(C) integral_L0^infinity L^(-p/2) dL`, finite exactly for `p>2`, with value `sqrt(C)L0^(1-p/2)/(p/2-1)`. Independent controls include the divergent endpoints p=1 and p=2 as well as convergent p=3,4,6.

For p=4 and `h=sin(L^3)/L`, direct differentiation gives

    h'' = (2/L^3-9L^3) sin(L^3).

The cosine terms cancel. Although `exp(h)` tends to one, it gives curvature proportional to the negative of `4/L^2+h''`. At the sine +1 subsequence this bracket is at most `-3L^3` for `L>=1`. At the sine −1 subsequence it is at least `2/L^2+9L^3`. Both signs therefore occur arbitrarily near the puncture. Positivity and smoothness of the metric hold throughout the punctured disk; no extension across zero is asserted. This is a valid countermodel to differentiating a C0 asymptotic, not a finite-type TZ example.

If instead `lambda/lambda0 -> 1` and `Delta_0 log(lambda/lambda0)=o(1/(r^2L^2))`, substituting in the conformal formula proves `K~-2L^2/C`. The hypothesis is stronger than pointwise equivalence and is not verified for the actual full TZ metric. OTW's normal upper estimate holds for all relevant plumbing directions, but its lower comparison has a puncture-adjacency hypothesis. Thus the p=4 model must not be promoted to a universal sharp asymptotic for every boundary stratum. The packet uses it only as a model. Melrose–Zhu supplies boundary analysis, not an inspected global TZ tangent-curvature sign theorem. [OTW](https://www3.math.kyushu-u.ac.jp/~weng/otw.pdf), [Melrose–Zhu](https://arxiv.org/abs/1606.01158)

The holomorphic curve `(t,t^2)` in flat C2 has induced coefficient `1+4|t|^2` and Gaussian curvature `-8/(1+4|t|^2)^3`. Ambient curvature is zero. This checks the Kähler Gauss-equation sign: intrinsic holomorphic curvature is the ambient contribution minus a nonnegative second-fundamental-form term, with consistent normalization. Therefore negative intrinsic slice curvature supplies no negative upper bound on ambient holomorphic sectional curvature. Mixed directions, inverse-metric estimates, and second-fundamental-form estimates genuinely remain necessary.

The actual incompleteness deduction uses only the verified OTW upper estimate `C_epsilon/(r^2L^(4-epsilon))`. Choose `0<epsilon<2`; its square-root radial integral converges. The resulting curve has tails of arbitrarily small length and hence yields a Cauchy sequence, while its degeneration has no limit in the smooth moduli or Teichmüller interior. A smooth positive Riemannian metric induces the manifold topology there, so an interior metric limit cannot supply the missing boundary point. This proves incompleteness without making any sign inference. Lifting the plumbing ray to Teichmüller space gives the same conclusion.

**Approach 4 outcome:** the models, logical counterexamples, sufficient differentiated condition, and known actual incompleteness deduction are correct. No differentiated actual curvature theorem or actual TZ positive direction has been obtained.

## 8. WP ratio and Ricci identities

In one complex dimension, positive tangent metrics necessarily differ by a positive scalar. Quotienting the two defining norms gives the packet's actual weighted average `f`; replacing the spanning harmonic vector by any nonzero scalar multiple cancels in numerator and denominator. It does not provide a bound on moduli derivatives of that average.

Writing `lambda_TZ=f lambda_WP` in `K=-(2lambda)^-1 Delta_0 log lambda` gives

    K_TZ = f^-1 (K_WP - (1/2) Delta_WP log f).

Thus strict negativity is equivalent to `Delta_WP log f > 2K_WP`. In particular the right-hand threshold is negative when WP curvature is negative; the criterion does not require the stronger condition `Delta_WP log f>=0`. The factor 1/2, strict inequality, and sign are correct. Generic factors `exp(a|z|^2)` alter the origin curvature by `-2a/lambda_WP(0)` and can give either sign. Even local two-sided zeroth-order comparison can coexist with arbitrarily prescribed second jets on a small enough neighborhood. None of these generic factors is claimed to equal the actual TZ ratio.

For higher-dimensional matrices, `A=W^-1 G` is not generally Hermitian in the coordinate Euclidean metric, but it is similar to `W^-1/2 G W^-1/2`, which is positive Hermitian. Consequently its determinant is positive. The quotient of the two metric determinants is a genuine positive coordinate-independent scalar, so the real logarithm is well-defined. Applying `-partial partial_bar` to `det G=det W det A` proves the Ricci identity. Differentiating the inverse matrix gives the Hessian formula with both the second-derivative trace term and the subtracted noncommuting quadratic term. The trace's cyclic property is sufficient; commutativity is not assumed. The independent complex two-jet control gives Hessian `11/20` and checks the determinant comparison after differentiation, rather than merely checking determinant products at a point.

**Approach 5 outcome:** both identities are valid, including the actual one-dimensional formula. No bound on the Hessian of the actual ratio or determinant ratio has been proved. Neither dimension-one case `(g,n)=(1,1)` or `(0,4)` is solved, and a hypothetical Ricci result alone would not settle all stronger target interpretations.

## 9. Independent controls and their limits

`independent_controls.py` produces `INDEPENDENT_RESULTS.json`. The 23 named check groups comprise exact input binding and byte preservation, separately labeled replay of the original eleven controls, independently authored exact identities, explicit model/negative controls, and one supplementary high-precision infinite-series quadrature. The quadrature is not represented as an exact proof or a finite-type surface calculation. It tests the model `q=exp(2 pi i z)/(1-exp(2 pi i z))`, whose strip norm equals `3*zeta(5)/(128*pi^5)` by the same independently justified nonnegative series argument. At 70 digits the reported relative discrepancy is below `10^-60`.

Eight deliberate mathematical errors are rejected: the Fourier coefficient multiplied by four under the unchanged convention; the wrong inverse-power weight; the wrong sum-defect sign; a missing Gaussian factor of one half; the reversed potential curvature sign; the reversed slice sign; a wrong conformal factor of one half; and omission of the inverse-metric quadratic term from the determinant Hessian. Complex-Hermitian controls prevent real-transpose tests from hiding a conjugation error. Equality controls prevent a strictly-positive-defect claim where only nonnegativity holds.

The original eleven controls and all independent checks pass under Python 3.12.14, SymPy 1.14.0, and mpmath 1.3.0. The proofs above, not finite samples or symbolic simplifier success, establish the general statements. No function in either script constructs a finite-type hyperbolic surface, varies its harmonic representatives, or evaluates the actual TZ Riemann tensor. No numerical result certifies the original sign question.

## 10. Source verification and limits

All six PDFs named in the frozen metadata were independently downloaded over their public source URLs during this audit. Each returned HTTP 200 and exactly matched the frozen byte count and SHA-256. The matched files and the precise inspection scope are recorded in `SOURCE_AUDIT.json`. The original OWR target, OTW definitions and normal bound, PTT metric/potential statements, Teo's special universal statement, and Teo 2024 Fourier formula were inspected directly; Melrose–Zhu's introduction and TZ boundary section were inspected to delimit its use. This is selective relevant-source inspection, not a certification of all proofs in those papers.

Three independent bounded searches concerned TZ negative curvature, TZ curvature in 2026, and TZ sectional curvature. They did not locate a complete answer in the inspected primary sources. Search results about hyperbolic fiber curvature, Liouville accessory parameters, universal WP curvature, analytic torsion, and Quillen/determinant Chern curvature are not substitutes for a theorem about the finite-type TZ tangent metric. Historical statements of an open problem are historical evidence only. No exhaustive current-literature or duplicate-work claim is made.

The frozen repository observations are explicitly time-bounded. This audit did not repeat them or obtain the missing raw upstream statement/report corpora, and it does not certify historical absence of other work. Frozen `SOURCE_VERIFICATION.json` accurately discloses those limits. Likewise a locally checked PDF hash says which bytes were inspected; it does not establish the provenance of an unavailable upstream dataset record.

## 11. Disposition

The five approach families are mathematically substantive and end at independently identified missing derivative/sign estimates. The submitted treatment is honest about those gaps and avoids the major false inferences tested here. With C1 and C2 controlling its wording, it supports an **unsolved 5/5 research record with rigorous partial reductions**. It supports neither a solved classification nor a statement that the question is conclusively still open in the literature. No extra approach, actual sign computation, or permission for remote publication is supplied by this audit.
