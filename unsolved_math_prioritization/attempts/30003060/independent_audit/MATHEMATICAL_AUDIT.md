# Independent mathematical audit: higher Koszul homology

Target: 30003060 / OWR-14218-004, queue rank 865. Date: 2026-10-06 UTC.

## Verdict

**Accept the negative answer to the literal unrestricted-field equivalence.** The free algebra on two degree-one generators is Koszul, yet its higher Koszul homology in homological degree one is nonzero in every positive characteristic. No mathematical correction to the author's proof or either checker is required. The source-scope wording and execution-hygiene corrections are accepted separately.

**Do not claim the characteristic-zero converse is resolved.** The example disproves the forward implication over positive-characteristic fields. It neither proves nor disproves the implication from higher vanishing to Koszulness, in characteristic zero or in general. It is a genuine example for the original invariant and the source's unrestricted written formulation, not a calculation of a substituted invariant. Historical authorial intention beyond that wording is not established.

## Independent reconstruction

Let V have basis x,y and A=T_k(V), with R=0. This is a permitted quadratic algebra; V is finite dimensional and A is connected and locally finite. No assumption that A itself be finite dimensional appears in the target source. For each j>=2, every defining intersection W_j contains a zero factor R and is zero. Thus the only coefficient-A Koszul chains are A in degree zero and A tensor V in degree one.

There are three distinct maps to keep apart:

1. The augmentation-resolution map mu(a tensor v)=av has image the augmentation ideal. Every nonempty basis word has exactly one final letter, so mu is a basis bijection onto that ideal. The resulting length-one graded free resolution of k is linear. Hence A is Koszul over any field.
2. The ordinary coefficient-A Koszul differential is b(a tensor v)=av-va, not mu. Its homology is HK_1=ker(b), HK_0=coker(b), and HK_j=0 for j>=2.
3. The higher differential is cap product by the fundamental cocycle e_A(v)=v. In degree one its raw left-cap convention gives va; on a sum that is a b-cycle, the sums of va and av agree. In the degree-zero commutator quotient they agree in any event. Therefore delta sends [sum a tensor v] to [sum av], with no extra weight multiplier or division.

For completeness, the Koszul property can also be checked directly in the bimodule convention used by BLS. On the subspace belonging to a fixed word of length n, A tensor A has n+1 basis vectors, one for each cut of the word. A tensor V tensor A has n basis vectors, one for each distinguished letter. Its differential is the incidence map of the path joining consecutive cuts. This map is injective and its image is the kernel of the multiplication map identifying all cuts with the word. The path incidence argument works over every field. Thus the bimodule Koszul complex is exact in positive degrees, without needing a hidden characteristic-zero equivalence theorem.

The image C of b is the full commutator subspace, not the commutator ideal. For words u,v, the difference uv-vu is a telescoping sum of differences between consecutive cyclic rotations of uv. Each consecutive difference is a generator commutator. Conversely every generator commutator is a commutator. This identifies HK_0=A/C and justifies the quotient used in the proof.

## Characteristic two, with both boundary checks

The two distinct basis tensors x tensor y and y tensor x have sum z!=0 even over F_2. Their ordinary boundaries cancel. Their higher image is [xy+yx]=2[xy]=0 in A/C. Because the degree-two chain space is zero, z is not an ordinary boundary. Because HK_2=0, its ordinary class is not an incoming higher boundary. Therefore z represents a nonzero class of HK_1^hi. Its homological degree is one, coefficient weight one, and total internal weight two. Positive internal weight has not been confused with positive homological degree.

The construction uses the fundamental cocycle. The restriction excluding characteristic two for a general derivation in BLS Section 5.1 is irrelevant: Section 5.2 explicitly removes that restriction for e_A. No Hochschild comparison requiring division by two is needed.

## Every positive characteristic

Let char(k)=p>0. The word x^(p-1)y has precisely p distinct cyclic rotations, because the unique y occurs in p different positions. Split each rotation w_i as a_i v_i and sum the p distinct basis tensors a_i tensor v_i. The ordinary differential is sum_i(w_i-w_(i+1))=0 as an integer formal expression. The higher image is p[w_0]=0. The tensor sum itself is nonzero; p distinct basis terms have not been mistaken for p copies of one term. There are again no incoming ordinary or higher boundaries. The same construction therefore works over every field of positive characteristic, including extensions of the prime field.

## Orbit formula and independent diagnostics

In total weight n>0, concatenate A_(n-1) tensor V with A_n to identify both with the word space E_n. Then b=I-rho for the last-to-first cyclic permutation. On an orbit of size d, the invariant space and the coinvariant space each have dimension one over every field. The invariant generator is the sum of its d distinct words; the quotient class of any one word is nonzero, witnessed by the coefficient-sum functional. The higher map is multiplication by d from this invariant line to this quotient line.

Thus an orbit contributes one degree-one and one positive-weight degree-zero higher class exactly when p divides d; none does so in characteristic zero. The degree-zero, total-weight-zero component is k. All higher homological degrees >=2 vanish. The extra degree-zero condition in BLS Conjecture 6.5 cannot repair the unrestricted equivalence: these same examples violate it too. The one-generator free algebra has only size-one orbits and hence has no such obstruction; that negative control is important.

The independent checker does not import the author's code. It computes exact column ranks of b and b^2. Since ker(delta)=ker(b) intersect im(b), its dimension is rank(b)-rank(b^2). A separate arithmetic implementation counts primitive necklaces of size d by (1/d) sum_(e|d) mu(e) r^(d/e), for d dividing n. This differs from the author's nullspace/augmented-matrix and explicit-orbit algorithms.

All 114 cases match both this independent necklace formula and all five dimensions in the author's recorded cases. The cases use r=1 through degree 8, r=2 through degree 7, and r=3 through degree 4, with characteristics 0,2,3,5,7,11. Eleven prime witnesses from 2 through 31 pass integer telescoping and explicit commutator certificates. Deleting a witness term fails the cycle test; the degree-two witness disappears in characteristic three; the two-generator degree-three component in characteristic three has dimension two. Normal and optimized independent runs give byte-identical outputs. These finite checks supplement, rather than prove, the universal algebraic arguments above.

## Acceptance limits

This is an AI-assisted independent reconstruction and adversarial audit, not a human referee report or proof-assistant certification. It found no mathematical defect within the stated literal scope. It makes no novelty or first-priority claim. A bounded literature search did not establish a new characteristic-zero result or priority for this elementary positive-characteristic observation. One substantive free-algebra/cyclic-orbit approach has been used; independent verification is not counted as a new problem-solving approach.
