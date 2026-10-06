# Independent audit of KP 2.33 partial results

## Disposition

The five numbered propositions are accepted as scoped partial results. The unrestricted faithful homeomorphism-action problem is **unsolved after five approaches**. The original author freeze needs one ancillary wording correction: local moving is not a stronger condition than existence of a dense global orbit. Those two dynamical properties are incomparable. The corrected derivative makes this distinction explicit; no numbered proposition, construction, or approach count changes.

This is an independent mathematical review of AI-assisted, unrefereed exposition, not peer review or formal verification. Existing deep theorems are credited inputs whose statements and applicability were checked. Their complete proofs were not formally verified or independently reconstructed.

The reviewed author archive is 15,841 bytes with SHA-256 eaa93db26033043b36df00fad6951c939ef428977a59489a1d9897fa3333aa65. Its external manifest is 1,284 bytes with SHA-256 54d7634813f0d1e95f9f359f3f1561133f4e12020d5b03a0494775b1f5af653c. It remains unchanged.

## Exact target and selection

The complete selected problem record, associated report, and catalog entry were independently loaded from the three bound datasets and read. Recomputing SHA-256 of Python's default json.dumps([complete_problem, reports.get(problem_number, {})], sort_keys=True).encode() gives 0518f75ab319961cd66f66105162a5dfa005ecbdacd78ee4948d40c8cb808fe4. The statement digest is 875a04d081985ecb1002a0fcfc1c2c51a82020cb81972e5b9a692a281e298930. The unique selection is problem 2781, KP-2.33, rank 859. The complete pair agrees with the selected-record copy. All three dataset byte counts and hashes match SOURCE_AUDIT.json. No dataset contents are included here.

The primary K3 Problem 2.33, printed pages 112 and 113, was inspected through its complete text and both page images, including all five remarks and the boundary before Problem 2.34. It asks for a finitely generated torsion-free group excluded from faithful homeomorphism actions on a prescribed closed surface. It imposes no freeness, orientation-preservation, differentiability, invariant measure, local moving, or local approximation assumption. The disk-relative-boundary remark is a related question, not an asserted equivalence. The surface may be nonorientable. The positive disk constructions also work when the ambient surface is noncompact or has boundary, by using an interior chart.

Primary source: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

## Proposition 1 and extension by identity

The lexicographic order on G times Q is countable, dense, and without endpoints, including when G is finite or trivial. Left multiplication preserves the order and detects every nonidentity element. The usual back-and-forth construction transfers this to Q. For a rational-order automorphism, the cut formula has finite upper and lower bounds; density and bijectivity prevent jumps or flat intervals. Extending the inverse and using agreement on Q establish both the homeomorphism property and the homomorphism law.

Conjugacy to the open interval extends continuously to its two endpoints. For the diamond formula, continuity along the sloping boundary follows from continuity of the interval homeomorphism and its endpoint fixation. At either tip, the horizontal image coordinate is bounded by 1 minus the absolute value of the vertical coordinate, independently of the interval map. This directly handles the only singular denominator. The inverse and composition formulas are exact; the equator detects faithfulness.

For completeness, these disk maps preserve orientation. The interval maps f_s(x)=(1-s)x+s f(x), for 0<=s<=1, give increasing endpoint-fixing homeomorphisms, and the same diamond bound makes their disk extensions a continuous isotopy relative to the boundary. Extending by the identity in a collared coordinate disk therefore gives homeomorphisms of any surface and preserves its orientation when an orientation is chosen. Pasting is legitimate because the disk boundary is fixed pointwise. A smaller disk leaves a common fixed nonempty open set. Such a fixed set does not compromise faithfulness.

## Proposition 2 and the Hyde input

Hyde's Theorem 3.2 supplies a six-generator non-left-orderable subgroup of the pointwise boundary-fixing disk group. The entire four-page author version was inspected. Its construction uses bounded translations and bounded periodic shears/reparametrizations. The shear displacement is bounded by 3, the one-dimensional reparametrization displacement by 1/6, and coordinate-swapped versions have the same bounds. Thus the bounded-displacement compactification argument actually applies to the named generators, not merely to an abstract plane action.

