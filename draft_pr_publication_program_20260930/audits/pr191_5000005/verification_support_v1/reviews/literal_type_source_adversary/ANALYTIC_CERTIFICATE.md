# Analytic certificate: literal obstruction and repaired type law

This is an independently written audit certificate. It distinguishes the exact imported unrestricted target from the parity-selected interpretation explicitly used by the submitted candidate. It neither assigns priority nor incorporates any prior review opinion.

## 1. Geometric calibration from the primary source

Let (n\geq3), (N=n-2), and (d=N\pi/n). Put (X_0=O=(0,0)), (X_{n-1}=(1,0)), and list the other regular-polygon vertices clockwise above this edge, as in Fuchs Figure 9. The outgoing oriented side at (O) points along the positive horizontal axis. At the terminal vertex the interior angle shown in Figure 8 is (\pi-\beta), rather than (\beta). Consequently

\[
0\leq\alpha\leq d,\qquad 2\pi/n\leq\beta\leq\pi.
\]

For the direct chord (X_0X_j), (1\leq j\leq n-1), the inscribed-angle theorem gives

\[
\alpha_j=(n-1-j)\pi/n,
\qquad \pi-\beta_j=(j-1)\pi/n.
\tag{A1}
\]

In particular,

\[
\beta_j-\alpha_j=2\pi/n
\quad\text{for every direct chord.}
\tag{A2}
\]

Fuchs Figure 9 assigns this chord (A_{j-1}), with (A_N=A_0). For a genuine diagonal, strict convexity puts its open segment strictly inside the polygon. It is therefore a one-segment short trajectory with no intermediate vertex, side encounter, or ambiguity about its first endpoint.

## 2. Universal counterexample to the unqualified imported conjunction

The authenticated imported target says types are unique residues modulo (N) and, without a parity or generic-direction qualification, characterizes (A_0) by (\beta-\alpha=2\pi/n). It then imposes the signed angle rule for all admissible literal angles. These requirements cannot all hold.

For every (n\geq5), take (j=n-2) in (A1). Then

\[
\alpha=\pi/n,\quad \beta=3\pi/n,
\quad \text{so the bare shorthand gives } k=0.
\]

Choose (\ell=2), (\varepsilon=-1). This is permitted for both parities of (n), including the even-(\ell) requirement when (n) is even. The transformed literal slope is

\[
\alpha'=2\pi/n-\alpha=\pi/n=\alpha.
\]

It is the same first-vertex chord, whereas the requested type is (A_{-2}). Since (N\geq3), (0\not\equiv-2\pmod N). This contradicts uniqueness. There is no reduction of an angle modulo (\pi) or (2\pi) in this argument.

The raw printed four triples also fail to supply the requested label. At this chord the difference rows give (A_0), while the sum rows give (A_{N-1}). The demanded residue (N-2) is neither of these when (N\geq3).

There is a version using distinct interior chords, so the obstruction does not require counting a trajectory as parallel to itself. Start at the same chord (X_0X_{n-2}). For odd (n\geq5), choose (\varepsilon=1,\ell=1). The new chord is (X_0X_{n-3}), with endpoint angles (2\pi/n,4\pi/n). For even (n\geq6), choose (\varepsilon=1,\ell=2). The new chord is (X_0X_{n-4}), with angles (3\pi/n,5\pi/n). All of these are strict interior diagonals. Equation (A2) gives the bare label (A_0) to both chords, whereas the rule asks for (A_{-1}) or (A_{-2}), respectively. Neither requested residue equals zero or the other raw printed label of the target chord.

This is an analytic all-(n\geq5) refutation of the **unrestricted imported conjunction**. The source's preceding enumeration takes the initial angle in (0<\alpha<\pi/(2n)) for odd (n), or (0<\alpha<\pi/n) for even (n). Our starting angle (\pi/n) is outside the former and at the endpoint of the latter. Thus this family does **not** refute a conjecture restricted to those open generic sectors. A source-convention repair, rather than a generic-sector counterexample, is needed.

