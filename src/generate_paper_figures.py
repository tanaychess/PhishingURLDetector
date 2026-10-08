"""
Figure generator module: creates high-resolution publication-quality figures for the IEEE paper.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, auc

# Set clean IEEE academic plot style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 12,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight"
})

def plot_system_architecture(fig_dir):
    """Figure 1: High-level System Architecture Diagram."""
    fig, ax = plt.subplots(figsize=(8.5, 3.8), dpi=300)
    ax.axis("off")
    
    # Draw block diagram components
    boxes = [
        {"x": 0.04, "y": 0.38, "w": 0.17, "h": 0.44, "title": "URL Stream &\nBenchmark Corpus\n(58,645 URLs)", "color": "#e8f4f8", "edge": "#2980b9"},
        {"x": 0.25, "y": 0.38, "w": 0.19, "h": 0.44, "title": "Structured Feature\nRepresentation\n(98 Retained Feats)", "color": "#eafaf1", "edge": "#27ae60"},
        {"x": 0.48, "y": 0.38, "w": 0.18, "h": 0.44, "title": "Machine Learning\nClassifiers\n(XGBoost / RF / DT)", "color": "#fef9e7", "edge": "#f39c12"},
        {"x": 0.70, "y": 0.56, "w": 0.26, "h": 0.34, "title": "Prediction Engine\n(Phishing vs. Legitimate)", "color": "#fbeee6", "edge": "#e67e22"},
        {"x": 0.70, "y": 0.10, "w": 0.26, "h": 0.38, "title": "TreeSHAP Attribution\n(Training Ranks &\nLocal Waterfall Triage)", "color": "#f4ecf7", "edge": "#8e44ad"},
    ]
    
    for b in boxes:
        rect = plt.Rectangle((b["x"], b["y"]), b["w"], b["h"], facecolor=b["color"], edgecolor=b["edge"], linewidth=1.8, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"]/2, b["title"], horizontalalignment='center', verticalalignment='center', fontsize=9.5, fontweight='bold', transform=ax.transAxes)
        
    # Draw arrows
    arrows = [
        (0.21, 0.60, 0.25, 0.60),
        (0.44, 0.60, 0.48, 0.60),
        (0.66, 0.60, 0.70, 0.73),
        (0.66, 0.60, 0.70, 0.29)
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=2.2))
        
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig1_system_architecture.png"))
    plt.savefig(os.path.join(fig_dir, "fig1_system_architecture.pdf"))
    plt.close()

def plot_class_distribution(y_train, y_test, fig_dir):
    """Figure 2: Dataset Class Distribution."""
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=300)
    
    train_counts = [int(sum(y_train == 0)), int(sum(y_train == 1))]
    test_counts = [int(sum(y_test == 0)), int(sum(y_test == 1))]
    
    labels = ["Legitimate (0)", "Phishing (1)"]
    x = np.arange(len(labels))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, train_counts, width, label='Training Set (80%)', color='#2980b9', edgecolor='black', alpha=0.9)
    rects2 = ax.bar(x + width/2, test_counts, width, label='Testing Set (20%)', color='#e74c3c', edgecolor='black', alpha=0.9)
    
    ax.set_ylabel('Sample Count', fontweight='bold', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontweight='bold', fontsize=11)
    max_count = max(train_counts)
    ax.set_ylim(0, max_count * 1.25)
    ax.legend(loc='upper right', framealpha=0.92, fontsize=9.5)
    ax.grid(True, linestyle='--', alpha=0.4, axis='y')
    
    # Add count labels on bars
    for rects in [rects1, rects2]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{int(height):,}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
            
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig2_class_distribution.png"))
    plt.savefig(os.path.join(fig_dir, "fig2_class_distribution.pdf"))
    plt.close()
def plot_model_comparison(results_df, fig_dir):
    """Figure 3: Model Performance Comparison Bar Plot with non-overlapping legend."""
    fig, ax = plt.subplots(figsize=(8.0, 4.4), dpi=300)
    
    models = results_df["model"]
    x = np.arange(len(models))
    width = 0.26
    
    rects1 = ax.bar(x - width, results_df["accuracy"] * 100, width, label="Accuracy (%)", color="#2980b9", edgecolor="black", alpha=0.9)
    rects2 = ax.bar(x, results_df["f1_score"] * 100, width, label="F1-Score (%)", color="#27ae60", edgecolor="black", alpha=0.9)
    rects3 = ax.bar(x + width, results_df["roc_auc"] * 100, width, label="ROC-AUC (%)", color="#8e44ad", edgecolor="black", alpha=0.9)
    
    ax.set_ylabel("Metric Score (%)", fontweight="bold", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15, fontweight="bold", fontsize=9.5)
    ax.set_ylim(80, 104)
    ax.legend(loc="lower right", framealpha=0.95, fontsize=9.5)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")
    
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            h = rect.get_height()
            ax.annotate(f"{h:.1f}%",
                         xy=(rect.get_x() + rect.get_width()/2, h),
                         xytext=(0, 2),
                         textcoords="offset points",
                         ha="center", va="bottom", fontsize=7.5, fontweight="bold", rotation=0)
    
    plt.title("Comparative Performance Across Evaluated Machine Learning Models", fontsize=11, fontweight="bold", pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig3_model_comparison.png"))
    plt.savefig(os.path.join(fig_dir, "fig3_model_comparison.pdf"))
    plt.close()

def plot_confusion_matrices(y_test, test_predictions, fig_dir):
    """Figure 4: Confusion Matrix Heatmaps for Top 2 Models."""
    top_models = ["XGBoost", "Random Forest"]
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8), dpi=300)
    
    for i, m_name in enumerate(top_models):
        if m_name in test_predictions:
            y_pred = test_predictions[m_name]
            cm = confusion_matrix(y_test, y_pred)
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[i],
                        xticklabels=["Legitimate", "Phishing"],
                        yticklabels=["Legitimate", "Phishing"],
                        annot_kws={"size": 11, "weight": "bold"})
            axes[i].set_title(f"Confusion Matrix: {m_name}", fontweight="bold", fontsize=11)
            axes[i].set_xlabel("Predicted Class", fontweight="bold", fontsize=10)
            axes[i].set_ylabel("True Class", fontweight="bold", fontsize=10)
            
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig4_confusion_matrices.png"))
    plt.savefig(os.path.join(fig_dir, "fig4_confusion_matrices.pdf"))
    plt.close()

def plot_roc_pr_curves(y_test, test_probabilities, fig_dir):
    """Figure 5: ROC and Precision-Recall Curves."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.2), dpi=300)
    
    colors = {
        "XGBoost": "#e74c3c",
        "Random Forest": "#27ae60",
        "Decision Tree": "#f39c12",
        "Linear SVM": "#8e44ad",
        "Logistic Regression": "#2980b9"
    }
    
    for name, prob in test_probabilities.items():
        fpr, tpr, _ = roc_curve(y_test, prob)
        roc_auc = auc(fpr, tpr)
        ax1.plot(fpr, tpr, label=f"{name} (AUC={roc_auc:.4f})", color=colors.get(name, "black"), lw=1.8)
        
        prec, rec, _ = precision_recall_curve(y_test, prob)
        pr_auc = auc(rec, prec)
        ax2.plot(rec, prec, label=f"{name} (AP={pr_auc:.4f})", color=colors.get(name, "black"), lw=1.8)
        
    ax1.plot([0, 1], [0, 1], 'k--', lw=1.0, alpha=0.7)
    ax1.set_xlabel('False Positive Rate (FPR)', fontweight='bold', fontsize=10)
    ax1.set_ylabel('True Positive Rate (TPR)', fontweight='bold', fontsize=10)
    ax1.set_title('(a) Receiver Operating Characteristic (ROC)', fontweight='bold', fontsize=11)
    ax1.legend(loc='lower right', fontsize=8.5, framealpha=0.9)
    ax1.grid(True, linestyle='--', alpha=0.4)
    
    ax2.set_xlabel('Recall', fontweight='bold', fontsize=10)
    ax2.set_ylabel('Precision', fontweight='bold', fontsize=10)
    ax2.set_title('(b) Precision-Recall (PR) Curve', fontweight='bold', fontsize=11)
    ax2.legend(loc='lower left', fontsize=8.5, framealpha=0.9)
    ax2.grid(True, linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig5_roc_pr_curves.png"))
    plt.savefig(os.path.join(fig_dir, "fig5_roc_pr_curves.pdf"))
    plt.close()

