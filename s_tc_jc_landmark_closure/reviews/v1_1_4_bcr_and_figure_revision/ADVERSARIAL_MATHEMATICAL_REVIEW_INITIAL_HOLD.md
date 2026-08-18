# Initial adversarial mathematical review

Status: **HOLD — preserved pre-repair verdict**

The independent mathematical reviewer found no theorem-level defect in the
v1.1.4 candidate.  It did identify one exact auditability omission in the
Omega supplement.

The supplement printed the alternative-rooting N26 arc order, label transport,
Jacobian row and column sets, and determinant values, but it did not print the
strict N26 source and target parameter vectors.  The displayed-rooting vectors
cannot be substituted in their place: in the declared N26 edge order they do
not reproduce the printed alternative-rooting determinants.  In addition, the
text said that the active clean-room JSON stored the same arrays, although that
record stored the graphs and rank data but not the parameter vectors.

The required repair was to print the exact N26 vectors, bind them to the
declared edge and inheritance-parameter order, add them to the active
clean-room output, and reject a mutation of either vector.  The immutable
historical certificate already contained the vectors and the independent
Fourier replay had evaluated them; the omission concerned the exposed
certificate chain, not the underlying equality or rank calculation.

This HOLD is part of the correction record.  It is not a release verdict.

HOLD
