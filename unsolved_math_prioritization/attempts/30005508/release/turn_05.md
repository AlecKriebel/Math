# Approach 5: an explicit nonnilpotent one-simple-module test

## Aim

Test the x=1 core of the conjecture outside the nilpotent all-pair model. The construction below is explicit and modest: 864 group elements and six conjugacy classes of elements whose square is 1. No general counterexample results.

This construction is closely related to the order-864 one-simple-module example discussed at the end of Sambale's nilpotent-block paper. We do not claim a new example or identify its SmallGroup library number.

## Group construction

Let V₁=V₂=F₂², D=V₁⊕V₂, and define

A = [[0,1],[1,1]],  T = [[0,1],[1,0]].

Then A has order 3, T has order 2, and TAT=A⁻¹. Let Q be the Heisenberg group of order 27, represented by triples (a,b,c)∈F₃³ with product

(a,b,c)(a',b',c')=(a+a',b+b',c+c'+ab').

Its center Z consists of (0,0,c). Let Q act on D by A^a on V₁ and A^b on V₂. The center acts trivially. Let τ act on Q by

(a,b,c)^τ=(-a,b,-c),

and on D by T on V₁ and the identity on V₂. These actions are compatible, so

G=D⋊(Q⋊⟨τ⟩)

is a group of order 16·27·2=864. Put E=D⋊⟨τ⟩, a Sylow 2-subgroup of order 32. The script uses six coordinates (u,v,a,b,c,t), encoding each F₂² vector as an integer 0–3 and t∈{0,1}.

## A real nonprincipal block with one simple module

Fix a nontrivial linear character θ of Z. The odd-order extraspecial group Q has exactly one irreducible character ρ above θ; its degree is 3 and

ρ(z)=3θ(z) for z∈Z,   ρ(q)=0 for q∉Z.

These facts can also be obtained directly from the three-dimensional shift/clock representation of Q. Its conjugate under τ is the unique character above bar θ.

Every simple kG-module is trivial on the normal 2-subgroup D. The group G/D=Q⋊⟨τ⟩ has a unique simple module S lying over the orbit {θ,bar θ}: it is induced from ρ and has dimension 6. Thus the central idempotent e_θ+e_{bar θ} supports exactly one simple module and is a single block B. It is real, since τ interchanges θ and bar θ, and it is nonprincipal, since neither central character is trivial.

Let z=(0,0,1) generate Z. In characteristic 2 the idempotent is explicitly

e_B=z+z⁻¹.

The class K={z,z⁻¹} has nonzero coefficient in e_B and acts on S by the nonzero scalar θ(z)+θ(z)⁻¹=1. It is therefore a real defect class. Its centralizer is D⋊Q, whose Sylow 2-subgroup is D; its extended centralizer is G, whose Sylow 2-subgroup is E. Hence (D,E) is the actual defect pair of B.

This block is nonnilpotent. Indeed C_G(D)=D×Z. A Brauer correspondent b_D is the block of D×Z over θ, and its stabilizer is D⋊Q. The inertial quotient is

N_G(D,b_D)/(D C_G(D)) ≅ Q/Z ≅ C₃×C₃,

which is nontrivial of odd order. A nilpotent block cannot have this inertial quotient.

## Exact projective character

Ind_Q^G ρ is projective in characteristic 2, because |Q| is odd. Its head contains S once by Frobenius reciprocity, as S restricted to Q is ρ⊕ρ^τ. It has no other simple constituent in its head. Thus its ordinary lift is the unique projective indecomposable character Φ of B.

The induction formula and the displayed values of ρ give

Φ(1)=96,
Φ(z)=Φ(z⁻¹)=−48,
Φ(g)=0 for g∉Z.  (6)

In particular, for an involution y centralizing Z the sum over C_G(y) is 96−48−48=0. For an involution inverting Z the centralizer intersects Z trivially and the multiplicity is 96/|C_G(y)|.

## Complete involution-class calculation

Every element of order at most 2 in D⋊Q lies in D, since the quotient Q has odd order. The G-orbits on D have sizes 1,3,3,9, according as the two vector coordinates are zero or nonzero. Their centralizer orders are 864,288,288,96, respectively. All four give multiplicity zero and have empty intersection with E\D.

Every outside involution is conjugate into E by Sylow's theorem. Such an element is dτ and is an involution exactly when its V₁ coordinate lies in Fix(T), of order 2; its V₂ coordinate is arbitrary. Thus E\D has eight involutions.

Conjugation by D interchanges the two possible V₁ coordinates because im(1+T)=Fix(T). Conjugation by the second C₃-factor rotates the three nonzero V₂ coordinates. There are exactly two resulting G-classes:

- V₂ coordinate zero: intersection with E\D has size 2. The centralizer has order 48, so (6) gives multiplicity 2. The G-class has size 18.
- V₂ coordinate nonzero: intersection with E\D has size 6. The centralizer has order 16, so (6) gives multiplicity 6. The G-class has size 54.

The centralizer counts can be checked directly from the multiplication law. For τ, fixed points in D have order 8 and the centralizer in Q⋊⟨τ⟩ has order 6, giving 48. For d₂τ with d₂≠0 in V₂, centralizing forces the second C₃-coordinate to vanish; the count becomes 16.

These are all six classes, containing 1+3+3+9+18+54=88 elements in total. Every class satisfies the conjectured equality. The scalar sum is 2+6=8, equal to the eight involutions in E\D; retaining the separate values 2 and 6 is essential to the orbit-by-orbit test.

## Reproducible verification and scope

`check_exact.py` implements the group law, finds exact inverses and centralizers, enumerates all six classes, and averages the integer-valued character (6) using rational arithmetic. It also verifies associativity for every group element followed by each pair from an explicit generating set; associativity of the group itself is established by the semidirect-product construction above. The program does not claim exhaustive triple-by-triple associativity testing.

All six restricted-character multiplicities equal the independently counted intersections. The checked case is x=1 in this block. We do not claim that the program enumerates every subsection of this group or every order-864 group.

The example disproves neither conjecture. It confirms that the reduction in Approach 2 still leaves substantial nonnilpotent cases, and supplies an exact positive test beyond the C₃⋊E model. After this fifth approach no universal proof or counterexample has been obtained.
