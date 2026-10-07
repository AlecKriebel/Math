# First complete review of the quantitative refinement

Reviewer: independent internal complete-package review agent `refinement_review_one`.
Checkpoint: **2026-10-06 23:11 PDT / 2026-10-07 06:11 UTC**.
Bounded review completion: **100%**. This percentage concerns this assigned review,
not a declaration that publication or tracking is complete. Automated adversarial
review is not human peer review or formal verification.

## Verdict

**No substantive mathematical defect or affirmative antecedent duplication of the
exact new model calibration was found. Three concrete package clarifications or
repairs are required before promotion, followed by a new complete reviewer of a
new exact frozen version.** The current frozen files were not changed by this
review. The required changes are:

1. Explicitly define `R=F_2[H]` in the augmentation paragraph after Theorem 5.
2. Explicitly choose the designated roots `x_A,x_B` for the tree words in `A′,B′`.
3. Move the existing-version guard in `verification/build_package.py` before any
   write to `source-and-audit.zip`.

The first two fix scope and extraction notation, without changing the underlying
valid proofs. The third repairs a reproducible freeze-order bug. None invalidates
the currently hashed PDF/archive, but this pass does not license publication of
an unrepaired version. A favorable mathematical assessment cannot substitute for
the mandated repair and fresh whole-package review.

## Exact reviewed version and custody

I read the original request directly from `notes/ORIGINAL_REQUEST.txt` and the
applicable `/Users/alec/Documents/Math/AGENTS.md`. I reviewed every file listed in
`reviews/refinement1_manifest.json`, including the complete manuscript, README,
claim/dependency/approach records, all authored audits, all six packaged Python
files, finite incidence data, priority evidence, licenses, separately downloadable
PDF and archive, and exact intended Zenodo metadata. The archive's own manifest
is an additional inspected member.

| Item | SHA-256 |
|---|---|
| `reviews/refinement1_manifest.json` | `303ee9dbbbd21374bbd484655fa74215407269f3b13342d98cb1cba23415ec76` |
| `main.tex` | `7035ad934e01b289cfeb1ce11c417983a28200a649e6cd57c946676ef2ef63f7` |
| `paper.pdf` | `7403f3c1176dbaf57d95d25ce2165aa1014b70201c00806a46ba71edba175506` |
| `source-and-audit.zip` | `c6f7a3f187a396b0089f4667e25676afaa7121706df8d721de005b80f89e726d` |
| `zenodo-deposit.json` | `e9eca7af65685bceaa410862c4b25ac0b1dfe662667aedd983b9edbc15327a72` |

All **47** frozen file hashes and lengths matched at the beginning and end of the
review. All **45** ZIP members matched the expected names, their manifest bytes,
sizes and SHA-256 values; CRC checking passed. There were no duplicate member
names. All **104** source-manifest entries and **85** priority-source-manifest
entries matched the retained local inputs. The primary October 4 sources are
pinned at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

The exact original source reviewed was all seven sections (introduction, algebra,
random, patterns, planar, topology, assembly), its main source, bibliography,
manuscript README/citation, repository README, family-197 Lean scope and the
relevant companion disclosures. I rechecked the actual arguments, rather than
accepting earlier favorable source/package verdicts as premises. Those earlier
reviews remain useful scoped evidence, not reviews of this changed package.

Scratch receipts and blinded supporting reviews are under
`reviews/refinement_review_one_work/`; that directory is outside the immutable
deposit archive. No Git state, source clone, deposit, tracker or frozen payload
was mutated. Public read-only source retrieval was performed; no individual was
contacted.

## Mathematical verification and attempted falsification

### Exact calibration

The quotient follows from classes of the actual incoming letter, not its inverse:
seven extras `E`, their seven ordinary mates `S`, and the remaining `v−7` ordinary
letters `O`. Inverse maps exchange `E,S` and preserve `O`. The forbidden successor
therefore removes respectively one `S`, one `E`, or one `O` letter. These counts
give exactly Equation (2), for every allowed pairing. The positive quotient
Perron vector lifts to a strictly positive full-matrix eigenvector; positive-vector
bounds also prove the stated conclusions directly. No spectral rounding is used.

The upper vector `(1,13/5,1)` at order 32 gives all three displayed exact ratios
strictly below `987/1000`. Because `1≤f`, summing the lifted entries gives precisely
`5376/5`; the claimed bound holds for every `h≥1`, including the boundary case
`h=1`. The eventual source decay follows by absorbing the prefactor, with
`δ=−log(987/1000)/4>0`.

