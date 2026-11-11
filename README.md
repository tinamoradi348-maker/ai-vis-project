# Do vision models really detect steel defects, or do they learn shortcuts?

**Team: Classified documents**

Group project for **AI and Visualization (JKU Linz, WS 2026)**.

We study two models on the NEU Surface Defect Database (6 defect classes of hot-rolled steel):

- **ResNet-18**: ImageNet-pretrained, fine-tuned on NEU
- **CLIP ViT-B/32**: zero-shot with text prompts

**Phase I – How does the model behave?** (black box): perturbations, counterfactuals and prompt variations, explored with investigative visualizations.
**Phase II – What did the model learn?** (inside the model): Grad-CAM saliency measured against the defect bounding boxes, and embedding projections.

## Team and pairs

Team: **Classified documents** · Team details: `team-info.json` · Workload: `workload.json`

| | Pair A | Pair B |
| --- | --- | --- |
| Members | Tina Moradi, Mehdi Khodadadi | Neda HosseinaliZadeh Shalmani, Reza Ghadiri |
| Phase I | with AI | without AI |
| Phase II | without AI | with AI |

**Without AI** means: single-line IDE autocomplete and documentation search only. No AI chat, no AI code generation, no AI design brainstorming, no AI interpretation of visualizations, no AI-generated images. Turn off chat and multi-line suggestions in your IDE before working in this condition.

Every AI interaction (and every foundation step done with AI) is recorded in `ai-interactions/`. The Phase I reflection is in `ai_reflection_midpoint.md`.

## Repository structure

```
README.md                  task, models, dataset
team-info.json             team details (course template)
workload.json              workload per member (course template)
ai_reflection_midpoint.md  Phase I reflection on GenAI use
ai-interactions/           AI interaction records (log + readable summaries)
data/
  split.csv       fixed stratified split, seed 42: 210 train / 45 val / 45 test per class
  boxes.csv       all 4,189 defect bounding boxes (normalized + pixel coordinates)
  raw/            extracted images (created by the notebook, not in git)
notebooks/
  01_foundation.ipynb   shared foundation: training, CLIP, perturbations -> outputs/predictions.csv
outputs/
  predictions.csv, train_history.csv   shared starting point for both pairs
phase1_pairA/   Phase I, AI-aided: explorer.html (open in a browser), build_explorer.py
phase1_pairB/   Phase I, human-only
phase2_pairA/  phase2_pairB/
docs/
  video_script_midpoint.md  plan for the midpoint video
requirements.txt
```

## Setup (local, Windows / Anaconda)

Open **Anaconda Prompt** and run once:

```
cd "PATH\TO\ai-vis-project"
conda create -n aivis python=3.11 -y
conda activate aivis
pip install -r requirements.txt
```

Every later session: `conda activate aivis`, then `jupyter lab` from the repo folder.

## How to run the foundation notebook

The notebook detects automatically whether it runs locally or on Colab.

**Locally (no GPU needed, ~20–40 min on CPU):** put `NEU-CLS.zip` into `data/` (or one folder above the repo), open `notebooks/01_foundation.ipynb` in Jupyter Lab and run all cells. Outputs land in `outputs/`.

**Google Colab (free GPU, ~10–15 min):** upload `NEU-CLS.zip` and `data/split.csv` to Google Drive → *My Drive* → `AI-Vis-Project`, upload the notebook to Colab, set **Runtime → Change runtime type → T4 GPU**, then **Run all**. Copy `predictions.csv` and `train_history.csv` from Drive into `outputs/` and commit them.

Only one person needs to run it. Everyone else pulls `outputs/predictions.csv` from GitHub.

## Working together (GitHub Desktop)

1. Install GitHub Desktop and sign in.
2. Owner: *File → Add local repository* → this folder → publish to `ai-vis-project`. Teammates: *File → Clone repository* → `ai-vis-project`.
3. Before you start working: **Fetch / Pull**. After a work session: **Commit** (short message saying what you did) → **Push**.
4. Each pair edits only its own `phase*_pair*` folder; shared files (`README.md`, `data/`, `notebooks/01_foundation.ipynb`) are changed only after telling the group.
5. The record log (`ai-interactions/AI_Vis_Record_Log.xlsx`) is an Excel file and cannot be merged: one person at a time edits it, then commits and pushes right away.

## Data notes

- 1,800 images (300 per class), 200×200 px, grayscale stored as RGB. Labels in YOLO format (`class cx cy w h`, normalized).
- The image-level class is taken from the file name. **123 images contain 188 boxes whose class differs from the file name** (e.g. `scratches` images with `inclusion` boxes). `boxes.csv` keeps both: `true_class` (image) and `box_class` (box), plus `matches_image_class`.
- The provided `valid` folder has only 30 images, so we use our own split in `data/split.csv`.

## Dataset citation

K. Song and Y. Yan, "A noise robust method based on completed local binary patterns for hot-rolled steel strip surface defects", *Applied Surface Science*, 285:858–864, 2013.
Download source used: SOURCE_URL (fill in).
