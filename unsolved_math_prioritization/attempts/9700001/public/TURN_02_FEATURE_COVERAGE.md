# Attempt 2: feature coverage rather than a small filtration

Keep a finite horizon and filtration F, and put Delta_t=X_{t+1}-X_t. Suppose phi_{t,j} are specified F_t-measurable real features with all products used below integrable. They need not generate a nested sequence of small sigma-fields. Suppose

|E[phi_{t,j} Delta_t]| <= eta_{t,j}.

## Theorem 2: explicit approximation cost for stopping rules

For an F-stopping time T, suppose deterministic coefficients a_{t,j} give

f_t=sum_j a_{t,j} phi_{t,j},
E[|1_{T>t}-f_t| |Delta_t|] <= rho_t.

Then

|E X_T-E X_0| <= sum_t (rho_t+sum_j |a_{t,j}| eta_{t,j}). (4)

Proof. Substitute f_t+(1_{T>t}-f_t) into the telescoping identity (2) of Attempt 1, take expectations, and apply the triangle inequality term by term. There are finitely many terms, and the stated integrability ensures each operation is valid. QED.

For bounded increments |Delta_t|<=L_t, an L1(P) approximation error alpha_t for the survival indicator suffices with rho_t=L_t alpha_t. Exact membership of every relevant survival indicator in the span gives a full guarantee for that specified strategy family. The coefficient norms must also be bounded for approximate moment constraints to be meaningful.

For indicator features phi=1_A, their moments are differences of genuine stopping expectations, using T(t,A) and deterministic t as in (1). Thus (4) can be certified by stopping constraints without disguising a general trading strategy as a stopping time. General signed features are a separate moment formulation; we do not call them individual stopping constraints.

## Current-state tests alone fail without a conditional-law hypothesis

Let B,C be independent fair signs. Define

X_0=0, X_1=B, X_2=B+C,
H=1 on (B,C)=(1,-1), H=-1 on (-1,1), and H=0 otherwise,
X_3=X_2+H.

The four equally likely paths are (0,1,2,2), (0,1,0,1), (0,-1,0,-1), and (0,-1,-2,-2). Each adjacent pair satisfies E[X_{t+1}|X_t]=X_t: the first two steps use centered independent signs, and at time 2 the only ambiguous state is 0, where the two H values cancel. Consequently every deterministic-time test and every one-step test for an atom of sigma(X_t) has zero expectation deviation.

But the entire observed history identifies B and C at time 2. Set T=3 on {(B,C)=(1,-1)} and T=2 otherwise. This is a stopping time for the natural filtration, and

E X_T = E X_2 + E[1_{(B,C)=(1,-1)} H] = 1/4.

The relevant survival indicator at time 2 is not a function of the current state X_2. This is why merely listing O(n times number-of-current-states) constraints is insufficient. Earlier stopping decisions retain information even when the state labels later coalesce.

## Outcome

Equation (4) gives a precise route from a finite feature dictionary to guarantees for a richer stopping class, with explicit approximation and conditioning costs. No theorem here provides polynomial-size coverage of all efficiently computable survival events for arbitrary processes. Selecting a useful dictionary remains part of the missing model, and Attempt 3 tests the possibility of an unrestricted fixed certificate family.
