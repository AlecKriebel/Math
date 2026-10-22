# Proof attempt 4: deliberately hiding the short vector in a tail block

Date: 2026-10-20 UTC. ID 8800068 / AMR-087-0068.

## Outcome

A proposed deliberate stationary-basis construction for the growing evaluation ideals is ruled out: keeping a long initial flag of their natural relation vectors and hiding the short vector by arbitrary changes in a small remaining block cannot yield an LLL-reduced basis. At the scale a approximately 2^(n/4), at least n/2-O(1) trailing dimensions must be involved. This is a proved obstruction to an infinite class of structured attempts, not a global bound over all reduced bases.

## 1. Construction under test

Use L=L(a,a^(n-1)+1,n), a>=2, with natural basis

    r_i=a e_i-e_(i+1),  0<=i<=n-2,
    v=e_0+e_(n-1).

The preceding attempts prove ideal closure, determinant a^(n-1)+1, and lambda_1=sqrt(2). To imitate the general near-critical construction's short relation v=2b_n-b_(n-1), take the deliberate last-block change

    b_(n-1)=2r_(n-2)-v,
    b_n=r_(n-2),

with r_0,...,r_(n-3) unchanged. This is unimodular, so it is an exact basis of the same ideal, and v=2b_n-b_(n-1) is now hidden rather than an individual basis vector. More generally the coefficient 2 may be any integer t, with b_(n-1)=t r_(n-2)-v and b_n=r_(n-2). An arbitrary unimodular tail transformation, not just this one, is covered by the theorem below.

The objective is an already-reduced poor basis, so it is not enough that a basis is long or hides v. The full LLL inequalities must survive the change.

## 2. Relation-row singular bound

Let R be the (n-1)-by-n matrix with rows r_0,...,r_(n-2). For any real coefficient vector z in R^(n-1),

    zR = a(z_0,...,z_(n-2),0) - (0,z_0,...,z_(n-2)).

The reverse triangle inequality gives

    ||zR|| >= (a-1)||z||.

Consequently, if distinct raw relation rows are ordered arbitrarily and Gram-Schmidt orthogonalized, every resulting Gram-Schmidt length is at least a-1. Indeed, the distance of a selected row to the real span of preceding selected rows is the minimum of ||zR|| over coefficient vectors whose coordinate at that selected row is 1 and whose other nonzero coordinates occur only among preceding rows. Such z have norm at least 1.

This lower bound is unchanged by multiplying each selected row by a sign and adding arbitrary integer combinations of its preceding rows. Such operations preserve the successive real prefix subspaces and each Gram-Schmidt pivot up to sign. **Arbitrary unimodular mixing of the entire selected prefix is not included:** it can change those pivots and is a remaining route.

## 3. Tail dimension obstruction

**Proposition.** Let 1<=k<n and r=n-k. Suppose B is a basis of L whose first k vectors are k distinct raw relation rows in some order, followed by arbitrary sign changes and integer additions of earlier rows to later rows within that ordered prefix. The remaining r basis vectors may be any completion whatsoever. If B is (3/4,1/2)-LLL-reduced, then

    a-1 <= 2^((r+1)/2).

**Proof.** Let P be orthogonal projection onto the complement of the real span of the first k basis vectors. Because the first k vectors belong to a lattice basis, their integer span is primitive. Hence P(L) is an r-dimensional lattice with basis (P b_(k+1),...,P b_n). Projecting away the entire initial prefix preserves all subsequent Gram-Schmidt lengths and coefficients; thus this projected tail basis is itself LLL-reduced.

The vector v is independent of the span of all n-1 relation rows, since those rows together with v form a full basis. Therefore P(v) is nonzero. Projection does not increase norm, so

    lambda_1(P(L)) <= ||P(v)|| <= sqrt(2).

Apply the classical r-dimensional SVP guarantee to the projected tail:

    ||b_(k+1)^*|| = ||P b_(k+1)||
       <= 2^((r-1)/2) lambda_1(P(L)) <= 2^(r/2).

On the other hand, section 2 gives ||b_k^*||>=a-1. The LLL inequalities across the boundary of prefix and tail imply

    ||b_(k+1)^*||^2 >= (3/4-mu_(k+1,k)^2)||b_k^*||^2
       >= (1/2)(a-1)^2.

Combining the bounds proves the claim.

## 4. Consequences for the explicit attempted basis

For n>=3 and a two-dimensional tail (r=2), the necessary condition is a-1<=sqrt(8). Thus for every integer a>=4, no completion of the first n-2 raw relation rows of the stipulated type is LLL-reduced. In particular, the deliberately hidden-v basis from section 1 fails for every choice of t, as does every other unimodular change confined to that last two-dimensional block.

For a one-dimensional tail the necessary condition is a<=3; the stronger direct boundary estimate can sometimes improve this. The proposition deliberately uses the general dimension-r guarantee so that arbitrary tail completions are covered uniformly.

For a=2^ceil(n/4), the necessary inequality is

    r >= 2 log_2(a-1)-1 = n/2-O(1).

Thus a bounded-size or sublinear trailing-block modification cannot solve the sharp target along this family while preserving the specified initial relation flag. At least about half the dimensions must be reorganized. This is a structural consequence, not a statement inferred from unsuccessful random LLL outputs.

## 5. Exact scope and remaining gap

The conclusion does not apply to every basis whose first k vectors lie in the relation sublattice. A general unimodular transformation of those k vectors may make the last prefix Gram-Schmidt pivot very small, defeating the singular-pivot argument. Nor does the proposition control a fully nonlocal basis with no preserved natural prefix flag. Those are genuine remaining possibilities, not established constructions.

No new finite search is used as evidence for the universal proposition. Its proof covers all dimensions and all completions satisfying the specified prefix condition. The attempt refutes the proposed local hiding mechanism, not the general ideal-lattice exponent-1/2 target.

Attempt 4 outcome: **deliberate short-relation hiding via a bounded tail block ruled out; quantitative minimum mixing dimension established; unrestricted target unresolved.**
