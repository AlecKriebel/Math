# Fresh complete-package adversarial review 1

Review completed October 6, 2026, approximately 22:32 PDT (October 7,
05:32 UTC). Reviewer: internal independent AI subagent
`complete_package_review_1`. This is an automated research review, not
human peer review or formal certification. No external individual was
contacted. No publication, Git, or reviewed-payload mutation was performed.

## Verdict on the exact frozen candidate

**One substantive reproducibility issue remains in the verification
supplement. Do not treat this exact frozen package as having a clean
complete-package verdict.** Its scoped energy report gives numerical
sample counts and precise maxima without the generating code or a saved
result artifact. The root concurrently flagged this issue; I independently
verified its location and absence from both actual archives. It is a
publication-protocol failure, rather than an identified mathematical gap.
The repair must be propagated into the supplement and reviewed afresh.

I found no substantive proof gap or counterexample in the new restriction,
transference, or convergence argument. I also reconstructed the pivotal
matrix, heat, smooth, refined-frequency, rough-error, measurable-selection,
and rank-summation steps of the pinned continuous input and found no
substantive mathematical gap in that reconstruction. Those findings are
scoped evidence, not an assumption that an upstream assertion is correct.
The note properly identifies itself as a consequence of the upstream
continuous theorem. No conclusion here overrides a new counterexample,
later correction, or substantive issue found by another reviewer.

## Exact candidate and scope actually reviewed

I started with `research/ORIGINAL_REQUEST.txt`, without a favorable verdict
being presumed, and read all of the current `main.tex`, README, theorem and
dependency ledgers, approach table, priority audit, primary priority evidence,
priority bibliography, root audit, independent restriction reconstruction,
both scoped upstream audit reports, and both supplied numerical programs
and their saved results. I inspected the actual ZIP directories, extracted
`source.zip` into my own review-assets directory, compared every archive
entry byte-for-byte with its corresponding current project file, and checked
ZIP CRCs. All entries matched, and neither archive had a bad CRC, unsafe
path, unrelated third-party source copy, or credential file.

I read the full pinned annular manuscript TeX tree: `main.tex`,
`references.bib`, and all nine sections (introduction, preliminaries,
matrix, heat, smooth, frequency, rough, completion, consequences), together
with its supplied README/citation, repository README, and `LEAN_SCOPE_082.md`.
I checked the upstream PDF's extracted front matter, theorem/variation
definition and metadata against that source. I did not visually inspect
every page of the 37-page upstream PDF; the mathematical proof audit was
conducted on the complete source. The copied source hashes were all
recomputed and matched `sources/SOURCE_HASHES.json`.

I independently read the actual read-only upstream
`lean/OAI/Analysis/TriangularHilbert/Model.lean` definition of `MainEstimate`
and `Main.lean` declaration `main_estimate`. They concern a supremum of
individual hard truncations, not full annular variation. No Lean build was
run or relied upon. The actual upstream checkout resolved to the stated
commit. The source hash ledger records exactly which annular source files
are pinned; its SHA-256 is listed below.

I read `zenodo-deposit.json`, the copied upload-kit README, payload hash
receipt and package-building allowlist. I rendered and visually inspected
all five pages of the intended deposit PDF, checked extracted formulas and
references, and inspected embedded fonts and PDF metadata. I independently
built the extracted source archive with the prescribed epoch and reran
both archived numerical programs. Details follow below. My temporary PNGs
were removed after inspection when the shared filesystem reported no free
space; the extracted PDF, extracted text and rerun JSON artifacts are
retained under `reviews/complete_package_review_1-assets/`.

The hashes below identify the frozen package, not a later repaired one.

