# Independent analytic and Lubin–Tate audit

Audit started 2026-10-24 19:44:37 UTC. Reviewer did not author the target proof.

## Exact conditional claim audited

For `n>2`, a prime `p`, and a nonzero coefficient of the integral polynomial `Q_n` modulo `(p,x_1^n,...,x_n^n)`, the analytic lemma gives a distinct-neighbor-sum cyclic enumeration of every `n`-point set in the maximal ideal of a complete mixed-characteristic discrete valuation field, under a one-dimensional integral formal group law. The Lubin–Tate construction then transfers this assertion to every finite abelian `p`-group, with no exponent or rank bound.

This review does **not** verify the claimed coefficient witnesses for `3≤n≤9`, the unrestricted coefficient conjecture, mixed-prime groups, or novelty. The strongest result verified here is the conditional implication.

## Verdict

**The analytic lemma and the finite abelian p-group embedding are valid under their stated hypotheses. No counterexample or central missing hypothesis was found.** The target leaves some standard arguments compressed; the details below close them without adding a new research assumption. The word “commutative” could be made explicit in the analytic lemma. It is already valid for the Lubin–Tate application, and is automatic for a one-dimensional formal group law over a characteristic-zero domain.

## 1. Operator substitution and reduction: direct proof

Write `g(U)=U^n+c_(n-1)U^(n-1)+...+c_0`. Since every `b` lies in `m`, each lower coefficient lies in `m`. In fact the coefficient of `U^(n-j)` lies in `m^j`, but that stronger assertion is unnecessary.

Identify the module `E` with the quotient algebra

`A=O[x_1,...,x_n]/(g(x_1),...,g(x_n))`

using its unique representatives of individual degrees `<n`. The existence and uniqueness of representatives follow from successive monic division, or tensoring the monic one-variable quotients. Thus `E` is finite free and complete, and the operators `T_i` are the commuting multiplication operators of this algebra. Their integral matrices preserve `m^r E` for every `r`.

The polynomial relation gives `T_i^n E ⊂ mE`. Consequently, for every multi-index `alpha`,

`T_1^(alpha_1)...T_n^(alpha_n) E ⊂ m^(r(alpha)) E`,

where `r(alpha)=Σ_i floor(alpha_i/n)`. Writing `D=|alpha|` yields

`D ≤ n r(alpha)+n(n−1)`,

so `r(alpha) ≥ (D−n(n−1))/n`. In particular, for any fixed `r`, all sufficiently high-total-degree monomials act into `m^r E`. Hence for an arbitrary integral series `f=Σ_alpha a_alpha x^alpha`, the sum `Σ_alpha a_alpha T^alpha` converges in the complete finite free module `End_O(E)`, independently of the order in which terms are summed. Define

`rho(f)=(Σ_alpha a_alpha T^alpha)(1)`.

This is exactly the limit of ordinary finite-polynomial remainders. It is also the continuous `O`-algebra evaluation map to `A`; the argument does not rely on an unproved formal division theorem.

Modulo `m`, one has `A/mA = k[x_1,...,x_n]/(x_1^n,...,x_n^n)`. This quotient kills every monomial of total degree greater than `n(n−1)`, so reduction of the infinite sum becomes a finite monomial truncation. No nonzero surviving monomial changes its degree. Therefore if `P_F` starts in total degree `d` with degree-`d` part `Q_n`, the degree-`d` part of `rho(P_F) mod m` is exactly `Q_n mod (p,x_1^n,...,x_n^n)`.

An integer coefficient not divisible by `p` maps to a nonzero element of the residue field: the prime subfield `F_p` embeds in that field. Thus the certificate forces `rho(P_F)≠0`, irrespective of ramification, the residue degree, or closeness of the grid points.

## 2. Equality at grid points and interpolation

For `beta=(b_1,...,b_n) ∈ B^n`, define `ev_beta:E→O` by polynomial evaluation. This map is `O`-linear and sends `m^rE` into `m^r`, because all the `b_i` are integral. It is therefore continuous. Every finite polynomial and its monic remainder have the same value at `beta`, because all `g(b_i)` vanish.

Let `f_≤D` be the truncation by total degree. On the operator side, `rho(f_≤D)→rho(f)` by the preceding estimate. On the scalar side, if `v` is normalized with `v(m)=1`, then each degree-`D` term at `beta` lies in `m^D`; there are only finitely many terms at each degree. Hence `f_≤D(beta)→f(beta)`. Continuity now gives

`rho(f)(beta)=lim_D rho(f_≤D)(beta)=lim_D f_≤D(beta)=f(beta)`.

This proves the claimed equality with no integral invertibility of interpolation denominators.

The evaluation map from polynomials of individual degrees `<n` to `K^(B^n)` is injective. For one variable this is the root bound for a nonzero degree-`<n` polynomial at `n` distinct field elements. Inductively, fix all but one coordinate and apply this root bound; then repeat for the coefficient polynomials in the remaining variables. Equivalently, the tensor-product Vandermonde matrix has a nonzero determinant over `K`. Its determinant generally lies in `m`, which does not affect invertibility over the field.

Thus a nonzero remainder has a nonzero grid value, and the original analytic series has the same nonzero value there.

## 3. Cancellation and evaluation of group identities

Every integral formal series converges at tuples in `m`; a formal series with zero constant term maps such tuples back into `m`. Therefore formal group identities, including associativity, commutativity, and the inverse identities, remain valid after evaluation, as the target needs.

Under commutativity, `F(u,v)=F(v,w)` can be rewritten `F(u,v)=F(w,v)` and cancelled by adding the formal inverse of `v`. That inverse is an integral formal series, so it also converges on `m`. This gives `u=w`.

