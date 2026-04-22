# """
# H1 — Main Effect of Condition on Accuracy and Response Time
# Non-parametric (Mann-Whitney U) & Regression (Logistic / OLS) Upgrades
# Generates: plots/H1_accuracy_RT.png
# """

# import pandas as pd
# import numpy as np
# from scipy import stats
# import statsmodels.api as sm
# import statsmodels.formula.api as smf
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import os
# import sys
# sys.path.insert(0, '..')

# from load_all_data import load_all_data

# df, _ = load_all_data(verbose=False)
# df['accuracy'] = pd.to_numeric(df['accuracy'], errors='coerce')

# os.makedirs('../plots', exist_ok=True)
# COLORS = {'AB': '#E07B54', 'NB': '#5B8DB8'}

# # ── 1. Per-participant means (For Mann-Whitney U) ──────────────────────────────
# # Exclude trials flagged as RT outliers
# df_clean_h1 = df[~df['rt_outlier']].copy()

# ppt_acc = df_clean_h1.groupby(['sub_id', 'condition'])['accuracy'].mean().reset_index(name='mean_acc')
# ppt_rt  = df_clean_h1.groupby(['sub_id', 'condition'])['rt'].mean().reset_index(name='mean_rt')

# ab_acc = ppt_acc[ppt_acc['condition'] == 'AB']['mean_acc']
# nb_acc = ppt_acc[ppt_acc['condition'] == 'NB']['mean_acc']
# ab_rt  = ppt_rt[ppt_rt['condition'] == 'AB']['mean_rt']
# nb_rt  = ppt_rt[ppt_rt['condition'] == 'NB']['mean_rt']

# n1, n2 = len(ab_acc), len(nb_acc)

# # ── Accuracy stats (Mann-Whitney U) ────────────────────────────────────────────
# u_acc, p_acc = stats.mannwhitneyu(ab_acc, nb_acc, alternative='two-sided')

# print("=== H1 Accuracy (Participant Means: Mann-Whitney U) ===")
# print(f"  AB: Median={ab_acc.median():.4f}, M={ab_acc.mean():.4f}, SD={ab_acc.std():.4f}, n={n1}")
# print(f"  NB: Median={nb_acc.median():.4f}, M={nb_acc.mean():.4f}, SD={nb_acc.std():.4f}, n={n2}")
# print(f"  Mann-Whitney U = {u_acc:.4f}, p = {p_acc:.4f}")

# # ── RT stats (Mann-Whitney U) ──────────────────────────────────────────────────
# u_rt, p_rt = stats.mannwhitneyu(ab_rt, nb_rt, alternative='two-sided')

# print("\n=== H1 RT (Participant Means: Mann-Whitney U) ===")
# print(f"  AB: Median={ab_rt.median():.4f}, M={ab_rt.mean():.4f}, SD={ab_rt.std():.4f}")
# print(f"  NB: Median={nb_rt.median():.4f}, M={nb_rt.mean():.4f}, SD={nb_rt.std():.4f}")
# print(f"  Mann-Whitney U = {u_rt:.4f}, p = {p_rt:.4f}")

# # ── 2. Trial-Level Models ──────────────────────────────────────────────────────
# print("\n" + "="*50)
# print("=== Trial-Level Logistic Regression (Accuracy) ===")
# df_acc_clean = df[~df['rt_outlier']].dropna(subset=['accuracy', 'condition']).copy()
# df_acc_clean['cond_num'] = (df_acc_clean['condition'] == 'NB').astype(int)
# try:
#     logit_model = smf.logit("accuracy ~ cond_num", data=df_acc_clean).fit(disp=0)
#     print(logit_model.summary())
# except Exception as e:
#     print(f"Logistic Regression failed: {e}")

# print("\n" + "="*50)
# print("=== Trial-Level OLS Linear Regression (RT) ===")
# df_rt_clean = df[~df['rt_outlier']].dropna(subset=['rt', 'condition']).copy()
# df_rt_clean['cond_num'] = (df_rt_clean['condition'] == 'NB').astype(int)
# try:
#     ols_model = smf.ols("rt ~ cond_num", data=df_rt_clean).fit()
#     print(ols_model.summary())
# except Exception as e:
#     print(f"OLS Regression failed: {e}")

