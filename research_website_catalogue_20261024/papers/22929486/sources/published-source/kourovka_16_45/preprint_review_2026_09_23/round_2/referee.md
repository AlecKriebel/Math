# Fresh adversarial preprint review, round 2

Date: 23 September 2026 (UTC). Reviewer: a new OpenAI Codex agent, independent
of the preceding reviewer. Review completion estimate: **100% of this round's
assigned preprint-readiness review**, not a numerical probability that the
theorem is correct.

## Verdict and frozen scope

**Zero actionable findings.** The stated theorem is supported by the complete
mathematical argument and freshly reconstructed exact checks:

\[
|G|=100920,\qquad b_{\mathrm f}(G)=b(G)=3<4=\mu'(G),
\]

for the displayed column-vector action of the specified matrix complement
on \(\mathbf F_{29}^2\). Within the assigned scope, the manuscript is ready
for release as an **unrefereed preprint**. I found no mathematical gap,
incorrect explicit datum, reproduction failure, or substantive delivery
defect requiring another repair round. No optional stylistic preference is
being treated as a finding.

The full source and every rendered page of the nine-page PDF were reviewed.
The exact reviewed inputs were:

| File | SHA-256 |
|---|---|
| `proof.tex` | `2c74f1291c165dbefe72ebddda0b0a47784b8202811b162cc4496d59acd04af4` |
| `proof.pdf` | `6225ed0ba605c1014c0e5e4954d97011f33eb8fa4c2b6243e4d071d5d82122df` |
| `submission/build_package.py` | `4c87c5ecf27f93499c17dd9497c32405fc4e9a9ffc95d9b199ff8e3fc238e59a` |
| Source/verification v1.0.1 ZIP | `ce3ec2de9e7921115f7e1e21b0392e85ca1d8b11746be508db574a0d16318e85` |
| Zenodo kit v1.0.1 ZIP | `b823679c7511e6ebb9ff5166b4539ec9d467d983254726066a0fd8eca839c156` |
| Local website `index.html` | `d88ec415bb6cbdaf80b5f32bcb1812c569c98ac0c4da16057cf067c9cbdf9bd4` |

The frozen `input_proof.*` copies and live manuscript had identical hashes.
The local website PDF and both downloadable ZIPs were byte-identical to the
reviewed manuscript and archives; full delivery hashes are in
`reviewed_delivery_hashes.json`. The remote public website was outside this
round's deployment check because it was intentionally still serving the
preceding release. Closing review-status metadata and including this report
will change the final ZIP hashes. Those final delivery hashes must be recorded
separately; the theorem verdict attaches to the manuscript hashes above.

## Independence and method

I read the manuscript in full and completed the independent mathematical pass
before inspecting the supplied verification implementations or their results.
I did not read the earlier reviewers' verdicts, reports, or findings. I then
wrote `independent_check.py` from the printed generators and witnesses, without
importing project code or reading any saved group tables or certificates.
Its exact calculations passed before I read the supplied Python/C++ code.
I subsequently inspected that code, the supplied audit scripts, the package
builder, the upload metadata, and the local paper page, and replayed the
documented workflow in a temporary extraction of the reviewed source ZIP.

No external researcher was contacted, no canonical proof or software was
edited, and no Git operation or publication action was performed by this
reviewer. Temporary extracted files, downloaded primary sources, and rendered
pages were kept in the ignored round-2 scratch directory.

## Section-by-section mathematical assessment

### Abstract and Section 1: definitions and subgroup formulations

The exact claim is an all-actions invariant, with bases taken for the
permutation image and minimality meaning inclusion-minimality. Allowing
independent subsets that need not generate the ambient group is explicit.
The faithful invariant is separately defined and not silently substituted
for the all-actions invariant. The trivial-group and empty-family conventions
are coherent, and infinite underlying sets introduce no infinite minimal
bases for finite permutation images.

