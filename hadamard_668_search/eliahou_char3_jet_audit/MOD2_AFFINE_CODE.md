# Characteristic-two affine code

After division by the common integer content four, every quadratic
coefficient in the twenty independent anti-fold equations is even.
Consequently, over `F_2` the normalized norm equation is exactly

```
A x = b.
```

This is the Frobenius linearization of the norm layer, not a relaxation of
some remaining quadratic system.  Adding the necessary parity consequence
of weight 39 gives

```
[ A ] x = [ b ]
[ 1 ]     [ 1 ].
```

`verify_mod2_affine_code.py` row-reduces this augmented system, constructs
one particular point and one null vector for every free coordinate, and
checks the parameterization by direct matrix multiplication.

For canonical case 26 there are 78 support variables.  The twenty norm
rows have rank 20; the weight-parity row is independent, so the augmented
affine space has rank 21 and dimension 57.  For canonical case 0 the
corresponding dimensions are 79, rank 21, and affine dimension 58.

There is a sharper quotient description.  In case 26 the 78 columns of
`A` form exactly 39 equal-syndrome pairs.  They are the reflected cell
pairs, with the two central cells `("L",20)` and `("S",20)` forming one
cross-block pair.  Thus the modulo-two layer depends only on the 39 pair
parities.  Those parities form an 18-dimensional affine quotient after
weight parity is imposed, while the 39 within-pair fiber bits account for
the remaining dimensions:

```
57 = 18 + 39.
```

Case 0 has 39 syndrome pairs and one singleton.  Its quotient dimension is
19 and its fiber dimension is 39, giving `58 = 19 + 39`.

The verifier completely enumerates these small quotients and lifts every
parity state to weight 39 by a closed binomial count.  The exact sizes of
the fixed-weight characteristic-two slices are

```
case 26: 25,941,166,955,843,488
case  0: 51,310,052,181,007,034
```

These counts make clear that characteristic two is a major structural
reduction but not, by itself, a small remaining exhaustive search.

Weight 39 itself is not linear—it is a slice of these parity-compatible
affine spaces.  `search_mod2_affine_code.py` obtains exact points in that
slice and moves only by null-code words having equally many selected and
unselected coordinates.  Its complete low-weight move catalogs use null
words of weights 2, 4, and 6.

In the bounded runs recorded during the audit, this search reached
characteristic-three defect 2 for both cases 0 and 26.  An exact joint
modulo-two/modulo-three SAT check excluded the entire Hamming-radius-eight
ball around the pinned best case-26 point.  That is a rigorous local fact,
not a global exclusion and not evidence that the two affine/jet layers are
disjoint.
