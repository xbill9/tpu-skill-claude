# 🚀 Gemma 4 DevOps Agents

Welcome to the **Gemma-4 DevOps Agents** workspace. This repository contains nine specialized, self-hosted AI-driven DevOps/SRE agents powered by Google's **Gemma 4** model. These agents are packaged as Model Context Protocol (MCP) servers to analyze, monitor, and troubleshoot infrastructure components.

---

## ⚡ Quick Start — set up a project in one command

`project-setup.sh` installs the `tpu-management` skill **and** registers the `tpu-devops` MCP server for any project (idempotent — re-run to refresh):

```bash
./project-setup.sh /path/to/project --project <gcp-project-id>   # one project (.mcp.json + .claude/skills)
./project-setup.sh --global                                      # all projects (~/.claude/skills + user-scope MCP)
make init TARGET=/path/to/project ARGS='--project <id>' # same, refreshing skill snapshots first
```

It uses the system `python3` (warning with a `pip install -r requirements.txt` hint if server dependencies are missing — it never creates a venv), merges the server entry into the project's `.mcp.json` without touching other servers, and prints the remaining manual steps (restart Claude Code, gcloud auth, HF token). See `./project-setup.sh --help` for all options. The installer is also bundled inside the skill itself (`mcp/project-setup.sh`), so an unzipped `dist/tpu-management-skill.zip` is self-installing.

---

## 📦 Installing the `tpu-management` Skill

Claude Code auto-discovers any skill folder containing a `SKILL.md` in two places:

- **Project-level:** `<project>/.claude/skills/tpu-management/` — available only in that project (this repo ships its own copy, so working inside this repo needs no install).
- **User-level:** `~/.claude/skills/tpu-management/` — available in every project on the machine.

Pick the install path that fits:

| Goal | Command |
| :--- | :--- |
| This machine, all projects | `make skill-install` |
| One specific project (skill **and** `tpu-devops` MCP server) | `make init TARGET=/path/to/project ARGS='--project <gcp-project-id>'` |
| All projects + user-scope MCP registration | `make init ARGS='--global'` |
| Another machine | `make skill-package`, copy `dist/tpu-management-skill.zip`, unzip into `~/.claude/skills/` |

### Install from GitHub

Clone and install (all projects on this machine):

```bash
git clone https://github.com/xbill9/tpu-skill-claude
cd tpu-skill-claude
make skill-install                                   # skill only
./project-setup.sh --global                          # skill + user-scope tpu-devops MCP server
```

Or skip the clone and install straight from the packaged zip:

```bash
curl -L -o /tmp/tpu-management-skill.zip \
  https://github.com/xbill9/tpu-skill-claude/raw/main/dist/tpu-management-skill.zip
mkdir -p ~/.claude/skills && unzip -o /tmp/tpu-management-skill.zip -d ~/.claude/skills/
~/.claude/skills/tpu-management/mcp/project-setup.sh --global   # optional: register the MCP server
```

All of these first run `make skill` (`refresh_skill.py`), which regenerates the bundled snapshot from the repo-root sources: `server.py`, `project-setup.sh`, and `requirements.txt` are copied into the skill's `mcp/` folder, and `references/tpu-builders-guide.md` is rebuilt from `tpu.md` with the embedded screenshots stripped. `SKILL.md` and `mcp/startup_script_template.sh` are hand-maintained and never overwritten.

After installing (or updating), **restart Claude Code** or start a new session so it picks up the skill. Verify with `/skills` — `tpu-management` should be listed.

Because installs are refresh-and-copy (not symlinks), an installed copy goes stale when `server.py`, `tpu.md`, or `SKILL.md` changes — rerun `make skill-install` (or `make init ...`) after editing those files.

---

## 📂 Project Structure

This workspace is organized into 31 distinct sub-agents, each tailored to a specific environment, model configuration, and serving stack:

