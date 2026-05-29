from fastapi import FastAPI
from routers import usuario_router, curso_router

app = FastAPI()
app.include_router(usuario_router.router, tags=["Usuários"])
app.include_router(curso_router.router, tags=["Cursos"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
