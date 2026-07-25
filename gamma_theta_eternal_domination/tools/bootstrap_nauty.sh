#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
archive="$script_dir/nauty2_9_3.tar.gz"
source_dir="$script_dir/nauty2_9_3"
url="https://pallini.di.uniroma1.it/nauty2_9_3.tar.gz"
expected="9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b"

if [ ! -f "$archive" ]; then
    curl -fL --retry 3 -o "$archive" "$url"
fi

actual=$(shasum -a 256 "$archive" | awk '{print $1}')
if [ "$actual" != "$expected" ]; then
    echo "nauty archive checksum mismatch" >&2
    exit 1
fi

if [ ! -d "$source_dir" ]; then
    tar -xzf "$archive" -C "$script_dir"
fi

cd "$source_dir"
if [ ! -f makefile ]; then
    ./configure
fi
make -j2 geng showg labelg shortg countg
