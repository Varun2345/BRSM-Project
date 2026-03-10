import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from config import PLOT_DIR, EXP_PLOT_DIR

from data_loader import load_all_data

from hypotheses import (
    plot_h1_accuracy,
    plot_h1_rt,
    plot_h2_h3_frame_type,
    plot_h4_confidence_accuracy,
    plot_h5_confidence_frame_type,
    plot_h6_demographics
)

from exploratory import (
    plot_exp_per_movie,
    plot_exp_demographic_effects,
    plot_exp_rt_frame_type,
    plot_exp_correlation_matrix
)

from multiple_comparisons import print_multiple_comparison_summary

def main():
    # Load and clean data
    trials_df, demo_df = load_all_data()

    # Collect all p-values for multiple comparison correction
    all_p_values = []

    # ── Hypothesis-driven plots ──
    p1 = plot_h1_accuracy(trials_df)
    all_p_values.append(p1)

    p2 = plot_h1_rt(trials_df)
    all_p_values.append(p2)

    p3_list = plot_h2_h3_frame_type(trials_df)
    all_p_values.extend(p3_list)

    p4_list = plot_h4_confidence_accuracy(trials_df)
    all_p_values.extend(p4_list)

    p5_list = plot_h5_confidence_frame_type(trials_df)
    all_p_values.extend(p5_list)

    p6_list = plot_h6_demographics(trials_df, demo_df)
    all_p_values.extend(p6_list)

    # ── Exploratory plots ──
    plot_exp_per_movie(trials_df)
    plot_exp_demographic_effects(trials_df)
    plot_exp_rt_frame_type(trials_df)
    plot_exp_correlation_matrix(trials_df)

    # ── Multiple Comparison Summary ──
    print_multiple_comparison_summary(all_p_values)


if __name__ == "__main__":
    main()
