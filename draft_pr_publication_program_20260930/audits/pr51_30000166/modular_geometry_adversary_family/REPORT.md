# PR51 independent modular geometry and priority review

**Verdict: qualified clean. No mandatory mathematical or priority correction.**
The exact all-positive-integer Möbius–totient eta-product question is a known
affirmative theorem. `already_solved`, zero fresh proof-attempt credit, and
one accepted package covering 30000166 and duplicate 30000167 are justified.
No new paper or discovery attribution follows from this review.

Original PR head: `8006dd5f134ad0a2fa930e7278d3cb17945f4201`.
Reviewed mathematical artifact: SOURCE_STATUS.md, 8478 bytes,
SHA-256 `46b114d041624894c9e248e262703e58751c68f68969b3e4ba1a5ca11f23ac62`.
Exact filesystem identities and full modes for all 15 source science files are
recorded in EXTERNAL_BINDINGS.json. Those bindings identify the literal source
snapshot, not a future acceptance state or an original-preparation closure.

## Independence and mechanism

I first read both pinned problem records and SOURCE_STATUS.md. The nearby
README was also read in that initial batch; its existing PASS was treated as
a hypothesis. I did not read the historical independent review or its checker
until after fixing my own route and producing the first actual diagnostic run.
No submitted checker or historical verdict was imported into my code.

The route is holomorphic theta geometry: normal convergence, removable product
poles, a functional equation on the multiplicative elliptic curve, and an
argument-principle zero count. A charged beta-set derivation supplies the
classical core-counting identity with the exact lattice exponent convention.
A completed-square bound certifies the specialized series' local finiteness.
The independent derivation is in ANALYTIC_PROOF.md. The factorization and its
all-N coverage are then checked against those analytic hypotheses. This route
does not infer an infinite theorem from finite coefficient agreement.

## Exact source, duplicate, and priority

