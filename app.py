import json
import subprocess
from pathlib import Path

import streamlit as st


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="NovaRetail QBR Generator",
    page_icon="📊",
    layout="wide"
)

OUTPUT_DIR = Path("output")

DRAFT_FILE = OUTPUT_DIR / "content_plan.json"

APPROVED_FILE = (
    OUTPUT_DIR
    / "approved_content_plan.json"
)

PPT_FILE = (
    OUTPUT_DIR
    / "NovaRetail_QBR_Final.pptx"
)


# =====================================================
# HELPERS
# =====================================================

def load_json(path):

    if not path.exists():
        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_json(data, path):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


# =====================================================
# HEADER
# =====================================================

st.title(
    "📊 NovaRetail Executive QBR Generator"
)

st.markdown(
    """
Generate, review, refine and approve
AI-created executive presentations.
"""
)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Generate Content",
        "Review & Refine",
        "Generate PPT"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.header(
        "Step 1 - Generate AI Content"
    )

    if st.button(
        "Generate Content Plan"
    ):

        with st.spinner(
            "Generating content..."
        ):

         result = subprocess.run(
            [
                "python",
                "generate_content_plan.py"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            st.error(
                "Content generation failed"
            )

            st.code(
                result.stderr
            )

        else:

            st.success(
                "Content generated successfully"
            )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.header(
        "Step 2 - Human Review & Refinement"
    )

    content = load_json(
        DRAFT_FILE
    )

    if not content:

        st.warning(
            "Generate content first."
        )

        st.stop()

    if "error" in content:

        st.error(
            f"ADK Error: {content['error']}"
        )

        st.stop()

    required_slides = [
        "slide1",
        "slide2",
        "slide3",
        "slide4",
        "slide5",
    ]

    missing = [
        slide
        for slide in required_slides
        if slide not in content
    ]

    if missing:

        st.error(
            f"Missing slides: {missing}"
        )

        st.json(content)

        st.stop()

    else:

        # ----------------------------
        # Slide 1
        # ----------------------------

        st.subheader(
            "Slide 1"
        )

        content["slide1"]["title"] = (
            st.text_input(
                "Title",
                content["slide1"]["title"]
            )
        )

        content["slide1"]["summary"] = (
            st.text_area(
                "Summary",
                content["slide1"]["summary"],
                height=120
            )
        )

        # ----------------------------
        # Slide 2
        # ----------------------------

        st.subheader(
            "Slide 2"
        )

        content["slide2"]["title"] = (
            st.text_input(
                "Slide 2 Title",
                content["slide2"]["title"]
            )
        )

        for i in range(4):

            content["slide2"][
                "insights"
            ][i] = st.text_input(
                f"Insight {i+1}",
                content["slide2"][
                    "insights"
                ][i],
                key=f"s2_{i}"
            )

        # ----------------------------
        # Slide 3
        # ----------------------------

        st.subheader(
            "Slide 3"
        )

        content["slide3"]["title"] = (
            st.text_input(
                "Slide 3 Title",
                content["slide3"]["title"]
            )
        )

        for i in range(4):

            content["slide3"][
                "insights"
            ][i] = st.text_input(
                f"Customer Insight {i+1}",
                content["slide3"][
                    "insights"
                ][i],
                key=f"s3_{i}"
            )

        # ----------------------------
        # Slide 4
        # ----------------------------

        st.subheader(
            "Slide 4"
        )

        content["slide4"]["title"] = (
            st.text_input(
                "Slide 4 Title",
                content["slide4"]["title"]
            )
        )

        for i in range(4):

            content["slide4"][
                "insights"
            ][i] = st.text_input(
                f"Risk Insight {i+1}",
                content["slide4"][
                    "insights"
                ][i],
                key=f"s4_{i}"
            )

        # ----------------------------
        # Slide 5
        # ----------------------------

        st.subheader(
            "Slide 5"
        )

        for i in range(4):

            content["slide5"][
                "recommendations"
            ][i] = st.text_input(
                f"Recommendation {i+1}",
                content["slide5"][
                    "recommendations"
                ][i],
                key=f"s5_{i}"
            )

        # ----------------------------
        # Human Feedback
        # ----------------------------

        st.divider()

        feedback = st.text_area(
            "Provide reviewer feedback",
            placeholder=
            "Example: Make Slide 2 headline more executive"
        )

        if st.button(
            "Approve Content"
        ):

            save_json(
                content,
                APPROVED_FILE
            )

            st.success(
                "Approved content saved"
            )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.header(
        "Step 3 - Generate Final Deck"
    )

    if st.button(
        "Generate PowerPoint"
    ):

        subprocess.run(
            [
                "python",
                "tools/chart_generator.py"
            ]
        )

        subprocess.run(
            [
                "python",
                "tools/ppt_generator.py"
            ]
        )

        st.success(
            "PowerPoint generated"
        )

    if PPT_FILE.exists():

        with open(
            PPT_FILE,
            "rb"
        ) as f:

            st.download_button(
                label="📥 Download PPT",
                data=f,
                file_name=
                "NovaRetail_QBR_Final.pptx",
                mime=
                "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )