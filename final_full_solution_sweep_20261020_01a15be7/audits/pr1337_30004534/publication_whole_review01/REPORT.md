# PR1337: fresh independent whole-publication review 01

**PASS for the exact frozen package reviewed. No substantive mathematical,
priority, reproducibility, citation or presentation objection remains.** One
nonblocking checker diagnostic is documented below. This is one new independent
whole-package review, not the required second review or root publication decision.
No publication, DOI reservation, merge, ledger write or other service mutation was
performed. Overall research estimate remains80%; this review is complete.

The input is publication_preparation_01, closed MANIFEST SHA256
08f11bcaf7dc4b45de2341b1de2fa8e7d8af8eedbdf411e2ef32c5d5df7896db.
All117 listed members and exact file closure were verified at entry and again at
closure. The four-page PDF is64028bytes, SHA256
0885cf6a89f82e819666b379ce04783351bbde54a9362375022851683030960b.
The entire13429-byte TeX source, all18 scientific source-folder files, the source
ZIP and five-member upload kit were reviewed. This review did not modify them.

## Target and universal proof

I freshly retrieved the publisher's original report and verified its bytes match
the cached584600-byte PDF, SHA256
59a81d9c60127680838f293516c7ab2434ccf6624fd373a037d65ecd4c419207.
I read the complete Römer contribution, printed1594–1596, and the separate
working-group discussion, printed1544–1545. The chain, its quantifiers and the
eventual WLP/SLP question match the manuscript. The contribution fixes a field and
any positive row count; the introductory one-row monomial discussion is a special
case. A single fixed infinite F_p(t), c=2 counterexample therefore answers both
unrestricted dichotomies. It does not answer the characteristic-zero or c=1
versions. [Original publisher source](https://ems.press/content/serial-article-files/46866?nt=1).

I challenged each step rather than assuming a claimed solution:

- **Integral dimensions.** The quadratic relations first kill distinct monomials.
  Among the remaining off-diagonal mixed monomials, the difference graph has one
  connected component for each x-index. A reference vertex and its differences
  form an integral basis change of determinant±1. Quotienting by those differences
  leaves a primitive rank-one summand, not a torsion relation involving n−1.
  Different components and the x-squares are disjoint. No linear relation exists;
  all degree≥3 terms vanish. Thus base change preserves the Hilbert function and
  the stated basis. The n=2 empty-difference case is valid.
- **Every form.** In the ordered u,v basis the x-column has u-coefficient a_j and
  v-coefficient B−b_j; the y-column has v_i-coefficient a_i for i≠j. This yields the
  displayed block triangular matrix for arbitrary coefficients, including zero
  x-coefficients and arbitrary nonzero y-coefficients. The determinant identity
  over Z follows by column multilinearity, without semisimplicity, eigenvectors,
  division by n, or a characteristic restriction. Its sign and squared product
  agree with an independent rational Gaussian computation.
- **Failure.** If p divides n−1, the determinant vanishes for every form. The
  degree-one element sum(y_j) is independently nonzero: it has n distinct basis
  coordinates equal to1. Its nonvanishing cannot be replaced by the scalar n.
  Every y_i kills it and every x_i sends it to (n−1)v_i. Equal source/target
  dimensions then force WLP failure for all forms, including after extension.
- **Success and SLP.** At other widths the form sum(x_i) makes the block matrix
  invertible. Its square has a coefficient1 on every independent u_i and survives
  characteristic2, even when p divides n. In socle degree2, the remaining
  nonzero-source/nonzero-target power map is degree0→2. Checking it completes SLP;
  maps to zero spaces have the required maximal rank. SLP entails WLP.
- **Initial width.** At n=1 the quadratic target is one-dimensional, so the uniform
  2n determinant is inapplicable. The displayed basis1,x,y,x² and multiplication by
  x check all adjacent and higher-power maps, in every characteristic.
- **Actual chain.** Every injection carries each generator to the same generator
  type. This covers the extension ideal and its larger symmetric-group translates,
  not merely invariance at individual widths. Repeated-index cubics are included.
  Each generator has support in≤3 columns; the supporting injection can be completed
  to a permutation. The tail is consequently generated from I3. The ideals are not
  selected according to n mod p, and the field and two rows stay fixed.
- **Quantifiers.** For a fixed p, the sequences2+kp(k≥0) and1+kp(k≥1) are both
  unbounded. They are respectively good and bad in the same chain over the same
  infinite field. This defeats both eventual constant truth values. The extension
  assertion follows from the integral basis, universal obstruction and explicit
  prime-field successful form. Killing extra rows consistently extends the example
  to c>2, though this is unnecessary for the counterexample.

No unproved external theorem is required for the construction. The familiar rank,
socle and determinant mechanisms are appropriately described as standard. Finite
checks are correctly distinguished from the written universal argument.

## Independent falsification and package replay

I authored independent_checks.py without importing or executing any earlier PR
claimant or independent-review mathematical checker. It builds the primitive
monomial relation graph and uses rational Gaussian determinants, a materially
different implementation from the supplied unit-pivot relation-matrix/Bareiss code.
All checks use explicit failures, not removable assertions. Normal/-O/-OO outputs
agree exactly, SHA256023783721f98a6910676cbc36c4c7bf4cf9533f2257d88d7d2b9fe071457b87c.

It checks quadratic widths1–13,180 dense nonzero-x integer determinants,60 fixed
width/prime cases for p=2,3,5,7,11, all8332 forms in seven finite-field cases,
435 nonadjacent injections n→n+2, and4858 width-three generator witnesses through
width9. Eleven deliberately false claims are rejected, including omitted relation
families, uniform initial dimension, both incorrect characteristic-two extremes,
vanishing good-width square, y-only success, one zero x-coefficient succeeding,
the wrong bad-width congruence, and treating sum(y_j) as the scalar n.
These are supplementary exact finite diagnostics, not an all-width certificate.

I read the entire supplied exact_checks.py, reproduce.py and build_package.py,
all expected output, provenance, licenses and metadata. The supplied reproduction
passes and internally runs the supplied checker in normal/-O/-OO modes, exactly
matching its sealed output:72 integer cases,2170 forms,872 injections and12 named
false controls. It does not invoke prior author scripts or external services.

I inspected every ZIP entry, rejecting duplicate names, traversal and unexpected
membership, and compared every extracted source byte with the frozen source tree.
The upload kit has precisely the five intended members, each matching its release
counterpart. An extraction inside my own review folder rebuilt all six release
files byte-identically to the reviewed release files. Altering sealed EXPECTED
bytes and adding an extra scientific member each caused explicit rejection; the
restored extraction passed. ROUNDTRIP.json records all23 member readbacks and six
release hashes. No external or third-party source body appears in the public ZIP.

## Priority and duplicate checks

The related Seceleanu–Şega PDF was freshly fetched and matches SHA256
43086ca7367df5762dbfbb61558eb059d842a9fe29731db74a6dcb29ecd2338c.
I independently read its byline/introduction, Theorem B/C, WLP definitions,
chain setup and full Theorem9.2 statement/proof, pages1,4–6,9,33–34. It studies
one-row general symmetric ideals. Theorem B assumes characteristic0 or>n;
Theorem9.2 assumes characteristic0. Neither gives this fixed-positive-characteristic
two-row construction. Its v1 submission date18June2025 and absence of another
listed version are confirmed on the [primary version page](https://arxiv.org/abs/2506.15459v1).
I did not audit the entire paper or use its proof as a premise.

I freshly fetched the FPSAC51 PDF, matching SHA256
ec753e2cca31390bb7e05e8d15f5ddd43da129e4a25c34e29dc44774b50a514d,
and read pages1–2. Its characteristic-zero squarefree/power-of-sum family is
different; no theorem is imported. Cook's journal metadata and abstract were
independently confirmed using the [author's primary preprint record](https://arxiv.org/abs/1111.4979)
after the journal/DOI tool open failed. The manuscript's background citation is
accurate, and its full body is not claimed as audited.

Fresh web searches deliberately varied invariant/symmetric-chain terminology,
eventual behavior, fixed positive characteristic, periodic behavior, socles and
the explicit mixed variables. Results repeatedly led to the original report,
the general symmetric-ideal work, or different algebraic/topological families.
The quadratic-monomial quotient lead was inspected only at title/abstract scope;
it did not authenticate an equivalent construction. Römer's publication page
states that its complete list is available on request; I did not request it or
contact anyone. PRIORITY_REVIEW.json records query/read limits. No worldwide
absence, exhaustive novelty, exclusive firstness or present-openness certificate
is inferred from bounded searches.

Fresh read-only GWS CLI calls bracketed both unformatted-value and formula reads
of numeric gid1254632077, all43 columns and the full1178-row grid. Both responses
had191 populated rows with identical raw value/formula captures; metadata stayed
stable. Exact problem/source/title/PR aliases had no hit. Three broad semantic
leads were read: complete-intersection Sperner theory, allocation theory and a
CP-rank record. Each is distinct from this result. Four fresh native Zenodo exact
phrase queries returned zero. These bounded queries do not prove global absence.
Private captures are retained privately; no row was appended or changed.

A fresh native GitHub read confirms PR1337 remains an open draft at full head
aa737e6da42a3a464761dd5d36de4d1f34781ff4, with no merge and no claimed DOI in
its current description. Its unpublished proof is credited as a source, not
misrepresented as an earlier published solution. Question/dependency DOIs are
correctly references. No same-result publication or solution DOI was authenticated.
The package's modest novelty wording is supported within these explicit limits.

## PDF, metadata, provenance and preservation

I independently rendered the frozen PDF and visually read all four pages. The
equations, symbols, proof, theorem, boundary cases, references and disclosures are
legible and complete, with no clipping, overlap or material layout defect.
PDF_VISUAL_QA.json binds each own PNG. Title, author, ORCID, date/version, scope,
preprint type and two intended scientific uploads agree across TeX, PDF, source,
metadata and deposit proposal. AI assistance in every phase and absence of formal
independent human peer review are explicit. The CC BY prose/MIT code split and
packaging-helper reuse attribution are clear. There is no invented solution DOI.

I independently hash-checked the existing official Tectonic0.17.0 binary and rebuilt
the exact reviewed TeX using cached resources only. A sandbox denied all network
access and all writes outside my own review directory. No install, download or
cache write occurred. Compilation succeeded; the four-page rebuilt PDF's extracted
text is identical to the frozen PDF. PDF bytes differ, as the package explicitly
allows; archive rebuild bytes match exactly. Two underfull bibliography warnings
are harmless. RECOMPILE.json binds invocation, source, compiler and output hashes.

The earlier57-member mathematical review seal
75e8c43616471802659d0fc140030633ebb49af733320bb654086f7d614a7989 was independently
rehashed with exact closure and no errors. Input filesystem metadata and bytes
were snapshotted after read-only work, then compared unchanged at final closure.
The original117-member preparation seal also remained unchanged. All review
writes stayed within this new folder. No Git/index/ref, STATE, case, service,
publication, ledger or unrelated-agent operation was performed. Own retained size
is under8MiB and available-space reserve150MiB was preserved for guarded writes.

## Nonblocking improvement

At verification/exact_checks.py:178, the control
sum_y_is_zero_when_p_divides_n evaluates only `not any([1]*4)`. It is a constant
coordinate observation, not a quotient-derived regression test; it would continue
to say rejected after an unrelated quotient defect. Replace it with actual
degree-one coordinates from the constructed algebra and per-generator products,
while distinguishing p|n from p|(n−1). MINOR_DIAGNOSTIC.json records the exact line.
This does not invalidate the complete elementary degree-one proof, the other
nonvacuous diagnostics or my independent check. I therefore do not treat it as a
substantive publication blocker, nor count it as extra independent evidence.

There are no required scientific repairs from this review. A second fresh
whole-package reviewer and root adoption remain necessary. If the optional
diagnostic is revised, regenerate affected manifests/archives and bind the new
edition before the next reviewer. This PASS conveys no authority to mutate any
account, spreadsheet, PR or publication record.
