# Independent operator-algebra derivation

This reconstruction was written after the original saved proof and official source inspection, and before reading any old bounded_region_v2 reviews or validation code. It audits the original mechanism rather than initiating a new proof search. Inner products are linear in the second entry. The analytic input isolated below is the uniform free-leakage bound in original equation (6); the separate PDE family audits that input.

## 1. Rigorous sector interpretation and coefficient

On the antisymmetric n-particle Hilbert space let the number-density measure act by n(dx) = sum_i delta_{x_i}(dx). Integrating the bounded measurable kernel 1_Lambda(x) 1_Lambda(y) V(x-y) against the product of these commuting sector measures gives multiplication by

    sum_{i,j} 1_Lambda(x_i) 1_Lambda(x_j) V(x_i-x_j).

The diagonal contribution is V(0) sum_i 1_Lambda(x_i). The normal-ordered quartic gives the ordered distinct-pair sum i != j, with no factor 1/2. For the original plateau V = 1 on Lambda-Lambda, V(0) = 1, so these are L_n^2 and L_n(L_n-1). Equivalently the formal CAR rewrite of a_x^* a_x a_y^* a_y adds the delta(x-y) one-particle term to a_x^* a_y^* a_y a_x. This explanation defines the sector operator and does not manipulate an undefined product of point fields as an operator.

The official report displays a density-density convention on printed p. 371, and a quartic ordered-pair convention on pp. 363-364. The original proof covers both with sigma = 0,1. There is no hidden half-pair factor. Were a convention to include a positive coefficient c, the reference gap would be c(2N+1-sigma), and the chosen times would have to be rescaled; the coefficient in the source is one.

T_n = sum_i (-Delta_i) is self-adjoint on the free n-particle domain, restricted to the closed invariant antisymmetric subspace. W_n = L_n(L_n-sigma) is real, bounded, permutation invariant, and nonnegative for both sigma. Thus H_n = T_n+W_n is self-adjoint on D(T_n). Its norm bound is at most n^2. This is boundedness for each fixed sector, not uniform boundedness over Fock space.

The Fock Hamiltonian is the self-adjoint maximal direct sum, with domain

    D(H) = {eta=(eta_n): eta_n in D(H_n), sum_n ||H_n eta_n||^2 < infinity}.

The vacuum is assigned H_0 = 0. No use of a potentially smaller intersection of formal global domains is necessary. The group U_H(t) exists and is strongly continuous; the finite-sector convergence extends to the direct sum by an arbitrarily small square-summable tail. The same facts apply to K_n = T_n+n(n-sigma).

For n >= 1 and M_n = n-L_n,

    H_n-K_n = -M_n(2n-sigma-M_n),
    ||(H_n-K_n)eta|| <= 2n ||M_n eta||.

This follows pointwise on the spectrum m=0,...,n, since 0 <= 2n-sigma-m <= 2n. At n=0 the difference is zero. At n=1,sigma=1 the interaction and difference vanish for both values of m. A discontinuity produced by n tending to infinity is compatible with these edges.

## 2. Exterior normalization and fixed observable

For an orthonormal list g_1,...,g_n the normalized Slater is a^*(g_1)...a^*(g_n)Omega. It has unit norm by the CAR. For normalized f orthogonal to every g_i, a(f)Psi = 0, Xi = a^*(f)Psi has norm one, and a(f)Xi = Psi. In the original construction f and the occupied orbitals have disjoint supports, so the orthogonality is exact for every N.

The CAR identity a(f)a^*(f)+a^*(f)a(f)=1 gives ||a(f)|| <= 1 and ||a^*(f)|| <= 1. Acting on the one-particle state f or the vacuum gives the reverse inequalities, hence both norms equal one. The same fixed f is used for all N; only the state and time vary. There is no Pauli upper bound on the number of orthogonal orbitals in the infinite-dimensional one-particle space of one bounded region. Their increasing kinetic cost is expressly included in the leakage input.

## 3. Independent CAR/exterior proof of the Slater second moment

