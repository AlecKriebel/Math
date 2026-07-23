#!/bin/sh
set -eu

destination=${1:-"$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/.tools"}
cadical_commit=c60730422e758ef1cebe7aeddf2dda31c996bf04
drat_trim_commit=2e3b2dc0ecf938addbd779d42877b6ed69d9a985

mkdir -p "$destination"

if [ ! -d "$destination/cadical/.git" ]; then
    git clone https://github.com/arminbiere/cadical.git "$destination/cadical"
fi
git -C "$destination/cadical" fetch --quiet origin "$cadical_commit"
git -C "$destination/cadical" checkout --quiet --detach "$cadical_commit"
(
    cd "$destination/cadical"
    ./configure
    make -j1
)

if [ ! -d "$destination/drat-trim/.git" ]; then
    git clone https://github.com/marijnheule/drat-trim.git "$destination/drat-trim"
fi
git -C "$destination/drat-trim" fetch --quiet origin "$drat_trim_commit"
git -C "$destination/drat-trim" checkout --quiet --detach "$drat_trim_commit"
make -j1 -C "$destination/drat-trim"

test "$(
    git -C "$destination/cadical" rev-parse HEAD
)" = "$cadical_commit"
test "$(
    git -C "$destination/drat-trim" rev-parse HEAD
)" = "$drat_trim_commit"

printf 'cadical=%s\n' "$destination/cadical/build/cadical"
printf 'drat_trim=%s\n' "$destination/drat-trim/drat-trim"
