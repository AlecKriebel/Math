#!/usr/bin/env python3
"""Owned-copy reproducibility and bounded negative probes; no original writes.

Tests intentionally expose verifier limits. They do not claim an OS sandbox.
"""
from pathlib import Path
import datetime, hashlib, importlib.util, io, json, os, shutil, stat
import subprocess, sys, tempfile, warnings, zipfile
sys.dont_write_bytecode = True

OUT = Path(__file__).resolve().parent
A = OUT.parents[1]
SOURCE = A / "original/unsolved_math_prioritization/attempts/30004549"
TMP = OUT / "tmp"
TMP.mkdir(exist_ok=True)
# Resolve from repository for clarity; this path is supplied read-only by parent.
PYTHON = str(OUT.parents[4] / "draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(TMP))
for key in ("PYTHONPATH", "PYTHONHOME"):
    ENV.pop(key, None)
EVENTS = []

def sha(b):
    return hashlib.sha256(b).hexdigest()

def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)

def run(args, cwd=TMP, env=ENV, timeout=90):
    p = subprocess.run([PYTHON, *args], cwd=cwd, env=env, capture_output=True, timeout=timeout)
    return p

def record(name, **kw):
    EVENTS.append({"test":name, **kw})

def record_run(name, p):
    return {"test":name, "exit_code":p.returncode, "stdout_bytes":len(p.stdout),
            "stdout_sha256":sha(p.stdout), "stderr_bytes":len(p.stderr), "stderr_sha256":sha(p.stderr)}

def zipped(items):
    out = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as z:
            for name, data in items:
                z.writestr(name,data)
    return out.getvalue()

