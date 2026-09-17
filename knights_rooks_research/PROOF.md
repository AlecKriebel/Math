# Boundary obstruction: nonexistence for N=4, R=2

## Stronger statement
There is no finite nonempty set of knights and finite nonempty set of rooks on
integer squares such that every knight attacks at least four rooks and every
rook sees exactly two knights and no rooks. Knight-knight attacks are allowed
in this stronger statement. Thus it implies nonexistence for the requested
case with exactly four rook targets and no knight targets.

## Proof
Assume such a placement exists. Every rook has x-coordinate between the
minimum and maximum knight x-coordinates: a rook strictly to the right of
all knights could see a knight only in its west ray, and so at most one.
The left-hand statement follows likewise. Translate a rightmost knight to
A=(0,0). Every square with x>0 is empty.

A has only four possible rook targets, so all of
U=(-2,1), V=(-1,2), W=(-1,-2), Z=(-2,-1)
are rooks. U and Z must be separated by a knight, forcing C=(-2,0).
Likewise V and W require a knight at at least one of
B+=(-1,1), B0=(-1,0), B-=(-1,-1).

B0 cannot be a knight: two of its eight knight-move destinations have x>0,
and each of the other six is immediately horizontally adjacent to one of
U,V,W,Z and so cannot be a rook. A knight at B0 would attack zero rooks.
Reflect in y=0 if necessary so that B+ is a knight.

U already sees C immediately south and B+ immediately east. Because it
sees exactly two occupied rays, its north and west rays must be completely
empty. In particular (-2,2) and (-2,3) are empty. The square (-3,2) cannot
be a rook either, since V=(-1,2) would be visible to it across empty
(-2,2).

Of the eight knight-move destinations of B+, only the following four can
therefore be rooks:
(-3,0), (-2,-1), (0,-1), (0,3).
Two other destinations have x>0, and the remaining two were excluded
above. All four listed squares must be rooks. In particular X=(0,-1)
is a rook. Z and X force a knight at their only intervening square B-.

Z now sees C immediately north and B- immediately east, so its south ray
is empty; in particular (-2,-2) and (-2,-3) are empty. Hence (-3,-2)
cannot be a rook, since it would see W=(-1,-2) across empty (-2,-2).
Also X sees A immediately north and B- immediately west, so its south
ray is empty; in particular (0,-3) is empty.

Now inspect the eight knight-move destinations of B-:
(-3,-2), (-3,0), (-2,-3), (-2,1),
(0,-3), (0,1), (1,-2), (1,0).
The last two have x>0, and (-3,-2), (-2,-3), (0,-3) have just been
excluded. At most three rook targets remain, contradicting the assumed
lower bound of four. QED.

No condition on board dimensions, piece inventory, reachability, checkerboard
color, or knight-knight attacks entered this argument. The only symmetry
operation was reflection after a proved two-case alternative.
