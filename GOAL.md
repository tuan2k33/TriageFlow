# 🎯 TriageFlow: Smart Issue & PR Triage Engine

Ký hiệu: ✅ đã có · 🟡 làm một phần · ⬜ chưa làm. Trạng thái tính theo dữ liệu thực trên `numpy/numpy` (33 063 issue/PR, trong đó 2 247 đang mở).

## 1. Tầm nhìn & Giá trị cốt lõi
Xây dựng công cụ phân tích, điều phối và dọn dẹp kho GitHub dựa trên **metadata và văn bản của Issues & Pull Requests**, không đọc source code hay code diff.

* **Siêu nhẹ & tiết kiệm:** chỉ dùng ngữ nghĩa văn bản (tiêu đề, mô tả, bình luận) và quan hệ đồ thị. Tiết kiệm cả request GitHub (crawl theo trang 100 mục, comment lấy theo cả repo, sync tăng dần) lẫn chi phí AI (embedding chạy local, LLM free chỉ dùng cho phần cần phán xét).
* **Giải quyết nỗi đau thực tế:** biến hàng nghìn Issue/PR hỗn loạn thành bản đồ dễ tra cứu, có thể hành động (gom nhóm, đóng, gắn nhãn) chỉ với vài cú click.
* **LLM để sau cùng:** flow chính chỉ dùng dữ liệu GitHub (văn bản, nhãn, trạng thái, liên kết GraphQL) và embedding local. Các bước LLM (tóm tắt thảo luận, phán xét close, LLM chọn nhãn, LLM đặt tên category) đã có code nhưng là tuỳ chọn, chưa dùng bây giờ.
* **Mục tiêu cuối (chưa làm bây giờ):** zero-setup, dán URL bất kỳ repo công khai là phân tích ngay, kèm giao diện đầy đủ. Xem Phase 4.

---

## 2. Luồng hoạt động (Pipeline)
1. **Input:** link repo GitHub (hiện chạy bằng lệnh).
2. **Crawl & Storage** ✅ Một lần crawl lấy mọi Issue/PR (mở và đóng), mọi comment hội thoại (comment gắn vào dòng code của PR mặc định bỏ qua), nhãn, trạng thái (`state_reason`, `merged`) vào SQLite. Liên kết "PR nào đóng issue nào" lấy từ GraphQL của GitHub. Chạy lại chỉ lấy phần thay đổi.
3. **Vectorize & Graph** 🟡 Embedding cho mọi mục (mở và đóng) ✅. Graph liên kết cứng ✅, liên kết mềm (độ tương đồng ngữ nghĩa) ⬜.
4. **Phân tích:** category chia một lần, mục mới gán vào category sẵn có ✅; gợi ý nhãn ✅; trạng thái PR của từng issue theo liên kết ⬜; gom trùng / PR cạnh tranh / tồn đọng ⬜. (Tóm tắt thảo luận và phán xét close bằng LLM: để sau.)
5. **Output & Action:** trang tra cứu một file HTML (bản đồ chủ đề, lọc nhãn, chi tiết từng mục) ✅; dashboard, danh sách đề xuất dọn dẹp, xuất script ⬜.

---

## 3. Các phân hệ nghiệp vụ

### 3.1. Tra cứu "Dây mơ rễ má" (Context Graph & Semantic Search)
Khi chọn một Issue/PR, hiển thị toàn bộ mạng lưới liên quan:
* ✅ **Liên kết cứng:** PR đóng issue (cả liên kết chính thức của GitHub lẫn từ khóa `Fixes #12`), và nhắc chéo `#56` trong mô tả, bình luận.
* ⬜ **Liên kết ngữ nghĩa:** các Issue/PR cùng một vấn đề dù không nhắc số hiệu của nhau, kể cả với mục đã đóng.
* ⬜ **Dòng chảy tiến độ:** cụm liên kết xếp theo thời gian: lỗi phát sinh ở đâu → bị báo trùng bao nhiêu lần → đã có PR xử lý chưa → PR đó mở, đã merge hay bị bỏ hoang.
* ✅ **Tìm kiếm toàn văn** trên tiêu đề, mô tả và bình luận.

