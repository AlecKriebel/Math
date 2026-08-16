# OUTCOME:

## FLAGSHIP-READY

The final flagship paper has been reconstructed around one reaction topology and one theorem suite. The topology-wide all-spectrum theorem, the general one-bad-minor diffusion theorem, the exact network diffusion law, sharp linear contrast bounds, the improved unit-equilibrium stable design, and the equilibrium-scaled stable trade-off family all survived independent manuscript-level reconstruction and exact verification.

No former stationary-only family, high-contrast profile, reaction-minimality claim, weak-reversibility theorem, projected-injectivity theorem, or private complexity result is required by the manuscript. The result is ready for external specialist audit and author-controlled submission. It is not represented as peer reviewed, externally confirmed, or submitted.

# CENTRAL TOPOLOGY:

For every integer `m >= 3`, let `Nhat_m` have species

```text
X1, ..., Xm, Z
```

and indexed reactions

```text
R0:  0 -> X1
Ri:  X1 + Xi -> X1 + X(i+1),      2 <= i <= m-2
Ra:  X1 + X(m-1) -> 2Xm
Rb:  2Xm -> X2
R+:  2Z -> X1 + Xm
R-:  X1 + Xm -> 2Z
```

The `Ri` range is empty at `m=3`. Writing `n=m+1`, the topology has `n` species and `n+1` indexed reactions. Every source and every target complex has total molecularity at most two; this is the exact meaning of **binary-complex mass action** in the paper.

The topology has one semipositive conservation law

```text
c = (0,4,...,4,2,1)^T.
```

It is described as stoichiometric codimension one, not as conservative, closed, or mass conserving. The conserved functional does not contain `X1`.

# COMPLETE REALIZATION SPACE:

Direct reconstruction from the reaction list gives

```text
c^T Gamma_m = 0,
rank Gamma_m = m,
im Gamma_m = c^perp,
```

and

```text
ker Gamma_m
  = span{(1_m,0,0),(0_m,1,1)}.
```

Thus the complete positive steady-flux cone is

```text
{v>0 : Gamma_m v=0}
  = {(a 1_m,b,b): a>0, b>0}.
```

At a general positive equilibrium every Jacobian is exactly

```text
J_m(a,b,H) = A_m(a,b) H,
```

where `a,b>0` and `H` is positive diagonal. Conversely, every such triple is physically realized by

```text
x_i^* = h_i^{-1},
k_r = v_r/(x^*)^{y_r} > 0.
```

The universal theorem therefore quantifies over every positive-equilibrium realization of the indexed topology, not over one tuned Jacobian and not through black-box semialgebraic elimination.

# ALL-SPECTRUM LOCALIZATION:

For every `m>=3`, every `a,b>0`, every positive diagonal `H`, and every principal species set `I` with `|I|<m`, the block

```text
J_m(a,b,H)[I,I]
```

is Hurwitz.

The exhaustive strongly connected diagonal blocks of every such principal matrix are:

1. the long cycle on `X1,...,X(m-1)`;
2. the long cycle on `X2,...,Xm`;
3. a principal block of the boundary triad `{X1,Xm,Z}`;
4. a negative singleton.

The two long cycles satisfy strict right-half-plane product inequalities. The full boundary triad has characteristic polynomial

```text
lambda^3 + c1 lambda^2 + c2 lambda + c3
```

with

```text
c1 = a h1 + 4a hm + b h1 + b hm + 4b hZ,
c2 = a(4a h1 hm + 7b h1 hm + 4b h1 hZ + 16b hm hZ),
c3 = 16a^2 b h1 hm hZ,
```

and `c1 c2-c3` is a sum of fourteen strictly positive monomials. The case `b=2a`, where one graph edge vanishes, only refines the Frobenius decomposition.

For

```text
C_m = {X1,...,Xm},
```

one has

```text
(-1)^m det J[C_m,C_m]
  = -2 a^(m-1) b product_i h_i < 0.
```

