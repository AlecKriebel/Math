"""Reproduce read-guard outcomes on owned copies; never mutate the package."""
from pathlib import Path
import argparse,datetime,json,os,shutil,subprocess,sys,tempfile
PIN="c893760f12971fd4a36e695996304885bb5a927d7fd8cb68cd99fea78808f66e"
def main():
    a=argparse.ArgumentParser();a.add_argument("--input-root",type=Path,required=True)
    a.add_argument("--scratch",type=Path,required=True);args=a.parse_args()
    p=args.input_root;s=args.scratch;s.mkdir(parents=True,exist_ok=True);rows=[]
    for optimized in [False,True]:
        for case in ["manifest_fifo","pdf_fifo","helper_fifo","manifest_directory","helper_symlink","root_symlink","ancestor_symlink"]:
            with tempfile.TemporaryDirectory(prefix="pr781-read-guard-",dir=s) as temp:
                base=Path(temp);source=base/"source";shutil.copytree(p/"source",source)
                script=source/"verify_bundle.py";extra=[]
                if case=="manifest_fifo":
                    f=source/"MANIFEST.json";f.unlink();os.mkfifo(f)
                elif case=="pdf_fifo":
                    f=base/"paper.pdf";os.mkfifo(f);extra=["--pdf",str(f)]
                elif case=="helper_fifo":
                    f=source/"build_package.py";f.unlink();os.mkfifo(f)
                elif case=="manifest_directory":
                    f=source/"MANIFEST.json";f.unlink();f.mkdir()
                elif case=="helper_symlink":
                    f=source/"build_package.py";d=f.read_bytes();f.unlink();g=base/"helper.py";g.write_bytes(d);f.symlink_to(g)
                elif case=="root_symlink":
                    link=base/"link";link.symlink_to(source,target_is_directory=True);script=link/"verify_bundle.py"
                elif case=="ancestor_symlink":
                    link=base/"link";link.symlink_to(base,target_is_directory=True);script=link/"source/verify_bundle.py"
                cmd=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])+[str(script),"--expected-manifest-sha256",PIN]+extra
                try:
                    v=subprocess.run(cmd,capture_output=True,text=True,timeout=2)
                    rows.append({"case":case,"optimized":optimized,"returncode":v.returncode,"stdout":v.stdout,"stderr":v.stderr})
                except subprocess.TimeoutExpired:
                    rows.append({"case":case,"optimized":optimized,"outcome":"TIMEOUT","seconds":2})
    print(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"cases":rows},indent=2))
if __name__=="__main__":main()
