# 📖 TA_Chatbot README — Version 2.0

**Version:** 2.0 (Information Processing Rules)  
**Last Updated:** April 8, 2026  
**Status:** ✅ **Production Ready**

---

## 🎯 Mục Tiêu

TA_Chatbot là một **AI Teaching Assistant** 24/7 cho khóa học **Lập trình C/C++ cơ bản (CS101)**, được thiết kế để:

1. **Giảm 80% khối lượng công việc** cho dàn TA
2. **Giảm thời gian chờ** của học viên từ "giờ" xuống "giây"
3. **Đảm bảo độ tin cậy**: Mọi thông tin từ Knowledge Base, KHÔNG bịa chuyện

---

## ⚡ Quick Start (3 bước)

### Bước 1: Cài Đặt
```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python -m rag.indexer  # One-time
```

### Bước 2: Chạy
```bash
streamlit run app.py
```

### Bước 3: Test
```bash
python test_new_rules.py
```

---

## 📋 Quy Tắc Xử Lý Thông Tin (3 Rules)

### **Rule 1: Phân Loại Chính Xác**
- Weekly Assignments ≠ Labs ≠ Projects
- Mỗi loại có deadline policy khác nhau
- AI phải xác định chính xác trước khi trả lời

### **Rule 2: Trích Xuất & Grounding**
- Mọi info từ Knowledge Base
- Ghi rõ nguồn: "(Theo course_info.json)"
- KHÔNG tự bịa ngày tháng

### **Rule 3: Xử Lý Thông Tin Thiếu**
- Nếu không có → Escalate cho TA
- Nếu "nằm ở LMS" → Báo & hỏi có cần tag TA

---

## 🚀 Escalation System (3 Trigger Levels)

| Trigger | Condition | Action |
|---------|-----------|--------|
| **Trigger 1** | Sinh viên yêu cầu ("Hỏi TA") | Escalate ngay |
| **Trigger 2** | Thông tin không tìm được | Escalate tự động |
| **Trigger 3** | Sinh viên phản bác lần 2+ | Escalate |

---

## 🧪 Test Results

```
✅ TEST 1: Technical Question (Con trỏ?) → PASS
✅ TEST 2: Deadline Question (Project 1?) → PASS
✅ TEST 3: Grading Info (Cách tính điểm?) → PASS
✅ TEST 4: TRIGGER 1 (Hỏi TA giúp) → PASS
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) | Tóm tắt update chi tiết |
| [INFORMATION_PROCESSING_RULES.md](INFORMATION_PROCESSING_RULES.md) | Quy tắc xử lý thông tin |
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Hướng dẫn phát triển |
| [DEBUG_REPORT.md](DEBUG_REPORT.md) | Các lỗi đã sửa |

---

## 💬 Example Conversations

### Con trỏ là gì?
```
👤: "Con trỏ là gì?"
🎓: "Con trỏ là biến lưu trữ địa chỉ...
     (Theo slide Chương 6 - Pointers)
     Bạn có cần giải thích thêm không?"
```

### Project 1 deadline?
```
👤: "Project 1 deadline khi nào?"
🎓: "Project 1 deadline: 30/03/2026
     (Theo course_info.json)
     Trễ sẽ trừ 10%/ngày, tối đa 5 ngày."
```

### Hỏi TA
```
👤: "Hỏi TA giúp em with"
🎓: "Đã chuyên cho TA. Sẽ phản hồi sớm. 📞"
[ESCALATED]
```

---

## 🔧 Tech Stack

- **Framework**: LangChain + LangGraph
- **LLM**: OpenAI GPT-4o-mini
- **RAG**: FAISS
- **Frontend**: Streamlit
- **Language**: Python 3.9+

---

## 📞 Support

**Need help?**
- Check [INFORMATION_PROCESSING_RULES.md](INFORMATION_PROCESSING_RULES.md)
- See examples in [test_new_rules.py](test_new_rules.py)
- Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

---

**✅ Ready for production deployment!** 🚀
