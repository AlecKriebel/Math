"""Root portable rebuild and negative output/input controls; copies only."""
from pathlib import Path
import datetime, hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile
P = Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr781_4600024/tmp/preprint-workspace/preprint")
PIN = "c893760f12971fd4a36e695996304885bb5a927d7fd8cb68cd99fea78808f66e"
def sha(raw): return hashlib.sha256(raw).hexdigest()
def need(value, message):
    if not value: raise ValueError(message)
def tree(root): return {p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob("*") if p.is_file()}
before=tree(P/"source"); release=json.loads((P/"RELEASE_INVENTORY.json").read_text());results=[]
with tempfile.TemporaryDirectory(prefix="root-portable-guards-",dir=P/"tmp") as d:
    work=Path(d); source=work/"source";source.mkdir()
    with zipfile.ZipFile(P/"source-and-verification.zip") as z:
        names=z.namelist();need(len(names)==150 and len(names)==len(set(names)),"archive closure")
        for name in names:
            need(not name.startswith("/") and ".." not in Path(name).parts,"unsafe source member")
            target=source/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(name))
    need(tree(source)==before,"portable source differs")
    pdf=work/"paper.pdf";pdf.write_bytes((P/"output/pdf/paper.pdf").read_bytes())
    for optimized in [False,True]:
        flags=[sys.executable]+(["-O"] if optimized else [])+["-B"]
        out=work/("positive"+str(optimized))
        cmd=flags+[str(source/"build_package.py"),"--expected-manifest-sha256",PIN,"--pdf",str(pdf),"--output-dir",str(out)]
        r=subprocess.run(cmd,capture_output=True,text=True)
        need(r.returncode==0,r.stdout+r.stderr)
        for row in release["files"]:
            need(sha((out/row["path"]).read_bytes())==row["sha256"],"portable output differs")
        need((out/"RELEASE_INVENTORY.json").read_bytes()==(P/"RELEASE_INVENTORY.json").read_bytes(),"release receipt differs")
        results.append({"case":"portable_exact_six_rebuild","optimized":optimized,"result":"PASS"})
        for case in ["destination_symlink","destination_fifo","protected_hardlink","ancestor_symlink",
                     "inside_source","destination_directory","multiply_linked_destination"]:
            base=work/(case+str(optimized));base.mkdir();target=base/"out";target.mkdir()
            protected=base/"sentinel";protected.write_bytes(b"owned sentinel\n");saved=protected.read_bytes()
            if case=="destination_symlink":(target/"paper.tex").symlink_to(protected)
            elif case=="destination_fifo":os.mkfifo(target/"RELEASE_INVENTORY.json")
            elif case=="protected_hardlink":os.link(source/"paper.tex",target/"zenodo-upload-kit.zip")
            elif case=="ancestor_symlink":
                link=base/"link";link.symlink_to(target,target_is_directory=True);target=link
            elif case=="inside_source":target=source
            elif case=="destination_directory":(target/"source-and-verification.zip").mkdir()
            elif case=="multiply_linked_destination":os.link(protected,target/"zenodo-deposit.json")
            cmd=flags+[str(source/"build_package.py"),"--expected-manifest-sha256",PIN,"--pdf",str(pdf),"--output-dir",str(target)]
            r=subprocess.run(cmd,capture_output=True,text=True)
            need(r.returncode!=0 and "ValueError:" in r.stderr,"negative accepted:"+case)
            need(protected.read_bytes()==saved and tree(source)==before,"protected input changed")
            if case not in ["inside_source","ancestor_symlink"]:
                # No completed paper output may precede a later target's rejection.
                if case!="destination_symlink":need(not (target/"paper.tex").exists(),"partial batch wrote")
            results.append({"case":case,"optimized":optimized,"result":"REJECTED_BEFORE_BATCH_WRITE",
                            "reason":r.stderr.splitlines()[-1]})
        copied=work/("helper-tamper"+str(optimized));shutil.copytree(source,copied)
        helper=copied/"build_package.py";helper.write_bytes(helper.read_bytes()+b"\nraise RuntimeError('untrusted helper executed')\n")
        r=subprocess.run(flags+[str(copied/"verify_bundle.py"),"--expected-manifest-sha256",PIN],capture_output=True,text=True)
        need(r.returncode!=0 and json.loads(r.stdout)["error"]=="Builder binding differs","unauthenticated helper executed")
        results.append({"case":"tampered_helper_before_import","optimized":optimized,"result":"REJECTED_BEFORE_IMPORT"})
need(tree(P/"source")==before,"original source changed")
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS",
         "source_manifest_sha256":PIN,"cases":results,"case_count":len(results),
         "portable_exact_six_rebuilds":2,"negative_controls":16,"closed_source_unchanged":True,
         "scope":"Exact frozen PDF reused; source/kit/metadata consistency and selected write/import guards, not compilation or theorem proof"}
(P/"ROOT_PORTABLE_REBUILD_AND_GUARDS.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