| Reviewed file | Bytes | SHA-256 |
| --- | ---: | --- |
| `main.tex` | 14748 | `b487be2a3233d56facde9713681733e5e6d7a8539ff6d78a94cf7d7db796f10f` |
| `README.md` and `publication/upload-kit/README.md` | 4438 | `90a0fc07d0c45268a8af3831d7a84e49f339496c1c52139813a1fbedd8d50c1d` |
| `zenodo-deposit.json` | 2896 | `5cff48980a8898e552f0b1945235b3cb3a8725b295ea351fdb010d0f3e8a3845` |
| `publication/paper.pdf` and `publication/upload-kit/paper.pdf` | 79186 | `5bfcfe064052e7e23005fbb45a8c83c2d1e3188ec4ef29ff97f46ea19edd60ea` |
| `publication/upload-kit/source.zip` | 14598 | `0ddfcd59401319df2e2c68788d51ce8a138dbb8aa8e77c7155a06ea6cbea4d8e` |
| `publication/upload-kit/verification-supplement.zip` | 45664 | `7849e1f0c644b7b5deef77fe09d495ad579295a70f6e87c9472ce2e71993cf4b` |
| `sources/SOURCE_HASHES.json` | 3025 | `5f31bf5adfe971410275c0e31cfb3d5dc6d35b95ff79e4f0482b5fd60cf9b06f` |
| Pinned original `annular-variation.pdf` | 523253 | `f5857c58037fa5289f2f9fe1fe4421af11df8d9fa9b2914ba041469f1195ea31` |

The source archive contains exactly six files: `main.tex`, `README.md`,
`references.bib`, `restriction_geometry_check.py`,
`frequency_audit_computations.py`, `SOURCE_HASHES.json`. The supplement
contains exactly the sixteen paths in the package-builder supplement
allowlist, including the two audit reports, independent reduction,
ledgers, priority records and two supplied programs/results. Every one
was compared with the current file; no archive/local mismatch was found.

## Substantive issue requiring repair

**R1 — Numerical evidence in the energy audit is not reproducible from the
reviewed package.** `reviews/upstream_energy_audit.md`, line 77 in the
frozen candidate, reports a seeded NumPy computation with 5,000 cyclic
matrix triples and 15,000 neighbor comparisons, with exact largest ratios
`0.07470168193073122` and `0.707003261832278`. Neither actual ZIP supplies
that experiment's program, draws/construction specification, numerical
support threshold, software version, or result file. A seed alone does not
determine an experiment. The two supplied programs instead concern cell
geometry and finite frequency quadrature. This directly fails the original
request's requirement to reproduce all computational/numerical claims and
retain checkable artifacts. The README also describes independent
numerical reruns; that statement must be scoped accurately to what was
actually reproduced.

Repair by supplying the original exact generator, result and sufficient
numerical-method/version details, or explicitly retracting the unrecorded
sample counts/maxima and replacing them with a separately recorded
reproducible experiment. Do not relabel a new experiment as reproducing
the original maxima. Any new NumPy requirement must be reflected in the
reproduction instructions and dependency claims. The analytic matrix
proof itself is independently checkable and does not depend on these
samples; this issue does not establish failure of that proof. A new
complete-package reviewer must examine the revised exact supplement.

## Independent reconstruction and falsification of the new argument

### Signed restriction and positive area

For a point `(i+a,j+b)` with `|a|,|b|<1/16`, the fixed coordinates select
exactly row `j` of the first array and column `i` of the second. Two moving
windows indexed by `k,l` can meet only if
`|k-l|<=2h+|a-b|<3/8`, hence `k=l`. Their intersection is
`I=[-h-min(a,b),h-max(a,b)]`, with length
`ell=2h-|a-b|>=1/8` and `|s|<=3/16`. This is uniformly nondegenerate on
the entire output square of area `1/64`. There is no selection of equal
phases or a zero-area subset.

Both signs of `k` satisfy `|k+s|` between `|k|-3/16` and
`|k|+3/16`. The endpoints `rho_N=N+1/2` therefore include precisely the
whole windows with `M<|k|<=N`; the zero window is excluded. For negative
`k`, the denominator retains its negative sign. Direct integration gives
`K_k=log|k+U|-log|k+L|`, and the exact remainder identity gives

`|K_k-ell/k|/ell <= (3/13)/k^2`.

This bound uses `|k+s|>=(13/16)|k|` and does not assume the generally false
phasewise identity `K_-k=-K_k`. The appropriate reflected-phase identity
is instead `K_-k(a,b)=-K_k(-a,-b)`. The paper uses neither stronger
symmetry nor a limiting-width argument.

