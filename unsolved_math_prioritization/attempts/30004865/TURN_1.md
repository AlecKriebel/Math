# Turn 1: a Werner state invisible to every unreshuffled local Hilbert tester

**Complete negative candidate for the source's central completeness question; 1/5 substantive author turns.** This proof covers every pair of complex-linear S1-to-Hilbert contractions, with arbitrary and unequal finite output dimensions. It also covers the larger class of real-linear maps on Hermitian matrices that are contractions on pure-state projectors. It does not depend on the preprint's ancillary real-to-complex extension assertion.

The Werner family and the failure thresholds of the two fixed realignment/SIC tests are prior results, explicitly discussed in Jivulescu–Lancien–Nechita Section8.2. The additional claim proved here is a uniform bound over **all** local testers. No novelty certification is claimed. The separate broad multipartite comparison and classification questions are not declared exhausted by this counterexample.

## 1. Main explicit counterexample

On C3 tensor C3 let F(x tensor y)=y tensor x be the flip and define

    rho=(19 I−9 F)/144.                                  (1)

Then rho is an entangled density matrix, but for every pair of maps

    E:S1^3 -> H_A,    G:S1^3 -> H_B,
    ||E||_(1->2)<=1,   ||G||_(1->2)<=1,

where H_A,H_B are arbitrary finite-dimensional complex Hilbert spaces,

    ||(E tensor G)(rho)||_(H_A tensor_pi H_B)<=1.         (2)

The scalar trace map is an allowed tester and gives value1, so the supremum over all these testers is exactly1. Thus (1) cannot be detected by any member of the source's unreshuffled family.

We prove a more general interval result below, using a finite second-moment identity rather than any numerical optimization.

## 2. A finite ensemble of pure projectors and its exact second moment

Fix d>=2. Let Q be a random rank-one orthogonal projector constructed by this finite distribution:

- With total probability 1/(d+1), choose one of the standard basis projectors uniformly.
- With total probability d/(d+1), choose z_1,...,z_d independently and uniformly from {1,i,-1,-i}, put v=d^(-1/2)(z_1,...,z_d), and take Q=|v><v|.

Then

    E(Q tensor Q)=(I+F)/(d(d+1)).                       (3)

To check (3) entrywise, for the flat vectors the (i,j;k,l) tensor coordinate is d^(-2) E(z_i conjugate(z_j) z_k conjugate(z_l)). Independence of the fourth-root phases makes this expectation1 exactly when the multisets {i,k} and {j,l} agree; otherwise it is0. Each individual phase exponent lies between -2 and2, so no extra fourth-root congruence case occurs. If all four indices coincide, the flat term contributes1/(d(d+1)) and the basis term contributes the same amount. If the multisets agree but there are two distinct indices, only the flat term contributes1/(d(d+1)). These are exactly the entries of I+F with its double diagonal count. This proves the identity over C with no design-existence assumption.

Let G_0=I/sqrt(d),G_1,...,G_(d²−1) be any Hilbert–Schmidt orthonormal basis of the real vector space of Hermitian matrices, with G_a traceless for a>0. The expansion Q=sum_a r_a G_a has real coefficients r_a=Tr(QG_a). From (3),

    E(r_a r_b)=(Tr(G_a)Tr(G_b)+Tr(G_a G_b))/(d(d+1)).    (4)

In particular E(r_0²)=1/d, E(r_a r_b)=delta_(a,b)/(d(d+1)) for positive indices, and the cross moments with index0 vanish.

## 3. The tester energy budget

Let L be a real-linear map from Hermitian d-by-d matrices to a real or complex Hilbert space and assume only

    ||L(Q)||_2<=1 for every rank-one orthogonal projector Q. (5)

Every required complex-linear tester satisfies (5), because ||Q||_1=1. Set

    u_L=||L(G_0)||_2,
    S_L=sum_(a=1)^(d²−1) ||L(G_a)||_2².

Expand L(Q) using the real coefficients r_a. Applying (4), including the real parts of inner products if the Hilbert space is complex, gives the exact identity

    E||L(Q)||_2²=u_L²/d+S_L/(d(d+1)).

Consequently

    u_L²/d+S_L/(d(d+1))<=1.                             (6)

No assumption of unitarily covariant, symmetric, positive, identical, informationally complete or fixed-output-size testers has been used. In particular averaging the input projectors does not replace an arbitrary tester by a symmetric one.

## 4. Uniform bound for the Werner interval

For -1<=f<=1 define

    rho_f=a I+b F,
    a=(d−f)/(d(d²−1)),    b=(df−1)/(d(d²−1)).           (7)

Here I is the identity on Cd tensor Cd. On the symmetric and antisymmetric subspaces its eigenvalues are

    a+b=(1+f)/(d(d+1)),
    a−b=(1−f)/(d(d−1)),

with multiplicities d(d+1)/2 and d(d−1)/2 respectively. Thus rho_f is positive semidefinite, trace1, and Tr(F rho_f)=f.

