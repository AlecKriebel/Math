# A finite simple left brace outside every two-trivial-factor asymmetric product

Problem 30004311 / OWR-17294-011, Cedó's Problem 9 in OWR 51/2019.

## Result and review status

We construct a left brace of order 20,000 whose multiplicative group is metabelian and has abelian Sylow subgroups. The brace is nontrivial and simple. Its additive Sylow 5-subbrace has a nonzero triple star product. Every two-trivial-factor asymmetric product with abelian multiplicative Sylow subgroups has zero such triple products. Thus the construction gives a negative answer to the exact question, accepted as complete by the accompanying [independent mathematical audit](MATHEMATICAL_AUDIT.md).

This AI-assisted manuscript and audit are unrefereed. Acceptance is not external human peer review, journal acceptance or proof-assistant certification, and no historical novelty or priority is claimed. The asymmetric-product framework, radical-ring braces, and the earlier cyclic orthogonal simple-brace constructions are credited in [SOURCE_REVIEW.md](SOURCE_REVIEW.md). The construction below is given by direct operations and proved from scratch; it does not import the incorrect earlier theorem discussed in the 2024 paper.

## 1. Elementary ingredients

### 1.1 The 5-primary ring

Let R=xF₅[x]/(x⁵), a commutative nilpotent ring without identity. Its elements are

    r=a₁x+a₂x²+a₃x³+a₄x⁴,        a_i∈F₅.

The circle operation r∘u=r+u+ru makes R a group: identify it with the group 1+R in the unital ring F₅[x]/(x⁵). Every 1+r has inverse 1−r+r²−r³+r⁴.

Define the truncated logarithm and exponential by

    L(r)=r−r²/2+r³/3−r⁴/4,
    E(t)=t+t²/2+t³/6+t⁴/24.

The denominators 2,3,4,6,24 are invertible in F₅. All terms of degree at least five vanish. The usual formal identities through degree four therefore give

    L(E(t))=t,  E(L(r))=r,  L(r∘u)=L(r)+L(u).        (1)

For completeness, these identities can be obtained by expanding in commuting indeterminates and discarding terms of total degree at least five. The coefficients only use denominators dividing 24, so the characteristic-five reduction is legitimate; there is no division by five. Thus L is an explicit isomorphism (R,∘)→(R,+).

Let σ be the ring automorphism induced by x↦−x. It is an involution. Put

    η(r)=[x⁴]L(r)
        =a₄−a₁a₃−a₂²/2+a₁²a₂−a₁⁴/4.             (2)

Equation (1) gives η(r∘u)=η(r)+η(u), and σ preserves η because x⁴ is even. Also L(σ(r))=σ(L(r)).

### 1.2 The binary orthogonal space

Let

    V={v∈F₂⁵ : v₀+v₁+v₂+v₃+v₄=0}.

It has dimension four. Let M cyclically rotate the five coordinates, and define

    β(v,w)=Σ_i v_i w_i,
    Q(v)=wt(v)/2 mod 2,                              (3)

where wt(v) is the ordinary integer Hamming weight, which is even for v∈V. For v,w∈V,

    Q(v+w)=Q(v)+Q(w)+β(v,w).                         (4)

Indeed wt(v+w)=wt(v)+wt(w)−2|supp(v)∩supp(w)|; divide this integer identity by two and reduce modulo two.

The form β is symmetric, alternating on V, and nondegenerate. To check the last assertion, its orthogonal complement to the even-weight space in F₂⁵ is the span of (1,1,1,1,1); that vector has odd weight and hence is not in V. Equivalently, testing v against vectors with ones in positions i,j forces all coordinates of v to be equal, and the even-weight condition then forces v=0.

M preserves V, β and Q, and M⁵=1. Its fixed vectors in F₂⁵ are constant vectors; its only fixed vector in V is zero. Hence M−1 is invertible on V. M has order exactly five because it is not the identity.

## 2. The operations

