# 1. Base image
FROM python:3.14-slim

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat-openbsd

ENV APP=/app

# 2. Change working directory
WORKDIR $APP

# 3. Copy requirements.txt
COPY requirements.txt $APP

# 4. Install requirements
RUN pip3 install -r requirements.txt

# 5. Copy the rest of the files
COPY . $APP

# 6. Expose port
EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

# 7. Set run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

