# 30003999: original rational-base power sums

Active research after **four of five** substantive author turns. No full solution or final unsolved outcome is claimed.

The source asks about sum (2/3)^r_i, not the cube-root expression in the extracted record. TURN_1.md gives exact input normalization, a credited polynomial-time equality test and an elementary fixed-parameter sign algorithm for the positive example. The missing goal is a polynomial bit-time sign algorithm for variable n, or a definitive obstruction.

Run `python3 verify_turn1.py` to reproduce turn1_verification.json. These finite exact tests do not certify a general complexity claim beyond the proved reductions. Source PDFs stay outside the public package.

TURN_2.md gives a unified signed-coefficient gap algorithm: fixed-parameter tractable for each fixed rational base, with a polynomial bound for the classical integer/reciprocal-integer cases. Run `python3 verify_turn2.py` to reproduce its finite exact controls. The remaining issue is polynomial dependence on the variable number of terms for a noninteger rational base.

TURN_3.md adds polynomial zero-block deletion and a certified adaptive truncation algorithm. Its remaining precision parameter is not bounded polynomially for the original noninteger rational base. An explicit easy-sign family exposes exponential work in the earlier conservative implementation and is handled immediately by the adaptive alternative.

TURN_4.md treats the original positive subcase directly: its near-threshold root is unique, simple and locally isolated on an inverse-polynomial scale, but its distance from 2/3 is still uncontrolled at the needed bit-complexity scale.
