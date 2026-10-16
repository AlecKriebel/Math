# Independent computation-family derivation, before original checker/verdict inspection

Recorded 2026-10-15 UTC. Scope: imported universal realization claim for prescribed matrix subgroups, restricted audit of candidate X={0,2/3,1}, A=(1/5)[[3,-4],[4,3]]. Read only the charter, identity preflight, original inventory, and complete private source record before this note. No original proof, checker, wrapper, verdict, or other-family reasoning was inspected.

## Universal arithmetic argument

Let (a_0,b_0)=(1,0), (a_{n+1},b_{n+1})=(3a_n-4b_n,4a_n+3b_n). Then A^n=5^{-n}[[a_n,-b_n],[b_n,a_n]]. For every n>=1, (a_n,b_n)=(3,4) modulo 5. The base n=1 is immediate; if the residues are (3,4), the next residues are (9-16,12+12)=(3,4). Thus b_n is never zero and A^n is never I. For n<0, A^n=I would imply A^{-n}=I. This proves infinite order for every nonzero integer exponent. The finite exact controls below will test this recurrence and its identities but cannot substitute for this induction.

Direct multiplication gives A^T A=I and det A=1. Hence every integer power preserves every Euclidean vector length, has operator norm 1 and determinant 1; it has no strict contraction in either a strict operator-norm or vector-length sense. The exact source convention still requires source-family verification. Norm preservation does not require using irrational angles or floating arithmetic.

Stronger finite controls will include independent Gaussian-integer and Fraction-matrix multiplication, inverse powers, a_n^2+b_n^2=25^n, the induction residue, and selected hostile near-rotation matrices to ensure controls detect broken orthogonality or order claims. Identity, -I, and quarter-turn matrices are finite-order negative controls: orthogonality alone must not be accepted as infinite order.

## Separated-end combinatorial mechanism and boundary controls

Suppose K is a connected compact core and S\\K has n connected tails U_1,...,U_n, each with one of n distinct ends, no additional ends. If a connected h(K) is disjoint from K, it lies in a single U_j. The connected set K together with all other U_i lies in one component of S\\h(K), so that component contains at least n-1 of the original ends. But homeomorphism invariance of the tail decomposition says every component of S\\h(K) has exactly one end. For n>=3, n-1>=2 is a contradiction. For n=2 the outside component has one end, so this combinatorial obstruction vanishes; translating a compact band in a cylinder gives disjoint copies. For n=1 it also vanishes; the existence of a nondisplaceable core does not follow from this count. These controls test the separated-end counting mechanism, not existence of the required core on every surface, analytic proper discontinuity, or source end conventions.

## Trust and success boundary

This family will authenticate the complete 27-file original snapshot against both supplied external pins and the actual immutable Git tree at head 704685791ec0053dc0a52590fdef49ed4aae61d9 before and after replay. Executing authenticated historical code is an explicit trust step; it is not a generic safe loader for arbitrary Python. Exact replay and hostile-input guards can verify consistency and authenticity, but do not prove the universal topology/conformal claims or certify novelty/current openness.
