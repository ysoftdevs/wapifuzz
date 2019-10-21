# We need .NET Core image for running parser
FROM mcr.microsoft.com/dotnet/core/sdk:2.1

ENV container=true

# Expose port for process monitor
EXPOSE 26002/tcp
EXPOSE 26002/udp

# Build Python 3.7.3, needed for fuzzer + OpenJDK installation for reporter
RUN apt update && apt install --yes build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev openjdk-8-jre ; rm -rf /var/lib/apt/lists/*
ADD https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz /usr/src/
RUN cd /usr/src ; tar xzf Python-3.7.3.tgz ; cd Python-3.7.3 ; ./configure --enable-optimizations ; make altinstall ; ln -s /usr/local/bin/python3.7 /usr/local/bin/python3 ; ln -s /usr/local/bin/pip3.7 /usr/local/bin/pip3

# Copy wapifuzz components into docker
COPY fuzzer /usr/local/fuzzer/fuzzer
COPY parser /usr/local/fuzzer/parser
COPY reporter /usr/local/fuzzer/reporter

# Set working directory
WORKDIR /usr/local/fuzzer/

COPY run.sh /usr/local/fuzzer/run.sh
RUN chmod +x /usr/local/fuzzer/run.sh

# Set run script as an entry point of the container
ENTRYPOINT ["/usr/local/fuzzer/run.sh"]
