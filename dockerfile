FROM python:3.10

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3","entrypoint.py"]
