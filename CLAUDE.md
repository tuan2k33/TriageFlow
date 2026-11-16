# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mục đích

Crawl toàn bộ issue/PR (mở và đóng) của một repo GitHub vào SQLite, chỉ lấy văn bản và metadata, **không bao giờ đọc code hay diff**, rồi xếp chúng vào category, gợi ý nhãn từ nhãn sẵn có của repo, và dựng một trang HTML để xem. Flow mặc định **không dùng LLM**; các bước LLM (tóm tắt thảo luận, phán xét close, LLM chọn nhãn, LLM đặt tên category) để dành cho sau cùng và chỉ chạy khi gọi tuỳ chọn. Mục tiêu, phạm vi và trạng thái từng phân hệ nằm trong `GOAL.md`; đọc nó trước khi thêm tính năng. Repo dùng để thử: `numpy/numpy` (33 nghìn mục) và `tqdm/tqdm` (1,8 nghìn mục, crawl đầy đủ khoảng 90 request, hợp để thử nhanh).

## Lệnh

Cần `gh` đã đăng nhập (crawler lấy token bằng `gh auth token`, không lưu ở đâu khác). `OPENROUTER_API_KEY` trong `.env` chỉ cần cho các bước LLM. Venv của project chỉ có datasette; `torch`, `transformers`, `sklearn`, `numpy` lấy từ env chung `~/.dev/venv` (qua `_base_env.pth` do `mkproj` tạo), nên không có trong `requirements.txt`.

Flow mặc định, chạy **tuần tự**, mỗi bước chạy lại được và chỉ làm phần còn thiếu:

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy   # crawl; --full lấy lại từ đầu, --review-comments thêm comment gắn vào code (mặc định tắt)
python analyze.py $R               # embed mục mới; lần đầu (hoặc --init) chia category, các lần sau gán mục mới vào category sẵn có
python suggest.py $R               # gợi ý nhãn loại (kNN) và thành phần (bỏ phiếu); in số đo trên mẫu giữ lại
python build_html.py $R            # -> graph.html cạnh repo.db
datasette $R                       # duyệt và chạy SQL
```

Tuỳ chọn có LLM: `analyze.py --init --llm-names`, `suggest.py --llm` (`--eval-only` để chỉ đo), `resolve.py`, `summarize.py --only-open --max-calls N`, rồi `build_html.py --with-llm` mới hiển thị kết quả của chúng.

Không có test suite. Cách kiểm tra:
- `suggest.py` luôn in độ chính xác: trục loại theo leave-one-out, trục thành phần theo từng nguồn và từng cách trộn trên mẫu cân bằng (600 mục có thành phần, 600 mục không), độ chính xác quy về tỉ lệ thật của repo. `--eval-only` chỉ đo, không ghi.
- Sau crawl, so `select sum(comments) from items` với số dòng `comments` có `kind='comment'`; lệch dưới 1% là bình thường (comment bị xoá hoặc thêm trong lúc crawl), lệch lớn nghĩa là crawl bị cắt.
- Gán category: xoá vài dòng `topics` của mục mở rồi chạy lại `analyze.py`; chúng phải về đúng category cũ, các mục khác giữ nguyên toạ độ.
- Mã JS trong `build_html.py` là một chuỗi Python: sau khi sửa, dựng lại trang rồi tách phần `<script>` ra file và chạy `node --check`.

## Kiến trúc

Mỗi repo một file SQLite `data/<owner>__<name>/repo.db` (`data` là symlink tới `~/.dev/data`, ngoài git). Mỗi script đọc DB và ghi bảng của riêng nó:

| Bảng | Ghi bởi | Ghi chú |
|---|---|---|
| `items` | triageflow | mọi issue/PR, mọi trạng thái (`state`, `state_reason`, `merged`) |
| `comments` | triageflow | khoá `(kind, id)`; `kind='comment'` (hội thoại) hoặc `review_comment` |
| `links` | triageflow | `closes_official` (GraphQL `closingIssuesReferences`), `closes` / `mentions` (regex `#N`, chỉ giữ số có trong `items`) |
| `fts` | triageflow | FTS5 trên tiêu đề, mô tả, comment; dựng lại mỗi lần |
| `meta` | triageflow, analyze | `repo`, các mốc sync `*_since` và ETag `*_since_etag`, `category_threshold` |
| `emb` | analyze | vector 384 chiều FP16 cho **mọi** mục; chỉ embed mục chưa có |
| `categories` | analyze | tạo **một lần** lúc init: tên, kích thước, tâm cụm (vector đã chuẩn hoá) |
| `topics` | analyze | category của **mọi** mục (`-1` = Unsorted, khi xa mọi tâm hơn ngưỡng) và toạ độ bản đồ cho mục mở |
| `suggested` | suggest | `source`: `knn` (loại), `vote` (thành phần), tính lại mỗi lần; `llm` chỉ khi `--llm`, được giữ lại |
| `resolve_hints`, `summaries` | resolve, summarize | chỉ có khi chạy bước LLM; trang HTML mặc định không hiển thị |

