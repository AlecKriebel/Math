# Turn 4: computably bounded first-value lookahead is still insufficient

Substantive author turn **4/5**. Turn 3 excludes finite global arity. This turn tests genuinely unbounded arity controlled by the first value and proves a larger restricted nonreduction. It does not exclude arbitrary open sets.

Say an open P⊆[N]^N has **computably bounded first-value lookahead** if there exists a total computable function ell:N→N with ell(n)>=1 such that, on the section f(0)=n, membership f∈P depends only on f's first ell(n) entries. There need be no global bound on ell. Neither ell nor a program index for it is supplied with the positive open-set name.

Let R_first and A_first be the restrictions of the full open Ramsey problem and of promised avoidance to this semantic class. Then

                   C_{N^N} not<=_W R_first,
                   C_{N^N} not<=_W A_first.                         (8)

The proof gives a hyperarithmetical basis property, not a uniform procedure for extracting an unsupplied lookahead bound.

## 1. A relativized basis lemma with a supplied bound

Suppose p is an open name, and an index of a p-computable total ell satisfying the promise is supplied for this paragraph. There is a homogeneous solution computable uniformly from

              (p^{(omega)})'',   p^{(omega)}=join_{j∈N} p^{(j)}.    (9)

This is an explicit hyperarithmetical upper bound. No claim of optimality is made.

For each n put r_n=ell(n)−1. On increasing r_n-tuples τ with every entry greater than n, define c_n(τ) to be the membership color of a sequence beginning with n followed by τ. The promise makes this independent of the remaining extension. Just as in turn 3, the existence of a compatible cylinder in the positive enumeration is a Sigma^0_1(p) question, so every c_n is uniformly p'-computable. When r_n=0 this is simply one bit.

Construct increasing x_0,x_1,... and nested infinite reservoirs R_s. Initially R_0=N. At stage s, choose x_s=min R_s and consider the tail of R_s above x_s. If r_{x_s}=0, keep that tail as R_{s+1} and record the single color a_s. Otherwise apply the finite-arity construction from turn 3 to c_{x_s} on that tail, obtaining an infinite homogeneous subset R_{s+1}; record its color a_s.

More precisely, retain at stage s a finite integer t_s>=1 and an index of an increasing enumeration of R_s computable in p^{(t_s)}. Membership of an infinite increasingly enumerated set is decidable in the same oracle: enumerate until reaching or passing the tested number. Reindexing c_{x_s} by the reservoir's enumeration gives a p^{(t_s)}-computable finite coloring. Turn 3 supplies an enumeration of R_{s+1} in p^{(t_s+2r_{x_s})}. Use this as t_{s+1}, or retain t_s if r_{x_s}=0. Every t_s is finite, though the sequence need not be bounded.

A program with oracle p^{(omega)} can reconstruct any finite stage and the indices of the relevant finite-jump programs. It need not finish generating an entire infinite reservoir before proceeding: the uniform Ramsey construction gives a program index, and only finitely many of its output values are needed to choose the next point or read its color. Thus both the sequence (x_s) and the color sequence (a_s) are computable in p^{(omega)}.

Use two more jumps to choose an infinite color class of the sequence (a_s), by deciding the Pi^0_2(p^{(omega)}) infinitude question. Let H be the corresponding subsequence of the x_s. Every later selected point after x_s lies in R_{s+1}. Therefore any infinite subsequence of H beginning with x_s has its first r_{x_s} later points in the reservoir on which c_{x_s} is constantly a_s. All the selected a_s have the same color, so H is homogeneous for P. This proves (9). If P is a valid avoidance instance, that color must be 0.

## 2. Remove the supplied-bound assumption for the separation

For a computable positive name p in the semantic class, there exists some ordinary computable ell and a finite program index witnessing the lookahead property. Fix such an index nonuniformly. Section 1 gives a hyperarithmetical homogeneous solution. This existence statement does not require an effective search for the index.

Apply a hypothetical ordinary reduction from Baire choice to a computable Kleene hard instance having no hyperarithmetical path (the credited dependency bound in turn 3). Its forward output has a computable positive name and, by hypothesis, some computable first-value lookahead bound. Choose the resulting hyperarithmetical homogeneous solution. The computable postprocessor with the computable original input would produce a hyperarithmetical path, a contradiction. The same reasoning applies to the avoidance restriction because every homogeneous solution on its domain avoids the set. This proves (8).

## 3. This class really permits unbounded global arity

Consider the computably clopen set

       P={f∈[N]^N : f(f(0)+1)=f(f(0))+1}.                           (10)

The two occurrences f(f(0)) and f(f(0)+1) are entries of the same increasing sequence. Membership is decided by ell(n)=n+2 entries on the section f(0)=n. No finite global arity works: after any proposed finite initial bound m, choose a first value n>=m, fix the first m entries, and complete the sequence so that the two entries at positions n and n+1 are either consecutive or separated by at least two. These extensions have opposite membership while agreeing on the first m entries.

The set also satisfies the avoidance promise. Every infinite sequence has an infinite subsequence whose successive differences are at least two. Such a subsequence is outside P, and in fact every one of its subsequences is outside P. Thus no infinite sequence can land homogeneously in P. The all-even sequence is a computable avoiding solution, so (10) is an example separating the coding classes, not a hard instance or a counterexample to the original question.

## 4. What the strengthened obstruction does not prove

Successful encodings of the fixed hard Baire-choice instance cannot always have a computable first-value lookahead bound. Merely allowing arities such as n+2, 2^n, or any other total computable growth rule is insufficient. This strengthens turn 3's specific coding obstruction.

Arbitrary computably open sets need not have this property. An attempted reduction may use more intricate dependence on successive entries, and the argument supplies no computable bound for those instances. The fusion in §1 is used to prove a low-solution existence theorem, not an ordinary Weihrauch realizer using no jumps. No uniform reduction for the semantic restriction with its bound withheld is claimed. Original unresolved4/5; classical finite Ramsey, finite jumps, fusion and the credited Kleene theorem remain the ingredients.
