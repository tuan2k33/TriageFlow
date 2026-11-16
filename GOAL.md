# 🎯 TriageFlow: Smart Issue & PR Triage Engine

Ký hiệu: ✅ đã có · 🟡 làm một phần · ⬜ chưa làm. Trạng thái tính theo dữ liệu thực trên `numpy/numpy` (33 063 issue/PR, trong đó 2 247 đang mở).

## 1. Tầm nhìn & Giá trị cốt lõi
Xây dựng công cụ phân tích, điều phối và dọn dẹp kho GitHub dựa trên **metadata và văn bản của Issues & Pull Requests**, không đọc source code hay code diff.

* **Siêu nhẹ & tiết kiệm:** chỉ dùng ngữ nghĩa văn bản (tiêu đề, mô tả, bình luận) và quan hệ đồ thị. Tiết kiệm cả request GitHub (crawl theo trang 100 mục, comment lấy theo cả repo, sync tăng dần) lẫn chi phí tính toán (embedding chạy local trên một GPU nhỏ).
* **Giải quyết nỗi đau thực tế:** biến hàng nghìn Issue/PR hỗn loạn thành danh sách dễ lọc và tra cứu, có thể hành động (gom nhóm, đóng, gắn nhãn) chỉ với vài cú click.
* **Không LLM:** từ crawl tới kết quả cuối chỉ là phân tích dữ liệu và học máy cổ điển trên dữ liệu GitHub (văn bản, nhãn, trạng thái, liên kết GraphQL) và embedding local. Các bước LLM từng thử (tóm tắt thảo luận, phán xét close, LLM chọn nhãn, LLM đặt tên category) đã bị gỡ.
* **Mục tiêu cuối (chưa làm bây giờ):** zero-setup, dán URL bất kỳ repo công khai là phân tích ngay, kèm giao diện đầy đủ. Xem Phase 4.

---

## 2. Luồng hoạt động (Pipeline)
1. **Input:** link repo GitHub (hiện chạy bằng lệnh).
2. **Crawl & Storage** ✅ Một lần crawl lấy mọi Issue/PR (mở và đóng), mọi comment hội thoại (comment gắn vào dòng code của PR mặc định bỏ qua), nhãn, trạng thái (`state_reason`, `merged`) vào SQLite. Liên kết do chính GitHub ghi nhận lấy qua GraphQL: PR nào đóng issue nào (kể cả PR đã bị bỏ), issue nào được đánh dấu trùng với issue nào, issue con của issue nào. Chạy lại chỉ lấy phần thay đổi.
3. **Vectorize & Links** ✅ Embedding cho mọi mục (mở và đóng). Liên kết cứng và liên kết ngữ nghĩa (hai mục nằm trong top 5 giống nhất của nhau).
4. **Phân tích:** category chia một lần, mục mới gán vào category sẵn có ✅; gợi ý nhãn ✅; trạng thái PR của từng issue theo liên kết ✅; gom trùng, zombie, PR cạnh tranh, tồn đọng ✅.
5. **Output & Action:** trang tra cứu một file HTML (bộ lọc, danh sách mục mở, chi tiết từng mục kèm dòng thời gian) ✅; trang tổng quan, báo cáo Markdown và script `gh` để duyệt ✅.

---

## 3. Các phân hệ nghiệp vụ

