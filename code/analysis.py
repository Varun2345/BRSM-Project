import matplotlib
matplotlib.use('Agg')

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
    run_accuracy_glm,
    plot_exp_rt_frame_type,
    plot_exp_glm_visuals
)


def main():
    # Load and clean data
    trials_df, demo_df = load_all_data()

    # ── Hypothesis-driven plots ──
    p1 = plot_h1_accuracy(trials_df)
    p2 = plot_h1_rt(trials_df)
    p3_list = plot_h2_h3_frame_type(trials_df)
    p4_list = plot_h4_confidence_accuracy(trials_df)
    p5_list = plot_h5_confidence_frame_type(trials_df)
    p6_list = plot_h6_demographics(trials_df, demo_df)


    # ── Exploratory analysis ──
    run_accuracy_glm(trials_df)
    plot_exp_rt_frame_type(trials_df)
    plot_exp_glm_visuals(trials_df)

if __name__ == "__main__":
    main()
