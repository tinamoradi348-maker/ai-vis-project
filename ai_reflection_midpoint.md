# Reflection on GenAI usage – Midpoint (end of Phase I)

**AI-aided pair in Phase I (Pair A):**
- Tina Moradi, k12455648
- Mehdi Khodadadi, k12453161

**Human-only pair in Phase I (Pair B):**
- Neda HosseinaliZadeh Shalmani, k12454244
- Reza Ghadiri, k12453160

**Team:** Classified documents · **Task:** classification of six surface-defect types on hot-rolled steel (NEU) · **Models:** ResNet-18 (fine-tuned), CLIP ViT-B/32 (zero-shot)
**AI tool used by Pair A:** Claude (Anthropic). Full record: `ai-interactions/`.

---

## 1. Shared direction agreed at the start of Phase I
- **Main question:** do the models recognize the defect, or do they rely on shortcuts such as brightness, texture or orientation?
- **Data:** the 270 test images, under 24 controlled input conditions (clean, brightness, contrast, blur, noise, rotation), plus the training images as a source of hypotheses. All predictions are in `outputs/predictions.csv` (40,050 rows).
- **Starting point:** accuracy per class and condition.
- **Agreed boundary of AI use:** see README (*Team and pairs*).

## 2. What each pair did and found

### Pair A (with AI)
- Built one interactive explorer (`phase1_pairA/explorer.html`) with six linked views and an image drill-down.
- Key findings, each checked in the explorer:
  1. ResNet-18 is 100% correct on clean images but drops to 36% with mild noise (σ = 10) and 33% with 3 px blur.
  2. Errors are systematic: each perturbation pulls predictions toward its own "sink" class (noise → patches, strong blur and low contrast → inclusion).
  3. A 90° or 270° rotation sends rolled-in scale to 0%, while 180° keeps it at 100%. In the training data, 100% of rolled-in scale images have left-right texture (the rolling direction), whereas scratches appear in both orientations (30/70) and survive rotation. The model learned the direction as part of the class.
  4. 15% of ResNet errors under perturbation have ≥ 90% confidence.
  5. Images with boxes of a second defect type are not harder (hypothesis rejected).
  6. CLIP zero-shot is near chance (26%), and its answer depends more on the prompt wording than on the image. The three prompts agree on only 2% of images.
- **Open questions for Phase II:** what in the image makes the model choose the sink classes? Does ResNet look at the defect region at all when it fails? Why does inclusion survive rotation although it is also one-directional?
- We accepted most of these findings after checking them in the explorer. We narrowed finding 3: orientation explains rolled-in scale, but not inclusion.

### Pair B (human-only)
- Built `phase1_pairB/behavior_analysis.ipynb` with pandas and seaborn: five static figures, each answering one question (what breaks, where, why, is it stable).
- Key findings:
  1. ResNet-18 drops from 1.00 on clean images to 0.22 with strong noise (σ = 30) and 0.33 with strong blur. Moderate brightness and contrast changes and a 180° rotation barely affect it.
  2. The failures are class-specific. At blur level 1, crazing and rolled-in scale fall to 0.00 while inclusion stays at 1.00. After a 90° or 270° rotation only rolled-in scale falls to 0.00.
  3. ResNet-18 confidence partly separates right from wrong (median 0.996 vs 0.41). CLIP confidence does not (median 0.45 vs 0.44).
  4. CLIP's class bias is not stable: scratches is predicted for 51% of clean images but only 4% under strong noise, where pitted surface rises to 69%.
  5. The prompt set flips CLIP's per-class recall (inclusion 0.91 with "steel" prompts, 0.00 with "ensemble").
- **Still open:** our explanations of why these errors happen are visual hypotheses; we will test them in Phase II.
- Full write-up: `phase1_pairB/ai_reflection_pairB.md`.

## 3. Comparing the two processes
| Question | Pair A (AI-aided) | Pair B (human-only) |
| --- | --- | --- |
| Insights the other pair overlooked | The cause of the rotation failure in the training data (all rolled-in scale images run left-right). Image drill-down into the "sink" classes. Images with boxes of a second defect type are not harder. | CLIP's class bias is not stable: it moves from scratches (51%) to pitted surface (69%) under strong noise. CLIP confidence gives no signal (median 0.45 correct vs 0.44 wrong). Exact per-class flip between prompt sets (inclusion 0.91 with "steel", 0.00 with "ensemble"). |
| Visualization choices | Interactive HTML explorer, six linked views, drill-down to images | Five static figures in a Jupyter notebook (pandas, seaborn): condition × model heatmap, class × condition heatmap, confidence strip plot, CLIP prediction-share heatmap, prompt-set heatmap. Each one answers one written question. |
| Breadth vs depth | Broad: all 24 conditions and both models at once; depth only on the rotation finding | Narrower: fewer views and no image drill-down, but exact numbers per class and condition. The explanations are still visual hypotheses. |
| Speed vs verification cost | Fast first version; extra time spent running, debugging and checking AI code and claims (see failure patterns) | Slower: the first version only covered clean images and had to be redone, and the pivot tables took trial and error. Little extra checking was needed, because every number was read directly from the dataframe. |
| Confidence in conclusions, and the evidence for it | Medium. The numbers are computed from the data and were checked in the explorer, but the written interpretations came from the AI and one of them failed on a counter-example (inclusion). | High for the numbers (45 or 270 images per cell, computed by hand). Lower for the "why": one model checkpoint, and no saliency or embedding evidence yet. |

## 4. Accepted, modified and rejected AI suggestions
- **Accepted:** topic and models; fixed split; no photometric augmentation; overview-first explorer.
- **Modified:** foundation notebook (crashed once, fixed); written observations (reworded where a counter-example contradicted them); axis of the direction view (rescaled after it hid data).
- **Rejected:** MVTec AD as data for the saliency analysis; letting the AI extend the analysis that Pair B does on its own.
- Details and reasons: `ai-interactions/phase1_pairA_interactions.md`.

## 5. Failure patterns of AI assistance
1. Code delivered without being run (CLIP cell crash).
2. Silent methodological flaws (noise added in color to grayscale images).
3. Misleading encodings that only show up in the rendered chart (clamped axis).
4. Suggestions that fit the current step but not the whole pipeline (MVTec for saliency).
5. Interpretations phrased as conclusions that a counter-example partly contradicts (inclusion).

## 6. Emerging best practices
1. Give the AI the exact assignment text before planning.
2. Ask for statements computed from the data instead of free-text interpretations.
3. Run every AI-written script before trusting its results.
4. Look at every rendered chart, and ask the AI to check its own render.
5. Test each AI explanation on at least one counter-example.
6. Keep the interaction log from day one.

## 7. Plan for Phase II (roles switch)
- Pair B works with AI and Pair A without AI.
- Candidate questions: saliency inside vs outside the defect box for correct vs wrong predictions, embedding projections of perturbed images (do they move toward the sink class?), and whether a CLIP linear probe removes the prompt effect.
