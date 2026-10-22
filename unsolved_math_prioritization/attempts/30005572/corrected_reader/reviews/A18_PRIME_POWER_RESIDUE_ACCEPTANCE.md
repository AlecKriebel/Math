# Independent acceptance: q-adic residue reduction and exact smoothing target

14 October 2026 UTC. Row 1777 / 30005572. Review within the final shared PASS5/5, not a sixth pass. No author proof, ledger, queue, or remote was edited by the reviewer.

## Verdict and final inputs

ACCEPT the restricted results in:

- `pass5_prime_power_integrality/CONGRUENCE_KERNEL_AND_SMOOTHING_RESIDUES.md`, SHA-256 `db401a8da74c019f6ee3c7ec856b212d5a0cbce76027591cb69603ed3bcb5b8d`.
- `pass5_prime_power_integrality/EXCEPTIONAL_FIVE_EXAMPLE.md`, SHA-256 `5cfa8d47078c8a72b8959ea4d294ee504b47130c030d0015797b8180a7214b31`.

The first proof starts with the actual previously constructed arithmetic maps at proper unit-injective prime-power level. It retains all Bianchi components. It proves a q-adic continuity/kernel-restriction equivalence for their residue homomorphisms and computes the common smoothing annihilator and quotient of the exact arithmetic residue module. The second gives an actual arithmetic example where the ambient five-lines occur.

No actual surviving cocycle residue is evaluated or proved zero. No prime-power integer-ring target, unrestricted compactification, or failure of the intended construction follows. The original problem remains UNSOLVED.

## 1. The starting residue and its group action are correct

The prior accepted localization theorem identifies the target residue module as

    M = Ind_<kappa>^C F_(Q^f)^times tensor Z[1/6],

where C is the full ordinary class group and kappa is arithmetic Frobenius at q. This is the actual residue module of F(q^n), inflated from the Hilbert class field. Inertia acts trivially; kappa acts on the local cyclic summand by Q. The whole module has order prime to 6 and to the residue characteristic ell.

The arithmetic cocycle restricts to a homomorphism on strict Gamma1, because its coefficient action there is trivial. A coefficient coboundary therefore restricts to zero, so the residual homomorphism is independent of the chosen cocycle representative. This does not presume existence of any unaugmented block that remained open in PASS4.

The source-sign arithmetic representative is retained explicitly. With the standard tame map fixed, negating the cocycle inverts its multiplicative residue. All new conclusions concern kernels, images, module actions, or vanishing, and are unchanged by that sign conversion. No explicit positive theta-pair residue is equated with the source-sign arithmetic residue.

## 2. The q-adic reduction is valid on every component

At q, every projective rank-two component lattice is free. A basis compatible with its primitive level marking puts the reduction of strict Gamma1 in upper-triangular form with bottom row (0,1). The other diagonal entry is the reduction of a global unit, because the determinant of an automorphism of the projective lattice is a global unit.

The reduction modulo q has an ell-group unipotent part and a diagonal part of order dividing |O^times|. The kernels in successive q-power reductions are ell-groups. Hence every finite q-adic congruence quotient has prime divisors only among ell,2,3, including nonprincipal components and nonprincipal q.

For any homomorphism rho from this arithmetic group to M, the quotient of its full image by the image of a principal q-adic congruence subgroup is simultaneously a quotient of that congruence quotient and a subquotient of M. Their orders are coprime. Thus every arbitrarily deep q-adic congruence subgroup has exactly the full image of rho.

This proves the equivalence between zero rho, factorization through one finite q-adic quotient, and q-adic continuity into discrete M. It does not prove any of those properties for the actual rho.

## 3. The kernel-restriction isomorphism is exact, with the correct terminology

Every homomorphism to finite M extends uniquely to the full profinite completion. Its q-adic closure has only finite quotients with order supported at ell,2,3: any continuous finite quotient factors through some q-power matrix quotient.

Positive-degree continuous cohomology of this closure with M coefficients vanishes. Indeed continuous cochains factor through finite quotients, and their orders act invertibly on M, permitting the usual finite-group averaging. The continuous Hochschild–Serre low-degree sequence therefore gives the stated isomorphism

    Hom_cont(Gamma-hat,M) = Hom_cont(C_r(q),M)^(G_r).

The invariant restriction class uniquely determines rho and is an exact reformulation of the missing residue calculation.

C_r(q) is the kernel of the map from the full profinite completion to the q-adic closure. It is a q-adic congruence kernel and can contain other-prime information. A nonzero class on it must not be described as a globally noncongruence class. The accepted result is precisely a q-adic continuity/kernel-restriction reduction.

## 4. Scalar auxiliary operators leave only one possible five

A principal scalar ideal (t) has trivial ordinary ideal class, so its Artin action on M is the identity, even if its full ray class is nontrivial. Its smoothing operator on M is t^4 - 1.

For allowed t prime to 5N, those scalars generate 5R. Every one is divisible by five; CRT supplies one with exact five-adic valuation one. For every p >= 7 a nonzero fourth non-root modulo p can be combined with the required coprimality conditions, excluding p from the common divisor. Factors two and three are already units in R.

Consequently M[J] is contained in M[5], and 5M is contained in JM. This assertion is about the actual action on M. It does not assert that five belongs to the original ideal of the full ray group ring. That distinction is needed because the principal scalar ray class need not be trivial before inflation to C.

