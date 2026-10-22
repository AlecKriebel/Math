# Independent interface verification

Scope: the authenticated frozen `source_question_family` reconstruction only. This document was written without reading the submitted candidate or any other review. It verifies mathematical sufficiency, not priority or novelty.

## 1. Exact target and the filtration

The target is: for every fixed closed oriented genus g >= 2, every fixed finite k >= 3, and every N >= 1, there are at least N ambient orientation-preserving Mod_g conjugacy classes of pseudo-Anosovs in I_g(k) with the same dilatation. The common value may depend on N. Powers are allowed.

The independently fetched original question confirms the outer-automorphism convention with pi_j = gamma_{j+1}(pi), and I_g(1) equal to Torelli. It also supplies the separating filling-pair assertion. See [F], printed pp.14,49-51, PDF pp.21,56-58: [author-hosted source](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

Here is the indexing check without importing a different Johnson convention. For alpha trivial on pi/pi_k, induction on j gives alpha(z) z^-1 in pi_{k+j} for z in pi_j. At the induction step [pi_k,pi_j] and [pi_0,pi_{k+j}] both lie in pi_{k+j+1}. This proves the statement for commutator generators of pi_{j+1}; their products and inverses preserve it.

For alpha in A(k), beta in A(l), write alpha(x)=xu and beta(x)=xv, with u in pi_k and v in pi_l. Mod pi_{k+l}, alpha beta(x)=xuv and beta alpha(x)=xvu, and [pi_k,pi_l] is contained in pi_{k+l+1}. Thus [A(k),A(l)] is contained in A(k+l). An outer class trivial on the quotient has a representative inducing an inner automorphism there. Lift its conjugating element through the surjection pi -> pi/pi_k, then compose with the inverse inner automorphism. This produces a representative in A(k). Applying the automorphism calculation and projecting to Out proves [I_g(k),I_g(l)] <= I_g(k+l). No preservation of selected lifts under brackets is needed.

A separating twist lies in I_g(2): choose a basepoint on one side and a representative fixing that side. It conjugates generators on the other side by the separating boundary word, which lies in gamma_2(pi). Its change on those generators therefore lies in gamma_3(pi)=pi_2. This also works in genus 2.

## 2. Separating curves, matrices, and depth

The existence assertion has an independent standard check. For a separating essential a and any pseudo-Anosov f, suppose arbitrarily large n admitted an essential curve e_n disjoint from both a and f^n(a). Normalize the measured curves and pass to a nonzero projective measured-lamination limit e. Continuity of intersection and north-south convergence give i(e,a)=i(e,lambda_+)=0. Since lambda_+ is filling and uniquely ergodic, the latter forces e proportional to lambda_+, contradicting its positive intersection with a. Thus a and f^n(a) fill for sufficiently large n; both remain separating. This argument has no genus-2 exception.

For a filling pair in minimal position, V=mu, E=2mu and the number F of complementary disks is mu+2-2g >= 1. Separating curves have zero mod-2 intersection, so mu is even. Hence mu >= 4 for g >= 2. No assertion that 4 is attainable or minimal is used.

The rectangle matrices, their parameter mu=i(a,b) for a single pair, and freeness at mu>2 agree with [L], section 5 and Lemma 6.3, printed pp.1319-1326, PDF pp.19-26: [publisher source](https://msp.org/gt/2004/8-3/gt-v8-n3-p10-s.pdf). In particular the lower-left entry of the second generator has the negative sign used in the frozen calculation. Freeness of the two matrix generators also proves faithfulness of the two-twist subgroup: a relation among its generators would give a relation in the free matrix group.

There is a direct full-matrix expansion. For C=(p,q;r,s), ps-qr=1, and B=(1,0;-mu,1),

    [B,C] = (1+mu*q*s,                 -mu*q^2;
              mu*(s^2-1)-mu^2*q*s,     1-mu*q*s+mu^2*q^2).

Its trace is 2+mu^2*q^2. Starting from q=mu gives q_r=-mu^(2^r-1) and trace(c_r)=2+mu^(2^r) for r>=2. Thus these are nontrivial hyperbolics. The centrality result gives c_r in I_g(2r), and r=max(2,ceil(k/2)) puts c_r in the specified I_g(k). The group and filtration term are fixed before N varies.

The q!=0 test is precisely what excludes the parabolic fixed point 0 from the fixed-point set of C. In the upper half-plane coordinate, B^M(z)=z/(1-M*mu*z); each z!=0, including infinity, converges projectively to 0 as |M| grows. Both endpoints of C therefore move into a small neighborhood of 0 disjoint from its original two endpoints. They stay distinct because B^M is a projective bijection. This supplies an M for which c and B^M c B^-M have disjoint fixed-point sets. Normality preserves membership in the same I_g(k).

## 3. Why high powers give compact convex core

Merely saying that the two elements do not commute would be insufficient here. The four distinct endpoints permit four disjoint small closed boundary intervals. Choose a repelling geodesic half-plane for each generator in its repelling interval. For sufficiently large common L, its image of the complementary half-plane is an attracting half-plane inside the corresponding attracting interval. These four half-planes have pairwise disjoint closures, including ideal endpoints.

The side-pairing region outside them is a classical Schottky fundamental region. Ping-pong proves that the prescribed generators are a free basis. Cyclically reduced nontrivial words have an attracting and a repelling interval separated from one another, so they are hyperbolic. This rules out elliptic and accidental parabolic words.

Compactness of the convex core follows from the same strict separation, rather than from an unproved identification of pure hyperbolicity with compactness. In the fundamental region, the ideal boundary misses the limit set: every first-letter limit cylinder lies strictly inside its corresponding interval, by applying its generator to the other three separated cylinders. The closure at infinity of the convex hull is exactly the limit set. Consequently the intersection of the closed fundamental region with that hull has no ideal accumulation point and is compact. Its translates cover the hull. This produces the compact set K required in the next step.

Since the derivative images of the chosen generators freely generate, their lifts freely generate H and the derivative is injective on H. All nonidentity elements are pseudo-Anosov by the disk theorem. No finite-index assumption about this subgroup or about the original two-twist group has entered.

## 4. The compact-core lemma with quantifiers exposed

Let J <= G <= PSL(2,R), with G discrete and J convex cocompact, and let X be the closed convex hull of Lambda(J) in H^2. Compactness of X/J gives a compact K with JK=X: take finitely many relatively compact metric neighborhoods projecting onto a cover of the quotient and take their closures. The properness of H^2 makes this construction valid even when X has boundary.

Set S={s in G: sK intersects K}. Fix o in H^2 and choose R with K contained in the R-ball about o. Every s in S satisfies d(o,so)<=2R. The set of orientation-preserving isometries satisfying this bound is compact, since the stabilizer of o is compact. Its intersection with the discrete subgroup G is finite. This proof requires no finite generation of G.

For a hyperbolic u in J, the entire axis lies in X because its endpoints are in Lambda(J). Choose one point on it, move that point into K by a J element, and replace u by the corresponding J conjugate. **From this moment keep this one u and this one x in K fixed for every ambient conjugator.** This is the crucial quantifier order.

For each v=tut^-1 in J, tx lies on the axis of v, hence lies in X. Choose j in J with jtx in K. Then s=jt lies in the same fixed finite S and jvj^-1=sus^-1. Each J class in the ambient G class thus has a representative on the finite list indexed by S. Some entries on that list might not belong to J; discarding them only improves the bound.

The bound |S| is uniform in u. The reference point x depends on u, but neither K nor S does. No axis segment, period, word-length bound, or translation-length bound is used. Proper powers have the same axis and cause no change. Centralizers need not be counted, and arbitrary choices of conjugator do not enlarge S. Torsion in G is harmless because point stabilizers in a discrete Fuchsian group are finite.

### An explicit failure if compactness is dropped

Let G=<a,b> be a classical rank-two Schottky group and let Q=ker(phi), where phi(a)=0, phi(b)=1 maps G onto Z. Set u_n=b^n a b^-n. Every u_n belongs to Q and to a single G-conjugacy class of hyperbolic elements. If h in Q conjugated u_n to u_m, then b^-m h b^n would centralize a. The centralizer of the free generator a is <a>. Applying phi therefore gives n-m=0. Thus all u_n, n in Z, represent distinct Q-conjugacy classes.

This Q is not convex cocompact. Its covering graph of the two-petal rose is a bi-infinite b-line with an a-loop at each integer, giving the infinite Schreier basis {u_n}. A convex-cocompact action on a proper convex space has a finite generating set from translates of a compact core; Q is infinitely generated. The frozen proof avoids exactly this counterexample by passing to its finitely generated Schottky subgroup before comparing conjugacy.

Discreteness is also essential to the given proof: if G were not discrete, the compact isometry set above could intersect it infinitely. The actual overgroup is discrete by the full disk-stabilizer theorem, so this altered hypothesis creates no gap.

## 5. Passing through every ambient mapping class

[L], Theorems 3.1-3.2, printed pp.1314-1315, PDF pp.14-15, gives the discrete full-stabilizer derivative image, finite kernel, uniqueness of a pseudo-Anosov's stabilized disk, and lambda=exp(L/2). These were inspected as complete pages and visually checked. The homology statement in Proposition 3.4 concerns square differentials; the main proof does not apply that hypothesis to the separating-twist disk.

If zfz^-1=h for nonidentity f,h in H, then h stabilizes D because h is in H and stabilizes z(D) because f stabilizes D. Uniqueness forces z(D)=D. This works for every orientation-preserving ambient mapping class z, not only for affine maps selected in advance. Its derivative therefore lies in the specified full group G.

Injection on H identifies H-conjugacy classes exactly with J-conjugacy classes: a conjugator in J lifts to an element of H, and equality of its conjugated images lifts by injection. Ambient Mod_g conjugacy implies G conjugacy. Therefore each ambient class contains at most |S| of the H classes. A nontrivial finite kernel on the larger stabilizer cannot invalidate this implication or collapse extra H classes within J. No assertion of ambient derivative faithfulness is made.

## 6. Universal traces and normalization

[H], Example 8.2, printed pp.648-649, PDF pp.14-15, has the frozen recurrence with exponents 2j and 2j-1; the exponent is linear in j. Its character convention is universal over representations, not equality in a selected Fuchsian group. The rank-two polynomial input is Theorem 3.1/Corollary 3.14, printed pp.638-641: [primary paper](https://www.math.purdue.edu/~eremenko/Pdf/horowitz.pdf).

An independent nonconjugacy check uses the cyclic form U^epsilon y^(2m-1) U^-epsilon y^(4m), with U=W_(m-1). The unique positive odd marker anchors the cyclic comparison; the unique closing marker separates its U blocks. Equality recovers U^epsilon. The absence of the opposite odd marker in U distinguishes its inverse for m>1; m=1 uses x!=x^-1. Induction recovers the signs. Thus there really are 2^m H classes, before ambient fusion.

For the trace check, tr(U^-1 y U y)=tr(U y U^-1 y) by cyclicity, and each conjugated y has trace tr(y). The two generator pairs therefore have identical rank-two trace coordinates. Expressing every later word in those pairs and flipping one sign at a time proves the universal identity. This does not infer universality from finitely many evaluations.

The free derivative representation lifts by freely choosing SL(2,R) lifts of its two basis elements. Universal equality holds for this chosen lift, including either sign choice of each generator. All words are nonidentity and hyperbolic in the actual Schottky representation, so their common absolute trace exceeds 2. The usual curvature-minus-one hyperbolic formula is ell=2 arcosh(|tr|/2); the disk theorem gives log(lambda)=ell/2. Equal exact trace therefore gives equal exact positive dilatation. The degenerate representations in the controls deliberately yield trace 2 and show why trace equality alone would not prove hyperbolicity.

Finally choose m so 2^m >= |S| N. Division by the uniform fusion bound yields N ambient classes at one value. Neither the Johnson depth nor H changes. The proof establishes unbounded finite multiplicity families, with no common value required across all m, no ambient primitivity conclusion, and no intersection-of-all-depths conclusion.

## 7. Computational scope

The frozen script was executed on an ignored copy and reproduced its recorded output byte for byte. The separate authored `adversarial_checks.py` tests 750 general determinant-one commutator cases, including rational/negative parameters and q=0; cyclic marker and conjugacy checks through m=6 (64 classes); and trace checks through m=4 in seven representations, including trivial, commuting, rational diagonal, and all generator-lift sign changes. All pass. These computations check finite consistency and test altered hypotheses; the preceding symbolic and geometric arguments carry the infinite quantifiers.

One initial control implementation incorrectly counted the first and last y runs separately in a cyclic word. Rotating the word to begin in x before counting syllables corrected that verifier-only issue. It exposed no failure of the frozen proof.
