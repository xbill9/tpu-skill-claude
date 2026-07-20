# 🤖 Gemini Workspace Context: Gemma 4 DevOps Agents

This workspace context file is designed to help **Gemini Code Assistant** (and developer tools) quickly understand the layout, goals, tools, and integration methods of the **Gemma-4 DevOps Agents** project.

---

## 🎯 Project Overview & Role

This repository provides a set of **Model Context Protocol (MCP) servers** representing specialized AI DevOps/SRE agents. They serve two main purposes:
1. **Infrastructure Operations:** Starting, stopping, configuring, scaling, and benchmarking Gemma 4 serving stacks (Ollama or vLLM) on Local, GPU, and TPU environments.
2. **Log & SRE Diagnostics:** Utilizing the self-hosted Gemma 4 models to analyze system/cloud logs and generate remediation suggestions.

---

## 📂 Quick Navigation

Here are the key entrypoints in the codebase:
- **Root Makefile:** [Makefile](file:///home/xbill/gemma4-tips/Makefile) (manages actions across all agents)
- **GPU Agent (12B QAT L4 / Gen2):**
  - Server source: [g2-4-12B-qat-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/g2-4-12B-qat-L4-devops-agent/server.py)
  - Details: [g2-4-12B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/g2-4-12B-qat-L4-devops-agent/GEMINI.md) & [g2-4-12B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/g2-4-12B-qat-L4-devops-agent/README.md)
- **GPU Agent (12B 6000):**
  - Server source: [gpu-12B-6000-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-12B-6000-devops-agent/server.py)
  - Details: [gpu-12B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-6000-devops-agent/GEMINI.md) & [gpu-12B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-6000-devops-agent/README.md)
- **GPU Agent (12B L4):**
  - Server source: [gpu-12B-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-12B-L4-devops-agent/server.py)
  - Details: [gpu-12B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-L4-devops-agent/GEMINI.md) & [gpu-12B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-L4-devops-agent/README.md)
- **GPU Agent (12B QAT L4):**
  - Server source: [gpu-12B-qat-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-12B-qat-L4-devops-agent/server.py)
  - Details: [gpu-12B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-L4-devops-agent/GEMINI.md) & [gpu-12B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-L4-devops-agent/README.md)
- **GPU Agent (12B QAT MTP 6000):**
  - Server source: [gpu-12B-qat-mtp-6000-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-6000-devops-agent/server.py)
  - Details: [gpu-12B-qat-mtp-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-6000-devops-agent/GEMINI.md) & [gpu-12B-qat-mtp-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-6000-devops-agent/README.md)
- **GPU Agent (12B QAT MTP L4):**
  - Server source: [gpu-12B-qat-mtp-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-L4-devops-agent/server.py)
  - Details: [gpu-12B-qat-mtp-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-L4-devops-agent/GEMINI.md) & [gpu-12B-qat-mtp-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-L4-devops-agent/README.md)
- **GPU Agent (26B 6000):**
  - Server source: [gpu-26B-6000-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent/server.py)
  - Details: [gpu-26B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent/GEMINI.md) & [gpu-26B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent/README.md)
- **GPU Agent (26B L4):**
  - Server source: [gpu-26B-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-26B-L4-devops-agent/server.py)
  - Details: [gpu-26B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-26B-L4-devops-agent/GEMINI.md) & [gpu-26B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-26B-L4-devops-agent/README.md)
- **GPU Agent (26B QAT L4):**
  - Server source: [gpu-26B-qat-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-26B-qat-L4-devops-agent/server.py)
  - Details: [gpu-26B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-26B-qat-L4-devops-agent/GEMINI.md) & [gpu-26B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-26B-qat-L4-devops-agent/README.md)
- **GPU Agent (31B 6000):**
  - Server source: [gpu-31B-6000-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent/server.py)
  - Details: [gpu-31B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent/GEMINI.md) & [gpu-31B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent/README.md)
- **GPU Agent (31B L4):**
  - Server source: [gpu-31B-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-31B-L4-devops-agent/server.py)
  - Details: [gpu-31B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-31B-L4-devops-agent/GEMINI.md) & [gpu-31B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-31B-L4-devops-agent/README.md)
- **GPU Agent (31B QAT L4):**
  - Server source: [gpu-31B-qat-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent/server.py)
  - Details: [gpu-31B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent/GEMINI.md) & [gpu-31B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent/README.md)
- **GPU Agent (4B 6000):**
  - Server source: [gpu-4B-6000-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent/server.py)
  - Details: [gpu-4B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent/GEMINI.md) & [gpu-4B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent/README.md)
- **GPU Agent (4B L4):**
  - Server source: [gpu-4B-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent/server.py)
  - Details: [gpu-4B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent/GEMINI.md) & [gpu-4B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent/README.md)
- **GPU Agent (4B QAT L4):**
  - Server source: [gpu-4B-qat-L4-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-4B-qat-L4-devops-agent/server.py)
  - Details: [gpu-4B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-4B-qat-L4-devops-agent/GEMINI.md) & [gpu-4B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-4B-qat-L4-devops-agent/README.md)
- **GPU Agent (6000):**
  - Server source: [gpu-6000-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent/server.py)
  - Details: [gpu-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent/GEMINI.md) & [gpu-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent/README.md)
- **GPU Agent (vLLM L4):**
  - Server source: [gpu-vllm-devops-agent/server.py](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent/server.py)
  - Details: [gpu-vllm-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent/GEMINI.md) & [gpu-vllm-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent/README.md)
- **Local Agent (2B):**
  - Server source: [local-2B-devops-agent/server.py](file:///home/xbill/gemma4-tips/local-2B-devops-agent/server.py)
  - Details: [local-2B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/local-2B-devops-agent/GEMINI.md) & [local-2B-devops-agent/README.md](file:///home/xbill/gemma4-tips/local-2B-devops-agent/README.md)
- **Local Agent (31B default):**
  - Server source: [local-devops-agent/server.py](file:///home/xbill/gemma4-tips/local-devops-agent/server.py)
  - Details: [local-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/local-devops-agent/GEMINI.md) & [local-devops-agent/README.md](file:///home/xbill/gemma4-tips/local-devops-agent/README.md)
- **macOS Agent (2B):**
  - Server source: [mac-2B-devops-agent/server.py](file:///home/xbill/gemma4-tips/mac-2B-devops-agent/server.py)
  - Details: [mac-2B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/mac-2B-devops-agent/GEMINI.md) & [mac-2B-devops-agent/README.md](file:///home/xbill/gemma4-tips/mac-2B-devops-agent/README.md)
- **macOS Agent (4B):**
  - Server source: [mac-4B-devops-agent/server.py](file:///home/xbill/gemma4-tips/mac-4B-devops-agent/server.py)
  - Details: [mac-4B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/mac-4B-devops-agent/GEMINI.md) & [mac-4B-devops-agent/README.md](file:///home/xbill/gemma4-tips/mac-4B-devops-agent/README.md)
- **TPU Agent (12B MTP v6e-1):**
  - Server source: [tpu-12B-mtp-v6e1-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-12B-mtp-v6e1-devops-agent/server.py)
  - Details: [tpu-12B-mtp-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-mtp-v6e1-devops-agent/GEMINI.md) & [tpu-12B-mtp-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-mtp-v6e1-devops-agent/README.md)
- **TPU Agent (12B Quant v6e-1):**
  - Server source: [tpu-12B-quant-v6e1-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-12B-quant-v6e1-devops-agent/server.py)
  - Details: [tpu-12B-quant-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-quant-v6e1-devops-agent/GEMINI.md) & [tpu-12B-quant-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-quant-v6e1-devops-agent/README.md)
- **TPU Agent (12B v6e-1):**
  - Server source: [tpu-12B-v6e1-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent/server.py)
  - Details: [tpu-12B-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent/GEMINI.md) & [tpu-12B-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent/README.md)
- **TPU Agent (12B v6e-4):**
  - Server source: [tpu-12B-v6e4-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-12B-v6e4-devops-agent/server.py)
  - Details: [tpu-12B-v6e4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e4-devops-agent/GEMINI.md) & [tpu-12B-v6e4-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e4-devops-agent/README.md)
- **TPU Agent (26B v6e-1):**
  - Server source: [tpu-26B-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent/server.py)
  - Details: [tpu-26B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent/GEMINI.md) & [tpu-26B-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent/README.md)
- **TPU Agent (2B v6e-1):**
  - Server source: [tpu-2B-v6e1-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-2B-v6e1-devops-agent/server.py)
  - Details: [tpu-2B-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e1-devops-agent/GEMINI.md) & [tpu-2B-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e1-devops-agent/README.md)
- **TPU Agent (2B v6e-4):**
  - Server source: [tpu-2B-v6e4-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-2B-v6e4-devops-agent/server.py)
  - Details: [tpu-2B-v6e4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e4-devops-agent/GEMINI.md) & [tpu-2B-v6e4-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e4-devops-agent/README.md)
- **TPU Agent (31B v6e-1):**
  - Server source: [tpu-31B-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent/server.py)
  - Details: [tpu-31B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent/GEMINI.md) & [tpu-31B-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent/README.md)
- **TPU Agent (4B v6e-1):**
  - Server source: [tpu-4B-v6e1-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-4B-v6e1-devops-agent/server.py)
  - Details: [tpu-4B-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e1-devops-agent/GEMINI.md) & [tpu-4B-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e1-devops-agent/README.md)
- **TPU Agent (4B v6e-4):**
  - Server source: [tpu-4B-v6e4-devops-agent/server.py](file:///home/xbill/gemma4-tips/tpu-4B-v6e4-devops-agent/server.py)
  - Details: [tpu-4B-v6e4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e4-devops-agent/GEMINI.md) & [tpu-4B-v6e4-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e4-devops-agent/README.md)

---

## 🛠 Development Workflow & Makefile Tasks

For developer convenience, the root [Makefile](file:///home/xbill/gemma4-tips/Makefile) aggregates tasks across all sub-agents:

```bash
# Run 'make clean', 'make test', 'make lint', or 'make install' to invoke it on all agents
make install   # Prepares dependencies for all servers
make lint      # Standardizes code formatting
make test      # Validates server initializations and mock tests
```

---

## 🔗 Integration with Gemini CLI via LiteLLM Proxy

You can redirect your standard Gemini CLI commands to run against the private self-hosted Gemma 4 models in this repository. This allows developers to use their own self-hosted inference engines under the hood.

> [!NOTE]
> Below are the configurations to route local or cloud endpoints via a LiteLLM Proxy.

### 1. Install LiteLLM Proxy
```bash
pip install 'litellm[proxy]'
```

### 2. Configure LiteLLM
Choose the configuration based on which agent endpoint you wish to target.

#### Option A: Target Local Agent (Ollama/vLLM)
Create a `litellm_config.yaml`:
```yaml
model_list:
  - model_name: "gemma4-local"
    litellm_params:
      model: "openai/gemma4:e2b"
      api_base: "http://localhost:8000/v1"
      api_key: "none"
    router_settings:
      model_group_alias:
        "gemini-2.0-flash": "gemma4-local"
        "gemini-2.0-flash-lite": "gemma4-local"
        "gemini-1.5-flash": "gemma4-local"
        "gemini-1.5-pro": "gemma4-local"
```

#### Option B1: Target Cloud Run GPU Agent (RTX 6000 Config)
Create a `litellm_config.yaml`:
```yaml
model_list:
  - model_name: "gemma4-gpu-6000"
    litellm_params:
      model: "openai/google/gemma-4-26B-it"
      api_base: "https://your-cloud-run-url/v1"
      api_key: "none"
    router_settings:
      model_group_alias:
        "gemini-2.0-flash": "gemma4-gpu-6000"
        "gemini-2.0-flash-lite": "gemma4-gpu-6000"
        "gemini-1.5-flash": "gemma4-gpu-6000"
        "gemini-1.5-pro": "gemma4-gpu-6000"
```

#### Option B2: Target Cloud Run GPU Agent (L4 Config)
Create a `litellm_config.yaml`:
```yaml
model_list:
  - model_name: "gemma4-gpu-l4"
    litellm_params:
      model: "openai/google/gemma-4-E4B-it"
      api_base: "https://your-cloud-run-url/v1"
      api_key: "none"
    router_settings:
      model_group_alias:
        "gemini-2.0-flash": "gemma4-gpu-l4"
        "gemini-2.0-flash-lite": "gemma4-gpu-l4"
        "gemini-1.5-flash": "gemma4-gpu-l4"
        "gemini-1.5-pro": "gemma4-gpu-l4"
```

#### Option C: Target Cloud TPU Agent
Create a `litellm_config.yaml`:
```yaml
model_list:
  - model_name: "gemma4-tpu"
    litellm_params:
      model: "openai/google/gemma-4-31B-it"
      api_base: "http://YOUR_TPU_IP_ADDRESS:8000/v1"
      api_key: "none"
    router_settings:
      model_group_alias:
        "gemini-2.0-flash": "gemma4-tpu"
        "gemini-2.0-flash-lite": "gemma4-tpu"
        "gemini-1.5-flash": "gemma4-tpu"
        "gemini-1.5-pro": "gemma4-tpu"
```

### 3. Run Proxy & Export Variables
Run the proxy locally:
```bash
litellm --config litellm_config.yaml --port 4000
```
Then configure your shell environment:
```bash
export GOOGLE_GEMINI_BASE_URL="http://localhost:4000"
export GEMINI_API_KEY="local-proxy-token"
# Select model target corresponding to option chosen
export GEMINI_MODEL="google/gemma-4-31B-it" # Or google/gemma-4-E2B-it / google/gemma-4-26B-it / google/gemma-4-E4B-it
```

---

## 🔧 Technical Standards for vLLM & Gemma 4 Tool Calling
When managing TPU/GPU deployments or customizing vLLM serving, ensure the following vLLM serving parameters are applied for stable Gemma 4 tool integration:
- **Optimization flags:** `--tensor-parallel-size 8` (TPU v6e-8), `--disable_chunked_mm_input`, `--max-model-len 16384`.
- **Tool Parsing:** `--enable-auto-tool-choice`, `--tool-call-parser gemma4`, and `--reasoning-parser gemma4` to enable native function calling compatibility.
- **Multimodal configuration:** `--limit-mm-per-prompt '{"image":4,"audio":1}'` and `--max_num_batched_tokens 4096`.
- **Universal SRE Help:** All agents expose a standardized `get_help` tool providing details on active configuration environment variables and all exposed tools.

## 📊 Benchmarking & Analysis Standards
When aggregating or executing benchmark analysis in the codebase:
- **Ignore Boilerplate Templates:** The default `benchmark_results.csv` files generated in the subdirectories (with MD5 hash `edaf3f0fcb3e213750bed5fe4bb9a0cb`) are template placeholders. Exclude these from statistics and instead analyze real run results such as `grid_benchmark_results.csv`, `matrix_benchmark_results.csv`, or `benchmark_sweep_results.csv`.
- **Dependency Portability:** Avoid assuming third-party analysis libraries like `pandas` are installed in the workspace environment. Prefer standard libraries (e.g., `csv`, `json`) for data parsing and aggregation scripts.

