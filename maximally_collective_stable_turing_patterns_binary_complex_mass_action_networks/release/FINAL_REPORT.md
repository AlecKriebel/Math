# OUTCOME

## V1.0.10 RELEASE-CANDIDATE REPAIR

Version 1.0.10 repairs the independent v1.0.9 preprint referee's four bounded
findings: missing hypotheses in standalone theorem exports, unchecked ordered
certificate variables, a shifted structured literature-comparison row, and
ambiguous rational-parameter notation. It also makes document refresh rebuild
the canonical theorem exports and manuscript PDFs before packaging, preventing
source/PDF drift. No theorem in the main manuscript, reaction, endpoint,
numerical profile, or nonlinear conclusion changes. The immutable v1.0.9
source remains unchanged at exact version DOI `10.5281/zenodo.22478273`.
Current qualification evidence is recorded in `REPLAY_STATUS.md`. The v1.0.10
release passes the 39-test, 39-entrypoint, optimized-Python rejection, package,
clean-source-build, semantic-PDF, and 96-page visual campaign.
The author has confirmed that this work received no specific funding, that
there are no competing interests, and that the manuscript is not submitted to
or under consideration by another journal; the active SIADS cover letter and
declarations now record those facts.

The remainder of this report records the mathematical and numerical campaign
through v1.0.7; v1.0.8 added the pinned toolchain, preserving manifest design,
39-entrypoint fail-closed audit, all-dimensional cubic bridge, explicit
fixed-mass Fourier/Fredholm argument, and scoped output provenance described in
the status and changelog. Version 1.0.9 closed the residual reproducibility
implementation defects identified by the independent v1.0.8 rereview;
v1.0.10 closes the four precision issues identified by its independent
preprint rereview.

The numerical-provenance, theorem-scope, proof-presentation,
certificate-visibility, and release-rebuild program through v1.0.7 is
complete.  This is a
**recreated corrected release**, not a claim of byte identity with the lost
archive.  A pre-submission adversarial pass found and repaired a false endpoint
in the equilibrium-scaled family while preserving every headline conclusion.
The final source audit also removed a false, unused stoichiometric-minor value,
replacing it with rank--nullity and the exact maximal minor $4(-1)^m$; it added
the $m=3$ SCC base case, reflection-equivariant oddness, the scaled bifurcation
parameter, and a paper-visible second-harmonic boundary system.  None changes a
theorem statement or the repaired piecewise endpoint.
The release was rebuilt from the exact current diffusion profile and one
machine-readable numerical source rather than from superseded tables or figure
data.

The 22 August source pass reserves $r_m$ and $\ell_m$ for components and uses
$r=(r_1,\ldots,r_m,r_Z)^T$ and $\ell=(\ell_1,\ldots,\ell_m,\ell_Z)^T$ for
full critical vectors.  It
also makes the scaled PDE statement self-contained, renames the local S9
design parameter, and displays the scaled cubic quotient.  These are
notation/proof-exposition changes only.  The final proof-closure pass also
makes componentwise branch positivity explicit, identifies the exact
within-family contrast minimum at $L_0$, quantifies positive diagonal diffusion
in the network theorem, and separates singleton from non-singleton SCC
terminology.  Release-facing metadata targets a new immutable v1.0.7 snapshot;
v1.0.6 remains unchanged.  The v1.0.7 document,
package, submission-source, portable-replay, and manifest checks recorded in
`REPLAY_STATUS.md` are now complete.

The v1.0.7 source and package are internally validated and ready for external
specialist audit and author-controlled submission.  Neither version is
represented as peer reviewed, independently confirmed, posted as a preprint,
or submitted.

# NUMERICAL PROVENANCE

## Stale items found

The inherited Table 1 and its dependent finite-dimensional illustrations mixed the current improved diffusion profile with normal-form coefficients from the superseded profile. In particular, the displayed value near `0.1054` for the base dimension did not belong to the profile used by the final theorem.

