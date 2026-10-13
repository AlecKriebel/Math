# An orientation-preserving cap is not a path-preserving hole filler

This is a local obstruction for a candidate construction, not a complexity classification and not a claim that nonunique boards were previously unknown.

Use full orientations `(T,B,N,S,E,W)` and the initial orientation `(1,6,2,5,3,4)`. North decreases the row index. The north and south quarter-turns are mutual inverses and each has order four. Hence the word

`N N N N E S S S S`

has exactly the same terminal orientation as `E`, for every initial orientation. Its geometric trace covers a 2-column, 5-row rectangle, beginning at the bottom-left and ending at the bottom-right. For the specified initial orientation its labels, top row first, are

```
1 4
2 2
6 3
5 5
1 4
```

Thus replacing an existing horizontal edge by this eight-cell cap preserves the two port orientations on the intended traversal. This proves only forward extendibility when these extra cells and this traversal are available.

The same labeled rectangle, from the same bottom-left start and same full initial orientation, has the full-coverage word

`E N N N N W S S S`.

It ends at the left cell one row above the start, not the intended bottom-right port. Both words can be checked directly with the displayed die orientation. Finite enumeration found exactly these two full-coverage paths from this start state; exact exhaustiveness is not needed for the obstruction, since the second explicit word suffices. Both paths, including their full orientation at every cell, are given in the [exact authored certificate](EXACT_AUTHORED_CERTIFICATE.json).

Consequently an unconstrained final endpoint defeats the proposed claim that every complete traversal must finish at the other port. A surrounding reduction must exclude all unintended boundary access and account for the global endpoint. Correct net orientation does not establish an exact interface.

More generally, for any set S of cells and any Hamilton path P,

`|P ∩ δ(S)| ≡ number of endpoints of P in S (mod 2)`.

This follows by summing the path degrees over S: the sum is twice the number of internal selected edges plus the number of selected boundary edges. If S is a nonempty proper subset containing neither endpoint, connectivity additionally requires at least two boundary crossings. A filler attached to the rest through a single possible selected edge therefore cannot be an internal detour. For a cycle every proper visited filler set similarly needs a positive even number of boundary crossings.

The cap does not eliminate arbitrary holes: no construction has been supplied that decomposes arbitrary blocked regions into such caps, guarantees forced attachment edges, labels all remaining cells, isolates all boundaries, and proves both directions for corner-start paths.
