ARG PYTHON_VERSION=3.8
ARG ALPINE_VERSION=3.14
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

ENV WORKDIR /app
ENV SRC_DIR ${WORKDIR}/portainer_deployer
ENV CONFIG_PATH /etc/pdcli

WORKDIR ${WORKDIR}

COPY . .

RUN mkdir -p ${CONFIG_PATH}

RUN touch ${SRC_DIR}/.env && \
        echo "[CONFIG]" >> ${SRC_DIR}/.env && \
        echo "PATH_TO_CONFIG=$CONFIG_PATH/app.conf" >> ${SRC_DIR}/.env

RUN pip install -e .

ENTRYPOINT [ "portainer-deployer" ]




