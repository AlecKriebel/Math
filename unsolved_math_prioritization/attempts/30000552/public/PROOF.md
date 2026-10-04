# A complete reconstruction of Breuillard's negative answer

## Result and credit

The general assertion in Dmitri Burago's problem-session question, Oberwolfach Report 33/2006, printed p. 2048, is false. The counterexample below is the construction in Emmanuel Breuillard, *Geometry of locally compact groups of polynomial growth and shape of large balls*, Groups, Geometry, and Dynamics **8** (2014), 669–732, §8.3(A), pp. 724–725, DOI [10.4171/GGD/244](https://doi.org/10.4171/GGD/244). This document reconstructs the argument and supplies elementary verifications of every hypothesis. It claims no new result or historical priority.

There are two complete length metrics on the same space, and one discrete group acting cocompactly by isometries for both, such that their ratio tends uniformly to one as distances tend to infinity, but their difference is unbounded. The construction already belongs to the length-space part of the question, so no interpretation of “coarse length” is needed.

## 1. An explicitly defined Heisenberg length metric

Let H be R^3 with multiplication

\[
(x,y,z)(x',y',z')=(x+x',y+y',z+z'+xy').
\]

The identity is (0,0,0), the inverse of (x,y,z) is (-x,-y,-z+xy), and c(u)=(0,0,u) is central. Associativity follows by expanding the central coordinate of a product of three elements: both associations give z+z'+z''+xy'+xy''+x'y''.

Call a piecewise C^1 path (x(t),y(t),z(t)) horizontal when z'=xy'. Its control length is the integral of |x'|+|y'|. Define D(p,q) as the infimum of these lengths over horizontal paths from p to q. Left translation by (a,b,c) changes the path to (a+x,b+y,c+z+ay); its last derivative is (a+x)y', so horizontality and control length are preserved.

### Finiteness, separation and topology

First move in x, then in y. This reaches (x,y,xy) with control length |x|+|y|. A horizontal lift of a planar square of side sqrt(|u|), with the appropriate orientation, is a path from the identity to c(u), of length 4 sqrt(|u|). Thus

\[
D(e,(x,y,z))\le |x|+|y|+4\sqrt{|z-xy|}. \tag{1}
\]

For any horizontal path starting at e and of control length L,

\[
|x|+|y|\le L,\qquad
|z|=\left|\int x\,dy\right|\le L^2. \tag{2}
\]

For the second bound use sup|x|≤L and total variation of y≤L. Taking infima shows that D(e,p)=0 only for p=e. Reversal gives symmetry, concatenation gives the triangle inequality, and the preceding translation calculation gives left invariance. Hence D is a finite metric.

Equations (1) and (2) show that its topology at e is the Euclidean topology, and translations give this everywhere. A closed D-ball at e is Euclidean closed and is contained in |x|+|y|≤R, |z|≤R^2. It is therefore compact. Translates show the same for every closed ball. Every D-Cauchy sequence is bounded, has a convergent subsequence in a compact closed ball, and then converges in D. Thus D is complete.

The metric length of any horizontal piecewise C^1 path is at most its control length: apply the definition of D to each restriction in a partition and sum. For every pair p,q and every ε>0, a horizontal path has control length below D(p,q)+ε. Its metric length is therefore also below that number. Conversely every continuous path has metric length at least its endpoint distance. These two facts prove that D is a length metric, without invoking a sub-Riemannian existence theorem.

### Exact central distance

We will need

\[
D(e,c(u))=4\sqrt{|u|}. \tag{3}
\]

The upper bound is the square construction. For the lower bound, any horizontal path to c(u) projects to a closed planar path. Let A and B be the total variations of its x and y coordinates, and let R_x=max x−min x. Closure gives A≥2R_x. With m=(max x+min x)/2 and using ∫dy=0,

\[
|u|=\left|\int(x-m)\,dy\right|
\le\frac{R_x B}{2}
\le\frac{AB}{4}
\le\frac{(A+B)^2}{16}.
\]

Thus the length A+B is at least 4 sqrt(|u|). This proof allows self-intersections and either orientation. It proves (3) for all real u, not merely square integers.

## 2. Two metrics on one space

Let M=R×H. Write its elements as (v,x,y,z), using componentwise product in the R factor and the above product in H. Define

\[
d_1((v,h),(w,k))=|w-v|+D(h,k).
\]

This is a left-invariant metric with the product Euclidean topology. It is complete, since a d_1-Cauchy sequence is Cauchy in each complete factor. It is a length metric: join the R coordinates and then follow a horizontal path in H whose control length is within ε of D(h,k). The resulting path has d_1-length at most d_1((v,h),(w,k))+ε. The reverse inequality holds for every path.

The map

\[
F(v,x,y,z)=(v,x,y,z-v)
\]

is a group automorphism: the two v coordinates add and do not enter the cross term xy'. Its inverse adds v to z. Put

\[
d_2(p,q)=d_1(F(p),F(q)).
\]

This pullback is a complete length metric with the same topology. Because F is an automorphism, it too is left invariant under the original group multiplication. In particular, **the same left-translation action**, not two separately chosen actions, preserves both metrics. Their identity-based formulas are

\[
\begin{aligned}
d_1(e,(v,x,y,z))&=|v|+D(e,(x,y,z)),\\
d_2(e,(v,x,y,z))&=|v|+D(e,(x,y,z-v)).
\end{aligned} \tag{4}
\]

These are Breuillard's §8.3(A) metrics. Our z is a matrix coordinate; the paper uses the exponential coordinate z_exp=z−xy/2. This coordinate change leaves the central shear z↦z−v unchanged and identifies the horizontal fields and their ℓ^1 norms.

## 3. One discrete cocompact isometric action

Let Γ=Z×H(Z), meaning the subgroup consisting of all integer quadruples. Closure under multiplication and inverse is immediate. It is discrete in the common topology and acts by left translations, hence by isometries of both metrics.

For any g=(v,x,y,z), set

\[
m=\lfloor v\rfloor,\quad a=\lfloor x\rfloor,\quad b=\lfloor y\rfloor,
\quad c=\lfloor z-a(y-b)\rfloor,
\quad\gamma=(m,a,b,c).
\]

Direct multiplication gives

\[
\gamma^{-1}g=(v-m,x-a,y-b,z-c-a(y-b))\in[0,1)^4.
\]

Consequently M=ΓK for the compact set K=[0,1]^4. The quotient is a continuous image of K and is compact. This is cocompactness for each metric, since both topologies are Euclidean. The action is also proper: for compact K_1,K_2, every γ with γK_1∩K_2 nonempty lies in the compact set K_2 K_1^{-1}; only finitely many integer quadruples do. Properness is additional, not needed by the printed question.

## 4. Uniform asymptotic equivalence

The two H-points in (4) differ by c(−v). The triangle inequality and (3) imply

\[
|d_1(e,g)-d_2(e,g)|\le4\sqrt{|v|}.
\]

Each metric in (4) is at least |v|. For arbitrary p,q, apply left invariance to g=p^{-1}q to obtain

\[
|d_1(p,q)-d_2(p,q)|
\le4\sqrt{\min\{d_1(p,q),d_2(p,q)\}}. \tag{5}
\]

For precision about the limit in the source, put r=d_1(p,q)>0 and s=d_2(p,q). If r≥64, then s≥r−4√r≥r/2. Therefore

\[
\left|\frac{d_1(p,q)}{d_2(p,q)}-1\right|
\le\frac{4\sqrt r}{s}\le\frac8{\sqrt r}. \tag{6}
\]

This is uniform over all pairs p,q. It proves exactly the source limit as d_1(p,q)→∞, rather than just a pointwise limit along selected rays or an assertion about isometric asymptotic cones.

## 5. Unbounded additive discrepancy

For t>0 let g_t=(t,0,0,t). Then F(g_t)=(t,0,0,0). Equations (3) and (4) give

\[
d_1(e,g_t)=t+4\sqrt t,\qquad d_2(e,g_t)=t.
\]

Their difference is 4√t, which is unbounded. All the question's hypotheses have already been verified, so this disproves its conclusion. Integer t already suffices, and these witnesses lie in Γ.

## 6. Boundaries of the conclusion

- This is a recovery of a published negative resolution, not a newly discovered counterexample.
- These particular metric spaces are isometric through F. That does not invalidate the example: the question concerns the difference of two functions on the same pairs of points. We do not claim this pair admits no rough isometry.
- The complete length metrics here are sub-Finsler. This argument does not answer a version that additionally requires Riemannian metrics.
- No general asymptotic-cone theorem, Pansu theorem, or unchecked quantitative approximation result is used. The elementary area calculation, metric construction and lattice reduction above supply all dependencies needed for this example.
