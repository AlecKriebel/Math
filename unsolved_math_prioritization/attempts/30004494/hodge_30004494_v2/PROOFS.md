# Boundary corrections: proved controls and the remaining gap

Problem 30004494 / OWR-1703871-010. Authored 2026-10-05. This is a partial-result packet, not a solution of the higher-dimensional Hodge-theoretic conjecture. The elementary propositions below are standard consequences of classical positivity and linear algebra; no novelty is asserted.

Throughout, a variety is over C; X is smooth, projective and integral, Z = union Z_i is a reduced SNC divisor, and L is a Cartier divisor. Additive line-bundle notation is used. The cone C = NEbar(X) is the closed cone of effective numerical curve classes in N_1(X)_R. Nef means nonnegative on C. Ample means that some positive tensor power is very ample. Big means maximal Iitaka dimension. Semiample means that some positive tensor power is globally generated. These properties must not be conflated.

## 1. Exact null-face criterion, including uniformity

**Proposition 1.** Suppose L is nef and E is a fixed real divisor. Then the following are equivalent:

1. tL-E is ample for some real t.
2. mL-E is ample for every sufficiently large integer m.
3. -E is strictly positive on every nonzero class in F = C intersect L-perp.

For (2), “ample” for a real class means membership in the real ample cone. An integral class in that cone is an ample line bundle.

**Proof.** (1) implies (3) by restriction to F and Kleiman's criterion. To prove the converse, choose an ample class H and consider K = {c in C : H.c = 1}. This is compact. For completeness, H is strictly positive on every nonzero c in C, so on the compact unit-sphere slice C intersect {||c||=1} it has a positive minimum. Therefore H.c=1 bounds ||c||, and K is closed and bounded. If K is empty, X has dimension zero and every line bundle is ample; otherwise proceed below.

If F intersect K is nonempty, (3) and compactness give eta>0 such that E.c <= -eta on that set. By continuity this remains negative in an open neighborhood U of F intersect K inside K. The compact complement K minus U has L.c >= delta>0. Let M = max_K E.c. Choose t with t delta > max(M,0). On U, tL-E is positive since L is nef and E is negative. On K minus U it is positive by the choice of t. Kleiman gives ampleness. If F intersect K is empty, min_K L.c>0 directly gives the same conclusion. Increasing t adds a nef class; the same argument, or the ample-plus-nef theorem, preserves ampleness. This proves (2) and (1). The implication (2) implies (1) is immediate. QED.

This is a criterion, not a proof that the required boundary E exists. Positivity merely on individual actual curves with L.C=0 does not automatically imply positivity on the whole closed null face. Nor does finding a threshold m(C) for every curve provide one threshold for all curves.

**Explicit nonuniformity control.** In R^3 let C consist of (x,y,z) with x,z>=0 and y^2<=xz, let L(x,y,z)=x and E(x,y,z)=y. For c_t=(t^2,t,1), t>0, (mL-E)(c_t)=mt^2-t becomes positive eventually for each fixed t. There is no common m: t=1/(2m) gives -1/(4m). The limiting null ray (0,0,1) also has E=0. This is an abstract cone countermodel to an inference, not a Hodge-theoretic or geometric counterexample.

## 2. Real, rational and fixed integer coefficients

**Proposition 2.** Suppose L is nef. The following existence assertions are equivalent:

(a) There are real t and a_i>=0 such that tL-sum a_i Z_i is ample.
(b) There are rational t and a_i>=0 with the same property.
(c) There are integers a_i>=0 and m_0 such that mL-sum a_i Z_i is ample for all integers m>=m_0.

**Proof.** (c) implies (b) implies (a). For (a) implies (b), the ample cone is open. Approximate t and the positive a_i by rational numbers, holding exactly zero coefficients at zero. All nonnegative signs are preserved and the class remains ample. Increase the rational t if necessary to make it positive; nefness of L preserves ampleness. Clear denominators with a positive integer q. Then m_0=qt is an integer, E=sum qa_i Z_i is effective integral, and m_0L-E is ample. For m>=m_0, add the nef divisor (m-m_0)L. QED.

