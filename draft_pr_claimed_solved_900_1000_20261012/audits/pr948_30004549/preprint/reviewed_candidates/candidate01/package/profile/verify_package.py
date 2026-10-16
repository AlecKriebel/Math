#!/usr/bin/env python3
"""Strict finite-file profile for PR948; run with Python -I -S -B.

An externally obtained manifest SHA256 is required. This is neither a digital
signature, an OS sandbox, nor a mathematical/priority certificate.
"""
import sys
if not (sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode):
    raise SystemExit("PROFILE_STARTUP: invoke Python with -I -S -B before loading this module")

import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import threading
import time
import zipfile

HEAD = "be4313efafa1af5962394e07d8a4debff2e94d92"
PREFIX = "original/unsolved_math_prioritization/attempts/30004549/"
MANIFEST = "PACKAGE_MANIFEST.json"
SCHEMA = "pr948-sourcefree-package-v1"
MAX_FILES, MAX_DIRS, MAX_DEPTH = 512, 128, 12
MAX_FILE_BYTES, MAX_TOTAL_BYTES, MAX_MANIFEST_BYTES = 8*1024**2, 32*1024**2, 128*1024
MAX_ZIP_MEMBERS, MAX_ZIP_RATIO = 512, 200
CHILD_SECONDS, CHILD_STDOUT_BYTES, CHILD_STDERR_BYTES = 60, 64*1024, 16*1024
MAX_SOURCE_BYTES = 16*1024
HEX64, HEX40 = re.compile(r"[0-9a-f]{64}\Z"), re.compile(r"[0-9a-f]{40}\Z")
# Generated ONLY from the independently authenticated immutable original24.
ORIGINAL_PINS = {'ANTI_INVARIANT_30004549_R3_AUTHOR_EXTERNAL_MANIFEST.json': {'bytes': 1483, 'sha256': '23b49259d2a3e8938f940323ec69a7cc17737cb4a0636817c6ae238609ffceb4', 'git_blob': '18b4e390c13e0c59561c3990b6d4b0089e6c0245', 'git_mode': '100644'}, 'ANTI_INVARIANT_30004549_R3_AUTHOR_PUBLICATION_PACKET.zip': {'bytes': 10680, 'sha256': '1ba558617ecbd40e4117da22897137118568204852b009bb2c02c99ef2521fc4', 'git_blob': '1bbdd7ac2d8de9fc26328eb4e7118af3642ab419', 'git_mode': '100644'}, 'PUBLIC_MANIFEST.json': {'bytes': 5639, 'sha256': '18b022a9f45f4b8194629cae8143f6be4884dbba51b7616cc64c1b7ab2cf7117', 'git_blob': '88b5721f626219ba2792d412696d7e2715b8f5d6', 'git_mode': '100644'}, 'PUBLIC_MANIFEST.sha256': {'bytes': 87, 'sha256': 'eb7c5ed0405944e90b937fb112dd5904ae3db07559af779f7b36bfc5a878d6c6', 'git_blob': '45bad253db481f6dbd5ff8e42758f28ea7009566', 'git_mode': '100644'}, 'README.md': {'bytes': 5096, 'sha256': '4b481f7ab77c2c4f9f3b79d25db0490db3637c81c66051910698db083f4135fe', 'git_blob': '56f3e706bdf77bcd85e174a2365fd422bdde20fe', 'git_mode': '100644'}, 'RESEARCH_LOG.md': {'bytes': 1480, 'sha256': '58a5dde3e1e07a1ec18d291745e2f86154be634cd438dade215a279f3dcecf34', 'git_blob': '6ef39d3ca088ef63ac26840f2014b4868c52b65a', 'git_mode': '100644'}, 'VERIFICATION_RESULTS.json': {'bytes': 3091, 'sha256': 'ddf1aeb2d60ddc798cd16c2637e6f38057f1ca287e3a5d3ef1c15f297a413e57', 'git_blob': '07a0e7ea87888a25c40be210433b112951766ccf', 'git_mode': '100644'}, 'audit_a/ALGEBRA_CHECK_OUTPUT.txt': {'bytes': 249, 'sha256': '762672096dd076376c2a5904d174e31a612407a252004283c6f5a740ea495cab', 'git_blob': '94e10b77a531eca51386deaf3647673c038ca0ee', 'git_mode': '100644'}, 'audit_a/AUDIT_MANIFEST.json': {'bytes': 835, 'sha256': '63c3515b28199b8f3fbbb791de9c20ffec01aefccd81797afffe649b4e05c66b', 'git_blob': '3c1cbc0476b095b973e4196591aba361d61dd0d9', 'git_mode': '100644'}, 'audit_a/INDEPENDENT_ACCEPTANCE_A.md': {'bytes': 10890, 'sha256': 'a4e8a88320d30cafe7fe5c95fa95f97fab999baa5dba1241c3e7919fb6b20988', 'git_blob': '4eb09c3baadc58a649bfb68ff29cc7c6fb34f811', 'git_mode': '100644'}, 'audit_a/check_algebra.py': {'bytes': 2310, 'sha256': 'ebffbe69e7076fadd8393d18dc36cad45e3458fceb7e700a6b30613bba04bfae', 'git_blob': '8fe0c6421b6eb9cdd8d32d813426621e9e114c45', 'git_mode': '100644'}, 'audit_b/AUDIT_MANIFEST.json': {'bytes': 2192, 'sha256': '8cb0e0288d3e2fdf6db124e979bc9f46c3e1ae626125afecb6ef620e78833327', 'git_blob': 'd6137f2770054de69c27d7f1cc2fc6e0aabdc44d', 'git_mode': '100644'}, 'audit_b/INDEPENDENT_ACCEPTANCE_REPORT.md': {'bytes': 12527, 'sha256': '05a1a99f0c825be6a623b0ad827008fb68a442f38f7908593bdef6ce4c612568', 'git_blob': 'f221ff761d2d5f147a7e66786b345641b47e31cb', 'git_mode': '100644'}, 'audit_b/check_local_algebra.py': {'bytes': 2196, 'sha256': '6e22fc8b0e9779869bf53cfdd861c76da5971c9360549acae60e3a3b99314606', 'git_blob': 'e4174df9432e748b0c2d8c79b5ca29614c1bcf1e', 'git_mode': '100644'}, 'audit_b/check_local_algebra_result.txt': {'bytes': 178, 'sha256': '17e391dd9e29b232a121094555127edd480a3d53185d6b6b0070932a31465837', 'git_blob': '0b5bbe3dcd39a2be9b119583d4552cf67ad236ee', 'git_mode': '100644'}, 'author/MANIFEST.json': {'bytes': 1233, 'sha256': '253e60cd7253ea548911c20fba6b91347fe0fe5ecd3d4fee0b027af3af7fbeaf', 'git_blob': '89d14b038766a2ff2003780b44a08877ccc03af5', 'git_mode': '100644'}, 'author/PUBLIC_SCOPE_CREDIT.md': {'bytes': 3343, 'sha256': 'f0aaddfa71af4f165e7e3176d72b8dc843ff8e14cd345cec4be57a138ab3b2da', 'git_blob': '30f13f1776c93d1630dccb5c10bc3ef3160bccf9', 'git_mode': '100644'}, 'author/R3_counterexample_candidate.md': {'bytes': 9997, 'sha256': '50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e', 'git_blob': '40c1d695e3a02ac9eccaceb81466abd61968f70e', 'git_mode': '100644'}, 'author/verification/check_deformation.py': {'bytes': 3388, 'sha256': '60734845e8d775eb97483099a2ada584af9f94e5f16d0bb5838c36553637910e', 'git_blob': '440734800e3a5e85e0b5e08b1a97b67aa86151cf', 'git_mode': '100644'}, 'author/verification/check_normal.json': {'bytes': 602, 'sha256': '36f781d5c0d0b95f3a428fa5e4cf0aef4eeeafd6db3f0c20ed7c35fbf031f21b', 'git_blob': '37ad44cf04fb0f071ae300e0a02a64a3b26d7de2', 'git_mode': '100644'}, 'author/verification/check_optimized.json': {'bytes': 602, 'sha256': '36f781d5c0d0b95f3a428fa5e4cf0aef4eeeafd6db3f0c20ed7c35fbf031f21b', 'git_blob': '37ad44cf04fb0f071ae300e0a02a64a3b26d7de2', 'git_mode': '100644'}, 'author/verification/source_verification_metadata.json': {'bytes': 2419, 'sha256': '84e9e428d7ac037d289d6ce07fea0d8dfd03c1ca28b5a8075bb041c9df1ea57c', 'git_blob': '04ce468b84d87035be7062374289425fb5df6658', 'git_mode': '100644'}, 'requirements.txt': {'bytes': 14, 'sha256': '25f9f1fb1988b230147a1d3092d34e09c069eb7a6c6d6df46b3973b9f2d36efc', 'git_blob': '1ca5fd06160543f8bd736f1b51db6f42372c66f4', 'git_mode': '100644'}, 'verify_publication.py': {'bytes': 11362, 'sha256': '994408c8bfb602939d03a8ed674f0aa06eed1e80477a473c17ddc8566e49aea5', 'git_blob': 'a2433ff3440560242c6c1120fbdcb35b8ef2afdd', 'git_mode': '100644'}}
ARCHIVE = "ANTI_INVARIANT_30004549_R3_AUTHOR_PUBLICATION_PACKET.zip"
EXTERNAL = "ANTI_INVARIANT_30004549_R3_AUTHOR_EXTERNAL_MANIFEST.json"
CHECKERS = (
    ("author/verification/check_deformation.py", "author/verification/check_normal.json"),
    ("audit_a/check_algebra.py", "audit_a/ALGEBRA_CHECK_OUTPUT.txt"),
    ("audit_b/check_local_algebra.py", "audit_b/check_local_algebra_result.txt"),
)