Disjoint radial shells of an arbitrary partition count each error term
at most once. Thus the entire error variation divided by `ell` is bounded
by `(3/13) sum_{k!=0}|A(i+k,j)B(i,j+k)|/k^2`. Hölder for each translated
product and Minkowski give norm at most `pi^2/13` times the product of
the input norms. This is a genuinely summable remainder, not an
absolute estimate of the nonsummable `1/k` main kernel.

The continuous variation dominates each list of the rational half-integer
endpoints at each output point, so no common partition is imposed.
After pointwise division by `ell`, integration over all disjoint output
boxes gives factor `8*(m_in/m_out)^(2/3)=8*4^(2/3)`. Consequently
`D_r=8*4^(2/3)C_r+pi^2/13` is correct. The finitely supported arrays
make all geometric identities unproblematic; extending the discrete
estimate beyond finite support is unnecessary for this transference.

### Arbitrary commuting systems and convergence

Fixing `M` before `L` is essential and is done. The arrays on
`Q_(L+M)` contain every entry required at indices of `Q_L`, including
all negative shifts. Commutation identifies the full finite sequence
of lattice outputs with `H_N(S^iT^j x)`, and hence identifies its
point-dependent finite maximum over partitions. Raising the discrete
norm bound to `p=3/2` yields exactly the two cube sums to power `1/2`.
Cauchy–Schwarz after integration and invariance produce

`|Q_L| ||W_M||_p^p <= D_r^p |Q_(L+M)| ||f||_3^(3/2)||g||_3^(3/2)`.

No integrability of `W_M` or convergence of orbit averages is assumed
in advance. The ratio tends to one at fixed `M`, then the finite menus
increase to the countable full variation. This requires no ergodicity,
standard probability-space model, suspension or jointly measurable flow.

The union of preimages of input exceptional sets under all finite group
words is a countable null union. With commutation modulo null sets, the
same removal of word preimages of the exceptional commutation set
ensures every needed identity on an invariant conull set. As usual,
"commuting modulo null sets" presupposes a measurable null exceptional
set where the selected map versions can fail to agree. The explicit
invertibility and measurability of inverses cover the negative words.
No uncountable family of null sets is removed.

Finite scalar `r`-variation forces Cauchy convergence: otherwise
arbitrarily late pairs separated by a fixed epsilon can be chosen in
strict order, giving variation at least `epsilon*J^(1/r)` for all `J`.
Choosing the single exponent `r=3` suffices for convergence. The bound
`sup_N|H_N|<=V^3` follows from `H_0=0`; the limit is dominated by the
same maximum. The countable tail supremum tends pointwise to zero and
is bounded by twice that `L^(3/2)` maximum. Dominated convergence of
its `3/2` power gives precisely the claimed maximal-tail norm
convergence. Norm limits preserve the complex bilinear identities.

Boundary checks included `S=T=id` (all symmetric sums vanish), `S=T`
without triviality, an identity in just one generator, zero inputs,
finite orbit systems, negative indices and nonergodic systems. None
requires a missing hypothesis. The paper does not infer one-sided
Cesaro convergence, an `r=2` bound, noncommuting generality or enlarged
input exponents.

## Adversarial audit of the inherited continuous theorem

I treated the full annular estimate as a pivotal claim requiring proof
inspection, rather than accepting its theorem label or a formalization
directory. The following reconstructs the vulnerable mechanisms.

1. **Matrices and supports.** The supported Hessian is the inverse
   Sylvester operator for `sqrt(P)`, with coefficient `3/2` and positive
   entry denominators. Order comparison follows from square-root order
   and inverse order with regularization. Joint averaging is justified
   by `(integral sqrt(T))^2<=integral T` and the inverse variational
   formula, so no false linearity of square roots is used. The mixed
   trace embedding gives `E>=Q/2`. The minimum-index multiplicity
   expansion bounds the cubic by `5D_*Q`; rotating a single edge
   preserves star costs and recovers complex phase, giving `5/3`.
   Singular Grams and changing support are explicitly treated.

