# Turn 3: exact quartic phase and a sharper residue test

2026-10-02. Third substantive author turn. The universal primitive-root conjecture is still unresolved. This turn studies the special Gaussian norm p=1+(4q^2)^2, rather than just the factorization of p-1. It obtains an exact phase for a power of3 and identifies precisely why that still does not decide the q-primary order.

## 1. An exact quartic-reciprocity identity

**Proposition.** If q is an integer not divisible by3 and p=16q^4+1 is prime, then

    3^(4q^4) = -4q^2 mod p.

**Proof.** Work in Z[i]. Let pi=1-4iq^2, whose norm is p. It is a Gaussian prime, primary because pi=1 modulo(1+i)^3. The Gaussian prime rho=-3 is also primary, has norm9, and is coprime to pi. Define the quartic symbol (a/pi)_4 as the unique fourth root of unity congruent to a^((Npi-1)/4) modulo pi.

The quartic reciprocity law for relatively prime primary Gaussian primes alpha,beta is

    (alpha/beta)_4 = (beta/alpha)_4 * (-1)^(((Nalpha-1)/4)*((Nbeta-1)/4)).

Here the sign exponent is4q^4*2 and hence even. Consequently

    (-3/pi)_4 = (pi/(-3))_4.

Modulo3, q^2=1, so pi=1-i. Since the residue field Z[i]/(3) has9 elements,

    (pi/(-3))_4 = (1-i)^2 = -2i = i mod3.

The fourth roots of unity remain distinct modulo3, so this determines the symbol as i. Also(-1/pi)_4=(-1)^(4q^4)=1; hence(3/pi)_4=i. In Z[i]/(pi), the equation1-4iq^2=0 gives i=(4q^2)^(-1)=-4q^2 modulo p, using16q^4=-1 modulo p. Under the natural identification of this residue field with F_p, the stated identity follows. QED.

This is a specialization of classical quartic reciprocity, not a claimed new reciprocity theorem. A checked primary reference for the symbol convention and reciprocity law is Wang–Zhang, section5.1, https://zhangshenxing.github.io/publications/WangZhang2022.pdf. It gives the primary convention modulo2+2i, equivalent to modulo(1+i)^3 up to a unit, and the norm-based reciprocity sign. All arithmetic above specifies the primary associates, so there is no hidden sign choice.

## 2. Exact residual target at one quarter of the previous exponent

Now impose the original hypotheses q>3 prime and p=16q^4+1 prime. Put s=-4q^2 modulo p. Then s^2=-1, so s has order4. Define x=3^(4q^3). The proposition gives x^q=s.

The original conjecture fails exactly when3^(16q^3)=1, i.e. x^4=1. Because q is odd, the map y->y^q is an automorphism of the fourth roots of unity. Therefore x^4=1 holds if and only if

    x = s^(q mod4).

Explicitly, a counterexample must satisfy

    3^(4q^3) = -4q^2 mod p    when q=1 mod4,
    3^(4q^3) =  4q^2 mod p    when q=3 mod4.

Conversely either displayed equality forces3^(16q^3)=1 and proves failure of primitivity. Thus this is an exact equivalent obstruction, not merely a necessary condition. The exponent is reduced by a factor4, but no inequality excluding the displayed values has been proved.

The phase identity itself does not force q^4 to divide ord_p(3): a cyclic group of order16q^4 contains elements of every order16q^j,1<=j<=4, with the same prescribed fourth-power phase. The q-part is annihilated by the exponent4q^4, so its determination from that exponent would be circular.

## 3. Octic exploration and its honest boundary

Squaring shows that3^(2q^4) is one of the two square roots of s. The explicit eighth root u=2q satisfies u^4=-1, and u^6=-4q^2=s. Thus

    3^(2q^4) is either 8q^3 or -8q^3 modulo p.

The exact first-turn certified sample exhibits the further sign pattern

    3^(2q^4) = -(q/3)*8q^3 mod p,

where(q/3)=1 forq=1 mod3 and-1 forq=2 mod3. The checker verifies this pattern on all7,669 certified prime cases throughq<=1,000,000. No universal proof of this additional sign pattern is supplied here, and it is not used in any claimed deduction. Even a universal proof would still concern only the 2-primary phase and would not by itself establish primitivity, for the reason proved in TURN_2.md.

## 4. Checks and remaining gap

verify_turn3.py regenerates the exact first-turn primality/primitive certificates, verifies the proved quartic identity, the square-root alternatives, and the observed octic sign on every certified case. It also verifies that neither of the residual equalities occurs in that finite range. This is reproducible finite evidence, not an extension to larger q.

The remaining unproved statement is now exactly the exclusion, for prime q>1,000,000 with p=16q^4+1 prime, of the residue +/-4q^2 at exponent4q^3, with sign selected byq mod4 as above. The special Gaussian norm gives a rigorous exact higher-power phase, but fails to control the surviving q-primary component. Two substantive author turns remain. Completion estimate15% of the universal proof goal, uncalibrated and not a correctness probability.
