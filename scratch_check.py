import json

with open('Automobile.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
    {
        "cell_type": "markdown",
        "id": "kde-header-01",
        "metadata": {},
        "source": [
            "## 📈 KDE vs Normal Distribution Comparison\n",
            "Overlay the actual data distribution (KDE) against a fitted normal curve to see how closely each feature follows a bell curve."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "kde-plot-01",
        "metadata": {},
        "outputs": [],
        "source": [
            "from scipy import stats\n",
            "\n",
            "def kde_vs_normal(data, col_name, ax):\n",
            "    \"\"\"Plot KDE of actual data vs fitted normal curve.\"\"\"\n",
            "    clean = data.dropna()\n",
            "    mu, sigma = clean.mean(), clean.std()\n",
            "\n",
            "    # Histogram (light, just for reference)\n",
            "    ax.hist(clean, bins=25, density=True, alpha=0.3, color='#3498db', edgecolor='white', label='Histogram')\n",
            "\n",
            "    # KDE (actual distribution)\n",
            "    sns.kdeplot(clean, ax=ax, color='#e74c3c', linewidth=2.5, label='KDE (Actual)')\n",
            "\n",
            "    # Fitted Normal curve\n",
            "    x = np.linspace(clean.min() - sigma, clean.max() + sigma, 300)\n",
            "    normal_pdf = stats.norm.pdf(x, mu, sigma)\n",
            "    ax.plot(x, normal_pdf, color='#2c3e50', linewidth=2, linestyle='--', label=f'Normal (\\u03bc={mu:.1f}, \\u03c3={sigma:.1f})')\n",
            "\n",
            "    # Shapiro-Wilk test for normality\n",
            "    stat, p = stats.shapiro(clean[:min(len(clean), 150)])  # Shapiro limited to ~5000\n",
            "    verdict = '\\u2705 Normal' if p > 0.05 else '\\u274c Not Normal'\n",
            "\n",
            "    ax.set_title(f'{col_name}\\nShapiro p={p:.4f} → {verdict}', fontweight='bold', fontsize=11)\n",
            "    ax.set_ylabel('Density')\n",
            "    ax.legend(fontsize=8)\n",
            "\n",
            "print('Function kde_vs_normal() defined \\u2713')"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "kde-plot-02",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- KDE vs Normal for key numeric features ---\n",
            "kde_cols = ['Price', 'Horsepower', 'Engine Size', 'Curb Weight', 'City MPG', 'Highway MPG']\n",
            "\n",
            "fig, axes = plt.subplots(2, 3, figsize=(18, 10))\n",
            "axes = axes.flatten()\n",
            "\n",
            "for i, col in enumerate(kde_cols):\n",
            "    kde_vs_normal(df[col], col, axes[i])\n",
            "\n",
            "plt.suptitle('KDE (Actual) vs Normal Distribution (Fitted)', fontsize=15, fontweight='bold', y=1.02)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "kde-plot-03",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- KDE vs Normal for remaining numeric features ---\n",
            "kde_cols2 = ['Wheelbase', 'Length', 'Width', 'Height', 'Compression Ratio', 'Insurance Risk Score']\n",
            "\n",
            "fig, axes = plt.subplots(2, 3, figsize=(18, 10))\n",
            "axes = axes.flatten()\n",
            "\n",
            "for i, col in enumerate(kde_cols2):\n",
            "    kde_vs_normal(df[col], col, axes[i])\n",
            "\n",
            "plt.suptitle('KDE (Actual) vs Normal Distribution (Fitted)', fontsize=15, fontweight='bold', y=1.02)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "kde-plot-04",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Log-transform on skewed features: Before vs After ---\n",
            "skewed_cols = ['Price', 'Horsepower', 'Engine Size']\n",
            "\n",
            "fig, axes = plt.subplots(len(skewed_cols), 2, figsize=(14, 5 * len(skewed_cols)))\n",
            "\n",
            "for i, col in enumerate(skewed_cols):\n",
            "    clean = df[col].dropna()\n",
            "    log_data = np.log1p(clean)\n",
            "\n",
            "    # Original\n",
            "    kde_vs_normal(clean, f'{col} (Original)', axes[i, 0])\n",
            "\n",
            "    # Log-transformed\n",
            "    kde_vs_normal(log_data, f'log({col})', axes[i, 1])\n",
            "\n",
            "plt.suptitle('Effect of Log Transform on Skewed Features',\n",
            "    fontsize=15, fontweight='bold', y=1.01)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "kde-plot-05",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Skewness & Kurtosis summary ---\n",
            "num_features = df.select_dtypes('number').columns\n",
            "skew_kurt = pd.DataFrame({\n",
            "    'Skewness': df[num_features].skew().round(3),\n",
            "    'Kurtosis': df[num_features].kurtosis().round(3)\n",
            "}).sort_values('Skewness', key=abs, ascending=False)\n",
            "\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 6))\n",
            "\n",
            "# Skewness bar chart\n",
            "colors_s = ['#e74c3c' if abs(v) > 1 else '#f39c12' if abs(v) > 0.5 else '#2ecc71' for v in skew_kurt['Skewness']]\n",
            "skew_kurt['Skewness'].plot(kind='barh', ax=axes[0], color=colors_s, edgecolor='white')\n",
            "axes[0].axvline(0, color='black', linewidth=0.8)\n",
            "axes[0].axvline(-1, color='gray', linestyle=':', alpha=0.5)\n",
            "axes[0].axvline(1, color='gray', linestyle=':', alpha=0.5)\n",
            "axes[0].set_title('Skewness by Feature\\n(|>1| Red, |>0.5| Yellow, |<0.5| Green)', fontweight='bold')\n",
            "axes[0].set_xlabel('Skewness')\n",
            "\n",
            "# Kurtosis bar chart\n",
            "colors_k = ['#e74c3c' if abs(v) > 3 else '#f39c12' if abs(v) > 1 else '#2ecc71' for v in skew_kurt['Kurtosis']]\n",
            "skew_kurt['Kurtosis'].plot(kind='barh', ax=axes[1], color=colors_k, edgecolor='white')\n",
            "axes[1].axvline(0, color='black', linewidth=0.8)\n",
            "axes[1].set_title('Kurtosis by Feature\\n(Normal = 0, Heavy tails > 0)', fontweight='bold')\n",
            "axes[1].set_xlabel('Excess Kurtosis')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "\n",
            "print('\\nFull Skewness & Kurtosis Table:')\n",
            "skew_kurt"
        ]
    }
]

# Insert before the last cell
last_idx = len(nb['cells']) - 1
for i, cell in enumerate(new_cells):
    nb['cells'].insert(last_idx + i, cell)

with open('Automobile.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Done - inserted {len(new_cells)} KDE cells at position {last_idx}")
