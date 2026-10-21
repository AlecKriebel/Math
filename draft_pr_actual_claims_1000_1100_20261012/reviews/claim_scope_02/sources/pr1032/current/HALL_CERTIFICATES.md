# Noninduction Hall certificates

All segments are on the trivial cuspidal line. Write A=[0,2], B=[1,4], C=[3,3], D=[2,5], E=[4,6]. Each row has a ladder side, so LM Proposition 5.20 applies. The indicated vertex belongs to X for the directed LC condition and has no neighbor in Y. A singleton Hall obstruction proves that LC condition false. All 15 unordered nontrivial partitions are listed.

| Partition | Ladder side(s) | Failing LC | Isolated X vertex | Y |
|---|---|---|---|---|
| E / DCBA | E | LC(DCBA, E) | (D, E) | [('D', 'E'), ('B', 'E')] |
| D / ECBA | D | LC(D, ECBA) | (D, E) | [('D', 'E')] |
| C / EDBA | C, EDBA | LC(C, EDBA) | (C, E) | [] |
| B / EDCA | B | LC(B, EDCA) | (B, D) | [('B', 'E'), ('B', 'D')] |
| A / EDCB | A | LC(A, EDCB) | (A, C) | [('A', 'D'), ('A', 'B')] |
| ED / CBA | ED | LC(CBA, ED) | (C, E) | [('B', 'E'), ('B', 'D'), ('A', 'D')] |
| EC / DBA | EC, DBA | LC(DBA, EC) | (D, E) | [('D', 'E'), ('B', 'E')] |
| EB / DCA | EB | LC(EB, DCA) | (B, D) | [('B', 'D')] |
| EA / DCB | EA | LC(EA, DCB) | (A, C) | [('A', 'D'), ('A', 'B')] |
| DC / EBA | EBA | LC(DC, EBA) | (D, E) | [('D', 'E')] |
| DB / ECA | DB, ECA | LC(DB, ECA) | (D, E) | [('D', 'E'), ('B', 'E')] |
| DA / ECB | DA | LC(DA, ECB) | (D, E) | [('D', 'E'), ('A', 'B')] |
| CB / EDA | EDA | LC(CB, EDA) | (C, E) | [('B', 'E'), ('B', 'D')] |
| CA / EDB | CA, EDB | LC(CA, EDB) | (C, E) | [('A', 'D'), ('A', 'B')] |
| BA / EDC | BA | LC(BA, EDC) | (B, D) | [('B', 'E'), ('B', 'D'), ('A', 'D')] |

Here X_(m,n)={(u,v):u in m,v in n,u≺v}; Y_(m,n)={(u,v):u−1≺v}. A Y vertex (u2,v2) can match X vertex (u1,v1) only if u1=u2 and v2≺v1, or v1=v2 and u1≺u2. The shift u−1 subtracts one from both endpoints. The relation [a,b]≺[c,d] means a<c≤b+1 and b<d.

The original matching implementation and this independent set-based checker use different implementations of ≺. Neither program evaluates an invariant-functional space. The certificate proves noninduction only after applying the exact representation-theoretic interfaces described in the proof.
