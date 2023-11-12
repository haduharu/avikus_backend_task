FROM python:3.7
WORKDIR /usr/src/avikus_backend
COPY ./app ./app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install pytest pytest-asyncio
RUN pip3 install httpx
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]