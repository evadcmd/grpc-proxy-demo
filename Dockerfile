FROM python:3.9 AS server
ENV APPDIR /opt/
WORKDIR ${APPDIR}
# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
# Copy using poetry.lock* in case it doesn't exist yet
COPY pyproject.toml poetry.lock* ${APPDIR}
# install python lib
RUN poetry install --no-dev --no-root
# copy src && run the server
COPY grpc_sample ${APPDIR}grpc_sample
ENTRYPOINT ["python", "-m", "grpc_sample.server"]


FROM envoyproxy/envoy-dev AS proxy
COPY envoy.yaml /etc/envoy/envoy.yaml
CMD /usr/local/bin/envoy -c /etc/envoy/envoy.yaml