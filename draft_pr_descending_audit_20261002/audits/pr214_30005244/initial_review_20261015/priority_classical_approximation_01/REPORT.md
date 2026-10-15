# Classical approximation and DDA priority audit

Audit date: 2026-10-15. Independent initial reconstruction was saved before reading sibling priority conclusions. No sibling conclusions were read for this report. This is a source and credit audit, not an additional proof-attempt turn. No external communications or repository/index/ref mutations were performed.

## Finding

**No exact prior covering theorem was verified in this search family. This is a bounded negative search result, not a novelty certificate.** The accessible primary sources distinguish sharply between established abstract spectral approximation, smooth-field DDA consistency, static DDA stability, and the exact nonzero-frequency off-lattice-interval spectral assertion. They do not supply all those pieces as an already proved theorem for the submitted scheme.

There is a material access limitation: Rahola's full 2000 eigenvalue paper was not obtained. Its publisher abstract and first-page preview were read, and its original 1998 report identity was recovered, but current full-text endpoints failed. Vainikko's original survey and the full Chatelin/Atkinson/Sloan books or articles were also not obtained. Accordingly this report does not claim to have excluded an uninspected theorem in those works. Full primary Anselone--Palmer, Anselone--Treuden and Descloux--Nassif--Rappaz papers provide checkable substitutes for the principal abstract mechanisms.

## Exact target tested

The target is fixed complex frequency on bounded Ω; translated cubic center-membership meshes satisfying voxel measure consistency (G); off-diagonal h³ times the negative Helmholtz Hessian kernel; zero diagonal; comparison with Sκ=Aκ−I/3; and no pollution, preservation of algebraic multiplicity, and operator-norm convergence of the embedded Riesz projections outside the **exact** static lattice numerical-range interval. Every bounded Lipschitz or boundary-null particle is included. Full resolvent norm convergence is not part of the target.

The distinction matters: a field-error estimate for one physical incident wave, a material regime excluding resonances, a sphere computation, a Galerkin matrix with integrated cell entries, or a compact-operator theorem without verified DDA hypotheses would not cover this claim.

## Independently tested families

| Family | Mechanism tested | Evidence/status | Exact remaining gap |
|---|---|---|---|
| Classical collectively compact theory | Apply a spectral approximation theorem directly to the finite-rank embedded matrices | Direct application fails its compactness premise; transformed compact factors remain applicable | Verify the sampled DDA decomposition and consistency before invoking the theorem |
| Regular/stable convergence | Stable principal approximation plus compact perturbation | Established abstract framework; primary theorem/proof read | Exact DDA static strong convergence and compact approximation premises |
| Noncompact Galerkin spectral approximation | Uniform consistency on changing trial spaces | DNR requires a stronger premise than strong convergence on fixed vectors | No published verification of that premise for this matrix; scheme is not the corresponding Galerkin compression |
| Historical DDA convergence | Smooth-field truncation errors plus discrete inverse control | Yurkin consistency is proved; inverse control is explicitly assumed | Uniform stability in the desired spectral region and spectral-subspace convergence |
| Historical DDA eigenvalue studies | A direct eigenvalue convergence proof may exist | Budko--Samokhin supplies numerical comparison; Rahola full text unresolved | Full Rahola theorem/proof read remains open |
| Singular quadrature on curves / Wiener--Hopf truncation | Related noncompact quadrature theory might cover the kernel | Publisher scope checks concern one-dimensional curves or integrable kernels | Three-dimensional r⁻³ volume kernel, cubic zero-diagonal matrix, changing particle grids |

## Primary source findings and credit

### Anselone--Palmer (1968)

