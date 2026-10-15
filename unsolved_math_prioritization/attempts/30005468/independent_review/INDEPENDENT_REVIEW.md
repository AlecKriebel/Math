# Independent source and proof review: 30005468

Verdict: **PASS_COMPLETE_LITERAL_FIXED_P_RATIONAL_SQUARE_TARGET**.

The frozen first-turn candidate gives an affirmative example for the literal OWR fixed-polynomial question, with rational SOS understood at the level of the polynomials being squared, equivalently rational positive-semidefinite Gram data. No mathematical correction is required. This verdict is not a finding of historical novelty or of the original authors' approval of a particular interpretation.

Bound author proof SHA-256:
`866f036f3541721d82cc9d06da2ee4e1d8ed8f083c44bdb914b7befc9fa12881`.

Bound author manifest SHA-256:
`4fd0839ba91bc760f1c272e34fb056a79480b9cc355da8b3b5d1b71be73ad6d2`.

The reviewer did not contribute to this construction. This audit read the complete frozen proof, the relevant full primary-source arguments, the report's original context and the companion's stronger formulation. Every one of the ten frozen author artifacts and four source PDFs matches its manifest. The author's 2,059-control receipt replays byte-identically. A separately authored checker passes 2,345 exact controls. Neither finite computation substitutes for the all-degree argument below.

## 1. Source coverage and its necessary qualifications

I read Naldi's complete OWR contribution on printed pages 802–804 and visually inspected the final question and the preceding example. The objects are all monomials of total degree at most d, arbitrary real truncated moment input, and a nonnegative representing measure supported on the specified basic closed set. No positive-semidefinite-input restriction is imposed. The displayed certificate has p in 1+Q(g), is strictly positive on K, and satisfies L_y(p)=0.

The question on page 804 concerns rational p and the possible absence of rational positivity certificates for that fixed membership. The candidate's existential quantifier is correct: one bad fixed p suffices. It need not make every possible separator for the same y bad. The report itself exhibits a p whose minimum on the unit ball is exactly one. Therefore it does not impose min p>1 merely by requiring strict positivity of p.

The companion preprint must be distinguished carefully. Its Definition 3 defines a separator using positivity and vanishing of the moment functional, while Corollary 2 constructs an additional strict margin p*>1. The candidate meets the former and the OWR's displayed conditions, not the latter additional margin. Powers's theorem actually removes the obstruction for the candidate's rational rescalings with strict margin. The author has stated this limitation correctly.

There is also a certificate-language distinction. The companion first describes an SOS certificate as a list of multiplier polynomials sigma_i. Merely requiring those multiplier polynomials to have rational coefficients, while permitting irrational real square decompositions, is weaker than requiring rational SOS data. In that weaker sense sigma_0=f, sigma_1=0 is already a rational list in this example. The OWR's explicit appeal to Scheiderer's distinction between sums of real squares and sums of rational squares, and the supplied target's SOS wording, support the stronger square-data reading used in the proof. The publication must retain that definition; an unqualified claim that even the multiplier-polynomial coefficients must be irrational would be false. The frozen proof already makes the distinction prominently.

These qualifications do not invalidate the literal fixed-p rational-square example. They rule out stronger or differently defined claims, and should remain visible in its queue summary and PR description.

## 2. Explicit moment and support data

The single generator g=1-x^2-y^2-z^2 gives a nonempty compact unit ball and a rational Archimedean certificate immediately. With all 35 degree-at-most-four moment entries included, m_0=1, m_(4,0,0)=-1 and all others zero, the exact quartic's x^4 coefficient gives L_m(1+f)=0. A nonnegative representing measure is impossible because its x^4 integral cannot be negative. Independently, the mass-one condition and p>=1 contradict a zero integral. These arguments do not use the compressed report's potentially missing general duality hypotheses.

The input is not positive semidefinite: the moment-matrix diagonal for x^2 is -1. That is permitted by the displayed source, not concealed by the construction. The polynomial p has degree four and is in the interior of the finite-degree nonnegative cone on K because it is bounded below by one on this compact set. Its minimum is precisely one, since f is nonnegative and f(0)=0.

## 3. The credited quartic obstruction

