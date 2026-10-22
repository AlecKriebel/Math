# Independent reconstruction, frozen before inherited review

Frozen in UTC on 2026-10-15, before reading the submitted `independent_review/FINAL_REVIEW.md`. The companion freeze record hashes this file and the independently authored controls. Nothing in this reconstruction treats the queue status, author verification output, or earlier review as a premise.

## Claim, assumptions, and success criteria

The statistical claim under test is that the ordinary concentration model on the complete bipartite graph with parts A={1,2,3,4}, B={5,6,7,8}, and the variant imposing the additional equality K11=K22, both have WMLT=2 under the fixed-zero-mean Gaussian sampling convention. The ordinary model additionally has MLT=4. The tied variant is not assigned an exact MLT by the candidate, and this reconstruction does not assign it one.

Here WMLT is the least positive integer r for which the MLE exists with positive probability, whereas MLT requires probability one. Samples are independent nondegenerate N(0,Sigma) vectors, with Sigma positive definite and, for correctly specified sampling, Sigma inverse in the concentration model. S=(1/r)XX^T is the uncentered sample covariance, with observations as columns of an 8 by r matrix X. Rank is almost surely min(8,r). The harmless positive scale is omitted when convenient. This is the convention explicitly used in the rigidity v3 introduction and its footnotes, including the definition of WMLT in section 8.

Validation must establish likelihood attainment and uniqueness, rather than only a formal covariance match; a full-dimensional positive-probability success set, rather than an isolated singular Gram matrix; and a one-sample obstruction valid for every observation, including zero components and the tied-diagonal model. The MLT=4 statement must be distinguished from WMLT=2 and not inferred from a generic-completion-rank equality without justification.

## 1. The exact model and statistic map

Let L be the real vector space of symmetric 8 by 8 matrices of the form

    K = [ D_A  C   ]
        [ C^T  D_B ],

where D_A,D_B are arbitrary diagonal matrices and C is arbitrary. Let L_t={K in L: K11=K22}. Both contain I8 and have nonempty positive-definite cones. These are linear concentration, or RCON, constraints; they constrain K=Sigma inverse, not the covariance entries and not correlations.

For singleton colors, pi(S) lists the eight diagonal entries followed by the sixteen cross entries. For the tied model pi_t replaces s11,s22 by s11+s22 and leaves all remaining coordinates alone. There are respectively 24 and 23 independent statistics. The edge coordinates in the trace pairing have factor 2:

    tr(SK) = sum_i s_ii d_i + 2 sum_(i in A,j in B) s_ij c_ij.

For L_t the first two diagonal terms become (s11+s22)d1. Thus ker(pi)=L perpendicular and ker(pi_t)=L_t perpendicular for the trace inner product. The factor 2 is invertible and changes neither the kernel nor feasibility of matching statistics. The report's color-class sums give precisely these maps. Merging the vertex colors does not require s11=s22 of a covariance completion.

## 2. A self-contained likelihood / PD-completion equivalence

The following applies to either linear space above. Denote it by L and its statistic projection by q. Put

    C_q = q(PD_8),     f_S(K)=tr(SK)-log det K,     K in L intersect PD_8.

For S positive semidefinite, these statements are equivalent:

1. f_S has a finite attained minimum in the model, necessarily unique.
2. There exists P positive definite with q(P)=q(S).
3. There is no nonzero A in L intersect PSD_8 with tr(AS)=0.

Here is a direct derivation that does not assume the claim being audited.

**Attainment implies completion.** At an interior minimizer Khat, every direction H in L has zero derivative. Hence tr((S-Khat inverse)H)=0 for all H in L. P=Khat inverse is positive definite and q(P)=q(S). The derivative is legitimate because L intersect PD is relatively open in L.

**Completion implies attainment.** If q(P)=q(S), then tr(PK)=tr(SK) for every K in L. Let alpha=lambda_min(P)>0. For eigenvalues lambda_i(K)>0,

    f_S(K)=f_P(K) >= sum_(i=1)^8 [alpha lambda_i - log lambda_i].

The scalar h(x)=alpha x-log x has finite minimum 1+log alpha and tends to positive infinity at both 0 and positive infinity. In any sublevel f_S(K)<=c, each h(lambda_i) is at most c-7(1+log alpha). Consequently all eigenvalues stay in a common compact subinterval of (0,infinity). The sublevel in the closed finite-dimensional linear space L is compact. Taking the sublevel through I8 proves attainment. The Hessian in a nonzero symmetric direction H is

    tr(K inverse H K inverse H)
      = ||K^(-1/2) H K^(-1/2)||_F^2 > 0,

so f_S is strictly convex on the model cone and the minimizer is unique.

