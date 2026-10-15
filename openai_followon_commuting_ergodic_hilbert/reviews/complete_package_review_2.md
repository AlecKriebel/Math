# Fresh independent complete-package adversarial review 2

Reviewer: internal AI research auditor `/root/complete_package_review_2`.
Review date: October 6 PDT / October 7 UTC, 2026.
This is an automated research audit, not conventional human peer review,
refereeing, formal certification, or external endorsement.

## Verdict and exact review boundary

**One substantive publication-presentation scope issue was found in the exact
candidate identified below: non-kernel numerical probes are presented in the
deposit supplement despite the original request's numerical boundary. This
candidate needs repair and fresh review before publication.** No substantive
mathematical, attribution, metadata, archive-completeness, or reproducibility
issue was otherwise found.
The restriction/transference proof is valid assuming the precisely cited
continuous pointwise annular theorem. I also independently reconstructed the
needed upstream proof chain and found no material unsupported step or
counterexample. Acceptance does not rest on the theorem's presence in a release,
a Lean directory, the earlier complete-package verdict, or successful numerical
experiments.

I read the workspace `AGENTS.md` and `research/ORIGINAL_REQUEST.txt`, and read
the primary annular proof sections before the saved favorable dependency-audit
reports. I did not use `complete_package_review_1.md` as proof evidence. The
full original mathematical target, rather than a weaker substitute, is resolved by the
candidate: arbitrary commuting invertible bimeasurable probability-preserving
transformations; complex `L3` inputs; symmetric Hilbert sums starting at `H0=0`;
full pointwise `r`-variation in `L^(3/2)` for every `r>2`; maximal control;
almost-everywhere and norm convergence. The stronger maximal-tail norm
convergence also follows.

Only my review artifact directory and this report were written. Candidate
files, Git state, deposit records, tracker, and external applications were not
modified. No individual was contacted. The two delegated internal AI audits
were independent archive/reproduction and primary-priority workstreams.

Review checkpoint: audit completion **100%**; best-guess mathematical-resolution
assessment **98%** and publication-package preparation assessment **80%** before
external publication/tracking. These percentages are estimates, not evidence.
No publication or tracker-success claim is made here.

## Required repair: keep numerical presentation within the user's boundary

The governing sentence is explicit in `research/ORIGINAL_REQUEST.txt:22`:
**"Any numerical checks must be presented as support for kernel bookkeeping
only."** This is narrower than merely saying that numerical experiments do not
prove the analytic theorem.

The exact current supplement contains `reviews/upstream_energy_audit.md:75`
under the heading **"Numerical corroboration and formalization boundary"**.
At line 77 it reports mixed-trace and neighbor-comparison ratios as numerical
corroboration of the matrix/heat machinery. These are matrix inequality
probes, not singular cell-kernel bookkeeping. The supplemental frequency
audit at `reviews/upstream_frequency_audit.md:334` through line 364 describes
output-dependent phase choices and discrete `ell^(3/2)` output-norm ratios
as falsification probes for the frequency-block estimate. The accompanying
program contains those norm/phase probes; its label as finite quadrature and
noncertificate does not turn them into kernel-only bookkeeping. The root and
deposited README at lines 22–35 prescribe both frequency and matrix reruns as
part of the verification package.

The scripts and claims reproduce accurately, and the analytic proofs do not
rely on them. That establishes reproducibility and prevents a false proof
claim, but it does **not** satisfy the user's more restrictive presentation
instruction. This issue was identified after explicitly rechecking that
boundary; the initially provisional no-issue assessment has been withdrawn.

