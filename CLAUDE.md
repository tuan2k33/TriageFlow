# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mục đích

Crawl toàn bộ issue/PR (mở và đóng) của một repo GitHub vào SQLite, chỉ lấy văn bản và metadata, **không bao giờ đọc code hay diff**, rồi xếp chúng vào category, gợi ý nhãn từ nhãn sẵn có của repo, và dựng một trang HTML để xem. Từ crawl tới trang xem chỉ là phân tích dữ liệu và học máy cổ điển (embedding local, KMeans, kNN, đếm phiếu); **không có LLM** ở bất kỳ bước nào (các bước LLM cũ đã bị gỡ theo quyết định của người dùng, đừng thêm lại). Mục tiêu, phạm vi và trạng thái từng phân hệ nằm trong `GOAL.md`; đọc nó trước khi thêm tính năng. Repo dùng để thử: `numpy/numpy` (33 nghìn mục) và `tqdm/tqdm` (1,8 nghìn mục, crawl đầy đủ khoảng 90 request, hợp để thử nhanh).

## Lệnh

Cần `gh` đã đăng nhập (crawler lấy token bằng `gh auth token`, không lưu ở đâu khác). Venv của project chỉ có datasette; `torch`, `transformers`, `sklearn`, `numpy` lấy từ env chung `~/.dev/venv` (qua `_base_env.pth` do `mkproj` tạo), nên không có trong `requirements.txt`.

Flow mặc định, chạy **tuần tự**, mỗi bước chạy lại được và chỉ làm phần còn thiếu:

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy   # crawl; --full lấy lại từ đầu, --review-comments thêm comment gắn vào code (mặc định tắt)
python analyze.py $R               # embed mục mới; lần đầu (hoặc --init) chia category, các lần sau gán mục mới vào category sẵn có
python suggest.py $R               # gợi ý nhãn loại (kNN) và thành phần (bỏ phiếu); in số đo trên mẫu giữ lại
python build_html.py $R            # -> graph.html cạnh repo.db
datasette $R                       # duyệt và chạy SQL
```

Không có test suite. Cách kiểm tra:
- `suggest.py` luôn in độ chính xác: trục loại theo leave-one-out, trục thành phần theo số phiếu tối thiểu 2/3/4 trên mẫu cân bằng (600 mục có thành phần, 600 mục không), độ chính xác quy về tỉ lệ thật của repo. `--eval-only` chỉ đo, không ghi.
- Sau crawl, so `select sum(comments) from items` với số dòng `comments` có `kind='comment'`; lệch dưới 1% là bình thường (comment bị xoá hoặc thêm trong lúc crawl), lệch lớn nghĩa là crawl bị cắt.
- Gán category: xoá vài dòng `topics` của mục mở rồi chạy lại `analyze.py`; chúng phải về đúng category cũ, các mục khác giữ nguyên toạ độ.
- Mã JS trong `build_html.py` là một chuỗi Python: sau khi sửa, dựng lại trang rồi tách phần `<script>` ra file và chạy `node --check`.

## Kiến trúc

Mỗi repo một file SQLite `data/<owner>__<name>/repo.db` (`data` là symlink tới `~/.dev/data`, ngoài git). Mỗi script đọc DB và ghi bảng của riêng nó:

| Bảng | Ghi bởi | Ghi chú |
|---|---|---|
| `items` | triageflow | mọi issue/PR, mọi trạng thái (`state`, `state_reason`, `merged`) |
| `comments` | triageflow | khoá `(kind, id)`; `kind='comment'` (hội thoại) hoặc `review_comment` |
| `links` | triageflow | từ GraphQL: `closes_official` (PR đóng issue, lấy từ cả phía PR lẫn phía issue nên gồm cả PR đã bị bỏ), `duplicate_of` (issue trùng → issue gốc), `sub_issue` (con → cha); từ regex `#N`: `closes` / `mentions` (chỉ giữ số có trong `items`) |
| `fts` | triageflow | FTS5 trên tiêu đề, mô tả, comment; dựng lại mỗi lần |
| `meta` | triageflow, analyze | `repo`, các mốc sync `*_since` và ETag `*_since_etag`, `category_threshold` |
| `emb` | analyze | vector 384 chiều FP16 cho **mọi** mục; chỉ embed mục chưa có |
| `categories` | analyze | tạo **một lần** lúc init: tên, kích thước, tâm cụm (vector đã chuẩn hoá) |
| `topics` | analyze | category của **mọi** mục (`-1` = Unsorted, khi xa mọi tâm hơn ngưỡng) và toạ độ bản đồ cho mục mở |
| `neighbors`, `similar` | analyze | 5 mục giống nhất của mỗi mục; `similar` là liên kết ngữ nghĩa: cặp nằm trong top 5 của nhau (`rank` 0 = gần nhất của nhau), tính lại mỗi lần |
| `pr_status` | analyze | mỗi issue mở: `merged` / `open` / `abandoned` / `none` theo các PR đóng nó (`closes_official`, `closes`), hoặc `tracking` nếu nó có issue con; tính lại mỗi lần |
| `dup_pairs`, `dup_master` | analyze | cặp issue có thể trùng theo mức `github` / `likely` (cosine ≥ `DUP_SIM` 0,90) / `possible` (gần nhất của nhau); `dup_master`: issue nên giữ lại cho mỗi issue |
| `suggested` | suggest | `source`: `knn` (loại), `vote` (thành phần), tính lại mỗi lần |

