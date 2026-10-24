# Fresh adversarial audit of the finite-action constructions

Checkpoint: **2026-10-24 16:59 UTC**. Independent audit completion: **100%**. Estimated progress toward a complete solution of Kourovka 21.139 remains **15%**; this audit supplies no new general case of that problem. The reviewer did not author either construction and imported none of their code or saved computational results.

**Disposition: PASS within the stated partial scope.** No substantive mathematical objection remains to the claims in `root_hnn_slot_flow.md` and `approach_hnn_20261024.md`. This is neither an originality certification nor a solution of 21.139. The precise missing universal assertion is recorded below.

## Cellular conventions

For a right covering action, a positive letter contributes the edge at its current sheet and then moves forward; a negative letter first moves backward and contributes minus the edge at the new sheet. I rebuilt all computational matrices from this rule. Consequently the tests use the actual boundary from faces to edges, rather than the kernel of an incorrectly transposed matrix.

The generalized-family author instead defines a left permutation representation rho and uses inverse generator permutations for the actual right action. Under that convention the actual boundary is the transpose of the evaluated left Fox derivative. For r_i=t^-1 a_i t w_i^-1, when rho kills both associated groups, its a_j block is

    delta_ij T - rho(partial w_i / partial a_j)^transpose,

and its stable-letter block is zero. Thus changing T on a common zero coordinate of all face vectors really does leave every relevant boundary vector unchanged. There is no omitted stable-letter term.

## Universal slot-flow theorem

The direct walk gives the advertised blocks

    T^-1 + P^-1 - N,  -N,  0,

with N=sum(P^j), j=0,...,q-1. With T=RP, their common kernel is exactly ker(N) intersect ker(R+I). Antisymmetry under R assigns a single oriented coefficient to each edge of the bipartite multigraph; ker(N) is precisely zero incidence boundary at each vertex. Thus the kernel is the ordinary graph cycle space. Connectivity is proved by the color-0 and color-1 edges, even when n=1 and these are parallel edges. Its dimension is nq-2n+1, proving the claimed formula for all parameters, independently of the finite tests.

The q=2 control is handled correctly: the dimension is one for every n. The particular group G_2 is the closed nonorientable genus-three surface group. No unboundedness is inferred in that boundary case. All height covers have the invertible b-block -qI, so their vanishing second homology is also exact. These covers are not a residual chain, and their normalized positive growth therefore gives no contradiction to residual L2 approximation.

## Sparse amplification and generalized family

The sparse amplification lemma is valid for arbitrary associated-subgroup rank. The base action connects each copy internally. Replacing T(omega,j) by (T_0(omega),j+1) is bijective because the list of removed targets is exactly the list of inserted targets. Only source columns at omega change. Since each copied face tuple vanishes in that coordinate, all n copied homology classes survive and remain independent. The new stable-letter edges connect the n copies. The aspherical HNN graph of spaces makes these actual group homology classes.

For q=kp+epsilon, the generalized-family a-block and b-block are correct, including epsilon=-1: in the latter case the final inverse b cancels the last positive b-edge before evaluation, leaving exactly q positive b-edges. The telescoping identity is

    sum(P^(-jk))(e_0-e_(-k)) = e_0-e_(-pk).

Since gcd(k,q)=gcd(p,q)=1 and -pk=epsilon modulo q, both source and target differences are nonzero. Multiplication by p is one valid choice of T. For q>=3 a common zero source exists, enabling the amplification lemma. At q=2 the construction makes no unbounded claim.

## Abelian and prime-group detection limits

The abelian-cover criterion is correct in both directions. After decomposing a finite abelian covering module into finite-order complex characters, the stable-letter derivative forces A=1 and the relation then forces B^q=1. At B=1, the b-derivative is -q. Otherwise the remaining sum S=(1-B^(-epsilon))/(1-B^k) has unit modulus exactly when B^k=B^(epsilon) or B^k=B^(-epsilon). The two resulting values of S, namely -B^(-epsilon) or 1, are themselves roots of unity. Thus the existence of a relevant finite character is equivalent to one of gcd(q,k-1), gcd(q,k+1) exceeding one. This also checks the p=1 and k=1 boundaries; the convention gcd(q,0)=q causes no exception. A finite character occurs in the regular representation of its finite cyclic image, so the reverse implication really constructs a finite cover with positive homology.

The prime-group monodromy argument is valid. In F_l[P] for a finite l-group P, the augmentation ideal I is nilpotent. Indeed choose a central element z of order l, apply induction in the quotient by z, obtain I^m contained in (z-1), and then I^(ml)=0 because (z-1)^l=0. Every element with nonzero augmentation is therefore a unit. A nonzero exponent sum modulo l makes one evaluated Fox block invertible on every covering permutation module. Transposition does not affect invertibility. This proves injectivity of the actual second boundary over F_l; a nonzero full-rank integral minor also proves injectivity over Q. For a primitive exponent vector, a suitable coordinate exists separately for each prime.