The safest concrete repair is to preserve these historical exploratory
programs/outputs in the research history, but exclude their non-kernel
numerical-corroboration claims and probe files from the deposit source and
supplement. Publish the exact analytic upstream audits without those numerical
sections, and retain the Section 2 signed kernel/support/error/variation
bookkeeping checks. A separately justified checker limited to Gaussian/kernel
identities could be included, but the current frequency program's output-norm
probes would need removal rather than relabeling. Update the README, archive
allowlists, ledgers/metadata wherever needed, rebuild deterministically,
recheck the new exact hashes, and obtain a new whole-package review. The
manuscript's mathematical proof and PDF need no mathematical repair on account
of this issue. Do not delete or rewrite historical evidence to conceal that
these explorations occurred.

## Exact intended payload and metadata hashes

The metadata manifest selects exactly the four files inside
`publication/upload-kit`, rather than an outer kit archive.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `publication/upload-kit/paper.pdf` | 79186 | `5bfcfe064052e7e23005fbb45a8c83c2d1e3188ec4ef29ff97f46ea19edd60ea` |
| `publication/upload-kit/source.zip` | 14925 | `104ab19cd39dffdde49b5985db5d97635ded44bedd79c96374df55132c613073` |
| `publication/upload-kit/verification-supplement.zip` | 53754 | `4887fcd6e1d239a734d97ce3f5b97539aac24a507b734f5c8474d7d456c1c9d5` |
| `publication/upload-kit/README.md` | 5285 | `fcc989ea6c06d2dc674e8fafef20d72b3711729cad4becbe19e67226a1bf4380` |
| `zenodo-deposit.json` | 2896 | `5cff48980a8898e552f0b1945235b3cb3a8725b295ea351fdb010d0f3e8a3845` |

The reviewed `main.tex` SHA-256 is
`b487be2a3233d56facde9713681733e5e6d7a8539ff6d78a94cf7d7db796f10f`.
`publication/paper.pdf` and the upload-kit PDF are identical. The root README
and kit README are identical. The SHA-256 of the manifest's `metadata` object
serialized as sorted compact UTF-8 JSON is
`d440c48b942a8fae80567280797eaa128a89e3d339af48435e406a83169ebc36`;
the raw manifest hash above is the authoritative exact file hash.

`reviews/complete_package_review_2-assets/reviewed_hashes.json` records a
51-file read-set snapshot. `source_pin_check.json` independently verifies all
15 copied upstream source/README/scope/PDF files against both
`sources/SOURCE_HASHES.json` and the actual immutable Git blobs at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Every comparison passed.
The pinned upstream PDF hash is
`f5857c58037fa5289f2f9fe1fe4421af11df8d9fa9b2914ba041469f1195ea31`.
The rendered upstream PDF's theorem statement agrees with its TeX.

## Independent reconstruction of the analytic dependency

The primary files reviewed are the annular manuscript's `build/main.tex` and
all nine included sections: introduction, preliminaries, matrix, heat, smooth,
frequency, rough, completion, and consequences. Its README and bibliography,
repository README, and actual supplied Lean scope document were also read.
The needed theorem is its Theorem 1.1, not the older maximal or dyadic result.

1. **Representatives and the full pointwise supremum.** For each fixed `t`,
   translation invariance and Hölder bound the product in `L^(3/2)` by the
   product of the two `L3` norms. Integrating `dt/|t|` proves the finite-annulus
   bound `2 log(R/epsilon)` times those norms. Countably many containing annuli
   give one null set for all finite endpoint pairs, and absolute continuity
   gives endpoint continuity. The rational supremum is measurable. In the
   completion proof, finite menus are linearized by measurable tie-breaking
   and complex phases, then approximated by common finite rectangular step
   partitions on compact support. The constants precede menu exhaustion.
   Consequently the partition may depend on the output point; the supremum
   is never moved outside the output norm.