## Exact corrected values

For the current unit-equilibrium profile at `m=3`, independent reconstruction from the indexed reactions gives

```text
ell^T r   = -7451873/924210
ell^T D r = -71818/462105
eta_3     = 143636/7451873
          = 0.0192751540451642158...

c_3       = -10077013332773/4123806134995638
          = -0.00244361955991504413...

sqrt(-eta_3/c_3)
          = sqrt(874356983548776/110847146660503)
          = 2.80854982195923431...
```

The exact values for `m=3,4,5,6,7,8,9,10` are stored in `data/current_profile_exact.json` and generated anew from the current reaction family, critical vectors, diffusion profile, conservation-gauged harmonic corrections, and cubic contraction.

## Table regeneration

`data/current_profile_exact.json` is the single source of truth for:

- Table 1;
- finite values in the manuscript and supplement;
- theorem-summary examples;
- normal-form predictions;
- simulation parameter files;
- public-repository demonstrations;
- submission-package numerical claims.

The exact table generator defines separately:

- `chi_D^unit`, the current unit-equilibrium stable-profile contrast;
- `chi_D^scale`, the diffusion contrast at the certified square-root-scaling endpoint;
- `chi_H^scale`, the equilibrium contrast there;
- their exact product;
- the topology-specific stationary square-root lower bound;
- the current `eta_m`, `c_m`, and amplitude coefficient.

The identity

```text
chi_D^unit = chi_D^scale * chi_H^scale
```

is verified algebraically for the construction.

## Figure regeneration

All numerical figures were regenerated from the corrected source. The stable-profile figure now contains a profile panel and a measured-to-predicted amplitude panel; no nonexistent “right panel” is referenced. The prediction uses the current quantity

```text
sqrt(-eta_m * mu / c_m).
```

## Simulation convergence

For `m=3,5,8`, multiple decreasing positive values of `mu` were simulated. The measured-to-predicted amplitude ratio converges monotonically toward one as `mu` decreases. Spatial and temporal refinement discrepancies are below `2e-8` in the recorded audit. These simulations remain illustrations and are not used in any proof.

A typed stale-claim audit distinguishes:

- current raw simulation values;
- deliberately retained mutation fixtures;
- claim-bearing stale values, of which none remain.

# ADVERSARIAL THEOREM REPAIR

The earlier scaled-family interval was false in high dimension.  At
`m=149`, `nu=147`, and its rational endpoint `L=1/21`, the exact homogeneous
characteristic determinant has an unstable complex pair.  The old 34-term
check proved positivity of a polynomial that was not connected by the needed
modulus inequality to that determinant.

The repair keeps the old endpoint for `nu=1` and uses

```text
L0(nu) = sqrt(5/(4nu)),  nu >= 2.
```

An exact 22-term certificate now acts directly on `QF-R`, the actual
homogeneous characteristic determinant.  The spatial 84-term certificate and
the nonlinear cubic/gauge arguments remain valid on the narrowed interval.
The endpoint contrasts still both scale as `Theta(sqrt(m))`, and their exact
product is unchanged.  An exact rational legacy-endpoint regression prevents
the disconnected certificate from returning.

# GENERAL MATRIX THEOREM

## Old hypotheses

The earlier presentation called the reusable result a one-bad-minor theorem and included a restriction on order-`n-1` minors that its proof did not consume.

## Generalized hypotheses

The corrected **principal-minor diffusion-ray theorem** assumes, in coefficient form,

```text
det J = 0,
a_I = (-1)^|I| det J[I,I] > 0 for |I| <= n-2,
sum_{|I|=n-1} a_I > 0.
```

The spectral formulation used in applications—one algebraically simple zero eigenvalue and all remaining eigenvalues in the open left half-plane—implies the final coefficient condition.

For positive diagonal `D`,

```text
p_D(s) = det(sD-J)
       = s[beta_1(D)+beta_2(D)s+...+beta_n(D)s^(n-1)],
```

