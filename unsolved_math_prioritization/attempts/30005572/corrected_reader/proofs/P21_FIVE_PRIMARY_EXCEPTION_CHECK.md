# The five-exception is not controlled by the printed p≥7 criterion

Shared PASS 4/5. This supplements Section 7–8 of ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md. It is a statement about the character and ambient coefficient module; it does not assert a nonzero value of the actual cocycle.

## 1. An exceptional block away from the level

Take F=Q(√−5), with discriminant −20 and class number 2. The extension M=F(√5) has third quadratic subfield Q(i). Its biquadratic discriminant is (−20)·5·(−4)=400. Since this is Disc(F)², M/F is unramified at every finite place. It is the Hilbert quadratic extension.

The squared mod-five cyclotomic character of G_F cuts out M. Thus it factors through every ray class group Q_N and has order two, even at levels prime to five. At N=(3), unit reduction is injective, so this is already inside the restricted arithmetic theorem, not merely a small-level phenomenon.

The principal auxiliary α=1+3√−5 is 1 modulo (3) and has norm 46. Its ideal c is prime to 5(3), its Artin action at N is trivial, and its smoothing scalar is

(Nc)²−1=46²−1=2115=5·423.

This scalar is a nonunit in Z₅. Every allowed auxiliary has nonunit smoothing factor on the exceptional block; the particular example also realizes valuation exactly one on a principal ray auxiliary.

## 2. Why 5 not dividing h does not automatically kill the localized exception

Keep F=Q(√−5), and take the prime-power ideal level N=(11). The rational prime 11 is inert, since −5 is not a square modulo 11, so q=(11) has norm 121. It is principal, and hence splits completely into two primes in the Hilbert quadratic extension H/F. The quadratic exceptional character χ for H/F has χ(q)=1.

In the source ray field F(q), the primes over q have residue field F₁₂₁. The relative ray inertia has order (121−1)/2=60; the unit quotient is legitimate because unit reduction modulo q is injective. There remain two primes over q, corresponding to the two primes of H. Consequently the arithmetic residue module for the localization at q has two F₁₂₁^× summands, permuted by Gal(H/F). Its χ-part has a nonzero five-primary subgroup, since 5 divides 121−1=120.

Equivalently, the accepted PASS 2 character-support criterion reads χ(q)≡Nq mod5, here 1≡121 mod5. The exact localization sequence is surjective onto this residue module. Projection to the χ-block is exact, so the χ-part of K₂(O_{F(q)}[1/q])⊗Z₅ is nonzero.

Thus 5∤h=2 does not imply vanishing of the exceptional component of this localized coefficient group. The source's p≥7 proof first replaces its localized target by the integer-ring target under (p)|N². That replacement cannot be made in the new ramified-five example, whose level is prime to five.

This does not prove failure of auxiliary removal: the actual smoothed family could still have a zero obstruction in E(M)/δ(M). It prevents an invalid vanishing shortcut.

## 3. Exact checks

The adjacent check_arithmetic_descent.py confirms the finite residue computations, norm 46, valuation of 2115, inertness of 11, the discriminant product, and the scalar-trace gcd used for the vertical residue proof. These checks complement the class-field and localization arguments; they do not replace them.
