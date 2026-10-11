# PR 27: independent homological-family adversarial audit

Target head: `84d7f6103b087e431d7afb751501380ebd7ffd42`. Audit date:
2026-10-01. Mathematical disposition: **verified known partial reduction and
credited layers; the source's unrestricted target is not solved in this packet**.
No novelty or worldwide-current-openness claim is made. This is an independent
AI audit and exact reproduction, not human peer review or formal verification.

## Independence, exact scope, and artifacts

The fixed [early seal](EARLY_INDEPENDENT_SEAL.md) was written before reading
PARTIAL.md, either old script, or review/REVIEW.md. Its SHA-256 is
`2aeb59f66bbd7f3335bf28b47f86b2bfaaaf741c0a2e937860a4d49e4d9417a0`.
Only the root assignment, AGENTS.md, and the literal primary source were used
for that reconstruction. No sibling report was read. The source question,
universal CE splitting, tensor resolution, action, Cauchy transpose, boundary
falsifiers, and remaining multiplicity gap were independently reconstructed
before exposure to the old PASS. No correction to the seal was needed.

All 13 frozen attempt files were read in full and checked against the exact
Git blobs, including bytes, SHA-256 and Git blob OID. The actual base-to-head
diff contains those 13 files plus QUEUE.md, 14 paths in total. The original
main working copy's queued 0/5 row was not confused with the head's unsolved
1/5 row. [PACKET_PROVENANCE_AND_REPLAY.json](PACKET_PROVENANCE_AND_REPLAY.json)
records every comparison, the exact queue line, input hashes, and the two
head commits. No Git mutation, canonical-file mutation, external communication,
PR change, release, or Zenodo operation was performed by this agent.

The audit code [audit_packet.py](audit_packet.py) replays the old scripts only
in `tmp/replay`, because both scripts write adjacent JSON. Its fresh copies of
the two receipts are [replayed_verification.json](replayed_verification.json)
and [replayed_independent_results.json](replayed_independent_results.json).
Both reproduce the frozen receipts byte for byte under `/usr/bin/python3`
(Python 3.9.6) and SymPy 1.14.0. This reproduces current computation; it cannot
attest the historically asserted author/reviewer model, reasoning effort,
independence, timing, or breadth of source reading. Those remain self-reported
in the historical packet.

## Literal primary source and dated literature scope

