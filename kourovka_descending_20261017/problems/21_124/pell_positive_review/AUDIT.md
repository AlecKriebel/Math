# Independent audit: positive witness for the Pell candidate

UTC checkpoint: 2026-10-24T22:52:00Z. Reviewer: internal subagent `p21124_flats_adversary`, not an author of the submitted witness or its search. Review completion estimate: **100%**. Full-problem discovery estimate remains **6%**. Input and output hashes are frozen in `RECEIPT.json`. The earlier `flats_review/` package was not altered.

**Verdict: PASS.** The exact integer certificate proves that the one specified four-edge Pell tubular group has(VRC), and hence is virtually special by the cited theorem. This defeats that candidate as a counterexample. It does not answer Kourovka21.124, certify novelty, supply a publication recommendation, or depend on the numerical search's correctness.

## Exact claim checked

The presentation from the frozen candidate file is

`G=<a,b,t,s1,s2,s3 | [a,t]=[b,t]=1, s_i(a^p_i t)s_i^-1=b^q_i t>`,

with the three pairs `(p_i,q_i)=(3,2),(20,14),(119,84)`. It is the fundamental group of the finite tubular graph with vertex groups `<a,t>` and `<b,t>`, both Z²; one tree edge identifies t, and three further cyclic edges have attaching vectors(p_i,1) and(q_i,1). These are nonzero vectors, so every edge map is injective. This presentation supplies precisely the graph-of-groups scope required below. No global injectivity of the constructed homomorphism is needed.

The older candidate note labels its specialness unresolved. That was its historical state; this new verified affirmative witness supersedes that status. Its CAT(0) and F5-by-Z arguments are not needed for the present theorem application and were not re-reviewed here.

## Literal finite object

The integer certificate contains517 triples `(a,b,t)` and517 positive integer multiplicities m. The independent checker reads the integers directly, rather than importing any author code. It verifies strict positivity, the declared count, common gcd1, the stated coordinate bounds, and

`2 sum(m) = N = 95419250146190292634685757020254542`.

For each pair of signs, a triple v contributes m indexed copies of v and m indexed copies of−v. This defines an ordinary **finite** set of coordinate positions Omega of cardinality N. The large cardinal is a positive integer; neither an infinite-dimensional completion nor a limiting construction occurs. Every coordinate vector has finite support because Omega itself is finite.

The compressed permutation file has1034 coordinate blocks. I checked that their consecutive half-open intervals partition exactly[0,N), each has the declared integer length and triple, and their ordered pairs of positive/negative blocks coincide with the support certificate. Thus the permutation file and multiset file refer to the same indexed object, rather than merely to two unrelated balanced multisets.

For every pair(p,q), I formed the **full signed** histograms

`H_L(x)=sum_(j:p A_j+T_j=x)1` and `H_R(x)=sum_(j:q B_j+T_j=x)1`.

All517 pairs and both signs contribute, including zero projected values. These counters agree exactly, with total N. The counts of distinct signed values are111,285,658 respectively. No absolute-value balance is substituted for signed balance, and no floating point arithmetic is used.

## Every permutation, including orientation

Each supplied segment(s,d,l,x) defines the literal map j↦j+d−s from[s,s+l) to[d,d+l). I checked l>0 and separately sorted all source intervals and all destination intervals. In each case the endpoints are consecutive from0 toN, without gaps, overlaps, or out-of-range endpoints. A translation is a bijection on each interval, and the image intervals partition[0,N), so these checks prove an actual permutation of all N positions.

I then swept every source and destination interval against all coordinate blocks, allowing for the possibility that a segment crosses block boundaries. On every overlap the source block has projected value `p a+t=x` and the destination block has value `q b+t=x`. There are1955,1777,1400 segments; in this data each lies in one block on each side. The checks cover every integer position by interval reasoning; the huge intervals are not sampled as a replacement for exhaustive coverage. Additionally,15396 endpoint/midpoint and inverse-map checks passed. Per value, sorting the source pieces also orders their destination pieces, confirming the claimed canonical increasing matching, although any correct matching would suffice mathematically.