The common lower vector `(193/500,1,97/250)` is positive and bounded above by one.
All nine displayed ratios at 4, 8 and 16 are strictly above `503/500`. Iteration
gives the displayed exponential-growth bound and proves that these same full
matrices cannot satisfy the source's eventual squared-word decay. Thus 32 really
is the least dyadic order in the stated domain, rather than merely a working trial
vector. The order-2 integrality obstruction is correct and expressly outside
that domain. The lower bounds do not forbid alternative graph/type constructions
or idempotents at smaller alphabets.

A fresh blinded parameter agent independently derived the quotient before reading
the supplied verifiers, checked all 1064 full-matrix rows, and reconstructed the
finite field/incidence data independently. Its exhaustive check found 1057 points
and lines, 33 incidences in each row/column, unique incidence for all 558096 pairs
of points and all 558096 pairs of lines, the seven Fano complements, and 532 inverse
pairs. The packaged field verifier also passed. These are finite label-model
certificates, not matching or group-ring certificates.

### Transfer of the difficult source proof

I checked the complete probability, pattern, planar and topology arguments and
the replacements needed at order 32. The balance formulas, even-distribution
errors and capacity coefficient `33/604<1` are correct. The weights remain fixed,
positive on reduced turns, at most one and symmetric under reversal. Degrees are
33, 37 and 40.

The two strict girth inequalities hold for `c0=1/100`; the switching exclusion is
`r_n=o(n)`. The switch count is an injection and does not divide by an unknown
girth probability. For nonexpanding `k`-sets the prescribed-edge count is
`ceil(33k/2)`, between `16.5k` and `17k`; the resulting exponent is `29/2`, with
small-`k` exponent `29/4`. The explicit conservative `η=10^−6` certificate is valid.
The same packing argument gives a newly chosen fixed diameter constant.

The multiplicity-stage proof uses distinct underlying prescriptions, injective
image embeddings and separate first moments; it does not assume independence of
stages or count traversals as independent edges. The common-grid, translation and
reflection self-link, word-bin and minimum-stage arguments survive with the new
fixed alphabet and decay constants. The unpaired fraction is chosen before the
fixed path-count, total-length and comparison bounds. No dependency reversal is
introduced by enormous subsequent fixed constants.

Deleting two incident edges still leaves degree at least 31, so the closure proof
works without cancellation of original occurrences. The ribbon/Euler and separator
arguments retain their budgets and handle disconnected neighborhoods, self-bands,
parallel edges and the single exceptional break. The extraction selects the same
fixed triple for every finite arrangement; there is no illicit unbounded union
bound. A separate fresh primary-only planar attack also found no defect and checked
174878 finite admissible ribbon decompositions. These finite tests supplement,
and do not replace, the deterministic proof.

The cone-picture argument is parameter-free. Its four same-edge surgeries preserve
either the essential sphere or the rooted disk failure; the self-inner surgery
uses a common lift and a homology identity, not an assumed embedded cone image.
Asphericity and root protection are distinct verified conclusions. The finite
two-dimensional contractible-cover resolution rules out prime-order torsion by
the cyclic periodic resolution. The parity proof then gives scalar `ab=1,ac=0`
and `c≠0` over **F₂**. The 532-edge rose supplies generators via the relative
cone replacement, rather than merely counting labels.

### Classical embedding and algebra

A separate fresh blinded embedding/ring attack verified the two free bases, HNN
injection, exact `W_i`, torsion preservation, finite 2D tree-of-spaces model and the
specific generator/defining-cell eliminations preserving the final `r`-relator
aspherical complex. It checked the general formulas and all indices 1 through 532
plus 8260 with an independent word representation. The published HNN and
Morozov–Schupp sources support the classical mechanism. The final cell-level
argument does not rely on the false statement that all Tietze moves preserve
asphericity. A torsion-free one-generator group has a domain group algebra, so
the least generator count of two is correct; the machinery is inherited.

The arbitrary-ring defect calculation, nontriviality, complementary right ideals,
`baR=bR`, and inverse maps by **left multiplication on right modules** all check.
`eR` is nonzero cyclic projective, absorption makes its `K₀` class zero, and this
does not make the module zero. Group inclusion and coefficient extension are
injective on bases. The same scalar example therefore persists over every
characteristic-two field. No characteristic-zero/odd-characteristic, analytic
projection, matrix-only substitute or nonzero `K₀` class is smuggled into these
arguments. The mismatched earlier torsion Lean example is not used as verification.

## Priority and publication scope

I independently retrieved the two exact antecedent triage files by anonymous
HTTPS at public commit `f27318d83bd7000ef817957a9a4b3087de28d198`; their bytes and
hashes matched the saved evidence. They already disclose the original scalar
defect, characteristic-two extension, cyclic projective, regular-module absorption
and zero `K₀` class, conditional on checking the source. Source auditing is valuable
new verification work, but cannot make those same consequences an independent
new discovery.

