# Turn 1: fixed-seed and finite-fragment reductions

Status: exact reformulations and a blocked route, not a decision of finite axiomatizability. No novelty claim. The game definitions and monotonicity used here are credited to Jeřábek's current paper, Definition4.5 and Lemma4.6.

Write A_n=PWin^0_n for the sentence asserting that Powerator wins n rounds from the empty position. Write B_n=PWin^1_(n+1)(1) for the sentence asserting that Powerator wins n additional rounds after the response1 has already been played. Both are sentences in the original ordered-ring language. Set A_0=B_0=true. Challenge moves and responses below are positive; the paper's unguarded quantifier presentation is equivalent over IOpen by Lemma4.6.

## 1. The forced-one sandwich

For every standard n≥0,

IOpen proves A_(n+1) -> B_n -> A_n.

The first implication follows by setting the first challenge to1. In a discretely ordered nonnegative ring, the legal response u≤1<2u is forced to be1. The remaining n rounds are exactly the seeded game. For the second implication, use the seeded strategy to answer n ordinary rounds and then omit the initial1 from the tuple. Every multiplicative forbidden triple among the remaining answers was already forbidden in the larger tuple, so the ordinary game is safe. These are finite syntactic/game implications, not an appeal to a definable infinite strategy.

Both sequences are decreasing in strength under shortening the number of rounds. Consequently

TEIP = IOpen + {A_n:n≥0} = IOpen + {B_n:n≥0}.

Thus all initial response parameters may be replaced by the one fixed standard seed1 when describing the *infinite theory*. This does not say that one finite seeded instance suffices.

## 2. Exact compactness criterion

TEIP is finitely axiomatizable over IOpen iff there exists a standard N such that IOpen+A_N entails every A_n. Equivalently, there exists N such that IOpen+B_N entails every B_n.

For example, if TEIP=IOpen+{sigma_1,...,sigma_k}, each sigma_i is provable from IOpen plus finitely many A_n. Taking the largest index occurring in these finitely many proofs and using monotonicity shows IOpen+A_N proves every sigma_i, hence every A_n. Conversely, such an A_N is itself the one additional axiom. The identical argument applies to B_N.

One adjacent equivalence B_N<->B_(N+1) alone is not asserted sufficient. The seeded sentences do not supply a uniform transition principle at arbitrary future positions; the criterion really quantifies over all later lengths.

## 3. Why the known strict parameter hierarchy does not answer this

The credited Theorem5.16 separates the formulas PWin^1_n(u) as u varies. It does so even over true arithmetic. It does not separate the closed sentences B_n, nor the A_n: every model of true arithmetic already satisfies TEIP. A proof of relative non-finite axiomatizability must produce, for each N, a model of IOpen+A_N in which some later A_m fails, or the corresponding fixed-seed version. A losing fixed response in the standard integers is not such a model.

The distinction is visible in small games. Starting with6, Challenger plays2; the response2 is forced and 2*2<6<2*2*2 gives an immediate loss. Starting with3, moves2 then1 force responses2 and1 and the forbidden inequality1*2<3<2*1*2. Yet an empty game in the standard integers has a winning strategy of every length: always reply with the largest power of2 at most the challenge. Seed1 is compatible with that strategy. These familiar finite examples are illustrations, not new lower bounds on the known hierarchy.

## 4. Search boundary and next route

The attempted deduction “strict fixed-parameter hierarchy implies TEIP is not finitely axiomatizable” is blocked by the quantifier gap above. No model witnessing a strict *closed-sentence* hierarchy was constructed in this turn. The next route is to examine concrete nonstandard IOpen models and whether a natural finite definable replacement for the power predicate actually axiomatizes their reducts.

`verify_turn1.py` checks finite-game conventions, the explicit losing certificates, and all bounded power-response states in its stated range. Such finite integer games are not finite models of IOpen and cannot decide the target.
