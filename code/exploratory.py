import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import EXP_PLOT_DIR, CONDITION_COLORS, FRAME_COLORS

def plot_exp_per_movie(trials_df):
    """Exploratory — Per-movie accuracy heatmap."""

    valid = trials_df.dropna(subset=['movie_id_num', 'accuracy', 'condition'])
    movie_acc = valid.groupby(['movie_id_num', 'condition'])['accuracy'].mean().unstack(fill_value=np.nan)
    movie_acc = movie_acc.sort_index()

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Exploratory: Per-Movie Recognition Accuracy', fontsize=14, fontweight='bold')

    ax = axes[0]
    hm_data = movie_acc[['AB', 'NB']] if 'AB' in movie_acc.columns and 'NB' in movie_acc.columns else movie_acc
    sns.heatmap(hm_data, annot=True, fmt='.2f', cmap='RdYlGn', ax=ax,
                vmin=0.3, vmax=1.0, linewidths=0.5, cbar_kws={'label': 'Accuracy'})
    ax.set_ylabel('Movie ID')
    ax.set_xlabel('Condition')
    ax.set_title('Accuracy Heatmap')

    ax = axes[1]
    if 'AB' in movie_acc.columns and 'NB' in movie_acc.columns:
        common = movie_acc.dropna()
        ax.scatter(common['NB'], common['AB'], s=80, alpha=0.7, color='#8E44AD', edgecolor='white')
        lims = [min(common.min().min(), 0.2), max(common.max().max(), 1.0)]
        ax.plot(lims, lims, 'k--', alpha=0.4, label='Equal accuracy')
        ax.set_xlabel('NB Accuracy')
        ax.set_ylabel('AB Accuracy')
        ax.set_title('Movie-Level: AB vs NB')
        ax.legend()
        for idx, row in common.iterrows():
            ax.annotate(str(int(idx)), (row['NB'], row['AB']), fontsize=7, alpha=0.7)

    plt.tight_layout()
    plt.savefig(os.path.join(EXP_PLOT_DIR, 'exp_per_movie.png'))
    plt.close()


def plot_exp_demographic_effects(trials_df):
    """Exploratory — Demographic effects on performance."""

    valid = trials_df.dropna(subset=['accuracy', 'age', 'gender'])
    subj = valid.groupby(['subject_id', 'condition', 'age', 'gender', 'vision']).agg(
        accuracy=('accuracy', 'mean')
    ).reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Exploratory: Demographic Effects on Performance', fontsize=14, fontweight='bold')

    ax = axes[0]
    for cond, color in CONDITION_COLORS.items():
        sub = subj[subj['condition'] == cond]
        ax.scatter(sub['age'], sub['accuracy'], s=60, alpha=0.5, color=color,
                   edgecolor='white', label=cond)
    ax.set_xlabel('Age (years)')
    ax.set_ylabel('Mean Accuracy')
    ax.set_title('Age vs Accuracy')
    ax.legend(title='Condition')

    ax = axes[1]
    sns.boxplot(data=subj, x='gender', y='accuracy', hue='condition', ax=ax,
                palette=CONDITION_COLORS, width=0.6, showfliers=False)
    ax.set_ylabel('Mean Accuracy')
    ax.set_xlabel('Gender')
    ax.set_title('Accuracy by Gender × Condition')

    ax = axes[2]
    sns.boxplot(data=subj.dropna(subset=['vision']), x='vision', y='accuracy', hue='condition', ax=ax,
                palette=CONDITION_COLORS, width=0.6, showfliers=False)
    ax.set_ylabel('Mean Accuracy')
    ax.set_xlabel('Vision Status')
    ax.set_title('Accuracy by Vision × Condition')
    ax.tick_params(axis='x', labelsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(EXP_PLOT_DIR, 'exp_demographic_effects.png'))
    plt.close()


def plot_exp_rt_frame_type(trials_df):
    """Exploratory — RT by frame type × condition."""

    valid = trials_df.dropna(subset=['rt', 'frame_type', 'condition'])
    valid = valid[(valid['rt'] >= 0.2) & (valid['rt'] <= 60)]
    subj_rt = valid.groupby(['subject_id', 'condition', 'frame_type'])['rt'].mean().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Exploratory: RT by Frame Type × Condition', fontsize=14, fontweight='bold')

    ax = axes[0]
    sns.boxplot(data=subj_rt, x='condition', y='rt', hue='frame_type', ax=ax,
                palette=FRAME_COLORS, width=0.6, showfliers=False)
    ax.set_ylabel('Mean RT per Participant (s)')
    ax.set_xlabel('Condition')
    ax.set_title('RT by Frame Type & Condition')
    ax.legend(title='Frame Type')

    ax = axes[1]
    for ft, color in FRAME_COLORS.items():
        means, sems = [], []
        for cond in ['AB', 'NB']:
            sub = subj_rt[(subj_rt['condition'] == cond) & (subj_rt['frame_type'] == ft)]
            means.append(sub['rt'].mean())
            sems.append(sub['rt'].sem())
        ax.errorbar(['AB', 'NB'], means, yerr=sems, marker='s', markersize=10,
                    linewidth=2.5, label=ft, color=color, capsize=5)
    ax.set_xlabel('Condition')
    ax.set_ylabel('Mean RT (seconds)')
    ax.set_title('Interaction Plot: RT')
    ax.legend(title='Frame Type')

    plt.tight_layout()
    plt.savefig(os.path.join(EXP_PLOT_DIR, 'exp_rt_frame_type.png'))
    plt.close()


def plot_exp_correlation_matrix(trials_df):
    """Exploratory — Accuracy-RT-Confidence-Age Correlation Matrix."""

    # We need participant-level means for Accuracy, RT, Confidence, and Age.
    valid = trials_df.dropna(subset=['accuracy', 'rt', 'confidence', 'age'])
    
    # Calculate subject-level means
    subj = valid.groupby(['subject_id', 'age']).agg(
        Accuracy=('accuracy', 'mean'),
        RT=('rt', 'mean'),
        Confidence=('confidence', 'mean')
    ).reset_index()
    
    # Rename age for the plot
    subj = subj.rename(columns={'age': 'Age'})
    
    # Calculate correlation matrix
    corr_vars = ['Accuracy', 'RT', 'Confidence', 'Age']
    corr_matrix = subj[corr_vars].corr(method='pearson')
    
    # Setup plot
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.title('Exploratory: Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
    
    # Create the heatmap
    sns.heatmap(corr_matrix, annot=True, fmt=".3f", cmap="coolwarm", center=0, 
                vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax,
                cbar_kws={"shrink": .8})
    
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(EXP_PLOT_DIR, 'exp_correlation_heatmap.png'))
    plt.close()
