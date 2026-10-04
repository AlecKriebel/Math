# Turn 2: a uniform large-volume gap from a sharp sixth-moment defect bound

The original optimal-flux question remains unresolved. This turn upgrades the first-turn non-saturation observation to a size-uniform energy gap for every phase configuration on even square tori of side L>=8. It also proves a sharp thermodynamic lower bound for a related sixth-degree spectral defect. The defect minimizer is not asserted to minimize the quarter-filled energy.

## 1. Closed-walk moment identities

Let N=L² with L>=8, and write each plaquette flux as phi_p modulo2pi. Let p~q denote adjacent plaquettes, each unordered pair counted once; there are2N such pairs. Since a length6 walk cannot wind around such a torus, its closed-walk expansion is the same local expansion as on the square lattice. Put S=sum_p cos(phi_p). Then

    Tr(T²)=4N,
    Tr(T⁴)=28N+8S,
    Tr(T⁶)=232N+144S+12 sum_(p~q) cos(phi_p+phi_q).         (1.1)

Here the orientation of every plaquette is chosen consistently. The length4 identity counts28 freely backtracking walks at each root and the eight oriented rooted traversals of each square.

For length6, there are400 closed walks at a root, from the elementary binomial count of horizontal and vertical steps. Of them232 reduce completely by deleting immediately reversed edges. They correspond to the five Dyck patterns of length6, with counts36,36,48,48,64 for a degree4 tree. The simple length6 cycles are the two shapes of1 by2 rectangle. There are2N rectangles, and each has six possible roots and two orientations, giving24N walks. Every remaining walk reduces to a single square traversal with one reversed-edge excursion; there are144N of these. Translation symmetry assigns the same aggregate coefficient to each plaquette, and orientation reversal pairs conjugate phases. Thus their total is144S. Each rectangle contributes12 cos(phi_p+phi_q), proving(1.1).

For completeness, the supplied exact enumerator lists all4096 direction words of length6, retains the400 returning words, and computes their integer plaquette winding vectors. It verifies the232/144/24 classification, including adjacency and equal orientation of the two rectangle plaquettes. This is an independent finite combinatorial certificate for the coefficients in(1.1).

## 2. The defect as an exact sum of squares

Define

    D(T)=||T³−8T||_F²=Tr(T⁶)−16Tr(T⁴)+64Tr(T²).

Using(1.1),

    D(T)=40N+16S+12 sum_(p~q) cos(phi_p+phi_q).             (2.1)

Write c_p=cos(phi_p), s_p=sin(phi_p). The identity

    cos(phi_p+phi_q)
      =[(c_p+c_q)²+(s_p−s_q)²]/2−1

gives

    D(T)=16N+16S+6 sum_(p~q)(c_p+c_q)²
                    +6 sum_(p~q)(s_p−s_q)².

The average of c_p+c_q over the2N edges is2S/N. Completing the square yields the exact formula

    D(T)−44N/3
      = (48/N)(S+N/6)²
        +6 sum_(p~q)(c_p+c_q−2S/N)²
        +6 sum_(p~q)(s_p−s_q)² >=0.                       (2.2)

Therefore D(T)>=44N/3 for every choice of hopping phases and torus holonomies.

The constant44/3 is sharp as a thermodynamic defect bound. Choose all plaquette fluxes equal to phi_L=2pi m_L/L², with m_L the nearest integer to L² arccos(−1/6)/(2pi). The compatibility condition is satisfied, so Turn1 constructs such a torus hopping matrix. Then phi_L tends to arccos(−1/6), and(2.1) gives

    D(T)/N =16+16 cos(phi_L)+48 cos²(phi_L) →44/3.

This optimizes only the displayed polynomial defect in the limit. It does not identify the minimizer of the sum of the lowest N/4 eigenvalues.

## 3. Conversion to a uniform quarter-filled energy gap

Let q=N/4 and r=sqrt8=2sqrt2. Use the singular values s_1>=...>=s_(2q)>=0 of the bipartite block B, as in Turn1. The operator norm bound ||T||<=4 follows from the degree4 row sums (or the elementary Cauchy–Schwarz bound on each row). Thus each singular value lies in[0,4]. Set

    delta=q r−sum_(j=1)^q s_j = E_q(T)+N/sqrt2 >=0.

Since sum_j s_j²=2N=8q,

    sum_(j<=q)(s_j−r)²+sum_(j>q)s_j²=2r delta.             (3.1)

For f(s)=s(s²−8), on[0,4] we have

    |f(s)|=s(s+r)|s−r| <= M |s−r|,  M=4(4+r)=16+8sqrt2,
    |f(s)|<=8s.

Use the first estimate on the top q singular values and the second on the remaining ones. Since8<=M,

    D(T)=2 sum_j f(s_j)² <=4r M² delta.                    (3.2)

Combining(2.2) and(3.2) gives the size-uniform bound

    E_q(T)/N >= −1/sqrt2 + 11/[3r M²]
              =−1/sqrt2 +11(3sqrt2−4)/1536.               (3.3)

The correction is strictly positive. All phases and both torus holonomies are allowed. The bound is deliberately coarse; there is no claim that equality in(3.3) is attained or that it matches the uniform-pi/2 energy.

## 4. Why this does not optimize the energy

The polynomial defect weights all singular values through s²(s²−8)², whereas the quarter-filled energy uses only the largest q singular values of B. The estimates in(3.2) have substantial slack and no implication that their minimizers coincide. In particular the defect-preferred limiting flux arccos(−1/6) must not be reported as an energy-preferred flux or a counterexample to pi/2.

The next comparison must retain the actual sorted spectral sum. Moment identities and universal lower bounds alone do not establish that a particular configuration attains the global energy minimum.

## 5. Exact controls

verify_turn2.py enumerates winding vectors, checks(1.1)–(2.2) by Gaussian-integer matrix multiplication on random quarter-root edge phases for L=8,10,12, and tests the scalar bounds in(3.2) using exact rational/quadratic-field comparisons. These finite checks support the proved all-L statements. They do not scan arbitrary continuous phases or certify the source's optimal-flux conjecture.
