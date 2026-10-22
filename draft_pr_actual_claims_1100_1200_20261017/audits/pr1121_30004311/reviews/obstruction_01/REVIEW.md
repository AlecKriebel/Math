# Independent exact-scope and universal-obstruction review

## Decision and identity

**PASS for the assigned family.** Section 6 of the frozen proof excludes every asymmetric product of two trivial left braces under the full admissible normalized symmetric-2-cocycle definition. It does not restrict to a preselected bilinear construction family. No mathematical repair is required for that obstruction or the retained fixed-set, center, and derived witnesses.

Reviewed PR: 1121. Exact supplied head: `f86b108ac1bc024302648eee9f47f74e26c810ec`. Reviewed `PROOF.md`: 14,213 bytes, SHA-256 `68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75`. The checker independently refuses different proof bytes. The head is the supplied review identity; this family made no Git/ref/index/publication mutations and does not claim to have independently re-fetched that Git commit.

This conclusion is an independent mathematical review, not formal proof-assistant certification or a historical priority determination. Prior acceptance statements were not used as premises. This family specifically reviewed the original question, definition scope, universal obstruction, and retained intrinsic witnesses. It did not conduct a broad novelty audit.

## Fresh primary-source check

The official [OWR 51/2019 report](https://ems.press/content/serial-article-files/46831), printed page 3228 / physical PDF page 22, asks whether each finite, nontrivial simple left brace with metabelian multiplication and abelian multiplicative Sylow subgroups has an asymmetric product presentation with two trivial factors. The manuscript retains every hypothesis and excludes precisely that conclusion. Its use of an isomorphism invariant is sufficient; a specific coordinate presentation is not required.

[arXiv:2001.08905v1, Theorem 2.2](https://arxiv.org/pdf/2001.08905v1), physical page 3, uses a normalized symmetric cocycle, an action by brace automorphisms, an admissibility identity, cocycle-twisted addition, and semidirect multiplication. The lambda formula agrees with the manuscript, including its minus sign. [arXiv:1705.08493v1, Theorem 3.1](https://arxiv.org/pdf/1705.08493v1), physical page 6, gives the same definition and formula. Its preceding normalization agrees as well. Thus there is no discrepancy in scope between the two inspected primary definition sources.

All three PDFs were freshly obtained on 2026-10-17 UTC, extracted privately, and their relevant rendered pages visually inspected. `SOURCE_RECEIPT.json` records URLs, sizes, SHA-256 identities, retrieval timestamps, and private paths. No source PDF, extracted source text, or source image is included among the public review artifacts. The original 2016 paper was not newly inspected; the two inspected papers explicitly attribute the framework to Catino, Colazzo, and Stefanelli.

## Independent universal proof

Let a finite brace C have any allowed presentation with trivial factors T and S. Write their operations additively. Starting with a normalized symmetric 2-cocycle b and the admissible action alpha, its operations are

    (t,s)+(u,v) = (t+u, s+v+b(t,u)),
    (t,s) o (u,v) = (t+alpha_s(u), s+v).

The cocycle identity implies b(t,0)=b(0,t)=0. Its additive difference and lambda map are consequently

    (t,s)-(u,v) = (t-u, s-v-b(t-u,u)),
    lambda_(t,s)(u,v) = (alpha_s(u), v-b(alpha_s(u),t)).

These are valid before biadditivity is known. In particular, no use of a bilinear subtraction formula has slipped into the reduction.

Because both factors are trivial, `(t,0) o (u,0)=(t+u,0)`. Every left brace satisfies lambda_(a o c)=lambda_a lambda_c. Evaluating this identity on `(w,0)` gives

    b(w,t+u) = b(w,t)+b(w,u).

This conclusion uses lambda as an actual multiplicative action, which admissibility guarantees. It does not assume the intended obstruction, a special source construction, or additivity of b. Symmetry now gives additivity in both entries. Nonlinear symmetric cocycles outside this consequence simply cannot be admissible with both factors trivial. Additivity of lambda_(0,s) additionally gives

    b(alpha_s(u),alpha_s(v)) = b(u,v).

Thus the replacement of an admissible symmetric cocycle by a biadditive invariant one is forced, not a restriction of the target class.

Fix a prime p and let T_p and S_p denote the ordinary primary subgroups of the finite abelian factor groups. If t is p-primary and u is q-primary for distinct p and q, b(t,u) is killed by coprime prime powers, so it is zero. If both are p-primary, b(t,u) is p-primary in S. Therefore the set

    P = T_p x S_p

is an additive subgroup for the twisted addition. It has order |T_p||S_p|, the full p-part of |C|, hence is the additive Sylow subgroup. This reasoning does **not** assert that its additive group is the direct product of the two factor groups. For example, in characteristic two its exponent can increase; the order-4 and order-36 controls below explicitly exercise that case.

Every alpha_s preserves T_p because it is an automorphism of T. Hence P is also a multiplicative subgroup, again of the full p-power order, and therefore a multiplicative Sylow subgroup. No Sylow normality is needed.

Suppose the multiplicative Sylow subgroups are abelian. Within P, commuting `(t,0)` and `(0,s)` shows that alpha_s(t)=t for t in T_p and s in S_p. For a=(t,s), c=(u,v) in P, the lambda formula followed by the **twisted** difference formula gives

    a*c = (u,v-b(u,t))-(u,v) = (0,-b(u,t)).

There is no leftover correction term: the first coordinate of the difference is zero, and b(0,u)=0. Write w=-b(u,t), which belongs to S_p. On P, lambda_(0,w) is the identity: alpha_w is identity on T_p, and b(alpha_w(q),0)=0. Thus

    (a*c)*d = 0 for all a,c,d in the additive Sylow p-subbrace.

This proves the desired lemma for all finite two-trivial-factor presentations, regardless of factor order, exponent, cocycle normalization coordinates, or additive splitting. Neither simplicity nor metabelianness is required for the lemma. Degenerate zero factors cause no exception.

In the proposed B, P_5=R x {0} x {0}. Its star operation is ordinary multiplication in R=x F_5[x]/(x^5). Therefore

    ((x,0,0)*(x,0,0))*(x,0,0) = (x^3,0,0) != 0.

A brace isomorphism preserves both star operations and the characteristic additive Sylow subgroup. The displayed nonzero value therefore rules out every allowed presentation, including an undiscovered one with unrelated coordinates. Once the independently displayed construction and simplicity arguments are combined with this lemma, the negative answer has the exact original target. There is no transferred unsupported classification problem.

## Retained intrinsic checks

The extra obstructions are valid in their stated simple two-trivial-factor class. Here is an independent justification to make the hidden hypotheses explicit.

A nontrivial simple product has T and S nonzero; otherwise the result is trivial. Let A=rad(b). The subset A x {0} is an additive subgroup because b vanishes there, is invariant under alpha by b-invariance, is multiplicatively normal, and is lambda invariant. It is a proper ideal, so simplicity forces A=0.

Let H be the subgroup of T generated by all alpha_s(t)-t. It is alpha invariant. The subset H x S is additively closed and lambda invariant. The map `(t,s) -> t+H` is a multiplicative homomorphism onto the abelian group T/H, and its kernel is H x S. Since S is nonzero, this ideal is nonzero; simplicity forces H=T. In the semidirect multiplicative group, the commutator subgroup is H x {0}, because the two factors are abelian and these action differences generate all commutators. Hence D=[G,G]=T x {0}.

An element `(u,v)` fixed by every lambda must have b(u,t)=0 for every t, by testing lambda_(t,0). Thus u=0, and conversely every `(0,v)` is fixed. Therefore Fix(C)={0} x S is a multiplicative complement to D, and

    |Fix(C)| = |G/D|.

Furthermore D*C is contained in Fix(C), since `(t,0)*(u,v)=(0,-b(u,t))`. This proves the exact intrinsic implication used by the derived witness.

The subset {0} x ker(alpha) is also a proper ideal: its elements are lambda fixed and multiplicatively central. Simplicity makes alpha faithful. A central `(t,s)` first has alpha_s=id by commuting with T x {0}, hence s=0; it then has alpha_u(t)=t for every u. Invariance of b gives b(t,alpha_u(v)-v)=0. Those differences generate H=T, so t belongs to rad(b)=0. Thus G has trivial center. This argument makes no assertion about general simple braces with nontrivial factors.

For the proposed B, lambda_(x,0,0) alone forces a globally fixed `(u,w,Z)` to have xu=0 and Mw=w, since eta(x)=1 in F_5. Thus u is a multiple of x^4 and w=0. Conversely every `(c x^4,0,Z)` is fixed by all lambdas. Hence |Fix(B)|=10.

The displayed group coordinates give

    G = (C_5^3 semidirect_tau C_2) x (V semidirect_M C_5).

The two commutator images have orders 25 and 16. Therefore |D|=400 and |G/D|=50, which differs from 10. The center consists exactly of `(E(c x^2),0,0)` for c in F_5, and has order 5. In particular the stated `(x^2+3x^4,0,0)` is a nonzero central element.

For k=(0,0,1), h=(E(2x),0,0), and commutator convention `[k,h]=k o h o k^-1 o h^-1`, reflection sends the logarithm 2x to -2x. Thus the commutator has logarithm -4x=x, and

    d = (x+3x^2+x^3+4x^4,0,0),
    d*x = (x^2+3x^3+x^4,0,0),
    x*(d*x) = (x^3+3x^4,0,0) != 0.

Every sign, coefficient, commutator orientation, and zero coordinate matches the manuscript. These three extra obstructions are logically redundant to the primary triple-product argument, but none needs removal or repair.

## Exact computation and falsification controls

`check_boundaries.py` was independently written from the displayed definitions, uses only the Python standard library, imports no author implementation or historical table, and uses explicit exceptions rather than removable assertions. Computation supplements the universal reasoning above; it is not claimed to exhaust all presentations or all 20,000-cubed brace triples.

The small finite controls check identities, inverses, both associativities, and lambda additivity on all indicated triples:

| Control | Full brace triples | Outcome |
| --- | ---: | --- |
| Order 25, T=S=C_5, b(t,u)=tu, trivial action | 15,625 | Nonzero star square `(0,4)`; all 15,625 triple products zero. A stronger square-zero claim would fail. |
| Order 4, T=S=C_2, b(t,u)=tu, trivial action | 64 | Coordinate `(1,0)` has additive order 4; all 64 triple products zero. |
| Order 36, T=S=C_2 x C_3, componentwise b, trivial action | 46,656 | Twisted primary sets equal the true additive primary subgroups, of orders 4 and 9; all 64 and 729 primary triples zero. The 2-primary additive exponent is 4. |
| Nonlinear b(t,u)=t^3+u^3-(t+u)^3 on C_5 | Not a brace | Normalization, symmetry, and all 125 cocycle triples pass; lambda composition on three copies of `(1,0)` gives `(1,2)` versus `(1,3)`, so admissibility fails. |
| Order 8, T=C_2^2, S=C_2, dot-product b, coordinate-swap action | 512 | A valid two-trivial-factor brace with nonabelian multiplication has 128 nonzero triple products. Abelian Sylow is an essential hypothesis. |

For B, the checker generates all 20,000 multiplicative elements from nine displayed generators before relying on generator tests. It performs 180,000 actual target/generator comparisons for each of the fixed-set and center checks, confirms fixed-set order 10 and center order 5, tests the central witness against all 20,000 elements, checks both inverse identities for all 20,000 elements, and independently computes the commutator and all stated star witnesses. Results are in `RESULTS.json`. Normal and optimized runs are compared byte for byte in `RUN_RECEIPT.json`.

## Remaining gap and recommended disposition

**No gap found in the assigned mathematical family.** The crucial exhaustive quantifier is discharged by the universal proof, not by finite searches or existing construction classifications. The input proof can retain its exact problem statement, full symmetric-cocycle scope, decisive Sylow triple-star argument, and all three intrinsic cross-checks. The separate construction audit and any historical novelty investigation remain outside this family's acceptance boundary. No external outreach was prepared or initiated.