with `beta_k(D)>0` for every `k>=2`.

## Proof changes

The proof now separates:

1. the principal-minor expansion;
2. positivity of every higher coefficient;
3. uniqueness and scalar simplicity of the nonzero positive dispersion root
   when `beta_1<0`;
4. strict monotonicity of `lambda -> det(lambda I+sD-J)` on `lambda>=0`;
5. the exact positive-real-eigenvalue band;
6. ordinary algebraic simplicity of the zero eigenvalue at threshold from
   `chi'_(s_*)(0)>0`, rather than from a generalized-pencil inference.

Thus, when `beta_1(D)<0`, there is one unique positive threshold
`s_*(a,b,H,D)` for the network application, and

```text
J-sD has a positive real eigenvalue
if and only if
0 < s < s_*(a,b,H,D).
```

The theorem controls stationary positive-real eigenvalues. It does not classify arbitrary oscillatory diffusion-driven instability.

## Application corollary

The reaction topology remains a genuine one-bad-minor application: omitting `Z` gives the unique negative order-`n-1` contribution, omitting an interior chain species gives a positive contribution, and omitting `X_1` or `X_m` gives zero.

# HOMOGENEOUS-STABILITY DOMAIN

For each `m`, the corrected release defines

```text
S_m = {(a,b,H): a,b>0, H positive diagonal,
       J_m(a,b,H)|_(c^perp) is Hurwitz}.
```

Every fixed-`H` diffusion and contrast theorem is stated on this domain.

Homogeneous stability implies

```text
T(H) = 8 h_Z sum_{j=2}^{m-1} 1/h_j > 1.
```

The converse is not claimed. The complete homogeneously stable equilibrium-scaling region is not characterized. The fixed-`H` contrast formula applies to every `H` in that region.

The product lower bound is described as sharp as an infimum over homogeneously stable realizations admitting a stationary crossing. No constant-optimal nonlinear stable-pattern frontier is claimed.

# ALL-SPECTRUM PROOF

## SCC cases

For every proper principal species set, every strongly connected diagonal block
is either a negative singleton or one of the following non-singleton blocks:

1. the long cycle on `X_1,...,X_(m-1)`;
2. the long cycle on `X_2,...,X_m`;
3. a principal block of `{X_1,X_m,Z}`;

The revised proof gives the full boundary-vertex and chain-segment case analysis. It explains how each long cycle closes, why proper chain segments do not create additional feedback blocks, why adding another boundary vertex to a complete long cycle requires at least `m` species, and why all remaining feedback lies in the boundary triad.

## The hypersurface `b=2a`

At `b=2a`, one Jacobian edge disappears. Deleting that edge can only refine the strongly connected decomposition; it cannot create a larger strongly connected block. All Hurwitz conclusions therefore persist.

## Cross-reference status

The previously incorrect “Theorem 3.1” reference now points to the actual SCC classification, **Lemma 3.1**. The semantic cross-reference audit verifies environment types, not merely label existence.

# OMISSION MINORS

The corrected proof presents the complete general-`m` signed order-`m=n-1` table:

```text
(-1)^m det J[omit Z]
  = -2 a^(m-1) b product_{i=1}^m h_i,

(-1)^m det J[omit X_j]
  = 16 a^(m-1) b h_Z product_{i != j} h_i,
  2 <= j <= m-1,

det J[omit X_1] = det J[omit X_m] = 0.
```

The manuscript and supplement expose the block/permutation structure, the surviving boundary determinant, the negative singleton factors, and the sign accounting. The coefficient `8` in the network diffusion law is visibly the ratio `16/2` between the interior positive and `Z`-omission negative weights.

# SYMBOLIC CERTIFICATES

The supplement prints or tabulates every certificate used in a headline claim, including:

