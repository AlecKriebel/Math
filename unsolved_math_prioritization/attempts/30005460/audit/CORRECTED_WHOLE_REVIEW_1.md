# Whole-preprint adversarial review 03

**Outcome: no issue requiring repair identified in the exact selected corrected
package.** This is a fresh bounded reviewer conclusion; it is neither ROOT
acceptance nor permission to publish, merge, update a tracker, or act on a provider.
Review date: 6 October 2026. Review completion estimate: 100% of this assigned
review after closure. Original submitted status remains `claimed_solved`, original
head `c0c88b18db237e97a0bddbf28a6d4fdd52af5522`, author budget 2/5; this
review adds no author proof-search turn.

## Exact object and independence

The selector is `ROOT_PREPRINT_PACKAGE_REVIEW_SELECTOR_02.json`, 9498 bytes,
SHA256 `848e9b90c91b9fead53f76f7fc13ee137629b9cbee65b54ecffa341a595b7d56`.
All 23 selected full bodies and all six selected page images were completely
byte-read and authenticated. All selected text/code/JSON bodies were read;
long outputs were recovered in smaller pieces where required. The PDF is
92284 bytes, SHA256 `78930bbd8e727df2de0ca64ac3b5994a7e3392a289bd9058a4fc8dce02fd9e66`;
the ZIP is 28376 bytes, SHA256
`680fb649cc1288684611fd2767334c5c9d9b62f8be086441319539704551033c`.
All 13 ZIP members were fully decompressed, CRC-read, hashed and compared with
their package counterparts. The exact pins and entry identities are retained
in `AUTHENTICATION.json`.

The early independent plan was frozen before any manuscript body or package
note was read, at 11:43:08.522287 UTC. It separated proof/domain attacks,
algebraic certificate attacks, quantitative counting attacks, source/scope and
priority attacks, and artifact/portability attacks. The independent conclusions
were frozen at 11:49:13.148610 UTC, before reading the earlier priority-family
conclusions or ledgers. No earlier whole-preprint REVIEW/VERDICT or ROOT
mathematical/priority assessment was read at any stage. The package itself
contains notes about earlier audits and three selected source-extent repair
records. Those records explicitly expose reviewer02's correction and ROOT's
response. Thus this is independent mathematical checking with disclosed
context, not a claim of a context-free blind review.

After the freeze, I read both priority-family plans, their complete final
reports and limits, Family A's every reading-extent entry, and Family B's full
overlap matrix. I parsed both complete source ledgers and verified all 112
reported source-body/derived-text pins they enumerate. Both families have 41
source entries. I did not independently reread every primary page they read or
reconstruct their entire searches. Their bounded historical findings are not
substituted for this review's proof, certificate or direct primary-source checks.

## Exact target, assumptions and success criterion

The imported original record asks whether the real homogeneous fixed odd-power
SOS-root sets are closed convex cones. The official OWR contribution's printed
page 779 defines the same sets for general positive n and even m. The preceding
ternary examples do not restrict this question to ternary forms. The current
publication defines C(n,m,q) with a prescribed positive odd q, real
coefficients, pointwise nonnegativity, and ordinary polynomial SOS. The claim
tested here is precisely nonconvexity of C(3*10^62,6,3), together with existence
of some finite sextic dimension n(q) for each fixed odd q>=3.

The original submitted RESULT and entire PROOF make the same bounded claim.
The preprint, abstract, README, claim scope, metadata and deposit description
agree. They do not assert ternary failure, a minimum or practical dimension,
one dimension for all odd q, parameter classification, a new seed/cube/tensor
principle, stubbornness of the average, worldwide firstness, or present openness.
The historical source documents' 778--780 citation is preserved rather than
silently rewritten; the corrected current publication gives 778--781.

