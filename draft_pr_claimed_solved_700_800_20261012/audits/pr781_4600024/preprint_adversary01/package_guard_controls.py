"""Independent physical output controls; copied inputs and owned outputs only."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile
PIN="c893760f12971fd4a36e695996304885bb5a927d7fd8cb68cd99fea78808f66e"
def need(c,m):
    if not c:raise ValueError(m)
def inventory(p):
    return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in p.rglob("*") if f.is_file()}
def main():
    a=argparse.ArgumentParser();a.add_argument("--input-root",required=True,type=Path)
    a.add_argument("--scratch",required=True,type=Path);x=a.parse_args();rows=[]
    for optimized in [False,True]:
        for case in ["late_fifo","late_symlink","protected_hardlink","ancestor_symlink","inside_source","destination_directory"]:
            with tempfile.TemporaryDirectory(prefix="review01-build-",dir=x.scratch) as temp:
                b=Path(temp);source=b/"source";shutil.copytree(x.input_root/"source",source)
                pdf=b/"paper.pdf";pdf.write_bytes((x.input_root/"output/pdf/paper.pdf").read_bytes())
                out=b/"output";out.mkdir();sent=b/"sentinel";sent.write_bytes(b"owned sentinel\n")
                if case=="late_fifo":os.mkfifo(out/"RELEASE_INVENTORY.json")
                elif case=="late_symlink":(out/"zenodo-upload-kit.zip").symlink_to(sent)
                elif case=="protected_hardlink":os.link(source/"paper.tex",out/"zenodo-deposit.json")
                elif case=="ancestor_symlink":
                    link=b/"link";link.symlink_to(out,target_is_directory=True);out=link
                elif case=="inside_source":out=source
                elif case=="destination_directory":(out/"source-and-verification.zip").mkdir()
                before=inventory(source);saved=sent.read_bytes()
                cmd=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])+[str(source/"build_package.py"),"--expected-manifest-sha256",PIN,"--pdf",str(pdf),"--output-dir",str(out)]
                v=subprocess.run(cmd,capture_output=True,text=True,timeout=8)
                need(v.returncode!=0,"Accepted bad output:"+case)
                need(inventory(source)==before and sent.read_bytes()==saved,"Protected bytes changed:"+case)
                if case not in ["inside_source","ancestor_symlink"]:
                    need(not (out/"paper.tex").exists(),"Partial batch written:"+case)
                rows.append({"case":case,"optimized":optimized,"returncode":v.returncode,
                             "source_and_sentinel_unchanged":True,"last_error":v.stderr.splitlines()[-1]})
    print(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","cases":rows},indent=2))
if __name__=="__main__":main()