Set

    B=R×V×F₂.

Addition is componentwise. For a=(r,v,z), define

    s(a)=η(r)∈F₅,
    e(a)=z+Q(v)∈F₂.

Use the element s(a) as an exponent of M, well-defined modulo five. Define

    (r,v,z)∘(u,w,Z)
      =(r+σ^{e(a)}(u)+rσ^{e(a)}(u),
        v+M^{s(a)}w,
        z+Z+β(v,M^{s(a)}w)).                         (5)

All products in the first coordinate are products in R. Formula (5) is an explicit finite construction using four residues modulo five, an even-weight five-bit vector, and one bit. Its cardinality is

    |B|=5⁴·2⁴·2=20,000.

## 3. Multiplicative group and left-brace compatibility

### 3.1 A direct group isomorphism

Write L(r)=l₁x+l₂x²+l₃x³+s x⁴, so s=η(r). Let K=F₅³ and let τ act on K by

    τ(l₁,l₂,l₃)=(−l₁,l₂,−l₃).

Consider the ordinary direct product of semidirect-product groups

    G₀=(K⋊_τ C₂) × (V⋊_M C₅).                      (6)

The map

    Ψ(r,v,z)=(((l₁,l₂,l₃), z+Q(v)), (v,s))           (7)

is bijective. Given its right side, use E to recover r from l₁x+l₂x²+l₃x³+s x⁴, and recover z from e+Q(v).

Let a=(r,v,z), b=(u,w,Z), s=η(r), t=η(u), e=z+Q(v), f=Z+Q(w). By (1), the logarithm of the first coordinate of a∘b is

    L(r)+σ^e(L(u)).

Its first three coefficients are k+τ^e h and its fourth is s+t. Meanwhile, (4) and M-invariance give

    e(a∘b)
      =z+Z+β(v,M^s w)+Q(v+M^s w)
      =z+Q(v)+Z+Q(w)=e+f.

The V-coordinate is v+M^s w. These are exactly the two semidirect-product laws in (6), so Ψ is a group isomorphism. In particular (5) is associative and has inverses and identity (0,0,0); those properties are not inferred from random testing.

### 3.2 The lambda maps are additive automorphisms

Because addition is componentwise, the lambda map computed from (5) is

    λ_(r,v,z)(u,w,Z)
      =((1+r)σ^{z+Q(v)}(u),
        M^{η(r)}w,
        Z+β(v,M^{η(r)}w)).                           (8)

The first component is an invertible F₅-linear map of R: multiply by the unit 1+r after the automorphism σ^{z+Q(v)}. The last two components form an invertible F₂-linear triangular map of V×F₂. Thus λ_a is an automorphism of the abelian group (B,+). Since (5) is a group law and a∘b=a+λ_a(b), additivity of λ_a is precisely the left-brace identity

    a∘(b+c)=a∘b−a+a∘c.

Therefore B is a left brace, with abelian additive group C₅⁴×C₂⁵.

## 4. All multiplicative hypotheses

In (6), K and C₂ are abelian, and V and C₅ are abelian. Each semidirect product is metabelian; their direct product is metabelian.

More explicitly, the derived subgroup of K⋊C₂ is (τ−1)K, the two-dimensional span of the first and third coordinates. The derived subgroup of V⋊C₅ is (M−1)V=V. Thus

    [G₀,G₀]≅C₅²×C₂⁴,         |[G₀,G₀]|=400,        (9)

an abelian group. The group is nonabelian because τ and M are nontrivial.

A Sylow 5-subgroup is K×C₅≅C₅⁴, and a Sylow 2-subgroup is C₂×V≅C₂⁵. Both are abelian. Conjugacy of Sylow subgroups then shows that **all** multiplicative Sylow subgroups are abelian. No normal-Sylow assumption is used.

The additive Sylow subbraces are

    P₅=R×{0}×{0},       P₂={0}×V×F₂.

