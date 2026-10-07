# Independent complete-packet review 01

Reviewed packet: `reviews/package_v1`, frozen inventory timestamp
2026-10-07T04:33:08.270210+00:00. Review completed 2026-10-07 UTC.
Assigned review completion estimate: **100%**. This percentage measures the
assigned review, not a probability of theorem correctness or a new estimate
for the parent project's discovery goal.

## Verdict

**No substantive mathematical defect was found in this full-packet review.**
The fixed finite-species ordinary proof is consistent with the stated initial
class and with the actual pinned primary proof. I found no sign/mass error,
unsupported aggregate-flow reduction, circular use of enhanced occupation,
uncontrolled bootstrap constant, lost logarithm, or counterexample among the
specified boundary cases. The local/continuation mechanism matches the
nonneutral `C_b^infinity intersect L^2` field class.

There is **one low-severity packaging issue**: several source-kit cross
references retain old local filenames absent from the archive, and one
continuation reference points to a nonexistent Section 9. This does not
undermine the available proof, but should be cleaned up in the next packet.
The verdict is `PASS_WITH_MINOR_NOTES`, not permission to upload or publish.
The candidate/pending-review language is appropriate for v1 and was not counted
as an objection. The absence of a reproduced Lean build is correctly disclosed
and is not used as mathematical certification.

This conclusion is an ordinary mathematical audit, not a formal proof or a
claim of exhaustive literature priority. No external individual was contacted;
no manuscript, frozen packet, Git state, release, deposit, or tracker was
modified. All review artifacts were written in this review's own directory.

## Scope actually reviewed

I read the frozen main manuscript, all four proof supplements, dependency
ledger, formal-scope/build disclosures, priority audit/search log,
primary-source provenance, both READMEs, reproduction instructions, license,
bibliography, inventory and intended Zenodo manifest. I reviewed the code of
all three Python certificates and ran frozen-byte copies independently.

I read the **actual primary mathematical proof** at the pinned commit,
including `introduction.tex`, `setup.tex`, `retarded.tex`, `occupation.tex`,
`direct.tex`, `cancellation.tex`, `direction.tex`, `selection.tex`,
`closure.tex`, and the local/persistence/localization/continuation arguments in
`continuation.tex`. These were not replaced by favorable summaries or theorem
headlines. The corresponding main source and figures were inventoried by hash.

An independent child audit read the actual occupation, direct, cancellation,
direction and selection proofs from scratch and checked the transferred
constants and scalar exponent/summation deductions. Its report is
`selection_audit.md`. That report has a conditional input boundary; the force,
energy, boundary and continuation inputs excluded from that narrower role
were checked in this complete review.

For established continuation machinery, I read the local primary
Bouchut--Golse--Pallard PDF text through Lemma 3.1 and Sections 4--5,
particularly (4.7)--(4.11), (5.1)--(5.12); I read Luk--Strain's exact
Theorem 1.1, Footnote 1 and Remark 1.2. Glassey's printed pp.140 and 159 and
Glassey--Schaeffer's printed pp.354 and 355 were also visually inspected,
including formulas. I did not independently reprove the full prior literature,
audit every Lean proof body, or reproduce Lean/comparator certification.

For the PDF, I inspected all ten page images, metadata and extracted text.
A clean independent Tectonic 0.17.0 build succeeds; all ten rendered page
images and the extracted text are identical to the frozen PDF. The PDF binary
hash changes on rebuild, consistent with generated metadata; no mathematical
or visible discrepancy was found. The archived source kit contains exactly
the frozen source/verification files, byte for byte.

## 1. Exact target, quantifiers and field class

The candidate's target is fixed `N>=1`, each `m_a>0`, each real `e_a`, and
nonnegative smooth compact phase-space initial number densities. The fields
are compatible `C_b^infinity intersect L^2`, with all spatial derivatives
bounded. This is more precise than arbitrary smooth finite-energy fields.
The physical-to-normalized density and momentum transformation is invertible
for every fixed positive mass, so physical smooth compact phase data are
equivalent to the normalized data in the theorem.

