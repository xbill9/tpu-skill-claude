# CLAUDE.md — Gemma 4 DevOps Agents

Guidance for Claude Code when working in this repository.

## Project Overview

This repository provides a set of **Model Context Protocol (MCP) servers** representing specialized AI DevOps/SRE agents. They serve two main purposes:

1. **Infrastructure Operations:** Starting, stopping, configuring, scaling, and benchmarking Gemma 4 serving stacks (Ollama or vLLM) on Local, GPU, and TPU environments.
2. **Log & SRE Diagnostics:** Using the self-hosted Gemma 4 models to analyze system/cloud logs and generate remediation suggestions.

## Repository Layout

Each top-level `*-devops-agent/` directory is one self-contained agent. Directory names encode the deployment target and model variant:

- **Prefix** — deployment environment:
  - `local-` — local Ollama/vLLM serving
  - `mac-` — macOS local serving
  - `gpu-` — Cloud Run GPU (suffix indicates `L4` or RTX `6000` hardware)
  - `g2-`, `g2-48-`, `g2-96-` — Gen2 GPU configurations
  - `tpu-` — Cloud TPU (suffix indicates topology, e.g. `v6e1`, `v6e4`, `v6e8`)
- **Middle tokens** — model size (`2B`, `4B`, `12B`, `26B`, `31B`) and options:
  - `qat` — quantization-aware-trained model
  - `mtp` — multi-token prediction
  - `quant` — quantized

Inside each agent directory the layout is consistent:

- `server.py` — the MCP server entrypoint (the agent itself)
- `Makefile` — per-agent `install` / `lint` / `test` / `clean` / `deploy` targets
- `test_agent.py` — agent tests
- `benchmarking_suite.py`, `load_test.py`, `plot_benchmark.py` — benchmarking tooling
- `README.md`, `GEMINI.md`, `DEPLOY.md` — per-agent documentation
- `init.sh`, `set_env.sh`, `set_adc.sh` — environment/deployment setup scripts

## Common Commands

The root `Makefile` dynamically discovers every subdirectory containing a `Makefile` and fans the target out to all of them:

```bash
make install   # Prepare dependencies for all agents
make lint      # Standardize code formatting across all agents
make test      # Validate server initializations and run mock tests
make clean     # Clean all agents
make deploy    # Deploy all agents
```

To work on a single agent, run the same targets from inside its directory (e.g. `cd local-devops-agent && make test`).

## Technical Standards: vLLM & Gemma 4 Tool Calling

When managing TPU/GPU deployments or customizing vLLM serving, apply these vLLM parameters for stable Gemma 4 tool integration:

- **Optimization flags:** `--tensor-parallel-size 8` (TPU v6e-8), `--disable_chunked_mm_input`, `--max-model-len 16384`
- **Tool parsing:** `--enable-auto-tool-choice`, `--tool-call-parser gemma4`, and `--reasoning-parser gemma4` for native function-calling compatibility
- **Multimodal configuration:** `--limit-mm-per-prompt '{"image":4,"audio":1}'` and `--max_num_batched_tokens 4096`
- **Universal SRE help:** every agent exposes a standardized `get_help` tool describing its active configuration environment variables and all exposed tools

## Benchmarking & Analysis Standards

- **Ignore boilerplate templates:** the default `benchmark_results.csv` files in subdirectories (MD5 hash `edaf3f0fcb3e213750bed5fe4bb9a0cb`) are placeholder templates. Exclude them from statistics; analyze real run results instead (`grid_benchmark_results.csv`, `matrix_benchmark_results.csv`, `benchmark_sweep_results.csv`).
- **Dependency portability:** do not assume third-party analysis libraries like `pandas` are installed. Prefer the standard library (`csv`, `json`) for data parsing and aggregation scripts.

## Related Documentation

- `GEMINI.md` (root) — Gemini CLI integration via a LiteLLM proxy, including `litellm_config.yaml` examples for routing Gemini CLI traffic to the self-hosted Gemma 4 endpoints
- Per-agent `README.md` / `DEPLOY.md` — deployment and usage details for each specific agent
