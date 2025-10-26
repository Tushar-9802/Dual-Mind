import streamlit as st
import anthropic
import openai
import sqlite3
import time
from datetime import datetime

# Page config
st.set_page_config(page_title="Dual-Mind", layout="wide")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = {'claude': 0.0, 'gpt': 0.0}

# DB setup
def init_db():
    conn = sqlite3.connect('dual_mind.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY, timestamp TEXT, user_msg TEXT, 
                  claude_response TEXT, gpt_response TEXT, 
                  claude_cost REAL, gpt_cost REAL)''')
    conn.commit()
    return conn

# Cost calculation (tokens * price per 1K)
def calc_cost(tokens, model_type):
    rates = {
        'claude_in': 0.003, 'claude_out': 0.015,
        'gpt_in': 0.01, 'gpt_out': 0.03
    }
    return (tokens / 1000) * rates[model_type]

# API calls
def get_claude_response(prompt, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    start = time.time()
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    latency = time.time() - start
    cost = calc_cost(response.usage.input_tokens, 'claude_in') + \
           calc_cost(response.usage.output_tokens, 'claude_out')
    
    return response.content[0].text, cost, latency

def get_gpt_response(prompt, api_key):
    client = openai.OpenAI(api_key=api_key)
    start = time.time()
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    
    latency = time.time() - start
    cost = calc_cost(response.usage.prompt_tokens, 'gpt_in') + \
           calc_cost(response.usage.completion_tokens, 'gpt_out')
    
    return response.choices[0].message.content, cost, latency

# UI
st.title("Dual-Mind")
st.caption("Compare Claude Sonnet 4.5 vs GPT-4 Turbo side-by-side")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    claude_key = st.text_input("Anthropic API Key", type="password", 
                                value=st.session_state.get('claude_key', ''))
    gpt_key = st.text_input("OpenAI API Key", type="password",
                             value=st.session_state.get('gpt_key', ''))
    
    st.session_state.claude_key = claude_key
    st.session_state.gpt_key = gpt_key
    
    st.divider()
    st.metric("Claude Cost", f"${st.session_state.total_cost['claude']:.4f}")
    st.metric("GPT Cost", f"${st.session_state.total_cost['gpt']:.4f}")
    st.metric("Total", f"${sum(st.session_state.total_cost.values()):.4f}")
    
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
prompt = st.chat_input("Ask both AIs anything...")

if prompt:
    if not claude_key or not gpt_key:
        st.error("Enter both API keys in the sidebar")
    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Create two columns for responses
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Claude Sonnet 4.5")
            with st.spinner("Thinking..."):
                try:
                    claude_resp, claude_cost, claude_time = get_claude_response(prompt, claude_key)
                    st.markdown(claude_resp)
                    st.caption(f"{claude_time:.2f}s | ${claude_cost:.4f}")
                    st.session_state.total_cost['claude'] += claude_cost
                except Exception as e:
                    claude_resp = f"Error: {str(e)}"
                    claude_cost = 0
                    st.error(claude_resp)
        
        with col2:
            st.markdown("### GPT-4 Turbo")
            with st.spinner("Thinking..."):
                try:
                    gpt_resp, gpt_cost, gpt_time = get_gpt_response(prompt, gpt_key)
                    st.markdown(gpt_resp)
                    st.caption(f"{gpt_time:.2f}s | ${gpt_cost:.4f}")
                    st.session_state.total_cost['gpt'] += gpt_cost
                except Exception as e:
                    gpt_resp = f"Error: {str(e)}"
                    gpt_cost = 0
                    st.error(gpt_resp)
        
        # Save to DB
        conn = init_db()
        c = conn.cursor()
        c.execute('''INSERT INTO conversations 
                     (timestamp, user_msg, claude_response, gpt_response, claude_cost, gpt_cost)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (datetime.now().isoformat(), prompt, claude_resp, gpt_resp, 
                   claude_cost, gpt_cost))
        conn.commit()
        conn.close()
        
        # Add to session
        st.session_state.messages.append({
            'user': prompt,
            'claude': claude_resp,
            'gpt': gpt_resp
        })

# Show history
if st.session_state.messages:
    st.divider()
    st.subheader("Conversation History")
    
    for i, msg in enumerate(reversed(st.session_state.messages[-5:])):
        with st.expander(f"{msg['user'][:60]}...", expanded=(i==0)):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Claude:**")
                st.markdown(msg['claude'])
            with col2:
                st.markdown("**GPT-4:**")
                st.markdown(msg['gpt'])