The conclusion is unique global classical existence in the specified class,
smoothness on every finite slab, a common compact phase-support bound on each
finite slab, preserved constraints, and a momentum-only continuation criterion
at a finite maximal endpoint. No massless limit, infinite family, momentum
tail, collision, curved-space, neutrality, or uniform parameter assertion is
made. Constants may grow with the fixed species list and horizon. These
quantifiers agree in the main manuscript, packet README and deposit metadata.

The compact-prefix support condition is not inferred from energy. It first
comes from local characteristics and is part of the a priori proof setting;
the uniform momentum estimate and continuation then prevent a finite maximal
endpoint. Thus I found no circular premise that already assumes the desired
global support bound.

## 2. Normalization, signs, energy and constraints

The transformation is

`v=p/m_a`, `f_a(t,x,v)=m_a^3 F_a(t,x,m_a v)`,
`q=sqrt(1+|v|^2)`, `u=v/q`, `lambda_a=e_a/m_a`.

The Jacobian is `dp=m_a^3 dv`, so `f_a dv=F_a dp`. Charge and current are
`sum e_a integral (1,u) f_a`; no extra source mass belongs there. The
normalized acceleration is `lambda_a(E+u cross B)`.

The phase divergence vanishes because `u=grad_v q`, hence
`div_v(u cross B)=0`. Each species has its own volume-preserving flow and
conserved nonnegative density, number and `L^infinity` cap. Summed continuity
gives `rho_t+div j=0`, so both Maxwell constraints propagate with every
charge sign.

The positive kinetic energy is `sum m_a integral q f_a`. Work from species
`a` is `m_a lambda_a E dot integral u f_a = e_a E dot integral u f_a`,
which exactly cancels the signed Maxwell work. The cone flux is

`U-n dot S = (|E+n cross B|^2+|n dot B|^2)/2
             + sum m_b integral q(1-n dot u) f_b`.

The plus sign in `E+n cross B` agrees with the outward normal `-n` of the
shrinking backward-cone ball. Thus the good-field and each positive species
particle-flux budget have the claimed signs and `H_0/m_b` dependence. Spatial
cutoffs and the independently established `C_t L^2` field class justify the
global energy identity without requiring square-integrable field derivatives.

I specifically rejected the tempting signed aggregate density as an energy
measure. The proof instead uses `f_* = sum f_b >=0` and its disjoint species
label spaces. It never assumes a scalar Vlasov equation for `f_*`.

## 3. Retarded force, pair identity and boundary terms

Linearity of the Maxwell potentials gives source multiplier `e_b/(4 pi)`.
The receiver multiplies force by `lambda_a`, so the complete pair factor is

`c_ab=lambda_a e_b=e_a e_b/m_a`.

The source acceleration inside the electric kernel is
`b_b=lambda_b q_b^(-1)(Id-u_b tensor u_b)(E+u_b cross B)`.
Consequently direct source-field and source-cutoff majorants carry
`|c_ab lambda_b|`, while transport and geometric terms carry `|c_ab|`.
Using `lambda_a lambda_b` for the pair factor would omit `m_b`; that error is
not present here.

The retarded inverse-flow determinant is `d=1-n dot u_b>0`. Together with
`dt/ds=d/D`, it gives `ds f_b0 dz = D dt f_b dy dv`. Both identities are
kinematic and hold separately for differently accelerated species. Collision
labels have zero source mass by the time-grid `O(zeta^2)` bound on a compact
prefix; exact coinciding trajectories or a self-label do not invalidate
integration over a smooth phase distribution.

I checked the primary potential differentiation, electric/magnetic kernels,
initial boundary sign, and initial time derivative. In particular the
potential part contributes the initial electric derivative `-j_0`, so the
homogeneous wave data are `(E_0,curl B_0)` and `(B_0,-curl E_0)` as in the
actual source. This avoids incorrectly declaring those two homogeneous waves
a joint vacuum Maxwell solution when the initial electric divergence is
nonzero.