2. **Supported matrix costs.** Independently differentiating the square root
   through the Sylvester equation gives
   `b_P(K)=(3/2) sum_ij |K_ij|^2/(sqrt(p_i)+sqrt(p_j))` on the support of `P`.
   Regularization justifies order comparison without a positive lower
   spectral bound. For probability averages,
   `(integral sqrt(T))^2 <= integral T`, followed by square-root order and the
   inverse variational formula, gives the claimed joint averaging inequality.
   This does not invoke an unproved interchange of inverses and averages.
   The mixed-trace proof places the three stars in a Hermitian block matrix,
   groups the signed cubic expansion by its smallest index, and uses one
   edge's phase to recover the complex modulus. The three cases exhaust the
   expansion, including repeated indices and zero eigenvalues. The phase
   change conjugates the relevant costs unitarily. I found no missing support,
   dimension, conjugation, or sign assumption in these steps.

3. **Heat and comparable-variance dissipation.** Row and column insertions
   use the appropriate Gram so that the support remains fixed during each
   derivative. The mixed column derivative equals the Hessian cross cost.
   Integrated pure and mixed center derivatives agree only after plane
   integration; the proof does not assert their false pointwise equality.
   The neighbor comparison follows from `T <= 2 diag(A*A,B*B)`, discarding
   nonnegative off-block costs, and a second order comparison. The resulting
   loss is `sqrt(2)`. For rates `(1,11/10,11/10)` the remaining coefficients
   are `-1+(3/5)sqrt(2)` and `-11/10+(1/2)sqrt(2)`, both strictly negative.
   Finite-array Gaussian bounds justify differentiation and integration by
   parts; the initial-energy bound has uniform grid mass once variances
   exceed the mesh scale. Single-edge energies pay the column costs at
   arbitrary positive rates without assuming comparable variances.

4. **Smooth annuli and switching.** Disjoint intervals bound each masked
   dual entry by its original modulus and its total switch variation by
   `2n` times that modulus, also for complex coefficients and coincident
   openings/closings. The entry-gradient estimate produces jump terms
   containing the dual norm twice. Gaussian averaging and lattice shears
   give line-maximal majorants independent of the switch scale. Normalizing
   the three norms to `(n^(-1/2),1,1)` gives the stated `sqrt(n)` loss after
   rescaling. The narrowed row cost gains a factor `s`, which is canceled
   by `ds/s`. The smooth/hard identity follows from Gaussian scaling with
   `psi=-g_3'''` and `c0=2g_3''(0) != 0`; its signs agree with the endpoint
   error definition.

5. **Frequency refinement and boundary energy.** I rederived
   `Dil_L ell_xi=(L/D) derivative[g_(qL^2) exp(i xi u/L)]` and the exact
   completing-the-square formula used to average modulated narrow windows.
   On the slab, `b'=theta s`, `theta=1/(16D^2)`, keeps `b'<a/2`; both the
   exponential prefactor and Gaussian-density ratio stay bounded independent
   of `D`. Joint averaging gains the essential `theta s` cost. Averaging
   the shifted row center adds `1-theta` to the heat coefficient `2+theta`,
   giving `3`, with the correct integration-by-parts sign. The boundary
   covariance is `s[[2theta,-theta],[-theta,3]]`. Its difference from
   `4s diag(theta,1)` has positive determinant `theta(2-theta)s^2`, and
   the Gaussian normalization ratio is `4/sqrt(6-theta)`, uniformly bounded
   as `theta` decreases to zero. Thus there is no hidden narrow-width loss.
   Boundary mixed terms retain coefficient squares at each output index;
   cubic terms use the pointwise coefficient bound times those squares.
   The proof does not replace the frequency-square condition by a stronger,
   unavailable sum of frequency suprema.

6. **Rough kernels, endpoint grouping, and all scales.** Three vanishing
   moments permit a Gaussian-weighted third primitive. Bounded variation
   gives the `m/D` Fourier bounds, including the `L2` bound via a translation
   difference; on `D<=|xi|<2D`, the multiplier of that difference is bounded
   away from zero. The finite cutoff error has an `L5` Gaussian envelope
   small enough to sum over the nonzero scale groups. The normalized block
   coefficients satisfy both the uniform and pointwise square-sum conditions.
   Odd kernels lose their first moment via a summable dilation identity.
   Endpoint pairs in one half-open dyadic group have total paired length at
   most one; at most two endpoints are unpaired, and at a nonendpoint radius
   only one paired hard indicator can be active. Complex coefficients do
   not destroy these absolute bounds. Large-count groups are at most
   `2sqrt(n)` pointwise. Shared endpoints and dyadic-boundary endpoints are
   accounted for exactly once.