Hence this order-`m` block has a positive real eigenvalue. Throughout every positive realization,

```text
min{|I| : alpha(J[I,I])>0} = m = n-1.
```

Every smaller block is Hurwitz, excluding both positive-real and complex-pair instability below the largest possible proper order.

# GENERAL DIFFUSION THEOREM:

Let a real `n x n` matrix `J` have one semisimple zero eigenvalue and otherwise stable spectrum. Assume every principal block of order at most `n-2` is Hurwitz and at most one signed principal minor of order `n-1` is negative. For `D>0` diagonal,

```text
p_D(s)=det(sD-J)
      =s(beta_1+beta_2 s+...+beta_n s^(n-1)),
```

with `beta_k>0` for every `k>=2`.

A nonzero stationary threshold exists on the ray `sD` if and only if

```text
beta_1(D)<0.
```

When it exists, the threshold `s_*` is unique and algebraically simple. Moreover,

```text
J-sD has a positive real eigenvalue
  iff 0<s<s_*.
```

The stronger band statement follows from strict monotonicity of

```text
lambda -> det(lambda I+sD-J)
```

on `lambda>=0`; the total order-`(n-1)` derivative contribution is the positive linear coefficient of `det(lambda I-J)`. The theorem does not exclude a nonreal wave instability outside the positive-real band.

# EXACT NETWORK DESIGN LAW:

The complete signed order-`m=n-1` omission table is

```text
omit Z:
  (-1)^m det J_hatZ
    = -2 a^(m-1) b product_{i=1}^m h_i;

omit interior X_j, 2<=j<=m-1:
  (-1)^m det J_hatXj
    = 16 a^(m-1) b h_Z product_{i!=j} h_i;

omit X1 or Xm:
  determinant = 0.
```

Consequently

```text
beta_1(D)
 = 2 a^(m-1) b product_i h_i
   [8 h_Z sum_{j=2}^{m-1} d_j/h_j - d_Z].
```

For every homogeneously stable realization,

```text
a stationary zero crossing occurs on the ray sD
iff
d_Z > 8 h_Z sum_{j=2}^{m-1} d_j/h_j.
```

The same sign is obtained independently from perturbation of the conservation eigenvalue. The coefficient eight is the exact ratio `16/2` between the positive interior-omission weights and the magnitude of the unique negative `Z`-omission weight.

# CONTRAST OPTIMALITY:

Define

```text
T(H)=8 h_Z sum_{j=2}^{m-1} 1/h_j,
chi_D=d_max/d_min,
chi_H=h_max/h_min=x_max^*/x_min^*.
```

For fixed `H`,

```text
inf{chi_D : D satisfies the stationary criterion}=T(H).
```

The infimum is not attained because the criterion is strict. At the unit equilibrium,

```text
inf chi_D = 8(m-2).
```

Every stationary crossing satisfies the universal strict product bound

```text
chi_D chi_H > 8(m-2).
```

The product lower bound is sharp as an infimum over stable realizations. Equal diffusion cannot destabilize because it shifts the nonzero homogeneous spectrum and conservation zero strictly left.

# UNIT-EQUILIBRIUM STABLE DESIGN:

At

```text
a=b=1,
H=I,
x^*=1,
```

put `K_i=91m-181-i` and use

```text
d1 = 23/63,
d_i = 1/K_i,       2<=i<=m-1,
d_m = 1/7,
d_Z = 16/45.
```

The exact contrast is

```text
chi_D(m)=23(91m-183)/63.
```

An exact critical vector satisfies `(A_m-D_m)r=0`. A 35-term homogeneous right-half-plane certificate and a 77-term spatial certificate prove:

- homogeneous stability on `c^perp`;
- one algebraically simple zero in the first nonzero Neumann mode;
- stability of every other first-mode eigenvalue;
- stability of every higher mode;
- no simultaneous complex crossing;
- transversality with `eta_m>0`.

The conservation-gauged stable-mode equations are

