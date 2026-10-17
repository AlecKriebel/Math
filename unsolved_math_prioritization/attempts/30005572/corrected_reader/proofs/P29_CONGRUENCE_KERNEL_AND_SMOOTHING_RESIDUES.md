# Exact congruence-kernel and smoothing obstructions for actual prime-power residues

14 October 2026 UTC. Final shared PASS 5/5, row 1777 / 30005572. Authored partial result; no novelty claim. The construction contract remains UNSOLVED.

## 1. Actual input and conclusions

Let F be imaginary quadratic, O its integer ring, R=Z[1/6], N=q^n a proper unit-injective level, Q=Norm(q), ell its residue characteristic, H the Hilbert class field, L=F(N), C=Gal(H/F), and kappa the arithmetic Frobenius of q in C. Set f=ord(kappa). Retain every Bianchi component and its actual PASS4 arithmetic auxiliary map. The target obstruction is the accepted module

  M = T_q(L) tensor R = Ind_<kappa>^C F_(Q^f)^× tensor R,

inflated to G=Gal(L/F). It has h/f cyclic summands and exponent the prime-to-6 part of Q^f−1. In particular |M| is prime to 6 ell.

The new results are:

1. On every component, a nonzero actual residue homomorphism has exactly the same full image on every arbitrarily deep q-adic principal congruence subgroup. Its restriction to the q-adic congruence kernel determines it uniquely, with an explicit restriction isomorphism. Hence proving finite q-adic dependence of the actual residue would prove full vanishing, but this dependence is NOT established here.
2. Let J denote the operators Norm(c)^2−R_N(c) for all proper auxiliaries c prime to 5N. Then both the common-annihilator M[J] and the quotient M/JM vanish except in the single situation

  5 ramifies in F and Q is congruent to 1 modulo 5.                 (1.1)

In situation (1.1), each is exactly one copy of F_5, with the unramified quadratic character of F(sqrt(5))/F. This retains the full possible 5-part of C; no class-number division or semisimple decomposition at 5 is used.

Neither theorem identifies the actual surviving residue class as zero. The second describes the precise common kernel and image quotient of the residue smoothing operators; it is not a divisibility theorem for the actual arithmetic family.

Throughout, use the source-sign arithmetic cocycles z_src=−z_std specified in the PASS4 sign addendum, while tau is the standard tame symbol. Changing the signed cocycle inverts its multiplicative residue and leaves all kernels and vanishing statements below unchanged. No positive raw theta pair is silently identified with a positive source-sign cocycle.

## 2. The actual residual homomorphisms

For a class component r, let Gamma_r=Gamma_1(N)_r in the source's strict convention, and let

  rho_(c,r)(gamma) = tau_q(z_(c,r),N(gamma)) in M.                (2.1)

On Gamma_r the arithmetic coefficient action is trivial, so (2.1) is an actual homomorphism. The same definition applies to every already constructed unaugmented block or map. It is independent of the arithmetic cocycle representative: a coefficient coboundary restricts to zero on Gamma_r. Existence of the full unaugmented map is not assumed where PASS4 left it open.

For a compactified map already justified separately, its arithmetic integrality is still equivalent to rho=0. Killing topological cusp homology does not kill M. At −23/q² the nonzero relative edge residue j-bar² is not a value of (2.1).

## 3. All q-adic congruence quotients are harmless, including nonprincipal components

Choose a q-adic basis of the rank-two projective O-lattice of component r. Every fractional ideal becomes free over O_q, so this is legitimate also when q or the component ideal is nonprincipal. Choose the basis compatibly with the level marking. It identifies Gamma_r with a subgroup of GL_2(O_q) whose reduction modulo q has the form

  [ a  b ]
  [ 0  1 ],

where a is the reduction of a global unit in O^×. This follows from the strict Gamma_1 condition and from det(gamma) in O^×. Changes of the chosen local basis conjugate the groups and do not affect their orders or conclusions.

For m>=1 put K_r(m)=ker[Gamma_r -> GL_2(O_q/q^m)]. If necessary one may start at m>=n; the conclusion for all m follows by taking a deeper subgroup.

### Theorem 3.1

