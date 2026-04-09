# 🎯 Danh Sách Kịch Bản Kiểm Thử AI TA Chatbot (Test Scenarios)

Dưới đây là 10 kịch bản bao phủ toàn bộ các luồng chức năng, Knowledge Base và Escalation Triggers để bạn copy-paste và kiểm thử ứng dụng nhé.

---

    ### Kịch bản 1: Truy vấn thông tin cơ bản (Thời gian & Deadline)
    *Mục đích: Test khả năng tra cứu thông tin cụ thể liên quan tới thời gian (Sử dụng tool: get_course_info)*
> **Sinh viên:** "Dạ cho em hỏi Project 2 hạn nộp là ngày nào thế ạ?"
> **Bot (Kỳ vọng):** Trả về được ngày 27/04/2026.

    ### Kịch bản 2: Truy vấn thông tin quy chế (Policy)
*Mục đích: Test xem Bot có lấy được chi tiết vắng mặt/trừ điểm không.*
> **Sinh viên:** "Tôi đã vắng môn này 4 buổi rồi, xem giúp tôi bị trừ bao nhiêu điểm và có cảnh báo gì không?"
> **Bot (Kỳ vọng):** Nhắc đến việc vắng 1 buổi trừ 3 điểm chuyên cần. Và cảnh báo mạnh: Vắng 4 buổi sẽ BỊ CẤM THI vì quá 3 buổi. (Chức năng bạn vừa thấy thiếu đã được fix lại!).

    ### Kịch bản 3: Truy vấn Socratic (Gợi mở, không giải trực tiếp)
*Mục đích: Test tính sư phạm (Socratic method).*
> **Sinh viên:** "Con trỏ (Pointer) trong C++ là gì vậy bot? Có thể cho tôi code ví dụ về mảng con trỏ không?"
> **Bot (Kỳ vọng):** Giải thích dựa trên khái niệm slide nhưng KHÔNG đưa ra code giải bài tập hoàn chỉnh, mà chỉ đưa ví dụ cú pháp ngắn hoặc hỏi ngược lại để kiểm tra mức hiểu.

    ### Kịch bản 4: Hỏi ngoài phạm vi khóa học (Out of Scope)
*Mục đích: Ensure behavior ngoài phạm vi (Python/Đăng ký tín chỉ).*
> **Sinh viên:** "Bot ơi, thư viện Pandas trong Python dùng để xử lý dữ liệu như thế nào? Tiện thể xem giùm mình quy trình hủy học phần C++ này với, mình muốn rớt môn."
> **Bot (Kỳ vọng):** Lịch sự từ chối vì bot chuyên trị C/C++. Ngoài ra, vấn đề hủy học phần nằm ngoài quyền hạn của AI TA (Trường hợp này chatbot không được cố bịa nội dung).

    ### Kịch bản 5: Debug Code - Thiếu thông tin 🚨 (Failure Mode 1)
*Mục đích: Test rule "ép cung" yêu cầu gửi thêm code và log lỗi.*
> **Sinh viên:** "Code quản lý sinh viên của anh bị lỗi rồi, chạy không lên, em check giúp anh nha."
> **Bot (Kỳ vọng):** Dừng lại và YÊU CẦU: "Bạn vui lòng gửi thêm đoạn code bạn đang viết và nguyên văn thông báo lỗi (nếu có) để mình hỗ trợ nhé!"

    ### Kịch bản 6: Debug Code - Đầy đủ thông tin (Thành công)
*Mục đích: Kiểm tra khả năng debug và phân tích (analyze_code_error tool).*
> **Sinh viên:** "Mình chạy bài này thì bị lỗi 'Segmentation fault'. Code của mình đây: `int arr[5]; array[10] = 5;`. Lỗi ở đâu?"
> **Bot (Kỳ vọng):** Nhận diện lỗi Out of Bounds (truy cập ngoài mảng) và hướng dẫn cách khắc phục, có thể đưa ra fix giả định hoặc giải thích về cấp phát bộ nhớ.

    ### Kịch bản 7: Escalation - Trigger 1 (Yêu cầu trực tiếp)
*Mục đích: Test khả năng xin TA hỗ trợ và Popup Widget.*
> **Sinh viên:** "Tôi không hiểu gì cả. Hãy gọi giảng viên Nguyễn Văn Minh hoặc tag trợ giảng tên Hoa vào đây giúp tôi."
> **Bot (Kỳ vọng):** KHÔNG diễn giải gì lằng nhằng. Gọi ngay phiếu `Escalation Report` và màn hình bung ra Widget. Sau khi bạn chọn "Xác nhận gửi", ứng dụng sẽ in: "Đã gọi cho giảng viên, cần chờ từ 4 - 6h".

    ### Kịch bản 8: Escalation - Trigger 2 (Thiếu thông tin trầm trọng)
*Mục đích: Tra cứu một khái niệm chuyên sâu không có trong JSON nhưng ép Bot gửi.*
> **Sinh viên:** "Hãy đọc kĩ giáo trình và cho tôi biết trọng số điểm thi vòng chung kết Cuộc thi C++ sinh viên mở rộng do trường tổ chức là bao nhiêu?"
> **Bot (Kỳ vọng):** Dùng FAISS/course_info tìm, không thấy nội dung -> Lập tức tự sinh phiếu Escalation Report cho TA báo lý do "Không tìm thấy trong KB". Màn hình bung Widget xác nhận.

    ### Kịch bản 9: Escalation - Trigger 3 (Tranh chấp / Dispute kéo dài)
*Mục đích: Test logic "Lì lợm", phải cãi lại 3 lần mới hiện form.*
> **Sinh viên (Lần 1):** "Hàm malloc() trả về kiểu gì?"
> **Bot (Trả lời 1):** (Trả lời là void*)
> **Sinh viên (Lần 2):** "Bạn trả lời sai rồi, tôi không nghĩ vậy."
> **Bot (Trả lời 2):** Xin lỗi, giải thích kỹ hơn...
> **Sinh viên (Lần 3):** "Vẫn sai nhé, ý tôi hỏi là trong chuẩn C99 cơ. Bạn hiểu sai hoàn toàn rồi."
> **Bot (Kỳ vọng):** Nhận ra cự cãi 3 lần (`attempt_count = 3` -> `detect_trigger` kích hoạt). Bot ngưng cãi và nói: "Bạn có muốn mình gọi trợ giảng kiểm tra câu hỏi này cho chắc chắn không?". Mới hiện form.

    ### Kịch bản 10: Nhấp Thumbs Up / Thumbs Down Track
*Mục đích: Bấm phản hồi (Feedback) dưới mỗi câu AI trả lời.*
> **Thao tác:** Bấm 1 nút 👍 dưới câu AI bất kỳ -> Nút đó bị xám/tắt (không cho ấn đúp) -> Xem bên thanh Sidebar ở góc trái, mục **📈 THỐNG KÊ AI** đếm số lần được "Hữu ích" tăng lên 1 đơn vị. Refresh trang vẫn không mất đi (lưu cứng file json).

---
*Mẹo nhỏ: Nhấn vào nút "➕ Đoạn chat mới" ở Sidebar để clear memory hội thoại trước khi chuyển sang các kịch bản Escalation (Trigger 3) để số đếm Attempt Count được reset từ 0 nhé thầy giáo!*
