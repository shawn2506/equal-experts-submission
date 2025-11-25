FROM python:3.12-alpine

WORKDIR /usr/src/doublee

RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
