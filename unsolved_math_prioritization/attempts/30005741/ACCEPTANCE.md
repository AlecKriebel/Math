# Acceptance of partial Poisson length equalities

## Decision and review status

**Accept Theorems A–D without mathematical correction.** Both unrestricted source questions remain unresolved by these results.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

Both full questions remain unresolved by this work. No novelty, priority, comprehensive literature-survey, or current global-openness claim is made.

## Exact accepted setting and indices

Let F be any field of characteristic p>0 and L any Lie algebra with alternating bracket, including at p=2. Put R=s(L)=S(L)/(v^p:v in L); no restricted structure or finite dimension of L is assumed. Products and brackets of subspaces mean their linear spans. The ordinary lower series starts gamma_1=R and gamma_(n+1)={gamma_n,R}; the strong powers start R^(0)=R and R^(n+1)={R^(n),R}R. Class c is the least index with gamma_(c+1)=0 or R^(c)=0 respectively. Ordinary and strong derived series start at index zero, and derived length is the first zero index. The nonzero abelian unital algebra has all four invariants equal to 1.

Question 1 concerns equality of nilpotency classes at p=2 or 3 assuming R is Lie nilpotent. Question 2 concerns equality of derived lengths at p>2 assuming R is solvable. They are separate questions.

## A. Nilpotent L with dim L' <= 2

In every positive characteristic the ordinary and strong nilpotency classes agree. The common class is 1 if L'=0; p if dim L'=1; 2p-1 if dim L'=2 and [L',L]=0; and 3p-2 if dim L'=2 and [L',L] is nonzero.

The full proof retains the truncated finite-support monomial basis, the breadth lemma valid over every field including F_2, and the four-dimensional filiform subalgebra extraction. In the noncentral two-dimensional case gamma_3 is one-dimensional and gamma_4=0. Its explicit left-normed word starts with x, appends (xy,x) p-1 times, then xy p-1 times, and evaluates to (-1)^(p-1)x z^(p-1)w^(p-1), a nonzero monomial with 3p-2 entries. The global weight upper bound gives the identical class without bounding the dimension of L. No division by 2 or 3 is introduced.

## B. Full-image class-two algebras and direct sums

If L has class two, m=dim L' is finite, and [x,L]=L' for some x, the common class is 1+(p-1)m. Choose [x,y_i]=z_i forming a basis of L'. Appending xy_i p-1 times each to x gives the nonzero word x product_i z_i^(p-1). The central-ideal upper bound matches it.

The proof retains the tensor-word lower bound c+d-1 and additive weight upper bound for the specified nilpotent families. Equality is preserved under direct sums with only finitely many nonabelian summands. Adding an arbitrary-dimensional central abelian direct summand preserves all four series by tensoring with its unital symmetric truncation. No assertion about arbitrary nonsplit central extensions or a general derived-length tensor formula is made.

## C. Derived lengths when dim L' <= 1

For p>2 the common length is 1 if L'=0, ceil(log_2(p+1)) if nonzero L' is central, and 1+ceil(log_2 p) if L' is noncentral.

In the central case the strong upper bound is D_n subset z^(2^n-1)R. The embedded six-monomial space V=span(1,x,y,x^2,xy,y^2) is perfect under the constant symplectic bracket, giving z^(2^n-1)V subset delta_n and the matching nonvanishing. All six bracket identities remain present. They work at p=3; the central-case proof does not extend to p=2 because the squared monomials vanish.

In the noncentral case the full decomposition L=(Fx direct-sum Fz) direct-sum C with [x,z]=z and arbitrary-dimensional central C is retained. For T=F[x,y]/(x^p,y^p), {x,y}=y, both derived series satisfy delta_n(T)=D_n(T)=y^(2^(n-1))T for n>=1. The explicit monomial constructions include the top x-exponent row. This formula and equality of entire series also hold at p=2, without asserting a general characteristic-2 derived-length equality.

## D. Finite-dimensional and finite-field counterexample reduction

For either question in its specified characteristic range, any counterexample over any field and any dimension yields one over a finite field with finite dimension and the identical unequal pair of finite invariants.

The necessity directions of Monteiro Alves–Petrogradsky Theorems 4.1 and 4.3 are cited inputs. They supply finite-dimensional L' and the corresponding finite strong invariant; the solvability input retains p>2. Last-nonzero expressions have finite support S, and the Lie algebra they generate lies in span(S)+L', which is finite-dimensional and bracket closed. The injective map s(H)->s(L) retains both witnesses and every required zero-stage identity.

For finite-dimensional H, the truncated basis has p^d monomials. The complete proof retains recursive multilinear strong and ordinary expressions, all finite basis-input zero equations, and one nonzero coefficient f,g for the last nonzero stages. The actual coefficient subring A_0=F_p[c_ij^k] subset F retains all inherited relations; A=A_0[(fg)^(-1)] makes both witnesses units. A maximal-ideal quotient preserves alternation, Jacobi, the free d-element Lie basis, the p^d monomial basis, all zero identities, and the two nonzero witnesses. Zariski's lemma makes the residue field a finite algebraic extension of F_p. The complete elementary proof of that lemma remains in the appendix.

The reduction gives neither a dimension bound nor a field-degree bound, an actual counterexample, an exhaustive finite search, or preservation of isomorphism type. Reduction to the prime field alone is not asserted. The F_9 coefficient-ring illustration is retained.

## Historical supporting checks and exact remaining gap

The independent audit checked 31 finite cases including all 25 candidate cases, matching 80 stored full dimension vectors. It also checked maximal words through p=13, the quadratic-space characteristic boundary, small-field breadth maps, a direct sum, central direct summands, an F_9 coefficient example, literal-factor bracket comparisons and Jacobi/Leibniz identities. These are finite supporting checks, not universal proof. Saved normal, -O and -OO independent outputs agree mathematically after removing the recorded optimization flag; the candidate receipts also have timing metadata. The distinct receipt hashes are retained in VERIFICATION.json, without claiming byte equality.

The analytical characteristic-2 boundary fixture is the six-dimensional Lie algebra with basis x,y_1,...,y_5 and [x,y_i]=y_i, all other defining brackets zero. The saved finite calculation reports ordinary and strong derived lengths 3 and 4. The raw dimension-vector table is omitted. It is supporting boundary evidence outside Question 2, not a new universal theorem or novelty claim.

The nilpotency question remains unresolved for general class-two bracket maps lacking a full-image adjoint vector and higher-class algebras with larger L'. The derived-length question remains unresolved beyond the proved dim L'<=1 range. Failure of the source's division-by-3 or division-by-2 method at small characteristic does not establish failure of the desired equality.

The complete written mathematical proofs, analytical constructions, source-theorem dependencies, and finite-field reduction appendix are retained. This is not a computational reproduction package: executable code, raw finite dimension-vector datasets and certificates, copied source documents and images, and private coordination material are omitted. Historical finite computations are supporting evidence only; they do not prove either unrestricted equality. The historical computations cannot be reproduced from this edition alone.

## Editorial changes and source limits

The central-extensions heading is clarified to central direct summands, and Siciliano's contribution uses its actual title, Solvability of symmetric Poisson algebras, followed by the workshop venue. Neither change alters a hypothesis or mathematical argument. The original candidate and audit remain unchanged. Source authentication and selected-page inspection are historical; they do not certify full-document inspection or a new literature survey. Exact original and distributed document identities are bound in ACCEPTANCE.json.