Thus a real-coefficient *ample* construction is enough, but a real-coefficient merely nef construction is not. Openness is essential. This does not assert that arbitrary real line bundles are semiample, a notion requiring additional conventions; semiampleness cannot be obtained by this openness argument.

## 3. A constructive surface theorem

**Theorem 3.** Let X be a smooth projective surface, L a nef and big Cartier divisor, and suppose every irreducible curve C with L.C=0 is a component of Z. Then there is an effective integral divisor E supported on those null components such that mL-E is ample for every sufficiently large integer m.

This recovers the algebraic mechanism of the known surface case once its Hodge-theoretic positivity hypotheses have been established. It does not establish those hypotheses in higher dimension.

**Step 1: finiteness and negative definiteness.** By Kodaira's lemma choose k>0, an ample Cartier divisor H, and an effective divisor G with kL linearly equivalent to H+G. A curve C not a component of G has G.C>=0, and hence kL.C>=H.C>0. Consequently there are only finitely many null curves, say C_1,...,C_r, all among the components of G. If r=0 the later uniform argument works with E=0.

For r>0 set A_ij=C_i.C_j. Off-diagonal entries are nonnegative. Since L^2>0 and every C_i is orthogonal to L, the Hodge index theorem implies v^T A v<=0 for all real v. In fact A is negative definite. Otherwise choose nonzero v with v^T A v=0. Because the off-diagonal entries are nonnegative, |v|^T A |v|>=v^T A v=0; negative semidefiniteness forces equality. The divisor D=sum |v_i| C_i is nonzero and effective, is orthogonal to L, and has square zero. The negative definiteness of the intersection form on L-perp in N^1(X)_R forces D to be numerically zero. This contradicts H.D>0. Thus A is negative definite without needing connectedness of the union.

**Step 2: rational coefficients without a false eigenvector claim.** For any rational symmetric negative-definite matrix A with off-diagonal entries >=0, put P=-A and solve Pa=1. Then every a_i is strictly positive. Indeed, P is positive definite with nonpositive off-diagonal entries. The unique minimizer of f(x)=x^T P x/2-1^T x is a=P^{-1}1. Replacing x by |x| cannot increase the quadratic term and cannot increase the linear term; if any coordinate is negative, the linear improvement is strict. Thus a>=0. If a_i=0, then (Pa)_i=sum_{j != i}P_ij a_j<=0, contrary to (Pa)_i=1. Hence a>0. Since P is rational and nonsingular, a is rational. Take q clearing all denominators and let b=qa, E=sum b_i C_i. Then b_i are positive integers and E.C_i=(Ab)_i=-q for every i.

A global strictly positive eigenvector is unnecessary and is in fact false for disconnected matrices: diag(-1,-2) has none. The construction above works on all blocks at once. This repairs that possible misuse of the statement of Lemma 2.3 in GGR 2021 without challenging the surface conclusion.

**Step 3: one m for all curves, not m(C).** Choose an integer c>0 such that cH-E is ample. Such c exists for any fixed E and ample H. If C is not a component of G, then

(mL-E).C >= (m/k)H.C-E.C > (m/k-c)H.C.

Thus all those curves are controlled simultaneously by m>=kc (indeed the strict inequality remains at equality). Only finitely many components C of G remain. If L.C>0, choose m greater than E.C/(L.C), if that ratio is positive. If L.C=0, Step 2 gives (mL-E).C=q>0 independently of m. Take a common maximum of the finitely many thresholds. Finally L.E=0, and

(mL-E)^2 = m^2 L^2 + E^2 >0

for m sufficiently large. Nakai-Moishezon on surfaces now gives ampleness for one common threshold. QED.