Các ý cần đọc nhiều file mới thấy:
- **Mở và đóng:** dữ liệu gốc, `emb` và category gồm mọi trạng thái (kNN và phiếu thành phần lấy từ cả mục đã đóng); gợi ý và trang HTML chỉ làm cho mục mở.
- **Số category:** mặc định bằng số nhãn có đánh số (`00 - Bug`, `57 - Close?`...) đang dùng trên mục mở, tức độ mịn mà maintainer của repo đã chọn; numpy ra 36. Repo không có kiểu nhãn này (ít hơn 8) thì `số mục mở / 45`, kẹp 8–80. Category gom theo nội dung, **không** ánh xạ với nhãn: embedding không có cụm rõ (AMI với nhãn thành phần chỉ khoảng 0,27; tâm của các nhãn thành phần gần nhau hơn khoảng cách từ thành viên tới tâm của chính nó); KMeans hội tụ nhưng hai hạt giống chỉ giống nhau ARI ≈ 0,6, nên chia lại sẽ xáo trộn đáng kể. Gợi ý nhãn không dùng category.
- **Category ổn định:** chỉ init mới chạy KMeans và t-SNE. Các lần sau mục mới vào tâm gần nhất (cosine), mục mở mới được đặt ở trung bình toạ độ của 8 láng giềng gần nhất đã có toạ độ, nên category và bản đồ không xáo trộn. Muốn chia lại thì `--init`.
- **Đếm phiếu thành phần** (`suggest.py`, `KC=5`, `MIN_VOTES=2`): mỗi láng giềng trong 5 mục có nhãn giống nhất cho một phiếu mỗi thành phần của nó, mục có liên kết cộng thêm (`closes_official` 3, `closes` 2, `mentions` 1); thành phần nào đủ 2 phiếu thì gợi ý, nên một mục có thể nhận nhiều thành phần (trang HTML hiện số phiếu). Đã thử và bỏ: trộn có trọng số với naive Bayes trên từ khoá (chỉ 1 nhãn, tìm được 56%), quả cầu tâm + bán kính cho mỗi nhãn (các nhãn chồng nhau trong embedding, chính xác ~0,2–0,3), K=5 ≥1 phiếu (74% mục không có thành phần cũng bị gợi ý), K=7 ≥3 phiếu (chắc hơn nhưng chỉ tìm được 63%). Số đo khớp đúng là cận dưới (0,50): chấm tay 50 nhãn bị tính "sai" thì 77% vẫn liên quan tới mục, tức khoảng 88% nhãn gợi ý là có liên quan; chỉ dùng số tự động để so luật này với luật kia.
- **Liên kết ngữ nghĩa** dùng tiêu chí tương đối (top 5 hai chiều) vì ngưỡng cosine tuyệt đối không tách được; chúng phục vụ graph, dòng thời gian và gom trùng. Đã thử cho láng giềng hai chiều phiếu nặng hơn khi bỏ phiếu thành phần: không cải thiện, chỉ trượt trên cùng đường đánh đổi, nên phiếu giữ nguyên.
- **Gom trùng** chỉ xét issue với issue và không nối chuỗi các cặp (thử nối thì một nhóm lên 151 issue). Embedding là tín hiệu duy nhất: đã thử thêm độ trùng chữ tiêu đề, tên hàm, cùng tác giả và hồi quy logistic trên 5 tín hiệu, xếp hạng issue gốc không tốt hơn cosine (gốc đứng đầu 39%, trong top 5 59%, trong top 30 78%).
- **Gợi ý không bao giờ đụng vào nhãn thật** hay GitHub: chúng nằm ở bảng riêng và trang HTML hiển thị nét đứt. Giữ nguyên tắc này.
- **GitHub API:** lớp `GitHub` trong `triageflow.py` gọi thẳng REST/GraphQL bằng `urllib`: tự ngủ khi gần hết hạn mức, thử lại khi 5xx hay lỗi mạng, phân trang theo header `Link`. `stream()` sắp theo `updated` tăng dần và lưu mốc `updated_at` cuối, nên đứt ở đâu thì chạy lại tiếp từ đó; ETag của trang đầu được lưu kèm `since` đã dùng, nên lần sync không có gì mới nhận 304 (không tốn hạn mức).
- **Trang HTML** là một file tự chứa (JS thuần, không thư viện, dữ liệu nhúng dạng JSON); chỉ mục mở có toạ độ, cạnh trên bản đồ chỉ giữ cặp mà hai đầu đều đang mở, và `closes_official` hiển thị như `closes`. Dòng thời gian trong chi tiết thì gồm cả mục đã đóng (liên kết cứng hai chiều và `similar`, tối đa 60 mục).

