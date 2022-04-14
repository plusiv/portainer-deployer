# Set Image versions
ARG PYTHON_VERSION=3.8
ARG ALPINE_VERSION=3.14
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

# Set Environment Variables
ENV WORKDIR /app
ENV PORTAINER_DEPLOYER_CONF_PATH /etc/portainer_deployer

WORKDIR ${WORKDIR}

# Copy application files
COPY . .

# Install application
RUN python setup.py install

# Run application
ENTRYPOINT [ "portainer-deployer" ]
