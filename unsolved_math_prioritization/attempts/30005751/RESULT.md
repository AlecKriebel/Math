# Finite axiomatizability of TEIP over open induction

Problem 30005751, OWR-14298016-007. Final author disposition: **unresolved after five substantive turns**. No complete answer or novelty claim is made. This packet awaits independent review.

## Original scope

The question asks whether TEIP, the first-order theory in the original language L_OR = {0, 1, +, multiplication, <} of nonnegative exponential integer parts, is finitely axiomatizable over IOpen. IOpen is open induction with parameters in the theory of discretely ordered nonnegative rings. An elementary extension may be needed to realize an expansion. The existence of a finite axiomatization in a language with a power predicate or exponential function does not answer the reduct-language question.

The source is Emil Jeřábek's OWR 2023 contribution, Question 6 on printed page 3040; the current author paper repeats the question as Question 5.1. Its credited game characterization is TEIP = IOpen + {A_n : n is a standard finite integer}, where A_n = PWin^0_n. The source's fixed-parameter hierarchy is not the closed-sentence hierarchy.

## Proved scoped conclusions

1. The forced seed 1 gives A_(n+1) implies B_n implies A_n, with B_n = PWin^1_(n+1)(1). Compactness makes finite axiomatizability equivalent to one A_N proving every later A_m over IOpen, equivalently one B_N proving every B_m.
2. In the credited real-algebraic finite Puiseux-polynomial model, the elements having no odd divisor except 1 are exactly the standard powers of 2. They are not cofinal. This model satisfies TEIP, so the known finite oddless-predicate upper theory properly extends TEIP. This rules out that proposed axiomatization only.
3. Archimedean-coefficient Hahn truncation integer parts with divisible exponent groups all admit external monomial power predicates and satisfy TEIP. Merely changing those groups cannot separate finite fragments. In contrast, finite-support polynomials over the lexicographic group Q squared fail IOpen, witnessed by a square root whose negative support is infinite.
4. Scaling automorphisms of the finite Puiseux model exclude every parameter-free definable power-predicate expansion, also allowing standard integer parameters. The same obstruction excludes parameter-free definable memoryless strategies safe for all three-round games. External predicates exist. Arbitrary finite axioms are not excluded.
5. TEIP is not finitely axiomatizable exactly if, for every N, some countable recursively saturated model of IOpen + A_N has a first challenge whose entire legal-response interval loses at a later finite horizon. The natural ultraproducts of hard parameters in ordinary arithmetic remain models of TEIP, so they do not give these separating models.

Detailed proofs and boundary conditions are in TURN_1.md through TURN_5.md. The dependencies on Jeřábek's game/expansion theorems, Shepherdson's integer-part theorem and the credited real-closed Hahn-field theorem are explicit. The source proofs are not all independently re-audited, and these conclusions are not certified novel.

## Sharp remaining gap

Produce one finite original-language extension of IOpen with a uniform proof of every A_m, or construct the bad-interval models above for arbitrarily large N. A single losing response, strictness of the parameter hierarchy, lack of definable expansions and finite scans do not decide this alternative.

The five checker scripts provide exact finite algebraic and logical controls only. No finite structure tested is claimed to model IOpen. FINAL_REPLAYS.json records byte-exact author replays and historical hash preservation. Source PDFs are not republished; their verified locations, hashes and reading limits are in the source manifests.
