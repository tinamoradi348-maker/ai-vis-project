# AI interaction record – Phase I (AI-aided pair: Pair A)

**Tool:** Claude (Anthropic), one continuous chat session in Persian, 15 Oct – 11 Nov 2026.
**Full structured log:** `AI_Vis_Record_Log.xlsx` in this folder (sheet *Log*; the *Summary* sheet counts entries, decisions and issues per pair and phase).
This file lists the interactions that influenced the analysis, in the order they happened. Prompts are translated from Persian; quotes are shortened.

> Entries marked **[Pair A]** are decisions that only we can make. They must be filled in before submission.

---

## Foundation (shared by both pairs, AI allowed for both)

| ID | Our request (translated) | What the AI produced | Our decision and why |
| --- | --- | --- | --- |
| F-1 | "Which topic and model should our group choose to get a good grade, and where do we get data?" | Proposed steel-defect classification on NEU with ResNet-18 + CLIP; listed NEU, MVTec AD and Severstal as data options | Accepted. Fits our industrial background, runs on a laptop, has defect boxes for a quantitative Phase II. |
| F-2 | (same conversation) | First hypotheses: lighting/contrast, background counterfactuals, CLIP prompt wording, saliency inside the defect box | Refined: used only as starting ideas. **These hypotheses originate from AI**, which also affects the human-only pair's starting point. |
| F-3 | "Download the data into my folder and prepare it." | Found that the downloaded zip already contained boxes for all 1,800 images; built `data/split.csv` (stratified 70/15/15, seed 42) and `data/boxes.csv` | Accepted. The AI also found that 123 images carry 188 boxes of another class (a data-quality finding). |
| F-4 | "Set up Colab and run everything you can." | `notebooks/01_foundation.ipynb`: ResNet-18 fine-tuning without photometric augmentation, CLIP zero-shot with 3 prompt sets + ensemble, 24 test conditions → `outputs/predictions.csv` | Refined. First run crashed in the CLIP cell (see *Failure patterns*); fixed after one round. |
| F-5 | "Create the GitHub repository structure." | README, `.gitignore`, `requirements.txt`, one folder per pair | Accepted. |

## Phase I – Pair A (with AI)

| ID | Our request (translated) | What the AI produced | Our decision and why |
| --- | --- | --- | --- |
| P1-A1 | "I am in Pair A – take the project as far as you can." | Pandas exploration of `predictions.csv`: perturbation-specific "sink" classes, rotation 90°/270° breaks rolled-in scale, mixed-box images not harder, CLIP answers driven by the prompt | **[Pair A]** accept / refine / reject each finding |
| P1-A2 | (same request) | Interactive `phase1_pairA/explorer.html`: class × condition heatmap, small-multiple robustness curves, confusion matrix with image drill-down, confidence strip plot, CLIP prompt heatmap | **[Pair A]** which views we keep, and why |
| P1-A3 | (same request) | Seven written observations, computed from the data so they update automatically | **[Pair A]** which statements we verified ourselves |
| P1-A4 | "What do we need for the midpoint?" | Proposed to go deeper on the rotation finding: measured texture direction in all training images (view 6) | **[Pair A]** accept / refine / reject |

### How the AI suggestions changed our analytical decisions
- **Direction of the investigation:** the AI proposed perturbations as the main Phase I lens. This became the shared direction for both pairs.
- **From pattern to explanation:** after the AI found the rotation failure, it proposed checking the *training data* for a cause. This turned a surprising observation into an explanation: rolled-in scale only ever appears with left-right texture in training.
- **Design choices we kept from the AI:** no photometric augmentation during training (so robustness tests measure what the model learned), overview-first layout with drill-down to images.
- **[Pair A]** add where we disagreed with the AI or changed its direction.

---

## Failure patterns observed during AI-assisted analysis

| # | What happened | How it was caught | Lesson |
| --- | --- | --- | --- |
| 1 | **Code that was never run.** The foundation notebook crashed in the CLIP cell (`.numpy()` on a tensor requiring grad, because `logit_scale` is a parameter). | Only when we ran it on Colab. The AI could not execute it in its own environment. | AI-written code is a draft until it has run once on real data. |
| 2 | **Silent design flaw.** Gaussian noise was added per RGB channel, turning grayscale images into colored ones. Part of the large noise effect may be a color effect. | The AI flagged it only after seeing the results, not when writing the code. | Ask the AI explicitly to list the assumptions behind each perturbation before running it. |
| 3 | **Misleading encoding.** The first version of view 6 clamped the axis at 15%, hiding that 30% of scratches images run left-right – the key evidence for the explanation. | The AI rendered and inspected the page itself. | Always look at the rendered chart; a correct-looking script can still hide the data. |
| 4 | **Plausible but wrong recommendation.** Early on the AI suggested MVTec AD for measuring saliency, but a model trained on NEU cannot classify MVTec images. | The AI corrected itself later. | Check whether a suggestion fits the whole pipeline, not only the current step. |
| 5 | **Confident interpretations.** The written observations read like conclusions. One of them (orientation as the cause) holds for rolled-in scale but not for inclusion, which is also one-directional yet survives rotation (84%). | Visible only when the explanation was tested on a second class. | Treat AI interpretations as hypotheses; test each on a counter-example. |
| 6 | **Overreach in scope.** The AI wanted to deepen analyses that the human-only pair should develop on their own. | We kept Pair B's work separate; the AI declined to do Pair B's part. | Agree on the boundary of AI use at the start and write it down (README). |

## Emerging best practices
1. Give the AI the exact assignment text. Its plan improved once it saw the official requirements.
2. Ask for computed statements, not prose: our observations are computed from the data, so they stay true if the predictions change.
3. Run every AI-written script before trusting any result from it, and log the failure if it breaks.
4. Make the AI render and look at its own visualizations; two of our fixes came from that check.
5. Keep a running log from day one – reconstructing prompts afterwards is unreliable.
6. **[Pair A]** add our own practices.
