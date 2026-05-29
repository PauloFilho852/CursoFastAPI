from fastapi import Depends, FastAPI,Header , HTTPException, Query, status, Path
from models import Curso

app = FastAPI(title="Curso de API", description="API do curso de FastAPI", version="1.0.0")

cursos: dict[int, dict] = {
    1: {"id": 1, "nome": "Python", "duracao": 40, "valor": 100.0},
    2: {"id": 2, "nome": "JavaScript", "duracao": 30, "valor": 80.0},
    3: {"id": 3, "nome": "Java", "duracao": 50, "valor": 120.0},
}

def criar_id_curso() -> int:
    if cursos:
        return max(cursos.keys()) + 1
    return 1


@app.get("/cursos", description="Obter a lista de cursos disponíveis", summary="Lista de cursos", response_model=dict[int, dict])
async def get_cursos(header: str = Header(None)):
    if header == "admin":
        return cursos
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")

#GET com query params
@app.get("/cursos/buscar" )
async def buscar_cursos(nome: str = None, duracao: int = Query(None, gt=29)):
    resultados = []
    for curso in cursos.values():
        if nome and nome.lower() not in curso["nome"].lower():
            continue
        if duracao and curso["duracao"] != duracao:
            continue
        resultados.append(curso )
    return resultados

#GET com path params
@app.get("/cursos/{curso_id}")
async def get_curso(curso_id: int = Path(..., title="ID do Curso", description="ID do curso a ser obtido", gt=0, lt=4)):
    curso = cursos.get(curso_id)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    return curso


@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def create_curso(curso: Curso, id: int = Depends(criar_id_curso)):
    curso.id = id
    cursos[id] = curso
    return curso


@app.put("/cursos/{curso_id}", status_code=status.HTTP_200_OK)
async def update_curso(curso_id: int, curso: Curso):
    if curso_id not in cursos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    curso.id = curso_id
    cursos[curso_id] = curso
    return curso


@app.delete("/cursos/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int):
    if curso_id not in cursos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    del cursos[curso_id]
    return None



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
