# Independent analytic reconstruction

This is the current analytic reviewer's derivation, not a historical review imported from the public archive. The ordinary derived series is \(G^{(0)}=G\), \(G^{(j+1)}=[G^{(j)},G^{(j)}]\). All closures below are the standard oriented closures of classical disk braids. The solvability convention is the integral smooth convention in Otto, Definition 2.3.

## 1. The signature really is nonhomomorphic on the pure subgroup

Let (s(b)) be the ordinary link signature, normalized to give the positive trefoil signature −2. Gambaudo–Ghys gives bounded defect for this closure signature on \(B_3\), a homogeneous quasimorphism \(q(b)=\lim_{r\to\infty}s(b^r)/r\), and 

\[
 |q(b)-s(b)|\leq6.
\]

This is a link statement: pure braids generally have multicomponent closures. It is not an assertion that the closure map is a group homomorphism on concordance classes.

Put \(x=\sigma_1,y=\sigma_2\), \(a=x^2,b=y^2,h=yx^2y^{-1},z=(xy)^3=\Delta_3^2\). All four are pure. The Artin relation gives

\[
 ahb=x^2yx^2y=x(xyx)xy=x(yxy)xy=(xy)^3=z.
\]

For positive integers \(r\), \(s(a^r)=1-2r\): the two-strand closure has this signature and the added third strand closes to a split unknot. Conjugacy gives \(q(a)=q(b)=q(h)=-2\). The three-strand full-twist formula of Gambaudo–Ghys gives \(s(z^{2r})=-8r\), hence \(q(z)=-4\). If \(q|_{P_3}\) were a homomorphism, the displayed product would instead force \(q(z)=-6\). Thus it is nonhomomorphic on the actual group needed, not just on \(B_3\).

The primary interfaces are Gambaudo–Ghys Theorem A/Remarks 1 and 3, printed p.545; Lemma 4.1 and its three-strand specialization, pp.568–569; homogenization, p.575. The constants and signs are also corroborated by fresh exact controls, but those controls do not replace the primary theorem.

## 2. Persistence at every finite derived depth

Suppose a homogeneous real quasimorphism \(f\) on a group \(G\), with defect \(D\), vanishes on \(N=G^{(k)}\), where \(k\geq1\) is finite. Normality yields

\[
 (gu)^r=g^r u_r,\qquad
 u_r=(g^{-(r-1)}ug^{r-1})\cdots(g^{-1}ug)u\in N
\]

for \(u\in N\). Apply the defect inequality once to the pair \(g^r,u_r\). Homogeneity and \(f(u_r)=0\) give

\[
 |r f(gu)-r f(g)|\leq D.
\]

Dividing by \(r\) proves \(f(gu)=f(g)\), so \(f\) descends to a homogeneous quasimorphism on \(G/N\). This quotient is solvable, hence amenable. Calegari's Proposition 2.65 says such a function on an amenable group is a homomorphism. Its pullback then is a homomorphism on \(G\). The contrapositive proves that a nonhomomorphic \(f\) is nonzero on every finite positive derived subgroup.

This argument neither assumes \(G\) amenable nor sums \(r\) separate error bounds. The ordinary derived quotient, finiteness of (k), and homogeneity are essential. It gives no one element lying in all the subgroups. The credited Kawasaki–Kimura–Maruyama–Matsushita–Mimura Lemma 7.12, printed p.1207, proves a stronger prior statement about defect equality under solvable quotients; the manuscript correctly does not claim the group-theoretic lemma as new.

## 3. Why the pointwise signature at −1 obstructs the specified 1-solution

Let \(L\) be algebraically split and suppose its zero surgery \(M_L\) bounds an integral smooth 1-solution \(W\). Otto's definition supplies \(H_1(W;\mathbb Z)\cong H_1(M_L;\mathbb Z)\cong\mathbb Z^m\), a free \(H_2(W;\mathbb Z)\) of rank \(2r\) represented by embedded oriented framed surfaces \(L_i,D_i\), one positive transverse intersection in each dual pair, and no other intersections. The fundamental groups of **both** sets of surfaces map into \(\pi_1(W)^{(1)}\).

The meridian character assigning −1 to every component extends across \(W\) through the stated integral \(H_1\) isomorphism. Call its rank-one rational local system \(\mathbb Q_\alpha\). On a finite CW model of \(W\), evaluating the group-ring boundary matrices at this character gives signed integer matrices. Reducing them modulo two gives the ordinary matrices over \(\mathbb F_2\). Any nonzero mod-two minor has odd integer determinant, so

\[
 \operatorname{rank}_{\mathbb Q}d_j^\alpha
 \geq\operatorname{rank}_{\mathbb F_2}d_j.
\]

Equal chain dimensions therefore imply \(b_2(W;\mathbb Q_\alpha)\leq b_2(W;\mathbb F_2)=2r\). The last equality uses the integral universal coefficient sequence and the absence of two-torsion in \(H_1(W;\mathbb Z)\). It does not assume acyclicity or an Alexander polynomial nonvanishing condition.

