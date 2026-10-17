# Independent PSD/statistical adversarial audit of original and current PR212 mathematics

**Mathematical family verdict: PASS for the exact numerical counterexample, under the declared known-mean sample convention.** No mathematical repair is required for the K4,4 construction or its tied-diagonal WMLT claim. The added equal-vertex-colored C4 mathematical statement also passes direct independent checks. This is not a priority, novelty, publication, full-package, or historical-disposition verdict.

This audit began only after exact custody/source gate acceptance. The independent mechanism was frozen before submitted proofs were read in ../psd_statistical_criteria_01/DERIVATION.md (SHA256 8c11737fce068856e50563e39529f2665a511b481bbbdb298a467ffbb188c50b). No Root mathematical derivation or other current auditor report was read. Findings below rest on this family's independently authored exact checker and quantified arguments, not on inherited reviews or another auditor's replay.

## 1. Exact input and audit scope

The two accepted Root gate files were verified by the supplied bytes/SHA256 values, followed by the two exact body ledgers. All20 original and35 current body files were independently rehashed. INPUT_REHASH.json records their native paths, sizes, and SHA256 hashes. Both full PROOF.md bodies were read, together with both distinct submitted Python programs, original/current verification receipts, and current VERIFICATION.md. Original/current mathematical Sections2–7 are byte-identical, and original/current verify.py is byte-identical.

Relevant proof pins:

- Original PROOF.md: 12506 bytes, SHA256 69ffeade6c2ee758e3c2869d9c5b7dd607c9a1b6782f7ecebfb81d0812fdb676.
- Current PROOF.md: 13266 bytes, SHA256 ae9971d5944d6a1dd7a4b7d0f19043809c7420f9f0006dc8834965e6e07250af.
- Shared verify.py: 3839 bytes, SHA256 364efab1e7c7c7b4647dfb23d5fc5c3f26c986bd00ddfb8a80351567cb264799.
- Original inherited independent_check.py: 4121 bytes, SHA256 036c125517e82473fdc526e3bee3e7e3cc6da8aa936a2c8c5c01c4cafab5a041.

Submitted programs were read but were not executed by this family. Both write beside their __file__, so changing cwd alone would not protect frozen inputs. The new independently authored standard-library checker imports no submitted source and writes only inside this owned audit folder. Its exact checks reproduce the central submitted constants and add independent open-failure certificates. No SymPy, numerical eigenvalues, Monte Carlo, or floating-point rank choices are used.

The original report's full printed pages3146–3149 were visually read before artifact exposure. For the current proof's additional C4 statement, only the specific cited primary mathematical dependency arXiv:2609.02382v1 was fetched; full PDF pages3,8,13 were visually read to verify model/sample conventions, Proposition3.9, and Proposition3.26. This was a mathematical dependency check, not a priority search. Its factor2 edge-statistic convention is an invertible coordinate change from the report's single edge sums. The C4 conclusion below is independently proved without relying on its generic-completion-rank converse. DEPENDENCY_SOURCE_PINS.json records the specific downloaded source hash; the PDF and rendered images are excluded from the finite authored seal.

## 2. The exact statistical criterion used

Let A be the report's projection: sums of diagonal entries within vertex color classes and sums of s_ij within edge color classes. Let L be the concentration subspace. Under tr(KS), A*y has the vertex coefficients on its diagonal and half the edge coefficients in its off-diagonal entries. Thus im(A*)=L. In particular, replacing s11,s22 by their sum imposes K11=K22, with no averaging factor.

Because the statistic map measures the full trace and contains I in L, D=A(PSD) is closed, C=A(PD)=int(D), and the PSD separation alternative gives

 MLE fails for X iff there exists nonzero K in L intersect PSD with KX=0.

A trace-one normalization is possible. The equivalence follows from tr(KXX^T)=||K^(1/2)X||_F^2 and closed-cone separation. Conversely, an actual Sigma PD with A(Sigma)=A(XX^T) proves existence; maximizing logdet(K)-tr(K Sigma) on L intersect PD gives a unique maximizer. A nonzero annihilating PSD K gives an unbounded increasing likelihood ray I+tK.

For known mean, n independent N_m(mu,Sigma) observations, Sigma PD, give an m-by-n matrix X after subtracting mu. Its density is strictly positive throughout R^{mn}; the positive factor1/n in covariance does not affect cone membership. Good data form an open set. Hence one actual real Gram/PD-completion pair proves positive probability, but one bad sample alone does not prove positive-probability failure. Almost-sure conclusions below use a nonzero-polynomial exceptional set or an open neighborhood of bad samples.