### 3.1. Tra cứu "Dây mơ rễ má" (Context Graph & Semantic Search)
Khi chọn một Issue/PR, hiển thị toàn bộ mạng lưới liên quan:
* ✅ **Liên kết cứng:** PR đóng issue (cả liên kết chính thức của GitHub lẫn từ khóa `Fixes #12`), đánh dấu trùng và issue cha/con do GitHub ghi nhận, và nhắc chéo trong mô tả, bình luận (`#56`, `gh-56`, URL đầy đủ của cùng repo).
* ✅ **Liên kết ngữ nghĩa:** các Issue/PR cùng một vấn đề dù không nhắc số hiệu của nhau, kể cả với mục đã đóng. Tiêu chí: hai mục nằm trong top 5 giống nhất của nhau (ngưỡng cosine tuyệt đối không tách được: mục nào cũng có láng giềng ở ~0,87, còn issue và PR sửa nó chỉ ~0,81). Trên numpy: 35 nghìn cặp, 15% đã có sẵn liên kết cứng; cặp là láng giềng gần nhất của nhau thì 40% đã có liên kết cứng, phần còn lại đọc tay đa số đúng là cùng vấn đề. So với 77 cặp GitHub ghi nhận là trùng: 35 cặp (45%) là liên kết ngữ nghĩa, 44 cặp (57%) nằm trong top 5 một chiều; đây là thước đo cho bước gom trùng.
* ✅ **Dòng chảy tiến độ:** trong chi tiết từng mục, mọi mục có liên kết cứng hoặc ngữ nghĩa với nó (cả mở lẫn đóng) xếp theo thời gian: lỗi phát sinh ở đâu → bị báo trùng bao nhiêu lần → đã có PR xử lý chưa → PR đó mở, đã merge hay bị bỏ hoang.
* ✅ **Tìm kiếm toàn văn** trên tiêu đề, mô tả và bình luận.

### 3.2. Gợi ý Dọn dẹp, Gom gọn & Đóng (Actionable Cleanup)
* ✅ **Gom trùng lặp:** ✅ ba mức tin cậy cho cặp issue: GitHub đã đánh dấu trùng (numpy: 74 cặp), rất có thể trùng (độ giống ≥ 0,92; chấm tay ~79% là cùng vấn đề, còn khoảng 0,91–0,92 chỉ ~29%; nếu issue cũ hơn đã đóng thì đề xuất là "kiểm tra tái phát" chứ không phải đóng), có thể trùng (là issue gần nhất của nhau; chấm tay ~42%, còn lại là cùng chủ đề). **Master Issue** là issue gốc GitHub ghi nhận, nếu không thì issue cũ nhất trong các cặp trực tiếp (không nối chuỗi, vì chuỗi trôi từ "cùng vấn đề" sang "cùng chủ đề"). Gồm cả issue mở trùng với issue đã đóng (94 trong 135 ca). Giới hạn đo được (embedding cũ): chỉ tìm lại được 15% (mức ≥ 0,90) đến 28% (gần nhất của nhau) số cặp trùng đã biết; embedding mới đọc cả comment đưa issue gốc lên đầu 47% (cũ 36%); tên hàm, chữ trong tiêu đề, cùng tác giả không cải thiện xếp hạng. ✅ Đề xuất đóng bản sao kèm lý do và câu bình luận mẫu nằm trong `report.md` và `actions.sh`.
* ✅ **Zombie Issues (mở mà PR đã merge giải quyết):** ✅ theo luật trên liên kết và trạng thái PR (có PR đã merge đóng nó, có PR đang mở, chỉ có PR bị bỏ, không có PR; numpy: 9 / 139 / 151 / 1617 issue mở; issue có issue con được xếp riêng là tracking), lọc được trong trang. ✅ Trường hợp tác giả quên link: issue mở và một PR đã merge tạo sau nó là gần nhất của nhau, độ giống ≥ 0,88, không có liên kết đóng (numpy: 72 issue; trên issue đã đóng có PR biết trước luật này đúng 87%, chấm tay 20 issue mở: 10 đã sửa thật, 6 sửa một phần, 4 chỉ liên quan).
* ✅ **PR cạnh tranh:** hai PR đang mở cùng có liên kết đóng một issue, hoặc hai PR mở rất giống nhau (≥ 0,92) của hai tác giả khác nhau (cùng tác giả là chuỗi PR, không tính). numpy: 5 + 3 cặp.
* ✅ **Tồn đọng:** lọc theo lần hoạt động cuối (trong 1 năm, 1–3 năm, 3–5 năm, trên 5 năm) thay cho một ngưỡng cố định; numpy: 728 mục mở im lặng trên 5 năm. ⬜ Nhận biết "thuộc phiên bản cũ" chưa làm.

