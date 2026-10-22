# Clarifications to accompany the frozen packet

The frozen author files remain unchanged. No correction to the principal
coefficient obstruction, dual certificate, twist maximum or compensation
threshold is required.

## Coefficient normalization

In RESEARCH.md, Proposition 4, the phrase “normalized vertical coefficient
w_Gamma of W_mid” is ambiguous and conflicts with the earlier lambda-12
normalization if read literally. The number 470/9963 applies to an increase
delta in the **raw coefficient w_Gamma of equation (62)**, whose lambda
coefficient is w_lambda=45/44. Its residual contribution is
(12y/w_lambda)delta.

If delta instead denotes the increase in the lambda-12-normalized table entry
W_b, the corresponding strict threshold is 16544/29889. These are equivalent
after multiplication by 12/w_lambda. Replace that phrase with “the raw
coefficient w_Gamma in equation (62), before lambda normalization.” The
displayed calculation and checker already use this raw convention correctly.
Neither threshold proves that the improved class is effective.

## Genus 13 auxiliary class

Section 5's phrase “a genus-13 analogue” should explicitly say that the positive
control uses W_mid and 2 BN. The interval printed there is correct for that
pair, and the author's code correctly uses it. NF is the even-genus auxiliary
class in the genus-12 test; the control is not a same-class continuation to
odd genus.

## Audit scope

The statements about a failed fixed test must remain qualified. A failure of
this sufficient coefficientwise criterion, including its compensated canonical
class and fixed divisor estimates, proves neither non-bigness of the actual
canonical divisor nor falsity of the genus-12 general-type conjecture. Neither
the independent arithmetic checks nor this audit change that unresolved status.
