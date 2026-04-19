# 1. Introduction

Human memory does not encode all experiences equally. Instead, certain moments are remembered better than others. One factor that strongly influences memory encoding is **event boundaries**—the moments when one meaningful activity or scene transitions into another. According to event segmentation theory, these transitions trigger an update of the brain’s internal model of the ongoing situation, which strengthens memory encoding for information occurring near these boundaries.

This study examines how event boundaries influence memory using short video clips. Participants viewed videos under two conditions: **Natural Cut (NB)**, where videos preserved their natural event boundaries, and **Abrupt Cut (AB)**, where videos were interrupted 1–5 seconds before a natural boundary and resumed in a new event context. This manipulation disrupts the natural boundary update process.

After viewing the videos, participants completed a recognition test in which they identified previously seen frames (**targets**) among unseen frames (**lures**). Targets were drawn either from **before event boundaries (BB)** or from the **middle of events (EM)**, allowing us to examine how boundary disruption affects memory encoding.
Below is a **cleaned, concise, and report-ready version** of your **Domain Background** section. I kept the academic tone, improved clarity, removed repetition, and made it suitable for a **cognitive science / psychology experimental report**.

---

# 1.2. Domain Background

## 1.2.1 How the Brain Segments Experience


Although human experience feels continuous, the brain organizes it into discrete units called **events**. An **event** is a meaningful segment of time and space with a clear beginning and end (Zacks & Tversky, 2001). These events can be hierarchically structured—for example, eating a meal is a large event, while taking a bite is a smaller event within it.

The process of identifying where one event ends and another begins is called **event segmentation**, and it occurs automatically during perception. Research shows that people generally agree on where event boundaries occur when watching the same activity or video. These boundaries often correspond to meaningful changes such as shifts in location, characters, objects, or goals. Importantly, the ability to detect event boundaries is closely related to memory performance: individuals who segment events more accurately tend to remember the content better.


---

## 1.2.2 Event Segmentation Theory (EST)

The primary theoretical framework explaining this process is **Event Segmentation Theory (EST)** (Zacks et al., 2007). According to EST, the brain continuously maintains a **working event model**, which represents the current situation—who is present, what actions are occurring, and which objects are relevant.

This model is used to generate **predictions** about what will happen next. Incoming perceptual information is constantly compared with these predictions. When the information matches expectations, the event model is updated only slightly. However, when the incoming information strongly violates predictions, **prediction error increases**, signalling that the current model is no longer accurate.

At this point, the brain identifies an **event boundary** and constructs a new event model. This transition has several cognitive consequences. First, information active in working memory becomes less accessible as attention shifts to the new event model. Second, attentional resources are temporarily redirected to updating the model. Third, the transition facilitates **long-term memory encoding**, particularly for information that was active immediately before the boundary.

---

## 1.2.3 Event Boundaries and Memory Encoding



A substantial body of research shows that **event boundaries play an important role in memory encoding**. One key finding is the **boundary advantage**, where information appearing near an event boundary is remembered better than information appearing in the middle of an event (Swallow, Zacks, & Abram, 2009). This suggests that the cognitive processes occurring at boundaries strengthen memory formation.

Another related phenomenon is the **doorway effect**, where passing through a physical boundary, such as a doorway, reduces access to information that was active in working memory before the transition (Radvansky, Krawietz, & Tamplin, 2011). This indicates that boundaries can both enhance encoding of completed events and create separation between successive events.

Research also shows that **prediction errors**—when incoming information differs from expectations—often trigger event boundary perception. These boundaries then act as **anchors in long-term memory**, organizing experiences into distinct episodes and improving retrieval of boundary-adjacent information (Radvansky & Zacks, 2017).

---

##  1.2.4 Film Editing as a Natural Manipulation

Naturalistic videos provide a useful stimulus for studying event segmentation because they contain rich, realistic event structures. Unlike simplified laboratory stimuli, videos engage the perceptual and cognitive processes that operate in everyday experience.

Film editing offers a convenient way to manipulate event boundaries. Each editing cut can function as an externally imposed event boundary, allowing researchers to control when transitions occur.

In the **Natural Cut (NB)** condition, videos retain their natural boundary structure, allowing viewers to segment events normally. Prediction errors accumulate naturally, and event models are updated at appropriate transition points.

In contrast, the **Abrupt Cut (AB)** condition interrupts the video **1–5 seconds before a natural boundary** and jumps directly to a new event context. This manipulation disrupts the normal segmentation process in several ways. It prevents the natural completion of the current event model, introduces an unexpected prediction error in the middle of an event, and creates a discontinuity between the encoded content and the subsequent event. As a result, the memory trace may become fragmented.

---

