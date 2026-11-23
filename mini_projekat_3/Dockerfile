FROM python:3.12-slim

WORKDIR /app

# requirements.txt se kopira prije koda zbog keširanja slojeva
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# aplikacija se ne pokreće kao root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
