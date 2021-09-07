FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app

RUN pip install -r ./requirements.txt

WORKDIR ./

CMD ["uvicorn", "main:app", "--reload"]