Successful review requires a checkable finite local certificate and valid
analytical steps from that certificate to the stated theorem, consistent scope
and publication artifacts, and truthful classical credit/provenance. A failed
attack is evidence only within its actual coverage. A mathematical gap,
unjustified scope expansion, stale current artifact, or materially false credit
or reading assertion would require repair. No such unresolved issue was found.

## Adversarial proof analysis

### 1. Product-functional degree control

The central step needs positivity on all squares relevant to S_s^q, not only
on univariate powers of the seed or individually square block expressions.
For m=6 and q=3, its local moment matrix indexes every monomial of degree at
most 9, including lower degrees. A global polynomial H of total degree at
most 9 has each block degree at most 9. Products of two such monomials therefore
have each block degree at most 18. The product functional is defined on this
entire finite per-block domain, so it evaluates every term of H^2 and S_s^3.
The global total-degree matrix is a principal submatrix of the complete tensor
moment matrix. Positivity of real PSD Kronecker products and their principal
submatrices gives precisely the required nonnegativity.

No cancellation of the highest homogeneous components of real square
summands is possible: a nonzero sum of real homogeneous squares cannot be the
zero polynomial. Hence an SOS polynomial of degree <=18 has square summands
of degree <=9. This excludes an SOS representation that tries to escape the
truncated domain using higher-degree summands. The same argument applies at
degree qm for arbitrary fixed q. The proof only uses finite products for a
finite integer s, so no infinite product construction, compactness of measures,
actual random-variable independence, or representing measure is assumed.

A separate two-block order-one exact tensor check confirms the entry rule and
positive leading minors as a finite control. It is not presented as an
enumeration of the enormous N-block matrix. The analytical PSD argument is the
general proof. The negative value on nonnegative p correctly prevents treating
the local functional as a positive measure on real points.

### 2. Separation, normalization and closedness

I tested whether the general-q argument presupposes convexity of the target
SOS-root set or merely transfers its difficulty to an unsupported extension
claim. It does neither. The separated cone is the ordinary finite-dimensional
SOS cone of degree <=2d, which is convex by direct addition of square
representations. Its closedness proof chooses an arbitrary Gram representation
Q_j>=0 for each member of a coefficient-convergent sequence. With a standard
Gaussian monomial Gram matrix G>0, coefficient convergence bounds
tr(Q_j G). The inequality tr(Q_j G)>=lambda_min(G) tr(Q_j) bounds Q_j, giving a
convergent PSD subsequence. A nonzero polynomial has positive Gaussian square
integral, so positive definiteness of G is justified.

A form already known not to be SOS remains outside this larger-degree SOS
cone, because extra high-degree square components cannot cancel. Strong
finite-dimensional separation gives L0(p)<0 with L0 nonnegative on the SOS
cone. Adding epsilon times the Gaussian functional preserves the strict
negative value for sufficiently small positive epsilon, makes the moment
matrix positive definite and makes its value on 1 positive. Division by that
value establishes normalization. This reasoning supplies a new finite-degree
functional for each q; the explicit degree-18 table is never reused beyond
its domain. Thus the general-q argument is not circular.

Closedness of C(n,m,q) is consistent with nonconvexity: the continuous
coefficient power map has this set as its inverse image of the fixed-degree
closed SOS cone. Oddness makes nonnegativity automatic. q=1 remains the
ordinary convex SOS cone; the proof does not falsely extend the seed's
SOS-power membership to q=1 or to even exponents. Classical equality cases
remain unaffected.

### 3. Counting, oddness and finite convex combinations

The labelled-factor expansion assigns each equality pattern of q factors a
set partition pi. Each distinct partition block is assigned to a distinct
variable block in exactly (s)_|pi| ways. These equality patterns partition the
full expansion without double counting. There is exactly one singleton
partition with q blocks. Its leading coefficient is a1^q, which is strictly
negative when a1<0 and q is odd. Every collision term has polynomial degree
at most q-1 in s. All local moments a_j are finite real numbers in the
functional's domain. This proves eventual strict negativity for sufficiently
large finite integer s, without any uniform-in-q estimate.