```text
A_m w_0 = -(1/4)B(r,r),     c^T w_0=0,
(A_m-4D_m)w_2 = -(1/4)B(r,r).
```

The exact normal form is

```text
dA/dt = eta_m mu A + c_m A^3
        + O(|A|^5+|A|^3|mu|+|A||mu|^2),
```

with

```text
c_m = ell^T[B(r,w_0)+(1/2)B(r,w_2)]/(ell^T r).
```

A four-factor chain recurrence and shifted-positive polynomial certificate prove `c_m<0` for every `m>=3`. Therefore

```text
8(m-2) <= chi_stable(m) <= 23(91m-183)/63.
```

The exact unit-equilibrium stable infimum remains open.

# STABLE TRADE-OFF FAMILY:

Let

```text
r=m-2,
L_0=1/sqrt(3r),
L_1=90r/(90r+1).
```

For any `L in [L_0,L_1]`, set

```text
h1=h_m=h_Z=1,
h_i=K_i/(L K_(i-1)),       2<=i<=m-1,
H_m(L)=diag(h),
D_phys(L)=H_m(L) Delta_m,
x^*=H_m(L)^(-1) 1,
```

where `Delta_m` is the improved unit-equilibrium effective diffusion profile. Positive rates are chosen to give unit reaction flux.

For every certified `L`, a 34-term homogeneous certificate, an 84-term spatial certificate, and a gauge-corrected cubic comparison prove a primary simple transverse stationary crossing, a negative cubic coefficient, and positive locally exponentially stable patterned branches.

The exact physical contrasts are

```text
chi_D(L) = (23/63) 91rL,
chi_H(L) = (91r-1)/(91rL),
chi_D(L) chi_H(L) = 23(91r-1)/63.
```

At the square-root-balanced endpoint `L=L_0`,

```text
chi_D = [2093/(63 sqrt(3))] sqrt(r),
chi_H = sqrt(3r) (91r-1)/(91r).
```

# EXPONENT OPTIMALITY:

The universal product bound implies

```text
max(chi_D,chi_H) > sqrt(8(m-2)).
```

The certified stable family has

```text
chi_D = Theta(sqrt(m)),
chi_H = Theta(sqrt(m)).
```

Thus exponent `1/2` is globally optimal when diffusion and equilibrium heterogeneity are controlled simultaneously. The theorem does not claim optimal constants or the complete global Pareto frontier.

# NONLINEAR FRONTIER:

For the canonical near-threshold path at `m=3`,

```text
c_3(epsilon)
 = 6/1379
   + (421985/11409846) epsilon
   + O(epsilon^2),
```

and exact rational remainder bounds give

```text
c_3(epsilon)>0
for 0<epsilon<=10^(-3).
```

This rigorously shows that approaching the sharp linear threshold does not automatically preserve supercriticality. It is not promoted to a universal nonlinear gap.

The manuscript states three open problems:

1. determine whether `chi_stable(m)=8(m-2)` as an infimum at unit equilibrium;
2. determine whether stable supercritical patterns require a strict nonlinear contrast gap;
3. determine the constant-optimal stable diffusion-equilibrium frontier.

# PDE STABILITY:

The bifurcation is formulated on the real fixed-integrated-mass phase space

```text
H_c^1
 = {u in H^1((0,pi);R^(m+1)) : integral c^T u = 0},
```

with Neumann `H^2` operator domain. Positive diagonal Neumann diffusion is sectorial and generates an analytic semigroup. In one dimension, `H^1` is a Banach algebra and the quadratic mass-action Nemytskii map is smooth into `L^2`.

The fixed-mass restriction removes the homogeneous conservation zero, and the Neumann interval has no continuous translation-generated neutral mode. The center eigenvalue on either supercritical branch is

```text
-2 eta_m mu + O(mu^2) < 0,
```

while the complementary spectral gap persists. For every fixed `m` and certified `L`, sufficiently close nonnegative initial data in the same integrated conservation class generate forward-global solutions that converge exponentially in `H^1` to the selected patterned equilibrium.

