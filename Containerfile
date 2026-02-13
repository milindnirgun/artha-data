FROM python:3.14-slim

WORKDIR /workspace

# Install curl
RUN apt-get update && apt-get install -y curl vi git git-lfs
RUN git lfs install

# Copy SSH Keys into container to enable pushing to git
COPY ~/.ssh /root/
COPY bashrc /root/.bashrc

# Install duckdb
RUN curl https://install.duckdb.org | sh
RUN echo "alias duckdb='/root/.duckdb/cli/latest/duckdb'" >> /root/.bashrc

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .



