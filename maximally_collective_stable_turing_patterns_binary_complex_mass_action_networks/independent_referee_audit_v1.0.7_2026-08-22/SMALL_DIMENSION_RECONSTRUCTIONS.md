# Small-dimensional reconstructions from the reaction list

Species are ordered `X_1,...,X_m,Z`; reactions retain the manuscript order. These matrices were constructed from source/target complexes without submitted code.

## `m=3`

The chain range is empty. With columns `R_0,R_a,R_b,R_+,R_-`,

```text
Y = [[0,1,0,0,1],
     [0,1,0,0,0],
     [0,0,2,0,1],
     [0,0,0,2,0]]

Gamma = [[1,-1, 0, 1,-1],
         [0,-1, 1, 0, 0],
         [0, 2,-2, 1,-1],
         [0, 0, 0,-2, 2]]

A_3(a,b) = [[-(a+b), -a,       -b,       2b],
            [-a,      -a,       2a,       0 ],
            [2a-b,     2a,     -(4a+b),   2b],
            [2b,       0,       2b,      -4b]]
```

Direct row reduction gives rank three and kernel basis `(1,1,1,0,0)` and `(0,0,0,1,1)` in reaction coordinates. The left conservation vector is `(0,4,2,1)` and the homogeneous right kernel vector of `A_3` is `(2,-2,0,1)`.

The two order-two long cycles are `{X_1,X_2}` and `{X_2,X_3}`. Every other nonsingleton SCC on fewer than three vertices lies inside `{X_1,X_3,Z}`; this remains true when `b=2a` deletes `X_1 -> X_3`.

## `m=4`

With columns `R_0,R_2,R_a,R_b,R_+,R_-`,

```text
Y = [[0,1,1,0,0,1],
     [0,1,0,0,0,0],
     [0,0,1,0,0,0],
     [0,0,0,2,0,1],
     [0,0,0,0,2,0]]

Gamma = [[1, 0,-1, 0, 1,-1],
         [0,-1, 0, 1, 0, 0],
         [0, 1,-1, 0, 0, 0],
         [0, 0, 2,-2, 1,-1],
         [0, 0, 0, 0,-2, 2]]

A_4(a,b) = [[-(a+b), 0,  -a,       -b,       2b],
            [-a,     -a,  0,        2a,       0 ],
            [0,       a, -a,        0,        0 ],
            [2a-b,    0,  2a,      -(4a+b),   2b],
            [2b,      0,  0,        2b,      -4b]]
```

Direct row reduction gives rank four, left conservation `(0,4,4,2,1)`, and homogeneous right kernel `(2,-2,-2,0,1)`.

## Omission table check

For both dimensions, and subsequently for `m=5,6,7`, exact determinant expansion after a nontrivial positive rational right scaling `H` gives:

```text
omit Z:       (-1)^m det J_hatZ       = -2 a^(m-1) b product_{i=1}^m h_i
omit X_j:     (-1)^m det J_hatXj      = 16 a^(m-1) b h_Z product_{i != j} h_i,
                                           2 <= j <= m-1
omit X_1,X_m:                            0
```

The `m=3` computation explicitly includes the exceptional zero-length chain; the `m=4` computation includes the shortest nonempty chain.
