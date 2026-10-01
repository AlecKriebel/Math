# Determinant-line convention in the Morita detection argument

This note records an ambiguity in scalar shorthand, a precise basis test, and the invariant formulation used in this review. It concerns the complete primary preprint KMP, arXiv:2609.12951v1, PDF SHA-256 `4baea31ded214f94ed9e3f5a7d6f83bafc91c7b868e9e7833663f43c08e30898`, especially p.4, Notation3.2 and the displayed coproduct. It does not assert that Theorem A is false.

## 1. Two different normalizations

Write a(v_1,...,v_n) for the ordinary apartment class in St(V), and D(V)=top exterior power of V. The wedge-normalized twisted class is

    z(v_1,...,v_n)=a(v_1,...,v_n) tensor (v_1 wedge ... wedge v_n).

Permuting the listed vectors multiplies both factors by the same sign, so z is invariant under that permutation. By contrast, with a fixed nonzero generator omega of D(V), the symbol

    a(v_1,...,v_n) tensor omega

changes by the permutation sign. AMP's basic twisted symbols are defined as ordinary sharblies tensored with a fixed generator 1; KMP Notation3.2 instead explicitly uses the basis wedge. A scalar formula must distinguish these conventions.

## 2. Exact basis-transposition witness

Set n=6, a=2, b=4, V=Q^6 and W=span(e_1,e_2). Compare the bases

    v=(e_1,e_2,e_3,e_4,e_5,e_6),
    w=(e_1,e_3,e_2,e_4,e_5,e_6).

Their wedge-normalized twisted apartments are equal. If the displayed ordinary shuffle sign is applied literally while every bracket is separately wedge-normalized, the W-component of the output from v is

    + z(e_1,e_2) tensor z(bar(e_3),bar(e_4),bar(e_5),bar(e_6)),

whereas the output from w is its negative. The unique (2,4) shuffle selecting positions 1,3 is odd. The target tensor is nonzero. Thus that bare scalar interpretation is not a well-defined linear map on the declared twisted module. This test addresses the actual (2,4) specialization, not only an irrelevant odd-rank case.

## 3. The natural invariant map

There is a canonical isomorphism

    D(W) tensor D(V/W) -> D(V),

sending a wedge in W followed by lifts of a quotient wedge to their concatenated wedge. The result is independent of the chosen lifts. Let iota_W be its inverse.

Take the ordinary apartment coproduct Delta^0 and tensor its W-component with iota_W. This defines

    Delta^det_W = Delta^0_W tensor iota_W.

It is well-defined and GL(V)-equivariant because both constituent maps are natural. In a basis for which W is spanned by the selected a vectors and sigma is the corresponding shuffle,

    iota_W(v_1 wedge ... wedge v_n)
      = sign(sigma) (v_sigma(1) wedge ... wedge v_sigma(a))
        tensor (bar(v_sigma(a+1)) wedge ... wedge bar(v_sigma(n))).

The ordinary apartment coproduct contributes the same sign(sigma). Consequently, in the wedge-normalized z notation, the two signs cancel and the fully expanded component has coefficient +1. In fixed determinant generators omega_W, omega_(V/W) compatible with omega_V, the formula instead retains the ordinary shuffle sign on the ordinary apartment factors. This is exactly the change of normalization which the scalar witness requires.

The identification with AMP can be checked at the standard subspace W_0=Q^a. Choose its coordinate determinant generator, the quotient coordinate generator, and their concatenation in Q^n. In these fixed generators, the degree-zero sharbly formula of AMP Definition2.7 is precisely the ordinary apartment shuffle formula tensored with iota_(W_0). Thus the two maps agree on the Steinberg-module W_0-component. The integral general linear group acts transitively on rational a-dimensional subspaces: their intersections with Z^n are saturated direct summands. Equivariance therefore identifies the whole induced-module map from this single component. The induced group-homology map is independent of which resolving complex realizes that module map, as KMP also notes. Hence the invariant coproduct used here is AMP's coproduct, rather than an unproved replacement required to have a Hopf property.

Changing compatible determinant generators changes only coordinate representatives of this same map. We do not use the inconsistent bare interpretation identified in Section2.

## 4. Compatibility with the actual duality and restriction maps

Project the ordinary coproduct to the summand W. On a cellular apartment, only flags passing through W remain; the flags before and after W are the joined apartment flags for W and V/W. This is Reeder's apartment restriction map, with at most the uniform chain/join orientation sign. Tensoring with the canonical determinant-line isomorphism gives the determinant-twisted Reeder map. Thus the comparison in KMP Lemma3.4 is valid in invariant determinant-line notation.

This is not an arbitrary new replacement for the cohomological restriction map. It is the same ordinary apartment map, tensored with its natural coefficient-line isomorphism. KMP Theorem3.3 identifies that restriction map under Bieri–Eckmann duality. Projection to the Levi factor and the fiber integration of Section2 then give Theorem3.5 in these invariant coordinates. All global orientation signs below are harmless for nonvanishing.

For the relevant standard splitting, det(Q^6) is identified with det(Q^2) tensor det(Q^4) in that order. The unipotent subgroup U=Mat_(2,4)(Z) has orientation character det(A)^4 det(C)^(-2)=1. Hence its top rational cohomology is the trivial one-dimensional module. There is no extra determinant twist on H_8(GL_6(Z);Q).

## 5. The nonzero pairing is unchanged

Let nu_n=n(n-1)/2. Let t_2 and t_4 be the Bieri–Eckmann images of the degree-zero unit classes, so their Steinberg homological degrees are 1 and 6. AMP's determinant-twisted Hopf algebra has primitive t_2,t_4. Its invariant product and coproduct therefore satisfy

    Delta_(2,4)(t_2 t_4)=t_2 tensor t_4.

The swapped tensor lies in the different (4,2) rank summand. Endpoint terms have one rank zero. Thus this component cannot cancel. The graded swap sign is also positive here, since (nu_2+2)(nu_4+4)=30, but the distinct rank summands already suffice.

Put x=BE_6^(-1)(t_2 t_4). It has ordinary cohomological degree 15-(1+6)=8. The invariant restriction/coproduct comparison gives

    integration_U(res_(P_(2,4))(x))=plus or minus 1

in H^0(GL_2(Z) times GL_4(Z);Q), with compatible unit normalizations. KMP Lemma2.4 identifies this with top-degree restriction to U, up to sign. Evaluating on the fundamental class of U=Z^8 consequently gives

    <x, inclusion_*[U]> = plus or minus 1, hence nonzero.

This proves the needed detection of the specified unipotent cycle using the credited duality, restriction and Hopf inputs. It does not depend on the ambiguous scalar notation. The elementary determinant-line normalization is the only reconciliation made here; no homological theorem beyond the stated primary inputs is invented.

## Review implication

The source statement, class identification and k=2 nonvanishing can be accepted with this explicit invariant convention. A public packet should retain this note, and should not say that the literal wedge-normalized shuffle display was independently verified as written. Both KMP and AMP remain preprints as recorded in the source audit. This check is not a claim of peer review, community validation, or a new campaign proof of the general Morita theorem.