The exact new result reviewed here is different: the three-class full-matrix
calibration, positive growth certificates at 4/8/16, pairing-independent least
dyadic threshold and complete order-32 parameter transfer. The source fixes 128.
Its original upper vector already works at 32, which the package acknowledges;
the lower-order obstruction and exact calibration are the added checkable content.
The three-extra zero-divisor companion has a different model and does not supply
this seven-extra threshold. The inspected core triage has no such calibration.

Fresh searches combining the exact source title, order 32, Fano, Kaplansky and
squared-turn spectral terms did not supply an affirmative additional disclosure.
Those negative searches are bounded evidence, not a proof of universal novelty.
The paper makes no first-priority claim. The two-generator embedding and the
idempotent/module machinery are expressly classical and inherited. The narrowed
model calibration is a defensible modest in-scope extension rather than a relabeling
of the duplicated core. This assessment does not license presenting it as a new
solution of direct finiteness or a global optimal alphabet/generator theorem.

Protocol-required checkpoints from this same effort are releases of its own new
finding, not independent antecedent disclosures that would circularly prohibit
the required later publication. The earlier separate public triage remains an
actual antecedent duplicate for the core.

## Reproduction, PDF and intended deposit

The documented reproduction was run from a clean extraction with no upstream
source working copies. All four finite checks passed, with absent optional source
checks explicitly marked skipped. `verification/reproduce.py` successfully created
its output directories, built the standalone TeX using Python 3.14.6 and Tectonic
0.16.9, verified extracted text and wrote a receipt. Poppler reports seven US-letter
pages; every font is embedded and subsetted, with no JavaScript, encryption or forms.
The expected title and author metadata match the source and intended deposit.

I rendered and personally inspected **every one of the seven original PDF pages**.
Formulas, tables, references, symbols, page breaks and margins are legible; there
is no clipping, overlap or missing-glyph defect. The clean rebuilt PDF has SHA-256
`c6156a0ade136acfa0ceae6f1b00ea428ed849d5369a11a174a465ae68d44d6f` because of build
metadata. All seven original and rebuilt page images at 110 dpi are byte-identical.

The intended upload manifest correctly lists the paper PDF separately from its
source/audit archive. Title, author, supplied ORCID, date, description, related
identifiers, license and boundary statements agree across the payload. AI use and
absence of human peer review are disclosed. The archive contains newly authored
material, exact finite data, public custody evidence and license notices; it does
not include third-party full manuscripts, local source caches, credentials, runtime
binaries or external authorship/affiliation inventions. Public metadata/header
evidence was inspected for credential fields; none was found. Mixed prose/data
CC BY 4.0 and code MIT terms are explicitly recorded.

## Required repairs and exact evidence

**R1 — Augmentation scope.** After the theorem uses `S=K[H]`, the next paragraph
reuses the arbitrary-ring letter `R` and asserts `F₂→R→F₂`. Such an augmentation is
not available for an arbitrary ring. Introduce `R=F₂[H]` there, or use the general
`K→K[H]→K` splitting. The valid group-algebra `K₀` claim is unchanged.

**R2 — Root convention.** In the tree-word extraction paragraph, explicitly take
the roots of `A′,B′` to be `x_A,x_B`. Those designated roots justify the stated
identity coefficient of `c` being one. Arbitrary new component roots preserve
nonvanishing by multiplication by a group unit, but root protection only directly
gives that particular coefficient in the designated-root convention. The existing
`ALGEBRA_PROOF.md` already states the correct choice.

**R3 — Freeze guard ordering.** Static inspection showed that the builder checks
whether `reviews/<version>_manifest.json` already exists only after overwriting
the source archive. A scratch attack copied the exact archive, metadata and frozen
manifest into the clean extraction, appended a marker to the scratch README and
reran the same version. The builder raised its expected overwrite refusal, but the
archive had already changed from `c6f7a3f1…` to `f71ffcdc…`. This is saved in
`freeze_order_attack.json`. Move the guard before any archive mutation. An atomic
temporary-file archive replacement would be optional further hardening; it is not
needed to resolve the observed repeated-version bug. The attack did not mutate
the actual reviewed project files.

Minor robustness observation: `verify_parameter.py` and the historical `verify.py`
use Python assertions, which optimization disables. The documented unoptimized
commands pass and establish their advertised finite checks. Optimized execution
is not advertised as verification; explicit always-active checks would nevertheless
be a reasonable optional improvement.

No other substantive concern remains from this first complete pass. After the
required repairs, freeze a new exact package and assign a **new** complete reviewer;
do not carry this verdict forward as certification of changed bytes.
