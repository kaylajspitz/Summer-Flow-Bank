import streamlit as st
import json
import os

st.set_page_config(page_title="Summer Flow Bank", page_icon="🏦")

# The "Shared Brain"
DATA_FILE = "bank_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"checking": 0.0, "savings": 0.0, "daily_earnings": 0.0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if "bank" not in st.session_state:
    st.session_state.bank = load_data()

# Initialize the new deposit bucket so the app doesn't crash
if "temp_tokens" not in st.session_state:
    st.session_state.temp_tokens = 0

def sync():
    save_data(st.session_state.bank)

# --- UI LAYOUT ---
st.title("☀️ Summer Flow & Token Bank")

tab1, tab2, tab3 = st.tabs(["🗓️ Schedule", "🏦 Bank", "🛍️ Store"])

# --- TAB 1: SCHEDULE ---
with tab1:
    st.header("Today's Flexible Blocks")
    
    st.divider()
    # 1. MORNING ROUTINE
    st.write("**🌅 Morning Routine**")
    c_teeth_am = st.checkbox("Brushed Teeth AM (+1)", key="t_am")
    c_coffee = st.checkbox("Drank Coffee (+1)", key="cof")
    c_journal = st.checkbox("Journaled (+1)", key="jou")
    c_shower = st.checkbox("Took a Shower (+1)", key="sho")
    c_clothes = st.checkbox("Changed Clothes (+1)", key="clo")
    c_launch = st.checkbox("Perfect Launch: Nailed Morning Anchor (+5)", key="lau")
    
    st.divider()
    
    # 2. BLOCK 1
    st.write("**🧠 Block 1: Brain Power**")
    c_python = st.checkbox("Study Python (+1)", key="py")
    c_german = st.checkbox("Practice German (+1)", key="ger")
    c_calc = st.checkbox("Calculus Refresh (+1)", key="cal")
    c_piano = st.checkbox("Practice Piano (+1)", key="pia")
    c_b1 = st.checkbox("Perfect Block 1 (+5)", key="b1")

    st.divider()
    
    # 3. BLOCK 2
    st.write("**🚶‍♀️ Block 2: Movement & Errands**")
    c_exer = st.checkbox("Exercise (+1)", key="exe")
    errands = st.number_input("Errands/tasks completed (+1 each)", min_value=0, step=1, value=0, key="err")
    c_b2 = st.checkbox("Perfect Block 2 (+3)", key="b2")

    st.divider()
    
    # 4. BLOCK 3
    st.write("**☕ Block 3: Unwind and Reward**")
    c_game = st.checkbox("Video Games (+1)", key="gam")
    c_read = st.checkbox("Read (+1)", key="rea")
    col_i, col_r = st.columns([1, 15])
    with col_r:
        pages = st.number_input("*↳ Total pages read (+1 per 10 pages)*", min_value=0, step=1, value=0, key="pag")
    c_cozy = st.checkbox("Cozy Organizing (+1)", key="coz")
    c_res = st.checkbox("Low-Key Research (+1)", key="res")
    c_b3 = st.checkbox("Perfect Block 3 (+5)", key="b3")

    st.divider()
    
    # 5. EVENING
    st.write("**🌌 Evening Routine**")
    c_meds = st.checkbox("Took Meds (+1)", key="med")
    c_teeth_pm = st.checkbox("Brushed Teeth PM (+1)", key="t_pm")
    c_call = st.checkbox("Called Wesley (+1)", key="cal_w")
    col_ii, col_w = st.columns([1, 15])
    with col_w:
        c_exc = st.checkbox("*↳ Wesley Exception (Sent text) (+1)*", key="exc")
    c_land = st.checkbox("Perfect Landing: Nailed Evening Anchor (+4)", key="lan")
    
    st.divider()
    
    # 6. BONUSES
    st.write("**⭐ Executive Function Bonuses**")
    c_start = st.checkbox("The 'Just Started' Bonus (+1)", key="sta")
    c_mon = st.checkbox("The Monster Hurdle (+1)", key="mon")
    c_perf = st.checkbox("Perfect Day (+50)", key="per")

    # --- LIVE CALCULATION ---
    calc = sum([c_teeth_am, c_coffee, c_journal, c_shower, c_clothes, (c_launch * 5), 
                c_python, c_german, c_calc, c_piano, (c_b1 * 5),
                c_exer, (c_b2 * 3), c_game, c_read, c_cozy, c_res, (c_b3 * 5), 
                c_meds, c_teeth_pm, c_call, c_exc, (c_land * 4), 
                c_start, c_mon, (c_perf * 50)]) + errands + (pages // 10)
    
    st.divider()
    st.metric(label="Pending Tokens", value=f"{int(calc)}")
    
# --- DEPOSIT LOGIC ---

# 1. Initialize confirmation state if it doesn't exist
if 'confirm_deposit' not in st.session_state:
    st.session_state.confirm_deposit = False

# 2. If we are NOT in confirmation mode, show the primary deposit button
if not st.session_state.confirm_deposit:
    if st.button("💰 Deposit Pending Tokens"):
        st.session_state.temp_tokens = calc  # Use your main 'calc' variable
        st.session_state.confirm_deposit = True
        st.rerun()

# 3. If we ARE in confirmation mode, show the warning and the Yes/No buttons
else:
    st.warning(f"Are you sure you want to deposit {int(st.session_state.temp_tokens)} tokens?")
    col_yes, col_no = st.columns(2)
    
    if col_yes.button("✅ Yes, Deposit!"):
        st.session_state.bank["checking"] += float(st.session_state.temp_tokens)
        st.session_state.bank["daily_earnings"] += float(st.session_state.temp_tokens)
        sync()
        st.balloons()
        st.success(f"Success! {int(st.session_state.temp_tokens)} tokens added.")
        st.session_state.confirm_deposit = False
        st.rerun()
        
    if col_no.button("❌ Cancel"):
        st.session_state.confirm_deposit = False
        st.rerun()

# --- TAB 2: BANKING ---
with tab2:
    st.metric("Checking", f"${st.session_state.bank['checking']:.2f}")
    st.metric("Savings", f"${st.session_state.bank['savings']:.2f}")
    
    amt = st.number_input("Transfer Amount ($)", min_value=0.0, step=1.0)
    
    c1, c2 = st.columns(2)
    if c1.button("Checking ➔ Savings"):
        if amt <= st.session_state.bank["checking"]:
            st.session_state.bank["checking"] -= amt
            st.session_state.bank["savings"] += amt
            sync(); st.rerun()
    if c2.button("Savings ➔ Checking"):
        if amt <= st.session_state.bank["savings"]:
            st.session_state.bank["savings"] -= amt
            st.session_state.bank["checking"] += amt
            sync(); st.rerun()

    if st.button("🌙 Calculate Daily Interest"):
        rate = 0.02 if st.session_state.bank["daily_earnings"] >= 20 else 0.005
        payout = st.session_state.bank["savings"] * rate
        st.session_state.bank["savings"] += payout
        st.session_state.bank["daily_earnings"] = 0.0
        sync(); st.rerun()

# --- TAB 3: REWARD STORE ---
with tab3:
    store = {"Small Shop": 5.0, "Premium Sip": 6.0, "Veggie Bowl": 12.0, 
             "New Book": 15.0, "Indie Game": 20.0, "Mobile Desk": 50.0, "Stillwater Date": 100.0}
    for item, price in store.items():
        if st.button(f"Buy: {item} (${price:.2f})"):
            if st.session_state.bank["checking"] >= price:
                st.session_state.bank["checking"] -= price
                sync(); st.balloons()