# Independent reconstruction before candidate or earlier verdict comparison

The task supplied issue names and mathematical hypotheses to challenge. This is consequently a source-first independent reconstruction, not a claim of blind review. No candidate turn proof, final verdict, family report, or root mathematical reconstruction was read before this document and the new controls were sealed.

## Source-defined claim and boundaries

Adiceam, arXiv:1604.06280v2, p.8, Problem 2.5.1 asks whether low radius-patch complexity `p(n)=O(n^d)` implies finite rational cohomology rank for an aperiodic repetitive d-dimensional tiling. Use the translational hull with the local matching topology and Čech cohomology. Julien 2017, pp.545-546, defines aperiodic as absence of *every* nonzero translational period, FLC as finitely many patches up to translation at each radius, and repetitive as bounded-distance occurrence of every finite patch. These distinctions exclude stripe constructions with a hidden period. Rational rank and finite generation over Z differ: the original source explicitly gives the Thue-Morse integral counterexample.

Success for the general problem requires a proof for every hull in these hypotheses, or a fully admissible counterexample with infinite rational rank. Finite computations, bounded approximant counts for an extra subclass, and nonexpansive Cantor actions cannot alone meet that criterion. No novelty certification follows from this audit.

Julien arXiv:0804.0145v1 uses Theorem 5.10, Proposition 5.13, Lemma 5.14, and Proposition 5.16, pp.23-27. These numbering labels differ from the later 2010 article labels cited by the problem source. Alternating left/right truncation of Rauzy graphs recovers both halves of the word, with the *unit suspension* as the inverse limit. Rational Čech continuity then identifies its cohomology with the direct limit. Connectedness gives `dim H1(R_n)=p(n+1)-p(n)+1`.

Koivusalo-Walton's published introduction, Example 4.3, Theorem 8.1 and Example 8.2 distinguish almost canonical from quasicanonical windows. A canonical projected fundamental cell is quasicanonical. Almost canonical alone does not justify identifying the cut-hyperplane topology with the actual transversal. A blanket extension of the source canonical statement to arbitrary almost canonical windows would be unsupported.

## 1. Cofinal rank and the sharp product coefficient

For a direct system of finite-dimensional Q-vector spaces, a cofinal subsequence with dimension at most M bounds the limit dimension by M: represent any M+1 alleged independent classes at one common stage, then map to a later bounded stage. No injectivity or stabilization of the individual stage dimensions is required.

Let `L=liminf p(n)/n<infinity`. If the integer increments `s(n)=p(n+1)-p(n)` were eventually strictly greater than L, their integer minimum would be some integer greater than L; telescoping would force a larger liminf. Therefore arbitrarily late increments satisfy `s(n)<=L` (or use the epsilon version and integrality). Consequently `r=dim H1 <= L+1`. Recurrence gives connected graphs; H0 is Q. Fully aperiodic words have `p(n)>=n+1`, so L>=1.

For a product of d such one-dimensional systems, rectangular n-block counts multiply exactly. If `P(n)=product p_i(n)<=C n^d` eventually, each factor is O(n) using the other factors' lower bounds. Write `L_i=liminf p_i(n)/n`. Positivity gives `product L_i <= liminf P(n)/n^d <= C`. The suspension is the product of the one-dimensional suspensions. Čech Künneth over Q follows at the finite graph product stages and commutes with the cofinal diagonal and direct limits. Its total rational rank is `product (1+r_i) <= product (L_i+2) <= 3^d product L_i <= 3^d C`.

This coefficient is sharp for this precise rectangular asymptotic normalization: a product of d Sturmian suspensions has complexity `(n+1)^d`, asymptotic coefficient 1, and total rank `3^d` (H1 rank 2 per factor). Replacing the window by an arbitrary ball or changing tile sizes rescales complexity and the coefficient; it does not preserve this literal normalization. This argument is a subclass result, not a solution for arbitrary low-complexity multidimensional tilings.

## 2. A source-admissible failure of raw Euler control

Let x be Thue-Morse and y Sturmian, with coding `z(i,j)=(x_(i+j),y_j)`. This is the integer unimodular shear of their product. Its full Z2 hull is the recoded product; the shear preserves minimality and freeness, and the finite alphabet gives FLC. The unit-cube suspension therefore meets the source assumptions. Its rational Betti numbers are `(1,4,4)` and total rank 9.

