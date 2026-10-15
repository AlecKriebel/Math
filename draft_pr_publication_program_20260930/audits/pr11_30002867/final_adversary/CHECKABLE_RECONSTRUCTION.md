# Fresh reconstruction and falsification record

This is a verification of the repaired PR11 candidate, not a new mathematical discovery. Let `R=C[x_1,...,x_d]`, `d>=1`, let `I` be proper of finite positive colength `N`, and let `M_i` act by multiplication on `A=R/I` in any common basis. All steps below require this promised regular representation.

## 1. Exact literal target

The official OWR report has its coordinate-multiplication display (1), Definition 5 and Problem 2 on printed p. 1183. Definition 5 concerns global generation by `d` polynomials. The preceding Theorem 6 adds a condition at infinity to a theorem about Hermite projectors; that condition is not part of Problem 2. Polynomial reconstruction, Gröbner bases, and primary decomposition are not prohibited by the question.

Every proper finite-colength ideal can occur as the kernel of an ideal projector: choose any linear complement to the ideal and project onto it. Thus replacing the projector by its finite quotient loses no ideal in the stated scope. The candidate explicitly omits the zero projector/unit ideal and dimension-zero ambient ring, avoiding dimension and empty-spectrum conventions. It covers the conventional positive-dimensional, nontrivial target.

## 2. Support and the Koszul count

At `lambda`, set `m_lambda=(x_i-lambda_i)` and `T_i=M_i-lambda_i Id`. The map `D1:A^d→A` has image `m_lambda A`. Therefore

`coker D1 = R/(I+m_lambda)`.

This is zero off the support and one-dimensional at every support point, including a nonreduced point. Consequently `rank D1=N-1` exactly on `V(I)`. Distinct support points give distinct Artinian factors, so the support has at most `N` points. Each support coordinate is an eigenvalue of the corresponding `M_i`; enumerating the Cartesian product of the individual spectra and filtering by `rank D1<N` recovers precisely the support.

The shifted coordinates form a regular sequence in `R`. Their Koszul complex resolves `R/m_lambda`; tensoring with `A` produces the candidate's block maps. Wedge contraction gives the `(i,j)` column `-T_j` in row `i`, `T_i` in row `j`. Commutation verifies `D1 D2=0`.

Tensor the exact sequence `0→I→R→A→0` with `R/m_lambda`. At support, `I⊂m_lambda`, so the map `I/m_lambda I→R/m_lambda` is zero. Since the middle term is free, this gives

`H1(K(T;A)) = Tor_1^R(A,R/m_lambda) ≅ I/m_lambda I`.

Localizing this vector space changes nothing: every element outside `m_lambda` acts by a nonzero complex scalar. Nakayama thus yields the exact local generator count

`mu(I_m)=dN-rank D1-rank D2=(d-1)N+1-rank D2`.

The formula does not require reducedness, diagonalizability or CI. The height of the local ideal is `d`; hence the count is at least `d`. Equality gives a system of parameters in a regular local ring, which is a regular sequence. Conversely a local CI has this count `d`. This proves the local equivalence independently of the subsequent global theorem.

## 3. Stronger global formula and its precise classical dependency

Put `Q=I/I²`. The Artinian ring `A` is a finite product of local rings. Any local module-generating lists can be padded to equal length and combined using the product idempotents. This proves

`mu_A(Q)=max_lambda mu_{A_lambda}(Q_lambda)`.

The local residue space is `I/(I²+m_lambda I)=I/m_lambda I`, because `I⊂m_lambda`. Thus `r=mu_A(Q)` is exactly the maximum of the local counts computed above. Also `mu_R(Q)=mu_A(Q)`, since the ideal `I` annihilates `Q`.

The original Mohan Kumar Theorem 5, printed pp. 234–235, says that an ideal in a polynomial ring over a field or PID satisfies `mu(I)=mu(I/I²)` if `mu(I/I²)>=dim(R/I)+2`. The threshold is inclusive; the theorem has no local-CI, radicality, algebraic-closure, characteristic or prescribed-lifting assumption. Here `dim(R/I)=0` and, for `d>=2`, `r>=d>=2`. This establishes exactly the claimed global minimum-generator formula. The theorem is not the later general Murthy-conjecture claim affected by the Fasel/Mandal errata.

The global height is `d`. Therefore `mu_R(I)=d` if and only if every local count is `d`; substituting the Koszul count gives the displayed `D2` rank threshold. For `d=1`, polynomial ideals are principal and `D2` has no columns. Its rank is zero, and the formula gives `mu_R(I)=1`. There is no unsupported local-to-global step.

## 4. Prior matrix-only mechanism, independent of the D2 theorem

Let `B=C[M_1,...,M_d]`. The regular map `A→B` is injective because a zero multiplication operator kills `1`, and it is onto by definition. Thus `dim B=N` and `ker(f↦f(M))=I`. Recover `B` by repeatedly multiplying a growing span beginning with `Id` by all generators. A stalled step is already closed; otherwise the dimension grows. Degrees through `N-1` suffice. The recovered basis includes the algebra unit internally; its coordinates in the original quotient basis are not needed.

