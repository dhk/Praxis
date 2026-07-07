import json
from pathlib import Path
from praxis.cli import run
from praxis.pipeline import run_pipeline

def test_harness_creates_artifacts(tmp_path: Path):
    source = Path("examples/concise_scientific_writing/input.md")
    out = tmp_path / "run"
    run(source, out)
    assert (out / "observations.json").exists()
    assert (out / "transformations.json").exists()
    assert (out / "validation.json").exists()
    assert (out / "final.md").exists()
    final = (out / "final.md").read_text()
    assert "It should be noted that" not in final
    assert "because" in final
    validation = json.loads((out / "validation.json").read_text())
    assert validation["status"] == "pass"

def test_run_pipeline_matches_cli_artifacts(tmp_path: Path):
    source = Path("examples/concise_scientific_writing/input.md")
    out = tmp_path / "run"
    run(source, out)
    result = run_pipeline(source.read_text(encoding="utf-8"))
    for name in ("observations", "recommendations", "transformations", "validation"):
        assert result[name] == json.loads((out / f"{name}.json").read_text())
    assert result["final"] == (out / "final.md").read_text()
    assert result["report"] == (out / "report.md").read_text()
    assert result["metrics"]["before"]["words"] >= result["metrics"]["after"]["words"]