Full relevant theory/proofs, printed pp. 423--431, were read. Proposition 3.1 already gives the compact-multiplication lemma: a uniformly bounded strongly convergent sequence converges in norm after multiplication on the right by a compact operator. Theorem 5.3 controls spectra/resolvents under strong convergence plus collective compactness of the differences; Theorem 6.1 and Proposition 6.3 transport functional calculus and spectral projections, including eventual dimension agreement. These are established ingredients and deserve explicit credit. [Primary PDF](https://msp.org/pjm/1968/25-3/pjm-v25-n3-p02-p.pdf)

The important direct-application obstruction is mathematical, not bibliographic: Sκ is noncompact on ordinary particles, while each embedded matrix has finite rank. Consequently Sκ,h−Sκ is noncompact. A collectively compact family must consist of compact operators; thus the differences do not meet this paper's hypothesis. Proposition 2.1 makes the same obstruction transparent. Factoring by the stable static resolvents produces compact operators to which old theory applies, but that factoring still requires exact-model consistency. The adjoint argument needed for multiplication on the other side is likewise ordinary Hilbert-space duality, not a new principle.

### Anselone--Treuden (1985)

The full relevant definitions, statements and proofs in §§7--9, printed pp. 263--267, were read. Stable convergence is formulated through strong convergence and uniformly bounded inverses. Regular convergence adds the compactness condition on bounded sequences with compact image sequences. Theorem 8.1 gives inverse convergence under regularity, injectivity and eventual surjectivity; Theorem 9.1 treats collectively/asymptotically compact approximations of I−K. The introduction explicitly describes the treatment as theoretical and only indicates applications. [Primary PDF](https://msp.org/pjm/1985/120-2/pjm-v120-n2-p01-p.pdf)

This confirms the age of the proof architecture. In the candidate, the principal resolvent bound and strong convergence give stable convergence away from the interval; the compact dynamic correction then supplies the compact factor. It does not establish a prior DDA verification: neither three-dimensional dipole kernels nor this matrix/grid are an application in the source.

### Descloux--Nassif--Rappaz (1978)

The relevant §§1--3 theorem/proof chain and the start of §4 were read, printed pp. 97--109. Their P1 requires the norm of A−Ah restricted to the entire finite-dimensional trial space to tend to zero; P2 requires density of the trial spaces. Section 2 proves exclusion of pollution and convergence of spectral subspaces with algebraic multiplicity, and §3 treats selfadjoint operators. Section 4 illustrates compact and multiplication operators, then a plasma differential problem. [Primary PDF](https://www.numdam.org/article/M2AN_1978__12_2_97_0.pdf)

Strong consistency on each fixed vector does not imply P1. The candidate's zero-diagonal sampling is not the continuous Galerkin form compression. A direct invocation of this paper would therefore leave a substantial unverified premise; known static overshoot also prevents casually asserting global spectral correctness. The candidate's restricted off-interval factorization avoids that stronger demand.

### Yurkin--Maltsev--Hoekstra (2006), with 2015 erratum

The model/discretization and the relevant consistency/error argument in §§2.A--2.E were read, especially Eqs. (30), (60)--(66), (69)--(70), and (75)--(87). The original point-polarizability prescription does correspond, after sign/normalization and affine material-variable changes, to the same omitted-self-interaction scheme. It is not dismissible merely as a different numerical method. However it assumes four bounded derivatives of field and susceptibility, uses an ℓ¹/L¹ error setting, and its shape argument uses a locally planar boundary assumption. At Eq. (65) the authors expressly make discrete inverse control an assumption; Eq. (66) and subsequent field-error bounds depend on it. [Primary manuscript](https://arxiv.org/pdf/0704.0033)

The complete erratum corrects weighted-discretization and self-term formulas and leaves the other parts unchanged. It does not prove Eq. (65). [Author-hosted erratum](https://scattering.ru/papers/Yurkin%20et%20al.%20-%202015%20-%20Convergence%20of%20the%20DDA%20-%20erratum.pdf)

A tempting combination is to pair those old smooth-field residual estimates with CDN's later static bound and a density argument. That is a plausible alternate route on regular particles, and weakens any claim that the candidate invented cubic cancellation or consistency estimates. It still needs an L² extension, treatment of changing masks, a compact sampled dynamic correction, and the parameter-dependent spectral argument. For arbitrary (G)-consistent measurable sets, the old boundary argument is not a covering result. Incident-field convergence also does not supply algebraic multiplicity or norm Riesz projections by itself. For nonnormal matrices even convergence of eigenvalue sets does not control inverse norms; [[1,n],[0,1]] has fixed spectrum and unbounded inverse norms.

### Budko--Samokhin (2005 manuscript / 2006 publication)

Full relevant continuum decomposition and spectral discussion in §§2--5 and the entire numerical §6 were read. Equations (5.1)--(5.7) already separate the static strongly singular part from a weakly singular compact correction. Their continuum coefficient hypothesis is Hölder continuity throughout R³, including the outer interface. Section 6 then computes matrix eigenvalues at finitely many cubic refinement levels; the text frames their agreement and persistence as numerical observations. There is no proved mesh-limit spectral-projection or multiplicity theorem in that section. [Primary manuscript](https://arxiv.org/pdf/math-ph/0505013)

The distinction between the sharp-interface homogeneous particle and a globally Hölder transition is an additional scope limit. More importantly, continuum compactness of the correction is not a proof of norm convergence of its zero-diagonal point-sampled kernels.

### Costabel (2023), finite Hilbert transformation

Full relevant model, stability, consistency and error proofs in §§1--3 were read. The paper explicitly discusses the difficulty of transferring compact-perturbation stability to delta--delta schemes through projection or Stummel--Vainikko frameworks. Its proved model is one-dimensional. For §§3.1--3.4 it aligns the interval endpoints with cell midpoints; Theorems 3.3--3.4 concern Hölder continuous solutions and discrete/L² field errors. There is no three-dimensional dipole spectral theorem. Reference [3] identifies a nonzero-frequency DDA stability manuscript as in preparation, without supplying its result. [Primary v2](https://arxiv.org/pdf/2303.13693v2)

This is useful contemporary evidence of an acknowledged verification obstacle, not a proof that no obscure prior theorem exists. Its compact-perturbation discussion must also not be represented as saying that abstract compact-perturbation mathematics is absent.

### OWR (2022) and CDN (2023)

The complete three-page OWR contribution, pp. 2580--2582, and CDN's relevant introductory, discretization and static-theorem sections were read. OWR §4 asks for a precise description/proof of isolated nonreal eigenvalues outside the lattice accumulation interval; it does not assert such a theorem. [OWR primary report](https://publications.mfo.de/bitstream/handle/mfo/3995/OWR_2022_43.pdf?sequence=4)

CDN verifies the static infinite lattice symbol/numerical-range bound for the exact sampled matrix and accounts for overshoot. Theorem 1.6 and §§2.1, 2.4 give the uniform off-range static resolvent bound; Proposition 3.15 covers the matrix-valued Maxwell static kernel. Its introduction separates this from still-needed spectral correctness of isolated eigenvalues and nonzero-frequency work. This is indispensable existing model-specific input and must remain credited. [Primary v3](https://arxiv.org/pdf/2302.13159v3)

## Premise-by-premise priority boundary

| Needed ingredient | Verified prior credit | What this audit did not find already verified |
|---|---|---|
| Exact static lattice interval and uniform bound | CDN 2023, explicitly used by candidate | No independent-new credit is available here |
| Cubic symmetry cancellations / smooth-field quadrature estimates | Yurkin et al. 2006 | Their extension to the candidate's full L²/changing-mask setting |
| Static strong convergence under (G) | General strong convergence technology is classical | A primary prior verification for the stated sampled 3D operator and all translated (G) meshes |
| Static/dynamic compact decomposition | Classical continuum analysis; explicit in Budko--Samokhin | Norm convergence of this particular dynamic sampled correction on changing particles |
| Compact multiplication, analytic Fredholm/Riesz machinery | Classical operator/spectral approximation theory | No abstract novelty claimed or supportable |
| All exact-matrix conclusions together | No covering prior theorem verified | Off-exact-interval no pollution, algebraic multiplicities, norm Riesz projections in this full scope |

## Unresolved source risks

1. **Rahola 2000:** Full source is an unresolved access gap. Publisher abstract and p. 1740 preview concern a spherical scatterer and iterative-solver behavior. They are insufficient to claim either coverage or complete exclusion. Discovery metadata identifies original CERFACS report `TR_PA_98_19.ps.gz` and CiteSeer `10.1.1.48.3838`; all attempted current full endpoints failed. No author was contacted.
2. **Vainikko / Chatelin / Atkinson / Sloan:** Some original full sources were unavailable. Their known generality must not be confused with verified DDA premises. The accessible full classic papers do show that the abstract mechanism predates the candidate by decades. The publisher scope of Prössdorf--Sloan 1992 is quadrature plus trigonometric interpolation on smooth closed curves, not the 3D cubic volume matrix; this is a scope check, not a full theorem audit. [Publisher](https://link.springer.com/article/10.1007/BF01385525)
3. **Announced nonzero-frequency work:** A bibliographic in-preparation reference is not an inspectable theorem. Its status is a documentary risk for the parent author's later-history audit; it cannot be settled by outreach under the project policy.

## Assessment

The candidate may credibly be presented as an exact-model verification/application of established spectral approximation ideas, conditional on (G), using CDN's static result. It should not be promoted as a new compact-perturbation theorem or as the first DDA consistency analysis. The present search did not locate a source that falsifies that narrower contribution by already proving it, nor a fully documented theorem combination with every exact-model premise already verified.

This family alone does not justify an unqualified novelty claim, chiefly because Rahola's full paper remains uninspected. The strongest checkable conclusion is the credit/scope boundary above. Estimated completion of this assigned bounded audit: 90%; remaining 10% is specifically the unresolved primary-source access, not a mathematical gap found in the submitted proof. This report does not independently assess novelty of the separate arbitrary-compact-support counterexample in TURN_2.