Proposition 1's converse uses the left-coset action correctly: its kernel is
the intersection of the subgroup cores, hence the core of the common
intersection. Normality of that intersection is precisely what makes it the
kernel. The chosen identity cosets give the stated minimal base. Passing to
faithful actions of quotients yields the displayed maximum formula without
assuming either subgroup monotonicity of `b` or a quotient by a nonnormal
subgroup.

The two directions of the meet-irredundance/independence lemma are valid,
including the singleton case. The restriction witnesses lie in the subgroup
being restricted to, so the restricted family stays essential and keeps the
same total intersection. Its empty-family case uses that subgroup as the
ambient intersection. The faithful strengthening follows exactly when the
bottom is the identity.

The Boolean mapping uses complements of index sets, preserves meets and top,
and is injective by the witnesses. There is no illicit assertion about joins
or about the bottom being normal. The use of this mapping agrees with the
primary formulations checked below.

### Section 2: the complement and its invariants

The determinant conditions, triangle relations, and nontrivial projective
image establish the order via the stated standard presentation and simplicity
of \(A_5\). The finite alternative independently confirms both the quotient
map and the claimed \(\mathrm{SL}_2(5)\) isomorphism, so this identification
does not rest on a group catalogue or an unverified abstract extension claim.

The elementary description of proper \(A_5\) subgroups is sufficient and
correct. An intransitive subgroup either fixes a point or lies in the even
part of the \(2+3\) set stabilizer. The proper transitive orders listed are
the possible proper divisors of 60 divisible by 5; Sylow theory and the
normalizer exclude 15 and 20, and the index-two argument excludes 30.
The independence bounds for \(A_4,D_{10},S_3\), followed by deleting a member
of an independent set, give the advertised upper bound for \(A_5\).

The unique-involution argument applies because the characteristic is odd and
the determinant is one. Thus every even-order subgroup contains \(Z\), while
the odd-order possibilities are exactly trivial, order 3, or order 5. If an
independent set becomes dependent as an indexed family modulo \(Z\), the
omission subgroup cannot contain \(Z\); this is the essential step giving
the stronger bound in that case. It does not confuse set independence with
an image having duplicated elements.

The faithful base bound uses an odd-order member in any identity-intersection
family, then a second member disjoint from that prime-order member. This
correctly gives \(b_{\mathrm f}(H)=2\), while a normal-bottom triple gives
\(b(H)=3\). The printed words for \(R_2,R_3\), their squares, all pair
orders, and the corrected product orders \(4,3,10\) were recomputed. Their
projective orders are \(2,3,5\), and the dihedral and intersection arguments
are valid. In particular, the last pair cannot contain \(R_3\), since the
triple generates order 120 whereas that pair has order 20. The triple
intersection is precisely \(Z\), not the identity.

### Section 3: the scalar and line-stabilizer lemmas

The scalar lemma includes the trivial cyclic 2-subgroup. For nontrivial
projection, a generating family must contain an element projecting to a
generator of the cyclic 2-group. Its geometric sum is zero because the
scalar is not one, so it generates a complement. Any generator outside that
complement, together with it, generates the whole subgroup. This proves the
independence bound for every subgroup rather than only the ambient affine
line group. Primality of the translation order and the 2-group condition are
used at the stated steps.

For a line stabilizer in \(H\), the kernel of scalar restriction consists
of determinant-one unipotent matrices. A nonidentity such matrix would have
order 29, impossible in order 120. The injective restriction into
\(\mathbf F_{29}^{\times}\) gives a cyclic group of order dividing 4.
Irreducibility follows. Exact enumeration confirms all 30 actual line
stabilizers have order 4 and are cyclic.

### Section 4: every affine subgroup and every action

The multiplication convention agrees with all matrices and witnesses. Since
29 is prime, additive translation subgroups are vector subspaces. A subgroup
missing \(V\) has translation intersection either zero or a line. In the
zero case it embeds into \(H\), and both independence and the faithful
base invariant have the required subgroup monotonicity. In the line case,
its projection is a cyclic 2-group of order dividing 4. A Sylow 2-subgroup
maps isomorphically onto that projection and complements the line; scalar
restriction is faithful. The preceding affine-line lemma therefore applies.
No assumption that an arbitrary complement is the displayed zero-translation
one is needed.

