import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

st.set_page_config(page_title="StudyLab — Math", page_icon="📐", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0.3rem; }
    .sub-title { text-align: center; color: #888; margin-bottom: 2rem; }
    .result-box { background: #1a1a2e; border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0; border-left: 4px solid #10b981; }
    h2 { border-bottom: 1px solid #333; padding-bottom: 0.3rem; }
    .stApp { background: #0f0f1a; }
    .block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📐 StudyLab — Math</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive mathematics tools</div>', unsafe_allow_html=True)

# ── SIDEBAR: Category → Topic ─────────────────────────────
category = st.sidebar.selectbox("Category", [
    "🔢 Algebra",
    "📐 Trigonometry",
    "📈 Calculus",
    "🧭 Vectors",
    "🧊 Geometry",
])

topic_map = {
    "🔢 Algebra": ["Quadratic Equation"],
    "📐 Trigonometry": ["Trigonometry Explorer", "Unit Circle"],
    "📈 Calculus": ["Derivative Visualizer", "Integral Area"],
    "🧭 Vectors": ["2D Vector Explorer", "Vector Addition", "Dot Product",
                    "3D Vector Explorer", "Cross Product (3D)",
                    "Shortest Distance", "Plane Vectors"],
    "🧊 Geometry": ["3D Geometry"],
}

topic = st.sidebar.radio("Topic", topic_map[category])

# ── Quadratic ─────────────────────────────────────────────
if topic == "Quadratic Equation":
    st.markdown("## ax² + bx + c = 0")
    st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")

    col1, col2, col3 = st.columns(3)
    with col1: a = st.slider("a", -10.0, 10.0, 1.0, 0.1)
    with col2: b = st.slider("b", -10.0, 10.0, 0.0, 0.1)
    with col3: c = st.slider("c", -10.0, 10.0, -4.0, 0.1)

    D = b**2 - 4*a*c
    st.markdown(f'<div class="result-box">Δ = {D:.2f}</div>', unsafe_allow_html=True)

    if D >= 0:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        st.success(f"**Roots:** x₁ = {x1:.4f},   x₂ = {x2:.4f}")
    else:
        real = -b / (2*a)
        imag = math.sqrt(-D) / (2*a)
        st.warning(f"**Complex roots:** {real:.4f} ± {imag:.4f}i")
        x1 = x2 = None

    x_vals = np.linspace(-10, 10, 500)
    y_vals = a*x_vals**2 + b*x_vals + c
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Parabola",
                              line=dict(color="#6366f1", width=2)))
    if D >= 0 and x1 is not None:
        fig.add_trace(go.Scatter(x=[x1, x2], y=[0, 0], mode="markers",
                                  marker=dict(size=10, color="#ef4444", symbol="x"),
                                  name="Roots"))
    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dash"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis_title="x", yaxis_title="y", hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Trigonometry ──────────────────────────────────────────
elif topic == "Trigonometry Explorer":
    st.markdown("## Interactive Trig Functions")
    func = st.selectbox("Function", ["sin(x)", "cos(x)", "tan(x)", "sin(x) & cos(x)"])
    amp = st.slider("Amplitude", 0.1, 5.0, 1.0, 0.1)
    freq = st.slider("Frequency", 0.1, 5.0, 1.0, 0.1)
    phase = st.slider("Phase shift", 0.0, 6.28, 0.0, 0.01)

    x = np.linspace(-2*np.pi, 2*np.pi, 600)
    fig = go.Figure()

    def add_fn(fn_name, y_fn, color, dash="solid"):
        y = amp * y_fn(freq * x + phase)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"{amp}{fn_name}({freq}x+{phase:.2f})",
                                  line=dict(color=color, width=2, dash=dash)))

    if func == "sin(x)":
        add_fn("sin", np.sin, "#6366f1")
    elif func == "cos(x)":
        add_fn("cos", np.cos, "#10b981")
    elif func == "tan(x)":
        y = amp * np.tan(freq * x + phase)
        y = np.where(np.abs(y) > 10, np.nan, y)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="tan(x)",
                                  line=dict(color="#f59e0b", width=2)))
    else:
        add_fn("sin", np.sin, "#6366f1")
        add_fn("cos", np.cos, "#10b981")

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                      yaxis_range=[-5, 5], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Derivative ────────────────────────────────────────────
elif topic == "Derivative Visualizer":
    st.markdown("## Function & Its Derivative")
    fn_choice = st.selectbox("Function", ["x²", "x³", "sin(x)", "cos(x)", "e^x", "ln(x)"])
    x = np.linspace(-5, 5, 500)

    if fn_choice == "x²":
        f = x**2; df = 2*x; label = "x²"; dlabel = "2x"
    elif fn_choice == "x³":
        f = x**3; df = 3*x**2; label = "x³"; dlabel = "3x²"
    elif fn_choice == "sin(x)":
        f = np.sin(x); df = np.cos(x); label = "sin(x)"; dlabel = "cos(x)"
    elif fn_choice == "cos(x)":
        f = np.cos(x); df = -np.sin(x); label = "cos(x)"; dlabel = "-sin(x)"
    elif fn_choice == "e^x":
        f = np.exp(x); df = np.exp(x); label = "eˣ"; dlabel = "eˣ"
    elif fn_choice == "ln(x)":
        mask = x > 0
        x = x[mask]; f = np.log(x[mask]); df = 1/x[mask]; label = "ln(x)"; dlabel = "1/x"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name=label, line=dict(color="#6366f1", width=2)))
    fig.add_trace(go.Scatter(x=x, y=df, mode="lines", name=f"d/dx {dlabel}",
                              line=dict(color="#ef4444", width=2, dash="dash")))
    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

    st.latex(r"\frac{d}{dx}f(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}")

# ── Integral ─────────────────────────────────────────────
elif topic == "Integral Area":
    st.markdown("## Definite Integral — Area Under Curve")
    fn_choice = st.selectbox("Function", ["x²", "x³", "sin(x)", "cos(x)"], key="int_fn")
    a_i, b_i = st.slider("Integration range [a, b]", -5.0, 5.0, (0.0, 2.0), 0.1)

    x = np.linspace(-5, 5, 600)
    if fn_choice == "x²": f = x**2; label = "x²"
    elif fn_choice == "x³": f = x**3; label = "x³"
    elif fn_choice == "sin(x)": f = np.sin(x); label = "sin(x)"
    elif fn_choice == "cos(x)": f = np.cos(x); label = "cos(x)"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name=label, line=dict(color="#6366f1", width=2)))
    mask = (x >= a_i) & (x <= b_i)
    fig.add_trace(go.Scatter(x=x[mask], y=f[mask], mode="lines", fill="tozeroy",
                              name=f"Area [{a_i}, {b_i}]",
                              line=dict(color="rgba(99,102,241,0.3)", width=0),
                              fillcolor="rgba(99,102,241,0.2)"))
    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

    dx = 0.001
    xs = np.arange(a_i, b_i, dx)
    if fn_choice == "x²": approx = np.sum(xs**2) * dx
    elif fn_choice == "x³": approx = np.sum(xs**3) * dx
    elif fn_choice == "sin(x)": approx = np.sum(np.sin(xs)) * dx
    elif fn_choice == "cos(x)": approx = np.sum(np.cos(xs)) * dx

    st.info(f"∫_{a_i}^{b_i} {label} dx ≈ {approx:.6f}")

