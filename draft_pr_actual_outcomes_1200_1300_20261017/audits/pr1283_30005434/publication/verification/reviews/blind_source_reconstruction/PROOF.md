# Independent source-only reconstruction of Dietzel Problem 3

Author: independent research subagent, acting within Alec Kriebel's research project. Alec Kriebel ORCID: https://orcid.org/0009-0001-9320-500X.

## Scope and exact mathematical input

The sole initial mathematical source was Carsten Dietzel, *Some problems on L-algebras*, Oberwolfach Report 9/2023, printed pp. 544-547. I inspected the supplied PDF's extracted text and the full supplied page images, including Definition 1, Definition 2, Problem 3, and the semilattice footnote. I did not inspect any candidate proof, PR text, audit conclusion, sibling report, or submission file.

Write a semilattice as `(X, meet)`, with `a <= b` meaning `a meet b = a`. The footnote specifies idempotence, associativity, and commutativity; it does not require a greatest element. Definition 2 requires a distinguished `e in X` and an operation `*` satisfying, for all `x,y,z`:

1. `x * (y meet z) = (x * y) meet (x * z)`;
2. `e * x = x`;
3. `(x meet y) * z = (x * y) * (x * z)`;
4. `x * e = e`.

Definition 1 additionally requires `x * x = e`, the cycloid identity, and the separation condition that `x * y = e = y * x` holds exactly when `x = y`. The cycloid identity already follows from item 3 and commutativity of `meet`.

The target consists of two existence questions: which semilattices admit Definition 2, and which admit Definition 2 and Definition 1 simultaneously. No nondegeneracy or prescribed relationship between `e` and the semilattice order is printed in Definition 2.

## Theorem

For the definitions as printed:

* A semilattice admits a meet-semibrace expansion if and only if its underlying set is nonempty. More precisely, every choice of a distinguished point admits one.
* A semilattice admits a meet-semibrace expansion that is also an L-algebra if and only if it has a greatest element. For a prescribed distinguished point `e`, this is possible if and only if `e` is that greatest element.

These statements hold without finiteness, lattice, distributivity, completeness, or cardinality assumptions.

## First question: proof of necessity and sufficiency

Necessity of nonemptiness follows from the requirement `e in X`.

For sufficiency, fix any point `e` of any nonempty semilattice and define

`x * y = y`.

Then `e * x = x` and `x * e = e`. Both sides of item 1 are `y meet z`, and both sides of item 3 are `z`. This proves all four axioms universally. In particular, the point need not be a maximum, or even maximal, in the semilattice order.

## Second question: necessity

In any L-algebra, different elements have different left translations. Indeed, put `L_a(t) = a * t`. If `L_a = L_b`, then

`a * b = b * b = e` and `b * a = a * a = e`,

so separation gives `a = b`.

Now suppose a meet-semibrace is also an L-algebra. Using item 3 with `y=e` and the unit axioms, for every `z` we have

`(x meet e) * z = (x * e) * (x * z) = e * (x * z) = x * z`.

Thus `L_(x meet e) = L_x`; injectivity of the indexing of left translations gives `x meet e = x`. Since this holds for every `x`, the distinguished element is the greatest element of the supplied semilattice. This argument establishes the connection to the supplied meet; it does not assume that connection from the separate canonical-order statement for L-algebras.

In fact, the orders must coincide. If `x meet y = x`, evaluate item 3 at `z=y` to obtain

`x * y = (x * y) * (x * y) = e`.

Conversely, if `x * y = e`, item 3 gives `L_(x meet y) = L_e L_x = L_x`, hence `x meet y=x`. Therefore `x * y=e` is equivalent to `x<=y` in every simultaneous structure.

## Second question: explicit universal construction

Let `(X,meet)` have greatest element `e`. Define

```
x * y = e           if x <= y,
        x meet y    if x is not <= y.
```

This is a total binary operation on the original set. It replaces the top of the principal ideal below `x` by the global top, after meeting with `x`.