Every finite quotient Gamma_r/K_r(m) has order dividing a product of powers of ell and |O^×|. In particular its order is prime to |M|. For every homomorphism rho:Gamma_r->M,

  rho(K_r(m)) = rho(Gamma_r) for every m.                        (3.1)

Consequently the following are equivalent:

(a) rho is zero;
(b) rho factors through some finite q-adic congruence quotient;
(c) rho is continuous for the q-adic topology on Gamma_r and the discrete topology on M.

Proof. Modulo q the image is an extension of a subgroup of the additive group O/q by a subgroup of the image of O^×. The former is an ell-group. The global unit order is 2, 4, or 6. Each successive kernel modulo q^(j+1) over modulo q^j embeds into the additive group of 2-by-2 matrices over O/q and is an ell-group. Thus all prime divisors of the displayed quotient order belong to {ell,2,3}.

The quotient rho(Gamma_r)/rho(K_r(m)) is both a quotient of Gamma_r/K_r(m) and a subquotient of M. Its order must be one. This proves (3.1). If rho factors through one congruence quotient, its kernel contains K_r(m), so (3.1) forces zero. Continuity into the finite discrete group implies its kernel is open and therefore contains some K_r(m); the converse and zero case are immediate. QED.

This does not assume the congruence subgroup property. On the contrary, it isolates exactly where a possible nonzero residue must live.

### Theorem 3.2 (exact congruence-kernel class)

Let Gamma-hat_r be the full profinite completion, let G_r be its image in GL_2(O_q), equivalently the q-adic closure of Gamma_r, and set

  C_r(q)=ker[Gamma-hat_r -> G_r].

For M with trivial Gamma action, restriction induces an isomorphism

  Hom_cont(Gamma-hat_r,M)
       --> Hom_cont(C_r(q),M)^(G_r).                            (3.2)

Thus the actual obstruction (2.1) is equivalently the explicitly defined invariant class

  epsilon_(c,r) = rho-hat_(c,r)|C_r(q).                          (3.3)

No class epsilon_(c,r) is evaluated or proved zero here.

Proof. Every homomorphism from Gamma_r to finite M has finite-index kernel and extends uniquely to its full profinite completion. The finite quotients of G_r have order supported on ell,2,3 by the preceding proof. For every such finite quotient, positive-degree group cohomology with M coefficients is zero: averaging by its order is an invertible operation on M. Continuous cochains with finite coefficients factor through finite quotients, so H^i_cont(G_r,M)=0 for i>0. The low-degree continuous Hochschild–Serre sequence for C_r(q) in Gamma-hat_r now gives (3.2), since the two outer terms H^1(G_r,M) and H^2(G_r,M) vanish. QED.

In particular, a nonzero value cannot disappear after passing to a sufficiently deep congruence level. For every m and every value in its image there exists a gamma_m congruent to the identity modulo q^m with exactly that residue. This is a consequence of (3.1), not an assertion that any such nonzero value has been found.

## 4. The exact smoothing module at prime-power level

Write J-action for the family of endomorphisms

  s_c = Norm(c)^2−R_N(c) acting on M,

with c proper and prime to 5N. Define M[J]=intersection_c ker(s_c), and JM=sum_c s_c M. All these operators factor through C because inertia acts trivially on M.

### Lemma 4.1 (only a single five can remain)

The principal scalar auxiliary operators generate multiplication by 5 on M. More precisely, the ideal of R generated by t^4−1 as t ranges over positive integers greater than one prime to 5N is 5R. Consequently

  M[J] is contained in M[5], and 5M is contained in JM.           (4.1)

Proof. The ordinary ideal class of (t) is trivial, so R_N((t)) acts as identity on M, regardless of its possibly nontrivial ray class. Since Norm((t))=t², its operator on M is t⁴−1. Every allowed t is a 5-adic unit, so 5 divides every t⁴−1. Choose t congruent to 2 modulo 25 and prime to every rational prime dividing N, using CRT. This gives v_5(t⁴−1)=1. For each rational p>=7, choose a nonzero residue u modulo p with u⁴!=1 and choose an allowed t congruent to u modulo p; if p divides N this still makes t prime to N. Hence no such p divides the common ideal. The only inverted primes are 2 and 3. The nonzero ideal generated by this set in R is therefore exactly 5R, and its generator is a finite R-linear combination of the scalar operators. QED.

