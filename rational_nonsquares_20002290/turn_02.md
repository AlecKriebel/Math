# Attempt 2: diagonal-fiber normal form and a one-square lower bound

## Strategy

Attempt 1 showed why finite fixed classes or places do not suffice. Here we search all positive-existential formulas through their exact algebraic normal form and try the simplest genuinely quantified fragment. The main new result is a rigorous lower bound: nonsquares cannot be defined by a finite disjunction of primitive-positive formulas containing at most one square-predicate atom each, even with arbitrarily many additive equations and existential variables.

## Exact normal form

Every positive-existential formula over M=(Q;0,1,+,P₂) is equivalent to a finite disjunction of formulas

exists y: A y+B x+C s=d, and P₂(s₁),...,P₂(s_k),

with rational fixed matrices. Here each original square atom P₂(l(x,y)) is replaced by P₂(s_j) and an additive equation s_j=l(x,y). Existing equalities are also affine linear. Rational coefficients abbreviate legal additive equations after clearing denominators and moving negative terms to the opposite side.

Eliminate the unconstrained y by rational Gaussian elimination. A finite rational linear system A y=v is solvable in Q exactly when every rational left-null vector of A annihilates v. Choosing a basis of that nullspace therefore yields an equivalent formula

exists s₁,...,s_k: C' s+B' x=d', and all P₂(s_j).       (NF)

This is an equivalence in the original language. As a metamathematical description of its fibers, one can replace s_j by z_j² and obtain a simultaneous system of diagonal quadratic equations

sum_j C'_{ij} z_j²=d'_i-B'_i x.                       (DQ)

The square roots z_j do not occur as arguments in the original formula; they only describe the semantics of P₂. Thus no illicit squaring function or multiplication has been introduced. Conversely, every finite system of the displayed diagonal form translates into (NF). General mixed quadratic terms or coefficients depending multiplicatively on x are not covered.

For several free variables, the same construction applies with x a vector. This exact normal form isolates the issue: one needs a finite union of fixed-coefficient diagonal-quadratic families whose rational fibers are nonempty exactly over nonsquare parameters.

## Classification with one square atom

Consider one primitive-positive disjunct with k≤1. After the elimination above, the feasible pairs (x,s) form an affine rational subspace L of Q², with the remaining condition P₂(s). An inconsistent linear system gives the empty set. Otherwise:

- If L is a point, the projected set is empty or a singleton.
- If L is a vertical line, x is fixed, again giving a singleton or empty set.
- If L=Q², the projected set is all Q, since s=0 is allowed.
- If L is a nonvertical line, write s=a x+b. For a=0 its projection is all Q or empty, depending on P₂(b). For a≠0 its projection is {x:P₂(a x+b)}.

The k=0 case is included: a projection of a rational affine subspace onto one coordinate is empty, a point, or Q.

## Counting obstruction on positive integers

**Theorem.** No finite union of the sets just classified equals Q\P₂.

**Proof.** If such a union equaled N, it could not contain an all-Q constituent, since 0 is a square. Singletons contribute only finitely many positive integers. Fix a remaining constituent S={x:P₂(a x+b)}, a≠0. Choose a positive integer D with Da and Db integral. If n is an integer and a n+b=q² with q in Q, then

(Dq)²=D²(a n+b)=A n+B,

where A=D²a and B=D²b are integers and A≠0. Because a rational whose square is an integer must be integral, Dq is an integer. For 1≤n≤H, the absolute value of A n+B is at most |A|H+|B|. Hence at most 2 sqrt(|A|H+|B|)+1 choices of the integer Dq occur, and each gives at most one n because A≠0. Thus |S∩{1,...,H}|=O(sqrt H). This estimate also handles negative a; when the radicand becomes negative it contributes nothing.

A finite union of these constituents and singletons still has O(sqrt H) positive integers up to H. But N has H-floor(sqrt H) such integers. These cardinalities cannot agree for all H. □

This is a proof over the unbounded domain, not evidence from a finite enumeration. It allows arbitrary fixed rational parameters because they can be eliminated additively. The bound concerns the number of literal P₂ occurrences after expansion; an abbreviation for positivity or nonzero contains several square atoms and cannot be counted as free.

## What this does and does not establish

The theorem does not say that every formula with two square atoms succeeds, nor that a finite number of atoms cannot succeed. In particular, projections with multiple square variables can have dense value sets and the O(sqrt H) argument then fails. The four-square representation of all nonnegative rationals is an immediate warning against extrapolating the count.

The normal form points toward a stronger next test: one independent diagonal equation, but any number of square atoms. If that entire family also fails, a successful definition must use genuinely simultaneous diagonal constraints, rather than merely longer sums of squares.

Fresh substantive attempt count: 2/5. Full Question 6 remains unresolved.