**Computable matrix example.** For A=[[-5,2],[2,-1]], -A^{-1}1=(3,7). Thus E=3C_1+7C_2 has E.C_i=-1. The unweighted divisor C_1+C_2 has intersections (-3,1); its negative has negative degree on C_2. Fixed unequal coefficients are genuinely needed. The example is an intersection-matrix illustration; no specific Hodge family realizing that matrix is claimed here.

## 4. Pullbacks, actual generic-Torelli obstruction and boundary blowups

**Proposition 4.1.** Let f:X->Y be a morphism of projective varieties, A ample on Y, and rL=f^*A for an integer r>0. If E is an integral divisor with O_X(-E) f-ample, then mL-E is ample for all sufficiently large m. Conversely, if mL-E is ample for some m, then O_X(-E) is f-ample.

**Proof.** Relative ampleness and ample twisting give k f^*A-E ample for all sufficiently large k. Thus rkL-E is ample. L is nef because a positive multiple is the pullback of an ample divisor. Adding any nonnegative multiple of L yields every larger integer m, not only multiples of r. Conversely mL-E restricted to any fibre equals -E restricted to the fibre; equivalently, tensoring a relatively ample bundle with a pullback from Y preserves relative ampleness, and an absolutely ample bundle is f-ample. QED.

So semiampleness of L reduces the target to finding a *boundary-supported effective* E with -E relatively ample for its contraction. Semiampleness itself supplies no such E. The full Griffiths-bundle theorem of BFMT 2025 supplies a contraction for that bundle, subject to its actual assumptions; it must not be silently identified with the earlier augmented bundle.

**Proposition 4.2 (generic immersion is insufficient).** Start with a smooth quasi-projective surface U_0 carrying a polarizable integral VHS with a generically immersive period map, and a smooth projective SNC compactification (X_0,Z_0). Blow up a point p in U_0, write pi:X->X_0, set Z=pi^{-1}Z_0, and pull the VHS back to U=X minus Z. Its period map remains generically immersive. Nevertheless, for every choice of boundary coefficients and every m, mL-sum a_i Z_i has degree zero on the exceptional curve F, provided L is the canonical extended Hodge line bundle.

**Proof.** The pulled-back family is smooth in a neighborhood of F, its period map is constant on F, and its Hodge line bundle is the pullback of the original one there. Hence L.F=0. Since F lies over an interior point, it is disjoint from Z, so Z_i.F=0. The asserted degree zero follows. An ample line bundle has positive degree on F. Off F the blowup is an isomorphism, preserving generic immersion. This construction applies, for example, to the direct sum of the two universal weight-one VHS on a product of fine modular curves with full level N>=3. Choose their smooth modular compactifications before blowing up. Their cusp monodromies are unipotent. QED.

This is a counterexample only to replacing the target's everywhere fibrewise logarithmic injectivity by generic injectivity. It is not a counterexample to problem 30004494: along F its ordinary differential has a kernel, hence the required logarithmic differential is not fibrewise injective. An injective morphism of locally free *sheaves* need only be generically injective; the source's local Torelli condition is the stronger injectivity on bundle fibres.

**Proposition 4.3 (stability under an allowed boundary blowup).** Suppose m_0 L-E is ample with E effective integral and supported on Z. Let pi:X'->X be the blowup of a smooth center contained in Z; assume X' is smooth and the reduced total boundary Z' is SNC. Let F be its exceptional Cartier divisor. Then a fixed effective integral E' supported on Z' exists such that m pi^*L-E' is ample for all sufficiently large m, provided L is nef.

**Proof.** O(-F) is pi-ample. For a sufficiently large integer k, k pi^*(m_0L-E)-F is ample. Write E'=k pi^*E+F. Pullback of an effective Cartier divisor is effective here, and all its components, as well as F, lie in Z'. Hence E' has the desired support and nonnegative integer coefficients. The ample divisor is km_0 pi^*L-E'. Since pi^*L is nef, add (m-km_0)pi^*L for every m>=km_0. QED.