- the fourteen-term boundary-triad Routh-Hurwitz expression;
- the corrected homogeneous certificate;
- the unit-profile 77-term spatial certificate;
- the scaled-family 22-term homogeneous and 84-term spatial certificates;
- shifted polynomial coefficient lists used in the cubic sign proofs;
- the comparison proving `N_m(L)>1/200`;
- the unique equality terms for each half-plane certificate.

Run

```bash
python independent_verifier/verify_symbolic_certificates.py
```

or, in the public package,

```bash
python independent_verifier/verify_symbolic_certificates.py
```

from the repository root. The command regenerates the exact expressions,
checks the machine-readable coefficient data from which the printed tables are
generated, verifies signs, determinant connections, and equality cases, and
exits nonzero under the prescribed endpoint, Fourier-factor, and certificate
mutations.

# STABLE UNIT DESIGN

The current unit-equilibrium profile is

```text
d_1 = 23/63,
d_i = 1/(91m-181-i),  2 <= i <= m-1,
d_m = 1/7,
d_Z = 16/45.
```

The exact contrast is

```text
chi_D^unit(m) = 23(91m-183)/63.
```

The corrected finite table contains only current-profile `eta_m`, `c_m`, and amplitude coefficients. Exact data and decimal renderings are generated automatically; no row is manually transcribed.

The 35-term homogeneous certificate, 77-term mode certificate, conservation-compatible harmonic equations, cubic telescoping identity, and shifted-positive sign proof establish for every `m>=3`:

```text
eta_m > 0,
c_m < 0,
```

The selected zero is algebraically simple by the exact identity
`Pi'_m(0)=-(163/45) ell_m^T r_m>0`; hence the critical kernel and cokernel are
one-dimensional before the fixed-mass bifurcation argument is applied.

followed by the supercritical locally exponentially asymptotically stable patterned branches in the fixed integrated-mass `H^1` phase space.

# STABLE TRADE-OFF FAMILY

Distinct notation is used throughout:

- `mathfrak h_m` for harmonic sums;
- `mathsf H_m(L)` for the equilibrium-scaling matrix;
- `rho_m` for the right homogeneous kernel vector;
- `r_m` for the critical eigenvector;
- `nu=m-2` for the dimension offset.

For `nu=1`, retain the interval

```text
L in [1/sqrt(3), 90/91].
```

For `nu>=2`, use

```text
L in [sqrt(5/(4nu)), 90nu/(90nu+1)].
```

the proof follows the complete chain:

1. physical equilibrium scaling `mathsf H_m(L)`;
2. physical diffusion `D_phys=mathsf H_m(L) Delta_m`;
3. normalized concentration coordinates;
4. mode operator `mathsf H_m(L)(A-t Delta_m)`;
5. chain-factor decomposition;
6. exact homogeneous and higher-mode certificates;
7. transformed left eigenvector and fixed-mass vector;
8. gauge correction `w_0(L)=w_0^ref+tau_m(L)rho_m`;
9. unchanged second harmonic;
10. cubic numerator `N_m(L)=N_m^ref+tau_m(L)S_m`;
11. exact bounds
   `N_m^ref>1/100`, `-1/10<S_m<0`, and `tau_m(L)<1/20`;
12. conclusion `N_m(L)>1/200`;
13. sign of the critical denominator;
14. `eta_m(L)>0`, `c_m(L)<0`;
15. exchange of stability.

The lower endpoint is therefore

```text
L_0 = 1/sqrt(3)                    if nu=1,
L_0 = sqrt(5/(4nu))                if nu>=2.
```

It is identified as a sufficient certificate boundary, not as a proved
intrinsic dynamical boundary. The endpoint is called the
**square-root-scaling endpoint**, not a balanced point with equal constants.

The theorem establishes a square-root exponent that is optimal among stationary-crossing realizations of the indexed topology. It does not establish optimal constants, a result for other topologies or arbitrary wave instability, or the complete diffusion--equilibrium Pareto frontier.

# LITERATURE FRAMING

