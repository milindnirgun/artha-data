FROM python:3.14-slim

WORKDIR /workspace

# Install curl
RUN apt-get update && apt-get install -y curl git
RUN apt-get install -y vi


# Install duckdb
RUN curl https://install.duckdb.org | sh
RUN echo "alias duckdb='/root/.duckdb/cli/latest/duckdb'" >> /root/.bashrc

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .



