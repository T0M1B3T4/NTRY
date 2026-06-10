FROM debian:bookworm-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tshark \
    iproute2 \
    procps && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /captures

CMD ["tail", "-f", "/dev/null"]