This is a local-in-phase-space conclusion. No arbitrary-data global existence, global attraction, explicit basin, far-from-onset persistence, or dimension-uniform radius is asserted.

# PRIOR FEEDBACK:

Applied:

- one central all-spectrum topology;
- exact diffusion design and visible omission table;
- sharp strict-infimum language;
- semipositive rather than conservative terminology;
- improved diffusion profile replacing the coefficient-1589 profile;
- exponent-only Pareto optimality;
- main-text visibility of the SCC, diffusion, mode, and cubic proof architectures;
- full symbolic certificate tables and exact verification command;
- precise local exponential stability statement;
- retuned codimension-one robustness;
- literal reference, DOI, cross-reference, and figure audits.

Removed as obsolete or inapplicable:

- the former full-rank stationary-only family as a competing theorem;
- minimum-reaction and reaction-subnetwork-minimality claims;
- no-bounded-catalog corollaries;
- the old high-contrast profile and 49-term certificate;
- weak-reversibility obstruction as a central theorem;
- projected-injectivity sharpness;
- private T-ALG claims;
- constant-optimal Pareto language.

# LITERATURE:

The manuscript anchors principal-subsystem order to Satnoianu-Menzinger-Maini and Anma-Sakamoto-Yoneda, while explicitly stating that order `n-1` for arbitrary fixed matrices is not new. It distinguishes the flagship theorem from:

- Mincheva-Craciun projected-network injectivity;
- interaction-topology and finite atlas studies;
- fixed-J stationary and wave criteria;
- parameter-rich unstable-core theory;
- minimal two-species reaction schemes and their weakly nonlinear analysis;
- selected biochemical network screens;
- monomial-steady-state sufficient conditions;
- results showing that linear Turing instability alone need not yield persistent patterns.

The claimed distinction is the conjunction of one indexed binary-complex classical mass-action topology, every positive realization, every smaller principal block Hurwitz, order-`n-1` instability, exact diffusion design, sharp heterogeneity lower bounds, and stable nonlinear branches in every dimension.

Every bibliography entry was checked against a DOI, publisher page, or primary preprint. Detailed priority-screen limitations remain in private audit files rather than manuscript prose. External specialists and referees remain the appropriate arbiters of novelty.

# MANUSCRIPT:

Final title:

> **Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks**
>
> *Exact Diffusion Design and Exponent-Optimal Heterogeneity Trade-Offs*

Current deliverables:

```text
Abstract:              203 words
Main manuscript:        14 pages
Technical supplement:   11 pages
Theorem summary:         2 pages
Proof skeleton:          5 pages
```

Paths:

```text
/mnt/data/qbio_mass_action_turing_final_flagship/manuscript/main.pdf
/mnt/data/qbio_mass_action_turing_final_flagship/manuscript/supplement.pdf
```

The main paper contains three principal figures: the reaction topology, the exact diffusion-equilibrium trade-off, and stable patterned-profile illustrations.

# REPRODUCIBILITY:

Full command:

```bash
cd /mnt/data/qbio_mass_action_turing_final_flagship
bash release/one_command_replay.sh
```

Portable command:

```bash
cd public/repository
bash replay.sh
```

The replay verifies the four frozen source archives; runs unit and mutation tests; checks the topology-wide, one-bad-minor, omission, diffusion, contrast, improved-profile, Pareto, cubic, and branch-stability certificates; regenerates exact `m=3,4,5,6,8,10` instances; rebuilds printed coefficient tables, simulations, figures, manuscripts, specialist packets, and submission bundles; performs clean-copy replay and PDF/font audits; and verifies the final SHA-256 manifest.

All-dimensional proof objects are listed in

```text
public/repository/CERTIFICATES.md
```

and verified by

```bash
python independent_verifier/verify_symbolic_certificates.py
```

Final replay markers:

```text
ALL_FINAL_FLAGSHIP_REPLAY_CHECKS_PASS
PUBLIC_REPLAY_PASS
```