### 3.3. Gợi ý Label từ nhãn sẵn có (Smart Labeling)
Chỉ **dùng lại nhãn đã có của repo** để gợi ý cho Issue/PR chưa có nhãn. Không tạo nhãn mới.
* ✅ **Dựa trên lịch sử:** láng giềng gần nhất (kNN trên embedding) của các mục đã có nhãn, tính cả mục đã đóng nên tập học lớn (hàng chục nghìn mục).
* ✅ **Thành phần bằng đếm phiếu:** 5 mục có nhãn giống nhất, mỗi mục một phiếu cho mỗi thành phần của nó, cộng phiếu từ mục có liên kết (liên kết chính thức nặng nhất); thành phần nào ≥ 2 phiếu thì gợi ý, có thể nhiều hơn một. Trên mẫu cân bằng có và không có thành phần: tìm được đúng nhãn thật cho 71% số mục có thành phần; chấm tay khoảng 88% nhãn gợi ý có liên quan tới mục (số khớp đúng tự động chỉ 0,50, là cận dưới vì nhãn thật thiếu nhiều). Không gợi ý `component: Other`, không gợi ý cho PR của bot, mục đã là Documentation thì không gợi ý `component: documentation`.
* ✅ **Phạm vi:** mọi mục mở còn thiếu loại hoặc thiếu thành phần (numpy: 1613 mục, 503 gợi ý loại và 803 gợi ý thành phần), không chỉ mục chưa có nhãn nào.
* ✅ **Hai trục gợi ý:** loại (Bug, Enhancement, Documentation...) và thành phần (`component: ...`). **Không** gợi ý nhãn quy trình (Close?, Needs decision, triaged...) vì đó là phán đoán của maintainer.
* ✅ **Gợi ý luôn tách khỏi nhãn thật** (bảng riêng, hiển thị nét đứt), không ghi đè.
* ✅ **Gắn hàng loạt (Bulk Apply):** `report.py` xuất lệnh `gh issue edit --add-label` cho từng gợi ý, để người dùng duyệt rồi chạy.
* 🟡 **Repo bất kỳ:** không còn cần mẫu trục viết tay. Repo không theo kiểu nhãn của numpy thì mọi nhãn đang dùng là ứng viên, và mỗi nhãn chỉ được gợi ý từ số phiếu mà phép thử giấu nhãn đúng ít nhất một nửa; nhãn không đoán được từ nội dung (đa số nhãn quy trình) tự rơi ra. tqdm: 9/21 nhãn được giữ, 465 gợi ý. ⬜ Chưa gom nhãn thành trục (loại, thành phần) cho repo lạ.

### 3.4. Tóm tắt thảo luận (Discussion Summary): không làm
* Cần LLM nên đã bỏ khỏi phạm vi. Đã thử trước khi bỏ: tóm tắt chỉ từ tiêu đề + mô tả + trạng thái không thêm được gì (LLM chỉ viết lại mô tả). Kết cục của một thảo luận nay đọc từ liên kết và trạng thái PR, và từ dòng thời gian của mục.

### 3.5. Bức tranh toàn cảnh (Triage Health Dashboard) ✅
* ✅ **Chỉ số phân mảnh:** số Issue độc lập so với tổng số đang mở, hiện ở góc trang (numpy: *1917 issue mở ≈ 1802 vấn đề*, tính theo mức GitHub đánh dấu và rất có thể trùng).
* ✅ **Điểm nóng:** category có nhiều bình luận nhất trên mục mở và các mục được bàn nhiều nhất, trong trang tổng quan (bấm tên repo).
* ✅ **Quick Wins:** các danh sách đề xuất xếp theo độ tin cậy trong trang tổng quan và trong `report.md` (numpy: 10 issue mở đã bị đánh dấu trùng, 14 issue có PR đóng đã merge).

