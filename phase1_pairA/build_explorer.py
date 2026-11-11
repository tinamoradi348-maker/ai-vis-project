"""Build phase1_pairA/explorer.html from outputs/predictions.csv.
Usage (from the repo root):
  python phase1_pairA/build_explorer.py outputs/predictions.csv data/boxes.csv data/raw phase1_pairA/explorer.html
"""
import sys, json, base64, io, glob, os
import pandas as pd, numpy as np
from PIL import Image
pred_csv, boxes_csv, img_root, out = sys.argv[1:5]
CLASSES=["crazing","inclusion","patches","pitted_surface","rolled-in_scale","scratches"]
d=pd.read_csv(pred_csv,keep_default_na=False,na_values=[""])
d["mk"]=np.where(d.model=="ResNet-18","resnet","clip_"+d.prompt_set.astype(str))
MODELS=["resnet","clip_ensemble","clip_defect","clip_steel","clip_plain"]
t=d[d.split=="test"].copy()
conds=t[["perturbation","level"]].drop_duplicates()
order={"clean":0,"brightness":1,"contrast":2,"blur":3,"noise":4,"rotation":5,"rotation_small":6}
conds=conds.assign(o=conds.perturbation.map(order)).sort_values(["o","level"])
COND=[(p,float(l)) for p,l in zip(conds.perturbation,conds.level)]
cidx={c:i for i,c in enumerate(COND)}
imgs=sorted(t.image.unique(), key=lambda s:(CLASSES.index(s.rsplit("_",1)[0]), int(s.rsplit("_",1)[1].split(".")[0])))
iidx={s:i for i,s in enumerate(imgs)}
b=pd.read_csv(boxes_csv); mixed=set(b[~b.matches_image_class].image)
rows=[]
for r in t.itertuples():
    rows.append([iidx[r.image], MODELS.index(r.mk), cidx[(r.perturbation,float(r.level))], CLASSES.index(r.pred_class), round(float(r.confidence),3), 0.0])
# true-class prob: itertuples renames columns with '-', so compute separately
P=t[[f"p_{c}" for c in CLASSES]].to_numpy()
tc=t.true_class.map(CLASSES.index).to_numpy()
ptrue=P[np.arange(len(t)),tc]
for i,row in enumerate(rows): row[5]=round(float(ptrue[i]),3)
thumbs={}
paths={os.path.basename(p):p for p in glob.glob(os.path.join(img_root,"**","*.jpg"),recursive=True)}
for s in imgs:
    im=Image.open(paths[s]).convert("L").resize((96,96))
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=72); thumbs[s]="data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()

def h_share(path):
    """Share of horizontal-gradient energy: <0.5 = texture runs mainly left-right, >0.5 = mainly up-down."""
    a=np.asarray(Image.open(path).convert("L"),dtype=np.float32)
    gx=a[:,2:]-a[:,:-2]; gy=a[2:,:]-a[:-2,:]
    ex,ey=float((gx*gx).mean()),float((gy*gy).mean())
    return round(ex/(ex+ey),4)
sp=pd.read_csv(os.path.join(os.path.dirname(boxes_csv),"split.csv"))
orient=[[CLASSES.index(r.true_class), h_share(paths[r.image]), r.split] for r in sp.itertuples() if r.split in ("train","test")]
data=dict(orient=orient, classes=CLASSES, models=MODELS, conds=COND, images=imgs,
          img_class=[CLASSES.index(s.rsplit("_",1)[0]) for s in imgs],
          img_mixed=[s in mixed for s in imgs], rows=rows, thumbs=[thumbs[s] for s in imgs])
tpl=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"explorer_template.html"),encoding="utf-8").read()
open(out,"w",encoding="utf-8").write(tpl.replace("__DATA__",json.dumps(data,separators=(",",":"))))
print(len(rows),"rows", len(COND),"conds", len(imgs),"images", round(os.path.getsize(out)/1e6,2),"MB")