class ProfileError(ValueError):
    pass

def need(ok, message):
    if not ok:
        raise ProfileError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def exact_int(value, minimum=0, maximum=MAX_TOTAL_BYTES):
    return type(value) is int and minimum <= value <= maximum

def keys(value, expected, label):
    need(type(value) is dict and set(value) == set(expected), "schema keys: " + label)

def canonical_path(value):
    need(type(value) is str and 0 < len(value) <= 512 and value not in (".",".."), "path scalar/length")
    need(re.fullmatch(r"[A-Za-z0-9_./-]+", value) is not None, "path characters")
    p = PurePosixPath(value)
    need(not p.is_absolute() and str(p) == value and len(p.parts) <= MAX_DEPTH, "path canonical/depth")
    reserved = {"CON", "PRN", "AUX", "NUL"} | {f"{s}{i}" for s in ("COM", "LPT") for i in range(1,10)}
    for part in p.parts:
        need(part not in (".", "..") and len(part) <= 255 and not part.endswith("."), "path component")
        need(part.split(".")[0].upper() not in reserved, "reserved portable path")
    return value

def load_json(data, label):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, "duplicate JSON key: " + label)
            out[k] = v
        return out
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(ProfileError("nonfinite JSON number")))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as e:
        raise ProfileError("invalid JSON: " + label) from e

