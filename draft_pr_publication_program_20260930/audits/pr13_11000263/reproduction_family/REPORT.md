# PR13 exact reproduction and numerical/proof consistency adversary

Frozen head: `7a845f7e025a24affe1b712cf7ada648570f9c64`.
Independent family conclusion reached 2026-10-01T13:40:00Z, before reading
`SCALAR_SCOPE_CHECK.md`, historical `REVIEW.md`/`verdict.json`, or sibling
conclusions. Historical review/verdict and sibling conclusions were not read.

**Verdict: PASS for the two explicitly repaired presentations over Q(q).**
No numerical/proof inconsistency or counterexample to that scoped claim was
found. The literal printed presentation remains outside the claim because its
last relation uses an absent generator. These are reproduction and verification
results, not a novelty or author-intent certificate.

## Claim, assumptions, and success criteria

Let F=Q(q), with q transcendental, and write bars as whole-word inverses.
For n>=3 the claims are X3!=0 in

- A_n=F B_n/(R2,...,R_(n-1));
- C_n=F B_(n+1)/(R2,...,Rn).

The defining Xk and Rk are those explicitly displayed in frozen `AUDIT.md`.
Success requires a unital F-algebra representation annihilating every defining
relation and retaining a nonzero X3 image, including the exceptional R2 row and
the C_n terminal row. It does not require a faithful representation. A finite
matrix test is not the success criterion for arbitrary n.

## Frozen replay

`replay_frozen.py` copies the two scripts and their stored receipts into ignored
`tmp/pr13_11000263_reproduction/frozen_replay` and runs them there using the
existing unmodified .venv (Python 3.9.6; SymPy 1.14.0). It writes a new receipt
only in this family's folder. Both exit successfully with empty stderr:

| Frozen computation | Reproduced result | Stored/fresh SHA-256 |
|---|---|---|
| `verify.py` | 42 cases, 1,590 equality/rank assertions | `dd9b19b4446f755defd1b921a6ebb570d1a9d011fe64e76823c49c00da3baf4f` |
| `independent_symbolic_check.py` | 23 symbolic checks | `20fb22bb0c09d6ba5e174a565d51652a7a9fa495922013bab99642401573a8ae` |

The output JSON files are byte-for-byte equal to the stored files, not merely
semantically equivalent. Hashes of the five replay inputs before and after
match; immutable snapshot files were not altered. Full input hashes, executable
identity, timestamps, stdout hashes, and paths are in `replay_receipt.json`.

## Different-mechanism exact verification

`independent_laurent_check.py` does not import either frozen module. Its main
calculations use hand-implemented integer-coefficient Laurent polynomials with
monomial exponents (q,u) and sparse-vector block action. There is no matrix
Gaussian elimination and no rational-parameter substitution in those primary
checks. Whole words act right-to-left, while their inverses act through inverse
blocks in the original listed order.

The suite passed 5,976 labeled checks. Full words, braid relations, inverses, each Xk
rank-one formula, every legal Rk, and both twists were checked on every basis
column for matrix strand count m=3,...,12. Thus the finite suite directly checks
A_n for n=3,...,12 and C_n for n=3,...,11; m=3 is A3, and m=4 is both A4 and C3.
The row manifest records this distinction explicitly. Deliberately failing to
reverse inverse factors is caught both by a whole-word round trip and by R2.

There are 160 exact specialization cases for m=3,...,7 with positive, negative,
unit, and fractional q,u values (always u!=0). SymPy independently computes the
ranks after evaluating the Laurent operators. These checks include q=0 only as
an operator control, explicitly marked outside a source convention requiring q
to be a unit. They verify that X3 has rank zero precisely when u=q or u=q^2,
and otherwise rank one; for m>=4, X4 has rank zero precisely when u is one of
q,q^2,q^3, and otherwise rank one. Repeated values are deduplicated.

## Arbitrary-index proof check

The exact local computation starts from the homogeneous vector
w=(a,-a/u,0). Acting with the Burau block
B=[[1-u,u],[1,0]] and its inverse gives

    B_r B_(r+1) w = (0,a,-a/u),
    B_r^-1 B_(r+1)^-1 w = (0,a/u,-a/u^2).

This is an identity in arbitrary amplitude a and invertible u; it does not
require a to be nonzero. Translation of coordinate positions makes it valid
for every r for which those three coordinates exist. With
v_r=u^(1-r)e_r-u^(-r)e_(r+1), these equations are respectively u v_(r+1)
and v_(r+1). Every factor with index at most r-1 fixes the resulting support
{r+1,r+2}. This proves the whole-word propagation identities for all r and the
versions starting at index 2 for r>=2. It also verifies the stated inverse order.

From direct X2 block action,

    rho(X2)=(q-u)v1 lambda,  lambda=-e1^T+e2^T.

Applying the propagated recurrence gives, by induction valid up to k=m,

    rho(Xk)=prod_(j=1)^(k-1)(q^j-u) v_(k-1) lambda.

