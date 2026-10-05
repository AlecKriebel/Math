# Independent adversarial audit: rank 745, ID 30004169

## Verdict and mandatory corrections

**PASS, scoped to an unresolved five-approach research packet.** All nine author
files were read. The mathematical statements actually asserted in PROOFS §§1-6
survive the checks below. No mandatory mathematical or provenance correction was
identified. The author freeze was not edited.

**Original problem: unresolved, 5/5 approaches used.** The packet neither proves
nor disproves general integral Milnor-Witt BLRS Zariski descent. Its bounded
literature search is not evidence that no resolution exists anywhere. PASS must
not be restated as “the conjecture passed,” “descent proved,” or “counterexample
verified.” The surviving gap is precisely the acyclicity of the lower-part
augmented Čech defect for arbitrary X and positive weight.

## 1. Identity, regime, definitions, and indexing

The primary question was independently checked in the freshly retrieved OWR
29/2019 PDF, printed p.1776, including a rendered visual inspection. The target
is the spliced Bloch-Levine-Rost-Schmid complex. Smooth finite-type schemes over
a perfect field of characteristic different from 2, q >= 0, and integral
coefficients are the stated regime. The usual separated convention is sufficient
for the packet's cover construction. The comparison is with derived Zariski
global sections, not merely with termwise associated sheaves.

Definition 4.1 and the adjoining discussion of Bachmann-Yakerson were checked
against the freshly retrieved published PDF, with visual inspection of p.1995.
The author preserves the degree-q kernel, the residue tail, the face condition in
each ambient face, and the endpoint splice. No low-degree supported boundaries
are quotiented out: q-good supports have codimension at least q in the whole
simplex, so their support complex is zero below degree q. Unions of finitely many
q-good supports remain q-good; this gives the filtered system and the injective
kernel description used later. Higher-codimension extra support cannot identify
away a nonzero generic degree-q coefficient.

The intrinsic line is the determinant of the normal space, equivalently the
inverse conormal determinant. The stated Kähler-differential expression has the
correct dual. GW in degree q and Witt-theoretic negative Milnor-Witt terms beyond
q are retained. The distinct indices are coherent: BLRS degree i has motivic
degree q+i; higher Chow-Witt index n means i=q-n and motivic degree 2q-n.

