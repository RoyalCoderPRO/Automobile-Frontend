import json

with open('Automobile.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
    {
        "cell_type": "markdown",
        "id": "ins-header-01",
        "metadata": {},
        "source": [
            "## 🛡️ Step 4: Insurance Risk Analysis"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "ins-plot-01",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Risk Rating distribution & Insurance Risk Score distribution ---\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "# Risk Rating (symboling): -2 (safest) to +3 (riskiest)\n",
            "risk_counts = df['Risk Rating'].value_counts().sort_index()\n",
            "colors = ['#2ecc71', '#27ae60', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b']\n",
            "risk_counts.plot(kind='bar', ax=axes[0], color=colors, edgecolor='white')\n",
            "axes[0].set_title('Risk Rating Distribution\\n(-2 = Safest, +3 = Riskiest)', fontweight='bold')\n",
            "axes[0].set_xlabel('Risk Rating')\n",
            "axes[0].set_ylabel('Number of Cars')\n",
            "axes[0].tick_params(axis='x', rotation=0)\n",
            "for i, v in enumerate(risk_counts):\n",
            "    axes[0].text(i, v + 1, str(v), ha='center', fontweight='bold')\n",
            "\n",
            "# Insurance Risk Score distribution\n",
            "axes[1].hist(df['Insurance Risk Score'].dropna(), bins=25, color='#3498db', edgecolor='white')\n",
            "axes[1].axvline(df['Insurance Risk Score'].median(), color='red', linestyle='--',\n",
            "    label=f\"Median: {df['Insurance Risk Score'].median():.0f}\")\n",
            "axes[1].set_title('Insurance Risk Score Distribution', fontweight='bold')\n",
            "axes[1].set_xlabel('Insurance Risk Score (Normalized Losses)')\n",
            "axes[1].set_ylabel('Frequency')\n",
            "axes[1].legend()\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "ins-plot-02",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Average Insurance Risk Score by Company ---\n",
            "fig, ax = plt.subplots(figsize=(12, 7))\n",
            "\n",
            "company_risk = df.groupby('Company')['Insurance Risk Score'].mean().sort_values()\n",
            "overall_avg = df['Insurance Risk Score'].mean()\n",
            "\n",
            "bar_colors = ['#e74c3c' if v > overall_avg else '#2ecc71' for v in company_risk]\n",
            "company_risk.plot(kind='barh', ax=ax, color=bar_colors, edgecolor='white')\n",
            "ax.axvline(overall_avg, color='#2c3e50', linestyle='--', linewidth=2,\n",
            "    label=f'Overall Avg: {overall_avg:.0f}')\n",
            "ax.set_title('Average Insurance Risk Score by Company\\n(Red = Above Average Risk)', fontsize=13, fontweight='bold')\n",
            "ax.set_xlabel('Avg Insurance Risk Score')\n",
            "ax.set_ylabel('')\n",
            "ax.legend(fontsize=11)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "ins-plot-03",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Risk Rating breakdown by Body Style and Drive Wheels ---\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "pd.crosstab(df['Body Style'], df['Risk Rating']).plot(\n",
            "    kind='bar', stacked=True, ax=axes[0],\n",
            "    color=['#2ecc71', '#27ae60', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b'])\n",
            "axes[0].set_title('Risk Rating by Body Style', fontweight='bold')\n",
            "axes[0].set_ylabel('Count')\n",
            "axes[0].tick_params(axis='x', rotation=30)\n",
            "axes[0].legend(title='Risk Rating', bbox_to_anchor=(1.0, 1), fontsize=8)\n",
            "\n",
            "pd.crosstab(df['Drive Wheels'], df['Risk Rating']).plot(\n",
            "    kind='bar', stacked=True, ax=axes[1],\n",
            "    color=['#2ecc71', '#27ae60', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b'])\n",
            "axes[1].set_title('Risk Rating by Drive Wheels', fontweight='bold')\n",
            "axes[1].set_ylabel('Count')\n",
            "axes[1].tick_params(axis='x', rotation=0)\n",
            "axes[1].legend(title='Risk Rating', bbox_to_anchor=(1.0, 1), fontsize=8)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "ins-plot-04",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Insurance Risk Score vs Price & Horsepower ---\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "axes[0].scatter(df['Price'], df['Insurance Risk Score'], alpha=0.6,\n",
            "    c=df['Risk Rating'], cmap='RdYlGn_r', edgecolors='white', s=60)\n",
            "axes[0].set_title('Insurance Risk Score vs Price', fontweight='bold')\n",
            "axes[0].set_xlabel('Price ($)')\n",
            "axes[0].set_ylabel('Insurance Risk Score')\n",
            "sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=plt.Normalize(-2, 3))\n",
            "plt.colorbar(sm, ax=axes[0], label='Risk Rating')\n",
            "\n",
            "axes[1].scatter(df['Horsepower'], df['Insurance Risk Score'], alpha=0.6,\n",
            "    c=df['Risk Rating'], cmap='RdYlGn_r', edgecolors='white', s=60)\n",
            "axes[1].set_title('Insurance Risk Score vs Horsepower', fontweight='bold')\n",
            "axes[1].set_xlabel('Horsepower')\n",
            "axes[1].set_ylabel('Insurance Risk Score')\n",
            "plt.colorbar(sm, ax=axes[1], label='Risk Rating')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "ins-plot-05",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Box plots: Insurance Risk Score by Risk Rating & Body Style ---\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "df.boxplot(column='Insurance Risk Score', by='Risk Rating', ax=axes[0],\n",
            "    patch_artist=True, boxprops=dict(facecolor='#3498db', alpha=0.7))\n",
            "axes[0].set_title('Insurance Risk Score by Risk Rating', fontweight='bold')\n",
            "axes[0].set_xlabel('Risk Rating')\n",
            "axes[0].set_ylabel('Insurance Risk Score')\n",
            "fig.suptitle('')  # Remove auto title\n",
            "\n",
            "df.boxplot(column='Insurance Risk Score', by='Body Style', ax=axes[1],\n",
            "    patch_artist=True, boxprops=dict(facecolor='#e74c3c', alpha=0.7))\n",
            "axes[1].set_title('Insurance Risk Score by Body Style', fontweight='bold')\n",
            "axes[1].set_xlabel('Body Style')\n",
            "axes[1].set_ylabel('Insurance Risk Score')\n",
            "axes[1].tick_params(axis='x', rotation=30)\n",
            "fig.suptitle('')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "ins-plot-06",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Correlation heatmap: Risk-related numeric features ---\n",
            "risk_cols = ['Risk Rating', 'Insurance Risk Score', 'Price', 'Horsepower',\n",
            "             'Engine Size', 'Curb Weight', 'City MPG', 'Highway MPG',\n",
            "             'Compression Ratio', 'Wheelbase']\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(10, 8))\n",
            "corr = df[risk_cols].corr()\n",
            "mask = np.triu(np.ones_like(corr, dtype=bool))\n",
            "sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn_r',\n",
            "    center=0, ax=ax, square=True, linewidths=0.5,\n",
            "    cbar_kws={'label': 'Correlation'})\n",
            "ax.set_title('Correlation Heatmap: Insurance Risk Factors', fontsize=13, fontweight='bold')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "ins-plot-07",
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- Average Risk Rating by Company (sorted) ---\n",
            "fig, ax = plt.subplots(figsize=(12, 7))\n",
            "\n",
            "company_rr = df.groupby('Company')['Risk Rating'].mean().sort_values()\n",
            "\n",
            "bar_colors = ['#e74c3c' if v > 0 else '#2ecc71' for v in company_rr]\n",
            "company_rr.plot(kind='barh', ax=ax, color=bar_colors, edgecolor='white')\n",
            "ax.axvline(0, color='#2c3e50', linestyle='-', linewidth=1.5)\n",
            "ax.set_title('Average Risk Rating by Company\\n(Negative = Safer, Positive = Riskier)', fontsize=13, fontweight='bold')\n",
            "ax.set_xlabel('Average Risk Rating')\n",
            "ax.set_ylabel('')\n",
            "\n",
            "for i, v in enumerate(company_rr):\n",
            "    ax.text(v + 0.05 if v >= 0 else v - 0.25, i, f'{v:.1f}', va='center', fontsize=9)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }
]

# Find the last empty cell and insert before it
last_idx = len(nb['cells']) - 1
for i, cell in enumerate(new_cells):
    nb['cells'].insert(last_idx + i, cell)

with open('Automobile.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Done - inserted {len(new_cells)} insurance risk cells")
