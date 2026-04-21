import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
matplotlib.use('Agg')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Data lives one level above the project folder
DATA_DIR = os.path.join(os.path.dirname(ROOT_DIR), "BRSM data csv")
DEMO_FILE = os.path.join(os.path.dirname(ROOT_DIR), "Demographic data.xlsx")

PLOT_DIR = os.path.join(ROOT_DIR, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

EXP_PLOT_DIR = os.path.join(ROOT_DIR, "exploratory_plots")
os.makedirs(EXP_PLOT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.bbox': 'tight',
    'font.family': 'serif',
})

CONDITION_COLORS = {'AB': '#E74C3C', 'NB': '#3498DB'}
FRAME_COLORS = {'BB': '#E67E22', 'EM': '#2ECC71'}
