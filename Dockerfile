FROM python:3.14.5-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*   # psycopg2-binary не имеет готового wheel для Python 3.14, поэтому собраю из исходников
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8501
CMD ["bash", "scripts/start.sh"]