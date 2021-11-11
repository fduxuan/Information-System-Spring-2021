FROM registry.cn-hangzhou.aliyuncs.com/xzzzh/alpine-python3:3.7.4

WORKDIR /backend
ADD requirements.txt .
RUN apk --update --no-cache add alpine-sdk gcc g++ make libffi-dev openssl-dev libtool  libldap

RUN echo '[global]' >> /etc/pip.conf && \
    echo 'index-url = https://mirrors.ustc.edu.cn/pypi/web/simple' >> /etc/pip.conf && \
    echo 'timeout = 6000' >> /etc/pip.conf && \
    echo 'format = columns' >> /etc/pip.conf && \
    echo 'no-cache-dir = false' >> /etc/pip.conf && \
    pip3 install -r requirements.txt

VOLUME /everything

ENV MONGO_URL=mongodb://bobo_mongo
ENV REDIS_URL=redis://bobo_redis
ENV LANG="en_US"
ENV MONGO_DATABASE="bobo"
ENV MINIO_ENDPOINT="locaohost:9000"
ENV MINIO_ACCESS_KEY="bobo"
ENV MINIO_SECRET_KEY="bobobobo"
ENV MINIO_SECURE=false




ADD . /backend
CMD ["bash", "start.sh"]