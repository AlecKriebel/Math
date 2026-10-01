# Author turn 5: contact approximation detects orbit-limit obstructions

**A necessary-condition theorem in the closed oriented coorientable C2 subclass; not an example or a general descent theorem.** The contact isotopy classes canonically approximating a foliation are constant on the closure of its identity-isotopy orbit as long as the limiting foliation also satisfies Vogel's hypotheses. Their construction commutes with finite covers. This supplies a genuinely foliation-sensitive test, beyond the plane-field homotopy obstruction which failed in TURN_4.

## 1. Exact classical uniqueness input

Vogel, *On the uniqueness of the contact structure approximating a foliation*, Geometry & Topology20(2016),2439–2573, Theorem1.4 on printedp2441, assumes a coorientable C2 foliation on a closed oriented 3-manifold which:

- has no torus leaf;
- is not a foliation entirely by planes;
- is not a foliation entirely by cylinders.

There is then a C0 neighborhood in plane-field space in which every positive contact structure has the same contact isotopy class. Theorem1.1 supplies arbitrarily close positive contact approximations, except for the sphere-product case, already excluded here. Applying the same statements to the opposite orientation of the ambient manifold gives the corresponding negative class.

For a closed oriented hyperbolic 3-manifold with a cooriented C2 taut foliation, these exclusions hold. A torus leaf would be incompressible for a Reebless foliation and would inject Z^2 into the closed hyperbolic group. A sphere leaf is incompatible with the aspherical ambient manifold. The plane-only and cylinder-only closed-manifold possibilities are excluded by the Rosenberg and Hector classification results recalled immediately after Vogel's theorem: the ambient manifold would be a torus or a parabolic torus bundle, not a closed hyperbolic manifold. The same reasoning applies to every finite cover with its lifted foliation.

We use this exact C2, closed, oriented, coorientable theorem. Question13.4 does not explicitly impose all of those restrictions, so conclusions here are not silently extended to every possible source interpretation.

## 2. Canonical classes and orbit closure

First keep a chosen coorientation. Denote the positive and negative approximating contact isotopy classes by A^+(F) and A^-(F). These mean isotopy of contact structures, rather than merely an arbitrary contactomorphism or a homotopy of plane fields.

Suppose h_n are endpoints of smooth identity isotopies and h_n(G) converges uniformly to F as cooriented plane fields, with F and G satisfying the preceding uniqueness hypotheses. Then

A^+(F)=A^+(G),       A^-(F)=A^-(G).                  (1)

Here is the direct neighborhood proof, which does not require uniform derivative bounds on h_n. Let U_F be a uniqueness neighborhood for F and U_G one for G. For sufficiently large n, h_n(G) lies in U_F. For this fixed diffeomorphism h_n, pushforward is continuous on the C0 space of plane distributions. Consequently there is a neighborhood V_n of G such that h_n(V_n) is contained in U_F. Choose a positive contact approximation eta_n of G in U_G intersect V_n. It is isotopic to A^+(G), while h_n(eta_n) belongs to U_F and hence is isotopic to A^+(F). Pushing eta_n along the original isotopy from the identity to h_n gives an isotopy through contact structures, so eta_n and h_n(eta_n) have the same contact isotopy class. This proves the positive equality. Repeat using the negative uniqueness neighborhoods for the other equality.

The approximations eta_n may depend on n and may need to be extremely close to G when derivatives of h_n are large. Their existence, rather than a uniform approximation scale, is all that is used. Thus this theorem applies even when the controlled-generator hypothesis of TURN_2 is unavailable.

## 3. Do not count coorientation reversal as a new source foliation

The original question does not distinguish a foliation from itself with reversed coorientation. To retain that convention, define the two-choice invariant

A(F) = { (A^+(F),A^-(F)), (bar A^+(F),bar A^-(F)) },

where the bar reverses the coorientation of each contact plane field, without changing whether the contact structure is positive or negative relative to the fixed ambient orientation. This operation is well defined on isotopy classes and is an involution.

If h_n(G) converges only as unoriented plane fields to F, choose one coorientation on G and one on F. For sufficiently close fields on connected M, the relative lift to the cooriented plane bundle differs by one global sign. Passing to a subsequence makes this sign constant; apply Section2 with that choice. It follows that

A(F)=A(G).                                           (2)

Both positive and negative entries use the same coorientation choice. This avoids falsely declaring F and its coorientation reversal to be different examples. In particular, Vogel's coorientation-reversal example on a Seifert homology sphere is not a solution of this unoriented hyperbolic question.

## 4. Compatibility with finite covers

Let p:N to M be a finite cover with the pullback orientation, and suppose both F and p*F satisfy the uniqueness hypotheses. Then

A^+(p*F)=p*A^+(F),      A^-(p*F)=p*A^-(F).             (3)

To see this, choose a sequence of contact representatives eta_j, all in the canonical class A^+(F), converging to F. Pullback preserves contactness, contact sign, contact isotopy and C0 convergence. Thus p*eta_j converge to p*F and all represent p*A^+(F). Eventually they lie in a uniqueness neighborhood upstairs, proving the positive equality; the negative one is identical. No deck equivariance of an independently chosen approximating isotopy is needed. No injectivity of pullback on contact isotopy classes is claimed.

The same statement holds for the two-choice invariant. Therefore the original upstairs convergence premise, in this closed coorientable C2 setting, implies

p*A(F)=p*A(G).                                       (4)

This is a necessary condition. If one can produce actual taut foliations with different invariants downstairs and the stipulated upstairs orbit convergence, equation(2) certifies the missing downstairs convergence. Equation(4) alone, even together with equality of lifted plane-field homotopy classes, does not supply that orbit convergence.

Conversely, any obstruction which distinguishes the pulled-back canonical contact classes already rules out the required upstairs premise. It is not a downstairs-only counterexample. No general injectivity or noninjectivity theorem for the relevant hyperbolic contact classes is assumed.

## 5. Final outcome of the five-turn attempt

The contact-class test is credited to Vogel's uniqueness framework, with the orbit-closure and covering deductions proved above. It sharpens the distinction between homotopy and foliation dynamics but does not produce the missing example. Limited searches and the inspected examples yielded neither a pair with verified upstairs isotopy convergence nor an unconditional method to turn arbitrary upstairs paths into equivariant ones.

The strongest retained package is:

1. finite-cover transfer and characteristic-class necessary conditions;
2. regular-cover reduction and a controlled equivariant-descent theorem;
3. an actual hyperbolic plane-field-only analogue with a finite cyclic cover;
4. a Floer obstruction showing that the proposed torsion fields in that analogue cannot be tautly realized in the stated standard setting;
5. the source-qualified contact-isotopy necessary conditions and cover compatibility above.

The original Question13.4 remains **unsolved after 5/5 substantive author turns**. A general existence or impossibility result, including the source's possible lower-regularity or nonclosed cases, is not claimed. No further proof-search turn is taken after this freeze; the scoped results and their exact gaps require independent review before publication. Completion estimate20%.