# ── 2D Vector Explorer ──────────────────────────────────
if topic == "2D Vector Explorer":
    st.markdown("## 2D Vector Explorer")
    col1, col2 = st.columns(2)
    with col1:
        vx = st.slider("x-component", -10.0, 10.0, 3.0, 0.1, key="vec_vx")
    with col2:
        vy = st.slider("y-component", -10.0, 10.0, 4.0, 0.1, key="vec_vy")

    magnitude = math.sqrt(vx**2 + vy**2)
    angle = math.degrees(math.atan2(vy, vx))

    fig = go.Figure()
    # Vector arrow
    fig.add_trace(go.Scatter(
        x=[0, vx], y=[0, vy], mode="lines+markers",
        line=dict(color="#6366f1", width=3),
        marker=dict(size=[0, 10], color=["#6366f1", "#ef4444"]),
        name=f"v = ({vx:.1f}, {vy:.1f})",
    ))
    # Component dashed lines
    fig.add_trace(go.Scatter(
        x=[0, vx], y=[vy, vy], mode="lines",
        line=dict(color="#f59e0b", width=1, dash="dot"),
        name=f"x = {vx:.1f}", showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=[vx, vx], y=[0, vy], mode="lines",
        line=dict(color="#10b981", width=1, dash="dot"),
        name=f"y = {vy:.1f}", showlegend=False,
    ))
    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dash"))

    max_r = max(abs(vx), abs(vy), 5) + 1
    fig.update_layout(
        height=450,
        xaxis=dict(range=[-max_r, max_r], scaleanchor="y", title="x"),
        yaxis=dict(range=[-max_r, max_r], title="y"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Magnitude |v|", f"{magnitude:.4f}")
    with c2: st.metric("Direction θ", f"{angle:.2f}°")
    with c3: st.metric("Unit vector", f"({vx/magnitude:.4f}, {vy/magnitude:.4f})" if magnitude > 0 else "(0, 0)")

    st.latex(r"\vec{v} = " + f"{vx:.1f}" + r"\hat{i} + " + f"{vy:.1f}" + r"\hat{j}")
    st.latex(r"|\vec{v}| = \sqrt{" + f"{vx:.1f}" + r"^2 + " + f"{vy:.1f}" + r"^2} = " + f"{magnitude:.4f}")

# ── Vector Addition ──────────────────────────────────────
elif topic == "Vector Addition":
    st.markdown("## Vector Addition")
    st.markdown("Adjust two vectors to see their sum.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Vector a**")
        ax = st.slider("aₓ", -10.0, 10.0, 3.0, 0.1)
        ay = st.slider("aᵧ", -10.0, 10.0, 1.0, 0.1)
    with col2:
        st.markdown("**Vector b**")
        bx = st.slider("bₓ", -10.0, 10.0, 1.0, 0.1)
        by = st.slider("bᵧ", -10.0, 10.0, 3.0, 0.1)

    rx, ry = ax + bx, ay + by

    fig = go.Figure()
    # Vector a
    fig.add_trace(go.Scatter(
        x=[0, ax], y=[0, ay], mode="lines+markers",
        line=dict(color="#6366f1", width=3),
        marker=dict(size=[0, 8], color="#6366f1"),
        name=f"a = ({ax:.1f}, {ay:.1f})",
    ))
    # Vector b (from tip of a)
    fig.add_trace(go.Scatter(
        x=[ax, ax+bx], y=[ay, ay+by], mode="lines+markers",
        line=dict(color="#10b981", width=3),
        marker=dict(size=[0, 8], color="#10b981"),
        name=f"b = ({bx:.1f}, {by:.1f})",
    ))
    # Resultant r
    fig.add_trace(go.Scatter(
        x=[0, rx], y=[0, ry], mode="lines+markers",
        line=dict(color="#ef4444", width=3, dash="dash"),
        marker=dict(size=[0, 10], color="#ef4444"),
        name=f"a+b = ({rx:.1f}, {ry:.1f})",
    ))
    # Parallelogram: vector b from origin
    fig.add_trace(go.Scatter(
        x=[0, bx], y=[0, by], mode="lines",
        line=dict(color="#10b981", width=1, dash="dot"),
        showlegend=False,
    ))
    # Parallelogram: a from tip of b
    fig.add_trace(go.Scatter(
        x=[bx, bx+ax], y=[by, by+ay], mode="lines",
        line=dict(color="#6366f1", width=1, dash="dot"),
        showlegend=False,
    ))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dash"))
    lim = max(abs(ax), abs(ay), abs(bx), abs(by), abs(rx), abs(ry), 5) + 1
    fig.update_layout(
        height=450,
        xaxis=dict(range=[-lim, lim], scaleanchor="y", title="x"),
        yaxis=dict(range=[-lim, lim], title="y"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("a + b", f"({rx:.1f}, {ry:.1f})")
    with c2: st.metric("Magnitude", f"{math.sqrt(rx**2+ry**2):.4f}")
    with c3: st.metric("Angle", f"{math.degrees(math.atan2(ry, rx)):.2f}°")

    st.latex(r"\vec{a} + \vec{b} = (" + f"{ax:.1f}" + r", " + f"{ay:.1f}" + r") + (" + f"{bx:.1f}" + r", " + f"{by:.1f}" + r") = (" + f"{rx:.1f}" + r", " + f"{ry:.1f}" + r")")

# ── Dot Product ──────────────────────────────────────────
elif topic == "Dot Product":
    st.markdown("## Dot Product (Scalar Product)")
    st.latex(r"\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta = a_xb_x + a_yb_y")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Vector a**")
        ax = st.slider("aₓ", -10.0, 10.0, 4.0, 0.1, key="dp_ax")
        ay = st.slider("aᵧ", -10.0, 10.0, 1.0, 0.1, key="dp_ay")
    with col2:
        st.markdown("**Vector b**")
        bx = st.slider("bₓ", -10.0, 10.0, 1.0, 0.1, key="dp_bx")
        by = st.slider("bᵧ", -10.0, 10.0, 3.0, 0.1, key="dp_by")

    dot = ax*bx + ay*by
    mag_a = math.sqrt(ax**2 + ay**2)
    mag_b = math.sqrt(bx**2 + by**2)
    cos_theta = dot / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0
    theta = math.degrees(math.acos(max(-1, min(1, cos_theta))))

    fig = go.Figure()
    # Vector a
    fig.add_trace(go.Scatter(
        x=[0, ax], y=[0, ay], mode="lines+markers",
        line=dict(color="#6366f1", width=3),
        marker=dict(size=[0, 8], color="#6366f1"),
        name=f"a = ({ax:.1f}, {ay:.1f})",
    ))
    # Vector b
    fig.add_trace(go.Scatter(
        x=[0, bx], y=[0, by], mode="lines+markers",
        line=dict(color="#10b981", width=3),
        marker=dict(size=[0, 8], color="#10b981"),
        name=f"b = ({bx:.1f}, {by:.1f})",
    ))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dash"))
    lim = max(abs(ax), abs(ay), abs(bx), abs(by), 5) + 1
    fig.update_layout(
        height=450,
        xaxis=dict(range=[-lim, lim], scaleanchor="y", title="x"),
        yaxis=dict(range=[-lim, lim], title="y"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("a · b", f"{dot:.3f}")
    with c2: st.metric("|a|", f"{mag_a:.3f}")
    with c3: st.metric("|b|", f"{mag_b:.3f}")
    with c4: st.metric("θ (angle)", f"{theta:.2f}°")

    st.markdown(
        f'<div class="result-box">'
        f'a · b = {ax:.1f}×{bx:.1f} + {ay:.1f}×{by:.1f} = <strong>{dot:.3f}</strong><br>'
        f'cos θ = {dot:.3f} / ({mag_a:.3f}×{mag_b:.3f}) = {cos_theta:.4f} → θ = {theta:.2f}°'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── 3D Vector Explorer ─────────────────────────────────
if topic == "3D Vector Explorer":
    st.markdown("## 3D Vector Explorer")
    col1, col2, col3 = st.columns(3)
    with col1: vx = st.slider("vₓ", -5.0, 5.0, 3.0, 0.1, key="3dv_vx")
    with col2: vy = st.slider("vᵧ", -5.0, 5.0, 2.0, 0.1, key="3dv_vy")
    with col3: vz = st.slider("v_z", -5.0, 5.0, 4.0, 0.1, key="3dv_vz")

    mag = math.sqrt(vx**2 + vy**2 + vz**2)
    alpha = math.degrees(math.acos(vx / mag)) if mag > 0 else 0
    beta = math.degrees(math.acos(vy / mag)) if mag > 0 else 90
    gamma = math.degrees(math.acos(vz / mag)) if mag > 0 else 90

    fig = go.Figure()
    # Vector arrow
    fig.add_trace(go.Scatter3d(
        x=[0, vx], y=[0, vy], z=[0, vz],
        mode="lines+markers",
        line=dict(color="#6366f1", width=6),
        marker=dict(size=[0, 8], color=["#6366f1", "#ef4444"]),
        name=f"v = ({vx:.1f}, {vy:.1f}, {vz:.1f})",
    ))
    # Component lines to each axis
    fig.add_trace(go.Scatter3d(
        x=[0, vx], y=[0, 0], z=[0, 0],
        mode="lines", line=dict(color="#f59e0b", width=2, dash="dash"),
        showlegend=False,
    ))
    fig.add_trace(go.Scatter3d(
        x=[vx, vx], y=[0, vy], z=[0, 0],
        mode="lines", line=dict(color="#10b981", width=2, dash="dash"),
        showlegend=False,
    ))
    fig.add_trace(go.Scatter3d(
        x=[vx, vx], y=[vy, vy], z=[0, vz],
        mode="lines", line=dict(color="#8b5cf6", width=2, dash="dash"),
        showlegend=False,
    ))
    # Origin dot
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers", marker=dict(size=5, color="white"),
        showlegend=False,
    ))

    lim = max(abs(vx), abs(vy), abs(vz), 5) + 1
    fig.update_layout(
        height=500,
        scene=dict(
            xaxis=dict(range=[-lim, lim], title="x"),
            yaxis=dict(range=[-lim, lim], title="y"),
            zaxis=dict(range=[-lim, lim], title="z"),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
        ),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Magnitude |v|", f"{mag:.4f}")
        st.metric("Direction α (x-axis)", f"{alpha:.2f}°")
    with c2:
        st.metric("Unit vector", f"({vx/mag:.4f}, {vy/mag:.4f}, {vz/mag:.4f})" if mag > 0 else "(0,0,0)")
        st.metric("β (y-axis), γ (z-axis)", f"β={beta:.1f}°, γ={gamma:.1f}°")

    st.latex(r"\vec{v} = " + f"{vx:.1f}" + r"\hat{i} + " + f"{vy:.1f}" + r"\hat{j} + " + f"{vz:.1f}" + r"\hat{k}")
    st.latex(r"|\vec{v}| = \sqrt{" + f"{vx:.1f}" + r"^2 + " + f"{vy:.1f}" + r"^2 + " + f"{vz:.1f}" + r"^2} = " + f"{mag:.4f}")
    st.caption("🖱️ Drag to rotate · Scroll to zoom")

# ── Cross Product (3D) ───────────────────────────────────
elif topic == "Cross Product (3D)":
    st.markdown("## Cross Product a × b")
    st.latex(r"\vec{a} \times \vec{b} = |\vec{a}||\vec{b}|\sin\theta\,\hat{n}")
    st.latex(r"= (a_yb_z - a_zb_y,\; a_zb_x - a_xb_z,\; a_xb_y - a_yb_x)")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Vector a**")
        ax = st.slider("aₓ", -5.0, 5.0, 2.0, 0.1, key="cp_ax")
        ay = st.slider("aᵧ", -5.0, 5.0, 0.0, 0.1, key="cp_ay")
        az = st.slider("a_z", -5.0, 5.0, 0.0, 0.1, key="cp_az")
    with col2:
        st.markdown("**Vector b**")
        bx = st.slider("bₓ", -5.0, 5.0, 0.0, 0.1, key="cp_bx")
        by = st.slider("bᵧ", -5.0, 5.0, 2.0, 0.1, key="cp_by")
        bz = st.slider("b_z", -5.0, 5.0, 0.0, 0.1, key="cp_bz")

    # Cross product
    cx = ay * bz - az * by
    cy = az * bx - ax * bz
    cz = ax * by - ay * bx

    mag_a = math.sqrt(ax**2 + ay**2 + az**2)
    mag_b = math.sqrt(bx**2 + by**2 + bz**2)
    mag_c = math.sqrt(cx**2 + cy**2 + cz**2)

    # Angle between a and b
    dot_ab = ax * bx + ay * by + az * bz
    cos_ang = dot_ab / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0
    angle_ab = math.degrees(math.acos(max(-1, min(1, cos_ang))))

    fig = go.Figure()
    # Vector a
    fig.add_trace(go.Scatter3d(
        x=[0, ax], y=[0, ay], z=[0, az],
        mode="lines+markers",
        line=dict(color="#6366f1", width=5),
        marker=dict(size=[0, 8], color="#6366f1"),
        name=f"a = ({ax:.1f}, {ay:.1f}, {az:.1f})",
    ))
    # Vector b
    fig.add_trace(go.Scatter3d(
        x=[0, bx], y=[0, by], z=[0, bz],
        mode="lines+markers",
        line=dict(color="#10b981", width=5),
        marker=dict(size=[0, 8], color="#10b981"),
        name=f"b = ({bx:.1f}, {by:.1f}, {bz:.1f})",
    ))
    # Cross product a×b
    c_label = f"a×b = ({cx:.2f}, {cy:.2f}, {cz:.2f})"
    fig.add_trace(go.Scatter3d(
        x=[0, cx], y=[0, cy], z=[0, cz],
        mode="lines+markers",
        line=dict(color="#ef4444", width=5, dash="dash"),
        marker=dict(size=[0, 10], color="#ef4444"),
        name=c_label,
    ))
    # Origin
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers", marker=dict(size=5, color="white"),
        showlegend=False,
    ))

    lim = max(abs(ax), abs(ay), abs(az), abs(bx), abs(by), abs(bz), abs(cx), abs(cy), abs(cz), 5) + 1
    fig.update_layout(
        height=500,
        scene=dict(
            xaxis=dict(range=[-lim, lim], title="x"),
            yaxis=dict(range=[-lim, lim], title="y"),
            zaxis=dict(range=[-lim, lim], title="z"),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
        ),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("|a|", f"{mag_a:.3f}")
    with c2: st.metric("|b|", f"{mag_b:.3f}")
    with c3: st.metric("|a×b|", f"{mag_c:.3f}")
    with c4: st.metric("θ (a,b)", f"{angle_ab:.2f}°")

    st.markdown(
        f'<div class="result-box">'
        f'a × b = ({ax:.1f}, {ay:.1f}, {az:.1f}) × ({bx:.1f}, {by:.1f}, {bz:.1f})<br>'
        f'= ({cx:.3f}, {cy:.3f}, {cz:.3f})<br>'
        f'|a×b| = {mag_c:.3f} = |a||b|sinθ = {mag_a:.3f}×{mag_b:.3f}×{math.sin(math.radians(angle_ab)):.4f}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.info("🔁 **Right-hand rule:** point fingers along a, curl toward b — thumb points along a×b.")

# ── Shortest Distance ────────────────────────────────────
elif topic == "Shortest Distance":
    st.markdown("## Shortest Distance Calculator")

    dist_mode = st.radio("Mode", [
        "Point → Line (2D)",
        "Point → Line (3D)",
        "Point → Plane",
    ], horizontal=True)

    if dist_mode == "Point → Line (2D)":
        st.markdown("### Point to Line Distance (2D)")
        st.latex(r"d = \frac{|ax_0 + by_0 + c|}{\sqrt{a^2 + b^2}}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Line: ax + by + c = 0**")
            a = st.slider("a", -10.0, 10.0, 2.0, 0.1, key="d_a")
            b = st.slider("b", -10.0, 10.0, -3.0, 0.1, key="d_b")
            c = st.slider("c", -10.0, 10.0, 6.0, 0.1, key="d_c")
        with col2:
            st.markdown("**Point P = (x₀, y₀)**")
            px = st.slider("x₀", -10.0, 10.0, 4.0, 0.1, key="d_px")
            py = st.slider("y₀", -10.0, 10.0, 5.0, 0.1, key="d_py")

        denom = math.sqrt(a**2 + b**2)
        if denom == 0:
            st.error("Invalid line: a = b = 0")
        else:
            dist = abs(a * px + b * py + c) / denom
            # Foot of perpendicular
            # The line's normal vector is (a, b). The foot is found by projecting.
            # line: ax+by+c=0, point P=(px,py)
            # foot F = (px - a*t, py - b*t) where t = (a*px+b*py+c)/(a²+b²)
            t_val = (a * px + b * py + c) / (a**2 + b**2)
            fx = px - a * t_val
            fy = py - b * t_val

            st.success(f"**Shortest distance d = {dist:.6f}**")

            # Visualization
            x_line = np.linspace(-10, 10, 400)
            if abs(b) > 0.001:
                y_line = (-a * x_line - c) / b
            else:
                x_line = np.full(400, -c / a)
                y_line = np.linspace(-10, 10, 400)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_line, y=y_line, mode="lines",
                line=dict(color="#6366f1", width=2),
                name=f"{a}x + {b}y + {c} = 0",
            ))
            # Point
            fig.add_trace(go.Scatter(
                x=[px], y=[py], mode="markers",
                marker=dict(size=10, color="#ef4444", symbol="x"),
                name=f"P({px:.1f}, {py:.1f})",
            ))
            # Perpendicular line (foot)
            fig.add_trace(go.Scatter(
                x=[px, fx], y=[py, fy], mode="lines",
                line=dict(color="#f59e0b", width=2, dash="dash"),
                name=f"d = {dist:.4f}",
            ))
            # Foot point
            fig.add_trace(go.Scatter(
                x=[fx], y=[fy], mode="markers",
                marker=dict(size=8, color="#10b981"),
                name=f"Foot({fx:.3f}, {fy:.3f})",
            ))
            fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
            fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dash"))
            fig.update_layout(
                height=450,
                xaxis=dict(range=[-10, 10], scaleanchor="y"),
                yaxis=dict(range=[-10, 10]),
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                f'<div class="result-box">'
                f'd = |{a}×{px:.1f} + {b}×{py:.1f} + {c}| / √({a}² + {b}²)<br>'
                f'd = |{a*px + b*py + c:.3f}| / {denom:.4f} = <strong>{dist:.6f}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

    elif dist_mode == "Point → Line (3D)":
        st.markdown("### Point to Line Distance (3D)")
        st.latex(r"d = \frac{|\vec{PA} \times \vec{d}|}{|\vec{d}|}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Line through A with direction d**")
            a0 = st.slider("Aₓ", -5.0, 5.0, 0.0, 0.1, key="d3_a0")
            a1 = st.slider("Aᵧ", -5.0, 5.0, 0.0, 0.1, key="d3_a1")
            a2 = st.slider("A_z", -5.0, 5.0, 0.0, 0.1, key="d3_a2")
            dx = st.slider("dₓ", -5.0, 5.0, 2.0, 0.1, key="d3_dx")
            dy = st.slider("dᵧ", -5.0, 5.0, 1.0, 0.1, key="d3_dy")
            dz = st.slider("d_z", -5.0, 5.0, 0.0, 0.1, key="d3_dz")
        with col2:
            st.markdown("**Point P**")
            px = st.slider("Pₓ", -5.0, 5.0, 3.0, 0.1, key="d3_px")
            py = st.slider("Pᵧ", -5.0, 5.0, 4.0, 0.1, key="d3_py")
            pz = st.slider("P_z", -5.0, 5.0, 2.0, 0.1, key="d3_pz")

        mag_d = math.sqrt(dx**2 + dy**2 + dz**2)
        if mag_d == 0:
            st.error("Direction vector d cannot be zero.")
        else:
            # PA = A - P
            pax, pay, paz = a0 - px, a1 - py, a2 - pz
            # Cross product PA × d
            cpx = pay * dz - paz * dy
            cpy = paz * dx - pax * dz
            cpz = pax * dy - pay * dx
            dist = math.sqrt(cpx**2 + cpy**2 + cpz**2) / mag_d

            # Foot: project A onto line
            # t = (P - A) · d / |d|²
            t_pa = ((px - a0) * dx + (py - a1) * dy + (pz - a2) * dz) / (mag_d**2)
            fx = a0 + t_pa * dx
            fy = a1 + t_pa * dy
            fz = a2 + t_pa * dz

            st.success(f"**Shortest distance d = {dist:.6f}**")

            # Visualization
            t_line = np.linspace(-5, 5, 100)
            fig = go.Figure()
            # Line
            fig.add_trace(go.Scatter3d(
                x=[a0 + ti * dx for ti in t_line],
                y=[a1 + ti * dy for ti in t_line],
                z=[a2 + ti * dz for ti in t_line],
                mode="lines", line=dict(color="#6366f1", width=4),
                name="Line",
            ))
            # Point P
            fig.add_trace(go.Scatter3d(
                x=[px], y=[py], z=[pz],
                mode="markers", marker=dict(size=8, color="#ef4444"),
                name=f"P({px:.1f}, {py:.1f}, {pz:.1f})",
            ))
            # Perpendicular
            fig.add_trace(go.Scatter3d(
                x=[px, fx], y=[py, fy], z=[pz, fz],
                mode="lines", line=dict(color="#f59e0b", width=3, dash="dash"),
                name=f"d = {dist:.4f}",
            ))
            # Foot
            fig.add_trace(go.Scatter3d(
                x=[fx], y=[fy], z=[fz],
                mode="markers", marker=dict(size=6, color="#10b981"),
                name=f"Foot({fx:.3f}, {fy:.3f}, {fz:.3f})",
            ))
            # Point A
            fig.add_trace(go.Scatter3d(
                x=[a0], y=[a1], z=[a2],
                mode="markers", marker=dict(size=5, color="white"),
                name="A (on line)",
            ))

            lim = 6
            fig.update_layout(
                height=500,
                scene=dict(
                    xaxis=dict(range=[-lim, lim], title="x"),
                    yaxis=dict(range=[-lim, lim], title="y"),
                    zaxis=dict(range=[-lim, lim], title="z"),
                    bgcolor="rgba(0,0,0,0)",
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🖱️ Drag to rotate · Scroll to zoom")

    elif dist_mode == "Point → Plane":
        st.markdown("### Point to Plane Distance")
        st.latex(r"d = \frac{|ax_0 + by_0 + cz_0 + d|}{\sqrt{a^2 + b^2 + c^2}}")
        st.markdown("**Plane: ax + by + cz + d = 0**")

        col1, col2 = st.columns(2)
        with col1:
            a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="dp_a")
            b = st.slider("b", -5.0, 5.0, 2.0, 0.1, key="dp_b")
            c = st.slider("c", -5.0, 5.0, 2.0, 0.1, key="dp_c")
            d = st.slider("d", -10.0, 10.0, -4.0, 0.1, key="dp_d")
        with col2:
            st.markdown("**Point P**")
            px = st.slider("Pₓ", -5.0, 5.0, 3.0, 0.1, key="dp_px")
            py = st.slider("Pᵧ", -5.0, 5.0, 1.0, 0.1, key="dp_py")
            pz = st.slider("P_z", -5.0, 5.0, -2.0, 0.1, key="dp_pz")

        denom = math.sqrt(a**2 + b**2 + c**2)
        if denom == 0:
            st.error("Invalid plane: a = b = c = 0")
        else:
            dist = abs(a * px + b * py + c * pz + d) / denom
            # Foot of perpendicular
            # F = P - (a*px+b*py+c*pz+d)/(a²+b²+c²) * (a,b,c)
            factor = (a * px + b * py + c * pz + d) / (a**2 + b**2 + c**2)
            fx = px - a * factor
            fy = py - b * factor
            fz = pz - c * factor

            st.success(f"**Shortest distance d = {dist:.6f}**")

            # Render plane as surface
            xx, zz = np.meshgrid(np.linspace(-5, 5, 20), np.linspace(-5, 5, 20))
            if abs(c) > 0.001:
                yy = (-a * xx - c * zz - d) / b if abs(b) > 0.001 else np.full_like(xx, (-a * xx - c * zz - d) / max(abs(b), 0.001))
                if abs(b) < 0.001:
                    yy = np.full_like(xx, 0)  # fallback
            else:
                yy = (-a * xx - d) / b if abs(b) > 0.001 else np.full_like(xx, 0)
                zz = np.full_like(xx, 5)

            mag_normal = math.sqrt(a**2 + b**2 + c**2)
            nx = a / mag_normal
            ny = b / mag_normal
            nz = c / mag_normal

            fig = go.Figure()
            # Plane surface
            fig.add_trace(go.Surface(
                x=xx, y=yy, z=zz,
                colorscale=[[0, "#6366f1"], [1, "#6366f1"]],
                opacity=0.3, showscale=False, name="Plane",
            ))
            # Normal vector (from origin or plane center)
            fig.add_trace(go.Scatter3d(
                x=[0, nx * 3], y=[0, ny * 3], z=[0, nz * 3],
                mode="lines+markers",
                line=dict(color="#8b5cf6", width=3, dash="dash"),
                marker=dict(size=[0, 6], color="#8b5cf6"),
                name="Normal n",
            ))
            # Point P
            fig.add_trace(go.Scatter3d(
                x=[px], y=[py], z=[pz],
                mode="markers", marker=dict(size=8, color="#ef4444"),
                name=f"P({px:.1f}, {py:.1f}, {pz:.1f})",
            ))
            # Perpendicular to plane
            fig.add_trace(go.Scatter3d(
                x=[px, fx], y=[py, fy], z=[pz, fz],
                mode="lines", line=dict(color="#f59e0b", width=3, dash="dash"),
                name=f"d = {dist:.4f}",
            ))
            # Foot point
            fig.add_trace(go.Scatter3d(
                x=[fx], y=[fy], z=[fz],
                mode="markers", marker=dict(size=6, color="#10b981"),
                name=f"Foot({fx:.3f}, {fy:.3f}, {fz:.3f})",
            ))

            fig.update_layout(
                height=500,
                scene=dict(
                    xaxis=dict(range=[-6, 6], title="x"),
                    yaxis=dict(range=[-6, 6], title="y"),
                    zaxis=dict(range=[-6, 6], title="z"),
                    bgcolor="rgba(0,0,0,0)",
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🖱️ Drag to rotate · Scroll to zoom · Purple dashed = plane normal")

            st.markdown(
                f'<div class="result-box">'
                f'd = |{a}×{px:.1f} + {b}×{py:.1f} + {c}×{pz:.1f} + {d}| / √({a}² + {b}² + {c}²)<br>'
                f'd = |{a*px + b*py + c*pz + d:.3f}| / {denom:.4f} = <strong>{dist:.6f}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ── Plane Vectors ────────────────────────────────────────
elif topic == "Plane Vectors":
    st.markdown("## Plane Vectors")

    plane_mode = st.radio("Mode", ["Point + Normal Vector", "Vector Equation r = a + λb + μc"], horizontal=True)

    if plane_mode == "Point + Normal Vector":
        st.markdown("### Plane: (r − r₀) · n = 0")
        st.markdown("Define a plane by a point on it and a normal vector.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Point on plane A**")
            a0 = st.slider("Aₓ", -5.0, 5.0, 0.0, 0.1, key="pl_a0")
            a1 = st.slider("Aᵧ", -5.0, 5.0, 0.0, 0.1, key="pl_a1")
            a2 = st.slider("A_z", -5.0, 5.0, 0.0, 0.1, key="pl_a2")
        with col2:
            st.markdown("**Normal vector n**")
            nx = st.slider("nₓ", -5.0, 5.0, 1.0, 0.1, key="pl_nx")
            ny = st.slider("nᵧ", -5.0, 5.0, 2.0, 0.1, key="pl_ny")
            nz = st.slider("n_z", -5.0, 5.0, 1.0, 0.1, key="pl_nz")

        mag_n = math.sqrt(nx**2 + ny**2 + nz**2)
        if mag_n == 0:
            st.error("Normal vector cannot be zero.")
        else:
            # Plane eq: nx(x-a0) + ny(y-a1) + nz(z-a2) = 0
            # => nx x + ny y + nz z + (-nx*a0 - ny*a1 - nz*a2) = 0
            d_plane = -nx * a0 - ny * a1 - nz * a2

            # Create grid
            xx, zz = np.meshgrid(np.linspace(-5, 5, 20), np.linspace(-5, 5, 20))
            if abs(nz) > 0.001:
                yy_plane = (-nx * xx - nz * zz - d_plane) / ny if abs(ny) > 0.001 else np.zeros_like(xx)
            else:
                if abs(ny) > 0.001:
                    yy_plane = (-nx * xx - d_plane) / ny
                else:
                    yy_plane = zz * 0

            fig = go.Figure()
            # Plane
            fig.add_trace(go.Surface(
                x=xx, y=yy_plane, z=zz,
                colorscale=[[0, "#6366f1"], [1, "#6366f1"]],
                opacity=0.25, showscale=False, name="Plane",
            ))
            # Normal vector from point A
            fig.add_trace(go.Scatter3d(
                x=[a0, a0 + nx], y=[a1, a1 + ny], z=[a2, a2 + nz],
                mode="lines+markers",
                line=dict(color="#ef4444", width=4),
                marker=dict(size=[0, 8], color="#ef4444"),
                name=f"n = ({nx:.1f}, {ny:.1f}, {nz:.1f})",
            ))
            # Point A
            fig.add_trace(go.Scatter3d(
                x=[a0], y=[a1], z=[a2],
                mode="markers", marker=dict(size=7, color="#f59e0b"),
                name=f"A({a0:.1f}, {a1:.1f}, {a2:.1f})",
            ))

            fig.update_layout(
                height=500,
                scene=dict(
                    xaxis=dict(range=[-6, 6], title="x"),
                    yaxis=dict(range=[-6, 6], title="y"),
                    zaxis=dict(range=[-6, 6], title="z"),
                    bgcolor="rgba(0,0,0,0)",
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                f'<div class="result-box">'
                f'<strong>Plane equation:</strong> {nx:.2f}(x − {a0:.1f}) + {ny:.2f}(y − {a1:.1f}) + {nz:.2f}(z − {a2:.1f}) = 0<br>'
                f'<strong>Cartesian:</strong> {nx:.2f}x + {ny:.2f}y + {nz:.2f}z + {d_plane:.2f} = 0'
                f'</div>',
                unsafe_allow_html=True,
            )

    else:
        st.markdown("### Vector Equation: r = a + λb + μc")
        st.markdown("Define a plane by a point **a** and two direction vectors **b** and **c**.")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Point a**")
            a0 = st.slider("aₓ", -5.0, 5.0, 0.0, 0.1, key="va_a0")
            a1 = st.slider("aᵧ", -5.0, 5.0, 0.0, 0.1, key="va_a1")
            a2 = st.slider("a_z", -5.0, 5.0, 0.0, 0.1, key="va_a2")
        with col2:
            st.markdown("**Direction b**")
            b0 = st.slider("bₓ", -5.0, 5.0, 2.0, 0.1, key="va_b0")
            b1 = st.slider("bᵧ", -5.0, 5.0, 0.0, 0.1, key="va_b1")
            b2 = st.slider("b_z", -5.0, 5.0, 0.0, 0.1, key="va_b2")
        with col3:
            st.markdown("**Direction c**")
            c0 = st.slider("cₓ", -5.0, 5.0, 0.0, 0.1, key="va_c0")
            c1 = st.slider("cᵧ", -5.0, 5.0, 2.0, 0.1, key="va_c1")
            c2 = st.slider("c_z", -5.0, 5.0, 0.0, 0.1, key="va_c2")

        # Check b × c ≠ 0
        n_cx = b1 * c2 - b2 * c1
        n_cy = b2 * c0 - b0 * c2
        n_cz = b0 * c1 - b1 * c0
        mag_n = math.sqrt(n_cx**2 + n_cy**2 + n_cz**2)

        if mag_n < 0.001:
            st.error("b and c are parallel: they don't define a plane (b×c = 0).")
        else:
            # Generate points on the plane
            lam_vals = np.linspace(-2, 2, 15)
            mu_vals = np.linspace(-2, 2, 15)
            points_x, points_y, points_z = [], [], []
            for lam in lam_vals:
                for mu in mu_vals:
                    points_x.append(a0 + lam * b0 + mu * c0)
                    points_y.append(a1 + lam * b1 + mu * c1)
                    points_z.append(a2 + lam * b2 + mu * c2)

            # Create mesh for surface
            ll, mm = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
            surf_x = a0 + ll * b0 + mm * c0
            surf_y = a1 + ll * b1 + mm * c1
            surf_z = a2 + ll * b2 + mm * c2

            fig = go.Figure()
            # Plane surface
            fig.add_trace(go.Surface(
                x=surf_x, y=surf_y, z=surf_z,
                colorscale=[[0, "#6366f1"], [1, "#6366f1"]],
                opacity=0.2, showscale=False, name="Plane",
            ))
            # Point a
            fig.add_trace(go.Scatter3d(
                x=[a0], y=[a1], z=[a2],
                mode="markers", marker=dict(size=7, color="#f59e0b"),
                name=f"a({a0:.1f}, {a1:.1f}, {a2:.1f})",
            ))
            # Vector b from a
            fig.add_trace(go.Scatter3d(
                x=[a0, a0 + b0], y=[a1, a1 + b1], z=[a2, a2 + b2],
                mode="lines+markers",
                line=dict(color="#10b981", width=4),
                marker=dict(size=[0, 6], color="#10b981"),
                name=f"b = ({b0:.1f}, {b1:.1f}, {b2:.1f})",
            ))
            # Vector c from a
            fig.add_trace(go.Scatter3d(
                x=[a0, a0 + c0], y=[a1, a1 + c1], z=[a2, a2 + c2],
                mode="lines+markers",
                line=dict(color="#ef4444", width=4),
                marker=dict(size=[0, 6], color="#ef4444"),
                name=f"c = ({c0:.1f}, {c1:.1f}, {c2:.1f})",
            ))
            # Normal = b × c
            fig.add_trace(go.Scatter3d(
                x=[a0, a0 + n_cx], y=[a1, a1 + n_cy], z=[a2, a2 + n_cz],
                mode="lines+markers",
                line=dict(color="#a855f7", width=3, dash="dash"),
                marker=dict(size=[0, 6], color="#a855f7"),
                name=f"n = b×c = ({n_cx:.2f}, {n_cy:.2f}, {n_cz:.2f})",
            ))

            # Scatter points
            fig.add_trace(go.Scatter3d(
                x=points_x, y=points_y, z=points_z,
                mode="markers", marker=dict(size=2, color="#6366f1", opacity=0.5),
                name="Grid",
            ))

            fig.update_layout(
                height=500,
                scene=dict(
                    xaxis=dict(range=[-6, 6], title="x"),
                    yaxis=dict(range=[-6, 6], title="y"),
                    zaxis=dict(range=[-6, 6], title="z"),
                    bgcolor="rgba(0,0,0,0)",
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    st.caption("🖱️ Drag to rotate · Scroll to zoom")

# ── Unit Circle ──────────────────────────────────────────
elif topic == "Unit Circle":
    st.markdown("## Unit Circle Explorer")
    angle = st.slider("Angle θ (degrees)", 0, 360, 45, 1)
    rad = math.radians(angle)
    cx, cy = math.cos(rad), math.sin(rad)

    theta = np.linspace(0, 2*np.pi, 400)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines",
                              name="Unit circle", line=dict(color="#6366f1", width=2)))
    fig.add_trace(go.Scatter(x=[0, cx], y=[0, cy], mode="lines",
                              name=f"θ = {angle}°",
                              line=dict(color="#f59e0b", width=2)))
    fig.add_trace(go.Scatter(x=[cx], y=[cy], mode="markers",
                              marker=dict(size=10, color="#ef4444"), name="Point"))
    fig.add_trace(go.Scatter(x=[0, cx], y=[cy, cy], mode="lines",
                              line=dict(color="#10b981", width=1, dash="dot"), name=f"sin = {cy:.4f}"))
    fig.add_trace(go.Scatter(x=[cx, cx], y=[0, cy], mode="lines",
                              line=dict(color="#8b5cf6", width=1, dash="dot"), name=f"cos = {cx:.4f}"))

    fig.update_layout(height=500, xaxis_range=[-1.3, 1.3], yaxis_range=[-1.3, 1.3],
                      xaxis=dict(scaleanchor="y"), margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("sin θ", f"{cy:.4f}")
    with col2: st.metric("cos θ", f"{cx:.4f}")
    with col3: st.metric("tan θ", f"{cy/cx:.4f}" if abs(cx) > 0.001 else "∞")

# ── 3D Geometry ────────────────────────────────────────────
elif topic == "3D Geometry":
    st.markdown("## 3D Geometry Explorer")
    st.markdown("Click, drag, and scroll to rotate and zoom. Dimension labels shown in color.")

    shape = st.selectbox("Shape", [
        "Sphere", "Cube", "Pyramid", "Prism",
        "Cylinder", "Cone", "Torus", "Helix", "Sinusoidal Surface"
    ])

    dim_color_r = "#ef4444"
    dim_color_h = "#3b82f6"
    dim_color_s = "#22c55e"
    dim_color_R = "#f97316"

    def label_3d(fig, x, y, z, text, color="white", size=14):
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode="text",
                                    text=[text], textfont=dict(color=color, size=size),
                                    hoverinfo="none", showlegend=False))

    def dim_line(fig, x1, y1, z1, x2, y2, z2, color, width=3):
        fig.add_trace(go.Scatter3d(x=[x1, x2], y=[y1, y2], z=[z1, z2],
                                    mode="lines", line=dict(color=color, width=width, dash="dash"),
                                    hoverinfo="none", showlegend=False))

    fig = go.Figure()

    if shape == "Sphere":
        r = st.slider("Radius", 0.5, 5.0, 2.0, 0.1)
        phi, theta = np.mgrid[0:2*np.pi:40j, 0:np.pi:40j]
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale="Viridis", opacity=0.85, showscale=False))
        dim_line(fig, 0, 0, 0, r, 0, 0, dim_color_r, 3)
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers",
                                    marker=dict(size=4, color="white"), hoverinfo="none", showlegend=False))
        label_3d(fig, r/2, 0, -0.4, "r", dim_color_r, 16)
        st.latex(r"V = \frac{4}{3}\pi r^3  \quad A = 4\pi r^2")
        c1, c2 = st.columns(2)
        with c1: st.metric("Surface Area", f"{4*math.pi*r**2:.2f}")
        with c2: st.metric("Volume", f"{(4/3)*math.pi*r**3:.2f}")

    elif shape == "Cube":
        s = st.slider("Side length", 0.5, 5.0, 2.0, 0.1)
        h2 = s / 2
        pts = [[x, y, z] for x in [-h2, h2] for y in [-h2, h2] for z in [-h2, h2]]
        edges = [[0,1],[1,3],[3,2],[2,0],[4,5],[5,7],[7,6],[6,4],[0,4],[1,5],[2,6],[3,7]]
        ex, ey, ez = [], [], []
        for a, b in edges:
            ex += [pts[a][0], pts[b][0], None]
            ey += [pts[a][1], pts[b][1], None]
            ez += [pts[a][2], pts[b][2], None]
        fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
                                    line=dict(color="#6366f1", width=4), hoverinfo="none", showlegend=False))
        fig.add_trace(go.Scatter3d(x=[p[0] for p in pts], y=[p[1] for p in pts],
                                    z=[p[2] for p in pts], mode="markers",
                                    marker=dict(size=5, color="#ef4444"), hoverinfo="none", showlegend=False))
        dim_line(fig, pts[0][0], pts[0][1]-0.8, pts[0][2],
                 pts[1][0], pts[1][1]-0.8, pts[1][2], dim_color_s, 2)
        label_3d(fig, 0, -h2-0.8, -h2, "s", dim_color_s, 16)
        st.latex(r"V = s^3  \quad A = 6s^2")
        c1, c2 = st.columns(2)
        with c1: st.metric("Surface Area", f"{6*s**2:.2f}")
        with c2: st.metric("Volume", f"{s**3:.2f}")

    elif shape == "Pyramid":
        bs = st.slider("Base side", 0.5, 5.0, 2.0, 0.1)
        ph = st.slider("Height", 0.5, 5.0, 2.0, 0.1)
        hb = bs / 2
        pts = [[-hb,-hb,0],[hb,-hb,0],[hb,hb,0],[-hb,hb,0],[0,0,ph]]
        edges = [[0,1],[1,2],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4]]
        ex, ey, ez = [], [], []
        for a, b in edges:
            ex += [pts[a][0], pts[b][0], None]
            ey += [pts[a][1], pts[b][1], None]
            ez += [pts[a][2], pts[b][2], None]
        fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
                                    line=dict(color="#f59e0b", width=4), hoverinfo="none", showlegend=False))
        fig.add_trace(go.Scatter3d(x=[p[0] for p in pts], y=[p[1] for p in pts],
                                    z=[p[2] for p in pts], mode="markers",
                                    marker=dict(size=5, color="#ef4444"), hoverinfo="none", showlegend=False))
        dim_line(fig, 0, 0, 0, 0, 0, ph, dim_color_h, 2)
        label_3d(fig, 0.4, 0, ph/2, "h", dim_color_h, 16)
        dim_line(fig, pts[0][0], pts[0][1]-0.6, 0, pts[1][0], pts[1][1]-0.6, 0, dim_color_s, 2)
        label_3d(fig, 0, -hb-0.6, 0, "s", dim_color_s, 16)
        slant = math.sqrt(hb**2 + ph**2)
        a_base = bs**2
        a_side = 2 * bs * slant
        st.latex(r"V = \frac{1}{3}s^2 h  \quad A = s^2 + 2s\sqrt{(\frac{s}{2})^2 + h^2}")
        c1, c2 = st.columns(2)
        with c1: st.metric("Surface Area", f"{a_base + a_side:.2f}")
        with c2: st.metric("Volume", f"{a_base*ph/3:.2f}")

    elif shape == "Prism":
        pr_h = st.slider("Height", 1.0, 6.0, 3.0, 0.1)
        bl = st.slider("Base side (triangle)", 0.5, 5.0, 2.0, 0.1)
        ht = st.slider("Triangle height", 0.5, 4.0, 1.5, 0.1)
        hht = ht / 3
        bt = bl / 2
        bot = [[-bt,-hht,0],[bt,-hht,0],[0,2*hht,0]]
        top = [[-bt,-hht,pr_h],[bt,-hht,pr_h],[0,2*hht,pr_h]]
        pts2 = bot + top
        edges2 = [[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]]
        ex2, ey2, ez2 = [], [], []
        for a, b in edges2:
            ex2 += [pts2[a][0], pts2[b][0], None]
            ey2 += [pts2[a][1], pts2[b][1], None]
            ez2 += [pts2[a][2], pts2[b][2], None]
        fig.add_trace(go.Scatter3d(x=ex2, y=ey2, z=ez2, mode="lines",
                                    line=dict(color="#10b981", width=4), hoverinfo="none", showlegend=False))
        fig.add_trace(go.Scatter3d(x=[p[0] for p in pts2], y=[p[1] for p in pts2],
                                    z=[p[2] for p in pts2], mode="markers",
                                    marker=dict(size=5, color="#ef4444"), hoverinfo="none", showlegend=False))
        dim_line(fig, -bl/2, -ht/3-0.6, 0, bl/2, -ht/3-0.6, 0, dim_color_s, 2)
        label_3d(fig, 0, -ht/3-0.6, 0, "s", dim_color_s, 16)
        dim_line(fig, bl/2+0.6, -ht/3, 0, bl/2+0.6, -ht/3, pr_h, dim_color_h, 2)
        label_3d(fig, bl/2+0.6, -ht/3, pr_h/2, "h", dim_color_h, 16)
        a_base_tri = (math.sqrt(3)/4) * bl**2
        st.latex(r"V = \frac{\sqrt{3}}{4}s^2 h  \quad A = \frac{\sqrt{3}}{2}s^2 + 3sh")
        c1, c2 = st.columns(2)
        with c1: st.metric("Surface Area", f"{2*a_base_tri + 3*bl*pr_h:.2f}")
        with c2: st.metric("Volume", f"{a_base_tri*pr_h:.2f}")

    elif shape == "Cylinder":
        r = st.slider("Radius", 0.5, 5.0, 2.0, 0.1)
        h = st.slider("Height", 1.0, 8.0, 4.0, 0.1)
        zc = np.linspace(-h/2, h/2, 30)
        tc = np.linspace(0, 2*np.pi, 40)
        tc, zc = np.meshgrid(tc, zc)
        fig.add_trace(go.Surface(x=r*np.cos(tc), y=r*np.sin(tc), z=zc,
                                  colorscale="Turbo", opacity=0.85, showscale=False))
        dim_line(fig, 0, 0, -h/2, r, 0, -h/2, dim_color_r, 2)
        label_3d(fig, r/2, -0.4, -h/2-0.4, "r", dim_color_r, 16)
        dim_line(fig, r+0.5, 0, -h/2, r+0.5, 0, h/2, dim_color_h, 2)
        label_3d(fig, r+0.5, 0, 0, "h", dim_color_h, 16)
        st.latex(r"V = \pi r^2 h  \quad A = 2\pi r(h+r)")
        c1, c2 = st.columns(2)
        with c1: st.metric("Surface Area", f"{2*math.pi*r*(h+r):.2f}")
        with c2: st.metric("Volume", f"{math.pi*r**2*h:.2f}")

    elif shape == "Cone":
        r = st.slider("Base radius", 0.5, 5.0, 2.0, 0.1)
        h = st.slider("Height", 1.0, 8.0, 4.0, 0.1)
        n = 40
        tc2, zc2 = np.meshgrid(np.linspace(0, 2*np.pi, n), np.linspace(0, h, n))
        rc = r * (1 - zc2 / h)
        fig.add_trace(go.Surface(x=rc*np.cos(tc2), y=rc*np.sin(tc2), z=zc2,
                                  colorscale="Electric", opacity=0.85, showscale=False))
        dim_line(fig, 0, 0, 0, r, 0, 0, dim_color_r, 2)
        label_3d(fig, r/2, -0.4, -0.4, "r", dim_color_r, 16)
        dim_line(fig, 0, 0, 0, 0, 0, h, dim_color_h, 2)
        label_3d(fig, 0.4, 0, h/2, "h", dim_color_h, 16)
        sl = math.sqrt(r**2 + h**2)
        dim_line(fig, r, 0, 0, 0, 0, h, "#a855f7", 2)
        label_3d(fig, r/2, 0.4, h/2, "l", "#a855f7", 16)
        st.latex(r"V = \frac{1}{3}\pi r^2 h  \quad A = \pi r(r+l)")
        c1, c2 = st.columns(2)
        with c1: st.metric("Surface Area", f"{math.pi*r*(r+sl):.2f}")
        with c2: st.metric("Volume", f"{(1/3)*math.pi*r**2*h:.2f}")

    elif shape == "Torus":
        R = st.slider("Major radius", 1.0, 5.0, 3.0, 0.1)
        r = st.slider("Minor radius", 0.3, 3.0, 1.0, 0.1)
        u, v = np.mgrid[0:2*np.pi:50j, 0:2*np.pi:50j]
        fig.add_trace(go.Surface(
            x=(R + r*np.cos(v))*np.cos(u),
            y=(R + r*np.cos(v))*np.sin(u),
            z=r*np.sin(v),
            colorscale="Portland", opacity=0.9, showscale=False))
        dim_line(fig, 0, 0, 0, R, 0, 0, dim_color_R, 2)
        label_3d(fig, R/2, -0.5, 0.4, "R", dim_color_R, 16)
        dim_line(fig, R, 0, 0, R+r, 0, 0, dim_color_r, 2)
        label_3d(fig, R+r/2, -0.5, 0.4, "r", dim_color_r, 16)
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers",
                                    marker=dict(size=4, color="white"),
                                    hoverinfo="none", showlegend=False))
        st.latex(r"V = 2\pi^2 R r^2  \quad A = 4\pi^2 R r")
        c1, c2 = st.columns(2)
        with c1: st.metric("Surface Area", f"{4*math.pi**2*R*r:.2f}")
        with c2: st.metric("Volume", f"{2*math.pi**2*R*r**2:.2f}")

    elif shape == "Helix":
        coils = st.slider("Coils", 1, 20, 5, 1)
        r = st.slider("Radius", 0.3, 3.0, 1.5, 0.1)
        t_h = np.linspace(0, coils*2*np.pi, 500)
        z_h = np.linspace(0, 5, 500)
        fig.add_trace(go.Scatter3d(x=r*np.cos(t_h), y=r*np.sin(t_h), z=z_h,
                                    mode="lines", line=dict(color="#6366f1", width=5),
                                    showlegend=False))
        fig.add_trace(go.Scatter3d(x=[r*np.cos(t_h[-1])], y=[r*np.sin(t_h[-1])],
                                    z=[z_h[-1]], mode="markers",
                                    marker=dict(size=7, color="#ef4444"),
                                    showlegend=False))
        dim_line(fig, 0, 0, 0, r, 0, 0, dim_color_r, 2)
        label_3d(fig, r/2, -0.4, 0, "r", dim_color_r, 16)
        dim_line(fig, 0, 0, 0, 0, 0, 5, dim_color_h, 2)
        label_3d(fig, 0.3, 0.3, 2.5, "h", dim_color_h, 16)
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers",
                                    marker=dict(size=4, color="white"),
                                    hoverinfo="none", showlegend=False))
        approx_len = math.sqrt((2*math.pi*r*coils)**2 + 25)
        st.info(f"**Estimated length:** {approx_len:.2f} units (one coil ≈ {approx_len/coils:.2f})")

    elif shape == "Sinusoidal Surface":
        amp = st.slider("Amplitude", 0.5, 5.0, 2.0, 0.1)
        freq_s = st.slider("Frequency", 0.5, 5.0, 2.0, 0.1)
        xs = np.linspace(-5, 5, 50)
        ys = np.linspace(-5, 5, 50)
        xs, ys = np.meshgrid(xs, ys)
        z_surf = amp * np.sin(freq_s * np.sqrt(xs**2 + ys**2))
        fig.add_trace(go.Surface(x=xs, y=ys, z=z_surf,
                                  colorscale="Thermal", opacity=0.9, showscale=False))
        dim_line(fig, 0, 0, 0, 0, 0, amp, dim_color_h, 2)
        label_3d(fig, 0.5, 0, amp/2, "A", dim_color_h, 16)
        st.latex(r"z = A\sin\left(f\sqrt{x^2+y^2}\right)")

    fig.update_layout(
        height=550,
        scene=dict(
            xaxis=dict(showgrid=True, gridcolor="#333", zeroline=False, showbackground=False),
            yaxis=dict(showgrid=True, gridcolor="#333", zeroline=False, showbackground=False),
            zaxis=dict(showgrid=True, gridcolor="#333", zeroline=False, showbackground=False),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("🖱️ Drag to rotate · Scroll to zoom · Dashed lines show dimensions")

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
