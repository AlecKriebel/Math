# Turn 5: actual branching rigidity for a two-trefoil-splice family

Problem 2676, KP-1.17. Fifth and final substantive author turn.
**Scoped partial result; the original problem remains unresolved after 5/5
author turns.** No mixed pair is constructed and no universal alternation
transport theorem is asserted.

This turn closes a specific infinite family of toroidal common-cover
candidates. It uses actual involutions and their boundary conjugacies, rather
than inferring equivalence from homology or L-space data alone. The result is
a consequence of classical equivariant JSJ, strong-inversion, and surface
mapping-class theory. No novelty or priority claim is made.

## 1. Family and precise theorem

For each integer (r\geq2\), put (p_r=r(r+1)-1\). Take two copies (E_1,E_2\)
of the right-handed trefoil exterior with the meridian–longitude convention
of Turn 4. Define

\[
 A_r=\begin{pmatrix}r+1&-p_r\\1&-r\end{pmatrix},\qquad
 Y_r=E_1\cup_{h_r}E_2,\qquad (h_r)_*=A_r.                         \tag{1.1}
\]

Columns are images of (\mu_1,\lambda_1\) in the ordered basis
\(\mu_2,\lambda_2\). The map is orientation reversing since (\det A_r=-1\).

**Theorem (family-scoped).**

1. (Y_r\) is an irreducible toroidal non-Seifert L-space, with
   \(H_1(Y_r;\mathbb Z)=\mathbb Z/p_r\). It has an actual double-branched-cover
   description over (S^3\).
2. Every link with branched double cover (Y_r\) is a prime knot with hyperbolic
   exterior. Up to reflecting links to match orientations, all such branch
   knots are Conway mutants of the reference branch knot constructed from
   the standard strong inversion on each trefoil exterior. There are at most
   four resulting link-equivalence classes from this construction; the bound
   does not assert that they are distinct.
3. Consequently (Y_r\) cannot be a cover shared by an alternating and a
   nonalternating link. For (r=2\), Turn 4 further proves that every branch
   is nonalternating. This work does not decide which alternative occurs for
   every (r\geq3\), and does not need to do so for the no-mixed-pair conclusion.

Since (p_r\) strictly increases, this is a family of pairwise nonhomeomorphic
common-cover candidates. It is not an assertion about every graph manifold
or every toroidal L-space.

## 2. Topology and L-space property

Mayer–Vietoris gives generators (x_i=[\mu_i]\) and relations

\[
 x_1=(r+1)x_2,\qquad p_rx_2=0.                                   \tag{2.1}
\]

Thus (H_1(Y_r)=\mathbb Z/p_r\). Both (x_1\) and (x_2\) generate this cyclic
group, because (\gcd(r+1,p_r)=1\). The number (p_r\) is odd and at least 5.
As in Turn 4, incompressible-boundary irreducible pieces give an irreducible
union and an essential gluing torus (T\).

The regular-fiber slope in a right trefoil exterior is 6, the peripheral
class (6\mu+\lambda\). Its image under (A_r\) is

\[
 (6(r+1)-p_r,\ 6-r).
\]

It is not proportional to ((6,1)\), since their determinant is

\[
 -r^2+11r-29\neq0                                                \tag{2.2}
\]

for an integer (r\); the discriminant is 5. The two Seifert pieces therefore
do not amalgamate to a Seifert fibration. More explicitly, an incompressible
torus in a Seifert manifold is vertical or horizontal after isotopy. A
horizontal torus would make the cut-open pieces torus-product or Klein-bottle
I-bundle types, not trefoil exteriors. In the vertical case the fiber slopes
on the two sides must match. The trefoil exterior, with base orbifold
(D^2(2,3)\), has its unique Seifert fiber slope; it is not one of the
solid-torus or twisted-I-bundle exceptions. Equation (2.2) excludes matching.
Thus (T\) is the single JSJ torus, with the two trefoil exteriors as pieces,
and (Y_r\) is non-Seifert.

The slope action is

\[
 h_r(s)=r+1+\frac1{s-r}.
\]

Recall from Turn 4 that the complement of the interior right-trefoil L-space
interval is (D=(-\infty,1]\cup\{\infty\}\). Its image is

\[
 h_r(D)=\left[r+1-\frac1{r-1},\ r+1\right]\subset(1,\infty).
                                                                    \tag{2.3}
\]

The endpoint inequality is strict relative to 1 even for (r=2\). The same
Hanselman–Rasmussen–Watson gluing theorem used in Turn 4 proves that (Y_r\)
is an L-space, with the meridional endpoint correctly included in (D\).

Choose the linear representative of (A_r\) in coordinates where each
standard trefoil strong inversion restricts to (x\mapsto-x\) on the boundary.
It commutes with that boundary involution. Gluing the two inversions gives a
reference involution (\tau^0\) whose quotient is two tangle balls glued to
give (S^3\), exactly as in Turn 4. Denote its branch set by (J_r^0\).

