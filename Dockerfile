FROM opencadc/astropy:3.8-slim

RUN apt-get update -y && apt-get dist-upgrade -y && \
    apt-get install -y \
       build-essential \
       git && \
    rm -rf /var/lib/apt/lists/ /tmp/* /var/tmp/*
    
RUN pip install --no-cache-dir \
    cadcdata \
    cadctap \
    caom2 \
    caom2repo \
    caom2utils \
    importlib-metadata \
    python-dateutil \
    PyYAML \
    spherical-geometry \
    vos

WORKDIR /usr/src/app

ARG OPENCADC_BRANCH=master
ARG OPENCADC_REPO=opencadc-metadata-curation
ARG PIPE_BRANCH=master
ARG PIPE_REPO=opencadc-metadata-curation

RUN pip install git+https://github.com/${OPENCADC_REPO}/caom2pipe.git@${OPENCADC_BRANCH}#egg=caom2pipe

RUN pip install git+https://github.com/${PIPE_REPO}/phangs2caom2.git@${PIPE_BRANCH}#egg=phangs2caom2

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
