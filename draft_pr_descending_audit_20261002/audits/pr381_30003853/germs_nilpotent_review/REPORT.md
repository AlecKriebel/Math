# PR381 germ and nilpotent adversarial review

**PASS for the scoped Turn4/Turn5 arguments. No mandatory mathematical repair
was found in those arguments. Original Question111 remains unproved in this
packet, five of five author turns.** This is an audit of fixed head
`5b7bd8db9f34294d10862fed0f723055da864df6`, not present-day open-status, novelty,
full-solution, or merge certification. No sixth author search was performed.

## Independence, exact claim and admissible sources

The initial proof reconstruction and new control code/output were sealed at
2026-10-03T03:02:34.935416Z, before reading historical independent REVIEW.md,
FINAL_RESULT.md, REVIEWED_STATUS.md or any sibling/root verdict. See
INITIAL_SEAL.json. All 45 frozen paths match the byte count and SHA256 in the
snapshot manifest and the corresponding bytes at the stated Git head;
INPUT_RECEIPT.json records each check. The workspace branch was main.

The target is universal over finitely presented H≤F. A counterexample must have
a proved faithful F embedding, finite presentation of the embedded group and
a nonzero torsion class in H/H'. A torsion-free group with torsion in its
abelianization is not contradictory. An abstract finitely presented group with
the desired quotient is not an F counterexample until its embedding is proved.

