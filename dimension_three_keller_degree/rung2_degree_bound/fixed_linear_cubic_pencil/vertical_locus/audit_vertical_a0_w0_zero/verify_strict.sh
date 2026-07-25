#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
parent_dir="$script_dir/.."
scratch=$(mktemp -d "${TMPDIR:-/tmp}/audit-a0-w0-zero.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

check_hash() {
    expected=$1
    file=$2
    actual=$(shasum -a 256 "$file" | awk '{print $1}')
    if [ "$actual" != "$expected" ]; then
        echo "FAIL: hash mismatch for $file" >&2
        echo "expected $expected" >&2
        echo "actual   $actual" >&2
        exit 1
    fi
}

check_hash d1f0889a54d9185a4f899d7ca6f5eb702a040a8cfdcb1733a4427896940eb09c \
    "$parent_dir/VERTICAL_A0_W0_ZERO_EXCLUSION.md"
check_hash 94961709c9bfbff7dd4fe0e4ce2d7283bcf958a9d52cc773dcd28c7edeec7566 \
    "$parent_dir/verify_vertical_a0_w0zero_sympy.py"
check_hash c57e44c44fb40cdd9557beec93e3594644360552115398bf4372684626391ed4 \
    "$parent_dir/verify_vertical_a0_w0zero_strict.sh"
check_hash 8523035eb97b20ce28c20e96d8b9946888bfd013bf4ab46eca429add26f979fb \
    "$parent_dir/VERTICAL_SZERO_W0_EXCLUSION.md"
check_hash e0ee3089f7e3155acc9497dbe4c0660637a3c2d84b863a0fd8f69f7a5cbd8c73 \
    "$parent_dir/verify_vertical_szero_w0_sympy.py"
check_hash b6eede6838de62051d07283d0fba3f52e2a27edc1c5ff597823dbd5b57c9a92e \
    "$parent_dir/verify_vertical_szero_w0_pari.gp"
check_hash 231d9e8284c94ac3bc12129cb4d9857244ecaa90fbf77061921f89496f7a06c3 \
    "$parent_dir/verify_vertical_szero_w0_strict.sh"

if ! "$parent_dir/verify_vertical_a0_w0zero_strict.sh" \
    >"$scratch/candidate.log" 2>&1
then
    cat "$scratch/candidate.log"
    exit 1
fi
cat "$scratch/candidate.log"
if ! tail -n 1 "$scratch/candidate.log" |
    grep -Fqx 'VERTICAL_A0_W0_ZERO_STRICT_PASS_91D42B'
then
    echo "FAIL: candidate strict sentinel missing" >&2
    exit 1
fi

if ! /bin/sh "$parent_dir/verify_vertical_szero_w0_strict.sh" \
    >"$scratch/independent.log" 2>&1
then
    cat "$scratch/independent.log"
    exit 1
fi
cat "$scratch/independent.log"
if ! grep -Fqx \
    'PASS: s=0, W0=0 vertical companion excluded on 2 nontriple + 3 minimal triple-root charts' \
    "$scratch/independent.log"
then
    echo "FAIL: independent SymPy sentinel missing" >&2
    exit 1
fi
if ! grep -Fqx 'VERTICAL_SZERO_W0_PARI_PASS_C5E4A2' \
    "$scratch/independent.log"
then
    echo "FAIL: independent PARI/GP sentinel missing" >&2
    exit 1
fi

echo 'VERTICAL_A0_W0_ZERO_AUDIT_PASS_90A7DC'