Reviewer-authored direct enumeration of labelled factors versus independent
set partitions passes for q=1..7 and s=0..3 with abstract test moments. Those
controls include both exponent parities and s below q; the analytical leading
coefficient, rather than the controls, establishes the arbitrary-q claim.
Even q has positive leading coefficient in these controls, as it should.

Each disjoint seed belongs to one common ambient form space and has the
credited SOS power there. If their finite average is outside the target, the
set cannot be convex, because a convex set contains every finite convex
combination by induction. Scalar closure makes sum and average equivalent.
The least failing prefix argument only proves existence of a violating pair:
it never claims a specified prefix belongs to the cone without testing it.
Adding unused variables preserves the counterexample by setting them equal
to zero in any proposed SOS representation.

### 4. Seed, cube and non-SOS obstruction

The seed has coefficient -1, not the stubborn coefficient -3 Motzkin form.
Its three positive monomials are nonnegative and their product is
(x^2 y^2 z^2)^3; AM--GM proves nonnegativity even at vanishing coordinates.
Its displayed cube identity has 16 positive-weight square terms of degree
9. Independent integer expansion of each binomial square, compared with a
multinomial-composition expansion of p^3, gives exact coefficient equality
on all 19 resulting monomials. This independently checks the paper's appendix
and the portability checker rather than accepting a recorded positivity flag.

The local table gives L(p)=1+1+1-4=-1. Since the local matrix is positive
on every nonzero square up to degree18, this excludes an SOS for p itself.
Thus the general-q seed is independently certified non-SOS; the appeal to
historical seed credit does not carry an unsupported mathematical assumption.
For odd q>=3, multiplying the SOS cube by the square p^((q-3)/2)^2 gives
an SOS q-th power, with nonnegative real weights. The exponent identity is
integer-valued exactly in the claimed range.

## Exact local certificate and quantitative falsification

The moment table covers every monomial up to degree18. Coordinate parity
annihilates entries between different parity blocks. There are 220 basis
monomials and eight blocks, four of size35 and four of size20. At order3 the
block dimensions total20. The paper's lexicographic ordering agrees with
the listed initial monomials and all20 leading minors.

The independent checker in this review does not import the portable checker
or earlier review code. It chooses full lexicographic parity-block bases,
clears actual rational denominators, and uses integer fraction-free Bareiss
elimination. All220 full local leading determinants are strictly positive.
The original20 initial minors are separately reproduced. This is a distinct
arithmetic route from the portable Fraction LDL implementation.

For all24 Schur extensions, independently constructed old/new monomial sets
and exact row-pivoted Gauss--Jordan inverses reproduce
tr(G^-1 B^T A^-1 B). Every exact fraction equals the certificate and lies in
[0,T_r). Gaussian G is positive definite; A is positive definite; hence
C=B^T A^-1 B is PSD. Its conjugate by G^-1/2 is PSD, so its largest eigenvalue
is at most its trace. The strict trace inequality gives T_r G-C>0 and the
Schur complement proves positive definiteness. No missing extension block
or numerical eigensolver is involved. The auxiliary fraction-free full-block
test also proves local positivity without depending on the Schur witness.

Independent multinomial expansion recovers a2=11292*10^53 and
a3=35039520*10^116. The exact cubic expression has the required signs and
multiplicities. Its difference from the stated upper bound is exactly
-3N(N-1)(a2-1)<=0. For N=10^62, a3<N^2-1 by exact integer comparison, so
both the upper bound and the actual value are negative. At s=1 and s=2 the
functional values are positive, consistent with the checked seed cube and
the absence of a claim about a specified small pair.

As a separate quantitative control, the independent script uses the integer
discriminant of the resulting quadratic in s and brackets the first integer
where this functional becomes negative:
59192495128212864229346964596861251235354347546945638149589436.
The preceding value is nonnegative, and the first value is negative. This
confirms the chosen sufficient bound has slack. It says nothing about the
first non-SOS sum or a minimum dimension. Complete fractions, determinants,
boundary values and reproducible source are in `DISTINCT_EXACT_RESULTS.json`
and `distinct_exact_checks.py`.