### Theorem 4.2 (exact target ambiguity and quotient)

If (1.1) fails, then

  M[J]=0 and M/JM=0.                                           (4.2)

If (1.1) holds, let psi:C->F_5^× be the quadratic character of H/F cutting out F(sqrt(5)). Then

  M[J] is isomorphic to F_5(psi),
  M/JM is isomorphic to F_5(psi).                              (4.3)

The isomorphisms are module isomorphisms; choosing a nonzero vector is not canonical.

Proof. By Lemma 4.1 the annihilator is computed in M[5] and the quotient in M/5M. If 5 divides Q, both are already zero. Suppose henceforth q does not lie over 5.

Let psi_5 be the square of the mod-five cyclotomic character of G_F. At an auxiliary prime a, psi_5(Frob_a)=Norm(a)² modulo 5. Chebotarev, allowing the fixed finite set 5N to be avoided, gives two cases.

If F(sqrt(5)) is not contained in H, there exists an auxiliary prime a whose Frobenius in H is the identity and whose psi_5-value is −1. Therefore s_a acts on M[5] and M/5M by the nonzero scalar −1−1 modulo 5. The two modules in (4.2) vanish.

If F(sqrt(5)) is contained in H, psi_5 descends to psi on C. Chebotarev realizes every element of C by auxiliary primes, so modulo 5 the ideal of smoothing operators is exactly the ideal imposing g=psi(g) for all g in C. Thus M[J] is the psi-eigensubspace of M[5], and M/JM is the psi-coinvariant quotient of M/5M.

The containment F(sqrt(5)) subset H holds exactly when 5 ramifies in F. This is the accepted PASS4 conductor calculation: in the ramified quadratic local field, norms of residue units are squares, making the squared mod-five cyclotomic character trivial on inertia; it is unramified elsewhere. When 5 is unramified in F, its inertia restriction at five is nontrivial. The extension is nontrivial for imaginary quadratic F.

It remains to compute the two dimensions without dividing by |C|. If 5 does not divide Q^f−1, M[5] and M/5M are zero. Otherwise both have the induced form

  Ind_<kappa>^C V,

where V is a one-dimensional F_5-space on which kappa acts by Q modulo 5. This follows either from the explicit integral presentation or directly from the cyclic residue-field summands. For the eigenspace use Frobenius reciprocity for induction of finite groups (which also equals coinduction); for the quotient use the elementary coinvariant adjunction. Both have dimension one if psi(kappa)=Q modulo 5, and dimension zero otherwise. Neither adjunction requires semisimplicity or a class-number inverse.

Since psi is the cyclotomic square and q is away from 5,

  psi(kappa)=Q² modulo 5.

The condition is Q²=Q, equivalently Q=1 modulo 5. In that case 5 does divide Q^f−1, so the induced module used above is nonzero. This proves (4.2)–(4.3). QED.

### Consequences for the actual family, with the correct limitation

On every constructed block, applying tame residue to auxiliary exchange yields an actual compatible smoothed family in Hom(Gamma_r,M). On any target part on which J is the unit ideal, its residual unaugmentation is unique and obtained by a finite Bezout combination. It need not vanish: unique solvability of the smoothing equations is distinct from integrality.

If two already existing unaugmented maps satisfy the same calibration, their difference after tame residue takes values in M[J]. Therefore the arithmetic integrality of calibrated choices cannot differ at all unless (1.1) holds; in that case their possible difference is confined to the one line F_5(psi). We do not assert that this entire ambient line is attained by differences of genuine K2-valued maps.

Likewise the nonzero quotient in (4.3) measures failure of J to act as the unit ideal on M. It is not identified with the full compatible-family existence obstruction E(M)/delta(M) defined in PASS4, and it is not a proved nonzero obstruction for the actual family. At −23/q², 5 is unramified and M=F_8^× has order seven, so J acts with unit ideal and the unique actual unaugmented residue remains to be computed. The old scalar t construction at p>=7 is recovered, while the exact five-primary exception is now identified on the full residue module.

## 5. Why good-model transport and rigidity do not yet finish the calculation

