#!/usr/bin/env python3
"""Actual bounded profile tests. Invoke with supplied Python -I -S -B.

Fixtures are created below this development directory and removed. No shared
runtime, original, sealed audit, native state, or Git metadata is modified.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit("Run tests with -I -S -B")
from pathlib import Path
import argparse
import copy
import datetime
import hashlib
import io
import json
import os
import shutil
import socket
import stat
import struct
import subprocess
import tempfile
import types
import warnings
import zipfile

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--originals",type=Path,required=True,help="authenticated historical original24 directory")
parser.add_argument("--output-dir",type=Path,required=True,help="owned development output directory outside a closed release tree")
parser.add_argument("--driver",type=Path,default=HERE/"verify_package.py")
options=parser.parse_args()
SOURCE=options.originals.resolve(strict=True)
OUTPUT=options.output_dir.resolve()
OUTPUT.mkdir(parents=True,exist_ok=True)
DRIVER=options.driver.resolve(strict=True)
PRIVATE=OUTPUT/"private_fixtures"
PRIVATE.mkdir(exist_ok=True)
EVENTS=[]
profile=types.ModuleType("profile_under_test")
profile.__file__=str(DRIVER)
exec(compile(DRIVER.read_bytes(),str(DRIVER),"exec",optimize=0),profile.__dict__)

def sha(data): return hashlib.sha256(data).hexdigest()
def need(ok,message):
    if not ok: raise RuntimeError(message)
def event(name,**data):
    record={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"test":name,**data}
    EVENTS.append(record)
    with (OUTPUT/"DEVELOPMENT_EVENTS.ndjson").open("a") as stream:
        stream.write(json.dumps(record)+"\n")
def manifest(root):
    return {"schema":profile.SCHEMA,"version":1,"problem_id":30004549,"original_head":profile.HEAD,"files":{p.relative_to(root).as_posix():{"bytes":p.stat().st_size,"sha256":sha(p.read_bytes()),"mode":"100644"} for p in sorted(root.rglob("*")) if p.is_file() and p.name!=profile.MANIFEST}}
def write_manifest(root,doc=None):
    raw=(json.dumps(manifest(root) if doc is None else doc,indent=2)+"\n").encode()
    (root/profile.MANIFEST).write_bytes(raw)
    return sha(raw)
def cli(root,anchor,flags=None,env=None,checkers=False,timeout=15):
    args=[sys.executable,*(flags if flags is not None else ["-I","-S","-B"]),str(DRIVER),"--root",str(root),"--manifest-sha256",anchor]
    if checkers: args.append("--run-checkers")
    return subprocess.run(args,capture_output=True,timeout=timeout,env=env)
def zipped(items,compression=zipfile.ZIP_DEFLATED):
    data=io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore",UserWarning)
        with zipfile.ZipFile(data,"w",compression=compression) as z:
            for name,body,mode in items:
                info=zipfile.ZipInfo(name)
                info.create_system=3
                info.external_attr=mode<<16
                info.compress_type=compression
                z.writestr(info,body)
    return data.getvalue()

try:
    with tempfile.TemporaryDirectory(dir=PRIVATE,prefix="run-") as td:
        temp=Path(td)
        # Keep child temporary directories in this exclusive development scope.
        os.environ["TMPDIR"]=str(temp)
        tempfile.tempdir=str(temp)
        base=temp/"baseline"
        original=base/profile.PREFIX
        original.mkdir(parents=True)
        for name in profile.ORIGINAL_PINS:
            dest=original/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(SOURCE/name,dest)
            dest.chmod(0o644)
        shutil.copyfile(DRIVER,base/"verify_package.py")
        anchor=write_manifest(base)
        doc=json.loads((base/profile.MANIFEST).read_bytes())
        result,authenticated=profile.verify(str(base),anchor)
        need(result["original_files"]==24 and result["archive_members"]==7,"baseline inventory")
        event("strict_baseline_inventory",outcome="pass",files=result["files"],manifest_sha256=anchor)
        for mode,flags in (("isolated_no_site",["-I","-S","-B"]),("outer_optimized",["-I","-S","-B","-O"])):
            p=cli(base,anchor,flags=flags,checkers=True,timeout=90)
            need(p.returncode==0 and not p.stderr,"baseline CLI "+mode+": "+p.stderr.decode(errors="replace")[:200])
            d=json.loads(p.stdout)
            need(len(d["checker_replays"])==3 and d["assertion_guard"]["result"]=="rejected_false_assertion","genuine checker/guard inventory")
            need(all(e["runtime"]["optimize"]==0 and e["runtime"]["dont_write_bytecode"] is True for e in d["checker_replays"]),"child flags")
            (OUTPUT/("BASELINE_"+mode.upper()+".json")).write_bytes(p.stdout)
            event("genuine_checker_replay_"+mode,outcome="pass",stdout_sha256=sha(p.stdout),checkers=3,outer_runtime=d["outer_runtime"])

        def mutation(name,edit,rebuild=False,expected=None):
            root=temp/"mutation"
            shutil.copytree(base,root)
            try:
                edit(root)
                new_anchor=write_manifest(root) if rebuild else anchor
                try: profile.verify(str(root),new_anchor)
                except (profile.ProfileError,OSError,zipfile.BadZipFile) as error:
                    need(expected is None or expected in str(error),name+" unexpected rejection: "+str(error))
                    event(name,outcome="rejected",exception=type(error).__name__,message=str(error))
                else: raise RuntimeError(name+" was accepted")
            finally: shutil.rmtree(root)
        mutation("unlisted_FIFO",lambda r:os.mkfifo(r/"unlisted-fifo"),expected="nonregular")
        def listed_fifo(r):
            target=r/profile.PREFIX/"README.md"
            target.unlink()
            os.mkfifo(target)
        mutation("listed_FIFO",listed_fifo,expected="nonregular")
        mutation("file_symlink",lambda r:(r/"link").symlink_to(r/"verify_package.py"),expected="nonregular")
        mutation("directory_symlink",lambda r:(r/"linked-dir").symlink_to(r/"original",target_is_directory=True),expected="nonregular")
        mutation("hard_link",lambda r:os.link(r/"verify_package.py",r/"hard-copy"),expected="hard-linked")
        mutation("empty_directory",lambda r:(r/"empty").mkdir(),expected="directory inventory")
        mutation("missing_file",lambda r:(r/profile.PREFIX/"README.md").unlink(),expected="inventory")
        mutation("extra_regular_file",lambda r:(r/"extra.txt").write_bytes(b"x"),expected="inventory")
        mutation("disk_executable_mode",lambda r:(r/"verify_package.py").chmod(0o755),expected="disk mode")
        mutation("changed_original_coherent_outer_manifest",lambda r:(r/profile.PREFIX/"README.md").write_bytes(b"changed\n"),rebuild=True,expected="immutable original")
        mutation("missing_original_coherent_outer_manifest",lambda r:(r/profile.PREFIX/"README.md").unlink(),rebuild=True,expected="original24")
        mutation("extra_original_coherent_outer_manifest",lambda r:(r/profile.PREFIX/"extra.txt").write_bytes(b"x"),rebuild=True,expected="original24")
        if hasattr(socket,"AF_UNIX"):
            sock=socket.socket(socket.AF_UNIX)
            root=temp/"socket-root"
            shutil.copytree(base,root)
            try:
                # Use a short root to respect macOS UNIX socket path limits.
                short=temp/"sock"
                previous=os.getcwd()
                os.chdir(temp)
                try:
                    sock.bind("sock")
                finally:
                    os.chdir(previous)
                short.rename(root/"socket")
                try: profile.verify(str(root),anchor)
                except profile.ProfileError as e: event("socket_object",outcome="rejected",message=str(e))
                else: raise RuntimeError("socket accepted")
            except OSError as e:
                event("socket_object",outcome="platform_path_limit_skip",message=str(e))
            finally:
                sock.close()
                shutil.rmtree(root)
        def change_manifest(r,change):
            d=json.loads((r/profile.MANIFEST).read_bytes())
            change(d)
            write_manifest(r,d)
        def manifest_mutation(name,change,expected=None):
            root=temp/"schema"
            shutil.copytree(base,root)
            try:
                change_manifest(root,change)
                new=sha((root/profile.MANIFEST).read_bytes())
                try: profile.verify(str(root),new)
                except profile.ProfileError as e:
                    need(expected is None or expected in str(e),name+" rejection mismatch: "+str(e))
                    event(name,outcome="rejected",message=str(e))
                else: raise RuntimeError(name+" accepted")
            finally: shutil.rmtree(root)
        for name,key,value in (("bool_version","version",True),("float_version","version",1.0),("float_problem","problem_id",30004549.0),("wrong_head","original_head","0"*40),("extra_top_key","surprise",1)):
            manifest_mutation(name,lambda d,key=key,value=value:d.update({key:value}))
        first=next(iter(doc["files"]))
        for name,key,value in (("bool_bytes","bytes",True),("float_bytes","bytes",float(doc["files"][first]["bytes"])),("bad_git_mode","mode","120000"),("disk_mode_in_git_field","mode","0644"),("uppercase_hash","sha256","A"*64),("wrong_payload_hash","sha256","0"*64)):
            manifest_mutation(name,lambda d,key=key,value=value:d["files"][first].update({key:value}))
        for bad in ("../escape","/absolute","a//b","a/./b","a\\b",".","NUL.txt"):
            manifest_mutation("bad_path_"+repr(bad),lambda d,bad=bad:d["files"].update({bad:d["files"].pop(first)}),"path")
        root=temp/"bad-json"
        shutil.copytree(base,root)
        for name,raw in (("malformed_JSON",b"{"),("duplicate_JSON_key",b'{"schema":1,"schema":2}'),("nonfinite_JSON",b'{"schema":NaN}')):
            (root/profile.MANIFEST).write_bytes(raw)
            try: profile.verify(str(root),sha(raw))
            except profile.ProfileError as e: event(name,outcome="rejected",message=str(e))
            else: raise RuntimeError(name+" accepted")
        shutil.rmtree(root)
        mutation("coherent_rebound_without_external_anchor",lambda r:change_manifest(r,lambda d:d.update(version=2)),expected="anchor mismatch")
        for name,value in (("historical_bool_bytes",{"bytes":True}),("historical_float_count",{"author_turn_count":4.0}),("historical_float_source_bytes",{"sources":[{"bytes":1.0}]}),("historical_nonstring_hash",{"sha256":12})):
            try: profile.strict_old_metadata(value)
            except profile.ProfileError as e: event(name,outcome="rejected",message=str(e))
            else: raise RuntimeError(name+" accepted")
        link=temp/"root-link"
        link.symlink_to(base,target_is_directory=True)
        for name,root in (("root_symlink",link),("ancestor_symlink",link/"original"),("root_parent_traversal",base/".."/"baseline")):
            try: profile.verify(str(root),anchor)
            except profile.ProfileError as e: event(name,outcome="rejected",message=str(e))
            else: raise RuntimeError(name+" accepted")
        for name,flags in (("missing_all_startup_flags",["-B"]),("missing_no_site",["-I","-B"]),("missing_no_bytecode",["-I","-S"])):
            p=cli(base,anchor,flags=flags)
            need(p.returncode!=0 and b"PROFILE_STARTUP" in p.stderr,name)
            event(name,outcome="rejected_before_root_reads",exit_code=p.returncode,stderr=p.stderr.decode(errors="replace"))
        import_code="exec(compile(open("+repr(str(DRIVER))+",'rb').read(),'profile','exec'))"
        p=subprocess.run([sys.executable,"-B","-c",import_code],capture_output=True,timeout=10)
        need(p.returncode!=0 and b"PROFILE_STARTUP" in p.stderr,"module startup guard")
        event("imported_module_startup_guard",outcome="rejected_before_profile_imports",stderr=p.stderr.decode(errors="replace"))
        def sparse(r,name,size):
            with open(r/name,"wb") as stream: stream.truncate(size)
        mutation("per_file_cap",lambda r:sparse(r,"large.bin",profile.MAX_FILE_BYTES+1),expected="per-file size cap")
        mutation("manifest_cap",lambda r:sparse(r,profile.MANIFEST,profile.MAX_MANIFEST_BYTES+1),expected="read size cap")
        mutation("total_size_cap",lambda r:[sparse(r,f"large{i}.bin",profile.MAX_FILE_BYTES) for i in range(5)],expected="total size cap")
        mutation("file_count_cap",lambda r:[(r/f"f{i}").write_bytes(b"") for i in range(profile.MAX_FILES)],expected="file count cap")
        mutation("directory_count_cap",lambda r:[(r/f"d{i}").mkdir() for i in range(profile.MAX_DIRS+1)],expected="directory count cap")
        def deep(r):
            q=r
            for i in range(profile.MAX_DEPTH+1):
                q=q/"d"
                q.mkdir()
        mutation("depth_cap",deep,expected="path canonical/depth")

        good=zipped([("a.txt",b"hello",0o100644)])
        need(profile.inspect_archive(good)["a.txt"]["bytes"]==5,"generic regular ZIP")
        event("generic_regular_archive",outcome="pass")
        zips=[("ZIP_symlink",zipped([("a.txt",b"target",0o120777)])),("ZIP_bad_permission",zipped([("a.txt",b"x",0o100600)])),("ZIP_parent",zipped([("../escape",b"x",0o100644)])),("ZIP_absolute",zipped([("/escape",b"x",0o100644)])),("ZIP_duplicate",zipped([("a",b"x",0o100644),("a",b"y",0o100644)])),("ZIP_ratio_cap",zipped([("a",b"x"*65536,0o100644)]))]
        def patch_central(raw,offset,value,fmt="<I"):
            b=bytearray(raw)
            start=0
            while True:
                at=b.find(b"PK\x01\x02",start)
                if at<0: break
                struct.pack_into(fmt,b,at+offset,value)
                start=at+4
            return bytes(b)
        zips += [("ZIP_oversize_metadata",patch_central(good,24,profile.MAX_FILE_BYTES+1)),("ZIP_unsupported_compression",patch_central(good,10,99,"<H")),("ZIP_encrypted_metadata",patch_central(good,8,1,"<H"))]
        zips.append(("ZIP_embedded_NUL_raw_name",good.replace(b"a.txt",b"a\x00txt")))
        cumulative=zipped([(f"a{i}",b"x",0o100644) for i in range(5)])
        cumulative=patch_central(patch_central(cumulative,20,profile.MAX_FILE_BYTES),24,profile.MAX_FILE_BYTES)
        zips.append(("ZIP_cumulative_cap_metadata",cumulative))
        for name,data in zips:
            original_open=zipfile.ZipFile.open
            decompressions=[]
            def forbidden_open(*args,**kwargs):
                decompressions.append(True)
                raise RuntimeError("decompression began before metadata rejection")
            zipfile.ZipFile.open=forbidden_open
            try:
                try: profile.inspect_archive(data)
                except (profile.ProfileError,zipfile.BadZipFile) as e:
                    need(not decompressions,name+" decompressed")
                    event(name,outcome="rejected_before_decompression",message=str(e))
                else: raise RuntimeError(name+" accepted")
            finally: zipfile.ZipFile.open=original_open
        expected={"a.txt":{"bytes":5,"sha256":"0"*64,"mode":"100644"}}
        try: profile.inspect_archive(good,expected)
        except profile.ProfileError as e: event("ZIP_wrong_expanded_hash",outcome="rejected",message=str(e))
        else: raise RuntimeError("wrong ZIP hash accepted")

        poison=temp/"poison"
        poison.mkdir()
        marker=temp/"POISON_EXECUTED"
        for name in ("sympy.py","sitecustomize.py","usercustomize.py"):
            (poison/name).write_text("from pathlib import Path\nPath("+repr(str(marker))+").write_text('executed')\nraise RuntimeError('PROFILE_OWNED_IMPORT_POISON')\n")
        control_env=dict(os.environ,PYTHONPATH=str(poison),TMPDIR=str(temp))
        control=subprocess.run([sys.executable,"-B","-c","import sympy"],cwd=poison,env=control_env,capture_output=True,timeout=15)
        need(control.returncode!=0 and marker.exists() and b"PROFILE_OWNED_IMPORT_POISON" in control.stderr,"ambient poison positive control")
        event("ambient_import_poison_positive_control",outcome="controlled_poison_executed_without_isolation",exit_code=control.returncode,stderr=control.stderr.decode(errors="replace"))
        marker.unlink()
        env=dict(os.environ,PYTHONPATH=str(poison),PYTHONUSERBASE=str(poison),PYTHONHOME=str(poison),PYTHONOPTIMIZE="2",PYTHONDONTWRITEBYTECODE="0",TMPDIR=str(temp))
        p=cli(base,anchor,env=env,checkers=True,timeout=90)
        need(p.returncode==0 and not p.stderr and not marker.exists(),"ambient import/environment poison")
        poisoned=json.loads(p.stdout)
        need(all(e["runtime"]["optimize"]==0 and e["runtime"]["dont_write_bytecode"] is True for e in poisoned["checker_replays"]),"poisoned child flag receipts")
        (OUTPUT/"BASELINE_POISONED_ENVIRONMENT.json").write_bytes(p.stdout)
        event("PYTHONPATH_user_site_sitecustomize_optimization_poison",outcome="ignored",marker_created=False,checker_replays=3)
        with tempfile.TemporaryDirectory(dir=temp,prefix="bounded-child-") as cwd:
            childenv=profile.child_environment(cwd)
            code,body,err,meta=profile.execute_source(b"print(__debug__)\n","<optimization-control>",cwd,childenv)
            need(code==0 and body==b"True\n" and not err,"forced compile optimize0")
            event("explicit_compile_optimize0",outcome="pass",runtime=meta)
            for name,source,kw in (("child_stdout_cap","import os; os.write(1,b'x'*100000)",{"stdout_cap":1024}),("child_stderr_cap","import os; os.write(2,b'x'*100000)",{"stderr_cap":1024}),("child_wall_time_cap","import time; time.sleep(2)",{"seconds":0.1})):
                try: profile.run_bounded([sys.executable,"-I","-S","-B","-c",source],cwd,childenv,**kw)
                except profile.ProfileError as e: event(name,outcome="bounded_rejection",message=str(e))
                else: raise RuntimeError(name+" not enforced")
        need(not any(temp.rglob("*.pyc")),"private fixture cache write")
        event("private_fixture_no_pyc",outcome="pass")
    event("owned_fixture_cleanup",outcome="pass",remaining_files=sum(1 for p in PRIVATE.rglob("*") if p.is_file()))
except Exception as error:
    event("TEST_RUN_FAILURE",outcome="failure",exception=type(error).__name__,message=str(error))
    raise
else:
    final={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"pass_development_tests_not_independent_review","event_count":len(EVENTS),"events":EVENTS,"runtime":{"python":sys.version.split()[0],"executable":sys.executable},"limits":"Development tests on supplied CPython3.14.6/SymPy1.14.0 only; no publication/priority acceptance or hostile-OS sandbox."}
    (OUTPUT/"DEVELOPMENT_RESULTS.json").write_text(json.dumps(final,indent=2)+"\n")
    print(json.dumps({k:v for k,v in final.items() if k!="events"},indent=2))