Bounded-displacement maps form a group: composition adds bounds, and inversion preserves the displacement supremum. At infinity, the unit-direction error is at most twice the displacement bound divided by the original radius. The conjugated maps and their inverses consequently extend continuously and fix the radial circle pointwise. This gives a faithful homomorphism. The packet correctly distinguishes this compactification from one-point compactification and correctly gives an unbounded twist that fails radial extension.

Constantin--Kolev Proposition 3.2 applies to every finite-order disk homeomorphism fixing the whole boundary pointwise and forces it to be the identity. Hence the disk-boundary group itself, and Hyde's subgroup, are torsion-free. No orderability conclusion was incorrectly drawn from torsion-freeness. Hyde's non-orderability proof is a credited external theorem, not an independent novelty claim here.

Sources: https://arxiv.org/abs/1810.12851 and https://arxiv.org/abs/math/0303256

## Proposition 3 and the regularity boundary

The principal congruence subgroup at level 3 in SL(4,Z) has finite index because reduction has finite image. The elementary-matrix generation argument and Schreier's lemma supply finite generation. Its distinct elementary unipotents supply infinitude.

The torsion proof is valid. Taking a prime-order power does not leave the congruence subgroup. Maximal divisibility of A-I gives A=I+3^k B with k>=1 and B nonzero modulo 3. The first binomial reduction forces the prime to be 3. Dividing the cubic expansion by 3^(k+1) leaves B+3^k B^2+3^(2k-1) B^3=0; both higher coefficients vanish modulo 3, contradicting the choice of B. Matrix noncommutativity causes no difficulty when expanding powers of I plus a single matrix.

Brown--Fisher--Hurtado's Theorem A in the SL(m,Z) paper explicitly covers finite-index subgroups, C2 homomorphisms into diffeomorphisms of closed manifolds, and dimension at most m-2 without an invariant-volume requirement. Here m=4 and dimension=2 satisfy the hypotheses. Neither connectedness nor orientability is a hidden requirement of this theorem; its introductory discussion explicitly allows disconnected manifolds. Finite image excludes faithfulness because the domain is infinite. This proves a C2 obstruction only. No simultaneous smoothing theorem for arbitrary topological actions is supplied.

Brown--Damjanovic--Zhang Theorem 1 and Corollary A were checked separately: the printed hypotheses distinguish uniform lattices from the full SL(n,Z), and still require C1 regularity. The packet does not invoke them as a C0 theorem. There is no substitution of the differently scoped BFH cocompact-lattice paper cited in K3 for the arithmetic theorem actually used.

Ye Theorem 1.2 concerns the full SAut(F_n), and hence its SL(n,Z) quotient, for connected manifolds with the stated Euler-characteristic residue and n>r+1. The relevant numbers 4 and 2 satisfy its dimension inequality, but passage to the torsion-free finite-index subgroup is not authorized by that theorem. The proof and subsequent discussion explicitly retain the torsion dependence. Surjectivity of reduction follows from elementary generation over F_3. Counting independent columns gives |SL(4,F_3)|=80*78*72*54/2=12,130,560. Inducing the subgroup action gives a disjoint union of that many copies, whose Euler characteristic is divisible by 6, so both cited topological hypotheses fail. This is a valid failed route, not a counterexample to Ye.

Sources: https://arxiv.org/abs/1710.02735 ; https://arxiv.org/abs/1801.04009 ; https://arxiv.org/abs/1707.06788

## Proposition 4 and the group relations

Write F for the free group on c_i, i in Z. The basis-inversion automorphism J and shift automorphism T commute. J sends a word to the word obtained by inverting each letter without reversing its order; it is not the word-inversion anti-automorphism. In F semidirect Z, the automorphism theta(w,b^k)=(T(w),b^(-k)) preserves the multiplication because J=J^(-1) and JT=TJ. Its explicitly stated inverse is valid.

The resulting iterated semidirect product has unique coordinates (w,k,l), and its multiplication is

    (w,k,l)(v,m,n) = (w J^k T^l(v), k+(-1)^l m, l+n).

Taking a=(1,0,1), b=(1,1,0), and c=(c_0,0,0) verifies the two presented relations and generation. Conversely, in the presented group, c_i=a^i c a^(-i). The relation b a^i=a^i b^((-1)^i) implies b c_i b^(-1)=c_i^(-1), since both b and b^(-1) invert c. Conjugation by a shifts c_i and inverts b. These identities supply the reverse homomorphism; both composites fix the generators. Thus no extra relations or unjustified injectivity are being assumed.

