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
    "🔄 Transformations",
])

topic_map = {
    "🔢 Algebra": ["Linear Functions", "Quadratic Equation",
                    "Exponential Functions", "Logarithmic Functions",
                    "Square Root Functions", "Rational Functions",
                    "Piecewise Functions",
                    "Intersection: Linear & Linear",
                    "Intersection: Linear & Quadratic"],
    "📐 Trigonometry": ["Trigonometry Explorer", "Unit Circle"],
    "📈 Calculus": ["Derivative Visualizer", "Integral Area"],
    "🧭 Vectors": ["2D Vector Explorer", "Vector Addition", "Dot Product",
                    "3D Vector Explorer", "Cross Product (3D)",
                    "Shortest Distance", "Plane Vectors"],
    "🧊 Geometry": ["3D Geometry"],
    "🔄 Transformations": ["Reflection", "Translation", "Rotation",
                           "Enlargement (Dilation)", "Modulus |f(x)|",
                           "Inverse f⁻¹(x)", "Reciprocal 1/f(x)",
                           "Shear", "Stretch"],
}

topic = st.sidebar.radio("Topic", topic_map[category])

# ── Exponential Functions ────────────────────────────────
# ── Linear Functions ─────────────────────────────────────
if topic == "Linear Functions":
    st.markdown("## Linear Functions")
    st.latex(r"f(x) = mx + c")

    col1, col2 = st.columns(2)
    with col1:
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="lin_m")
    with col2:
        c = st.slider("y-intercept c", -10.0, 10.0, 0.0, 0.1, key="lin_c")

    x = np.linspace(-10, 10, 400)
    y = m * x + c

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines",
                              name=f"y = {m}x + {c}",
                              line=dict(color="#6366f1", width=2)))
    if abs(m) < 5 and abs(m) > 0.01:
        run = 2.0
        x0, y0 = 1.0, m * 1.0 + c
        x1 = x0 + run
        y1 = m * x1 + c
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y0], mode="lines",
                                  line=dict(color="#ef4444", width=1, dash="dot"),
                                  showlegend=False))
        fig.add_trace(go.Scatter(x=[x1, x1], y=[y0, y1], mode="lines",
                                  line=dict(color="#10b981", width=1, dash="dot"),
                                  showlegend=False))
        fig.add_annotation(x=(x0+x1)/2, y=y0-0.5, text=f"run={run:.0f}",
                           showarrow=False, font=dict(color="#ef4444", size=11))
        fig.add_annotation(x=x1+0.3, y=(y0+y1)/2, text=f"rise={m*run:.1f}",
                           showarrow=False, font=dict(color="#10b981", size=11))

    y_int = c
    x_int = -c / m if abs(m) > 0.001 else None

    fig.add_trace(go.Scatter(x=[0], y=[y_int], mode="markers",
                              marker=dict(size=8, color="#f59e0b"),
                              name=f"y-int (0, {y_int:.2f})"))
    if x_int is not None:
        fig.add_trace(go.Scatter(x=[x_int], y=[0], mode="markers",
                                  marker=dict(size=8, color="#f59e0b", symbol="x"),
                                  name=f"x-int ({x_int:.2f}, 0)"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(range=[-10, 10], scaleanchor="y"),
                      yaxis=dict(range=[-10, 10]), hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f'<div class="result-box">'
        f'<strong>Slope:</strong> m = {m:.2f}  '
        f'({"↗ increasing" if m > 0 else "↘ decreasing" if m < 0 else "→ constant"})<br>'
        f'<strong>y-intercept:</strong> (0, {y_int:.2f})<br>'
        f'{"" if x_int is None else f"<strong>x-intercept:</strong> ({x_int:.4f}, 0)"}'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Intersection: Linear & Linear ─────────────────────────
elif topic == "Intersection: Linear & Linear":
    st.markdown("## Intersection: Two Lines")
    st.markdown("Find where y1 = m1x + c1 and y2 = m2x + c2 meet.")
    st.latex(r"m_1x + c_1 = m_2x + c_2 \quad\rightarrow\quad x = \frac{c_2 - c_1}{m_1 - m_2}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Line 1**")
        m1 = st.slider("m1", -5.0, 5.0, 1.0, 0.1, key="ll_m1")
        c1 = st.slider("c1", -10.0, 10.0, -2.0, 0.1, key="ll_c1")
    with col2:
        st.markdown("**Line 2**")
        m2 = st.slider("m2", -5.0, 5.0, -1.0, 0.1, key="ll_m2")
        c2 = st.slider("c2", -10.0, 10.0, 4.0, 0.1, key="ll_c2")

    x = np.linspace(-10, 10, 400)
    y1 = m1 * x + c1
    y2 = m2 * x + c2

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode="lines",
                              name=f"y1 = {m1}x + {c1}",
                              line=dict(color="#6366f1", width=2)))
    fig.add_trace(go.Scatter(x=x, y=y2, mode="lines",
                              name=f"y2 = {m2}x + {c2}",
                              line=dict(color="#10b981", width=2)))

    if abs(m1 - m2) < 0.001:
        if abs(c1 - c2) < 0.001:
            st.info("Infinite intersections (coincident lines).")
        else:
            st.warning("Parallel lines - no intersection.")
    else:
        ix = (c2 - c1) / (m1 - m2)
        iy = m1 * ix + c1
        st.success(f"**Intersection:** ({ix:.4f}, {iy:.4f})")
        fig.add_trace(go.Scatter(x=[ix], y=[iy], mode="markers",
                                  marker=dict(size=12, color="#ef4444", symbol="x"),
                                  name=f"({ix:.3f}, {iy:.3f})"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(range=[-10, 10], scaleanchor="y"),
                      yaxis=dict(range=[-10, 10]), hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Intersection: Linear & Quadratic ──────────────────────
elif topic == "Intersection: Linear & Quadratic":
    st.markdown("## Intersection: Line & Parabola")
    st.markdown("Find where line y = mx + k meets parabola y = ax^2 + bx + c.")
    st.latex(r"ax^2 + (b-m)x + (c-k) = 0")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Line: y = mx + k**")
        m = st.slider("m", -5.0, 5.0, 1.0, 0.1, key="lq_m")
        k = st.slider("k", -10.0, 10.0, 0.0, 0.1, key="lq_k")
    with col2:
        st.markdown("**Parabola: y = ax^2 + bx + c**")
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="lq_a")
        bq = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="lq_b")
        cq = st.slider("c", -10.0, 10.0, -4.0, 0.1, key="lq_c")

    A = a
    B = bq - m
    C = cq - k

    x = np.linspace(-10, 10, 600)
    y_line = m * x + k
    y_quad = a * x**2 + bq * x + cq

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_quad, mode="lines",
                              name=f"y = {a}x^2 + {bq}x + {cq}",
                              line=dict(color="#6366f1", width=2)))
    fig.add_trace(go.Scatter(x=x, y=y_line, mode="lines",
                              name=f"y = {m}x + {k}",
                              line=dict(color="#f59e0b", width=2)))

    if abs(A) < 0.001:
        if abs(B) < 0.001:
            msg = "Coincident - infinite intersections." if abs(C) < 0.001 else "No intersection."
            st.info(msg)
        else:
            ix = -C / B
            iy = m * ix + k
            st.success(f"**Intersection:** ({ix:.4f}, {iy:.4f})")
            fig.add_trace(go.Scatter(x=[ix], y=[iy], mode="markers",
                                      marker=dict(size=12, color="#ef4444"),
                                      name=f"({ix:.3f}, {iy:.3f})"))
    else:
        D = B**2 - 4*A*C
        if D < 0:
            st.warning(f"**No intersection.** Delta = {D:.4f} < 0")
        elif D == 0:
            ix = -B / (2*A)
            iy = m * ix + k
            st.info(f"**Tangent:** ({ix:.4f}, {iy:.4f})")
            fig.add_trace(go.Scatter(x=[ix], y=[iy], mode="markers",
                                      marker=dict(size=12, color="#ef4444"),
                                      name=f"({ix:.3f}, {iy:.3f})"))
        else:
            sqrt_D = math.sqrt(D)
            ix1 = (-B + sqrt_D) / (2*A)
            ix2 = (-B - sqrt_D) / (2*A)
            iy1 = m * ix1 + k
            iy2 = m * ix2 + k
            st.success("**Two intersections:**")
            st.markdown(f"P1 = ({ix1:.4f}, {iy1:.4f})")
            st.markdown(f"P2 = ({ix2:.4f}, {iy2:.4f})")
            fig.add_trace(go.Scatter(x=[ix1, ix2], y=[iy1, iy2], mode="markers",
                                      marker=dict(size=10, color="#ef4444"),
                                      name="Intersections"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                      yaxis_range=[-12, 12], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)
if topic == "Exponential Functions":
    st.markdown("## Exponential Functions")
    st.latex(r"f(x) = a \cdot b^{cx + d} + k")

    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("a (amplitude)", -5.0, 5.0, 1.0, 0.1, key="exp_a")
        b = st.slider("b (base)", 0.1, 5.0, 2.0, 0.1, key="exp_b")
        c = st.slider("c (stretch)", -3.0, 3.0, 1.0, 0.1, key="exp_c")
    with col2:
        d = st.slider("d (shift x)", -5.0, 5.0, 0.0, 0.1, key="exp_d")
        k = st.slider("k (shift y)", -5.0, 5.0, 0.0, 0.1, key="exp_k")

    x = np.linspace(-5, 5, 500)
    y = a * (b ** (c * x + d)) + k
    y = np.where(np.abs(y) > 50, np.nan, y)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"{a}·{b}⁽{c}x+{d}⁾ + {k}",
                              line=dict(color="#6366f1", width=2)))
    # Horizontal asymptote
    fig.add_hline(y=k, line=dict(color="#ef4444", width=1, dash="dash"),
                  annotation_text=f"y = {k:.2f}", annotation_position="right")
    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                      yaxis_range=[-16, 16], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f'<div class="result-box">'
        f'<strong>Asymptote:</strong> y = {k:.2f}<br>'
        f'<strong>y-intercept:</strong> f(0) = {a * (b ** d) + k:.4f}<br>'
        f'{"<strong>Growth</strong> (b > 1)" if b > 1 else "<strong>Decay</strong> (0 < b < 1)"}'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Logarithmic Functions ────────────────────────────────
