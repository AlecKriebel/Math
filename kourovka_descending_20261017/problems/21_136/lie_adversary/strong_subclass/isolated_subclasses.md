# A local isolated infinite-order conjugacy class: abelian-kernel obstruction

Checkpoint: 2026-10-24T17:40:57Z. Status: self-contained deduction; a simpler proof supplied independently by the parent was adversarially checked in both directions without finding a gap. Completion estimate for the assigned subclass question: 100%; the unrestricted profinite question remains open here.

## Exact condition

For a profinite group G and an infinite-order element x, consider the condition

    (L) There is an open neighborhood U of x such that every
        infinite-order element y in U is G-conjugate to x.

Using a clopen neighborhood makes no difference: every open neighborhood in a profinite group contains a clopen neighborhood. We make no assumption about the number of infinite-order conjugacy classes outside U. No assertion about novelty is made pending literature comparison.

**Main result.** No virtually solvable profinite group admits (L). In particular, (L) is impossible in virtually metabelian groups and in virtually nilpotent groups of finite nilpotency class.

The main checkable mechanism is more general than those subclasses: an abelian normal subgroup already rules out (L) if it contains a positive power of x.

## Preliminary facts

1. If x has infinite order, each positive power x^n has infinite order. Moreover, for every open neighborhood U of x there is an integer n>1 with x^n in U. Indeed, choose an open normal subgroup W with xW contained in U; if k is the order of xW in the finite quotient G/W, take n=1+k.

2. Condition (L) descends through any continuous quotient pi:G->K for which pi(x) still has infinite order. The set pi(U) is an open neighborhood of pi(x). If z in pi(U) has infinite order, choose a lift y in U; then y has infinite order, so y is conjugate to x and z is conjugate to pi(x). If U is clopen, its image is compact and open and hence clopen as well.

3. If x satisfies (L) and b=pi(x) has finite order in a quotient K, every element of pi(U) has finite order. Otherwise an infinite-order z in pi(U) would lift to an infinite-order y in U, making z conjugate to the finite-order element b.

## Abelian-kernel lemma

**Lemma.** Let A be a closed normal abelian subgroup of a profinite group G. An infinite-order element x whose image xA in G/A has finite order cannot satisfy (L).

**Proof.** Suppose (L) holds, and write B=G/A and pi:G->B. Let b=pi(x) have finite order r>=1. By preliminary fact 3, pi(U) consists entirely of torsion. Choose an open subgroup V of B with bV contained in pi(U), and put

    C=C_B(b),
    K=C intersect V.

The subgroup K is open in C; it need not be open in B. For k in K, the commuting elements b and bk both have finite order, so k=b^(-1)(bk) has finite order. Thus K is torsion. Since K has finite index in C, every element of C has a positive power in K and consequently has finite order. Hence C is a torsion group.

Choose an integer n>1 satisfying both

    x^n in U,
    n=1 modulo r.

Such a choice exists: in preliminary fact 1 choose n-1 divisible by both r and the order of x in the relevant finite quotient. Condition (L) supplies g in G with x^g=x^n. Since b^n=b, the image pi(g) lies in C and therefore has finite order m. Thus g^m lies in A.

Now a=x^r is an infinite-order element of A. From x^g=x^n we get a^g=a^n and a^(g^m)=a^(n^m). But g^m lies in the abelian group A, so it centralizes a. Consequently

    a=a^(n^m),
    a^(n^m-1)=1,

contradicting the infinite order of a. [End proof.]

This shorter proof was supplied independently by the parent research agent and checked here. It does not require the quotient B or the centralizer C to be abelian, nor does it require a uniform bound on torsion orders in C.

### Independently derived alternative proof

The following norm-product argument was found independently before the preceding simplification. It is retained as a checkable second mechanism for the same lemma.

Suppose (L) holds, and write K=G/A and pi:G->K. Let b=pi(x) have finite order r>=1, and put

    a=x^r in A.

The element a has infinite order. Since A is abelian, conjugation on A factors through K. We use right conjugation notation a^g=g^(-1)ag, and use the same notation for the well-defined action of K on A. In particular,

    a^b=a.

By preliminary fact 3, every element of pi(U) is torsion. Choose an open normal subgroup V of K such that

    bV is contained in pi(U).

By preliminary fact 1, there is an integer n>1 with x^n in U. Condition (L) gives g in G satisfying

    x^g=x^n,
    a^g=a^n.

Because K/V is finite, some positive integer s satisfies

    v=pi(g^s) in V.

Iteration of conjugation gives

    a^v=a^(n^s).

For every integer i, the fact that b fixes a implies

    a^(v^(b^i))=a^(n^s).

Now bv belongs to pi(U), so bv has finite order. Hence

    t=(bv)^r

has finite order, say d. Since b^r=1 in K, the group power formula writes

    t=v^(b^(r-1)) ... v^b v.

Each of these r factors acts on a by raising it to n^s. Therefore

    a^t=a^(n^(sr)),
    a=a^(t^d)=a^(n^(srd)).

Thus a^(n^(srd)-1)=1. The exponent n^(srd)-1 is a positive integer, contradicting the infinite order of a.

Important scope point: neither K nor its action on A is assumed abelian or of bounded exponent. The element t has finite order because bv lies in the specific torsion neighborhood pi(U). No general prohibition on power-fusion relations is used.

## Closure under extensions by abelian kernels

Let C be any class of profinite groups in which (L) is impossible. If A is closed normal abelian in G and G/A belongs to C, then (L) is impossible in G. Indeed, for a hypothetical x there are only two cases:

- If xA has infinite order, preliminary fact 2 produces (L) in G/A.
- If xA has finite order, the abelian-kernel lemma gives a contradiction directly.

Finite profinite groups trivially do not admit (L), since they have no infinite-order elements. Consequently the obstruction applies to every profinite group with a finite normal series whose factors are either finite or abelian.

## Virtually solvable groups

Here is a direct induction avoiding any ambiguity about that series description. Let G have an open solvable subgroup; replacing it by its core gives an open normal solvable subgroup M. Use the closed derived series and induct on its finite derived length d.

For d=0, M=1 and G is finite. For d>=1, put

    A=M^(d-1).

This is a closed normal abelian subgroup of G, and G/A has the open normal solvable subgroup M/A of derived length at most d-1. The induction hypothesis rules out (L) in G/A. Closure under abelian kernels now rules out (L) in G.

This proves the main result, including the requested virtually metabelian and finite-class nilpotent subclasses.

## Exact gap

The proof does not settle arbitrary profinite or arbitrary pro-p groups. It uses an abelian normal subgroup in which a positive power of x lands, or finitely many quotient reductions guaranteeing that such a subgroup is eventually reached. Infinite derived-length prosolvable groups and groups without suitable nontrivial abelian normal subgroups are not covered. No actual counterexample to (L) is constructed here.

No other construction-agent notes or isolated-local-audit notes were consulted. No Git operations, publication, or external communication were performed.
