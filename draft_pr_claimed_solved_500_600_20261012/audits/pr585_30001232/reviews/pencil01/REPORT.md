# Independent adversarial audit: the plane pencil and its minimal double cover

PR 585, problem 30001232 / OWR-3471-006. Reviewed head:
`0a94b2a7e8d682af7d51a3fba7fe8df4a36f6f27`.

**Mathematical verdict: PASS for the complete stated counterexample family, for every integer d >= 7.** I found no missing construction step, incorrect intersection number, or required mathematical repair. In particular the claimed degree-seven example satisfies all hypotheses of the primary conjecture and strictly violates its displayed bound. This is an internal AI mathematical review, not human peer review, a formal proof certificate, or a historical-priority clearance.

The assigned emphasis was plane-pencil existence, local algebra, intersection calculations, and the exact inequality. I also checked the cover, minimality, and degree-one lifted curve needed to connect those ingredients to the full conclusion. I did not consult the other new review family. The source-first checkpoint predates opening the candidate proof and the older audit; its first deductions agree with the subsequently read candidate. The older audit was read afterward for comparison, not used as a proof premise.

## 1. Exact source question and success criterion

I independently inspected the publisher PDF, including the image of printed page 1124, Conjecture 2, in [Szemberg's contribution to OWR 21/2009](https://ems.press/content/serial-article-files/46224?nt=1), report DOI [10.4171/OWR/2009/21](https://doi.org/10.4171/OWR/2009/21). The target is

    epsilon(S,L;x) >= 1 / (2 + |K_S^2|^(1/4)).

It concerns a smooth minimal complex projective surface, an ample integral line bundle, and an arbitrary point. Picard number one and very general points are distinguished elsewhere in the source and are not restrictions on this conjecture. The constant 2 is outside the fourth root. The question on [arXiv:0711.0584v1, page 7](https://arxiv.org/pdf/0711.0584), and Question 6.1.6 in [arXiv:0810.0728v2, printed page 17](https://arxiv.org/pdf/0810.0728v2), visually corroborate the formula.

The complete imported catalogue record and empty prior report were read with the read-only queue inspection command and preserved as `CATALOG_AND_PRIOR.json`. The catalogue's radical includes the 2; that is a substantive transcription error. The present candidate targets the primary formula, and its d=7 example also violates the stronger catalogue formula. Exact-ID inspection of the related-target groups found no match. No status or queue mutation was performed.

The success criterion is one valid example with a strict reverse inequality. The candidate supplies a family of varying surfaces; it does not assert an exact Seshadri constant, vanishing on a fixed surface, a Picard-rank-one counterexample, or a very-general-point violation.

## 2. The singular plane curve is globally integral

Set

    f_d = Z(X^(d-1)-Y^(d-1)) + X^d,    p=[0:0:1].

Over C[X,Y], the coefficients of this degree-one polynomial in Z are coprime. Indeed a common divisor of X^d and X^(d-1)-Y^(d-1) would have to divide both X and Y. Therefore f_d is primitive; over C(X,Y) it has degree one and is irreducible. Gauss's lemma proves irreducibility over C[X,Y,Z]. A square-free tangent cone alone would not establish this global integrality; the primitive linear-polynomial argument does.

In the chart Z=1 the lowest-degree term is x^(d-1)-y^(d-1). In characteristic zero its d-1 roots in tangent-direction coordinates are distinct. Thus p is an ordinary point of multiplicity d-1. To check the rest of the projective curve, f_Z=0 and f=0 imply X^d=0, hence X=Y=0. This leaves only p. Alternatively, on the Y=1 chart the three derivatives generate the unit ideal: f_Y forces Z=0, f_Z forces X^(d-1)=1, while f_X then cannot vanish. The latter excludes all points with Y nonzero, and f_Z excludes every remaining point other than p.

An independent normalization check is

    [s:t] -> [sA:tA:-s^d],    A=s^(d-1)-t^(d-1).

These homogeneous degree-d coordinates have no common zero. Substitution annihilates f_d; away from A=0 the ratio X:Y recovers s:t. This confirms an integral rational curve, with d-1 distinct points above p. Local branching does not make the global curve reducible.

The fresh program checks the primitive coefficient criterion, square-free tangent cone, actual affine Jacobian ideal `(x^(d-2),y^(d-2))`, complementary projective chart, and normalization identities for d=3,...,23. The general arguments above, not this finite range or factorization over Q, establish the statements over C for all relevant d.

## 3. A pencil whose every member is integral really exists

Let P(V_d) be the projective space of degree-d forms, of dimension N_d=d(d+3)/2. For a split d=a+(d-a), the product map from P(V_a) x P(V_(d-a)) is a morphism from a projective variety. Its image is closed and has dimension at most N_a+N_(d-a). The finite union R of these images contains exactly the reducible degree-d polynomials, including repeated factors. A nonreduced homogeneous polynomial of degree at least two over C necessarily has a nontrivial factorization, so it is included.

For every split,

    N_d - N_a - N_(d-a) = a(d-a) >= d-1.

Consequently dim R <= N_d-(d-1). Since [f_d] is not in R, the closure J of the union of joining lines from [f_d] to R has dimension at most dim R+1 <= N_d-d+2. This is strictly smaller than N_d for d>=3. Taking the closure is legitimate and does not increase this bound: the joining-line family is parametrized by a projective-line family over R; its image or closure has at most the dimension of that family. The entire construction can equivalently be described as the projective join.

Choose [g] outside J. It is automatically independent of [f_d], and the pencil line has no point in R: if a reducible member r lay on it, g would lie on the joining line from f_d to r. Hence **every** member is integral and reduced, not just a general member. This argument would not work in degree two: the upper bound on J equals the ambient dimension. The proposed theorem only needs d>=7.

There is no compatibility problem with the other generic requirements. The complete O(d) linear system on P2 generates the bundle and gives the Veronese closed immersion. Thus a general member is smooth; its restriction to the smooth open curve C_0 minus p remains generated and gives an immersion, so a general member cuts that curve transversely. The open condition g(p) != 0 excludes the sole singular point. These are nonempty open subsets of the same irreducible parameter space. Their finite intersection with P(V_d) minus J is nonempty. This is the precise situation of the smooth hyperplane-section statement in [Stacks Project, Lemma 33.47.3](https://stacks.math.columbia.edu/tag/0FD4), whose hypotheses and proof I read.

A direct jet-count explanation also checks nonemptiness: value plus tangent derivative at a smooth point of C_0 impose two independent linear conditions on degree-d forms; the point varies in dimension one. The bad incidence therefore has image closure of codimension at least one. For smoothness of g in P2, value plus two first derivatives impose three independent conditions, with the point varying in dimension two. The local monomials 1,x,y already span these jets. Avoiding p removes another hyperplane. None of these proper closed conditions can consume the nonempty open complement of J.

There is no common component because g is not proportional to the integral f_d. Bezout now gives exactly d^2 distinct intersections, each of local intersection length one and all away from p. No high-multiplicity or infinitely near basepoint was omitted. It is unnecessary to exhibit numerical coefficients for g: the nonempty-open proof is a complex geometric existence proof, unlike a finite sample of pencils.

## 4. One blowup per basepoint suffices; no fibre components appear

At a transverse basepoint, local equations for f_d and g are regular parameters u,v in the smooth plane. The graph of their ratio is the blowup of the ideal (u,v). In the chart with graph equation u*beta-v*alpha=0 and alpha=1, one has v=u*beta. The exceptional curve maps isomorphically onto the pencil parameter line. In particular it is a section.

Every nonzero combination a*u+b*v has nonzero linear term, so every member has multiplicity one at each basepoint. Subtracting each exceptional divisor once removes exactly that base multiplicity. No exceptional curve is a fibre component, no residual basepoint remains, and no second blowup is necessary. The fibres of f:Y->P1 are precisely the integral reduced strict transforms of the pencil members. The blowup is an isomorphism at p, so the distinguished fibre C retains its ordinary (d-1)-fold point y. These local blowup facts are also presented in Kumar's [MIT surface notes, Lecture 2, printed page 4](https://live.ocw.mit.edu/courses/18-727-topics-in-algebraic-geometry-algebraic-surfaces-spring-2008/198274c0c471d31fc05d600e28e403db_lect2.pdf), which I read in addition to the candidate.

## 5. The polarization is ample on every curve

For H the pulled-back line and E_i the exceptional curves,

    F=dH-sum E_i,    F^2=0,    F.E_i=1,    E_i^2=-1.

The divisor A=2F+E_1 has A^2=3, A.E_1=1, A.F=1. The class F=f^*O(1) is nef. For an integral curve D different from E_1, E_1.D>=0 on the smooth surface. If D is horizontal then F.D>0, so A.D>0. If F.D=0, the proper integral curve maps to a point: a nonconstant map to P1 would have positive degree. Since that fibre is integral and reduced, D must be the whole fibre, so A.D=1. The remaining curve E_1 has intersection one. These exhaust all curves.

Thus the surface Nakai-Moishezon criterion applies. Its square and all curve-intersection hypotheses were checked, rather than positivity on a list of displayed curves alone. I read the statement and proof sketch in the same [MIT notes, §1.3, printed page 3](https://live.ocw.mit.edu/courses/18-727-topics-in-algebraic-geometry-algebraic-surfaces-spring-2008/198274c0c471d31fc05d600e28e403db_lect2.pdf).

The classical provenance is correctly Miranda's pencil mechanism, explicitly treated in [Bauer, arXiv:math/9903072v1, Proposition 3.3](https://arxiv.org/pdf/math/9903072), which I read with its proof and Lemma 3.5 on pp.11–14. His d=m+1 choice is stated for sufficiently large d; I visually inspected that qualification on p.13. It cannot serve as a finite degree-seven existence theorem. The present direct parameter-space proof supplies that finite case independently. The release note already makes this correction while preserving the older author prose.

## 6. The double cover is smooth, connected, and projective

There is a smooth pencil member g, so at least one fibre is smooth. The critical locus has closed image under the proper morphism f, and does not dominate the base; hence nonsmooth values form a finite set. Choose four distinct smooth values away from the distinguished singular fibre. A connected double cover h:B->P1 branched simply there exists by the square-root construction for a square-free quartic. Riemann-Hurwitz gives genus one.

The fibre product S=Y x_(P1) B is finite flat of degree two over Y. Its branch divisor is the disjoint union of the four smooth fibres. Away from them the map is etale over a smooth surface, so the source is smooth even above singular fibres. On a branch fibre f is a smooth map with local coordinates (t,u); the cover has t=v^2, giving smooth coordinates (v,u). Thus the fibre product itself is smooth; no normalization, resolution, or contraction changes the claimed invariants. The negative control that branches through the marked singular fibre instead has all local partial derivatives zero, demonstrating why the smooth-branch restriction matters.

The morphism S->B is proper with connected fibres, all base changes of the geometrically integral pencil fibres over C. If S were disconnected, its disjoint proper components would have disjoint closed images partitioning the connected B, which is impossible; no connected fibre can meet both pieces. Therefore S is connected. A connected smooth complex scheme has only one irreducible component, since regular irreducible components are disjoint. It is reduced, hence integral. It is projective because it is finite over the projective Y. No part of the assertion relies on treating a singular branch cover as automatically smooth.

## 7. Canonical formula, ampleness, and the formerly exceptional curves

The cover h is defined by the line bundle O_P1(2) with branch section of O_P1(4). Its base change is therefore the standard double-cover algebra O_Y plus O_Y(-2F). The ramification divisor has line bundle pi^*O_Y(2F). Locally dt=2v*dv gives ramification order one, yielding the line-bundle identity

    K_S=pi^*(K_Y+2F),
    K_Y=-3H+sum E_i,
    N=K_Y+2F=(d-3)H+F.

There are no discrepancies from singular fibres, because the cover is etale there. This is stronger than merely guessing the correct numerical class. H and F are nef. Every nonexceptional integral curve D has H.D equal to the positive degree of its plane image, so N.D >= (d-3)H.D>0 for d>=4. Each exceptional curve has N.E_i=1. The square is

    N^2=(2d-3)^2-d^2=3(d-1)(d-3)>0.

Nakai-Moishezon proves N ample. Finite pullback preserves ampleness, applicable to both N and A; I also checked [Stacks Project, Lemma 29.38.7(2)](https://stacks.math.columbia.edu/tag/0892). In the present surface setting it follows directly from the projection formula: every curve has a curve image under the finite map and positive degree, so its pullback intersection is positive, and the square is multiplied by two. Thus K_S and L=pi^*A are ample integral line bundles.

This proves minimality on the constructed S itself. A smooth rational (-1)-curve would have K_S intersection -1 by adjunction, contradicting ampleness. Each old exceptional section lifts instead to the elliptic curve B, with square -2 and canonical degree 2, so it is not a surviving rational exceptional curve. The passage from nonminimal Y to minimal S has been justified without losing the polarization by contraction.

The degree-two projection formula gives

    K_S^2=6(d-1)(d-3),    L^2=6.

The fresh controls verify these identities using the restricted H,F,E_1 Gram matrix, independently of both the author's full diagonal blowup lattice and the older audit's incidence-hypersurface calculation. They also retain zero- and two-branch formal comparisons: with two branches the canonical intersection on a lifted section is zero, whereas four branches give 2. These are controls of the specified formula, not additional constructions or new proof-search turns.

## 8. The individual lifted curve has degree one and the strict bound holds

Over the unbranched value of C, the two points of B give

    pi^(-1)(C)=C' disjoint union C''.

Both curves are isomorphic to C, not connected degree-two covers of it. Thus C' is integral, and at its point x above y it has multiplicity d-1. Projection formula on that individual curve gives L.C'=A.C=1. The total pullback of F has twice this intersection. Numerically, writing Q for one fibre of S->B and T for the lifted section, pi^*F=2Q, T^2=-2, T.Q=1, and L is numerically 4Q+T; this gives L.Q=1 and L^2=6. No linear equivalence of arbitrary degree-one divisors on the elliptic base is asserted.

The definition of the Seshadri constant now gives only the needed upper bound epsilon(S,L;x)<=1/(d-1). To beat the primary bound strictly, for d>3 it is equivalent to require

    d-3 > [6(d-1)(d-3)]^(1/4),
    (d-3)^3 > 6(d-1).

At d=7 the second inequality is 64>36. Its forward difference is 3(d-3)^2+3(d-3)-5, positive for all d>=7. This proves every asserted integer case. Equivalently, at d=7 alone, K^2=144<4^4=256 implies 2+144^(1/4)<6. Hence epsilon<=1/6 lies strictly below the source bound.

The specified witness does not beat that bound in degrees 4,5,6: the fourth-power margins are -17,-32,-9. This says nothing about whether another curve could have smaller quotient on those surfaces; no lower bound or exact epsilon was proved. The d=3 canonical square is zero and canonical ampleness fails; the proof does not claim it. A counterexample over C also suffices if one asks the same universal statement over a broader characteristic-zero class.

## 9. Actual reproduction and fresh falsification controls

`reproduce_originals.py` verified all eighteen file bytes and sizes against `ORIGINAL_SNAPSHOT.json`, whose independently observed SHA-256 is

    b74088ad62046937bc4835f761a500d7a8f9a39ac4eb0da9e3dcb03143adb6cf.

Each original was also read directly from the pinned Git commit and compared byte-for-byte. The exact inventory was checked before and after. The author SHA256SUMS binds nine author payloads; the audit JSON manifest binds the author freeze and its three audit payloads; the outer release manifest binds seventeen payloads. All eighteen originals remained unchanged.

Five top-level actual programs ran in separate disposable copies, each under macOS OS network denial. A localhost connection probe yielded EPERM, rather than mere lack of a listening service. Python bytecode writes were disabled and all temporary writes stayed in this family's ignored cache:

- Author `verify_intersections.py`: 27 rows, stdout bytes exactly equal the recorded JSON.
- Author `verify_formulas.py`: 97 rows, stdout bytes exactly equal the recorded JSON.
- Older `audit/independent_checks.py`: full actual 60,731-check result exactly equal the saved JSON.
- Original `verify_release.py`: actual strict seventeen-payload inventory and three nested exact replays passed.
- Original `test_integrity.py`: eight actual rejection controls passed, including optimization, changed/missing/extra content, symlink, duplicate, and traversal cases.

All five source programs were read, rather than accepting their summary flags. The nested jobs repeat some computations; they are not distinct proofs. Full provenance, output hashes, and result summaries are in `ORIGINAL_REPLAY.json`.

Separately, `fresh_controls.py` and `fresh_results.json` preserve 28,945 exact checks: the polynomial and chart computations above; 20,100 factor-split identities; jet-rank and local-blowup controls; eight symbolic restricted-lattice identities; local branch smoothness; full-cover versus single-fibre factors; and exact threshold checks through d=2001. Ten altered claims are rejected, including nonprimitive irreducibility, repeated tangent roots, the degree-two join threshold, the degree-six strict inequality, the wrong ramification correction, the wrong lifted-fibre degree, and the missing degree-two canonical factor.

The fresh result was independently rerun under OS network denial with Python 3.14 / SymPy 1.14.0 and matched the saved Python 3.9.6 / SymPy 1.14.0 stdout in every byte. `CROSS_RUNTIME_REPLAY.json` records that check. No clocks or machine-specific paths enter the mathematical JSON.

These finite calculations certify the encoded algebra and reproducibility only. They do not prove the existence of a complex all-integral pencil, Bertini, Nakai-Moishezon, connectedness, or historical priority. Those geometric steps were checked separately above. Increasing the control ranges would not strengthen a missing existence proof.

## 10. Disposition and limits

No required mathematical correction was found. The current release note already supplies the two useful clarifications: Bauer's degree choice is asymptotic, and N=(d-3)H+F makes all-curve positivity transparent. A concise preprint should keep those explanations, the distinction between one fibre and its total pullback, and the strict source denominator. Keep the eighteen historical originals unchanged; subsequent presentation belongs in separately versioned files.

This review does not clear priority. The classical pencil and cover methods must be credited, no firstness claim is supported, and source inspection of these passages is not a comprehensive current-literature search. A separate priority audit and new adversarial review of the completed publication package remain the parent's responsibility. No source PDFs, OCR, page images, or private catalogue corpus are in the authored seal; only source identifiers, fingerprints, and precise read scopes are included. No external individual or other shard agent was contacted, and no branch, Git index, queue, PR, publication service, or editor was modified.
