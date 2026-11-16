# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mục đích

Crawl toàn bộ issue/PR (mở và đóng) của một repo GitHub vào SQLite, chỉ lấy văn bản và metadata, **không bao giờ đọc code hay diff**, rồi đề xuất hành động triage: gợi ý nhãn, issue mở có thể đóng, tóm tắt thảo luận, và một trang HTML để xem. Mục tiêu, phạm vi và trạng thái từng phân hệ nằm trong `GOAL.md`; đọc nó trước khi thêm tính năng. Repo dùng để thử: `numpy/numpy` (33 nghìn mục) và `tqdm/tqdm` (1,8 nghìn mục, crawl khoảng 2 phút, hợp để thử nhanh).

## Lệnh

Cần `gh` đã đăng nhập và `OPENROUTER_API_KEY` trong `.env`. Venv của project chỉ có datasette; `torch`, `transformers`, `sklearn`, `numpy` lấy từ env chung `~/.dev/venv` (qua `_base_env.pth` do `mkproj` tạo), nên không có trong `requirements.txt`.

Pipeline, chạy **tuần tự** theo thứ tự này, mỗi bước chạy lại được và chỉ làm phần còn thiếu:

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy        # crawl; --full lấy lại từ đầu, --review-comments thêm comment gắn vào code (mặc định tắt)
python analyze.py $R                    # embedding (GPU) + chủ đề + bản đồ 2D
python suggest.py $R                    # gợi ý nhãn; --no-llm chỉ kNN, --eval-only đo kNN vs LLM trên mục đã có nhãn
python resolve.py $R                    # issue mở nhắc PR đã merge: close / needs_decision / none
python summarize.py $R --max-calls 500  # tóm tắt thảo luận; --only-open
python build_html.py $R                 # -> graph.html cạnh repo.db
datasette $R                            # duyệt và chạy SQL
```

Không có test suite. Cách kiểm tra:
- `suggest.py` luôn in độ chính xác kNN leave-one-out; `--eval-only` so thêm với LLM (tốn khoảng 3 call).
- Sau crawl, so `select sum(comments) from items` với số dòng `comments` có `kind='comment'`; lệch dưới 1% là bình thường (comment bị xoá hoặc thêm trong lúc crawl), lệch lớn nghĩa là crawl bị cắt.
- Mã JS trong `build_html.py` là một chuỗi Python: sau khi sửa, dựng lại trang rồi tách phần `<script>` ra file và chạy `node --check`.

## Kiến trúc

Mỗi repo một file SQLite `data/<owner>__<name>/repo.db` (`data` là symlink tới `~/.dev/data`, ngoài git). Mỗi script đọc DB và ghi bảng của riêng nó:

| Bảng | Ghi bởi | Ghi chú |
|---|---|---|
| `items` | triageflow | mọi issue/PR, mọi trạng thái (`state`, `state_reason`, `merged`) |
| `comments` | triageflow | khoá `(kind, id)`; `kind='comment'` (hội thoại) hoặc `review_comment` |
| `links` | triageflow | `closes_official` (GraphQL `closingIssuesReferences`), `closes` / `mentions` (regex `#N`, chỉ giữ số có trong `items`) |
| `fts` | triageflow | FTS5 trên tiêu đề, mô tả, comment; dựng lại mỗi lần |
| `meta` | triageflow | `repo` và các mốc sync `*_since` |
| `emb` | analyze | vector 384 chiều FP16 cho **mọi** mục; chỉ embed mục chưa có |
| `topics` | analyze | cụm và toạ độ 2D, **chỉ mục mở**; tính lại toàn bộ mỗi lần |
| `suggested` | suggest | `source` là `knn` (tính lại mỗi lần) hoặc `llm` (giữ lại, chỉ gọi cho mục chưa có) |
| `resolve_hints` | resolve | mỗi issue chỉ phán xét một lần |
| `summaries` | summarize | tóm tắt lại khi số comment đổi |

Các ý cần đọc nhiều file mới thấy:
- **Mở và đóng:** dữ liệu gốc và `emb` gồm mọi trạng thái (kNN học từ cả mục đã đóng); `topics`, gợi ý, phán xét và trang HTML chỉ làm cho mục mở.
- **Gợi ý không bao giờ đụng vào nhãn thật** hay GitHub: chúng nằm ở bảng riêng và trang HTML hiển thị nét đứt. Giữ nguyên tắc này.
- **LLM:** `suggest.call_llm` là chỗ gọi OpenRouter duy nhất (có thử lại); `resolve.py` và `summarize.py` nạp `suggest.py` bằng `importlib`. Model lấy từ `LLM_MODEL`, mặc định một model `:free`. Mọi bước LLM gom nhiều mục vào một call và yêu cầu trả về mảng JSON.
- **Sync tăng dần:** `stream()` trong `triageflow.py` gọi `gh api --paginate` sắp theo `updated` tăng dần, lưu mốc `updated_at` cuối vào `meta`, nên đứt ở đâu thì chạy lại tiếp từ đó.
- **Trang HTML** là một file tự chứa (JS thuần, không thư viện, dữ liệu nhúng dạng JSON); liên kết chỉ giữ cặp mà hai đầu đều đang mở, và `closes_official` hiển thị như `closes`.

## Lưu ý

- GitHub âm thầm dừng mọi listing ở 300 trang (30 000 dòng mỗi trang 100). `stream()` tự đi tiếp từ mốc cuối; đừng bỏ đoạn đó.
- Endpoint `pulls/comments` hay trả 502 trên repo lớn; vì thế review comment mặc định tắt. Nội dung các lần review (approve kèm nhận xét) không được crawl.
- SQLite chỉ cho một tiến trình ghi: không chạy song song hai bước ghi vào cùng DB (`database is locked`). `build_html.py` vẫn dùng timeout mặc định 5 giây.
- Hạn mức: GitHub 5000 request/giờ (GraphQL tính riêng); OpenRouter free khoảng 1000 request/ngày, 20/phút. Danh sách model free thay đổi; model bị gỡ thì báo 404, đổi `LLM_MODEL`. Model suy luận cần `max_tokens` cao, nếu không nội dung trả về rỗng.
- `AXES` trong `suggest.py` (trục loại và thành phần) viết theo nhãn của numpy; repo khác sẽ in "nothing to suggest". Chỉ gợi ý hai trục này, không tạo nhãn mới, không gợi ý nhãn quy trình (Close?, Needs decision).
- `data/numpy__numpy/repo.v1.db` và các file `*.csv` trong đó là của schema cũ (chỉ mục mở), đã lỗi thời.
- Khi dừng tiến trình chạy nền, dùng mẫu có `^` (`pgrep -f "^python -u triageflow.py"`); `pkill -f` không neo sẽ khớp cả chính shell đang gõ lệnh.
