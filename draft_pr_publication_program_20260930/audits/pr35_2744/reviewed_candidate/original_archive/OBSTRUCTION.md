# Canonical-component compact-real arcs: normalization and remaining obstruction

**Disposition: unresolved. No full proof or counterexample was obtained.** The known cone-manifold theorem covers a substantial class, including hyperbolic two-bridge knots, but it does not establish the universal assertion. The deductions below clarify its exact coverage and isolate the missing step; they are not claimed as new discoveries.

**Target:** 2744 / KP-1.85. **Date:** 30 September 2026. **Model and effort:** gpt-6-astra, xhigh. **Substantive response:** 1/5.

## 1. Exact target and original source

[K3: A New Problem List in Low-Dimensional Topology](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), Problem 1.85, printed pp. 76–77, fixes a hyperbolic knot $K\subset S^3$ and the distinguished $\mathrm{PSL}_2(\mathbb C)$ character component containing the discrete faithful representation. It asks whether this particular component contains an arc of $\mathrm{SO}(3)$ representations, considered up to conjugacy. The question was proposed and scribed for K3 by T. Lidman.

A family produced only by conjugating one representation is constant in the character variety and does not count. Nor does an arc on another character component, an isolated compact-image character, or a real-character arc of noncompact type. The usual affine character variety uses the reductive/GIT quotient rather than the naive orbit space at nonsemisimple reducible representations. This causes no ambiguity for compact-group characters, whose orbits are closed.

