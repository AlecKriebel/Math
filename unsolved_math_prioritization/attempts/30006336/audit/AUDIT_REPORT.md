# Independent adversarial audit: rank 629 / 30006336

Date: 2026-10-04. Exact catalogue identifier: OWR-14299291-005.

## Verdict

**PASS as an unresolved, source-qualified research checkpoint. NOT a resolution.**
The appropriate disposition remains `unsolved`, with five recorded approaches and
an explicit prior-announcement/novelty hold. The first-order divisibility and
countercontrols survive independent mathematical checking. No fatal mathematical
error was found in the frozen note. No counterexample to the actual geometric
statement, all-order proof, or independently verified proof-bearing prior theorem
was obtained. The announced theorem must be credited, without upgrading an
announcement to an inspected proof or asserting that the literature remains open.

This audit binds only the original 12-file author packet with
`SHA256SUMS.json` digest
`05a9835d5c4c302afe24c47d6143096301ce658e7bd29e4fef884f2c2a2705c8`.
Eleven payload hashes plus the manifest itself are listed in `AUTHOR_BINDING.json`.
Originals were not edited. No remote writes or auxiliary research workers were
used. This is an AI-assisted adversarial review, not expert peer review.

## 1. Exact source and scope

The official [Oberwolfach report](https://doi.org/10.4171/OWR/2025/29),
pp. 1532–1534, was read, including Theorem 2 and all of section 4. The source
requires smooth proper X over Z_p, vanishing of global degree-i forms on its
special fibre, and a dense affine open U. Section 4 asks for vanishing in the
maximal-ideal-separated prismatic quotient, reports only a fixed I-squared
coefficient calculation, and explicitly leaves the general extension unchecked.
It does not ask for zero in unrestricted integral prismatic cohomology.

The author's explicit interpretation uses the bounded Breuil–Kisin prism
A=Z_p[[u]], phi(u)=u^p, d=u-p, I=(d), m=(p,u)=(p,d). This is a valid standard
base for A/I=Z_p; the short source does not itself specify this Frobenius and
coordinate. Its choice is therefore an explicit convention, not a verbatim
source datum. It introduces no demonstrated contradiction or extra geometric
hypothesis. The non-separated quotient is M/(intersection of m^n M), not an
unjustified inverse limit of derived coefficient cohomology groups.

In particular, neither density on the special fibre nor good compactification
may silently be added. Those conditions belong to different nearby questions.
An empty formal open contributes zero. For nonempty X, the degree-zero vanishing
hypothesis is vacuous; the substantive cases have positive degree. No p>2 or
large-p restriction is needed in the checked first-order argument.

## 2. Independent reconstruction of the first-order argument

Let K_X be the pushed-forward relative prismatic complex and let
Kbar_X=K_X tensor^L_A A/d. The Hodge–Tate comparison gives
H^j(Kbar_X)=Omega^j of the formal scheme, tensored with the invertible base
line (I/I^2)^(-j). This is the comparison of cohomology sheaves, not an asserted
splitting of the whole complex. The relevant references are
[Bhatt–Scholze](https://arxiv.org/abs/1905.08229), Theorem 1.8(2),
Remark 1.11 and Theorem 6.3.

Write F=Omega^i_{X/Z_p}. Smoothness makes F locally free and p-torsion-free.
Properness makes H^0(X,F) finite over Z_p. The long exact sequence for reduction
modulo p injects H^0(X,F)/p into H^0(X_Fp,F_Fp)=0. Nakayama and proper formal
functions therefore kill H^0 of the formal differential sheaf as well. Tensoring
with the invertible line over the base cannot change this vanishing.

To make the edge-map step explicit, the hypercohomology filtration in total
degree i has graded terms from H^a(Xhat,H^b(Kbar_X)), a+b=i. On the affine
formal target Uhat all terms with a>0 vanish, by coherent affine acyclicity.
Functoriality thus kills the positive filtration pieces, and the only possible
remaining piece factors through H^0(Xhat,H^i(Kbar_X)), already zero. Equivalently,
the natural edge maps give a commutative square with an isomorphism at Uhat.
No global Hodge–Tate spectral-sequence degeneration is assumed or needed.

Because A/d is the perfect two-term cone of d on A, reduction commutes with
RΓ here. The coefficient triangle on Uhat gives the exact identity

    ker[H^i(C_U) → H^i(C_U tensor^L_A A/d)] = d H^i(C_U).

Restriction and reduction commute. Consequently the author's inclusion
image[H^i(C_X) → H^i(C_U)] subset d H^i(C_U) is correct, integrally, with
torsion allowed. Importantly, this kernel identity does not assume d-injectivity
on the cohomology group. The statement is a consequence of the known comparison
and is not presented as new research.

## 3. Attempts to force higher orders

The triangle through successive d-power coefficients is valid because d is a
non-zero-divisor in A. A lift in target cohomology need not come from source
cohomology. Multiplication-by-d on A itself is already a finite free, separated
control: its reduction modulo d is zero while its image is not in m^2 A.
Therefore the first-order argument alone cannot be iterated.

The conditional sheaf lemma is valid with its stated d-injectivity, global
quotient-section vanishing and natural affine edge-isomorphism assumptions.
A bounded-below complex is a clean setting for its edge maps. These assumptions
have not been supplied for the integral prismatic cohomology sheaf. Without
d-injectivity the sequence 0 → F[d] → F → dF → 0 supplies a possible H^1(F[d])
obstruction to lifting a global section through division. This is a real missing
step, not a proof of failure in the geometric situation.

The cited Frobenius and Nygaard statements are genuine: Theorem 15.3 gives the
Frobenius-twisted affine prismatic complex as the décalage L eta_I, and
Theorem 1.8(6)/Corollary 15.5 gives inverse Frobenius up to I^i. None of these
statements licenses cancelling powers of d on torsion or replacing iterated
phi(d) by d. Over this base phi^r(d)=u^(p^r)-p. On the toy module A/(u), each
acts as -p, so p belongs to every individual divisor image but not m^2 M.
This module has not been equipped with all geometric/prismatic structures and
cannot be advertised as a target counterexample. Independent controls also
check that the product of r+1 such factors has order r+1; this emphasizes the
difference between separate divisibilities and a product divisibility estimate.

The exact remaining requirement is unchanged: for every restricted integral
class y and every n≥1, establish y in m^n H^i(C_U), with torsion and topology
controlled. The audit supplies no such all-order argument.

## 4. Countercontrols and topology

All written elementary controls are correct in their declared scope:

- d^N is nonzero of m-adic order N, but vanishes modulo (d^N,p^s) for every s.
  Fixed d-thickness, even with every p-adic level, does not detect a zero map.
- u(u-p) vanishes at u=0 and u=p and is still a nonzero map on the free module A.
  The two specializations do not detect zero morphisms, even between perfect
  complexes in degree zero. This does not deny conservativity for testing an
  isomorphism via other hypotheses.
- A/(p) disappears after p-inversion but is nonzero integrally.

For R=Z_p<T>, the continuous derivative maps R into R dT. Both terms are flat
p-complete Z_p-modules; the two-term complex is derived p-complete. The form
omega=sum_{n≥1} p^n T^(p^n-1) dT lies in R dT. If it were the derivative of a
restricted series, the coefficients at T^(p^n) of that series would all be 1.
They do not tend to zero. Multiplication by any nonzero scalar a changes those
coefficients to the same nonzero a, and yields the same contradiction.
Thus its cohomology class is nonzero and is killed by no nonzero Z_p scalar.

For each k, subtracting the derivative of sum_{1≤n<k} T^(p^n) leaves p^k times
a restricted one-form, because the tail coefficients have valuations n-k tending
to infinity. This proves the claimed nonzero class belongs to every p^k H^1.
It disproves automatic separatedness of cohomology, not derived completeness of
the complex. It does not produce compatible successive divisions and does not
produce a restriction from a smooth proper source. Finite truncations alone
cannot prove the infinite coefficient contradiction.

## 5. Literature and prior-announcement hold

The [Strasbourg announcement of 2 October 2025](https://www.math.unistra.fr/seminaires/seminaire-arithmetique-et-geometrie-algebrique-2025.html)
explicitly announces a separated integral-prismatic restriction result for
smooth proper p-adic schemes over a prism. Its global-form hypothesis is met in
the packet's setting by the proper/Nakayama argument. Its short abstract is not
a proof and does not specify every topology convention.

The [Princeton/IAS announcement of 20 October 2025](https://www.math.princeton.edu/events/restriction-map-cohomology-2025-10-20t193000)
also announces a separated-prismatic result, and separately describes a stronger
statement modulo I-torsion involving H^1 of differential forms. Its prose begins
with a projective source; it is not by itself a checked all-smooth-proper theorem.
Those extra assumptions must not be imported into the original separated target.

[Caro–D'Addezio, arXiv:2511.11444](https://arxiv.org/abs/2511.11444),
Theorem 1.3.2, attributes the separated crystalline/de Rham restriction theorem
and the bibliography lists the joint EKP manuscript as in preparation. This is
an attribution in that version, not proof of the manuscript's current absence.
Their negative comparison results answer a distinct comparison problem and do
not refute the present separated-prismatic assertion.

A bounded fresh search of the [Petrov](https://sasha-pt.github.io/),
[Esnault](https://page.mi.fu-berlin.de/esnault/helene_publ.html), and
[Kisin](https://people.math.harvard.edu/~kisin/preprints.html) public lists and
the exact manuscript title did not locate a full proof. Petrov's linked February
2026 course notes were also checked; they do not supply this prismatic theorem.
An additional [Milan announcement from February 2025](https://matematica.unimi.it/it/seminario-esnault)
mentions a weaker prismatic version and adds historical context only. None of
these bounded negative searches establishes nonexistence of a manuscript.

Fresh private downloads of the OWR report, Bhatt–Scholze paper, and
author-hosted Caro–D’Addezio paper match all three frozen source hashes.
The separate arXiv PDF was also read at the relevant statements. Its internal
date differs from the author-hosted copy; the theorem and bibliography checks
above agree in scope. Fingerprints are recorded in `SOURCE_CHECKS.json`.

## 6. Replay and evidentiary limits

Both original verifier scripts were read before running and passed. Their 88
controls consist of 32 thickening, 4 specialization, 28 Frobenius-divisor, and
24 finite differential identities. Independent code, without importing either
original script, passes 655 controls on primes 2,3,5,7,11: 480 thickening
quotients, 5 specializations, 40 individual Frobenius divisors, 40 products,
50 differential-tail identities, 30 scalar-primitive coefficient tests,
5 distinguished-generator computations, and 5 localization controls.

`verify_audit.py` checks the full exact author binding and audit payload manifest,
then reruns all three control/manifest scripts. These checks protect reproducibility
and elementary identities only. They do not formalize comparison theorems, prove
the infinite statements by enumeration, substantiate novelty, or establish any
resolution. The repository's live duplicate searches were not rerun: no remotes
were used, and the author's repository-state assertions remain outside this audit.

The portable audit contains analysis, URLs, source metadata, code and result
summaries only. No source PDF, source full text, catalogue corpus or private
coordination content is included.