The report itself does not explicitly name a mean convention on these pages. The submitted proof states the zero-mean/rank-indexed interpretation, consistent with its cited Uhler dependency's known-mean model. Under an unknown completely unrestricted mean and N observations the effective centered column count is N-1, so the numerical observation counts shift by one. Partially constrained means require a separate model-specific derivation. No unknown-mean assertion is accepted here.

## 3. Exact nonzero/zero ideal transition for BOTH K4,4 models

There are eight vertices, sixteen individually observed cross edges, and either eight singleton diagonal coordinates (d=24) or seven vertex-color coordinates after tying vertices1,2 (d=23). The graph is connected, and the tied model has a genuine vertex-color equality while retaining all singleton cross edges.

### I(G,3) is nonzero

The cross block B uses rows1–4 and columns5–8. The nonzero polynomial f=det(B), equal to1 at B=I4, is literally a defining4-minor of the generic symmetric8-by8 matrix. Replacing observed entries by their statistic variables changes this determinant by a sum of multiples of the linear statistic equations: telescope the sixteen entry replacements and use determinant multilinearity. Thus f belongs to the exact elimination ideal I(G,3), not merely to its radical or a numerical rank-fit relation. Tying diagonal colors does not change any entry of B. Therefore the same nonzero ideal certificate applies to both models.

This also confirms the distinction between all minors and principal minors: the selected cross minor is generally not principal. The submitted proof uses the correct all-minor ideal.

### I(G,4) is zero, and four observations succeed almost surely

At X4=[I4; V], where V has rows e1+e2,e2+e3,e3+e4,e4+e1, this family's independent Jacobian construction gives:

- Singleton statistic map: shape24-by32, full-row-rank square minor determinant256.
- Tied statistic map: shape23-by32, full-row-rank square minor determinant128.

Pivot columns and all exact input data are in INDEPENDENT_EXACT_CERTIFICATES.json, produced by independent_psd_exact.py using Fraction arithmetic. They agree with the submitted constants, but the matrices were reconstructed independently from the statistic definition.

Every element of the elimination ideal vanishes on the real Gram-statistic image. A full-row-rank derivative makes that image contain an open set, so no nonzero polynomial can belong to I(G,4). This proves the full zero ideal, not merely absence of a selected relation. Symmetric determinantal primeness is unnecessary for this direction.

For the statistical conclusion, let h(X) be the indicated Jacobian minor polynomial. It is not identically zero. Outside h=0 the Jacobian adjoint y -> 2(A*y)X is injective, so no nonzero symmetric K in L, in particular no PSD K, annihilates X. The Gaussian probability of h=0 is zero. Thus p4=1 directly, independently of any converse between completion rank and MLT.

## 4. WMLT=2 for BOTH models: actual lift, open box, and universal lower bound

Let X2 have four rows e1 and then four rows e2. Its real PSD Gram matrix has rank2, unit diagonals, and zero observed cross block, exactly matching I8. After tying the first two diagonal statistics the match remains exact. This is an actual real PSD lift and a PD completion, not merely an algebraic zero-set intersection.

For every data matrix within coordinate distance epsilon=1/100 of X2, form M(X) by retaining the Gram diagonals and cross block and setting off-diagonal within-part entries to zero. Each diagonal is at least9801/10000 and each cross entry has absolute value at most202/10000. Each row has four such off-diagonal entries, giving the uniform strict dominance margin

 9801/10000 - 4(202/10000) = 8993/10000 >0.

For symmetric M with positive diagonal, the bound z^T M z >= sum_i (M_ii-sum_{j!=i}|M_ij|)z_i^2 proves positive definiteness. M(X) matches all singleton statistics and therefore the tied statistics. A left/right2-by2 row determinant is at least(1-epsilon)^2-epsilon^2=1-2epsilon>0, so all data in this box have rank2. Gaussian full support gives this nonempty open box positive probability. Therefore both WMLTs are <=2.

For every one-column data vector x, edge3–5 has both diagonal coordinates singleton in both models. Any matching completion has the2-by2 principal block [[x3^2,x3*x5],[x3*x5,x5^2]], determinant zero. Such a block cannot be principal in a PD matrix. This includes vanishing-coordinate boundary cases; a zero diagonal is also fatal. Therefore no one-observation sample succeeds, and both WMLTs equal2. This lower bound is universal, not almost-sure only.

