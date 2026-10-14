# Approach 2: a local obstruction surviving projectivization

Status: the unrestricted natural higher-dimensional short exact sequence is false, even for hyperplanes. This does not settle the source's broader request for a suitable generalization or characteristic-class method.

## Example and credit

Use homogeneous coordinates [x:y:z:w] on P^3. Let H=(z=0) and let A be the six planes with product
f=xy(x-z)(y-z)(x-y+z)(x-y-z).
The total divisor A+H is the seven-plane arrangement used by Abe–Kawanoue, arXiv:2406.00305v2, Example 4.3(3), in affine three-space. Their Euler-restriction cokernel has dimension two. We reconstruct a concrete nonliftable derivation and place that affine example in a projective chart; the arrangement and obstruction are credited, not claimed new.

All components are smooth. At every point, a hyperplane arrangement is analytically a product of a central linear arrangement with smooth directions; factors not vanishing are units and do not affect its reduced divisor. Thus A and A+H are locally quasihomogeneous. On H, the reduced intersection R is xy(x-y)=0. The point p=[0:0:0:1] remains in P^3, and the chart w=1 is A^3.

## Nonliftability proof

On H near p, eta=x(x-y) partial_x is logarithmic for R. Suppose eta lifted to a germ theta logarithmic for A+H. Complete at p and take the homogeneous degree-two coefficient part. Since every defining form is linear, each tangency ideal is homogeneous, so that part is itself logarithmic. Its restriction to z=0 is eta. Hence it suffices to exclude a homogeneous quadratic lift.

Tangency to x, y and z forces any such lift to have coefficients
u=x(x-y+a z), v=b y z, t=z(c x+d y+e z)
for constants a,b,c,d,e in C. Tangency to x-z gives d=-1 and c+e=1+a. Tangency to y-z gives c=0 and b=d+e. Consequently e=1+a and b=a.

But on the hyperplane x-y+z=0, substituting x=y-z yields
u-v+t = -2z(y-z),
which is not the zero polynomial. This contradicts tangency, independently of a. The additional factor x-y-z is not needed for this contradiction but is retained to match the credited example exactly. Therefore the restriction map
D_{P^3}(A+H) -> i_*D_H(R)
is not surjective at p.

The map has the usual kernel D_{P^3}(A)(-H), proved separately in Approach 3. Thus the natural analogue with quotient D_H(R) fails right exactness. Merely retaining the original line bundle O_H(-K_H-R) cannot be the general replacement either: away from R the quotient is T_H of rank two. The determinant loses rank and does not fix the issue.

For every n>=3 the same equations in P^n give the same obstruction along the linear locus x=y=z=0: adjoining smooth coordinates cannot create a lift, since restricting all other coordinates to constants preserves the tangency equations and the prescribed eta. The dimension-two theorem is consistent with this: the affine origin disappears on Proj C[x,y,z], but remains in the affine chart of P^3 used here.

## What remains

This disproves an explicitly stated natural blanket extension, not every possible higher-dimensional theorem. It neither rules out a defect term nor rules out stronger freeness, transversality or characteristic-class hypotheses. The complete original request is retained as unresolved.
