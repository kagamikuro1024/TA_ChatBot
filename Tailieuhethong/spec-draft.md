# SPEC — AI Online TA

**Nhóm:** C3-C401-Day05
**Track:** ☑ VinUni-VinSchool · ☐ Khác
**Problem statement:** Học viên chờ 4–24h để được giúp về lỗi cơ bản; TA xử lý 50–100 câu/ngày (60–70% FAQ lặp lại, kiệt sức). AI 24/7 xử lý FAQ & lỗi tự động, TA focus ca phức tạp → tiết kiệm 3–5h/ngày, học viên giảm chờ từ hours → seconds.

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Học viên** | Chờ 4–24h để được TA giúp về FAQ/lỗi cơ bản (cú pháp, môi trường, cài đặt). Pain: mạch học bị đứt, tỷ lệ bỏ cuộc cao. AI trả lời FAQ ngay (<3s), hướng dẫn debug step-by-step từ tài liệu khóa học (Socratic, không cho đáp án). | **Đúng:** FAQ được trả lời, sinh viên tiếp tục. **Sai:** AI gợi ý hướng sai → sinh viên mất thêm thời gian. **Không chắc:** Chuyện gì xảy ra? **Khôi phục:** Nút "Hỏi TA thật" luôn hiển thị, TA audit hàng tuần (50 response ngẫu nhiên, score 0/1/2 hữu ích). Giải pháp: disclaimer khi confidence <80%, escalate nếu cần. | Latency <3s (FAQ) / <10s (tech via RAG). Cost ~$0.02–0.05/câu hỏi (LLM API). Stack: Chroma vector DB + semantic search trên tài liệu khóa (slide PDF, code mẫu, FAQ markdown). Risk: mô tả lỗi mơ hồ ("code không chạy") → hint chung chung → học viên thất vọng. [?] latency thực tế |
| **TA (Hỗ trợ giảng viên)** | Xử lý 50–100 câu/ngày. 60–70% FAQ (link, lịch, quy tắc nộp) — không tạo giá trị cao, kiệt sức. AI tự trả lời FAQ, TA chỉ nhận escalation + summary. Tiết kiệm TA 3–5h/ngày → focus vào ca debug khó. | **Đúng:** Cần escalate, TA nhận context. **Sai:** Logic escalate bỏ sót câu khó hoặc escalate câu dễ. **Không chắc:** Audit như thế nào? **Khôi phục:** Audit hàng tuần: đo false positive (escalate khi không nên) + false negative (không escalate khi nên). Target <5% false negative, nếu không thì pause + retune. | Escalation rule-based + LLM confidence (threshold <60% HOẶC timeout >10s HOẶC "need help" → escalate). Dashboard monitor auto-responses. Tech: web app đơn giản + Discord/Slack API. [?] baseline escalation rate từ dữ liệu lịch sử |

**Tự động hay augmentation?** ☑ Augmentation có phần tự động
- FAQ/routine → Tự động hoàn toàn (TA không can thiệp)
- Lỗi kỹ thuật → Augment (AI hướng dẫn, sinh viên thử, TA kiểm tra chất lượng thread)
- Phức tạp/mơ hồ → Escalate với context (TA quyết định)

**Lý do:** Mô tả lỗi của user thường mơ hồ HOẶC AI confidence thấp → tự động nguy hiểm. Augmentation + escalation an toàn hơn.

**Learning signal:**

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | Correction của user đi vào đâu? | Phản ứng sinh viên (👍/👎) log mỗi response. TA sửa response sai của AI → correction dataset (versioned). Weekly error pattern report → lưu. |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | Hàng tuần: % auto-responses, F1 per intent class, false pos/neg escalation rate, student "hữu ích" rate. Top 5 failure modes by frequency. |
| 3 | Data thuộc loại nào? | ☑ Domain-specific (KB khóa học proprietary) · ☑ Human-judgment (TA labels) · ☑ Real-time (production errors) |

**Có giá trị biên tế?** Có — error patterns khóa học ("lỗi hàng đầu tuần 3 Python") không có trong public LLM. Weekly curriculum improvement report cho giảng viên là sản phẩm mới.

