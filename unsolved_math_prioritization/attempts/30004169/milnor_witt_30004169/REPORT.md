# Scope and findings

## Exact question

Fix a perfect field k with char(k) != 2 and q >= 0. For every smooth separated
finite-type k-scheme X, put B_q(X) = C^*(X,K_q^MW,q), the BLRS complex.
The question is whether its canonical comparison

    B_q(X) -> RΓ_Zar(X, a_Zar B_q)

is a quasi-isomorphism for every X. Here sheafification is degreewise; the
complex is cohomologically unbounded below. Our proof below also shows that
the terms on the small Zariski site are already sheaves. Derived global
sections, rather than termwise sheafification, are the issue.

This is the interpretation supplied by the original report's use of
hypercohomology and by Bachmann–Yakerson, Remark 4.5. It is not a question
about the ordinary Rost–Schmid complex R^*(X,K_q^MW), which is a flasque
resolution. The OWR statement does not impose an arbitrary line-bundle
twist, invert 2, assume affineness, or assume trivial canonical bundle.
It does not ask about characteristic 2 or an imperfect base. Broader
extensions in later references are not silently included in this packet's
target.

## Definitions and indexing

For a strictly A¹-invariant Nisnevich sheaf M, let

    R^p(X,M) = ⊕_{x in X^(p)} M_{-p}(κ(x), ω_{x/X}),
    ω_{x/X} = det(Ω_{κ(x)/k}) ⊗ det(Ω_{X/k}|_x)^(-1).

The latter is canonically the determinant of the normal vector space at x
(the dual of the determinant of m_x/m_x²). For M=K_q^MW the coefficient
is K_{q-p}^MW with this twist. In degree p=q it is twisted GW, and for p>q
it is negative Milnor–Witt theory, identified with Witt theory. Those terms
must not be discarded as if the coefficient were ordinary Milnor K-theory.

Write Δ^i=Spec(k[t_0,...,t_i]/(Σt_j-1)). A closed support Z in X×Δ^i is
q-good if Z intersects every face X×F in codimension at least q inside
X×F, including the full simplex. Empty intersections are permitted.

For p >= q set B_q^p(X)=R^p(X,K_q^MW). For p=q-i, i>0, set

    B_q^(q-i)(X) = colim_{Z q-good} H_Z^q(X×Δ^i,K_q^MW).

Cohomology with support can be computed by the support Rost–Schmid complex.
As that complex has no terms below q for these supports, H_Z^q is a kernel
in degree q, not a quotient by unspecified lower-degree boundaries.

The differential in p>=q is the residue differential. Below p=q-1 it is
the alternating face pullback. At the splice p=q-1 it is i_1^*-i_0^*, followed
by the inclusion of the degree-q residue kernel in R^q(X,K_q^MW).
Face pullback is defined on supported cohomology; an arbitrary choice of
chain-level Gysin maps on ordinary Rost–Schmid complexes does not provide
strict simplicial identities automatically.

If i denotes BLRS cohomological degree, the hypercohomological comparison
has motivic degree q+i and weight q. Equivalently, higher Chow–Witt index n
corresponds to i=q-n and motivic degree 2q-n. These three indices are not
interchangeable.

## Source-verified positive results and limits

The original OWR report proves the hypercohomological comparison and asks
whether hypercohomology can be omitted. The published Bachmann–Yakerson
paper gives the canonical map B_q(X)->(K_q^MW)^(q)(X), identifies its Zariski
localization with the target, and proves an objectwise equivalence when X
is affine with trivial canonical bundle. The map itself does not depend on
choosing a trivialization. The finite-field case is included by their
transfer argument; an infinitude hypothesis should not be added to this
published theorem. See Definition 4.1, Remark 4.5, Theorem 4.7,
Corollaries 4.9–4.10, and Proposition 4.14.

For general M the exact comparison theorem assumes that M_{-q} admits a
homotopy-module structure. Strict A¹ invariance alone is not the stated
transfer hypothesis. Milnor–Witt coefficients meet the required condition.

Later literature was checked for a resolution, rather than treating the
2019 question as proof of present openness:

1. Déglise–Feld–Jin, *Moving lemmas and the homotopy coniveau tower*,
   arXiv:2303.15906v1, §1.3: the smooth-smooth-site result improves
   functoriality, but its discussion still retains a localization problem.
   This does not prove BLRS descent.
