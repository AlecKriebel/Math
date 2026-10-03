# Turn 4: finite local covers and a low-complexity family with growing finite rank

This turn extends the positive product result to a class of finite local covering extensions and constructs explicit fully aperiodic repetitive examples whose second rational Betti number is arbitrarily large but finite. Their complexity constants grow with the covering degree. This does not contradict the original finiteness question.

## 1. A finite-stage covering theorem

Suppose Omega is the product of suspensions of d minimal aperiodic one-dimensional subshifts with linear complexity. Model it by finite products K_n of their Rauzy graphs, using independently chosen cofinal word lengths in the factors. Let a D-sheeted covering of one such finite product K_0 be given, and pull it back to every later K_n and then to Omega.

**Claim.** The resulting covering space has finite total rational Čech cohomology. If cofinally the ith graph has cycle rank at most M_i, then its total rank is at most

    D product_i(1+M_i).                                  (1.1)

Each connected graph of cycle rank at most M_i is homotopy equivalent, by collapsing a spanning tree, to a wedge of at most M_i circles. The product therefore has a finite CW model with at most product_i(1+M_i) cells in all degrees. Pulling back a finite covering along a homotopy equivalence gives a homotopy-equivalent covering: lift the homotopy inverse and the two homotopies, using the covering homotopy property. A D-sheeted cover of that finite CW model has D copies of every cell. Thus(1.1) bounds every cofinal covering approximant's total cohomology dimension.

The inverse limit of these pullback covers is the cover pulled back to Omega, since compatible coordinates and their sheet coordinate give exactly the fiber product. Čech continuity and the direct-limit bound of Turn1 now prove the claim. This formulation assumes the finite-level cover explicitly; no unrestricted descent theorem for arbitrary finite-to-one maps is invoked.

## 2. Local permutation decorations fit this framework

For the Cartesian-product symbolic tiling, suppose each positive coordinate edge carries a permutation of D fiber states, determined by a fixed finite radius R of the base configuration. Assume the permutations satisfy the square consistency equations, so transport along two sides of any elementary square is independent of the order. Start from a state at one vertex and transport it over the grid. Flatness makes the result independent of the chosen lattice path.

At a sufficiently large product-pattern approximant, each edge permutation is well defined from its cell label and every square relation holds because that cell label is realized in a genuine base configuration. Lift each vertex to D vertices, each edge using its permutation, and each square to its closed lifted boundary. The higher product cells lift consistently because their square faces do. This constructs an actual finite-sheeted covering, not merely a finite-to-one factor map. The decorated hull is its inverse pullback.

The complexity of the full decorated system satisfies

    D P(n)<=P_lift(n)<=D P(n+2R+c),                       (2.1)

for a fixed collar convention constant c, where P counts n-box base patterns. The upper bound follows because an expanded base pattern and one fiber state determine the decorated pattern. For the lower bound, each base pattern has a realization, and each of the D choices of state at its distinguished vertex gives a different decorated pattern with that base pattern. This assumes the full D-sheet extension, as constructed, rather than an arbitrarily selected subset of its fibers.

Consequently low complexity is preserved and

    liminf P_lift(n)/n^d =D liminf P(n)/n^d.               (2.2)

The equality follows by shifting the integer argument in the liminf; no regular variation is assumed. Combined with the cofinal one-dimensional rank bounds, it yields finite cohomology for these local covers. These constructions do not include arbitrary local factor maps with non-covering singular fibers.

For completeness, if c_i=liminf p_i(n)/n, the Rauzy argument gives M_i=floor(c_i)+1 on cofinal choices. Since c_i>=1, 1+M_i<=3c_i; also product_i c_i<=liminf P(n)/n^d. Thus(1.1) even gives the same numerical bound3^d times the decorated liminf coefficient in(2.2). As before, the coefficient refers to the specified box convention.

## 3. A proper two-letter substitution with a two-loop model

We use a separate explicit building block, so no integral Thue–Morse computation is needed. Let

    tau(a)=aab,  tau(b)=ab.

It is primitive and proper: both images start with a and end with b. Every occurrence of b ends a substituted block, and the preceding run consists of one or two a's. Thus the partition into blocks ab and aab is unique; its preimage is again in the substitution language. This gives recognizability directly. Primitivity proves repetitivity as in Turn2.

