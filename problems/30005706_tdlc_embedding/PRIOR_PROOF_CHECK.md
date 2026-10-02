# Check of the published negative answer

This is an expository verification of Caprace–Cornulier's published construction and obstruction, specialized to the exact TDLC target. It is not a new theorem, construction or author proof-search turn. Classical finite alternating-group simplicity and van Dantzig's compact-open-subgroup theorem are the standard inputs.

## 1. The concrete source group

For k≥0 let E_k be disjoint finite sets of size u_k=k+5. Let X be their countable union. Write X_n=E_0 union ... union E_n and define permutation groups

    K_n = Alt(X_n) × product over k>n of Alt(E_k).

They form an increasing sequence by the natural block inclusions. Let S=union_n K_n and give it the topology in which K_0=product_k Alt(E_k) is compact open with its product topology. The inclusions K_n⊂K_n+1 are open continuous inclusions of compact groups: their only difference is a finite block, and that block inclusion has finite index. Conjugation by an element in K_n is continuous on the open subgroup K_n. Hence this specification gives a Hausdorff group topology on the union.

Each K_n is a product of one finite group and countably many finite groups, so is compact, totally disconnected and second countable. It is open in S. Their countable union shows S is sigma-compact and second countable, and the compact-open neighborhood shows local compactness. S is nontrivial. This is the published S(u)^+ for the countable index set and increasing block sizes.

The subgroup A of even finitary permutations of X is dense in S: any element of K_n can be approximated by retaining its action on finitely many blocks and taking the identity on the remaining tail. A is the classical infinite finitary alternating group.

## 2. Topological simplicity

If N is a nontrivial normal subgroup of S, choose s≠1 in N. Enlarge n so that s belongs to K_n and moves a point of X_n. The restriction s|X_n is a nonidentity even permutation. Since |X_n|≥5, the center of Alt(X_n) is trivial, so some a in Alt(X_n) has [s,a]≠1. This commutator lies in N∩Alt(X_n). Normality and finite alternating-group simplicity imply Alt(X_n)⊂N. Enlarging n further and repeating the argument, or taking normal closures in larger finite alternating groups, shows A⊂N. Density implies every nontrivial closed normal subgroup is S. Thus S is topologically simple. Abstract simplicity is neither true nor used.

## 3. Large prime torsion in every identity neighborhood

Every identity neighborhood contains all factors beyond some finite initial block of K_0. Given any sufficiently large odd prime p, select k in this tail with u_k≥p. A p-cycle in Alt(E_k) is even because p is odd, and generates a nontrivial subgroup C_p inside the neighborhood. Consequently arbitrarily large primes occur locally.

Let S act continuously on a connected graph of maximum degree d. A vertex stabilizer is open, so it contains a C_p as above for some prime p>max(d,2). This C_p fixes that vertex. An action of C_p on at most d neighbors has only singleton orbits, because every nontrivial orbit has size p. It fixes every neighbor, then every vertex by induction along finite paths. Hence C_p lies in the kernel of the graph action. This kernel is a nontrivial closed normal subgroup, so the entire S-action is trivial.

## 4. No homomorphism into a compactly generated TDLC group

Suppose f:S→G is a nontrivial continuous homomorphism and G is compactly generated TDLC. Choose s with f(s)≠1. By van Dantzig, choose a compact open subgroup U of G that does not contain f(s). Let C be a symmetric compact generating set together with U. Construct the standard coset graph on G/U, joining gU to hU when g^-1 h lies in UCU. It is connected because C generates, vertex-transitive under G, and locally finite: compactness gives finitely many double cosets UcU in UCU, and each UcU/U is finite since U∩cUc^-1 is open in the compact group U. Loops can be deleted; they are irrelevant to connectivity. Transitivity makes the finite degree a global bound.

Compose f with this continuous G-action. Section3 says the S-action is trivial. Therefore f(S) fixes the base vertex U and lies in U, contradicting f(s) not in U. This proves every continuous homomorphism S→G is trivial, so no continuous injective embedding exists. No assumption of closed image, properness of f, or transfer of compact generation to subgroups has been made.

## 5. Exact conclusion and credit

The explicit S meets even the stronger second-countability hypothesis, so it is a counterexample to the unrestricted sigma-compact question exactly as printed. The construction and nonembedding mechanism are prior results of the cited authors. The full published theorem additionally treats all locally compact targets and abstract homomorphisms; those stronger clauses are not needed for the source match and are not claimed independently reproved here.

A finite checker tests alternating permutation commutators and the large-prime graph-action lemma on small fixtures. It is a supplemental audit, not a numerical proof of the topology or the infinite group statement.