---

## 2. User Stories — Feature Paths

### Feature: Tự động trả lời FAQ

**Trigger:** Sinh viên post câu hỏi → Intent classifier phát hiện "FAQ" (high confidence) → FAQ Agent retrieve từ KB tĩnh → responds

| Path | Mô tả | Ví dụ |
|------|-------------|---------|
| **Tốt** | FAQ match chính xác, confidence >95%, sinh viên thấy answer + source link, đóng thread | SV: "Deadline dự án khi nào?" → AI: "Dự án deadline 2026-04-22 (từ course syllabus PDF p.3)" + link. SV ✓ hài lòng. |
| **Không chắc** | FAQ match partial hoặc nhiều candidates, show top 2 + confidence %, sinh viên chọn | SV: "Làm sao để submit?" → AI: "Cách 1: GitHub (85%) / Cách 2: Email (60%)" → SV chọn GitHub → AI giải thích. |
| **Fail** | Không match FAQ, AI says "Không có trong FAQ, hỏi TA" + escalates | SV: "Giáo viên có thể hoãn deadline của tôi không?" → AI: "Cần quyết định từ giáo viên, hỏi TA..." → escalated. TA responds. |
| **Correction** | SV rate answer 👍/👎, nếu downvote + comment → correction logged | SV downvote với comment "deadline là 04-25 chứ không phải 04-22" → system log correction → FAQ refined. |

### Feature: Hỗ trợ Debug (Lỗi Code)

**Trigger:** Sinh viên post error + code → Intent classifier phát hiện "Technical" → Retrieval+Synthesis agents search + guide

| Path | Mô tả | Ví dụ |
|------|-------------|---------|
| **Tốt** | Top-3 docs retrieved relevant, LLM synthesize 2–3 hint step-by-step, sinh viên thử, solve | SV: "ModuleNotFoundError: numpy" + code snippet → AI: "Bước 1: Check xem numpy đã cài (pip list). Bước 2: Nếu chưa, chạy pip install numpy. Bước 3: Verify với import numpy." → SV làm, works ✓. |
| **Không chắc** | Mô tả error mơ hồ, AI hỏi clarification hoặc retrieve 3 docs nhưng không chắc cái nào giúp, show all + ask SV | SV: "Code không chạy" (no error msg). AI: "Tôi tìm được 5 nguyên nhân [list]. Bạn có thể share error message?" SV add stderr → AI refine. |
| **Fail** | SV stuck dù sau guide của AI, hoặc guide sai hướng (SV test all steps, none work). SV escalate. | SV: "Thử cả steps của bạn rồi, vẫn bị AttributeError..." → SV click "Hỏi TA" → escalated với full conversation. |
| **Correction** | SV report "hint của bạn sai, đây là solution đúng" → TA validate + add to KB | SV: "AI bảo dùng .append() nhưng phải dùng .extend()." → TA confirm, KB doc update, model học. |

### Feature: Escalation Summary (TA nhận ca khó)

**Trigger:** Escalation Agent phát hiện question phức tạp cao hoặc SV explicitly request TA → tạo summary + tag @ta-team

| Path | Mô tả | Ví dụ |
|------|-------------|---------|
| **Tốt** | Summary tóm tắt, TA nhanh hiểu context, không overhead context-switching | SV question: "Tại sao cả test suite fail khi refactor X?" (complex debug). AI escalate với summary: "SV refactor Module X, test suite break (5 failures, stderr [...]).Đã thử: ...". TA read 2 min, biết full context. |
| **Không chắc** | Summary thiếu key info, TA phải read full thread anyway | Escalation: "Code bị lỗi gì đó" (generic). TA phải scroll all messages để hiểu. |
| **Fail** | TA miss escalation hoặc escalation message quá dài/buried | Escalation post nhưng TA offline, SV chờ 8h. Hoặc escalation 500 words, TA skim và misunderstand. |
| **Correction** | TA review escalation quality hàng tuần, flag bad summaries → tune system prompts | Hàng tuần: TA check 10 escalations, tìm 2 cái unclear → adjust Escalation Agent system prompt. |