Exact canonical model transport proves that (2.1) is the right arithmetic map. Zero vertical residue on the good surface model, proved in PASS4, does not prove its value is integral when the marked section meets a deleted horizontal divisor in the special fiber. At prime-power level the marked torsion reduces to the origin, precisely the point removed from the relevant open.

The elementary local example makes the logical gap explicit. Let V be a DVR with uniformizer pi and residue field k, choose u in V^× with nontrivial reduction, and on the generic affine line take

  Z={u,x} in K2(Frac(V)(x)).

At the generic point of the vertical special fiber, u and x both have valuation zero, so Z has trivial vertical tame residue. But the section x=pi is generically disjoint from x=0 and its specialized value has

  tau{u,pi}=u-bar.

Thus it can have nonzero arithmetic residue. The section's special point lies on the deleted horizontal divisor x=0. This is exactly why one cannot replace the source's reduced-point avoidance condition by mere generic regularity.

Gabber rigidity applies to K-theory of a henselian pair with finite invertible coefficients. It does not put Z into the K2 of the local ring at the deleted point, nor identify the moved geometric cocycle with a continuous cocycle of GL2(O_q). The theorem needs a class on that henselian ring or an explicitly controlled localization problem. Also, passing to an arbitrarily large unramified field and then using K1/p is unsafe for detecting the original p-torsion residue: a finite-field p-torsion element can become p-divisible in the larger residue field although its multiplicative image remains nonidentity.

The outstanding comparison can be stated exactly as follows. For every component r, every auxiliary c, and every target prime p>=5 dividing Q^f−1, prove that the actual map (2.1) has finite q-adic dependence (equivalently prove epsilon_(c,r)=0 in (3.3)). Alternatively compute a nonzero epsilon through an actual evaluated group element. It is NOT enough to prove this for the horizontal C1 boundary, the raw unshifted swap symbol, or the fixed same-curve denominator potential.

For the source's exact moving identity,

  Theta_(mu eta)(gamma) = Theta_eta(gamma mu)−Theta_eta(mu),

the complete difference is regular at the generic marked point. Its two terms need not specialize separately. The missing local theorem must control this whole expression near the closed marked point, including the normalized shear transitions and all E_r×E_1 products. The swap and theta-pair potential already proved do not establish that control.

## 6. Sources, dependencies, and verification boundary

Read and used at their accepted scope:

- PASS2 ABSOLUTE_INTEGRALITY_AND_RESIDUES and its independent acceptance: exact Hilbert-class residue module and arithmetic localization.
- PASS3 EXACT_THETA_RESIDUE_TEST and normalization addendum: the actual local edge example, including F8 constants.
- PASS4 ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL, FIVE_PRIMARY_EXCEPTION_CHECK, and OPEN_HOMOLOGY_GOOD_HECKE: actual R-valued auxiliary maps and exact exceptional-five conductor.
- PASS4 EXACT_SWAP_AND_CYCLIC_FOUR and CYCLIC_FOUR_RAY_FIELD_DESCENT: genuine swap calibration and its stated missing moved-cocycle comparison.
- PASS4 GERSTEN_SIGN_TRANSPORT_ADDENDUM and MODEL_TRANSPORT_SCOPE_CLARIFICATION: signs and the product-coordinate scope are preserved.
- LSSW, Eisenstein cocycles for imaginary quadratic fields, retained author manuscript, §§4.2 and 5.2, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf. Its reduced-point avoidance hypothesis is essential at the cited step.
- Clausen–Mathew–Morrow, K-theory and topological cyclic homology of henselian pairs, Theorem 1.4 (statement of Gabber rigidity), https://people.math.rochester.edu/faculty/doug/otherpapers/CMM.pdf. This is used to delimit an attempted application, not as a proof of the missing continuity claim.

The finite checker verifies small congruence images and the smoothing eigenspace/coinvariant dimensions for cyclic and noncyclic class-group models, including a nontrivial 5-Sylow. It does not replace the arithmetic descent, continuous Hochschild–Serre theorem, or the unproved actual cocycle calculation.

No existing accepted file, queue, ledger, or remote was changed. No new mathematical pass after this final shared PASS5 is requested or implied.