The character is trivial on each surface group, so each surface has a local-coefficient fundamental class. Its normal framing makes its self-pairing zero. Disjointness makes the off-pair entries zero, and the unique intersection in each dual pair has coefficient +1 or −1. Changing the sign of one member makes each block the hyperbolic matrix. These \(2r\) classes are independent because their pairing matrix is nonsingular; the dimension bound makes them a full basis. Thus the whole twisted intersection form has signature zero, including any potential issue of an ambient radical. The ordinary full form is hyperbolic as well. The case \(r=0\) is included by the same dimension argument.

For a unitary rank-one character that extends over this bounding four-manifold, Toffoli Eq.(1.1) identifies the rho invariant with the ordinary signature minus the twisted signature, hence zero. In the one-colour surgery formula, Theorem 4.24/Remark 4.25 Eq.(4.21), zero framing and algebraic splitting make **every entry** of the framed linking matrix zero. The framing is compatible by Definition 4.7/Remark 4.8: all surgery relations evaluate trivially. Consequently every correction vanishes and \(\rho_\alpha(M_L)=-\sigma_L(-1)\). The one-colour hypothesis is automatic, and \(\omega=-1\\) lies in the allowed domain \(U(1)\setminus\{1\}\). The formula is pointwise and does not exclude Alexander roots. Therefore \(\sigma_L(-1)=0\).

This closes the central topology interface without substituting a knot-only theorem, a rational solution, a half-step solution, an averaged signature, or a concordance homomorphism assertion.

## 4. Conclusion with the correct quantifiers

Fix finite \(k\geq1\). Sections 1–2 give \(v\in P_3^{(k)}\) with \(q(v)\ne0\). Choose a positive integer \(r\) so that \(r|q(v)|>6\). Then \(\gamma=v^r\in P_3^{(k)}\), and the homogenization error bound implies \(s(\gamma)\ne0\). Taking the power is necessary: \(q(v)\ne0\) alone does not establish \(s(v)\ne0\).

Every pairwise linking number is a homomorphism on \(P_3\), so it vanishes on its commutator subgroup and on all positive derived subgroups. Thus the closure of \(\gamma\) is algebraically split, and Section 3 rules out a 1-solution. Add geometrically split vertical strands to obtain the claim for any \(m>3\); this group homomorphism preserves derived membership, and its closure adds split unknots, which preserve signature. Finally \(\mathcal F_n^m\subseteq\mathcal F_1^m\) for integer \(n\geq1\), so set \(k=n+2\).

For \(m=1,2\), positive derived groups are trivial; the theorem excludes them. The witness may depend on (k). No conclusion for rational, surface-braid, power-subgroup, lower-central, or infinite-intersection variants follows from this argument.

## 5. Independent finite witness calculation

Before reading any submitted executable, `fresh_braid_controls.py` constructed

\[
 c=[a,b],\quad d=a^{-1}ca,\quad e=b^{-1}cb,
 \quad u=[c,d],\quad v=[d,e],\quad\beta=[u,v].
\]

Normality puts \(c,d,e\in P_3^{(1)}\), \(u,v\in P_3^{(2)}\), and \(\beta\in P_3^{(3)}\). Fresh free reduction gave 104 Artin letters. Exact strand tracking gave identity permutation and zero pairwise signed crossing sums.

The independent numerical mechanism used \(X=\bigl(\begin{smallmatrix}1&0\\-1&1\end{smallmatrix}\bigr)\), \(Y=\bigl(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\bigr)\) and the Gambaudo–Ghys Meyer form on \(\operatorname{im}(M^{-1}-I)\cap\operatorname{im}(I-G)\). For a single generator the latter image has rank one, so exact rational linear solves and the sign of a scalar suffice. This is materially different from the supplied full-kernel/pullback implementation. Summing the 104 signed contributions gives signature −2 and final Burau matrix

\[
 \begin{pmatrix}
 -1401703009468415&3686720931790848\\
 2187353096552448&-5753116310519807
 \end{pmatrix},\qquad\det=1.
\]

Afterward, the unchanged current release verifier replayed the author's exact Goeritz certificate, a planar-face Goeritz reconstruction, and the full-kernel Meyer reconstruction. All 104 Meyer terms, the literal word, and the final matrix agree with the fresh result. The Goeritz certificate has size 48, inertia ((23,25,0)), determinant −7154819319988224 and correction zero.

The required supporting proof openly handles an index discrepancy in Erle's printed cyclic-matrix formula. Visual inspection of the original definitions and crossing/region diagrams supports the current-block edge contribution used in the package; the supplied planar-face computation also derives it from the diagram, rather than blindly using that printed index. The witness alone would not detect the discrepancy because its even block lengths yield a sign congruence. The package's unequal-sign short control distinguishes the two formulas. This is a disclosed primary-source indexing issue already addressed by the published proof, not a defect newly repaired during this review.

These finite calculations verify the explicit depth-three example. The arbitrary-depth theorem rests on Sections 1–4 above, not extrapolation from the example or from sampled controls.
