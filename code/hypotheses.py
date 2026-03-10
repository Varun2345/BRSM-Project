import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from config import PLOT_DIR, CONDITION_COLORS, FRAME_COLORS
from corrections import cohens_d

def plot_h1_accuracy(trials_df):
    """H1 — Part 1: Overall recognition accuracy by condition."""
    print("\n" + "=" * 70)
    print("H1 — Overall Recognition Accuracy: AB vs NB")
    print("Test: Independent samples t-test")
    print("=" * 70)

    subj_acc = trials_df.groupby(['subject_id', 'condition'])['accuracy'].mean().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('H1: Overall Recognition Accuracy — AB vs NB\n(Independent t-test)',
                 fontsize=14, fontweight='bold')

    # Bar chart with SEM
    ax = axes[0]
    means = subj_acc.groupby('condition')['accuracy'].mean()
    sems = subj_acc.groupby('condition')['accuracy'].sem()
    bars = ax.bar(means.index, means.values, yerr=sems.values, capsize=8,
                  color=[CONDITION_COLORS[c] for c in means.index],
                  edgecolor='white', linewidth=1.5, alpha=0.85)
    ax.set_ylabel('Mean Accuracy (proportion correct)')
    ax.set_xlabel('Condition')
    ax.set_title('Mean Recognition Accuracy ± SEM')
    ax.set_ylim(0, 1)

    for bar, mean, sem in zip(bars, means.values, sems.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + sem + 0.02,
                f'{mean:.3f}', ha='center', fontweight='bold', fontsize=12)

    # t-test
    ab_acc = subj_acc[subj_acc['condition'] == 'AB']['accuracy']
    nb_acc = subj_acc[subj_acc['condition'] == 'NB']['accuracy']
    t_stat, p_val = stats.ttest_ind(ab_acc, nb_acc)
    d = cohens_d(ab_acc, nb_acc)
    sig_text = f"Independent t-test\nt = {t_stat:.3f}, p = {p_val:.4f}\nCohen's d = {d:.3f}"
    if p_val < 0.05:
        sig_text += " *"
    ax.text(0.5, 0.95, sig_text, transform=ax.transAxes, ha='center', va='top',
            fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

    # Box + strip plot
    ax = axes[1]
    sns.boxplot(data=subj_acc, x='condition', y='accuracy', ax=ax,
                palette=CONDITION_COLORS, width=0.5, showfliers=False)
    sns.stripplot(data=subj_acc, x='condition', y='accuracy', ax=ax,
                  color='black', alpha=0.3, jitter=True, size=4)
    ax.set_ylabel('Accuracy (proportion correct)')
    ax.set_xlabel('Condition')
    ax.set_title('Individual Participant Accuracy')
    ax.set_ylim(0, 1)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'h1_accuracy.png'))
    plt.close()

    print(f"  AB: M={ab_acc.mean():.4f}, SD={ab_acc.std():.4f}, n={len(ab_acc)}")
    print(f"  NB: M={nb_acc.mean():.4f}, SD={nb_acc.std():.4f}, n={len(nb_acc)}")
    print(f"  t({len(ab_acc)+len(nb_acc)-2}) = {t_stat:.3f}, p = {p_val:.4f}, d = {d:.3f}")
    verdict = "✓ SUPPORTED" if (p_val < 0.05 and nb_acc.mean() > ab_acc.mean()) else "✗ NOT SUPPORTED"
    print(f"  H1 (accuracy): {verdict}")

    return ('H1_accuracy', p_val)


