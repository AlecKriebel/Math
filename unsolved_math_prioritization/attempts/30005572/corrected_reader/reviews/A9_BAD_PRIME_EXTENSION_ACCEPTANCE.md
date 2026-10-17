# Independent acceptance: proper nonadmissible lower levels

Date: 14 October 2026 UTC. Shared PASS 3/5; row 1777 / 30005572. This verification opens no further mathematical pass and changes no proof.

## Verdict

ACCEPT the frozen restricted extension in `pass3_bad_prime_extension/SMALL_LOWER_LEVEL_BAD_U.md`, SHA-256 `88f9e52d3119a446038789c8352d801e2387d78dd8611ea2a2f326fbe72b5d53`.

For principal q, N=Mq^n admissible, and M proper and q-free, the actual auxiliary bad-U defect has zero norm to F(M), even if M itself does not have injective unit reduction. The source coefficient restriction p>=7 and all existing norm-kernel restrictions remain. This is a real enlargement of the accepted PASS 2 theorem; it is not a full bad-U theorem or a prime-power-level result. No novelty claim is made.

## 1. Where lower admissibility is, and is not, needed

The accepted PASS 2 norm/coset proof is the baseline, including its corrected row lattice, actual geometric representative, full-fiber support check, dual Hecke normalization, and Artin inverse. This audit checks the changed hypothesis rather than silently reusing a descent theorem outside its scope.

With an admissible definition modulus f, source Section 3.1 defines the CM curves, all Hom maps and compatible proper-level torsion markings over F(f), with the marked A-torsion over F(Af). This setup does not require admissibility of A. The latter first enters source Section 4.1 for descent to F(A).

For proper A, the marked point is nonzero. The same sheared support calculation therefore gives a regular specialization at that point and a homomorphism on the strict Gamma_A group with values in K_2(F(Af)) tensor Z_p. The draft does not invoke an arithmetic map to F(A) at a nonadmissible lower level. Its low-level Artin automorphism is explicitly at Af, represented by a congruent to pi modulo A and 1 modulo f.

The strict group remains legitimate geometrically even when central units lie in it. Only at the admissible high level is the source group replaced using the direct-product argument. Thus no invalid low-level direct-product decomposition is assumed.

## 2. The geometric norm and Hecke identities retain their hypotheses

The prime-to-c one-coordinate norm fixes the unsheared primitive. The compatible shears satisfy mu_(Aq) alpha = alpha mu_A, and every point above P_A avoids both support components because its moved first coordinate is xP_A, which is nonzero. This uses properness of A, not unit-injectivity.

Since Af is admissible, relative marked fibers over F(Af) have the full Q or Q-1 size. At the first step the extra A-torsion branch has the inverse Artin action at Af; it is not discarded. The source geometric Hecke class relation is available before descent, and the strict-group double-coset identities require only the congruences already retained.

The missing good-Hecke branch is therefore still sigma_A^(-1)gF. The good dual constant-coefficient eigenvalue remains 1+Q sigma_A^(-1), as follows from the weighted geometric identity after specialization. These two inverse actions cancel exactly in the first-step calculation. At higher levels the Q-branch conjugation propagates norm-zero. Consequently the claimed norm-zero identity over F(Mf) follows for the actual specialized cocycle, without asserting that any lower specialization already descends to F(M).

The unchanged formal identities and their all-component row-ideal membership were independently accepted in PASS 2. No extra component shift arises here because q remains principal.

## 3. Independent CRT and field-transfer calculation

Put V=U_M, X=(O/q^n)^times, and Y=(O/f)^times. The relative ray-class exact sequence gives G=(X×Y)/diag(V). The projections of V to both X and Y are injective: the first uses high-level N admissibility, and the second uses f admissibility.

Inside G, the images of X×{1} and {1}×Y generate G, and their intersection has size |V|. Thus, with K=F(N), B=F(Mf), T=F(Nf), and A=F(M), one gets

K intersect B = A,
[T:KB]=|V|.

The second equality is crucial: this field square is generally not Cartesian before factoring through KB. The displayed degree formulas follow, in particular

[K:A]=Q^(n-1)(Q-1)/|V|.

For z in K_2(K), factor restriction and transfer through C=KB. Transfer from T back to C after restriction multiplies by [T:C]=|V|. The Cartesian C/A square then gives

Cor_(T/B) res_(T/K)(z) = |V| res_(B/A) Cor_(K/A)(z).

This derives the exact correction factor, rather than inferring a field intersection from equal degrees. Both |V| and [B:A]=|Y|/|V| are prime to p: |V| divides 6, while the prescribed definition prime makes |Y| congruent to 1 or 3 modulo p. Therefore the norm-zero identity upstairs descends by legitimate cancellation and restriction injectivity. No arbitrary division, invariant-equals-descent assumption, or hidden change of norm degree occurs.

## 4. Actual vanishing and example

On a source prime-to-p character component trivial on I=Gal(F(N)/F(M)), with p not dividing [F(N):F(M)], I acts trivially and the restriction of the norm is multiplication by that p-adic unit. This proves the stated actual U*=1 equation there. The retained p-Sylow part is not averaged away. Source auxiliary cancellation is used only at the admissible high level and only where an invertible smoothing factor is available.

The example F=Q(i), M=(1+i), q=(3) is valid. All four global units reduce to 1 modulo M; N=Mq is admissible; Q=9; and the relative ray degree is (9-1)/4=2. It confirms that the added hypothesis range is nonempty. It does not compute or claim nonzero K_2 values.

## 5. Acceptance boundary

The exact enlargement is removal of lower-level unit-injectivity while retaining a proper lower level. The following remain outside this result:

- nonprincipal q and the corresponding component assembly;
- a nonadmissible high target level;
- pure prime-power N, whose q-free lower level is O and whose marked point would be the origin;
- noninflated relative characters and p-primary norm kernels;
- wild depth above p where the norm degree is not a unit;
- the five-primary construction and source coefficient improvement;
- unrestricted compactification, integer-ring target improvement and the relative theta formula.

The accepted source/coefficient convention is still Z[1/30] or Z_p for p>=7. This report does not combine this lane with the scalar-five geometric normalization to assert an unproved arithmetic R-valued theorem.

## Sources

Source Sections 3.1–3.4 and 4.1 were directly checked against the retained author manuscript, especially the placement of the admissibility condition and the marked-torsion/Artin rules:

https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf

The original construction remains UNSOLVED.
