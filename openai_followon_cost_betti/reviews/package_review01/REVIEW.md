# Complete-package adversarial review 01: frozen candidate v1

Reviewer: `/root/package_review01`, a new complete-package reviewer.
Completed: October 6, 2026, America/Los_Angeles; exact UTC completion and
source hashes are recorded in `reviewed_hashes.json`.

**Verdict: repair required before publication.** No substantive mathematical,
attribution, or priority defect was identified, but one supplied supplemental
verifier fails after extraction because its proof path was not adapted to the
archive layout. This is a reproducibility defect in the complete package. It
does not falsify the mathematics. Repair it, rebuild the affected inventory
and archive, and give the entire resulting exact package to a NEW independent
complete-package reviewer. This review is not a clean verdict on a repaired
package and authorizes no publication operation.

The reviewed PDF and manuscript give a valid direct all-degree invariant
calculation, and the complete primary-source positive Bernoulli cost chain
withstood independent reconstruction. Publication eligibility is qualified
for the accurately attributed expanded consequence and verification note;
neither firstness nor an independent fixed-price discovery is established.

## Exact candidate and reproducible finding

The candidate is the one identified by `receipts/frozen_package_v1.json`.
I independently verified every listed byte length and SHA-256, equality with
the preserved `verification/frozen-v1` snapshot, all 35 archive entries, and
every entry's inventory hash. Intended uploads and metadata were unchanged
through this review:

| Item | SHA-256 |
|---|---|
| `publication/main.tex` | `7475979d063f5ad6e9e85f09fca5eca6f1beb83a83f654bc9011854dc8c4182a` |
| `publication/paper.pdf` | `d2af46715d94a23d4c51b25a4b78e5e2dab64cd7cae3fa61f2349194e5fc6f75` |
| `publication/cost-betti-source-and-verification.zip` | `727b57db8efeb6054a9fd0ee34f08560b4d02ee58e47a069cbd3ee0bba3411c2` |
| `zenodo-deposit.json` | `2c8d034e5ab30787c747b8e9bb195f332cd6a63f421147a8e2656cd1d39ae4de` |

**F1 — supplemental Fox verifier is not portable.** In the unchanged extracted
archive, run `python3 verification/check_fox.py`. It exits 1 before executing
its checks. Line 119 sets
`Path(__file__).parent.parent / "DIRECT_BETTI.md"`, and line 121 reads that
nonexistent file. The bundled proof is instead
`proof-audits/direct/DIRECT_BETTI.md`. The exact traceback and command result
are retained in `checks/extra_checks.json`. The script's SHA-256 is
`efb103e13d3a2a6358b4a7c1d655d05ce79985d4a39a033f8cbfcd75c1f3a711`.

The two commands actually listed in the README pass, so the primary
reproduction instructions are accurate. Nevertheless, the full uploaded
verification collection contains a broken command, and its independent-review
text states that this script reproduces its recorded result. The exact
remaining repair is a proof lookup that works both in the original research
layout and in the archive, or an explicit supported proof-file argument.
Regenerate the relevant code hash/receipt and package inventory. Run all four
supplied verifiers from a fresh extraction before the new complete review.

I separately imported the unchanged script and called `check(n)` for
`n=0,1,2,99`; every algebraic assertion passed. This bypassed the path error
solely to localize the finding, without editing the candidate. The independent
result is `checks/imported_fox_checks.json`. Thus F1 is a layout defect rather
than evidence of a Fox identity failure.

## Actual reviewed coverage

I read the original full `REQUEST.txt` and `/Users/alec/Documents/Math/AGENTS.md`,
the entire frozen manuscript, publication README, exact intended metadata,
theorem and dependency ledgers, all three priority reports and source/version
manifests, every bundled proof/audit report, all four verification programs,
their certificates, software/adaptation/build receipts, and the complete
archive inventory. I did not take the earlier favorable audits as certification.

For the pinned upstream input I read the repository README, source warning,
manuscript-specific citation, introduction, group/actions, compression,
deployment, finite models, planar lemma, rank surgery, conclusion, bibliography,
wrapper and figure references. All primary input hashes independently match
the bundled source manifest; the upstream checkout remained clean at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Catalogue, Lean documentation and
Comparator searches identified no corresponding formalization. No Lean
declaration or build is certified here.