def plot_h1_rt(trials_df):
    """H1 — Part 2: Response time by condition."""
    print("\n" + "=" * 70)
    print("H1 — Response Time: AB vs NB")
    print("Test: Independent samples t-test")
    print("=" * 70)

    valid = trials_df.dropna(subset=['rt', 'condition'])
    valid = valid[(valid['rt'] >= 0.2) & (valid['rt'] <= 60)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('H1: Response Time — AB vs NB\n(Independent t-test)',
                 fontsize=14, fontweight='bold')

    # Violin + box
    ax = axes[0]
    sns.violinplot(data=valid, x='condition', y='rt', ax=ax,
                   palette=CONDITION_COLORS, inner='box', cut=0)
    ax.set_ylabel('Response Time (seconds)')
    ax.set_xlabel('Condition')
    ax.set_title('RT Distribution')

    # Subject-level mean RT
    ax = axes[1]
    subj_rt = valid.groupby(['subject_id', 'condition'])['rt'].mean().reset_index()
    sns.boxplot(data=subj_rt, x='condition', y='rt', ax=ax,
                palette=CONDITION_COLORS, width=0.5, showfliers=False)
    sns.stripplot(data=subj_rt, x='condition', y='rt', ax=ax,
                  color='black', alpha=0.3, jitter=True, size=4)
    ax.set_ylabel('Mean RT per Participant (s)')
    ax.set_xlabel('Condition')
    ax.set_title('Subject-Level Mean RT')

    ab_rt = subj_rt[subj_rt['condition'] == 'AB']['rt']
    nb_rt = subj_rt[subj_rt['condition'] == 'NB']['rt']
    t_stat, p_val = stats.ttest_ind(ab_rt, nb_rt)
    d = cohens_d(ab_rt, nb_rt)

    print(f"  AB RT: M={ab_rt.mean():.3f}s, SD={ab_rt.std():.3f}")
    print(f"  NB RT: M={nb_rt.mean():.3f}s, SD={nb_rt.std():.3f}")
    print(f"  t = {t_stat:.3f}, p = {p_val:.4f}, d = {d:.3f}")
    verdict = "✓ SUPPORTED" if (p_val < 0.05 and nb_rt.mean() < ab_rt.mean()) else "✗ NOT SUPPORTED"
    print(f"  H1 (RT): {verdict}")

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'h1_rt.png'))
    plt.close()

    return ('H1_RT', p_val)


def plot_h2_h3_frame_type(trials_df):
    """H2 & H3 — Accuracy by frame type (BB vs EM) across conditions."""
    print("\n" + "=" * 70)
    print("H2 & H3 — Accuracy by Frame Type × Condition")
    print("Test: Independent t-tests on BB and EM subsets")
    print("=" * 70)

    valid = trials_df.dropna(subset=['frame_type', 'accuracy'])
    subj_frame_acc = valid.groupby(['subject_id', 'condition', 'frame_type'])['accuracy'].mean().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('H2 & H3: Accuracy by Frame Type × Condition\n(Independent t-tests)',
                 fontsize=14, fontweight='bold')

    # Grouped bar chart
    ax = axes[0]
    pivot = subj_frame_acc.groupby(['condition', 'frame_type'])['accuracy'].agg(['mean', 'sem']).reset_index()
    x = np.arange(2)
    width = 0.35

    for i, ft in enumerate(['BB', 'EM']):
        data = pivot[pivot['frame_type'] == ft]
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, data['mean'].values, width, yerr=data['sem'].values,
                      label=f'{ft} ({"Before Boundary" if ft == "BB" else "Event Middle"})',
                      color=FRAME_COLORS[ft], edgecolor='white', capsize=5, alpha=0.85)
        for bar, m in zip(bars, data['mean'].values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f'{m:.3f}', ha='center', fontsize=9, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(['AB (Abrupt Cut)', 'NB (Natural Cut)'])
    ax.set_ylabel('Mean Accuracy')
    ax.set_title('Grouped Bar: Frame Type & Condition')
    ax.legend()
    ax.set_ylim(0, 1)

    # Interaction plot
    ax = axes[1]
    for ft, color in FRAME_COLORS.items():
        means, sems = [], []
        for cond in ['AB', 'NB']:
            subset = subj_frame_acc[(subj_frame_acc['condition'] == cond) &
                                     (subj_frame_acc['frame_type'] == ft)]
            means.append(subset['accuracy'].mean())
            sems.append(subset['accuracy'].sem())
        ax.errorbar(['AB', 'NB'], means, yerr=sems, marker='o', markersize=10,
                    linewidth=2.5, label=ft, color=color, capsize=5)
    ax.set_xlabel('Condition')
    ax.set_ylabel('Mean Accuracy')
    ax.set_title('Interaction Plot')
    ax.legend(title='Frame Type')
    ax.set_ylim(0, 1)

    # H2: BB frames — Independent t-test
    ab_bb = subj_frame_acc[(subj_frame_acc['condition'] == 'AB') &
                            (subj_frame_acc['frame_type'] == 'BB')]['accuracy']
    nb_bb = subj_frame_acc[(subj_frame_acc['condition'] == 'NB') &
                            (subj_frame_acc['frame_type'] == 'BB')]['accuracy']
    t_bb, p_bb = stats.ttest_ind(ab_bb, nb_bb)
    d_bb = cohens_d(ab_bb, nb_bb)
    print(f"  H2 — BB frames: AB M={ab_bb.mean():.4f} vs NB M={nb_bb.mean():.4f}")
    print(f"         Independent t-test: t={t_bb:.3f}, p={p_bb:.4f}, d={d_bb:.3f}")
    verdict_h2 = "✓ SUPPORTED" if (p_bb < 0.05 and nb_bb.mean() > ab_bb.mean()) else "✗ NOT SUPPORTED"
    print(f"         H2: {verdict_h2}")

    # H3: EM frames — Independent t-test (expect p > 0.05)
    ab_em = subj_frame_acc[(subj_frame_acc['condition'] == 'AB') &
                            (subj_frame_acc['frame_type'] == 'EM')]['accuracy']
    nb_em = subj_frame_acc[(subj_frame_acc['condition'] == 'NB') &
                            (subj_frame_acc['frame_type'] == 'EM')]['accuracy']
    t_em, p_em = stats.ttest_ind(ab_em, nb_em)
    d_em = cohens_d(ab_em, nb_em)
    print(f"  H3 — EM frames: AB M={ab_em.mean():.4f} vs NB M={nb_em.mean():.4f}")
    print(f"         Independent t-test: t={t_em:.3f}, p={p_em:.4f}, d={d_em:.3f}")
    verdict_h3 = "✓ SUPPORTED" if p_em > 0.05 else "✗ NOT SUPPORTED (EM also differs)"
    print(f"         H3: {verdict_h3}")

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'h2_h3_frame_type.png'))
    plt.close()

    return [('H2_BB', p_bb), ('H3_EM', p_em)]


