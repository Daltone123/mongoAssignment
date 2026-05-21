FROM python:3.11-slim

# Set up a generic non-root user required by Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements and install dependencies using --user flag
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the rest of the application files
COPY --chown=user . .

# Expose required container port
EXPOSE 7860

# Run using Gunicorn web server bound to Hugging Face's port
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