### Unit, diagonal, and separation

`x<=e` and `x<=x`, so `x*e=x*x=e`. If `y=e`, then `e*y=e=y`. If `y!=e`, the greatest-element property implies `e` is not `<=y`, and `e*y=e meet y=y`. Thus `e*y=y` in all cases.

Moreover, `x*y=e` if and only if `x<=y`. The forward direction in the non-order case would imply `x meet y=e`; since `e` is greatest and `x meet y<=x,y`, that forces `x=y=e`, contradicting the non-order case. Antisymmetry of the semilattice order now proves separation.

### Preservation of meet

Fix `x,y,z`. If `x<=y` and `x<=z`, then `x<=y meet z`, and the two sides of item 1 are both `e`.

If `x<=y` but `x` is not `<=z`, then `x` is not `<=y meet z`. The left side is `x meet y meet z = x meet z`; the right side is `e meet (x meet z) = x meet z`. The symmetric case is identical with `y,z` exchanged.

If `x` is not `<=y` and is not `<=z`, then it is not `<=y meet z`; both sides are `x meet y meet z`.

These cases are exhaustive and use only the semilattice laws and the greatest-element property.

### Composition lemma

For this construction, whenever `u<=x`,

`L_u L_x = L_u`.

To prove it, fix `z`. If `x<=z`, then `L_x(z)=e`, `L_u(e)=e`, and `u<=z`, so `L_u(z)=e`. Otherwise `L_x(z)=x meet z`. Since `u<=x`, the conditions `u<=x meet z` and `u<=z` are equivalent. When they hold, both `L_u(L_x(z))` and `L_u(z)` equal `e`. When they fail, the former is `u meet x meet z = u meet z`, which is the latter. The identity follows for every `z`.

### Mixed identity and cycloid identity

If `x<=y`, then `x meet y=x` and `x*y=e`; consequently

`L_(x*y) L_x = L_e L_x = L_x = L_(x meet y)`.

Otherwise put `u=x meet y`. Then `x*y=u` and `u<=x`; the composition lemma gives

`L_(x*y) L_x = L_u L_x = L_u = L_(x meet y)`.

The two cases prove item 3 universally. Exchanging `x` and `y` in its left side gives the cycloid identity

`(x*y)*(x*z) = (y*x)*(y*z)`.

All of Definition 2 and all of Definition 1 have now been checked, proving sufficiency.

## Boundary cases and attempts at falsification

* Empty set: if empty semilattices are allowed by convention, neither expansion exists because a distinguished point is required. If the word semilattice already means nonempty, the first classification simply says all semilattices.
* Singleton: the unique point is the greatest element; the unique operation satisfies both questions, and the two constructions coincide.
* Non-top prescribed point: the first construction works, while the necessity argument rules out the second. A point being merely maximal is insufficient.
* Semilattice with no greatest element: the first construction works at every point, and the second is impossible. For example, the usual meet on the integers is `min` and there is no greatest integer.
* Infinite semilattice with a greatest element: the universal proof applies without modification. For example, all subsets of any set with intersection and the whole set as greatest element work.
* Nondistributive examples: both the five-element diamond `M3` and the pentagon `N5` have greatest elements, so both admit the second construction. No distributivity is used or implied. In `M3`, for distinct atoms `a,b`, the constructed product is the bottom, not a relative pseudocomplement.
* The source's later displayed order-based trivialization is a different operation: it retains `y` in the non-order case. It was not assumed to preserve the supplied meet. The construction above retains `x meet y`, which is the mechanism that permits every semilattice with a greatest element.

## Status

The two printed existence questions are completely resolved by the two universal proofs above. The strongest verified mathematical result is the full classification, including the prescribed-point form and equality of the two orders in every simultaneous structure. There is no remaining gap for the axioms as printed. Whether an author intended additional unstated conditions, and whether these constructions have prior appearances, are separate questions not settled by this source-only assignment.
