# Turn 2: arbitrary additions over projection multiplication and a Rees-matrix branch

**Unreviewed structural partials. Original target remains unresolved,2/5 turns.** This route moves beyond meet multiplication and the special addition from Turn1. All associated maps are computed from the original formula and all three braid coordinates are retained. No novelty is claimed for these elementary semigroup consequences.

## 1. Left-zero multiplication: exactly additive bands, all giving solutions

Suppose multiplication is left zero, ab=a. This is completely regular with a^-=a. For an associative addition, the brace identity becomes

    a=a+a.

Thus the compatible additions are exactly bands, meaning associative idempotent operations. For every such addition, the original map is

    r(a,b)=(a,a+b).

Both braid words send (a,b,c) to

    (a,a+b,a+b+c).

Indeed the only reductions are a+a=a and b+b=b, together with associativity. Hence every generalized left semi-brace with left-zero multiplication produces a solution, for arbitrary cardinality and arbitrary additive band. No commutativity or cancellation is needed.

## 2. Right-zero multiplication: a different exact additive condition

Now let ab=b, again with a^-=a. The brace law is precisely

    b+c=b+a+c   for all a,b,c.                            (2.1)

Thus, among associative additions, this is an exact description of the compatible ones. Equivalently, every three-term sum x+y+z equals x+z. Such an addition need not be a band: a constant-zero addition on a larger set is allowed.

The associated map is

    r(a,b)=(a+b,b).

The left braid word gives ((a+b)+(b+c),b+c,c) and the right gives (a+(b+c),(b+c)+c,c). Equation(2.1) reduces both to

    (a+c,b+c,c).

Therefore every compatible associative addition also gives a solution in this branch. This result concerns projection multiplication; it is different from the original source's projection-addition examples.

## 3. Combining the two projection directions can fail

Let S={0,1,2,3}, identified with {0,1}×{0,1} by a=2*i+j. Define rectangular-band multiplication

    (i,j)(k,l)=(i,l),

and addition by

    a+b=0 if a=0 or b=0, and a+b=2 otherwise.              (3.1)

Addition is associative: zero is absorbing, and every sum of nonzero inputs is2, which is nonzero. All multiplicative elements are idempotent and are their own group inverse.

The brace identity holds. Write the row of a as i. The product a(b+c) is (i,0), since every additive output has column0. On the right, a(a+c) also has column0. If i=0 this latter factor is0 and the sum is0=(i,0). If i=1 both ab and a(a+c) have row1, hence are nonzero, and their sum is2=(i,0). This proves compatibility for all triples without relying on a computer search.

Its tables, with rows and columns ordered0,1,2,3, are

    multiplication        addition
    0 1 0 1              0 0 0 0
    0 1 0 1              0 2 2 2
    2 3 2 3              0 2 2 2
    2 3 2 3              0 2 2 2.

Directly applying the source map at (0,1,1) gives

    r_12 r_23 r_12(0,1,1)=(0,0,3),
    r_23 r_12 r_23(0,1,1)=(0,0,1).

Consequently rectangular-band multiplication alone, even together with the full brace identity and additive associativity, does not ensure Yang–Baxter. It is non-Clifford: its idempotents do not commute. This example blocks an attempted extension from the two projection cases to all completely simple multiplication. It does not refute any properly stated ordinary or weak-brace theorem.

A coordinate enumeration specific to this four-element rectangular multiplication finds26 labeled compatible associative additions,16 yielding solutions and10 failing. The example above is one failure. These finite counts are supplementary, not an arbitrary-size classification.

## 4. Coinciding laws in an arbitrary Rees-matrix presentation

Let G be any group, I and Λ nonempty sets, and P=(p_(λ,i)) a matrix of group elements. On S=I×G×Λ define

    (i,g,λ)(j,h,μ)=(i,g p_(λ,j) h,μ).                     (4.1)