A positive result after modifying X does not descend to the original fixed boundary without further argument. Conversely, even pullback of an ample line bundle alone fails ampleness on exceptional curves; the exceptional correction in this proposition cannot be omitted.

## 5. Finite cone algorithm and sharp dual obstruction

**Theorem 5.1.** Suppose C is generated by finitely many nonzero numerical curve classes r_1,...,r_s and L is nef. Let J={j:L.r_j=0}, and let B be the matrix B_ji=Z_i.r_j for j in J. There exist fixed a_i>=0 in Z with mL-sum a_i Z_i ample for all sufficiently large m if and only if the rational strict system Ba<0, a>=0 is feasible. When J is empty, E=0 suffices. Rationality means that the r_j have been chosen rational, as in a rational polyhedral cone.

**Proof.** Necessity follows by evaluating an ample class on each null generator. For sufficiency choose rational feasible a and clear denominators. For each non-null generator require m>(Ba)_j/(L.r_j), interpreting B here as the full intersection matrix. There are finitely many such requirements. On null generators -Ba is already positive. Every nonzero class in C is a nonnegative combination of generators, so the resulting class is strictly positive on C minus {0}. Kleiman gives ampleness. QED.

A dual certificate of impossibility is a nonzero y>=0 such that B^T y>=0. If Ba<0 and a>=0, then y^TBa<0 while (B^Ty)^T a>=0, a contradiction. Conversely such a certificate exists whenever Ba<0, a>=0 is infeasible. To see this rigorously, scaling shows that strict feasibility is equivalent to Ba<=-1 with a>=0. Introduce a nonnegative slack vector s to write Ba+s=-1. The cone generated by the columns of B and the identity is a closed polyhedral cone. If it does not contain -1, the separating-hyperplane theorem gives y with y^T B>=0, y>=0, and y^T(-1)<0; thus y is nonzero. Conversely the preceding dot-product contradiction excludes feasibility. This also proves the real alternative; rational feasible solutions exist by density with zero coordinates held fixed, while rational dual certificates follow from rational polyhedral elimination.

**Simultaneity control.** Let B=[[1,-1],[-1,1]]. Each row separately admits a nonnegative a making it negative, but no single a works for both. The certificate y=(1,1) has B^Ty=0. Thus one cannot sum or glue locally successful coefficient choices without controlling their effect on the other strata. This matrix is not asserted realizable by a logarithmically immersive VHS. It is a rigorous obstruction to that proposed proof strategy, not to the conjecture.

**Higher-dimensional gap.** Hodge curvature provides nefness and positivity away from period-constant directions. Boundary extension data provides fibrewise theta-bundle relations. To use Proposition 1 one still needs one effective boundary combination E which is negative on every nonzero class in the entire closed L-null face. The source hypotheses have not been shown here to yield that common combination. There is no justification for replacing this requirement by pairwise positivity, pointwise thresholds, an ample line bundle on the period image, or a result on a different birational compactification. This is the exact unresolved step.

## Standard dependencies, not reproved here

The proofs use the Hodge index theorem and Nakai-Moishezon for smooth projective surfaces; Kodaira's lemma for a big divisor; Kleiman's closed-cone criterion; openness of the ample cone and ample-plus-nef; and relative ample twisting. These classical algebraic-geometric inputs are explicitly distinguished from the unproved higher-dimensional Hodge assertion. The code only checks exact finite arithmetic and examples; it is not a formal proof of those inputs or of the Hodge conjecture.

References: [Kleiman, *Toward a numerical theory of ampleness*](https://annals.math.princeton.edu/1966/84-3/p01); [Stacks Project, relatively ample sheaves](https://stacks.math.columbia.edu/tag/01VG); [Stacks Project, blowing up](https://stacks.math.columbia.edu/tag/01OF); [GGR 2021](https://arxiv.org/abs/2102.06310); [BFMT 2025, v2](https://arxiv.org/abs/2508.19215v2).