For R2, direct three-coordinate action of its two bracket sides on v1 gives
(q-u)v2. For k>=3, both Rk bracket sides act on v_(k-1) as
(q^(k-1)-u)vk. Hence each defining relation image is zero for all legal
k<=m-1, including k=n when m=n+1. Setting m=n and m=n+1 separately proves
factorization through both repaired quotients. No previously nonzero element
is assumed to remain nonzero after adding an unchecked relation.

The (row 2,column 1) entry of rho(X3) is

    -(q-u)(q^2-u)/u = -u+q+q^2-q^3/u.

Its Laurent coefficient at u is -1, so it is nonzero. A homomorphism with this
nonzero image proves X3 nonzero in its source quotient. Extension of scalars
from F to Q(q,u) causes no logical gap: the constructed map is itself an
F-algebra map, and a zero source element would have zero image in any target.

In fact, the same check constructs a map into matrices over R[u,u^-1] for any
nonzero commutative unital base ring R and distinguished central q; the -1
coefficient still proves the image nonzero. No q denominator is used in the
generic witness. This stronger observation is recorded as a scope check, not
as a requested extension of the frozen published claim or as a new discovery.

## Scalar and singular controls

This analysis was completed and logged before inspecting the existing scalar
scope note. In a one-dimensional representation, invertible braid generators
all have the same scalar z. Direct independent factorization gives

    X2=(1-z)(z+q)/z,
    X3=(q^2-z^4)X2/z^2,
    R2 coefficient=(z^2-q)(z^2-z+1)/z^2,
    Rk coefficient=(z-1)(q^(k-1)+z^(2k-1))/z^k, k>=3.

If X3 is nonzero, R2 rules out z^2=q, leaving z^2-z+1=0. These primitive
sixth roots yield scalar witnesses for A3 in an algebraic extension of F.
For m>=4, R3 would force q^2=-z^5, impossible with transcendental q. Thus this
scalar route is blocked for A_n with n>=4 and all C_n with n>=3, but that
obstruction says nothing against the checked matrix witness.

At the special algebraic parameter q=z, the scalar construction does retain
X3 on four strands. On five or more strands it fails R4: independent reduction
of the numerator of R4*X4 modulo z^2-z+1 gives 8-4z!=0. The alternative q=-z
kills X2. This tests the distinction between generic and algebraic q.

The matrix witness requires u invertible (det B=-u); u=0 is inadmissible, not a
counterexample. Generic q,u are independent. The specialization u=q^3 is valid
over Q(q), annihilates X4 when m>=4, and retains X3. At q=1 or q=-1 the latter
specialization instead kills X3; the frozen audit does not claim survival at
every numerical q. On three strands X4 is not defined, so no X4 claim is made.

## Extra relations and coverage limits

The matrices also satisfy (B-I)(B+uI)=0. This is an additional kernel relation,
and does not invalidate their use as a witness: the proof checks every required
relation and then displays a nonzero image. It does prevent any inference of
faithfulness or finite dimension of the universal quotient. The twist identities
are B1 X2=-u X2 and (B1B2)^3 X3=u^3 X3; an extra twist parameter would have to be
matched to these scalars. No arbitrary unrelated scalar control is assumed.

The frozen finite suite covers matrix m=3,...,9, equivalently A3,...,A9 and
C3,...,C8. Its phrase “both indexing readings” does not itself mean that C9
was directly tested; the all-index proof supplies C9 and every higher case.
The frozen optional symbolic suite checks full words only for m=4,5 plus a
local arbitrary-amplitude identity. Neither finite suite proves the full claim
alone. The support proof above is the required all-index component.

Rational q,u test values evaluate the integral Laurent coefficient model.
They are not field homomorphisms Q(q)->Q: evaluation at any rational q has
poles for some rational functions in the full field. This does not compromise
the finite regression tests or the generic theorem, because the generic
F-algebra map is checked separately before any numerical evaluation.

No number of these matrix checks establishes the author's intended correction,
an unconditional answer to the literal defective presentation, universal
finite-dimensionality under additional relations, nonvanishing under every
specialization, or historical novelty/priority. Those remain outside this
family's verification scope.

## Post-conclusion comparison

After recording the independent conclusion, `SCALAR_SCOPE_CHECK.md` was read at
2026-10-01T13:41:56Z. It agrees with the independent scalar factorization,
generic four-strand obstruction, exceptional q=z four-strand case, and
five-strand obstruction. No correction to that note is needed. The stored
`verifier_rerun.json` likewise records the exact same `verify.py` hash and
42-case/1,590-check data; the comparison is included in the final verdict.
The historical review/verdict and sibling conclusions remain unread.

## Reproduction commands

From `/Users/alec/Documents/Math`:

    .venv/bin/python draft_pr_publication_program_20260930/audits/pr13_11000263/reproduction_family/replay_frozen.py
    .venv/bin/python draft_pr_publication_program_20260930/audits/pr13_11000263/reproduction_family/independent_laurent_check.py

No environment mutation, canonical-file mutation, Git mutation, or external
communication was performed. All retained artifacts are in this family folder;
the copied execution inputs/outputs remain in ignored scratch.