On P₅ the star product a*b=λ_a(b)−b is precisely ordinary multiplication in R. Thus x*x=x²≠0, proving that B is nontrivial.

## 5. A complete simplicity proof

We use only two elementary consequences of the ideal definition. If I is an ideal, i∈I and a∈B, then

    λ_a(i)−i∈I,            i*a=λ_i(a)−a∈I.          (10)

The first is lambda invariance and additive closure. For the second, the operations descend to B/I and the coset of i is zero, so the cosets of λ_i(a) and a agree. Equivalently it follows by combining multiplicative normality with the brace identity. Also all additive integer multiples of i lie in I.

Let I be a nonzero ideal. If some (r,v,z)∈I has r≠0, its additive double is (2r,0,0)∈I∩P₅ and is nonzero. Otherwise I has a nonzero element of P₂.

### Step 1. A nonzero P₅ element gives a=(x⁴,0,0)

Suppose (r,0,0)∈I is nonzero and the lowest nonzero term of r is c x^j. If j=4, an additive scalar multiple gives a. If j<4, formula (8) restricted to P₅ gives

    λ_(x^{4−j},0,0)(r,0,0)−(r,0,0)=(c x⁴,0,0).

This lies in I by (10), and multiplying additively by c^−1∈F₅ gives a.

### Step 2. A nonzero P₂ element gives b=(0,0,1)

Suppose (0,v,z)∈I is nonzero. If v=0 it is b. If v≠0, nondegeneracy of β provides w∈V with β(w,v)=1. Taking the lambda map of (0,w,0) in (8) gives

    λ_(0,w,0)(0,v,z)−(0,v,z)=(0,0,1)=b∈I.

### Step 3. Either a or b gives both

If b∈I, its e-coordinate equals 1 and (8) gives

    b*(x,0,0)=(−2x,0,0)=(3x,0,0).

This is a nonzero P₅ element, so Step 1 gives a∈I.

If a∈I, then η(x⁴)=1, and (8) gives, for every w∈V,

    a*(0,w,0)=(0,(M−1)w,0).

Since M−1 is onto, every (0,v,0) lies in I. Taking any nonzero such v and applying Step 2 gives b∈I. Thus every nonzero ideal contains a,b and all (0,v,0), hence all of P₂.

### Step 4. All of P₅ lies in I

The calculation b*(x,0,0)=(3x,0,0) and additive scaling give (x,0,0)∈I. For j=1,2,3, apply (10) and (8) to get

    λ_(x,0,0)(x^j,0,0)−(x^j,0,0)=(x^{j+1},0,0)∈I.

These four monomials additively generate P₅. Since I contains P₅ and P₂, it is B. Hence B is simple.

This proof treats every possible nonzero ideal. It does not assume that ideals are coordinate subspaces, does not enumerate only selected subgroups, and does not use irreducibility of an unverified module.

## 6. Obstruction to every two-trivial-factor presentation

We give the needed invariant directly from the full asymmetric-product definition. The accompanying [audit](MATHEMATICAL_AUDIT.md) independently proves the same obstruction.

### Lemma. Sylow triple products in a two-trivial-factor asymmetric product

Let C be a finite left brace that is an asymmetric product of two trivial braces and whose multiplicative Sylow subgroups are abelian. If P is an additive Sylow p-subgroup of C, then

    (a*b)*c=0       for all a,b,c∈P.                  (11)

Proof. In any proposed presentation, write

    (t,s)+(u,v)=(t+u,s+v+b(t,u)),
    (t,s)∘(u,v)=(t+α_s(u),s+v),

for abelian groups T,S, a symmetric biadditive b:T×T→S, and a b-preserving action α:S→Aut(T).

This covers the general admissible symmetric-2-cocycle definition as well: the lambda formula is

    λ_(t,s)(u,v)=(α_s(u),v−b(α_s(u),t)),

