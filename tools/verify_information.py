"""
Tool: verify_information_exists
Kiểm tra xem thông tin có tồn tại trong Knowledge Base trước khi trả lời.

Nguyên tắc:
1. Xác định loại thông tin sinh viên hỏi (Deadline, Điểm, Về LMS, v.v.)
2. Tra cứu xem thông tin đó có trong Knowledge Base không
3. Trả về kết quả: Tìm thấy / Không tìm thấy / Nằm ở ngoài KB
"""

from langchain_core.tools import tool
from rag.retriever import search_documents


@tool
def verify_information_exists(
    query: str,
    information_category: str = "general"
) -> dict:
    """Kiểm tra xem thông tin có tồn tại trong Knowledge Base.
    
    Sử dụng trước khi trả lời câu hỏi liên quan đến:
    - Deadline (La, Project, Quiz, Exam)
    - Cách tính điểm (Grading rubric)
    - Chính sách khóa học (Plagiarism, Attendance, etc.)
    - Thông tin khóa học (Schedule, Contact, etc.)
    
    Args:
        query: Câu hỏi/thông tin cần tìm kiếm
        information_category: Loại thông tin (deadline, grading, policy, schedule, other)
    
    Returns:
        {
            "found": bool,
            "confidence": float (0-1),
            "source": str (Knowledge Base / LMS / Other),
            "data": str (nội dung tìm được),
            "recommendation": str (gợi ý hành động tiếp theo)
        }
    """
    try:
        # Tra cứu trong Knowledge Base
        results = search_documents(query, k=3)
        
        if not results:
            return {
                "found": False,
                "confidence": 0.0,
                "source": "Unknown",
                "data": None,
                "recommendation": "Không tìm thấy thông tin trong KB. Nên escalate cho TA."
            }
        
        # Có kết quả tìm được
        top_result = results[0]
        confidence = 0.7  # Placeholder, trong thực tế sẽ dùng similarity score
        
        # Xác định source
        source = top_result.metadata.get("source", "Knowledge Base")
        if "lms" in query.lower() or "lms" in str(source).lower():
            source = "LMS"
        
        # Kiểm tra xem thông tin có rõ ràng không
        if len(top_result.page_content) < 50:
            recommendation = "Thông tin có nhưng chưa rõ ràng. Nên hỏi thêm TA để chắc chắn."
        else:
            recommendation = "Thông tin tìm được, có thể trả lời dựa trên KB."
        
        return {
            "found": True,
            "confidence": confidence,
            "source": source,
            "data": top_result.page_content[:200] + "..." if len(top_result.page_content) > 200 else top_result.page_content,
            "recommendation": recommendation
        }
    
    except Exception as e:
        return {
            "found": False,
            "confidence": 0.0,
            "source": "Error",
            "data": None,
            "recommendation": f"❌ Lỗi tra cứu: {str(e)}"
        }
