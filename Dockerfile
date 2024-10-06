FROM python:3.12 AS builder

ADD . /app
WORKDIR /app
RUN pip install --target=/app requests


FROM bitnami/python:3.12-debian-12
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app

CMD ["/app/deploy_to_rancher.py"]