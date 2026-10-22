# Turn 5: finite-depth entropy tests and the remaining transition gap

**Final substantive author turn 5. Original question remains unsolved.** This turn proves a richer constructive criterion for the same unknown uniform Cayley-tree mixture, including mean degree c=3/2. The true transition and the critical c=e information law remain unproved. The construction develops the source's credited hairy-path idea; no novelty claim or polynomial-time guarantee.

## 1. A finite-depth branching experiment

Fix c>0. Let Q_d be a Poisson(c) Galton–Watson tree observed to depth d. Let P_d have a signal root, with two latent vertex types:

- A signal vertex has independent Poisson(1) signal children and Poisson(c) noise children
- A noise vertex has Poisson(c) noise children

Only the untyped depth-d rooted tree is observed. Children can be randomly ordered for construction; the likelihood below is symmetric and applies to unordered rooted trees as well. Put R_d=dP_d/dQ_d and D_d=E_(Q_d)[R_d log R_d]. At depth zero R_0=1 and D_0=0.

Conditioning on the root children gives the exact likelihood recursion

    R_(d+1)=exp(−1) product_(children v) [1+R_d(v)/c]. (1)

Under Q_(d+1), the child count is Poisson(c) and the R_d(v) are iid copies under Q_d. Hence E R_d=1. Poisson generating functions and their differentiated form give

    m_(d+1)=exp(m_d/c), m_d=E_(Q_d)R_d², m_0=1,   (2)
    D_(d+1)=−1+E_(Q_d)[(c+R_d)log(1+R_d/c)].      (3)

All finite-depth moments needed here are finite. For example log R_d≥−1 for d≥1, and its positive part is bounded by a constant (depending on c,d) times the number of vertices in the depth-d tree. That count has finite moments of every fixed order under both finite-depth laws.

### Constructive criterion for the original graph model

For any fixed depth d≥1, if

    D_d(c)>log c,                                  (4)

then strong detection in the original unknown-tree experiment is possible whenever k/(log n)²→infinity. This statement is proved in Sections 2–5, including the bridges from the auxiliary branching model to an actual planted Cayley tree and to the null graph. It is not based on a bare local-weak-limit assertion.

At d=1, (3) gives D_1=(c+1)log(1+1/c)−1, recovering Turn 2's criterion. Section 6 gives an exact certificate that D_2(3/2)>log(3/2), although D_1(3/2)<log(3/2).

## 2. Exact selected-root forest law in a conditioned Cayley tree

Condition a uniform labelled k-tree on containing a specified path of length D, with its ordered labels fixed. Select r of the path vertices as roots. Remove the path edges, and observe their off-path rooted trees to fixed depth d. A possible rooted forest F has j new vertices, I internal vertices (those at depth less than d, including its r roots), and automorphism number aut(F) fixing each root. Its inclusion with the specified depth-d neighborhood means no further edges may leave the I internal vertices.

The full specified graph H consists of the D+1 path vertices and the j new ones. It is connected and has V=D+1+j vertices. Its allowed attachment vertices for an extension are precisely the b=V−I noninternal vertices of H. Contract H. Weighted Cayley enumeration with weight b for this component and weight one for each remaining singleton gives

    number of extensions = b(k−I)^(k−V−1),        (5)

provided V<k. When V=k there is one extension, H itself; this handles the formal zero-weight edge case without a 0/0 expression. In the asymptotic range below b>0 and V<k automatically.

There are (k−D−1)_j/aut(F) ways to assign the new labels. The total number of trees containing the specified path is (D+1)k^(k−D−2). Thus the exact probability of the rooted shape F is

    [(k−D−1)_j/aut(F)]
      [(D+1+j−I)/(D+1)]
      [(k−I)^(k−D−j−2)/k^(k−D−2)].               (6)

The corresponding shape probability for r independent depth-d Poisson(1) Galton–Watson trees is

    exp(−I)/aut(F).                               (7)

Equations (5)–(7) are checked by direct labelled-tree enumeration in the checker, including complete-extension exceptions. They follow from the same classical weighted Prüfer identity as Turn 1.

## 3. A growing number of actual off-path neighborhoods

Let r=O(log n), with r→infinity and r=o(sqrt(k)). If D satisfies

    r/D→0 and rD/k→0,                             (8)

then the joint depth-d off-path forest at the r selected path vertices is at total-variation distance o(1) from r independent Poisson(1) depth-d trees.

To prove this, restrict first to shapes with j+I≤Mr for a fixed M. Dividing (6) by (7), and extracting k^j from the falling factorial, gives the ratio

    [(k−D−1)_j/k^j]
    [1+(j−I)/(D+1)]
    (1−I/k)^(k−D−j−2) exp(I).                    (9)

