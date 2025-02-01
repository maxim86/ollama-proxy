# Ollama Proxy

Ollama Proxy is a lightweight proxy service built with Flask. This guide provides essential steps to build and run the application using Docker. This proxy will remove the reasoning information (inside <think/> tag) from the model response. Build as a simple workaround for deepseek model being too explicit 

## Prerequisites

- Docker installed on your machine.

## Steps to Build and Run Container

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/ollama-proxy.git
cd ollama-proxy
```

Replace `https://github.com/your-repo/ollama-proxy.git` with your project's GitHub URL.

### 2. Build the Docker Image

```bash
docker build -t ollama-proxy .
```

### 3. Run the Docker Container

Run the container using the following command:

```bash
docker run -d \
    --name ollama-proxy-container \
    -p 11435:11435 \
    -e OLLAMA_API_KEY=your_api_key_here \
    -e OLLAMA_SERVER=http://your_ollama_server:11434 \
    ollama-proxy
```

### 4. Access the Proxy

Once the container is running, you can access the proxy at:

- **Localhost:** `http://localhost:11435`

## Environment Variables

| Variable              | Description                                      | Default Value       |
|-----------------------|--------------------------------------------------|---------------------|
| `OLLAMA_API_KEY`      | Your API key for accessing Ollama.               | (Optional)          |
| `OLLAMA_SERVER`       | URL of your Ollama server.                        | `http://localhost:11434` |
| `OLLAMA_PROXY_PORT`   | Port on which the proxy will run.                 | `11435`             |
| `OLLAMA_PROXY_HOST`   | Host address to bind the proxy.                   | `0.0.0.0`           |

**Note:** Replace placeholders like `your_api_key_here`, `your_ollama_server`, etc., with actual values.

---

Feel free to customize this template based on your specific requirements!