[OWR 2/2018, printed page 118, Question 13](https://ems.press/content/serial-article-files/46724)
specifies arbitrary finite-dimensional complex E,V and a square-zero algebra
C⊕E. It requests homology expressed as polynomial functors in both variables.
The complete success criterion is an evaluated decomposition in all homogeneous
degrees. The curated source_record's weaker word “preferably,” broad “open”
status, and 2019 citation label are not substituted for the literal 2018 report.
The source packet correctly calls out the first discrepancy in PARTIAL.md.

[The 2017 proposer discussion](https://mathoverflow.net/questions/273196/homology-of-an-interesting-lie-algebra)
already records the exterior coefficient-homology reformulation. Petersen
identifies computing those groups as the remaining difficulty; Tosteson's
June 29 comment supplies the two-term tensor-algebra complex and the adjoint
Whitehouse interpretation. This supports the packet's attribution without
turning those observations into a new result.

I read the relevant primary bodies as well as metadata. [Gadish–Hainaut 2024](https://ahl.centre-mersenne.org/item/10.5802/ahl.213.pdf),
§1.3, printed page 847, states complete decomposition through ten particles
and some eleven-particle data; §4.4 gives the bead-representation dictionary.
[Powell 2023](https://arxiv.org/pdf/2309.07607), introduction and Theorems 1,
3, 4, provides a DG-category structure and a universal two-term complex. Its
introduction explicitly notes that its syzygy formulation supplies no extra
computational information. Neither inspected statement is an unrestricted
irreducible decomposition.

[Powell v4](https://arxiv.org/html/2507.03453v4), dated 16 December 2025,
§2.1, §3.1, Proposition 3.3, Example 3.1 and Theorem 1, gives the precise
coefficient permutations, right-module resolution, cyclic-Lie layer, and
relative degrees one and two used here. Its rational coefficient field and
ungraded place permutations were checked. Crossref publisher metadata gives
online publication 4 March 2026 for DOI
[10.1080/10586458.2025.2608243](https://doi.org/10.1080/10586458.2025.2608243);
the publisher webpage failed through the browser tool, so that exact date was
checked against the publisher-deposited Crossref record, not the failed page.
The [author's publication list](https://math.univ-angers.fr/~powell/home/publi/)
also lists the 2026 journal article.

These are bounded dated source checks. They establish that the inspected
sources provide the credited reductions and specified diagonals; they do not
establish worldwide absence of a later or differently formulated full solution.

## Source-byte provenance qualification

Fresh Gadish–Hainaut and Powell v4 PDFs reproduce the recorded original
checksums exactly. The currently served EMS PDF is 734,914 bytes with SHA-256
`91efb3f45550efd99cbae32c72001ea6b8d40fd0a9c1301c2f524398f9530de5`,
whereas source_checksums.json records 654,519 bytes and
`9d4c4b3ece921051f15c24c23b911839ed968607225fe9244b409960658065be`.
The historical PDF bytes are not in the frozen Git packet. I do not claim a
byte match for this download or infer why the PDFs differ. The fresh PDF's
Question 13 was extracted and visually verified at PDF page index 75,
printed page 118. Its mathematical target matches the independently read web
body. The new download's provenance is recorded separately in
[SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json); original checksum bytes
remain preserved. All foreign PDFs, HTML/metadata responses and rendered
source images remain in this agent's ignored `tmp` directory.

## Universal verification of the CE splitting

Let L=Lie(V), M=L⊗E and h=L⋉M. Square-zero multiplication makes [M,M]=0;
[x,y⊗e]=[x,y]⊗e. The canonical exterior direct-sum identity gives

\[
C_n(h)=\Lambda^n(L\oplus M)
=\bigoplus_{p+q=n}\Lambda^pL\otimes\Lambda^qM.
\]

Choose the wedge identification putting all L factors before the M factors.
The ordinary trivial-coefficient CE differential is

\[
d(z_0\wedge\cdots\wedge z_{n-1})=
\sum_{i<j}(-1)^{i+j+1}[z_i,z_j]\wedge
z_0\wedge\cdots\widehat z_i\cdots\widehat z_j\cdots\wedge z_{n-1}.
\]

An L–L term decreases p by one and preserves q. An L–M term also decreases p
by one and preserves q. An M–M term is zero. Thus q is preserved at chain
level, not only on a filtered spectral sequence. The L–L terms are precisely
the bracket terms of the coefficient CE differential for Λ^qM. For the mixed
pair consisting of L factor i and M factor a, its raw sign is
(-1)^{i+p+a+1}. Moving the new M bracket past p−1 L factors and then a earlier
M factors multiplies by (-1)^{p−1+a}, leaving (-1)^i. Those are exactly the
left-coefficient action terms. Consequently the q summand is the coefficient
CE complex C_*(L;Λ^qM) with all degrees shifted by q, and

\[
H_n(h)\cong\bigoplus_{q=0}^n H_{n-q}(L;\Lambda^qM).
\tag{A}
\]

This is a natural direct-sum homology isomorphism. It does not require
choosing a splitting of spectral-sequence extensions. Even without invoking
reductivity, the chains have already split. E→tE acts by t^q on this summand.

## The free tensor resolution and convention audit

U(L)=T(V). For the trivial **right** T(V)-module C, use

\[
0\to V\otimes T(V)\xrightarrow{\phi}T(V)\xrightarrow\epsilon C\to0,
\qquad\phi(v\otimes a)=va.
\tag{B}
\]

Right linearity is immediate: φ((v⊗a)b)=vab=φ(v⊗a)b. Every nonempty tensor
word has a unique first letter and tail, so φ is a bijection onto ker ε.
This proves exactness in every word length, hence for the ordinary algebraic
direct sum. Both terms are right free. Tensor (B) over T(V) with a **left**
coefficient module N; Tor, equivalently Lie coefficient homology, becomes

\[
V\otimes N\xrightarrow{v\otimes n\mapsto v\cdot n}N,
\]

with no terms above homological degree one. This proof handles arbitrary
coefficient modules, including the infinite-dimensional graded modules here.

The frozen PARTIAL displays T(V)⊗V instead, which is the correct *left*-free
trivial-module resolution, using multiplication on the last letter. The
resulting asserted action complex is correct after passing to the right-module
counterpart (or using the antipode to exchange conventions), as the original
review explains. The text would be clearer and directly checkable if it
displayed (B) and labelled sides explicitly. Simply tensoring its left-free
display with another left module is not a legitimate derivation. This is a
recommended presentation repair, not a counterexample to its formulas.

Putting W_q=Λ^qM and δ_q(v⊗w)=v·w, (A)–(B) prove universally

\[
H_0(h)=\mathbb C,\qquad
H_n(h)\cong\operatorname{coker}\delta_n\oplus\ker\delta_{n-1}\quad(n\ge1).
\tag{C}
\]

The two terms have respective E weights n and n−1. For n=0 the omitted
kernel convention and δ_0=0 give C. For n=1 the second term is V.

## Action, Schur decomposition, grading and naturality

The actual action is the degree-zero derivation

\[
v\cdot\bigwedge_i(x_i\otimes e_i)
=\sum_i(x_1\otimes e_1)\wedge\cdots\wedge([v,x_i]\otimes e_i)
\wedge\cdots\wedge(x_q\otimes e_q).
\]

There is no position-dependent Leibniz sign in this action. Exterior sorting
signs must still be retained. Jacobi establishes the representation law, and
the action commutes with simultaneous ordinary coefficient place permutations.

In characteristic zero, the antisymmetrizer is an exact idempotent. Therefore

\[
W_q=(E^{\otimes q}\otimes L^{\otimes q}\otimes\operatorname{sgn}_q)_{S_q}
=\bigoplus_{\lambda\vdash q} S_\lambda(E)\otimes S_{\lambda'}(L).
\tag{D}
\]

The transpose arises from exactly one exterior sign twist. Equation (D) uses
ordinary exterior powers of ordinary complex vector spaces; no graded Lie
or topological sphere signs are introduced into the source problem. Finite
group coinvariants are exact over C by averaging, so the action homology
commutes with them and with tensoring E^{⊗q}. This proves PARTIAL equation (3)
as an actual module identity, not a character heuristic. It also makes δ_q
componentwise on the E-Schur pieces.

L=⊕_{d≥1}L_d(V) uses bracket-length degree in V. Each fixed degree of every
W_q is finite dimensional, and its degree-d action map has domain
V⊗(W_q)_{d−1}. Exterior and Schur identities can first be applied to finite
truncations of L, then to each stable fixed degree. Each homology degree has
finitely many q, but generally unbounded d; the result is an ordinary locally
finite sum of homogeneous polynomial functors, also called an analytic
functor. No completed tensor algebra, direct product of homogeneous degrees,
topological dual, or continuous homology appears in the source or proof.

Every linear E map induces a square-zero algebra map; every linear V map
induces a free-Lie map. All displayed decompositions and action maps commute
with these, including noninjective maps. Partition lengths exceeding the
evaluation dimension yield zero Schur functors, not exceptional corrections.

## Adjoint layer, credited diagonals, and exact boundaries

H_1(h)=h/[h,h]=(C⊕E)⊗V. For E weight one the coefficient module is E⊗L.
For d≥2, [V,L_{d−1}] spans L_d: expand any Lie word as a bracket, and use
Jacobi to move a generator from the left nested factor outward, reducing that
factor's length. Induction gives surjectivity of V⊗L_{d−1}→L_d. Thus the
kernel is an actual module, with characteristic p_1ℓ_{d−1}−ℓ_d, where the
standard free-Lie Witt characteristic is
ℓ_d=d^{-1}Σ_{a|d}μ(a)p_a^{d/a}. The cited cyclic-Lie identification supplies
the name, not a new rank assumption. The initial kernels Sym²V, Λ³V and
S_(2,2)V agree with both old receipts. E weight one contributes only to H_1
and H_2. It must not be confused with evaluating dim E=1, which retains all q.

The independently checked sign translation of Powell is as follows. On
d=q+1 his coefficient permutation representation is trivial, so (D) turns
it into Λ^qE⊗Sym^{q+1}V, and d≤q contributes no kernel. On d=q+2, q>1,
his sign summand becomes Sym^qE⊗Λ^{q+2}V, while his trivial summand becomes
Λ^qE⊗S_(q,1,1)V. The q=1 exception has just E⊗Λ³V. Tensoring the rational
complex and theorem with C is exact, so these are valid complex functors.
These checks establish PARTIAL equations (4)–(5) in their stated ranges.

All source boundary cases follow from the universal proof:

* E=0 leaves C in H_0, V in H_1 and zero above H_1.
* V=0 leaves C in H_0 and zero positive homology.
* dim V=1 makes L and h abelian. Every δ_q is zero and (C) is precisely
  Λ^n(V⊗(C⊕E))=Λ^n(V⊗E)⊕V⊗Λ^{n−1}(V⊗E).
* q=0 has δ_0=0, and d=0 contributes only H_0=C.
* No nonzero q-fold coefficient can have V degree below q. The first
  possible domain degree of δ_q is q+1, consistently with the quoted theorem.

## Independent finite controls beyond the old receipts

[exact_ce_controls.py](exact_ce_controls.py) imports neither frozen script.
Its free-Lie basis spans commutators over **all binary degree splits** in the
tensor algebra and selects an exact independent basis. This differs from both
the original Lyndon construction and the old reviewer's generator-only basis.
It builds the *full* CE differential using every factor pair of h, checks
d²=0, and compares each actual homology block with an independently built
generator-action kernel/cokernel. It retains E weight throughout.

[NEW_EXACT_CE_RECEIPT.json](NEW_EXACT_CE_RECEIPT.json) records 24 models and
131 nonempty (n,q) CE blocks: V=0, E=0, dim V=1, dim V=2 through degree 5,
and higher ideal-weight degree-4 models including (dim V,dim E)=(3,3),(4,2).
For (4,2), degree 4, the E-weight-2 H_3 has dimension 18, agreeing with
3·dim Λ⁴(C⁴)+dim S_(2,1,1)(C⁴)=3+15. For (3,3), degree 4, E-weight-3 H_4
has dimension 15, while E-weight-2 H_3 has dimension 9. The full-complex
comparison also validates their other nonzero weights, rather than only the
single theorem-predicted kernel.

Twenty-one CE chain-map blocks were checked under V/E shears, swaps and
noninvertible projections. The right-resolution control checks unique first
letter/tail decompositions on 120 augmentation words and 360 right-linearity
equations. Six explicit wrong-side witnesses explain why left/right tensor
orders cannot be interchanged without conventions.

The negative sign control uses a 12→8 action matrix at (dim V,dim E,q,d)
=(2,2,2,3). A spurious position-dependent Leibniz sign and omitted wedge-sorting
sign each change its matrix, yet all three matrices have rank 8. This is a
concrete falsifier of the idea that matching bounded ranks verifies all signs.
The new controls distinguish maps and use chain/naturality equations in
addition to ranks. The universal proof above supplies the arbitrary-degree
reduction; none of these finite checks is promoted to an arbitrary-degree
decomposition or a new theorem.

## Budget, history, exact remaining gap and disposition

The frozen ledger has one substantive turn (2026-09-30 04:40:14 UTC), before
the recorded 06:33 UTC cap, and says the route was blocked. Its known mechanism
transfers the original difficulty to kernels/cokernels of

\[
D_{\lambda,d}:V\otimes S_{\lambda'}(L(V))_{d-1}
\longrightarrow S_{\lambda'}(L(V))_d.
\]

This is not a new solution family; reopening solely to rename those kernels
would be circular. This audit and receipt reproduction do not add a new
substantive discovery attempt. The 1/5 ledger and head QUEUE status are
consistent. Historical duplicate-search breadth and model metadata are not
independently attested by a one-line ledger.

For each λ,d, the exact complex determines only the virtual relation
[coker D]−[ker D]=[target]−[domain]. Without separately evaluating one actual
module, equal virtual differences allow both kernel and cokernel to gain the
same irreducible summand. The credited layers and relative degrees one and
two do not supply general multiplicities for unrestricted d−q. That remains
the exact missing source-level answer. No implicit injectivity, surjectivity,
positivity, spectral-collapse extension, or Euler cancellation argument fills
it here.

The mathematics passes for the stated **known partial** scope. Recommended
concrete editorial repairs are explicit right-module resolution conventions,
separate current versus historical EMS download hashes, and the PR body's
inaccurate assertion that all changed files are inside the attempt directory.
The root coordinator owns those global repairs and the fresh current-head
gate. This report alone does not approve publishing changed bytes or promote
the packet to a full answer. It identifies no substantive mathematical defect
in the stated reduction, adjoint layer, or correctly credited diagonals.

Audit completion estimate: **100% of this homological-family audit**, not
100% of Petersen's research goal. Research discovery remains the verified
known partial reduction with unrestricted multiplicities unevaluated.