def root_without_links(value):
    need(type(value) is str and value != "", "root path")
    need(".." not in Path(value).parts, "root parent traversal")
    root = Path(os.path.abspath(value))
    chain = list(reversed(root.parents)) + [root]
    for item in chain:
        st = item.lstat()
        need(stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode), "root/ancestor is not a real directory")
    return root

def validate_namespace(files, directories=()):
    """Check the combined namespace, including all implied ancestor names."""
    files, directories = set(files), set(directories)
    for name in files | set(directories):
        canonical_path(name)
        directories.update(p.as_posix() for p in PurePosixPath(name).parents if p.as_posix()!=".")
    need(not files.intersection(directories),"file used as ancestor/directory")
    folded = {}
    for name in sorted(files | directories):
        key = name.casefold()
        need(key not in folded or folded[key]==name,"case-alias file/directory namespace")
        folded[key] = name

def scan_tree(value):
    """Reject unsupported objects and enforce bounds BEFORE any payload read."""
    root = root_without_links(value)
    files, directories, pending, total = {}, set(), [(root, "")], 0
    while pending:
        folder, prefix = pending.pop()
        with os.scandir(folder) as entries:
            for entry in entries:
                rel = canonical_path(prefix + entry.name)
                st = entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(st.st_mode):
                    need(len(directories) < MAX_DIRS, "directory count cap")
                    directories.add(rel)
                    pending.append((root / rel, rel + "/"))
                else:
                    need(stat.S_ISREG(st.st_mode), "nonregular object: " + rel)
                    need(stat.S_IMODE(st.st_mode) == 0o644, "disk mode must be 0644: " + rel)
                    need(st.st_nlink == 1, "hard-linked payload: " + rel)
                    need(exact_int(st.st_size, maximum=MAX_FILE_BYTES), "per-file size cap: " + rel)
                    need(len(files) < MAX_FILES, "file count cap")
                    total += st.st_size
                    need(total <= MAX_TOTAL_BYTES, "total size cap")
                    files[rel] = st
    validate_namespace(files,directories)
    return root, files, directories

