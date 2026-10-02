# Turn 4: a three-by-three resolvent construction with explicit regularization error

**Disposition: a constructive matrix-valued workaround for compact inputs, with a certified error bound; not the requested stronger scalar/positive-factor extension.** The general operator-valued subordination and self-adjoint linearization method is existing work of [Belinschi–Mai–Speicher](https://arxiv.org/abs/1303.3196), Theorem 2.2, Corollary 3.6 and Theorem 4.1, building on Anderson. It predates the OWR question. Here it is specialized and the commutator's regularization error is derived explicitly. No novelty is claimed for the general method.

## 1. Deterministic linearization

Let a,b be bounded self-adjoint elements in a tracial probability space, and put c=i(ab-ba). No symmetry or centering is imposed. Define self-adjoint scalar coefficient matrices

    M = E_12+E_21,
    N = E_13+E_31,
    Q0 = -i E_23+i E_32,

and the self-adjoint pencil

    L = Q0 + M tensor a + N tensor b
      = [[0,a,b], [a,0,-i], [b,i,0]].

The lower two-by-two corner Q=[[0,-i],[i,0]] satisfies Q^2=I, and

    [a,b] Q [a,b]^T = -i(ab-ba) = -c.

Therefore the Schur complement of the lower corner in diag(z,0,0)-L is z-c. For every z in the upper half-plane,

    [(diag(z,0,0)-L)^(-1)]_11 = (z-c)^(-1).       (1)

This is an exact identity in any unital algebra where the indicated resolvent exists; freeness is not used in this step.

## 2. Positive-imaginary regularization and its exact error

Let epsilon>0 and define Lambda_epsilon(z)=diag(z,i epsilon,i epsilon). Its imaginary part is strictly positive. The inverse of the lower corner i epsilon I-Q is

    (-i epsilon I-Q)/(1+epsilon^2).

The upper-left block of the regularized inverse is consequently

    R_epsilon(z)
      = [z-c/(1+epsilon^2)
           + i epsilon(a^2+b^2)/(1+epsilon^2)]^(-1).      (2)

If eta=Im(z)>0, the operator in brackets has imaginary part at least eta I. Hence its inverse has norm at most 1/eta. The ordinary resolvent R_0(z)=(z-c)^(-1) obeys the same bound. Subtracting their inverses and applying the resolvent identity gives

    ||R_epsilon(z)-R_0(z)||
       <= [epsilon^2 ||c|| + epsilon ||a^2+b^2||]
          / [(1+epsilon^2) eta^2]
       <= [2 epsilon^2 A B + epsilon(A^2+B^2)]
          / [(1+epsilon^2) eta^2],                      (3)

where A>=||a|| and B>=||b||. Taking the trace preserves this bound. In particular the limit epsilon down to zero is uniform on any region Im(z)>=eta_0>0 for fixed input norm bounds. The limit is not asserted uniformly as eta approaches zero, and no density estimate on the real axis follows from (3) alone.

There is no sign ambiguity in (2): the regularization adds a positive imaginary multiple of a^2+b^2. Reversing that sign would destroy the coercivity argument. The exact controls explicitly check this sign in noncommuting examples.

## 3. Incorporating freeness through existing subordination theory

Now suppose a and b are free. In the amplified space with expectation E=id_(M3) tensor trace, put X=M tensor a and Y=N tensor b. They are free with amalgamation over M3: entries of alternating conditionally centered matrix words are sums of alternating centered scalar words, whose traces vanish. Their matrix Cauchy transforms are determined solely by the separate input laws:

    G_X(W)=integral (W-xM)^(-1) dmu_a(x),
    G_Y(W)=integral (W-xN)^(-1) dmu_b(x),

for matrices W with Im(W)>0. These integrals are entrywise integrals of bounded resolvents.

Apply the cited subordination theorem at D=Lambda_epsilon(z)-Q0, which still has strictly positive imaginary part. With h_X(W)=G_X(W)^(-1)-W and similarly h_Y, its fixed-point characterization is

    Omega_X(D)=lim_k f_D^k(W),
    f_D(W)=h_Y(h_X(W)+D)+D,
    G_(X+Y)(D)=G_X(Omega_X(D)).                         (4)

The theorem supplies the analytic upper-half-plane branch, uniqueness and convergence from any W in that half-plane; these facts are credited inputs, not deduced from a numerical iteration here. Its companion equation gives Omega_Y, with Omega_X+Omega_Y-D=G_(X+Y)(D)^(-1).

Because D-X-Y=Lambda_epsilon(z)-L, the (1,1) entry of (4) is trace(R_epsilon(z)). Combining this with (3) recovers G_c(z) from the input measures with an explicit bound for the final regularization step. This does not supply a certified stopping bound for a finite fixed-point iteration; that separate numerical error must not be confused with (3).

## 4. Boundary checks and scope

- All compactly supported self-adjoint input laws are covered, including nonsymmetric, noncentered, atomic and deterministic laws; there is no variance division
- The exact block identity and norm bound require no freeness. Freeness is used only in the subordination step recovering the law from separate inputs
- Constant or commuting examples have c=0 and reduce at epsilon=0 to the scalar resolvent 1/z, though the auxiliary regularization can still have nonzero error for epsilon>0
- Arbitrary noncommuting finite matrices in the checker test the deterministic identity. They are not treated as freely independent random variables, and no finite-matrix spectral scan is claimed to prove the free-probability statement
- The known subordination theorem is applied to bounded X,Y. An extension to unbounded laws is not silently assumed in this turn

This construction escapes Turns 1–3 precisely because its auxiliaries are matrix-valued and its final scalar transform is obtained by a regularized resolvent limit. It does not establish the OWR scalar mapping-class or positive-factor representations in new generality. The general approach was already available before the report, which is further reason not to label this a full solution.

## 5. Status

The new retained derivation is the explicit commutator pencil, its exact regularized Schur complement, and the fully quantified operator-norm error (3), combined transparently with a credited existing theorem. `verify_turn4.py` checks formal noncommutative coefficient signs and exact finite-matrix identities and bounds; it does not run floating-point fixed-point approximations.

Estimated completion toward the source's full requested representation: 20%, low confidence. Four genuine author turns are complete; one remains. The next issue is controlling input truncation for arbitrary laws without conflating this workaround with the report's stronger desired format. Independent review is pending.
