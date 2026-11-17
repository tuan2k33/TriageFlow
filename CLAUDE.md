# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mục đích

Crawl toàn bộ issue/PR (mở và đóng) của một repo GitHub vào SQLite, chỉ lấy văn bản và metadata, **không bao giờ đọc code hay diff**, rồi xếp chúng vào category, gợi ý nhãn từ nhãn sẵn có của repo, và dựng một trang HTML để xem. Từ crawl tới trang xem chỉ là phân tích dữ liệu và học máy cổ điển (embedding local, KMeans, kNN, đếm phiếu); **không có LLM** ở bất kỳ bước nào (các bước LLM cũ đã bị gỡ theo quyết định của người dùng, đừng thêm lại). Ngoại lệ duy nhất là `tools/llm_judge.py`: người dùng muốn một model free trên OpenRouter chấm sơ các dòng của báo cáo để đỡ việc kiểm chứng bằng tay; nó nằm ngoài pipeline, chỉ ghi `judge.jsonl`, không bước nào đọc lại. Mục tiêu, phạm vi và trạng thái từng phân hệ nằm trong `GOAL.md`; đọc nó trước khi thêm tính năng. Repo dùng để thử: `numpy/numpy` (33 nghìn mục) và `tqdm/tqdm` (1,8 nghìn mục, crawl đầy đủ khoảng 90 request, hợp để thử nhanh).

## Lệnh

Cần `gh` đã đăng nhập (crawler lấy token bằng `gh auth token`, không lưu ở đâu khác). Venv của project chỉ có datasette; `torch`, `transformers`, `sklearn`, `numpy` lấy từ env chung `~/.dev/venv` (qua `_base_env.pth` do `mkproj` tạo), nên không có trong `requirements.txt`.

