# Turn 2: a precise limit of congruence/reciprocity arguments

2026-10-02. Second substantive author turn. The original exponent-four conjecture remains unresolved. The results below are theoretical obstruction results for broader approaches, not a counterexample to the original conjecture. Sixteen-adic character information and even exact local valuations do not by themselves force the needed q-primary order. A related prime-power-family counterexample is certified separately.

## 1. Infinitely many compatible bad primes for each fixed q

**Proposition.** Fix a prime q>3. Set M=96q^5 and a=16q^4+1. There are infinitely many primes r with

    r = a mod M,
    3 is a qth power modulo r.

Their natural density among all primes is 1/[32q^5(q-1)]. In particular they have r=5 mod12, v_2(r-1)=4 and v_q(r-1)=4, but 3 is not a primitive root modulo r.

**Proof.** Write E=Q(zeta_q,3^(1/q)) and C=Q(zeta_M). The polynomial x^q-3 is Eisenstein at3, so Q(3^(1/q)) has degree q. Its intersection with Q(zeta_q), whose degree is q-1, is Q. Since the cyclotomic extension is Galois, the compositum E has degree q(q-1). It is the splitting field of x^q-3, with Galois group the full affine group F_q semidirect F_q^*. The translation subgroup U, of order q, is the kernel of restriction to Q(zeta_q).

The commutator subgroup is U. Indeed the quotient by U is abelian, so the commutator subgroup is contained in U. If tau is translation by1 and sigma has multiplier2, then sigma tau sigma^(-1) tau^(-1)=tau, so the commutator subgroup contains U. Therefore the maximal abelian subextension of E/Q is precisely Q(zeta_q).

As C/Q is abelian and contains Q(zeta_q), we obtain E intersection C=Q(zeta_q). The residue class a is coprime to M: it is odd, nonzero modulo q, and a=2 mod3. Thus it defines a cyclotomic automorphism sigma_a of C. Since a=1 modq, sigma_a restricts to the identity on Q(zeta_q). Therefore there exists a unique automorphism gamma of EC restricting to identity on E and sigma_a on C. This follows from the fiber-product description of the Galois group over the common intersection.

This gamma is central: conjugation leaves its E-component equal to identity, and leaves its C-component unchanged because Gal(C/Q) is abelian. Its conjugacy class is a singleton. Chebotarev's density theorem now gives the set of unramified rational primes with Frobenius gamma density

    1/[EC:Q] = 1/[q phi(M)] = 1/[32q^5(q-1)].

For such a prime r, its cyclotomic Frobenius implies r=a modM, and its trivial E-Frobenius means x^q-3 splits completely modulo r. In particular3 is a qth power. Since q divides r-1, every qth power in F_r^* has order dividing(r-1)/q, so3 is not primitive.

Finally r-1=16q^4(1+6qk) for some integer k. The last factor is odd and equal1 modulo q, giving the exact two valuations. Also r=a=5 mod12. QED.

The standard Chebotarev theorem used here: in a finite Galois extension of Q, unramified primes with Frobenius in a conjugacy class K have natural density |K|/|G|. See J.S.Milne, *Algebraic Number Theory*, Theorem8.31, https://www.jmilne.org/math/CourseNotes/ANTc.pdf; the Dirichlet-density proof is in *Class Field Theory*, Theorem7.4, https://www.jmilne.org/math/CourseNotes/CFT.pdf. The Kummer splitting interpretation is also standard in Artin primitive-root theory, e.g. https://web.math.ucsb.edu/~agboola/teaching/2005/winter/old-115A/murty.pdf.

### What this does and does not prove

This proposition does NOT produce a counterexample p=16q^4+1. For a fixed q it supplies primes r=16q^4+1+96q^5 k, typically with k>0. The original problem picks the single value k=0 and lets q vary. There is no logical passage from an infinite set of r for every fixed q to that diagonal choice. Its purpose is exact: a proof retaining only these congruences and exact v_2/v_q data cannot conclude the desired qth-power nonresiduacity, because those same data occur for infinitely many bad primes.

## 2. Two-power characters cannot detect the missing q-factor

Let G be cyclic of order16q^4, with generator g. Choose c in{1,3,5,...,15} satisfying qc=1 mod16, and put h=g^(qc). As q is prime>3, c<16 need not be coprime to q; choose instead any positive integer c congruent q^(-1) mod16 and not divisible by q, which always exists. Then gcd(qc,16q^4)=q, so h has order16q^3 and is not a generator.

For every homomorphism chi:G->mu_16,

    chi(h)=chi(g)^(qc)=chi(g),

because qc=1 mod16. Thus all characters of order dividing16, including quadratic, quartic, octic and sixteenth-power characters, can agree on a generator and a non-generator of index q. Such character data alone cannot prove the full order. This does not rule out a more refined reciprocity argument exploiting the integer equality p-1=16q^4.

## 3. A rigorously certified neighboring-family counterexample

The tempting broader assertion that3 is primitive whenever q>3 is prime and r=16q^m+1 is prime is false. It is already false for

    q=5, m=42,
    r=3,637,978,807,091,712,951,660,156,250,001.

Here N=r-1=16*5^42, and base6 supplies a complete Lucas primality certificate:

    6^N = 1 mod r,
    6^(N/2) = r-1 mod r,
    6^(N/5) = 505004010963654974860773778891 mod r,
    gcd(6^(N/2)-1,r) = gcd(6^(N/5)-1,r) = 1.

By the lemma proved in TURN_1.md, r is prime and6 is primitive. But3 has exact order

    D=16*5^41=727595761418342590332031250000,

as witnessed by

    3^D = 1 mod r,
    3^(D/2) = r-1 mod r,
    3^(D/5) = 505004010963654974860773778891 != 1 mod r.

Because the only prime factors of D are2 and5, these certify exact order D, of index5. All values are checked by verify_turn2.py using exact standard-library integer arithmetic. This is an author-constructed certificate for the adjacent exponent42 family, not the exponent4 target and not a historical-priority claim.

## 4. Historical near-match checked

G.Wertheim, *Primitive Wurzeln der Primzahlen von der Form 2^x q^lambda+1, in welcher q=1 oder eine ungerade Primzahl ist*, Acta Mathematica20(1896), pp143–152, https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5021-11511_2006_Article_BF02418029.pdf, does NOT prove the present exponent4 assertion. Printed p145 treats lambda>1 by testing the appropriate residue, whereas the explicit universal claim printed p148 that3 is primitive for16q+1 concerns lambda=1. This primary-source near-match cannot legitimately be promoted to a solution for16q^4+1.

## Remaining target and turn count

The exact finite theorem through q<=1,000,000 remains as in TURN_1.md. The universal statement still requires proving, for every larger prime q with p=16q^4+1 prime, that3^(16q^3) is not1 modulo p; equivalently it must exclude orders16q,16q^2,16q^3. Neither the Chebotarev result nor the neighboring exponent42 certificate settles that diagonal assertion. Three substantive author turns remain. Completion estimate10% of the original universal proof target, uncalibrated and not a probability.