**Failure gives an actual likelihood ray.** q is surjective, so C_q is an open full-dimensional convex cone. For S PSD, q(S+epsilon I8) belongs to C_q for epsilon>0, so q(S) is in its closure. If q(S) is not in C_q, a supporting functional gives a nonzero matrix A in the adjoint image L with A PSD and tr(AS)=0. This follows from self-duality of PSD under the trace pairing: tr(AP)>=0 for every P PD is equivalent to A PSD. Injectivity of the adjoint ensures A is nonzero. Conversely such A prevents a matching P PD, because tr(AP)>0 whenever A is nonzero PSD. Along the feasible ray K(t)=I8+tA, t>=0,

    f_S(K(t)) = tr(S)-log det(I8+tA) -> -infinity.

Thus the likelihood is unbounded above and the MLE does not exist. This also proves the separation alternative (2) iff (3). When S=XX^T/c, tr(AS)=||A^(1/2)X||_F^2/c, and for A PSD it vanishes exactly when AX=0.

This proof avoids the possible gap in arguing that divergence on each fixed ray alone implies a uniform compact sublevel. Its compactness bound is uniform over all feasible K.

**A matching completion need not be the estimated covariance.** Take P=I8+(1/4)(E12+E21). It is PD, with eigenvalues 5/4,3/4 and six 1's, and it has the same singleton and tied statistics as I8. Yet (P inverse)12=-4/15, a forbidden within-part entry. This is harmless: P certifies coercivity; the optimizer's inverse, obtained from the score equations, is the completion whose inverse is in L. At statistics q(I8), the optimizer is I8 itself. The candidate uses the correct existence criterion and does not require its arbitrary completion M(X) to have inverse in the model.

## 3. Two samples succeed on a full-dimensional open set

Let Xstar have first four rows (1,0) and last four rows (0,1). Then

    Tstar = Xstar Xstar^T = diag(J4,J4),
    rank(Xstar)=rank(Tstar)=2,
    pi(Tstar)=pi(I8),    pi_t(Tstar)=pi_t(I8).

This exact point alone would be insufficient for WMLT. Let U be the open box in R^(8 by 2) given by |X_ij-Xstar_ij|<epsilon, epsilon=1/100. Every left row is (1+a,b) and every right row (c,1+d), with |a|,|b|,|c|,|d|<epsilon. Define M(X) by preserving all diagonal and cross entries of XX^T and setting within-part off-diagonal entries to zero. Then M(X) matches both sets of statistics, though it need not itself satisfy M11=M22 and is not required to do so.

Uniformly throughout U,

    M_ii >= (1-epsilon)^2 = 9801/10000,
    |M_ij| <= 2 epsilon(1+epsilon) = 202/10000  (cross entries),
    M_ii - sum_(j != i)|M_ij| >= 8993/10000.

The arithmetic is 9801-4*202=8993. For any real z, the inequality 2|z_i z_j|<=z_i^2+z_j^2 gives

    z^T M z >= sum_i (M_ii - sum_(j != i)|M_ij|) z_i^2
             >= (8993/10000)||z||^2.

Hence M(X) is positive definite with a uniform rigorous spectral lower bound. For the actual S=XX^T/2, use completion M(X)/2 and lower bound 8993/20000. The two-sample data rank is also exactly two: a left row and a right row have determinant

    (1+a)(1+d)-bc >= (1-epsilon)^2-epsilon^2
                  = 1-2 epsilon = 49/50 > 0.

The open box has volume (1/50)^16 and is full-dimensional in the two-observation sample space. For any Sigma PD the joint Gaussian density is

    (2 pi)^(-8) (det Sigma)^(-1)
      exp[-tr(Sigma inverse XX^T)/2] > 0.

The density is strictly positive at every point. For an optional explicit lower bound, ||X||_F^2<=8((101/100)^2+(1/100)^2)=8.1616 throughout the box, so its probability is at least

    (1/50)^16 (2 pi)^(-8) (det Sigma)^(-1)
      exp[-(5101/1250) lambda_max(Sigma inverse)] > 0.

This proves WMLT<=2 for both models. The numerical probability can depend on Sigma, but whether this event has positive probability, zero probability, or probability one does not: nondegenerate Gaussian laws for the whole data matrix are mutually absolutely continuous with Lebesgue measure. Correct specification of the model introduces no support restriction.

## 4. One sample never succeeds, including all zero cases

For one observation x in R8, edge 3–5 has singleton endpoint-diagonal and edge colors in both models. Every matching PD completion would have the principal block

    [ x3^2   x3 x5 ]
    [ x3 x5  x5^2  ],

which has determinant zero. A PD matrix has all principal blocks PD. If x3 or x5 is zero there is additionally a zero prescribed diagonal, so no zero-component exception exists. The tied constraint K11=K22 changes neither endpoint statistic nor the edge coordinate.

