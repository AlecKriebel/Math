"""Finite engineering controls for the wrapper; no mathematical acceptance.

Run beside portable.py, with the private fixture already prepared. This helper
is an audit artifact, not part of the original candidate or a publication build.
"""
from pathlib import Path
import datetime
import importlib.util
import io
import json
import os
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib

HERE=Path(__file__).absolute().parent
spec=importlib.util.spec_from_file_location("portable",HERE/"portable.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]


def reject(label,call):
    try: call()
    except (ValueError,OSError,zipfile.BadZipFile,zlib.error,struct.error) as exc:
        results.append({"control":label,"status":"REJECTED_AS_REQUIRED","exception":type(exc).__name__,"reason":str(exc)})
    else: raise RuntimeError("control accepted: "+label)


def main():
    for label,raw in [("duplicate_JSON",b'{"a":1,"a":2}'),("NaN_JSON",b'{"a":NaN}'),("infinite_JSON",b'{"a":1e999}')]:
        reject(label,lambda raw=raw:m.strict_json(raw))
    for label,name in [("absolute_path","/x"),("parent_path","a/../b"),("empty_segment","a//b"),("unicode_path","caf\u00e9"),("backslash_path","a\\b")]:
        reject(label,lambda name=name:m.safe_name(name))
    row={"path":"x","bytes":0,"sha256":"0"*64}
    reject("boolean_byte_count",lambda:m.rows_map([{**row,"bytes":False}]))
    reject("float_byte_count",lambda:m.rows_map([{**row,"bytes":0.0}]))
    reject("duplicate_inventory",lambda:m.rows_map([row,row]))
    reject("case_alias_inventory",lambda:m.rows_map([row,{**row,"path":"X"}]))
    reject("directory_alias_inventory",lambda:m.rows_map([{**row,"path":"A/x"},{**row,"path":"a/y"}]))
    reject("file_directory_collision",lambda:m.rows_map([row,{**row,"path":"x/y"}]))
    reject("extra_index_key",lambda:m.typed_index(json.dumps({"schema":m.PACKAGE_SCHEMA,"problem_id":"30005079","files":[row],"extra":1}).encode(),m.PACKAGE_SCHEMA))
    reject("numeric_problem_id",lambda:m.typed_index(json.dumps({"schema":m.PACKAGE_SCHEMA,"problem_id":30005079,"files":[row]}).encode(),m.PACKAGE_SCHEMA))
    expected={"a.txt":b"hello\n"};raw=m.deterministic_zip(expected)
    m.zip_payloads(raw,expected,generated=True)
    results.append({"control":"canonical_ZIP","status":"PASS"})
    reject("ZIP_trailer",lambda:m.zip_payloads(raw+b"x",expected,generated=True))
    bad=bytearray(raw);bad[14]^=1
    reject("ZIP_local_CRC_disagreement",lambda:m.zip_payloads(bytes(bad),expected,generated=True))
    bad=bytearray(raw);central=raw.index(b"PK\x01\x02");struct.pack_into("<I",bad,central+38,(stat.S_IFLNK|0o777)<<16)
    reject("ZIP_symlink_mode",lambda:m.zip_payloads(bytes(bad),expected,generated=True))
    bad=bytearray(raw);struct.pack_into("<H",bad,central+12,1)
    reject("ZIP_wrong_timestamp",lambda:m.zip_payloads(bytes(bad),expected,generated=True))
    # Add a suffix INSIDE the declared raw DEFLATE region; update all offsets and
    # compressed lengths so local/central/EOCD metadata remain mutually coherent.
    local=struct.unpack_from("<4s5H3I2H",raw,0);end=struct.unpack_from("<4s4H2IH",raw,len(raw)-22)
    at=30+local[9]+local[7];bad=bytearray(raw[:at]+b"X"+raw[at:]);newcentral=central+1
    struct.pack_into("<I",bad,18,local[7]+1);struct.pack_into("<I",bad,newcentral+20,local[7]+1)
    struct.pack_into("<I",bad,len(bad)-22+16,end[6]+1)
    reject("ZIP_unused_raw_deflate_suffix",lambda:m.zip_payloads(bytes(bad),expected,generated=True))
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w",zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("a.txt",expected["a.txt"]);archive.writestr("a.txt",expected["a.txt"])
    reject("ZIP_duplicate_member",lambda:m.zip_payloads(b.getvalue(),expected,generated=True))
    fixture=HERE/"private_tmp/fixture"
    blobs={p.relative_to(fixture).as_posix():p.read_bytes() for p in fixture.rglob("*") if p.is_file()}
    m.original_inputs(blobs)
    bad=dict(blobs);bad["source/PROOF.md"]+=b"x"
    reject("original_source_tamper_despite_new_outer_index",lambda:m.original_inputs(bad))
    bad=dict(blobs);bad["root_evidence/SOURCE_MANIFEST.json"]+=b" "
    reject("source_manifest_external_pin",lambda:m.original_inputs(bad))
    meta=m.strict_json(blobs["metadata.json"]);meta["version"]="2.0.0"
    bad=dict(blobs);bad["metadata.json"]=json.dumps(meta).encode()
    reject("metadata_identity_drift",lambda:m.publication_metadata(bad))
    bad=dict(blobs);deposit=m.strict_json(blobs["zenodo-deposit.json"]);deposit["files"].append({"name":"extra","path":"extra"});bad["zenodo-deposit.json"]=json.dumps(deposit).encode()
    reject("third_deposit_asset",lambda:m.publication_metadata(bad))
    with tempfile.TemporaryDirectory(prefix="rank-two-fano-controls-",dir=HERE/"private_tmp") as td:
        tree=Path(td)/"tree";m.materialize(tree,{"a/b.txt":b"x"})
        (tree/"empty").mkdir();reject("unlisted_empty_directory",lambda:m.closed_tree(tree,{"a/b.txt"}));(tree/"empty").rmdir()
        (tree/"extra").write_bytes(b"x");reject("unlisted_file",lambda:m.closed_tree(tree,{"a/b.txt"}));(tree/"extra").unlink()
        (tree/"a/b.txt").unlink();(tree/"a/b.txt").symlink_to(HERE/"portable.py")
        reject("symlink_leaf",lambda:m.closed_tree(tree,{"a/b.txt"}))
        (tree/"a/b.txt").unlink();(tree/"a").rmdir();(tree/"a").symlink_to(HERE)
        reject("symlink_directory",lambda:m.closed_tree(tree,{"a/b.txt"}))
    # Existing APFS aliases are used when available; no system mutation occurs.
    output=fixture/"source/checks/rank-two-fano-verification.zip"
    reject("output_inside_indexed_nested_directory",lambda:m.output_preflight(fixture,blobs,output))
    data_alias=Path("/System/Volumes/Data")/output.relative_to("/")
    if data_alias.parent.is_dir() and data_alias.parent.stat().st_ino==output.parent.stat().st_ino:
        reject("actual_APFS_firmlink_nested_output_alias",lambda:m.output_preflight(fixture,blobs,data_alias))
    else: results.append({"control":"actual_APFS_firmlink_nested_output_alias","status":"UNAVAILABLE_ON_THIS_FILESYSTEM"})
    index=m.sha(blobs["package_index.json"])
    proc=subprocess.run([sys.executable,"-I","-S","-B",str(fixture/"portable.py"),"build",index,str(HERE/"private_tmp/rank-two-fano-verification.zip"),"--verify-only"],capture_output=True)
    if proc.returncode!=2 or b"unrecognized arguments: --verify-only" not in proc.stderr: raise RuntimeError("build accepted verify-only")
    results.append({"control":"build_verify_only_CLI_rejected_before_execution","status":"REJECTED_AS_REQUIRED","actual_subprocess_exit":proc.returncode})
    receipt={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"completion_estimate_percent":80,"scope":"Finite wrapper engineering controls; no mathematical acceptance or final artifact PDF validation.","actual_CLI_subprocess_count":1,"in_process_control_count":len(results)-1,"results":results}
    (HERE/"ENGINEERING_CONTROL_RECEIPT.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","controls":len(results)}))


if __name__=="__main__": main()