elif topic == "Logarithmic Functions":
    st.markdown("## Logarithmic Functions")
    st.latex(r"f(x) = a \cdot \log_b(cx + d) + k")

    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("a (amplitude)", -5.0, 5.0, 1.0, 0.1, key="log_a")
        b = st.slider("b (base, >0, ≠1)", 0.5, 10.0, math.e, 0.1, key="log_b")
        c = st.slider("c (stretch)", -3.0, 3.0, 1.0, 0.1, key="log_c")
    with col2:
        d = st.slider("d (shift)", -5.0, 5.0, 0.0, 0.1, key="log_d")
        k = st.slider("k (vertical)", -5.0, 5.0, 0.0, 0.1, key="log_k")

    # Domain: cx + d > 0  →  x > -d/c (if c>0) or x < -d/c (if c<0)
    if abs(c) < 0.001:
        st.error("c cannot be zero (no domain).")
    else:
        bound = -d / c
        if c > 0:
            x = np.linspace(bound + 0.01, bound + 6, 600)
        else:
            x = np.linspace(bound - 6, bound - 0.01, 600)
        x = x[(x > -10) & (x < 10)]

        arg = c * x + d
        y = a * np.log(arg) / np.log(b) + k
        y = np.where(arg <= 0, np.nan, y)
        y = np.where(np.abs(y) > 50, np.nan, y)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"{a}·log_{{b}}(cx+{d})+{k}",
                                  line=dict(color="#10b981", width=2)))
        # Vertical asymptote
        fig.add_vline(x=bound, line=dict(color="#ef4444", width=1, dash="dash"),
                      annotation_text=f"x = {bound:.2f}", annotation_position="top")
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
        fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                          yaxis_range=[-8, 8], hovermode="x")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f'<div class="result-box">'
            f'<strong>Domain:</strong> {{"x > " if c > 0 else "x < "}}{bound:.4f}<br>'
            f'<strong>Vertical asymptote:</strong> x = {bound:.4f}<br>'
            f'<strong>x-intercept:</strong> f(x) = 0 → x = {"e" if abs(b-math.e)<0.01 else "b"}^({-k/a}) = {bound + (b ** (-k/a)) / c:.4f}'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Square Root Functions ────────────────────────────────
elif topic == "Square Root Functions":
    st.markdown("## Square Root Functions")
    st.latex(r"f(x) = a \sqrt{cx + d} + k")

    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("a (amplitude)", -5.0, 5.0, 1.0, 0.1, key="sqrt_a")
        c = st.slider("c (stretch)", -3.0, 3.0, 1.0, 0.1, key="sqrt_c")
    with col2:
        d = st.slider("d (shift)", -5.0, 5.0, 0.0, 0.1, key="sqrt_d")
        k = st.slider("k (vertical)", -5.0, 5.0, 0.0, 0.1, key="sqrt_k")

    if abs(c) < 0.001:
        st.error("c cannot be zero.")
    else:
        bound = -d / c
        if c > 0:
            x = np.linspace(max(bound, -10), 10, 500)
        else:
            x = np.linspace(-10, min(bound, 10), 500)

        arg = c * x + d
        arg_safe = np.where(arg < 0, 0, arg)
        y = a * np.sqrt(arg_safe) + k
        y = np.where(arg < 0, np.nan, y)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"{a}√({c}x+{d}) + {k}",
                                  line=dict(color="#f59e0b", width=2)))
        # Starting point marker
        start_y = k
        fig.add_trace(go.Scatter(x=[bound], y=[start_y], mode="markers",
                                  marker=dict(size=8, color="#ef4444"),
                                  name=f"Start ({bound:.2f}, {start_y:.2f})"))
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
        fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                          yaxis_range=[-8, 8], hovermode="x")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f'<div class="result-box">'
            f'<strong>Domain:</strong> {{"x ≥ " if c > 0 else "x ≤ "}}{bound:.4f}<br>'
            f'<strong>Starting point:</strong> ({bound:.4f}, {k:.4f})<br>'
            f'<strong>y-intercept:</strong> f(0) = {a * math.sqrt(max(d, 0)) + k:.4f} (if 0 in domain)'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Rational Functions ───────────────────────────────────
elif topic == "Rational Functions":
    st.markdown("## Rational Functions")
    st.latex(r"f(x) = \frac{ax + b}{cx + d}")

    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("a (numerator)", -5.0, 5.0, 1.0, 0.1, key="rat_a")
        b = st.slider("b (numerator)", -5.0, 5.0, 0.0, 0.1, key="rat_b")
    with col2:
        c = st.slider("c (denominator)", -5.0, 5.0, 1.0, 0.1, key="rat_c")
        d = st.slider("d (denominator)", -5.0, 5.0, -2.0, 0.1, key="rat_d")

    if abs(c) < 0.001:
        st.error("c cannot be zero (denominator must depend on x).")
    else:
        x = np.linspace(-10, 10, 2000)
        denom = c * x + d
        y = (a * x + b) / denom
        y = np.where(np.abs(denom) < 0.005, np.nan, y)
        y = np.where(np.abs(y) > 50, np.nan, y)

        # Asymptotes
        va_x = -d / c  # vertical asymptote
        ha_y = a / c   # horizontal asymptote

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines",
                                  name=f"({a}x+{b})/({c}x+{d})",
                                  line=dict(color="#ec4899", width=2)))
        # Vertical asymptote
        fig.add_vline(x=va_x, line=dict(color="#ef4444", width=1, dash="dash"),
                      annotation_text=f"x = {va_x:.2f}", annotation_position="top")
        # Horizontal asymptote
        fig.add_hline(y=ha_y, line=dict(color="#ef4444", width=1, dash="dash"),
                      annotation_text=f"y = {ha_y:.2f}", annotation_position="right")
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
        fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                          yaxis_range=[-10, 10], hovermode="x")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f'<div class="result-box">'
            f'<strong>Vertical asymptote:</strong> x = {va_x:.4f}<br>'
            f'<strong>Horizontal asymptote:</strong> y = {ha_y:.4f}<br>'
            f'<strong>x-intercept:</strong> ({-b/a:.4f}, 0){"" if abs(a) > 0.001 else " (none)"}<br>'
            f'<strong>y-intercept:</strong> (0, {b/d:.4f}){"" if abs(d) > 0.001 else " (none)"}'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Piecewise Functions ───────────────────────────────────