The substitution matrix is A=[[2,1],[1,1]]. Its positive eigenvalue is(3+sqrt5)/2, and normalized letter counts in long substituted blocks converge to an irrational a-frequency. The two substituted-block lengths have ratio at most2; choosing a minimal level with the shorter length at least n gives longer length less than6n. Every length-n factor lies in the substitution of an adjacent letter pair at that level. Four possible pairs and at most6n starting positions give p_tau(n)<=24n. Uniform frequency convergence for arbitrary long factors follows by cutting into high-level blocks and making the two boundary fragments negligible. A periodic word would have rational frequency, so the system is aperiodic.

The uncollared graph is a wedge of two oriented circles, labeled a and b, with the substitution map given by the two displayed words. Properness supplies the missing borders: an expanded level-n supertile has common prescribed prefixes and suffixes of length at least the shorter level-(n−1) block. Together with recognizable hierarchy, inverse-limit coordinates therefore determine neighborhoods of growing radius, including at a vertex. The same compactness argument as in Turn3 identifies the inverse limit of this two-loop map with the suspension hull.

On the free group generated by a,b the map is an automorphism. If the new generators are A'=aab and B'=ab, then

    a=A'(B')^(-1),  b=B'(A')^(-1)B'.                      (3.1)

Thus the graph map is a homotopy equivalence. In particular its first rational cohomology has rank2 and its higher cohomology vanishes. No claim that this word has a particular exact Sturmian complexity formula is needed.

## 4. Cyclic local extensions in dimension two

Take the product of two copies of this substitution tiling. For q>=1 attach a state g in Z/qZ to each lattice vertex. Moving horizontally adds1 to g exactly when the horizontal base letter is a; moving vertically adds1 exactly when the vertical base letter is a. These transports commute because the two base sequences are independent, so the square equations hold. The state at one corner and the base pattern determine all states in an n-box, and every state is allowed. Hence

    P_q(n)=q p_tau(n)²=O(n²).                            (4.1)

The finite graph model is the q-sheeted cyclic cover of the product of two two-loop graphs. Its monodromy sends each a-loop to1 and each b-loop to0. It has q vertices,4q edges and4q squares. This cover is connected, since an a-loop reaches every fiber state. Pullback along the substitution product remains connected: the base map induces a fundamental-group automorphism, so it carries the kernel of this surjective monodromy isomorphically to its pullback kernel. The lifted maps are homotopy equivalences. The inverse-limit covering hull is therefore connected and its cohomology is the same as that finite covering complex.

The lifted translation system is minimal. Here is the finite-extension point requiring care. A minimal closed invariant subset exists. Its fiber cardinality over the minimal base is upper semicontinuous and invariant under the base action, hence constant. A closed subset with constant cardinality inside a finite discrete fiber bundle is also open, by excluding the finitely many missing states locally. Thus minimal components are clopen in the transversal, and their suspensions are clopen in the covering hull. Connectedness of that hull rules out more than one component. A period of the extension would project to a period of the fully aperiodic base, so there is no nonzero period. These are genuine source-admissible repetitive aperiodic tilings.

## 5. Exact Betti numbers of the cyclic cover

Complexify the finite cellular cochain complex and Fourier-decompose the q fiber states. The trivial character gives the ordinary product of two two-loop graphs, with Betti numbers(1,4,4). For a nontrivial qth-root character zeta, each graph factor has cochain differential

    C → C²,  v↦((zeta−1)v,0).

Its H^0 is0 and its H^1 has dimension1. The tensor product of these two complexes therefore contributes one dimension in degree2 and none elsewhere. There are q−1 nontrivial characters. Thus, over Q as well as C,

    (beta_0,beta_1,beta_2)=(1,4,q+3).                     (5.1)

The equality of rational and complex ranks follows from extension of scalars for a finite rational chain complex. Pullback homotopy equivalences preserve these ranks in the inverse limit. This family has unbounded finite second Betti number as q varies, accompanied by a complexity coefficient proportional to q. It does not give any single tiling with infinite rational rank.

## 6. Controls and remaining gap

verify_turn4.py checks the free-group inverse words, block-length bounds, all cellular boundary identities and exact rational Betti numbers of the cyclic covering complexes for several q. It also checks covering/transfer chain identities needed to distinguish finite rank from its possible inverse-limit behavior.

The positive theorem still requires a finite local covering over a product model. Arbitrary low-complexity tilings need not have that form. Sending q to infinity is a new limiting operation whose finite-alphabet, expansivity and complexity consequences require separate analysis; it is not a counterexample supplied by(5.1).
