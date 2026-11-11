### Pair B (Without AI) – Workflow & Findings

**How we approached Phase I**
In our first attempt, we only plotted standard performance metrics (like confusion matrices and class accuracy) on the clean test images. Since ResNet-18 got 100% on the clean test set (270 images), those plots didn't really tell us anything about how the model actually works or fails. After discussing the rubric with the team, we redid our notebook using `pandas` and `seaborn` to look at the full `predictions.csv` file across all 23 perturbation conditions (plus the clean baseline, 45 images per class). 

We tried to follow a simple step-by-step logic for our plots: first see which perturbations break the models, then check which specific classes fail, look at whether confidence scores are reliable, and finally test if CLIP's behavior is stable across different prompts.

**Main Findings**

**1. Where does accuracy drop? (`accuracy_by_perturbation.png`)**
ResNet-18 gets 1.00 accuracy on clean images, but drops badly on Gaussian noise (0.36 at sigma 10, 0.23 at sigma 20, and 0.22 at sigma 30—which is close to random guessing at 0.167). It also struggles with Gaussian blur, dropping to 0.57, 0.40, and 0.33 from level 1 to 3. On the other hand, changing brightness (0.6 to 1.2), contrast (0.6 to 1.6), or rotating by 180° and 15° barely affects it (accuracy stays >= 0.99, except at extreme low contrast 0.4 where it drops to 0.66). 90° and 270° rotations bring accuracy down to 0.81 and 0.83.
CLIP (with ensemble prompts) stays between 0.17 and 0.32 everywhere. The line looks flat, but only because the model is already performing near the floor on clean data.

**2. Which defect classes are most sensitive? (`resnet_class_by_perturbation.png`)**
When we plotted a heatmap of `true_class × perturbation` for ResNet-18, we saw that errors don't happen evenly across classes:
- **Blur:** `crazing` and `rolled-in_scale` drop to 0.00 right away at blur level 1, whereas `inclusion` stays at 1.00 across all blur levels and `scratches` stays >= 0.96.
- **Noise:** `crazing`, `inclusion`, and `rolled-in_scale` hit 0.00 across all noise levels, and `scratches` goes from 0.53 down to 0.00. However, `patches` (0.58–0.78) and `pitted_surface` (0.60–0.87) still hold up reasonably well. Looking at what ResNet actually predicts at noise level 30, it predicts almost only `patches` (69% of all images) and `pitted_surface` (31%).
- **Rotation:** 90° and 270° rotations completely break `rolled-in_scale` (drops from 1.00 to 0.00), while a 180° flip keeps it at 1.00. Other classes stay above 0.84.
- *Our interpretation:* Looking at the raw images, `crazing` and `rolled-in_scale` have very fine surface details that get wiped out when blurred. Gaussian noise adds grainy dots over the image, which probably looks similar to `pitted_surface` or `patches` to the model. Also, `rolled-in_scale` defects seem to follow a specific horizontal/vertical rolling direction—rotating by 180° keeps the same axis, but 90° or 270° flips it perpendicular to what the model saw during training.

**3. Can we trust model confidence? (`confidence_correct_vs_wrong.png`)**
For ResNet-18, mostly yes: across all 6,480 test predictions, correct answers have a mean confidence of 0.940 (median 0.996) while wrong ones average 0.511 (median 0.410). Still, under heavy noise or 90° rotation, there are several wrong predictions with high confidence (> 0.80).
For CLIP, confidence doesn't help at all: correct predictions average 0.475 (median 0.448) and wrong ones average 0.460 (median 0.436). The scores sit around 0.44–0.48 either way.

**4. Does CLIP always have the same class bias? (`clip_prediction_share.png`)**
Not across perturbations. On clean images (using `ensemble` prompts), CLIP heavily favors `scratches` (predicting it 51% of the time) and `pitted_surface` (31%), while never predicting `inclusion`. But under heavy noise (sigma 30), `scratches` predictions drop to 4% and `pitted_surface` jumps to 69% (with `crazing` at 13% and `inclusion` at 10%).

**5. How much do text prompts matter for CLIP? (`clip_prompt_sets.png`)**
We compared the four prompt sets (`plain`, `steel`, `defect`, `ensemble`) on clean images. Overall accuracy is low for all of them (0.18 to 0.26), but the class predictions flip completely depending on the wording. With `steel` prompts, `inclusion` gets 0.91 recall and `pitted_surface` gets 0.04. With `ensemble` prompts, `inclusion` drops to 0.00 while `pitted_surface` goes up to 0.89. This shows zero-shot CLIP is very sensitive to small wording changes on industrial images.

**Limitations & Challenges**
- Coding the pivot tables and sorting the 24 conditions manually in Pandas/Seaborn took some trial and error with the syntax, though it forced us to check the dataframe values directly.
- Each cell in the class heatmap only has 45 test images from a single model run.
- Our explanations for *why* blur, noise, and 90° rotations cause these specific errors are visual hypotheses for now—we plan to test them with Grad-CAM and embeddings in Phase II.