## 1.2.5 Research Gap Addressed in This Study

Previous research has either used naturalistic videos without directly manipulating boundary timing or relied on simplified experimental stimuli that lack real-world complexity. The present study combines both approaches.

Specifically, this experiment:

* Uses **naturalistic YouTube Shorts** as stimuli
* Manipulates event boundary structure through controlled editing (**NB vs AB**)
* Employs a **between-subjects design** to avoid familiarity effects
* Tests memory for frames occurring **before boundaries (BB)** and in the **middle of events (EM)**
* Uses a **two-alternative forced-choice recognition task**, providing a sensitive measure of recognition memory

By integrating naturalistic stimuli with controlled boundary manipulation, the study provides a direct test of the hypothesis that **disrupting natural event boundaries impairs recognition memory, particularly for boundary-adjacent content**.

---



## 1.3 Dataset Description

The dataset was collected to test how disrupting event boundaries affects visual recognition memory. A total of **185 participants** were enrolled in a **between-subjects** experiment comparing two video-editing conditions: **Abrupt Cut (AB)** and **Natural Cut (NB)**. Participants were recruited from a university sample (age range: 19–34 years; M = 22.3, SD = 2.3; 113 male, 50 female, 22 missing gender data) and reported normal or corrected-to-normal vision. All behavioural data were collected using **PsychoPy 2025.1.1**.

The raw dataset consists of **171 per-participant CSV files** (47 rows × 105 columns each), stored in the `BRSM data csv/` folder. AB participants span sub23–sub157 (81 files) and NB participants span sub14–sub185 (90 files), following the naming convention `sub{ID}_{CONDITION}_recognitionstage_{YYYY-MM-DD_HHhMM.SS.mmm}.csv`. Three additional stimulus files accompany the participant data: `abruptmovies.csv` and `naturalmovies.csv` (each 45 rows, listing the video playlists for each condition) and `target_and_lures.csv` (40 rows, mapping the target and lure frame for each video).

---

### Table 1.3.1 — Stimulus and Trial Design

| Property | Value |
|---|---|
| Total unique videos | 40 (YouTube Shorts; 17–57 s, mean ≈ 33.4–33.5 s) |
| Vigilance (repeat) videos | 5 |
| Total playlist entries per participant | 45 |
| Max duration difference between AB and NB versions | ≤ 2 s (duration-matched) |
| AB manipulation | Video cut 1–5 s *before* consensus event boundary |
| NB manipulation | Video played continuously through the natural boundary |
| Task type | Two-alternative forced-choice (2AFC) |
| Trials per participant | 40 (one per unique video) |
| Options per trial | 1 target (seen) + 1 lure (unseen; same video) |
| BB trials per participant | 20 — target drawn 1–5 s before consensus boundary |
| EM trials per participant | 20 — target drawn from temporal centre of event |
| Side assignment (left/right) | Counterbalanced |
| Total trial rows across all participants | 7,400 (185 × 40) |

---

### Table 1.3.2 — Measured Variables

| Variable | Type | Source Column | Notes |
|---|---|---|---|
| **Accuracy** | Binary (0 / 1) | `resp.corr` | 1 = target selected correctly |
| **Response Time (RT)** | Continuous (seconds) | `resp.rt` | Stored as list string `"[x]"` — unpacked on load |
| **Confidence** | Ordinal (1–5) | `conf_radio.response` | 1 = not at all confident; 5 = very confident |
| **Frame Type** | Categorical (BB / EM) | Derived from `target_img` | `_BB_` in filename → BB; `_EM_` → EM |
| **Condition** | Categorical (AB / NB) | Derived from video path | Substring in path field (not filename) |

---


---

## 1.4 Aim of This Report

This report investigates whether disrupting natural event boundaries at encoding impairs visual recognition memory. Specifically, it tests:

1. Whether participants in the **NB condition** recognise target frames more accurately than those in the **AB condition** (main effect of boundary disruption — H1).
2. Whether this disruption effect is larger for **BB frames** than for **EM frames** (interaction of condition × frame type — H2), given that BB frames are the content most proximal to the aborted boundary update.
3. Whether boundary disruption affects **response times** and **confidence ratings**, and what these measures reveal about the metacognitive representation of memory quality.

By using naturalistic YouTube Shorts with precise, annotator-validated boundary timings and a sensitive 2AFC recognition paradigm, the study provides a direct, ecologically grounded test of Event Segmentation Theory's predictions about memory encoding at event boundaries.

---
# 2. Methods

## 2.1 Participants

