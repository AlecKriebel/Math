# Code review before execution

The independent checker was written after the derivation and before reading
the submitted checker or its certificate. Its entire source was reviewed at
construction. It imports only fractions, itertools, pathlib, hashlib, and
json and sys; it neither executes shell commands nor accesses a network or external
application. It hashes submitted files without interpreting their contents.
Every write is anchored to the directory containing this review script, so
the submitted proof/certificate and shared repository metadata are untouched.

Arithmetic uses Gaussian integer pairs, exact rational fractions, sparse
commutative polynomial coefficient dictionaries, and explicit antisymmetric
exterior multiplication. No floating-point comparisons or numerical ranks
occur. The implementation has two exterior arithmetic paths: a Gaussian
polynomial path for all formal a,b and a rational scalar path for hostile
concrete boundary examples. Matrix rank uses rational elimination and every
check uses an unconditional failure function, so Python optimization cannot
disable validation. The
negative controls require the correct checker to reject a wrong overall sign,
a missing factor 1/4, a transposed projector convention, non-Hermitian reality,
and rank-two mixed tensors. These detect convention errors but cannot prove
the geometric convex-hull equality; the independent derivation supplies that.
