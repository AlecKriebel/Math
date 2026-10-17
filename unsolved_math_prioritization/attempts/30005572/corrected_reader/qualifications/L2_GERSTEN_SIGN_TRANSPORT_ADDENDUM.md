# Gersten sign transport and the source-comparison boundary

14 October 2026 UTC. Row 1777 / 30005572. Independent review within shared PASS4/5. No frozen earlier proof is edited by this addendum. The original construction remains UNSOLVED.

## 1. The two differentials

For a discrete valuation v, call

 tau_std{a,b}=(-1)^(v(a)v(b)) overline(a^v(b)/b^v(a))

the standard tame convention used explicitly in PASS1's relative-symbol and arithmetic-residue computations. For separated variables its additive Gersten differential is

 d2_std{u(x),v(y)}=u(x) exterior div(v(y))-div(u(x)) exterior v(y).

This is exactly the formula printed in PASS2 RIGHT_END_LIFTING, section 6. It is not the reciprocal of the displayed tau_std. For example, at a zero of u with v(y) a unit, both formulas give v(y)^(-ord u).

Sharifi–Venkatesh explicitly use the reciprocal in equation (2.4):

 tau_SV{a,b}=(-1)^(v(a)v(b)) overline(b^v(a)/a^v(b)).

The residue-field value of -1 has order at most two, and the two tame formulas are exact multiplicative inverses even before passing to R=Z[1/6]. In additive notation d2_SV=-d2_std. The next differential d1 is the ordinary divisor map in both conventions.

LSSW section 3.2 introduces its product Gersten complex “as in [ShVe, (2.5)].” No contrary explicit tame-sign formula was found in the inspected LSSW sections. Accordingly, a comparison to that cited source convention must use the sign transport below; one must not infer literal equality of underlying K2 symbols merely from uniqueness stated using an unnamed residue map. If an alternative identification of LSSW's differential is used, it must be specified and verified explicitly.

## 2. The chain isomorphism is explicit

Let C_std and C_SV be the two complexes with identical coefficient groups C2,C1,C0, ordinary divisor d1, and d2_SV=-d2_std. The maps

 J2=-Id on C2,   J1=Id on C1,   J0=Id on C0

form a chain isomorphism C_std -> C_SV: d2_SV J2=d2_std and d1 J1=d1. It fixes every auxiliary zero-cycle e_c and every chosen C1 primitive eta_c. It commutes with group actions, field restriction, proper transfer, isogeny pullbacks, and all scalar trace operators. It also induces multiplication by -1 on the constants quotient and on ordinary/normalized K2 lifts.

Suppose the normalized cocycle is defined by d2_std z_std(gamma)=gamma eta-eta. Then

 z_SV(gamma)=-z_std(gamma)

is the normalized source-sign cocycle with the same eta. This is an equality of actual K2 classes after changing convention by J; it is not a claim that a class equals its own negative. Likewise a correction b_std with boundary eta'-eta transports to b_SV=-b_std.

## 3. Which comparisons must carry the sign

If an authored geometric cocycle is interpreted using the explicit standard differential in PASS2, its direct comparison with the ShVe-sign source geometric cocycle requires J2. The same is true after specialization to K2 of a marked-point field or ray field, and after passage to integral or localized integer-ring subgroups.

Consequently the following phrases in earlier proofs/acceptances must be read only after identifying the complexes by J, or be qualified if they are read as literal identities in the same fixed K2 group:

- PASS3 scalar-five proof section 7: comparison with the existing source geometric family after inverting five.
- Any subsequent arithmetic comparison obtained by specializing that geometric family, including the comparison to source auxiliary classes and maps in the construction contract.
- The good-component identification with the published unaugmented classes when it is derived from that auxiliary comparison.

One can consistently use the source differential for the entire arithmetic construction; then the scalar-five projector and all subsequent homogeneous arguments apply unchanged, and its source comparison is literal. Alternatively one can consistently use the standard differential; then source geometric, arithmetic, and unaugmented classes are the negatives under the displayed identification. It is not consistent to use the positive standard swap formula and silently call it the positive source-sign swap formula.

This addendum does not determine the final orientation convention between a Cremona edge and a group-cocycle path. That is part of the unsolved relative calibration, and must be verified rather than chosen just to force the comparison test.

## 4. Homogeneous statements that are unchanged

All already accepted existence, exactness, regularity, uniqueness, trace invariance, constant-kernel, transfer, model-transport, norm, auxiliary-exchange, and homogeneous Hecke-annihilation statements are unchanged under J. An equality whose terms are all constructed K2 cocycles or correction cochains is transported by multiplying every such term by -1.

Vanishing of an arithmetic residue, a finite annihilator, an integrality assertion, a kernel or image subgroup, and the fact that a class is nonzero are also unchanged. Explicit nonzero multiplicative residue values are inverted if the K2 class itself is negated while tau_std is retained. If both the complex differential and class are transported, the corresponding C1 residue stays fixed, exactly as the chain-map identity requires.

The same distinction applies to a cusp-potential computation: its telescoping vanishing is unaffected by a uniform sign, but its actual edge values and any prescribed theta-symbol formula have a definite sign.

## 5. The swap result makes the distinction visible

The corrected PASS4 symbol theorem works explicitly with d2_std and proves

 z_std(w)={f(x),f(y)}.

With the same primitive and the source reciprocal differential, the transported statement is

 z_SV(w)=-{f(x),f(y)}.

The product norm calculation proving literal T5-fixedness remains valid in either convention. Its purpose is to remove constants, not to identify these two differently signed symbols. At cyclic-four level the distinction between raw factor576 and three-term smoothing factor624 remains a separate calibration issue; a sign change does not supply the missing mixed terms or the missing shear transitions.

## 6. Source and review boundary

The explicit source formula was inspected in the retained Sharifi–Venkatesh text, equation(2.4), section2.2, and LSSW section3.2 was checked for its reference to that complex. The public sources are:

- Sharifi–Venkatesh, *Eisenstein cocycles in motivic cohomology*: https://math.ucla.edu/~sharifi/eisensymbol.pdf .
- Lecouturier–Sharifi–Shih–Wang, *Eisenstein cocycles for imaginary quadratic fields*: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf .

The initial PASS4 symbol draft incorrectly described d2_std as reciprocal to its own displayed tame formula. The author corrected that label and stated the sign change with eta fixed. The chain calculations themselves were unchanged. This audit does not declare a defect in either source's internally consistent convention.