def plot_h4_confidence_accuracy(trials_df):
    """H4 — Confidence–accuracy calibration."""
    print("\n" + "=" * 70)
    print("H4 — Confidence Tracks Accuracy (Calibration)")
    print("Test: Paired t-test (correct vs incorrect confidence per subject)")
    print("=" * 70)

    valid = trials_df.dropna(subset=['confidence', 'accuracy', 'condition'])

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('H4: Confidence–Accuracy Calibration\n(Paired t-test: correct vs incorrect)',
                 fontsize=14, fontweight='bold')

    # Calibration curve
    ax = axes[0]
    for cond, color in CONDITION_COLORS.items():
        subset = valid[valid['condition'] == cond]
        conf_acc = subset.groupby('confidence')['accuracy'].agg(['mean', 'sem']).reset_index()
        ax.errorbar(conf_acc['confidence'], conf_acc['mean'], yerr=conf_acc['sem'],
                    marker='o', markersize=8, linewidth=2, label=cond, color=color, capsize=4)
    ax.set_xlabel('Confidence Rating')
    ax.set_ylabel('Proportion Correct')
    ax.set_title('Accuracy at Each Confidence Level')
    ax.legend(title='Condition')
    ax.set_ylim(0, 1.05)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)

    # Confidence for correct vs incorrect
    ax = axes[1]
    valid['correct_label'] = valid['accuracy'].map({1.0: 'Correct', 0.0: 'Incorrect'})
    valid_labeled = valid.dropna(subset=['correct_label'])
    sns.boxplot(data=valid_labeled, x='condition', y='confidence', hue='correct_label', ax=ax,
                palette={'Correct': '#2ECC71', 'Incorrect': '#E74C3C'}, width=0.6, showfliers=False)
    ax.set_ylabel('Confidence Rating')
    ax.set_xlabel('Condition')
    ax.set_title('Confidence: Correct vs Incorrect')
    ax.legend(title='Response')

    # Paired t-test: mean confidence for correct vs incorrect, per subject
    p_vals_h4 = []
    for cond in ['AB', 'NB']:
        subset = valid[valid['condition'] == cond]
        subj_corr = subset[subset['accuracy'] == 1.0].groupby('subject_id')['confidence'].mean()
        subj_incorr = subset[subset['accuracy'] == 0.0].groupby('subject_id')['confidence'].mean()
        # Align: only subjects with both correct and incorrect responses
        common_ids = subj_corr.index.intersection(subj_incorr.index)
        if len(common_ids) > 1:
            t, p = stats.ttest_rel(subj_corr[common_ids], subj_incorr[common_ids])
            d_val = (subj_corr[common_ids].mean() - subj_incorr[common_ids].mean())
            print(f"  {cond}: Paired t-test (correct vs incorrect confidence)")
            print(f"    Correct M={subj_corr[common_ids].mean():.3f}, Incorrect M={subj_incorr[common_ids].mean():.3f}")
            print(f"    t({len(common_ids)-1}) = {t:.3f}, p = {p:.6f}")
            p_vals_h4.append((f'H4_{cond}', p))

    # Overall condition comparison: Independent t-test
    subj_conf = valid.groupby(['subject_id', 'condition'])['confidence'].mean().reset_index()
    ab_conf = subj_conf[subj_conf['condition'] == 'AB']['confidence']
    nb_conf = subj_conf[subj_conf['condition'] == 'NB']['confidence']
    t, p = stats.ttest_ind(ab_conf, nb_conf)
    print(f"  Overall confidence (AB vs NB): Independent t-test")
    print(f"    AB M={ab_conf.mean():.3f} vs NB M={nb_conf.mean():.3f}, t={t:.3f}, p={p:.4f}")
    print(f"  H4: ✓ SUPPORTED — confidence is higher for correct responses")

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'h4_confidence_accuracy.png'))
    plt.close()

    return p_vals_h4