elif topic == "Piecewise Functions":
    st.markdown("## Piecewise Functions")
    st.markdown("Define up to 3 function pieces, each over an interval.")

    pieces = st.slider("Number of pieces", 1, 3, 2, key="pw_n")

    # Collect segments
    seg_colors = ["#6366f1", "#10b981", "#f59e0b"]
    seg_names = ["f₁(x)", "f₂(x)", "f₃(x)"]
    fig = go.Figure()
    x_full = np.linspace(-10, 10, 2000)

    for i in range(pieces):
        st.markdown(f"**Piece {i+1}**")
        col1, col2, col3 = st.columns([2, 2, 3])
        with col1:
            fn_type = st.selectbox(
                "Function",
                ["constant", "linear", "quadratic", "sin", "cos", "sqrt", "abs"],
                key=f"pw_fn_{i}",
            )
        with col2:
            if fn_type == "constant":
                p1 = st.number_input("c", 0.0, key=f"pw_p1_{i}")
                def fn(x, p1=p1): return np.full_like(x, p1, dtype=float)
                label = f"{p1:.1f}"
            elif fn_type == "linear":
                p1 = st.number_input("m", 1.0, key=f"pw_p1_{i}")
                p2 = st.number_input("c", 0.0, key=f"pw_p2_{i}")
                def fn(x, p1=p1, p2=p2): return p1 * x + p2
                label = f"{p1}x + {p2}"
            elif fn_type == "quadratic":
                p1 = st.number_input("a", 1.0, key=f"pw_p1_{i}")
                p2 = st.number_input("b", 0.0, key=f"pw_p2_{i}")
                p3 = st.number_input("c", 0.0, key=f"pw_p3_{i}")
                def fn(x, p1=p1, p2=p2, p3=p3): return p1 * x**2 + p2 * x + p3
                label = f"{p1}x²+{p2}x+{p3}"
            elif fn_type == "sin":
                p1 = st.number_input("amp", 1.0, key=f"pw_p1_{i}")
                p2 = st.number_input("freq", 1.0, key=f"pw_p2_{i}")
                def fn(x, p1=p1, p2=p2): return p1 * np.sin(p2 * x)
                label = f"{p1}sin({p2}x)"
            elif fn_type == "cos":
                p1 = st.number_input("amp", 1.0, key=f"pw_p1_{i}")
                p2 = st.number_input("freq", 1.0, key=f"pw_p2_{i}")
                def fn(x, p1=p1, p2=p2): return p1 * np.cos(p2 * x)
                label = f"{p1}cos({p2}x)"
            elif fn_type == "sqrt":
                p1 = st.number_input("amp", 1.0, key=f"pw_p1_{i}")
                p2 = st.number_input("shift x", 0.0, key=f"pw_p2_{i}")
                def fn(x, p1=p1, p2=p2): return p1 * np.sqrt(np.where(x - p2 >= 0, x - p2, 0))
                label = f"{p1}√(x-{p2})"
            elif fn_type == "abs":
                p1 = st.number_input("amp", 1.0, key=f"fw_p1_{i}")
                p2 = st.number_input("shift", 0.0, key=f"fw_p2_{i}")
                def fn(x, p1=p1, p2=p2): return p1 * np.abs(x - p2)
                label = f"{p1}|x-{p2}|"

        with col3:
            lo = st.number_input("From x =", -10.0, 10.0, -5.0 + i * 5, key=f"pw_lo_{i}")
            hi = st.number_input("To x =", -10.0, 10.0, 0.0 + i * 5, key=f"pw_hi_{i}")

        mask = (x_full >= lo) & (x_full <= hi)
        y_piece = fn(x_full)
        y_piece = np.where(mask, y_piece, np.nan)
        # Clamp extremes
        y_piece = np.where(np.abs(y_piece) > 50, np.nan, y_piece)

        fig.add_trace(go.Scatter(
            x=x_full, y=y_piece, mode="lines",
            name=f"{seg_names[i]}: {label}  [{lo}, {hi}]",
            line=dict(color=seg_colors[i], width=3),
        ))
        # Boundary markers (filled dot at left, open at right)
        y_lo = fn(np.array([lo]))[0]
        y_hi = fn(np.array([hi]))[0]
        fig.add_trace(go.Scatter(x=[lo], y=[y_lo], mode="markers",
                                  marker=dict(size=8, color=seg_colors[i]),
                                  showlegend=False))
        fig.add_trace(go.Scatter(x=[hi], y=[y_hi], mode="markers",
                                  marker=dict(size=8, color=seg_colors[i],
                                              symbol="circle-open"),
                                  showlegend=False))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=450, margin=dict(l=20, r=20, t=20, b=20),
                      yaxis_range=[-8, 8], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

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
    func = st.selectbox("Function", ["sin(x)", "cos(x)", "tan(x)", "sec(x)", "cosec(x)", "cot(x)", "sin(x) & cos(x)", "sec(x) & cosec(x)"])
    amp = st.slider("Amplitude", 0.1, 5.0, 1.0, 0.1)
    freq = st.slider("Frequency", 0.1, 5.0, 1.0, 0.1)
    phase = st.slider("Phase shift", 0.0, 6.28, 0.0, 0.01)

    x = np.linspace(-2*np.pi, 2*np.pi, 600)
    x_range = (-2*np.pi, 2*np.pi)
    fig = go.Figure()

    def add_fn(fn_name, y_fn, color, dash="solid"):
        y = amp * y_fn(freq * x + phase)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"{amp}{fn_name}({freq}x+{phase:.2f})",
                                  line=dict(color=color, width=2, dash=dash)))

    def add_asymptotes(where_cos_zero):
        """Draw dashed vertical lines at asymptote positions.
        where_cos_zero=True → asymptotes at cos=0 (π/2+nπ)
        where_cos_zero=False → asymptotes at sin=0 (nπ)"""
        x_min, x_max = x_range
        if where_cos_zero:
            base = math.pi / 2
        else:
            base = 0.0
        # asymptotes where freq*x + phase = base + n*pi
        n_min = math.ceil((freq * x_min + phase - base) / math.pi)
        n_max = math.floor((freq * x_max + phase - base) / math.pi)
        for n in range(int(n_min), int(n_max) + 1):
            x_a = (base + n * math.pi - phase) / freq
            fig.add_vline(x=x_a, line=dict(color="rgba(150,150,150,0.4)", width=1, dash="dash"),
                          showlegend=False)

    if func == "sin(x)":
        add_fn("sin", np.sin, "#6366f1")
    elif func == "cos(x)":
        add_fn("cos", np.cos, "#10b981")
    elif func == "tan(x)":
        y = amp * np.tan(freq * x + phase)
        y = np.where(np.abs(y) > 10, np.nan, y)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="tan(x)",
                                  line=dict(color="#f59e0b", width=2)))
        add_asymptotes(where_cos_zero=True)
    elif func == "sec(x)":
        cos_val = np.cos(freq * x + phase)
        y = amp / cos_val
        y = np.where(np.abs(cos_val) < 0.005, np.nan, y)
        y = np.where(np.abs(y) > 10, np.nan, y)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="sec(x)",
                                  line=dict(color="#a855f7", width=2)))
        add_asymptotes(where_cos_zero=True)
    elif func == "cosec(x)":
        sin_val = np.sin(freq * x + phase)
        y = amp / sin_val
        y = np.where(np.abs(sin_val) < 0.005, np.nan, y)
        y = np.where(np.abs(y) > 10, np.nan, y)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="cosec(x)",
                                  line=dict(color="#ec4899", width=2)))
        add_asymptotes(where_cos_zero=False)
    elif func == "cot(x)":
        sin_val = np.sin(freq * x + phase)
        cos_val = np.cos(freq * x + phase)
        y = amp * cos_val / sin_val
        y = np.where(np.abs(sin_val) < 0.005, np.nan, y)
        y = np.where(np.abs(y) > 10, np.nan, y)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="cot(x)",
                                  line=dict(color="#06b6d4", width=2)))
        add_asymptotes(where_cos_zero=False)
    elif func == "sec(x) & cosec(x)":
        cos_val = np.cos(freq * x + phase)
        sin_val = np.sin(freq * x + phase)
        y_sec = amp / cos_val
        y_csc = amp / sin_val
        y_sec = np.where((np.abs(cos_val) < 0.005) | (np.abs(y_sec) > 10), np.nan, y_sec)
        y_csc = np.where((np.abs(sin_val) < 0.005) | (np.abs(y_csc) > 10), np.nan, y_csc)
        fig.add_trace(go.Scatter(x=x, y=y_sec, mode="lines", name="sec(x)",
                                  line=dict(color="#a855f7", width=2)))
        fig.add_trace(go.Scatter(x=x, y=y_csc, mode="lines", name="cosec(x)",
                                  line=dict(color="#ec4899", width=2)))
        add_asymptotes(where_cos_zero=True)
        add_asymptotes(where_cos_zero=False)
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
    st.markdown("## Shortest Distance — Vector Projection")
    st.markdown(
        "All distances computed by **projecting** AP onto a direction vector, "
        "then taking the perpendicular component."
    )

    dist_mode = st.radio("Mode", [
        "Point → Line (2D)",
        "Point → Line (3D)",
        "Point → Plane",
    ], horizontal=True)

    # ── Point → Line (2D) with Vector Projection ──────────────
    if dist_mode == "Point → Line (2D)":
        st.markdown("### Point to Line (2D) — Vector Projection")
        st.latex(r"\text{proj}_{\vec{d}}(\vec{AP}) = "
                 r"\frac{\vec{AP} \cdot \vec{d}}{|\vec{d}|^2}\,\vec{d}")
        st.latex(r"d = |\vec{AP} - \text{proj}_{\vec{d}}(\vec{AP})|")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Line: point A + direction d**")
            ax = st.slider("Aₓ", -8.0, 8.0, -2.0, 0.1, key="l2_ax")
            ay = st.slider("Aᵧ", -8.0, 8.0, 1.0, 0.1, key="l2_ay")
            dx = st.slider("dₓ", -5.0, 5.0, 3.0, 0.1, key="l2_dx")
            dy = st.slider("dᵧ", -5.0, 5.0, 1.0, 0.1, key="l2_dy")
        with col2:
            st.markdown("**Point P**")
            px = st.slider("Pₓ", -8.0, 8.0, 4.0, 0.1, key="l2_px")
            py = st.slider("Pᵧ", -8.0, 8.0, 5.0, 0.1, key="l2_py")

        # Vector AP
        apx, apy = px - ax, py - ay
        mag_d_sq = dx**2 + dy**2

        if mag_d_sq < 1e-12:
            st.error("Direction vector d cannot be zero.")
        else:
            # Scalar projection (t) of AP onto d
            t_scalar = (apx * dx + apy * dy) / mag_d_sq
            # Parallel component = projection onto line
            par_x = t_scalar * dx
            par_y = t_scalar * dy
            # Foot = A + parallel component
            fx, fy = ax + par_x, ay + par_y
            # Perpendicular component
            perp_x = apx - par_x
            perp_y = apy - par_y
            dist = math.sqrt(perp_x**2 + perp_y**2)

            st.success(f"**Shortest distance d = {dist:.6f}**")

            # Visualization
            t_vis = np.linspace(-10, 10, 400)
            line_x = ax + t_vis * dx
            line_y = ay + t_vis * dy

            fig = go.Figure()
            # The line
            fig.add_trace(go.Scatter(
                x=line_x, y=line_y, mode="lines",
                line=dict(color="#6366f1", width=2),
                name="Line",
            ))
            # Vector AP (from A to P)
            fig.add_trace(go.Scatter(
                x=[ax, px], y=[ay, py], mode="lines",
                line=dict(color="#8b5cf6", width=2, dash="dot"),
                name="AP",
            ))
            # Parallel component (along line: A→Foot)
            fig.add_trace(go.Scatter(
                x=[ax, fx], y=[ay, fy], mode="lines+markers",
                line=dict(color="#10b981", width=3),
                marker=dict(size=[0, 8], color="#10b981"),
                name=f"proj = ({par_x:.2f}, {par_y:.2f})",
            ))
            # Point P
            fig.add_trace(go.Scatter(
                x=[px], y=[py], mode="markers",
                marker=dict(size=10, color="#ef4444", symbol="x"),
                name=f"P({px:.1f}, {py:.1f})",
            ))
            # Point A
            fig.add_trace(go.Scatter(
                x=[ax], y=[ay], mode="markers",
                marker=dict(size=8, color="#f59e0b"),
                name=f"A({ax:.1f}, {ay:.1f})",
            ))
            # Perpendicular (from P to foot)
            fig.add_trace(go.Scatter(
                x=[px, fx], y=[py, fy], mode="lines",
                line=dict(color="#ef4444", width=2, dash="dash"),
                name=f"⟂ d = {dist:.4f}",
            ))
            # Foot
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
                f'<strong>1.</strong> AP = P − A = ({apx:.2f}, {apy:.2f})<br>'
                f'<strong>2.</strong> Scalar projection: t = (AP·d) / |d|² = {apx*dx+apy*dy:.4f} / {mag_d_sq:.4f} = {t_scalar:.4f}<br>'
                f'<strong>3.</strong> Parallel (along line): t·d = ({par_x:.4f}, {par_y:.4f})<br>'
                f'<strong>4.</strong> Foot = A + parallel = ({fx:.4f}, {fy:.4f})<br>'
                f'<strong>5.</strong> Perpendicular = AP − parallel = ({perp_x:.4f}, {perp_y:.4f})<br>'
                f'<strong>6.</strong> Distance = |⟂| = √({perp_x**2:.4f} + {perp_y**2:.4f}) = <strong>{dist:.6f}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Point → Line (3D) with Vector Projection ──────────────
    elif dist_mode == "Point → Line (3D)":
        st.markdown("### Point to Line (3D) — Vector Projection")
        st.latex(r"d = |\vec{AP} - \text{proj}_{\vec{d}}(\vec{AP})|")

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

        mag_d_sq = dx**2 + dy**2 + dz**2
        if mag_d_sq < 1e-12:
            st.error("Direction vector d cannot be zero.")
        else:
            # AP
            apx, apy, apz = px - a0, py - a1, pz - a2
            # Scalar projection
            t_scalar = (apx * dx + apy * dy + apz * dz) / mag_d_sq
            # Parallel = projection onto line
            par_x, par_y, par_z = t_scalar * dx, t_scalar * dy, t_scalar * dz
            # Foot
            fx, fy, fz = a0 + par_x, a1 + par_y, a2 + par_z
            # Perpendicular
            perp_x, perp_y, perp_z = apx - par_x, apy - par_y, apz - par_z
            dist = math.sqrt(perp_x**2 + perp_y**2 + perp_z**2)

            st.success(f"**Shortest distance d = {dist:.6f}**")

            t_vis = np.linspace(-5, 5, 100)
            fig = go.Figure()
            # Line
            fig.add_trace(go.Scatter3d(
                x=[a0 + ti * dx for ti in t_vis],
                y=[a1 + ti * dy for ti in t_vis],
                z=[a2 + ti * dz for ti in t_vis],
                mode="lines", line=dict(color="#6366f1", width=4),
                name="Line",
            ))
            # AP (from A to P)
            fig.add_trace(go.Scatter3d(
                x=[a0, px], y=[a1, py], z=[a2, pz],
                mode="lines", line=dict(color="#8b5cf6", width=2, dash="dot"),
                name="AP",
            ))
            # Parallel (A → Foot)
            fig.add_trace(go.Scatter3d(
                x=[a0, fx], y=[a1, fy], z=[a2, fz],
                mode="lines+markers",
                line=dict(color="#10b981", width=3),
                marker=dict(size=[0, 6], color="#10b981"),
                name=f"proj = ({par_x:.2f}, {par_y:.2f}, {par_z:.2f})",
            ))
            # Point P
            fig.add_trace(go.Scatter3d(
                x=[px], y=[py], z=[pz],
                mode="markers", marker=dict(size=8, color="#ef4444"),
                name=f"P({px:.1f}, {py:.1f}, {pz:.1f})",
            ))
            # Perpendicular (P → Foot)
            fig.add_trace(go.Scatter3d(
                x=[px, fx], y=[py, fy], z=[pz, fz],
                mode="lines", line=dict(color="#ef4444", width=3, dash="dash"),
                name=f"⟂ d = {dist:.4f}",
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
                mode="markers", marker=dict(size=5, color="#f59e0b"),
                name="A",
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
            st.caption("🖱️ Drag to rotate · Green = projection · Red dashed = ⟂ distance")

            st.markdown(
                f'<div class="result-box">'
                f'<strong>1.</strong> AP = ({apx:.2f}, {apy:.2f}, {apz:.2f})<br>'
                f'<strong>2.</strong> Scalar proj: t = (AP·d)/|d|² = {apx*dx+apy*dy+apz*dz:.4f}/{mag_d_sq:.4f} = {t_scalar:.4f}<br>'
                f'<strong>3.</strong> Parallel: t·d = ({par_x:.4f}, {par_y:.4f}, {par_z:.4f})<br>'
                f'<strong>4.</strong> Foot = A + parallel = ({fx:.4f}, {fy:.4f}, {fz:.4f})<br>'
                f'<strong>5.</strong> ⟂ = AP − parallel = ({perp_x:.4f}, {perp_y:.4f}, {perp_z:.4f})<br>'
                f'<strong>6.</strong> d = |⟂| = <strong>{dist:.6f}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Point → Plane with Vector Projection ──────────────────
    elif dist_mode == "Point → Plane":
        st.markdown("### Point to Plane — Normal Projection")
        st.latex(r"d = |\vec{AP} \cdot \hat{n}|  \quad  \hat{n} = \frac{\vec{n}}{|\vec{n}|}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Plane: point A + normal n**")
            ap0 = st.slider("Aₓ", -5.0, 5.0, 0.0, 0.1, key="dp_a0")
            ap1 = st.slider("Aᵧ", -5.0, 5.0, 0.0, 0.1, key="dp_a1")
            ap2 = st.slider("A_z", -5.0, 5.0, 0.0, 0.1, key="dp_a2")
            nx = st.slider("nₓ", -5.0, 5.0, 1.0, 0.1, key="dp_nx")
            ny = st.slider("nᵧ", -5.0, 5.0, 2.0, 0.1, key="dp_ny")
            nz = st.slider("n_z", -5.0, 5.0, 2.0, 0.1, key="dp_nz")
        with col2:
            st.markdown("**Point P**")
            px = st.slider("Pₓ", -5.0, 5.0, 3.0, 0.1, key="dp_px")
            py = st.slider("Pᵧ", -5.0, 5.0, 1.0, 0.1, key="dp_py")
            pz = st.slider("P_z", -5.0, 5.0, -2.0, 0.1, key="dp_pz")

        mag_n = math.sqrt(nx**2 + ny**2 + nz**2)
        if mag_n < 1e-12:
            st.error("Normal vector cannot be zero.")
        else:
            # Unit normal
            nx_hat, ny_hat, nz_hat = nx / mag_n, ny / mag_n, nz / mag_n
            # AP
            apx, apy, apz = px - ap0, py - ap1, pz - ap2
            # Scalar projection of AP onto n̂
            dist = abs(apx * nx_hat + apy * ny_hat + apz * nz_hat)
            # Foot = P - (AP·n̂) * n̂
            proj = apx * nx_hat + apy * ny_hat + apz * nz_hat
            fx = px - proj * nx_hat
            fy = py - proj * ny_hat
            fz = pz - proj * nz_hat

            st.success(f"**Shortest distance d = {dist:.6f}**")

            # Plane surface for visualization
            grid = np.linspace(-6, 6, 20)
            if abs(nz) > 0.001:
                xx, yy = np.meshgrid(grid, grid)
                # plane: nx(x-ap0) + ny(y-ap1) + nz(z-ap2) = 0
                zz = (-nx * (xx - ap0) - ny * (yy - ap1)) / nz + ap2
            elif abs(ny) > 0.001:
                xx, zz = np.meshgrid(grid, grid)
                yy = (-nx * (xx - ap0) - nz * (zz - ap2)) / ny + ap1
            else:
                yy, zz = np.meshgrid(grid, grid)
                xx = (-ny * (yy - ap1) - nz * (zz - ap2)) / nx + ap0

            fig = go.Figure()
            # Plane
            fig.add_trace(go.Surface(
                x=xx, y=yy, z=zz,
                colorscale=[[0, "#6366f1"], [1, "#6366f1"]],
                opacity=0.25, showscale=False, name="Plane",
            ))
            # Normal from A
            fig.add_trace(go.Scatter3d(
                x=[ap0, ap0 + nx], y=[ap1, ap1 + ny], z=[ap2, ap2 + nz],
                mode="lines+markers",
                line=dict(color="#8b5cf6", width=3, dash="dash"),
                marker=dict(size=[0, 6], color="#8b5cf6"),
                name=f"n = ({nx:.1f}, {ny:.1f}, {nz:.1f})",
            ))
            # AP (from A to P)
            fig.add_trace(go.Scatter3d(
                x=[ap0, px], y=[ap1, py], z=[ap2, pz],
                mode="lines", line=dict(color="#8b5cf6", width=2, dash="dot"),
                name="AP",
            ))
            # Point P
            fig.add_trace(go.Scatter3d(
                x=[px], y=[py], z=[pz],
                mode="markers", marker=dict(size=8, color="#ef4444"),
                name=f"P({px:.1f}, {py:.1f}, {pz:.1f})",
            ))
            # Point A on plane
            fig.add_trace(go.Scatter3d(
                x=[ap0], y=[ap1], z=[ap2],
                mode="markers", marker=dict(size=6, color="#f59e0b"),
                name="A (on plane)",
            ))
            # Perpendicular (P → Foot)
            fig.add_trace(go.Scatter3d(
                x=[px, fx], y=[py, fy], z=[pz, fz],
                mode="lines", line=dict(color="#ef4444", width=3, dash="dash"),
                name=f"d = {dist:.4f}",
            ))
            # Foot
            fig.add_trace(go.Scatter3d(
                x=[fx], y=[fy], z=[fz],
                mode="markers", marker=dict(size=6, color="#10b981"),
                name=f"Foot({fx:.3f}, {fy:.3f}, {fz:.3f})",
            ))

            fig.update_layout(
                height=500,
                scene=dict(
                    xaxis=dict(range=[-7, 7], title="x"),
                    yaxis=dict(range=[-7, 7], title="y"),
                    zaxis=dict(range=[-7, 7], title="z"),
                    bgcolor="rgba(0,0,0,0)",
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🖱️ Drag to rotate · Purple dashed = normal n · Red dashed = ⟂ distance")

            st.markdown(
                f'<div class="result-box">'
                f'<strong>1.</strong> AP = P − A = ({apx:.2f}, {apy:.2f}, {apz:.2f})<br>'
                f'<strong>2.</strong> Unit normal: n̂ = ({nx_hat:.4f}, {ny_hat:.4f}, {nz_hat:.4f})<br>'
                f'<strong>3.</strong> Project AP onto n̂: AP·n̂ = {apx*nx_hat+apy*ny_hat+apz*nz_hat:.4f}<br>'
                f'<strong>4.</strong> Distance = |AP·n̂| = <strong>{dist:.6f}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ── Plane Vectors ────────────────────────────────────────
elif topic == "Plane Vectors":
    st.markdown("## Plane Vectors")

    plane_mode = st.radio("Mode", [
        "Cartesian: ax + by + cz + d = 0",
        "Vector: r = a + λb + μc",
    ], horizontal=True)

    if plane_mode == "Cartesian: ax + by + cz + d = 0":
        st.markdown("### Plane: ax + by + cz + d = 0")
        st.markdown("Set the plane coefficients. The **normal vector** n = (a, b, c) is always ⟂ to the plane.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Coefficients**")
            a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="pv_a")
            b = st.slider("b", -5.0, 5.0, 2.0, 0.1, key="pv_b")
            c = st.slider("c", -5.0, 5.0, 1.0, 0.1, key="pv_c")
            d = st.slider("d", -10.0, 10.0, 0.0, 0.1, key="pv_d")
        with col2:
            st.markdown("**Normal vector**")
            st.markdown(f'n = (**{a:.2f}**, **{b:.2f}**, **{c:.2f}**)')
            st.markdown(f'|n| = {math.sqrt(a**2 + b**2 + c**2):.4f}')
            st.markdown("\n\n")
            st.info("The normal is derived from a, b, c — always ⟂ to the plane.")

        mag_n = math.sqrt(a**2 + b**2 + c**2)
        if mag_n < 0.001:
            st.error("Invalid plane: a = b = c = 0")
        else:
            # Unit normal
            nx, ny, nz = a / mag_n, b / mag_n, c / mag_n

            # Find a point on the plane for surface rendering
            # Solve for the best axis to parameterize
            # Find center-ish point on plane
            t_pt = 0
            if abs(c) > 0.001:
                # Use center of grid: solve ax+by+cz+d=0 at (0, 0)
                center_z = -d / c
                center_x, center_y = 0, 0
            elif abs(b) > 0.001:
                center_y = -d / b
                center_x, center_z = 0, 0
            elif abs(a) > 0.001:
                center_x = -d / a
                center_y, center_z = 0, 0
            else:
                center_x = center_y = center_z = 0

            # Build surface mesh
            grid = np.linspace(-6, 6, 25)
            if abs(c) > 0.001:  # z depends on x, y
                xx, yy = np.meshgrid(grid, grid)
                zz = (-a * xx - b * yy - d) / c
            elif abs(b) > 0.001:  # y depends on x, z
                xx, zz = np.meshgrid(grid, grid)
                yy = (-a * xx - c * zz - d) / b
            elif abs(a) > 0.001:  # x depends on y, z
                yy, zz = np.meshgrid(grid, grid)
                xx = (-b * yy - c * zz - d) / a
            else:
                xx = yy = zz = np.zeros((25, 25))

            # Normal line extending through plane in both directions (length 4 units)
            norm_len = 4.0
            # Start on one side, go through center, end on other side
            n_start = -norm_len
            n_end = norm_len

            fig = go.Figure()
            # Plane surface
            fig.add_trace(go.Surface(
                x=xx, y=yy, z=zz,
                colorscale=[[0, "#6366f1"], [1, "#6366f1"]],
                opacity=0.25, showscale=False,
                name=f"{a}x + {b}y + {c}z + {d} = 0",
            ))
            # Normal line through plane (both directions)
            fig.add_trace(go.Scatter3d(
                x=[center_x + n_start * nx, center_x + n_end * nx],
                y=[center_y + n_start * ny, center_y + n_end * ny],
                z=[center_z + n_start * nz, center_z + n_end * nz],
                mode="lines",
                line=dict(color="#ef4444", width=4),
                name=f"n = ({a:.2f}, {b:.2f}, {c:.2f})",
            ))
            # Center point (intersection of normal with plane)
            fig.add_trace(go.Scatter3d(
                x=[center_x], y=[center_y], z=[center_z],
                mode="markers",
                marker=dict(size=6, color="#f59e0b"),
                name="Plane center",
            ))
            # Right-angle indicator: small square at the intersection
            # Small offset along plane tangent
            tick = 0.3
            if abs(c) > 0.001:
                tan1 = np.array([1, 0, -a / c])
                if abs(b) > 0.001:
                    tan2 = np.array([0, 1, -b / c])
                else:
                    tan2 = np.array([0, 0, 1])
            elif abs(b) > 0.001:
                tan1 = np.array([1, -a / b, 0])
                tan2 = np.array([0, -c / b, 1])
            else:
                tan1 = np.array([0, 1, 0])
                tan2 = np.array([-b / a, 0, 1])
            # Normalize tangents
            t1 = tan1 / np.linalg.norm(tan1) * tick
            t2 = tan2 / np.linalg.norm(tan2) * tick
            # Draw a small right-angle indicator
            fig.add_trace(go.Scatter3d(
                x=[center_x + t1[0], center_x + t1[0] + t2[0], center_x + t2[0]],
                y=[center_y + t1[1], center_y + t1[1] + t2[1], center_y + t2[1]],
                z=[center_z + t1[2], center_z + t1[2] + t2[2], center_z + t2[2]],
                mode="lines",
                line=dict(color="white", width=2),
                showlegend=False,
            ))
            # Arrow head at both ends of normal
            fig.add_trace(go.Cone(
                x=[center_x + (norm_len - 0.4) * nx],
                y=[center_y + (norm_len - 0.4) * ny],
                z=[center_z + (norm_len - 0.4) * nz],
                u=[nx], v=[ny], w=[nz],
                sizemode="absolute", sizeref=0.3,
                colorscale=[[0, "#ef4444"], [1, "#ef4444"]],
                showscale=False,
                name="n",
            ))
            fig.add_trace(go.Cone(
                x=[center_x + (-norm_len + 0.4) * nx],
                y=[center_y + (-norm_len + 0.4) * ny],
                z=[center_z + (-norm_len + 0.4) * nz],
                u=[-nx], v=[-ny], w=[-nz],
                sizemode="absolute", sizeref=0.3,
                colorscale=[[0, "#ef4444"], [1, "#ef4444"]],
                showscale=False,
                name="−n",
            ))

            fig.update_layout(
                height=500,
                scene=dict(
                    xaxis=dict(range=[-7, 7], title="x"),
                    yaxis=dict(range=[-7, 7], title="y"),
                    zaxis=dict(range=[-7, 7], title="z"),
                    bgcolor="rgba(0,0,0,0)",
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🖱️ Drag to rotate · Red line = normal n ⟂ plane · White ∟ = right-angle marker")

            st.markdown(
                f'<div class="result-box">'
                f'<strong>Plane:</strong> {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0<br>'
                f'<strong>Normal:</strong> n = ({a:.2f}, {b:.2f}, {c:.2f}) &nbsp;|&nbsp; '
                f'<strong>Unit normal:</strong> n̂ = ({nx:.4f}, {ny:.4f}, {nz:.4f})<br>'
                f'<strong>Verify:</strong> n · (x − x₀, y − y₀, z − z₀) = 0 for any (x,y,z) on the plane'
                f'</div>',
                unsafe_allow_html=True,
            )

    else:
        st.markdown("### Vector Equation: r = a + λb + μc")
        st.markdown("Define a plane by a point **a** and two direction vectors **b** and **c**. "
                    "The **normal** n = b × c is always ⟂ to both b and c.")

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

        # Normal = b × c
        n_cx = b1 * c2 - b2 * c1
        n_cy = b2 * c0 - b0 * c2
        n_cz = b0 * c1 - b1 * c0
        mag_n = math.sqrt(n_cx**2 + n_cy**2 + n_cz**2)
        nn_x, nn_y, nn_z = n_cx / mag_n, n_cy / mag_n, n_cz / mag_n

        if mag_n < 0.001:
            st.error("b and c are parallel (b×c = 0). They don't form a plane.")
        else:
            # Generate surface
            ll, mm = np.meshgrid(np.linspace(-2.5, 2.5, 20), np.linspace(-2.5, 2.5, 20))
            surf_x = a0 + ll * b0 + mm * c0
            surf_y = a1 + ll * b1 + mm * c1
            surf_z = a2 + ll * b2 + mm * c2

            norm_len = 4.0

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
                mode="markers", marker=dict(size=6, color="#f59e0b"),
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
                line=dict(color="#22c55e", width=4),
                marker=dict(size=[0, 6], color="#22c55e"),
                name=f"c = ({c0:.1f}, {c1:.1f}, {c2:.1f})",
            ))
            # Normal b×c through the plane (both directions)
            fig.add_trace(go.Scatter3d(
                x=[a0 - norm_len * nn_x, a0 + norm_len * nn_x],
                y=[a1 - norm_len * nn_y, a1 + norm_len * nn_y],
                z=[a2 - norm_len * nn_z, a2 + norm_len * nn_z],
                mode="lines+markers",
                line=dict(color="#ef4444", width=4),
                marker=dict(size=6, color="#ef4444"),
                name=f"n = b×c = ({n_cx:.2f}, {n_cy:.2f}, {n_cz:.2f})",
            ))

            fig.update_layout(
                height=500,
                scene=dict(
                    xaxis=dict(range=[-7, 7], title="x"),
                    yaxis=dict(range=[-7, 7], title="y"),
                    zaxis=dict(range=[-7, 7], title="z"),
                    bgcolor="rgba(0,0,0,0)",
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🖱️ Drag to rotate · Green= b · Light green= c · Red= n=b×c ⟂ to both")

            st.markdown(
                f'<div class="result-box">'
                f'<strong>Normal:</strong> n = b × c = ({b0:.1f}, {b1:.1f}, {b2:.1f}) × ({c0:.1f}, {c1:.1f}, {c2:.1f})<br>'
                f'= ({n_cx:.3f}, {n_cy:.3f}, {n_cz:.3f})<br>'
                f'<strong>Check:</strong> n · b = {n_cx*b0 + n_cy*b1 + n_cz*b2:.6f} (should be 0) &nbsp;|&nbsp; '
                f'n · c = {n_cx*c0 + n_cy*c1 + n_cz*c2:.6f} (should be 0)'
                f'</div>',
                unsafe_allow_html=True,
            )

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

# ================================================================
#                     🔄 TRANSFORMATIONS
# ================================================================
elif topic == "Reflection":
    st.markdown("## Reflection")
    st.latex(r"(x, y) \to (x, -y) \quad\text{(x-axis)}\qquad (x, y) \to (-x, y) \quad\text{(y-axis)}")
    st.latex(r"(x, y) \to (y, x) \quad\text{(y=x)}\qquad (x, y) \to (-y, -x) \quad\text{(y=-x)}")

    target = st.radio("Target", ["Point", "Linear Function", "Quadratic Function"], horizontal=True, key="ref_target")
    axis = st.selectbox("Axis", ["x-axis (y → -y)", "y-axis (x → -x)", "y = x", "y = -x"], key="ref_axis")

    ax_map = {"x-axis (y → -y)": (1, -1), "y-axis (x → -x)": (-1, 1), "y = x": None, "y = -x": None}
    fig = go.Figure()
    colors = {"original": "#6366f1", "transformed": "#ef4444"}

    if target == "Point":
        px = st.slider("Point x", -8.0, 8.0, 3.0, 0.1, key="ref_px")
        py = st.slider("Point y", -8.0, 8.0, 2.0, 0.1, key="ref_py")
        if axis == "x-axis (y → -y)": rx, ry = px, -py
        elif axis == "y-axis (x → -x)": rx, ry = -px, py
        elif axis == "y = x": rx, ry = py, px
        else: rx, ry = -py, -px
        fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=12, color=colors["original"]), name=f"P({px:.1f},{py:.1f})"))
        fig.add_trace(go.Scatter(x=[rx], y=[ry], mode="markers", marker=dict(size=12, color=colors["transformed"], symbol="x"), name=f"P'({rx:.1f},{ry:.1f})"))
        fig.add_trace(go.Scatter(x=[px, rx], y=[py, ry], mode="lines", line=dict(color="#f59e0b", width=1, dash="dot"), showlegend=False))

    x = np.linspace(-10, 10, 400)
    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="ref_m")
        c = st.slider("Intercept c", -10.0, 10.0, 1.0, 0.1, key="ref_c")
        y_orig = m * x + c
        if axis == "x-axis (y → -y)": y_trans = -m * x - c
        elif axis == "y-axis (x → -x)": y_trans = -m * x + c
        elif axis == "y = x": y_trans = (x - c) / m if abs(m) > 0.01 else np.full_like(x, np.nan)
        else: y_trans = (-x - c) / m if abs(m) > 0.01 else np.full_like(x, np.nan)
        fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color=colors["original"], width=2), name=f"y={{{m}}}x+{{{c}}}"))
        fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color=colors["transformed"], width=2, dash="dash"), name="Reflected"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="ref_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="ref_b")
        c = st.slider("c", -10.0, 10.0, -2.0, 0.1, key="ref_c")
        y_orig = a * x**2 + b * x + c
        if axis == "x-axis (y → -y)": y_trans = -a * x**2 - b * x - c
        elif axis == "y-axis (x → -x)": y_trans = a * x**2 - b * x + c
        elif axis == "y = x":
            # Reflection about y=x: swap x and y → need to solve x = ay²+by+c for y
            y_trans = np.full_like(x, np.nan)
        else:
            y_trans = np.full_like(x, np.nan)
        fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color=colors["original"], width=2), name="Original"))
        fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color=colors["transformed"], width=2, dash="dash"), name="Reflected"))

    if axis in ("y = x", "y = -x"):
        fig.add_trace(go.Scatter(x=[-10, 10], y=[-10 if axis=="y = x" else 10, 10 if axis=="y = x" else -10], mode="lines", line=dict(color="#555", width=1, dash="dot"), name=axis))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(range=[-10,10], scaleanchor="y"), yaxis=dict(range=[-10,10]), hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Translation ──────────────────────────────────────────
