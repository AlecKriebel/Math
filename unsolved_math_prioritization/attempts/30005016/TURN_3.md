# Turn 3: a complete obstruction to a natural four-space construction

AI-assisted mathematical proof candidate; independent review pending.

## 1. The attempted improvement and result

The five-space cover in turn 1 uses two univariate cubic spaces and three quadratic extensions of the affine space. Can two suitably chosen quadratic extensions replace the three and give a four-member cover?

No. Over any characteristic-zero field K, for arbitrary polynomials q_1,q_2 of degree at most two, the four spaces

A=span{1,x,x²,x³}, E=span{1,y,y²,y³}, Q_j=span{1,x,y,q_j} (j=1,2)

do not cover all four-point configurations. The conclusion includes the case when one Q_j has dimension below four, which plainly cannot help. It also applies after every invertible affine change of the coordinate pair (x,y). This is an obstruction to an entire construction class, not a lower bound of five for arbitrary spaces.

We prove it by realizing every possible nonzero quadratic determinant direction on configurations for which both coordinates repeat.

## 2. Realization lemma

For an ordered configuration P of four points, write

D(P)=(det[1,x,y,x²], det[1,x,y,xy], det[1,x,y,y²]),

with evaluations at the four points as the rows. For every nonzero vector (U,V,W)∈K³, there exists a four-point configuration with a repeated x-coordinate and a repeated y-coordinate, and D(P) a nonzero scalar multiple of (U,V,W).

### Case A: V≠0

Choose c∈K with c≠0, c≠U/V, and, if W≠0, c≠V/W. At most three values are forbidden; K is infinite. Define

a=1−cW/V, b=c−U/V,

and take the ordered points

(0,0), (0,a), (b,0), (c,1).

Here a,b,c are nonzero. All four points are distinct: the first three lie respectively at the origin and on the two punctured axes; the fourth has both coordinates nonzero. The first two points repeat x=0, and the first and third repeat y=0. Subtracting the first row in each determinant and expanding gives

D(P)=−ab·(c(c−b), c, 1−a)=−abc/V·(U,V,W).

The scalar is nonzero, as required.

### Case B: V=0 and U,W are both nonzero

Choose nonzero r,t∈K with r²≠U and t²≠−W. Put s=U/r and u=−W/t. Then r,s,t,u are nonzero, r≠s and t≠u. Take

(r,0), (s,0), (0,t), (0,u).

These are four distinct points, with repeated coordinates on both axes. Direct expansion gives

D(P)=(s−r)(t−u)·(rs,0,−tu)=(s−r)(t−u)·(U,0,W).

Again the multiplier is nonzero.

### Case C: exactly one of U,W is nonzero and V=0

If U≠0, use (0,0),(1,0),(2,0),(0,1). Its determinant vector is a nonzero multiple of (1,0,0), and both coordinates repeat. If W≠0, interchange x and y. The exact nonzero scalar need not equal U or W, since only the projective direction is prescribed. These exhaust all nonzero vectors. ∎

## 3. Defeating every pair of quadratic choices

Write the homogeneous quadratic parts as

q_j = A_j x²+B_j xy+C_j y² + affine terms.

The two linear equations A_j U+B_j V+C_j W=0 have a nonzero solution in K³. Apply Section 2 to such a solution. Because the first three columns are 1,x,y, the affine terms in q_j do not change its determinant. Linearity in the fourth column gives

det[1,x,y,q_j]=A_j D_x²+B_j D_xy+C_j D_y²=0.

Thus neither Q_j interpolates the configuration. Repeated x-values make the evaluation rows in A identical, and repeated y-values do the same in E. All four spaces fail at once. ∎

For two independent affine coordinates ℓ_1,ℓ_2, apply the same argument in those coordinates and transport the points through the inverse affine map. If their linear parts are dependent, four points on a common fiber already defeat both cubic spaces, and every degree-two polynomial has restriction of dimension at most three on that line, defeating the other spaces too.

## 4. Scope and next gap

This rules out obtaining a universal four-space construction merely by replacing the three classical quadratic extensions with two arbitrary quadratic combinations while retaining the two directional Vandermonde spaces. It is valid over R and C and is not just a finite-grid obstruction. It does not rule out four spaces of different shapes, higher-degree generators, different shared affine subspaces, or arbitrary polynomial subspaces.

The turn 2 algebraically closed range remains {4,5}. The real unrestricted range established here remains [2,5]. The worst-case characteristic-zero range remains [4,5]. The function-field exact value remains one. No new general minimum is claimed.

The exact checker implements every branch of the realization construction for all nonzero triples in {-3,…,3}³ and tests every ordered pair of quadratic coefficient triples in {-1,0,1}³. These are finite controls of the symbolic identities and construction, not substitutes for the proof.

Completed substantive author turns: 3/5. Informal completion estimate: 35%. All earlier frozen artifacts remain unchanged; independent final review is still required.
