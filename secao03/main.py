from fastapi import FastAPI

app = FastAPI()

cursos: dict[int, dict] = {
    1: {"id": 1, "nome": "Python", "duracao": 40, "valor": 100.0},
    2: {"id": 2, "nome": "JavaScript", "duracao": 30, "valor": 80.0},
}


@app.get("/cursos")
async def get_cursos():
    return cursos


@app.get("/cursos/{curso_id}")
async def get_curso(curso_id: int):
    return cursos.get(curso_id, {"message": "Curso não encontrado"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