If “formal group law” is defined without including commutativity, characteristic zero still supplies it in dimension one. Over the fraction field, the usual formal logarithm is obtained by integrating the reciprocal invariant differential; it obeys `log_F(F(X,Y))=log_F(X)+log_F(Y)`. Its linear coefficient is `1`, so formal inversion shows `F(X,Y)=F(Y,X)`. This is a coefficient identity over the fraction field, hence also over `O`; no analytic convergence of that logarithm on the torsion set is asserted or needed. In the application, Lubin and Tate's Theorem 1 explicitly proves the symmetry identity.

For `n>2`, two different cycle edges either are disjoint or share exactly one vertex. The disjoint-edge factors handle the former, while cancellation handles the latter. At `n=3` there are no disjoint edge factors, and cancellation alone handles all three pairwise comparisons. The excluded `n=2` would be false for a commutative law, because the two oriented neighbor sums coincide.

## 4. Arbitrary finite abelian p-groups: explicit realization

Let `G ≅ ⊕_(j=1)^h Z/p^(e_j)Z`, with `e_j≤k`. Map its `j`th cyclic factor into `Z/p^kZ` by `a ↦ p^(k−e_j)a`. This is injective, so `G` embeds into `(Z/p^kZ)^h`. For the trivial group one can take `h=k=1`; any `n>2` subset claim is then vacuous.

For every positive integer `h`, the unramified extension `K/Q_p` of degree `h` exists. Its ring of integers `O_K` is a free `Z_p`-module of rank `h`, and `p` is a uniformizer. Taking a `Z_p`-basis gives an additive-group isomorphism

`O_K/p^kO_K ≅ (Z/p^kZ)^h`.

This uses a different local field when the required rank changes; it does not claim that one fixed height-one formal group over `Q_p` contains all ranks.

Put `q=p^h` and choose the permitted Lubin–Tate polynomial `f(T)=pT+T^q`. The cached original, p. 380, defines precisely this allowed class. Its Theorem 1, p. 382, constructs a commutative formal group `F_f ∈ O_K[[X,Y]]`, makes `O_K` act by endomorphisms, and identifies `[p]_f=f`. Its Theorem 2(b), pp. 383–384, states that the kernel of `[p^k]_f` on the positive-valuation elements of the separable algebraic closure is an `O_K`-module isomorphic to `O_K/p^kO_K`. These are exactly the hypotheses and conclusion imported by the target.

There is also a direct finiteness and location check. The iterate `f^∘k(T)` is monic of degree `q^k`, has coefficients in `O_K`, and satisfies

`f^∘k(T) ≡ T^(q^k) mod p`.

Every algebraic root is integral, because the polynomial is monic and integral. Reduction in the residue field of an extension then forces the root to have zero residue, so every root has strictly positive valuation. All its roots lie in its finite splitting field `L/K`; a finite extension of a complete discretely valued field is again complete and discretely valued. The integral formal law over `O_K` remains integral over `O_L`.

For completeness, separability also presents no issue in characteristic zero. On positive-valuation elements,

`f'(T)=p+qT^(q−1)`

cannot vanish: `v(qT^(q−1))>v(p)`, since `q=p^h`, `h≥1`, and `v(T)>0`. Along any root of an iterate, all intermediate values have positive valuation, so the chain-rule derivative is nonzero. The entire `p^k` torsion set therefore consists of `q^k` distinct roots, consistently with the source module isomorphism.

Composing the two abstract group embeddings with the source module isomorphism places `G` inside `(m_L,F_f)`. An `n`-element subset remains `n` distinct field coordinates. The analytic lemma applies, and injectivity pulls distinct formal sums back to distinct sums in `G`.

## 5. Failed counterexample attacks and exact boundaries

- **High-order terms folding down in the monic remainder.** This does occur over `O`, but every downward fold uses a lower coefficient of `g`, hence a factor in `m`. Modulo `m` such folds vanish. The operator estimate handles infinitely many folds uniformly.
- **Very close points and nonunit Vandermonde denominators.** The integral remainder is proved nonzero first. Only then is interpolation done over the fraction field, so this causes no gap.
- **Nonconvergence at torsion points or infinite extension coefficients.** The torsion level is finite and lies in one finite splitting field; integral power series converge on its maximal ideal. No completion of an infinite algebraic extension is used in this application.
- **One-dimensional formal group cannot contain high-rank torsion.** False as an objection here: the unramified base degree is `h`, and the resulting Lubin–Tate group has `p`-height `h` when viewed over `Z_p`.
- **Formal logarithm would kill torsion.** Its formal existence gives commutativity, but its analytic injectivity is not used and need not hold on the whole maximal ideal.
- **Points of valuation zero.** The maximal-ideal hypothesis matters. For example substituting `T=1` into the integral formal series `Σ_(j≥0) X^j` does not converge. This is an example outside the lemma's hypotheses, not a counterexample to it.
- **Two-torsion.** The conditional theorem does not assert the coefficient condition at all primes. In `(Z/2Z)^2`, the full four-element set has no desired cyclic ordering: the first and third edge sums coincide because the sum of all four vertices is zero. Accordingly, any valid polynomial certificate must fail modulo `2` at `n=4`; this is a useful boundary consistency check, not a contradiction.
- **Mixed-prime torsion.** The construction cannot contain torsion of order prime to the residue characteristic. Multiplication by such an order has an integral inverse formal series because its linear coefficient is a unit. The target explicitly records this limitation.

## Exact remaining gap

No analytic or Lubin–Tate gap remains in the conditional theorem reviewed here. To promote its stated `3≤n≤9` consequence, another audit must validate the coefficient certificates. To reach the unrestricted Kourovka target, the coefficient statement for all `n` and the mixed-prime reduction remain separate unsupported claims. This audit supplies neither.
