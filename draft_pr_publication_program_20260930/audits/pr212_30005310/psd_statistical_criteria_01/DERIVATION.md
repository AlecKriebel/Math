# Independent PSD and statistical criteria: pre-artifact freeze

Family: PSD duality, positive definite completion, Gram projection, and real probability.

Status: independently derived before seeing any submitted PR212 proof, counterexample, audit, or script. No submitted result has been accepted or rejected. This document freezes the mechanism, certificate requirements, and gaps for the later audit. Authored 2026-10-17; initial freeze timestamp appears in RESEARCH_LOG.md.

## 1. Source custody and question interpretation

Original source: Roser Homs, joint work with Olga Kuznetsova, “Weak maximum likelihood threshold of colored Gaussian graphical models,” in *Algebraic Structures in Statistical Methodology*, Oberwolfach Report 55/2022, DOI [10.4171/OWR/2022/55](https://doi.org/10.4171/OWR/2022/55). Official PDF: <https://ems.press/content/serial-article-files/46992?nt=1>. Printed pages 3146–3149 were read in full as actual local PNG pixels. They are PDF zero-indexed pages 25–28, one-indexed pages 26–29. These include adjoining text from other contributions, all figures, Proposition 3, and Conjecture 4. Text-only web screenshot outputs were not treated as visual reading.

Source summary (paraphrase, not an assumption of correctness): the report defines colored concentration matrices by graph zeros and within-color equalities, and uses sums over vertex and edge color classes as sufficient statistics. It defines I(G,n) by eliminating symmetric matrix entries from the rank-at-most-n minor ideal plus the statistic equations. Its Theorem 2 gives the sufficient condition I(G,n)=0 for almost-sure MLE existence. Proposition 3 assumes I(G,n+1)=0 and I(G,n) nonzero and gives two asserted threshold outcomes, based respectively on a nonvanishing signed SOS after a full positive-diagonal Cholesky substitution, or a positive definite covariance whose statistics lie in V(I(G,n)). Conjecture 4 says those two cases exhaust the possibilities. The report's rank-n PSD completion discussion, not algebraic closure alone, supplies the relevant statistical question.

Dependency source, checked only for assumptions and the elimination criterion: Caroline Uhler, *Geometry of maximum likelihood estimation in Gaussian graphical models*, Annals of Statistics 40 (2012), 238–261, DOI [10.1214/11-AOS957](https://doi.org/10.1214/11-AOS957), primary author preprint <https://arxiv.org/pdf/1012.2643>, version shown in PDF: arXiv:1012.2643v2, 29 May 2012. Full PDF pages 2, 3, and 7 were visually read. The paper explicitly assumes known mean, specializes to mean zero, and defines covariance as n^{-1} sum_i X_i X_i^T. Theorem 3.3 is a one-way sufficient criterion. Its discussion explicitly requires analysis of polynomial inequalities when the ideal is nonzero. No historical novelty/priority conclusion is drawn.

Source files, hashes, and actual inspected page numbers are in source_pins.json. The primary report alone determines interpretation of its Conjecture 4. Uhler is used only for a dependency and the sample-mean convention.

## 2. Exact model and normalization

Let m>=1. Let V_1,...,V_r be a partition of all vertices and E_1,...,E_s a partition of the graph's edges, each class nonempty. Set d=r+s. Work over the real symmetric matrices Sym_m, with inner product <K,S>=tr(KS). The report's linear map A=pi_G is

A_i(S)=sum_{a in V_i} S_aa,
A_{r+j}(S)=sum_{{a,b} in E_j} S_ab.

Let L be the real linear space of symmetric matrices with graph zeros and equality within each vertex or edge color class. Then I_m belongs to L. The coordinates of A are linearly independent (disjoint nonempty supports), so A is onto R^d.

Important factor of two: if y=(a_1,...,a_r,b_1,...,b_s), the adjoint K=A* y has K_aa=a_i for a in V_i, and K_ab=b_j/2 for {a,b} in E_j. Therefore <A*y,S>=y dot A(S) and im(A*)=L. One can instead use edge coordinates 2 A_{r+j}; that is an invertible coordinate change, but it must be applied consistently to ideals, adjoints, and certificates.

Define

D=A(Sym_m^{PSD}),  C=A(Sym_m^{PD}),
Q_n={ A(XX^T): X in R^{m x n} }.

C is a full-dimensional open convex cone. D is closed in this particular model: if A(S_k) converges and S_k is PSD, then tr(S_k)=sum_{i=1}^r A_i(S_k) is bounded. The PSD matrices S_k are bounded, and a subsequence converges to a PSD preimage. Moreover D=closure(C), by replacing any S by S+epsilon I_m. We also have C=int(D): if t is interior to D, choose epsilon>0 such that t-epsilon A(I_m) belongs to D and add epsilon I_m to a PSD preimage. The reverse inclusion follows because a surjective linear map is open.

Q_n is also closed: a convergent sequence A(X_k X_k^T) has bounded trace, hence bounded Frobenius norm of X_k, and therefore a convergent subsequence in the fixed finite-dimensional data space. Closedness of these images uses the measured trace. It must not be borrowed for an arbitrary PSD-cone projection that does not control trace.

For n=0, Q_0={0} and no covariance MLE exists for m>=1. For n>=m, a full-row-rank real X gives XX^T PD and hence good statistics. Gaussian X has full row rank almost surely. Thus both thresholds are <=m under the known-mean convention.

## 3. PSD alternative and exact MLE criterion

For t=A(S) with S PSD, the following statements are equivalent:

1. t belongs to C.
2. There is Sigma_0 PD with A(Sigma_0)=A(S).
3. tr(KS)>0 for every nonzero K in L intersect PSD.
4. There is no K in L intersect PSD with tr(K)=1 and tr(KS)=0.

Proof: D* consists exactly of y with A*y PSD, since y dot A(S)>=0 for all PSD S iff A*y is PSD. Since D is closed and full dimensional, a point t in D fails to be interior exactly when it has a nonzero supporting dual vector y with y dot t=0. A* is injective, so this is equivalent to a nonzero PSD K in L orthogonal to S. Normalize its positive trace to one.

For S=XX^T,

tr(KS)=tr(X^T K X)=||K^{1/2}X||_F^2.

Thus tr(KS)=0 iff KX=0. In particular:

  BAD_n(X) iff exists K in L, K PSD, tr(K)=1, KX=0.
  GOOD_n(X) iff exists Sigma_0 PD, A(Sigma_0)=A(XX^T).

These are exact real feasibility statements. K may depend on X. An arbitrary nonzero symmetric K in L with KX=0 is not enough: it must be PSD (or negative semidefinite, after changing sign). Indefinite null directions establish Jacobian rank deficiency but not likelihood failure.

One can also derive the likelihood statement directly. For K PD in L, take ell(K)=log det(K)-tr(KS), omitting a positive sample-size factor. If Sigma_0 as above exists, ell(K)=log det(K)-tr(K Sigma_0). With Sigma_0>=epsilon I, the upper bound sum_i [log lambda_i(K)-epsilon lambda_i(K)] prevents escape to infinity; the logarithm prevents approach to the PD boundary on bounded sets. A superlevel set is compact inside L intersect PD, so a maximum exists. Strict concavity of log det gives uniqueness. Conversely, a PSD stress K_0 with K_0 S=0 gives ell(I_m+t K_0)=log det(I_m+tK_0)-tr(S), which tends to infinity as t tends to infinity. Thus no maximum exists. This direct proof avoids an unverified exponential-family dependency for the criterion above.

For finite exact verification, PSD can be expressed by nonnegativity of all principal minors; PD can be expressed by positivity of all leading principal minors. Exact LDL^T or a supplied Gram factor gives shorter PSD/PD certificates when available. Approximate eigenvalues near zero alone do not certify either condition.

## 4. Data distribution, mean, and sample count

Use n independent observations from N_m(mu,Sigma), with mu known and Sigma PD. Subtract mu and arrange observations as columns of X in R^{m x n}. The usual covariance is S=(1/n)XX^T. Because C is a cone, the factor 1/n has no effect on existence, so the preceding formulas use XX^T. The Gaussian distribution of X has a strictly positive density everywhere in R^{mn}. Therefore null, positive, and full probability of a fixed measurable data event depend only on its Lebesgue measure, not on the chosen PD Sigma. The numerical probability need not be independent of Sigma.

The report itself does not explicitly state the mean convention on these four pages; interpreting its n observations as rank at most n is consistent with the known-mean convention confirmed in its cited Uhler dependency. No unknown-mean result should be silently inferred.

If the mean is unknown and completely unrestricted, maximize first over mu to get the sample mean. For N original observations let H=I_N-(1/N)11^T, and choose Q in R^{N x (N-1)} with orthonormal columns spanning 1-perp. Then H=QQ^T and ZHZ^T=(ZQ)(ZQ)^T. The columns of ZQ are independent N_m(0,Sigma) under Gaussian sampling. Thus the relevant effective column count is n=N-1, and the covariance divisor N is irrelevant to cone membership. A mean constrained by color classes, partially known, or jointly constrained with covariance requires a separate derivation; there is no automatic universal sample-size shift for those models.

For n<=m, X has column rank n almost surely. A witness with smaller rank still proves positive probability for n columns because GOOD_n is open and contains nearby full-rank X. If exact WMLT=n is claimed, such a lower-rank witness can instead provide evidence that the claimed lower bound needs checking.

## 5. Probability and threshold certificates

Let p_n=P(GOOD_n(X)) for a Gaussian X with n columns. The good set is the inverse image of the open set C under the continuous polynomial q_n(X)=A(XX^T), hence is open. The bad set is closed. Both are semialgebraic: the feasibility predicates above use polynomial equalities/inequalities and real existential quantification.

Consequently:

(A) p_n>0 iff GOOD_n is nonempty iff Q_n intersects C. One actual real Gram/PD-completion pair is necessary and sufficient for the positive-probability assertion.

(B) p_n=0 iff GOOD_n is empty. Thus a verified universal failure for rank at most n is equivalent to zero probability; it is stronger than a single failure example.

(C) p_n<1 iff BAD_n has positive Lebesgue measure. Since it is semialgebraic, this is equivalent to BAD_n having nonempty Euclidean interior. A single boundary data point does not establish p_n<1. A certified open ball of bad data, or an exact PSD-stress construction valid on a specified nonempty open data set, does.

(D) p_n=1 iff BAD_n has dimension less than mn, equivalently no full-dimensional semialgebraic piece. A useful sufficient certificate is a nonzero polynomial h(X) and a proof that h(X)!=0 implies GOOD_n(X). Nonzero-polynomial zero sets have Gaussian probability zero. An exact real quantifier-elimination proof that BAD_n has no interior is also valid. The equivalence between zero measure and empty interior here uses the standard semialgebraic cell/dimension theorem; it does not hold for arbitrary closed sets.

These events are monotone in sample count under coupling: if X is good and one adds a column z, then A(XX^T+zz^T) belongs to C+D, which is contained in C. Thus p_{n+1}>=p_n. Define WMLT=min{n>=1:p_n>0} and MLT=min{n>=1:p_n=1}.

Exact threshold claims require both sides:

- WMLT=n: an actual real n-column good witness, plus universal failure at n-1 (unless n=1, where the n=0 case is automatic).
- MLT=n: an almost-sure good certificate at n, plus a positive-measure bad certificate at n-1.
- WMLT=MLT=n+1: universal failure at n, plus an almost-sure good certificate at n+1.
- WMLT=n<MLT=n+1: actual good n-column witness, universal failure at n-1, positive-measure bad n-column certificate, and an almost-sure good certificate at n+1.

For positive-probability existence a rational exact certificate is available in principle whenever a real witness exists. The good data set is nonempty open, hence contains rational X. For rational A and rational X, rational symmetric matrices are dense in the affine fiber A(Sigma)=A(XX^T): use a rational linear right inverse of A to correct a rational approximation. Therefore one can choose rational Sigma_0 PD as well. It is enough to publish rational X, rational Sigma_0, the exact statistic equality, and an exact PD certificate. No numerical probability estimate is necessary to prove positivity.

### 5.1. A finite robust PSD-stress certificate for MLT lower bounds

The following sufficient condition turns one bad sample into a proof of positive-probability failure. It is not claimed necessary.

Assume 1<=n<m and write k=m-n. Supply an exact full-column-rank X_0 in R^{m x n} and a basis V_0 in R^{m x k} for ker(X_0^T). Supply B_0 PD in Sym_k with

 K_0=V_0 B_0 V_0^T in L.

Thus K_0 is PSD, has rank k, and annihilates X_0. Let P be any linear quotient map Sym_m -> Sym_m/L, represented by exact linear forms that vanish exactly on L. Define

 T_0: Sym_k -> Sym_m/L,  B -> P(V_0 B V_0^T).

Require T_0 to have full row rank, i.e. to be onto. This is an exact matrix-rank certificate. Equivalently, L+{V_0 B V_0^T:B in Sym_k}=Sym_m.

Proof of robustness: after permuting rows choose an invertible n-by-n top block A_0 of X_0. Nearby X has block form [A;D] and a continuously varying, rational nullspace basis V(X)=[-A^{-T}D^T; I_k]. Replace V_0 by this basis if necessary, transforming B_0 by congruence. Let T_X(B)=P(V(X)B V(X)^T). A nonzero full-row-rank minor of T_0 persists nearby. Fix its column selection and invert that square block to obtain a continuous right inverse R_X of T_X. Put

 B(X)=B_0-R_X[T_X(B_0)].

Then T_X(B(X))=0, B(X_0)=B_0, and B(X) remains PD near X_0. Therefore K(X)=V(X)B(X)V(X)^T is a nonzero PSD matrix in L annihilating X for every X in a neighborhood of X_0. This neighborhood is BAD_n, proving p_n<1 and MLT>=n+1. Normalizing tr(K(X)) to one is harmless.

Every premise is finite and exactly checkable: rank of X_0; X_0^T V_0=0; PD of B_0; color/zero equalities for K_0; and a nonzero determinant for a full-row-rank minor of T_0. If all inputs are rational, all checks use rational arithmetic. This certifies existence of an open bad neighborhood without relying on a numerical Monte Carlo frequency or an isolated stress. When this sufficient rank condition fails, the route is inconclusive; another robust family or exact semialgebraic argument can still establish a lower bound.

### 5.2. Explicit openness of a good completion

An actual good pair (X_0,Sigma_0) also has a constructive persistence proof. Fix a linear right inverse R_A of A, and define

 Sigma(X)=Sigma_0+R_A[A(XX^T)-A(X_0 X_0^T)].

This matches the nearby data statistics exactly and equals Sigma_0 at X_0. Positive definiteness persists in a neighborhood. This gives a direct positive-probability proof and identifies exactly which strict inequality must survive an approximate-to-exact reconstruction.

## 6. Elimination, Gram maps, and real versus complex arguments

Let J_n be exactly the ideal in the report: statistic equations t_i-A_i(S) and all (n+1)-minors of the generic symmetric S. Let I_n=J_n intersect R[t_1,...,t_d]. It is crucial to distinguish:

- Q_n, the actual projected real PSD Gram image;
- the real zero set V_R(I_n);
- the complex zero set V_C(I_n), or the Zariski closure of a complex projection;
- C, a real open cone defined by positive definite feasibility.

Always Q_n is contained in V_R(I_n) intersect D. This inclusion follows by direct substitution, without any radicality theorem. Equality with V_R(I_n) intersect D or with V_R(I_n) intersect C must not be assumed. Elimination can forget inequalities, signatures, and real lifting. Even complex image membership is stronger than membership in its Zariski closure.

A precise finite certificate for I_n nonzero is a nonzero polynomial f(t) and an exact identity

 f(t) = sum_i a_i(t,S)[t_i-A_i(S)] + sum_M b_M(t,S) det(S_M),

where M ranges over (n+1)-minors and all coefficients are real (preferably rational). Checking the coefficient identity and f!=0 proves membership and nonzeroness. A fully verified elimination Groebner basis can also establish nonzeroness. A mere low-rank numerical fit does not.

A particularly transparent sufficient certificate for I_n=0 is a full-row-rank Jacobian of q_n at one exact real X_0. Indeed, q_n then maps a neighborhood onto a neighborhood in R^d. Every f in I_n vanishes on all q_n(X), so it vanishes on an open set and is the zero polynomial. This proof does not require identifying J_n with the entire vanishing ideal.

The derivative is

 Dq_n(X)[H] = A(XH^T+HX^T),
 (Dq_n(X))*[y] = 2(A*y)X.

Thus a full-row-rank Jacobian is equivalent to the absence of any nonzero K in L, even indefinite, with KX=0. A nonzero d-by-d Jacobian minor evaluated at one rational X_0 is a finite exact certificate. Its symbolic polynomial is not identically zero, so outside its zero set no PSD stress exists; hence p_n=1. This independently rederives the statistical implication for this certificate.

For the full equivalence I_n=0 iff q_n is dominant iff its generic Jacobian has full row rank, one uses that the symmetric determinantal ideal generated by the (n+1)-minors is prime over a characteristic-zero field, together with the characteristic-zero Jacobian/algebraic-independence criterion. The complex rank-at-most-n symmetric matrices are parametrized by XX^T over C (complex symmetric congruence); real PSD rank-at-most-n matrices are Zariski dense in that variety because a polynomial identity on all real X extends to complex X. These facts explain the connection but do not convert real zero-set membership into a real PSD lift. The primeness theorem is a named external algebraic dependency, not reproved or independently source-verified here. The direct certificate implications above do not depend on accepting that external equivalence.

Other finite zero-ideal verification is possible via an exact Groebner basis of J_n, with a stated elimination order and Buchberger reduction certificates, whose elimination portion is empty. A bare software claim of zero should be independently reproducible, with exact coefficients and conventions.

A dimension obstruction supplies a useful independent check: for 0<=n<=m, rank-at-most-n symmetric matrices have dimension mn-n(n-1)/2. Therefore I_n=0 is impossible if d exceeds this number (using the standard defining-variety correspondence); the Jacobian cannot have full row rank in that case. The count is necessary, never sufficient.

The key logical limitation is one-way: I_n=0 gives the source's almost-sure upper bound MLT<=n. I_n nonzero alone gives no probability conclusion by the PSD mechanism. A generic Jacobian kernel can consist only of indefinite matrices. No converse to the elimination criterion is assumed in this freeze.

## 7. Exact signed-SOS criterion and the report's second case

For f in I_n, define P_f(L)=f(A(LL^T)), now using a full m-by-m triangular L with strictly positive diagonal. This substitution parametrizes positive definite covariances, not rank-n data covariances.

If an exact identity +/-P_f(L)=sum_j h_j(L)^2 holds and the h_j have no common zero anywhere on the positive-diagonal domain, then P_f does not vanish on any PD covariance. Since f vanishes on Q_n, Q_n intersect C is empty. Therefore p_n=0. If an independent I_{n+1}=0 or Jacobian certificate supplies p_{n+1}=1, the exact conclusion is WMLT=MLT=n+1. A nonzero SOS polynomial is not enough: it can vanish at points in the allowed domain. The no-common-zero assertion must be proved, for example by an explicitly positive diagonal-monomial square among the summands. Triangular orientation and all indices must be checked in the actual algebraic identity.

The source's second case asks for Sigma_0 PD with A(Sigma_0) in V(I_n). The independent PSD mechanism requires more to deduce positive probability: one must exhibit or prove existence of a real X in R^{m x n} with A(XX^T)=A(Sigma_0). If the submitted reasoning proves a suitable real lifting theorem, its assumptions and applicability must be checked. Without it the argument has moved from an actual Gram image to a larger algebraic zero set.

Even after a lift is supplied, the immediate conclusion is WMLT<=n. Exact WMLT=n still requires exclusion of good data with n-1 columns. Exact MLT=n+1 requires p_n<1 in addition to the upper certificate at n+1. The nonzero ideal is not substituted for either probability certificate in this family. These are audit obligations arising from the mechanism, not a counterexample or verdict on the report or any submitted proof.

Failure to find a signed SOS certificate does not prove that no such certificate exists. More generally, real nonvanishing on PD need not be represented by a particular requested SOS form unless an applicable representation theorem, its multipliers, and domain assumptions are supplied. Searching a bounded SOS degree gives partial evidence only.

## 8. Frozen mechanism, evidence, and gaps

Mechanism: the measured-trace projection gives a closed convex cone with a PSD dual. A rank-limited Gram statistic lies in its interior precisely when its data column span has no nonzero annihilating PSD concentration matrix. Positive probability is openness plus full Gaussian support. Almost-sure conclusions require exclusion of full-dimensional bad data, not just existence of a good point.

Verified independently by derivation: adjoint normalization; closedness/interior; exact PSD alternative; direct likelihood equivalence; positive-probability witness equivalence; sample monotonicity; Gaussian support assumptions; the Jacobian sufficient certificate; the robust PSD-stress lower-bound certificate; the signed-SOS sufficient certificate; the need for real lifting and separate lower-bound certificates.

Explicit dependencies: elementary separation of a closed convex cone; spectral theorem; strict concavity and derivative of log det; nonzero-polynomial zero sets have Lebesgue measure zero. The semialgebraic exact dimension criterion uses cell decomposition. The full algebraic equivalence involving the ideal uses symmetric determinantal primeness and characteristic-zero Jacobian theory; these are not needed for the direct one-sided exact certificates. No unproved dependency is silently promoted to an audited submitted result.

Pending before actual result audit: receive Root's frozen original/revised artifact packet; verify graph/color definitions and exact claim; compare all submitted certificates against these predicates; test boundary cases and claimed threshold equalities; determine whether any required real-lifting, lower-sample failure, or positive-measure failure argument is present; conduct independent exact checks without executing submitted scripts until authorized by Root's custody process.

Blocked route rule: treating V(I_n) membership as a real PSD lift, or treating I_n nonzero as an almost-sure lower bound, is blocked in this family unless materially new supporting theorem/evidence is supplied. It merely transfers the central difficulty. No submitted result is adjudicated in advance.

Completion estimate: 100% for this pre-artifact independent criteria freeze; 0% for the as-yet-unreceived submitted-result audit. These percentages concern this family's assigned work, not discovery of a resolution of Conjecture 4.