[Chinburg–Reid–Stover](https://arxiv.org/abs/1706.00952), Conjecture 1.9, gives the corresponding $\mathrm{SL}_2(\mathbb C)$/$\mathrm{SU}(2)$ formulation. The current arXiv version is v3, 27 July 2020; the paper appeared in *IMRN* 2022, pp. 4969–5036. The checked conjecture and theorem statements come from this revised version and the published text, rather than the initial v1.

## 2. The finite-quotient normalization bridge

Let $M$ be the knot exterior and $\Gamma=\pi_1(M)$. The central projection

$$p:\mathrm{SL}_2(\mathbb C)\longrightarrow\mathrm{PSL}_2(\mathbb C)$$

induces a finite character map

$$p_X:X_{\mathrm{SL}_2}(\Gamma)\longrightarrow X_{\mathrm{PSL}_2}(\Gamma).$$

The precise reference is [Heusener–Porti](https://arxiv.org/pdf/math/0302075), Proposition 4.2, Remark 4.3, and Example 4.6. For a knot exterior every projective representation lifts. The obstruction lies in $H^2(\Gamma;\mathbb Z/2)$, which vanishes here; equivalently one can use the knot-exterior example in that source. The lifts differ by $H^1(\Gamma;\mathbb Z/2)\cong\mathbb Z/2$, acting by the meridian-sign twist. The projective character variety is the finite quotient by this action.

Fix the chosen oriented discrete faithful projective character $\chi_0$, and let $C_{\mathrm{PSL}}$ be its component. A lifted canonical curve $C_{\mathrm{SL}}$ containing a lift of $\chi_0$ maps onto $C_{\mathrm{PSL}}$. Indeed, its finite image is a closed irreducible curve containing $\chi_0$; the discrete faithful character is a smooth point on its unique local character component. The complex dimension is one for a one-cusped hyperbolic manifold.

The compact real groups match exactly:

$$p(\mathrm{SU}(2))=\mathrm{PSU}(2)\cong\mathrm{SO}(3),\qquad
p^{-1}(\mathrm{PSU}(2))=\mathrm{SU}(2).$$

Thus a genuine $\mathrm{SU}(2)$ character arc on $C_{\mathrm{SL}}$ projects to a nonconstant compact-real set on the chosen projective curve. It cannot collapse to a point because the map has finite fibers. The compact-real locus is semialgebraic; after restricting to a smaller subarc away from the finite branching and singular sets, its image is an arc of $\mathrm{SO}(3)$ characters.

Conversely, a projective compact-real arc has lifts on the finite preimage of $C_{\mathrm{PSL}}$. At least one one-dimensional component of this preimage contains infinitely many lifted unitary characters. Its finite image is all of $C_{\mathrm{PSL}}$, so it contains a point above $\chi_0$ and is a lifted canonical component. The semialgebraic unitary locus on it consequently contains an arc. This explains why the SL/SU and PSL/SO formulations do not have a hidden normalization gap for knot exteriors. It does **not** produce the missing arc.

## 3. What Dix's theorem actually proves

[James P. Dix, *Ribbon Concordances and Representation Varieties*](https://escholarship.org/content/qt27j2v475/qt27j2v475_noSplash_7f3e70d717e17eaf9515cffc4ef313be.pdf), Berkeley dissertation, 2024, Section 3.3, Theorem 3.3.3, proves the compact-real curve assertion when the pair $(S^3,K)$ admits a Euclidean cone-manifold structure with cone angle at most $\pi$. Corollary 3.3.4 covers hyperbolic two-bridge knots. These are existing results, not results of this attempt.

The proof does more than exhibit one rotational holonomy. It obtains a unitary real curve through a smooth Euclidean-holonomy character, regenerates nearby hyperbolic cone structures, and follows a decreasing-angle deformation to the complete hyperbolic holonomy. Smoothness along that path supplies the needed component control. The finite quotient described above turns the asserted SL/SU curve into the arc requested by KP-1.85.

There are two separate dependencies: producing a compact-real arc and proving it lies on the geometric component. Retaining only the Euclidean rotational representation would discard the first; retaining only a connected path without the smooth-component argument would discard the second.

The dissertation's Section 5 explicitly describes the obstacle outside the angle criterion. A cone path reaching angle $\pi$ can degenerate into geometries other than the Euclidean geometry used in the theorem. In particular, the Montesinos-knot discussion is posed as future work, not an extension of Theorem 3.3.3 to all hyperbolic Montesinos knots. No universal continuation through those alternatives was established here.

## 4. Multiple SL components do not refute the projective question

[Boyle–Rouse, *Freely 2-periodic knots have two canonical components*](https://arxiv.org/pdf/2403.07157), Theorem 1.1 and Remarks 1.2–1.3, gives hyperbolic knots whose **SL** character varieties have two canonical components, corresponding to the two lifts of the same oriented complete holonomy. The paper's example includes $10_{157}$.

This is a useful warning against assuming a unique SL canonical component, but it does not establish two distinguished PSL components. If $C_+$ and $C_-$ contain the positive- and negative-meridian-trace lifts, the nontrivial sign twist $\epsilon$ exchanges them. Hence

$$p_X(C_+)=p_X(\epsilon C_+)=p_X(C_-).$$

Both images are precisely the component containing the fixed projective holonomy. The twist also preserves $\mathrm{SU}(2)$. Thus these two components neither supply nor obstruct the requested unitary arc by themselves. Changing orientation by complex conjugation is a separate operation; it must not be confused with the central sign quotient.

## 5. Routes checked and where each stops

### General compact representations

Gauge-theoretic existence results, as discussed in the introduction of Chinburg–Reid–Stover, provide nonabelian unitary representations somewhere in the character variety of a nontrivial knot. This existence statement does not identify their irreducible algebraic component with $C_{\mathrm{PSL}}$, and by itself does not supply an arc there. Moving between those components is the central missing assertion, so the general existence theorem cannot simply be substituted.

### A single unitary point

An isolated point does not prove an arc, particularly at a singular point. The elementary irreducible complex curve

$$y^2+x^2(1+x)=0$$

has an isolated real point at $(0,0)$: in $|x|<1/2$ its left side is at least $y^2+x^2/2$. Its complex discriminant as a quadratic in $y$ is $-4x^2(1+x)$, not a square, so this is not merely a union of conjugate lines. It also has a genuine real arc elsewhere, for example

$$x=-1-t^2,\qquad y=t(1+t^2).$$

This is an algebraic diagnostic, not a knot-character counterexample. It shows exactly why a computed isolated character, without regularity or a positive-dimensional compact-real locus, is inadequate.

Real trace values alone are also insufficient: real irreducible characters can be of $\mathrm{SL}_2(\mathbb R)$ type. Even elliptic individual generators do not force simultaneous compactness. For example, the real determinant-one matrices

$$A=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
B=\begin{pmatrix}0&-4\\1/4&0\end{pmatrix}$$

both have trace zero, but $\operatorname{tr}(AB)=-17/4$, impossible for a unitary product. Again this is only a representation-theoretic control; no knot relation is asserted for this pair.

### Complex-conjugation and field-of-definition shortcut

If a complex canonical curve differs from its complex conjugate, their intersection is finite. Any compact-real character lies in that intersection, so such a curve cannot contain the requested arc. This gives a possible obstruction test, but it requires an actual hyperbolic knot in $S^3$ with that property. Examples for other one-cusped manifolds are not enough.

[Long–Reid, *Fields of definition of canonical curves*](https://math.rice.edu/~ar99/fields_of_defn_published.pdf), Sections 4–6, discusses precisely this distinction and examples outside the knot-in-$S^3$ setting. Chinburg–Reid–Stover also warns that general one-cusped manifolds can lack real characters on the canonical component. No qualifying knot counterexample was found in this attempt. Boyle–Rouse's sign-exchanged pair from Section 4 is not such a counterexample.

### Cone-manifold continuation

The known Euclidean regeneration route succeeds under Dix's stated hypothesis. Extending it to every hyperbolic knot requires a new theorem controlling degenerations and obtaining a regular compact-real locus on the same component. The presently available argument stops there; it has not been replaced by an assumption that all knots admit the required Euclidean cone angle.

## 6. Verification and stopping point

The exact original statement, current primary versions, finite quotient, Dix's proof and limitations, and the 2024 multiple-component result were inspected. No later universal proof or counterexample was located in bounded searches through 30 September 2026. This is not a claim of an exhaustive literature review.

`check_controls.py` checks the algebraic examples and finite-quotient matrix identities exactly. Such tests are controls against invalid shortcuts, not evidence that a new knot satisfies or refutes the conjecture. No large knot census, floating-point continuation, or exhaustive search was performed.

**Exact remaining task:** for every hyperbolic knot not already covered by a verified geometric or arithmetic criterion, produce a positive-dimensional compact-real character locus on the chosen discrete-faithful component, or produce a verified knot for which that locus has no arc. None of the checked routes closes this gap. The original problem remains **unsolved in this attempt**.