Free groups are left-orderable. The lexicographic positive cone for an extension of two left-orderable groups is closed under multiplication and separates each nonidentity element from its inverse. A left order does not require conjugation invariance of this cone. Applying this extension fact twice proves left-orderability and hence torsion-freeness of the three-generator group. Proposition 1 supplies its faithful disk and surface actions.

Le Roux Corollary 2.1 applies to exactly this presentation, called G2, and excludes free orientation-preserving actions on the plane. The source's subsequent line-action discussion agrees with the positive conclusion. The audited proof does not depend on a questionable interpretation of its printed normal-form formula. Faithful actions with fixed points do not contradict the free-action obstruction.

Source: https://arxiv.org/abs/1101.3137

## Proposition 5 and the necessary wording correction

For a faithful torsion-free locally moving action, choose n disjoint open disks. A homeomorphism which is the identity outside one disk preserves that disk, so the chosen supported elements commute. Each has infinite order. Restriction of a relation among their powers to each disk makes the corresponding power the identity everywhere; faithfulness and torsion-freeness force its exponent to vanish. This proves Z^n for every n, with no finite-generation claim. The cyclic-group control correctly proves that faithful surface actions need not be locally moving.

The opening comparison in the author's Section 5 went too far. There is a faithful locally moving torsion-free action on S2 with no dense orbit: take the product of the two pointwise boundary-fixing hemisphere homeomorphism groups, extended by identity across the opposite hemisphere. Every nonempty open set contains a smaller disk in a hemisphere interior, where a nontrivial supported homeomorphism exists. Each hemisphere is invariant and the equator is pointwise fixed, so no orbit is dense. The factors and their product are torsion-free by the periodic disk theorem.

Conversely, a torus translation by a vector whose coordinates together with 1 are rationally independent generates a faithful cyclic action with dense orbits. Every nonidentity translation has full support, so this action is not locally moving. The familiar density statement follows from the irrational torus-rotation theorem. The first counterexample alone already refutes the author's claimed implication.

The correction replaces the comparison with the precise statement that, among faithful actions, local moving is an additional condition and is incomparable with existence of a dense global orbit. It also defines local moving using a nonidentity induced homeomorphism, so a nontrivial kernel cannot supply a spurious witness. These clarifications do not alter Proposition 5, which already assumes faithfulness.

Koberda--Lodha Theorem 1.2 and its definitions concern generic countable torsion-free groups and locally moving quotient images on Hausdorff spaces with at least two points. They do not prohibit arbitrary faithful surface actions, and passage to a finitely generated subgroup is not established. The publisher confirms the May 2026 publication metadata. The locally approximating definitions in Koberda--de la Nuez Gonzalez require density of rigid stabilizers; arbitrary faithful embeddings do not supply that hypothesis.

Sources: https://arxiv.org/abs/2503.11772 ; https://www.sciencedirect.com/science/article/pii/S0168007225001538 ; https://arxiv.org/abs/2410.16108

## Integrity and limitations

All six original archive members were checked against the pinned external manifest and embedded manifest, and all nine bound source PDFs independently matched their recorded hashes and byte counts. The corrected data-only derivative and this audit packet have separate manifests and acceptance records. Validation is performed by trusted external code under isolated Python, including normal, optimized, relocated, and hostile-working-directory profiles; mutation tests exercise rejection of malformed inventories and tampered data. These checks establish byte identity and packaging properties, not mathematical correctness.

No copied scholarly PDFs, extracted source text, source images, raw corpus records, private sources, or private coordination files occur in the public-safe outputs. No packet code is executed. No source fetch or executable mathematical checker is promised by archive verification. Prior repository-search receipts were inspected as bounded author evidence, not repeated as an exhaustive independent repository search. The dated primary-source status statements and bounded source checks do not certify worldwide open status or novelty.

The acceptance applies to the corrected partial-results derivative. It does not certify a solution of KP-2.33, a universal embedding theorem for torsion-free groups, a new non-left-orderable example, or removal of smoothness, freeness, or local-action hypotheses.
