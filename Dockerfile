# Set Image versions
ARG PYTHON_VERSION=3.8
ARG ALPINE_VERSION=3.14
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

# Set Environment Variables
ENV WORKDIR /app
ENV SRC_DIR ${WORKDIR}/portainer_deployer
ENV CONFIG_PATH /etc/pdcli

WORKDIR ${WORKDIR}

# Copy application files
COPY . .

# Create config directory
RUN mkdir -p ${CONFIG_PATH}

# Create .env file for application
RUN touch ${SRC_DIR}/.env && \
        echo "[CONFIG]" >> ${SRC_DIR}/.env && \
        echo "PATH_TO_CONFIG=$CONFIG_PATH/app.conf" >> ${SRC_DIR}/.env

# Install application
RUN pip install -e .

# Run application
ENTRYPOINT [ "portainer-deployer" ]
