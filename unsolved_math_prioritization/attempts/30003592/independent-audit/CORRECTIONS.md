# Corrections and clarifications

## Required corrections

None. The frozen mathematical conclusions are valid in their explicitly stated smooth-projective complex scope. The universal problem remains unsolved.

## C1. Quotient parameter-space notation (minor; non-blocking)

Location: PARTIAL.md, Approach 2, the covering family of surfaces of class xi^2-xi f.

The construction chooses one-dimensional quotients of A and B and names their parameter space P(A*) x P(B*). Earlier, the note explicitly adopts quotient-projectivization. With that convention applied uniformly, one-dimensional quotients of A are parametrized by P(A), not P(A*). If the expression P(A*) is intended to mean lines in A*, it uses the other projective-space convention.

Suggested local clarification, without changing the construction:

"Let S=Gr_quot(1,A) x Gr_quot(1,B), the product of the Grassmannians of one-dimensional quotients. The universal quotient line bundles over S give the required rank-two quotient bundle over S x P^1."

The parameter space is a product of projective lines either way. The quotient construction, class, flatness over S, irreducibility, and surjectivity of evaluation are correct. This does not block the audit verdict and no input file was modified.

## C2. Optional strengthening of computational controls

The supplied product extraction test applies an identity matrix that it explicitly constructs. It does not independently derive that identity from the projective-bundle grading and pushforward. This limitation is consistent with the notebook's validation disclaimer and is not a mathematical error. The audit's independent_checks.py supplies additional truncated-ring pushforward checks over a range of dimensions, including infeasible and endpoint dimensions.

## C3. Historical audit-status fields

The frozen README, STATUS, and log correctly report that an audit was pending at the moment of freeze. Preserve those bytes when using this audit's binding and attach this later audit separately. An edited replacement packet has a new identity and is not automatically covered by the present hash-bound verdict.
