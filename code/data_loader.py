import os
import glob
import re
import numpy as np
import pandas as pd
from config import DATA_DIR, DEMO_FILE

def load_all_data():
    """Load all participant CSVs, extract recognition trials, merge demographics,
    and perform vigilance-based data cleaning."""
    print("=" * 70)
    print("LOADING DATA")
    print("=" * 70)

    csv_files = sorted(glob.glob(os.path.join(DATA_DIR, "sub*_recognitionstage_*.csv")))
    print(f"Found {len(csv_files)} participant CSV files.")

    all_trials = []

    for fpath in csv_files:
        fname = os.path.basename(fpath)
        match = re.match(r'(sub\d+)_(AB|NB)\s*_recognitionstage_', fname)
        if not match:
            match = re.match(r'(sub\d+)_(AB|NB)_recognitionstage_', fname)
        if not match:
            continue

        sub_id = match.group(1)
        condition = match.group(2)

        if sub_id == 'sub42':
            print(f"  Excluding {sub_id} (no trial data available).")
            continue
            
        if sub_id == 'sub157':
            # Reclassify sub157 from AB to NB based on video paths
            condition = 'NB'
            
        try:
            df = pd.read_csv(fpath)
        except Exception:
            continue

        if 'movie_id' not in df.columns or 'resp.corr' not in df.columns:
            continue

        trial_rows = df[df['movie_id'].notna()].copy()
        if len(trial_rows) == 0:
            continue

        trial_rows['subject_id'] = sub_id
        trial_rows['condition'] = condition

        def get_frame_type(img_path):
            if pd.isna(img_path):
                return np.nan
            if '_BB_T' in str(img_path):
                return 'BB'
            elif '_EM_T' in str(img_path):
                return 'EM'
            return np.nan

        trial_rows['frame_type'] = trial_rows['target_img'].apply(get_frame_type)

        def parse_rt(val):
            if pd.isna(val):
                return np.nan
            s = str(val).strip("[]' ")
            try:
                return float(s)
            except Exception:
                return np.nan

        trial_rows['rt'] = trial_rows['resp.rt'].apply(parse_rt)
        trial_rows['accuracy'] = pd.to_numeric(trial_rows['resp.corr'], errors='coerce')
        trial_rows['confidence'] = pd.to_numeric(trial_rows['conf_radio.response'], errors='coerce')
        trial_rows['movie_id_num'] = pd.to_numeric(trial_rows['movie_id'], errors='coerce')

        # Encoding time for vigilance check
        vid_start_col = 'instruction_2.stopped'
        vid_end_col = 'Videos.stopped'
        if vid_start_col in df.columns and vid_end_col in df.columns:
            enc_start = pd.to_numeric(df[vid_start_col], errors='coerce').dropna()
            enc_end = pd.to_numeric(df[vid_end_col], errors='coerce').dropna()
            if len(enc_start) > 0 and len(enc_end) > 0:
                encoding_time = enc_end.max() - enc_start.min()
                trial_rows['encoding_time_sec'] = encoding_time
                trial_rows['encoding_time_min'] = encoding_time / 60.0
            else:
                trial_rows['encoding_time_sec'] = np.nan
                trial_rows['encoding_time_min'] = np.nan
        else:
            trial_rows['encoding_time_sec'] = np.nan
            trial_rows['encoding_time_min'] = np.nan

        cols_to_keep = ['subject_id', 'condition', 'movie_id_num', 'frame_type',
                        'accuracy', 'rt', 'confidence',
                        'encoding_time_sec', 'encoding_time_min']
        trial_rows = trial_rows[[c for c in cols_to_keep if c in trial_rows.columns]]
        all_trials.append(trial_rows)

    trials_df = pd.concat(all_trials, ignore_index=True)
    print(f"\nTotal recognition trials loaded: {len(trials_df)}")
    print(f"Unique participants: {trials_df['subject_id'].nunique()}")
    print(f"Condition split: {trials_df.groupby('condition')['subject_id'].nunique().to_dict()}")

    # Load demographics
    demo_df = pd.read_excel(DEMO_FILE)
    demo_df.columns = ['sub_id_raw', 'age', 'gender', 'handedness', 'vision']
    demo_df['subject_id'] = demo_df['sub_id_raw'].str.lower().str.replace(r'_[a-z]{2}$', '', regex=True)
    demo_df['demo_condition'] = demo_df['sub_id_raw'].str.extract(r'_(AB|NB|ab|nb)$', expand=False)
    demo_df['demo_condition'] = demo_df['demo_condition'].str.upper()

    trials_df['subject_id_norm'] = trials_df['subject_id'].str.lower()
    demo_for_merge = demo_df[['subject_id', 'age', 'gender', 'handedness', 'vision']].copy()
    demo_for_merge = demo_for_merge.rename(columns={'subject_id': 'subject_id_norm'})
    trials_df = trials_df.merge(demo_for_merge, on='subject_id_norm', how='left')

    # ── VIGILANCE-BASED DATA CLEANING ──
    VIGILANCE_THRESHOLD_MIN = 27.05
    subj_enc_time = trials_df.groupby('subject_id')['encoding_time_min'].first().reset_index()
    subj_enc_time = subj_enc_time.dropna(subset=['encoding_time_min'])
    inattentive_ids = subj_enc_time[
        subj_enc_time['encoding_time_min'] > VIGILANCE_THRESHOLD_MIN
    ]['subject_id'].tolist()

    n_before = trials_df['subject_id'].nunique()
    print(f"\n── VIGILANCE-BASED DATA CLEANING ──")
    print(f"  Threshold: {VIGILANCE_THRESHOLD_MIN} minutes")
    print(f"  Participants before cleaning: {n_before}")
    print(f"  Inattentive participants (>{VIGILANCE_THRESHOLD_MIN} min): {len(inattentive_ids)}")
    if inattentive_ids:
        print(f"  Removed IDs: {inattentive_ids}")
        for sid in inattentive_ids:
            cond = trials_df[trials_df['subject_id'] == sid]['condition'].iloc[0]
            enc_t = subj_enc_time[subj_enc_time['subject_id'] == sid]['encoding_time_min'].values[0]
            print(f"    {sid} ({cond}): {enc_t:.2f} min")

    trials_df = trials_df[~trials_df['subject_id'].isin(inattentive_ids)].copy()

    n_after = trials_df['subject_id'].nunique()
    print(f"  Participants after cleaning: {n_after}")
    print(f"  Trials after cleaning: {len(trials_df)}")
    print(f"  Condition split: {trials_df.groupby('condition')['subject_id'].nunique().to_dict()}")

    # ── RT OUTLIER FLAGGING ──
    rt_outliers = trials_df[(trials_df['rt'] < 0.2) | (trials_df['rt'] > 60)]
    if len(rt_outliers) > 0:
        print(f"\n── RT OUTLIER FLAGGING ──")
        print(f"  Trials with RT < 0.2s or > 60s: {len(rt_outliers)}")
        for _, r in rt_outliers.iterrows():
            print(f"    {r['subject_id']} ({r['condition']}) Movie {r['movie_id_num']:.0f}: RT={r['rt']:.3f}s")

    return trials_df, demo_df