# # ── Plot ───────────────────────────────────────────────────────────────────────
# fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5))
# rng = np.random.default_rng(42)

# for ax, (ab_data, nb_data), ylabel, title, p_val in zip(
#     axes,
#     [(ab_acc, nb_acc), (ab_rt, nb_rt)],
#     ['Mean Recognition Accuracy', 'Mean Response Time (s)'],
#     ['H1a — Accuracy by Condition', 'H1b — Response Time by Condition'],
#     [p_acc, p_rt]
# ):
#     means = [ab_data.mean(), nb_data.mean()]
#     sems  = [1.96 * ab_data.sem(), 1.96 * nb_data.sem()]
    
#     ax.bar([0, 1], means, color=[COLORS['AB'], COLORS['NB']],
#            edgecolor='black', linewidth=0.8, width=0.5)
#     ax.errorbar([0, 1], means, yerr=sems, fmt='none', color='black',
#                 capsize=5, linewidth=1.4)
    
#     for xi, data in enumerate([ab_data, nb_data]):
#         jit = rng.uniform(-0.12, 0.12, len(data))
#         ax.scatter(np.full(len(data), xi) + jit, data,
#                    color=list(COLORS.values())[xi], alpha=0.3, s=14, zorder=3)
    
#     # Annotate p-value from Mann-Whitney test
#     sig_text = f"Mann-Whitney\n$p = {p_val:.4f}$" if p_val >= 0.0001 else "Mann-Whitney\n$p < 0.0001$"
    
#     if ylabel == 'Mean Recognition Accuracy':
#         ax.set_ylim(0.4, 1.05)
    
#     ax.text(0.5, 0.95, sig_text, transform=ax.transAxes, ha='center', va='top', 
#             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.2'), 
#             fontsize=10)

#     ax.set_xticks([0, 1])
#     ax.set_xticklabels(['AB', 'NB'], fontsize=12)
#     ax.set_ylabel(ylabel, fontsize=11)
#     ax.set_title(title, fontsize=11, fontweight='bold')
#     ax.spines[['top', 'right']].set_visible(False)
    
# fig.tight_layout()
# fig.savefig('../plots/H1_accuracy_RT.png', dpi=150, bbox_inches='tight')
# plt.close(fig)
# print("\nPlot saved: plots/H1_accuracy_RT.png")