A total of 185 participants were recruited from a university sample and randomly assigned to one of two conditions: **Natural Boundary (NB)** or **Abrupt Boundary (AB)**. All participants reported normal or corrected-to-normal vision and provided informed consent prior to participation. The age range of participants with available demographic data was 19–34 years (*M* = 22.3, *SD* = 2.3; 113 male, 50 female). Twenty-two participants did not complete the demographic questionnaire and are retained in all core analyses but excluded from demographic balance tests.

After applying all exclusion criteria (detailed in Section 2.2), the **final analysed sample comprised 166 participants** (AB: *n* = 78; NB: *n* = 88).

---

## Data Set Cleaning

## 2.2.1 Exclusion Criteria

**Incomplete data.** The file for participant sub42 (NB) contained only demographic form
output with no recognition trial data. This participant was excluded from all analyses.

**Excessive encoding time.** As a proxy for attentiveness during encoding, total encoding
time was computed as the interval between the onset of the instruction screen and the offset
of the final video:

$$t_{\text{encoding}} = \frac{t_{\text{Videos.stopped}} - t_{\text{instruction}_{2}\text{.stopped}}}{60}$$

The experiment embedded five repeated vigilance videos among the 40 unique stimuli. Under
normal viewing, the full encoding session should not exceed 27.05 minutes. Four participants
whose encoding time exceeded this threshold were excluded:

| Participant | Condition | Encoding Time (min) |
|:-----------:|:---------:|:-------------------:|
| sub32 | AB | 27.33 |
| sub36 | AB | 27.77 |
| sub151 | NB | 27.16 |
| sub161 | NB | 28.00 |

**Response time outliers.** Individual trials were screened for implausible response times.
Trials with RT < 0.2 s or RT > 60 s were excluded from response time analyses only;
accuracy and confidence data from the same trials were retained. One outlier trial was
identified: participant sub28 (AB condition, Movie 8, RT = 71.09 s). No trials with
RT < 0.2 s were found.

**Condition re-classification.** The data file for participant sub157 was labelled as AB in
the filename, but the video path column within the file confirmed that this participant viewed
natural boundary stimuli. Sub157 was therefore re-classified to the NB condition.

**Missing demographic data.** Twenty-two participants did not complete the demographic
questionnaire. These individuals are retained in all core analyses but excluded from
demographic balance tests (H6).

After applying all exclusion criteria, the **final analysed sample comprised 166 participants**
(AB: *n* = 78; NB: *n* = 88).

## 2.2.2 Participant Flow

| Stage | *n* |
|:------|:---:|
| Enrolled | 185 |
| Files available (sub1--sub13, sub20 unrecoverable) | 171 |
| Excluded: sub42 (no trial data) | 170 |
| Excluded: sub32, sub36, sub151, sub161 (encoding time > 27.05 min) | 166 |
| Re-classified: sub157 (AB → NB) | 166 |
| **Final analysed sample** | **166** |
| AB condition | 78 |
| NB condition | 88 |

# Section 2.2: Variables and Derivations

**Table** *All variables used in the analysis*
    
| Variable | CSV Column | Type | Description |
|:---|:---|:---:|:---|
| Accuracy | `resp.corr` | Binary (0/1) | Correct (1) or incorrect (0) recognition response |
| Response time | `resp.rt` | Continuous (s) | Time from stimulus onset to key press; unpacked from list string |
| Confidence | `conf_radio.response` | Ordinal (1--5) | Self-reported confidence in the recognition decision |
| Frame type | Derived from `target_img` | Categorical | BB (before boundary) or EM (event middle) |
| Condition | Derived from filename | Categorical | NB (natural boundary) or AB (abrupt boundary) |
| Encoding time | `Videos.stopped` $-$ `instruction_2.stopped` | Continuous (min) | Duration of encoding phase; used for attentiveness screening only |

---

## 2.3 Hypotheses

Based on Event Segmentation Theory, this report tests the following six hypotheses:

**H1 — Main effect of condition on recognition accuracy and RT.**
*   **$H_0$ (Null):** There is no difference in overall recognition accuracy or response times between the NB and AB conditions.
*   **$H_A$ (Alternative / Our Hypothesis):** Participants in the NB condition will show higher overall recognition accuracy and faster response times than participants in the AB condition. Disrupting the event boundary update process during encoding is expected to produce weaker, less accessible memory traces.

**H2 — Condition effect is larger for BB frames.**
*   **$H_0$ (Null):** There is no difference in BB frame accuracy between the NB and AB conditions.
*   **$H_A$ (Alternative / Our Hypothesis):** The NB advantage in recognition accuracy will be greater for before-boundary (BB) frames than for event-middle (EM) frames. BB frames are the content most proximal to the aborted boundary update in the AB condition and are therefore the most sensitive to the manipulation.