The paper states the exact non-improvability consequence supported by the mathematics: the endpoint `n-1` in general principal unstable-subsystem localization cannot be reduced within binary-complex classical mass action, even when locally stable patterned branches are required.

The general subsystem-order range is anchored to
Satnoianu--Menzinger--Maini, the unstable-subsystem mechanism to
Anma--Sakamoto--Yoneda, and the statistical many-species diffusion-threshold
comparison to Haas--Goldstein. The manuscript does not state that any source
posed this exact result as a conjecture.

A separate paragraph compares the topology with equal-diffusion Turing-network literature. Equal diagonal diffusion cannot destabilize this topology; the exact required stationary heterogeneity is

```text
d_Z > 8 h_Z sum d_j/h_j.
```

At unit equilibrium, the contrast infimum is `8(m-2)`, while equilibrium
scaling yields the topology-wide necessary product bound for stationary
crossings

```text
chi_D chi_H > 8(m-2).
```

These are presented as topology-specific stationary results, not statements
about other topologies, arbitrary wave instability, or every pattern-forming
mechanism.

A numbered open problem asks for the exact threshold for oscillatory diffusion-driven instability and whether wave instability can occur below the sharp stationary contrast. No stationary theorem is described as a complete wave criterion.

# EDITORIAL REPAIRS

The release uses one title consistently:

> **Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks**
>
> *Topology-Wide All-Spectrum Localization and Exponent-Optimal Stationary Heterogeneity Trade-Offs*

Repairs include:

- bibliography and DOI checks;
- environment-type-aware cross-reference checking;
- final notation separation;
- defined Table 1 columns;
- corrected figure caption and panels;
- removal of stale profile names and values;
- replacement of the old theorem name;
- exact stationary-versus-wave scope;
- honest `L`-interval and optimality language;
- identical title and claims across manuscript, supplement, summaries, packets, and cover letters;
- a self-contained near-threshold affine ansatz with all induced diffusion
  formulas, checked directly from $(A_m-D)r^{\rm aff}=0$;
- the explicit equilibrium-scaled transversality numerator; and
- a nonempty-set qualifier in the localization minimum.

# MANUSCRIPT

- Final title: *Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*
- Subtitle: *Topology-Wide All-Spectrum Localization and Exponent-Optimal Stationary Heterogeneity Trade-Offs*
- Abstract: below the 250-word limits used by the planned venues
- Main manuscript: 18 pages
- Technical supplement: 18 pages
- Theorem summary: 3 pages
- Proof skeleton: 6 pages

The PDFs were rebuilt after the corrections. Final rendered-page and font audits are part of the replay.

# REPRODUCIBILITY

Full working-tree replay:

```bash
bash release/one_command_replay.sh
```

Portable public replay:

```bash
bash public/repository/replay.sh
```

The full replay emits the required markers:

```text
NUMERICAL_PROVENANCE_PASS
MATRIX_THEOREM_GENERALIZATION_PASS
STABLE_DOMAIN_SCOPE_PASS
SCC_EXHAUSTION_PASS
OMISSION_MINOR_PASS
SYMBOLIC_CERTIFICATE_VISIBILITY_PASS
TABLE_REGENERATION_PASS
FIGURE_REGENERATION_PASS
SUBMISSION_BUNDLE_FRESHNESS_PASS
ALL_FINAL_RELEASE_REPLAY_CHECKS_PASS
```

The self-contained portable replay and the exact, numerical, document, and
package checks for this repaired release are recorded in
`release/REPLAY_STATUS.md`. The five frozen historical-lineage archives are
external prerequisites for the top-level lineage stage and are not bundled;
they were unavailable in the final repair environment, so no post-repair full
lineage replay is claimed. For an ordinary third-party downloader, the
self-contained command is `cd public/repository && bash replay.sh`.

The immutable release series is indexed by the stable Zenodo concept DOI
`10.5281/zenodo.21753404`. The exact preceding v1.0.9 snapshot is archived at
version DOI `10.5281/zenodo.22478273`. The corrected source targets the distinct
v1.0.10 tag and does not misassign a not-yet-minted DOI to that new tree.

