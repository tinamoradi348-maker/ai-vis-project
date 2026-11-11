# Midpoint progress video – plan (max. 5:00)

Required structure (Moodle): briefly introduce the problem, summarize what each pair did and found, show key visualizations (slides, notebook or UI).
**Hard limit: 5 minutes. Aim for 4:30.** Exceeding the limit costs points.

| Time | Speaker | Show on screen | What to say (~130 words per minute) |
| --- | --- | --- | --- |
| 0:00–0:40 | [name] | Title slide: team name, the six defect classes (one example image each) | Automated visual inspection is used in steel production. We ask whether vision models really recognize surface defects, or rely on shortcuts such as brightness, texture or orientation. Dataset: NEU, 1,800 images, six classes. Models: ResNet-18 fine-tuned, and CLIP used zero-shot with text prompts. |
| 0:40–1:00 | [name] | One slide: setup | Black-box setup: 270 test images under 24 controlled conditions – brightness, contrast, blur, noise, rotation. Pair A worked with Claude, Pair B without generative AI. |
| 1:00–2:30 | Pair A (Tina, Mehdi) | `phase1_pairA/explorer.html`, live | View 1 heatmap: ResNet is perfect on clean images but collapses with mild noise and blur. View 3: errors go to one "sink" class per perturbation – click noise → patches, show the images. View 6: rotation by 90° breaks rolled-in scale completely; all training images of this class run left-right, scratches appear in both directions and survive – the model learned the rolling direction as part of the class. View 5: CLIP's answer depends on the prompt, not the image. |
| 2:30–3:40 | Pair B (Neda, Reza) | Pair B's visualizations | Four steps: what breaks, where, why, is it stable. ResNet falls to 22% with strong noise and 33% with blur; the failures are class-specific (crazing and rolled-in scale under blur, rolled-in scale under 90° rotation). ResNet confidence partly separates right from wrong, CLIP confidence does not. CLIP's bias moves from scratches to pitted surface under noise and flips with the prompt set. |
| 3:40–4:20 | [name] | Comparison slide (table from `ai_reflection_midpoint.md`, section 3) | Where the pairs found the same thing and where they differed; speed vs. verification effort; one or two AI failure patterns (crashed code, colored noise). |
| 4:20–4:40 | [name] | Next-steps slide | Phase II: saliency inside vs outside the defect box for correct vs wrong predictions; embeddings of perturbed images; roles switch. |

**Recording tips**
- Record with Zoom or OBS (screen + voice); camera optional.
- Rehearse once with a timer. If you are over 4:45, cut from the Pair A explorer part first.
- Upload to Google Drive → right-click → Share → *General access: Anyone with the link (Viewer)*. Open the link in a private browser window to check that it plays without signing in.
