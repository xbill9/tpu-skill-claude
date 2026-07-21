---
name: tpu-management
description: Manage Google Cloud TPU capacity and Gemma 4 vLLM serving on TPU VMs. Use when the user asks about provisioning, finding, listing, or destroying TPUs / queued resources / flex-start VMs, starting or debugging vLLM on TPU (v6e, v5p, v5e), TPU quotas and zones, TPU cost estimates, benchmarking TPU serving, or the TPU devops MCP agent. Triggers include "TPU", "queued resource", "flex-start", "v6e", "vLLM on TPU", "TPU quota".
---

# TPU Management

Operate Google Cloud TPU serving infrastructure for Gemma 4: acquire capacity, run vLLM,
verify health, benchmark, and tear down. Two ways to act:

1. **Preferred — MCP agent tools.** If the `tpu-31B-v6e8-devops-agent` MCP server is
   connected in this session, use its tools (catalog below). They wrap the correct
   `gcloud` invocations, discovery, and retry/cleanup logic.
2. **Fallback — direct `gcloud`.** If the MCP server is not connected, either offer to
   register the bundled server (see "Registering the MCP server") or run the equivalent
   `gcloud` commands from `references/tpu-guide.md`.

## Bundled files

- `mcp/server.py` — the FastMCP DevOps agent (snapshot of the repo-root `server.py`;
  the live copy at the repo root is authoritative if the two differ).
- `mcp/project-setup.sh` — one-command installer: copies this skill into a target project and
  registers the MCP server (see "Registering the MCP server").
- `mcp/startup_script_template.sh` — the TPU VM startup script the agent injects when
  creating a queued resource (pulls `vllm/vllm-tpu:nightly` and serves the model).
- `references/tpu-guide.md` — the TPU getting started guide: prerequisites,
  flex-start capacity zones per TPU family, `gcloud` creation templates for v6e/v5p/v5e,
  persistent-disk + startup-script patterns, quota metrics and request procedure,
  troubleshooting/FAQ. Read it when working without the MCP tools, diagnosing
  provisioning failures, or answering quota/capacity/billing questions.

## Registering the MCP server

Easiest path — run the bundled installer (idempotent; installs this skill into the
target project and writes the `tpu-devops` entry into the project's `.mcp.json`,
using the system `python3` — it warns if the pip deps below are missing but never
creates a venv):

```bash
mcp/project-setup.sh /path/to/project --project <gcp-project-id>   # one project
mcp/project-setup.sh --global                                      # all projects (user scope)
# from the skill repo root: make init TARGET=/path/to/project ARGS='--project <id>'
```

Run `mcp/project-setup.sh --help` for all options (`--model`, `--accelerator`, `--tp`,
`--server-name`, `--skip-deps`). Then restart Claude Code in the target project and
approve the server when prompted; `/mcp` should list `tpu-devops`.

Manual alternative:

```bash
claude mcp add tpu-devops \
  --env GOOGLE_CLOUD_PROJECT=<project-id> \
  --env MODEL_NAME=google/gemma-4-31B-it \
  --env ACCELERATOR_TYPE=v6e-8 \
  --env TENSOR_PARALLEL_SIZE=8 \
  -- python .claude/skills/tpu-management/mcp/server.py
```

Requires: `pip install -r mcp/requirements.txt`, an authenticated
`gcloud` CLI with alpha components (`gcloud components install alpha`), and the TPU API
enabled. The server reads config from env vars: `GOOGLE_CLOUD_PROJECT`, `MODEL_NAME`,
`ACCELERATOR_TYPE`, `TENSOR_PARALLEL_SIZE` (zone defaults to `europe-west4-a` in code).
A Hugging Face token must exist as Secret Manager secret `hf-token` (save one with the
`save_hf_token` tool) before any resource creation.

## Standard lifecycle

1. **Status first.** `get_system_status` (dashboard) or `list_queued_resources` /
   `find_gpu`. Never create before checking what already exists.
2. **Acquire capacity.**
   - Preferred (v6e/v5p): `create_tpu_vm_instance` — GCE flex-start VM with vLLM
     auto-start; watch boot with `get_tpu_vm_serial_log`.
   - Known zone, legacy API: `create_tpu_queued_resource` / `manage_queued_resource`
     (flex-start by default: 4h max-run; `reserved=True` for reservations).
   - Unknown zone: `get_zones_with_available_quota`, or `find_tpu` which sweeps every
     zone with quota, polls until ACTIVE (3 min, extended to 10 min once PROVISIONING),
     and cleans up failures. It skips zones marked failed in `tpu_zones_status.md`.
3. **Wait for ACTIVE.** `check_tpu_availability` or `describe_queued_resource`.
   Queued resources move QUEUED → PROVISIONING → ACTIVE; FAILED/SUSPENDED means
   delete and retry (the manage tool does this automatically).
4. **Serve.** The creation startup script auto-starts vLLM. Otherwise
   `manage_vllm_docker` with action `start|stop|restart|status|log|rm`. It auto-picks
   load format, max-model-len, and memory utilization from the model size
   (26B/31B → `tpu_streaming_loader`, 16384 ctx, 0.80 util; smaller → `runai_streamer`,
   65536 ctx, 0.90 util). Model load can take many minutes — check
   `get_vllm_docker_logs` for "Application startup complete."
5. **Verify.** `verify_model_health`, `get_vllm_endpoint`, `get_model_details`,
   `query_queued_gemma4[_with_stats]`.
6. **Benchmark (optional).** `run_vllm_benchmark` (runs `vllm bench serve` in a
   separate container on the VM).
