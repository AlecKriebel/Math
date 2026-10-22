# A legal lead-sixteen defeat of the exact two-layer tracker

Status: PASS4 restricted-policy obstruction, submitted for independent audit. This is not a Devil-winning strategy against an unrestricted full-history Angel.

## Policy class

Fix a deterministic real reference sequence known to the Devil, and a deterministic tie order. Consider the PASS3 controller which, before move n, forms the admissible moves

    G_n={q in N(a_(n-1)): q is not bombed at time n,
                           at most seven known time-(n+1) bombs lie in N(q)}.

It chooses the member whose displacement has greatest projection toward the next reference point, with its fixed tie rule. Its choice depends on the bombs only through G_n; it does not use more distant timestamps or use sparse next-layer bombs to change the tie rule. The argument also applies to any deterministic policy whose action agrees with its bomb-free action whenever G_n=N(a_(n-1)).

All bombs in the construction have lead at most sixteen. The controller is here hypothetically asked to include all of them in its two-layer guard. If G_n becomes empty, any legal continuation is permitted; the construction still kills it.

## Construction from the empty initial state

Let q be the controller's position at time 16 on its bomb-free run with the prescribed reference. This q is known to the Devil before play. Choose two distinct points c,d in N(q), and choose any e in N(c). Put

    A=N(q) minus {c,d},     |A|=7,
    B=N(c) minus {e},       |B|=8.

Schedule the following announcements, each after its round's Angel move:

- Round 1: one point of A, target time 17.
- Rounds 2 through 9: the eight points of B, each with target time 18.
- Rounds 10 through 15: the other six points of A, each with target time 17.
- Round 16: point d, target time 17.
- Round 17: point e, target time 18.

Every announcement is effective and has lead at most sixteen. The maximal leads are 17-1=16 and 18-2=16. There is exactly one announcement per round, and the two target times may be shared by many announced positions, as the original game permits.

## Why the controller follows its bomb-free run through time sixteen

Through move 15, no announced target is at the current or following time. Thus G_n=N(a_(n-1)) for all n<=15, and the controller agrees with its bomb-free run.

At move 16 there is no time-16 bomb, and the known time-17 set is exactly A, with only seven points globally. Consequently every possible next position has at most seven time-17 neighbors in A. Once again G_16=N(a_15), so the controller reaches its known bomb-free position q.

The round-16 announcement changes the time-17 set to N(q) minus {c}. Thus move 17 has exactly one immediately safe choice, c. If the two-layer controller is now undefined because its admissible set is empty, every immediately surviving extension must still choose c.

At c, the eight time-18 bombs are exactly B. The round-17 announcement adds e, completing N(c). Every move at time 18 is therefore bombed by an earlier announcement. The Angel loses at move 18.

## Scope and consequence

This is a legal causal construction from the empty board, not a preloaded-state example. Its prediction of q is valid only for the stated policy class and the fixed known reference: the earlier bombs leave its exact local guard unchanged. A general full-history strategy can react to those same earlier announcements and need not reach q. A secretly randomized reference is also outside the prediction used here.

Thus changing the constants of the accepted two-layer tracker does not extend that same controller from maximum lead fifteen to sixteen. A successful extension must use the distant announcement history before the current/next guard activates, or otherwise change the state and move-selection rule. The unrestricted game remains unresolved.
