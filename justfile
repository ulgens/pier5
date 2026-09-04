# List available commands
default:
    @just --list --unsorted

# Run tests
[group("tests")]
test *ARGS:
    uv run pytest {{ ARGS }}

# Run tests but headless - doesn't work under the latest macOS, intended to use in CI environments
[group("tests")]
test_headless *ARGS:
    xvfb-run -a uv run pytest {{ ARGS }}
