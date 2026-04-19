import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import EXP_PLOT_DIR, CONDITION_COLORS, FRAME_COLORS

import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

def run_accuracy_glm(trials_df):
    """Exploratory — Logistic Regression (GLM) for Trial-Level Accuracy prediction."""
    print("\n" + "=" * 70)
    print("Exploratory GLM — Predicting Accuracy")
    print("Model: accuracy ~ confidence + condition + frame_type")
    print("=" * 70)

    model_data = trials_df.dropna(subset=['accuracy', 'confidence', 'condition', 'frame_type']).copy()
    
    model_data['accuracy'] = model_data['accuracy'].astype(int)

    try:
        model = smf.logit("accuracy ~ confidence + condition + frame_type", data=model_data)
        result = model.fit(disp=0)

        print(result.summary())

        params = result.params
        pvalues = result.pvalues
        conf = result.conf_int()
        conf['OR'] = params
        conf.columns = ['5%', '95%', 'OR']
        or_df = np.exp(conf)
        print("\nOdds Ratios (exp(beta)):")
        print(or_df)
        
        print("\n" + "-" * 40)
        print("CONCLUSIONS")
        print("-" * 40)
        
        # Interpret Confidence
        if pvalues['confidence'] < 0.05:
            direction = "positive" if params['confidence'] > 0 else "negative"
            print(f"[✓] Confidence: Significant {direction} predictor (p={pvalues['confidence']:.3f}).")
            print(f"    Odds Ratio = {or_df.loc['confidence', 'OR']:.2f}. Each point increase in confidence increases")
            print(f"    odds of accuracy by {((or_df.loc['confidence', 'OR']-1)*100):.1f}%.")
        else:
            print("[ ] Confidence: Not a significant predictor.")

        # Interpret Condition (Main effect at baseline)
        if pvalues.get('condition[T.NB]', 1) < 0.05:
            res = "higher" if params['condition[T.NB]'] > 0 else "lower"
            print(f"[✓] Condition: Significant (p={pvalues['condition[T.NB]']:.3f}).")
            print(f"    NB group has {res} accuracy than AB at baseline confidence.")
        else:
            print("[ ] Condition: No significant main effect (p > .05).")

        # Interpret Frame Type
        if pvalues.get('frame_type[T.EM]', 1) < 0.05:
            res = "higher" if params['frame_type[T.EM]'] > 0 else "lower"
            print(f"[✓] Frame Type: Significant (p={pvalues['frame_type[T.EM]']:.3f}).")
            print(f"    EM frames have {res} accuracy than BB frames.")
        else:
            print("[ ] Frame Type: No significant difference between BB and EM.")


        # --- DIAGNOSTIC CHECKS (VIF) ---
        print("\n" + "-" * 40)
        print("DIAGNOSTIC CHECKS")
        print("-" * 40)
        
        # Prepare data for VIF (must be numeric matrix with intercept)
        from patsy import dmatrices
        _, X = dmatrices("accuracy ~ confidence + condition + frame_type", 
                         data=model_data, return_type='dataframe')
        
        vif_data = pd.DataFrame()
        vif_data["Predictor"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        
        print("VIF (Multi-collinearity) Check:")
        print(vif_data[vif_data['Predictor'] != 'Intercept'].to_string(index=False))
        
        vif_max = vif_data[vif_data['Predictor'] != 'Intercept']['VIF'].max()
        if vif_max < 5:
            print(f"\n[✓] VIF Check Passed: Max VIF is {vif_max:.2f} (under 5.0).")
            print("    The predictors are sufficiently independent; results are stable.")
        else:
            print(f"\n[!] High VIF detected ({vif_max:.2f}). Some predictors may be redundant.")

    except Exception as e:
        print(f"  [Error] GLM failed: {e}")
        print("  Please ensure 'statsmodels' is installed (pip install statsmodels).")


def plot_exp_glm_visuals(trials_df):
    """Exploratory — Visualizing the GLM relationships."""
    
    # 1. Prepare data
    valid = trials_df.dropna(subset=['accuracy', 'confidence', 'condition', 'frame_type']).copy()
    valid['accuracy'] = valid['accuracy'].astype(int)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Exploratory GLM: Visualising Key Predictors of Accuracy', 
                 fontsize=14, fontweight='bold', y=1.02)

    # --- Plot A: Logistic Regression Curves (Accuracy ~ Confidence by Condition) ---
    ax = axes[0]
    for cond, color in CONDITION_COLORS.items():
        subset = valid[valid['condition'] == cond]
        # sns.regplot with logistic=True provides a nice sigmoid fit
        sns.regplot(data=subset, x='confidence', y='accuracy', 
                    logistic=True, scatter=False, ax=ax,
                    label=f'{cond} Condition', color=color, 
                    line_kws={'linewidth': 3})
        
        # Add binned means for context
        binned = subset.groupby('confidence')['accuracy'].mean().reset_index()
        ax.scatter(binned['confidence'], binned['accuracy'], color=color, s=100, 
                   edgecolor='white', alpha=0.8, zorder=5)

    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0.8, 6.2)
    ax.set_xlabel('Subjective Confidence (1-6)')
    ax.set_ylabel('Probability of Correct Recognition')
    ax.set_title('A: Confidence vs. Predicted Accuracy\n(Logistic Fit Curves)')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # --- Plot B: Frame Type x Condition Interaction (Predictive Effects) ---
    ax = axes[1]
    # Calculate means and SEMs per subject first to avoid trial-level bias in error bars
    subj_means = valid.groupby(['subject_id', 'condition', 'frame_type'])['accuracy'].mean().reset_index()
    
    sns.pointplot(data=subj_means, x='frame_type', y='accuracy', hue='condition',
                  palette=CONDITION_COLORS, markers=['o', 's'], linestyles=['-', '--'],
                  errorbar='se', capsize=0.1, ax=ax)
    
    ax.set_ylim(0.7, 0.95) # Zoom in to see differences
    ax.set_ylabel('Mean Recognition Accuracy')
    ax.set_xlabel('Frame Type')
    ax.set_title('B: Frame Type × Condition Interaction\n(Predictive Effects)')
    ax.legend(title='Condition')

    plt.tight_layout()
    plt.savefig(os.path.join(EXP_PLOT_DIR, 'exp_glm_visuals.png'))
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
