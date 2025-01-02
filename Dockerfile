ARG BASE_REGISTRY="docker.io"
ARG BASE_IMAGE="python"
ARG BASE_TAG="3.10.15-bookworm"

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG} as build

SHELL ["/bin/bash", "-c"]

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV TZ=Asia/Singapore

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get -y update && \
    apt-get install --no-install-recommends -y ffmpeg && \
    apt-get clean && rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/* && apt-get -y autoremove && \
    rm -rf /var/cache/apt/archives/

COPY requirements.txt .

RUN python -m venv /venv && \
    source /venv/bin/activate && \
    python -m pip install --upgrade --no-cache-dir pip && \
    python -m pip install --no-cache-dir -r requirements.txt

ENV PATH="/venv/bin:${PATH}"

WORKDIR /workdir
ADD /clearvoice /workdir/clearvoice

WORKDIR /workdir/clearvoice
RUN ["python", "-c", "from clearvoice import ClearVoice", "ClearVoice(task='speech_enhancement', model_names=['MossFormer2_SE_48K'])"]

ENTRYPOINT ["bash"]