For *any* branch link (J\) of (Y_r\), the formula
\(\dim H_1(\Sigma_2(J);\mathbb F_2)=\#\pi_0(J)-1\) shows that (J\) is a knot.
Irreducibility and the connected-sum cover formula make it prime; the only
knot with cover (S^3\) is the unknot, and (H_1(Y_r)\neq0\). A Seifert-exterior
branch knot would, by the exact BGH theorem from Turn 3, be ADE: the (D/E\)
cases have determinant at most 4, and the (A\) case has lens-space cover.
Neither can give (Y_r\). A toroidal-exterior branch knot would have non-L-space
double cover by the degree-two BGH theorem. Hence its exterior is hyperbolic.
This proves the geometric assertions in the theorem, without confusing the
hyperbolic branch exterior with the toroidal branched cover.

## 3. Peripheral rigidity of a trefoil exterior

**Lemma.** Every orientation-preserving homeomorphism between marked copies
of the right trefoil exterior acts on boundary homology by (I\) or (-I\).

**Proof.** The kernel of
\(H_1(\partial E;\mathbb Z)\to H_1(E;\mathbb Z)\) is generated by the primitive
longitude. Thus the boundary matrix is

\[
 B=\begin{pmatrix}\epsilon&0\\k&\delta\end{pmatrix},
 \qquad \epsilon,\delta\in\{1,-1\}.
\]

It preserves the boundary orientation, so (\delta=\epsilon\). The center of
the trefoil group \(\langle a,b\mid a^2=b^3\rangle\) is generated by its
regular fiber (a^2=b^3\), represented peripherally by (6\mu+\lambda\). A
group automorphism takes this central generator to its positive or negative
generator. Consequently (B(6,1)\) equals (\pm(6,1)\). Its first coordinate
determines the sign to be (\epsilon\), and the second then gives (k=0\).
Boundary incompressibility ensures that these peripheral classes are genuinely
distinguished in the group. Hence (B=\epsilon I\). ∎

This is stronger than preserving the abstract first-homology group; it uses
the marked peripheral kernel and the characteristic central fiber.

## 4. A branching involution cannot exchange the pieces

Let (\tau\) be any branching involution on (Y_r\) with quotient (S^3\).
By the equivariant JSJ theorem, take the unique JSJ torus (T\) invariant under
(\tau\), after an ambient isotopy of the splitting. This input is applicable
here: (Y_r\) is an irreducible Haken non-Seifert manifold, not a torus bundle,
and the branch set is a prime knot. Gordon–Luecke's full 2006 paper, Section 2,
printed p. 2060, states precisely this invariant-JSJ conclusion for the
covering involution of a prime knot, crediting Meeks–Scott.

If (\tau\) interchanged (E_1,E_2\), its restrictions on piece homology would
send (x_2\) to (\eta x_1\), where (\eta=\pm1\). Equation (2.1) would then
give

\[
 \tau_*(x_2)=\eta(r+1)x_2.
\]

But Turn 2 proves that *every* double-cover deck involution of an (S^3\) link
acts by (-I\) on integral first homology. Thus

\[
 \eta(r+1)\equiv-1\pmod {p_r}.                                  \tag{4.1}
\]

This is impossible because (1<r+1<p_r-1\) for every (r\geq2\). This is an
actual use of the two marked inclusion maps into (H_1(Y_r)\); it does not
claim that abstract deck homology by itself distinguishes branches.

There is also a peripheral check, not needed for (4.1). Any orientation-
preserving homeomorphism exchanging the two pieces has boundary matrices
(B_1,B_2=\pm I\) by Section 3. Compatibility with the gluing gives
(B_1=A_rB_2A_r\), hence (A_r^2=\pm I\). The lower-left entry of (A_r^2\)
is 1, contradicting either possibility. Thus in this family even an arbitrary
orientation-preserving piece-exchanging homeomorphism is excluded.

It follows that (\tau\) preserves each (E_i\). The maps
\(H_1(E_i)\to H_1(Y_r)\) are onto groups of odd order greater than 2. Since
(\tau_*=-I\) downstairs in this homology group, its restriction on
\(H_1(E_i)\cong\mathbb Z\) must also be (-1\). Section 3 then gives

\[
 (\tau|_{\partial E_i})_*=-I.                                   \tag{4.2}
\]

## 5. Local strong-inversion conjugacy is genuinely available

An orientation-preserving torus involution acting as (-I\) is conjugate to
the elliptic involution (x\mapsto-x\). The conjugating map can be chosen to
act trivially on torus homology: compose any such conjugacy with the inverse
of its linear homology representative, which commutes with (-I\).

Thus the boundary involution in (4.2) extends over the meridional solid torus
by the standard elliptic extension, reversing its core. Meridional filling
of (E_i\) is (S^3\); the extended action is a strong inversion of the
trefoil core. The fixed set is an unknotted circle meeting the core twice by
the classical (S^3\) involution theorem. No arbitrary four-dimensional
extension, quotient filling assumption, or push-in assertion is involved.

Sakuma's uniqueness theorem for a torus knot's strong inversion now supplies
an orientation-preserving conjugacy on each piece taking (\tau|_{E_i}\) to
the chosen reference strong inversion (\tau_i^0\). Invariant tubular
neighborhoods can be matched by equivariant isotopy, so the conjugacies
restrict to the chosen exteriors. Write them as (f_i:E_i\to E_i\). Their
boundary matrices are (\epsilon_iI\) by Section 3.

The exact input is Sakuma (1985), Proposition 3.1(1), printed p. 185, together
with his orientation-preserving equivalence definition on p. 176. Both pages
were inspected in the complete author-hosted scan. The same statement and
orientation convention are explicit in Hirasawa–Hiura–Sakuma,
arXiv:2206.02097v2, Proposition 2.1(2). This is a uniqueness statement for
strong inversions of the **trefoil pieces**, not for arbitrary hyperbolic
knots or arbitrary actions on a graph manifold.

## 6. Global gluing ambiguity is only Conway mutation

Applying (f_1,f_2\) to the pieces changes the gluing to

\[
 g=f_2\circ h_r\circ f_1^{-1},\qquad g_*=\pm A_r.
\]

The map (g\) intertwines the two reference boundary involutions, exactly, so
it descends to a map (\bar g\) of the four-marked boundary spheres of their
tangle balls. The reference branch (J_r^0\) uses (\bar h_r\). The difference

\[
 u=g\circ h_r^{-1}
\]

commutes with the boundary elliptic involution and acts on torus homology by
(\pm I\). Its quotient (\bar u\) is an orientation-preserving mapping class
of the four-marked sphere in the kernel of the homology-lift map

\[
 \rho:\operatorname{Mod}(S_{0,4})\longrightarrow
             \operatorname{PSL}(2,\mathbb Z).
\]

The elementary pillowcase mapping-class calculation gives
\(\ker\rho\cong(\mathbb Z/2)^2\). Its three nonidentity elements are the
three half-turns permuting the four marked points in double transpositions.
They are precisely the Conway mutation maps. One way to check the kernel
calculation is to use the two slope curves generating a Farey edge: a kernel
element preserves their isotopy classes; composing with one of the four
half-turn classes fixes the marked points, and the Alexander method on the
complementary once-marked disks makes the remaining class trivial.
Farb–Margalit, *A Primer on Mapping Class Groups*, Proposition 2.7,
printed pp. 56–57, gives this calculation explicitly.

It follows that gluing by (\bar g\) instead of (\bar h_r\) changes the
reference branch by at most one of these three mutations, up to isotopy of
the boundary gluing. This establishes both the mutation conclusion and the
at-most-four bound. We do not assume the two piece conjugacies agree on their
boundary; their discrepancy is exactly what the kernel calculation controls.

Menasco's theorem that Conway mutation preserves alternation now excludes a
mixed pair for (Y_r\). This completes the family-scoped theorem.

## 7. What still prevents an original solution

The turn genuinely attempts the remaining toroidal involution route and
closes this family, but its hypotheses do not cover the original problem.

* A general toroidal common cover can have a different JSJ graph, pieces with
  more boundary components, and nontrivial permutations of pieces. The simple
  peripheral matrices and cyclic-generator inclusions above no longer follow.
* Local involutions need not be unique up to an orientation-preserving
  conjugacy with boundary action (\pm I\). Hyperbolic pieces can already have
  distinct strong-inversion classes. One cannot infer a mutation relation by
  forgetting these choices.
* A closed hyperbolic common cover has no such JSJ torus. Turn 1 restricts its
  isometry-group involutions but does not prove that all (S^3\)-quotient
  involutions are conjugate or have branches of the same alternation type.
* Opposite definite fillings of the common cover are still insufficient
  unless the actual branching involution extends with the exact push-in
  branch-surface property from Turn 2.

No universal replacement for these missing compatibility statements was
proved, and no opposite-alternation branch was found in a valid common-cover
construction. **The original question is unresolved in this work, 5/5.**
Further packaging and independent review must not be used as a sixth author
search turn.

## 8. Source-access qualifications

The complete Gordon–Luecke publisher PDF and complete Sakuma author-hosted
scan were retrieved. Sakuma's relevant source pages were rendered and
visually inspected; the scan has no embedded text. The complete 2022v2
Hirasawa–Hiura–Sakuma PDF is a corroborating primary statement.
Farb–Margalit's full primary book text was read at the accessible online
transcription, specifically Proposition 2.7 and its proof; no local publisher
PDF is claimed. Attempts to retrieve several author-hosted book endpoints
failed. The original Meeks–Scott full paper was not recovered; the precise
equivariant-JSJ consequence used here is explicitly stated in the complete
Gordon–Luecke primary paper for the present prime-knot-cover setting. These
are documented source limitations, not concealed additional assumptions.