This is the standard Rees-matrix completely simple construction, used explicitly here rather than assuming every source structure has already been reduced to it. Associativity follows directly. The commuting group inverse and local identity of a=(i,g,λ) are

    a^-=(i,p_(λ,i)^(-1) g^(-1) p_(λ,i)^(-1),λ),
    a^0=(i,p_(λ,i)^(-1),λ).                              (4.2)

Set addition equal to multiplication. We characterize exactly when this is a generalized left semi-brace and prove that all such cases give solutions.

### Compatibility is exactly a row-column factorization of P

For coinciding laws the brace identity is

    abc=ab a^0 c.                                       (4.3)

Using (4.1)–(4.2) and cancelling only inside G, this is equivalent to

    p_(μ,k)=p_(μ,i) p_(λ,i)^(-1) p_(λ,k)                 (4.4)

for every i,k∈I and λ,μ∈Λ. Fix i0,λ0. Equation(4.4) is equivalent to a factorization

    p_(λ,i)=u_λ v_i,                                   (4.5)

where u_λ=p_(λ,i0) and v_i=p_(λ0,i0)^(-1)p_(λ0,i). Necessity follows by taking i=i0, λ=λ0 in(4.4); sufficiency follows by substituting (4.5), with the order of the noncommuting factors preserved. This is group factorization, not a commutative matrix-rank assertion.

When (4.5) holds, the bijection

    (i,g,λ) ↦ (i,v_i g u_λ,λ)                           (4.6)

takes multiplication to rectangular-group multiplication

    (i,g,λ)(j,h,μ)=(i,gh,μ).

Indeed the group coordinate of the image of a product is v_i g p_(λ,j)h u_μ=(v_i g u_λ)(v_j h u_μ). The inverse of (4.6) multiplies by v_i^(-1) and u_λ^(-1), so it is an isomorphism of both coinciding laws. This proves the exact compatibility classification within the entire presented Rees family.

### The associated map always solves Yang–Baxter in the compatible branch

In normalized rectangular-group coordinates, substitute the actual group inverse from (4.2) into the source formula. For a=(i,g,λ), b=(j,h,μ), it gives

    r(a,b)=((i,h,μ),(i,h^(-1)g h,μ)).                    (4.7)

In particular both outputs have row i and column μ. Replacing (a^-b)^- by b^-a would give incorrect index coordinates in this non-Clifford setting.

Map(4.7) is the Cartesian product of three maps:

    (i,j)↦(i,i),
    (g,h)↦(h,h^(-1)g h),
    (λ,μ)↦(μ,μ).

The first and third satisfy the braid equation by direct duplication. Both braid words for the middle map send (g,h,k) to

    (k,k^(-1)h k,k^(-1)h^(-1)g h k).

Thus all three maps, and consequently their product, solve Yang–Baxter. Transporting by (4.6) proves the claim for every compatible P. This proof allows arbitrary groups, arbitrary nonempty index sets, and non-bijective maps when an index set has more than one element. It does not invoke a Clifford hypothesis or assume anti-multiplicativity of the commuting group inverse.

This branch completely handles coinciding laws in (4.1). It does not handle general associative additions on that same multiplication: section3 is an explicit warning that those can fail.

## 5. Exact finite controls and scope

verify_turn2.py tests both projection-multiplication branches against every associative table of orders at most3, validates the four-element counterexample directly, and checks the Rees factorization/gauge/braid calculations over cyclic and noncommutative groups. rectangular_catalogue.py separately enumerates every compatible addition for the specific2×2 rectangular multiplication, using necessary column-profile constraints from the brace equation and then checking all remaining axioms.

No finite enumeration is used as proof of the arbitrary-cardinality statements in sections1,2 or4. All these claims follow from the displayed identities.

The original full characterization remains open within this campaign. In particular, additions that do not have the special shapes above and completely regular multiplication not covered by the explicit presentation still require analysis. The four-element counterexample shows that even a very simple non-Clifford multiplicative structure does not eliminate that difficulty. Two substantive author turns are complete; no final unsolved disposition or claimed full result is made yet.