### 3.2. Gợi ý Dọn dẹp, Gom gọn & Đóng (Actionable Cleanup)
* ⬜ **Gom trùng lặp:** gom các Issue cùng nội dung vào một **Master Issue** (cũ nhất hoặc nhiều tương tác nhất, sẽ chọn khi làm). Gồm cả trường hợp issue mở trùng với issue đã đóng. Đề xuất đóng bản sao kèm lý do và câu bình luận mẫu.
* ⬜ **Zombie Issues (mở mà PR đã merge giải quyết):** làm theo luật trên liên kết và trạng thái PR (có PR đã merge đóng nó, có PR đang mở, chỉ có PR bị bỏ, không có PR). Trường hợp tác giả quên link thì cần so khớp ngữ nghĩa Issue mở với PR đã merge. (Bản LLM xếp `close / needs_decision / none` đã có code, để sau.)
* ⬜ **PR cạnh tranh:** nhiều PR đang mở cùng sửa một lỗi hoặc làm một tính năng, để Maintainer chọn lọc và tránh lãng phí công review.
* ⬜ **Tồn đọng & lỗi thời:** Issue/PR không tương tác quá lâu hoặc thuộc phiên bản cũ.

### 3.3. Gợi ý Label từ nhãn sẵn có (Smart Labeling)
Chỉ **dùng lại nhãn đã có của repo** để gợi ý cho Issue/PR chưa có nhãn. Không tạo nhãn mới.
* ✅ **Dựa trên lịch sử:** láng giềng gần nhất (kNN trên embedding) của các mục đã có nhãn, tính cả mục đã đóng nên tập học lớn (hàng chục nghìn mục).
* ✅ **Thành phần bằng đếm phiếu:** 5 mục có nhãn giống nhất, mỗi mục một phiếu cho mỗi thành phần của nó, cộng phiếu từ mục có liên kết (liên kết chính thức nặng nhất); thành phần nào ≥ 2 phiếu thì gợi ý, có thể nhiều hơn một. Trên mẫu cân bằng có và không có thành phần: tìm được đúng nhãn thật cho 71% số mục có thành phần; chấm tay khoảng 88% nhãn gợi ý có liên quan tới mục (số khớp đúng tự động chỉ 0,50, là cận dưới vì nhãn thật thiếu nhiều). Không gợi ý `component: Other`, không gợi ý cho PR của bot, mục đã là Documentation thì không gợi ý `component: documentation`.
* ✅ **Hai trục gợi ý:** loại (Bug, Enhancement, Documentation...) và thành phần (`component: ...`). **Không** gợi ý nhãn quy trình (Close?, Needs decision, triaged...) vì đó là phán đoán của maintainer.
* (để sau) **LLM chọn trong danh sách cho phép:** đã có code (`suggest.py --llm`), không dùng trong flow chính.
* ✅ **Gợi ý luôn tách khỏi nhãn thật** (bảng riêng, hiển thị nét đứt), không ghi đè.
* ⬜ **Gắn hàng loạt (Bulk Apply):** xuất danh sách để áp dụng sau khi người dùng duyệt (xem Phase 3).
* ⬜ **Tự nhận diện trục nhãn của repo bất kỳ** (hiện mẫu trục đang viết theo nhãn của numpy). Thuộc Phase 4.

### 3.4. Tóm tắt thảo luận (Discussion Summary): để sau
* Đã thử: tóm tắt chỉ từ tiêu đề + mô tả + trạng thái không thêm được gì (LLM chỉ viết lại mô tả), kết cục nằm trong comment hoặc trong liên kết PR. Hiện có 710 bản tóm tắt cho mục mở của numpy, ẩn khỏi trang mặc định.
* (để sau) Mỗi thảo luận (từ 2 bình luận của người thật) nén thành một đoạn ngắn: vấn đề, điều đã thống nhất hoặc bất đồng, kết cục, kèm trạng thái (`resolved / agreed_plan / disagreement / waiting / abandoned / unclear`). Làm mục mở trước, tiếp tục được qua nhiều ngày vì hạn mức LLM free.