For an n by m rectangle, `P(n,m)=t(n+m-1)(m+1)`, where t is Thue-Morse factor complexity. The usual rectangle cell counts are

`V=t(k-1)m, Eh=t(k)m, Ev=t(k)(m+1), F=t(k+1)(m+1), k=n+m-2`.

Thus `chi=(m+1)s(k)-m s(k-1)`. Recognizable substitution parity yields `t(2a)=t(a)+t(a+1)` and `t(2a+1)=2t(a+1)` for a>=2. The base increments and recurrence give `s(2^q)=2`, `s(2^q+1)=4`. Set `n=2^(q-1)+1`, `m=n+1`. Then `k=2^q+1` and `chi=2n+6`, unbounded along a cofinal rectangle family. Since `beta2=chi+beta1-1`, the raw H2 ranks are also unbounded. Their eventual images still have rank at most 4. This falsifies the inference from low complexity to bounded raw rectangular Euler/Betti data, not the open problem.

The initial new control incorrectly selected exact squares; the positive Thue-Morse increment jumps in this convention occur at odd k. That failed assertion is preserved. Nearly square rectangles provide the required cofinal witness. This shape dependence is one reason literal raw formulas must be checked rather than inferred from an O(n^2) growth label.

## 3. The exact persistence quantifiers and actual Thue-Morse hierarchy

For finite-dimensional stages `V_i`, the following are equivalent:

`dim colim V_i <= D` and `for every i there exists j>=i with rank(V_i -> V_j)<=D`.

The forward implication uses finite dimensionality: the kernel of `V_i -> colim V` has a finite basis, each basis element dies at a finite later stage, and a common maximum kills the whole kernel. The reverse implication sends any D+1 classes to a common stage and then through the promised rank bound. There is no assertion of a uniform delay j-i.

A new exact countermodel has a persistent backbone Q and one transient e_n born at n and killed at 2n+1. At stage i the surviving transient labels are `ceil(i/2),...,i`. The limit has rank 1; mapping stage i to 2i+1 kills all its transients. Every fixed lag misses the death of arbitrarily late e_i. Hence raw dimension can grow and no uniform lag is implied.

For actual Thue-Morse, use the six legal triples as collared edges and four legal pairs as vertices. The central letter of each collared triple is replaced by its two-letter substitution, with its output collars read from the adjacent images. The independently constructed matrices satisfy `B M = V B`. The cycle-space image ranks are exactly `3,2,2,2,2`; the first image is an invariant two-dimensional space on which the induced map is invertible. Thus the actual collared substitution limit has rational H1 rank 2.

The topological applicability is not supplied by matrix rank alone. Equal adjacent letters 00 or 11 can only cross Thue-Morse supertile boundaries. They occur with bounded gaps, fixing the parity of supertile boundaries; the word can then be decoded uniquely into 01/10 pairs. Repeating gives recognizability at every scale. Triple collars record both adjacent supertiles, which forces the border of each substituted central tile. This is a cofinal border hierarchy for the tiling hull. Tensoring with the Sturmian hierarchy gives the sheared witness's stable H2 rank 4. A counterfeit arbitrary matrix system lacks these recognizability/border facts.

## 4. Fixed full local covers and changing monodromy

A D-sheet cellular covering of a finite CW complex has D times each cell count. Therefore its total rational cohomology rank is at most D times the base total cell count. This applies uniformly to a compatible inverse tower with *the same finite D* and cofinal base complexes of bounded cell count. Degree growing with scale is outside this argument.

For a tiling interpretation one additionally needs an equivariant local projection, a full D-sheet local lifting rule with unique continuation, a common bounded locality radius, and a minimal extension with the intended sheet count. Under those hypotheses, an n-patch lift is determined by a projected (n+c)-patch and one of D local sheets, hence `p_lift(n)<=D p_base(n+c)`. Base aperiodicity passes to an equivariant extension; repetitivity/minimality of an arbitrary finite extension does not follow solely from minimality of the base. Cellular covering data without local geometric/symbolic realization are not by themselves an admissible tiling.