The phrase **finite l-group monodromy** is essential. An index l or l-power subgroup need not have l-group monodromy. Nor does this argument extend to all finite solvable or all mixed-prime nilpotent monodromy. These qualifications are retained in the author notes.

## Exact E family and the solvable witness

For E=<a,b,t | t^-1 a t=a b^2 a b^3>, the claimed degree-5n actions are transitive. In the first boundary block T-I-P^-2, the coordinates 0 and 1 force z_2=z_3=0; the coordinate 3 then forces z_0=0 even across the cyclic block link, and coordinate 4 gives z_4=-z_1. These vectors also satisfy the b-block. Thus the kernel has exactly n basis vectors e_(1,j)-e_(4,j), and b_1=5n+1+n=6n+1 follows from Euler characteristic.

For the alternative degree-five affine witness, the permutations i->i+1 and i->2i generate precisely all twenty maps i->u i+v over F_5, u!=0. The translation subgroup is normal cyclic of order five and the quotient is cyclic of order four, proving solvability. Independent relator walks give b_2=1. This witness is fully compatible with the abelian and l-group blindness statements.

## Asphericity and category gates

The associated cyclic edge maps are injective, so the standard finite graph of aspherical spaces is aspherical. Its finite covers consequently compute group homology, with no unmentioned three-cell quotient.

A separate narrow reviewer checked the cached primary sources. [Kapovich, Proposition 4.11](https://arxiv.org/abs/math/9704203) requires a hyperbolic base, quasiconvex isomorphic associated groups, malnormality, and absence of nontrivial cross-conjugacy. Primitivity supplies maximal cyclic, hence quasiconvex and malnormal, associated groups in the free base. Conjugacy of nonzero powers would give (m,0)=n(p,q) in abelianization, impossible because q>=2. Hyperbolicity follows. The height kernel is an increasing union of finite-interval free groups with free-factor inclusions, hence is free; the height map splits. [Linton v2, Corollary 1.5](https://arxiv.org/html/2510.10178v2#S1.Thmtheorem5) really is the virtual compact specialness corollary and allows the infinitely generated free-kernel setting through the paper's stated convention. The category claims therefore pass their gates.

## Independent reproduction

`verify_finite_actions_fresh.py` uses only Python's standard library and Fraction elimination. It imports neither the construction scripts nor their results. Run from the project root:

    python3 kourovka_descending_20261017/problems/21_139/reviews/verify_finite_actions_fresh.py

The saved `finite_action_fresh_checks_20261024.json` records **67** successful cases:

- 24 slot-flow cases: q=2,...,7 and n=1,...,4; direct boundary columns also equal the displayed slot-flow block formula.
- 26 generalized telescoping cases with epsilon=+1 and -1, including p=1 and q=2 boundaries; every claimed copied vector is checked in the actual boundary kernel.
- Eight exact E covers, degrees 5 through 40, all with b_2=n.
- One affine degree-five witness with b_2=1 and independently enumerated monodromy of order 20.
- Eight height-cover checks for the higher-rank F(a,b,c), A=<a,b>, B=<bc,ca> control, using both actual relators. They give b_2=1 in even degree and zero in odd degree.

Script SHA256: `0adde9f04147f5de43154348be68a5a5e7d12bdc2762611acf22053e7943665a`.

Results SHA256: `d10ef3c3b5f63507d5f5d47c997480b5990d5e284d2b3471d471f689a1ce33b4`.

The finite computations corroborate the proofs; they are not substitutes for the universal graph-flow, sparse-amplification, or character arguments. The result file contains its own precise run timestamp, so rerunning changes its hash without changing the mathematical assertions.

## Exact remaining obstruction

None of these arguments proves that every nonfree hyperbolic compact special free-factor HNN extension admits a positive finite-cover H_2 witness. The sparse lemma assumes a transitive finite base action killing both associated groups and a common zero in a nonzero kernel tuple. Those are genuine additional hypotheses, not consequences established here.

The higher-rank control makes the limitation concrete: killing A=<a,b> and B=<bc,ca> kills the whole free base, so the lemma has no nontrivial base-transitive action, while an even height cover nevertheless detects H_2. No deduction from unbounded homology in an overgroup to a subgroup is supplied or used. Replacing the missing certificate-existence theorem by another unsupported subgroup-existence theorem would merely transfer the central difficulty.

These examples belong to the cyclic-edge class already addressed qualitatively in the literature. This audit therefore supports preserving the explicit constructions as checked partial research, retaining status **unsolved** for 21.139, and withholding any new publication or first-priority claim.