## Publication, portability and provenance correspondence

All13 portable ZIP bodies equal their selected package counterparts. Its
manifest lists12 files, with manifest.json as its explicit sole self-exception.
The manifest is a change detector rather than an independent signature, as
the README expressly says. It intentionally authenticates the portable
archive payload, not the companion PDF by implication. The selector and
assembly receipts authenticate the exact PDF and archive separately.

The isolated extraction runs with `/opt/homebrew/bin/python3 -E -B`. The
portable verifier returns PASS, verifies all12 listed bodies, and its child
checker reproduces the full expected output. A separately recorded direct
checker run also matches all2334 expected bytes with empty stderr. The checker
uses standard-library integer/Fraction arithmetic, independently recomputes
positivity and identities, and does not merely trust JSON success fields.
Its domain is the finite certificate; its output explicitly leaves the
analytical and priority claims to the written review. The Python3.9 statement
is consistent with the APIs used; actual execution here tests the captured
installed interpreter, not every Python release or platform.

Two corruption controls modify only this review's private extraction. Changing
one Schur trace to 1 is rejected by a direct checker run, and the changed full
body is rejected by the manifest verifier. Both native returncodes are1, their
full stderr is retained and they are explicitly expected rejections. The
original private certificate bytes are restored afterward; no selected
author/package/peer file is edited. Original-certificate and checker-basis
provenance pins match retained bodies. No proof-search budget is consumed.

An independent native `pdftotext -layout` extraction yields exactly18467 bytes,
SHA256 `cdaa7d9a63373b441dc83ff6f0c6ea3ad27f606012add373072be5a2cfc0a5d5`,
equal to the retained full output. I directly inspected all six authenticated
pages. Author/ORCID/date, theorem/dimension, all displayed tables, local proof,
negative sign, disclosures, appendix and all seven references are legible and
agree semantically with the source. No clipping, overlap, missing equation,
unreadable glyph or stale source/PDF content was observed. Page6 shows the
corrected OWR contribution range778--781. The initial-minor table and witness
filename wrap remain readable.

Metadata and deposit wrapper use identical metadata, identify an unrefereed
preprint, preserve the theorem's limits, identify extensive AI use, give the
provided ORCID and credit established ingredients. The license does not claim
ownership of earlier results. Build/visual/assembly receipts describe their
historical stage honestly; an earlier visual-pending phase is followed by a
separate visual acceptance rather than misrepresented as a native compiler
guarantee. The native-editor receipt explicitly leaves unknown PID/reap facts
unknown. This reviewer neither recompiled nor edited the selected source; the
PDF extraction and visual inspection are separate checks of the actual PDF.

## Priority, classical credit and the current source-extent repair

My own primary-source readings are precisely listed in the independent freeze
and reading ledger. I directly viewed all seven article pages of BCJ1979,
printed163--169. Lemma1 proves the exact dehomogenized coefficient1 seed;
Proposition2 and Theorems3--4 give duality, closure and separation. The
manuscript correctly credits these earlier ingredients and supplies its own
finite-degree proofs. The earlier paper's measure-convolution discussion is
not silently promoted to this fixed-power averaging theorem.

The OWR operative definition/question is printed779. Its contribution starts
on778 and its bibliography ends on781 before the next contribution. I read
the retained text for PDF38--41 and visually inspected781. The corrected
package records earlier778--780 operative-text/partial-bibliography reading
separately from later reading of the continuation. It does not retrospectively
attribute page781 to Family A or the original source reviewer. The source
version's `whole_paper_body_read=false` refers to the whole workshop report;
the detailed contribution extent is now accurate.