**H3 — No condition effect for EM frames.**
*   **$H_0$ (Null / Our Hypothesis):** Recognition accuracy for EM frames will not differ significantly between the NB and AB groups. EM frames are located away from the manipulation point, so boundary disruption is not expected to affect their encoding.
*   **$H_A$ (Alternative):** There is a significant difference in EM frame accuracy between the groups.

**H4 — Confidence calibration.**
*   **$H_0$ (Null):** Within each condition (AB and NB), confidence ratings are equal for correctly and incorrectly recognised trials.
*   **$H_A$ (Alternative / Our Hypothesis):** Within each condition (AB and NB), confidence ratings will be higher for correctly recognised trials than for incorrectly recognised trials. This tests whether participants' subjective confidence tracks the quality of their memory signal, independently of which viewing condition they were assigned to.

**H5 — Confidence by frame type.**
*   **$H_0$ (Null):** Confidence ratings are equal for BB and EM trials.
*   **$H_A$ (Alternative / Our Hypothesis):** Confidence ratings will be higher for BB trials than for EM trials. If natural boundaries enhance encoding of boundary-adjacent content, participants should feel more certain about those memories.

**H6 — Demographic balance.**
*   **$H_0$ (Null / Our Hypothesis):** The NB and AB groups will not differ significantly on age, gender distribution, handedness distribution, or vision status, confirming that random assignment produced comparable groups.
*   **$H_A$ (Alternative):** The demographic distributions differ significantly between the groups.

---

## 2.4 Statistical Analysis

### 2.4.1 Inferential Tests

All hypotheses were tested using standard parametric tests.

The assumptions of normality and homogeneity of variance were checked prior to each test. 

The choice of test for each hypothesis was determined by the structure of the comparison, as detailed below.

**H1, H2, H3 — Independent-samples *t*-test.** H1 compares overall recognition accuracy and RT between the NB and AB groups; H2 and H3 repeat this comparison separately for BB and EM frame subsets. In all three cases the comparison is **between two independent groups** — participants were randomly assigned to either NB or AB and each contributed data to only one condition. The independent-samples *t*-test is the appropriate test for comparing the means of two unrelated groups on a continuous dependent variable.

**H4 — Shapiro-Wilk followed by Paired-samples *t*-test or Wilcoxon Signed-Rank.** H4 asks whether, within each participant, confidence is higher when they are correct than when they are incorrect. Because every participant contributes **both** a mean confidence-correct and a mean confidence-incorrect score, the two values are not independent. To ensure statistical rigor, we first performed a **Shapiro-Wilk test** on the differences between correct and incorrect confidence ratings. For the AB group, where the distribution was normal, a **paired samples *t*-test** was used. For the NB group, where the distribution deviated significantly from normality, the non-parametric **Wilcoxon Signed-Rank test** was employed.

**H5 — Paired-samples *t*-test.** H5 compares mean confidence for BB trials against mean confidence for EM trials. Each participant sees exactly 20 BB trials and 20 EM trials, so again **both scores come from the same individual**. A paired *t*-test is therefore required for the same reason as H4.

**H6 (age) — Shapiro-Wilk followed by Mann-Whitney U test.** Age is a continuous variable. Because the Shapiro-Wilk test indicated the age distribution was significantly non-normal for both the AB and NB groups, we used the non-parametric independent-samples Mann-Whitney U test rather than an independent *t*-test.

**H6 (gender, handedness, vision) — Chi-square test of independence.** These variables are **categorical** (e.g., male/female/other; right-/left-handed; normal/corrected vision). A chi-square test of independence tests whether the frequency distribution of a categorical variable differs across groups, making it the correct choice here.

| Hypothesis | Dependent Variable | Design | Test |
|:-----------|:-------------------|:------:|:----:|
| H1 — NB > AB overall accuracy | Mean accuracy | Between-subjects | Independent *t*-test |
| H1 — NB < AB overall RT | Mean RT | Between-subjects | Independent *t*-test |
| H2 — NB > AB for BB frames | Mean BB accuracy | Between-subjects | Independent *t*-test |
| H3 — NB = AB for EM frames | Mean EM accuracy | Between-subjects | Independent *t*-test |
| H4 — Confidence: correct > incorrect | Mean confidence | Within-subjects | Shapiro-Wilk + t-test/Wilcoxon |
| H5 — Confidence: BB > EM | Mean confidence | Within-subjects | Paired *t*-test |
| H6 — Demographic equivalence | Age / Gender / Handedness / Vision | Between-subjects | Shapiro-Wilk + t-test/Mann-Whitney U (age); Chi-square (categorical) |


### 2.4.2 Software

