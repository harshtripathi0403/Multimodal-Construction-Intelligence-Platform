from __future__ import annotations

import hashlib
import json
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageStat


st.set_page_config(page_title="BuildSight AI", page_icon="🏗️", layout="wide")

STATUS_COLORS = {"Safe": "#15803d", "Attention needed": "#d97706", "Critical": "#dc2626"}


def rupees(amount: float) -> str:
    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:.2f} Cr"
    if amount >= 100_000:
        return f"₹{amount / 100_000:.2f} L"
    return f"₹{amount:,.0f}"


def uploaded_image(uploaded_file) -> Image.Image | None:
    if uploaded_file is None:
        return None
    return Image.open(uploaded_file).convert("RGB")


def image_signals(image: Image.Image) -> dict:
    """Basic image statistics for transparent, local demonstration mode only."""
    thumbnail = image.copy()
    thumbnail.thumbnail((400, 400))
    stat = ImageStat.Stat(thumbnail)
    grayscale = np.asarray(thumbnail.convert("L"), dtype=np.float32)
    contrast = float(grayscale.std())
    darkness = float((grayscale < 55).mean() * 100)
    brightness = float(grayscale.mean())
    digest = hashlib.sha256(thumbnail.tobytes()).hexdigest()[:10]
    return {
        "image_id": f"IMG-{digest.upper()}",
        "brightness": round(brightness, 1),
        "contrast": round(contrast, 1),
        "dark_pixel_ratio": round(darkness, 1),
        "dimensions": f"{image.width} × {image.height}",
        "mean_rgb": [round(value, 1) for value in stat.mean],
    }


def safety_report(image: Image.Image | None, site_type: str, workers: int) -> dict:
    signals = image_signals(image) if image else {"image_id": "DEMO-SAFETY-001", "dimensions": "No image"}
    # Deliberately conservative: local heuristics are not treated as computer vision detection.
    base_score = 72 if image else 65
    if image:
        base_score -= 7 if signals["dark_pixel_ratio"] > 24 else 0
        base_score -= 5 if signals["contrast"] < 30 else 0
    findings = [
        {"item": "Safety helmet", "status": "Manual review required", "note": "Confirm every worker wears a correctly fitted helmet."},
        {"item": "High-visibility vest", "status": "Manual review required", "note": "Check visibility around plant, vehicles, and low-light areas."},
        {"item": "Safety footwear", "status": "Manual review required", "note": "Confirm steel-toe footwear and clear walking paths."},
        {"item": "Fall protection", "status": "Review if working at height", "note": "Inspect harness anchor points and guardrails before work begins."},
    ]
    hazards = [
        {
            "hazard": "Pre-start PPE verification",
            "severity": "Medium",
            "remedy": "Conduct a supervisor-led PPE toolbox check before the shift.",
        },
        {
            "hazard": "Mobile plant interaction",
            "severity": "High" if site_type in ["Roadwork", "Commercial high-rise"] else "Medium",
            "remedy": "Use segregated walkways, a banksman, and marked exclusion zones.",
        },
    ]
    if workers > 25:
        hazards.append(
            {
                "hazard": "Large crew coordination",
                "severity": "Medium",
                "remedy": "Issue a recorded daily induction and appoint zone supervisors.",
            }
        )
    return {
        "report_type": "site_safety_ppe_audit",
        "mode": "local demonstration - manual verification required",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "site_type": site_type,
        "declared_workers": workers,
        "image_metadata": signals,
        "safety_score": max(0, base_score),
        "overall_status": "Attention needed",
        "ppe_checklist": findings,
        "hazards": hazards,
        "disclaimer": "This demonstration does not detect PPE or certify site safety. A competent safety professional must inspect the site.",
    }


