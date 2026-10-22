# Final pass: transverse repair costs and accepted-result ledger

E-6322, 2026-10-16. The examples below delimit estimates based only on determinant amplitude and full-class energy. Section 2 uses the genuine identity minimizer and expensive finite comparisons. The varying-map sequence in Section 3 is nonminimal; its lack of stationarity is part of the scope, not an omitted condition. Neither example refutes the frozen target.

## 1. The derivative hidden in fiberwise determinant repair

For the genuine triangular construction in COMPENSATED_REPAIR_CRITERION.md, a prescribed smooth density increment h determines

f(x_1,x')=integral_alpha^{x_1} h(s,x') ds,
D' f=integral_alpha^{x_1} D' h(s,x') ds.

The fiber zero-mean condition controls the boundary values of f. A bound on h controls the determinant and the x_1 derivative. It does not control the transverse derivatives. This is a limitation of this particular triangular realization, not a theorem excluding all solutions of a prescribed-Jacobian problem.

## 2. Bounded determinant density, unbounded finite comparison cost

Work in a fixed interior cube Q of a smooth domain, and use identity boundary data. Choose nonzero A in C_c^infinity(I), with A>=0, and nonzero b in C_c^infinity(S). Set

w_N(x)=A(x_1)b(x_2,x_3) sin(Nx_2),
xi_N=-epsilon w_N e_1,
h_N=div xi_N=-epsilon A'(x_1)b(x') sin(Nx_2).

Choose epsilon>0 once so that |h_N|<=1/2 for all N. Every fiber has integral h_N=0. Consequently

phi_{N,t}=Id+t xi_N, 0<=t<=1,

is a smooth orientation-preserving diffeomorphism, equal to the identity outside Q. Its determinant lies between 1/2 and 3/2. The determinant amplitudes and all scalar L^p norms of h_N remain uniformly bounded.

For the original map y=Id, the competitor y composed with phi_{N,1}^{-1}=phi_{N,1}^{-1} has positive energy at least cN^6 for large N. Indeed,

Dphi_{N,1}^{-1}(phi_{N,1}(x))
 =I-e_1 tensor D(xi_N)_1/(1+h_N),

and |partial_2(xi_N)_1| has L^6 norm bounded below by cN. On a fixed subregion where |A b| is bounded below, the integral of cos^6(Nx_2) has a uniform positive lower bound. The transformed a-term is

a integral_Q (1+h_N)|Dphi_{N,1}^{-1}(phi_{N,1}(x))|^6 dx >=cN^6.

Thus determinant amplitudes alone do not bound the finite energy cost of this triangular repair. The unperturbed identity map is a genuine minimizer, but these comparisons are expensive; there is no contradiction with minimality.

## 3. Bounded baseline energy also does not bound the chosen first cost

To examine the signed first positive-energy cost, fix delta>0 and set

y_N=Id+(delta/N) w_N e_1.

For all sufficiently large N,

F_N=Dy_N=I+s_N e_1 tensor e_2+O(N^{-1}),
s_N=delta A b cos(Nx_2),
J_N=1+(delta/N)A' b sin(Nx_2).

The error is uniform on the fixed cube. In particular, F_N is uniformly bounded, J_N is bounded uniformly away from zero, y_N has identity trace, and the original full target energy is bounded uniformly in N. These are finite-energy maps in precisely the original class.

For a pure shear F(s)=I+s e_1 tensor e_2, put S=3+s^2. Direct matrix algebra gives

|F(s)|^2=|cof F(s)|^2=S,
(E_+(F(s)))_{12}=-[6a S^2+3b sqrt(S)]s.

The determinant-square term contributes only to the diagonal of U_+ and hence does not appear in this off-diagonal entry. On the other hand,

(Dxi_N)_{12}=-epsilon N A b cos(Nx_2)+O(1),

and all other entries of Dxi_N are bounded uniformly. The smoothness of E_+ on the bounded set of matrices involved, together with F_N-F(s_N)=O(N^{-1}), gives