The complete branch-measure kernel includes the transport term. The signed
identity is obtained by differentiating `k_0/(r d)` with
`k_0=u_b-(1-a dot u_b)n/D`; source accelerations cancel before their sign is
discarded. The geometric identities use only `|u_b|^2=1-q_b^-2` and
`|a|^2=1-q_X^-2`. The residual in receiver measure is
`c_ab f_b n(a_t dot k_0)/(r D)`, with
`a_t=q_X^-1(Id-a tensor a)K_a`. Here `K_a` is the full normalized receiver
force, so no second receiver charge factor is introduced.

The source/angular/radial cutoff derivatives, moving-projector derivative,
time-weight derivative and central residual have the claimed pointwise
majorants. The selected partition is differentiated only after factoring out
the common pair multiplier. It does not cancel different signed kernels.
The initial-cone coefficient has bounded initial `d_0` and bounded `D k_0`;
its cost is a datum/horizon constant times the time-weight integral. Cone-tip
cutoffs have `O_prefix(gamma)` errors, used only to justify identities before
removal; those prefix constants never enter the uniform estimates.

## 4. Occupation, direct bounds and logarithmic accounting

The spatial hit map at fixed source time is injective with Jacobian `r^2 D`.
This yields both the crude energy hit bound and the source-label residence
interpretation. A bin density has cap `C p^3 nu^2`; the allowed cone normals
have cap area `C phi^2`. These estimates hold for each species and for the
positive aggregate.

The stability length uses the simultaneous signed bootstrap for both the
source and the receiver. The first-exit stopping argument makes their energies
comparable before integrating `||D_v u||<=1/q`; thus no equality of
accelerations is assumed. Actual bins have a fixed monotone relative-velocity
projection, and the positive mass at a common cell time is `O(1/p)` after
summing species. The two angular energy indicators retain bounded overlap
and a unique retarded receiver time. Their joint budget is independent of
`theta,h,M,A`, including the clipped-cell treatment. Deficit bins retain
their explicit exception and are estimated directly.

I checked the actual near/far table and radial balances. The small-sector
transport term retains the joint `(p,phi)` energy budget. The squared
Cauchy--Schwarz sums are `O(L^2+L(P/w)^2)` and `O(L+(P/w)^2)` for its `M`
and `sqrt(A L)` parts; no extra logarithm is introduced. The remaining-sector
angular factors, magnetic `h>I` terms, and deficit near bounds are summable.
The latter have ratio `O(L^3/P)` to `I S(w)`. Fixed pair/species factors are
exterior constants and do not affect any exponent.

The resulting baseline estimate is
`C[P sqrt(I)+(M+sqrt(A)) I P^2 L/w]`; the absolute-force estimate adds exactly
`sqrt(w)`. Both constants remain independent of `M,A,P,t_*` after fixing the
datum, horizon and species parameters.

## 5. Direction occupation and selected receiver coefficient

The direction-count proof is logically before enhanced occupation. It uses
the signed bootstrap, baseline occupation, direct absolute force, and the
projected pair identity with selection `theta<kappa phi,
p theta sqrt(h)<=1`. Disjoint first-exit weights share one upper length bound;
only the weight-derivative term carries the exit count. The inequality

`N_c w delta/2 <= C(M,A) w L^6 + C L^2 N_c`

closes because `w delta>=P^(6/25)`. I found no use of enhanced occupation at
this stage. The same proof applies to any species regarded as receiver,
providing the direction control later needed for source trajectories too.

Enhanced occupation uses stable energy cells, then the **sum** of source and
receiver direction-partition counts. Bad hits have source-time duration
`O(h)` per receiver boundary. Good hits have same-time separation
`O(h phi)` and a monotone relative projection `Omega(phi)`. Their total
duration remains bounded even for a disconnected hit set. The intermediate
window supplies `phi^(-4/25)>=P^(56/3125)`, absorbing the fixed
`C(M,A)L^7` before the final selection step. The final occupation constant
is therefore independent of bootstrap parameters; only its threshold depends
on them.

Selection uses exact pure representative bounds, keeping the real occupation
constant outside their minimum. I independently rederived the unsafe-bin
implications: actual separation precedes use of stable-cell occupation,
stable-cell occupation forces the enhanced window for both momenta, and the
enhanced bound contradicts unsafety. In the final rational comparison,

`H/z > 62/125`, whereas `H/z < 37487/93500`,

