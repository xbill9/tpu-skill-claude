"""Smoke and regression tests for the tpu-devops MCP server and repo invariants.

Standard library + the server's own dependencies only; run via `make test` or
`python3 -m unittest discover -s tests`. No GCP calls are made — tests cover
pure logic, tool registration, template rendering, and repo hygiene.
"""

import asyncio
import filecmp
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import server  # noqa: E402

EXPECTED_DESTRUCTIVE = {
    "destroy_queued_resource",
    "destroy_tpu_vm_instance",
    "manage_queued_resource",
    "manage_vllm_docker",
    "find_tpu",
}


def run(coro):
    return asyncio.run(coro)


class ToolCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools = {t.name: t for t in run(server.mcp.list_tools())}

    def test_every_tool_has_title_description_and_annotations(self):
        for name, tool in self.tools.items():
            self.assertTrue(tool.title, f"{name} has no title")
            self.assertTrue(tool.description, f"{name} has no description")
            self.assertIsNotNone(tool.annotations, f"{name} has no annotations")

    def test_destructive_hints_match_expected_set(self):
        destructive = {
            name for name, t in self.tools.items() if t.annotations.destructiveHint
        }
        self.assertEqual(destructive, EXPECTED_DESTRUCTIVE)

    def test_read_only_tools_never_marked_destructive(self):
        for name, t in self.tools.items():
            if t.annotations.readOnlyHint:
                self.assertFalse(
                    t.annotations.destructiveHint,
                    f"{name} is both readOnly and destructive",
                )

    def test_action_and_type_enums_in_schema(self):
        props = self.tools["manage_vllm_docker"].inputSchema["properties"]
        self.assertEqual(
            props["action"]["enum"], ["start", "stop", "restart", "status", "log", "rm"]
        )
        self.assertEqual(
            self.tools["estimate_deployment_cost"].inputSchema["properties"]["tpu_type"]["enum"],
            ["v6e", "v5e", "v5p"],
        )

    def test_log_tails_are_bounded(self):
        for name in ("get_vllm_docker_logs", "get_tpu_system_logs", "get_tpu_vm_serial_log"):
            tail = self.tools[name].inputSchema["properties"]["tail"]
            self.assertIn("maximum", tail, f"{name}.tail has no upper bound")


class HelperTests(unittest.TestCase):
    def test_zone_defaults_to_current_global(self):
        self.assertEqual(server._zone(None), server.ZONE)
        self.assertEqual(server._zone("us-east5-b"), "us-east5-b")

    def test_filter_key_metrics_drops_comments_and_noise(self):
        text = (
            "# HELP vllm_requests_running Running requests\n"
            "vllm_requests_running 3.0\n"
            "vllm_request_latency_bucket{le=\"0.5\"} 12\n"
            "process_resident_memory_bytes 1024\n"
        )
        self.assertEqual(
            server._filter_key_metrics(text),
            ["vllm_requests_running 3.0", "process_resident_memory_bytes 1024"],
        )

    def test_estimate_cost_math_and_rejects_bad_topology(self):
        result = run(server.estimate_deployment_cost(hours=2.0, tpu_type="v6e", topology="2x4"))
        self.assertIn("$21.60", result)  # 8 chips * 1.35 * 2h
        self.assertTrue(run(server.estimate_deployment_cost(topology="0x4")).startswith("❌"))

    def test_run_command_success_and_timeout(self):
        rc, out, _ = run(server.run_command(["echo", "hi"]))
        self.assertEqual((rc, out), (0, "hi"))
        rc, _, err = run(server.run_command(["sleep", "5"], timeout=1))
        self.assertEqual(rc, -1)
        self.assertIn("Timeout", err)


class StartupTemplateTests(unittest.TestCase):
    def render(self):
        template = (
            ROOT / ".claude/skills/tpu-management/mcp/startup_script_template.sh"
        ).read_text()
        return template.format(
            project_id="test-project",
            zone="europe-west4-a",
            model_name="google/gemma-4-31B-it",
            hf_secret_id="hf-token",
            tp_size=8,
            limit_mm_per_prompt_env="export VLLM_LIMIT_MM_PER_PROMPT='{\"image\":4,\"audio\":1}'",
        )

    def test_renders_without_leftover_placeholders_or_token(self):
        rendered = self.render()
        self.assertNotIn("{hf_token}", rendered)
        self.assertIn("secretmanager.googleapis.com", rendered)
        self.assertIn("test-project", rendered)

    def test_rendered_script_passes_bash_syntax_check(self):
        rendered = self.render()
        proc = subprocess.run(
            ["bash", "-n", "/dev/stdin"], input=rendered, text=True, capture_output=True
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)


class RepoHygieneTests(unittest.TestCase):
    def test_shell_scripts_parse(self):
        for script in ("project-setup.sh", "init.sh", "set_env.sh", "set_adc.sh"):
            proc = subprocess.run(
                ["bash", "-n", str(ROOT / script)], capture_output=True, text=True
            )
            self.assertEqual(proc.returncode, 0, f"{script}: {proc.stderr}")

    def test_skill_snapshots_in_sync_with_sources(self):
        """Sources at the repo root are authoritative; `make skill` regenerates the
        copies. A mismatch means someone edited one side without resyncing."""
        for src, snap in (
            ("server.py", ".claude/skills/tpu-management/mcp/server.py"),
            ("project-setup.sh", ".claude/skills/tpu-management/mcp/project-setup.sh"),
            ("requirements.txt", ".claude/skills/tpu-management/mcp/requirements.txt"),
        ):
            self.assertTrue(
                filecmp.cmp(ROOT / src, ROOT / snap, shallow=False),
                f"{snap} is stale — run `make skill`",
            )

    def test_plugin_copy_matches_skill(self):
        for rel in ("mcp/server.py", "SKILL.md", "mcp/startup_script_template.sh"):
            self.assertTrue(
                filecmp.cmp(
                    ROOT / ".claude/skills/tpu-management" / rel,
                    ROOT / "skills/tpu-management" / rel,
                    shallow=False,
                ),
                f"skills/tpu-management/{rel} is stale — run `make skill`",
            )


if __name__ == "__main__":
    unittest.main()
