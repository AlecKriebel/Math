# Checkable priority comparison

The exact target is the prescribed-map equivalence P1 and the canonical saturation step P2 in COMPARISON.json. Known general theorems can be composed with a new application; the mere existence of an old general theorem does not identify an earlier publication of that application.

## Dependency boundary

1. For a chosen completed local rule F, the output-forbidden input language B is regular and upward closed under taking contexts. Passing to a large enough canonical approximation T[n] makes every other extension rule agree with F. This is elementary; Ballier's Lemma2.1 already uses SFT approximation normalization.
2. If F(T[n]) lies in T, the language of that irreducible SFT is LT and separates L(T) from B.
3. The converse needs a conversion. An LT separator is an arbitrary union of profile classes, while L(T[n]) consists of all words locally consistent with the allowed n-blocks. The authored conversion pads a bad word, uses the ideal property to keep it bad, and uses irreducibility to force the same profile set as an allowed universal word. This is P2.
4. [PRZ2014 Theorem4.2](https://lmcs.episciences.org/1163/pdf), pp.8–9, supplies the separator bound after P1 is established. It does not state P1 or P2. The older arXiv v1 Theorem3, p.6, has a two-monoid product bound. Both are properly prior machinery.
5. Thus neither a citation to general LT separation nor an SFT-membership algorithm alone is a complete priority match. A genuine match must supply the missing application, an equivalent regular-ideal/local-neighborhood theorem, or a stronger prescribed steady-map theorem with the same quantifiers.

This is an audit comparison, not a claim that the application is original.

## A precise obstruction to a naive conversion

Let A={a,b,c} and C={a,b}* union {b,c}*. C is factorial, prolongable and LT: membership means that at least one of a,c is absent. Its associated shift is the union of two full shifts. For every n≥1, w_n=a b^n c is not in C, although every length-n factor of w_n is in C and extends to a point of that union. Therefore the associated shift is not SFT. Merely treating a generic factorial LT separator as an SFT language is invalid. The candidate's irreducibility-dependent padding mechanism addresses a real logical conversion; this example does not refute that mechanism.

## Why density approximation is not the same test

For the binary even shift E, L(E) excludes 010. The LT language D of finite words avoiding 010 contains L(E). Among binary words of length m, the fraction avoiding 010 is at most (7/8)^floor(m/3), by testing disjoint blocks. Hence D and L(E) have limiting density0. Nevertheless 01110 lies in D and outside L(E). A constant outer density approximation D, together with the empty inner approximation, loses this exact bad-word obstruction. This distinguishes [Sin’ya–Yuyama2025 Definition7](https://arxiv.org/pdf/2506.14134), p.5, from disjointness of a separator and B. It does not characterize all possible consequences of the unread2022 paper.

The even identity map also has no SFT-neighborhood extension: for each n, a periodic sequence made from 0 followed by a sufficiently long odd run of1s is n-locally E-admissible but violates E. Thus density approximability cannot replace exact steadiness in this control.

verify_comparison.py checks finite instances of these two explicit word constructions. Their universal conclusions follow from the arguments above; no finite cutoff is used as evidence for a new theorem.

## Quantifiers and boundaries

Ballier's cover-based statements impose closing/continuing conditions or assert existence of a map with such properties. They do not automatically classify the given f. In the target, onto is used to turn image inclusion into equality; irreducibility is used for padding and strong connectivity; nonempty two-sided finite-alphabet hypotheses are retained. Neither the separate existence-over-f question16.2 nor classification of stable CA limit sets16.1 follows from testing each fixed input code. No present-day global openness claim is made.