For a support point define `J_lambda=(T_i)B`. The coefficient map `B^d→J_lambda` is an ordinary finite complex-linear map once a basis of `B` is known. A complex-vector-space basis of its kernel also generates the kernel as a `B`-module, since scalar coefficients are elements of `B`. The resulting `d×r` matrix `U` presents `J_lambda`; its `d×d` determinant minors generate `Fitt_0^B(J_lambda)`.

In the selected local factor, `J_lambda` is its maximal ideal. In every other factor, some coordinate difference is a unit, so `J_lambda` is the free rank-one module. Its zeroth Fitting ideal is zero. Localization/product compatibility of Fitting ideals therefore implies that some determinant matrix is nonzero if and only if `Fitt_0` of the selected factor's maximal ideal is nonzero.

Wiebe's original Satz 3, printed p. 260, makes this equivalent to an Artinian local CI. The original p. 258 explicitly defines the ideal using any free-module presentation and states presentation independence. The use of all `d` coordinates is therefore permitted even when they do not minimally generate the maximal ideal. In a reduced singleton factor the maximal ideal is zero and `Fitt_0(0)=B`; the full kernel provides unit determinant columns, as required.

This intrinsic ring test is the fixed-embedding condition used here. KLR's definition preceding Definition 3.1, p. 7, defines the relevant local CI through a regular sequence of length `d` in the given polynomial local ring; Algorithm 3.4, p. 10, explicitly decides generation of `Q P_m` by a regular sequence. Equivalently, a redundant regular embedding contributes eliminable linear parameters before a minimal Cohen presentation. It does not change the CI property.

Mohan Kumar's original Theorem 4, p. 234, bounds the global number of generators of any locally CI ideal in a polynomial ring over a field by the ambient variable count. Height gives the reverse bound. Thus the entire older matrix-only route answers the exact global Boolean target, using the 1969 local criterion and 1978 global theorem, without the candidate's shifted-Koszul rank equation.

The determinant in this route is a determinant over the commutative ring `B`, evaluated as an `N×N` matrix. The check is matrix nonzeroness. It is not invertibility, an ordinary scalar matrix determinant or a determinant of a block matrix. For the dual numbers, the valid determinant can be a nonzero nilpotent multiplication matrix with ordinary determinant zero. The repaired mapping uses the correct meaning throughout.

## 5. Prior reconstruction route, independent of the direct Fitting adapter

Use an actual multiplicative degree-compatible monomial order. Retain exactly the linearly independent evaluations `t(M)`. Dependence propagates to multiples, so the retained monomials form a divisor-closed order ideal. For each border monomial express its evaluation in the retained basis, obtaining a relation in `I` with that monomial as leading term. Division terminates and spans the quotient by the order ideal. That quotient surjects to `A`, where these `N` monomials are independent; dimensions force equality of the ideals. This reconstructs the full `I`, including every nilpotent and support component.

Alternatively, the recovered algebra basis supplies multiplication matrices and a unit vector for the normal-form map in Abbott–Kreuzer–Robbiano 2005, Propositions 2.6/2.8 and Theorem 3.1. Their generalized Buchberger–Möller algorithm explicitly computes the defining Gröbner basis; Remark 3.3 uses the multiplication matrices and unit data. No previously supplied Gröbner basis is assumed.

KLR's 2019 Algorithm 3.6 then computes primary components and applies Algorithm 3.4 to each. Its output is all-local-CI, precisely the fixed regular-embedding property, not the stricter degree-form condition of their later sections. The same verified 1978 global bridge turns this into the literal global target. All input gaps are closed, with no transfer to an unproved theorem.

## 6. Boundaries that falsify tempting extensions

The fresh exact script checks 96 plane staircase quotients, 19 three-variable lower ideals, and four special cases. Expected `H1` counts come from minimal complementary monomials; top homology counts come from maximal staircase monomials. All differentials are built independently by generic wedge contraction, and every CI case has the full binomial Betti vector. The special cases test a four-coordinate nonlinear curvilinear embedding after similarity, a redundant-coordinate non-CI, three mixed nilpotent/reduced support factors, and irrational univariate support. All 119 pass, as does the exact Cartesian-spectrum filter.

An arbitrary commuting tuple can fail the regular quotient promise. Even a faithful transpose representation of a non-Gorenstein quotient can produce the CI second-rank signal while its kernel ideal is non-CI; the saved independent ideal certificates give that concrete example. Such inputs are expressly excluded. Likewise Gorenstein does not imply CI in three variables, and affine CI does not imply strict CI. The candidate's diagnostic examples correctly enforce these distinctions.

These finite checks are corroboration. The preceding deductions and explicitly scoped classical theorems establish the universal claims. Exact algorithms require an effective coefficient field and exact root/equality operations; neither prior route nor candidate claims stable numerical certification of approximate matrices.
