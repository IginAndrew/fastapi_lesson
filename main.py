# Импортируем FastAPI и необходимые компоненты (Request, JSONResponse)
from fastapi import FastAPI, Request
# Импортируем маршруты из отдельных модулей
from routers import user, dates, journals, auth

# Импортируем логгер loguru и UUID-генератор для уникальных идентификаторов логов
from loguru import logger
from uuid import uuid4
from fastapi.responses import JSONResponse

# Настраиваем логгер: запись в файл info.log, формат логов, уровень INFO
# Логи будут содержать ID лога, время, уровень и сообщение
logger.add("info.log", format="Log: [{extra[log_id]}:{time} - {level} - {message} ", level="INFO", enqueue=True)

# Создаем экземпляр приложения FastAPI
app = FastAPI()


# Мидлварь для логирования всех HTTP-запросов
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    # Генерируем уникальный ID для текущего запроса
    log_id = str(uuid4())
    # Устанавливаем контекст логгера с этим ID
    with logger.contextualize(log_id=log_id):
        try:
            # Передаем запрос дальше по цепочке обработки
            response = await call_next(request)
            # Если статус ответа указывает на ошибку (401, 402, 403, 404), логируем предупреждение
            if response.status_code in [401, 402, 403, 404]:
                logger.warning(f"Request to {request.url.path} failed")
            else:
                # Иначе логируем успешный запрос
                logger.info('Successfully accessed ' + request.url.path)
        except Exception as ex:
            # Логируем ошибку, если произошло исключение
            logger.error(f"Request to {request.url.path} failed: {ex}")
            # Возвращаем общий ответ об ошибке сервера
            response = JSONResponse(content={"success": False}, status_code=500)
        # Возвращаем ответ клиенту
        return response


# Основной маршрут корня ("/"), возвращает приветственное сообщение
@app.get("/")
async def welcome() -> dict:
    return {"message": "My journals API"}


# Регистрируем роутеры из отдельных модулей
app.include_router(user.router)
app.include_router(dates.router)
app.include_router(journals.router)
app.include_router(auth.router)

# Комментарий с командой запуска приложения через uvicorn
"""uvicorn main:app --reload"""