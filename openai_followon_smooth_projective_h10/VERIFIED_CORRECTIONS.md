# Explicit corrections used in the arithmetic audit

Status: technical substitutions checked and reconciled in the completed integration audit (reviews/dependency_integration.md). Complete-package and priority review gates remain pending. Pinned input is adc7f1241b42e322a6451854ab7e4b4c146bf78a. The upstream clone is unchanged.

## Coefficient prime for the non-CM height argument

Construct the source's prime-independent corrected action at primes 5 and 2. Apply published Pan Theorem1.0.4 at5, rather than the new unrestricted modularity companion at2. Its hypotheses are checked from the geometric Tate module after the finite splitting field: continuity, absolute irreducibility, oddness, finite ramification, potential semistability and distinct Hodge–Tate weights. Compare prime-independent algebraic Frobenius traces to identify r2 with the same weight-two form. Use r5 to compute the conductor away from5 and r2 at5. The modular-factor/Faltings and final height deductions then apply unchanged. The standalone derivation is manuscript/height-repair.tex. Its geometric inputs concern the five fixed discriminant210 quotient branch values, never arbitrary five points.

## Universal Euler convention in the non-CM cyclotomic argument

Let Lambda=Z2[[t]], O be the completed localization at(2), G a fixed finite elementary two-group, and gamma_q the cyclotomic group-like unit. Put Z_q=theta_q gamma_q, with theta_q²=1, and P_q(Z)=1-(a_q/q) Z+(1/q)Z², the determinant on the actual local inertia-cohomology module V_h(-1). Comparing inverse Frobenius conventions requires the ratio

    r_q = P_q(Z_q)/(Z_q² P_q(Z_q^-1)).

Both denominators are O[G]-units in the construction. Since q is odd,

    P_q(Z)-Z²P_q(Z^-1) = ((q-1)/q)(1-Z²)

is divisible by2. Consequently r_q-1 belongs to2 O[G], and

    U_q = 1+((r_q-1)/2)(1+g_q)

is integral before character evaluation. It equals r_q when q is unused and1 when q is active. Multiply the universal inverse-convention class first by V_Q=product gamma_q², then by product U_q. At an unused character this changes the inverse Euler factor to the intended direct factor; at an active character it adds just gamma_q², an integral unit with central value1. No factor of2 is lost per prime. The central determinant formula and its valuation bound are unchanged.

For smoothing integers c,d, put A_c±=c²-c gamma_c±1, B_c=gamma_c A_c-, and R_c=A_c+/B_c. The identity

    A_c+ - B_c = c(c+1)(1-gamma_c)

gives R_c=1 modulo2 and R_c(0)=1; the same holds for d. Multiplication by gamma_c gamma_d V_Q (product U_q) R_c R_d before division by A_c+ A_d+ equals V_Q (product U_q)/(A_c- A_d-) on the inverse-convention smoothed class. The smoothing central valuations remain the two fixed valuations from the source. These are universal operations, rather than characterwise idempotent divisions. Full construction and primary Kato/PT hypothesis checks are in agent_notes/two_converse_cyclotomic.md.

## Fixed curves in the actual application

For each selected Family004 parameter l, apply the pointwise converse to the fixed curve E_l first. Its bad primes, including those dividing l, are fixed support. The internal signed twist parameters then have the odd conductors required by the cyclotomic construction. Since l itself is3 modulo4, treating it as an odd fundamental discriminant with fixed base E_1 would be an invalid application. The source theorem does not require that application or uniform constants across all l.

These substitutions do not independently prove the pointwise converse, H10(Q), or the geometric undecidability target.

## Complete-package normalization repair

The first promoted correction summary and manuscript mistakenly substituted the unnormalized polynomial 1-a_q Z+q Z² at the same Z. The exact cyclotomic source and detailed cyclotomic audit already used the normalized determinant 1-(a_q/q)Z+Z²/q. These are reciprocal polynomials, and their correction ratios are reciprocals; agreement of central valuations alone would not justify substituting them. The candidate now uses the actual normalized local determinant consistently. The ratio U_q changes precisely P_q(Z^-1) into P_q(Z), after the global gamma_q² translation, so it pays the local height-one divisor D_q in the actual localization sequence. The smoothing multiplier is applied to the inverse-convention smoothed class before division by the direct smoothing factors. This correction was found by the first complete-package reviewer and is explicitly rechecked in the integration addendum.