Put `u=pA+T` and `v=qB+T`. The certificate establishes `u_j=v_(P(j))` at every position. For the convention **P e_j=e_(P(j))**, one has `(Pu)_(P(j))=u_j`. Since P is onto, the checked identity is exactly `Pu=v`. Using the inverse permutation instead without changing the convention would be an unjustified reversal. The supplied orientation is correct.

As an independent consistency check, the exact Gram matrix of A,B,T satisfies the three resulting squared-norm identities. In fact `||B||²=2||A||²`, `2<A,T>=||A||²`, and `<B,T>=||A||²`, with positive `||A||²`; all calculations are integral. These moment checks supplement the full signed identities and do not replace them.

The permutations are not forced into commuting holonomy. Direct evaluation gives

`P1 P2(0)=12283930943422629964559322200280710`,

`P2 P1(0)=11163582194361178508258746276426716`.

The different values prove noncommutation. Earlier obstructions to commuting holonomy therefore present no contradiction. No group order or irreducible decomposition is assumed.

## Homomorphism, injection, and discreteness

Let Q be the subgroup of the finite symmetric group Sym(Omega) generated by the three checked permutations. It is finite because Omega is finite. Its permutation action on R^Omega is orthogonal and integral; extend it trivially over one additional real coordinate. Thus `R^(N+1) semidirect Q` is a Euclidean-by-finite group.

Send a,b,t to the translations `(A,0),(B,0),(T,1)`, and send s_i to the zero-offset isometry with linear part P_i. The vertex commutators vanish because translations commute. For a pure translation by u, conjugation by(0,P_i) translates by P_i u. The checked vector identity therefore gives

`rho(s_i) rho(a^p_i t) rho(s_i)^-1 = translation(P_i(p_i A+T),1) = translation(q_i B+T,1)`.

This is exactly the defining relation, for all three stable letters. The common tree-edge generator t has one image, so that relation is also respected. There are no additional presentation relators to check.

A and B are both nonzero by direct support inspection. If the image of `a^r t^s` is trivial, the extra coordinate gives s=0, and then rA=0 gives r=0. The same argument with B proves injectivity on `<b,t>`. It deals with the entire integer lattice, not just the two generators individually. The image lies in `Z^(N+1) semidirect Q`, a discrete subgroup of the Euclidean-by-finite target: integer translation coordinates form a lattice, and Q is finite. Both vertex images are consequently discrete. The added coordinate avoids any issue of real dependence between A and T or between B and T.

## External theorem application

Primary source checked live2026-10-24: Merladet Urigüen–Minasyan, *Virtual retractions in free constructions*, [arXiv2505.18054v3](https://arxiv.org/html/2505.18054v3), dated2025-10-29, with the appendix jointly authored by Wu and Ye. [Theorem1.6(ii)](https://arxiv.org/html/2505.18054v3) applies to finite graphs of finitely generated virtually abelian vertex groups and equates(VRC) with a homomorphism to a Euclidean-by-finite group having injective discrete vertex images. No bound on the finite Euclidean dimension is imposed. [Proposition1.10](https://arxiv.org/html/2505.18054v3) says that a tubular group with(VRC) is virtually special, equivalently virtually embeds in a finitely generated RAAG. All hypotheses have been checked above. These are established external dependencies, not new lemmas of the witness.

## Adversarial disposition and reproducibility

`independent_check.py` uses only the standard library. It imports neither the author's verifier nor SciPy, NumPy, flint, or an exact linear solver. The claimed rank517, absence of free columns, LP feasibility, and solver uniqueness are unnecessary for this proof and are not accepted merely from metadata. Even an erroneous search or solver would not invalidate positive integers that pass every direct finite-object check here. Their audit is sufficient for existence.

No arithmetic, sign, permutation-direction, finite-dimensionality, vertex-injection, or theorem-scope error was found. No outside communication occurred. The author files were unchanged; hashes match the supplied manifest. The reviewer checker and result are frozen separately. For reproduction, run the checker in a byte-copy of the directory tree so the timestamped `RESULTS.json` in this frozen review remains intact.

The verified outcome is an affirmative result for **this candidate only**. The universal Kourovka problem remains open in this research effort. No originality audit has been completed for this candidate conclusion, and no publication status should be promoted from it alone.
