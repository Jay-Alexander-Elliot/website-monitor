# Stage 1: Compile and install dependencies
FROM python:3.10-slim as build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc 
WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2: Copy the compiled dependencies and application code
FROM python:3.10-slim
WORKDIR /usr/app/venv
COPY --from=build /usr/app/venv ./venv
COPY . .
ENV PATH="/usr/app/venv/bin:$PATH"
CMD [ "python", "monitor_script.py" ]