All data processing, data cleaning, and statistical analyses were conducted in **Python 3** using standard open-source libraries. Data manipulation was performed using `pandas` and `numpy`. Inferential tests and multiple comparison corrections were conducted using `scipy.stats`. Visualisations were generated using `matplotlib` and `seaborn`. Data collection was originally performed using **PsychoPy**.


---

# 3. Results

## 3.1 H1 — Main Effect of Condition on Accuracy and Response Time

**Prediction:** NB participants would show higher recognition accuracy and faster response times than AB participants.

### 3.1.1 Accuracy

Before running our main comparisons, a normality test indicated that participant accuracy was not perfectly normally distributed. However, because our sample sizes are large (78 and 88 participants), standard statistical tests remain fully robust. A variance homogeneity test showed no significant difference in variance between the two groups.

Participants in the Natural Boundary (NB) group recognised significantly more targets (*M* = 87.0%) than those in the Abrupt Boundary (AB) group (*M* = 83.8%), *p* = .007. This confirms that disrupting natural event boundaries during viewing leads to a mild but significant reduction in visual memory.

### 3.1.2 Response Time

A normality test confirmed that response times were positively skewed (a typical feature of reaction times), and a variance homogeneity test showed similar variance between the groups.

Contrary to our related prediction, NB participants (*M* = 5.75 s) were **not** noticeably faster than AB participants (*M* = 5.57 s). The difference was not statistically significant (*p* = .448).

**H1 is partially supported: boundary disruption impaired memory accuracy, but it did not slow down response times.**

*Figure 3.1 — H1 results: mean recognition accuracy and mean response time by condition. Bars show group means; error bars are 95% confidence intervals; dots show individual participant means.*

![H1 Accuracy](plots/h1_accuracy.png)
![H1 RT](plots/h1_rt.png)

---

## 3.2 H2 — Recognition Accuracy for Pre-Boundary (BB) Frames

**Prediction:** NB participants would show higher recognition accuracy for before-boundary (BB) frames than AB participants.

**Rationale:** The boundary advantage hypothesis predicts that frames occurring just before a natural boundary benefit from heightened perceptual and attentional processing. In the AB condition, the artificial early cut disrupts this boundary context, eliminating the boundary-driven encoding advantage for BB frames.

### 3.2.1 BB Frame Accuracy

Normality tests showed non-normal distributions for BB accuracy, but sample sizes were sufficient for the tests to remain valid. A variance homogeneity test confirmed similar spread of data between groups.

| Group | *M* | *SD* | *n* |
|:------|:---:|:----:|:---:|
| AB | 0.822 | 0.105 | 78 |
| NB | 0.857 | 0.097 | 88 |

*Table 3.1. Mean BB-frame recognition accuracy by condition.*

NB participants (*M* = 0.857) achieved significantly higher BB-frame accuracy than AB participants (*M* = 0.822), *p* = .030. This indicates that the natural boost in memory for events right before a boundary is weakened when the boundary is artificially cut off. **H2 is supported.**

---

## 3.3 H3 — Recognition Accuracy for Event-Middle (EM) Frames

**Prediction:** Recognition accuracy for event-middle (EM) frames would not differ significantly between the groups.

**Rationale:** If the event boundary effect only strengthens memory for the moments immediately surrounding the boundary, frames from the middle of an event should be encoded similarly in both conditions regardless of an end cut.

### 3.3.1 EM Frame Accuracy

Normality tests again showed non-normality, but variance homogeneity tests were passed, making our statistical comparisons reliable.

| Group | *M* | *SD* | *n* |
|:------|:---:|:----:|:---:|
| AB | 0.853 | 0.093 | 78 |
| NB | 0.884 | 0.079 | 88 |

*Table 3.2. Mean EM-frame recognition accuracy by condition.*

Contrary to our prediction, NB participants (*M* = 0.884) were also significantly more accurate on event-middle frames than AB participants (*M* = 0.853), *p* = .022. Because the accuracy drop in the AB group occurred uniformly across both BB and EM frames, the disruption caused by an abrupt cut seems to broadly impair memory for the entire event clip, rather than uniquely affecting frames adjacent to the cut. **H3 is NOT supported.**

*Figure 3.2 — H2 & H3 results: mean recognition accuracy by frame type (BB, EM) and condition. Bars show group means; error bars are 95% confidence intervals; dots show individual participant means.*

![H2 H3 Frame Type Accuracy](plots/h2_h3_frame_type.png)

---

## 3.4 H4 — Confidence Calibration (Correct vs. Incorrect Trials)

**Prediction:** Participants would report higher confidence on trials they answered correctly than on trials they answered incorrectly.