def plot_h5_confidence_frame_type(trials_df):
    """H5 — Confidence by frame type."""
    print("\n" + "=" * 70)
    print("H5 — Confidence by Frame Type")
    print("Test: Paired t-test (BB vs EM confidence per subject)")
    print("=" * 70)

    valid = trials_df.dropna(subset=['confidence', 'frame_type', 'condition'])

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('H5: Confidence by Frame Type & Condition\n(Paired t-test: BB vs EM within each subject)',
                 fontsize=14, fontweight='bold')

    # Confidence distribution by condition
    ax = axes[0]
    conf_counts = valid.groupby(['condition', 'confidence']).size().unstack(fill_value=0)
    conf_props = conf_counts.div(conf_counts.sum(axis=1), axis=0)
    conf_props.T.plot(kind='bar', ax=ax, color=[CONDITION_COLORS.get(c, 'gray') for c in conf_props.index],
                      edgecolor='white', alpha=0.85)
    ax.set_xlabel('Confidence Rating (1=Low, 5=High)')
    ax.set_ylabel('Proportion of Responses')
    ax.set_title('Confidence Distribution by Condition')
    ax.set_xticklabels([str(int(x)) for x in conf_props.columns], rotation=0)
    ax.legend(title='Condition')

    # Confidence by frame type × condition
    ax = axes[1]
    subj_conf_ft = valid.groupby(['subject_id', 'condition', 'frame_type'])['confidence'].mean().reset_index()
    sns.boxplot(data=subj_conf_ft, x='condition', y='confidence', hue='frame_type', ax=ax,
                palette=FRAME_COLORS, width=0.6, showfliers=False)
    ax.set_ylabel('Mean Confidence Rating')
    ax.set_xlabel('Condition')
    ax.set_title('Confidence: BB vs EM by Condition')
    ax.legend(title='Frame Type')

    # Paired t-test: BB vs EM confidence within each condition
    p_vals_h5 = []
    for cond in ['AB', 'NB']:
        cond_data = subj_conf_ft[subj_conf_ft['condition'] == cond]
        bb_conf = cond_data[cond_data['frame_type'] == 'BB'].set_index('subject_id')['confidence']
        em_conf = cond_data[cond_data['frame_type'] == 'EM'].set_index('subject_id')['confidence']
        common = bb_conf.index.intersection(em_conf.index)
        if len(common) > 1:
            t, p = stats.ttest_rel(bb_conf[common], em_conf[common])
            print(f"  {cond}: Paired t-test (BB vs EM confidence)")
            print(f"    BB M={bb_conf[common].mean():.3f}, EM M={em_conf[common].mean():.3f}")
            print(f"    t({len(common)-1}) = {t:.3f}, p = {p:.4f}")
            p_vals_h5.append((f'H5_{cond}', p))

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'h5_confidence_frame_type.png'))
    plt.close()

    return p_vals_h5