## 5. Full conductor scope and nonsemisimple induction

If q lies over five, M has no five-part and both modules vanish. Otherwise the squared mod-five cyclotomic character has value Norm(a)^2 at every allowed auxiliary Frobenius.

If F(sqrt(5)) is not contained in H, the two extensions are disjoint over F because the former is quadratic. Chebotarev gives an allowed auxiliary prime trivial in H and nontrivial in F(sqrt(5)). Its smoothing operator is then a nonzero scalar on both M[5] and M/5M, proving vanishing.

If F(sqrt(5)) lies in H, the character descends to the full C. The accepted conductor calculation shows this occurs exactly when five ramifies in F. Auxiliary primes outside the fixed set 5N realize every element of C, so their operators impose g = psi(g) on the residual module. This is not a restriction to the principal ray subgroup or a deletion of class-group characters.

Both M[5] and M/5M are induced from the one-dimensional local residue module on which kappa acts by Q modulo five. The psi-eigenspace is computed by the induction/coinduction adjunction, and the psi-coinvariant quotient by the corresponding tensor adjunction. Each has dimension one exactly when psi(kappa) = Q; otherwise each is zero. These adjunctions hold in characteristic five even when C has a nontrivial five-Sylow subgroup. No averaging over C, semisimple decomposition, or class-number division occurs.

Since psi(kappa) = Q^2, the remaining condition is Q = 1 modulo five. Thus the common annihilator and quotient are both zero unless five ramifies in F and Q is congruent to one modulo five. In that case both are one-dimensional F5 modules with the unramified quadratic character psi. A basis of either line is not canonically chosen.

## 6. The concrete exceptional example checks

For F = Q(sqrt(-5)), the two reduced forms of discriminant -20 give C = C2. The prime (11) is inert because -5 is not a square modulo eleven. Its norm is 121 and its ideal class is trivial. Hence f = 1, and the prime-power residue module over R has two cyclic order-five summands, interchanged by the nontrivial class.

The auxiliary ideal (3,1+sqrt(-5)) has norm three and is nonprincipal, as the norm form does not represent three. It is prime to 5(11), and its smoothing operator is 9 minus the swap, namely minus identity minus swap modulo five. Its kernel is the anti-diagonal and its image the diagonal. The general theorem makes those the common annihilator and common image for all auxiliaries. Both the annihilator and quotient have the nontrivial C2 character.

These are actual ambient arithmetic residue modules, not merely abstract group models. The example does not evaluate the image of any normalized cocycle or establish nonexistence of a compatible unaugmented class.

## 7. Smoothing quotients and integrality are not conflated

The final wording correctly distinguishes M/JM from the compatible-family existence obstruction E(M)/delta(M) of PASS4. M/JM measures the failure of the auxiliary operators to generate the identity on M. Its nonzero line is not an evaluation of the actual family's existence obstruction.

If two already constructed calibrated unaugmented maps exist, their residue difference takes values in M[J]. Outside the exceptional five-case their residues must agree; they may still be the same nonzero residue. On a part where J acts as the unit ideal, Bezout gives the unique residual unaugmentation of a compatible family, but does not show it is zero.

The -23/q^2 example has an order-seven residue target and no smoothing ambiguity, yet the actual unaugmented residue remains uncomputed. This accurately preserves the distinction between unique calibration and integer-ring values.

## 8. Vertical residues, specialization, and the surviving analytic gap

The local example Z = {u,x} is correct. Its vertical tame residue over a DVR is trivial because both entries are units at the generic point of the special fiber. Pulling back along x = pi gives {u,pi}, whose arithmetic tame residue is the reduction of u. The closed point of the section meets the deleted horizontal divisor.

Therefore vanishing of the good-model vertical residue cannot replace the source's reduced-point avoidance hypothesis. LSSW Lemmas 4.2.2–4.2.3 were inspected directly: the source proves both steps separately and excludes level primes from the prime-power target at the avoidance step.

Gabber rigidity concerns K-theory with finite invertible coefficients for a henselian pair. It neither moves a class across a deleted horizontal divisor nor automatically proves q-adic continuity of this group cocycle. The restriction in the report is therefore appropriate. Theorem 1.4 was independently checked in the author-hosted Clausen–Mathew–Morrow manuscript: https://www.imo.universite-paris-saclay.fr/~matthew.morrow/Clausen,%20Mathew,%20Morrow,%20K-theory%20and%20TC%20of%20Henselian%20pairs.pdf . The initially cited Rochester mirror timed out during this review; the author-hosted source was accessible.

The whole moved-primitive difference must still be controlled near the closed marked point. Its two terms need not specialize separately, and the already known raw swap transition or denominator potential does not establish the required continuity on any component, much less all mixed CM products.

## 9. Reproducibility

The author checker was read. Its initial assertions were replaced by explicit RuntimeError checks before final freeze, so optimization does not remove validation. The repaired checker was copied to this audit directory and independently replayed under ordinary Python, -O, and -OO; stdout is identical and the complete result matches the author's result byte for byte. It verifies 204 induced-module cases, including 190 with nontrivial class-group five-part, and finite congruence examples.

These tests support the finite group calculations. They do not prove q-adic continuity, evaluate a congruence-kernel class, or replace the actual arithmetic construction. The proof and example above are accepted only with their explicit limitations.
