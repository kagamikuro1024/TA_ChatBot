# AI Product Canvas — Chatbot NEO (Vietnam Airlines)

## Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Trả lời** | **User:**<br>- Hành khách cần tra cứu nhanh (vé, hành lý, đổi chuyến…)<br><br>**Pain:**<br>- Phải tự tìm info trên web rối<br>- Hotline chờ lâu<br>- FAQ khó tìm đúng mục<br><br>**AI giải quyết:**<br>- Chat trực tiếp → lấy info nhanh hơn<br>- Giảm friction so với web navigation<br><br> Nhưng thực tế:<br>- NEO chủ yếu = FAQ retrieval (search UI trá hình chatbot)<br>- Value chỉ ở **speed**, không phải **intelligence** | **Phân tích theo 4 paths:**<br><br>**1. Khi AI đúng:**<br>- User thấy: câu trả lời dạng FAQ + link<br>-  Không confirm hiểu đúng<br><br>**2. Khi AI không chắc (fail):**<br>-  Không hỏi lại<br>-  Không clarify intent<br>- → Trả lời chung chung<br><br>**3. Khi AI sai (fail nặng):**<br>- User biết qua nội dung không liên quan<br>-  Không có feedback loop (“có đúng không?”)<br>-  Không có cách sửa ngoài hỏi lại từ đầu<br><br>**4. Khi user mất tin (fail):**<br>-  Không có “talk to human” rõ ràng<br>-  Exit bị ẩn<br><br> Kết luận:<br>- Trust rất yếu vì thiếu recovery + transparency | **Cost:**<br>- Thấp (FAQ retrieval + rule-based + LLM nhẹ)<br><br>**Latency:**<br>- Nhanh (≈1–2s)<br><br>**Risk chính:**<br>- Trả lời sai nhưng user tưởng đúng<br>- Không hỗ trợ recovery → drop-off<br><br>**Trade-off hiện tại:**<br>- Optimize cost & speed<br>- Hy sinh trust & UX<br><br> Nếu cải thiện theo 4 paths:<br>- Cost tăng (clarification, multi-turn)<br>- Nhưng trust tăng mạnh |

---

## Automation hay augmentation?

☐ Augmentation — AI gợi ý, user quyết định cuối cùng
<br>☑ Automation — AI làm thay, user không can thiệp  

**Justify:**
- NEO đang trả lời trực tiếp như “nguồn sự thật”
- Nhưng thiếu Path 2–3–4 → automation risky
- User không biết khi AI sai

---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | User correction đi vào đâu? |  Gần như không có loop rõ ràng |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | - Số lượt chat |
| 3 | Data thuộc loại nào? ☐ User-specific · ☐ Domain-specific · ☐ Real-time · ☐ Human-judgment · ☐ Khác: ___ | ☑ Domain-specific (FAQ hàng không)<br>☑ Khác: User query logs |

---

### Có marginal value không?

Có, nhưng thấp:  
- FAQ công khai, dễ copy  
- Không có data moat, không learning loop
