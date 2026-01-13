from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.resources.weather_resource import router as weather_router
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Health",
        "description": "Health check endpoints",
    },
    {
        "name": "Weather",
        "description": "Endpoints pour récupérer les données météo actuelles et les prévisions",
    },
]

app = FastAPI(
    title="CY Weather API",
    description="API for CY Weather application",
    version="0.1.0",
    openapi_tags=tags_metadata,
    redoc_url="/docs",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

Instrumentator().instrument(app).expose(app)

# Liste explicite des domaines autorisés
origins = [
    "https://lategardener.github.io",
    "https://lategardener.github.io/cy-weather",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Autorise GET, POST, etc.
    allow_headers=["*"],  # Autorise tous les headers
)

router = APIRouter(
    prefix="/api",
)

@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

app.include_router(router)
app.include_router(weather_router, prefix="/api")