**Rationale:** If participants' subjective confidence reflects genuine memory signal strength, it should be positively calibrated — higher when the recognition decision was accurate and lower when it was a mistake. This is a within-subjects test because each participant contributes a mean confidence value for both trial outcomes.

### 3.4.1 Analysis

We first tested the normality of the differences between correct and incorrect confidence ratings using the Shapiro-Wilk test. In the **AB group**, the distribution was found to be normal ($W = 0.975, p = .134$), justifying the use of a **paired-samples *t*-test**. In the **NB group**, the distribution was non-normal ($W = 0.969, p = .033$), so we applied the **Wilcoxon Signed-Rank test**.

| Condition | Correct *M* | Incorrect *M* | Test Type | Statistic | *p*-value | Effect Size |
|:----------|:---:|:----:|:---|:---:|:---:|:---:|
| **AB** | 4.201 | 3.362 | Paired *t*-test | *t* = 12.562 | < .001 | *d* = 1.422 |
| **NB** | 4.311 | 3.356 | Wilcoxon | *W* = 50.5 | < .001 | *r* = 0.971 |

*Table 3.3. Mean confidence ratings and hypothesis test results for H4.*

In both conditions, participants were significantly more confident on correct trials than on incorrect trials ($p < .001$). The direction of the effect was consistent with our prediction (**Correct > Incorrect**), and the effect sizes were very large (Cohen’s $d = 1.42$ for AB; Rank-Biserial $r = 0.97$ for NB). This demonstrates that participants have a robust, reliable internal signal of their own memory quality. **H4 is strongly supported.**

*Figure 3.3 — H4 results: mean confidence rating on correct and incorrect trials. Bars show participant-level means; error bars are 95% confidence intervals; dots show individual participant means.*

![H4 Confidence Calibration](plots/h4_confidence_accuracy.png)

---

## 3.5 H5 — Confidence by Frame Type (BB vs. EM)

**Prediction:** Participants would report higher confidence for before-boundary (BB) frames than for event-middle (EM) frames.

**Rationale:** If the encoding advantage conferred by event boundaries extends to subjective memory strength, participants should feel more certain about their recognition decisions for frames that occurred close to a boundary. This is a within-subjects comparison because every participant responded to both BB and EM trials.

### 3.5.1 Analysis

We tested confidence for pre-boundary frames separately for each viewing condition. A normality test showed that the difference in confidence scores checked out as normally distributed.

| Group | BB Frame Confidence | EM Frame Confidence | Difference |
|:------|:-------------------:|:-------------------:|:----------:|
| AB    | 4.02                | 4.12                | -0.10      |
| NB    | 4.19                | 4.21                | -0.02      |

*Table 3.4. Mean confidence ratings by frame type and condition.*

Contrary to our prediction, the Abrupt Boundary (AB) group showed significantly **lower** confidence for BB frames (*M* = 4.02) than for EM frames (*M* = 4.12), *p* = .002. However, for the Natural Boundary (NB) group—where the natural boundary was preserved—there was **no significant difference** in confidence between frame types (*p* = .498). **H5 is not supported in the predicted direction.**

*Figure 3.4 — H5 results: mean confidence rating by frame type. Bars show participant-level means; error bars are 95% confidence intervals; dots show individual participant means.*

![H5 Confidence Frame Type](plots/h5_confidence_frame_type.png)

---

## 3.6 H6 — Demographic Equivalence Between Conditions

**Prediction:** AB and NB participants would not differ significantly in age, gender distribution, handedness, or visual status.

**Rationale:** Random assignment to condition should produce comparable groups. Confirming demographic equivalence rules out confounds — for instance, if one condition had systematically older participants, age-related memory differences could masquerade as a condition effect. Demographic data were obtained from a separate Excel record linked to participant IDs; 149 of the 166 participants had complete demographic records (AB: *n* = 73–78; NB: *n* = 76–88, depending on variable).

### 3.6.1 Analysis

We first verified the normality of the age distribution using the Shapiro-Wilk test. Age was found to be significantly non-normal in both the AB group ($W = 0.855, p < .001$) and the NB group ($W = 0.929, p < .001$). Consequently, an independent-samples **Mann-Whitney U test** was used to compare age between groups. Categorical variables (gender, handedness, vision) were compared using **Chi-square tests** of independence.

| Variable | AB | NB | Test | Statistic | *p*-value |
|:---------|:---:|:---:|:---|:---:|:---:|
| **Age** | Mdn=22.3 | Mdn=22.0 | Mann-Whitney U | *U* = 4391.5 | .564 |
| **Gender** (F/M) | 23/50 | 23/53 | Chi-square | $\chi^2(1) = 0.205$ | .651 |
| **Handedness** (L/R) | 3/70 | 5/71 | Chi-square | $\chi^2(1) = 0.491$ | .484 |
| **Vision** (C/N/U) | 33/40/0 | 38/36/2 | Chi-square | $\chi^2(2) = 2.161$ | .339 |

*Table 3.5. Demographic distribution and balance checks across condition groups.*

None of the demographic traits varied significantly between conditions (all *p* > .05). **H6 is fully supported.** Because the experimental groups are demographically balanced, we can be confident that our main performance findings (H1–H3) were truly driven by the movie boundaries and not skewed by underlying demographic differences.

*Figure 3.5 — H6 results: age by condition (left) and gender distribution by condition (right). Bars show means; error bars are 95% confidence intervals.*

![H6 Demographics](plots/h6_demographics.png)

---

## 3.7 Descriptive Statistics

The final analysed sample comprised 166 participants (AB: *n* = 78; NB: *n* = 88), contributing a total of 6,650 recognition trials (3,320 BB; 3,320 EM). Overall recognition accuracy was high in both conditions. Response times and confidence ratings were broadly similar across groups. Descriptive statistics for all core variables are summarised in Table 3.7.

| Variable | AB (*n* = 78) | NB (*n* = 88) |
|:---------|:-------------:|:-------------:|
| Accuracy — *M* (*SD*) | 0.84 (0.08) | 0.87 (0.07) |
| RT — *M* (*SD*) s | 5.57 (1.42) | 5.75 (1.63) |

*Table 3.7. Participant-level means and standard deviations for accuracy and response time by condition. RT excludes the one outlier trial.*

---

## 3.9 Exploratory Analyses

We did 6 additional analyses to better understand the data.


---

### 3.9.2 Response Time by Frame Type and Condition

We broke down response times by frame type (BB vs EM) within each condition to check whether the overall null RT result (H1b) hid any frame-specific patterns.

| Condition | Frame Type | *M* RT (s) |
|:----------|:----------:|:----------:|
| AB | BB | 5.71 |
| AB | EM | 5.47 |
| NB | BB | 5.77 |
| NB | EM | 5.74 |

Both groups were slightly slower for BB than EM frames. NB participants were slightly *slower* overall yet still more *accurate* — ruling out a speed–accuracy trade-off as an explanation for the NB advantage.

*Figure 3.8 — Mean response time by frame type and condition. Error bars are 95% confidence intervals.*

![RT by Frame Type](exploratory_plots/exp_rt_frame_type.png)

### 3.9.3 Exploratory Analysis: Predicting Recognition Accuracy

While our previous tests looked at factors separately, we used a General Linear Model (specifically, a Logistic Regression) to assess $N = 6,640$ trials simultaneously. This allowed us to test how confidence, condition, and frame type (BB vs. EM) jointly predict accuracy. Variance Inflation Factor (VIF) checks confirmed that all predictors were independent ($VIF \approx 1.0$), ensuring the model is stable.

**Model:** `Accuracy ~ Confidence + Condition + Frame_Type`

| Predictor | Coef ($B$) | Odds Ratio | *p*-value | Result |
|:---|:---:|:---:|:---:|:---|
| **Intercept** | −0.692 | 0.50 | <.001 | Significant |
| **Condition (NB)** | 0.183 | 1.20 | .012 | Significant |
| **Frame Type (EM)** | 0.208 | 1.23 | .004 | Significant |
| **Confidence** | 0.589 | 1.80 | <.001 | Significant |

**Conclusions:**
- **The Power of Confidence:** This was the strongest independent predictor. Every time a participant felt more confident, their odds of being correct increased by **80.2%** ($OR = 1.80$).
- **Condition Effect:** Even when controlling for confidence and frame type, being in the Natural Boundary condition increased the odds of a correct answer by **20%** ($OR = 1.20$).
- **Diagnostic Stability:** The $VIF \approx 1.0$ confirms that these factors are independent drivers of recognition accuracy.

*Figure 3.9 — (A) Logistic regression curves showing predicted accuracy probability by confidence. (B) Interaction plot for frame type and condition effects.*

![GLM Visuals](exploratory_plots/exp_glm_visuals.png)

---

# 4. Conclusion

## 4.1 Summary of Findings

166 participants (AB: *n* = 78; NB: *n* = 88) completed a video recognition task. The table below summarises the outcome of all six hypotheses based on the raw *p*-value threshold ($\alpha = 0.05$).