---

## 3. Chỉ số Đánh giá + Ngưỡng

**Optimize precision hay recall?** ☑ Precision (tránh escalate Q tầm thường thành complex, lãng phí TA time) + ☑ Recall (không tự động trả lời Q mà không chắc, risk sai lệch)

| Chỉ số | Target | Red flag (dừng) | Cách đo |
|--------|--------|-----------------|------------|
| % tự trả lời (không escalate) | ≥60% | <40% | Count auto-responses / total Q |
| "Hữu ích" rate sinh viên | ≥75% | <60% | Thumbs up / total responses |
| Response latency (FAQ) | <3s | >5s | Latency logs |
| Response latency (Tech) | <10s | >15s | Latency logs |
| False negative escalation | <5% | >8% | TA audit hàng tuần (sample 50 auto-responses) |
| Intent classifier F1 | >85% | <75% | Hold-out test set (50 Q) |
| System uptime | ≥99% | <95% trong 2 ngày | Monitoring dashboard |

---

## 4. Top 3 Failure Modes

| # | Nguyên nhân | Hậu quả | Giải pháp |
|---|---------|-------------|-----------|
| **1. Mô tả error mơ hồ** | SV nói "code không chạy" không có stack trace, error message, hoặc minimal reproducible example (MRE). | AI give generic debugging guide (check imports, syntax, setup...). SV try all, none work. Thất vọng, escalate. TA spend 10 min extract actual error từ SV message. | Detect keyword absence (no "Error:", no code snippet) → prompt SV "Please share error message or code" before AI responds. Nếu baseline Q quá short (<20 tokens), ask thêm context. Force-escalate nếu no response sau 2 rounds. |
| **2. KB lỗi thời/conflict** | KB có old slide (v1.0) + new slide (v2.0) trong cùng vector DB. Retrieval return both → synthesis LLM confused hoặc mix old+new info. | SV follow AI advice từ old material → khác với cái giáo viên dạy bây giờ → SV miss current week's lessons. | 1) Version-mark all KB docs (slide_Week3_v2.0.pdf). 2) Weekly doc audit before course week starts. 3) Khi TA fix 1 question, mark doc "needs review" → lecturer check. 4) Nếu AI retrieve docs >3 versions cũ, flag [outdated]. |
| **3. Escalation logic miss ca khó** | Edge case question về course policy, academic integrity, grade appeal, permission request. Classifier mark "Technical" → auto-answer → SV think problem solved → sau nhận ra AI sai → trust broken. | SV learn AI không đáng tin trên policy questions. Stop dùng system hoặc làm sai dựa vào bad AI advice. | 1) Expand "escalate keywords": ["grade", "deadline", "permission", "appeal", "policy", "exception"]. 2) Lower confidence threshold cho policy-adjacent Q. 3) Weekly audit: TA flag "AI should escalate cái này" → adjust thresholds. 4) Force-escalate nếu question mention "course policy" hoặc "tôi có thể...". |

---

## 5. ROI — 3 Kịch Bản

|   | Bảo thủ | Hiện thực | Lạc quan |
|---|-------------|-----------|------------|
| **Giả định** | 1 khóa, 100 SV, 50% adopt AI, 50% helpful | 1 khóa, 150 SV, 70% adopt, 75% helpful | 3 khóa, 400 SV, 85% adopt, 80% helpful |
| **Câu hỏi/tuần** | 100 Q | 300 Q | 900 Q |
| **TA time tiết kiệm/tuần** | 4 Q × 15 phút = 1h (chỉ FAQ auto-answer, 40% các 100) | 210 Q × 60% auto = 126h save labor thủ công, ÷ TA effort = ~15h/tuần | 540 Q × 70% = 378h manual labor prevent = ~40h/tuần |
| **Chi phí/tuần** | 100 Q × $0.03 = $3 inference + $50 infra | 300 Q × $0.03 = $9 + $50 infra | 900 Q × $0.03 = $27 + $100 infra (scale) |
| **Lợi ích (TA salary equivalent)** | 1h × $25/h = $25/tuần | 15h × $25/h = $375/tuần | 40h × $25/h = $1000/tuần |
| **Net (Lợi ích - Chi phí)/tuần** | $25 - $53 = **-$28** | $375 - $59 = **+$316** | $1000 - $127 = **+$873** |
| **Lợi ích bổ sung** | — | Course completion rate ↑5% (retention) = ~7 SV × $2K/SV lifetime = $14K | Course completion ↑10% × 3 khóa = 40 SV × $2K = $80K LTV |

