# Mandatory mathematical repair to the author freeze

Problem 5300062. The original author ZIP and its files are immutable audit inputs.
This document does not modify or supersede that freeze. A separately frozen v2,
followed by a bounded-delta check, is required before an accepted publication state.

## C1: meet the actual convergence hypothesis in the cited source

Location: REPORT.md, §3.2, displayed conditions on the interval and eta.

Old:

    a>max{x_0,K+6},             b+eta<F(a).

New:

    a>max{x_0+2 log(K+3),K+6},   b+eta<F(a).

Reason: [FS, Lemma 4.4] identifies the finite inverse-log approximants with the
standard dynamic ray only above t_s^*+2 log(K+3), where

    t_s^* = sup_{j>=0} F^{-j}(|s_(j+1)|).

The original inequality does not imply that sufficient hypothesis. For example,
K=1, x_0=100, a=100.01 meets the old displayed inequality but fails the strengthened
one. This is a counterexample to the claimed implication of hypotheses, not a
counterexample to convergence or to the smoothness theorem.

Location: §3.2, immediately after the displayed definition of g_(n,kappa,s).

Old:

    These finite approximants converge to the usual dynamic ray on such tails by [FS].

New:

    The address bound implies t_s^*:=sup_{j>=0} F^{-j}(|s_(j+1)|)<=x_0.
    Therefore a>t_s^*+2 log(K+3), and [FS, Lemma 4.4] identifies the locally
    uniform limit of these finite approximants with the standard dynamic ray.

This correction separates the independent derivative estimate from the cited
identification of its limiting curve. No change to estimates (1)-(5) is required.

## C2: retain the stronger condition after the low-potential shift

Location: REPORT.md, §3.3, the sentence beginning “Increase N until”.

Old:

    Increase N until F^N(inf J)>K+6 and F^N(u)>=2, where a parameter
    neighborhood has |kappa|<=K.

New:

    Increase N until F^N(inf J)>max{F^N(u)+2 log(K+3),K+6} and
    F^N(u)>=2, where a parameter neighborhood has |kappa|<=K. This is
    possible because inf J>u>0: after finitely many iterates both are
    at least 2, and their difference then grows at least geometrically.

Then x_0=F^N(u) and a=F^N(inf J) satisfy the repaired tail hypothesis.
Shrinking J afterwards preserves these strict inequalities. No change to the
main theorem, addresses allowed, number of approaches, or unresolved status is
needed.

## Required downstream state

- Keep original target UNSOLVED, approaches 5/5, with geometric analyticity and
  endpoints outside the proved conclusion.
- Preserve the original author freeze and identify a revised REPORT.md as v2.
- Regenerate the v2 manifest and ZIP, and replay its retained controls.
- Bind the v2 source state and exact content diff in a bounded-delta acceptance.
- Do not describe the original unmodified freeze as an unqualified audit pass.

The supplied REPORT_MANDATORY.patch applies only these three textual replacements.
The additional explanations in AUDIT.md establish that the repaired proof works;
they are not an unrequested extension to the mathematical claim.