## 3. Exact parity-selected completion of Definition 2.1

For a trajectory of (q) segments, select the sum relation when (q) is odd and the difference relation when (q) is even. This is the sign convention in the paragraph immediately before Definition 2.1. Put (a=n\alpha/\pi\), (b=n\beta/\pi\). Then (0\leq a\leq N\), (2\leq b\leq n\), and the intended type is

\[
\begin{array}{ll}
q\text{ odd}:&s=(a+b)/2\in\mathbb Z,\quad k=n-1-s\pmod N,\\
q\text{ even}:&s=(b-a)/2\in\mathbb Z,\quad k=s-1\pmod N.
\end{array}
\tag{A3}
\]

Here is a full algebraic verification, rather than a numerical assertion that the printed inequalities agree. In the odd-segment case (1\leq s\leq n-1), so take the integer representative (k=n-1-s\in[0,N]). The lower-(k) sum row's restriction on (a) is (a\geq2s-n), precisely the already required (b\leq n). The upper-(k) sum row requires (a\leq2s-2), precisely (b\geq2). For even (n=2m) the ranges meet at (k=m-1) and give the same type; for odd (n=2m+1) they meet between (k=m-1) and (k=m).

In the even-segment case, (s\geq1) yields (k=s-1), and the lower-(k) difference row again reduces to (a\leq n-2s\), or (b\leq n). For (s\leq0) take (k=s-1+N); the upper-(k) difference row reduces to (a\geq2-2s\), or (b\geq2). The ranges of (s) implied by the endpoint-angle bounds put these representatives exactly in the corresponding printed (k)-ranges. Thus there is a unique residue for each selected parity.

The representative (k=N\equiv0) is needed for the one-segment horizontal side, (a=0,b=2,s=1). It is the explicit endpoint identification (A_{n-2}=A_0) in Figure 9. If the prose insists on representatives (0\leq k\leq n-3) **before** applying the printed inequalities, this side has no odd-segment row. Equation (A3) already handles it, but the endpoint representative must be stated when claiming literal equivalence to all printed inequalities.

For (A1), the one-segment formula gives (s=n-j) and (k=j-1), agreeing with Figure 9. In particular the counterexample chord's parity-selected type is (A_{N-1}), not (A_0), and its self-reflection gives (-k-2\equiv k\pmod N). The bare (A_0) characterization is therefore not globally valid for the repaired convention.

## 4. Audit certificate for the candidate's central mechanism

The following verifies the candidate's mechanism for the repaired convention; it is not a proof of the inconsistent literal conjunction.

Form the labelled double polygon (P\cup Q), (Q=-P), with opposite parallel edges glued by translations reversing endpoint order. Corner succession increases the vertex index by one and changes copies. For odd (n) the (2n) corners form one cone of angle (2N\pi). For even (n) they form two cones of angle (N\pi), based at (P_0,Q_0). Give each cone coordinate (\phi), increasing through each corner by (d=N\pi/n). Physical direction is (\phi\pmod{2\pi}) in the odd case and (\phi+c\pi\pmod{2\pi}) at even cone (c\in\{0,1\}).

For a fixed real lift of direction (\theta), label any forward or backward germ in its unoriented line by

\[
L_\theta(\phi)=(\phi-\theta)/\pi\pmod N.
\tag{A4}
\]

For either oriented physical direction these give all (N) residues without repetition. For odd (n), multiplication by two permutes residues since (N) is odd. For even (n), the two cones contribute the opposite parity classes. This argument never inverts two modulo an even integer.

For a connection starting at (P_0) in direction (\alpha), its initial label is zero. At a terminal corner numbered (t), the backwards offset within that corner is (\pi-\beta) in (P) and (\beta-2\pi/n) in (Q). In the first case physical direction gives (t+s\equiv0\pmod n), where (s=n(\alpha+\beta)/(2\pi)). The terminal label is (1+(tN-2s)/n\equiv n-1-s\pmod N). In the second case it gives (t-s+1\equiv0\pmod n), and the terminal label is ((tN+2s-2)/n\equiv s-1\pmod N). Thus terminal minus initial label is exactly (A3). This also checks the (\pi-\beta) convention rather than assuming the desired type identity.