def crack_report(image: Image.Image | None, material: str, observed_width: float) -> dict:
    signals = image_signals(image) if image else {"image_id": "DEMO-CRACK-001", "dimensions": "No image"}
    if observed_width < 0.3:
        defect, urgency = "Hairline / surface crack", "Monitor"
    elif observed_width < 1.0:
        defect, urgency = "Potential settlement or shrinkage crack", "Engineer review recommended"
    else:
        defect, urgency = "Potential structural crack", "Urgent qualified engineer assessment"
    repairs = {
        "Hairline / surface crack": ["Photograph and date-mark the crack", "Monitor width and length", "Use a suitable surface repair only after professional confirmation"],
        "Potential settlement or shrinkage crack": ["Measure and log progression", "Investigate moisture, settlement, and loading", "Seek an engineer's repair specification before sealing"],
        "Potential structural crack": ["Restrict access if there is immediate risk", "Do not rely on this app for diagnosis", "Arrange urgent inspection by a licensed structural engineer"],
    }[defect]
    return {
        "report_type": "crack_diagnostics",
        "mode": "local demonstration - not a structural diagnosis",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "material": material,
        "image_metadata": signals,
        "classification": defect,
        "reported_crack_width_mm": observed_width,
        "possible_contributors": ["thermal movement", "shrinkage", "settlement", "overloading", "water ingress"],
        "recommended_next_steps": repairs,
        "urgency": urgency,
        "disclaimer": "Do not make structural or occupancy decisions from this demonstration. Get an on-site assessment from a qualified engineer.",
    }


def valuation_plan(structure: str, area: int, city_tier: str, completion: int, quality: str) -> dict:
    construction_rates = {"Residential": 2200, "Commercial": 2900, "Warehouse / Industrial": 1900, "Villa / Premium residential": 3400}
    tier_multiplier = {"Tier 1": 1.25, "Tier 2": 1.0, "Tier 3": 0.82}
    quality_multiplier = {"Economy": 0.86, "Standard": 1.0, "Premium": 1.28}
    base_cost = area * construction_rates[structure] * tier_multiplier[city_tier] * quality_multiplier[quality]
    incurred = base_cost * completion / 100
    land_and_market = {"Tier 1": 1.52, "Tier 2": 1.30, "Tier 3": 1.16}[city_tier]
    estimated_value = base_cost * land_and_market * (0.55 + completion / 200)
    return {
        "structure": structure,
        "built_up_area_sqft": area,
        "location_tier": city_tier,
        "quality_level": quality,
        "completion_percentage": completion,
        "estimated_construction_budget": round(base_cost),
        "estimated_capex_incurred": round(incurred),
        "illustrative_market_value": round(estimated_value),
        "cement_bags_estimate": round(area * 0.42 * quality_multiplier[quality]),
        "steel_tonnes_estimate": round(area * 0.0042 * quality_multiplier[quality], 2),
        "disclaimer": "Illustrative planning estimate only. Verify quantities, rates, approvals, land value, and taxes with qualified local professionals.",
    }


def advisory(weather: str) -> tuple[str, list[str]]:
    guidance = {
        "Normal": ("Safe to proceed with normal controls", ["Hold the daily toolbox talk.", "Inspect access routes and PPE.", "Record permits and equipment checks."]),
        "High wind": ("Elevated wind risk", ["Pause lifting operations when manufacturer or site limits are exceeded.", "Secure loose materials and temporary works.", "Review scaffolding and elevated-work permits."]),
        "Heavy rain": ("Rain and electrical risk", ["Inspect excavations for water ingress and slope instability.", "Protect temporary electrical systems and stop unsafe work.", "Check slips, access routes, and concrete curing plan."]),
        "Extreme heat": ("Heat-stress risk", ["Schedule hydration and shaded rest breaks.", "Move intensive work to cooler hours where feasible.", "Train supervisors to recognize heat illness signs."]),
    }
    return guidance[weather]


def assistant_reply(question: str, weather: str) -> str:
    lowered = question.lower()
    if any(word in lowered for word in ["rain", "weather", "wind", "heat"]):
        status, actions = advisory(weather)
        return f"For **{weather.lower()}** conditions, the current advisory is **{status}**. Start with: {actions[0]} {actions[1]}"
    if any(word in lowered for word in ["crack", "structural", "wall"]):
        return "Log the crack's location, width, direction, and date; compare it over time. If it is widening, displaced, near a beam/column, or accompanied by distress, restrict risk exposure and contact a qualified structural engineer."
    if any(word in lowered for word in ["ppe", "safety", "helmet"]):
        return "Run a documented pre-start PPE check: helmet, high-visibility clothing, appropriate footwear, task-specific eye/hand protection, and fall protection where needed. A competent supervisor should verify these on site."
    if any(word in lowered for word in ["cost", "budget", "valuation"]):
        return "Use the Planning & Valuation tab for an illustrative estimate, then validate it with current local quotations, drawings, site conditions, taxes, and a quantity surveyor or engineer."
    return "I can help with a daily safety checklist, weather controls, planning estimates, or what to document for a crack observation. This is educational guidance, not professional engineering or safety certification."


