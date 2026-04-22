# """
# H5 — Confidence by Frame Type: BB vs EM Frames
# Paired t-test (within-subject): mean confidence for BB vs EM frames per participant
# Generates: plots/H5_confidence_frame_type.png
# """

# import pandas as pd
# import numpy as np
# from scipy import stats
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import os
# import sys
# sys.path.insert(0, '..')

# from load_all_data import load_all_data

# df, _ = load_all_data(verbose=False)
# df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')

# os.makedirs('../plots', exist_ok=True)

# # ── Analysis Split by Condition ────────────────────────────────────────────────
# # For within-subjects, we check normality of the differences per group.
# def analyze_h5_group(cond):
#     sub_df = df[(df['condition'] == cond) & (~df['rt_outlier'])]
#     # per-participant BB vs EM mean confidence
#     p_data = sub_df.groupby(['sub_id', 'frame_type'])['confidence'].mean().unstack()
#     p_data = p_data.dropna(subset=['BB', 'EM'])
#     bb, em = p_data['BB'], p_data['EM']
#     d = bb - em
#     shapiro = stats.shapiro(d)
#     # If p < 0.05, use Wilcoxon
#     if shapiro.pvalue < 0.05:
#         test_type = "Wilcoxon"
#         stat, p = stats.wilcoxon(bb, em)
#     else:
#         test_type = "Paired t-test"
#         stat, p = stats.ttest_rel(bb, em)
    
#     print(f"\nCondition: {cond} (n={len(p_data)})")
#     print(f"  BB M={bb.mean():.4f}, EM M={em.mean():.4f}")
#     print(f"  Shapiro-Wilk on diff: W={shapiro.statistic:.4f}, p={shapiro.pvalue:.4f}")
#     print(f"  {test_type}: stat={stat:.4f}, p={p:.4f}")
#     return bb, em, test_type, p

# bb_ab, em_ab, type_ab, p_ab = analyze_h5_group('AB')
# bb_nb, em_nb, type_nb, p_nb = analyze_h5_group('NB')

# # ── Trial-Level OLS Regression ───────────────────────────────────────────────
# print("\n" + "="*50)
# print("=== Trial-Level OLS Regression (Confidence) ===")
# # Predict confidence using frame type and condition
# # Map BB=1, EM=0; NB=1, AB=0
# df_ols = df.dropna(subset=['confidence', 'frame_type', 'condition']).copy()
# df_ols = df_ols[~df_ols['rt_outlier']] # Exclude cleaning outliers
# df_ols['is_bb'] = (df_ols['frame_type'] == 'BB').astype(int)
# df_ols['is_nb'] = (df_ols['condition'] == 'NB').astype(int)

# import statsmodels.formula.api as smf
# # We include the interaction term (is_bb * is_nb) to see if the boundary effect 
# # differs significantly between the two experimental conditions.
# ols_model = smf.ols("confidence ~ is_bb * is_nb", data=df_ols).fit()
# print(ols_model.summary())

# # ── Plot ───────────────────────────────────────────────────────────────────────
# # We will create a side-by-side plot matching the H1 style
# fig, axes = plt.subplots(1, 2, figsize=(8, 4), sharey=True)
# COLORS_MAP = {'AB': '#E07B54', 'NB': '#5B8DB8'}
# rng = np.random.default_rng(42)

# for ax, cond, (bb, em), p_val, t_type in zip(
#     axes, ['AB', 'NB'], [(bb_ab, em_ab), (bb_nb, em_nb)], [p_ab, p_nb], [type_ab, type_nb]
# ):
#     means = [bb.mean(), em.mean()]
#     sems  = [1.96 * bb.sem(), 1.96 * em.sem()]
#     # Draw bars
#     ax.bar([0, 1], means, color=['#6DBF8E', '#C97DC4'], 
#            edgecolor='black', linewidth=0.8, width=0.5)
#     ax.errorbar([0, 1], means, yerr=sems, fmt='none', color='black',
#                 capsize=5, linewidth=1.4)
#     # Jittered dots
#     for xi, data in enumerate([bb, em]):
#         jit = rng.uniform(-0.12, 0.12, len(data))
#         ax.scatter(np.full(len(data), xi) + jit, data,
#                    color=['#6DBF8E', '#C97DC4'][xi], alpha=0.3, s=12, zorder=3)
    
#     sig_text = f"{t_type}\n$p = {p_val:.4f}$" if p_val >= 0.0001 else f"{t_type}\n$p < 0.0001$"
#     ax.text(0.5, 0.95, sig_text, transform=ax.transAxes, ha='center', va='top', 
#             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.2'), 
#             fontsize=9)

#     ax.set_xticks([0, 1])
#     ax.set_xticklabels(['BB', 'EM'], fontsize=11)
#     ax.set_ylabel('Mean Confidence', fontsize=10)
#     ax.set_title(f'H5 ({cond} Group)', fontsize=11, fontweight='bold')
#     ax.set_ylim(3.0, 5.2)
#     ax.spines[['top', 'right']].set_visible(False)

