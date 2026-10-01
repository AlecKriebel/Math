# Turn 5: Clifford-component rigidity and genuine two-argument obstruction families

**Final scoped partial,5/5 substantive author turns. Original Question2 remains unresolved.** The final route addresses coupling among multiplicative group components, rather than assuming that the one-component Rees classification extends unchanged. It also propagates the arbitrary-addition obstruction to completely simple structures with arbitrary maximal groups. No novelty is asserted.

## 1. Clifford multiplication and its left ideals

Let S be a nonempty completely regular semigroup whose idempotents are central, that is, a Clifford semigroup. Denote its idempotent semilattice by E(S), with e≤d meaning ed=e. For x∈S write x^0=xx^-.

The central-idempotent assumption implies

    (xy)^-=y^-x^-,       (xy)^0=x^0 y^0.                  (1.1)

These follow by checking that y^-x^- is a commuting inverse of xy; centrality permits the idempotent factors x^0,y^0 to move past the other elements. Only then is inverse anti-multiplicativity used.

Let J be a nonempty multiplicative left ideal. It is a union of full maximal groups, since x∈J implies x^0=x^-x∈J, and x^0∈J implies x=xx^0∈J. It is also a two-sided ideal: if x∈J and s∈S, then xs=(xs)x^0, with x^0∈J, so xs∈J. Thus

    F=E(S)∩J

is a nonempty lower subset of E(S), and membership in J is equivalent to x^0∈F. The lower-subset property follows from e∈F, d≤e implying d=de∈J.

As before, every retraction f:S→J defines a compatible associative addition a+b=f(b). We now classify exactly which of these produce solutions, without assuming f is an endomorphism.

## 2. Exact rigidity theorem across all Clifford components

**Theorem.** For fixed J there is at most one retraction f whose associated map is a Yang–Baxter solution. Such a retraction exists if and only if, for each e∈E(S), the set

    {d∈F : d≤e}

has a greatest element, denoted τ(e). In that case the unique retraction is

    f(b)=τ(b^0)b.                                       (2.1)

Equivalently, among the retractions onto J, r is a solution exactly when f is a multiplicative endomorphism. The criterion by greatest idempotents supplies the stronger explicit existence and uniqueness statement.

The sets in question are nonempty: if d∈F, then de belongs to F and is below e. They need not have a greatest element when F has several incomparable upper directions.

### Necessity from the three braid coordinates

Put h(b)=f(b)^-b and e_b=f(b)^0. Since J is a two-sided ideal, both first and second outputs of r lie in J. On J the retraction is the identity. For arbitrary a,b,c, direct composition therefore gives

    r_12 r_23 r_12(a,b,c)
       =(a e_b b f(c), (h(b)f(c))^0, h(c)),              (2.2)

    r_23 r_12 r_23(a,b,c)
       =(ab f(c), (b f(c))^0 h(c), h(c)^0).              (2.3)

The third coordinate forces h(c) to be idempotent. By(1.1), its local identity is e_c c^0, so

    h(c)=e_c c^0.                                       (2.4)

The middle coordinates, using centrality and(1.1), now say

    e_b b^0 e_c = b^0 e_c c^0.                          (2.5)

Choose b=f(c), which is fixed by f. Then e_b=b^0=e_c, and (2.5) gives e_c≤c^0. Hence h(c)=e_c. Multiplying f(c)h(c)=e_c c and using f(c)e_c=f(c) yields

    f(c)=e_c c,       e_c∈F,       e_c≤c^0.              (2.6)

The first coordinate in(2.2)–(2.3) now requires a e_b b f(c)=ab f(c). Set y=b f(c) and a=y^-. Since e_b is central, this yields

    y^0 e_b=y^0,
    b^0 e_c≤e_b.                                       (2.7)

For every d∈F, choose c=d. Then f(c)=d and e_c=d. In particular, any d∈F below b^0 satisfies d≤e_b. Together with(2.6), this proves that e_b is the greatest member of F below b^0. Thus e_b=τ(b^0), independent of the particular group element in that component, and (2.1) is necessary. This proves uniqueness without cancelling arbitrary semigroup elements.

### Sufficiency and endomorphic behavior

Suppose all these greatest elements exist. The map τ is order-preserving, fixes F, and is below the identity. Moreover

    τ(ed)=τ(e)τ(d)                                     (2.8)

for e,d∈E(S). The product on the right lies in F and below ed, so is below τ(ed). Conversely τ(ed) lies in F and below each of e,d, so is below τ(e)τ(d).

Define f by(2.1). It maps into J and fixes J, and centrality with(1.1) and(2.8) gives

    f(ab)=τ(a^0b^0)ab
          =τ(a^0)τ(b^0)ab=f(a)f(b).