def execute():
    require(sha((SOURCE/"PUBLIC_MANIFEST.json").read_bytes()) == "18b022a9f45f4b8194629cae8143f6be4884dbba51b7616cc64c1b7ab2cf7117", "external PUBLIC_MANIFEST pin")
    require(sha((SOURCE/"verify_publication.py").read_bytes()) == "994408c8bfb602939d03a8ed674f0aa06eed1e80477a473c17ddc8566e49aea5", "external wrapper pin")
    runtime = run(["-I","-c","import json,sys,platform,sympy,importlib.util; print(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'executable':sys.executable,'sympy':sympy.__version__,'sympy_origin':sympy.__file__,'isolated':sys.flags.isolated,'optimize':sys.flags.optimize}))"])
    require(runtime.returncode == 0 and not runtime.stderr,"runtime query")
    runtime_info = json.loads(runtime.stdout)
    require(runtime_info["python"] == "3.14.6" and runtime_info["sympy"] == "1.14.0","runtime version")
    (OUT/"ENVIRONMENT.json").write_text(json.dumps(runtime_info,indent=2)+"\n")
    own = OUT/"independent_algebra.py"
    own_outputs=[]
    for mode,flags in (("normal",[]),("optimized",["-O"]),("isolated",["-I"])):
        p=run([*flags,str(own)])
        require(p.returncode == 0 and not p.stderr,"independent algebra "+mode)
        doc=json.loads(p.stdout)
        require(type(doc["canonical_math"]["alpha_square"]) is int and doc["canonical_math"]["alpha_square"]==2,"canonical exact scalar type")
        require(all(type(s) is str for s in doc["checks"]),"canonical string types")
        own_outputs.append(p.stdout)
        EVENTS.append(record_run("independent_algebra_"+mode,p))
    require(len(set(own_outputs))==1,"independent mode byte equality")
    (OUT/"INDEPENDENT_ALGEBRA_RESULT.json").write_bytes(own_outputs[0])
    with tempfile.TemporaryDirectory(dir=TMP) as temp:
        root=Path(temp)/"package"
        shutil.copytree(SOURCE,root)
        spec=importlib.util.spec_from_file_location("frozen_pr948_verifier",root/"verify_publication.py")
        verifier=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        archive_data=(root/verifier.ARCHIVE).read_bytes()
        ext=json.loads((root/verifier.EXTERNAL).read_bytes())
        with zipfile.ZipFile(io.BytesIO(archive_data)) as z:
            members=[(i.filename,z.read(i)) for i in z.infolist()]
            zip_result=[{"path":i.filename,"bytes":i.file_size,"compressed_bytes":i.compress_size,"external_mode":oct(i.external_attr>>16),"sha256":sha(z.read(i)),"mirror_equal":z.read(i)==(root/"author"/i.filename).read_bytes()} for i in z.infolist()]
        require(len(members)==7 and all(r["mirror_equal"] for r in zip_result),"seven archive mirror members")
        require({n for n,d in members}=={e["path"] for e in ext["files"]},"archive name inventory")
        (OUT/"ZIP_MEMBERS.json").write_text(json.dumps(zip_result,indent=2)+"\n")
        for mode,flags in (("normal",[]),("optimized",["-O"]),("isolated",["-I"])):
            p=run([*flags,str(root/"verify_publication.py"),"--self-test","--run-checkers"],timeout=120)
            EVENTS.append(record_run("wrapper_self_test_and_replay_"+mode,p))
            require(p.returncode==0 and not p.stderr,"wrapper mode "+mode+" failed: "+p.stderr.decode(errors="replace")[:300])
            doc=json.loads(p.stdout)
            require(type(doc["files"]) is int and doc["files"]==24,"wrapper count/type")
            require(type(doc["archive_members"]) is int and doc["archive_members"]==7,"ZIP count/type")
            require(len(doc["checker_replays"])==9 and all(r["assertions_enabled"] is True for r in doc["checker_replays"]),"wrapper replay inventory/type")
            require(len(doc["self_tests"])==17,"wrapper self-test count")
            (OUT/("WRAPPER_"+mode.upper()+".json")).write_bytes(p.stdout)
        for checker,expected in verifier.CHECKERS:
            output=[]
            for mode,flags in (("normal",[]),("optimized",["-O"]),("isolated",["-I"])):
                p=run([*flags,str(root/checker)])
                require(p.returncode==0 and p.stdout==(root/expected).read_bytes() and not p.stderr,"direct checker "+checker+mode)
                output.append(p.stdout)
                EVENTS.append(record_run("direct_"+checker+"_"+mode,p))
            require(len(set(output))==1,"checker modes unequal")
        author_doc=json.loads((root/verifier.CHECKERS[0][1]).read_bytes())
        require(type(author_doc["result"]) is str and author_doc["result"]=="pass","author result type")
        require(type(author_doc["checks"]) is list and len(author_doc["checks"])==13 and all(type(c) is str for c in author_doc["checks"]),"author check list type")

        def mutation(name,edit,accept=False):
            clone=Path(temp)/"mutated"
            shutil.copytree(root,clone)
            try:
                edit(clone)
                try:
                    result=verifier.verify(clone)
                except Exception as error:
                    record(name,outcome="rejected",exception=type(error).__name__,message=str(error))
                    require(not accept,"expected limitation acceptance: "+name)
                else:
                    record(name,outcome="accepted",result=result)
                    require(accept,"unexpected acceptance: "+name)
            finally:
                shutil.rmtree(clone)

        mutation("manifest_invalid_json",lambda p:(p/"PUBLIC_MANIFEST.json").write_text("{"))
        mutation("manifest_wrong_sidecar",lambda p:(p/"PUBLIC_MANIFEST.sha256").write_text("0"*64))
        for name,value in (("absolute","/etc/passwd"),("parent","../escape"),("backslash","a\\b"),("dot","a/./b"),("repeated_separator","a//b"),("empty","")):
            mutation("manifest_path_"+name,lambda p,value=value:verifier.rewrite_manifest(p,lambda m:m["files"][0].update(path=value)))
        mutation("manifest_null_entries",lambda p:verifier.rewrite_manifest(p,lambda m:m.update(files=None)))
        mutation("manifest_duplicate",lambda p:verifier.rewrite_manifest(p,lambda m:m["files"].append(m["files"][0])))
        mutation("manifest_wrong_git_hash",lambda p:verifier.rewrite_manifest(p,lambda m:m["files"][0].update(git_blob_sha1="0"*40)))
        mutation("manifest_wrong_sha256",lambda p:verifier.rewrite_manifest(p,lambda m:m["files"][0].update(sha256="0"*64)))
        mutation("manifest_wrong_size",lambda p:verifier.rewrite_manifest(p,lambda m:m["files"][0].update(bytes=0)))
        mutation("manifest_wrong_problem",lambda p:verifier.rewrite_manifest(p,lambda m:m.update(problem_id=30004550)))
        mutation("manifest_wrong_turn_count",lambda p:verifier.rewrite_manifest(p,lambda m:m.update(author_turns="5/5")))
        mutation("package_symlink",lambda p:(p/"owned-link").symlink_to(p/"README.md"))
        mutation("package_mode_change_not_checked",lambda p:(p/"README.md").chmod(0o755),accept=True)
        mutation("manifest_ignored_git_mode",lambda p:verifier.rewrite_manifest(p,lambda m:m["files"][0].update(git_mode="120000")),accept=True)
        mutation("manifest_integral_float_size_accepted",lambda p:verifier.rewrite_manifest(p,lambda m:m["files"][0].update(bytes=float(m["files"][0]["bytes"]))),accept=True)
        mutation("unlisted_FIFO_ignored",lambda p:os.mkfifo(p/"unlisted-fifo"),accept=True)
        # Listed FIFO demonstrates lack of regular-file check, with a strict owned-child timeout.
        clone=Path(temp)/"fifo-package"
        shutil.copytree(root,clone)
        (clone/"README.md").unlink()
        os.mkfifo(clone/"README.md")
        try:
            try:
                p=run([str(clone/"verify_publication.py")],timeout=2)
                record("listed_FIFO",outcome="returned",exit_code=p.returncode)
                require(False,"listed FIFO unexpectedly returned")
            except subprocess.TimeoutExpired:
                record("listed_FIFO",outcome="timeout",timeout_seconds=2,limitation="No regular-file check before read; not a sandbox")
        finally:
            shutil.rmtree(clone)
        # check_archive performs no extraction; attributes and decompression caps are probed directly.
        for name,items in (("zip_parent",members+[("../escape",b"x")]),("zip_duplicate",members+[members[0]]),("zip_missing",members[1:]),("zip_extra",members+[("extra",b"x")]),("zip_bad_data",[(members[0][0],members[0][1]+b"x")]+members[1:])):
            try:
                verifier.check_archive(zipped(items),ext["files"])
            except Exception as error:
                record(name,outcome="rejected",exception=type(error).__name__,message=str(error))
            else:
                require(False,name+" accepted")
        link_info=zipfile.ZipInfo(members[0][0])
        link_info.create_system=3
        link_info.external_attr=(stat.S_IFLNK|0o777)<<16
        link_zip=zipped([(link_info,members[0][1])]+members[1:])
        verifier.check_archive(link_zip,ext["files"])
        record("ZIP_symlink_attribute_ignored",outcome="accepted_direct_helper",note="Member bytes are never extracted; full verify rejects changed archive by frozen SHA")
        large=b"x"*262144
        cap_zip=zipped([("bounded.bin",large)])
        verifier.check_archive(cap_zip,[{"path":"bounded.bin","bytes":len(large),"sha256":sha(large)}])
        record("ZIP_decompression_cap_absent",outcome="accepted_direct_helper",uncompressed_bytes=len(large),compressed_bytes=len(cap_zip),note="Bounded 256KiB fixture only; original archive is externally frozen")

        mutations=[
            ("author/verification/check_deformation.py","scale(s.diff(R,t),vol)","scale(-s.diff(R,t),vol)",False),
            ("audit_a/check_algebra.py","assert wedge(alpha,alpha)=={V:2}","assert wedge(alpha,alpha)=={V:3}",True),
            ("audit_b/check_local_algebra.py","assert wedge(alpha,alpha)==scale(2,V)","assert wedge(alpha,alpha)==scale(3,V)",True),
        ]
        for checker,old,new,assert_only in mutations:
            text=(root/checker).read_text()
            require(text.count(old)==1,"unique mutation site")
            path=Path(temp)/"mutated_checker.py"
            path.write_text(text.replace(old,new))
            for mode,flags in (("normal",[]),("optimized",["-O"])):
                p=run([*flags,str(path)])
                accepted=p.returncode==0
                require(accepted==(assert_only and mode=="optimized"),"mutation rejection pattern")
                record("wrong_math_"+checker+"_"+mode,outcome="accepted" if accepted else "rejected",exit_code=p.returncode,limitation="assertions disabled" if accepted else None)
            wrapper="import sys; p=sys.argv[1]; exec(compile(open(p,'rb').read(),p,'exec',optimize=0),{'__name__':'__main__','__file__':p})"
            p=run(["-O","-c",wrapper,str(path)])
            require(p.returncode!=0,"forced optimize=0 must reject mutation")
            record("wrong_math_"+checker+"_forced_optimize0",outcome="rejected",exit_code=p.returncode)
        # The verifier protects package-local imports via an empty working directory.
        poison=Path(temp)/"poison"
        poison.mkdir()
        (poison/"sympy.py").write_text("raise RuntimeError('OWNED_IMPORT_POISON')\n")
        poisoned=dict(ENV,PYTHONPATH=str(poison))
        p=run([str(root/"author/verification/check_deformation.py")],env=poisoned)
        require(p.returncode!=0 and b"OWNED_IMPORT_POISON" in p.stderr,"ambient import probe")
        record("ambient_PYTHONPATH_not_sandboxed",outcome="controlled_poison_imported",exit_code=p.returncode)
        p=run(["-I",str(root/"author/verification/check_deformation.py")],env=poisoned)
        require(p.returncode==0 and p.stdout==(root/"author/verification/check_normal.json").read_bytes(),"isolated poison control")
        record("isolated_ignores_ambient_PYTHONPATH",outcome="pass",exit_code=p.returncode)
        p=run(["-I",str(root/"verify_publication.py"),"--run-checkers"],env=poisoned)
        require(p.returncode!=0 and b"checker failed" in p.stderr,"wrapper child environment probe")
        record("isolated_wrapper_replay_inherits_environment",outcome="controlled_poison_caused_replay_failure",exit_code=p.returncode,note="Child normal/optimized modes inherit PYTHONPATH; no sandbox claimed")
    return {"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"pass_with_explicit_limits","test_events":EVENTS,"test_event_count":len(EVENTS),"public_manifest_external_sha256":"18b022a9f45f4b8194629cae8143f6be4884dbba51b7616cc64c1b7ab2cf7117","wrapper_external_sha256":"994408c8bfb602939d03a8ed674f0aa06eed1e80477a473c17ddc8566e49aea5"}

try:
    result=execute()
except Exception as error:
    result={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"harness_failure","exception":type(error).__name__,"message":str(error),"test_events":EVENTS}
    (OUT/"REPRODUCTION_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    raise
else:
    (OUT/"REPRODUCTION_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="test_events"},indent=2))