"""
H1 — Main Effect of Condition on Accuracy and Response Time
Non-parametric (Mann-Whitney U) & Regression (Logistic / OLS) Upgrades
Generates: plots/H1_accuracy_RT.png
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, '..')

from load_all_data import load_all_data

df, _ = load_all_data(verbose=False)
df['accuracy'] = pd.to_numeric(df['accuracy'], errors='coerce')

os.makedirs('../plots', exist_ok=True)
COLORS = {'AB': '#E07B54', 'NB': '#5B8DB8'}

# ── 1. Per-participant means (For Mann-Whitney U) ──────────────────────────────
# Exclude trials flagged as RT outliers
df_clean_h1 = df[~df['rt_outlier']].copy()

ppt_acc = df_clean_h1.groupby(['sub_id', 'condition'])['accuracy'].mean().reset_index(name='mean_acc')
ppt_rt  = df_clean_h1.groupby(['sub_id', 'condition'])['rt'].mean().reset_index(name='mean_rt')

ab_acc = ppt_acc[ppt_acc['condition'] == 'AB']['mean_acc']
nb_acc = ppt_acc[ppt_acc['condition'] == 'NB']['mean_acc']
ab_rt  = ppt_rt[ppt_rt['condition'] == 'AB']['mean_rt']
nb_rt  = ppt_rt[ppt_rt['condition'] == 'NB']['mean_rt']

n1, n2 = len(ab_acc), len(nb_acc)

# ── Accuracy stats (Mann-Whitney U) ────────────────────────────────────────────
u_acc, p_acc = stats.mannwhitneyu(ab_acc, nb_acc, alternative='two-sided')

print("=== H1 Accuracy (Participant Means: Mann-Whitney U) ===")
print(f"  AB: Median={ab_acc.median():.4f}, M={ab_acc.mean():.4f}, SD={ab_acc.std():.4f}, n={n1}")
print(f"  NB: Median={nb_acc.median():.4f}, M={nb_acc.mean():.4f}, SD={nb_acc.std():.4f}, n={n2}")
print(f"  Mann-Whitney U = {u_acc:.4f}, p = {p_acc:.4f}")

# ── RT stats (Mann-Whitney U) ──────────────────────────────────────────────────
u_rt, p_rt = stats.mannwhitneyu(ab_rt, nb_rt, alternative='two-sided')

print("\n=== H1 RT (Participant Means: Mann-Whitney U) ===")
print(f"  AB: Median={ab_rt.median():.4f}, M={ab_rt.mean():.4f}, SD={ab_rt.std():.4f}")
print(f"  NB: Median={nb_rt.median():.4f}, M={nb_rt.mean():.4f}, SD={nb_rt.std():.4f}")
print(f"  Mann-Whitney U = {u_rt:.4f}, p = {p_rt:.4f}")

# ── 2. Trial-Level Models ──────────────────────────────────────────────────────
print("\n" + "="*50)
print("=== Trial-Level Logistic Regression (Accuracy) ===")
df_acc_clean = df[~df['rt_outlier']].dropna(subset=['accuracy', 'condition']).copy()
df_acc_clean['cond_num'] = (df_acc_clean['condition'] == 'NB').astype(int)
try:
    logit_model = smf.logit("accuracy ~ cond_num", data=df_acc_clean).fit(disp=0)
    print(logit_model.summary())
except Exception as e:
    print(f"Logistic Regression failed: {e}")

print("\n" + "="*50)
print("=== Trial-Level OLS Linear Regression (RT) ===")
df_rt_clean = df[~df['rt_outlier']].dropna(subset=['rt', 'condition']).copy()
df_rt_clean['cond_num'] = (df_rt_clean['condition'] == 'NB').astype(int)
try:
    ols_model = smf.ols("rt ~ cond_num", data=df_rt_clean).fit()
    print(ols_model.summary())
except Exception as e:
    print(f"OLS Regression failed: {e}")

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5))
rng = np.random.default_rng(42)

for ax, (ab_data, nb_data), ylabel, title, p_val in zip(
    axes,
    [(ab_acc, nb_acc), (ab_rt, nb_rt)],
    ['Mean Recognition Accuracy', 'Mean Response Time (s)'],
    ['H1a — Accuracy by Condition', 'H1b — Response Time by Condition'],
    [p_acc, p_rt]
):
    means = [ab_data.mean(), nb_data.mean()]
    sems  = [1.96 * ab_data.sem(), 1.96 * nb_data.sem()]
    
    ax.bar([0, 1], means, color=[COLORS['AB'], COLORS['NB']],
           edgecolor='black', linewidth=0.8, width=0.5)
    ax.errorbar([0, 1], means, yerr=sems, fmt='none', color='black',
                capsize=5, linewidth=1.4)
    
    for xi, data in enumerate([ab_data, nb_data]):
        jit = rng.uniform(-0.12, 0.12, len(data))
        ax.scatter(np.full(len(data), xi) + jit, data,
                   color=list(COLORS.values())[xi], alpha=0.3, s=14, zorder=3)
    
    # Annotate p-value from Mann-Whitney test
    sig_text = f"Mann-Whitney\n$p = {p_val:.4f}$" if p_val >= 0.0001 else "Mann-Whitney\n$p < 0.0001$"
    
    if ylabel == 'Mean Recognition Accuracy':
        ax.set_ylim(0.4, 1.05)
    
    ax.text(0.5, 0.95, sig_text, transform=ax.transAxes, ha='center', va='top', 
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.2'), 
            fontsize=10)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(['AB', 'NB'], fontsize=12)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    
fig.tight_layout()
fig.savefig('../plots/H1_accuracy_RT.png', dpi=150, bbox_inches='tight')
plt.close(fig)
print("\nPlot saved: plots/H1_accuracy_RT.png")