I independently downloaded EMS46748 and visually inspected printed
pp.1624–1625. The source supplies a finitely generated embedded wreath example
before asking the finitely presented question. Its original PDF SHA256 exactly
matches the historical source binding. [Original primary report](https://ems.press/content/serial-article-files/46748).

The one-bump centralizer dependency is exactly Kassabov–Matucci Corollary4.5 and
Lemma4.6 on printed pp.9–10. A commuting finite-piece PL map with initial slope
one is identity; the initial-slope homomorphism is injective on that one-bump
centralizer. Replacing a right-moving bump by its inverse covers either
direction. This suffices for the packet's proof; cyclicity of the centralizer
is unnecessary. Its primary PDF also matches the historical SHA256.
[Kassabov–Matucci v3](https://arxiv.org/pdf/math/0607167v3).

Bleak's geometric Theorem1.1 characterizes finite derived length by tower depth;
his algebraic Theorem1.2/Lemma1.3 embed a solvable group in the corresponding
restricted sum/wreath hierarchy. These are source-admissible classification
inputs under the stated solvability hypotheses; they do not supply finite
generation of a merely finitely normally generated kernel or make every subgroup
solvable. I independently read their primary statements, and the algebraic PDF
matches the author's historical SHA256. [Geometric paper](https://arxiv.org/pdf/math/0602036),
[algebraic paper](https://arxiv.org/pdf/math/0602038).

Fresh-source metadata and PDF hashes are in SOURCE_RECEIPTS.json. Sources and
private replay copies remain ignored. Three central source PDFs are exact matches;
the public replay deliberately reports zero raw source bindings. I have not
freshly reproduced all 20 historical PDF/text/PNG byte bindings in this family.
That limitation is distinct from inspecting the controlling primary proofs.

## Turn4: proof and attempted falsifications

The theorem is valid for finite-piece PL maps. For a nontrivial ordinarily
finitely generated normal subgroup N of H, the support of N equals the finite
union of the generating supports. Normality makes that finite ordered component
list invariant. Every h∈H fixes each endpoint, including interior endpoints.
If all N generator slopes at a chosen left endpoint were one, their genuine
affine germs would be identity on a common positive interval, contradicting the
support component. This proves that an ambient real character detects N. For
H≤F, log base two gives integer values even at a nondyadic fixed point.

Every character annihilates the preimage T of torsion in H/H'. Hence no
nontrivial ordinarily finitely generated H-normal subgroup lies in T. In
particular the normal closure of a nonidentity torsion witness is infinitely
generated. The proof does not assume that H is finitely generated or presented.
It uses finitely many pieces in each N generator and each ambient element, and
uses finitely many N generators to take a common initial neighborhood. Finite
normal generation cannot replace that hypothesis.

New controls use an affine-segment implementation, with no candidate-code imports.
For a genuine F top map t with vertices
(0,0),(1/2,1/4),(3/4,1/2),(1,1), put a equal to its rescaled copy supported on
(1/2,3/4), and a_i=t^i a t^-i. Their support interiors are disjoint. The lamp
model is faithful because a nonzero lamp word acts nontrivially in a disjoint
support component; nonzero t powers have nontrivial global endpoint slopes.
Thus this is an actual F realization of Z wr Z, not an assumed embedding.

For H_m=<t,a_0^m,r>, r=a_1 a_0^-1, exact PL composition confirms
r^m=[t,a_0^m] for m=2,3,4,6,8,12. The separately proved Laurent quotient
I_m/(t-1)I_m≅Z⊕Z/m proves the exact class order m. The normal closure of r is
(t-1)Z[t,t^-1], an abelian group of infinite rank. These examples satisfy the
Turn4 conclusion and do not possess the missing finite-presentation certificate;
the packet's Turn1 separately excludes FP2 in that wreath ambient group.

The representative r has support (1/4,1/2)∪(1/2,3/4), global endpoint slopes
one, and right slope 1/2 at its own support endpoint 1/4. Since t moves 1/4,
that internal germ is not a character of H_m. This directly falsifies a tempting
overextension of the theorem: annihilation under ambient characters does not
force all germs at the witness's own support boundaries to vanish. The torsion
witness is noncentral, as the exact commutator [t,r] is nonidentity.

Further new controls cover two disjoint components, components sharing an
isolated fixed endpoint, and a genuine F map with nondyadic fixed point 7/24
and right slope 4. Its vertices are
(0,0),(1/4,1/8),(3/8,5/8),(1/2,3/4),(1,1). Its two support components remain
distinct at 7/24 and all signed powers have the expected germ 4^n.

Real or rational character evidence cannot certify an integral quotient:
P_m,ab⊗Q≅Q² while P_m,ab≅Z²⊕Z/m. In the actual H_m example, the global endpoint
slope pair sees the top generator but kills the torsion witness and the compact
lamps. No rational-to-integral saturation inference is admissible here.

## Turn5: exact group and nonembedding

The matrix realization M(a,b,c)=[[1,ma,c],[0,1,b],[0,0,1]] with integers a,b,c
reconstructs the proposed presentation
P_m=<x,y,z | [x,z]=[y,z]=1,[x,y]=z^m>. Collection to x^a y^b z^k yields c=mab+k.
All such matrices are generated, and distinct collected forms give distinct
matrices, proving this is the presented group exactly rather than a quotient.
Matrix multiplication provides an independent implementation of the triple law.

The commutator is (0,0,m(ab'-a'b)), so the derived subgroup is <z^m>, and the
central quotient is Z²⊕Z/m. Central z has infinite order and exact quotient order
m. Signed power coordinates are (na,nb,nc+m n(n-1)ab/2). They establish
torsion-freeness and unique positive roots, and comparison of noncentral
coordinates, followed by the central case, establishes balanced signed powers.
The lexicographic positive cone is closed under multiplication and invariant
under conjugation, proving bi-orderability. Class two precludes a nonabelian free
subgroup. The finite presentation is explicit and each of these assertions has
a formula proof, not merely a bounded computation.

The class-two matrix model passes controls for m=1,2,3,4,6,8,12, including
negative exponents, composite torsion moduli, the identity, central elements and
noncentral elements. The m=1 boundary gives trivial abelianization torsion but
the same nonembedding obstruction.

Every homomorphism P_m→PL_+(I) kills z. If h=image(z) were nonidentity, select a
support component J. Images of x and y centralize h and preserve each component
of its finite support list. Their restrictions lie in the abelian one-bump
centralizer on J, contradicting [x,y]|J=h^m|J≠1. Every image is consequently
abelian; none of these P_m embeds in F. A cross-check using Turn4 reaches the
same conclusion: <h> would be a nontrivial ordinarily finitely generated normal
subgroup inside the torsion preimage of the image group's abelianization.

The packet's unique-root and balanced-power proofs also cover multi-component
supports: increasing maps fix the finite ordered component list, and a point
fixed by a nonzero power of an increasing homeomorphism is fixed by that map.
The one-bump endpoint slope is nonunit because a unit affine germ would remove
an initial interval from the component. Conjugator slopes cancel at each common
fixed endpoint. No hidden dyadic-endpoint, single-global-bump or positive-only
exponent assumption was found.

## Historical comparison, exact replay and counterfeit controls

After the seal, I read the full historical independent review and its code and
the final/current wrappers. Their Turn4/Turn5 conclusions agree with the
independent reconstruction. The historical reviewer covers signed integer
formulas but does not implement the new actual F torsion witness or nondyadic
endpoint controls. That is additional validation coverage, not a mathematical
correction or novelty claim.

The complete author code and replay/publication wrappers were inspected. Private
copies replay all five author scripts with byte-exact stdout counts
17,826;15,397;75,294;6,950;447,168, total562,635. The historical independent
script reproduces byte-exact 110,736 assertions. REPLAY_ALL.py and
verify_publication.py both pass. My independent controls pass 801,018 assertions,
with no imported author routines. NEW_CONTROLS_RECEIPT.json binds their exact
output to the initial seal; REPLAY_RECEIPTS.json records individual command
status, duration and stdout/stderr SHA256. Raw replay output is preserved in
replay_outputs/. All computations are bounded supplements to the written proofs.

Counterfeit source controls use files of the expected lengths and PDF magic.
Explicit --source-dir replay rejects them at the frozen SHA check. A one-byte
tamper of each fresh primary PDF likewise retains its length/PDF header but fails
the historical hash. Omitted-source mode still passes and explicitly reports
zero source bindings. This is the advertised public-scope behavior; it cannot be
used as evidence of fresh all-source inspection. No counterfeit theorem was
accepted as a mathematical input.

## Required action, strongest result and remaining gap

There is **no mandatory mathematical repair in this family's Turn4/Turn5 scope**.
Preserve the packet's finite-piece hypothesis, ordinary-versus-normal finite
generation distinction, explicit P_m nonembedding conclusion and unresolved
original status. Do not describe the source-free public replay as fresh
verification of all 20 local sources, or these 801,018 finite checks as a proof
for every finitely presented subgroup. The new model controls are recommended
audit artifacts rather than a requirement to rewrite frozen author bytes.

The strongest verified result is the character obstruction to ordinarily
finitely generated normal torsion-witness closures, together with the precise
finitely presented proxy countermodels and a proof that every PL image of those
countermodels is abelian. The exact remaining gap is a valid finite-presentation
mechanism excluding an arbitrary noncentral torsion witness with infinitely
generated normal closure, or a faithfully embedded finitely presented example
with such a witness. Neither is supplied here. Original-resolution progress is
not increased by this audit.

The prior PR384/383/382 README files still describe pending draft/whole-package
gates; root was notified to resolve that workflow dependency before disposition.
This family has made no candidate, queue, index, Git, service or external-contact
mutation. Final family audit completion:100% of the assigned independent
Turn4/Turn5 proof/model/replay audit, with the all-20-fresh-source limitation
stated above. No merge certification is issued.
