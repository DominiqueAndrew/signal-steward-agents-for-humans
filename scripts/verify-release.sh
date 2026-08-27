#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
python_spec="${SIGNAL_STEWARD_PYTHON_BIN:-$repo_root/.venv/bin/python}"

if [[ "$python_spec" == */* ]]; then
  python_bin="$python_spec"
elif python_bin="$(command -v "$python_spec")"; then
  :
else
  python_bin=""
fi

cd "$repo_root"

if [[ -z "$python_bin" || ! -x "$python_bin" ]]; then
  printf 'missing configured Python %s; create the environment with: python3 -m venv .venv && .venv/bin/python -m pip install -e '\''.[dev]'\''\n' "$python_spec" >&2
  exit 2
fi

printf '%s\n' '== Signal Steward release verification =='
printf 'repository: %s\n' "$repo_root"
printf 'commit: '
git -C "$repo_root" rev-parse HEAD

printf '%s\n' '-- tests --'
PYTHONPATH="$repo_root" "$python_bin" -m pytest -rA "$repo_root/tests"

printf '%s\n' '-- dependencies --'
"$python_bin" -m pip check

printf '%s\n' '-- main holdout --'
PYTHONPATH="$repo_root" "$python_bin" -m benchmarks.run

printf '%s\n' '-- negative control --'
PYTHONPATH="$repo_root" "$python_bin" -m benchmarks.run --negative-control

printf '%s\n' '-- threshold sensitivity --'
PYTHONPATH="$repo_root" "$python_bin" -m benchmarks.run --sensitivity

printf '%s\n' '-- whitespace --'
git -C "$repo_root" diff --check
printf '%s\n' 'git diff --check: clean'

printf '%s\n' '-- secret-pattern scan --'
if git -C "$repo_root" grep -nE 'AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|sk-[A-Za-z0-9]{20,}' -- ':!docs/HUMAN_GATE_PACKET.md'; then
  printf '%s\n' 'secret-pattern scan: FAILED' >&2
  exit 1
else
  grep_status=$?
  if [[ "$grep_status" -ne 1 ]]; then
    exit "$grep_status"
  fi
  printf '%s\n' 'secret-pattern scan: clean'
fi

printf '%s\n' '== release verification passed =='
