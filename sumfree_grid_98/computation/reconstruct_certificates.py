#!/usr/bin/env python3
"""Reconstruct the unchanged d=3, N=5 gzip certificate from ASCII transport parts.

Uses only Python's standard library. Missing, extra, or modified parts fail before
any output is written. Decoded size and SHA-256 are checked before an atomic write.
An already-correct output is retained; an incorrect existing output is rejected.
All paths are relative to this script, independently of the working directory.
"""
from pathlib import Path
import base64
import binascii
import hashlib
import json
import os
import sys
import tempfile

OUTPUT_NAME = "finite_certificate_d3_n5.json.gz"
EXPECTED_BYTES = 1146536
EXPECTED_SHA256 = "25835b71af17eb7eab18d817b1f65d9aceb380d169a7b5ab317ee82388a4c716"
MAX_PART_BYTES = 32768
# Each entry authenticates the exact ASCII file, including its final newline.
PARTS = (
    ('finite_certificate_d3_n5.json.gz.part001.b64', 32765, '34e1dcd1a2c988328c995c693c0a71dab90ff8c964ed39d735276b90492834f7'),
    ('finite_certificate_d3_n5.json.gz.part002.b64', 32765, 'c36149584b03bb0115ea31c28f503ea8861490382b1582c39469a8cfc709b7bb'),
    ('finite_certificate_d3_n5.json.gz.part003.b64', 32765, 'a772aabd61d9b626772964702af22f795a9109d395ba0ce5ea277ca4dc801bbe'),
    ('finite_certificate_d3_n5.json.gz.part004.b64', 32765, 'f4ec2958a66ea29338e03711729c6d5b0feb22f0acf994717bdccb30477c8276'),
    ('finite_certificate_d3_n5.json.gz.part005.b64', 32765, '430130511e60edb741ebb6855ad8c0e97079cc14d728ec5df5c7789bbccf3275'),
    ('finite_certificate_d3_n5.json.gz.part006.b64', 32765, 'f0976e0fcac722e064adbb19f4e4517112e0e961e154f160b0f793b7871e9661'),
    ('finite_certificate_d3_n5.json.gz.part007.b64', 32765, 'ea1b045fbe10c25adad415089c008ff5cf5741b66881143a0a0f3c1559f19f38'),
    ('finite_certificate_d3_n5.json.gz.part008.b64', 32765, '691a586ff13160205ca797602615e89c48614f4b68f47bcd77e6112bf3103273'),
    ('finite_certificate_d3_n5.json.gz.part009.b64', 32765, '08520e620c9e044e46c422eb40fbf48361ff7c759d2d2948f3a4ad7b85262c2b'),
    ('finite_certificate_d3_n5.json.gz.part010.b64', 32765, 'e87048923c52f6e88b8a14db81c0a40b9790773da7e0cde71f4e2f457941dee8'),
    ('finite_certificate_d3_n5.json.gz.part011.b64', 32765, 'a85a58d2d5c673d4dd6cbf2654c68515b62868caf9afadca770bc77b3ebf4989'),
    ('finite_certificate_d3_n5.json.gz.part012.b64', 32765, 'b78cfaa9e30dfa311b55c7cef97c8dcdd19e0e4c60812e7905ce0031d72a6e78'),
    ('finite_certificate_d3_n5.json.gz.part013.b64', 32765, '7381733a40e4a10137010670ff8aac8b9e8b5a7b86cffbc9dadb89b55cb1dc84'),
    ('finite_certificate_d3_n5.json.gz.part014.b64', 32765, 'b2dcbc31e133107515217573ce8562b1e4186068a7c2d5c134a79a44f16aecf6'),
    ('finite_certificate_d3_n5.json.gz.part015.b64', 32765, 'd9d99fe3c62aad22e01c2d3d1dc439573aef42820efb70147d80151fa21a6478'),
    ('finite_certificate_d3_n5.json.gz.part016.b64', 32765, '16cfbbd59b2f75210c355a79a95e042d27e9d64f4d2c4d73b929c0aeaa163131'),
    ('finite_certificate_d3_n5.json.gz.part017.b64', 32765, '043e7d0890548d2185573bfea1bf779bfd73159f57ae04f51c2769d60c9656d9'),
    ('finite_certificate_d3_n5.json.gz.part018.b64', 32765, 'ec356530e03c6b3ea4f73cfd9d33b59d5c25414114230826e4a96c1772e16696'),
    ('finite_certificate_d3_n5.json.gz.part019.b64', 32765, '4df6ae015f04306255c7db60897a713ba76417aaad384066fcc83b48ae972c87'),
    ('finite_certificate_d3_n5.json.gz.part020.b64', 32765, 'dcd2481e8ab9199326c12ab6f4338118b1366861e3e169ea892b318fa0201207'),
    ('finite_certificate_d3_n5.json.gz.part021.b64', 32765, 'cf678accb72ba7bcfc58579d63b6494c96f8d5d9d1c59087ced37a510b0f4e4c'),
    ('finite_certificate_d3_n5.json.gz.part022.b64', 32765, 'e08593a319580337fbea1fa02ca4554a83bbe11b746e0050b1fe65ac027d9613'),
    ('finite_certificate_d3_n5.json.gz.part023.b64', 32765, '0a024ad9bef870cb84e34b64c9e3d7b1d10770c4a4bb6dc5b7496eee2dde4e2a'),
    ('finite_certificate_d3_n5.json.gz.part024.b64', 32765, '79332411f92bd0c5c865098a4b8fd931ae2415d3bdf0d84b079d8beadda7eb79'),
    ('finite_certificate_d3_n5.json.gz.part025.b64', 32765, '615037fb6e6edeb511200d08245a7028baa419962f752ed5ea13d02bf6a9ff46'),
    ('finite_certificate_d3_n5.json.gz.part026.b64', 32765, 'ed883ccc14ecd1cc7e01247fc26fefb3dfba683600c5bfce7d141780cf7d482c'),
    ('finite_certificate_d3_n5.json.gz.part027.b64', 32765, '401f5e85dd721648dd43b2858f4bc82a45657fd3f131df91de81534609213d79'),
    ('finite_certificate_d3_n5.json.gz.part028.b64', 32765, 'b5c7d1d955d4b7815b4772ceb9d4d7977e1146f9b4ea4e093de48b211244dbc3'),
    ('finite_certificate_d3_n5.json.gz.part029.b64', 32765, 'd1242d783779597c7905a139b283775dab4c51b6ee73c42ecb3684091b24ba98'),
    ('finite_certificate_d3_n5.json.gz.part030.b64', 32765, '1e072bebeca42590aea0fb10dcf229c142adb69fb44ba32c6b492b23344e7c89'),
    ('finite_certificate_d3_n5.json.gz.part031.b64', 32765, 'c747b646703a5e980ae3bf3f40dbb16e72edd4fc89d235c0e358536155013ad9'),
    ('finite_certificate_d3_n5.json.gz.part032.b64', 32765, 'da317f8af9717c3c4d3c596a1de50bfd4697cdec04eabadb1c66b3b5f3cb436e'),
    ('finite_certificate_d3_n5.json.gz.part033.b64', 32765, 'b13ca78e0f1886cd41cefa07011952766b4bd989fbad5a3ab675d1b70c3bdb6d'),
    ('finite_certificate_d3_n5.json.gz.part034.b64', 32765, '8242d9eed4a688b6afe1e082c6db8fbef5b08f622331b88e1191f8f22dd89941'),
    ('finite_certificate_d3_n5.json.gz.part035.b64', 32765, '469ceb5e54d7fc7f67167f70c49cb8c77a925d8ea542582cffa7c72d64d82b36'),
    ('finite_certificate_d3_n5.json.gz.part036.b64', 32765, '2ef99d70242d968f787f3e5ed0386d1dd2f7c8850c44fe7ee94698a2bfa4fd78'),
    ('finite_certificate_d3_n5.json.gz.part037.b64', 32765, '630f8ca7bf589d2b4eb29db48425397b9da35ffd7725c7b9c9ec1c6968a1d464'),
    ('finite_certificate_d3_n5.json.gz.part038.b64', 32765, '68f789066166d74c1d0d09f2fd4d52964f743487edb6cc1ea8f2c2a029996717'),
    ('finite_certificate_d3_n5.json.gz.part039.b64', 32765, 'dffa3e2728a3a6c1e298f72b87fee8f5cb8c5a1e2ac434ea4d0c17dc786dc9e0'),
    ('finite_certificate_d3_n5.json.gz.part040.b64', 32765, '12e731625071d278148600276a196a64ab818617fe737f63a9f2961623a90453'),
    ('finite_certificate_d3_n5.json.gz.part041.b64', 32765, 'a5d6e099151177820ac4a825d6984050671b459437a5faf245ab239fd3ac8789'),
    ('finite_certificate_d3_n5.json.gz.part042.b64', 32765, 'e3aa72cd6ad3d39954dff678995348f07dc489dabab2fec7457bb42c25bc7c03'),
    ('finite_certificate_d3_n5.json.gz.part043.b64', 32765, 'ab937212b071119b6309b01c79ea85a59487762efed0d6cfea6f6b45872e5d14'),
    ('finite_certificate_d3_n5.json.gz.part044.b64', 32765, '296f212c8ed1dabcb31a53f50cd52c19c97d3b9e9eea17e72ed5b82401876aa5'),
    ('finite_certificate_d3_n5.json.gz.part045.b64', 32765, 'b664de9d76d09fd13b4f959ac99e52fe18048097f1d8c31542cd9db13eb3bbed'),
    ('finite_certificate_d3_n5.json.gz.part046.b64', 32765, '6c928db318f80670d2bbcebce40c0b8405fdc0c55f65c17a86f5bff5331d81a6'),
    ('finite_certificate_d3_n5.json.gz.part047.b64', 21573, '9e500989b4bfdb3294b945668cb928e48824290bca1a82f0b7e8bbad40d25b65'),
    )


