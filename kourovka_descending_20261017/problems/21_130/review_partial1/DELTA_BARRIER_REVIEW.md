# Independent review of the seven-point mixed-prime barrier

Completed 2026-10-24, 19:53 UTC. **Assigned delta-audit completion: 100%.** No publication, originality, or full-problem conclusion is asserted.

**Verdict: accepted without a substantive mathematical correction.** The example obstructs an injective collision-preserving model in any one abelian p-group. It does not obstruct a rainbow cyclic ordering of the original set.

Frozen reviewed sources:

- `relation_cover/MIXED_PRIME_BARRIER.md`: SHA-256 `97dab16cf6ce37d933618f45680006de627e2941df845fdff278b10bee071e77`.
- `relation_cover/mixed_prime_barrier_check.json`: SHA-256 `6211ec931f7d6af70e79805d0ecdc6c632e2dbd4b52685e9b375f2d9b78f9b00`.

The source bytes are saved under this audit's `snapshot/relation_cover/`. The independent program and exact outputs are `mixed_prime_barrier_audit.py` and `mixed_prime_barrier_audit_results.json`.

## Equations and normalization

All seven elements of A={0,1,2,3,4,7,9} are distinct in C15. Each of the six displayed sum equalities is true modulo 15 and uses four distinct vertices. In particular, the last equality is 7+9=16=1=0+1 modulo 15.

For complete precision, normalize by setting `g(a)=f(a)-f(0)`. This preserves injectivity and every relevant equality because both sides lose `2f(0)`. Then g(0)=0 and t=g(1).

In the source order define relation expressions

`r1=g(3)-g(1)-g(2)`,
`r2=g(4)-g(1)-g(3)`,
`r3=g(1)+g(4)-g(2)-g(3)`,
`r4=g(7)-g(3)-g(4)`,
`r5=g(9)-g(2)-g(7)`,
`r6=g(7)+g(9)-g(1)`.

They all vanish. The integral consequences include

`g(2)-2t = r2-r3`,
`g(3)-3t = r1+r2-r3`,
`g(4)-4t = r1+2r2-r3`,
`g(7)-7t = 2r1+3r2-2r3+r4`,
`g(9)-9t = 2r1+4r2-3r3+r4+r5`,

and the explicit annihilator certificate

`15t = -4r1-7r2+5r3-2r4-r5+r6`.

Thus no division by 2, 3, 5, or any other group integer is hidden in the derivation. It works in an arbitrary abelian target until the p-group property is used. Independently, the six reduced integer relation rows have determinant of absolute value 15. The audit enumerates all eight actual disjoint-edge collision pairs in A and checks that each row already lies in the integer lattice of the six selected rows.

Indeed these equations classify the maps under discussion exactly: they have the form `f(a)=b+a t`, where b is arbitrary and `15t=0`. The displayed equations force this form, and this form preserves every original sum equality because any difference of equal sums in C15 is a multiple of 15.

## The p-group quantifier

For p=3, coprimality of 5 with the p-power order of any element makes multiplication by 5 invertible; `15t=0` therefore gives `3t=0`, and f(3)=f(0).

For p=5, similarly `5t=0`, and `f(9)-f(4)=5t=0`.

For every other prime, an element killed by 15 cannot have nontrivial p-power order, so t=0 and f is constant. This includes p=2 if it is allowed in the target quantifier. The argument holds for finite abelian p-groups and also for arbitrary abelian p-primary torsion groups; finiteness of the target is not needed. No assumption that f is a homomorphism, or that it preserves inequalities or repeated-vertex Freiman relations, is used.

The consequence is precisely the stated one: no single-primary injective model preserving the displayed collisions exists. It leaves reductions using several primary components or other mechanisms untouched.

## Positive cyclic witness

The proposed cycle `(0,1,2,3,7,4,9)` enumerates A once. Including its closing edge, its adjacent sums are

`(1,3,5,10,11,13,9) mod 15`,

which are pairwise distinct. Hence this is a verified method obstruction and a positive instance of the original conjecture. The audit also checked the induced map classification in cyclic targets of orders 8,27,125,343,1331; their maximum image sizes are respectively 1,3,5,1,1, as predicted by the proof.
