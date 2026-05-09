FROM python

RUN pip install PyJWT
RUN pip install requests
RUN apt update
RUN apt install -y dcmtk

COPY . /app

CMD ["python3", "/app/upload_data.py", "trial3", "/data"]