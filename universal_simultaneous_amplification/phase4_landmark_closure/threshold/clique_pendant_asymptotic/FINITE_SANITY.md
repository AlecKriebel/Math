# Finite-chain sanity check

This table is not part of the asymptotic proof. It was produced by exact
rational solution of every transient equation in the previously audited
`clique_pendant_product_audit` quotient solver. The displayed decimals are
only readable renderings of exact fractions.

The singleton columns are ordered `(hub, ordinary clique vertex, leaf)`.

| `m` | Bd average | Bd normalized | Bd singleton values | dB average | dB normalized | dB singleton values |
|---:|---:|---:|---|---:|---:|---|
| 1 | .341099813 | 1.005553860 | (.210043597, .299328856, .806323684) | .283635296 | .920857636 | (.335904642, .306117984, .051504445) |
| 2 | .357308467 | 1.071441863 | (.155410519, .309554879, .840286144) | .284767407 | .901153285 | (.343278765, .313285025, .027370784) |
| 3 | .367870670 | 1.103599062 | (.123835101, .316895721, .857015459) | .288255171 | .896778080 | (.349730967, .319368767, .018854464) |
| 4 | .373151151 | 1.119453112 | (.102508104, .320139597, .864904349) | .290215591 | .894830997 | (.353284857, .322723019, .014388853) |

A separate sparse solve, used only as a conditioning and trend check, gave:

| `m` | Bd hub | Bd ordinary | Bd leaf | dB hub | dB ordinary | dB leaf |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | .0605784 | .3256473 | .8766634 | .3587896 | .3279319 | .00738883 |
| 20 | .0272020 | .3299091 | .8839269 | .3621801 | .3311491 | .00300410 |
| 50 | .0114430 | .3318986 | .8868911 | .3635550 | .3324558 | .00120958 |

These trends agree with the derived singleton limits `1/3,8/9,0`. No sign
or limit in the theorem is inferred from this table.

