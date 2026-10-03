# Turn 4: integrate the surgery comparison and locate the missing constants

**Result:** in the common diagram normalization of the cited finite-type
theory, the degree-two Kricker–Lescop difference is constant on each
integral Blanchfield-module class. This is a consequence of existing
theorems, with a short proof below. It gives a relative comparison but
does not determine the class-dependent calibration or the full target.
This is the fourth substantive attempt.

## 1. A precise comparison framework

Fix an integral Blanchfield module B=(A_Z,b_Z). Consider pairs (M,K),
where M is an integral homology three-sphere and K is a knot, whose
integral Blanchfield modules are isomorphic to B. The target knots in S^3
are included; intermediate surgeries are allowed to change M.

Let F_0^Z(B) be the rational vector space on these pairs, with F_n^Z(B)
the null-Borromean surgery filtration. The convention counts trivalent
vertices: the theta term has degree 2, not degree 1. Write
G_n^Z=F_n^Z/F_(n+1)^Z.

We use the following *credited* inputs, not newly established topology:

- Moussard, *Finite type invariants of knots in homology 3-spheres with
  respect to null LP-surgeries*, Geometry & Topology 23 (2019), 2005–2050,
  <https://msp.org/gt/2019/23-4/gt-v23-n4-p07-s.pdf>.
  Theorem 2.16 characterizes the integral null-surgery classes by B.
  Lemma 2.15 and Theorem 2.17 give Corollary 2.18: G_(2n+1)^Z(B)=0.
- Audoux–Moussard (2025), Section 7 and its last comparison statement,
  <https://doi.org/10.1112/topo.70036>:
  the degree-two components Z_2^Kri and Z_2^Les have the same induced map
  on G_2^Z(B). Both are of finite type of degree 2 and take values in the
  same beaded-diagram space A_2(delta), where delta annihilates A_Z⊗Q.

These facts use unmarked pairs and rational vector spaces. A marked theory
has more information; neither marking nor integral torsion can be dropped
without checking the applicable theorem. We do not replace equality of
the integral Blanchfield module by equality of Alexander polynomials.

## 2. Relative equality

Set E=Z_2^Kri-Z_2^Les, using precisely the common normalization above.
Both invariants vanish on F_3^Z. Since their maps on F_2^Z/F_3^Z agree,
E vanishes on F_2^Z. Corollary 2.18 gives

F_1^Z(B)/F_2^Z(B)=0, hence F_1^Z(B)=F_2^Z(B).

Therefore E also vanishes on F_1^Z(B). By Theorem 2.16, for any two pairs
K,J in the class B, their formal difference [K]-[J] lies in F_1^Z(B).
Consequently

Z_2^Kri(K)-Z_2^Kri(J)=Z_2^Les(K)-Z_2^Les(J).

Equivalently, there is a well-defined value c_B in A_2(delta) such that

Z_2^Kri(K)=Z_2^Les(K)+c_B

for every pair in this class. This conclusion is stronger than merely
restating graded equality; the vanishing of G_1 is the extra necessary
step. It still does not say c_B=0.

## 3. Attempt to make the reconstruction absolute

Choose a reference pair J_B in each B-class. The preceding equation gives

Z_2^Kri(K)=Z_2^Les(K)-Z_2^Les(J_B)+Z_2^Kri(J_B).

The first two terms are topologically constructed. The remaining reference
value is exactly the unresolved calibration. Null surgeries cannot connect
a nontrivial B-class to the unknot's trivial B-class. Therefore normalizing
at the unknot alone does not provide all the values Z_2^Kri(J_B).

This is a genuine logical gap, not an issue of having used too few examples.
For any assignment of constants d_B in the respective diagram targets,
the function Z_2^Les(K)+d_B has exactly the same variation under every
nonempty null-surgery bracket. Setting d_B=0 for the trivial class leaves
unknot calibration intact. Such formal modified functions are not asserted
to satisfy every other property of the Kricker invariant; they show that
the surgery characterization *by itself* has a class-constant ambiguity.

A canonical band presentation of a Seifert form supplies a possible
reference knot, but evaluating its two-loop Kontsevich data would reinsert
the invariant the construction is meant to explain. We did not derive an
independent closed topological formula for all these reference values.

## 4. Conditional ways to remove a constant

The following elementary criterion may be useful in restricted classes.
Suppose an involution K↦K* maps B to B* and negates both invariants in the
chosen common target identification. Then c_(B*)=-c_B. If B*=B and the
target identification is the identity, c_B=0 over Q. This follows simply
by applying the relative-constant statement to K and K*.

For an application using ambient orientation reversal, one must verify
the induced Blanchfield isometry, bead/meridian identification, orientation
sign and normalization. Those hypotheses are not certified here for an
additional family of knots, and this conditional criterion is not counted
as a new resolved subclass. In the trivial Alexander case, Lescop's
Theorem 9.2 already supplies the relevant credited comparison.

## 5. Relation to the exact requested P_K^theta

This argument is conducted in A_2(delta), where the two cited invariant
conventions are already common. Passing to the source's P_K^theta requires
the hair expansion, its theta identification, the Alexander denominator,
and the sum-versus-average convention discussed in SOURCE_GATE.md.
No scalar version of Lescop's Q is silently substituted for that target.
Even if every such normalization were fixed, the general c_B would still
have to be determined. Thus the original problem is not resolved.

**Next attempt:** replace unbounded comparison data with an effective
finite reconstruction using the genus bound, and determine exactly what
topological measurements would suffice.