Proposition 8 chooses a family member missing \(V\) and applies the faithful
restriction bound, giving at most three members. Proposition 9's normality
argument is complete: \(N\cap V\) is an invariant subspace; if trivial,
normality gives \([N,V]=1\), and the faithful matrix action gives
\(C_G(V)=V\). This forces \(N=1\). Every nontrivial kernel therefore
contains \(V\), so nonfaithful actions are actions of \(H\), whose
all-actions invariant is three. This is a universal structural proof, not
an inference from enumeration of selected affine subgroups.

### Section 5: attained bounds and exact independence

Projection witnesses independence of each of the three linear elements in
the four-set; the translation is outside the zero-translation complement.
Irreducibility gives generation of all translations. Each pair complement
has order exceeding four, so cannot stabilize a line, which justifies the
three full-translation omission subgroups and their printed orders.

For the upper independence bound, an intersection family all of whose
members contain \(V\) descends irredundantly to \(H\). Otherwise restriction
to a member missing \(V\) gives the bound of four (or three in the line
case). No assumption on normality of the total intersection is introduced.

The three explicit affine subgroups have order 58, the exact printed
pairwise intersections, and trivial triple intersection. They consequently
give a faithful minimal three-base in the disjoint coset union, with degree
5220. These exact sets were recomputed, not merely their orders. The theorem
follows with both equalities attained.

### Section 6: the normality obstruction and cores

The four omission subgroups meet in the displayed embedded \(Z_0\). The
translation conjugate is exactly \((2e_1,-I)\), so \(Z_0\) is nonnormal.
The pair cores in \(H\) are \(Z\), using simplicity of the quotient and
the fact that the pair subgroups contain \(Z\). Their affine preimages have
cores \(V\rtimes Z\). The complement core is trivial by the already proved
normal-subgroup fact. Passing to cores destroys essentiality exactly as
claimed. No normality claim is imported from centrality in the complement.

### Section 7: finite certification and characteristic boundary

The subgroup-adjoining search is exhaustive: follow a generating sequence of
any subgroup from the identity. Every required next generator is tried.
An irredundant family of size greater than four contains an irredundant
four-subfamily, so the four-family exclusion suffices for all larger ranks.
Together with the faithful three-family check and explicit lower witnesses,
the finite conclusions for \(H\) are valid. Proper-subgroup families suffice
because an ambient-group member is redundant in any nonempty multi-member
family.

The fresh checker found 76 actual subgroups, rejected all 1,215,450
four-families as redundant, and found no faithful irredundant three-family
among all 67,525 triples. It independently generated the 100920-element
affine group and all omission and base subgroups. Complete subgroup sets
agree as sets of matrices with both fresh supplied implementations and both
archived certificates, not just in their order distribution.

The printed characteristic-11 matrix \(C\) lies in the printed complement,
has order 10, and preserves the stated distinct lines. Its four subgroup
families have trivial total intersection and deletion orders 11, 11, 5, 2.
This boundary example is correct. The text's refusal to generalize the
29-characteristic argument indiscriminately is mathematically justified.
Exploratory floating-point optimization is not used in any proof step.

### Author statement, bibliography, and PDF

Attribution, AI assistance, unrefereed status, and the distinction between
finite checking and structural proof are stated accurately. No minimum-order
or exhaustive novelty claim is made. All nine PDF pages were rendered and
visually inspected: equations, table, theorem statements, references, page
numbers, and links are readable, with no clipping or overlapping text found.
The extracted PDF text matches the source's substantive content. A clean
`make pdf` build succeeds, and its extracted text is identical to that of
the reviewed PDF.

## Primary-source checks

I checked the notebook's current printed page 100 and relevant definitions in
Cameron's primary works, rather than relying on old review summaries:

- [September 2026 notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21tkt.pdf):
  Problem 16.45 asks the displayed equality and states the normal-bottom
  semilattice equivalent. No solution is attached to that problem there.
  The [separate update](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf)
  does not mention 16.45.