The immutable source manifest contains 755 entries. The final archive checksum is supplied in the adjacent `.zip.sha256` file.

# EXTERNAL AUDIT:

Three unsent specialist packets are prepared:

1. reaction-network and Turing localization;
2. PDE bifurcation and stability;
3. symbolic and algebraic verification.

Each packet contains the two-page theorem summary, five-page proof skeleton, network diagram, exact unit and Pareto `m=3,4` instances, targeted questions, and a minimal independent verifier.

The most failure-prone questions isolated for review are:

- SCC exhaustion, including `b=2a`;
- the one-bad-minor derivative monotonicity;
- the complete omission-minor table;
- equality cases in the 34-, 35-, 77-, and 84-term certificates;
- physical equilibrium scaling and fixed-mass gauge correction;
- the comparison `N_m(L)>1/200`;
- the semilinear linearized-stability upgrade.

Nothing has been sent automatically.

# SUBMISSION:

Prepared but not submitted:

- bioRxiv-first package, proposed category **Systems Biology**, article type **New Results**;
- arXiv fallback source, proposed primary `q-bio.MN`, secondary `q-bio.QM`, cross-list `nlin.PS`;
- journal-neutral source plus cover letters for the *Journal of Mathematical Biology*, SIADS, and *Physica D*.

The bioRxiv package includes manuscript and supplement PDFs, complete source, metadata, 203-word abstract, significance statement, data/code statements, scope note, checklist, and a factual AI-assistance disclosure marked for author approval.

No ORCID, repository URL, DOI, funding declaration, or competing-interest declaration was invented. Author confirmation remains required before submission.

# LIMITATIONS:

- The reaction family is synthetic and is not proposed as a natural biochemical mechanism.
- The system has one semipositive conservation law and an inflow; `X1` is not bounded by that law.
- All species use strictly positive diagonal diffusion.
- Immobile species, cross-diffusion, nonlocal transport, and other spatial geometries are not classified.
- The exact stable unit-equilibrium contrast infimum remains unknown.
- The globally constant-optimal diffusion-equilibrium frontier remains unknown.
- The one-bad-minor theorem controls positive-real stationary eigenvalues; arbitrary wave instability remains separate unless an explicit mode certificate is supplied.
- The nonlinear branch and robustness results are local for every fixed dimension.
- No arbitrary-data global boundedness, global attraction, explicit basin, far-from-onset persistence, or dimension-uniform stability radius is proved.
- No reaction minimality, species minimality, minimum-reaction theorem, projected-injectivity theorem, weak-reversibility theorem, or complexity theorem is claimed.
- External specialist review and peer review remain outstanding.
- The AI disclosure and final submission metadata require human approval.

# FILES:

Project root:

```text
/mnt/data/qbio_mass_action_turing_final_flagship/
```

Primary files:

```text
manuscript/main.pdf
manuscript/supplement.pdf
release/FINAL_REPORT.md
release/one_command_replay.sh
release/reproducibility.md
release/sha256_manifest.txt
```

External audit:

```text
external_audit/theorem_summary.pdf
external_audit/proof_skeleton.pdf
external_audit/packets/reaction_network_audit_packet.zip
external_audit/packets/pde_audit_packet.zip
external_audit/packets/symbolic_audit_packet.zip
```

Submission:

```text
submission/biorxiv/manuscript.pdf
submission/biorxiv/supplement.pdf
submission/biorxiv/source_package.zip
submission/arxiv/arxiv_source.zip
submission/journal/source_package.zip
submission/journal/cover_letter_JMB.md
submission/journal/cover_letter_SIADS.md
submission/journal/cover_letter_PhysicaD.md
```

Public package:

```text
public/repository/
public/data_archive/flagship_data.zip
```

Complete release archive:

```text
/mnt/data/qbio_mass_action_turing_final_flagship.zip
SHA-256: recorded in the adjacent `qbio_mass_action_turing_final_flagship.zip.sha256` file
```
