# Independent checks on the old counterexample

This is an application audit of published results, not a new obstruction
theorem or a fresh proof-search attempt. Source locations are in
[SOURCE_AUDIT.md](SOURCE_AUDIT.md).

## 1. A completely specified input

Give the circle six successive marked positions `0,1,2,3,4,5`. Identify pairs
according to the arrows

```
a = (4,0), b = (3,1), c = (5,2).
```

At an arrow `(tail,head)`, make the ordered tangent vectors positive in the
oriented surface. At the corresponding four-valent vertex the cyclic dart
order is `(tail+, head+, tail-, head-)`, where `+` is outgoing along the
oriented circle and `-` is incoming. Glue untwisted ribbons between successive
circle positions; then cap every boundary circle of this ribbon neighborhood
with a disk. The core circle becomes a smooth generic curve on a closed
oriented surface, with precisely three transverse double points. This gives
the realization directly, without relying on an unread picture.

The signed word is Carter's `a b c b^-1 a^-1 c^-1`. With his left-to-right
crossing convention the negative letter is the arrow tail. Reversing every
arrow changes the surface orientation convention but does not change the
polynomial computed below. Thus a simultaneous sign-convention reversal
cannot make this obstruction disappear.

## 2. Genus from a ribbon permutation

There are `V=3` vertices and `E=6` edges. Let `sigma` be the above rotation
permutation and let `tau` pair `i+` with `(i+1)-`, modulo 6. Boundary components
are cycles of `sigma*tau`. There is exactly one cycle:

```
0- -> 2+ -> 1- -> 4- -> 1+ -> 5+ ->
4+ -> 2- -> 3- -> 5- -> 0+ -> 3+ -> 0-.
```

Consequently the capped surface has `chi=V-E+1=-2`, hence genus **2**.
This verifies the ambient genus independently of Carter's genus assertion.

## 3. Polynomial by direct endpoint counting

For an arrow `e=(a,b)`, count `+1` for another arrow whose tail, but not head,
is in the positively directed open arc from `a` to `b`, and `-1` when only
its head is in that arc. Let the sum be `n(e)`. The ordered linking matrix is

```
      a   b   c
a     0   0   1
b     0   0   1
c    -1  -1   0
```

Its row sums are `(1,1,-2)`, so

```
u(t) = sum_(n(e) != 0) sign(n(e))*t^abs(n(e)) = 2t - t^2 != 0.
```

Useful sanity checks are `sum n(e)=0` and `u'(1)=0`. Reversing all arrows
preserves this polynomial; reversing the circle negates it. Either sign is
nonzero. No assignment of over/under crossing data is involved.

For a redundant genus check, the homological based matrix in order
`(s,a,b,c)`, computed from Turaev's Section 4.2 formula, is

```
 0  -1  -1   2
 1   0   0   1
 1   0   0   2
-2  -1  -2   0
```

Its Pfaffian is `-1` and determinant is `1`; its rank is 4, agreeing with
genus 2. The ribbon calculation does not depend on this formula.

## 4. Audit of the topological implication

Here is the disk specialization of the published obstruction argument.
Write `K=ker(H_1(boundary M;Z) -> H_1(M;Z))` and `s=[gamma]`.
Double-decker arcs of a generic disk induce an involution on its boundary
crossings. For a singleton crossing the corresponding half-loop class lies
in `K`; for a paired orbit the sum of its two half-loop classes lies in `K`.
Also `s` lies in `K`. The oriented boundary intersection form vanishes on
`K x K`; hence singleton indices are zero and paired indices sum to zero.
Every orbit's contribution to `u` cancels. The source proof includes simple
branch points, which create singleton orbits. For `(1,1,-2)` the four possible
partitions into singletons/pairs all fail these required index sums.

This explains which hypotheses the application needs. It does not purport to
derive a sufficient criterion from the cancellation condition.

## 5. Why nonorientable fillings do not provide an escape

This applicability check does not assume that an oriented boundary forces the
whole 3-manifold to be orientable; that assertion would be false.

Suppose `gamma` had a disk extension in a nonorientable `M`. Take the connected
component containing its boundary and then its orientation double cover
`p: Mtilde -> M`. The outward normal line along the boundary is trivial, so
`w_1(TM)|S = w_1(TS)=0`. Therefore `p^-1(S)` consists of two disjoint copies of
`S`. Because the disk is simply connected, its map lifts to `Mtilde`. Its
boundary lift lies entirely on one copy of `S`, and has the same arrow diagram
up to the orientation choices already checked.

The oriented obstruction applies to that lifted disk. It allows other unused
boundary components, so it already gives a contradiction. Alternatively cap
the other copy of `S` by an oriented handlebody; the lifted disk is unchanged
and the resulting oriented manifold has exactly the selected `S` as boundary.
Compactness is preserved. A covering is a local diffeomorphism, so it also
preserves the permitted stable local models if those are required.

Thus the example obstructs **any** compact bounding 3-manifold, rather than
only an already chosen handlebody or only an oriented choice of `M`.

## 6. Scope and verification limits

- A disk extension implies null-homotopy. For a fixed smooth filling, a
  null-homotopy can be put in boundary-product form using a collar and then
  made generic relative to that collar. This keeps the source a disk
- “Proper” in the present question requires the boundary-preimage condition;
  ordinary compact-preimage properness alone is automatic for a compact disk
- Odd crossing count alone rules out certain **immersions**, not the allowed
  maps with branch points. The nonzero polynomial is essential here
- Changing the source to a positive-genus surface changes the question
- Vanishing `u`, existence of a formal pairing, or algebraic sliceness is not
  being claimed sufficient
- The verifier checks 24 basepoint/orientation variants, all four crossing
  partitions, two genus computations, small-diagram sanity cases, and invalid
  input rejection. It proves no unrestricted topological decision result

The full conclusion is the historical counterexample to universal existence.
Nothing here resolves arbitrary prescribed inputs that escape known
obstructions.