7. **Tear down.** `destroy_queued_resource`. Flex-start bills until deletion and
   cannot be paused — always confirm teardown of idle resources with the user, and
   remind them a flex-start resource left running expires at max-run-duration.

## MCP tool catalog (by task)

**Capacity & lifecycle (GCE flex-start — recommended for v6e/v5p):**
`create_tpu_vm_instance` (creates the VM with the proven flags: 200GB boot disk,
docker-installing startup script, cloud-platform scopes), `list_tpu_vm_instances`,
`destroy_tpu_vm_instance`, `get_tpu_vm_serial_log`, `get_tpu_vm_endpoint`

**Capacity & lifecycle (queued resources — legacy, v5e):** `find_tpu`,
`create_tpu_queued_resource`,
`manage_queued_resource`, `destroy_queued_resource`, `list_queued_resources`,
`describe_queued_resource`, `get_reservation_status`, `check_tpu_availability`,
`get_zones_with_available_quota`, `find_gpu`, `estimate_deployment_cost`

**Serving:** `manage_vllm_docker`, `get_vllm_endpoint`, `get_deployed_endpoint`,
`get_vllm_deployment_config` (gcloud one-liner), `get_vllm_tpu_deployment_config`
(GKE manifest), `save_hf_token`

**Health, logs & diagnostics:** `get_system_status`, `verify_model_health`,
`get_model_details`, `get_metrics`, `get_vllm_docker_logs`, `get_tpu_system_logs`,
`get_cloud_logging_logs`, `analyze_cloud_logging` (Gemma-4-powered log triage)

**Inference & benchmarking:** `query_queued_gemma4`, `query_queued_gemma4_with_stats`,
`run_vllm_benchmark`

Every agent in this repo also exposes `get_help` for its live configuration.

## vLLM on TPU — required flags (Gemma 4)

When composing or reviewing a vLLM serve command for TPU, use:
`--tensor-parallel-size 8` (v6e-8), `--max-model-len 16384`,
`--disable_chunked_mm_input`, `--max_num_batched_tokens 4096`,
`--enable-auto-tool-choice --tool-call-parser gemma4 --reasoning-parser gemma4`,
and `--limit-mm-per-prompt '{"image":4,"audio":1}'` for multimodal
(the agent uses `{"image":0,"audio":0}` for text-only serving).
Image: `vllm/vllm-tpu:nightly`, run with `--privileged --net=host --shm-size 10gb`
and `HF_HOME=/dev/shm`.

## Field notes — GCE flex-start path (`gcloud compute instances create`)

Verified on a live v6e-1 deployment (Jul 2026). When creating TPU VMs as GCE
instances (the reference guide's template) rather than queued resources, the
guide's command as written will fail; apply all of these:

- **Boot disk:** the default is only 10 GB (hyperdisk-balanced) — `vllm/vllm-tpu:nightly`
  overflows it during layer extraction ("no space left on device"). Add
  `--boot-disk-size=200GB`. If already created, recover without losing flex-start
  capacity: `gcloud compute disks resize <name> --size=200GB` then
  `gcloud compute instances reset <name>` (never delete/recreate — that forfeits
  the capacity grant and restarts the max-run clock).
- **Docker:** not preinstalled on the `ubuntu-accel-2204-amd64-tpu-v5e-v5p-v6e`
  image (unlike TPU runtime images). The bundled startup script template now
  installs `docker.io` when missing; custom scripts must do the same.
- **Secrets at boot:** add `--scopes=cloud-platform` at creation and grant the
  default compute SA `roles/secretmanager.secretAccessor` on `hf-token`
  (`gcloud secrets add-iam-policy-binding hf-token --member=serviceAccount:<project-number>-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor`).
  Fetch the token in the startup script via the metadata server + Secret Manager
  REST API with a retry loop (~30 min) so an IAM grant applied after creation
  still lands. Symptom of a missing grant/scope: the fetch 403s forever.
- **Watch boot via serial console, not SSH:** SSH is often blocked by firewall
  policy. The startup template mirrors its log to `/dev/console`; follow it with
  `gcloud compute instances get-serial-port-output <name>`. Grep for the final
  "vLLM application startup complete." line — the earlier "Waiting for
  'Application startup complete.'" echo is a false-positive match.
- **Quota is per region AND per TPU family:** creation fails immediately with
  `Quota 'TPUS_PER_TPU_FAMILY' exceeded. Limit: 0.0` in regions without CT6E
  quota (observed: us-east5 = 0, europe-west4 OK). This dimensioned quota is not
  visible via `gcloud compute regions describe` — attempt creation (fails fast)
  or check the console. Failure sequence for a v6e-1: boot ~1 min → docker
  install ~1 min → image pull ~5 min → model download/compile ~5-10 min.

## Cautions

- `destroy_queued_resource` and `manage_queued_resource` delete infrastructure —
  `manage_queued_resource` deletes ALL queued resources in the zone other than the
  named primary. Confirm with the user before invoking against a zone that may hold
  resources they want kept.
- Flex-start requests expire (`--valid-until-duration`) and instances self-delete at
  `--max-run-duration`; data on the VM is lost. Persist data on a separate disk or GCS
  (see the reference guide).
- Stuck in `WAITING_FOR_RESOURCES`/`PROVISIONING` or `STOCKOUT`: usually the
  `GPUS_ALL_REGIONS` global quota is 0 — see the Troubleshooting section of
  `references/tpu-guide.md` before retrying other zones.
- v5e uses the legacy queued-resources API and separate quota metrics; v6e/v5p use GCE
  machine types (`ct6e-standard-4t`, `ct5p-hightpu-4t`). Zone/family table is in the
  reference guide.
