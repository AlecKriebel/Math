# Failure of the uncorrected one-step entropy drift

Consider the directed weakly reversible cycle

    0 -> A+B -> B -> 0

with arbitrary positive rates.  At a state `(n,0)`, only `0 -> A+B` is
enabled.  For

    U(x)=sum_i [x_i log x_i-x_i+1]

(with `0 log 0=0`),

    L U(n,0)=kappa_1[U(n+1,1)-U(n,0)]>0

for every `n>=1`, and the increment is asymptotic to `log n`.  Thus the
standard entropy cannot satisfy a one-step Foster inequality, even though
this network has a strong restoring mechanism after the missing co-reactant
`B` is created.

This is an exact counterexample to the intermediate lemma, not a
counterexample to positive recurrence.
