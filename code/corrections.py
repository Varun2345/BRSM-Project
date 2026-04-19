import numpy as np

def bonferroni_correction(p_values, alpha=0.05):
    """Apply Bonferroni correction: adjusted α = α / k."""
    k = len(p_values)
    adjusted_alpha = alpha / k
    results = []
    for label, p in p_values:
        significant = p < adjusted_alpha
        results.append((label, p, adjusted_alpha, significant))
    return results

def holm_correction(p_values, alpha=0.05):
    """Apply Holm (step-down) correction."""
    k = len(p_values)
    sorted_pvals = sorted(p_values, key=lambda x: x[1])
    results = []
    for i, (label, p) in enumerate(sorted_pvals):
        adjusted_alpha = alpha / (k - i)
        significant = p < adjusted_alpha
        results.append((label, p, adjusted_alpha, significant))
    return results

def benjamini_hochberg_correction(p_values, alpha=0.05):
    """Apply Benjamini-Hochberg FDR correction."""
    k = len(p_values)
    sorted_pvals = sorted(p_values, key=lambda x: x[1])
    results = []
    for i, (label, p) in enumerate(sorted_pvals):
        rank = i + 1
        bh_threshold = (rank / k) * alpha
        significant = p < bh_threshold
        results.append((label, p, bh_threshold, significant))
    return results

def cohens_d(group1, group2):
    """Compute Cohen's d effect size for two independent groups."""
    n1, n2 = len(group1), len(group2)
    pooled_std = np.sqrt(((n1 - 1) * group1.std()**2 + (n2 - 1) * group2.std()**2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return (group1.mean() - group2.mean()) / pooled_std