def bounded_read(root, name, before, cap=MAX_FILE_BYTES):
    flags = os.O_RDONLY | getattr(os,"O_NOFOLLOW",0) | getattr(os,"O_NONBLOCK",0) | getattr(os,"O_BINARY",0)
    fd = os.open(root / name, flags)
    try:
        now = os.fstat(fd)
        need(stat.S_ISREG(now.st_mode) and stat.S_IMODE(now.st_mode)==0o644 and now.st_nlink==1,
             "object changed before read: " + name)
        need((now.st_dev,now.st_ino,now.st_size)==(before.st_dev,before.st_ino,before.st_size), "file identity/size changed: " + name)
        need(now.st_size <= cap, "read size cap: " + name)
        parts, size = [], 0
        while True:
            chunk = os.read(fd,min(65536,cap+1-size))
            if not chunk:
                break
            size += len(chunk)
            need(size <= cap and size <= now.st_size, "file grew while reading: " + name)
            parts.append(chunk)
        need(size == now.st_size, "file shortened while reading: " + name)
        return b"".join(parts)
    finally:
        os.close(fd)

def entry_metadata(entry, label):
    keys(entry,("bytes","sha256","mode"),label)
    need(exact_int(entry["bytes"],maximum=MAX_FILE_BYTES),"integer byte size: "+label)
    need(type(entry["sha256"]) is str and HEX64.fullmatch(entry["sha256"]),"SHA256 scalar: "+label)
    need(type(entry["mode"]) is str and entry["mode"]=="100644","Git mode scalar: "+label)

def manifest_schema(doc):
    keys(doc,("schema","version","problem_id","original_head","files"),"package manifest")
    need(type(doc["schema"]) is str and doc["schema"]==SCHEMA,"manifest schema")
    need(type(doc["version"]) is int and doc["version"]==1,"manifest version")
    need(type(doc["problem_id"]) is int and doc["problem_id"]==30004549,"problem ID")
    need(type(doc["original_head"]) is str and doc["original_head"]==HEAD,"immutable original head")
    need(type(doc["files"]) is dict and 24 <= len(doc["files"]) < MAX_FILES,"manifest file count")
    need(MANIFEST not in doc["files"],"manifest cannot inventory itself")
    for name,entry in doc["files"].items():
        canonical_path(name)
        entry_metadata(entry,name)
    need(len({n.casefold() for n in doc["files"]})==len(doc["files"]),"case aliases in manifest")

def strict_old_metadata(value):
    """Strict scalar checks wherever frozen historical JSON carries metadata."""
    if type(value) is dict:
        for k,v in value.items():
            if k in ("bytes","problem_id","target_problem_id","author_turn_count","denominator"):
                need(type(v) is int and v >= 0,"historical integer metadata: "+k)
            if k=="sha256":
                need(type(v) is str and HEX64.fullmatch(v),"historical SHA256")
            if k=="git_blob_sha1":
                need(type(v) is str and HEX40.fullmatch(v),"historical Git blob SHA1")
            strict_old_metadata(v)
    elif type(value) is list:
        for item in value:
            strict_old_metadata(item)

def old_entries(entries, expected, path_key="path", git=False):
    need(type(entries) is list and len(entries)==len(expected),"historical entry count")
    seen=set()
    for e in entries:
        keys(e,(path_key,"bytes","sha256","git_blob_sha1") if git else (path_key,"bytes","sha256"),"historical entry")
        name=canonical_path(e[path_key])
        need(name not in seen and name in expected,"historical path set")
        seen.add(name)
        pin=expected[name]
        need(type(e["bytes"]) is int and e["bytes"]==pin["bytes"] and e["sha256"]==pin["sha256"],"historical entry binding")
        if git:
            need(e["git_blob_sha1"]==pin["git_blob"],"historical Git blob binding")
    need(seen==set(expected),"historical complete entry set")

