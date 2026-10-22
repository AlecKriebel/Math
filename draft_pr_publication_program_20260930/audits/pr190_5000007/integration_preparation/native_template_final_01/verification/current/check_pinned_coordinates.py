"""Check the separate displayed-coordinate inconsistency in the pinned public text."""
from fractions import Fraction as F
import json
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def main():
    aa=(F(31,2),F(13,2));bb=(F(-17),F(-8));phi=(F(1,2),F(1,2))
    actual=add(add(mul(aa,aa),mul(phi,mul(aa,bb))),mul(bb,bb))
    advertised=(F(307,2),F(137,2))
    difference=add(actual,(-advertised[0],-advertised[1]))
    if actual!=(F(425,2),F(189,2)) or difference!=(F(59),F(26)):
        raise ValueError("Exact pinned-coordinate norm falsification failed")
    return {"actual_displayed_coordinate_norm":[str(x) for x in actual],"advertised_face_word_norm":[str(x) for x in advertised],"difference":[str(x) for x in difference],"scope":"Displayed coordinates are inconsistent; the independently reconstructed face word is separately valid."}
if __name__=="__main__":print(json.dumps(main(),indent=2))

