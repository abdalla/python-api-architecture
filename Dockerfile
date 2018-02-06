FROM python:3.6.4

ENV LANG en_US.utf8

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN if [ -z ${FLASK_API_CONF+x} ]; then export FLASK_API_CONF=${FLASK_API_CONF}; fi
RUN if [ -z ${FLASK_API_SQLALCHEMY_DATABASE_URI+x} ]; then export FLASK_API_SQLALCHEMY_DATABASE_URI=${FLASK_API_SQLALCHEMY_DATABASE_URI}; fi
RUN if [ -z ${FLASK_API_INIT_SAMPLE_DATA+x} ]; then export FLASK_API_INIT_SAMPLE_DATA=${FLASK_API_INIT_SAMPLE_DATA}; fi
RUN if [ -z ${FLASK_API_CLEANUP_INVALIDATED_TOKENS_INTERVAL_SECONDS+x} ]; then export FLASK_API_CLEANUP_INVALIDATED_TOKENS_INTERVAL_SECONDS=${FLASK_API_CLEANUP_INVALIDATED_TOKENS_INTERVAL_SECONDS}; fi

EXPOSE 5000 443 80 8080

CMD ["python3","run.py"]