`python run.py <link repo hoặc owner/name>` chạy cả năm bước dưới đây theo thứ tự và in đường dẫn `repo.db`, `browse.html`, `report.md`, `actions.sh`. `python web.py [port]` mở web local (chỉ nghe ở 127.0.0.1): ô dán link gọi `run.py` và hiện log, mỗi repo có bốn trang Browse (`browse.html` trong iframe), Report, Actions, Database (mở `repo.db` chỉ đọc, có ô SQL). Từng bước, chạy **tuần tự**, mỗi bước chạy lại được và chỉ làm phần còn thiếu:

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy   # crawl; --full lấy lại từ đầu, --review-comments thêm comment gắn vào code (mặc định tắt)
python analyze.py $R               # embed mục mới; lần đầu (hoặc --init) chia category, các lần sau gán mục mới vào category sẵn có
python suggest.py $R               # gợi ý nhãn loại (kNN) và thành phần (bỏ phiếu); in số đo trên mẫu giữ lại
python report.py $R                # bảng actions + report.md và actions.sh cạnh repo.db (mọi lệnh gh đều bị chú thích)
python build_html.py $R            # -> browse.html cạnh repo.db
datasette $R                       # duyệt và chạy SQL
```

`python -m pytest tests -q` chạy kiểm tra offline (vài giây, không cần mạng hay model): một repo giả có cài sẵn các ca trùng, zombie, PR cạnh tranh đi qua analyze, suggest, report, build_html; và mẫu regex liên kết. Kiểm tra trên dữ liệu thật:
- `suggest.py` luôn in độ chính xác: trục loại theo leave-one-out, trục thành phần theo số phiếu tối thiểu 2/3/4 trên mẫu cân bằng (600 mục có thành phần, 600 mục không), độ chính xác quy về tỉ lệ thật của repo. `--eval-only` chỉ đo, không ghi.
- Sau crawl, so `select sum(comments) from items` với số dòng `comments` có `kind='comment'`; lệch dưới 1% là bình thường (comment bị xoá hoặc thêm trong lúc crawl), lệch lớn nghĩa là crawl bị cắt.
- Gán category: xoá vài dòng `topics` của mục mở rồi chạy lại `analyze.py`; chúng phải về đúng category cũ.
- Mã JS trong `build_html.py` là một chuỗi Python: sau khi sửa, dựng lại trang rồi tách phần `<script>` ra file và chạy `node --check`.

## Kiến trúc

Mỗi repo một file SQLite `data/<owner>__<name>/repo.db` (`data` là symlink tới `~/.dev/data`, ngoài git). Mỗi script đọc DB và ghi bảng của riêng nó:

| Bảng | Ghi bởi | Ghi chú |
|---|---|---|
| `items` | triageflow | mọi issue/PR, mọi trạng thái (`state`, `state_reason`, `merged`); `labels` là mảng JSON (tên nhãn có thể chứa dấu phẩy); `state='deleted'` cho mục đã bị xoá hoặc chuyển repo (`reconcile` đối chiếu danh sách mục mở với GitHub mỗi lần crawl) |
| `comments` | triageflow | khoá `(kind, id)`; `kind='comment'` (hội thoại) hoặc `review_comment` |
| `links` | triageflow | từ GraphQL: `closes_official` (PR đóng issue, lấy từ cả phía PR lẫn phía issue nên gồm cả PR đã bị bỏ), `duplicate_of` (issue trùng → issue gốc), `sub_issue` (con → cha); từ văn bản: `closes` / `mentions`, bắt `#N`, `gh-N` và URL đầy đủ của cùng repo (chỉ giữ số có trong `items`) |
| `fts` | triageflow | FTS5 trên tiêu đề, mô tả, comment; dựng lại mỗi lần |
| `meta` | triageflow, analyze | `repo`, các mốc sync `*_since` và ETag `*_since_etag`, `category_threshold` |
| `emb` | analyze | vector 384 chiều FP16 cho **mọi** mục: trung bình của embedding tiêu đề + mô tả và embedding bản tóm tắt cả thread (`digest.py`), cả hai 512 token; kèm `hash` của tiêu đề, mô tả và comment, nên mục mới, bị sửa hay có comment mới thì embed lại |
| `categories` | analyze | tạo **một lần** lúc init: tên, kích thước, tâm cụm (vector đã chuẩn hoá) |
| `topics` | analyze | category của **mọi** mục (`-1` = Unsorted, khi xa mọi tâm hơn ngưỡng) |
| `neighbors`, `similar` | analyze | 5 mục giống nhất của mỗi mục; `similar` là liên kết ngữ nghĩa: cặp nằm trong top 5 của nhau (`rank` 0 = gần nhất của nhau), tính lại mỗi lần |
| `pr_status` | analyze | mỗi issue mở: `merged` / `open` / `abandoned` / `none` theo các PR đóng nó (`closes_official`, `closes`), hoặc `tracking` nếu nó có issue con; tính lại mỗi lần |
| `dup_pairs`, `dup_master` | analyze | cặp issue có thể trùng theo mức `github` / `likely` (cosine ≥ `DUP_SIM` 0,92) / `possible` (gần nhất của nhau); `dup_master`: issue nên giữ lại cho mỗi issue |
| `zombie`, `pr_compete` | analyze | issue mở có vẻ đã được một PR merge sau đó sửa mà không link (`ZOMBIE_SIM` 0,88, gần nhất của nhau); cặp PR mở cùng đóng một issue hoặc rất giống nhau của hai tác giả khác nhau |
| `actions` | report | mọi đề xuất: `kind`, `number`, `target`, `confidence` (0–1), `reason`, `command`; tính lại mỗi lần |
| `suggested` | suggest | numpy: `axis` `type` (`source` `knn`) và `component` (`vote`); repo khác: `axis` `label` (`vote`); tính lại mỗi lần |

