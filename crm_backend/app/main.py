from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.routes import auth, users, companies, contacts, leads, deals, activities, tasks, dashboard

app=FastAPI(title=settings.app_name,version=settings.app_version,description="CRM REST API built with FastAPI and PostgreSQL")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list or ["*"],allow_credentials=False if settings.cors_origins == "*" else True,allow_methods=["*"],allow_headers=["*"])

@app.exception_handler(HTTPException)
async def http_exception_handler(request:Request,exc:HTTPException):
    return JSONResponse(status_code=exc.status_code,content={"success":False,"error":{"code":f"HTTP_{exc.status_code}","message":str(exc.detail)}})

@app.exception_handler(Exception)
async def unhandled_exception_handler(request:Request,exc:Exception):
    return JSONResponse(status_code=500,content={"success":False,"error":{"code":"INTERNAL_SERVER_ERROR","message":"An unexpected error occurred"}})

@app.get("/",)
async def entry(): return {"Message":"CRM Backend System is running"}

@app.get("/health",tags=["Health"])
async def health(): return {"status":"ok"}

for router in [auth.router,users.router,companies.router,contacts.router,leads.router,deals.router,activities.router,tasks.router,dashboard.router]:
    app.include_router(router,prefix=settings.api_v1_prefix)