def need(condition, message):
    if not condition:
        raise ValueError(message)


def reconstruct():
    here = Path(__file__).resolve().parent
    part_dir = here / "certificate_parts"
    need(part_dir.is_dir(), "missing certificate_parts directory")
    expected_names = {entry[0] for entry in PARTS}
    actual_names = {entry.name for entry in part_dir.iterdir()}
    need(actual_names == expected_names, "missing or unexpected certificate part")
    decoded = []
    for filename, expected_size, expected_sha256 in PARTS:
        part = part_dir / filename
        need(part.is_file() and not part.is_symlink(), "invalid part: " + filename)
        need(part.stat().st_size == expected_size <= MAX_PART_BYTES,
             "incorrect part size: " + filename)
        content = part.read_bytes()
        need(len(content) == expected_size, "changed part size: " + filename)
        need(hashlib.sha256(content).hexdigest() == expected_sha256,
             "incorrect part SHA-256: " + filename)
        need(content.endswith(b"\n") and b"\n" not in content[:-1],
             "invalid part newline: " + filename)
        decoded.append(base64.b64decode(content[:-1], validate=True))
    data = b"".join(decoded)
    need(len(data) == EXPECTED_BYTES, "incorrect reconstructed byte count")
    need(hashlib.sha256(data).hexdigest() == EXPECTED_SHA256,
         "incorrect reconstructed SHA-256")
    output = here / OUTPUT_NAME
    need(not output.is_symlink(), "refusing an output symlink")
    if output.exists():
        need(output.is_file(), "output exists but is not a regular file")
        need(output.read_bytes() == data,
             "existing output differs; use a clean disposable package copy")
        status = "already_verified"
    else:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode="wb", dir=here, prefix=".reconstruct-", delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, output)
            temporary = None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        status = "reconstructed"
    return {"file": OUTPUT_NAME, "bytes": EXPECTED_BYTES,
            "sha256": EXPECTED_SHA256, "parts": len(PARTS), "status": status}


def main():
    try:
        result = reconstruct()
    except (OSError, ValueError, binascii.Error) as error:
        print("Certificate reconstruction failed: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
