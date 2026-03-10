import os
import matplotlib.pyplot as plt

from config import PLOT_DIR
from corrections import bonferroni_correction, holm_correction, benjamini_hochberg_correction

def print_multiple_comparison_summary(all_p_values):
    """Apply and compare Bonferroni, Holm, and BH corrections across all tests."""
    print("\n" + "=" * 70)
    print("MULTIPLE COMPARISON CORRECTIONS")
    print("=" * 70)

    print(f"\n  Total hypothesis tests conducted: {len(all_p_values)}")
    print(f"  Uncorrected α = 0.05")

    # Bonferroni
    print(f"\n  ── BONFERRONI CORRECTION (α / {len(all_p_values)} = {0.05/len(all_p_values):.4f}) ──")
    bonf = bonferroni_correction(all_p_values)
    for label, p, adj_alpha, sig in bonf:
        print(f"    {label:20s}: p={p:.4f}  α_adj={adj_alpha:.4f}")

    # Holm
    print(f"\n  ── HOLM (STEP-DOWN) CORRECTION ──")
    holm = holm_correction(all_p_values)
    for label, p, adj_alpha, sig in holm:
        print(f"    {label:20s}: p={p:.4f}  α_adj={adj_alpha:.4f}")

    # Benjamini-Hochberg
    print(f"\n  ── BENJAMINI-HOCHBERG (FDR) CORRECTION ──")
    bh = benjamini_hochberg_correction(all_p_values)
    for label, p, threshold, sig in bh:
        print(f"    {label:20s}: p={p:.4f}  BH_thresh={threshold:.4f}")

    # ── Generate Image Table dynamically ──
    label_map = {
        "H1_accuracy": ("H1a", "Overall accuracy", "Alt"),
        "H1_RT": ("H1b", "Overall RT", "Alt"),
        "H2_BB": ("H2", "BB-frame accuracy", "Alt"),
        "H3_EM": ("H3", "EM-frame accuracy", "Null"),
        "H4_AB": ("H4", "Confidence (AB)", "Alt"),
        "H4_NB": ("H4", "Confidence (NB)", "Alt"),
        "H5_AB": ("H5", "Confidence BB vs EM (AB)", "Alt"),
        "H5_NB": ("H5", "Confidence BB vs EM (NB)", "Alt"),
        "H6_age": ("H6a", "Age", "Null"),
        "H6_gender": ("H6b", "Gender", "Null"),
        "H6_handedness": ("H6c", "Handedness", "Null"),
        "H6_vision": ("H6d", "Vision", "Null")
    }

    # Desired order in table
    ordered_labels = ["H1_accuracy", "H1_RT", "H2_BB", "H3_EM", "H4_AB", "H4_NB", "H5_AB", "H5_NB", "H6_age", "H6_gender", "H6_handedness", "H6_vision"]

    p_dict = {label: p for label, p in all_p_values}
    holm_dict = {label: limit for label, p, limit, sig in holm}
    bh_dict = {label: limit for label, p, limit, sig in bh}

    data = []
    for label in ordered_labels:
        if label in label_map and label in p_dict and label in holm_dict and label in bh_dict:
            tid, desc, hyp_type = label_map[label]
            data.append((tid, desc, p_dict[label], holm_dict[label], bh_dict[label], hyp_type))

    def format_p(val):
        if val < 0.001:
            return "<.001"
        return f"{val:.3f}".replace("0.", ".")

    def is_supported(raw_p, threshold, hyp_type):
        if hyp_type == "Alt":
            return raw_p < threshold
        else: # "Null"
            return raw_p >= threshold

    table_data = []
    cell_colors = []
    header_color = "#4472c4"
    row_colors = ["#f2f2f2", "#ffffff"]
    sig_color = "#c6efce"
    ns_color = "#ffc7ce"

    for i, row in enumerate(data):
        test_id, desc, raw_p, holm_limit, bh_limit, hyp_type = row
        raw_support = is_supported(raw_p, 0.05, hyp_type)
        holm_support = is_supported(raw_p, holm_limit, hyp_type)
        bh_support = is_supported(raw_p, bh_limit, hyp_type)

        raw_str = f"{'✓' if raw_support else '✗'} {format_p(raw_p)}"
        holm_str = f"{'✓' if holm_support else '✗'} {format_p(holm_limit)}"
        bh_str = f"{'✓' if bh_support else '✗'} {format_p(bh_limit)}"

        table_data.append([test_id, desc, format_p(raw_p), format_p(holm_limit), format_p(bh_limit), raw_str, holm_str, bh_str])

        base_color = row_colors[i % 2]
        cell_colors.append([
            base_color, base_color, base_color, base_color, base_color,
            sig_color if raw_support else ns_color,
            sig_color if holm_support else ns_color,
            sig_color if bh_support else ns_color
        ])

    original_font_family = plt.rcParams['font.family']
    plt.rcParams['font.family'] = 'sans-serif'

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('off')
    ax.axis('tight')

    columns = ["Test", "Description", "Raw p", "Holm α limit", "BH-FDR threshold", "Support (Raw)", "Support (Holm)", "Support (BH-FDR)"]
    table = ax.table(cellText=table_data, colLabels=columns, cellColours=cell_colors, loc='center', cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    for i in range(len(columns)):
        cell = table[0, i]
        cell.set_facecolor(header_color)
        cell.set_text_props(color='white', weight='bold')

    table.auto_set_column_width(col=list(range(len(columns))))
    table._cells[(0, 1)].set_width(0.35)
    for i in range(1, len(data) + 1):
        table._cells[(i, 1)].set_width(0.35)

    footnote_text = (
        "Note on symbols:\n"
        "✓ = Hypothesis Supported. ✗ = Hypothesis Not Supported.\n"
        "For H1, H2, H4, H5 (predicting a difference): Supported if Raw p < Threshold Limit.\n"
        "For H3, H6 (predicting NO difference): Supported if Raw p \u2265 Threshold Limit."
    )
    plt.figtext(0.1, 0.05, footnote_text, fontsize=10, style='italic', va='top')
    plt.title("Table 3.8: Multiple Comparisons Correction and Hypothesis Support", fontweight="bold", fontsize=14, pad=20)

    plt.tight_layout()
    output_path = os.path.join(PLOT_DIR, "multiple_comparisons.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Restore font
    plt.rcParams['font.family'] = original_font_family

