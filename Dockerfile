FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install uv
RUN uv sync
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "mock_api.src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
