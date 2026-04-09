"""
Streamlit Web UI — AI Trợ Giảng cho khóa học Lập trình C/C++ cơ bản.

Chạy: streamlit run app.py
"""

import streamlit as st
import uuid
from agent import stream_chat
from utils.storage import (
    get_metrics, update_metric, save_chat_session, 
    load_chat_session, list_past_chats
)
from utils.email_service import send_escalation_email

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="AI Trợ Giảng — C/C++",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ===== THEME MANAGEMENT =====
def get_theme():
    """Get current theme from session state."""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    return st.session_state.dark_mode


def toggle_theme():
    """Toggle between light and dark mode."""
    st.session_state.dark_mode = not st.session_state.dark_mode


# ===== CUSTOM CSS =====
def apply_styles():
    dark = get_theme()

    if dark:
        # Dark mode (Claude style)
        bg_primary = "#18181a"
        bg_secondary = "#202022"
        bg_card = "#202022"
        bg_chat_user = "#2a2a2c"
        bg_chat_ai = "transparent"
        text_primary = "#ecece9"
        text_secondary = "#a09d94"
        border_color = "#36342e"
        accent = "#d97757"
        accent_hover = "#c06b4e"
        sidebar_bg = "#19191a"
        input_bg = "#202022"
        shadow = "rgba(0,0,0,0.3)"
    else:
        # Light mode (Claude style)
        bg_primary = "#fdfcfb"
        bg_secondary = "#f3f2ee"
        bg_card = "#ffffff"
        bg_chat_user = "#f0efe9"
        bg_chat_ai = "transparent"
        text_primary = "#1a1918"
        text_secondary = "#666460"
        border_color = "#e2e0da"
        accent = "#d97757"
        accent_hover = "#c06b4e"
        sidebar_bg = "#f9f8f6"
        input_bg = "#ffffff"
        shadow = "rgba(0,0,0,0.04)"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap');

        /* ===== GLOBAL ===== */
        .stApp {{
            background-color: {bg_primary};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {text_primary};
        }}

        /* ===== HEADER ===== */
        .main-header {{
            background: {bg_card};
            border: 1px solid {border_color};
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px {shadow};
            text-align: center;
        }}
        .main-header h1 {{
            color: {text_primary};
            font-size: 1.8rem;
            font-family: 'Newsreader', 'Georgia', serif;
            font-weight: 600;
            margin: 0;
            letter-spacing: -0.01em;
        }}
        .main-header p {{
            color: {text_secondary};
            font-size: 0.95rem;
            margin: 0.5rem 0 0;
            font-weight: 400;
        }}

        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            border-right: 1px solid {border_color};
        }}
        section[data-testid="stSidebar"] .stMarkdown {{
            color: {text_primary};
        }}
        section[data-testid="stSidebar"] h4 {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {text_secondary};
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }}

        /* ===== CHAT MESSAGES ===== */
        .stChatMessage {{
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            border: 1px solid transparent;
        }}
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
            background-color: {bg_chat_user} !important;
            border: 1px solid {border_color};
        }}
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
            background-color: {bg_chat_ai} !important;
        }}

        /* ===== BUTTONS ===== */
        .stButton > button {{
            border-radius: 8px !important;
            border: 1px solid {border_color} !important;
            background-color: {bg_card} !important;
            color: {text_primary} !important;
            transition: all 0.2s ease !important;
            font-weight: 500 !important;
        }}
        .stButton > button:hover {{
            border-color: {accent} !important;
            color: {accent} !important;
            box-shadow: 0 2px 8px {shadow} !important;
        }}
        .stButton > button[data-testid="baseButton-primary"] {{
            background-color: {accent} !important;
            color: #ffffff !important;
            border: none !important;
        }}
        .stButton > button[data-testid="baseButton-primary"]:hover {{
            background-color: {accent_hover} !important;
            color: #ffffff !important;
        }}

        /* ===== CHAT INPUT ===== */
        .stChatInput {{
            border-color: {border_color};
            padding-bottom: 2rem;
        }}
        .stChatInput > div {{
            background-color: {input_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            transition: border-color 0.2s, box-shadow 0.2s;
            box-shadow: 0 2px 10px {shadow};
        }}
        .stChatInput > div:focus-within {{
            border-color: {accent};
            box-shadow: 0 0 0 2px {accent}33;
        }}

        /* ===== CARDS ===== */
        .info-card {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 8px {shadow};
            transition: transform 0.2s;
        }}
        .info-card:hover {{
            transform: translateY(-1px);
        }}
        .info-card h4 {{
            color: {text_primary};
            margin: 0 0 0.5rem;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: none !important;
            letter-spacing: normal !important;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .info-card p {{
            color: {text_secondary};
            margin: 0;
            font-size: 0.82rem;
            line-height: 1.6;
        }}

        /* ===== STATUS BADGE ===== */
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: {bg_card};
            border: 1px solid {border_color};
            color: {text_secondary};
            padding: 0.25rem 0.6rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }}
        .status-dot {{
            width: 6px;
            height: 6px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
        }}

        /* ===== QUICK ACTION BUTTONS ===== */
        .quick-action {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 0.6rem 0.8rem;
            margin: 0.25rem 0;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.8rem;
            color: {text_primary};
            display: block;
            width: 100%;
            text-align: left;
        }}
        .quick-action:hover {{
            border-color: {accent};
            color: {accent};
        }}

        /* ===== THEME TOGGLE ===== */
        .theme-toggle {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 0.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }}

        /* ===== TEXT COLORS ===== */
        .stMarkdown, .stMarkdown p, .stMarkdown li {{
            color: {text_primary};
        }}
        h1, h2, h3, h4, h5 {{
            color: {text_primary} !important;
        }}

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {{
            width: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        ::-webkit-scrollbar-thumb {{
            background: {border_color};
            border-radius: 3px;
        }}

        /* ===== MISC ===== */
        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 1rem;
        }}
        .stSpinner > div {{
            border-top-color: {accent} !important;
        }}
    </style>
    """, unsafe_allow_html=True)


# ===== SIDEBAR =====
def render_sidebar():
    with st.sidebar:
        # Theme toggle
        dark = get_theme()
        theme_icon = "🌙" if not dark else "☀️"
        theme_label = "Chế độ tối" if not dark else "Chế độ sáng"
        if st.button(f"{theme_icon} {theme_label}", use_container_width=True, key="theme_toggle"):
            toggle_theme()
            st.rerun()

        st.markdown("---")

        # Dashboard / Metrics
        bg_card = "#202022" if dark else "#ffffff"
        border_color = "#36342e" if dark else "#e2e0da"
        accent = "#d97757"
        text_primary = "#ecece9" if dark else "#1a1918"
        text_secondary = "#a09d94" if dark else "#666460"
        inner_bg = "#18181a" if dark else "#f9f8f6"

        metrics = get_metrics()
        st.markdown(f"""
        <div style="background: {bg_card}; padding: 16px; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid {border_color}; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <div style="color: {text_secondary}; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 1rem;">📊</span> Thống kê Agent
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; text-align: center; margin-bottom: 12px;">
                <div style="background: {inner_bg}; padding: 10px 4px; border-radius: 8px; border: 1px solid {border_color};">
                    <div style="font-size: 1.1rem; margin-bottom: 2px;">👍</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: {text_primary};">{metrics['helpful']}</div>
                </div>
                <div style="background: {inner_bg}; padding: 10px 4px; border-radius: 8px; border: 1px solid {border_color};">
                    <div style="font-size: 1.1rem; margin-bottom: 2px;">👎</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: {text_primary};">{metrics['unhelpful']}</div>
                </div>
                <div style="background: {inner_bg}; padding: 10px 4px; border-radius: 8px; border: 1px solid {border_color};">
                    <div style="font-size: 1.1rem; margin-bottom: 2px;">⚠️</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: {accent};">{metrics['escalated']}</div>
                </div>
            </div>
            <div style="font-size: 0.75rem; color: {text_secondary}; text-align: center; border-top: 1px solid {border_color}; padding-top: 8px;">
                Tổng câu hỏi giải quyết: <b style="color: {text_primary};">{metrics['total']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Status
        st.markdown("""
        <div class="status-badge" style="width: fit-content;">
            <div class="status-dot"></div>
            Online — Sẵn sàng
        </div>
        """, unsafe_allow_html=True)

        # Course info card
        st.markdown("""
        <div class="info-card">
            <h4>📚 Khóa học</h4>
            <p><strong>Lập trình C/C++ cơ bản</strong><br>
            Mã: CS101 | HK2 2025-2026<br>
            GV: ThS. Nguyễn Văn Minh</p>
        </div>
        """, unsafe_allow_html=True)

        # Schedule card
        st.markdown("""
        <div class="info-card">
            <h4>📅 Lịch học</h4>
            <p>🏫 Lý thuyết: Thứ 3, 8:00-10:00<br>
            💻 Thực hành: Thứ 5, 13:00-16:00</p>
        </div>
        """, unsafe_allow_html=True)

        # TA info card
        st.markdown("""
        <div class="info-card">
            <h4>👩‍💼 Trợ giảng</h4>
            <p>Trần Thị Hoa (TA chính)<br>
            <em>T2-T6: 18:00-21:00</em><br>
            Lê Minh Tuấn (TA phụ)<br>
            <em>T7: 9:00-12:00</em></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Quick actions
        st.markdown("#### 💡 Câu hỏi mẫu")

        quick_questions = [
            "🔧 Cách cài đặt gcc trên Windows?",
            "📝 Con trỏ trong C là gì?",
            "🐛 Segmentation fault là lỗi gì?",
            "📅 Lịch thi cuối kỳ khi nào?",
            "💻 Cho em xem code mẫu vòng lặp for",
        ]

        for q in quick_questions:
            if st.button(q, use_container_width=True, key=f"quick_{q}"):
                st.session_state.pending_question = q
                st.rerun()

        st.markdown("---")

        # Reset chat
        if st.button("➕ Đoạn chat mới", use_container_width=True, type="primary"):
            st.session_state.session_id = uuid.uuid4().hex
            st.session_state.messages = []
            st.session_state.attempt_count = 1
            st.session_state.rated_messages = set()
            if "pending_question" in st.session_state:
                del st.session_state.pending_question
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🕒 Lịch sử Chat")
        past_chats = list_past_chats()
        if not past_chats:
            st.markdown("<div style='font-size:0.8rem; color:gray'>Chưa có lịch sử</div>", unsafe_allow_html=True)
        else:
            for chat in past_chats[:5]: # Hiển thị 5 chat gần nhất
                if st.button(f"💬 {chat['title']}", key=f"hist_{chat['session_id']}", use_container_width=True):
                    st.session_state.session_id = chat['session_id']
                    st.session_state.messages = load_chat_session(chat['session_id'])
                    st.session_state.attempt_count = sum(1 for m in st.session_state.messages if m["role"] == "user") + 1
                    st.session_state.rated_messages = set(range(len(st.session_state.messages))) # Giả định các câu cũ không rate lại
                    st.rerun()

        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; opacity: 0.5; font-size: 0.7rem;">
            Powered by GPT-4o-mini + LangGraph<br>
            © 2026 AI Teaching Assistant
        </div>
        """, unsafe_allow_html=True)


# ===== MAIN CHAT =====
def render_main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>AI Trợ Giảng</h1>
        <p>Hỗ trợ học tập Lập trình C/C++ với GPT-4</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize state variables
    if "session_id" not in st.session_state:
        st.session_state.session_id = uuid.uuid4().hex
    if "attempt_count" not in st.session_state:
        st.session_state.attempt_count = 1
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rated_messages" not in st.session_state:
        st.session_state.rated_messages = set()

    # Display welcome message if no history
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown("""
**Xin chào! 👋 Mình là AI Trợ Giảng** cho khóa học *Lập trình C/C++ cơ bản*.

Mình có thể giúp bạn:
- 📖 **Giải thích kiến thức**: Biến, mảng, con trỏ, hàm, struct,...
- 🐛 **Debug code**: Gửi code lỗi cho mình phân tích
- 📋 **Thông tin khóa học**: Lịch học, điểm số, tài liệu
- 💡 **Gợi ý bài tập**: Hướng dẫn approach, không spoil đáp án

*Hãy gõ câu hỏi bên dưới hoặc chọn câu hỏi mẫu ở sidebar!* ✨
            """)

    # Display chat history
    for i, msg in enumerate(st.session_state.messages):
        avatar = "👤" if msg["role"] == "user" else "🎓"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            
            # Feedback widget cho lời giải của AI
            if msg["role"] == "assistant":
                is_rated = i in st.session_state.rated_messages
                feedback = st.feedback("thumbs", key=f"fb_{st.session_state.session_id}_{i}", disabled=is_rated)
                if feedback is not None and not is_rated:
                    st.session_state.rated_messages.add(i)
                    if feedback == 1:
                        update_metric("helpful", 1)
                        st.toast("Cảm ơn bạn đã đánh giá hữu ích! 👍")
                    elif feedback == 0:
                        update_metric("unhelpful", 1)
                        st.toast("Cảm ơn góp ý của bạn để AI tốt hơn! 👎")
                    # Lưu lại state messages
                    st.rerun()

    # Handle pending escalation response
    if "pending_escalation_report" in st.session_state:
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown("⚠️ **Xác nhận yêu cầu hỗ trợ từ Giảng viên/Trợ giảng**")
            with st.expander("Xem chi tiết phiếu hỗ trợ sẽ gửi", expanded=True):
                st.code(st.session_state.pending_escalation_report)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Xác nhận Gửi TA", use_container_width=True, type="primary"):
                    with st.spinner("Đang gửi email cho TA..."):
                        success = send_escalation_email(st.session_state.pending_escalation_report)
                    
                    st.session_state.messages.append({"role": "user", "content": "Xác nhận gửi phiếu escalate."})
                    if success:
                        st.session_state.messages.append({"role": "assistant", "content": "✅ Đã gửi email thành công cho giảng viên/TA. Họ sẽ hỗ trợ bạn trong thời gian sớm nhất nhé! ⏳"})
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": "❌ Lỗi: Không thể gửi email cho giảng viên. Bạn vui lòng thử liên hệ trực tiếp qua email ở trên nhé!"})
                    
                    update_metric("escalated", 1)
                    del st.session_state.pending_escalation_report
                    save_chat_session(st.session_state.session_id, st.session_state.messages)
                    st.rerun()
            with col2:
                if st.button("❌ Hủy bỏ", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Hủy gửi phiếu escalate."})
                    st.session_state.messages.append({"role": "assistant", "content": "Đã hủy yêu cầu gọi TA. Bạn cần mình hỗ trợ gì thêm không? 😊"})
                    del st.session_state.pending_escalation_report
                    save_chat_session(st.session_state.session_id, st.session_state.messages)
                    st.rerun()
        
        # Stop rendering chat input while waiting for confirmation
        return

    # Handle pending quick question
    pending = st.session_state.get("pending_question")
    if pending:
        del st.session_state.pending_question
        process_message(pending)

    # Chat input
    if prompt := st.chat_input("Hỏi mình bất cứ gì về C/C++..."):
        process_message(prompt)


def process_message(prompt: str):
    """Process a user message and get AI response."""
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Update total questions count metric
    update_metric("total", 1)

    # Build history for agent
    history = []
    for msg in st.session_state.messages[:-1]:  # Exclude current message
        history.append({"role": msg["role"], "content": msg["content"]})
        
    hidden_prompt = f"Lượt hỏi thứ {st.session_state.attempt_count} | Nội dung: {prompt}"

    # Stream AI response
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("🤔 Đang suy nghĩ..."):
            try:
                response_chunks = []
                response_placeholder = st.empty()

                for chunk in stream_chat(hidden_prompt, history):
                    response_chunks.append(chunk)
                    full_response = "".join(response_chunks)
                    response_placeholder.markdown(full_response + "▌")

                full_response = "".join(response_chunks)
                response_placeholder.markdown(full_response)

                if not full_response.strip():
                    full_response = "Xin lỗi, mình gặp sự cố khi xử lý câu hỏi. Bạn thử hỏi lại nhé! 🙏"
                    response_placeholder.markdown(full_response)

            except Exception as e:
                full_response = f"⚠️ Đã xảy ra lỗi: {str(e)}\n\nBạn vui lòng thử lại nhé!"
                st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Cập nhật số lần thử debug/giải thích liên tục
    st.session_state.attempt_count += 1
    
    # Check if an escalation was triggered
    if "--- ESCALATION REPORT ---" in full_response:
        parts = full_response.split("--- ESCALATION REPORT ---")
        ai_text = "⚠️ Mình đã chuẩn bị Phiếu yêu cầu hỗ trợ (Escalation Report). Bạn vui lòng kiểm tra thông tin bên dưới và bấm **Xác nhận** để gửi cho TA nhé!"
        report_text = parts[1].strip() if len(parts) > 1 else ""
        
        # Swap out the last message to hide the report string and prevent LLM hallucination
        st.session_state.messages[-1]["content"] = ai_text
        st.session_state.pending_escalation_report = report_text
    elif "chuyển câu hỏi cho TA" in full_response or "gọi cho giảng viên" in full_response:
        update_metric("escalated", 1)
        
    # Lưu phiên bản mới nhất của đoạn chat
    save_chat_session(st.session_state.session_id, st.session_state.messages)
    st.rerun()


# ===== MAIN =====
if __name__ == "__main__":
    apply_styles()
    render_sidebar()
    render_main()