I read the final BKR Sections5--6 and both bibliography pages, PDF20--25,
and Stubborn PDF1--6, including the complete Section2. BKR's final §6 asks
the fixed-exponent question, its p24 supplies the parameterized cube, and
Theorem5.3 raises the sum exponent to k+k'-1. Stubborn Theorem2.2 does the
same on varieties. Equal q gives2q-1 rather than q. The six Stubborn authors
are correct in the current paper and note, and its arXiv1Feb/PDF3Feb dates
are correctly distinguished. The historical family report's abbreviated
link text is not carried into the publication's author listing.

BKS's complete AppendixA and direct-product LemmaA.5 were read. Its
normalization, domain and Gram positivity agree with the paper's credited
use. Acevedo--Blekherman Lemma2.1 and proof on PDF5--6 and Blekherman--Riener
Proposition6.4 on PDF22 are genuine distinct-index/collision asymptotic
precedents. They are presented as prior methods, not asserted to be a
fixed-power counterexample. The current note's tensor predecessor/corroboration
claims are supported by Family B's bounded reading ledger; I did not separately
reread the full Papp thesis or Kapelevich paper and do not claim that I did.

After my independent conclusion freeze, I compared both complete family
reports and all their declared reading extents with the current note. The
only difference between the eight selected current source-version entries
and Family A's historical ledger is the explicitly identified OWR R1
correction. Exact source bytes are unchanged. The reports preserve early
independence and disclose later cross-family leads. They support the package's
bounded description of two extensive priority audits. They do not establish
worldwide absence, full exact-version exclusions for inaccessible bodies,
or that no unpublished resolution exists.

The final Papp--Alizadeh2013 full body remains unavailable, Schmuedgen1979
remains an unreviewed403 body, and the captured Choi--Lam--Reznick1995 scan
is explicitly unread and unused. Partial successor readings, stale author
inventories, imperfect citation indexes and talk abstracts are disclosed.
These are real limits, but no specific competing result is identified in
this bounded evidence, and the preprint makes no stronger priority claim
that would require those exclusions. A material competitor would reopen
priority. Missing bodies are not treated as read and absence of search
results is not used as proof of novelty or present openness.

## Failures, custody and remaining boundaries

Two reviewer-side implementation mistakes are preserved. The first full
authentication run omitted the ZIP's top-level folder when looking up local
counterparts and exited1. The corrected namespace authentication exited0;
this was not a package mismatch. The first independent arithmetic run used
a local denominator1024 in an auxiliary tensor control whose denominator can
be1024^2, and exited1. A generic least-common-denominator correction passed.
No failed attempt is relabeled successful or suppressed. Full prelaunch
source snapshots make the exact failed and corrected programs distinguishable.

Helper-owned substantive native children have explicit argv, actual recorder
and child PIDs, gzip full-body stdout/stderr with both logical/stored hashes,
completed communicate, explicit wait and observed reap. Prelaunch captures
include full reviewer sources, helper source and resolved executable bodies;
large bodies are gzip-compressed, not raw-copied. Direct checker and PDF
extraction input captures are present. The portable verifier internally uses
subprocess.run; its internal checker PID is not independently reported, so
that internal custody is not inferred. Its direct checker is separately
recorded. Outer tool launchers/controller reaping and OS/shared-library
provenance remain UNKNOWN. Visual tools are direct observations, not fabricated
native subprocess records. No native Tectonic compile was needed or claimed.

The strongest verified result is the stated finite-dimensional nonconvexity
theorem and the analytical existence for each fixed odd q>=3, with the exact
local rational certificate independently reproduced. This is an unrefereed
mathematical review, not formal proof-assistant verification or human peer
review. The original target's ternary/minimal/uniform/classification variants
remain outside scope. There is no required global repair from this reviewer.
The whole-folder closure covers every nested file by exact full-byte SHA256,
with only the exact root CLOSURE.json self-exception; files are0444 and
directories0555. Publication actions remain ROOT/human responsibilities.