def inspect_archive(data, expected=None):
    """Validate bounded metadata before decompression, then bounded bytes; never extract."""
    need(type(data) is bytes and len(data)<=MAX_FILE_BYTES,"archive byte cap")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos=archive.infolist()
        need(0<len(infos)<=MAX_ZIP_MEMBERS,"archive member count")
        names,total=[],0
        for item in infos:
            need(item.orig_filename==item.filename,"archive raw-name truncation")
            name=canonical_path(item.filename)
            need(not item.is_dir(),"archive directory member")
            need(item.create_system==3 and item.external_attr>>16 in (0o644,0o100644),"archive member mode/type")
            need(not(item.flag_bits & 1) and item.compress_type in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED),"archive encryption/compression")
            need(exact_int(item.file_size,maximum=MAX_FILE_BYTES) and exact_int(item.compress_size,maximum=MAX_FILE_BYTES),"archive member size cap")
            need(item.file_size <= MAX_ZIP_RATIO*max(1,item.compress_size),"archive compression ratio cap")
            total += item.file_size
            need(total<=MAX_TOTAL_BYTES,"archive cumulative size cap")
            names.append(name)
        need(len(set(n.casefold() for n in names))==len(names),"duplicate/case-alias archive member")
        validate_namespace(names)
        if expected is not None:
            need(type(expected) is dict and set(names)==set(expected),"archive exact member set")
            for item in infos:
                e=expected[item.filename]
                entry_metadata(e,item.filename)
                need(item.file_size==e["bytes"],"archive declared member size")
        result={}
        for item in infos:
            with archive.open(item,"r") as stream:
                content=stream.read(item.file_size+1)
                need(len(content)==item.file_size and not stream.read(1),"archive expanded size mismatch")
            if expected is not None:
                need(sha(content)==expected[item.filename]["sha256"],"archive member SHA256")
            result[item.filename]={"bytes":len(content),"sha256":sha(content),"mode":"100644"}
        return result

def authenticate_originals(payload):
    expected_paths={PREFIX+n for n in ORIGINAL_PINS}
    need(len(ORIGINAL_PINS)==24 and {n for n in payload if n.startswith(PREFIX)}==expected_paths,"exact original24 inventory")
    originals={n:payload[PREFIX+n] for n in ORIGINAL_PINS}
    for n,pin in ORIGINAL_PINS.items():
        content=originals[n]
        blob=hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()
        need(len(content)==pin["bytes"] and sha(content)==pin["sha256"] and blob==pin["git_blob"] and pin["git_mode"]=="100644","immutable original binding: "+n)
    docs={n:load_json(b,n) for n,b in originals.items() if n.endswith(".json")}
    for doc in docs.values():
        need(type(doc) is dict,"historical JSON object")
        strict_old_metadata(doc)
    public=docs["PUBLIC_MANIFEST.json"]
    need(public["schema"]=="anti-invariant-publication-v1" and public["problem_id"]==30004549 and public["author_turns"]=="4/5","historical public identity")
    old_entries(public["files"],{n:p for n,p in ORIGINAL_PINS.items() if n not in ("PUBLIC_MANIFEST.json","PUBLIC_MANIFEST.sha256")},git=True)
    need(originals["PUBLIC_MANIFEST.sha256"]==sha(originals["PUBLIC_MANIFEST.json"]).encode()+b"  PUBLIC_MANIFEST.json\n","historical sidecar")
    author_pins={n.removeprefix("author/"):p for n,p in ORIGINAL_PINS.items() if n.startswith("author/")}
    author=docs["author/MANIFEST.json"]
    need(author["schema"]=="anti-invariant-author-publication-payload-v1" and author["problem_id"]==30004549 and author["author_turn_count"]==4 and author["denominator"]==5,"historical author identity")
    old_entries(author["files"],{n:p for n,p in author_pins.items() if n!="MANIFEST.json"})
    ext=docs[EXTERNAL]
    need(ext["schema"]=="anti-invariant-final-author-external-manifest-v1" and ext["problem_id"]==30004549 and ext["author_turn_count"]==4,"historical external identity")
    keys(ext["archive"],("filename","bytes","sha256"),"historical archive pin")
    need(ext["archive"]["filename"]==ARCHIVE and ext["archive"]["bytes"]==len(originals[ARCHIVE]) and ext["archive"]["sha256"]==sha(originals[ARCHIVE]),"historical archive binding")
    old_entries(ext["files"],author_pins)
    archive_expected={n:{"bytes":p["bytes"],"sha256":p["sha256"],"mode":"100644"} for n,p in author_pins.items()}
    need(inspect_archive(originals[ARCHIVE],archive_expected)==archive_expected,"historical ZIP mirrors")
    a_expected={"R3_counterexample_candidate.md":ORIGINAL_PINS["author/R3_counterexample_candidate.md"],**{n.removeprefix("audit_a/"):p for n,p in ORIGINAL_PINS.items() if n.startswith("audit_a/") and n!="audit_a/AUDIT_MANIFEST.json"}}
    old_entries(docs["audit_a/AUDIT_MANIFEST.json"]["files"],a_expected,path_key="filename")
    b=docs["audit_b/AUDIT_MANIFEST.json"]
    need(b["target_problem_id"]==30004549,"historical audit B identity")
    old_entries([b["candidate"]],{"R3_counterexample_candidate.md":ORIGINAL_PINS["author/R3_counterexample_candidate.md"]},path_key="name")
    old_entries(b["authored_artifacts"],{n.removeprefix("audit_b/"):p for n,p in ORIGINAL_PINS.items() if n.startswith("audit_b/") and n!="audit_b/AUDIT_MANIFEST.json"},path_key="name")
    return originals