| Sub-Agent Directory | Purpose / Role | Model Configuration | Serving Engine | Target Infrastructure |
| :--- | :--- | :--- | :--- | :--- |
| [g2-4-12B-qat-L4-devops-agent](file:///home/xbill/gemma4-tips/g2-4-12B-qat-L4-devops-agent) | Serverless cloud SRE leveraging the 12B parameter QAT model on L4 GPU via Cloud Run Gen2. | `google/gemma-4-12B-it-qat-w4a16-ct` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-12B-6000-devops-agent](file:///home/xbill/gemma4-tips/gpu-12B-6000-devops-agent) | Serverless cloud SRE running the 12B configuration on an NVIDIA RTX 6000 GPU. | `gemma-4-12B-it` | vLLM | Google Cloud Run (RTX 6000 GPU) |
| [gpu-12B-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-12B-L4-devops-agent) | Serverless cloud SRE running the 12B configuration on an NVIDIA L4 GPU. | `gemma-4-12B-it` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-12B-qat-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-12B-qat-L4-devops-agent) | Serverless cloud SRE running the 12B QAT configuration on an NVIDIA L4 GPU. | `google/gemma-4-12B-it-qat-w4a16-ct` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-12B-qat-mtp-6000-devops-agent](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-6000-devops-agent) | Serverless cloud SRE running the 12B QAT configuration with Multi-Token Prediction (MTP) on an RTX 6000 GPU. | `google/gemma-4-12B-it-qat-w4a16-ct` | vLLM | Google Cloud Run (RTX 6000 GPU) |
| [gpu-12B-qat-mtp-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-L4-devops-agent) | Serverless cloud SRE running the 12B QAT configuration with Multi-Token Prediction (MTP) on an NVIDIA L4 GPU. | `google/gemma-4-12B-it-qat-w4a16-ct` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-26B-6000-devops-agent](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent) | Serverless cloud SRE running the 26B configuration on an NVIDIA RTX 6000 GPU. | `google/gemma-4-26B-it` | vLLM | Google Cloud Run (RTX 6000 GPU) |
| [gpu-26B-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-26B-L4-devops-agent) | Serverless cloud SRE running the 26B configuration on an NVIDIA L4 GPU. | `nvidia/gemma-4-26B-A4B-NVFP4` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-26B-qat-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-26B-qat-L4-devops-agent) | Serverless cloud SRE leveraging the 26B QAT configuration on an NVIDIA L4 GPU. | `google/gemma-4-26B-A4B-it-qat-w4a16-ct` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-31B-6000-devops-agent](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent) | Serverless cloud SRE running the 31B configuration on an NVIDIA RTX 6000 GPU. | `google/gemma-4-31B-it` | vLLM | Google Cloud Run (RTX 6000 GPU) |
| [gpu-31B-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-31B-L4-devops-agent) | Serverless cloud SRE running the 31B NVFP4 quantized configuration on an NVIDIA L4 GPU. | `nvidia/Gemma-4-31B-IT-NVFP4` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-31B-qat-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent) | Serverless cloud SRE leveraging the 31B QAT configuration on an NVIDIA L4 GPU. | `google/gemma-4-31B-it-qat-w4a16-ct` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-4B-6000-devops-agent](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent) | Serverless cloud SRE running the 4B configuration on an NVIDIA RTX 6000 GPU. | `google/gemma-4-E4B-it` | vLLM | Google Cloud Run (RTX 6000 GPU) |
| [gpu-4B-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent) | Serverless cloud SRE running the 4B configuration on an NVIDIA L4 GPU. | `google/gemma-4-E4B-it` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-4B-qat-L4-devops-agent](file:///home/xbill/gemma4-tips/gpu-4B-qat-L4-devops-agent) | Serverless cloud SRE leveraging the 4B QAT configuration on an NVIDIA L4 GPU. | `google/gemma-4-E4B-it-qat-w4a16-ct` | vLLM | Google Cloud Run (L4 GPU) |
| [gpu-6000-devops-agent](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent) | Cloud-based SRE managing GPU-accelerated serverless endpoints (RTX 6000 GPU configuration). | `google/gemma-4-E4B-it` | vLLM | Google Cloud Run (RTX 6000 GPU) |
| [gpu-vllm-devops-agent](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent) | Cloud-based SRE managing GPU-accelerated serverless endpoints (L4 GPU configuration). | `google/gemma-4-E4B-it` | vLLM | Google Cloud Run (L4 GPU) |
| [local-2B-devops-agent](file:///home/xbill/gemma4-tips/local-2B-devops-agent) | Local CPU/GPU DevOps/SRE Agent optimized for 2B parameter model execution. | `gemma4:e2b` | Ollama / vLLM | Local Workstation (Docker CPU/GPU) |
| [local-devops-agent](file:///home/xbill/gemma4-tips/local-devops-agent) | Specialized SRE for local CPU/GPU containerized workloads. | `google/gemma-4-31B-it` | Ollama / vLLM | Local Workstation (Docker CPU/GPU) |
| [mac-2B-devops-agent](file:///home/xbill/gemma4-tips/mac-2B-devops-agent) | Local macOS/Apple Silicon SRE Agent optimized for 2B parameter model execution on local hardware. | `gemma4:e2b` | Ollama / vLLM | Local macOS (Apple Silicon) |
| [mac-4B-devops-agent](file:///home/xbill/gemma4-tips/mac-4B-devops-agent) | Local macOS/Apple Silicon SRE Agent optimized for 4B parameter model execution on local hardware. | `gemma4:e4b` | Ollama / vLLM | Local macOS (Apple Silicon) |
| [tpu-12B-mtp-v6e1-devops-agent](file:///home/xbill/gemma4-tips/tpu-12B-mtp-v6e1-devops-agent) | High-performance TPU SRE/DevOps running the 12B configuration with Multi-Token Prediction (MTP) on a v6e-1 TPU VM. | `google/gemma-4-12B-it` | vLLM | Google Cloud TPUs (v6e Trillium v6e-1) |
| [tpu-12B-quant-v6e1-devops-agent](file:///home/xbill/gemma4-tips/tpu-12B-quant-v6e1-devops-agent) | High-performance TPU SRE/DevOps running the quantized 12B configuration (FP8) on a v6e-1 TPU VM. | `vrfai/gemma-4-12B-it-fp8` | vLLM | Google Cloud TPUs (v6e Trillium v6e-1) |
| [tpu-12B-v6e1-devops-agent](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent) | High-performance TPU SRE/DevOps managing TPU workloads with the 12B configuration on a v6e-1 TPU VM. | `google/gemma-4-12B-it` | vLLM | Google Cloud TPUs (v6e Trillium v6e-1) |
| [tpu-12B-v6e4-devops-agent](file:///home/xbill/gemma4-tips/tpu-12B-v6e4-devops-agent) | High-performance TPU SRE/DevOps managing TPU workloads with the 12B configuration on a v6e-4 TPU VM. | `google/gemma-4-12B-it` | Ollama / vLLM | Google Cloud TPUs (v6e Trillium v6e-4) |
| [tpu-26B-devops-agent](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent) | High-performance TPU SRE/DevOps running the 26B configuration (running 31B model) on a v6e-1 TPU VM. | `google/gemma-4-31B-it` | vLLM | Google Cloud TPUs (v6e Trillium v6e-1) |
| [tpu-2B-v6e1-devops-agent](file:///home/xbill/gemma4-tips/tpu-2B-v6e1-devops-agent) | High-performance TPU SRE/DevOps managing TPU workloads with the 2B configuration on a v6e-1 TPU VM. | `google/gemma-4-E2B-it` | Ollama / vLLM | Google Cloud TPUs (v6e Trillium v6e-1) |
| [tpu-2B-v6e4-devops-agent](file:///home/xbill/gemma4-tips/tpu-2B-v6e4-devops-agent) | High-performance TPU SRE/DevOps managing TPU workloads with the 2B configuration on a v6e-4 TPU VM. | `google/gemma-4-E2B-it` | Ollama / vLLM | Google Cloud TPUs (v6e Trillium v6e-4) |
| [tpu-31B-devops-agent](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent) | High-performance TPU SRE/DevOps running the 31B configuration on a v6e-1 TPU VM. | `google/gemma-4-31B-it` | vLLM | Google Cloud TPUs (v6e Trillium v6e-1) |
| [tpu-4B-v6e1-devops-agent](file:///home/xbill/gemma4-tips/tpu-4B-v6e1-devops-agent) | High-performance TPU SRE/DevOps managing TPU workloads with the 4B configuration on a v6e-1 TPU VM. | `google/gemma-4-E4B-it` | Ollama / vLLM | Google Cloud TPUs (v6e Trillium v6e-1) |
| [tpu-4B-v6e4-devops-agent](file:///home/xbill/gemma4-tips/tpu-4B-v6e4-devops-agent) | High-performance TPU SRE/DevOps managing TPU workloads with the 4B configuration on a v6e-4 TPU VM. | `google/gemma-4-E4B-it` | Ollama / vLLM | Google Cloud TPUs (v6e Trillium v6e-4) |

--- | :--- | :--- | :--- |
| [Local DevOps Agent](file:///home/xbill/gemma4-tips/local-devops-agent) | CPU/GPU local analysis & prototyping | Ollama / vLLM | Local Docker / Workstations |
| [GPU DevOps Agent (4B L4)](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent) | Serverless cloud SRE (4B model on L4 GPU) | vLLM | Google Cloud Run (us-east4) |
| [GPU DevOps Agent (4B 6000)](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent) | Serverless cloud SRE (4B model on RTX 6000 GPU) | vLLM | Google Cloud Run (us-central1) |
| [GPU DevOps Agent (26B 6000)](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent) | Serverless cloud SRE (26B model on RTX 6000 GPU) | vLLM | Google Cloud Run (us-central1) |
| [GPU DevOps Agent (31B 6000)](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent) | Serverless cloud SRE (31B model on RTX 6000 GPU) | vLLM | Google Cloud Run (us-central1) |
| [GPU DevOps Agent (6000)](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent) | Serverless cloud SRE (RTX 6000 GPU configuration) | vLLM | Google Cloud Run (us-central1) |
| [GPU DevOps Agent (vLLM)](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent) | Serverless cloud SRE (L4 GPU configuration) | vLLM | Google Cloud Run (us-east4) |
| [GPU DevOps Agent (31B QAT L4)](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent) | Serverless cloud SRE (31B QAT model on L4 GPU) | vLLM | Google Cloud Run (us-east4) |
| [TPU DevOps Agent (26B)](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent) | Ultra-high performance TPU SRE (26B configuration) | vLLM | Google Cloud TPUs (v6e Trillium) |
| [TPU DevOps Agent (31B)](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent) | Ultra-high performance TPU SRE (31B configuration) | vLLM | Google Cloud TPUs (v6e Trillium) |
| [TPU DevOps Agent (12B v6e-1)](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent) | Ultra-high performance TPU SRE (12B configuration) | vLLM | Google Cloud TPUs (v6e Trillium) |

---

## 🛠 Features & Capabilities

- **Automated SRE Diagnostics:** Fetches and reviews system, container, and Cloud Logging entries using Gemma 4 to identify root causes and generate 3-step remediation plans.
- **Serving Stack Control:** Built-in tools to provision, start, stop, restart, and scale your vLLM and Ollama containers or Cloud TPU Queued Resources.
- **Observability Dashboards:** Real-time dashboards monitoring HBM usage, Tensor Core pressure, Prometheus metrics, and service latencies.
- **Model Benchmarking:** Tools to run load tests and vLLM's internal benchmark suites, returning performance metrics (TTFT, throughput, P95 latency).
- **Gemini CLI Integration:** Custom setup instructions using a LiteLLM Proxy to route standard Gemini CLI commands directly to your private, self-hosted Gemma 4 instance.

---

## 🏗 Global Makefile Usage

A root [Makefile](file:///home/xbill/gemma4-tips/Makefile) is provided to manage the sub-agents collectively:

- **Help / Display commands:**
  ```bash
  make all
  ```
- **Install dependencies in all subdirectories:**
  ```bash
  make install
  ```
- **Run tests across all agents:**
  ```bash
  make test
  ```
- **Lint all Python directories:**
  ```bash
  make lint
  ```
- **Clean build/cache folders:**
  ```bash
  make clean
  ```

---

## 🚀 Sub-Agent Overviews

### 1. [GPU Agent (12B QAT L4 / Gen2)](file:///home/xbill/gemma4-tips/g2-4-12B-qat-L4-devops-agent)
- **Role:** Serverless cloud SRE leveraging the 12B parameter QAT model on L4 GPU via Cloud Run Gen2.
- **Inference Stack:** Runs `google/gemma-4-12B-it-qat-w4a16-ct` via vLLM.
- **Documentation:** See [g2-4-12B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/g2-4-12B-qat-L4-devops-agent/README.md) and [g2-4-12B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/g2-4-12B-qat-L4-devops-agent/GEMINI.md).

### 2. [GPU Agent (12B 6000)](file:///home/xbill/gemma4-tips/gpu-12B-6000-devops-agent)
- **Role:** Serverless cloud SRE running the 12B configuration on an NVIDIA RTX 6000 GPU.
- **Inference Stack:** Runs `gemma-4-12B-it` via vLLM.
- **Documentation:** See [gpu-12B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-6000-devops-agent/README.md) and [gpu-12B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-6000-devops-agent/GEMINI.md).

### 3. [GPU Agent (12B L4)](file:///home/xbill/gemma4-tips/gpu-12B-L4-devops-agent)
- **Role:** Serverless cloud SRE running the 12B configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `gemma-4-12B-it` via vLLM.
- **Documentation:** See [gpu-12B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-L4-devops-agent/README.md) and [gpu-12B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-L4-devops-agent/GEMINI.md).

### 4. [GPU Agent (12B QAT L4)](file:///home/xbill/gemma4-tips/gpu-12B-qat-L4-devops-agent)
- **Role:** Serverless cloud SRE running the 12B QAT configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `google/gemma-4-12B-it-qat-w4a16-ct` via vLLM.
- **Documentation:** See [gpu-12B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-L4-devops-agent/README.md) and [gpu-12B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-L4-devops-agent/GEMINI.md).

### 5. [GPU Agent (12B QAT MTP 6000)](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-6000-devops-agent)
- **Role:** Serverless cloud SRE running the 12B QAT configuration with Multi-Token Prediction (MTP) on an RTX 6000 GPU.
- **Inference Stack:** Runs `google/gemma-4-12B-it-qat-w4a16-ct` via vLLM.
- **Documentation:** See [gpu-12B-qat-mtp-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-6000-devops-agent/README.md) and [gpu-12B-qat-mtp-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-6000-devops-agent/GEMINI.md).

### 6. [GPU Agent (12B QAT MTP L4)](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-L4-devops-agent)
- **Role:** Serverless cloud SRE running the 12B QAT configuration with Multi-Token Prediction (MTP) on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `google/gemma-4-12B-it-qat-w4a16-ct` via vLLM.
- **Documentation:** See [gpu-12B-qat-mtp-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-L4-devops-agent/README.md) and [gpu-12B-qat-mtp-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-12B-qat-mtp-L4-devops-agent/GEMINI.md).

### 7. [GPU Agent (26B 6000)](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent)
- **Role:** Serverless cloud SRE running the 26B configuration on an NVIDIA RTX 6000 GPU.
- **Inference Stack:** Runs `google/gemma-4-26B-it` via vLLM.
- **Documentation:** See [gpu-26B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent/README.md) and [gpu-26B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-26B-6000-devops-agent/GEMINI.md).

### 8. [GPU Agent (26B L4)](file:///home/xbill/gemma4-tips/gpu-26B-L4-devops-agent)
- **Role:** Serverless cloud SRE running the 26B configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `nvidia/gemma-4-26B-A4B-NVFP4` via vLLM.
- **Documentation:** See [gpu-26B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-26B-L4-devops-agent/README.md) and [gpu-26B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-26B-L4-devops-agent/GEMINI.md).

### 9. [GPU Agent (26B QAT L4)](file:///home/xbill/gemma4-tips/gpu-26B-qat-L4-devops-agent)
- **Role:** Serverless cloud SRE leveraging the 26B QAT configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `google/gemma-4-26B-A4B-it-qat-w4a16-ct` via vLLM.
- **Documentation:** See [gpu-26B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-26B-qat-L4-devops-agent/README.md) and [gpu-26B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-26B-qat-L4-devops-agent/GEMINI.md).

### 10. [GPU Agent (31B 6000)](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent)
- **Role:** Serverless cloud SRE running the 31B configuration on an NVIDIA RTX 6000 GPU.
- **Inference Stack:** Runs `google/gemma-4-31B-it` via vLLM.
- **Documentation:** See [gpu-31B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent/README.md) and [gpu-31B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-31B-6000-devops-agent/GEMINI.md).

### 11. [GPU Agent (31B L4)](file:///home/xbill/gemma4-tips/gpu-31B-L4-devops-agent)
- **Role:** Serverless cloud SRE running the 31B NVFP4 quantized configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `nvidia/Gemma-4-31B-IT-NVFP4` via vLLM.
- **Documentation:** See [gpu-31B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-31B-L4-devops-agent/README.md) and [gpu-31B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-31B-L4-devops-agent/GEMINI.md).

### 12. [GPU Agent (31B QAT L4)](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent)
- **Role:** Serverless cloud SRE leveraging the 31B QAT configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `google/gemma-4-31B-it-qat-w4a16-ct` via vLLM.
- **Documentation:** See [gpu-31B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent/README.md) and [gpu-31B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-31B-qat-L4-devops-agent/GEMINI.md).

### 13. [GPU Agent (4B 6000)](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent)
- **Role:** Serverless cloud SRE running the 4B configuration on an NVIDIA RTX 6000 GPU.
- **Inference Stack:** Runs `google/gemma-4-E4B-it` via vLLM.
- **Documentation:** See [gpu-4B-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent/README.md) and [gpu-4B-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-4B-6000-devops-agent/GEMINI.md).

### 14. [GPU Agent (4B L4)](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent)
- **Role:** Serverless cloud SRE running the 4B configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `google/gemma-4-E4B-it` via vLLM.
- **Documentation:** See [gpu-4B-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent/README.md) and [gpu-4B-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-4B-L4-devops-agent/GEMINI.md).

### 15. [GPU Agent (4B QAT L4)](file:///home/xbill/gemma4-tips/gpu-4B-qat-L4-devops-agent)
- **Role:** Serverless cloud SRE leveraging the 4B QAT configuration on an NVIDIA L4 GPU.
- **Inference Stack:** Runs `google/gemma-4-E4B-it-qat-w4a16-ct` via vLLM.
- **Documentation:** See [gpu-4B-qat-L4-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-4B-qat-L4-devops-agent/README.md) and [gpu-4B-qat-L4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-4B-qat-L4-devops-agent/GEMINI.md).

### 16. [GPU Agent (6000)](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent)
- **Role:** Cloud-based SRE managing GPU-accelerated serverless endpoints (RTX 6000 GPU configuration).
- **Inference Stack:** Runs `google/gemma-4-E4B-it` via vLLM.
- **Documentation:** See [gpu-6000-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent/README.md) and [gpu-6000-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-6000-devops-agent/GEMINI.md).

### 17. [GPU Agent (vLLM L4)](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent)
- **Role:** Cloud-based SRE managing GPU-accelerated serverless endpoints (L4 GPU configuration).
- **Inference Stack:** Runs `google/gemma-4-E4B-it` via vLLM.
- **Documentation:** See [gpu-vllm-devops-agent/README.md](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent/README.md) and [gpu-vllm-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/gpu-vllm-devops-agent/GEMINI.md).

### 18. [Local Agent (2B)](file:///home/xbill/gemma4-tips/local-2B-devops-agent)
- **Role:** Local CPU/GPU DevOps/SRE Agent optimized for 2B parameter model execution.
- **Inference Stack:** Runs `gemma4:e2b` via Ollama / vLLM.
- **Documentation:** See [local-2B-devops-agent/README.md](file:///home/xbill/gemma4-tips/local-2B-devops-agent/README.md) and [local-2B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/local-2B-devops-agent/GEMINI.md).

### 19. [Local Agent (31B default)](file:///home/xbill/gemma4-tips/local-devops-agent)
- **Role:** Specialized SRE for local CPU/GPU containerized workloads.
- **Inference Stack:** Runs `google/gemma-4-31B-it` via Ollama / vLLM.
- **Documentation:** See [local-devops-agent/README.md](file:///home/xbill/gemma4-tips/local-devops-agent/README.md) and [local-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/local-devops-agent/GEMINI.md).

### 20. [macOS Agent (2B)](file:///home/xbill/gemma4-tips/mac-2B-devops-agent)
- **Role:** Local macOS/Apple Silicon SRE Agent optimized for 2B parameter model execution on local hardware.
- **Inference Stack:** Runs `gemma4:e2b` via Ollama / vLLM.
- **Documentation:** See [mac-2B-devops-agent/README.md](file:///home/xbill/gemma4-tips/mac-2B-devops-agent/README.md) and [mac-2B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/mac-2B-devops-agent/GEMINI.md).

### 21. [macOS Agent (4B)](file:///home/xbill/gemma4-tips/mac-4B-devops-agent)
- **Role:** Local macOS/Apple Silicon SRE Agent optimized for 4B parameter model execution on local hardware.
- **Inference Stack:** Runs `gemma4:e4b` via Ollama / vLLM.
- **Documentation:** See [mac-4B-devops-agent/README.md](file:///home/xbill/gemma4-tips/mac-4B-devops-agent/README.md) and [mac-4B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/mac-4B-devops-agent/GEMINI.md).

### 22. [TPU Agent (12B MTP v6e-1)](file:///home/xbill/gemma4-tips/tpu-12B-mtp-v6e1-devops-agent)
- **Role:** High-performance TPU SRE/DevOps running the 12B configuration with Multi-Token Prediction (MTP) on a v6e-1 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-12B-it` via vLLM.
- **Documentation:** See [tpu-12B-mtp-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-mtp-v6e1-devops-agent/README.md) and [tpu-12B-mtp-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-mtp-v6e1-devops-agent/GEMINI.md).

### 23. [TPU Agent (12B Quant v6e-1)](file:///home/xbill/gemma4-tips/tpu-12B-quant-v6e1-devops-agent)
- **Role:** High-performance TPU SRE/DevOps running the quantized 12B configuration (FP8) on a v6e-1 TPU VM.
- **Inference Stack:** Runs `vrfai/gemma-4-12B-it-fp8` via vLLM.
- **Documentation:** See [tpu-12B-quant-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-quant-v6e1-devops-agent/README.md) and [tpu-12B-quant-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-quant-v6e1-devops-agent/GEMINI.md).

### 24. [TPU Agent (12B v6e-1)](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent)
- **Role:** High-performance TPU SRE/DevOps managing TPU workloads with the 12B configuration on a v6e-1 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-12B-it` via vLLM.
- **Documentation:** See [tpu-12B-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent/README.md) and [tpu-12B-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e1-devops-agent/GEMINI.md).

### 25. [TPU Agent (12B v6e-4)](file:///home/xbill/gemma4-tips/tpu-12B-v6e4-devops-agent)
- **Role:** High-performance TPU SRE/DevOps managing TPU workloads with the 12B configuration on a v6e-4 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-12B-it` via Ollama / vLLM.
- **Documentation:** See [tpu-12B-v6e4-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e4-devops-agent/README.md) and [tpu-12B-v6e4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-12B-v6e4-devops-agent/GEMINI.md).

### 26. [TPU Agent (26B v6e-1)](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent)
- **Role:** High-performance TPU SRE/DevOps running the 26B configuration (running 31B model) on a v6e-1 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-31B-it` via vLLM.
- **Documentation:** See [tpu-26B-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent/README.md) and [tpu-26B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-26B-devops-agent/GEMINI.md).

### 27. [TPU Agent (2B v6e-1)](file:///home/xbill/gemma4-tips/tpu-2B-v6e1-devops-agent)
- **Role:** High-performance TPU SRE/DevOps managing TPU workloads with the 2B configuration on a v6e-1 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-E2B-it` via Ollama / vLLM.
- **Documentation:** See [tpu-2B-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e1-devops-agent/README.md) and [tpu-2B-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e1-devops-agent/GEMINI.md).

### 28. [TPU Agent (2B v6e-4)](file:///home/xbill/gemma4-tips/tpu-2B-v6e4-devops-agent)
- **Role:** High-performance TPU SRE/DevOps managing TPU workloads with the 2B configuration on a v6e-4 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-E2B-it` via Ollama / vLLM.
- **Documentation:** See [tpu-2B-v6e4-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e4-devops-agent/README.md) and [tpu-2B-v6e4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-2B-v6e4-devops-agent/GEMINI.md).

### 29. [TPU Agent (31B v6e-1)](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent)
- **Role:** High-performance TPU SRE/DevOps running the 31B configuration on a v6e-1 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-31B-it` via vLLM.
- **Documentation:** See [tpu-31B-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent/README.md) and [tpu-31B-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-31B-devops-agent/GEMINI.md).

### 30. [TPU Agent (4B v6e-1)](file:///home/xbill/gemma4-tips/tpu-4B-v6e1-devops-agent)
- **Role:** High-performance TPU SRE/DevOps managing TPU workloads with the 4B configuration on a v6e-1 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-E4B-it` via Ollama / vLLM.
- **Documentation:** See [tpu-4B-v6e1-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e1-devops-agent/README.md) and [tpu-4B-v6e1-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e1-devops-agent/GEMINI.md).

### 31. [TPU Agent (4B v6e-4)](file:///home/xbill/gemma4-tips/tpu-4B-v6e4-devops-agent)
- **Role:** High-performance TPU SRE/DevOps managing TPU workloads with the 4B configuration on a v6e-4 TPU VM.
- **Inference Stack:** Runs `google/gemma-4-E4B-it` via Ollama / vLLM.
- **Documentation:** See [tpu-4B-v6e4-devops-agent/README.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e4-devops-agent/README.md) and [tpu-4B-v6e4-devops-agent/GEMINI.md](file:///home/xbill/gemma4-tips/tpu-4B-v6e4-devops-agent/GEMINI.md).
---

## 🔒 Security & Credentials
When deploying to Google Cloud or Hugging Face, secure credentials using:
- **Hugging Face Access Token:** Saved locally or to Google Secret Manager.
- **Application Default Credentials (ADC):** Set up using GCP credentials helper scripts.

## Credits
Google Cloud credits are provided for this project.

#AgenticArchitect #GoogleAntigravity
