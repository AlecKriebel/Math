# Complete fixed structural examples

All six authored fixtures are preserved below. Each matrix entry in row u, column v is its actual arc color when u points to v; a dot means no such arc, including the diagonal. Rows and columns are numbered from zero. These are explicit mathematical examples, not raw search enumeration. None is a conjecture counterexample.

## affine four color order9

The sharp four-color affine example has nine vertices. Each color has three SCCs of size three. Every vertex is a monochromatic source, but no color spans.

```text
. 3 . 0 1 2 . . .
. . 3 2 0 1 . . .
3 . . 1 2 0 . . .
. . . . 3 . 0 1 2
. . . . . 3 2 0 1
. . . 3 . . 1 2 0
0 1 2 . . . . 3 .
2 0 1 . . . . . 3
1 2 0 . . . 3 . .
```

## balanced without spanning color

This balanced three-color example has nine vertices. Each color has SCC sizes four and five; no color spans. Every vertex is a source. It has exactly 11 cyclic rainbow triangles and is not claimed rainbow-free.

```text
. 0 . 0 . 1 . 2 .
. . 0 . 0 . 1 . 2
0 . . 0 . 1 . 2 .
. 0 . . 0 2 . 1 .
0 . 0 . . . 2 . 1
. 1 . . 2 . 1 0 .
1 . 1 2 . . . . 0
. 2 . . 1 . 0 . 2
2 . 2 1 . 0 . . .
```

## color permuting rainbow triangle

The directed triangle is rainbow. Rotating the vertices and colors gives a transitive action, but it has no universal monochromatic source. It distinguishes color-permuting from color-preserving symmetry.

```text
. 0 .
. . 1
2 . .
```

## hamilton cycle with extra color arcs

This four-vertex tournament is monochromatic and has a Hamilton cycle plus extra arcs of that color. Its module {0,1} shows why mere containment of a Hamilton cycle does not imply colored primeness.

```text
. 0 0 .
. . 0 .
. . . 0
0 0 . .
```

## nonregular action order9

This nine-vertex two-used-color example has a color-preserving transitive group of order 27 and vertex-zero stabilizer order three. Its spanning-color set is exactly {0}. The supplied generators include a nonidentity shear fixing zero.

```text
. 1 . 0 0 0 . . .
. . 1 0 0 0 . . .
1 . . 0 0 0 . . .
. . . . 1 . 0 0 0
. . . . . 1 0 0 0
. . . 1 . . 0 0 0
0 0 0 . . . . 1 .
0 0 0 . . . . . 1
0 0 0 . . . 1 . .
```

Generator image lists, in vertex order:

- 3, 4, 5, 6, 7, 8, 0, 1, 2
- 1, 2, 0, 4, 5, 3, 7, 8, 6
- 0, 1, 2, 4, 5, 3, 8, 6, 7

## prime full core order7

This seven-vertex instance of the distance-colored family is cyclic-rainbow-free, colored-prime, and has its entire incidence core. Color zero is exactly one spanning directed cycle.

```text
. 0 1 2 . . .
. . 0 1 2 . .
. . . 0 1 2 .
. . . . 0 1 2
2 . . . . 0 1
1 2 . . . . 0
0 1 2 . . . .
```

For the general odd-order family and affine-line family, see the complete construction and proof in [STRUCTURAL_PROOFS.md](STRUCTURAL_PROOFS.md). The proofs apply to all stated orders; the listed fixtures are not the extent of the theorems.