integral_Omega E_+(F_N):Dxi_N
 =epsilon delta N integral_Q [6a(3+s_N^2)^2+3b sqrt(3+s_N^2)]
                            (A b)^2 cos^2(Nx_2) dx +O(1)
 >=cN-C.                                                      (1)

The lower bound follows by choosing a fixed sub-box where |A b| is bounded below. Its cosine-square integrals stay bounded below for large N.

This is exactly the signed positive-energy first cost R for the corresponding genuine material comparison, expressed in primal coordinates. Thus no uniform bound on this particular repair cost follows merely from a uniform total baseline energy, uniformly positive J, and bounded prescribed determinant density h_N.

Important scope distinctions:

- These y_N are not minimizers. The barrier contribution to their inner first variation is bounded, since J_N^{-2} and h_N are uniformly bounded, while (1) diverges. Thus (1) directly detects their failure of inner stationarity.
- The donor and recipient sign sets of h_N are not asserted to be the high-K and fixed low-K sets in the sufficient criterion. This example does not disprove that a minimizer admits a better tailored repair.
- The example does not show that every realization of the same density has this cost, nor that an optimal prescribed-Jacobian construction is impossible.
- For the exact identity minimizer in Section 2, the first positive-energy derivative is zero, because E_+(I) is a constant scalar matrix and integral div xi_N=0. Its large finite cost does not imply a large first cost.

What remains unsupported is an estimate for a minimizer-specific, level-set-aligned repair. The example prevents replacing that missing theorem by a scalar determinant-amplitude argument for the triangular map.

## 4. Accepted variational conclusions across the five passes

The following list records established results, without promoting them to a positivity proof.

1. Safe full-class outer and inner diffeomorphism comparisons, including exact finite-energy formulas and integrably dominated stress identities. The integrable fields are T=DW(F)F^T and E=WI-F^TDW(F); ordinary DW(F) need not be integrable in the full class.

2. Interior concentric and whole-boundary collar comparisons give genuine barrier-mass estimates with a positive-energy source. Those scalar L^1 estimates alone do not self-improve.

3. The inverse is an actual Sobolev almost-everywhere inverse, with derivative H=(F composed with v)^{-1}, exponents H in L^{9/5}, cof H in L^{9/4}, K in L^3, and full inverse boundary trace. This is stronger than a formal inverse matrix field but does not imply a homeomorphism.

4. Primal and inverse multiplicative first variations are dual versions of the same two equilibrium identities. Coupling them has not produced an additional independent equation or a reverse-Holder estimate.

5. Additional energy moments w=W(Dy) in L^{7/6} and L^{11/6} justify ordinary inverse and primal equilibrium, respectively. The thresholds are sharp for energy-only stress integrability, but the required moments have not been proved for arbitrary minimizers.

6. Compact W^{1,9/4} inverse additions are legitimate whenever their resulting dual energy is finite. Accepted structured graph transformations also cover certain natural W^{1,9/5} differences, again conditional on finite energy. Neither statement supplies a nonzero finite-energy amplitude interval.

7. Relative derivative bounds and controlled rank-one endpoints supply actual finite-energy intervals. A compatible finite-energy inverse has been exhibited with one fixed smooth direction for which every nonzero amplitude has infinite energy. That map is not a minimizer.

8. The current compensated estimate is

   3d(lambda^2-kappa^2) m <= R(u;v).

   A uniform upper bound R<=C_0 m for level-set-aligned repairs with a fixed low-K recipient threshold would yield a global bound on K and hence the requested lower bound on J. The actual triangular construction proves finite-energy admissibility and volume compensation for smooth fiber-compatible densities. It does not prove that uniform repair-cost theorem for arbitrary minimizers.

## 5. Final mathematical disposition

No proof or compliant counterexample to E-6322 has been obtained in this variational lane. The strongest remaining comparison gap is now quantitative: construct, for every sufficiently high inverse determinant level of a minimizer, a genuine finite-energy repair transferring nonzero determinant mass to a uniformly low-K region with signed positive-energy first cost bounded uniformly per unit transferred mass. Existing full-class energy, class-stability results, and safe finite comparisons do not establish that construction or cost estimate.

This is the fifth and final pass. No additional pass is presumed.