def verify(root_value, anchor):
    need(type(anchor) is str and HEX64.fullmatch(anchor),"external manifest SHA256 required")
    root,files,directories=scan_tree(root_value)
    need(MANIFEST in files,"manifest missing")
    raw=bounded_read(root,MANIFEST,files[MANIFEST],MAX_MANIFEST_BYTES)
    need(sha(raw)==anchor,"external manifest anchor mismatch")
    doc=load_json(raw,MANIFEST)
    manifest_schema(doc)
    need(set(files)==set(doc["files"])|{MANIFEST},"closed regular-file inventory mismatch")
    implied={p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix()!="."}
    need(directories==implied,"extra/empty directory inventory mismatch")
    payload={}
    for n,e in doc["files"].items():
        need(files[n].st_size==e["bytes"],"declared byte size mismatch: "+n)
        data=bounded_read(root,n,files[n])
        need(sha(data)==e["sha256"],"payload SHA256 mismatch: "+n)
        payload[n]=data
    originals=authenticate_originals(payload)
    return {"result":"pass","schema":SCHEMA,"problem_id":30004549,"original_head":HEAD,
            "files":len(files),"original_files":24,"archive_members":7,"manifest_sha256":anchor},originals

CHILD_BOOT = r'''import base64,json,platform,sys
source=base64.b64decode(sys.argv[2],validate=True)
if len(source)>16384: raise RuntimeError("source cap")
import sympy
if sympy.__version__!="1.14.0": raise RuntimeError("SymPy 1.14.0 required")
meta={"python":platform.python_version(),"implementation":platform.python_implementation(),"sympy":sympy.__version__,"isolated":sys.flags.isolated,"no_site":sys.flags.no_site,"no_user_site":sys.flags.no_user_site,"dont_write_bytecode":sys.dont_write_bytecode,"optimize":sys.flags.optimize}
print("PR948_RUNTIME "+json.dumps(meta,sort_keys=True),flush=True)
exec(compile(source,sys.argv[1],"exec",optimize=0),{"__name__":"__main__","__file__":sys.argv[1]})
'''

def child_environment(temp):
    env={"TMPDIR":temp,"TMP":temp,"TEMP":temp}
    for name in ("SYSTEMROOT","WINDIR"):
        if name in os.environ:
            env[name]=os.environ[name]
    return env

