# Turn 5: positive names of semantically clopen instances

Substantive author turn **5/5**. The final attempt examines whether withholding a complement name can make clopen oracle instances powerful enough for the original Baire-choice reductions. It cannot: both relevant semantic clopen restrictions retain the unique-choice degree. This is a source-qualified corollary with explicit representation transformations, not a solution of either unrestricted open-set question.

Let R_cl+ be Sigma^0_1-RT restricted to open P which are topologically clopen, **with only the positive open name supplied**. Let A_cl+ be the analogous restriction of A=wFindHS_{Pi^0_1}. Then

        R_cl+ equivalent_W A_cl+ equivalent_W UC_{N^N} <_W C_{N^N}.   (11)

A separate representation task used in the proof has exact degree J: converting a positive name of a promised clopen set to a positive name of its complement. Here J is the ordinary Turing-jump operation on Baire names. The ordinary, strong and arithmetic reducibilities are not conflated.

## 1. Recover a complement name using one jump

Let Comp take a positive open name p of a topologically clopen P⊆[N]^N and output any positive open name of [N]^N\P. For a finite increasing string σ,

 [σ]∩P ≠∅ iff some cylinder [τ] enumerated by p is compatible with [σ].

This is a Sigma^0_1(p) property. The jump J(p) decides it uniformly in σ. Enumerate every σ for which the intersection is empty. The union of these cylinders is always the interior of the complement, and equals the entire complement under the clopen promise. Thus

                              Comp <=_W J.                         (12)

The input p may be retained by the ordinary postprocessor. Compatibility is decidable from finite strings, so this is an explicit name transformation, not an appeal to a supplied modulus of local constancy.

The promise matters. For P=[N]^N\{h_0}, where h_0(n)=n, P is computably open but not closed. No nonempty basic cylinder is disjoint from P. The above enumeration gives the empty interior, not the singleton complement; there is no open name of that complement. No extension of Comp to arbitrary open inputs has been used.

## 2. One jump is also necessary for this conversion task

For p∈N^N, let J(p)(e)=1 iff the e-th oracle machine with oracle p halts on input e. Compute a positive open name for

             P_p=⋃_{e:J(p)(e)=1} {f∈[N]^N:f(0)=e}.                 (13)

Dovetail the oracle computations and enumerate the corresponding first-coordinate cylinders when they halt. Every P_p is topologically clopen, since its complement is the union of the cylinders for the remaining first coordinates. In fact membership depends only on the first coordinate.

Given any open name of the complement, compute J(p)(e) as follows. Use the computable point f_e(n)=e+n. Dovetail the original positive membership test for f_e in P_p and the membership test in the returned complement name. Exactly one eventually succeeds. Output 1 or 0 accordingly. This is computable from the original input p and the oracle answer, proving

                              J <=_W Comp.                         (14)

Hence Comp equivalent_W J. This classifies a representation-conversion task, not the Ramsey operation itself. In particular it does not imply that a Ramsey answer supplies the missing complement name.

## 3. The credited clopen Ramsey and jump-absorption inputs

We now use precisely these published results:

- Marcone–Valenti, Theorems4.5–4.6: with the usual **two-sided** clopen representation, full clopen Ramsey and the weak clopen homogeneous-side problem are ordinary Weihrauch equivalent to UC_{N^N}. Their definitions and proofs in §§4.1–4.2 were read. The reduction is not asserted to be strong.
- Unique Baire choice absorbs a prior finite Turing jump: UC_{N^N} star J <=_W UC_{N^N}. This is the a=1 case of Marcone–Osso Corollary2.28, following their stated classical composition facts. The source and relevant argument were read.
- UC_{N^N} <_W C_{N^N}, with the strictness witnessed by the credited Kleene nonhyperarithmetical closed set, as recorded in turn 3.

These are established dependencies, not new conclusions credited to this attempt.

Apply (12) to turn the positive name of a semantically clopen P into its two-sided clopen name. The known full clopen Ramsey solver then returns a homogeneous solution. At the degree level,

 R_cl+ <=_W (clopen Ramsey) star J
       equivalent_W UC_{N^N} star J <=_W UC_{N^N}.                 (15)

Conversely, full clopen Ramsey reduces to R_cl+ by discarding the complement component of its input name. This gives R_cl+ equivalent_W UC_{N^N}.

The domain restriction gives A_cl+<=_W R_cl+. For the reverse bound, take an instance D of the known weak clopen problem, with a two-sided name and the promise that every homogeneous solution lands in D. Compute the positive name of P=[N]^N\D. No homogeneous solution lands in P, so P∈dom(A_cl+). Every output of A_cl+(P) lands in D and solves the original weak clopen instance. By the known equivalence this proves UC_{N^N}<=_W A_cl+. Together these establish (11).

## 4. Consequence for both original reductions

Neither original question can be solved by a forward functional whose outputs are always topologically clopen, even if it supplies only positive names, hides every bound, or uses unbounded finite adaptive inspection to determine membership. On the fixed computable hard Baire-choice input, any hypothetical successful reduction must produce a genuinely nonclopen open set.

For clarity, the obstruction is to **full** Ramsey and **promised avoidance**. It does not apply to the stronger task of selecting a landing solution when avoiding solutions also exist. The primary paper explicitly shows that its strong FindHS clopen task can compute C_{N^N}. A low-complexity homogeneous solution may lie on the wrong side for that different task.

Turn 5 subsumes the ordinary nonreduction conclusions of turns 3–4, while their explicit finite and omega-jump bounds under additional supplied lookahead hypotheses remain useful finer statements. The original historical files are preserved; they are not rewritten as if this final classification had been known at the start.

## 5. Final remaining gap

Countably many independent calls and effectively indexed all-valid feedback are absorbed by promised avoidance. Semantically clopen oracle encodings cannot solve either original question. What remains is arbitrary genuinely nonclopen open instances with full infinite-answer-dependent feedback and the source's exact domain promises. No proof gives C_{N^N}<=_W Sigma^0_1-RT or C_{N^N}<=_W A, and no argument separates C_{N^N} from either unrestricted target.

The original remains unresolved after all five substantive author turns. No historical novelty or full resolution is claimed. The known clopen results, classical hard-instance theorem, and arithmetic/ordinary distinction remain explicit. No sixth author search is part of this packet.
