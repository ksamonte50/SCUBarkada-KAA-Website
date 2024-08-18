# used for creating the image in Docker
# image is used for Cloud Run
FROM python:3.12

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

CMD exec gunicorn --chdir ./app --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app