For every product density matrix A tensor B,

    Tr(F(A tensor B))=Tr(AB)>=0.

The last inequality follows by writing Tr(AB)=Tr(A^(1/2) B A^(1/2)). By convexity it holds for every separable state. Therefore rho_f is entangled whenever f<0. This elementary witness is sufficient here; no converse separability theorem is needed.

The Hilbert–Schmidt Hermitian basis obeys the tensor identity

    F=sum_(a=0)^(d²−1) G_a tensor G_a.                   (8)

Indeed its coefficients against G_b tensor G_c are Tr(F(G_b tensor G_c))=Tr(G_b G_c)=delta_(b,c). Since ad+b=1/d, equations (7)-(8) become

    rho_f=(1/d)G_0 tensor G_0+b sum_(a>0)G_a tensor G_a. (9)

Let E and G be any two maps satisfying (5), with their respective Hilbert codomains. The projective norm of a simple tensor is the product of the two Hilbert norms. Apply its triangle inequality to (9), then ordinary Cauchy–Schwarz to the sum over a>0:

    ||(E tensor G)(rho_f)||_pi
       <= u_E u_G/d + |b| sum_(a>0)||E(G_a)|| ||G(G_a)||
       <= u_E u_G/d + |b| sqrt(S_E S_G).                (10)

If |b|<=1/(d(d+1)), a second Cauchy–Schwarz inequality and (6) give

    RHS(10)
       <= (u_E/sqrt(d))(u_G/sqrt(d))
          +(sqrt(S_E)/sqrt(d(d+1)))(sqrt(S_G)/sqrt(d(d+1)))
       <= sqrt(u_E²/d+S_E/(d(d+1)))
          sqrt(u_G²/d+S_G/(d(d+1)))
       <=1.                                            (11)

From (7), the condition is equivalent to |df−1|<=d−1, or

    2/d−1 <= f <=1.                                    (12)

Combining these statements proves:

**Theorem.** For every d>=3 and every f in [2/d−1,0), rho_f is entangled but no pair of local Schatten-1-to-Hilbert contractions, of any finite output dimensions, detects it without input index permutation. Its optimized tester value is exactly1, attained by the scalar trace testers. The same non-detection holds under the weaker local assumption (5).

For d=2 the interval [2/d−1,0) is empty, so no two-qubit counterexample is inferred.

## 5. Explicit rational instance and exact entanglement certificate

Take d=3,f=-1/6. Then a=19/144 and b=-1/16, which is exactly (1). Its symmetric eigenvalue is5/72 with multiplicity6; its antisymmetric eigenvalue is7/36 with multiplicity3. Both are positive and their weighted sum is1. The flip expectation is -1/6. Moreover |b|=1/16<1/12, so (11) applies with a strict coefficient margin. The proof is about a full-rank, strictly entangled mixed state, rather than a boundary or limiting non-state.

In the source's parameterization

    sigma_mu=mu(I+F)/(d(d+1))+(1−mu)(I−F)/(d(d−1)),

one has f=2mu−1. The interval is mu in [1/d,1/2). Section8.2 of the primary paper already notes that its two fixed testers fail there. Equations (3)-(11) establish the stronger universal failure across all allowed testers. Merely repeating the two fixed norm calculations would not prove this theorem.

## 6. Multipartite and unequal-dimension consequences

For m>2, tensor rho_f with arbitrary local density matrices tau_3,...,tau_m. It is not fully separable: tracing out the last parties gives the entangled rho_f. For any local testers, the output is the tensor product of the first two-party output and the local vectors E_j(tau_j). Those local vectors have norm at most1, by the trace-norm contraction, or by convexity under (5). The projective norm is multiplicative for adjoining simple tensor factors, so the whole output norm is at most1.

This gives unreshuffled counterexamples for every m>=2 with two equal local dimensions d>=3. If two desired local dimensions are larger than d, embed the respective Cd spaces isometrically. The induced matrix embedding X->VXV* preserves the trace norm; composing a tester with it preserves contractivity. Non-detection therefore persists in these larger dimensions. Entanglement persists as well: local compression back to the supported Cd subspaces takes a hypothetical separable decomposition to a separable one. Equivalently the embedded flip witness has nonnegative expectation on all product states and negative expectation on the embedded rho_f.

These examples need not be genuinely multipartite entangled. Their relevance is to the source's full-separability completeness question. No tensor-power activation, local filtering with postselection, or index-permuted tester family is included in the theorem.

## 7. Verification and remaining scope

verify_turn1.py supplies exact finite second-moment and rational Werner certificates, plus finite controls for the two Cauchy–Schwarz budgets. None of the universal quantifiers is inferred from a numerical search: arbitrary testers are covered by the analytic energy inequality.

The central completeness question has a complete negative candidate at this first author turn, pending independent review. The source's additional broad requests about classification and relative performance of fixed testers on mixed multipartite states remain separate; this proof does not claim a general comparison theorem for them.