Source: [Bachmann-Yakerson, published article](https://doi.org/10.2140/gt.2020.24.1969),
§2 and Definition 4.1; [OWR 29/2019](https://doi.org/10.4171/OWR/2019/29), pp.1775-1777.

## 2. Weight zero: PASS

The full space is a final 0-good support. Projection identifies every negative
term with M(X); the identification is compatible with face maps and restriction.
The unnormalized constant simplicial tail therefore has alternating identity
and zero maps. The splice at degree -1 is zero. Identity pairs occupy degrees
-2j to -(2j-1), and the displayed inverse-pair homotopy contracts them.

This is a natural splitting on the small Zariski site into the ordinary
Rost-Schmid resolution and a contractible complex, so it remains valid under
derived global sections. It does not assume that the unnormalized lower terms
are literally zero. The independent verifier checks 160 negative degrees and
rejects a mutation making the splice nonzero. The proof itself covers all degrees.
The published article already states the weight-zero homotopy equivalence, so
there is no historical novelty implication.

## 3. Nonflasque lower term: PASS with the stated limitation

The graph over Gm is a regular codimension-two closed immersion with a global
normal frame from the two equations. Purity supplies the constant rank-one
coefficient. Its nonzero generic rank guarantees that any preimage under
restriction has the same generic point in its closed support.

Independent parametrized calculations checked every simplex face, without
reusing the author's row-reduction routine. The full simplex gives codimension
2. The t0 face has the single point x=1/2 and codimension 2. The t1 and t2 faces
are empty over Gm. Every vertex is empty there. Over A1, exactly the vertex
(t1,t2)=(0,0) becomes forbidden: its intersection has codimension 1 in its
one-dimensional ambient face. A larger closed support cannot remove this point.
The coefficient-group colimit does not permit cancellation of its nonzero
rank-one coefficient by changing the support label.

A negative control checking only facets falsely accepts the closure; the full
face test rejects it. A constant graph with all three simplex coordinates 1/3
provides a harmless admissible-closure control.

This proves failure of surjectivity for a single term B_2^0. It is not a cycle
class in the total-complex descent defect. The packet expressly states this and
points out that its ambient A1 is in the positive comparison theorem. No false
implication from nonflasqueness to failure of derived descent occurs.

## 4. Quadratic residue example: PASS with the stated limitation

On the divisor t=a, the normal line is framed and <x> is a nondegenerate
unramified form on Gm. The divisor and its closure avoid both simplex endpoints.
At the missing x=0 point, the second residue of this odd-valuation rank-one
coefficient is nonzero in W(Q); parity of rank detects the nonzero class.
Determinant-frame or sign conventions cannot turn it into zero.

This is a cocycle obstruction for closure on that one component without
correction. A new component over the deleted base divisor may contribute a
cancelling residue; the author correctly does not exclude it. The computer
parity checks are elementary controls, not an implementation of GW, purity,
Milnor-Witt residues, or the required global corrections.

## 5. Degreewise sheaves and Čech contraction: PASS

For a lower term, injectivity into the degree-q point-chain group is essential.
It permits compatible local representatives to be glued as coefficients, rather
than as arbitrary choices of cohomology representatives. Every open of X is
quasicompact because X is noetherian, so a finite subcover keeps the chain finite.
Residue vanishing and determinant identifications restrict correctly.

The closure argument survives an adversarial check: if a closure of a generic
support point meets an open, that open also contains the generic point. Hence the
global closure restricted to a covering member is contained in that member's
given closed support. Facewise codimension is local on the base, so the resulting
support remains q-good. This proves ordinary sheaf gluing; it does not prove
hypercohomological descent or flasqueness.

For the ordinary tail, a point contributes the augmented cochains of a full
simplex on the opens containing it. The insertion contraction is valid over any
abelian coefficient group, including the twisted group at that point. Finite
products commute with the direct sum over points. An independently implemented
basis-addition differential checks 34,992 integral basis contractions for all
255 nonempty subsets of an eight-vertex ground set and every possible base
vertex. Unsigned differential and unsigned nonminimal-vertex contraction
mutations are both rejected.

Pointwise insertion homotopies need not commute with the vertical residue
map. The author explicitly avoids that assertion. An independent two-row toy
bicomplex verifies total square-zero and acyclicity while exhibiting failure of
vertical commutation of the chosen least-vertex contractions.

## 6. Finite Čech defect and unboundedness: PASS

A finite affine cover trivializing the canonical line exists. Separatedness
makes its finite intersections affine, and restriction preserves the chosen
local trivializations. Published comparison therefore applies on every
nonempty intersection. The comparison map is natural for open immersions and
independent of a choice of canonical-line frame.

The argument uses the actual derived-localization equivalence in
Bachmann-Yakerson Corollary 4.9, not an inference from ordinary sheaf gluing.
The finite alternating Čech total complex of the intersectionwise comparisons
computes the derived sections. Its horizontal width is finite, so each total
degree has finitely many summands despite the negative unboundedness of BLRS.
Compatibility with the augmentation identifies its cone with the canonical
comparison defect. This establishes a test for descent, not vanishing of that
cone. No arbitrary hypercover theorem for the unlocalized BLRS complex has been
proved or silently assumed.

The tail T_q is a genuine subcomplex, and the lower part is its brutal quotient
L_q. In particular the differential out of degree q-1 is zero in L_q. The
short exact sequence is split degreewise, not necessarily as complexes. Finite
products, finite-width totalization, and cones preserve it. The augmented Čech
tail has finitely many vertical degrees q through dim X, so exact rows imply an
acyclic total complex by a bounded spectral-sequence argument. This needs no
vertical compatibility of the row contractions. Consequently the map between
defect cones is a quasi-isomorphism. The same reasoning covers a zero tail when
q > dim X.

Cover independence follows by identifying the defect with the canonical derived
comparison cone. It supplies no reason for that cone to vanish. These statements
are correct as derived-category statements; no canonical strict inverse or
strict chain homotopy natural in every arbitrary scheme map is asserted.

## 7. Square orientations: PASS

For a specified line L, square local frames differ by <u^2>=<1>, so the local
twist trivializations glue. Keeping another line D in the calculation gives the
claimed relative version. A specified square-root orientation of the canonical
line is enough for this elementary identity, but no such root exists universally:
O(-3) is not divisible by two in Pic(P2). A rational frame can introduce odd
valuation residues, as the preceding example demonstrates.

The lemma does not provide the transfer-and-moving argument needed to remove the
actual comparison theorem's hypotheses. The author does not claim it does.

## 8. Source hypotheses, later literature, and status

Theorem 4.7, Remark 4.8, Corollaries 4.9-4.10, Lemma 4.12, Proposition 4.14 and
its proof were inspected, together with the finite-field reduction in Theorem
3.12. The exact affine comparison requires M_-q to extend to a homotopy module;
strict A1 invariance alone is not substituted for that condition. Its field
hypothesis is perfect, not infinite. The transfer reduction covers finite
fields. The orientation and open-restriction claims used in the proof are
supported. Purity and the Rost-Schmid resolution remain imported foundations,
not results independently re-proved by this audit.

The 2023 moving-lemma paper's §1.3 retains a localization qualification. The
2025-linked author monograph compares derived Zariski and Nisnevich calculations;
in particular its Chapter 3 Corollary 3.2.13 assumes an infinite perfect field of
characteristic different from 2. It supplies no objectwise identification for
this particular splice. The relevant definitions and representability arguments
in the 2026 preprint concern ordinary Rost-Schmid complexes of MW-homodules,
with their own normalization and twists. The introduction explicitly separates
that higher theory from the Bachmann-Yakerson construction. No BLRS identification
was found in the inspected passages. None of these three sources is silently
used as a full descent theorem here.

Optional documentation improvement: spell out the monograph's infinity
hypothesis when expanding its summary. This does not invalidate the existing
negative scope conclusion or require revision of the packet.

Current primary-source pages confirm the cited 2023 v1, the 2026 v1/preprint
status, the 2025 Memoirs bibliographic identification, and the 2020 published
Bachmann-Yakerson article. Three fresh targeted BLRS/descent/localization
searches found no additional full resolution. This is a bounded search result.
The monograph and 224-page Gysin preprint were not audited in full.

Sources and exact fresh-download hashes are recorded in `SOURCE_AUDIT.json` and
`INDEPENDENT_RESULTS.json`. Reading copies and extracts are excluded.

## 9. Integrity, provenance, and executable scope

The original archive hash and manifest hash match the handoff. All nine archive
members equal the corresponding frozen author bytes. The author verifier and
stored controls replay exactly. The independent verifier imports no author
module and uses only the Python standard library. It verifies the stated bounded
calculations and intentional negative controls. These tests supplement the
proof review; they do not compute motivic spectra or decide the original problem.

All five scholarly PDFs were independently downloaded and match every pinned
byte count and SHA-256. The primary question and published definition page were
rendered and visually inspected. The two complete public dataset files and
catalog were independently rehashed. A fresh immutable repository-manifest read
matches the dataset revision, hashes, and sizes. There is one selected numeric
ID and one selected problem code, and the full prior-report dictionary lacks
that exact key rather than containing a null value. Fresh repository exact-ID
code and PR searches returned no results; that remains a bounded index search,
not a proof of repository-wide historical absence.

No source text, source PDFs, raw dataset contents, or private coordination files
are in this audit packet. No commit, push, PR edit, publication, or external
communication was performed. The frozen author artifacts remain unchanged.
