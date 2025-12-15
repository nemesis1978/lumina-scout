import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import openai
import os
import json
import time
import io
from urllib.parse import urlparse

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="Lumina Scout v3",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for "Senior" Look
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #212529; }
    .main-header { font-size: 2.5rem; font-weight: 800; color: #1a1a1a; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #6c757d; margin-bottom: 2rem; }
    .card { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 1rem; }
    .metric { font-size: 1.8rem; font-weight: bold; color: #2563eb; }
    div[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #dee2e6; }
</style>
""", unsafe_allow_html=True)

# --- 2. BACKEND LOGIC ---

def get_serper_results(query, api_key):
    """
    Executes a search on Google Maps via Serper.dev /places endpoint.
    """
    url = "https://google.serper.dev/places"
    payload = json.dumps({
        "q": query,
        "gl": "it",
        "hl": "it"
    })
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("places", [])
        else:
            st.error(f"Serper API Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Connection Error (Serper): {e}")
        return []

def generate_synonyms_openai(target, location, api_key):
    """
    Uses OpenAI to generate intelligent search variations.
    """
    if not api_key:
        return [f"{target} {location}"]
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""
        Act as a Lead Generation Expert.
        Target Category: "{target}"
        Location: "{location}"
        
        Task: Generate a Python list of 5 distinct Google Maps search queries to find all businesses of this type in the area.
        Strategy: Use synonyms (e.g., if 'Dentist' -> 'Dental Clinic', 'Odontoiatra', 'Studio Dentistico').
        Format: Return ONLY the list of strings, nothing else.
        Example Output: ["Dentista Polla", "Studio Dentistico Polla", "Clinica Odontoiatrica Polla"]
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        # Safe evaluation of the list string
        try:
            # Attempt to parse valid python list syntax
            if content.startswith("[") and content.endswith("]"):
                import ast
                queries = ast.literal_eval(content)
                return queries
            else:
                # Fallback splitting if LLM is chatty
                return [x.strip() for x in content.split(',') if x.strip()]
        except:
            return [f"{target} {location}"]
            
    except Exception as e:
        st.warning(f"OpenAI Generation Error: {e}. Falling back to basic query.")
        return [f"{target} {location}"]

def enrich_lead_data(url):
    """
    Scrapes the website to detect Chatbots, Tech Stack, and special features.
    """
    if not url:
        return {"Chatbot": "No", "Tech Stack": "N/A", "VTO": "No"}
        
    data = {"Chatbot": "No", "Tech Stack": "Unknown", "VTO": "No"}
    
    try:
        # User-Agent rotation or standard
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.0.0 Safari/537.36'
        }
        
        if not url.startswith("http"):
            url = "https://" + url
            
        response = requests.get(url, headers=headers, timeout=5, verify=False) # verify=False for robustness
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text().lower()
            html_content = str(soup).lower()
            
            # 1. Chatbot Detection
            chatbots = ['intercom', 'zendesk', 'tidio', 'whatsapp', 'drift', 'tawk.to', 'livechat', 'crisp']
            if any(bot in html_content for bot in chatbots):
                data["Chatbot"] = "Yes"
                
            # 2. Tech Stack Detection
            stack = []
            if 'wp-content' in html_content: stack.append("WordPress")
            if 'shopify' in html_content: stack.append("Shopify")
            if 'wix' in html_content: stack.append("Wix")
            if 'squarespace' in html_content: stack.append("Squarespace")
            
            if stack:
                data["Tech Stack"] = ", ".join(stack)
            
            # 3. VTO (Virtual Try-On) Detection
            vto_keywords = ['virtual try-on', 'magic mirror', 'fit analytics', 'prova virtuale', '3d try on']
            if any(k in text_content for k in vto_keywords):
                data["VTO"] = "Yes"
                
    except Exception:
        # Fail silently or gracefully on scrape error
        data["Tech Stack"] = "Scrape Failed"
        
    return data

# --- 3. UI LAYOUT ---

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    serper_key = st.text_input("SERPER_API_KEY", type="password", help="Required for Google Maps Search")
    openai_key = st.text_input("OPENAI_API_KEY", type="password", help="Required for Keyword Expansion")
    
    st.divider()
    st.markdown("Developed by **Lumina AI**")
    st.caption("v3.0.0 - Senior Build")

# Main Content
st.markdown('<div class="main-header">🦅 Lumina Scout</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">B2B Lead Generation & Intelligence Engine</div>', unsafe_allow_html=True)

# Checks
if not serper_key or not openai_key:
    st.warning("⚠️ Please configure API Keys in the sidebar to proceed.")
    st.stop()

# Inputs
with st.container():
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        target_category = st.text_input("Target Category", placeholder="e.g. Supermarket, Dentist")
    with c2:
        target_location = st.text_input("Location", placeholder="e.g. Polla, SA")
    with c3:
        st.write("") # Spacer
        st.write("")
        start_btn = st.button("Start Scouting 🚀", use_container_width=True, type="primary")

    c4, c5 = st.columns([3, 1])
    with c4:
        radius_mock = st.slider("Visual Radius (km)", 5, 50, 20, help="Visual indicator. Logic is handled by AI keyword selection.")
    with c5:
        deep_analysis = st.checkbox("Deep Analysis", value=True, help="Scrape websites for Tech Stack & Chatbots")

# Execution Flow
if start_btn:
    if not target_category or not target_location:
        st.error("Please fill in both Target and Location.")
    else:
        st.divider()
        
        # A. Keyword Generation
        with st.status("🧠 Step 1: generating strategic search vectors...", expanded=True) as status:
            queries = generate_synonyms_openai(target_category, target_location, openai_key)
            st.write(f"**Generated Strategy:**")
            st.code("\n".join(queries))
            status.update(label="✅ Search Strategy Ready", state="complete", expanded=False)
            
        # B. Maps Search
        all_leads = []
        seen_ids = set() # For deduplication
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, q in enumerate(queries):
            status_text.text(f"📍 Scouting Sector: {q}...")
            places = get_serper_results(q, serper_key)
            
            for p in places:
                # Deduplication logic: Address is strong, Title is fallback
                uid = p.get('address', p.get('title'))
                if uid not in seen_ids:
                    seen_ids.add(uid)
                    
                    # Basic Object
                    lead = {
                        "Business Name": p.get("title"),
                        "Address": p.get("address"),
                        "Phone": p.get("phoneNumber"),
                        "Website": p.get("website"),
                        "Rating": p.get("rating"),
                        "Reviews": p.get("userRatingCount")
                    }
                    all_leads.append(lead)
            
            progress_bar.progress((i + 1) / len(queries))
            time.sleep(0.5) # Polite delay
            
        status_text.text("✅ Maps Scouting Complete.")
        
        # C. Deep Analysis (Enrichment)
        if deep_analysis:
            st.write(f"🔬 Enriching {len(all_leads)} leads with Tech Intelligence...")
            enrich_bar = st.progress(0)
            
            for i, lead in enumerate(all_leads):
                if lead.get("Website"):
                    tech_data = enrich_lead_data(lead["Website"])
                    lead.update(tech_data)
                else:
                    lead.update({"Chatbot": "N/A", "Tech Stack": "N/A", "VTO": "N/A"})
                
                enrich_bar.progress((i + 1) / len(all_leads))
                
        # D. Display & Export
        if all_leads:
            df = pd.DataFrame(all_leads)
            
            # Reorder columns for professional look
            preferred_order = ["Business Name", "Address", "Website", "Phone", "Rating", "Chatbot", "Tech Stack", "VTO"]
            # Filter only existing columns
            cols = [c for c in preferred_order if c in df.columns] + [c for c in df.columns if c not in preferred_order]
            df = df[cols]
            
            st.divider()
            st.success(f"🎉 Mission Complete: Found {len(df)} Unique Leads.")
            
            st.dataframe(
                df,
                column_config={
                    "Website": st.column_config.LinkColumn("Website URL"),
                    "Rating": st.column_config.NumberColumn(format="%.1f ⭐")
                },
                use_container_width=True
            )
            
            # Excel Export
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Leads')
                worksheet = writer.sheets['Leads']
                for idx, col in enumerate(df.columns):
                    series = df[col]
                    max_len = max((series.astype(str).map(len).max(), len(str(col)))) + 1
                    worksheet.set_column(idx, idx, max_len)
            
            fn = f"Lumina_Scout_{target_category}_{target_location}.xlsx".replace(" ", "_")
            st.download_button(
                label="📥 Download Excel Report",
                data=buffer.getvalue(),
                file_name=fn,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
        else:
            st.error("🚫 No results found. Try expanding the radius or changing the target.")
