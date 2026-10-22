# Second fresh whole-package adversarial review: PR1337

**PASS. No remaining substantive mathematical, scope, priority-attribution,
reproducibility, bibliographic, or presentation objection was found in the exact
revised preparation02 package.** This accepts an independent scientific review
role only. Root adoption, current prepublication duplicate checks, integration,
publication, DOI/file verification, and tracker recording remain separate.
It is an AI review, not independent human peer review or formal verification.
Assigned review100%; overall sweep80%.

## Exact reviewed package and independence

Preparation02 MANIFEST.json hashes to
`133d668fa299623611e989802ed3aee10904efbc6cb0a2c4b68379b43c432c36`.
Its63 payload members and complete closed membership were read back. The four-page
PDF is64,028bytes, SHA256
`0885cf6a89f82e819666b379ce04783351bbde54a9362375022851683030960b`.
The revised scientific ZIP is
`b8e275c921f9b63babcf4cd3287763c7f6e144afa2b8ba927ab61894ced74770`;
the upload kit is
`083f2fb702d49c0a0f497ae894a91c095080c4098dcc78dd448ecec52e4d92e3`.

I read the complete final TeX manuscript and every text/code member of the
18-member scientific source, including both full metadata representations,
source/read-limit provenance, licenses, reproduction/build code, expected
diagnostics, and public manifest. I read the complete bounded-repair report and
changeset. The earlier review's verdict is not counted as my mathematical
verification. My numerical mechanism is a new monomial connected-component
quotient, independent of the preparer's unit-pivot elimination and of all
claimant or earlier reviewer programs. I did not execute claimant programs.
I separately executed the supplied publication checker through its documented
reproduction/build entry points after reading it.

The supplied baseline already binds the188 old files in preparation01 and the
first whole review, including their seals. My additional baseline/readback
checks both old packets and preparation02:252 files in total, with complete
bytes, modes and integer nanosecond mtimes, plus directories. Preparation
manifests originally certify byte/hash membership; I do not retroactively
describe them as original mode/mtime seals. The first whole-review seal does
include those attributes. Final preservation receipt records my new baseline's
stronger readback. No old file or source was edited.

## Original problem and quantifiers

