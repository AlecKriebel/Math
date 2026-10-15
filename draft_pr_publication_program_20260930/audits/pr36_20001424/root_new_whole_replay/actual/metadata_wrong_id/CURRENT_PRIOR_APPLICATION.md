# PR36: an earlier exact PCF counterexample is already printed

**Verdict: PRIOR_APPLICATION.** The universal AIM question has a negative answer by a direct, independently checkable consequence of Silverman's printed 1995 example. This does not assert that the source calls its example PCF, or that it is the earliest example worldwide. It establishes a specific prior algebraic conjugacy class with all the properties needed here.

## 1. Literal target and prior class

The independently recovered live AIM page, Problem 2.6, asks: “Are all PCF maps defined over their field of moduli?” It places no odd-postcritical-cardinality condition on this question. The original degree-11 candidate was read before the operative primary literature. Its graph-defined class need not coincide with the class below: the latter already disproves the universal target.

Silverman, *The field of definition for dynamical systems on P1*, Compositio Mathematica 98 (1995), 269–304, printed p.271 equation (1), explicitly gives

\[
\phi(z)=i\left(\frac{z-1}{z+1}\right)^3.
\]

That page explicitly identifies its field of moduli as Q and excludes a field of definition contained in R. The same formula with any odd exponent is printed on p.296. Both formulas were checked visually in the independently downloaded original PDF: physical PDF pages 4 and 29, respectively. Text extraction omits the formula glyphs in this scan, so the visual checks are essential. The publication title page is physical page 2, printed p.269; publication year is 1995. [Original primary source](https://www.numdam.org/item/CM_1995__98_3_269_0/).

The primary source supplies the class and the descent assertion. The next sections independently verify descent and add the elementary PCF calculation, without a computer approximation or a hyperbolic-center premise.

## 2. Exact ramification and PCF portrait

For every odd integer d>=3, let

\[
\phi_d(z)=i\left(\frac{z-1}{z+1}\right)^d.
\]

Its numerator and denominator have distinct sole roots 1 and -1, so its degree is d. At 1 and -1 it has local degree d. Direct differentiation away from the pole gives

\[
\phi'_d(z)=\frac{2di(z-1)^{d-1}}{(z+1)^{d+1}}.
\]

Equivalently the affine ramification polynomial is

\[
N'D-ND'=2di(z-1)^{d-1}(z+1)^{d-1}.
\]

In the infinity chart w=1/z, the map is i((1-w)/(1+w))^d, whose derivative at w=0 is -2di. Thus infinity is not critical. The only critical points are 1 and -1, each with ramification multiplicity d-1; their total multiplicity is 2d-2.

The following exact evaluations hold:

\[
\phi_d(1)=0,\quad \phi_d(-1)=\infty,\quad
\phi_d(0)=-i,\quad \phi_d(\infty)=i,
\]

\[
\frac{i-1}{i+1}=i,\qquad
\frac{-i-1}{-i+1}=-i,
\quad\text{so}\quad
\phi_d(i)=i^{d+1},\quad\phi_d(-i)=i(-i)^d.
\]

For d=3, this yields exactly

\[
1\longmapsto0\longmapsto-i\longmapsto-1
\longmapsto\infty\longmapsto i\longmapsto1.
\]

Both critical points are periodic on this six-cycle. Hence this printed algebraic cubic is PCF, with reduced postcritical cardinality six. For all d congruent to 3 modulo 4, the same six-cycle occurs. For d congruent to 1 modulo 4, there are two three-cycles:

\[
1\longmapsto0\longmapsto-i\longmapsto1,
\qquad -1\longmapsto\infty\longmapsto i\longmapsto-1.
\]

Thus every printed odd-exponent map in this particular family is PCF. This is a deduction by substitution, not an assumption about generic pseudo-real maps.

## 3. Exhaust all holomorphic dynamical automorphisms

If a Mobius transformation T commutes with phi_d, it permutes the critical set {1,-1} and carries their respective critical values {0,infinity} compatibly.

If it fixes each critical point, then it fixes each critical value. Therefore T fixes 0 and infinity and has the form T(z)=lambda z. Fixing 1 gives lambda=1.

If it exchanges the critical points, it also exchanges 0 and infinity. Therefore T(z)=lambda/z, and T(1)=-1 forces lambda=-1. But this sole possible swap fails to commute, since

\[
T\phi_d(0)=T(-i)=-i,
\qquad \phi_dT(0)=\phi_d(\infty)=i.
\]

The two values differ in characteristic zero. These two cases exhaust the action on the critical set. Consequently Aut(phi_d)=1 for every odd d>=3.

## 4. Antipodal symmetry and the absence of a real model

Set A(z)=-1/bar(z), exchanging 0 and infinity. Writing r(z)=(z-1)/(z+1), direct algebra gives

\[
r(A(z))=-\frac{1}{\overline{r(z)}}.
\]

Since d is odd,

\[
\phi_d(A(z))=-\frac{i}{\overline{r(z)}^d}
=A(\phi_d(z)).
\]

These are identities of maps on the whole sphere; the finite exceptional values follow by continuity or homogeneous coordinates. Also A^2=1 and A has no fixed point, because a finite fixed point would require |z|^2=-1 and 0,infinity are exchanged.

Any antiholomorphic Mobius symmetry B commuting with phi_d has BA holomorphic and commuting with phi_d. By the complete centralizer calculation, BA=1. Thus B=A: this is the only antiholomorphic symmetry.

If some conjugate g=M phi_d M^-1 had real coefficients, ordinary conjugation c would commute with g. Then M^-1 c M would be an antiholomorphic symmetry of phi_d having a circle of fixed points. It would have to equal A, whose fixed set is empty, a contradiction. Therefore the class has **no real model**. This independently verifies the descent obstruction stated by the primary source. The equivalence between a real model and a reflecting symmetry is also explicitly proved in Hidalgo–Quispe, arXiv:1502.05306v4, Lemma 4, p.8; Theorem 6, p.17, gives the same trivial-centralizer obstruction. [Primary corroboration](https://arxiv.org/abs/1502.05306).

## 5. Absolute field of moduli is exactly Q

The coefficients of phi_d belong to Q(i), so any sigma in Gal(Qbar/Q) either fixes the coefficients or replaces i by -i. For L(z)=-1/z, the antipodal identity equivalently gives

\[
\overline{\phi_d}=L\phi_dL^{-1}.
\]

Here L is defined over Q. Hence every sigma fixes the PGL2 conjugacy class. The fixed field of the full absolute Galois group is Q, so the absolute field of moduli is exactly Q. All quantities in the example are algebraic; no rigidity or algebraicity theorem about PCF centers is needed. A Q-model would be a real model, which Section 4 excludes.

This verifies every premise of the earlier exact counterexample: degree 3, algebraic coefficients, PCF, trivial dynamical automorphisms, real absolute field of moduli Q, and no real model. The odd reduced-postcritical-set descent criterion is unaffected because the cardinality is six.

## 6. What the BBM center audit does and does not establish

Before finding the simpler Silverman example, I independently read Bonifant–Buff–Milnor arXiv:1512.01850v1, dated 6 December 2015, and the full relevant proof in the public author-hosted *On Antipode Preserving Cubic Maps*, explicitly labeled Draft of Feb.15,2015. The latter Section 6, pp.38–46, constructs each even-denominator tongue and its cyclic attracting-basin pattern. The 2015 Fjord paper Lemma 2.3, pp.10–11, gives unique PCF centers; its numerical figure 12 at p.14 is insufficient alone to certify a particular nonaxis center.

An elementary normal-form calculation was reconstructed and sealed before receiving any other priority judgment: a commuting symmetry of f_q=z²(q-z)/(1+bar(q)z) must preserve or exchange the fixed-critical pair 0,infinity. A scaling is identity. A swap lambda/z requires both lambda=-q/bar(q) and lambda=-bar(q)/q, hence q²=bar(q)². Thus a nonaxis parameter with only those critical fixed points has trivial centralizer. Reflection in an axis conjugates the basin-ring rotation to its negative, so a tongue with rotation 1/4 cannot contain an axis parameter. This checks the needed symmetry mechanism instead of assuming all antipodal PCF centers are pseudo-real.

The author-hosted draft is mutable and its printed date alone is not an immutable deposit date. Lodge–Mukherjee arXiv:1710.05071v2, dated 19 October 2020 and labeled the published version, pp.33–34, explicitly references that draft's Theorem 6.1 for tongue existence/classification, and Proposition 8.1 states the unique PCF-center property. Milnor arXiv:1205.2668v1, pp.32–35, contains the underlying real-form and marked-rational-map center arguments. These were read, including their operative proofs. This establishes meaningful earlier primary context, but the decisive priority verdict above does not depend on the draft's publication status, a numerical center label, or an uncompleted center-coefficient elimination. [BBM arXiv version](https://arxiv.org/abs/1512.01850), [author draft](https://www.math.stonybrook.edu/~jack/bbm.pdf), [Lodge–Mukherjee](https://arxiv.org/abs/1710.05071), [Milnor](https://arxiv.org/abs/1205.2668).

## 7. Computational scope and falsification controls

The standard-library verifier uses exact pairs of rational numbers for Q(i), expands the ramification identity, checks the infinity chart, evaluates every point of the six-point support, and checks the coefficient-conjugation identity by polynomial cross multiplication. It checks the sole possible swapping holomorphic symmetry at 0. Four positive cases d=3,5,7,11 pass. Seven actual mutated input files and one optimization-mode replay fail with preserved stdout/stderr: even degree, degree one, wrong coefficient, wrong critical support, wrong ramification multiplicities, false swap symmetry, and wrong orbit. Three actual altered executable files are also run and rejected (ramification derivative corruption, pole corruption, infinity evaluation corruption).

These controls do not enumerate arbitrary Mobius transformations or prove a global Galois statement. The complete two-case centralizer proof, uniqueness of antiholomorphic symmetry, real-model contradiction, and absolute-field-of-moduli argument above supply those logical steps. Rejecting an altered source coefficient is an input guard; it is not itself proof that the altered map has infinite critical orbits.

## 8. Priority limit and allowed disposition

The exact negative answer is a verified elementary consequence of an earlier **printed algebraic map and explicitly printed descent assertion**. The PCF portrait is the new-to-this-audit observation, with an elementary checkable derivation; it is not presented as new mathematics. No bounded search can certify earliest appearance worldwide. No claim about priority or novelty of the degree-11 decorated graph itself is made.

This family modifies no candidate mathematics, shared state, queue, original packet, remote, paper, or DOI. It adds zero research attempts. The independent source verifier independently retrieved the original primary PDF, sealed a complete agreeing proof, and its exact checker reproduces its recorded receipt. Two initially wrong control predictions in that independent run are transparently preserved and corrected. Original-packet source-context exposure is detailed in EXPOSURE_AND_SCOPE.md; the child verification was sealed before any original-packet or other priority opinion. Its final foreign-source cleanup and seals are included in the family closure. Any final PR36 publication/disposition decision belongs to the parent audit, after all family closures and whole-packet checks.