Its logarithm is uniformly

    O_M(rD/k+r²/k+r/D)=o(1).                      (10)

All factors are legal under (8) for large k. For fixed d, the total size and internal count of r independent Poisson(1) depth-d trees obey a law of large numbers, with finite variance. Choose M larger than their mean per root. Then j+I≤Mr has probability 1−o(1) under (7). The uniform ratio (9) makes its probability 1−o(1) under (6) as well, and summing the density difference proves the total-variation claim. This argument does not require every individual rooted neighborhood to have bounded size.

To obtain (8) for a typical planted tree, take its path between two fixed labels. Turn 2 gives the exact distance distribution, and telescoping it also gives

    Pr(D≥t)=(k−2)_(t−1)/k^(t−1).                  (11)

Put u_n=sqrt(k)/r→infinity and a_n=sqrt(u_n). With probability 1−o(1),

    r a_n ≤ D ≤ sqrt(k) a_n.                      (12)

The lower failure probability is O(1/u_n) by Turn 2's short-distance bound; the upper is at most exp(−Omega(a_n²)) by (11). Both conditions (8) hold uniformly in (12).

Use an initial ell-edge prefix of this long path, with ell=r+1, and select only its r interior vertices. In the eventual detector the two endpoints are deleted before off-path exploration. Therefore neither endpoint's continuation of the planted path contaminates the rooted off-path neighborhoods. Edges among the r roots are ignored during exploration. The selected-root law just proved applies to these interior vertices.

## 4. Adding the background graph on the alternative side

It suffices first to consider k≤n/(log n)²; larger k are strongly detected by the classical edge-count test because they exceed sqrt(n) by a diverging factor.

For the selected path, couple its signal-only depth-d forest to the independent Poisson(1) forests from Section 3. Now expose independent background edges by a simultaneous breadth-first exploration to depth d, after deleting the two path endpoints and ignoring edges among the selected roots. Noise branches are followed in the same way as signal branches, but types are hidden from the detector.

The reference process is exactly r independent copies of P_d. For fixed d, its total number of explored vertices is O(r) with probability tending to one; stop at Mr vertices first and then choose a sufficiently large fixed M. During such a stopped exploration:

- Each background offspring count is Bin(n−k−O(r),c/n), with total-variation error O((k+r)/n) from Poisson(c)
- A background edge hits an unexposed planted vertex with total probability O(rk/n)
- Collisions, extra edges among exposed vertices, or merges between different roots have total probability O(r²/n)

These follow by exposing previously unqueried independent Bernoulli edges, the elementary binomial-to-Poisson bound, and a union bound over O(r) exposed vertices. All tend to zero because r=O(log n) and k≤n/(log n)². The signal forest has no cross-root edges because it is attached to a tree path; an off-path connection between two roots would form a cycle. Its already controlled depth-d law can therefore be used throughout the coupled exploration. A hit into other planted vertices is explicitly counted as a bad event, rather than silently treated as a noise vertex.

The reference process exceeds Mr vertices with probability o(1) when M is above its finite mean per root, by its law of large numbers. Removing the stopping rule proves that the observed joint rooted forest on the alternative side is within o(1) total variation of P_d raised to the r-th product power. In particular, with high probability it is a forest and has at most Mr vertices for a suitable constant M.

## 5. A multiplicative null bound and the actual test

An additive local coupling error is insufficient for a union bound over many candidate paths. We instead use an exact exploration probability.

Fix an ordered simple ell-edge path under the null and condition on its path edges being present. Delete its endpoints, and let its r=ell−1 interior vertices be the roots. Ignore root-root edges. Perform simultaneous depth-d breadth-first exploration. Require all queried edges outside the root set to form disjoint rooted trees; edges between two depth-d frontier vertices are not queried and are irrelevant.

Write m=n−2 for the remaining ambient vertex count. For a rooted exploration forest F with j nonroot vertices and I internal vertices, its exact probability is

    [(m−r)_j/aut(F)] p^j (1−p)^A,
    A=I m−I(I+1)/2−binom(r,2)−j.                 (13)

The exponent counts all queried incident pairs at internal vertices, excluding root-root pairs and the j present forest edges. Frontier-frontier pairs are unqueried. Conditioning on the original path has no effect on these off-path edges.

The r-fold Q_d shape probability is c^j exp(−cI)/aut(F). Uniformly when j≤Mr, equation (13) divided by this reference probability is

    exp(O_(c,d,M)(r²/n))=1+o(1).                 (14)

Indeed the label falling factorial contributes O(r²/n) in its logarithm, and expanding log(1−c/n) in (13) cancels the term −cI with the same error. This is a relative bound on each shape, so it remains valid for rare score events after summation. It is not an additive approximation multiplied by the number of paths.