- [2010 exposition](https://cameroncounts.wordpress.com/2010/07/22/the-symmetric-group-7/):
  the notation and permission for nonfaithful, intransitive actions agree
  with the manuscript's comparison.
- [2014 preprint](https://arxiv.org/pdf/1408.0968): Section 2 explicitly allows
  nonfaithful representations; Section 3 uses the action kernel and normal
  bottom in the coset-action formulation. The cited proposition numbering
  agrees with the source.
- [2024 published account](https://msp.org/mt/2024/3-2/mt-v3-n2-p08-s.pdf):
  pages 428–429 use \(b_2\) and \(\mu^\uparrow\), allow nonfaithful
  representations, and state the corresponding normal-bottom condition.
  The title, journal, volume, issue, pages, and DOI agree.

These checks validate the interpretation of the target problem and the
manuscript's bounded literature statement. They are not a claim to have
exhausted all possible earlier unpublished or published solutions.

## Reproducibility and delivery checks

Before replay, every one of the 150 source payload checksums and corresponding
manifest byte lengths passed; all eight kit payload checksums passed. The
kit has precisely the two documented upload files, and both are identical
to the reviewed PDF and source ZIP. Results are in `package_integrity.json`.

From a fresh extraction, `make audit` completed successfully. This includes
`make verify`, the independently implemented Python and C++17 reconstruction,
their subgroup-set comparison, the supplied additional checker, the supplied
structural checker, and comparison against the archived and fresh
certificates. `submission/test_package.py` passed its stale-output isolation,
exactly-two-upload-files, checksum, and deterministic-rebuild checks. The
builder uses an explicit kit member map; it neither sweeps an old output
directory into the kit nor deletes preexisting working upload files.

The run used Python 3.14.6 and Apple Clang 21.0.0. The principal verifiers use
explicit checks. The additional audit scripts use assertions, and the README
and local website correctly tell readers to avoid Python's optimization flag
for those scripts. No nonstandard Python dependency, optimizer, catalogue,
or remote service was required for the replay. The independent round-2
checker also uses explicit checks and remains usable in a packaged source
tree where the duplicate frozen input manuscripts are omitted.

The local website's theorem, definitions, proof outline, reproduction commands,
review qualifications, and version agree with the manuscript and package.
The README, citation metadata, upload guide, and descriptive metadata agree
on version 1.0.1, author/ORCID, date, unrefereed status, and the absence of a
claimed deposit/DOI. The author-selected license field remains honestly unset;
that is a documented manual deposit choice, not a mathematical or packaging
defect within this review. I did not treat the expected final-review and
deployment-status updates as findings.

## Remaining gaps and strongest supported result

**No unresolved actionable proof or reproduction gap was identified.** The
strongest supported mathematical result is the exact displayed theorem for
the explicit group, including all faithful and nonfaithful actions. The
abstract structural arguments remain ordinary mathematical proofs reviewed
by an AI agent, not proof-assistant theorems. The large affine subgroup
lattice was not enumerated, because the universal bound is proved
structurally. This review does not establish minimal possible group order,
unqualified bibliographic priority, external human peer review, or a Zenodo
deposit; none is claimed as a theorem premise.

Final administrative closure, final ZIP rebuilding to include this report,
final hash recording, and deployment are tasks for the parent workflow.
They do not change this zero-actionable verdict on the frozen manuscript.

## Checkable artifacts from this round

- `independent_check.py`, `independent_check.log`, `independent_results.json`:
  fresh reconstruction and all finite checks from the printed inputs.
- `independent_subgroups.json`: complete actual-matrix subgroup set.
- `cross_implementation_comparison.json`: equality with supplied fresh and
  archived subgroup sets.
- `package_integrity.json`, `reviewed_delivery_hashes.json`: pre-replay
  checksums, manifest checks, and exact reviewed delivery identities.
- `package_make_audit.log`, `package_regression.log`, `package_pdf_build.log`:
  clean-extraction replay, packaging regression, and source-to-PDF build.
- `findings.json`, `research_log.md`: machine-readable verdict and checkpoints.
