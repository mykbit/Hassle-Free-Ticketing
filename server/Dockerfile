FROM python:3.12.2

WORKDIR /backend
COPY ./ ./
RUN pip install -r requirements.txt

EXPOSE 8000
CMD sleep 5; python ./run.py

