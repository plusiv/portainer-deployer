# Set Image versions
ARG PYTHON_VERSION=3.8
ARG ALPINE_VERSION=3.14
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

# Set Environment Variables
ENV WORKDIR /app
ENV PORTAINER_DEPLOYER_CONF_DIR /etc/portainer-deployer
ENV PORTAINER_DEPLOYER_CONF_FILE app.conf
ENV PAKG_FOLDER portainer_deployer 

WORKDIR ${WORKDIR}

# Copy application files
COPY . .

RUN mkdir -p ${PORTAINER_DEPLOYER_CONF_DIR} && \
    cp -a ${WORKDIR}/${PAKG_FOLDER}/app.conf.example ${PORTAINER_DEPLOYER_CONF_DIR}/${PORTAINER_DEPLOYER_CONF_FILE}

# Install application and configure it 
RUN python -m pip install --upgrade pip && \ 
    python -m pip install -r requirements.txt && \
    python -m pip install . && \
    portainer-deployer config --config-path ${PORTAINER_DEPLOYER_CONF_DIR}/${PORTAINER_DEPLOYER_CONF_FILE}

# Run application
ENTRYPOINT [ "portainer-deployer" ]