**Kill criteria:** Nếu (Chi phí > Lợi ích) >4 tuần HOẶC (False negative escalation > 10%) HOẶC (SV helpful rate < 60%), pause + retune.

---

## 6. Mini AI Spec (1 trang)

### Tóm tắt Sản phẩm
**AI Online TA** là hệ thống multi-agent 24/7 tự động trả lời câu hỏi SV về lập trình, escalate ca khó cho TA thật kèm context summary, và collect error patterns để cải tiến curriculum.

**Cho ai:** Chủ yếu SV (instant help, safe space to ask), secondary TA (reduce routine workload 60–70%) và giảng viên (data về common mistakes).

**AI làm gì:**
- **FAQ Agent** → retrieve answers từ static KB (schedules, links, policies) trong <3s
- **Retrieval+Synthesis Agent** → search course materials (slides, code examples, docs), guide debug bằng Socratic method (hints, không solution) trong <10s
- **Escalation Agent** → detect ambiguous/complex questions, tạo summaries, tag @ta-team
- **Intent Classifier** → route question đến agent đúng dựa FAQ vs. Technical vs. Escalate

**Tự động vs. Augment vs. Escalate:**
- ✅ Hoàn toàn tự động: FAQ (links, schedules, basic how-to)
- 🤝 Augmented: Lỗi kỹ thuật (AI guides, SV thử, TA spot-checks)
- 👤 Human-in-loop: Policy, permission, grade, complex multi-file debugging (TA owns)

**Chỉ tiêu chất lượng:**
- **Precision matters:** Tránh false escalations (lãng phí TA time) — confidence threshold ≥60% để auto-answer
- **Recall matters:** Không miss ca khó — false negative escalation <5%, TA audit hàng tuần
- **Latency:** FAQ <3s, Tech <10s (Discord API + Chroma search + LLM inference)
- **SV trust:** >75% rate AI response "hữu ích" (thumbs up), <5% false negative escalation

**Data flywheel:**
1. **Correction loop:** SV corrections (text + ratings) → TA validates → KB docs refined
2. **Pattern discovery:** Weekly error frequency report (VD: "SV tuần 3 Python struggle với list comprehensions") → giảng viên adjust course
3. **Model improvement:** Correction dataset → retrain Intent Classifier + Synthesis prompts mỗi 2 tuần

**Main risks:**
1. Mô tả error mơ hồ (SV: "code không chạy") → AI give generic advice → SV thất vọng
2. KB lỗi thời (old slides mix với new) → AI dạy sai chuyện
3. Escalation miss policy/permission questions → SV trust sai advice → damage reputation

**Giải pháp:** Force escalate on keywords (grade, permission, policy). Weekly KB audit. TA weekly audit false negatives. Confidence disclaimers khi unsure.

**Timeline:** 8-week pilot trên 1 khóa (100–150 SV). Phases: Week 1 data prep, Week 2–4 dev, Week 5–6 staging QA, Week 7–8 live + monitoring.

## Phân công

- **Hoàng Đức Nghĩa:** Canvas 
- **Nguyễn Thành Vinh:**failure modes + risk analysis → 4 UX flows mỗi cái
- **Lê văn Quang Trung:** User stories — 3 feature paths (FAQ auto-answer, debugging assist, escalation summary) 
- **Trịnh Xuân Đạt:** Eval metrics + ROI calculation + kill criteria
- **Nguyễn Trọng Minh:** Prototype research — LangGraph agent flow design + RAG pipeline setup + prompt test trên dataset 150–200 real questions

---

**Ngày:** 2026-04-08 | **Phiên bản:** 1.0 (Spec Template)