def run_bounded(argv, cwd, env, seconds=CHILD_SECONDS, stdout_cap=CHILD_STDOUT_BYTES, stderr_cap=CHILD_STDERR_BYTES):
    """Cap wall time and captured output. No memory/process/filesystem sandbox."""
    need(seconds>0 and stdout_cap>0 and stderr_cap>0,"child bounds")
    process=subprocess.Popen(argv,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    buffers=[bytearray(),bytearray()]
    overflow=threading.Event()
    def consume(stream,index,cap):
        try:
            while True:
                chunk=stream.read(4096)
                if not chunk: break
                room=cap-len(buffers[index])
                buffers[index].extend(chunk[:max(0,room)])
                if len(chunk)>room:
                    overflow.set()
                    break
        finally:
            stream.close()
    threads=[threading.Thread(target=consume,args=(stream,i,cap),daemon=True) for i,(stream,cap) in enumerate(((process.stdout,stdout_cap),(process.stderr,stderr_cap)))]
    for thread in threads: thread.start()
    deadline=time.monotonic()+seconds
    failure=None
    while process.poll() is None:
        if overflow.is_set():
            failure="child output cap"
            break
        if time.monotonic()>=deadline:
            failure="child wall-time cap"
            break
        overflow.wait(min(0.02,max(0,deadline-time.monotonic())))
    if failure:
        process.kill()
    process.wait(timeout=5)
    for thread in threads: thread.join(timeout=1)
    need(not any(thread.is_alive() for thread in threads),"child stream cleanup failed")
    need(not overflow.is_set(),"child output cap")
    need(failure is None,failure or "child failure")
    return process.returncode,bytes(buffers[0]),bytes(buffers[1])

def execute_source(source,label,cwd,env,seconds=CHILD_SECONDS):
    need(type(source) is bytes and len(source)<=MAX_SOURCE_BYTES,"checker source bound")
    args=[sys.executable,"-I","-B","-c",CHILD_BOOT,label,base64.b64encode(source).decode("ascii")]
    code,out,err=run_bounded(args,cwd,env,seconds)
    header,sep,body=out.partition(b"\n")
    need(sep and header.startswith(b"PR948_RUNTIME "),"missing child runtime receipt")
    meta=load_json(header.removeprefix(b"PR948_RUNTIME "),"child runtime")
    need(meta["isolated"]==1 and meta["no_user_site"]==1 and meta["no_site"]==0 and meta["dont_write_bytecode"] is True and meta["optimize"]==0,"child flags")
    return code,body,err,meta

def replay(originals):
    results=[]
    with tempfile.TemporaryDirectory(prefix="pr948-profile-") as temp:
        need(not any(Path(temp).iterdir()),"child working directory is not empty")
        env=child_environment(temp)
        for source,expected in CHECKERS:
            code,out,err,meta=execute_source(originals[source],PREFIX+source,temp,env)
            need(code==0 and not err and out==originals[expected],"checker failed/output mismatch: "+source)
            need(not any(Path(temp).iterdir()),"checker wrote to empty working directory")
            results.append({"checker":source,"result":"pass","stdout_sha256":sha(out),"runtime":meta,"assertions_forced":True,"argv_flags":["-I","-B"],"environment_keys":sorted(env)})
        code,out,err,meta=execute_source(b"assert False, 'PROFILE_ASSERTION_GUARD'\n","<assertion-guard>",temp,env)
        need(code!=0 and b"AssertionError" in err and b"PROFILE_ASSERTION_GUARD" in err,"false assertion guard failed")
        need(not any(Path(temp).iterdir()),"guard wrote to working directory")
    return results,{"result":"rejected_false_assertion","runtime":meta}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",required=True)
    parser.add_argument("--manifest-sha256",required=True)
    parser.add_argument("--run-checkers",action="store_true")
    args=parser.parse_args()
    result,originals=verify(args.root,args.manifest_sha256)
    result["outer_runtime"]={"isolated":sys.flags.isolated,"no_site":sys.flags.no_site,"dont_write_bytecode":sys.dont_write_bytecode,"optimize":sys.flags.optimize}
    if args.run_checkers:
        result["checker_replays"],result["assertion_guard"]=replay(originals)
    result["limits"]="Externally anchored finite byte/schema checks and fixed local checker replays only; trusted installed SymPy/site packages; no hostile-OS race sandbox, global proof, human peer review, priority or novelty certificate."
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    try:
        main()
    except (ProfileError,OSError,zipfile.BadZipFile,RuntimeError,subprocess.SubprocessError) as error:
        print("PROFILE_REJECT: "+str(error),file=sys.stderr)
        raise SystemExit(1)
