# Book Management API

REST API quản lý **sách**, **tác giả**, và **thể loại**, xây dựng với [FastAPI](https://fastapi.tiangolo.com/), SQLAlchemy 2.x và SQLite.

## Yêu cầu

- Python **3.10+** (khuyến nghị 3.11+)

## Cài đặt

```bash
cd pythonFastAPI
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu hình cơ sở dữ liệu

URL mặc định là SQLite file `book.db` trong thư mục project (`app/core/config.py`). Đổi `SQLALCHEMY_DATABASE_URL` trong code hoặc mở rộng config (biến môi trường) nếu cần.

## Migration (Alembic)

Tạo / cập nhật bảng từ thư mục gốc repository:

```bash
alembic -c alembic.ini upgrade head
```

Cấu hình script: `alembic.ini` (thư mục migration: `migration/`).

## Chạy server

```bash
uvicorn app.main:app --reload
```

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoint chính

| Prefix | Mô tả |
|--------|--------|
| `/authors` | CRUD tác giả |
| `/categories` | CRUD thể loại |
| `/books` | CRUD sách; danh sách hỗ trợ lọc `author_id`, `category_id`, `year`, `keyword` (tìm trong tiêu đề và mô tả) |

Response sách (`BookResponse`) gồm thông tin lồng **author** và **category** khi lấy chi tiết, tạo, cập nhật, hoặc liệt kê.

## Cấu trúc thư mục (rút gọn)

```
app/
  main.py              # FastAPI app, mount router
  api/endpoints/     # author, book, category
  core/config.py     # cài đặt (DB URL, …)
  db/                # engine, session, Base
  model/             # SQLAlchemy models
  schemas/           # Pydantic
migration/             # Alembic revisions
alembic.ini
```

## License

Dự án mẫu / cá nhân — bổ sung file license nếu công khai ngoài mạng.
