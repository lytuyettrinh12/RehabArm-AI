import os
import time
import random
import math
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import joblib
import pickle
import base64

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(PROJECT_ROOT, "assets", "anatomical_hologram_arm.jpg")
B64_IMAGE = ""
if os.path.exists(IMAGE_PATH):
    with open(IMAGE_PATH, "rb") as img_file:
        B64_IMAGE = base64.b64encode(img_file.read()).decode('utf-8')

from signal_processing import SignalProcessor, calculate_effort_score
from train_openvino_model import SimpleFatigueClassifier

# Page Config
st.set_page_config(
    page_title="FlexiMind AI - Tele-Rehab Dashboard",
    page_icon="🦾",
    layout="wide"
)

# Custom CSS for UI Wow Factor
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00D2FF;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #8892B0;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card-normal {
        background-color: #0D2818;
        border: 2px solid #00E676;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #00E676;
    }
    .metric-card-fatigue {
        background-color: #3B0000;
        border: 2px solid #FF1744;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #FF1744;
        animation: pulse 1s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Load AI Model (Intel OpenVINO Core)
@st.cache_resource
def load_ai_model():
    return SimpleFatigueClassifier()

model = load_ai_model()
processor = SignalProcessor()

# Title Header with Intel OpenVINO Badge
st.markdown("<div class='main-header'>FlexiMind AI 🦾</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Smart Active-Assistive Rehab Sleeve powered by Intel OpenVINO</div>", unsafe_allow_html=True)
device_str = getattr(model, 'device_name', 'Intel Core CPU')
st.markdown(f"""
<div style='text-align: center; margin-top: -10px; margin-bottom: 20px;'>
    <span style='background: rgba(0, 210, 255, 0.15); border: 1px solid #00D2FF; color: #00D2FF; padding: 5px 15px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; box-shadow: 0 0 10px rgba(0,210,255,0.2);'>
        ⚡ Intel® OpenVINO™ Runtime Engine: ACTIVE [{device_str}]
    </span>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.header("⚙️ System Settings")
mode = st.sidebar.radio("Input Source Mode:", ["Simulated Data (Demo)", "Hardware ESP32 Serial"])

com_port = "COM3"
if mode == "Hardware ESP32 Serial":
    com_port = st.sidebar.text_input("Serial COM Port (e.g. COM3 / /dev/ttyUSB0):", "COM3")
    baud_rate = st.sidebar.selectbox("Baud Rate:", [115200, 9600])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏥 Physiotherapist Control")
target_reps = st.sidebar.number_input("Target Daily Repetitions:", value=15)
fatigue_sensitivity = st.sidebar.slider("Fatigue Sensitivity Threshold:", 0.5, 0.95, 0.75)

# Initialize Session State
if 'semg_history' not in st.session_state:
    st.session_state.semg_history = [0.0] * 50
if 'effort_history' not in st.session_state:
    st.session_state.effort_history = [0.0] * 50
if 'angle_history' not in st.session_state:
    st.session_state.angle_history = [0.0] * 50
if 'is_flexing' not in st.session_state:
    st.session_state.is_flexing = False
if 'rep_count' not in st.session_state:
    st.session_state.rep_count = 0
if 'fatigue_count' not in st.session_state:
    st.session_state.fatigue_count = 0

# Dashboard Layout Columns
col1, col2, col3 = st.columns([1, 1, 1])

# Simulation Data Generator
def get_next_sample(is_simulated=True, serial_conn=None):
    if is_simulated:
        # Simulate normal flexing vs fatigue over time
        t = time.time()
        is_fatigued_sim = (int(t) % 20 > 12) # Simulate fatigue every 20 seconds
        
        # Simulate Arm Flexing (Sine Wave for Angle 0 -> 90 -> 0)
        sim_angle = abs(math.sin(t * 1.5)) * 90 
        sim_ay = 16384 * math.sin(sim_angle * math.pi / 180)
        sim_az = 16384 * math.cos(sim_angle * math.pi / 180)

        if is_fatigued_sim:
            raw_semg = float(np.random.normal(650, 150))
            # If fatigued, maybe simulate spasm (rapid changes) or joint lock (no movement)
            if int(t*2) % 2 == 0:
                sim_ay += random.randint(-8000, 8000) # Spasm
        else:
            raw_semg = float(np.random.normal(250, 50))
            
        ax = random.randint(-500, 500)
        return raw_semg, ax, int(sim_ay), int(sim_az)
    else:
        # Real Serial Communication logic
        try:
            import serial
            if serial_conn and serial_conn.in_waiting:
                line = serial_conn.readline().decode('utf-8').strip()
                parts = line.split(',')
                if len(parts) >= 4:
                    return float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
        except Exception:
            pass
        return 0.0, 0, 0, 16384

# Live Loop Container Layout Setup (OUTSIDE LOOP)
st.sidebar.markdown("### 🟢 Real-time Control")
run_loop = st.sidebar.checkbox("Start Live Stream", value=True)

metrics_cols = st.columns(5)
m1_ph = metrics_cols[0].empty()
m2_ph = metrics_cols[1].empty()
m3_ph = metrics_cols[2].empty()
m4_ph = metrics_cols[3].empty()
m5_ph = metrics_cols[4].empty()

st.markdown("---")
banner_ph = st.empty()
st.markdown("<br>", unsafe_allow_html=True)

g1, g2, g3 = st.columns(3)
g1_ph = g1.empty()
g2_ph = g2.empty()
g3_ph = g3.empty()

if run_loop:
    for i in range(1000): # Run for demo streaming
        raw_val, ax, ay, az = get_next_sample(is_simulated=(mode == "Simulated Data (Demo)"))
        
        # Update sEMG History Buffer
        st.session_state.semg_history.pop(0)
        st.session_state.semg_history.append(raw_val)
        
        # Feature Extraction
        features = processor.extract_features(st.session_state.semg_history[-30:])
        rms_val, mav_val, var_val, zcr_val, med_freq = features
        
        effort_score = calculate_effort_score(rms_val)
        st.session_state.effort_history.pop(0)
        st.session_state.effort_history.append(effort_score)

        # Calculate Arm Angle using IMU data (Ay, Az)
        # pitch = atan2(ay, az)
        current_angle = abs(math.atan2(ay, az) * 180 / math.pi) if az != 0 else 90.0
        
        st.session_state.angle_history.pop(0)
        st.session_state.angle_history.append(current_angle)
        
        # --- IMU ALGORITHM 1: Rep Counting State Machine ---
        if current_angle > 60 and not st.session_state.is_flexing:
            st.session_state.is_flexing = True
        elif current_angle < 30 and st.session_state.is_flexing:
            st.session_state.is_flexing = False
            st.session_state.rep_count += 1
            
        # --- IMU ALGORITHM 2: Safety Detection (Spasm & Joint Lock) ---
        is_spasm = False
        is_joint_lock = False
        
        # Calculate delta angle over the last 3 samples
        delta_angle_rapid = abs(current_angle - st.session_state.angle_history[-3])
        if delta_angle_rapid > 35: 
            is_spasm = True
            
        # Calculate angle change over the last 20 samples (~2 seconds)
        delta_angle_slow = abs(current_angle - st.session_state.angle_history[-20])
        if effort_score > 70 and delta_angle_slow < 5:
            is_joint_lock = True

        # AI Prediction via Intel OpenVINO / Joblib Model (sEMG Fatigue)
        fatigue_predicted = False
        fatigue_prob = 0.0
        if model is not None:
            features_input = np.array([features])
            prediction = model.predict(features_input)[0]
            probs = model.predict_proba(features_input)[0]
            fatigue_prob = probs[1] if len(probs) > 1 else float(prediction)
            if fatigue_prob > fatigue_sensitivity:
                fatigue_predicted = True

        # Closed-loop Actuation Trigger
        actuator_status = "NORMAL (Servo at 0°)"
        alert_reason = ""
        
        if fatigue_predicted or is_spasm or is_joint_lock:
            actuator_status = "⚡ EMERGENCY STOP (Servo rotated 90° - Tension Released!)"
            st.session_state.fatigue_count += 1
            if is_spasm:
                alert_reason = "SPASM / CO GIẬT ĐỘT NGỘT"
            elif is_joint_lock:
                alert_reason = "JOINT LOCK / KẸT KHỚP (Cố sức nhưng tay không gập được)"
            else:
                alert_reason = f"FATIGUE / MỎI CƠ (OpenVINO Confidence: {fatigue_prob*100:.1f}%)"

        # Render Live Dashboard UI (IN-PLACE UPDATES)
        m1_ph.metric("Live sEMG Signal", f"{int(raw_val)} µV")
        m2_ph.metric("Effort Score", f"{effort_score:.1f} %")
        m3_ph.metric("Arm Angle", f"{int(current_angle)}°")
        m4_ph.metric("Completed Reps", f"{st.session_state.rep_count} / {target_reps}")
        m5_ph.metric("Median Frequency", f"{med_freq:.1f} Hz")

        # AI Status Banner
        if alert_reason != "":
            banner_ph.markdown(f"""
            <div class="metric-card-fatigue">
                🚨 <b>AI SAFETY ALERT: {alert_reason}</b><br>
                {actuator_status}
            </div>
            """, unsafe_allow_html=True)
        else:
            banner_ph.markdown(f"""
            <div class="metric-card-normal">
                🟢 <b>AI STATUS: NORMAL (OpenVINO Confidence: {(1-fatigue_prob)*100:.1f}%)</b><br>
                Muscle status healthy. Patient actively exercising. {actuator_status}
            </div>
            """, unsafe_allow_html=True)

        # Live Graphs
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(y=st.session_state.semg_history, mode='lines', name='Raw sEMG (µV)', line=dict(color='#00D2FF', width=2)))
        fig1.add_trace(go.Scatter(y=st.session_state.effort_history, mode='lines', name='Effort Score (%)', line=dict(color='#00E676', width=2, dash='dot')))
        fig1.update_layout(title="Real-Time sEMG Signal & Effort Score", template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20))
        g1_ph.plotly_chart(fig1, use_container_width=True, key=f"fig1_{i}")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(y=st.session_state.angle_history, mode='lines', name='Arm Angle (°)', line=dict(color='#FFCA28', width=2)))
        # Draw threshold lines for rep counting
        fig2.add_hline(y=60, line_dash="dash", line_color="rgba(255, 255, 255, 0.3)", annotation_text="Flex Threshold (60°)")
        fig2.add_hline(y=30, line_dash="dash", line_color="rgba(255, 255, 255, 0.3)", annotation_text="Release Threshold (30°)")
        fig2.update_layout(title="Real-Time IMU Arm Angle", template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20), yaxis_range=[0, 100])
        g2_ph.plotly_chart(fig2, use_container_width=True, key=f"fig2_{i}")
        
        # --- REALISTIC HUMAN ARM DIGITAL TWIN ---
        hud_color = "#00E676" if not fatigue_predicted and not is_spasm and not is_joint_lock else "#FF1744"
        hud_status = "STABLE" if not fatigue_predicted else "FATIGUE"
        
        bg_url = f"data:image/jpeg;base64,{B64_IMAGE}" if B64_IMAGE else ""
        
        html_code = f"""<div style="background: radial-gradient(circle at center, #0a1128 0%, #000411 100%); border-radius: 12px; height: 350px; position: relative; overflow: hidden; border: 1px solid rgba(0, 210, 255, 0.3); box-shadow: 0 0 25px rgba(0, 210, 255, 0.1) inset;">
<div style="position: absolute; width: 100%; height: 100%; opacity: 0.15; background-image: radial-gradient(#00D2FF 1px, transparent 1px); background-size: 24px 24px;"></div>
<div style="position: absolute; top: 15px; left: 15px; color: #00D2FF; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; z-index: 10;">
<div style="font-size: 1rem; font-weight: 700; color: #FFFFFF; text-shadow: 0 0 8px rgba(0,210,255,0.8); letter-spacing: 0.5px;">🧑 PATIENT DIGITAL TWIN</div>
<div style="color: {hud_color}; margin-top: 4px; font-weight: 600; font-size: 0.85rem; text-shadow: 0 0 6px {hud_color};">STATUS: {hud_status}</div>
<div style="color: #00E676; margin-top: 2px; font-size: 0.8rem;">EFFORT: {effort_score:.1f}%</div>
<div style="color: #FFCA28; margin-top: 2px; font-size: 0.8rem; font-weight: 600;">JOINT ANGLE: {int(current_angle)}&deg;</div>
</div>
<!-- Human Bicep (Left Half) -->
<div style="position: absolute; left: 5%; top: 50%; width: 45%; height: 260px; margin-top: -130px; background-image: url('{bg_url}'); background-size: 200% 100%; background-position: left center; background-repeat: no-repeat; mix-blend-mode: screen;"></div>
<!-- Human Forearm (Right Half - Rotating Pivot) -->
<div style="position: absolute; left: 50%; top: 50%; width: 45%; height: 260px; margin-top: -130px; background-image: url('{bg_url}'); background-size: 200% 100%; background-position: right center; background-repeat: no-repeat; transform-origin: left center; transform: rotate({-current_angle}deg); mix-blend-mode: screen; filter: drop-shadow(0 0 8px rgba(255,160,0,0.4));"></div>
<!-- Central Elbow Joint Medical Glow Ring -->
<div style="position: absolute; left: 50%; top: 50%; width: 24px; height: 24px; margin-left: -12px; margin-top: -12px; border-radius: 50%; background-color: #FF9100; box-shadow: 0 0 15px #FF9100, 0 0 30px #FF9100; opacity: 0.85; mix-blend-mode: screen;"></div>
<div style="position: absolute; left: 50%; top: 50%; width: 36px; height: 36px; margin-left: -18px; margin-top: -18px; border-radius: 50%; border: 2px solid #FFAB00; box-shadow: 0 0 10px #FFAB00 inset; opacity: 0.6;"></div>
<!-- Medical HUD Tracking Tag -->
<div style="position: absolute; right: 15px; bottom: 15px; background: rgba(0,210,255,0.1); border: 1px solid rgba(0,210,255,0.3); border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; color: #00D2FF; font-family: monospace;">
ROM: 0&deg; - {int(current_angle)}&deg; (Active)
</div>
</div>"""
        g3_ph.markdown(html_code, unsafe_allow_html=True)

        time.sleep(0.05)