| Hypothesis | Prediction | Raw *p* | Verdict |
|:-----------|:-----------|:-------:|:-------:|
| H1a — Overall accuracy | NB > AB | .007 | **Supported** |
| H1b — Overall RT | NB faster than AB | .448 | Not Supported |
| H2 — BB-frame accuracy | NB > AB for BB frames | .030 | **Supported** |
| H3 — EM-frame accuracy | NB = AB for EM frames | .022 | Not Supported |
| H4 — Confidence calibration (AB) | Higher confidence when correct | <.001 | **Supported** |
| H4 — Confidence calibration (NB) | Higher confidence when correct | <.001 | **Supported** |
| H5 — Confidence by frame type (AB) | BB > EM confidence | .002 | Not Supported (reverse) |
| H5 — Confidence by frame type (NB) | BB > EM confidence | .498 | Not Supported |
| H6 — Demographic equivalence | AB ≈ NB on demographics | .339 | **Supported** |

*Table 4.1. Verdict reflects whether $p < 0.05$ (for directional hypotheses) or $p > 0.05$ (for null hypotheses H3 and H6).*

**Key takeaways:**

- **Accuracy (H1a, H2):** Cutting a clip early slightly reduced recognition accuracy across the board (*d* = 0.34–0.42), and these effects were statistically significant at $\alpha = 0.05$ for both overall accuracy and BB frames.
- **EM frames (H3):** The EM accuracy difference was also significant at the raw level (*p* = .022), contradicting the prediction of no difference. The boundary disruption appears to impair the whole event clip, not just boundary-adjacent frames.
- **Response time (H1b):** No meaningful difference. NB participants were even slightly slower, ruling out a speed–accuracy trade-off.
- **Confidence (H4):** The strongest result. Within both conditions (AB: *t* = 12.562, *d* = 1.422; NB: *W* = 50.5, *r* = 0.971), participants were much more confident when correct than incorrect (*p* < .001 in both cases), showing a robust metacognitive signal.
- **Confidence by frame type (H5):** The predicted effect did not appear. The AB group showed significantly *lower* confidence for BB than EM frames — the opposite of what was expected.
- **Exploratory Analysis (GLM):** Using a multi-factor model with $VIF \approx 1.0$, we confirmed that confidence, condition, and frame type are all independent, significant drivers of recognition accuracy. Confidence remains the most powerful predictor, yielding an 80.2% increase in the odds of accuracy per point.
- **Demographics (H6):** Both groups were perfectly matched on all demographic factors (age, gender, handedness, and vision). No sample imbalances were found.

---

## 4.2 Limitations

**1. Missing demographic data.** 17 of 166 participants had no demographic records, reducing the H6 sample to *n* = 149. This is unlikely to affect the main findings but is worth noting.

**2. Sample size.** The study had enough power to detect large effects (like H4) but was only moderately powered for the smaller accuracy effects (H1–H3). Slightly more participants per group would be needed for reliable detection at this effect size.

**3. Response time measure.** The task had no time limit, so RT reflects both thinking time and response — making it a noisy measure. This likely explains why no RT effects were found.

---

## 4.3 Next Steps (Report 2)

Report 2 will revisit the same dataset using more advanced inferential methods — specifically ANOVA, regression, and GLM — to answer questions that the t-tests and chi-square tests in this report could not directly address.

**1. ANOVA.** The current report tested BB and EM frame accuracy in two separate t-tests (H2 and H3). A mixed ANOVA with frame type (BB/EM) as a within-subjects factor and condition (NB/AB) as a between-subjects factor will test both effects together and, importantly, whether the NB advantage differs between frame types.

**2. Regression.** A regression model will examine which variables — such as confidence, age, and encoding time — predict recognition accuracy across participants, building on the H4 finding that confidence is linked to performance.

**3. GLM.** A General Linear Model will allow multiple predictors (condition, frame type, confidence) to be examined simultaneously, giving a more complete picture of what drives accuracy differences than single comparisons can provide.

---

## 4.4 References

Cutting, J. E., Brunick, K. L., & Candan, A. (2012). Perceiving event boundaries in motion pictures. *Psychology of Aesthetics, Creativity, and the Arts*, *6*(4), 323–330. https://doi.org/10.1037/a0027737

Radvansky, G. A., & Zacks, J. M. (2017). Event cognition. *Psychological Science in the Public Interest*, *18*(1), 1–57. https://doi.org/10.1177/1529100617691164

Swallow, K. M., Zacks, J. M., & Abrams, R. A. (2009). Event boundaries in perception affect memory encoding and updating. *Journal of Experimental Psychology: General*, *138*(2), 223–244. https://doi.org/10.1037/a0015631

Zacks, J. M., Speer, N. K., Swallow, K. M., Braver, T. S., & Reynolds, J. R. (2007). Event perception: A mind-brain perspective. *Psychological Bulletin*, *133*(2), 273–293. https://doi.org/10.1037/0033-2909.133.2.273
