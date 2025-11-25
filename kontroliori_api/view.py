from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from users_data import users
app = FastAPI()
users_by_id = {str(u["id"]): u for u in users}
@app.get("/card")
def get(_id: str) -> str:
    try:
        user = users_by_id.get(_id)
        if not user:
            return "user doesnt exist"

        tz = ZoneInfo("Asia/Tbilisi")
        now = datetime.now(tz)
        last = datetime.fromisoformat(user["last_payment_date"])
        if last.tzinfo is None:
            last = last.replace(tzinfo=tz)
        diff = now - last
        minutes = diff.total_seconds() / 60

        if minutes <= 90:
            return f"valid payment, last payment - {int(minutes)} minutes ago!"
        else:
            return f"Invalid payment, last payment - {str(minutes) + " minutes ago!" if minutes < 120 else str(int(minutes // 60)) + " hours ago!"}"

    except Exception as e:
        return str(e)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)