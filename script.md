---
Tôi muốn tạo 1 Agent AI trợ giảng sử dụng API LLM của Openai model gpt-4o-mini cho khóa học "Lập trình C/C++ cơ bản"
Với problem statement chính như sau:
Problem Statement: AI Trợ Giảng (Online TA) Tự Động Hóa Quá Trình Hỗ Trợ Học Viên
Vấn đề: Trong các khóa học trực tuyến (đặc biệt là các môn lập trình, công nghệ), tỷ lệ học viên trên mỗi Trợ giảng (TA) quá cao. Học viên thường xuyên gặp vướng mắc ở các lỗi thực hành cơ bản hoặc có câu hỏi lặp đi lặp lại, nhưng thời gian học lại phân tán (thường vào đêm khuya).

Hiện trạng: Khi học viên vướng bug hoặc không hiểu slide, họ gửi câu hỏi lên group chat hoặc forum khóa học và phải chờ từ 4 đến 24 tiếng để TA người thật phản hồi. Thời gian chờ đợi này làm đứt gãy mạch học và gây nản chí. Ở chiều ngược lại, các TA bị quá tải, kiệt sức vì ngày nào cũng phải đi lướt trả lời thủ công hàng chục câu hỏi giống hệt nhau (ví dụ: xin link tài liệu, lỗi cài đặt môi trường cơ bản).

Giải pháp AI (Đầu ra): Hệ thống AI Online TA hoạt động 24/7 tích hợp thẳng vào nền tảng chat/forum của khóa học. Khi có câu hỏi, hệ thống lập tức phân luồng:

Tự động trả lời ngay các câu hỏi thủ tục, cung cấp tài liệu.

Tra cứu trực tiếp vào kho dữ liệu nội bộ (slide, bài giảng, file code mẫu) của khóa đó để phân tích lỗi và gợi ý hướng sửa cho học viên.

Chỉ "leo thang" (escalate) và tag tên TA người thật vào những ca quá phức tạp, kèm theo báo cáo tóm tắt lỗi để TA xử lý nhanh hơn.

Từ chối những câu hỏi không liên quan đến khóa học
Vì sao "pain point" này đủ đau và đủ tốt để làm?
Nỗi đau thực tế từ 2 phía: Học viên thì đau vì "chờ đợi", TA thì đau vì "lặp lại và quá tải". Giải quyết được 1 lúc 2 tập user.

Tính khả thi cực cao: Hoàn toàn có thể build một luồng LangGraph hoặc ReAct mượt mà cho bài này. Một Agent và các tool để có thể xử lý được công việc của một TA

Impact (Tác động): Giảm ngay 80% khối lượng công việc cho dàn TA, và giảm thời gian chờ của học viên từ tính bằng "giờ" xuống tính bằng "giây".