Các ý cần đọc nhiều file mới thấy:
- **Mở và đóng:** dữ liệu gốc, `emb` và category gồm mọi trạng thái (kNN và từ khoá học từ cả mục đã đóng); gợi ý và trang HTML chỉ làm cho mục mở.
- **Số category:** mặc định bằng số nhãn có đánh số (`00 - Bug`, `57 - Close?`...) đang dùng trên mục mở, tức độ mịn mà maintainer của repo đã chọn; numpy ra 36. Repo không có kiểu nhãn này (ít hơn 8) thì `số mục mở / 45`, kẹp 8–80. Category gom theo nội dung, **không** ánh xạ với nhãn: embedding không có cụm rõ (AMI với nhãn thành phần chỉ khoảng 0,27; tâm của các nhãn thành phần gần nhau hơn khoảng cách từ thành viên tới tâm của chính nó); KMeans hội tụ nhưng hai hạt giống chỉ giống nhau ARI ≈ 0,6, nên chia lại sẽ xáo trộn đáng kể. Gợi ý nhãn không dùng category.
- **Category ổn định:** chỉ init mới chạy KMeans và t-SNE. Các lần sau mục mới vào tâm gần nhất (cosine), mục mở mới được đặt ở trung bình toạ độ của 8 láng giềng gần nhất đã có toạ độ, nên category và bản đồ không xáo trộn. Muốn chia lại thì `--init`.
- **Bỏ phiếu thành phần** (`suggest.py`): ba nguồn là kNN, nhãn thành phần của mục có liên kết (trọng số `closes_official` 3, `closes` 2, `mentions` 1) và naive Bayes trên từ khoá tiêu đề + mô tả. Script thử vài cách trộn và ngưỡng, rồi chọn cách tìm được nhiều nhất mà vẫn đạt `--min-precision` (mặc định 0,7; số đo là cận dưới vì nhiều ca "báo nhầm" là nhãn bị thiếu).
- **Gợi ý không bao giờ đụng vào nhãn thật** hay GitHub: chúng nằm ở bảng riêng và trang HTML hiển thị nét đứt. Giữ nguyên tắc này.
- **GitHub API:** lớp `GitHub` trong `triageflow.py` gọi thẳng REST/GraphQL bằng `urllib`: tự ngủ khi gần hết hạn mức, thử lại khi 5xx hay lỗi mạng, phân trang theo header `Link`. `stream()` sắp theo `updated` tăng dần và lưu mốc `updated_at` cuối, nên đứt ở đâu thì chạy lại tiếp từ đó; ETag của trang đầu được lưu kèm `since` đã dùng, nên lần sync không có gì mới nhận 304 (không tốn hạn mức).
- **LLM:** `suggest.call_llm` là chỗ gọi OpenRouter duy nhất (có thử lại); `analyze.py`, `resolve.py` và `summarize.py` nạp `suggest.py` bằng `importlib`. Model lấy từ `LLM_MODEL`, mặc định một model `:free`.
- **Trang HTML** là một file tự chứa (JS thuần, không thư viện, dữ liệu nhúng dạng JSON); chỉ mục mở có toạ độ, liên kết chỉ giữ cặp mà hai đầu đều đang mở, và `closes_official` hiển thị như `closes`.

## Lưu ý

- GitHub âm thầm dừng mọi listing ở 300 trang (30 000 dòng mỗi trang 100). `stream()` tự đi tiếp từ mốc cuối; đừng bỏ đoạn đó.
- Endpoint `pulls/comments` hay trả 502 trên repo lớn; vì thế review comment mặc định tắt. Nội dung các lần review (approve kèm nhận xét) không được crawl.
- SQLite chỉ cho một tiến trình ghi: không chạy song song hai bước ghi vào cùng DB (`database is locked`).
- Hạn mức: GitHub 5000 request/giờ (GraphQL tính riêng); OpenRouter free khoảng 1000 request/ngày, 20/phút (xem `GET https://openrouter.ai/api/v1/key`, trường `free_model_daily_requests`). Danh sách model free thay đổi; model bị gỡ thì báo 404, đổi `LLM_MODEL`. Model suy luận cần `max_tokens` cao, nếu không nội dung trả về rỗng.
- `AXES` trong `suggest.py` (trục loại và thành phần) viết theo nhãn của numpy; repo khác sẽ in "nothing to suggest". Chỉ gợi ý hai trục này, không tạo nhãn mới, không gợi ý nhãn quy trình (Close?, Needs decision).
- Tóm tắt chỉ bằng tiêu đề + mô tả + trạng thái đã được thử: LLM chỉ viết lại phần mô tả và mọi mục ra `waiting`, nên không đáng tốn call. Kết cục phải lấy từ liên kết và trạng thái PR, hoặc từ comment.
- `data/numpy__numpy/repo.v1.db` và các file `*.csv` trong đó là của schema cũ (chỉ mục mở), đã lỗi thời.
- Khi dừng tiến trình chạy nền, dùng mẫu có `^` (`pgrep -f "^python -u triageflow.py"`); `pkill -f` không neo sẽ khớp cả chính shell đang gõ lệnh.
