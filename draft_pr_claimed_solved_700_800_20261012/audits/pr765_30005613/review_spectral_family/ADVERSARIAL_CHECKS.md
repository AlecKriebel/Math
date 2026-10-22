# Adversarial checks of the spectral mechanism

These are independent analytic counterexamples to weakened statements. They do not contradict the candidate, whose assumptions explicitly rule them out. The finite exact controls in controls.py check algebraic instances only; the Hilbert-space proofs below are the infinite-dimensional evidence.

## A. Strong projection convergence alone can lose the protected space

On H=ell2(N), let e_j be the standard basis and A e_j=j e_j, so R=(A+1)^(-1) e_j=(j+1)^(-1)e_j is a genuine injective resolvent. Put R_n=R and P_n=|e_n><e_n|. Then [R_n,P_n]=0, rank(P_n)=1 for every n, and P_n converges strongly to zero: ||P_n f||=|f_n| -> 0 for every f in ell2. However ||P_n||=1, and the limiting rank is zero. In particular, strong convergence does not preserve the protected one-dimensional space. For n != m, ||P_n-P_m||=1, so the summable operator-norm transport hypothesis of the candidate fails. Uniform norm convergence of P_n^k for each fixed k is substantive; merely following a weakly escaping normalized eigenvector would not prove the result.

## B. Exact finite-rank transport does not imply completeness

Let H=ell2(N) direct_sum L2([0,1],dx), and let A=diag(q_j) direct_sum M_x where (q_j) lists all positive rational numbers. This is nonnegative self-adjoint, and R=(A+1)^(-1) is positive, bounded, and injective. Put R_n=R. Let P_n^k be projection onto span(e_1,...,e_k) in the first summand, for every n>=k. These projections are finite-rank, exactly nested, and commute with R_n; every transport difference is zero. Their limiting ranges lie in H_pp(A), and the point spectrum is dense in [0,infinity). Nevertheless the entire nonzero L2 summand is absolutely continuous. Thus exact transport plus dense eigenvalues does not exclude H_ac.

Replace dx by the standard middle-thirds Cantor probability measure mu_C and take A=diag(q_j) direct_sum M_x on ell2 direct_sum L2(mu_C). Since mu_C has no atoms and is singular with respect to Lebesgue measure, the second summand has singular continuous spectral type and has no eigenvectors. All the finite-rank transport statements and density of the point eigenvalues remain true, but H_sc is nonzero. Therefore absence of H_sc requires completeness, not a trace-class no-ac theorem or dense eigenvalues.

The candidate explicitly avoids both counterexamples: its probes are an actual basis of the entire final L2 space, every fixed probe is revisited at all sufficiently late birth stages, and the birth errors plus transport tails tend to zero.

## C. Without injectivity, protected vectors can escape to infinite energy

On H=ell2(N), define A_n e_1=(n-1)e_1 and A_n e_j=j e_j for j>=2, with the usual diagonal domain. These are densely defined nonnegative self-adjoint operators, and their genuine resolvents satisfy

R_n e_1=(1/n)e_1, and R_n e_j=(1/(j+1))e_j for j>=2.

R_n converges in operator norm to R with R e_1=0 and R e_j=(j+1)^(-1)e_j for j>=2. Let P_n^k project onto the first k coordinate vectors, independent of n>=k. All ranks, nesting, commutation identities, zero transport errors, and exhaustive birth probes hold exactly. Yet the nonzero protected vector e_1 has energy n-1 -> infinity. The limiting R has a kernel and cannot be the resolvent of a densely defined self-adjoint operator on H. The candidate first identifies its strong limit as the actual final-domain resolvent; its injectivity rules this out. Positivity by itself would be insufficient.

## D. A single vector inside a multiple eigenspace need not follow one split branch

Take R_0=diag(1/2,1/2,1/5,4/5). Let U rotate the first two coordinates with cosine 3/5 and sine 4/5. For t>0 tending to zero put R_t=U diag(1/2-t,1/2+t,1/5,4/5) U*. Then ||R_t-R_0||=t. The rank-one spectral projection for the first split branch stays at norm distance 4/5 from |e_1><e_1|, although the complete rank-two cluster projection is constant. The exact rational control verifies the projection identity. This falsifies a proof that arbitrarily selects a vector or a proper subspace of a degenerate eigenspace. The candidate transports full eigenspaces and full split clusters and hence does not make that mistake.

## E. Explicit split-cluster and finite-nonresonance controls

The independent controls use Fraction arithmetic and no nonstandard dependencies. Two coordinate-plane rotations with c=(1-t^2)/(1+t^2), s=2t/(1+t^2), for t=1/8,1/16,1/32,1/64, transport rank-two and rank-three nested projections. Exact matrix multiplication checks self-adjointness, idempotence, nesting, ranks via traces, and commutation with split resolvents. The norm distances of the projections are exactly s, because the squares of their differences are diagonal with entries 0 or s^2.

For d=2, protected cube eigenvalues measured in units pi^2/4 are 2,5,8,13. The candidate width interval is (2,3). Exhausting integer pairs within the proved coordinate bound produces 39 distinct forbidden squared widths. The rational width 8/3 is outside this finite set; each protected equality would force a noninteger rational sum of integer squares, impossible. This is an exact finite sanity check of the formula, while the general nonresonance conclusion is established by the finite-bound proof in the candidate.

All assertions in controls.py passed. Neither these matrix controls nor finite cube arithmetic certifies norm-resolvent convergence of PDE operators or the infinite diagonal completeness argument.

## F. Boundary cases and limiting arguments checked analytically

- d=1 is excluded correctly. Adjacent intervals become a single interval after their point interface is opened; shrinking the nominal window does not restore a Dirichlet separation. The point-removability mechanism is dimension-sensitive.
- At d=2 the finite-window input is logarithmic-capacity rather than a uniform spectral-gap statement. The candidate requests no numerical window lower bound or effective modulus.
- Arbitrarily small nonresonant gaps and arbitrarily large finite multiplicities do not obstruct the induction: each stage makes only finitely many norm-error requests and is free to choose a smaller positive aperture.
- No projection-rank bound uniform in k is required. Each fixed k has finite preserved rank; the birth ranks may grow arbitrarily rapidly.
- Strong convergence of R_n suffices for commutation in the limit because the P_n^k converge in norm and ||R_n||<=1. The proof does not need norm convergence of the unbounded-domain exhaustion.
- Zero-extended sine probes need only lie in H=L2(O). They need not belong to H_0^1(O), so no false domain assertion is hidden in the completeness argument.
- For lambda=0 the Weyl sequence gives approximate zero modes but no eigenvector at zero. This is compatible with injectivity of A and with zero lying in the essential spectrum.