---

## 4. Nguyên tắc thiết kế
* **Không đụng tới Code:** không tải source code, không đọc diff.
* **Human-in-the-loop:** công cụ chỉ phân tích và đề xuất. Mọi thay đổi trên GitHub (đóng issue, gắn nhãn) chỉ thực thi khi người dùng duyệt, hoặc xuất ra script để tự chạy.
* **Minh bạch độ tin cậy:** mọi gợi ý đi kèm **điểm tin cậy** và **lý do ngắn**. Các ngưỡng như "> 75%" hay "> 90%" trong tài liệu này chỉ mang tính tượng trưng; ngưỡng thật sẽ hiệu chỉnh bằng dữ liệu của chính repo (các issue đã đóng với lý do `duplicate`, các cặp đã có liên kết, các mục đã có nhãn).
* **Đo trước khi tin:** mỗi bộ gợi ý phải có số đo độ chính xác trên dữ liệu có đáp án (VD: gợi ý nhãn được so với nhãn thật bằng cách giấu nhãn đi).
* **Gợi ý tách khỏi dữ liệu gốc:** nằm ở bảng riêng, có thể sinh lại bất kỳ lúc nào.
* **Chạy lại được và tiết kiệm:** sync tăng dần, tiếp tục được sau khi đứt hoặc hết hạn mức.

---

## 5. Lộ trình
- [x] **Phase 1 (Core Data & Search):** crawler → SQLite → embedding → tìm kiếm và trang xem (lọc nhiều nhãn, liên kết cứng).
  - [x] Liên kết ngữ nghĩa, dòng thời gian trong chi tiết từng mục.
  - Bản đồ chấm điểm (t-SNE 2D/3D) đã làm rồi bỏ: embedding không có cụm rõ nên hình chiếu chỉ là một đám mờ, không cho thấy tương quan nào; đường biên KMeans cũng sẽ là ranh giới tuỳ ý.
- [x] **Phase 2 (Smart Cleanup):**
  - [x] Category chia một lần lúc init, mục mới gán vào category sẵn có.
  - [x] Trạng thái PR của từng issue theo liên kết (không cần LLM).
  - [x] Gom trùng lặp + Master Issue (ngưỡng chấm tay, đo lại bằng cặp trùng GitHub ghi nhận), chỉ số phân mảnh.
  - [x] Zombie theo ngữ nghĩa, PR cạnh tranh, tồn đọng.
  - [x] Trang tổng quan sức khỏe triage.
- [x] **Phase 3 (Labeling & Action):**
  - [x] Gợi ý nhãn: loại bằng kNN, thành phần bằng đếm phiếu (5 láng giềng + liên kết, ≥ 2 phiếu), không LLM.
  - [x] Điểm tin cậy thống nhất: mỗi đề xuất mang tỉ lệ đúng đo được của loại đề xuất đó (so với nhãn bị giấu, với liên kết GitHub ghi nhận, hoặc chấm tay) kèm lý do.
  - [x] Xuất `report.md` và `actions.sh` (`gh issue close ... --comment ...`, `gh issue edit --add-label`; mọi dòng đều bị chú thích, người dùng bỏ chú thích dòng mình duyệt rồi chạy).
- [x] Một lệnh từ link tới kết quả (`run.py`) và web local để dán link và xem bốn kết quả (`web.py`: Browse, Report, Actions, Database).
- [ ] **Phase 4 (Mục tiêu cuối, chưa làm bây giờ):** zero-setup (dán URL là chạy), tự nhận diện trục nhãn của repo bất kỳ, giao diện đầy đủ, nút thực thi trực tiếp qua GitHub Token.
