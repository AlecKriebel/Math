"""Independent PR786 package guards, rebuild and custody mutations; owned copies only."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
PIN="32d7a891fa5ad3ff49269865e122f5ed3327da4fe83b3344738d958130bcf38b"
def need(c,m):
    if not c:raise ValueError(m)
def tree(p):
    return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in p.rglob("*") if f.is_file()}
def main():
    a=argparse.ArgumentParser();a.add_argument("--frozen",required=True,type=Path)
    a.add_argument("--source",required=True,type=Path);a.add_argument("--scratch",required=True,type=Path);x=a.parse_args()
    release=json.loads((x.frozen/"RELEASE_INVENTORY.json").read_text())
    rows=[]
    for optimized in [False,True]:
        flags=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])
        with tempfile.TemporaryDirectory(prefix="pr786-rebuild-",dir=x.scratch) as temp:
            out=Path(temp)/"output"
            cmd=flags+[str(x.source/"build_package.py"),"--expected-manifest-sha256",PIN,
                 "--pdf",str(x.frozen/"output/pdf/paper.pdf"),"--output-dir",str(out)]
            v=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
            need(v.returncode==0,v.stderr)
            for row in release["files"]:
                need((out/row["path"]).read_bytes()==(x.frozen/row["path"]).read_bytes(),"Rebuild differs:"+row["path"])
            need((out/"RELEASE_INVENTORY.json").read_bytes()==(x.frozen/"RELEASE_INVENTORY.json").read_bytes(),"Release differs")
            rows.append({"case":"exact_six_rebuild","optimized":optimized,"result":"PASS"})
        for case in ["manifest_fifo","helper_fifo","pdf_fifo","extra_fifo","manifest_symlink","helper_tamper",
                     "source_content_tamper","wrong_pin","output_late_fifo","output_symlink","output_hardlink",
                     "output_ancestor_symlink","output_inside_source"]:
            with tempfile.TemporaryDirectory(prefix="pr786-guard-",dir=x.scratch) as temp:
                b=Path(temp);source=b/"source";shutil.copytree(x.source,source)
                pdf=b/"paper.pdf";pdf.write_bytes((x.frozen/"output/pdf/paper.pdf").read_bytes())
                out=b/"output";out.mkdir();sent=b/"sentinel";sent.write_bytes(b"owned sentinel\n")
                pin=PIN;kind="read"
                if case=="manifest_fifo":f=source/"MANIFEST.json";f.unlink();os.mkfifo(f)
                elif case=="helper_fifo":f=source/"build_package.py";f.unlink();os.mkfifo(f)
                elif case=="pdf_fifo":pdf.unlink();os.mkfifo(pdf)
                elif case=="extra_fifo":os.mkfifo(source/"extra.fifo")
                elif case=="manifest_symlink":
                    f=source/"MANIFEST.json";s=b/"manifest";s.write_bytes(f.read_bytes());f.unlink();f.symlink_to(s)
                elif case=="helper_tamper":
                    f=source/"build_package.py";f.write_bytes(f.read_bytes()+b"\nraise RuntimeError('BAD_HELPER_EXECUTION')\n")
                elif case=="source_content_tamper":
                    f=source/"paper.tex";f.write_bytes(f.read_bytes()+b"X")
                elif case=="wrong_pin":pin="0"*64
                elif case=="output_late_fifo":os.mkfifo(out/"RELEASE_INVENTORY.json");kind="write"
                elif case=="output_symlink":(out/"zenodo-upload-kit.zip").symlink_to(sent);kind="write"
                elif case=="output_hardlink":os.link(source/"paper.tex",out/"zenodo-deposit.json");kind="write"
                elif case=="output_ancestor_symlink":
                    f=b/"link";f.symlink_to(out,target_is_directory=True);out=f;kind="write"
                elif case=="output_inside_source":out=source;kind="write"
                if kind=="read":
                    cmd=flags+[str(source/"verify_bundle.py"),"--expected-manifest-sha256",pin,"--pdf",str(pdf)]
                else:
                    cmd=flags+[str(source/"build_package.py"),"--expected-manifest-sha256",pin,"--pdf",str(pdf),"--output-dir",str(out)]
                saved=sent.read_bytes()
                # Only regular-file digests are inventoried. FIFO cases must reject promptly.
                before={str(f.relative_to(source)):hashlib.sha256(f.read_bytes()).hexdigest()
                        for f in source.rglob("*") if f.is_file()}
                v=subprocess.run(cmd,capture_output=True,text=True,timeout=4)
                need(v.returncode!=0,"Negative accepted:"+case)
                need("BAD_HELPER_EXECUTION" not in v.stdout+v.stderr,"Untrusted helper executed")
                after={str(f.relative_to(source)):hashlib.sha256(f.read_bytes()).hexdigest()
                       for f in source.rglob("*") if f.is_file()}
                need(before==after and sent.read_bytes()==saved,"Protected source changed:"+case)
                if kind=="read":
                    need(json.loads(v.stdout)["result"]=="FAIL","Missing structured failure")
                elif case not in ["output_inside_source","output_ancestor_symlink"]:
                    need(not(out/"paper.tex").exists(),"Partial output wrote before preflight")
                rows.append({"case":case,"optimized":optimized,"result":"REJECTED","returncode":v.returncode,
                             "protected_regular_bytes_unchanged":True})
    print(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS",
                      "cases":rows,"positive_rebuilds":2,"negative_cases":26},indent=2))
if __name__=="__main__":main()