Changing monodromy is not a rank loophole when D is fixed. New controls use the Fibonacci rose automorphism `a->ab,b->a`, whose abelianization T is unimodular. Cyclic cover cocycles satisfy `v_i=T^t v_(i+1)` modulo D; explicitly `v_(i+1)=(v_i(b),v_i(a)-v_i(b))`. For D=3,5,7 the cocycles change, every edge path lift has the correct endpoint, every cover is connected, and its H1 rank is D+1. The lifted automorphism induces an isomorphism on the corresponding covers. Primitivity/recognizability of an actual substituted tiling and full local lifting would still need to be checked separately; this control does not pretend the abstract rose is such a hull.

PF tile lengths and unit lengths give homeomorphic suspension spaces by rescaling fractional position separately on each tile interval. At the endpoints the identifications agree. This map reparametrizes time along orbits. It does not in general intertwine translation at the same real time. Čech rank only needs the homeomorphism; an action-conjugacy claim would require a separate cohomological roof condition. The new fractional control makes the changed time speed explicit.

## 5. An actual inverse 2-adic transfer tower and its exact exclusion

Let Y be a Sturmian Cantor system with shift S, Z another Sturmian system, and X=`Y x Z x Z_2`. Define the specified Z2 action by `(a,b)(y,z,u)=(S^a y, S^b z, u+a)`. It is free. It is minimal because each S^(2^k) is minimal (irrational rotation by 2^k alpha), so each residue class in the finite 2-adic quotient can be reached densely. The suspension maps at each quotient to the product of a suspension of S^(2^k) and the other Sturmian suspension.

There is a direct cohomology calculation, not merely a growing finite-stage conjecture. The Sturmian system is a circle with the orbit of a coding boundary split into left and right points. Its locally constant rational functions C have a finite-jump map onto `J=ker(augmentation Q[t,t^-1])=(t-1)Q[t,t^-1]`, with constants as kernel. The shift acts by t. J has no nonzero invariant vector of finite support under t^D. Passing to coinvariants of S^D therefore yields an exact injection of constants and quotient `J/(t^D-1)J` of dimension D. The suspension H1 has dimension D+1. Künneth with the second Sturmian factor gives H2 rank `2(D+1)`.

The quotient suspension at D=2^(k+1) is a genuine two-sheet cover of the one at D=2^k. Transfer composed with pullback equals 2 times the identity on rational cohomology, so every pullback is injective. Thus their increasing H2 classes survive and the inverse suspension has infinite rational H2. The exact circulant and repeated-residue matrices in the new control verify the quotient ranks and transfer identity; the geometry and jump-module argument above justify their relevance.

For the *specified action*, every finite continuous partition of X factors through some finite 2-adic quotient, uniformly by compactness. Points with the same y,z and distinct u,u+2^N then have identical partition itineraries at every group element. There is no finite continuous generator and no finite-alphabet expansive recoding of this action. Equivalently, these two fibre points stay arbitrarily close under all translates, so the action is nonexpansive. This disqualifies this construction as a low-complexity FLC subshift witness for the source problem. It does not prove that the underlying suspension space cannot be homeomorphic to an FLC tiling hull carrying some *different* action; no such stronger claim is made.

## Source and computational qualifications

Independent downloads of the 2016 original v2 content, Julien v1, Julien 2017, and the published Koivusalo-Walton paper were obtained before candidate comparison. The versioned 2016 PDF endpoint rejected direct acquisition with HTTP 406; its unversioned arXiv endpoint gave the frozen exact bytes, while the versioned web PDF and printed title confirmed v2. A Numdam retry timed out; the publisher mirror supplied the exact 2017 bytes. The freshly downloaded Cambridge PDF contains a new download timestamp and differs from the frozen PDF hash; the relevant mathematical content was separately checked in text and visually. This does not support a claim of four frozen-byte PDF matches.

New controls are exact rational/integer computations implemented from scratch using Python's standard library. Their finite outputs check the mechanisms above and explicitly label their universal proofs. They neither solve Problem 2.5.1 nor certify originality, a sixth author turn, publication readiness, or a DOI result.
