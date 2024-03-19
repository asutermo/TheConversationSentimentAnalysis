FROM python:3.9

COPY requirements_cpu.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV PORT=5000
ENV QUART_DIR=/app
ENV QUART_APP=main:app

COPY /app/ $QUART_DIR
WORKDIR /app

ENTRYPOINT hypercorn --reload --bind 0.0.0.0:$PORT --workers 1 --root-path $QUART_DIR $QUART_APP
EXPOSE $PORT