Các ý cần đọc nhiều file mới thấy:
- **Mở và đóng:** dữ liệu gốc, `emb` và category gồm mọi trạng thái (kNN và phiếu thành phần lấy từ cả mục đã đóng); gợi ý và trang HTML chỉ làm cho mục mở.
- **Số category:** mặc định bằng số nhãn có đánh số (`00 - Bug`, `57 - Close?`...) đang dùng trên mục mở, tức độ mịn mà maintainer của repo đã chọn; numpy ra 36. Repo không có kiểu nhãn này (ít hơn 8) thì `số mục mở / 45`, kẹp 8–80. Category gom theo nội dung, **không** ánh xạ với nhãn: embedding không có cụm rõ (AMI với nhãn thành phần chỉ khoảng 0,27; tâm của các nhãn thành phần gần nhau hơn khoảng cách từ thành viên tới tâm của chính nó); KMeans hội tụ nhưng hai hạt giống chỉ giống nhau ARI ≈ 0,6, nên chia lại sẽ xáo trộn đáng kể. Gợi ý nhãn không dùng category.
- **kNN nhãn loại** (`suggest.py`, `K=10`, gợi ý khi độ tin ≥ 0,5): dò trên embedding mới, K=3/5/10 cho phủ / chính xác 0,85/0,84, 0,82/0,86, 0,79/0,88; K từ 15 trở lên không hơn. Phiếu thành phần dò lại thì các cặp KC, m khác (7 và 3, 10 và 3) nằm trên cùng đường đánh đổi với 5 và 2, nên giữ 5 và 2.
- **Luật từ tiêu đề** (`suggest.py`, chế độ numpy): tiền tố như `BUG:`, `ENH:` → nhãn loại, và tên thành phần nằm trong tiêu đề (`f2py`, `np.ma`...) → nhãn thành phần. Luật được học từ mục có nhãn (không viết cứng), chỉ giữ luật đúng ≥ 85% trên ≥ 20 mục. numpy: tiền tố phủ 72% mục, đúng 96% (kNN trên cùng mục 90%; chỗ hai bên bất đồng thì tiền tố đúng 93%, kNN 25%), nên tiền tố đứng trước kNN; ghép lại phủ 93%, đúng 93% (kNN một mình 79% / 88%). Tên thành phần giữ 10 luật (CI, SIMD, f2py, linalg, ma, random...), đo trên mục đã có nhãn thành phần; `build`, `dtype`, `ufunc`, `documentation` bị loại vì tên chung chung.
- **Đếm phiếu thành phần** (`suggest.py`, `KC=5`, `MIN_VOTES=2`): mỗi láng giềng trong 5 mục có nhãn giống nhất cho một phiếu mỗi thành phần của nó, mục có liên kết cộng thêm (`closes_official` 3, `closes` 2, `mentions` 1); thành phần nào đủ 2 phiếu thì gợi ý, nên một mục có thể nhận nhiều thành phần (trang HTML hiện số phiếu). Đã thử và bỏ: trộn có trọng số với naive Bayes trên từ khoá (chỉ 1 nhãn, tìm được 56%), quả cầu tâm + bán kính cho mỗi nhãn (các nhãn chồng nhau trong embedding, chính xác ~0,2–0,3), K=5 ≥1 phiếu (74% mục không có thành phần cũng bị gợi ý), K=7 ≥3 phiếu (chắc hơn nhưng chỉ tìm được 63%). Số đo khớp đúng là cận dưới (0,50): chấm tay 50 nhãn bị tính "sai" thì 77% vẫn liên quan tới mục, tức khoảng 88% nhãn gợi ý là có liên quan; chỉ dùng số tự động để so luật này với luật kia.
- **Category ổn định:** chỉ init mới chạy KMeans; các lần sau mục mới vào tâm gần nhất (cosine) nên category không xáo trộn. Muốn chia lại thì `--init`.
- **Ma trận loại × thành phần** (nút Matrix trong `browse.html`, người dùng yêu cầu thay cho bản đồ): hàng là nhãn loại, cột là nhãn thành phần, ô là các mục đang mở; kích thước = số mục, màu = tỉ lệ im lặng ≥ 3 năm, viền đứt = có mục chỉ vào ô nhờ nhãn gợi ý. Mục nhiều nhãn đếm ở mọi ô. Tính hoàn toàn trong JS từ dữ liệu sẵn có, theo các bộ lọc đang chọn; bấm ô thì lọc danh sách theo ô đó.
- **Không có bản đồ:** hình chiếu t-SNE 2D/3D đã làm rồi bỏ theo quyết định của người dùng (embedding không có cụm rõ nên hình không nói lên điều gì); đừng thêm lại. `browse.html` là một file tự chứa (JS thuần, dữ liệu nhúng dạng JSON): bộ lọc, danh sách mục mở, chi tiết kèm dòng thời gian (gồm cả mục đã đóng, tối đa 60), trang tổng quan đọc bảng `actions`.
- **Liên kết văn bản:** numpy viết `gh-1234` và dán URL nhiều hơn `#1234`; chỉ bắt `#N` thì sót 25% số cặp. Câu "fixes #N" chỉ tính là `closes` khi nằm trong tiêu đề hoặc mô tả của chính mục đó; trong bình luận thì là `mentions` (numpy: GitHub xác nhận 69% câu trong mô tả PR nhưng chỉ 1% câu trong bình luận).
- **Comment đáng tiền crawl** dù chiếm 3/4 số request: 31% số tham chiếu chỉ có trong comment, và 71/77 cặp trùng GitHub ghi nhận chỉ được nhắc tới trong comment.
- **Embedding đọc cả thread** qua `digest.py`: tiêu đề, mô tả và comment không phải bot, bỏ code, traceback, trích dẫn, link và số `#N`; thread vừa 500 token thì giữ nguyên (numpy: 26 nghìn / 33 nghìn mục), dài hơn thì giữ tiêu đề và câu đầu rồi chọn câu bằng MMR (câu của maintainer và câu có "fix", "duplicate"... được cộng điểm). Không model nào viết chữ: mọi câu lấy nguyên từ thread. Vector = trung bình với embedding tiêu đề + mô tả. Đo trên liên kết GitHub của numpy (thứ hạng của đáp án đúng): trùng → issue gốc đứng đầu 47% (cách cũ chỉ tiêu đề + mô tả 256 token: 36%), issue → PR đã merge đóng nó 41% (34%). Riêng bản tóm tắt thì không giúp tìm trùng (comment lan sang chuyện khác) nên phải lấy trung bình. Chấm tay sau khi đổi (đọc mô tả và comment của maintainer, numpy): trùng ≥ 0,92 ~79% cùng vấn đề (24 cặp), zombie 10/20 đã sửa hẳn và 6/20 sửa một phần, nhãn loại K=10 20/30 đúng, 5 tranh cãi được. Gợi ý nhãn không đổi theo số tự động; chấm tay mù trên các mục hai cách bất đồng thì nhãn loại hơi kém hơn, nhãn thành phần ngang. Embed lại toàn bộ numpy khoảng 8 phút GPU.
- **Ngưỡng theo embedding:** đổi cách embed thì phải đo lại `DUP_SIM` (khớp số cặp vượt ngưỡng với embedding cũ chỉ cho điểm xuất phát; phải chấm tay: embedding mới ở 0,91 ra cùng số cặp nhưng chỉ ~54% đúng, ≥ 0,92 thì ~79%), `ZOMBIE_SIM` (luật zombie trên issue đã đóng có PR đóng đã biết: tỉ lệ PR khớp là một trong số đó) và `K` của kNN; category phải `--init` lại.
- **Liên kết ngữ nghĩa** dùng tiêu chí tương đối (top 5 hai chiều) vì ngưỡng cosine tuyệt đối không tách được; chúng phục vụ dòng thời gian và gom trùng. Đã thử cho láng giềng hai chiều phiếu nặng hơn khi bỏ phiếu thành phần: không cải thiện, chỉ trượt trên cùng đường đánh đổi, nên phiếu giữ nguyên.
- **Gom trùng** chỉ xét issue với issue và không nối chuỗi các cặp (thử nối thì một nhóm lên 151 issue). Embedding là tín hiệu duy nhất: đã thử thêm độ trùng chữ tiêu đề, tên hàm, cùng tác giả và hồi quy logistic trên 5 tín hiệu, xếp hạng issue gốc không tốt hơn cosine (gốc đứng đầu 39%, trong top 5 59%, trong top 30 78%).
- **Bố cục báo cáo (người dùng chốt):** phần đầu gồm cách báo cáo được làm ra (5 bước, lời thường), cách đọc (Confidence = điểm của thuật toán/ML cho dòng đó, 0–1, trong ngoặc sau đề xuất; `1.00` chỉ khi chắc chắn đúng, tức maintainer đã đánh dấu trùng; mọi thứ thuật toán quyết định tối đa 0,99; Check = manual check từ `manual.jsonl`, hiện trước, cộng LLM check từ `judge.jsonl`), và Tech used của mọi mục. Mỗi mục sau đó chỉ có tên và bảng. Bảng viết bằng HTML có `<colgroup>` (34/33/33%) vì bảng Markdown `|` không cố định được độ rộng cột trong bản xem trước của VS Code; `web.py` cho các dòng HTML đi qua nguyên vẹn. Mục đánh dấu trùng có Check là "checked by maintainer". Không có cột level, không có phần trăm suy ra cho từng dòng.
- **Trùng với issue đã đóng không phải đề xuất đóng:** `report.py` tách thành `check_recurrence` (lệnh chỉ là `gh issue view`), vì nếu issue cũ đã sửa xong thì issue mở có thể là lỗi tái phát. Chỉ khi issue gốc còn mở mới đề xuất đóng bản mới hơn.
- **Gợi ý không bao giờ đụng vào nhãn thật** hay GitHub: chúng nằm ở bảng riêng và trang HTML hiển thị nét đứt. Giữ nguyên tắc này.
- **GitHub API:** lớp `GitHub` trong `triageflow.py` gọi thẳng REST/GraphQL bằng `urllib`: tự ngủ khi gần hết hạn mức, thử lại khi 5xx hay lỗi mạng, phân trang theo header `Link`. `stream()` sắp theo `updated` tăng dần và lưu mốc `updated_at` cuối, nên đứt ở đâu thì chạy lại tiếp từ đó; ETag của trang đầu được lưu kèm `since` đã dùng, nên lần sync không có gì mới nhận 304 (không tốn hạn mức).