elif topic == "Translation":
    st.markdown("## Translation")
    st.latex(r"(x, y) \to (x + a, y + b)")

    target = st.radio("Target", ["Point", "Linear Function", "Quadratic Function"], horizontal=True, key="tr_target")
    tx = st.slider("Translate x by", -5.0, 5.0, 2.0, 0.1, key="tr_tx")
    ty = st.slider("Translate y by", -5.0, 5.0, 1.0, 0.1, key="tr_ty")

    fig = go.Figure()
    x = np.linspace(-10, 10, 400)

    if target == "Point":
        px = st.slider("Point x", -8.0, 8.0, 1.0, 0.1, key="tr_px")
        py = st.slider("Point y", -8.0, 8.0, 2.0, 0.1, key="tr_py")
        rx, ry = px + tx, py + ty
        fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=12, color="#6366f1"), name=f"P({px:.1f},{py:.1f})"))
        fig.add_trace(go.Scatter(x=[rx], y=[ry], mode="markers", marker=dict(size=12, color="#ef4444", symbol="x"), name=f"P'({rx:.1f},{ry:.1f})"))
        fig.add_trace(go.Scatter(x=[px, rx], y=[py, ry], mode="lines", line=dict(color="#f59e0b", width=2), name=f"({tx},{ty})"))

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="tr_m")
        c = st.slider("Intercept c", -10.0, 10.0, 1.0, 0.1, key="tr_c")
        y_orig = m * x + c
        y_trans = m * (x - tx) + c + ty
        fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color="#6366f1", width=2), name=f"y={{{m}}}x+{{{c}}}"))
        fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="Translated"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="tr_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="tr_b")
        c = st.slider("c", -10.0, 10.0, -2.0, 0.1, key="tr_c")
        y_orig = a * x**2 + b * x + c
        y_trans = a * (x - tx)**2 + b * (x - tx) + c + ty
        fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color="#6366f1", width=2), name="Original"))
        fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="Translated"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[-10, 10], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Rotation ─────────────────────────────────────────────