The actual publisher PDF's printed1594–1596 were freshly extracted and visually
inspected. Römer explicitly fixes a field and an arbitrary fixed number of rows,
with column permutations and compatibility between widths. His final Artinian
question concerns eventual WLP/SLP truth or failure. I also read the report's
opening and separate working-group discussion: its one-row monomial focus does
not amend that contribution's setup. No global characteristic-zero restriction
was found. The new construction is therefore within the unrestricted target.
This does not certify a negative answer for a one-row, monomial-only, Gorenstein,
or characteristic-zero variant. The note states those limits correctly.
[Original publisher source](https://ems.press/content/serial-article-files/46866).

The intended output is a counterexample to eventual constancy, not a complete
classification of all chains. The note supplies one fixed chain over one fixed
infinite field. It does not change the characteristic with the width. Its
successful forms already lie over the prime field, so existence over a finite
field and genericity over an infinite field are not confused.

## Independent universal proof reconstruction and attacks

View the quadratic monomials as vertices of a graph. Delete off-diagonal xx,
all yy, and diagonal xy vertices. Each remaining binomial relation identifies
two mixed vertices with the same x index. For each x index there is exactly one
mixed connected component, provided the width is at least two. Its relation
lattice consists of differences of vertices and is saturated: choosing a
spanning tree eliminates one vertex at a time with coefficient1. Distinct
components and each x-square remain independent. This proves the integral
quadratic quotient is free of rank2n, independently of characteristic. Degree
one has its original2n generators, and all degree-three and higher monomials
are zero. At width one the quadratic rank is instead1. This independently
establishes the manuscript's Hilbert functions and rules out hidden torsion or
characteristic-dependent loss of its displayed basis.

Direct polynomial convolution gives the image of each raw generator under an
arbitrary linear form. The x-square coefficients give the diagonal upper block;
the remaining mixed coefficients in a y column are all x coefficients except
the matching one. Thus the lower diagonal block is D(a)(J-I); the b coefficients
affect only the lower-left block. Block triangularity removes that block from
the determinant. Multilinearity in the columns of J-I leaves only the term
with no all-ones column and the n terms with exactly one such column. Their sum
is (-1)^(n-1)(n-1). This is an identity over the integers, so it remains valid
over every field and every extension, including when n itself vanishes.
No diagonalization, division by n, or restriction to invariant forms is needed.

When p divides n-1, the actual degree-one vector z=sum(y_i) is nonzero because
there are no linear relations. Every generator kills it: the y products are
zero and each x product has n-1 identical mixed terms. This is a universal
common-kernel obstruction, including for linear forms over an extension. The
potential confusion z=n times one vector is invalid; its summands are distinct
basis vectors. I tested that confusion in both the repaired diagnostic and my
independent checks.

At every other width, ell=sum(x_i) has invertible degree-one-to-two
multiplication. Its degree-zero-to-one map is injective. Its square is the sum
of distinct independent x-square classes, and is nonzero even in characteristic
two. This checks the only extra positive-power map with nonzero target needed
for SLP. All remaining maps either were checked or have zero target. Since SLP
implies WLP, the common classification is complete. At width one, the separate
basis1,x,y,x^2 gives the asserted strong element x directly. In particular the
exceptional width one has not been incorrectly included in the bad congruence.

The ideal generators are genuinely equivariant under all injections of columns.
Every cubic, even with repeated variables, has at most three supporting columns;
the same is true of every quadratic relation. Compress those supporting columns
into width three, preserving row indices and repetitions, then extend its
inverse to a permutation at the target width. This proves orbit generation
from the single fixed width-three ideal. Arbitrarily selecting unrelated
algebras according to n modulo p is not the mechanism. Over F_p(t), widths
2+kp and1+kp give unbounded good and bad subsequences, respectively. This
proves failure of each unrestricted eventual dichotomy.

I found no central unsupported lemma, circular reduction, missing characteristic
case, field-extension exception, or incompatibility in this proof. Its elementary
determinant/socle tools are standard; the note does not claim a new general tool.

## Independent quantitative falsification

My new standard-library program constructs the quadratic quotient by graph
components, then computes products directly. Rational Gaussian elimination
computes integer determinants independently of the preparer's Bareiss routine.
Finite-field elimination includes an independently implemented F4 using
F2[w]/(w^2+w+1), so extension-field checks do not merely repeat prime-field
samples. The three normal/-O/-OO runs have identical output SHA256
`c4dc510b09cc2911d0cd5391bbc1a1e57544d24db6430247f23d4b1743a5d472`.

- 153 integer arbitrary-form determinant cases at widths2–10, with independently
 recovered orientation of the displayed integral basis.
- 29,296 finite-field forms. These include exhaustive coefficients at several
 widths over F2,F3,F5 and exhaustive F4 checks at widths2/3, with further
 larger-width and extension samples. Both singular and nonsingular residues
 are included.
- 289 injections and31,406 generator images, with3,124 generator compressions
 checking width-three generation through width eight.
- Seven false assertions rejected, including omitted yy relations, identifying
 different mixed rows, the wrong initial Hilbert function, confusing all forms
 with existence of one form, characteristic-two square cancellation, the wrong
 bad congruence, and reliance on prime-field points alone.

Counts describe finite conditions and parameter substitutions, not independent
scientific discoveries or a formal proof. They supplement the universal argument.

## Revised diagnostic, archives, and presentation

The repaired sum-y test actually obtains degree-one coordinates from the
presentation and multiplies them through the constructed quadratic quotient.
It tests widths3/4 in characteristic2, where dividing n-1 and dividing n differ.
Its false linear relation sum(y)=0 is rejected. I found no remaining substantive
diagnostic issue. All13 publication-package false controls pass as intended.

I verified CRC and every byte of all18 source ZIP and five kit members, with
safe relative regular-file paths. The kit contains exactly the scientific PDF,
scientific ZIP, matching metadata and deposit proposal, and upload instructions.
It contains no private captures, downloaded manuscripts, credentials or operations
driver. I freshly extracted the source, ran its reproduction entry point, and
rebuilt all six releases byte-identically. Three additional corruptions, each in
normal/-O/-OO modes, are rejected: changed TeX, an unexpected member, and an
incorrect expected result with its byte manifest correspondingly updated. All
own corruption copies were restored to the immutable source bytes afterward.

The existing pinned Tectonic binary was independently rehashed and run once
with cached-only/untrusted flags under a macOS policy denying network and all
writes outside this review. It succeeded. The regenerated PDF has identical
complete extracted text; byte-identical TeX recompilation is not claimed, and
the frozen reviewed PDF remains unchanged. I independently rendered and visually
inspected all four final pages: equations, references, links, pagination and
disclosures are legible, without clipping, overlap or missing glyphs. I also
rendered and inspected the three original-problem pages.

Metadata, paper, source and deposit agree on the title, author/ORCID, date,
version, scientific scope and two upload files. The manuscript's all-phase AI
disclosure, unrefereed status and absence of independent human peer review are
explicit. Prose/code licenses and attribution are consistent. Crossref confirms
the Cook title, author suffixII, volume369, pages42–58 and2012 date. Its body is
not imported into this proof.

## Independent priority challenge and limits

Fresh numeric-tab GWS CLI checks at14:02UTC covered191 rows and all43 columns,
with strictly equal complete value/formula responses and stable full metadata.
The single ledger/local-state lead is the characteristic-zero complete-
intersection Sperner note23204810, expressly excluding a Lefschetz theorem;
it is not this result. Four fresh public queries had no exact target hit. A
large Clay-attractor metadata hit uses Lefschetz in Hodge contexts; targeted
context reading identified no same result. Its full immense description was
not claimed read. No row or service was changed.

I independently read the actual Seceleanu–Şega v1 introduction, TheoremB,
chain setup and complete Theorem9.2 proof, from freshly re-extracted pinned PDF
bytes. B is a positive WLP theorem for one-row general ideals with char0 or
char>n;9.2 assumes char0. These do not answer the present fixed-positive-
characteristic two-row question. The current primary arXiv page identifies v1
submitted18June2025. None of its theorems is a premise of this elementary proof.
[Primary preprint](https://arxiv.org/abs/2506.15459v1).

Additional primary leads were deliberately checked under different terminology.
McDaniel–Watanabe's actual Theorem1.8 and WLP section concern the quadratic
monomial complete intersection and a characteristic threshold. In the inspected
family, fixed characteristic eventually fails; it does not give recurrent good
and bad widths. Larson–Stapledon's actual Examples5.1/5.2 give local-face-module
tensor-product failures beyond thresholds. Those are relevant antecedents for
characteristic-sensitive failures, but supply no inspected equivariant chain
with unbounded good and bad widths. The2020 symmetric-ideal survey's introduction
and complete term/heading search concern other asymptotic invariants and give no
Lefschetz statement. Exact reading extents, URLs and hashes are in SOURCE_INDEX.md;
their full bodies are not all claimed audited.

The20 actual query formulations in PRIORITY_SEARCH_LOG.md cover the original
question, invariant-chain/asymptotic terminology, periodic WLP, positive
characteristic, related authors and alternative source families. No earlier
full original-question negative, equivalent complete construction, or solution
DOI was authenticated. Search absence does not certify exhaustive novelty,
exclusive discovery priority or worldwide current openness. These are already
disclaimed in the paper. I found no material contradiction to its modest
construction/negative-answer claim or missing attribution requiring a repair.
The unpublished own PR is not an existing publication; no source-only tracker
row is proposed as a substitute for publishing the note.

## Preservation and final disposition

All writes were confined to this new review folder; original source, packages,
prior reviews, toolchain and caches were not changed. No outside person or
unrelated agent was contacted. No credentials, Zenodo write, GWS write, Git
mutation, production CASE or approval/action authority was used. The initial
gws-shared skill prerequisite was absent; it was not generated, and the actual
read-only raw CLI was used with explicit numeric-tab/schema checks. An initial
attempt to print the huge unrelated native metadata was truncated; the report
does not count that as a full reading, and the exact relevant contexts were
subsequently read separately.

The final closed review binds every own payload, including private evidence,
and complete byte/mode/nsmtime membership. Own storage remains below6MiB and
guarded writes preserve the150MiB free-space reserve. Final preservation and
seal verification receipts provide the exact counts and hashes. The reviewed
preparation02 scientific package has no remaining substantive objection from
this second independent whole review. Root should adopt only the exact reviewed
hashes and perform the current live publication/accounting gates separately.