and λ_(t,0)λ_(u,0)=λ_(t+u,0) forces additivity of b in its second argument. Symmetry forces additivity in its first argument.

Biadditivity implies b(T_p,T_q)=0 for p≠q and b(T_p,T_p)⊆S_p. Consequently the additive Sylow p-subgroup is T_p×S_p; it is also a multiplicative Sylow subgroup. Abelianness of the latter gives α_s(t)=t for all s∈S_p,t∈T_p.

For a=(t,s), b₀=(u,v) in T_p×S_p, direct additive subtraction in the displayed law gives

    a*b₀=(0,−b(u,t)).

An element (0,w) with w∈S_p acts trivially by lambda on T_p×S_p, because α_w is the identity on T_p. Therefore (a*b₀)*c=0 for all c in this Sylow subbrace. ∎

Any brace isomorphism preserves additive Sylow subgroups and star products. In our B, take a=b=c=(x,0,0)∈P₅. Ordinary ring multiplication gives

    (a*b)*c=(x³,0,0)≠0.                              (12)

This contradicts the lemma in every possible two-trivial-factor presentation. Thus B has no such presentation. Combined with Sections 3–5, this is a counterexample to all the hypotheses of Cedó's original Problem 9, rather than an example merely outside one known construction family.

## 7. Independent intrinsic cross-checks

These checks are redundant to (12). Section 7 of the accompanying [audit](MATHEMATICAL_AUDIT.md) supplies standalone proofs of the two-trivial-factor fixed-set and center properties used here.

From (8), a globally lambda-fixed (u,w,Z) must satisfy ru=0 for every r∈R, so u∈F₅x⁴. The element (x⁴,0,0) forces Mw=w, hence w=0. Conversely all (c x⁴,0,Z) are fixed. Therefore

    Fix(B)=F₅x⁴×{0}×F₂,            |Fix(B)|=10.       (13)

By (9), |G/[G,G]|=20,000/400=50. A simple two-trivial-factor product has Fix(B) as a complement to the derived subgroup, so the mismatch 10≠50 is a second intrinsic obstruction.

The nonzero element (x²+3x⁴,0,0) is central multiplicatively. Under L it corresponds to x², which is fixed by σ, has η=0, and occupies the central coordinate of K in (6). A simple nontrivial two-trivial-factor product has trivial multiplicative center, giving a third cross-check. No general claim that arbitrary simple braces have centerless multiplicative groups is used.

For an explicit witness to the intrinsic condition stated below, put k=(0,0,1) and h=(E(2x),0,0). With [k,h]=k∘h∘k^−1∘h^−1,

    d=[k,h]=(E(x),0,0)=(x+3x²+x³+4x⁴,0,0)∈[G,G].

For g=u=(x,0,0), the local ring product gives

    d*u=(x²+3x³+x⁴,0,0),
    g*(d*u)=(x³+3x⁴,0,0)≠0.

Thus the intrinsic condition [G,G]*B⊆Fix(B) fails in the required simple class itself.

## 8. Verification scope

The mathematical proof above is complete and independent of software. The historical exact checker verified the finite ingredient identities, all 390,625 ordered pairs for the logarithm homomorphism, the binary form/quadratic/rotation identities, the group-coordinate map, fixed/central/socle computations, explicit obstruction witnesses, and ideal-propagation derivations for all 19,999 nonzero starting elements. Componentwise identities are used to certify the group and brace laws; an exhaustive enumeration of all 20,000³ triples is neither performed nor claimed.

Earlier 72- and 54-element controls were separate historical checks: the 72-element brace is a known positive construction, while the 54-element brace fails simplicity. They are not the counterexample. The full mathematical proof and substantive independent audit are included in this proof-only edition. Programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material are excluded. Historical computation counts are supplementary metadata; no theorem depends on omitted software or certificates. Edition preparation rechecked frozen input bytes and publication integrity without rerunning historical mathematical computations or performing new scholarly-source retrieval, source-text inspection or literature search.