st.markdown(
    """
    <style>
      .stApp { background: #f7fafc; }
      .hero { background: linear-gradient(115deg, #102a43, #0f766e); padding: 1.5rem 1.8rem;
        border-radius: 18px; color: white; margin-bottom: 1.2rem; }
      .hero h1 { margin: 0; font-size: 2.15rem; }
      .hero p { margin: .35rem 0 0; opacity: .92; }
      .warning-box { border-left: 5px solid #d97706; background: #fffbeb; padding: .75rem 1rem; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='hero'><h1>🏗️ BuildSight AI</h1><p>Multimodal Construction Intelligence Platform · planning, observation, and daily site advisory.</p></div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Project controls")
    demo_mode = st.toggle("Demonstration mode", value=True, help="Local, transparent rule-based reports. No image is sent to a cloud service.")
    site_name = st.text_input("Project / site name", "Demo Construction Site")
    weather_condition = st.selectbox("Today's weather", ["Normal", "High wind", "Heavy rain", "Extreme heat"])
    st.divider()
    st.caption("Privacy-first demo: uploaded images are processed only in the active browser/app session and are not saved by this app.")

st.warning("Important: This app is an educational capstone demo. It does not certify PPE compliance, diagnose structural defects, or replace a qualified safety officer, engineer, surveyor, or local authority.")

tab_safety, tab_crack, tab_plan, tab_assistant = st.tabs(
    ["🦺 Safety & PPE Audit", "🧱 Crack Diagnostics", "📐 Planning & Valuation", "🌦️ Daily Site Assistant"]
)

with tab_safety:
    st.subheader("Site Safety & PPE Audit")
    st.caption("Upload a site image to attach image metadata to a transparent, manually verifiable audit report.")
    col_upload, col_controls = st.columns([1.4, 1])
    with col_upload:
        safety_file = st.file_uploader("Construction site image (JPG / PNG)", type=["jpg", "jpeg", "png"], key="safety")
        safety_image = uploaded_image(safety_file)
        if safety_image:
            st.image(safety_image, caption="Uploaded site image", use_container_width=True)
    with col_controls:
        site_type = st.selectbox("Site type", ["Residential", "Commercial high-rise", "Roadwork", "Industrial"], key="site_type")
        workers = st.number_input("Workers on this shift", min_value=1, max_value=500, value=12, key="workers")
        run_safety = st.button("Generate safety audit", type="primary", use_container_width=True)
    if run_safety:
        st.session_state["safety_report"] = safety_report(safety_image, site_type, int(workers))
    report = st.session_state.get("safety_report")
    if report:
        c1, c2, c3 = st.columns(3)
        c1.metric("Safety readiness score", f"{report['safety_score']} / 100")
        c2.metric("Overall status", report["overall_status"])
        c3.metric("Declared workers", report["declared_workers"])
        st.subheader("Manual PPE verification checklist")
        st.dataframe(pd.DataFrame(report["ppe_checklist"]), use_container_width=True, hide_index=True)
        st.subheader("Priority controls")
        st.dataframe(pd.DataFrame(report["hazards"]), use_container_width=True, hide_index=True)
        st.download_button("Download safety JSON report", json.dumps(report, indent=2), "safety-audit-report.json", "application/json")

with tab_crack:
    st.subheader("Crack Diagnostics & Structural Integrity")
    st.caption("Record an observation for professional review. Image statistics are shown only as metadata; the app does not infer a structural condition from an image.")
    col_upload, col_controls = st.columns([1.4, 1])
    with col_upload:
        crack_file = st.file_uploader("Wall / concrete image (JPG / PNG)", type=["jpg", "jpeg", "png"], key="crack")
        crack_image = uploaded_image(crack_file)
        if crack_image:
            st.image(crack_image, caption="Uploaded surface image", use_container_width=True)
    with col_controls:
        material = st.selectbox("Surface material", ["Reinforced concrete", "Brick masonry", "Plaster / render", "Blockwork"])
        crack_width = st.number_input("Observed crack width (mm)", min_value=0.0, max_value=25.0, value=0.4, step=0.1)
        run_crack = st.button("Create observation report", type="primary", use_container_width=True)
    if run_crack:
        st.session_state["crack_report"] = crack_report(crack_image, material, float(crack_width))
    crack = st.session_state.get("crack_report")
    if crack:
        m1, m2, m3 = st.columns(3)
        m1.metric("Observed width", f"{crack['reported_crack_width_mm']} mm")
        m2.metric("Classification", crack["classification"])
        m3.metric("Action", crack["urgency"])
        st.write("**Possible contributors:** " + ", ".join(crack["possible_contributors"]))
        st.write("**Recommended next steps:**")
        for step in crack["recommended_next_steps"]:
            st.write(f"- {step}")
        st.download_button("Download crack JSON report", json.dumps(crack, indent=2), "crack-observation-report.json", "application/json")

with tab_plan:
    st.subheader("Construction Planning & Real Estate Valuation")
    st.caption("Illustrative costs in INR. These figures are not a bill of quantities, valuation, or quotation.")
    c1, c2, c3 = st.columns(3)
    with c1:
        structure = st.selectbox("Structure type", ["Residential", "Commercial", "Warehouse / Industrial", "Villa / Premium residential"])
        built_up_area = st.number_input("Built-up area (sq ft)", min_value=300, max_value=2_000_000, value=1800, step=100)
    with c2:
        city_tier = st.selectbox("City tier", ["Tier 1", "Tier 2", "Tier 3"])
        quality = st.selectbox("Finish quality", ["Economy", "Standard", "Premium"], index=1)
    with c3:
        completion = st.slider("Construction completion", min_value=0, max_value=100, value=35)
        run_plan = st.button("Calculate project estimate", type="primary", use_container_width=True)
    if run_plan:
        st.session_state["plan_report"] = valuation_plan(structure, int(built_up_area), city_tier, completion, quality)
    plan = st.session_state.get("plan_report")
    if plan:
        a, b, c = st.columns(3)
        a.metric("Estimated construction budget", rupees(plan["estimated_construction_budget"]))
        b.metric("Estimated capex incurred", rupees(plan["estimated_capex_incurred"]))
        c.metric("Illustrative market value", rupees(plan["illustrative_market_value"]))
        st.progress(plan["completion_percentage"] / 100, text=f"Milestone progress: {plan['completion_percentage']}%")
        st.subheader("Illustrative material indicators")
        mat_a, mat_b = st.columns(2)
        mat_a.metric("Cement", f"{plan['cement_bags_estimate']:,} bags")
        mat_b.metric("Steel", f"{plan['steel_tonnes_estimate']:,} tonnes")
        table = pd.DataFrame(
            [{"Estimate": "Total construction budget", "Amount": plan["estimated_construction_budget"]}, {"Estimate": "Capex incurred", "Amount": plan["estimated_capex_incurred"]}, {"Estimate": "Illustrative market value", "Amount": plan["illustrative_market_value"]}]
        )
        st.bar_chart(table.set_index("Estimate"))
        st.download_button("Download planning JSON report", json.dumps(plan, indent=2), "planning-estimate.json", "application/json")

with tab_assistant:
    st.subheader("Daily Site Assistant & Weather-Aware Advisory")
    status, actions = advisory(weather_condition)
    st.markdown(f"### Current condition: {weather_condition}")
    st.info(status)
    for action in actions:
        st.write(f"- {action}")
    st.divider()
    st.markdown("#### Construction guidance assistant")
    prompt = st.text_input("Ask about site safety, crack documentation, weather controls, or budget planning", placeholder="What should I do before heavy rain?")
    if st.button("Ask assistant"):
        if prompt.strip():
            st.session_state["assistant_answer"] = assistant_reply(prompt, weather_condition)
        else:
            st.warning("Enter a question first.")
    if answer := st.session_state.get("assistant_answer"):
        st.markdown(answer)

st.caption(f"BuildSight AI · {site_name} · Mode: {'Local demonstration' if demo_mode else 'Demonstration controls enabled'} · {datetime.now().strftime('%d %b %Y')}")