Choose b with log c<b<D_d(c) and K>1/(b−log c), and let ell=ceil(K log n). For each candidate path, use the exploration above and reject the null if it is a forest with j≤Mr and

    sum_(roots v) log R_d(F_v) ≥ b r.             (15)

Under the r-fold Q_d law, exp of the score has expectation one. Markov's inequality and (14) bound a candidate's conditional null probability by (1+o(1))exp(−br). There are at most n c^ell ordered paths in expectation. The total null rejection probability is therefore at most

    (1+o(1)) n c^ell exp(−b(ell−1))=o(1).         (16)

Under the alternative, Sections 3–4 provide a candidate whose neighborhood law approaches the r-fold P_d law. Its average score tends to D_d(c)>b by the law of large numbers, and its total size is at most Mr with probability 1−o(1) if M is chosen above the mean. Thus it satisfies (15). For k>n/(log n)² use the edge-count branch of the test. This proves criterion (4) for all k/(log n)²→infinity, with no assumption that the hidden shape is revealed.

The path scan may take n raised to O(log n) time; no polynomial-time result is claimed.

## 6. Exact improvement to c=3/2

At depth one, R_1=exp(−1)(1+1/c)^J with J~Poisson(c) under Q_1. Therefore

    D_2(c)=−1+exp(−c) sum_(j≥0) c^j/j!
      (c+r_j)log(1+r_j/c),
    r_j=exp(−1)(1+1/c)^j.                        (17)

Every summand is nonnegative. At c=3/2, retain only j=0,...,9. Exact rational bounds certify that the sum of these ten terms is at least

    1407870769705 / 10^12,

while log(3/2) is at most 405465108109/10^12. Hence

    D_2(3/2)−log(3/2)
       ≥601415399/250000000000 > 1/500.           (18)

The certificate uses odd-order alternating lower bounds for exp(−1) and exp(−3/2), and the positive atanh series for logarithms after reducing arguments by powers of two. Each retained term is rounded down to a rational with denominator 10^12. All omitted terms are nonnegative. The ten lower numerators and all interval parameters are recorded in `verification_turn5.json`; the checker uses rational arithmetic only for (18).

Thus one may take b=log(3/2)+1/1000 and K=2000 in (15)–(16). The exact checker also confirms that the depth-one criterion fails at c=3/2, so this uses genuinely richer local information than Turn 2's boundary count. It still requires k≫log² n and does not answer the O(log n) question.

## 7. Why the recursion does not finish the transition

The scalar sequence in (2) is increasing. A finite fixed point satisfies c=x/log x for x>1; the minimum of x/log x is e. Therefore:

- For c>e, m_d increases to the smaller fixed point in (1,e)
- For c=e, m_d increases to e
- For c<e, m_d diverges

These are exact auxiliary second-moment statements. They do not imply that the entropy crosses log c whenever c<e.

Data processing makes D_d nondecreasing in d. For c≥e, Jensen under P_d gives

    D_d≤log(E_(P_d)R_d)=log m_d≤log c.            (19)

Thus no finite depth passes criterion (4) at or above e. At c=e the likelihood martingale is L² bounded and has an L² limit; the second-moment divergence below e does not establish failure of uniform integrability or any entropy threshold.

There is also a noise-addition channel from c_1 to c_2>c_1 in the auxiliary tree experiment: recursively add independent Poisson(c_2−c_1) noise children at each existing vertex, growing their descendants with the c_2 noise law. It does not need to know the latent types and maps both hypotheses at c_1 to those at c_2. Hence D_d(c) is nonincreasing in c.

Let C_ent be the supremum of fixed c for which D_d(c)>log c for some finite d. The proved detector and Turn 1 give

    3/2 ≤ C_ent ≤ C_poly ≤ e.                     (20)

No converse equating C_ent with the true graph threshold has been proved. Nor has the value of C_ent been determined. A divergent recursion m_d for c<e is not enough to fill either gap. Similarly Turn 3's exact critical L² window remains without a total-variation law for growing supports.

## 8. Final status after five substantive turns

The original transition is **unsolved after 5/5 author turns**. The package now includes exact forest moments, a high-c detection scale, a critical L² law, an actual high-c likelihood/TV limit, and rigorous finite-depth constructive detection including c=3/2. These are scoped partial results, not a sharp information-theoretic phase diagram.

Missing are the actual boundary in (20), a converse or stronger detector in the remaining interval, the optimal low-c unknown-tree size, and the critical c=e testing law. The source's fixed-C log² result is credited but not reproved here; our constructive condition k≫log² remains explicit. Separate full analytic adversarial review is required before a partial-result PR.
