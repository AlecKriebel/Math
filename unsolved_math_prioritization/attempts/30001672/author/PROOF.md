# Existing negative resolution of the n/3 influence question

Problem 30001672 (OWR-4791-032), **High Influence Small Sets in Boolean Functions**.

Status: **already_solved**. This is a literature correction and a verification of the implication to the recorded problem. It is not a new counterexample or a novelty claim.

## Target and conventions

For a Boolean function f on {0,1}^n, let U_S(f) be the probability that a uniform assignment to the coordinates outside S leaves a nonconstant function on the free coordinates S. The question asks for an absolute c in (0,1) such that every function whose mean is bounded away from 0 and 1 admits |S| <= n/3 with U_S(f) >= 1-c^n, in the intended asymptotic sense.

Nati Linial's problem in the 2011 Oberwolfach report, printed pp. 75–76, uses this definition and also mentions replacing 1/3 by any fixed fraction below 1/2. [Original report](https://doi.org/10.4171/owr/2011/01).

## The existing theorem

Use Theorem 1.1 of Bourgain, Kahn and Kalai, *Influential Coalitions for Boolean Functions I: Constructions*, Theory of Computing 20(4) (2024), p. 2. Its specialization to mean 1/2 and delta=1/6 provides a fixed C>0 and, for every sufficiently large n, a Boolean function f_n with

- E f_n = 1/2;
- J_S^+(f_n) <= 1-n^(-C) for every S with |S| <= n/3.

Here J_S^+(f) is the probability that the restricted fiber contains at least one input with output 1. Enlarging C if necessary gives C>0 and retains the weak inequality used here. [Published theorem](https://toc.cs.uchicago.edu/articles/v020a004/v020a004.pdf#page=2).

The earlier Kahn–Kalai preprint *Functions without influential coalitions* (2013), Theorem 1.1, p. 2, already has this counterexample theorem for coalitions of the specified size. Smaller coalitions follow by containment and monotonicity. [Earlier primary source](https://arxiv.org/abs/1308.2794).

## Bridge to the recorded notion of influence

Fix S and an outside assignment u. Let A(u) mean that some completion of u has output 1, and B(u) mean that some completion has output 0. Every fiber is nonempty, so A union B is the whole outside-assignment space. The fiber is undetermined exactly when A and B both occur. Consequently

U_S(f) = J_S^+(f) + J_S^-(f) - 1 <= J_S^+(f).

Equivalently, a fiber with no 1-output is forced to 0 and cannot contribute to U_S. This proves the required implication from a one-sided obstruction; no simultaneous lower obstruction for the other output is needed. The shifted quantity I_S^+ = J_S^+ - E f is not itself U_S.

Apply the displayed inequality to the supplied f_n. Every allowed S satisfies

U_S(f_n) <= 1-n^(-C).

Now fix any c in (0,1), and set a=-log(c)>0. Since log(n)/n tends to zero, eventually C log(n) < an. Thus n^(-C) > exp(-an) = c^n, and

U_S(f_n) < 1-c^n

for every |S| <= n/3. This contradicts the proposed universal guarantee. Because all f_n have mean exactly 1/2, no ambiguity about how far the mean stays from 0 or 1 affects the conclusion. Integer coalition sizes mean |S| <= floor(n/3); the published theorem covers this directly.

The same argument with delta=1/2-r refutes the reported extension for each fixed r in (0,1/2). It does not make a claim at r=1/2 or about optimal polynomial error rates.

## Scope of verification

The proof above is a complete reduction to a published counterexample theorem. The relevant definitions, theorem and its proof on p. 8 were inspected, along with the original problem and earlier primary source. The proof of the published existence theorem is not reproduced here. The accompanying finite controls check the bridge and its normalization; they do not replace that existence theorem.
