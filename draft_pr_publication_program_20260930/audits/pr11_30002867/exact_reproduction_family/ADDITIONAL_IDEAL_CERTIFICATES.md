# Additional independent ideal certificates for the matrix tests

These complete the expected-data arguments for cases not covered by the
explicit resolutions in `ideal_certificate/REPORT.md`. They use polynomial
ideals, coordinate changes, and localization, not the proposed matrix-rank
formula. The coefficient field for the target remains C.

## 1. Univariate nonreduced and nonreal support

`f=x⁴+x²=x²(x−i)(x+i)`. The factors are pairwise coprime, giving by the
Chinese remainder theorem a length-two quotient at zero and reduced quotients
at i and −i. Global length is four. At each point the ideal localizes to a
nonzero principal ideal in the one-variable polynomial local ring, and the
minimal resolution of its quotient is `0→R→R→R/(f)→0`. Its localized
differential is multiplication by a nonunit, so each Betti vector is `(1,1)`.
The map is injective because the polynomial ring is a domain. D2 has no
columns; this covers the candidate's d=1 boundary without assuming distinct
roots or real support.

## 2. Algebraic spectra and coefficient fields

For `(x²−2,y²)`, write `a=±sqrt(2)`. At `(a,0)` the other factor of
`x²−2=(x−a)(x+a)` is a unit. The localized ideal is therefore
`(x−a,y²)`. The quotient has basis `1,y` and length two. These two parameters
are a regular sequence: first kill the independent polynomial coordinate
`x−a`, then the nonzero element `y²` in the one-variable domain. Tensoring
the two two-term resolutions gives the exact minimal Betti vector `(1,2,1)`.
There are two support points and total length four.

For `(x²−2,y²+1)`, both factors are separable. At each of the four points
`(±sqrt(2),±i)`, the local ideal is its maximal ideal `(x−a,y−b)` because
the remaining scalar factors are units. Each point is reduced and its
minimal Betti vector is `(1,2,1)`. Tensoring the univariate quotients gives
global length four.

For `(x²−sqrt(2),y²)`, the same argument applies with
`a=±2^(1/4)` in the explicit algebraic extension. The derivative `2a` is
nonzero, so the x roots are simple. The local quotient again has length two
and Betti vector `(1,2,1)`. This tests an input coefficient extension as well
as a splitting extension; it does not claim exact computability of arbitrary
complex numbers.

## 3. Six-variable nonlinear curvilinear CI

Set `a=b0` and `c_i=b_i−b0^(i+1)` for 1≤i≤5. This is a polynomial
automorphism with inverse `b0=a`, `b_i=c_i+a^(i+1)`. It fixes the origin.
The supplied ideal becomes `(a⁷,c1,…,c5)`.

The quotient basis is `1,a,…,a⁶`, giving length seven. Each generator is
nonzero and independent modulo the maximal ideal times this monomial ideal:
no displayed generator is divisible by a positive-degree monomial times
another displayed generator. Consequently the generator count is six.

The six-term coordinate sequence is regular. Multiplication by each new c
coordinate is an injective coefficient shift, and after imposing them all,
`a⁷` is a nonzero element of the one-variable domain. Tensoring the two-term
resolutions gives an exact minimal resolution with Betti vector
`(1,6,15,20,15,6,1)`. The coordinate automorphism preserves exactness and
minimality.

## 4. Four support points with the full global length

The components used are:

- `K+(z)` at (0,0,0): length five, Betti `(1,4,5,2)` by tensoring the
  independently proved plane resolution `(1,3,2)` with the two-term z
  resolution.
- J translated to (−2,3,5): length five, Betti `(1,5,5,1)`.
- The triangular coordinate CI translated to (2,−1,4): length six,
  Betti `(1,3,3,1)`.
- A reduced point at (7,−1,4): length one, Betti `(1,3,3,1)`.

Let the translated component ideals be I_j. Each radical is the distinct
maximal ideal of its named point. More explicitly, each I_j contains some
power of its first coordinate difference `x−a_j`. The four scalars a_j are
distinct, so the corresponding univariate powers are pairwise coprime.
Bezout identities show `I_j+I_k=R`. Thus

`R/(intersection_j I_j) ≅ product_j R/I_j`

by CRT, with length 5+5+6+1=17. The unit maps to the tuple of component
units, so the block-diagonal matrices are a regular quotient representation,
not just a direct sum of arbitrary modules. Localizing at one support point
kills every other component and leaves exactly its certified local ideal.
The local generator counts 4,5,3,3 therefore are independent expected data.

This argument proves the local expected counts used by the computation. It
does not invoke or independently reprove a general global efficient-generation
theorem for the intersection ideal.

## 5. A valid discontinuous family and exact ideal equality

Let

`I_e=(x²,xy,y²−e*x)`.

At e=0 this is `(x,y)²`, whose three distinct quadrics minimally generate
it; the quotient basis is `1,x,y`.

For e≠0, let `L_e=(x−y²/e,y³)`. The identity

`e*xy+y*(y²−e*x)=y³`

and the third generator show `L_e⊆I_e`. Conversely,

`xy=y*(x−y²/e)+y³/e`,

`x²=(x+y²/e)*(x−y²/e)+y⁴/e²`,

`y²−e*x=−e*(x−y²/e)`

show `I_e⊆L_e`. Hence the ideals are equal. The polynomial automorphism
`a=x−y²/e,b=y` identifies the ideal with `(a,b³)`. It is a height-two
CI of length three and has Betti vector `(1,2,1)`.

The fixed basis `1,x,y` remains independent for every e: for e≠0 it maps
to `1,y²/e,y` in `C[y]/(y³)`; at zero it is the square-zero basis.
The matrices depend polynomially on e, with their only variable entry given
by `y*y=e*x`. Thus the CI indicator is discontinuous within the permitted
regular-representation input class. This is a deductive instability example,
not merely the empirical observation of one numerical rank routine.

## 6. A nonregular commuting tuple with a false D2 signal

For the regular quotient `C[x,y]/(x,y)²`, use basis `1,x,y`. Its coordinate
matrices are

```text
Mx = [[0,0,0],[1,0,0],[0,0,0]],
My = [[0,0,0],[0,0,0],[1,0,0]].
```

Transpose both. The resulting X,Y commute. Because polynomial evaluation
in commuting transposes transposes the original evaluation, their annihilator
is still `(x,y)²`. They are a faithful representation of the same algebra,
but not its regular representation.

At the origin, `[X Y]` has image the line spanned by the first basis vector,
so its rank is one. The map `[-Y; X]` maps a vector `(a,b,c)` to
`(-c,0,0,b,0,0)`, and hence has rank two. Thus D2 equals the CI target
`(d−1)(N−1)=2` while the annihilator is not CI. The regular support-rank
test already fails because one is not N−1=2. This proves the necessity of
the scope restriction without depending on a computed rank result.