7. **Count-to-variation completion.** For any finite partition, its largest
   `2^j` increments are an admissible disjoint-annulus list. Rank grouping
   therefore gives
   `V_r <= sum_j 2^(j/r-j) S_(2^j)`.
   Applying the count estimate yields the convergent series
   `sum_j (1+j)2^(j(1/r-1/2))` for every `r>2`. Density is used on a finite
   menu before countable exhaustion, preserving representatives and the
   pointwise supremum. No restriction to dyadic endpoints or a bounded
   number of partition increments remains. There is no circular invocation
   of full variation in its own proof.

These exact deductions, rather than the numerical checks, are the basis for
accepting the required continuous dependency. The family 082 Lean scope names
the older maximal theorem. No applicable annular formalization/build is used
as evidence, and the candidate correctly makes no formal-verification claim.

## Independent attack on the new restriction and transference

The key proof locations are `main.tex:126` through `main.tex:284`.

**Supports, signs, and fixed positive area.** With input half-width `h=1/8`
and output half-width `q=1/16`, different moving indices cannot overlap:
their center difference has magnitude at least `1-|a-b| > 7/8`, exceeding
the total input interval width `1/4`. The common offset interval is exactly
`[-h-min(a,b), h-max(a,b)]`, with length `ell=1/4-|a-b| >= 1/8` and
`|s|<=3/16`. Each nonzero integer window has a constant sign and radial
support in `[|k|-3/16,|k|+3/16]`. Half-integer endpoints include or exclude
the entire window on both sides of zero; the `k=0` window is always excluded.
The negative denominator is retained as `k+s`. In particular the proof never
assumes the generally false identity `K_(-k)(a,b)=-K_k(a,b)` for asymmetric
phases. The exact coefficient is
`log|k+h-max(a,b)|-log|k-h-min(a,b)|`.

**Uniform error variation.** The identity
`1/(k+s)-1/k=-s/[k(k+s)]` and
`|k+s| >= (13/16)|k|` give
`|delta_k|/ell <= 3/(13k^2)` for every nonzero signed integer.
Distinct radial increments use disjoint sets of coefficients. Their full
variation is bounded by their total absolute sum; it is not multiplied by
the partition length. Hölder, translations, and Minkowski then give the
uniform error norm `pi^2/13` times the input norms. Countable integer lists
share a common null set. Integrating over output boxes of area `1/64` and
input boxes of area `1/16` yields exactly
`D_r=8*4^(2/3)C_r+pi^2/13`. No phase diagonal or shrinking-width limit occurs.

**Finite menus before growing windows.** At fixed truncation maximum `M`,
the partition menu is finite and measurable. Orbit arrays are restricted
to `Q_(L+M)`; every entry needed on `Q_L` lies there. Commutation identifies
each complete truncated lattice sum with the corresponding ergodic sum
at the orbit point, for negative indices too. Raising the lattice estimate
to `p=3/2` produces two sums to the power `1/2`. Integration and
Cauchy–Schwarz give the outer-window cardinality and the correct input
norm powers. At fixed `M` the cardinality ratio tends to one as `L` grows.
Only afterward does `M` increase, by monotone convergence, to the full
countable partition supremum. No ergodicity, pointwise convergence of orbit
averages, standard-Borel model, or suspension assumption is inserted.