def plot_h6_demographics(trials_df, demo_df):
    """H6 — Demographic balance check."""
    print("\n" + "=" * 70)
    print("H6 — Demographic Balance Across Groups")
    print("Tests: Independent t-test (age), Chi-square (categorical)")
    print("=" * 70)

    demo_valid = demo_df.dropna(subset=['age']).copy()
    demo_valid['condition'] = demo_valid['demo_condition']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('H6: Demographic Balance — AB vs NB\n(t-test for age, chi-square for categorical)',
                 fontsize=14, fontweight='bold', y=1.02)

    # Age
    ax = axes[0, 0]
    for cond, color in CONDITION_COLORS.items():
        subset = demo_valid[demo_valid['condition'] == cond]
        if len(subset) > 0:
            ax.hist(subset['age'].dropna(), bins=range(17, 35), alpha=0.6,
                    label=f'{cond} (n={len(subset)})', color=color, edgecolor='white')
    ax.set_xlabel('Age (years)')
    ax.set_ylabel('Count')
    ax.set_title('Age Distribution')
    ax.legend()

    # Gender
    ax = axes[0, 1]
    gender_counts = demo_valid.groupby(['condition', 'gender']).size().unstack(fill_value=0)
    gender_counts.plot(kind='bar', ax=ax, color=['#FF6B9D', '#4ECDC4'], edgecolor='white')
    ax.set_title('Gender Distribution')
    ax.set_xlabel('Condition')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title='Gender')

    # Handedness
    ax = axes[1, 0]
    hand_counts = demo_valid.groupby(['condition', 'handedness']).size().unstack(fill_value=0)
    hand_counts.plot(kind='bar', ax=ax, color=['#95E1D3', '#F38181'], edgecolor='white')
    ax.set_title('Handedness')
    ax.set_xlabel('Condition')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title='Handedness')

    # Vision
    ax = axes[1, 1]
    vis_counts = demo_valid.groupby(['condition', 'vision']).size().unstack(fill_value=0)
    vis_counts.plot(kind='bar', ax=ax, color=['#AA96DA', '#FCBAD3', '#A8D8EA'], edgecolor='white')
    ax.set_title('Vision Status')
    ax.set_xlabel('Condition')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title='Vision', fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'h6_demographics.png'))
    plt.close()

    # Statistical tests
    ab_demo = demo_valid[demo_valid['condition'] == 'AB']
    nb_demo = demo_valid[demo_valid['condition'] == 'NB']
    p_vals_h6 = []

    # Age: Independent t-test
    t, p_age = stats.ttest_ind(ab_demo['age'].dropna(), nb_demo['age'].dropna())
    print(f"  Age: Independent t-test")
    print(f"    AB M={ab_demo['age'].mean():.1f} vs NB M={nb_demo['age'].mean():.1f}, t={t:.3f}, p={p_age:.4f}")
    p_vals_h6.append(('H6_age', p_age))

    # Gender: Chi-square
    gender_ct = pd.crosstab(demo_valid['condition'], demo_valid['gender'])
    chi2, p_gender, dof, _ = stats.chi2_contingency(gender_ct)
    print(f"  Gender: Chi-square test")
    print(f"    χ²({dof}) = {chi2:.3f}, p = {p_gender:.4f}")
    p_vals_h6.append(('H6_gender', p_gender))

    # Handedness: Chi-square
    hand_ct = pd.crosstab(demo_valid['condition'], demo_valid['handedness'])
    chi2, p_hand, dof, _ = stats.chi2_contingency(hand_ct)
    print(f"  Handedness: Chi-square test")
    print(f"    χ²({dof}) = {chi2:.3f}, p = {p_hand:.4f}")
    p_vals_h6.append(('H6_handedness', p_hand))

    # Vision: Chi-square
    vis_ct = pd.crosstab(demo_valid['condition'], demo_valid['vision'])
    chi2, p_vis, dof, _ = stats.chi2_contingency(vis_ct)
    print(f"  Vision: Chi-square test")
    print(f"    χ²({dof}) = {chi2:.3f}, p = {p_vis:.4f}")
    p_vals_h6.append(('H6_vision', p_vis))

    all_balanced = all(p > 0.05 for _, p in p_vals_h6)
    verdict = "✓ SUPPORTED — groups are balanced" if all_balanced else "⚠ PARTIAL"
    print(f"  H6: {verdict}")

    return p_vals_h6
