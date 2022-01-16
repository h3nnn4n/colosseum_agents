FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP agent

# FIXME: Binding to 0 is probably unecessary
CMD ["flask", "run", "--port=80"]
