# Independent real-coordinate derivation and direct written-proof audit

This derivation was made from direct real projections and paired-edge expansion,
before reading the archive's real-coordinate derivation or review_01. The
companion fresh exact checker verifies the local polynomial equalities in the
quotient by the two unit-normal equations.

Let the real pedal point be `m=(X,Y)`, the positive support foot be `w_i=h_i n_i`,
and the doubled normal be `U_i=(cos 2psi_i,sin 2psi_i)`. Define

```
A(U) = [[U_x,U_y],[U_y,-U_x]],    B(U)=A(U)/2.
Q_i = m/2 + V_i,                 V_i = w_i-B(U_i)m.
```

Half-period pairing negates `w_i` and fixes `U_i`. Every mixed area term cancels,
and `cross(B(U)m,B(V)m)=|m|^2 cross(U,V)/4`. Consequently
`S(Q)=S(0)+|m|^2 S_U/4`, with no division by area.

For a paired edge `(i,i+N/2)`, its averaged first moment has only a linear and a
cubic part. Its linear matrix, derived directly from real cross products, is

```
K m = -cross(w_i,w_j)(B_i+B_j)m
      -[cross(w_i,B_j m)+cross(B_i m,w_j)](w_i+w_j).
```

Put `alpha=cross(U,V)`, `(u_x,u_y)=U+V`, `D=F/d`. Substituting only the support
squares and support product gives the division-free identity

```
K = Phi(U)-Phi(V) - alpha/4 *
    [[D+2H+3e+(2D+e)u_x, (2D-e)u_y],
     [(2D+e)u_y, D+2H-3e+(e-2D)u_x]],

f(U)=H U_x+e(U_x^2-U_y^2),   g(U)=H U_y+2e U_x U_y,
Phi(U)=1/4 [[g+e U_y,-f-e U_x],[-f+e U_x,e U_y-g]].
```

The endpoint potential telescopes for every closed ordered polygon, without
simplicity or any area assumption. The cubic term of that averaged edge is
`-|m|^2 alpha A(U+V)m/8`.

The doubled-normal dot relation is `U·V=u+v(U_x+V_x)`. In real coordinates the
unit-circle identity is

```
cross(U,V)(U+V)=(1+U·V)(V_y-U_y,U_x-V_x).
```

Its constant term telescopes. Also
`sum (U_x+V_x)(V_x-U_x)=0` and
`sum (U_x+V_x)(V_y-U_y)=sum cross(U,V)=2S_U`.
Thus `sum alpha(U+V)=(2v S_U,0)`, even for self-intersections and zero area.
Together with `sum alpha=2S_U`, the matrix/potential formula yields

```
T(V)_x = -S_U X [D(1/2+v)+H+3e/2+ev/2+v|m|^2/4],
T(V)_y = -S_U Y [D(1/2-v)+H-3e/2+ev/2-v|m|^2/4].
```

These are exactly the real and imaginary parts of the manuscript's complete
cubic identity. Translation gives `T(Q)=T(V)+3m S(Q)` because translation by
`m/2` changes `T` by `6(m/2)S`. The signed-triangle formula, or direct closed
shoelace expansion, proves that translation law even for self-intersecting or
zero-area polygons. Only the final centroid division requires `S(Q)!=0`.

## Direct general geometric audit

1. `T` is an orientation-preserving circle homeomorphism for the fixed positive
   tangent choice. The porism gives finite order `N`; `A=-id` commutes with it,
   so the generated group is finite. Every finite-order orientation-preserving
   circle homeomorphism with a fixed point is the identity: on the cut interval,
   a moved point has strictly increasing or decreasing iterates. A stabilizer of
   any point is therefore trivial. The group acts faithfully on a finite orbit,
   and its order-preserving permutation action is a subgroup of the cyclic
   rotation group. The unique nontrivial involution is both `A` and `T^(N/2)`.
   This reasoning uses least even period; a repeated odd orbit does not qualify.

2. The origin lies strictly inside the caustic. For the positive tangent branch
   it lies on the left of every directed billiard chord, so `cross(P_i,P_j)>0`.
   On the centrally symmetric boundary the lifted forward boundary step is
   strictly less than a half-turn. The increasing Gauss map commutes with the
   half-turn, giving `0<Delta_i<pi`, including stars. Hence every origin pedal
   area summand `h_i h_j sin Delta_i` is positive. Adjacent normals cannot be
   equal or antiparallel; outer tangent intersections are finite.

3. The chord tangency relation follows by evaluating the confocal ellipse's
   support in the chord's normal direction. The manuscript's conversion to
   unit-normal support is checked independently coefficient by coefficient.
   The factors `F+ed=a^2-lambda(a^2/b^2-1)>b^2` and
   `F-ed=b^2+lambda(1-b^2/a^2)>0` prove all displayed denominator controls.
   Squaring a true support relation supplies a necessary dot relation; the proof
   never uses it backwards to assert an orbit, so squaring introduces no gap.

4. The origin-area identity uses
   `cos(psi_i+psi_j) sin(psi_j-psi_i)=(sin2psi_j-sin2psi_i)/2`.
   The endpoint terms telescope in trajectory order. With `d!=0`, positive
   `S(0)` forces nonzero `S_U`; its sign may be negative for stars, and the proof
   never assumes otherwise.

5. For `N=4`, the two support relations use an antipodal third normal; their
   right sides negate while their left sides agree. Positive support implies
   `d=0`. Conversely `d=0` implies every normal step is exactly `pi/2`, hence
   least period four, not a larger primitive period. The separate rectangle
   calculation avoids dividing by `d` or `S_U`.

6. For every simple winding-one even period `N>=6`, trajectory normals are
   circularly ordered. The first `N/2` span exactly a half-turn; doubling yields
   `N/2>=3` distinct circularly ordered points. The full doubled-normal polygon
   traverses their strictly convex polygon twice, so `S_U>0`. Thus `D>0` and
   `d>0`. Period four has `d=0`. This proves all-M validity for every such family,
   not merely finitely tested periods.

7. The zero locus follows from `S(0)>0`, `F>0`, and the full polynomial area
   identity: no zeros for `d>=0`; precisely the circle `|m|^2=-2F/d` for `d<0`.
   At circle points the signed centroid as defined is excluded, irrespective of
   possible numerator zeros. The explicit formula divides exactly by `G` and
   agrees with the preceding undivided identities.

8. Reversing order negates both area and moment, while centroid remains fixed.
   Repeating an even least-period orbit multiplies both equally. Reflection
   reverses signed area and transforms the moment accordingly. The theorem
   explicitly excludes circular boundaries, hyperbolic/degenerate caustics,
   unsigned region centroids, and odd least periods; no proof step extends the
   conclusion silently to those cases.

The written complex edge identities were also inspected directly: the pairing
is an average, but summing averages over all N edges equals the original sum;
there is no missing factor two. The `r` sum is `-4iS_U`, the `s` sum is
`-2iT_U`, and all endpoint differences are cyclic. The real expansion above
independently fixes their signs and linear/cubic constants.
