# Independent pre-candidate reconstruction

Created before reading TURN_1, TURN_2, RESULT, README, or any historical review.

## Literal source target

Source arXiv1604.06280v2 page8 Problem2.5.1 asks: for a repetitive aperiodic tiling in dimension d with patch complexity O(n^d), is total rational cohomology rank finite? The source's cited one-dimensional theorem is already affirmative. Julien0804.0145v1 Theorem5.10 identifies the suspension with inverse limits of alternating left/right Rauzy graphs; Lemma5.14 passes bounded rank on a cofinal subsequence to rational Cech cohomology; Proposition5.16 gives linear complexity implication. Julien2017 page546 defines aperiodicity as absence of every nonzero translational period and repetition as syndetic occurrence of every finite patch. Finite local complexity is automatic in the finite-symbol lattice subclasses. The translational hull is the suspension, not a rotation quotient or singular-cohomology substitute.

Koivusalo-Walton's introduction, Example4.3 and Section8 establish a published qualification: acceptance domains and hyperplane cut regions need not describe the same topology under almost-canonicity alone; quasicanonicity suffices and canonical schemes satisfy it. This is credited background, not a new correction.

## Product family deduced independently

Let X_i be minimal aperiodic one-dimensional subshifts, with the Zd action acting in coordinate i on X_i only. The cube language is the Cartesian product of the factor languages, hence P(n)=product_i p_i(n). Each factor has p_i(n)>=n+1. Thus P(n)=O(n^d) implies p_i(n)=O(n), by division by the remaining factors. The suspension is homeomorphic to the product of the one-dimensional suspensions: [(x,t)] maps to ([x_i,t_i])_i, with a continuous bijection between compact Hausdorff spaces. The rational Cech Kunneth theorem gives dim H^k = sum over |I|=k of product_{i in I} r_i, where r_i=dim H^1(Omega_i;Q), H^0=Q, and higher groups vanish. The published one-dimensional theorem gives each finite r_i, establishing this restricted family.

A quantitative estimate may use A_i=liminf_n p_i(n)/n, since liminf of increments cannot exceed A_i and Rauzy graph rank is increment+1. This implies r_i<=floor(A_i)+1 when A_i is finite. From P(n)<=C n^d one only directly gets A_i<=C; different liminf subsequences must not be multiplied without proof. Stronger joint/product coefficient claims need separate scrutiny. Sturmian factors have p_i(n)=n+1 and expected rational H^1 rank2; if each rank2 is justified at the limit, product degree ranks are binomial(d,k)2^k and total3^d. Merely observing every graph has rank2 gives an upper bound, not equality, unless the bonding maps preserve both classes.

## Independent planned falsifiers

1. Generate complete finite Fibonacci factor languages from substitution images of all legal length-two words, rather than importing candidate rotation arithmetic; compare Cartesian and sheared box counts against formulas.
2. Build boundary matrices independently from signed edge/face cropping, using dense exact integer/rational rank; compare homology ranks and graph product identities at several scales.
3. For shear A(i,j)=(i+j,j), distinguish the fact that the infinite suspension is homeomorphic to a product from the assertion that axis-aligned finite approximants are Cartesian products. Every n by m array reveals an x-word of length n+m-1 and a y-word of length m, but the face gluing may add spurious cycles. Growing approximant ranks cannot alone prove growing direct-limit cohomology.
4. Verify exact snapshot bytes against both outer SHA manifest and frozen Git objects, then privately reproduce candidate scripts and retain stdout/stderr and returncodes. Finite checks are explicitly finite; all-scale bounds require deductions.

Audit completion estimate:20%. No candidate or historical verdict consulted.