2. **Heat and smooth masks.** Positive Gaussian row scaling fixes the
   kernel used for row derivatives; positive column scaling fixes the
   range used for column derivatives. The plane derivative equality is
   an integrated equality, derived by changing free coordinates. The
   neighbor comparison loses `sqrt(2)`, and the rates `(1,1.1,1.1)`
   leave strictly negative coefficients. Switch bounds depend on
   `n*n_0^2*(n_1+n_2)`, which is exactly what permits normalization
   `(n^-1/2,1,1)` and a square-root loss. The inserted window narrows
   just a row; its cost has factor `s`, canceled by `ds/s`.

3. **Refined frequency proof.** With `a=qL^2`, the dilated derivative
   window is `(L/D) derivative[g_a exp(i xi u/L)]`. For
   `theta=1/(16D^2)` and slab `2a<s<3a`, the modulated Gaussian
   average has uniformly bounded exponential prefactor and inserted
   coefficient bounded by `C(q)sqrt(theta s)`. Its Gram average has
   common support. The resulting factor is `theta s`, precisely the
   one needed to pay a refined row cost. Averaging the shifted plane
   heat adds `1-theta` to `2+theta`, giving coefficient `3`, with the
   correct sign. The residual column coefficient is `1/2` and can
   be paid by single-edge heat without dividing by `theta`.

4. **Boundary costs and frequency squares.** The covariance is
   `s[[2theta,-theta],[-theta,3]]`. Its difference from
   `4s diag(theta,1)` is positive with determinant
   `theta(2-theta)s^2`; the Gaussian normalization ratio is uniform.
   The line-maximal majorant is evaluated under a bijective lattice
   shear. The star jump contains the switching edge squared times
   the unchanged edge norm, permitting the actual pointwise
   scale/frequency square integral of coefficients to be used.
   Cubic terms use the coefficient supremum times that square
   integral. No sum of separate frequency suprema is substituted.

5. **Rough endpoints and completion.** Pairing endpoints within a
   dyadic group leaves total paired length at most one and at most
   two unpaired contributions. This bounds the grouped kernel and
   its derivative uniformly despite many jumps. Removing three
   moments with a Gaussian-weighted primitive leads to Fourier
   supremum `Cm/D` and square integral `Cm/D` for `D^3 fhat`.
   Thus `mu=D*(D^3 fhat)/sqrt(n)` satisfies both coefficient
   hypotheses, and only logarithmically many cutoff blocks occur.
   The finite cutoff error is summable; the first-moment dilation
   identity has geometrically summable coefficients. Deleting
   groups with count greater than `sqrt(n)` leaves at most
   `2sqrt(n)` such groups at each output, paid by the Gaussian
   maximal envelope.

6. **The actual pointwise supremum.** Finite step menus pass by
   rectangular approximation to measurable finite choices, with
   annuli bounded away from zero for each fixed menu. Complex
   increments are phase-linearized using a finite set of four
   phases. Finite maxima pass through smooth density using the
   finite-annulus norm bound; rational lists are then exhausted
   monotonically. The rank estimate
   `V_r<=sum_j 2^(j/r-j) S_(2^j)` yields the convergent series
   `sum_j (1+j)2^(j(1/r-1/2))` exactly when `r>2`. This verifies
   that the inherited estimate covers point-dependent partitions,
   all positive scales and unrestricted finite length, as needed.

I found no circular use of the desired triangular estimate in these
steps: initial energies use only cubed input norms, inserted costs use
the proved matrix inequalities, rough maxima use one-dimensional
maximal estimates, and the frequency mechanism proves its own
dimension/frequency-uniform estimate. The continuous principal-value
and flat/simplex consequences were also read, but the new proof only
needs full continuous annular variation.

## Priority, attribution, and metadata