At n=0 no covariance likelihood maximum exists. Consequently the smaller-sample edge cases are fully accounted for.

## 5. Independent MLT=4 for BOTH models: a robust exact rank3 PSD stress

The submission asserts MLT4 only for singleton K4,4, relying on a cited theorem. This family proves that value directly and additionally proves the tied model's unclaimed MLT4. This strengthening is an audit fact, not a novelty or publication claim.

Define rational orthogonal Householder matrices

 H=I4-(1/15)ww^T,   w=(1,2,3,4)^T,
 G=I4-(2/87)zz^T,   z=(2,3,5,7)^T.

Let U and V be the first three columns of G and H respectively, and let v be H's fourth column. Set

 X0=[U;V],  Q=UV^T,
 R=[ I4  -Q ; 0  v^T ],  W=R^T,
 K0=R^T R = [ I4 -Q ; -Q^T I4 ].

All entries are rational. Because U,V have orthonormal columns, Q^TQ+vv^T=I4. The five rows of R are independent. Therefore K0 is PSD of rank5, X0 has rank3, K0X0=0, and every diagonal of K0 is1. Its only nonzero off-diagonals are cross edges, so K0 lies in both concentration spaces, including K11=K22. Also W has five independent columns spanning ker(X0^T), and K0=W I5 W^T with I5 strictly PD.

A single such stress would not prove an almost-sure lower bound. The following exact variation ranks provide the necessary open-set argument.

Let P_s select the twelve within-part off-diagonal entries, so ker(P_s)=L_singleton. Let P_t add the thirteenth coordinate K11-K22. For symmetric5-by5 B define T_s(B)=P_s(WBW^T), and similarly T_t. In the upper-triangular B-coordinate order recorded in the certificate, exact rational elimination finds:

- T_s is12-by15 and onto; the first twelve columns have determinant469673776/28036176789375.
- T_t is13-by15 and onto; the first thirteen columns have determinant7313152/322254905625.
- T_s(I5)=0 and T_t(I5)=0.

Here is the full quantified persistence argument. For X near X0 define the orthogonal projector

 P_X=I8-X(X^T X)^{-1}X^T,   W(X)=P_X W.

For full-rank X near X0 this is rational and continuous; W(X0)=W, and W(X) stays full-column-rank while satisfying X^T W(X)=0. Replace W by W(X) in the variation map T_X. The displayed nonzero minor persists on a neighborhood, giving a continuous right inverse J_X from the selected square block. Define

 B(X)=I5-J_X[T_X(I5)].

Then T_X(B(X))=0 and B(X0)=I5. Continuity makes B(X) PD on a sufficiently small nonempty open neighborhood. Hence K(X)=W(X)B(X)W(X)^T is a nonzero PSD matrix in the relevant L, annihilating every X in that neighborhood. The exact failure criterion proves all those samples bad. This gives p3<1 for both models, with genuinely positive Gaussian probability. There is no isolated-sample inference or appeal to PSD membership from approximate eigenvalues.

Since p4=1 from Section3, both MLTs equal4. Fewer columns cannot have almost-sure success: under coupling, adding a PSD observation to a good statistic keeps it in C, so probabilities are nondecreasing with column count. Thus p3<1 rules out MLT1,2,3. Combined with Section4:

 singleton K4,4: (WMLT,MLT)=(2,4),
 tied-diagonal K4,4: (WMLT,MLT)=(2,4).

The final certificate follows a transparent failed-search boundary: the auxiliary choice U=[e1,e2,e3] supplied singleton transversality but not tied transversality. That first construction was inconclusive for the tied lower bound. The independently selected rational G above resolves it. No failed rank test was presented as negative evidence about the mathematical claim.

## 6. The report's intersection and signed-SOS alternatives

I8 has the same statistics as a real rank2 PSD matrix, so every polynomial in I(G,3) vanishes at A(I8). Hence the positive-definite intersection antecedent is truly satisfied. Any generator or any other ideal polynomial also vanishes after the full positive-diagonal Cholesky substitution at L=I8. Therefore none can be everywhere nonvanishing on that domain, regardless of whether it has a signed SOS representation.

