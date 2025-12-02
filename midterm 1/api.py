from connection import DBConnection
from fastapi import FastAPI

app = FastAPI()
db = DBConnection()
async def get_count(table_name: str):
    if table_name not in ("authors", "books", "readers"):
        raise ValueError("Invalid table name")
    conn = await db.get_connection()
    try:
        return await conn.fetchval(f'SELECT COUNT(*) FROM {table_name}')
    finally:
        await conn.close()

@app.get("/authors_count")
async def authors_count():
    return {"authors_count": await get_count("authors")}

@app.get("/books_count")
async def books_count():
    return {"books_count": await get_count("books")}

@app.get("/readers_count")
async def readers_count():
    return {"readers_count": await get_count("readers")}


@app.get("/bestsellers")
async def get_bestsellers():
    conn = await db.get_connection()
    try:
        rows = await conn.fetch("""
            SELECT b.title, COUNT(br.reader_id) AS reader_count
            FROM books b
            JOIN book_readers br ON b.id = br.book_id
            GROUP BY b.id
            ORDER BY reader_count DESC
            LIMIT 3
        """)
        result = [{"title": r["title"], "reader_count": r["reader_count"]} for r in rows]
    finally:
        await conn.close()
    return result

@app.get("/flops")
async def get_flops():
    conn = await db.get_connection()
    try:
        rows = await conn.fetch("""
            SELECT b.title, COUNT(br.reader_id) AS reader_count
            FROM books b
            JOIN book_readers br ON b.id = br.book_id
            GROUP BY b.id
            ORDER BY reader_count
            LIMIT 3
        """)
        result = [{"title": r["title"], "reader_count": r["reader_count"]} for r in rows]
    finally:
        await conn.close()
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