A direct ray certificate checks all model equalities as well. If (x3,x5) is not (0,0), set v=x5 e3-x3 e5 and A=vv^T. Then A is nonzero PSD, Ax=0, its only off-diagonal support is edge 3–5, and A11=A22=0. It belongs to both L and L_t. If x3=x5=0, take A=e3 e3^T. This covers even the all-zero observation. The previous likelihood-ray proof establishes nonexistence for every one-sample datum, not just almost every datum.

Combining sections 3 and 4 yields WMLT=2 for each model.

## 5. Literal PD intersection and strict signed-SOS exclusion

The relevant ideal is the report's elimination ideal from all (n+1)-minors of a generic symmetric matrix and the statistic equations. For every f in I(G,3), evaluation at any rank-at-most-three matrix T with statistic t forces f(t)=0, by its membership in that elimination ideal. The concrete Tstar has rank two and pi(Tstar)=pi(I8), so every such f vanishes at the positive-definite statistic pi(I8), for both colorings. This argument uses an actual PSD preimage, not a merely complex or Zariski-limit point.

Even a hidden request for exactly rank three would not rescue the numerical implication here. Let Z have left rows e1,e3,e1,e3 and right rows all e2 in R3. It has rank three, unit row norms, and zero cross block, hence the same singleton and tied statistics as I8. This extra control is not needed for the literal second bullet, which only requests a point of the variety.

On the positive-diagonal triangular Cholesky domain, I8 has Cholesky factor I8. Every pulled-back ideal polynomial f(pi(LL^T)) therefore vanishes at L=I8. No such polynomial can be nowhere zero on that domain, whether it or its negative is SOS. This excludes the report's strict separator mechanism. The source's example explains nonvanishing through positive Cholesky diagonal factors, supporting this strict meaning. A merely nonzero SOS polynomial can have zeros and would not be excluded by this argument; the candidate appropriately invokes strict nonvanishing, not just nonzero as a polynomial. Upper versus lower triangular indexing conventions do not affect the I8 test.

Conditional on the separately audited ideal facts I(G,4)=0 and I(G,3) nonzero, the index in the report's displayed premise is n=3. This statistically verified WMLT=2 contradicts the equality WMLT=n in its second bullet, even though the second bullet's PD-intersection hypothesis actually holds. The present audit does not rely on or certify any separate source-scope or algebraic-family verdict.

## 6. Full primary theorem check for the separately credited MLT

Blekherman–Sinn v2, Theorem 2.7 (printed p. 15) assumes a complete bipartite ordinary graph K_(m,n), n>=m>=2, and defines M as the smallest k with k(k+1)/2>=m+n. It states MLT=min(M,m+1). For m=n=4, 3*4/2=6<8 and 4*5/2=10>=8, so M=4 and min(4,5)=4. This is exactly the candidate's application and uses all its premises.

I read the full argument on pp. 15–18, including the dual sparse PSD matrices in L_(Kmn), the Schur-complement / isometry parameterization, the open real-solvability argument in Lemma 2.9 needed for the lower bound, and the dimension upper bound in Lemma 2.10. Their Proposition 1.5 links generic data subspaces to absence of a PSD sparse matrix annihilating the data. The four-cycle case and the abstract alone were not substituted for that proof. The paper explicitly reiterates the m=4,n=4,5,6 value on p. 19. No diagonal color equality is part of that theorem. Some general-case proof ingredients cite external results; the following specialization bypasses those dependencies and independently verifies the actual numerical case used here.

### 6a. Four observations succeed almost surely in the singleton model

Write a four-sample data matrix X as [U;V], with U,V both 4 by 4. Outside an algebraic null set they are invertible. A symmetric sparse matrix A=[D C;C^T E] annihilating X must satisfy

    D U+C V=0,     C^T U+E V=0.

Eliminating C gives

    U^T D U = V^T E V.

This is a homogeneous system in the eight diagonal entries of D,E. Let C4(U,V) be its 10 by 8 coefficient matrix: columns are the symmetric coordinate vectors of u_a u_a^T and -v_b v_b^T, for rows u_a,v_b of U,V. At U=I4 and V whose row i is e_i+2e_(i+1) (cyclic indices), V has determinant -15. The exact 8 by 8 minor in zero-based rows (0,1,3,4,5,7,8,9), with pair coordinates ordered lexicographically i<=j, has determinant -16. Thus a fixed coefficient minor is a nonzero polynomial in the data.

Outside the zero sets of that minor and det(U)det(V), the only D,E are zero and then C=0. Therefore no nonzero sparse symmetric matrix, in particular no PSD one, annihilates X. Section 2 gives an MLE. Nonzero polynomial zero sets have Lebesgue measure zero, hence the MLE exists almost surely for four nondegenerate Gaussian samples. This proves MLT<=4 independently of an elimination-criterion citation.