with strict positive gap `8889/93500`. The selection arithmetic certificate
confirms these fractions but was not taken as proof of their analytic premises.
The two-sided coefficient bound therefore gives `C U`, with
`U<=w^-1/2 W` and summable `sum W<=C`.

The spatial-transition crossing retains `R` independent of `theta,h`. Its
radial/angle tails have positive geometric exponents and cost
`C sqrt(I) R p phi`, so no additional logarithm is spent. The source derivatives
are assigned to unselected neighbors only within their pair. Structural
neighbors and deficit exceptions are covered. For endpoint time weights,
`h<=I` is controlled by the central residual; `h>I` has positive exponents
`1-6 epsilon/(1-epsilon)` and `3-4 epsilon/(1-epsilon)`. Thus every derivative
and boundary term is included.

The selected coefficient `C w^-1/2` multiplies the full absolute-force bound
`C sqrt(w) B(I,w)`, cancelling that loss without requiring small charges.
This gives a weighted signed impulse constant independent of `M,A`.

## 6. Coupled bootstrap and momentum continuation

Endpoint ranges bound trivial long increments. For the remaining intervals,
the two monotone endpoint ramps are restored using signed increments rather
than absolute force. The order of choices is valid: choose ramp fraction,
then common `M`, then common `A`, then the common large-`P` threshold. The
displayed constants give a quarter-bound in the nontrivial case; the asserted
half-bound is weaker and valid.

Bootstrap closedness follows by interval truncation. Relative right openness
uses a temporary common compact-prefix force bound only for short suffixes.
It does not contaminate the chosen uniform constants. Finite species permit
the same margin and force bound across all supported labels.

The first joint dyadic-hit construction remains valid when different species
attain successive maxima. At the first hit of `2^n`, the selected label's last
half-energy time is at least the first joint hit of `2^(n-1)`; otherwise the
joint maximum would have crossed that threshold earlier. The harmonic
lower bound on elapsed times therefore excludes finite-time unbounded joint
normalized momentum. Fixed positive masses make this equivalent to bounded
physical momenta.

## 7. Local theory, nonneutral broad fields and uniqueness

The Sobolev construction uses one common Maxwell field, separate transport
equations, fixed momentum radius and fixed species coefficients. Its local
`H^6` bounds control first derivatives on six-dimensional phase space.
Tame higher-norm estimates have a common low-norm lifespan. The difference
energies sum all distribution components and compare the shared field once;
no signed-density positivity is needed for uniqueness.

The actual Bouchut--Golse--Pallard division lemma is purely kinematic and its
coefficients are bounded for a fixed radius `R`. Applying the first- and
second-derivative computations to each source gives the fixed `e_b`,
`lambda_b`, `lambda_b^2` and mixed force-derivative coefficients described in
the supplement. The zero angular residue controls the only remaining density
derivative with a small-radius subtraction and logarithmic split. Its
`delta`-supported term contributes only a bounded density term. This produces
the logarithmic field derivative estimate and the Osgood inequality for the
sum of species density derivative norms. No a priori signed impulse is used
by this bounded-radius continuation argument.

The literal BGP theorem's compact-field clause is not silently applied to
nonneutral data. Luk--Strain's `H^5` criterion and multispecies remark are
credited, while the supplement gives the actual finite-species derivative
adaptation. Glassey's book's printed neutrality condition is explicitly
acknowledged. I found no transfer to an equivalent or stronger unsupported
continuation claim.

For broad fields, the signed compact initial charge has Coulomb field
`E_C=-grad(-Delta)^-1 rho_0` in every `H^k`: the low-frequency singularity
is `O(|xi|^-1)`, square integrable in dimension three. The sign gives
`div E_C=rho_0`. For a divergence-free remainder `G`, the potential
`A_G=(integral_0^1 t G(tx)dt) cross x` has curl `+G`; reversing the cross
product would be wrong, but is not done. Cutting this potential off preserves
constraints and agrees with the original fields on a large ball.