For genus at least two, exchanging the two polygons by a half-turn is the hyperelliptic involution. It has (n+1=2g+2) fixed points for odd (n) and (n=2g+2) for even (n); Riemann-Hurwitz gives the sphere quotient. Conjugation by an affine map preserves its derivative (-I), so the conjugate is holomorphic, again has the sphere quotient, and equals it by uniqueness of the hyperelliptic involution. In the even case, this commutation synchronizes the angular maps at the two cones. An orientation-preserving derivative has a real angular lift (F(x+\pi)=F(x)+\pi). Hence (A4) changes by one common residue at every forward and backward germ. Terminal minus initial label is preserved.

For a model direction (\theta=h\pi/n), every inward vertex germ runs along a direct polygon chord: reflection in the polygon symmetry axis perpendicular to the direction pairs its endpoint vertices. A fixed vertex gives a supporting direction rather than an inward germ. For a chord between vertices (j,j'), its two corner offsets add to (d), and its direction gives (j+j'\equiv n-1-h\pmod n). Therefore its endpoint labels satisfy (a+b\equiv-h\pmod N), including side germs with their two identified corner descriptions.

The needed classical input is precise: the odd double-polygon group has one cusp orbit; the even double-polygon group has two cusp orbits represented by symmetry directions separated by (\pi/n); every saddle-connection direction is a cusp direction. Finster's complete §§3.1-3.2, particularly p.7, explicitly identify the even double-polygon group with the group stated there, so this is not an unproved transfer from the smaller opposite-side quotient. Finster pp.6,8,20 and Boulanger-Lanneau-Massart §1.4 p.791 supply the stated group/cusp facts. The original Veech (1989) full text was not independently read in this audit. [Finster](https://arxiv.org/pdf/1005.4588v3), [Boulanger-Lanneau-Massart](https://ahl.centre-mersenne.org/item/10.5802/ahl.211.pdf).

Apply the single affine map taking a given saddle direction to one of the model directions. It acts on **all** germs. Every model germ ends at a first vertex, so its inverse proves finiteness for every original germ. Transport of the endpoint-sum law by the common label shift gives one residue (C\) such that (b=C-a\) for every connection in that direction. No assertion equivalent to the target has been inserted as an unsupported lemma.

Finally rotate the initial germ of angle (\alpha'=\alpha+\ell\pi/n) into direction (\alpha). Such rotations exist for every integer (\ell) in the odd case and every even (\ell) in the even case, respecting the gluing. Its cone label (a) obeys (na=tN+\ell\) for its corner number (t), hence (2a\equiv\ell\pmod N). The endpoint-sum constant for the original connection is its type (k), so the rotated connection's intrinsic type is (k-2a=k-\ell). This proves the positive rule without division by two. Reflection about the angle bisector transforms (\alpha\) into (d-\alpha), (\beta\) into (\pi+2\pi/n-\beta), and (A3) into (-k). Composing gives the negative rule (k'=-k-\ell). Literal admissibility is retained throughout.

The torus cases (n=3,4) use triangular and square lattice unfolding. There is one type for (n=3); for (n=4), the primitive endpoint has type one exactly when both coordinates are odd, a property unchanged by the permitted coordinate swap. For (n=6), primitive coordinates in the honeycomb basis give the four classes in candidate Equation (12); rotation ((p,q)\mapsto(p-q,p)) changes the type by (-2\pmod4), and bisector reflection swaps the coordinates and negates the type. The missing honeycomb residue is handled by taking the first multiple one or two, rather than falsely claiming every primitive point is itself a vertex. These facts give every allowed transformation, including edges.

Conclusion: the candidate's universal **parity-selected** signed angle theorem is supported by a complete analytic mechanism and the explicitly credited classical input. It needs a source-convention qualification and an endpoint-representative clarification. It cannot establish the unamended literal imported conjunction, which Section 2 analytically refutes.