Let P project onto span{g_i} and q be any orthogonal projection, including 1_{Lambda^c}. Complete the occupied list to an orthonormal basis. On Psi, only the occupied annihilation indices contribute to M=dGamma(q). The occupied diagonal terms contribute lambda Psi, where lambda = Tr(Pq). All occupied off-diagonal terms vanish by exclusion. The remaining terms are one-particle/one-hole Slaters:

    M Psi = lambda Psi + sum_{i occupied, alpha unoccupied}
             <e_alpha,qg_i> a^*(e_alpha)a(g_i)Psi.

These one-particle/one-hole vectors are mutually orthonormal up to irrelevant signs and orthogonal to Psi. The series is norm convergent because only finitely many i occur and ||qg_i|| <= 1. Therefore

    ||M Psi||^2 = lambda^2 + sum_i ||(1-P)qg_i||^2
               = lambda^2 + Tr(Pq(1-P)q)
               = lambda^2 + lambda - Tr(PqPq).

In particular Var(M) = Tr(Pq(1-P)q) <= lambda and

    ||M Psi|| <= sqrt(lambda+lambda^2) <= sqrt(lambda)+lambda.

Equivalently, on the occupied subspace C=PqP has eigenvalues nu_i in [0,1], and the variance is sum_i nu_i(1-nu_i). The exterior determinant identity gives the characteristic function det(I+(exp(iu)-1)C), consistent with the same moments. Neither argument assumes q diagonal in the occupied basis.

This estimate is false for arbitrary states. With all-inside and all-outside n-particle unit Slaters I_n,O_n, the normalized superposition sqrt(1-epsilon) I_n + sqrt(epsilon) O_n has lambda=n epsilon and variance=n^2 epsilon(1-epsilon). For n=4, epsilon=1/16, lambda=1/4 while variance=15/16. This is a concrete control against silently applying the Slater bound to interacting states. The original proof applies it only after FREE evolution, which preserves a Slater and orbital orthogonality.

## 4. Exactly what leakage suffices for the comparison

Suppose the analytic family establishes, uniformly for the N and N+1 Slaters and the relevant small times,

    lambda_n(s) <= C s^2 n^(5/3).

The preceding identity then gives

    ||M_n exp(-is T_n)Phi_n|| <= C (|s| n^(5/6) + s^2 n^(5/3)).

Since H_n-K_n is bounded on each sector, the strong Duhamel identity is valid for every vector. Applying it to the ORIGINAL initial Slater, with reference evolution exp(-isK_n) equal to free evolution times a scalar, gives

    E_n(t) := ||(exp(-itH_n)-exp(-itK_n))Phi_n||
            <= 2n integral_0^t ||M_n exp(-isT_n)Phi_n|| ds
            <= C (n^(11/6)t^2 + n^(8/3)t^3).

No interacting Slater assumption occurs. At t_N = pi/(2N+1-sigma), both n=N and n=N+1 obey E_n(t_N) <= C (N^(-1/6)+N^(-1/3)), so both errors tend to zero. A first moment alone would be inadequate: ||M Phi||^2 <= n lambda is the generic bound and may lose the needed limit. The stronger Slater moment identity is what converts the PDE-family quantity into a Fock-space vector comparison.

## 5. Two-vector comparison and phase sign

Write A=a^*(f), Xi=A Psi, U_H(t)=exp(-itH), and similarly U_K. For the N-to-N+1 matrix element,

    F_H(t) = <U_H(t)Xi, A U_H(t)Psi>.

The exact telescoping identity is

    F_H-F_K = <(U_H-U_K)Xi, A U_H Psi>
            + <U_K Xi, A (U_H-U_K)Psi>.

Both vectors are normalized under either unitary, hence |F_H-F_K| <= E_{N+1}+E_N. The second error alone does not suffice. For example, keep the N-sector evolution identical to the reference but multiply the N+1-sector evolution by -1 at the observation time. Then E_N=0 while the matrix element changes sign. The original proof includes both errors and needs no estimate on A applied to an evolved interacting vector.