Thus it is an idempotent multiplicative endomorphism with left-ideal image J. The image J is Clifford, hence satisfies the right-cryptogroup identity from Turn3§5. That theorem proves r is a solution. Alternatively, with p=f(a),q=f(b),t=f(c), both braid words have outputs

    (pqt,q^0 t^0,t^0),

which directly checks all three coordinates.

Conversely, if a retraction onto J is an endomorphism, Turn3§5 proves it gives a solution because J is Clifford; the necessity argument then forces(2.1). This proves the stated equivalence and the theorem.

## 3. Multiplicative identity and a failure caused by component coupling

If S has a multiplicative identity1, E(S) has greatest element1. Existence of the solution retraction is then equivalent to F having a greatest element e. Since F is lower, F={d:d≤e}, and

    J=eS,       τ(b^0)=eb^0,       f(b)=eb.               (3.1)

Thus in a Clifford monoid the admissible ideals in this retracted-addition family are precisely those generated by a central idempotent, and their admissible retraction is uniquely multiplication by that idempotent.

For an explicit obstruction, take the four-element Boolean meet-semilattice E={0,p,q,1}, with p,q incomparable, and J={0,p,q}. It is a nonempty ideal but has no greatest element below1. Every set-theoretic retraction f:E→J still defines a generalized left semi-brace through a+b=f(b), yet none produces a Yang–Baxter solution. This is a component-coupling failure, not a failure of the compatibility law. Replacing each component by a group does not create the missing greatest idempotent.

The theorem includes Turn1's meet case, but adds arbitrary group components and derives the actual restriction map within each one. Its rigidity contrasts sharply with the nonhomomorphic retractions allowed over non-Clifford Rees multiplication in Turns3–4. Neither conclusion may be transferred to the other setting by name alone.

## 4. An attempt at arbitrary two-argument addition: a sharp obstruction family

The remaining addition need not be a retraction depending only on its second input. A simple product argument shows that the obstruction from Turn2 survives in structures with genuine dependence on both inputs and arbitrary maximal groups.

For generalized left semi-braces S and T, coordinatewise addition and multiplication make S×T a generalized left semi-brace. The commuting group inverse is coordinatewise, and its associated map is the Cartesian product of the two associated maps. Consequently, for nonempty factors, the product map solves Yang–Baxter if and only if both component maps do: sufficiency is coordinatewise, and necessity follows by projecting each braid identity to a factor.

Let C be the four-element rectangular-band counterexample from Turn2§3. Let G be any group, with its addition equal to its multiplication. The associated map on the group is the conjugation solution

    (g,h)↦(h,h^(-1)gh),

whose braid identity was proved in Turn2. On C×G use

    (a,g)+(b,h)=(a+_C b,gh),
    (a,g)(b,h)=(ab,gh).                                  (4.1)

This addition depends genuinely on both group coordinates when G is nontrivial. It is associative, and the brace law holds coordinatewise. Nevertheless, at ((0,1_G),(1,1_G),(1,1_G)), the two braid outputs differ by the last C-coordinate,3 versus1, exactly as in Turn2. Thus (4.1) fails Yang–Baxter for every group G.

The multiplication in(4.1) is a rectangular group with maximal subgroups isomorphic to G. On that exact same multiplication, taking addition equal to multiplication gives a solution by Turn2§4. Hence multiplicative structure, maximal groups and complete simplicity alone cannot distinguish success from failure. A full criterion must retain substantive information about the two-argument addition. The examples do not disprove the source's classification request or any properly stated ordinary/skew/weak-brace theorem.

## 5. Final five-turn outcome and exact gap

The five turns establish:

- The exact meet/retracted-addition criterion, with independent middle-coordinate and product-preservation countercontrols
- Arbitrary-addition results for left-zero and right-zero multiplication, a four-element rectangular failure, and the coinciding-law Rees classification
- All one-column, then all multi-column, retractions over arbitrary Rees multiplication, parametrized by idempotent residual maps and compatible column labels
- The exact existence/uniqueness and endomorphism criterion across arbitrary Clifford components
- Two-argument counterexample families over rectangular groups with any chosen maximal group

These are all-size theorems within stated subclasses, with exact finite checks as diagnostics. They are not a characterization of every generalized left semi-brace. General associative additions depending on both arguments, and their coupling with arbitrary non-Clifford completely regular components, remain unresolved. The strong-semilattice constructions in the literature do not prove that all source structures have such a decomposition respecting addition.

The original target therefore remains **unsolved,5/5 substantive author turns**, pending separate review of these partial results. No sixth proof-search turn will be used to fill this gap. No novelty or current historical-openness claim is made. A source-qualified partial packet, rather than a full-resolution PR, is the appropriate deliverable.
