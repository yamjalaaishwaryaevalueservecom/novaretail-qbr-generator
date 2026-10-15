import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("input/novaretail_dataset.xlsx")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

# Executive deck palette
COLORS = {
    "North America": "#A8B5C5",   # muted blue-gray
    "Europe": "#D3DAE3",          # light blue-gray
    "APAC": "#00A99D",            # teal (positive/growth)
    "Latin America": "#D9534F"    # red (risk)
}

plt.style.use("default")

def generate_performance_chart():

    performance = pd.read_excel(
        DATA_PATH,
        sheet_name="Regional_Performance"
    )

    pivot = performance.pivot(
        index="Quarter",
        columns="Region",
        values="Revenue_USD_M"
    )

    ax = pivot.plot(
        kind="bar",
        figsize=(10, 5),
        color=[
            COLORS[col]
            for col in pivot.columns
        ],
        edgecolor="none"
    )

    ax.set_title(
        "Revenue by Region",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_ylabel(
        "Revenue (USD M)",
        fontsize=11
    )

    ax.set_xlabel("")

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    plt.xticks(rotation=0)

    plt.legend(
        frameon=False,
        ncol=2
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "performance_chart.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()


def generate_customer_chart():

    customer = pd.read_excel(
        DATA_PATH,
        sheet_name="Customer_Experience"
    )

    pivot = customer.pivot(
        index="Quarter",
        columns="Region",
        values="NPS"
    )

    plt.figure(figsize=(10, 5))

    for region in pivot.columns:

        linewidth = 3

        if region == "APAC":
            linewidth = 4

        plt.plot(
            pivot.index,
            pivot[region],
            marker="o",
            linewidth=linewidth,
            color=COLORS[region],
            label=region
        )

    plt.title(
        "NPS Trend by Region",
        fontsize=16,
        fontweight="bold"
    )

    plt.ylabel("Net Promoter Score")

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    plt.legend(frameon=False)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "customer_chart.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()


def generate_risk_chart():

    risk = pd.read_excel(
        DATA_PATH,
        sheet_name="Operational_Risk"
    )

    latest_qtr = risk[
        "Quarter"
    ].drop_duplicates().iloc[-1]

    latest = risk[
        risk["Quarter"] == latest_qtr
    ]

    plt.figure(figsize=(10, 5))

    bars = plt.bar(
        latest["Region"],
        latest["Stockout_Rate_pct"],
        color=[
            COLORS[region]
            for region in latest["Region"]
        ],
        edgecolor="none"
    )

    plt.title(
        f"Stockout Rate ({latest_qtr})",
        fontsize=16,
        fontweight="bold"
    )

    plt.ylabel("%")

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.3,
            f"{height:.1f}%",
            ha="center",
            fontsize=10
        )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "risk_chart.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()


if __name__ == "__main__":

    generate_performance_chart()
    generate_customer_chart()
    generate_risk_chart()

    print("✅ Charts generated successfully")