The removed divergence-free part has smooth bounded-derivative, finite-energy
vacuum evolution. Mollification plus the unitary Maxwell group gives
`C_t L^2` without imposing `L^2` derivatives. Finite propagation makes it
vanish throughout `|x|<=R_0+t` when the cutoff ball exceeds `R_0+2T`.
Adding/subtracting it preserves every species force on its density support,
all Maxwell equations and constraints, and normalized momenta. This is an
exact finite-horizon equivalence. It justifies local theory, persistence and
momentum continuation in the candidate's exact field class without neutrality.

## 8. Adversarial boundary cases

* Two equal unit masses and charges `+1,-1`: the pair matrix is
  `[[1,-1],[-1,1]]`; the source-acceleration coefficient rows are `[1,1]`
  and `[-1,-1]`. Actual signed accelerations are retained until the
  kinematic cancellation. The common signed field cannot be replaced by a
  one-species aggregate theorem.
* Zero receiver charge: `K_a=0` and all its pair factors vanish. No division
  by charge occurs. Zero source charge: no field source and free transport;
  keeping its positive energy is harmless.
* One species with unit mass/charge: every displayed identity and range
  reduces to the primary source. Other fixed signed charges only alter
  exterior constants.
* Repeated/coinciding mass/charge species: identical force laws permit adding
  densities; separate labels are also valid. Coinciding trajectories are
  covered by the null source-label collision argument.
* Opposite charge reversal: reversing fields and all charges preserves
  characteristic forces and positive energy, providing an independent sign
  consistency check.
* Empty components or all zero densities: empty label integrals vanish;
  fully empty kinetic data are the global vacuum case. Nonempty neutral
  components are passive, even if all charged components vanish.
* Extreme fixed positive mass ratios and arbitrary fixed real charge sizes:
  normalization is exact; `1/m_b`, `|lambda_b|`, `|c_ab|`, initial normalized
  caps and thresholds may grow. No forbidden parameter-uniform assertion is
  required to choose common constants for a fixed finite list.
* Nonzero total charge: the initial Coulomb tail is admissible in `L^2`.
  Neither energy, occupation nor localization invokes integrated neutrality.
* Low receiver momentum and zero receiver velocity: moving projection is
  used only in the high-energy direction estimate; the final signed identity
  uses the identity projection. No hidden division by zero arises.

## 9. Priority, authorship, formal claims and metadata

The manuscript credits OpenAI's one-species large-data theorem and analytic
angular-selection machinery. The primary source indeed states one-species
scope. Prior normalization and signed source sums are present explicitly in
Glassey--Schaeffer 1988, whose actual theorem imposes small signed phase-space
`C^1` norm, small `C^2` fields and compact support; it does not duplicate the
unrestricted target. Glassey and Luk--Strain are credited for species
formulation/continuation, with their exact restrictions reconciled.