### 3.5. Bức tranh toàn cảnh (Triage Health Dashboard) ⬜
* **Chỉ số phân mảnh:** số Issue độc lập so với tổng số đang mở (VD: *500 Open Issues thực chất là 310 vấn đề*). Có được ngay khi gom trùng xong.
* **Điểm nóng:** cụm vấn đề được quan tâm nhiều hoặc có nhiều PR cùng nhắm tới.
* **Quick Wins:** danh sách có độ tin cậy cao có thể đóng hoặc gom ngay.

---

## 4. Nguyên tắc thiết kế
* **Không đụng tới Code:** không tải source code, không đọc diff.
* **Human-in-the-loop:** công cụ chỉ phân tích và đề xuất. Mọi thay đổi trên GitHub (đóng issue, gắn nhãn) chỉ thực thi khi người dùng duyệt, hoặc xuất ra script để tự chạy.
* **Minh bạch độ tin cậy:** mọi gợi ý đi kèm **điểm tin cậy** và **lý do ngắn**. Các ngưỡng như "> 75%" hay "> 90%" trong tài liệu này chỉ mang tính tượng trưng; ngưỡng thật sẽ hiệu chỉnh bằng dữ liệu của chính repo (các issue đã đóng với lý do `duplicate`, các cặp đã có liên kết, các mục đã có nhãn).
* **Đo trước khi tin:** mỗi bộ gợi ý phải có số đo độ chính xác trên dữ liệu có đáp án (VD: kNN và LLM được so với nhãn thật bằng cách giấu nhãn đi).
* **Gợi ý tách khỏi dữ liệu gốc:** nằm ở bảng riêng, có thể sinh lại bất kỳ lúc nào.
* **Chạy lại được và tiết kiệm:** sync tăng dần, tiếp tục được sau khi đứt hoặc hết hạn mức, LLM chỉ dùng cho mục đang mở.

---

## 5. Lộ trình
- [x] **Phase 1 (Core Data & Search):** crawler → SQLite → embedding → tìm kiếm và trang xem (bản đồ chủ đề, lọc nhiều nhãn, graph liên kết cứng).
  - [ ] Còn thiếu: cạnh ngữ nghĩa trong graph, dòng thời gian của cụm.
- [ ] **Phase 2 (Smart Cleanup):**
  - [x] Category chia một lần lúc init, mục mới gán vào category sẵn có, bản đồ ổn định.
  - [ ] Trạng thái PR của từng issue theo liên kết (thay cho phán xét close bằng LLM).
  - [ ] Gom trùng lặp + Master Issue (hiệu chỉnh ngưỡng bằng issue `duplicate` thật), zombie theo ngữ nghĩa, PR cạnh tranh, tồn đọng.
  - [ ] Dashboard sức khỏe triage.
- [ ] **Phase 3 (Labeling & Action):**
  - [x] Gợi ý nhãn: loại bằng kNN, thành phần bằng đếm phiếu (5 láng giềng + liên kết, ≥ 2 phiếu), không LLM.
  - [ ] Điểm tin cậy thống nhất cho mọi loại gợi ý.
  - [ ] Xuất báo cáo Markdown và script (`gh issue close ... --comment ...`, `gh issue edit --add-label`) để người dùng duyệt rồi chạy.
- [ ] **Phase 4 (Mục tiêu cuối, chưa làm bây giờ):** zero-setup (dán URL là chạy), tự nhận diện trục nhãn của repo bất kỳ, giao diện đầy đủ, nút thực thi trực tiếp qua GitHub Token.