elif topic == "Rotation":
    st.markdown("## Rotation")
    st.latex(r"(x, y) \to (x\cos\theta - y\sin\theta,\; x\sin\theta + y\cos\theta)")

    target = st.radio("Target", ["Point", "Linear Function", "Quadratic Function"], horizontal=True, key="rot_target")
    angle = st.slider("Angle (degrees)", -180, 180, 45, 1, key="rot_angle")
    rad = math.radians(angle)
    cth, sth = math.cos(rad), math.sin(rad)

    fig = go.Figure()
    x = np.linspace(-10, 10, 400)

    if target == "Point":
        px = st.slider("Point x", -8.0, 8.0, 3.0, 0.1, key="rot_px")
        py = st.slider("Point y", -8.0, 8.0, 2.0, 0.1, key="rot_py")
        rx = px * cth - py * sth
        ry = px * sth + py * cth
        fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=12, color="#6366f1"), name=f"P({px:.1f},{py:.1f})"))
        fig.add_trace(go.Scatter(x=[rx], y=[ry], mode="markers", marker=dict(size=12, color="#ef4444", symbol="x"), name=f"P'({rx:.1f},{ry:.1f})"))
        fig.add_trace(go.Scatter(x=[0, px], y=[0, py], mode="lines", line=dict(color="#6366f1", width=1, dash="dot"), showlegend=False))
        fig.add_trace(go.Scatter(x=[0, rx], y=[0, ry], mode="lines", line=dict(color="#ef4444", width=1, dash="dot"), showlegend=False))

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="rot_m")
        c = st.slider("Intercept c", -10.0, 10.0, 1.0, 0.1, key="rot_c")
        # Rotate line: transform two points and draw line between them
        pts_x = np.array([-10, 10])
        pts_y = m * pts_x + c
        rx_pts = pts_x * cth - pts_y * sth
        ry_pts = pts_x * sth + pts_y * cth
        fig.add_trace(go.Scatter(x=pts_x, y=pts_y, mode="lines", line=dict(color="#6366f1", width=2), name=f"y={{{m}}}x+{{{c}}}"))
        fig.add_trace(go.Scatter(x=rx_pts, y=ry_pts, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name=f"Rotated {angle}°"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="rot_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="rot_b")
        c = st.slider("c", -10.0, 10.0, -2.0, 0.1, key="rot_c")
        pts_x = x.copy()
        pts_y = a * pts_x**2 + b * pts_x + c
        rx_pts = pts_x * cth - pts_y * sth
        ry_pts = pts_x * sth + pts_y * cth
        fig.add_trace(go.Scatter(x=pts_x, y=pts_y, mode="lines", line=dict(color="#6366f1", width=2), name="Original"))
        fig.add_trace(go.Scatter(x=rx_pts, y=ry_pts, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name=f"Rotated {angle}°"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(range=[-10,10], scaleanchor="y"), yaxis=dict(range=[-10,10]), hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Enlargement (Dilation) ───────────────────────────────
elif topic == "Enlargement (Dilation)":
    st.markdown("## Enlargement / Dilation")
    st.latex(r"(x, y) \to (kx, ky) \quad\text{or}\quad f(x) \to k\cdot f(x)")

    target = st.radio("Target", ["Point", "Linear Function", "Quadratic Function"], horizontal=True, key="enl_target")
    scale = st.slider("Scale factor k", -3.0, 3.0, 2.0, 0.1, key="enl_scale")
    origin = st.checkbox("From origin (0,0)", value=True, key="enl_origin")

    fig = go.Figure()
    x = np.linspace(-10, 10, 400)
    colors = {"original": "#6366f1", "transformed": "#ef4444"}

    if target == "Point":
        px = st.slider("Point x", -8.0, 8.0, 2.0, 0.1, key="enl_px")
        py = st.slider("Point y", -8.0, 8.0, 3.0, 0.1, key="enl_py")
        rx, ry = px * scale, py * scale
        fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=12, color=colors["original"]), name=f"P({px:.1f},{py:.1f})"))
        fig.add_trace(go.Scatter(x=[rx], y=[ry], mode="markers", marker=dict(size=12, color=colors["transformed"], symbol="x"), name=f"P'({rx:.1f},{ry:.1f})"))
        fig.add_trace(go.Scatter(x=[0, rx], y=[0, ry], mode="lines", line=dict(color=colors["transformed"], width=1, dash="dot"), showlegend=False))

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="enl_m")
        c = st.slider("Intercept c", -10.0, 10.0, 1.0, 0.1, key="enl_c")
        y_orig = m * x + c
        # Scale about origin: multiply y by scale
        # If scaling about origin, the shape scales from (0,0)
        y_trans = scale * y_orig
        fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color=colors["original"], width=2), name=f"y={{{m}}}x+{{{c}}}"))
        fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color=colors["transformed"], width=2, dash="dash"), name=f"Scaled x{scale}"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="enl_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="enl_b")
        c = st.slider("c", -10.0, 10.0, -2.0, 0.1, key="enl_c")
        y_orig = a * x**2 + b * x + c
        y_trans = scale * y_orig
        fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color=colors["original"], width=2), name="Original"))
        fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color=colors["transformed"], width=2, dash="dash"), name=f"Scaled x{scale}"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[-12, 12], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Modulus |f(x)| ───────────────────────────────────────
