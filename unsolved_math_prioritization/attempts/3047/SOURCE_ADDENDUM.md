# Additional historical scope check

The independent source auditor identified [David Newman's September 2017 question, “Yet another question about unrestricted partitions”](https://mathoverflow.net/questions/282057/yet-another-question-about-unrestricted-partitions). We subsequently inspected the complete primary-page text ourselves on 12 October 2026.

That variant allows arbitrary signs in the numerator series \(F_1(q)\), and independent signs in every denominator binomial \(1\pm q^m\), \(m\ge2\). Max Alekseyev's 27 September 2017 answer reports exhaustive impossibility for that variant, with maximum feasible degree 121, and displays a witness and PARI/GP search code. We inspected the source code as text but did not execute it, and did not independently certify its exhaustive maximum claim in this task.

The denominator signs can change many original factors simultaneously, since \((1+q^m)^{-1}=1-q^m+q^{2m}-\cdots\). Conversely their alternating coefficient constraint does not allow arbitrary independent signs in an active factor such as \(F_2\). Thus this is a different restricted class, and its reported degree 121 neither contradicts nor establishes the at-most-two-active-factor theorem proved here. Our degree-85 witness is not claimed as a general finite-prefix record.

The original problem remains outside both restricted impossibility statements. The frozen mathematical proof is unchanged; this addendum supplements its historical source discussion.