## Lưu ý

- GitHub âm thầm dừng mọi listing ở 300 trang (30 000 dòng mỗi trang 100). `stream()` tự đi tiếp từ mốc cuối; đừng bỏ đoạn đó.
- Endpoint `pulls/comments` hay trả 502 trên repo lớn; vì thế review comment mặc định tắt. Nội dung các lần review (approve kèm nhận xét) không được crawl.
- SQLite chỉ cho một tiến trình ghi: không chạy song song hai bước ghi vào cùng DB (`database is locked`).
- Hạn mức: GitHub 5000 request/giờ (GraphQL tính riêng).
- **Hai chế độ gợi ý nhãn** (`suggest.py`): repo có nhãn khớp `AXES` (numpy) thì gợi ý loại bằng kNN và thành phần bằng đếm phiếu. Repo khác đi vào `generic()`: mọi nhãn đang dùng đều là ứng viên, mỗi nhãn có số phiếu tối thiểu riêng là mức nhỏ nhất (2..10) mà phép thử giấu nhãn đúng ≥ 50% trên ≥ 10 lần gợi ý, nhãn không đạt thì không bao giờ được gợi ý (trên tqdm các nhãn quy trình như `need-feedback`, `to-review`, `duplicate` tự rơi ra). Ngưỡng chọn trên chính mẫu thử nên con số hơi lạc quan. Mặc định gợi ý cho mọi mục mở còn thiếu loại hoặc thiếu thành phần (`--unlabeled-only` để chỉ làm mục chưa có nhãn nào). Không tạo nhãn mới.
- GraphQL phía issue (`issue_links`): 100 issue mỗi truy vấn, khoảng 3 điểm hạn mức; toàn bộ numpy 142 truy vấn, ~9 phút, các lần sau chỉ lấy issue có thay đổi. Sự kiện "marked as duplicate" nằm trên dòng thời gian của issue **gốc** và phải đọc cả `duplicate` lẫn `canonical`. Tham chiếu chéo (`CROSS_REFERENCED_EVENT`) đã thử và bỏ: GitHub trả 502 hoặc RESOURCE_LIMITS_EXCEEDED ngay cả với 25 issue mỗi truy vấn; regex `#N` phủ phần đó.
- Repo nhỏ là ca biên thật: `pypa/wheel` chỉ có 26 mục mở, từng làm bước vẽ bản đồ (nay đã bỏ) hỏng. Khi đổi `analyze.py`, thử lại bằng `python run.py pypa/wheel` (crawl đầy đủ khoảng 50 request, 1 phút).
- Mức tồn đọng (hoạt động cuối trong 1 / 1–3 / 3–5 / trên 5 năm) và trang tổng quan được tính ngay trong JS của trang, không có bảng riêng; tổng quan đọc bảng `actions` nên phải chạy `report.py` trước `build_html.py`.
- Khi dừng tiến trình chạy nền, dùng mẫu có `^` (`pgrep -f "^python -u triageflow.py"`); `pkill -f` không neo sẽ khớp cả chính shell đang gõ lệnh.