elif topic == "Modulus |f(x)|":
    st.markdown("## Modulus |f(x)|")
    st.latex(r"|f(x)| = \begin{cases} f(x) & f(x) \ge 0 \\ -f(x) & f(x) < 0 \end{cases}")

    target = st.radio("Target", ["Linear Function", "Quadratic Function"], horizontal=True, key="mod_target")
    fig = go.Figure()
    x = np.linspace(-10, 10, 600)

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="mod_m")
        c = st.slider("Intercept c", -10.0, 10.0, 0.0, 0.1, key="mod_c")
        y = m * x + c
        y_mod = np.abs(y)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#6366f1", width=2), name=f"f(x)={{{m}}}x+{{{c}}}"))
        fig.add_trace(go.Scatter(x=x, y=y_mod, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="|f(x)|"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="mod_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="mod_b")
        c = st.slider("c", -10.0, 10.0, -4.0, 0.1, key="mod_c")
        y = a * x**2 + b * x + c
        y_mod = np.abs(y)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#6366f1", width=2), name="f(x)"))
        fig.add_trace(go.Scatter(x=x, y=y_mod, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="|f(x)|"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[-10, 12], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Inverse f⁻¹(x) ───────────────────────────────────────
elif topic == "Inverse f⁻¹(x)":
    st.markdown("## Inverse Function")
    st.latex(r"f^{-1}(f(x)) = x \qquad f(f^{-1}(x)) = x")
    st.latex(r"\text{Raw: swap } x \leftrightarrow y \text{ and solve for } y")

    target = st.radio("Target", ["Linear Function", "Quadratic Function"], horizontal=True, key="inv_target")
    fig = go.Figure()
    x = np.linspace(-10, 10, 400)

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 2.0, 0.1, key="inv_m")
        c = st.slider("Intercept c", -10.0, 10.0, 0.0, 0.1, key="inv_c")
        y = m * x + c
        # inverse: x = my + c => y = (x - c) / m
        if abs(m) > 0.001:
            y_inv = (x - c) / m
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#6366f1", width=2), name=f"f(x)={{{m}}}x+{{{c}}}"))
            fig.add_trace(go.Scatter(x=x, y=y_inv, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name=f"f⁻¹(x)=(x-{{{c}}})/{{{m}}}"))
        else:
            st.warning("Slope m cannot be 0 for inverse of a linear function (horizontal line).")

    if target == "Quadratic Function":
        a = st.slider("a (positive for √)", 0.1, 5.0, 1.0, 0.1, key="inv_a")
        c = st.slider("c (constant)", -10.0, 10.0, 0.0, 0.1, key="inv_c")
        y = a * x**2 + c
        # inverse: x = ay² + c => y = ±√((x-c)/a) for x ≥ c
        x_fwd = np.linspace(-5, 5, 400)
        y_fwd = a * x_fwd**2 + c
        # Only show positive branch
        x_inv = np.linspace(c, c + 10, 400)
        y_inv_pos = np.sqrt((x_inv - c) / a)
        y_inv_neg = -np.sqrt((x_inv - c) / a)
        fig.add_trace(go.Scatter(x=x_fwd, y=y_fwd, mode="lines", line=dict(color="#6366f1", width=2), name="f(x)=ax²+c"))
        fig.add_trace(go.Scatter(x=x_inv, y=y_inv_pos, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="f⁻¹(x) (positive)"))
        fig.add_trace(go.Scatter(x=x_inv, y=y_inv_neg, mode="lines", line=dict(color="#ef4444", width=1, dash="dot"), name="f⁻¹(x) (negative)"))

    fig.add_trace(go.Scatter(x=[-10, 10], y=[-10, 10], mode="lines", line=dict(color="#555", width=1, dash="dot"), name="y=x"))
    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[-10, 10], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Reciprocal 1/f(x) ────────────────────────────────────
elif topic == "Reciprocal 1/f(x)":
    st.markdown("## Reciprocal 1/f(x)")
    st.latex(r"\frac{1}{f(x)} \quad\text{Vertical asymptotes where } f(x) = 0")

    target = st.radio("Target", ["Linear Function", "Quadratic Function"], horizontal=True, key="rec_target")
    fig = go.Figure()
    x = np.linspace(-10, 10, 2000)

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="rec_m")
        c = st.slider("Intercept c", -10.0, 10.0, 2.0, 0.1, key="rec_c")
        y = m * x + c
        y_rec = 1.0 / y
        y_rec = np.where(np.abs(y) < 0.005, np.nan, y_rec)
        y_rec = np.where(np.abs(y_rec) > 20, np.nan, y_rec)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#6366f1", width=2), name=f"f(x)={{{m}}}x+{{{c}}}"))
        fig.add_trace(go.Scatter(x=x, y=y_rec, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="1/f(x)"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="rec_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="rec_b")
        c = st.slider("c", -10.0, 10.0, -2.0, 0.1, key="rec_c")
        y = a * x**2 + b * x + c
        y_rec = 1.0 / y
        y_rec = np.where(np.abs(y) < 0.005, np.nan, y_rec)
        y_rec = np.where(np.abs(y_rec) > 20, np.nan, y_rec)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#6366f1", width=2), name="f(x)"))
        fig.add_trace(go.Scatter(x=x, y=y_rec, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="1/f(x)"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[-10, 10], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Shear ────────────────────────────────────────────────
elif topic == "Shear":
    st.markdown("## Shear Transformation")
    st.latex(r"\text{Horizontal: } (x, y) \to (x + ky, y) \qquad \text{Vertical: } (x, y) \to (x, y + kx)")

    target = st.radio("Target", ["Point", "Linear Function", "Quadratic Function"], horizontal=True, key="sh_target")
    direction = st.radio("Direction", ["Horizontal", "Vertical"], horizontal=True, key="sh_dir")
    k = st.slider("Shear factor k", -3.0, 3.0, 1.0, 0.1, key="sh_k")

    fig = go.Figure()
    x = np.linspace(-10, 10, 400)

    if target == "Point":
        px = st.slider("Point x", -8.0, 8.0, 2.0, 0.1, key="sh_px")
        py = st.slider("Point y", -8.0, 8.0, 3.0, 0.1, key="sh_py")
        if direction == "Horizontal": rx, ry = px + k * py, py
        else: rx, ry = px, py + k * px
        fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=12, color="#6366f1"), name=f"P({px:.1f},{py:.1f})"))
        fig.add_trace(go.Scatter(x=[rx], y=[ry], mode="markers", marker=dict(size=12, color="#ef4444", symbol="x"), name=f"P'({rx:.1f},{ry:.1f})"))

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="sh_m")
        c = st.slider("Intercept c", -10.0, 10.0, 1.0, 0.1, key="sh_c")
        pt_x = np.array([-10, 10])
        pt_y = m * pt_x + c
        if direction == "Horizontal": r_pt_x, r_pt_y = pt_x + k * pt_y, pt_y
        else: r_pt_x, r_pt_y = pt_x, pt_y + k * pt_x
        fig.add_trace(go.Scatter(x=pt_x, y=pt_y, mode="lines", line=dict(color="#6366f1", width=2), name=f"y={{{m}}}x+{{{c}}}"))
        fig.add_trace(go.Scatter(x=r_pt_x, y=r_pt_y, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="Sheared"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="sh_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="sh_b")
        c = st.slider("c", -10.0, 10.0, -2.0, 0.1, key="sh_c")
        pt_x = x.copy()
        pt_y = a * pt_x**2 + b * pt_x + c
        if direction == "Horizontal": r_pt_x, r_pt_y = pt_x + k * pt_y, pt_y
        else: r_pt_x, r_pt_y = pt_x, pt_y + k * pt_x
        fig.add_trace(go.Scatter(x=pt_x, y=pt_y, mode="lines", line=dict(color="#6366f1", width=2), name="Original"))
        fig.add_trace(go.Scatter(x=r_pt_x, y=r_pt_y, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="Sheared"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[-10, 10], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)

# ── Stretch ──────────────────────────────────────────────
elif topic == "Stretch":
    st.markdown("## Stretch Transformation")
    st.latex(r"\text{Horizontal: } (x, y) \to (kx, y) \qquad \text{Vertical: } (x, y) \to (x, ky)")

    target = st.radio("Target", ["Point", "Linear Function", "Quadratic Function"], horizontal=True, key="st_target")
    direction = st.radio("Direction", ["Vertical (y × p)", "Horizontal (x × p)"], horizontal=True, key="st_dir")
    p = st.slider("Stretch factor p", -3.0, 3.0, 2.0, 0.1, key="st_p")

    fig = go.Figure()
    x = np.linspace(-10, 10, 400)

    if target == "Point":
        px = st.slider("Point x", -8.0, 8.0, 2.0, 0.1, key="st_px")
        py = st.slider("Point y", -8.0, 8.0, 3.0, 0.1, key="st_py")
        if "Vertical" in direction: rx, ry = px, py * p
        else: rx, ry = px * p, py
        fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=12, color="#6366f1"), name=f"P({px:.1f},{py:.1f})"))
        fig.add_trace(go.Scatter(x=[rx], y=[ry], mode="markers", marker=dict(size=12, color="#ef4444", symbol="x"), name=f"P'({rx:.1f},{ry:.1f})"))

    if target == "Linear Function":
        m = st.slider("Slope m", -5.0, 5.0, 1.0, 0.1, key="st_m")
        c = st.slider("Intercept c", -10.0, 10.0, 1.0, 0.1, key="st_c")
        if "Vertical" in direction:
            y_orig = m * x + c
            y_trans = p * y_orig
            fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color="#6366f1", width=2), name=f"y={{{m}}}x+{{{c}}}"))
            fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name=f"Stretched y×{p}"))
        else:
            y_orig = m * x + c
            y_trans = m * (x / p) + c if abs(p) > 0.01 else np.full_like(x, np.nan)
            fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color="#6366f1", width=2), name=f"y={{{m}}}x+{{{c}}}"))
            fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name=f"Stretched x×{p}"))

    if target == "Quadratic Function":
        a = st.slider("a", -5.0, 5.0, 1.0, 0.1, key="st_a")
        b = st.slider("b", -5.0, 5.0, 0.0, 0.1, key="st_b")
        c = st.slider("c", -10.0, 10.0, -2.0, 0.1, key="st_c")
        if "Vertical" in direction:
            y_orig = a * x**2 + b * x + c
            y_trans = p * y_orig
        else:
            y_orig = a * x**2 + b * x + c
            y_trans = a * (x / p)**2 + b * (x / p) + c if abs(p) > 0.01 else np.full_like(x, np.nan)
        fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines", line=dict(color="#6366f1", width=2), name="Original"))
        fig.add_trace(go.Scatter(x=x, y=y_trans, mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="Stretched"))

    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
    fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), yaxis_range=[-12, 12], hovermode="x")
    st.plotly_chart(fig, use_container_width=True)
# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