The exact polynomial matches Scheiderer's final published Theorem 2.1 and Example 2.8. I checked the norm identity independently by a resultant. For h(t)=t^4-t+1, the real-root exclusion is valid. Reduction modulo two is irreducible and separable; reduction modulo three has distinct irreducible factors of degrees one and three. Thus the Galois group contains a four-cycle and a three-cycle. Its order is divisible by twelve and divides twenty-four; the only index-two subgroup of S_4 is A_4, which has no four-cycle. Hence the group is S_4.

The four conjugate linear forms x+alpha_i y+alpha_i^2 z are in general position by their Vandermonde minors. Pairing conjugates proves the norm is the squared complex modulus of a quadratic and is therefore a sum of two real squares. The displayed resolvent-root SOS identity is also exact; a negative root exists in (-2,-1).

For rational quadratic square summands, each real intersection of a conjugate pair is a zero of every summand. Such a conjugation-invariant projective point has a real representative; homogeneous vanishing is independent of its normalization. Galois conjugation of the rational equations carries that vanishing to every pair intersection. Each of the four lines contains three distinct such points. A degree-two restriction with three distinct projective zeros vanishes identically on that line, so all four line equations divide the quadratic. It must be zero, a contradiction.

Allowing arbitrary inhomogeneous square summands does not escape this proof. The largest homogeneous square degrees cannot cancel in a sum of real squares, so all summands have degree at most two. The constant and then linear parts vanish because the quartic has no lower-degree terms. This recovers exactly the excluded rational quadratic forms. The proof is a valid reproduced classical argument, not an unsupported computational non-SOS assertion.

## 4. Arbitrarily high-degree module multipliers

This is the essential extension from the cited quartic to the requested fixed membership. At the origin, both weights in sigma_0+g sigma_1 equal one. A rational-square representation of f therefore forces the constant term of every square factor to vanish. The homogeneous degree-two part is then a sum of squares of their linear parts, with no contribution from g-1; all linear parts vanish too. Consequently every factor has order at least two. Taking degree four leaves exactly the sum of the squares of their quadratic parts. The term (g-1) sigma_1 has order at least six.

This would make f a sum of rational quadratic squares, already excluded. The argument is independent of the maximum degrees or number of square factors. Potential cancellations among high-degree terms cannot alter the fourth-order jet. Nonhomogeneous or arbitrarily high-degree multipliers are fully covered. There is no bounded-SDP-search loophole.

The optional generalization for rational positive generator values also follows: positive rational weights can be expressed as sums of rational squares and absorbed into the square factors. That generalization is not needed for this ball, where both values are exactly one.

## 5. Negative controls and the strict-margin theorem

The same moment vector has the simple separator q=1+x^4, whose membership q in 1+Q_Q(g) is explicit. Thus the construction is not an unavoidable-irrationality theorem for every separator of that vector.

For rational c>1, cp-1 is strictly positive on K. Powers's final Theorem 7 supplies a rational SOS representation with the original generators plus a rational ball term. Here the original generator is already that ball term, so it can be absorbed without changing the presentation. Hence cp has a rational certificate. This does not contradict the candidate: p-1=f has zeros, and Powers's strict-positivity premise fails at p itself. No degree or bit-complexity bound is inferred.

The proof therefore passes exactly with its stated normalization, rational-square meaning, fixed-p quantifier, and permissive moment-input scope. It does not settle a stronger strict-margin problem, a universal-separator statement, rational coefficient lists without rational square factors, or the separate general rational Archimedean descent question.

## 6. Reproducibility and disposition

The independent checks include the norm resultant, finite-field factorization and separability, exact real-root counts, the cubic-resolvent identity, the S_4 pair orbit, 126 distinct six-point quadratic-interpolation configurations, the full degree-four moment indexing, and independent fourth-jet controls with higher tails. They also check the original report's normalization example and rational strict-margin rescalings.

Recommended disposition: a complete first-turn candidate for the literal fixed-p rational-SOS-data question, with the stated scope and classical credits. Any public claimed-solved label must keep those qualifiers. The parent retains the publication decision; this report neither creates a PR nor asserts a priority claim.