**Null sets, convergence, and boundary cases.** Countably many preimages
under finite transformation words remove infinite representatives and any
modulo-null commutation failures on an invariant conull set. Changing
representatives affects all finite sums only on such a null union. Fixing
`r=3`, finite variation forces the complex scalar sequence to be Cauchy:
failure would supply arbitrarily many strictly ordered disjoint pairs with
a fixed positive separation. The same anchored variation controls the
maximum because `H0=0`. The measurable maximal tail tends to zero and is
dominated by `2H_*`; dominated convergence proves both the asserted tail
bound and norm convergence. Bilinearity survives the norm limit. Zero
inputs, identity maps, coinciding maps, and finite atomic systems introduce
no exception to any step.

The theorem does not imply a noncommuting result, the endpoint `r=2`, an
input-exponent extension, or ordinary one-sided commuting Cesaro
convergence. Title, abstract, README, ledgers, and metadata maintain these
boundaries. No optional flow statement needing joint measurability appears.

## Attribution, priority, and metadata

I independently opened the primary arXiv texts and checked the exact relevant
statements; a delegated primary-priority reviewer also fetched primary texts,
immutable OpenAI sources, supplied BibTeX, and public repository metadata.

- [Demeter, math/0601277v1](https://arxiv.org/html/math/0601277v1), Theorem 1.2
  and Remark 1.3, treat `tau^n` and `tau^(-n)` for one transformation. They
  do not state the arbitrary commuting target. Section 3.3 already uses
  fixed-width cell supports and a summable singular-kernel error, reinforcing
  the established provenance of the method rather than a claim that cell
  restriction itself was invented here.
- [Becker–Durcik, 2603.20173v1](https://arxiv.org/html/2603.20173v1), equation
  (1.5) and Corollary 1.4, concern bilinear averages along `T` and `T^(-1)`.
  At the candidate's output exponent `3/2`, the range is `r>2`. The discussion
  of (1.8) distinguishes arbitrary commuting transformations. This is an
  accurate comparator, not the claimed new Hilbert theorem.
- [Demeter–Thiele, 0803.1268v1](https://arxiv.org/html/0803.1268v1), Section 6
  and footnote 36, explicitly identify the continuous-to-lattice and orbit
  array reductions. The candidate credits them. The old commuting problem
  stated there is an averages problem, so it does not license the candidate
  to claim one-sided Cesaro convergence.
- [Durcik–Kovac–Skreb–Thiele, 1603.00631](https://arxiv.org/abs/1603.00631),
  Section 5, supplies a positive-area phase-integration predecessor and
  norm-variation for commuting averages. Its fixed-list norm estimate does
  not equal the full pointwise Hilbert variation used here.

The supplied annular README attributes the work to OpenAI. Its specific
BibTeX entry is preserved verbatim in the packaged `references.bib`; the
paper's internal bibliography supplies the same author/title/provenance with
an immutable commit URL. The annular, maximal, and dyadic companion source
sections were checked for exact duplication: they contain the continuous
results and ergodic motivation, but no exact arbitrary-commuting discrete
Hilbert theorem or complete present restriction proof was identified.

The honest novelty statement is a newly available corollary with explicit
signed restriction bookkeeping and full transfer, not an independent solution
of the continuous triangular-Hilbert breakthrough or invention of transference.
That is the candidate's framing. Primary-source negative findings are scoped;
they are not proof that no earlier equivalent theorem exists or a claim of
being first. Manuscript dates are not presented as public-priority certificates.

The exact metadata title, description, date `2026-10-06`, preprint type,
version `1.0.0`, CC BY 4.0 license, author `Kriebel, Alec`, ORCID
`0009-0001-9320-500X`, and `isDerivedFrom` identifier agree with the note and
original instructions. No affiliation, coauthor, human refereeing, or formal
certificate is fabricated. AI-use disclosure and absence of conventional
human peer review are explicit.

## Actual archives, code, PDF, and reproducibility

The independent archive reviewer freshly extracted the actual intended ZIPs,
inspected their code and result files, and reran in its owned directory.
The source archive contains six files and the supplement 25. All 31 entries
match current owned inputs byte for byte; both ZIPs pass CRC, no duplicate
names, no symlinks, and safe relative-name checks. Every advertised matrix
probe now has its exact program, stored stdout, and environment/provenance
record in the supplement. No unpublished input data are needed. Upstream
PDFs/TeX, credentials, caches, and reviewer scratch material are excluded.
The isolated replica of the actual package builder recreates every intended
payload byte exactly.

Fresh runtimes and outcomes:

| Check | Fresh result |
| --- | --- |
| Extracted geometry program; Python 3.14.6 | Exit 0; 14,850 assertions; parsed result exactly equals saved JSON |
| Extracted frequency program; Python 3.14.6 | Exit 0; generated JSON exactly equals saved bytes |
| Extracted TeX; Tectonic 0.16.9, epoch 1791349200 | Exit 0; PDF exactly matches deposit SHA-256 |
| Energy program; Python 3.12.14, NumPy 2.3.5, arm64 Accelerate | Exit 0; stored stdout reproduced exactly |
| Matrix seed 9132784; same runtime | Exit 0; stored stdout reproduced exactly |
| Matrix seed 882064; same runtime | Exit 0; stored stdout reproduced exactly |

The exact energy maximum ratios reproduced as `0.07470168193073122` and
`0.707003261832278`. The two matrix programs reproduce all their recorded
maxima and scalar lines. The standard-library frequency program reproduces
12 finite quadrature probes and three covariance probes. The code and text
consistently disclose the finite, floating-point, eigenvalue-cutoff, backend,
and uncertified-quadrature limits. None is advertised as an analytic proof
or a certificate for near-singular spectra. Nevertheless, the non-kernel
corroboration presentation violates the separate original numerical boundary,
as detailed in the required-repair section above. I inspected all five numerical
programs, their saved result files, and the build script; the delegated
reviewer additionally executed them from the exact extracted archives.

I rendered the actual upload-kit PDF afresh with Poppler and visually
inspected all five pages, then checked its extracted text against the source.
Formulas, signs, exponents, bounds, labels, hyperlinks, references, author,
and page breaks are legible and consistent. There is no clipping, missing
glyph, unresolved reference, or overfull text. The clean TeX build emits
only underfull bibliography-box warnings. PDF title and author match the
metadata, and the PDF has no forms, JavaScript, or encryption.

The detailed reproduction report and machine-readable per-entry/runtime
evidence are under
`reviews/complete_package_review_2-assets/archive_repro/`. They establish the
current hashes, independent of older clean-build receipts.

## Nonblocking historical and operational boundaries

`receipts/clean_checks.json` and
`receipts/PREPUBLICATION_SOURCE_REFRESH.json` contain superseded archive
hashes. They are historical checkpoint receipts, not current-payload
certificates. The frozen ledgers still say whole-package review is pending;
the README explicitly identifies them as prepublication checkpoint snapshots
and says later reviews are retained separately. These are coherent historical
records; on their own they do not identify an unresolved mathematical objection
or require mutation. The separate numerical-presentation issue does require
repair. Current hashes and fresh reproduction evidence identify this reviewed
candidate; the revised publication will require new hashes and remote
verification. Do not accidentally treat the older receipts as describing
either the current kit or a future revision.

Fresh primary priority evidence at 2026-10-07 05:36:49 UTC showed a public
repository and only the pinned initial commit; a later read-only remote-head
check at 05:40:50 UTC still resolved `main` to that SHA. Subsequent GitHub API
directory requests encountered a shared-IP rate limit; successful immutable
raw reads supplied the companion-source coverage. The delegated report records
this limit, exact primary URLs, 29 matching overlapping source hashes, and
the distinction between creation/commit/push times and first public visibility.

No Zenodo staging/schema acceptance, remote upload checks, DOI publication,
DOI resolver propagation, tracker entry, or final Git push was attempted by
this reviewer. Those remain the lead researcher's expressly authorized
operational steps **after the substantive scope repair and a fresh review**.
The hash-specific verdict must not be
carried over to materially changed payloads or metadata without renewed review.