I checked the actual published Gaboriau source, its global standard atomless
probability-space convention, Corollary 3.16, Properties 3.15(1), Corollary 3.23,
and dimension Properties 1.2. The relevant published pages 126 and 128 were
also visually inspected. The optional Lück reference was checked against
[the primary arXiv text](https://arxiv.org/html/math/0310489v1), Theorem 1.11
and section 2.3. It is consistent with the dimension use; Gaboriau already
supplies the needed finite Hilbert-module rank formula.

Two fresh scoped children preserved distinct checking mechanisms. Their
reports belong to this complete review, and are not substituted for its
package-wide integration:

* `cost_chain/AUDIT.md` independently reconstructs the entire positive-cost
  argument from primary source, with exact coverage/hashes and separate finite
  falsification checks.
* `priority_recheck/REPORT.md` independently retrieves the already-public
  preliminary triage, PSV version 1, Linnell's paper and current upstream
  public records. Its byte/hash receipts are in `coverage_manifest.json`.

Third-party inspection text, rendered pages and the temporary extraction are
excluded by this review folder's `.gitignore`. Check receipts and findings are
retained. No source-clone mutation, external individual communication, tracker
write, deposit operation, Git mutation, or candidate modification occurred.

## Independent mathematical reconstruction and falsification

**Group and actions.** A reduced word in the abstract `b_i,w` generators
expands to a nonempty reduced word in `A`: the `a` endpoints of the `w` words
cannot cancel against `b` blocks, and opposite consecutive `w` symbols are
excluded. The amalgam normal form embeds both factors and gives infinite
order for `t`; finite generation gives countability. The exponent-sum map
extends consistently, including `chi(w)=100`. Independent continuous
Bernoulli coordinates make each nonidentity fixed-point set null, and
countability gives the invariant Borel free locus. Coordinate permutations
and uniform height translation preserve probability. The `t` transformation
is mixing because finitely many coordinate supports eventually separate.
It fixes height, while `a` cycles heights, proving ergodicity of every `Y_M`.
These proofs also cover `M=1`, without using an upper-cost bound there.

**Tree and convolution.** The two-copy graph has degree 100 and is connected
through the identity matching and generator paths. A nonbacktracking closed
walk produces an alternating-sign word with neighboring labels distinct.
Identity labels cannot be adjacent; deleting one joins equal signs, leaving
a nonempty freely reduced word. This rules out cycles. At depth `n>=2`,
Cauchy--Schwarz gives `E_(n+1)>=E_(n-1)` because each parent is counted
`d-1` times. Nonnegative, nondecreasing, summable odd and positive even
layer energies vanish; the neighbor equation then kills the root value.
The argument covers complex coefficients and `d=2`. The block adjacency
is exactly `[[0,T],[T*,0]]`, and coefficient right convolution by `S` is
`T*`. It preserves left cosets `gF`. Right `t-1` annihilation makes a vector
constant on infinite right-`t` orbits. Neither injectivity proof requires
a bounded inverse, closed range, ambient torsion-free assumption, or general
analytic zero-divisor conjecture.

**Fox boundary and topology.** I rederived the attaching-prefix rule with
left coefficients and right coordinate multiplication. For
`r_v=t v t^-1 v^-1`, the free derivative is
`D_x r_v=t D_x v-r_v D_x v` when `x!=t`. Evaluating the relator gives
`(t-1)D_x v` in that order, while the `t` entry becomes `1-v`.
The derivatives of `w` are exactly `S` and `P_i`; the displayed matrix
therefore has the stated order and no hidden commutation. Its first
coordinate removes `S`, then `t-1`, killing `q_w`; the remaining coordinates
kill every `q_i`. The telescoping identity gives `d1d2=0` by the actual
commutation relations. Finite integral chains embed in the completed chain
spaces, so injection kills ordinary second homology. Simple connectivity
and dimension two give acyclicity; successive Hurewicz and CW Whitehead give
contractibility. This does not mistake a general acyclic space for a
contractible one.

**Dimension and all degrees.** The orthogonal complement of `im d1` consists
of vectors fixed by every generator, hence constant and zero on the infinite
group. The completed image is dense. Finite Hilbert-module rank then gives
dimension 100 both to `ker d1` and to `closure(im d2)`. Their quotient has
dimension zero. The proved classifying-space property makes this the group
calculation, kills degree two by injection and all higher degrees by absence
of cells. Euler characteristic alone would only give `beta1=beta2`; the
candidate explicitly avoids that shortcut. No cost input enters this proof.

**Upper graphing and boundaries.** The null marker correction meets every
`t` orbit and has measure zero. Restricting the 100 `J` generator maps to
the positive-measure marker, plus the full `t` map, supplies every `B` step
through commutation. The 99 initial height `a` maps propagate to the next
source height using `w=u_99 a`. For `k=0,...,M-100` this supplies sources
99 through `M-1`, including wraparound. The proof needs no coprimality
assumption; infimizing over marker measure gives exactly `1+99/M` and
does not claim attainment.

**Positive cost dependency.** Both I and the fresh cost child read/reconstructed
the full primary chain. Compression deletes one indexed edge per excluded
finite supplied class; endpoint splitting makes the many-to-one push a
family of genuine partial isomorphisms with exact summed cost. Deployment
keeps the measure unnormalized and generated factor relations increasing,
and projects at finite stages; it does not take a graphing limit. Normal
form and free displacements exhaust `J`, forcing `kappa` to zero. The exact
finite-model cocycle retains word labels even at colliding endpoints. It
kills every `J` word, and finite cylinder/path tests are fixed before the
model limit. Expectation bounds a generating list for every labeling.

The 99 independent permutation containment estimates leave exponent three;
the fixed-size/geometric-tail split and diagonal fixed-point choice give
the same expanding asymptotically free sequence. Bad overlaps imply fixed
points of a fixed finite list of nonidentity words, including identity-label
boundary cases. Saturation bounds its coefficient alphabet below `n`.
Using the actual subgroup `H` and all its true relations is a legitimate
relative-presentation replacement with inverse generator maps, so coefficient
injection is not an unsupported additional hypothesis. The planar tracks,
minimality, dipoles, exact coefficient gaps and Euler count give two disjoint
long intervals or a full cyclic match. The shortest-loop slide/fold argument
and seam bookkeeping preserve a long original segment. Distinct exterior
indices make its removable arc avoid the surrounding paths; replacing
at least 31 edges by at most 12 preserves rank, connectivity and loop
surjectivity while contradicting minimality. No substantive gap was found
in these mechanisms. The optional stronger curvature discussion retained
in historic supplements is not used by the main result; its new weights
also satisfy the listed face inequalities.

**Classical use, constants and scope.** Gaboriau's published invariance has
no ergodicity requirement, and all spaces here satisfy its standard atomless
probability assumptions. Infinite free orbits justify `beta0=0`; the finite
group example keeps the zeroth correction. Exact integer arithmetic verifies
`2*3^97*96^4<2^183` and `2^61>200`, giving the stated admissible
`eta=1/(100*2^61)`. Arbitrarily large `Y_M` therefore give group infimum
cost one, which satisfies the group equality. Only the relation/action
equality is strict. Infimum one does not assert a cost-one action exists.

## PDF, code, metadata, archive and priority

I rendered and visually inspected all six actual deposited-PDF pages.
Equations, Greek and superscript glyphs, references, page breaks, margins and
font embedding are clean. PDF metadata gives the intended title and Alec
Kriebel as author; no encryption, JavaScript or form appears. Extracted
content matches the manuscript. Rebuilding from the archive with Tectonic
0.16.9 succeeded without warnings; its extracted text is byte-identical to
the actual PDF's text. Timestamp-dependent PDF byte differences are correctly
not claimed reproducible.

The README's exact arithmetic and 329,027-case finite-boundary commands pass
from extraction. The separate constants verifier also passes. The finite
checks state their finite/equal-weight and arithmetic scopes; no code claims
to certify Borel measurability, infinite Hilbert-space injectivity, or the
entire cost theorem. The extra Fox program's algebra passes by import, but
its CLI path fails as F1. Build/software/adaptation receipts are consistent
with the actual source hashes and correctly describe the three guarded
engine-specific upstream metadata primitives.

The archive is free of secrets, credentials, source caches and original
third-party PDFs/TeX. Public-response header strings such as `Vary:
Authorization` are not authentication values. Author/ORCID/date/license,
related identifiers, theorem scope and caveats agree across manuscript,
README and intended Zenodo metadata. CC BY 4.0 is limited to original
material, and third-party sources are attributed through links and hashes.
The local production Zenodo check receipt matches the exact reviewed intended
files; no draft existed in the checked local state. Actual remote publication
and tracker operations remain pending and were not reviewed as completed.

The original short cost-limit proof was already public in the researcher's
preliminary triage, and the fixed-price implication was already explicit in
PSV by 2018. The candidate says so, cites the source free basis, credits
OpenAI's group and positive cost bound, and uses classical attribution.
The direct tree/Fox/classifying-space proof is materially different from
that public cost-limit proof. All-degree vanishing itself is also obtainable
through classical graph-of-spaces/Euler arguments; neither the degree range
nor rational eta creates priority. Qualified eligibility is therefore for
the additional explicit cost-independent proof and reproducible verification
record within the user's requested consequence note. No global novelty,
firstness, general new machinery, or independent fixed-price solution is
certified. The extensive AI/no-human-refereeing/no-formalization disclosure
is accurate and consistent.

## Final status and limitations

Assigned complete-package review completion estimate: **100%**. This is an
estimate of coverage, not evidence of truth. Mathematical reconstruction
found no substantive gap; priority/attribution found no mandatory change;
package reproducibility has the one exact repair F1. A later package must
receive the required fresh independent full review after repair.

This review is automated adversarial evidence. It is not human refereeing,
a formal proof certificate, an exclusion of every possible unnoticed flaw,
or proof of worldwide novelty. The substantial Bernoulli cost input remains
inherited from the explicitly pinned OpenAI source, with its intermediate
source warning preserved. No conclusion is certified by theorem labels,
percentages, successful finite checks, or earlier favorable reviews alone.