## Lưu ý

- GitHub âm thầm dừng mọi listing ở 300 trang (30 000 dòng mỗi trang 100). `stream()` tự đi tiếp từ mốc cuối; đừng bỏ đoạn đó.
- Endpoint `pulls/comments` hay trả 502 trên repo lớn; vì thế review comment mặc định tắt. Nội dung các lần review (approve kèm nhận xét) không được crawl.
- SQLite chỉ cho một tiến trình ghi: không chạy song song hai bước ghi vào cùng DB (`database is locked`).
- Hạn mức: GitHub 5000 request/giờ (GraphQL tính riêng).
- `AXES` trong `suggest.py` (trục loại và thành phần) viết theo nhãn của numpy; repo khác sẽ in "nothing to suggest". Chỉ gợi ý hai trục này, không tạo nhãn mới, không gợi ý nhãn quy trình (Close?, Needs decision).
- GraphQL phía issue (`issue_links`): 100 issue mỗi truy vấn, khoảng 3 điểm hạn mức; toàn bộ numpy 142 truy vấn, ~9 phút, các lần sau chỉ lấy issue có thay đổi. Sự kiện "marked as duplicate" nằm trên dòng thời gian của issue **gốc** và phải đọc cả `duplicate` lẫn `canonical`. Tham chiếu chéo (`CROSS_REFERENCED_EVENT`) đã thử và bỏ: GitHub trả 502 hoặc RESOURCE_LIMITS_EXCEEDED ngay cả với 25 issue mỗi truy vấn; regex `#N` phủ phần đó.
- `data/numpy__numpy/repo.v1.db` và các file `*.csv` trong đó là của schema cũ (chỉ mục mở), đã lỗi thời.
- Khi dừng tiến trình chạy nền, dùng mẫu có `^` (`pgrep -f "^python -u triageflow.py"`); `pkill -f` không neo sẽ khớp cả chính shell đang gõ lệnh.