The scalar reference energy is e_n=n(n-sigma), and

    e_{N+1}-e_N = 2N+1-sigma.

Free covariance, with the stated inner-product convention, is

    exp(it dGamma(h)) a^*(f) exp(-it dGamma(h)) = a^*(exp(ith)f).

Consequently

    F_K(t) = exp(it(2N+1-sigma)) <a^*(f)Psi,a^*(exp(ith)f)Psi>
           = exp(it(2N+1-sigma)) <f,exp(ith)f>.

The final equality uses <Psi,a(f)a^*(g)Psi>=<f,g> and a(f)Psi=0. It does NOT require a(g)Psi=0 or g=exp(ith)f remaining orthogonal to the occupied space. The prescribed t_N makes the phase exactly -1 for both conventions. Because t_N tends to zero, the free overlap tends to one. The two errors therefore imply F_H(t_N) tends to -1.

## 6. Adjoint witness, norms, states, and topology

Let B_N=exp(it_NH) A exp(-it_NH)-A and D_N=B_N^*. Since ||A||=1, ||B_N||=||D_N|| <= 2. Also

    <Xi,B_N Psi> = F_H(t_N)-1 -> -2,
    <Psi,D_N Xi> = conjugate(F_H(t_N)-1) -> -2.

The unit-vector lower bound and the uniform upper bound yield both ||D_N Xi|| -> 2 and ||D_N|| -> 2. Moreover the same evidence implies the useful directional control

    ||D_N Xi + 2 Psi||^2 <= 8 + 4 Re< Psi,D_N Xi> -> 0.

For the normal vector states omega_N(C)=<Xi_N,C Xi_N>, omega_N(D_N^*D_N)=||D_N Xi_N||^2 tends to four. These are genuine states on B(Fock), and restricting them to the CAR algebra also gives states. The positive product D_N^*D_N need not lie in CAR because invariance is not asserted; its expectation is legitimately taken in B(Fock).

For every fixed eta and every bounded observable B, Stone continuity instead gives

    ||(exp(itH)B exp(-itH)-B)eta||
    <= ||B|| ||(exp(-itH)-1)eta|| + ||(exp(itH)-1)B eta|| -> 0.

Thus fixed-vector SOT continuity survives, as does adjoint SOT continuity. Since ||D(t)|| <= 2, D(t)^*D(t) also tends strongly to zero. Every FIXED normal state has expectation of D(t)^*D(t) tending to zero, by a finite-rank approximation of its trace-class density operator. No fixed normal-state discontinuity is established or required.

The witnesses escape to particle sectors N+1. They converge weakly to zero as vectors, vanish asymptotically on compact operators as vector states, and cannot have a normal state limit. This varying-state lack of uniformity is precisely allowed by operator norm. On every fixed adjacent-sector block norm continuity also holds: comparison with free dynamics bounds that block by ||exp(ith)f-f||+|t|(||W_n||+||W_{n-1}||), which tends to zero for fixed n.

The operator conclusion is failure of pointwise norm continuity of one fixed CAR generator as an orbit in B(Fock). It rules out any norm-continuous CAR dynamical system agreeing with this Fock conjugation, whether or not separate CAR invariance is available. It neither proves nor needs non-invariance. The conclusion is existential in dimension three, one bounded ball, one potential, and variable increasing local density. It is not a fixed-density thermodynamic result, a statement about every interaction, or a fixed-vector discontinuity.

## 7. Source scope

The official report explicitly distinguishes the C*-algebra norm continuity from the weaker strong operator topology on printed p. 365. Its fermion question on p. 371 concerns a bounded interaction region. The fixed-density extended-system condition is in the separate boson question immediately before it. This audit uses those source facts solely to fix topology, coefficient, and admissible quantifiers, with no historical-priority or current-openness conclusion.

Primary source: [Oberwolfach Report 7/2025, printed pp. 363-365 and 371](https://ems.press/content/serial-article-files/51350), DOI 10.4171/OWR/2025/7. Source statements here are paraphrased; no PDF, raw source text, or screenshot is part of this public review.