A fresh read-only GitHub API check found current main still at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`; family README equals the pinned
bytes, and family path history returned that commit alone. See
`source_receipt.json` and saved responses. Fresh web searches did not identify
an unrestricted multispecies duplicate; this is bounded evidence, not a
firstness certificate. September 23 is correctly described as a manuscript
date, not an established public disclosure date.

The actual Lean `Model.lean` and `Main.lean` contain a one-species unit-charge
model with admissibility matching the source theorem; they do not contain the
new finite-species model. I repeated the local admission-marker screen and
read those real declarations, but did not compile them or inspect the kernel
axiom closure. The packet correctly states that no formal certificate was
reproduced and that no full follow-on formalization is claimed. The Python
certificates correctly limit themselves to algebra/arithmetic.

Author name/ORCID, date, title, intended license, data class, contribution
scope, AI use, lack of human peer review and candidate status agree among the
PDF, README and intended deposit. No affiliation, coauthor, exhaustive
novelty, human-refereeing, or full Lean claim is manufactured. The intended
manifest's project-root upload paths were compared with the frozen kit and
matched at review time. Those are intentional destination paths, not a
missing-packet-path defect. The source archive contains no third-party PDF,
source clone, Lean build cache, credential, or hidden upload payload.

## 10. Only demonstrated concern: stale package navigation

Severity: **P3 / low; non-substantive packaging correction**.

Evidence in exact reviewed bytes:

* `SUPPLEMENT_TRANSFER_LEMMA.md:10,16,69` names `PAIR_IDENTITY.md`, while the
  archive supplies `SUPPLEMENT_PAIR_IDENTITY.md`.
* `SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md:3,301` names `AUDIT.md` as the fuller
  rational proof record, while no such file is in the archive. The actual
  primary `selection.tex`, main manuscript and certificate provide the
  mathematical material inspected here, so this is not a missing theorem
  premise.
* `DEPENDENCY_LEDGER.md:3,9,15,16` uses `sources/PINNED_SOURCE.json`,
  `PAIR_IDENTITY.md` and `LOCAL_THEORY.md`. The corresponding source-kit files
  are `PINNED_SOURCE.json`, `SUPPLEMENT_PAIR_IDENTITY.md` and
  `SUPPLEMENT_LOCAL_THEORY.md`. Row L additionally references Section 9,
  although the packaged local supplement's final numbered proof section is 8.
* The historical formal audit reproduction paragraph points to project-local
  `checks/formal_scope/reproduce.sh`, absent from the kit. Its scope is clearly
  a prior failed-build receipt, and the kit's `REPRODUCE.md` directs readers
  to obtain the pinned upstream sources, so this is navigation rather than a
  false certification claim.

Suggested correction: replace those local names with the packaged names and
correct the section numbers; where a historical project-local artifact is
intentionally omitted, explicitly identify it as an external-to-kit record
and give the pinned upstream alternative. No mathematical change is required
for this concern. All packet files remain untouched by this review.

## 11. Reproducibility and exact reviewed hashes

`reproduction_receipt.json` records the checked inventory, all exact code
hashes, certificate exit statuses/output, and archive comparison. All three
exit statuses are zero. `exact_kernel_certificate.py` verifies zero generic
polynomial residuals plus 292 supplementary exact rational cases;
`verify_pair_identity.py` independently verifies generic cleared-denominator
pair polynomials; `rational_selection_certificate.py` verifies the exact
rational margins and positive tail exponents. These outputs do not establish
PDE hypotheses or novelty by themselves.

`source_receipt.json` independently verifies all **235** hashes in the
packaged pinned-source catalogue with zero mismatch. It also records the fresh
remote source check. `metadata_correspondence.json` records the intended-kit
file comparison. `pdf_reproduction.json` and compiler logs record the clean
build, exact extracted-text equality and ten exact image comparisons.

The machine-readable verdict incorporates all frozen inventory file hashes,
so the review cannot silently transfer to another version. Key exact hashes:

| Reviewed file | SHA-256 |
|---|---|
| `source-and-verification/main.tex` | `64e2f3f4d7972274b29a77d7980bc9255d38d86879eff5fc2143dcb5ba9b8696` |
| `upload-kit/paper.pdf` | `91b45e243369d62a95d609f901adfe550659b27463136dd973124ff7aeeadc8a` |
| `upload-kit/source-and-verification.zip` | `bd8604219a0d2c147021f31d6c8737af4cb0298dc3a0d076ce73d1cbed7ce1da` |
| `zenodo-deposit.json` | `db57320f7afa483e9940b8ce1e3c419e50003719784007f261712bdcb6330fa3` |
| `SUPPLEMENT_PAIR_IDENTITY.md` | `2e2cc01799947bee5bd4ad3e67e4674101e6514e6bfef3b42bfe4da4b08153b4` |
| `SUPPLEMENT_TRANSFER_LEMMA.md` | `2a524884114100d7c86fd7af74e7a3eebed31141beeb47f5fe7d3a4ae5ff35ae` |
| `SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md` | `78d3472c25c57333aa5be5db380563b42c38251daceef8803b26edadb35fa0d4` |
| `SUPPLEMENT_LOCAL_THEORY.md` | `5f9914612bbccbccc2f2ee73c38a07ea646f29ab28e73d0264c86c31002693bc` |

The report's substantive conclusion applies to these reviewed bytes and the
stated ordinary-proof scope. No demonstrated central gap remains in that
scope; the only recorded unresolved issue is the minor package navigation
correction. Formal certification and exhaustive novelty remain expressly
outside the claims rather than being silently supplied by this review.
