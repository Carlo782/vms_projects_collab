import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uvicorn.logging import DefaultFormatter

from variamos_security import load_keys, is_authenticated, has_roles, has_permissions, SessionUser, VariamosSecurityException, variamos_security_exception_handler

import uuid
from src.db_connector import get_db, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.model.modelDAO import UserDao, ProjectDao
from pydantic import BaseModel

# Configure logging
formatter = DefaultFormatter()
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[handler])
logger = logging.getLogger(__name__)

class TokenRequest(BaseModel):
    user_id: uuid.UUID


class ShareProjectInput(BaseModel):
    user_id: str
    project_id: str

class ConfigurationInput(BaseModel):
    project_json: dict
    id_feature_model: str
    config_name: str
    id: str


class ConfigurationInput2(BaseModel):
    id_feature_model: str
    id: str

app = FastAPI()
origins = [
    "*",
    "https://app.variamos.com/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_exception_handler(VariamosSecurityException, variamos_security_exception_handler)

@app.get("/version")
async def getVersion():
    return {"transactionId": "1", "message": "vms_projects 1.25.2.14.14"}

@app.get("/testdb")
async def testDb():
    return project_DAO.get_template_projects()

@app.on_event("startup")
async def iniciar_app():
    print("Se está inicializando la conexión con la base de datos")
    db = SessionLocal()
    global user_DAO
    global project_DAO
    user_DAO = UserDao(db)
    project_DAO = ProjectDao(db)
    load_keys()


@app.on_event("shutdown")
def shutdown_event():
    close_db()


def close_db():
    db = SessionLocal()  # Aquí obtienes la sesión
    db.close()


@app.post("/saveProject", dependencies=[Depends(is_authenticated)])
async def guardar_modelo(request: Request, project_dict: dict):
    template=False
    user_id = request.state.user.id
    print("intento guardar modelo")
    project_id=project_dict['id']
    if project_id == None:
        print("project id is none")
        return project_DAO.create_project(project_dict, user_id)
    else:
        print("project is updated")
        return project_DAO.update_project(project_dict, user_id)


@app.get("/getProjects", dependencies=[Depends(is_authenticated)])
async def obtener_modelos(request: Request):
    user_id = request.state.user.id
    return user_DAO.get_projects(user_id)

@app.get("/getTemplateProjects", dependencies=[Depends(is_authenticated)])
async def obtener_modelos_template():
    return project_DAO.get_template_projects()

@app.get("/getProject", dependencies=[Depends(is_authenticated)])
async def obtener_modelo(project_id: str):
    return project_DAO.get_by_id(project_id)


@app.post("/shareProject", dependencies=[Depends(is_authenticated)])
async def compartir_modelo(data: ShareProjectInput):
    return project_DAO.share_project(data.project_id, data.user_id)


@app.get("/usersProject", dependencies=[Depends(is_authenticated)])
async def obtener_usuarios_proyecto(request: Request, project_id: str):
    user_id = request.state.user.id
    return project_DAO.get_users(project_id, user_id)


@app.get("/findUser")
async def buscar_usuario_email(user_mail: str, db: Session = Depends(get_db)):
    return user_DAO.get_by_email(user_mail)


@app.get("/permissionProject")
async def obtener_permisos(project_id: str, db: Session = Depends(get_db)):
    return None

@app.put("/updateProjectName", dependencies=[Depends(is_authenticated)])
async def update_project_name_endpoint(project_dict: dict):
    return project_DAO.update_project_name(project_dict)

@app.delete("/deleteProject", dependencies=[Depends(is_authenticated)])
async def delete_project_endpoint(project_dict: dict):
    return project_DAO.delete_project(project_dict)

@app.post("/addConfiguration", dependencies=[Depends(is_authenticated)])
def add_configuration(project_id: str, config_input: ConfigurationInput):
    try:
        return project_DAO.add_configuration(project_id, config_input.project_json, config_input.id_feature_model, config_input.config_name)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/deleteConfiguration", dependencies=[Depends(is_authenticated)])
def delete_configuration(project_id: str, model_id : str, configuration_id: str):
    try:
        return project_DAO.delete_configuration_from_project(project_id, model_id, configuration_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getConfiguration", dependencies=[Depends(is_authenticated)])
def get_configuration(project_id: str, configuration_id: str):
    return project_DAO.get_configuration(project_id, configuration_id)

@app.get("/getAllConfigurations", dependencies=[Depends(is_authenticated)])
def get_model_configurations(project_id: str, model_id: str):
    return project_DAO.get_model_configurations(project_id, model_id)

@app.post("/applyConfiguration2", dependencies=[Depends(is_authenticated)])
def apply_configuration2(project_id : str, model_id : str, configuration_id: str):
    return project_DAO.apply_configuration(project_id, model_id, configuration_id)

@app.post("/applyConfiguration", dependencies=[Depends(is_authenticated)])
def apply_configuration(project_id : str, config_input: ConfigurationInput2):
    return project_DAO.apply_configuration(project_id, config_input.id_feature_model, config_input.id)
