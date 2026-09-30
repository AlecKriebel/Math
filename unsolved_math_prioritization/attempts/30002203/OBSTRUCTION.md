# The pentagon symmetry: affine obstruction and the unresolved marked lift

**Original target unresolved after two approaches.** The explicit geometry below distinguishes the specified order-four homology action from its realizable square and from unmarked equivalences of arrangement complements. These are scoped controls, not a solution or a historical novelty claim. Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.

## 1. The exact arrangement and the two questions

Problem3 in the [OWR 49/2012 problem session, printed p.2978](https://ems.press/content/serial-article-files/46421), asks about the eight complexified affine lines
\[
 AB,\ CE,\ AC,\ DE,\ AD,\ BC,\ AE,\ BD
\]
from a regular pentagon A,B,C,D,E. The specified vertex permutation is
\[
 s=(B\ C\ E\ D),\qquad s(A)=A.
\]
The questions are whether its induced integral homology automorphism extends to an automorphism of the natural \(E_\infty\)-coalgebra and whether its action on first homology is induced by a fundamental-group automorphism.

The surrounding contribution by Rybnikov, printed pp.2966–2968, works over the integers and uses morphisms in a homotopy-compatible category of \(E_\infty\)-coalgebras. The target is not merely an automorphism of the ordinary cohomology ring. Nor is it an unmarked assertion that two abstract groups are isomorphic.

This is an eight-line affine arrangement, or a nine-line projective arrangement after adding the line at infinity. It is not the eleven-line arrangement consisting of all ten pentagon sides and diagonals plus infinity, which is also called a pentagon arrangement in other literature.

## 2. Exact coordinates and incidence data

Set
\[
 a=\frac{1+\sqrt5}{2},\qquad a^2=a+1.
\]
After an affine change of coordinates, the five vertices are
\[
 A=(0,0),\quad B=(1,0),\quad C=(a,1),\quad
 D=(1,a),\quad E=(0,1).
 \tag{1}
\]
For example, take the two side vectors AB and AE as the coordinate basis in a Euclidean regular pentagon. The standard golden-ratio relation gives (1).

Number the lines in the source order:
\[
\begin{array}{c|c|c}
 i&\text{line}&\text{equation}\\ \hline
0&AB&y=0\\
1&CE&y=1\\
2&AC&x-ay=0\\
3&DE&x-ay+a=0\\
4&AD&ax-y=0\\
5&BC&ax-y-a=0\\
6&AE&x=0\\
7&BD&x=1.
\end{array}
 \tag{2}
\]
Thus the four parallel pairs are (0,1),(2,3),(4,5),(6,7), and the line permutation is
\[
 \sigma=(0\ 2\ 6\ 4)(1\ 3\ 7\ 5).
 \tag{3}
\]
Use positive complex meridians for the basis of \(H_1\) of the affine complement.

The finite intersection sets of size at least three are
\[
\begin{array}{c|c}
 A&\{0,2,4,6\}\\
 B&\{0,5,7\}\\
 C&\{1,2,5\}\\
 D&\{3,4,7\}\\
 E&\{1,3,6\}.
\end{array}
\]
The finite double-point pairs are
\[
 \{0,3\},\{1,4\},\{1,7\},\{2,7\},\{3,5\},\{5,6\}.
\]
Together with the four parallel pairs, these exhaust all pairs of the eight lines. The permutation (3) preserves this full incidence data. Adding the line at infinity, indexed8, creates the four triple sets \(\{0,1,8\},\{2,3,8\},\{4,5,8\},\{6,7,8\}\), while fixing line8.

These elementary exact checks recover the combinatorial symmetry that the source already supplies. They do not add the missing higher operations.

## 3. Approach1: geometric realization fails for sigma, but works for its square

### 3.1 No affine or projective self-map induces sigma

Suppose an invertible complex affine map T sends each line in (2) to its sigma image. The multiple intersections force T to send A,B,C,D,E according to s. In particular,
\[
 T(A)=A,\quad T(B)=C,\quad T(E)=D.
\]
The three points A,B,E are affinely independent, so necessarily
\[
 T(x,y)=(ax+y,\ x+ay).
 \tag{4}
\]
But
\[
 T(C)=T(a,1)=(a^2+1,2a)=(a+2,2a)\ne(0,1)=E.
\]
This contradicts the required image of C. Thus no such affine map exists, even with complex coefficients.

The same conclusion holds for projective transformations inducing the specified permutation on the projectivized arrangement. The infinity line is fixed. Even if this were not imposed separately, the images of two distinct intersections of parallel pairs force their common line at infinity to be preserved. Such a projective transformation restricts to an affine transformation, already excluded.

**This excludes only the affine/projective realization route.** It does not rule out a nonlinear homeomorphism of the complement, a self-homotopy equivalence, an \(E_\infty\) automorphism, or an abstract fundamental-group automorphism with the required homology action.

### 3.2 The square has both requested lifts

The complex-linear involution
\[
 R(x,y)=(y,x)
 \tag{5}
\]
permutes the lines by
\[
 \sigma^2=(0\ 6)(2\ 4)(1\ 7)(3\ 5).
\]
It restricts to a homeomorphism of the complement and fixes the basepoint (2,2), which lies on none of the eight lines. Hence it gives a based fundamental-group automorphism.

A complex-linear local normal map preserves the positive orientation of a complex meridian. Consequently the induced map on \(H_1\) is the positive permutation \(\sigma^2\), not its negative. Naturality of the \(E_\infty\) chain structure and transfer to torsion-free homology give the corresponding \(E_\infty\) automorphism in the category used by the source.

This solves the lifting problem for the square only. An automorphism lifting sigma itself need not have order four: its fourth power could act trivially on first homology without being the identity. Therefore imposing a finite-order condition on a candidate group lift would add an unjustified restriction.

### 3.3 Galois conjugacy does not repair the missing self-map

Let \(a'=1-a\). Then
\[
 a+a'=1,\qquad aa'=-1.
\]
The linear map (4), now applied to the realization with parameter \(a'\), sends its labelled vertices according to s into the realization with parameter a:
\[
 T(1,0)=C,\quad T(a',1)=E,\quad
 T(0,1)=D,\quad T(1,a')=B.
\]
Its determinant is a, so it is invertible. This gives a geometric map **between the two different labelled realizations**, with a nontrivial label permutation.

Coefficient-field conjugation \(a\mapsto a'\) is not complex conjugation, since both parameters are real. It supplies no continuous label-preserving map between the two complex complements. A continuous field automorphism of C fixes Q and hence, by continuity, every real number, so it cannot perform this exchange.

Combining an unmarked equivalence with another unmarked equivalence does not ensure the prescribed action on the fixed meridian basis. That action is the unresolved datum.

## 4. Identification with the Falk–Sturmfels type and the limits of prior results

The affine transformation
\[
 (X,Y)=\bigl(y,\ 1-x+(a-1)y\bigr)
 \tag{6}
\]
takes (2), together with infinity, to the Falk–Sturmfels arrangement in **Nazir–Yoshinaga, Example5.2**, with parameter \(\gamma_+=a\). Using their order
\[
 (L_1,L_2,L_3,L_4,K_1,K_2,K_3,K_4,H_9),
\]
the images of our lines0 through8 are
\[
 (L_1,K_1,L_4,K_4,L_3,K_3,L_2,K_2,H_9).
 \tag{7}
\]
Substitution into the nine defining linear forms checks this exactly.

Nazir–Yoshinaga prove that the two Galois-conjugate Falk–Sturmfels complements are homeomorphic, by a projective map that permutes their labels. Their statement is an unmarked equivalence and does not provide a self-map of the fixed arrangement with homology action sigma.

**Amram–Cohen–Sun–Teicher–Ye–Zarkh, Proposition6.1 and Remark6.2**, compute the combinatorial automorphism group as cyclic of order four and explain that its order-two subgroup acts trivially on the two-point realization space. This agrees with (3)–(5). It does not assert that every combinatorial automorphism lifts to a marked fundamental-group automorphism.

Thus identifying the source with this classical arrangement is useful, but the published unmarked equivalences do not answer either of the source's specified lifting questions.

## 5. Approach2: a bounded degree-three screen and its precise limitation

A modest exploratory computation generated a real wiring diagram for (2), using projection \(t=x+2y\), and formed degree-at-most-three noncommutative Magnus polynomials for a meridian-relator model. It tested the linear coefficient conditions for images with the prescribed degree-one permutation and arbitrary commutator corrections of degree two.

The resulting formal systems were consistent over \(\mathbb F_2,\mathbb F_3,\mathbb F_5,\mathbb F_7\), for the identity, sigma squared and sigma, and for both half-twist sign conventions. No finite-field inconsistency certificate was found.

The archived experiment is explicitly **not a certified fundamental-group quotient computation**. The truncated algebra model, the presentation conventions and their relation to the complete integral group would require their own proof and independent validation before any such interpretation. Even a fully certified lift through one finite truncation would not prove an automorphism of the full group or an extension of all \(E_\infty\) operations. The experiment is preserved as a failed search for a low-degree obstruction, not as positive lifting evidence.

Rybnikov's source describes the first obstruction through an abelian cokernel built from the homology coproduct and degree-three holonomy Lie algebra. His later [2014 manuscript](https://arxiv.org/abs/1402.6272), Theorem12 and Proposition14, relates the natural \(E_\infty\) structure to the **dimension completion** of the group algebra/fundamental group. The completion is not silently identified here with the full discrete fundamental group. Neither vanishing of one obstruction nor rational formality fills the integral higher-coherence gap.

## 6. Exact surviving question

For the fixed eight-line complement and the positive meridian permutation (3), one still needs either:

- a fully defined group automorphism or \(E_\infty\) automorphism inducing sigma; or
- a rigorous invariant obstructing the corresponding marked lift.

The geometric square (5), ordinary incidence/coproduct preservation, unmarked homeomorphism type, and the bounded exploratory truncations do not decide this.

The original target remains **unsolved,2/5 substantive approaches**. The exact verifier certifies the finite geometry and identities (1)–(7), not either unresolved extension. No historical novelty is claimed.
