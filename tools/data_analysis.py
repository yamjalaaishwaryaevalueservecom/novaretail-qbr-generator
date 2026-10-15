import pandas as pd
from pathlib import Path


DATA_PATH = Path("input/novaretail_dataset.xlsx")


def load_data():
    """
    Load all sheets from the NovaRetail dataset.
    """

    performance = pd.read_excel(
        DATA_PATH,
        sheet_name="Regional_Performance"
    )

    customer = pd.read_excel(
        DATA_PATH,
        sheet_name="Customer_Experience"
    )

    risk = pd.read_excel(
        DATA_PATH,
        sheet_name="Operational_Risk"
    )

    return performance, customer, risk


def analyze_data():

    performance, customer, risk = load_data()

    # -----------------------------
    # Latest and Previous Quarter
    # -----------------------------

    quarters = performance["Quarter"].drop_duplicates()

    latest_quarter = quarters.iloc[-1]
    previous_quarter = quarters.iloc[-2]

    latest_perf = performance[
        performance["Quarter"] == latest_quarter
    ]

    previous_perf = performance[
        performance["Quarter"] == previous_quarter
    ]

    # -----------------------------
    # KPI 1 : Revenue
    # -----------------------------

    latest_revenue = latest_perf[
        "Revenue_USD_M"
    ].sum()

    previous_revenue = previous_perf[
        "Revenue_USD_M"
    ].sum()

    revenue_growth = (
        (latest_revenue - previous_revenue)
        / previous_revenue
    ) * 100

    # -----------------------------
    # KPI 2 : NPS
    # -----------------------------

    latest_customer = customer[
        customer["Quarter"] == latest_quarter
    ]

    avg_nps = latest_customer[
        "NPS"
    ].mean()

    # -----------------------------
    # Latest Risk Data
    # -----------------------------

    latest_risk = risk[
        risk["Quarter"] == latest_quarter
    ]

    # -----------------------------
    # Region-level growth
    # -----------------------------

    regional_growth = latest_perf.merge(
        previous_perf[
            [
                "Region",
                "Revenue_USD_M"
            ]
        ],
        on="Region",
        suffixes=(
            "_latest",
            "_previous"
        )
    )

    regional_growth[
        "Revenue_Growth_pct"
    ] = (
        (
            regional_growth["Revenue_USD_M_latest"]
            - regional_growth["Revenue_USD_M_previous"]
        )
        / regional_growth["Revenue_USD_M_previous"]
        * 100
    )

    # -----------------------------
    # Best and Worst Region
    # -----------------------------

    best_region = regional_growth.loc[
        regional_growth[
            "Revenue_Growth_pct"
        ].idxmax()
    ]

    worst_region = regional_growth.loc[
        regional_growth[
            "Revenue_Growth_pct"
        ].idxmin()
    ]

    # -----------------------------
    # High-Risk Region
    # -----------------------------

    high_risk_region = latest_risk.loc[
        latest_risk[
            "Stockout_Rate_pct"
        ].idxmax()
    ]

    # -----------------------------
    # Customer Satisfaction Leader
    # -----------------------------

    customer_leader = latest_customer.loc[
        latest_customer[
            "NPS"
        ].idxmax()
    ]

    # -----------------------------
    # Return final payload
    # -----------------------------

    results = {

        "latest_quarter": latest_quarter,

        "previous_quarter": previous_quarter,

        "kpis": {

            "total_revenue_usd_m":
                round(
                    float(latest_revenue),
                    0
                ),

            "revenue_growth_pct":
                round(
                    float(revenue_growth),
                    1
                ),

            "average_nps":
                round(
                    float(avg_nps),
                    1
                ),
        },

        "best_region": {

            "region":
                best_region["Region"],

            "growth_pct":
                round(
                    float(
                        best_region[
                            "Revenue_Growth_pct"
                        ]
                    ),
                    1
                )
        },

        "worst_region": {

            "region":
                worst_region["Region"],

            "growth_pct":
                round(
                    float(
                        worst_region[
                            "Revenue_Growth_pct"
                        ]
                    ),
                    1
                )
        },

        "customer_leader": {

            "region":
                customer_leader["Region"],

            "nps":
                int(
                    customer_leader["NPS"]
                )
        },

        "highest_risk_region": {

            "region":
                high_risk_region["Region"],

            "stockout_rate":
                float(
                    high_risk_region[
                        "Stockout_Rate_pct"
                    ]
                )
        },

        "regional_growth":
            regional_growth.to_dict(
                orient="records"
            ),

        "customer_data":
            latest_customer.to_dict(
                orient="records"
            ),

        "risk_data":
            latest_risk.to_dict(
                orient="records"
            )
    }

    return results


if __name__ == "__main__":

    results = analyze_data()

    print("\n===== ANALYSIS RESULTS =====\n")

    for key, value in results.items():
        print(f"{key}:")
        print(value)
        print()