# fig.tight_layout()
# fig.savefig('../plots/H5_confidence_frame_type.png', dpi=150, bbox_inches='tight')
# plt.close(fig)
# print("\nPlot saved: plots/H5_confidence_frame_type.png")


"""
H5 — Confidence by Frame Type: BB vs EM Frames
Paired t-test (within-subject): mean confidence for BB vs EM frames per participant
Generates: plots/H5_confidence_frame_type.png
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, '..')

from load_all_data import load_all_data

df, _ = load_all_data(verbose=False)
df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')

os.makedirs('../plots', exist_ok=True)

# ── Analysis Split by Condition ────────────────────────────────────────────────
# For within-subjects, we check normality of the differences per group.
def analyze_h5_group(cond):
    sub_df = df[(df['condition'] == cond) & (~df['rt_outlier'])]
    # per-participant BB vs EM mean confidence
    p_data = sub_df.groupby(['sub_id', 'frame_type'])['confidence'].mean().unstack()
    p_data = p_data.dropna(subset=['BB', 'EM'])
    bb, em = p_data['BB'], p_data['EM']
    d = bb - em
    shapiro = stats.shapiro(d)
    # If p < 0.05, use Wilcoxon
    if shapiro.pvalue < 0.05:
        test_type = "Wilcoxon"
        stat, p = stats.wilcoxon(bb, em)
    else:
        test_type = "Paired t-test"
        stat, p = stats.ttest_rel(bb, em)
    
    print(f"\nCondition: {cond} (n={len(p_data)})")
    print(f"  BB M={bb.mean():.4f}, EM M={em.mean():.4f}")
    print(f"  Shapiro-Wilk on diff: W={shapiro.statistic:.4f}, p={shapiro.pvalue:.4f}")
    print(f"  {test_type}: stat={stat:.4f}, p={p:.4f}")
    return bb, em, test_type, p

bb_ab, em_ab, type_ab, p_ab = analyze_h5_group('AB')
bb_nb, em_nb, type_nb, p_nb = analyze_h5_group('NB')

# ── Trial-Level OLS Regression ───────────────────────────────────────────────
print("\n" + "="*50)
print("=== Trial-Level OLS Regression (Confidence) ===")
# Predict confidence using frame type and condition
# Map BB=1, EM=0; NB=1, AB=0
df_ols = df.dropna(subset=['confidence', 'frame_type', 'condition']).copy()
df_ols = df_ols[~df_ols['rt_outlier']] # Exclude cleaning outliers
df_ols['is_bb'] = (df_ols['frame_type'] == 'BB').astype(int)
df_ols['is_nb'] = (df_ols['condition'] == 'NB').astype(int)

import statsmodels.formula.api as smf
# We include the interaction term (is_bb * is_nb) to see if the boundary effect 
# differs significantly between the two experimental conditions.
ols_model = smf.ols("confidence ~ is_bb * is_nb", data=df_ols).fit()
print(ols_model.summary())

# ── Plot ───────────────────────────────────────────────────────────────────────
# We will create a side-by-side plot matching the H1 style
fig, axes = plt.subplots(1, 2, figsize=(8, 4), sharey=True)
COLORS_MAP = {'AB': '#E07B54', 'NB': '#5B8DB8'}
rng = np.random.default_rng(42)

for ax, cond, (bb, em), p_val, t_type in zip(
    axes, ['AB', 'NB'], [(bb_ab, em_ab), (bb_nb, em_nb)], [p_ab, p_nb], [type_ab, type_nb]
):
    means = [bb.mean(), em.mean()]
    sems  = [1.96 * bb.sem(), 1.96 * em.sem()]
    # Draw bars
    ax.bar([0, 1], means, color=['#6DBF8E', '#C97DC4'], 
           edgecolor='black', linewidth=0.8, width=0.5)
    ax.errorbar([0, 1], means, yerr=sems, fmt='none', color='black',
                capsize=5, linewidth=1.4)
    # Jittered dots
    for xi, data in enumerate([bb, em]):
        jit = rng.uniform(-0.12, 0.12, len(data))
        ax.scatter(np.full(len(data), xi) + jit, data,
                   color=['#6DBF8E', '#C97DC4'][xi], alpha=0.3, s=12, zorder=3)
    
    sig_text = f"{t_type}\n$p = {p_val:.4f}$" if p_val >= 0.0001 else f"{t_type}\n$p < 0.0001$"
    ax.text(0.5, 0.95, sig_text, transform=ax.transAxes, ha='center', va='top', 
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.2'), 
            fontsize=9)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(['BB', 'EM'], fontsize=11)
    ax.set_ylabel('Mean Confidence', fontsize=10)
    ax.set_title(f'H5 ({cond} Group)', fontsize=11, fontweight='bold')
    ax.set_ylim(3.0, 5.2)
    ax.spines[['top', 'right']].set_visible(False)

fig.tight_layout()
fig.savefig('../plots/H5_confidence_frame_type.png', dpi=150, bbox_inches='tight')
plt.close(fig)
print("\nPlot saved: plots/H5_confidence_frame_type.png")
