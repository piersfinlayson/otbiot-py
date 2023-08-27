FROM python:3

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        wget && \
    apt clean && \
    rm -fr /var/lib/apt/lists/*

WORKDIR /usr/src/app/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./otbiot.py" ]