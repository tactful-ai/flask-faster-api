from fastapi import FastAPI, status, HTTPException
from app.routes.courses_routes import router as courses_router
from app.routes.auth_routes import router as auth_router

import uvicorn
app = FastAPI()

app.include_router(courses_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)
