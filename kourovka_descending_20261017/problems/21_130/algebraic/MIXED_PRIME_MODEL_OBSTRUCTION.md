# A mixed-prime obstruction to a single-primary Freiman model

2026-10-24. This is a counterexample to a proposed *reduction*, not to Kourovka 21.130.

Let `G=C_3×C_5`, with `a=(1,0)` and `b=(0,1)`, and let

`A={0,b,a,a+b,−a,−a+b,2b,3b,4b}`.

All nine listed elements are distinct. There is no injective map from `A` to any abelian `p`-group, for any prime `p`, which preserves every equality between sums of two distinct elements of `A`.

Here is an exact integral annihilator proof. Suppose `f` preserves all those equalities. Translating the target by `−f(0)` still preserves pair-sum equalities, so assume `f(0)=0`. Write `u=f(a)`, `w=f(−a)`, `v=f(b)`, and `v_i=f(ib)` for `i=2,3,4`.

The following are equalities between sums of distinct elements, and distinct pairs:

- `0+(a+b)=a+b`, interpreted as the two pairs `{0,a+b}` and `{a,b}`, gives `f(a+b)=u+v`.
- `0+(−a+b)=−a+b`, using pairs `{0,−a+b}` and `{−a,b}`, gives `f(−a+b)=w+v`.
- `0+b=a+(−a+b)` gives `u+w=0`.
- `a+(a+b)=(−a)+b` gives `2u=w`.

Therefore `3u=0` integrally in the target group.

The five-element subgroup on `b` supplies four further distinct-pair equalities:

- `0+3b=b+2b` gives `v_3=v+v_2`.
- `0+4b=b+3b` gives `v_4=v+v_3=2v+v_2`.
- `0+b=2b+4b` gives `v+2v_2=0`.
- `0+2b=3b+4b` gives `3v+v_2=0`.

Combining the last two equations gives `5v=0` integrally. In a `p`-group, if `p=3` then `v=0`; if `p=5` then `u=0`; otherwise both vanish. Hence at least one of the distinct pairs `(0,a)` and `(0,b)` collapses. This excludes targets of arbitrary exponent, rather than only elementary abelian targets.

The example itself has a valid rainbow Hamiltonian cycle. In the displayed element order, index it from zero as

`[0,b,a,a+b,−a,−a+b,2b,3b,4b]`.

A valid cyclic index order is `(0,1,2,3,5,8,4,6,7)`. Its sums in `C_3×C_5` are respectively

`(0,1),(1,1),(2,1),(0,2),(2,0),(2,4),(2,2),(0,0),(0,3)`.

They are all distinct. Thus this construction explains exactly why the verified primary-group theorem cannot be promoted to mixed-prime groups merely by requesting a single-primary injective sum-preserving model.

## Sharper seven-point obstruction (independently supplied by root)

The root family subsequently found a smaller example, `A'={0,1,2,3,4,7,9}⊂C_15`. This is retained separately from the independently derived nine-point example above.

Let `f` preserve distinct-element pair-sum equalities and normalize `f(0)=0`. Put `u=f(1)`. The relations

`0+3=1+2`, `0+4=1+3`, `1+4=2+3`

force `f(2)=2u`, `f(3)=3u`, `f(4)=4u`. Then

`0+7=3+4`, `0+9=2+7`, `7+9=0+1 mod15`

force `f(7)=7u`, `f(9)=9u`, and `15u=0`. Each equality uses four distinct vertices. In a `3`-group target, `3u=0`, so `f(3)=f(0)`; in a `5`-group target, `5u=0`, so `f(9)=f(4)`; in every other primary target, `u=0`. Thus no such map is injective into any abelian `p`-group, with arbitrary exponent.

This seven-point set also satisfies the conjecture: `(0,1,2,3,7,4,9)` is a cyclic order with distinct sums `(1,3,5,10,11,13,9) mod15`. It remains an obstruction only to the proposed reduction.
