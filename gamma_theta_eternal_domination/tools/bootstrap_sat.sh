#!/bin/sh
set -eu

# Install the independent solver and checker used by the proof-producing SAT
# lane. Both source archives are content-pinned. The script deliberately
# refuses to replace an existing source directory.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TOOLS="$ROOT/tools"

CADICAL_COMMIT=c60730422e758ef1cebe7aeddf2dda31c996bf04
CADICAL_ARCHIVE_SHA256=2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e
CADICAL_ARCHIVE="$TOOLS/cadical_3_0_1.tar.gz"
CADICAL_TARGET="$TOOLS/cadical_3_0_1"

DRAT_TRIM_COMMIT=2e5e29cb0019d5cfd547d4208dca1b3ec290349f
DRAT_TRIM_ARCHIVE_SHA256=2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108
DRAT_TRIM_ARCHIVE="$TOOLS/drat_trim_2023_05_22.tar.gz"
DRAT_TRIM_TARGET="$TOOLS/drat_trim_2023_05_22"

sha256_file() {
  shasum -a 256 "$1" | awk '{print $1}'
}

fetch_and_check() {
  url=$1
  destination=$2
  expected=$3
  if [ ! -f "$destination" ]; then
    curl -L --fail --silent --show-error "$url" -o "$destination"
  fi
  actual=$(sha256_file "$destination")
  if [ "$actual" != "$expected" ]; then
    echo "SHA-256 mismatch for $destination" >&2
    echo "expected $expected" >&2
    echo "actual   $actual" >&2
    exit 1
  fi
}

install_archive() {
  archive=$1
  source_name=$2
  target=$3
  if [ -e "$target" ]; then
    echo "Refusing to replace existing $target" >&2
    exit 1
  fi
  temporary=$(mktemp -d "${TMPDIR:-/tmp}/gamma-theta-sat.XXXXXX")
  trap 'rm -rf "$temporary"' EXIT HUP INT TERM
  tar -xzf "$archive" -C "$temporary"
  mv "$temporary/$source_name" "$target"
  trap - EXIT HUP INT TERM
  rmdir "$temporary"
}

mkdir -p "$TOOLS"

if [ ! -x "$CADICAL_TARGET/build/cadical" ]; then
  fetch_and_check \
    "https://codeload.github.com/arminbiere/cadical/tar.gz/$CADICAL_COMMIT" \
    "$CADICAL_ARCHIVE" "$CADICAL_ARCHIVE_SHA256"
  install_archive "$CADICAL_ARCHIVE" \
    "cadical-$CADICAL_COMMIT" "$CADICAL_TARGET"
  (
    cd "$CADICAL_TARGET"
    ./configure
    make -j2
  )
fi

if [ ! -x "$DRAT_TRIM_TARGET/drat-trim" ]; then
  fetch_and_check \
    "https://codeload.github.com/marijnheule/drat-trim/tar.gz/$DRAT_TRIM_COMMIT" \
    "$DRAT_TRIM_ARCHIVE" "$DRAT_TRIM_ARCHIVE_SHA256"
  install_archive "$DRAT_TRIM_ARCHIVE" \
    "drat-trim-$DRAT_TRIM_COMMIT" "$DRAT_TRIM_TARGET"
  (
    cd "$DRAT_TRIM_TARGET"
    make -j2
  )
fi

"$CADICAL_TARGET/build/cadical" --version
"$DRAT_TRIM_TARGET/drat-trim" 2>&1 | sed -n '1p'
sha256_file "$CADICAL_TARGET/build/cadical"
sha256_file "$DRAT_TRIM_TARGET/drat-trim"
