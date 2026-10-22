# Fifth and final substantive author-turn checkpoint

2026-10-02 04:51 UTC. The final turn attacked genuinely non-diagonal positivity certificates. Proved that every integral SU(3) virtual character of Haar mean one which is a Hermitian sum of squares of arbitrary complex character polynomials is one irreducible square, with no support bound. The Gram matrix may initially be fully non-diagonal.

The mechanism is: highest-degree integrality concentrates the trace-one positive Gram matrix at one character height; integral Laurent extremality kills its nonzero-distance band sums; a stable-strip Littlewood–Richardson coefficient formula reduces each successive diagonal character coefficient to an integer boundary mass. Positive semidefiniteness then removes boundary rows or confines the matrix to a conjugate pair, which gives one square. The proof retains the possibility of rank-two diagonal Gram matrices for conjugate roots.

verify_turn5.py passes 11,403 new exact assertions on 1,784 cross tensor products and 4,804 stable-strip entries, and reruns all 2,265 turn-4 controls. A non-diagonal positive definite band-cancellation example checks that the proof does not mistakenly infer diagonality from leading terms alone.

The Weyl discriminant is an explicit integral virtual character nonnegative on SU(3), with Haar mean 15, that cannot be a Hermitian sum of character-polynomial squares because its formal value at trace 4 is negative. This is not a source counterexample, but pinpoints why general positivity cannot be replaced by the SOS hypothesis without using the mean-one condition.

Original status: exhausted and unresolved after 5/5 substantive author turns. No full candidate solution or counterexample was obtained. All five scoped mathematical artifacts are preserved for independent review. The remaining gap is arbitrary mean-one pointwise positivity outside the Hermitian-SOS cone, already on SU(3), and all other higher-rank groups for a full affirmative answer. No sixth substantive proof-search turn is included. Completion estimate 30%, subjective and uncalibrated.