At the adjacent ideal transition n=3, WMLT is2 rather than3 or4. This disproves the literal universal numerical threshold classification and specifically its second bullet's lower-bound inference. The construction already satisfies the second algebraic mechanism, so it does not refute the bare Boolean claim “strict signed-SOS separator or PD intersection.” This qualification is correct in both proof versions. The K4,4 construction itself does not decide a four-cycle-only interpretation.

No inference from I(G,3) nonzero to p3<1 was used: Section5 supplied an independent open bad set. No inference from rank3 success to absence of rank2 success was used: rank2 success is explicitly exhibited.

## 7. Direct audit of the current added equal-vertex-color C4 mathematical statement

Take edges12,14,23,34, each its own edge color, and give all four vertices one color. The report's statistics are

 A(S)=(tr(S),s12,s14,s23,s34),

and every concentration matrix has a common diagonal a. Reorder vertices into parts(1,3),(2,4). Then K=[aI2,B;B^T,aI2].

### I1 nonzero and I2 zero

The observed2-minor f=s12*s34-s14*s23 is a defining minor at rank at most1, and it is a nonzero polynomial in the four edge statistics. Thus I1 is nonzero by exact ideal membership. At the real two-column data rows(1,0),(0,1),(1,1),(1,2), this family's5-by8 Gram-statistic Jacobian has a square minor from its first five columns of determinant -2. Thus I2=0 by the same open-image argument. The adjacent full elimination-ideal transition is verified directly; Proposition3.9 is not needed as an unverified bridge.

### Almost-sure MLT1, not a numerical approximation

Write a one-column sample as x=(u,v) in the bipartition order. If Kx=0, the two block equations give

 a||u||^2+u^T Bv=0,
 a||v||^2+u^T Bv=0.

Therefore a Delta(x)=0, where Delta=x1^2+x3^2-x2^2-x4^2. This polynomial is nonzero (Delta(e1)=1), so it vanishes with Gaussian probability zero. Outside its zero set a=0; PSD then forces every row and column of K to vanish, because a PSD matrix with zero diagonal is zero. Thus no nonzero PSD stress exists almost surely and MLT=1. With thresholds defined for positive sample counts, this also gives WMLT=1.

An actual one-column completion witness is x=e1 and Sigma=I4/4; both have trace1 and all edge statistics zero. This is another true PD intersection, so this C4 example also refutes a numerical MLT=2 conclusion without refuting the bare mechanisms alternative.

For completeness, the exceptional set is not ignored: if ||u||=||v||=r>0, choose a=1 and B=-uv^T/r^2, whose operator norm is1, producing a PSD stress. If r=0, x=0 and K=I works. Hence the bad set is exactly Delta=0, a lower-dimensional hypersurface, not an open set. This checks the boundary and limiting cases behind the almost-sure claim.

The specifically cited Homs–Kuznetsova–Stolz v1 Proposition3.26 states the same even-cycle MLT1 and generic completion rank2; the displayed C4 model and its known-mean normalization agree with the current text. The independent proof above verifies precisely the C4 consequence used here. No assertion about first discovery, earlier publication priority, or current status already_solved is accepted by this family.

## 8. Coverage, gaps, and disposition

All principal mathematical claims in original/current Sections2–7 pass: model/color normalization; true real lifts; full zero/nonzero adjacent ideals; WMLT2 with a positive-probability success box and a universal one-column obstruction; PD-intersection antecedent; impossibility of a globally nonvanishing separator; exact singleton MLT4; correct distinction between the literal numerical classification and the bare mechanisms question. The additional current C4 mathematical route passes independently too. The tied model's exact MLT4 has also been verified, although neither submitted proof claims it.

The strongest verified result is the collection of exact ideal/threshold certificates above. There is no remaining mathematical gap for the literal numerical counterexample under the stated convention. The bare SOS/intersection conjecture remains unresolved by these examples, exactly as the current proof says. Historical credit and priority assertions are outside this gate and are neither accepted nor rejected. Full future package/manifest/review sequencing is outside this mathematical family task.

Operational restrictions were respected: no Git, network mutation, provider/PR/ref/tracker writes, original-lock/global-five changes, outreach, or other-chat communication. The only fetched material was a named primary mathematical dependency. No submitted program or frozen body was modified. A final all55-body rehash verifies that preservation.

Completion estimate:100% of the assigned original/current PSD mathematical family audit. This does not mean completion of Root's overall research/publication workflow or a solution of the bare mechanism conjecture.