### 6b. Three observations fail on an open set in the singleton model

Let

    H = (1/2) [ 1  1  1  1 ]
              [ 1 -1  1 -1 ]
              [ 1  1 -1 -1 ]
              [ 1 -1 -1  1 ],

U0 be the first three columns of I4, and V0=H U0. The 8 by 3 seed data [U0;V0] has rank three. Since H is orthogonal, U0^T U0=V0^T V0=I3. The sparse matrix

    A0 = [ I4  -H^T ] = [ I4 ] [ I4  -H^T ]
         [ -H    I4 ]   [ -H ]

is nonzero PSD of rank four and annihilates the seed data. In fact det(I8+t A0)=(1+2t)^4, making its likelihood divergence explicit.

To obtain an open failure set, rather than an exceptional example, for any nearby U,V define the 6 by 8 coefficient matrix C3(U,V) of

    U^T diag(d) U - V^T diag(e) V = 0.

At the seed, C3 times the all-ones vector is zero. The square minor in zero-based columns P=(0,1,2,4,5,6) is -1/16, so C3 has full row rank. In a neighborhood where this minor stays invertible, fix the two nonpivot weights to 1 and set the pivot correction to

    w_P = 1_P - C3_P inverse (C3 1_8).

Then C3 w=0. The formula is continuous and equals the all-ones vector at the seed, so every weight remains strictly positive on a smaller open neighborhood. U and V retain column rank three there.

Put D=diag(w1,...,w4)>0 and E=diag(w5,...,w8)>0. The relation U^T D U=V^T E V implies that the map sending the columns of D^(1/2)U to those of E^(1/2)V is an isometry between three-dimensional subspaces of R4. Extend it to an orthogonal Q on R4. Then

    A = [ D                         -D^(1/2) Q^T E^(1/2) ]
        [ -E^(1/2) Q D^(1/2)                       E     ]

is the PSD Gram matrix [D^(1/2);-E^(1/2)Q][D^(1/2),-Q^T E^(1/2)], is nonzero, has the required diagonal within-part blocks, and annihilates [U;V]. Section 2 gives likelihood nonexistence for every data point in this full-dimensional open neighborhood. Such a set has positive probability for every Sigma PD. Hence three samples do not have almost-sure existence.

For completeness, almost-sure success is monotone in the sample count: a PD completion P of the unnormalized scatter from r samples remains a PD completion after adding a further outer product yy^T, by using P+yy^T. Therefore an almost-sure threshold below four cannot coexist with the positive-probability failure at three. This proves MLT>=4 and consequently MLT(K4,4)=4.

This independent specialization has no claim of novelty and must not be transferred to L_t merely by citing the ordinary graph theorem. The original candidate already makes that distinction.

## 7. Boundary conventions, strongest result, and remaining gaps

An estimated, unconstrained unknown mean changes the sample-count convention. For r Gaussian observations, centered scatter has the distribution ZZ^T with r-1 independent N(0,Sigma) columns after an orthogonal change of coordinates in sample space. Thus ordinary centered-data thresholds would be WMLT=3 and MLT=5, and the proved tied weak threshold would be 3. These are a change of question, not exceptions to the explicitly fixed-zero-mean result. A true singular covariance or a sampling law supported on a proper subset would also invalidate the positive-everywhere density premise and is excluded here.

The strongest verified statistical statement is:

    singleton K4,4: (WMLT,MLT)=(2,4);
    tied K11=K22 variant: WMLT=2;
    both: pi(I8) is realized by a rank-two PSD Gram matrix,
          and also by an exactly rank-three PSD Gram matrix.

The candidate's likelihood, open-set, rank, rational margin, one-sample, genuine-color, and strict-separator arguments have no substantive defect under these assumptions. Useful presentational strengthening is to state the likelihood objective and provide the compact-sublevel proof, since an arbitrary matching covariance is not automatically the MLE. Exact probability values, an exact tied MLT, a Boolean separator-versus-intersection classification, intended source restrictions, algebraic-ideal completeness, historical priority, eligibility, and publication decisions are outside this statistical audit. No outside communication was initiated or prepared.

## Checkable artifacts at freeze

`exact_controls.py` is independently authored and passes 188 exact assertions. Its controls include the trace-statistic pairing for both colorings; rank-two and exactly rank-three preimages; all rational box bounds; boundary-aware sparse PSD rays; eight additional rational interior data matrices; the matching-completion/inverse distinction; and the independent singleton MLT upper/lower constructions with explicit nonzero minors. The complete numerical output is in `exact_controls_results.json`. The first execution had a checker-only failure because an expanded polynomial was compared structurally with a factored expression; replacing that comparison by exact polynomial subtraction gave zero. No mathematical certificate changed. These computations supplement the analytic proof; they do not estimate a probability by simulation.
