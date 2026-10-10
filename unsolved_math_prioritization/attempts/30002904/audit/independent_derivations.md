# Independent derivations for the partial-result audit

These are independently authored calculations, not a copied source document. They supplement the frozen proof without changing its scope. Throughout this document, probabilities on SL3(R) mean normalized Haar measure on the indicated continuous region, never counting measure on SL3(Z).

## A. Cartan density and normalization from the local differential

Let D=diag(e^a,e^b,e^c), where a >= b >= c and a+b+c=0. Differentiate the map (k,D,l) -> kDl at k=l=I and left-trivialize the derivative. In the pair of off-diagonal directions (i,j),(j,i), the two compact variables x,y from skew-symmetric left and right perturbations have coefficient matrix

\[
\begin{pmatrix}e^{t_j-t_i}&1\\-e^{t_i-t_j}&-1\end{pmatrix}.
\]

Its determinant is e^(t_i-t_j)-e^(t_j-t_i)=2sinh(t_i-t_j). Multiplying these three factors and including the constant diagonal-coordinate volume gives a positive constant times

\[
\sinh(a-b)\sinh(a-c)\sinh(b-c)\,da\,db.
\]

The compact groups have finite volume. On the chamber interior the residual decomposition ambiguity is finite and constant; chamber walls have zero measure. These factors therefore cancel in every ratio considered here. This recovers the multiplicity-one density independently of a singular-value convention in a citation.

## B. Exact finite-radius gap-tail mass

Set p=a-b and q=b-c. Then

\[
a=(2p+q)/3,\qquad b=(-p+q)/3,\qquad c=-(p+2q)/3,
\]

and the absolute Jacobian from (p,q) to (a,b) is 1/3. With L=log X >= 0, the exact ordinary operator-ball chamber is

\[
p\ge0,\quad q\ge0,\quad 2p+q\le3L.
\]

The top gap is p. Define the radial mass, with the same coordinate normalization as the frozen proof, by

\[
I(L,s)=\frac13\int_s^{3L/2}\int_0^{3L-2p}
\sinh p\sinh q\sinh(p+q)\,dq\,dp
\]

for 0 <= s <= 3L/2; it is zero if s >= 3L/2. The identity

\[
4\sinh p\sinh q\sinh(p+q)
=\sinh(2p+2q)-\sinh(2p)-\sinh(2q)
\]

reduces both integrations to elementary antiderivatives. The result is

\[
\begin{aligned}
I(L,s)={}&\frac{\sinh(6L-2s)}{48}
-\frac{\sinh(6L-4s)}{96}
-\frac{\sinh(3L)}{12}
+\frac{\sinh(2s)}{16}\\
&+\frac{(3L-2s)(2\cosh(2s)+1)}{48}.
\end{aligned}
\tag{A}
\]

For direct verification, the inner integral after division by three is

\[
-\frac{(3L-2p)\sinh(2p)}{12}
-\frac{\cosh(2p)}{24}
-\frac{\cosh(6L-4p)}{24}
+\frac{\cosh(6L-2p)}{24}+\frac1{24}.
\]

The negative s-derivative of (A) equals this expression with p=s, and (A) vanishes at s=3L/2. These two facts verify (A) independently of a computer algebra simplifier.

In particular,

\[
I(L,0)=\frac{\sinh(6L)}{96}-\frac{\sinh(3L)}{12}+\frac{3L}{16}
\sim\frac{e^{6L}}{192}.
\]

For each fixed s >= 0, formula (A) gives

\[
e^{-6L}I(L,s)\longrightarrow
\frac{2e^{-2s}-e^{-4s}}{192}.
\]

Consequently I(L,s)/I(L,0) has exactly the limit asserted in the frozen proof. The Haar normalization constant cancels. The probability at s=0 is one, and for s>0 the limit equals 1-(1-e^(-2s))^2, strictly between zero and one. This calculation is for fixed s; no uniform asymptotic for moving s is inferred.

## C. Exact finite-radius inverse-bounded mass

In the same coordinates, the additional inverse condition is p+2q <= 3L. Its region is the symmetric quadrilateral with vertices (0,0), (3L/2,0), (L,L), (0,3L/2). Splitting at the diagonal p=q and using symmetry gives radial mass

\[
K(L)=\frac23\left[
\int_0^L\int_0^p+\int_L^{3L/2}\int_0^{3L-2p}
\right]\sinh p\sinh q\sinh(p+q)\,dq\,dp.
\]

