FROM python:3.12-slim

WORKDIR /app

# Cloudtype containers run without a writable root home. Keep Streamlit and
# Matplotlib runtime files in /tmp and disable telemetry file writes.
ENV HOME=/tmp \
    MPLCONFIGDIR=/tmp/matplotlib \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8501

CMD ["sh", "-c", "streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port ${PORT:-8501} --server.headless true --browser.gatherUsageStats false"]