The [official 2005 OWR report](https://ems.press/content/serial-article-files/45975)
places the displayed product and the remaining composite question in
Ibukiyama's contribution, printed pp. 54–55. Its numerator is
eta(N tau) to phi(N), and its divisor denominator has Möbius powers. Thus
the formula at SOURCE_STATUS.md:11 and the all-N quantifier match the primary
source. The source's regular-weight-system discussion is separate. Its p. 55
open paragraph is the same composite-case question pinned under 30000167;
the second record supplies no independent broader formula. Duplicate coverage
is confined to this exact source question, not every possible Saito conjecture.

Fresh primary reads of [the 2006 version](https://arxiv.org/pdf/math/0607606v1)
and [the expanded 2007 version](https://arxiv.org/pdf/math/0702027v1)
confirm exact matching of Conjecture 1.1 and the all-N conclusion. The theorem
is not left unresolved merely because its historical statement is labelled a
conjecture. Relevant 2007 proof sections were read in full: core/theta formulas
in section 1, the functional-equation proof in section 2, and all three cases
of section 3. Both arXiv landing pages currently list only v1: 25 July 2006
and 1 February 2007, respectively; neither displayed a withdrawal notice.

Publication identification is corroborated by the publisher's indexed article
record and [Garvan's own publication list](https://qseries.org/fgarvan/publist.html):
*Journal of Number Theory* 128 (2008), no. 6, 1731–1748,
[DOI 10.1016/j.jnt.2007.02.002](https://doi.org/10.1016/j.jnt.2007.02.002).
The direct publisher opening failed; I did not obtain or compare the typeset
journal proof. [Yasuda's 2010 primary paper](https://ems.press/content/serial-article-files/41111),
p. 563, independently credits that specific eta-product result and distinguishes
it from regular systems of weights. This supports attribution, not a substitute
argument. A bounded current search found no relevant correction; irrelevant
search hits are not evidence of exhaustive absence. SOURCE_OBSERVATIONS.json
states exactly what was accessed and what was not independently revalidated.

## Adversarial hypotheses and boundary cases

- **Fourier convention:** SOURCE_STATUS.md:23–29 uses the correct shift
  `(N phi(N)-sum d mu(d))/24`. The extracted OWR text displays denominator
  12 in its prime-case line, inconsistent with its own eta definition. The
  correct 24 follows directly and agrees with Berkovich–Garvan (1.6).
  My screenshot requests did not provide inspectable pixels, so I do not
  claim a fresh visual confirmation of the historical typography.
- **Modularity shortcut:** N=2,3,6 have leading exponents 1/8,1/3,5/12.
  They have nontrivial T multipliers. A blanket integral-character modular
  form argument at level N would therefore be invalid. The PR uses no such
  shortcut; the p>=5 modular/lattice argument in the OWR report is not needed
  or extrapolated. Fourier positivity concerns the specified expansion at
  infinity, not arbitrary other cusps.
- **Theta hypotheses:** normal convergence on C* is Gaussian; all apparent
  denominator poles are removable; a nonzero function with the required
  functional equation has exactly a-1 zeros in a fundamental annulus, while
  the difference has a distinct roots of unity. This verifies the uniqueness
  assertion in SOURCE_STATUS.md:49, including complex q.
- **Formal substitution:** the affine lattice maps are bijective and obey
  the exact exponent shift in lines 63–69. The specialized exponent is a
  positive combination of two nonnegative core energies. The explicit
  coercive bound proves each coefficient is a finite integer sum, validating
  line 71. Substitutions outside 0<r<M produce negative-power witnesses and
  cannot be added casually.
- **Degenerate progressions:** r=M/2 is valid if the two bracket progressions
  retain multiplicity. The new checks include even-M examples and composite
  a=4. The eta factorization itself pairs distinct residues for odd M.
- **Quantifier:** choose p=2 for even N or any prime divisor for odd N, and
  remove its full prime power. The remaining M is odd and coprime to p.
  M=1 uses the core base case rather than residue pairing; N=1 is exactly 1.
  The lifting factor is a t-core series for t=p^(alpha-1), including t=1.
  Other prime powers in M cause no restriction. This validates lines 89–113
  for all positive integers, not merely squarefree or two-prime examples.
- **Coefficient conclusion:** nonnegative means zeros are allowed. The
  two-core coefficient at degree 2 is zero, rejecting strict positivity.

The additional cusp-expression calculations in ANALYTIC_PROOF.md are algebraic
consistency checks, carefully qualified by modularity hypotheses. They are not
used as a general modular-form positivity theorem or as proof of a Dirichlet
character that fails the necessary congruences.

## Actual fresh computations

The final unchanged source ran as actual child **39624** on
2026-10-03T09:49:43.985032+00:00 through
2026-10-03T09:49:44.458432+00:00, exit 0, with empty stderr.
`captures/geometry_exact_v2` retains the source before launch, literal argv,
start/completion records, and complete stdout/stderr. The stdout is 3832 bytes,
SHA-256 `da1e695759054b74593b476129ae238ba95ee00b3de7f518fecee57424614ad5`.
Its **140,708 exact assertions** cover beta-set energies, all affine indices,
specialization near the upper endpoint, certified complete theta coefficients
in eight cases (degrees 36–48), and eta/cusp expressions through N=300.
Binomial-factor convolution is independently implemented; no submitted code
is imported. The result and capture were personally read completely.

The earlier actual child 38813 passed 138,800 assertions in six odd-M theta
cases. Its unchanged launch source and streams remain in `geometry_exact`.
Before finalization I extended the suite to coincident progressions, replaced
set membership with separate multiplicity indicators, and renamed the
multiplier flag to `trivial_T_multiplier`. The first receipt is historical;
the final receipt covers the current source. Neither run is an infinite proof.

## Disposition and limits

No mandatory correction to the source mathematical package was found.
The strongest checked conclusion is the exact known all-N nonnegativity
theorem, with attribution to Berkovich–Garvan and their classical core/theta
foundations. The new derivation makes the analytic and combinatorial foundation
checkable, but is an AI review, not human peer review or a formal proof-assistant
certificate. Existing historical PASS receipts were read for consistency after
the new route and first run; they do not authorize this verdict by inheritance.

This review does not certify the campaign-wide native ledger, root preparation
closure, acceptance operations, future queue edits, merge, DOI, preprint, or
tracker row. Those remain the parent workflow's responsibility.