The same product identity yields

\[
K(L)=\frac{\sinh(4L)}{16}-\frac{\sinh(3L)}6
+\frac{\sinh(2L)}{16}+\frac L8
\sim\frac{e^{4L}}{32}.
\]

Therefore the continuous inverse-bounded-to-ordinary ratio is

\[
\frac{K(L)}{I(L,0)}\sim6e^{-2L}=6X^{-2}.
\]

This strengthens only the continuous zero-limit check. It does not assert this asymptotic, or even zero density, for integer matrices.

## D. Why a leading-term numerical bound can fail

For fixed d=a-b with a growing, the leading density terms are

\[
\frac18\bigl(e^{4a+2b}-e^{2a+4b}\bigr).
\]

They have opposite signs. After integration their total leading mass is proportional to 1/2-1/4; imposing d >= s replaces it by e^(-2s)/2-e^(-4s)/4. The quotient is 2e^(-2s)-e^(-4s), not a positive weighted average bounded above by e^(-2s). Thus cancellation cannot be discarded in a termwise exponential comparison. This calculation identifies the obstruction in dimension three without purporting to repair the source's argument in every dimension.

For eta=5, exact rational arithmetic gives

\[
2/5^4-1/5^8=1249/390625=0.00319744>1/625=0.0016.
\]

## E. Independent reconstruction of the Q=1 exceptional count

Write A=((a,b),(c,d)), ad-bc=1, with all entries bounded in absolute value by X and c nonzero. For 1 <= Y <= X, there are X^(1+o(1))Y matrices with |c| <= Y: choose b and c, then use the divisor bound on ad=1+bc. The exceptional equality 1+bc=0 contributes only O(X) choices and is harmless. Absolute values handle both signs.

For a fixed dyadic interval Y/2 < min(|c1|,|c2|) <= Y, take |c1| to be the smaller. There are at most X^(1+o(1))Y choices for A1. An intersection or tangency between the two disks centered at a_i/c_i requires

\[
|a_1/c_1-a_2/c_2|\le1/|c_1|+1/|c_2|\le4/Y.
\]

For each nonzero c2, this allows O(|c2|/Y+1) integer a2. The congruence a2*d2=1 modulo c2 has either no solutions or a single residue class, and therefore O(X/|c2|) possible d2; b2 is then fixed. Summing over c2 gives O(X^2/Y+X log X) choices. Multiplication by the first-matrix bound and Y <= X yields X^(3+o(1)) pairs. Summing O(log X) dyadic intervals preserves this exponent. At the lowest scale one may use the interval containing |c|=1 directly.

Inverting either matrix preserves maximum-entry height and |c| and swaps its two centers. It therefore supplies the other three cross-disk counts with the same bound. A matrix's own two disks fail strict separation only if |a+d| <= 2. For each of the five possible traces t, choose a and count solutions to bc=a(t-a)-1 by the divisor bound; the zero-product case contributes only O(X). Thus there are X^(1+o(1)) bad individual matrices, and at most X^(3+o(1)) pairs containing one, using the elementary O(X^2) total count.

The union of these events contains every failure of four strictly separated closed disks, including all tangencies. This independently recovers the exact special case of the modern primary lemma needed by the frozen proof. After adding c=0 cases and dividing by the square of the independently proved operator-ball lower bound, the finite-index probability is at most X^(-1+o(1)). The proof that separated disks imply infinite index is the bounded-orbit/translation argument reviewed in `audit.md`.

## F. Elementary group identities and ping-pong inequalities

Use the commutator convention [V,W]=VWV^(-1)W^(-1). For the 3-cycle P and U=I+E12, the conjugates are V=I+E23 and W=I+E31. Then [U,V]=I+E13, [V,W]=I+E21, and [W,U]=I+E32. All six elementary transvections are available, and their integral powers generate SL3(Z) by elementary row reduction.

On the affine projective coordinate x=v1/v2, U^(2k) acts by x -> x+2k, while [V,W]^(2k) acts by x -> x/(2kx+1). For every nonzero integer k, the first maps |x|<1 into |x|>1, and the second maps |x|>1 into |x|<1, including infinity. Indeed |2kx+1| >= 2|k||x|-1 > |x| in the second case. Two infinite cyclic factors consequently satisfy ping-pong. Their subgroup fixes e3; the full lattice has infinitely many images of e3, so the subgroup's index is infinite. This is a counterexample only to passage from a subgroup generated by words to its parent subgroup.
