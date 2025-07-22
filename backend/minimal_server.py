from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/working-test")
async def working_test():
    return {"message": "MINIMAL TEST WORKS", "success": True}

@app.get("/working-login")
async def working_login():
    return HTMLResponse("""
    <html><body style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;font-family:system-ui;padding:2rem;text-align:center">
    <h1>🚀 PostVelocity Login</h1>
    <form action="/api/auth/login" method="post" style="background:white;color:black;padding:2rem;border-radius:1rem;display:inline-block">
    <div style="margin:1rem 0"><label>Email:</label><br><input type="email" name="email" value="user@postvelocity.com" style="padding:0.5rem;width:300px"></div>
    <div style="margin:1rem 0"><label>Password:</label><br><input type="password" name="password" value="user123" style="padding:0.5rem;width:300px"></div>
    <button type="submit" style="background:#667eea;color:white;padding:1rem 2rem;border:none;border-radius:0.5rem">Login</button>
    </form></body></html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)