The 5 September full-referee repair additionally closes malformed-certificate
acceptance, coefficient-table overlap, two inaccurate determinant-proof
descriptions, and the formerly hard-coded $m=3$ near-threshold control. The
strengthened verifier reconstructs that control from the reactions and proves
its simple transverse onset and complementary mode stability. These repairs do
not alter a headline theorem, the reaction topology, the piecewise endpoint,
or the current-profile numerical data.

# EXTERNAL AUDIT

Updated unsent packets are provided for:

1. reaction-network and Turing localization;
2. PDE bifurcation and stability;
3. symbolic and algebraic verification.

Each packet contains the corrected theorem summary, proof skeleton, network figure, exact low-dimensional instances, targeted questions, and detached minimal verifier.

The main remaining specialist questions concern:

- the exhaustive SCC classification;
- derivative monotonicity in the generalized diffusion-ray theorem;
- the omission-minor calculation;
- equality cases in the large modulus certificates;
- the physical equilibrium-scaling and fixed-mass gauge correction;
- the cubic comparison `N_m(L)>1/200`;
- the semilinear principle-of-linearized-stability application.

Nothing was sent automatically.

# SUBMISSION

Fresh packages were rebuilt from the revised source tree for:

- bioRxiv Systems Biology / New Results;
- arXiv `q-bio.MN`, with `q-bio.QM` and `nlin.PS` metadata as an optional
  fallback;
- a maintained review bundle for a later SIAM Journal on Applied Dynamical
  Systems submission.

Each source ZIP is detached-built and integrity-tested. The SIADS review
format, keywords/MSC, supplement index, line numbering, declarations, and PDF
cover letter are present. Portal-specific metadata, final author approval, and
inspection of the publisher-generated preview remain listed in
`submission/journal/README.md`. No preprint, submission, endorsement request,
specialist inquiry, or email was sent automatically. The factual AI-assistance
disclosure remains marked for author approval.

# LIMITATIONS

- The reaction family is synthetic and is not claimed to be a natural biochemical mechanism.
- It has one semipositive conservation law; `X_1` is not bounded by that conserved functional.
- All species use strictly positive diagonal diffusion.
- The complete homogeneously stable equilibrium-scaling region is not classified.
- The exact nonlinear stable contrast infimum and constant-optimal Pareto frontier remain open.
- The general diffusion-ray theorem controls stationary positive-real eigenvalues, not arbitrary wave instability.
- Selected profiles have exact all-mode stability certificates; arbitrary diffusion vectors satisfying the stationary scalar inequality need not.
- Bifurcation, robustness, and nonlinear stability are local for each fixed dimension.
- No arbitrary-data global boundedness, global attraction, explicit basin, far-from-onset theorem, or dimension-uniform stability radius is proved.
- No projected-injectivity, weak-reversibility, biochemical, cross-diffusion, immobile-species, reaction-minimality, species-minimality, or complexity theorem is claimed.
- External human specialist review and journal peer review remain outstanding.
- Final submission metadata and the AI disclosure require human approval.

# FILES

The corrected project contains:

- `manuscript/main.pdf`;
- `manuscript/supplement.pdf`;
- `data/current_profile_exact.json`;
- `independent_verifier/`;
- `public/repository/`;
- `public/data_archive/final_release_data.zip`;
- `external_audit/packets/`;
- `submission/biorxiv/`;
- `submission/arxiv/`;
- `submission/journal/`;
- `release/one_command_replay.sh`;
- `release/REPLAY_STATUS.md`;
- `release/BUNDLE_SHA256.txt`;
- `release/reproducibility.md`;
- `release/sha256_manifest.txt`.

The tracked manifest covers the corrected project artifacts. Canonical ZIP
construction for each public, submission, and specialist bundle is part of
the repository replay; no untracked outer-release archive is claimed here.