I independently checked the live primary texts and version histories of
[Becker–Durcik](https://arxiv.org/html/2603.20173v1) and
[Demeter](https://arxiv.org/html/math/0601277), together with the relevant
reduction passages of
[Demeter–Thiele](https://arxiv.org/html/0803.1268) and
[Durcik–Kovac–Skreb–Thiele](https://arxiv.org/html/1603.00631).
Becker–Durcik's full variation corollary concerns averages along opposite
powers of one transformation. Demeter's Hilbert result likewise uses
opposite powers. Neither provides the arbitrary two-generator Hilbert
variation theorem. The inspected live submission histories list only
the stated v1 versions for the two specifically requested papers.

Demeter–Thiele Section 6 footnote 36 explicitly describes the
continuous/lattice/orbit reduction. The later norm-variation paper's
Section 5 integrates phase fractions of positive area and transfers
orbit arrays; its main result is fixed-partition norm variation of
averages, not the present pointwise Hilbert variation. These inherited
mechanisms are credited in the note. I also read the saved primary
companion/citation-chain evidence; this review does not claim an
exhaustive new search of every equivalent theorem.

The strongest warranted novelty framing is the note's current one:
an explicit newly available restriction/transference consequence of
OpenAI's continuous result, with checkable singular-kernel bookkeeping.
Neither the title nor abstract advertises an independent solution of
the continuous base problem or invention of transference. The upstream
author matches its supplied citation. The saved priority record correctly
distinguishes manuscript dates from first public accessibility; no
first-priority assertion is made. A final correction/history refresh
remains a publication-operation responsibility because the source is new.

The manifest matches the intended four individually downloadable files.
The title, author/ORCID, October 6 local publication date, license,
related upstream pinned URL and mathematical description match the
paper/README. No affiliation, coauthor or human-review claim is invented.
AI-use and lack of conventional human refereeing are plainly disclosed.
No theorem is advertised as formally verified. Upstream manuscripts are
excluded from the deposit archives, avoiding an unestablished
redistribution claim. I did not inspect remote Zenodo draft state or
tracker state and make no publication claim.

## Independent artifact reproduction and PDF inspection

Using Python 3.14.6 and Tectonic 0.16.9, I extracted the actual source
archive to `reviews/complete_package_review_1-assets/source/` and ran
the README build command with `SOURCE_DATE_EPOCH=1791349200`. The build
succeeded, with only two underfull bibliography boxes. The independently
generated PDF is **byte-identical** to the intended deposit PDF:
79,186 bytes, SHA-256
`5bfcfe064052e7e23005fbb45a8c83c2d1e3188ec4ef29ff97f46ea19edd60ea`.
Thus this source archive reproduces the actual reviewed paper, not merely
a different editor preview.

Both programs were run from that extracted directory, leaving the
reviewed package untouched. The geometry output exactly matched the
saved JSON, including 14,850 checks and the signed-kernel error value.
The frequency program's entire parsed JSON exactly matched the saved
result. Its frequencies and coefficients are finite midpoint quadrature,
properly labeled as exploration rather than a certified continuum
counterexample search. Those programs support bookkeeping only. The
unrecorded matrix experiment in R1 was not reproduced.

All five rendered deposit pages were inspected: equations, supremum
placement, exponent/sign/kernel symbols, references, proof endings and
page breaks are legible without clipped content. All PDF fonts are
embedded. Title and author metadata are correct; the fixed creation epoch
is consistent with the documented build. PDF inspection reports no
encryption, JavaScript or form.

## Optional edits, separate from substantive issues

1. The frozen supplement's theorem/approach ledgers still say complete
   package review is pending. These are clearly pre-publication research
   checkpoints, and README explains that final reviews are retained
   separately, so this is not a mathematical contradiction. A future
   package could label them explicitly as checkpoint snapshots to reduce
   reader confusion.
2. The product `8\,4^{2/3}` is standard but visually close-set. An explicit
   multiplication dot would improve readability. The two underfull
   reference paragraphs also permit a cosmetic line-break improvement.

Neither optional edit should be conflated with R1. Any changed deposit
bytes require the renewed exact-hash package review demanded by the
original protocol. My strongest verified finding is the rigorous
continuous-to-discrete-to-arbitrary-commuting implication with its stated
constant, together with an independent reconstruction finding no gap in
the upstream proof needed for the cited continuous premise. The exact
frozen package remains short of a clean publication verdict because of R1.