2. *Milnor-Witt Motives*, author PDF linked to the 2025 Memoirs volume:
   Chapters 3–4 compare Zariski and Nisnevich hypercohomology of MW-motivic
   complexes. This compares two derived computations; it does not identify
   naive global sections of this BLRS splice with either one. The inspected
   text gives no theorem making that missing identification.
3. Déglise–Feld–Jin, *Homotopy coherent Gysin functoriality*,
   arXiv:2605.01855v1, introduction pp.6–8 and §§6.1–6.3: the constructed
   objects retain ordinary Rost–Schmid complexes of MW-homodules. Their
   descent, representability and Borel–Moore localization do not identify
   the q-good simplicial splice with its localization. The introduction
   itself distinguishes its higher theory from the Bachmann–Yakerson
   construction. It is a preprint; no independent audit of its 224-page
   argument was attempted here.

No full resolution was located in this targeted search. This is a bounded
literature finding, not a proof of literature-wide openness.

## Prior attempts and duplicate check

The supplied catalog marks numeric ID 30004169 queued, 0/5, rank 745.
The complete cached public dataset files were rehashed against the pinned
repository manifest. Exactly one problem has this numeric ID. The prior
report dictionary has no key OWR-16941-010, rather than a present null report.
The full problem record and its dated literature assessment were read.

Current repository code search and exact-ID PR search returned no match;
the listed attempts directory and root/problems directory contain no
matching name. A full recursive tree call failed with a transport error,
so repository absence is not asserted exhaustively. The related-target
group file contains no exact-ID occurrence. The dataset title/code scan
found no other Rost–Schmid/Chow–Witt target or reused problem code.
Unrelated personal-context search results were excluded, not assimilated
as prior mathematics on this problem.

## Five approaches and exact stopping points

### 1. Use the published comparison and weight-zero contraction

Weight zero is affirmative by the explicit contraction in PROOFS §1.
Affines with trivial canonical bundle are already covered by the source.
These results do not cover arbitrary X for q>0. Local validity of the
comparison does not imply objectwise validity on X without descent.

### 2. Prove descent by flasqueness of every term

This sufficient route is false. PROOFS §2 constructs a nonextendable section
of B_2^0 over Gm⊂A¹ using the curve t_1=t_2=x in Δ². Its closure hits the
vertex t_1=t_2=0 in codimension 1, violating the required codimension 2.
No added component confined to the complement can remove that violation.
The example does not disprove descent of the total complex, which is already
known on A¹. It disproves a particular shortcut.

### 3. Extend quadratic coefficients by taking closure

Even admissible closure of a support does not imply extension of an
unramified coefficient. Over Gm, the form <x> on the constant divisor t=a
is unramified; over A¹ it has nonzero second residue at x=0. PROOFS §3
computes this. Added boundary-supported cycles could cancel that residue,
so this is not a counterexample to the restriction map or to descent.
The missing step is a simultaneous correction preserving all face support
conditions and all residue identities.

### 4. Glue the known affine comparisons

PROOFS §§4–5 gives an exact finite Čech formulation. A cover by affine
opens trivializing ω has the published comparison on every nonempty
intersection. Its total Čech complex therefore computes the desired
derived global sections. The remaining assertion is precisely that the
augmentation from B_q(X) is a quasi-isomorphism.

The augmented Čech defect is unchanged if the entire ordinary
Rost–Schmid tail p>=q is removed by the brutal quotient. This is proved
using an explicit pointwise simplex contraction. Thus the unproved
acyclicity is localized in the lower q-good simplicial part. This is a
checkable reduction, not a proof that the defect vanishes.

### 5. Remove orientation dependence or use stable Gysin functoriality

PROOFS §6 proves the elementary square-twist identity. It explains some
orientation flexibility, but a general canonical bundle need not be a
square and the comparison still needs a global support-moving argument.
Choosing rational frames introduces residue terms; the preceding example
shows why they cannot simply be ignored. Replacing the BLRS construction
by a different representable Rost–Schmid/Borel–Moore theory, or by its own
Zariski sheafification, establishes descent only for the replacement.

## Final gap

For q>0 and an arbitrary smooth separated finite-type X in the source regime,
prove that the lower-part augmented finite Čech total complex of PROOFS §5
is acyclic, or exhibit a genuine nonzero class in it. No such proof or class
is supplied. In geometric terms, compatible local q-good quadratic cycles
and their homotopies must admit the required global corrections with
admissibility on every face and cancellation of all quadratic residues.

The original question remains unresolved by this packet. All five approaches
are closed at their stated gaps; no candidate full resolution is promoted.
