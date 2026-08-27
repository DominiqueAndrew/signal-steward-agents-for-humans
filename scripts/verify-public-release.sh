#!/usr/bin/env bash
set -euo pipefail

public_repo="${SIGNAL_STEWARD_PUBLIC_REPO:-DominiqueAndrew/signal-steward-agents-for-humans}"
public_branch="${SIGNAL_STEWARD_PUBLIC_BRANCH:-main}"
github_repo="https://github.com/${public_repo}.git"
api_base="https://api.github.com/repos/${public_repo}"
curl_args=(--fail --silent --show-error --location --max-time 20)
github_token="${SIGNAL_STEWARD_GITHUB_TOKEN:-${GITHUB_TOKEN:-}}"
if [[ -n "$github_token" ]]; then
  curl_args+=( -H "Authorization: Bearer $github_token" )
fi

printf '%s\n' '== Signal Steward public release verification =='
printf 'repository: %s\n' "$public_repo"
printf 'branch: %s\n' "$public_branch"

public_sha="$(git ls-remote "$github_repo" "refs/heads/${public_branch}" | awk 'NF >= 1 { print $1; exit }')"
if [[ ! "$public_sha" =~ ^[0-9a-f]{40}$ ]]; then
  printf 'could not resolve a 40-character public branch SHA\n' >&2
  exit 1
fi

raw_base="https://raw.githubusercontent.com/${public_repo}/${public_sha}"
receipt="$(curl "${curl_args[@]}" "${raw_base}/docs/RELEASE_RECEIPT.md")"
release_sha="$(printf '%s\n' "$receipt" | awk '/^\*\*Validated release-content tree:\*\*/ { match($0, /`[0-9a-f]{40}`/); if (RSTART) { print substr($0, RSTART + 1, RLENGTH - 2); exit } }')"
if [[ ! "$release_sha" =~ ^[0-9a-f]{40}$ ]]; then
  printf 'receipt does not expose a valid release-content SHA\n' >&2
  exit 1
fi

printf 'public_main: %s\n' "$public_sha"
printf 'receipt_release_content: %s\n' "$release_sha"
printf 'artifact_ref: %s\n' "$public_sha"

printf '%s\n' '-- receipt boundary --'
compare_json="$(curl "${curl_args[@]}" -H 'Accept: application/vnd.github+json' "${api_base}/compare/${release_sha}...${public_sha}")"
printf '%s' "$compare_json" | python3 -c '
import json
import sys

comparison = json.load(sys.stdin)
comparison_status = comparison.get("status")
behind_by = comparison.get("behind_by")
files = [item.get("filename") for item in comparison.get("files", [])]
unexpected = sorted({name for name in files if name != "docs/RELEASE_RECEIPT.md"})
if comparison_status not in {"identical", "ahead"} or behind_by != 0:
    raise SystemExit("release boundary is not ancestor-safe: status={!r} behind_by={!r}".format(comparison_status, behind_by))
if len(files) >= 300:
    raise SystemExit("GitHub compare file list may be truncated at the 300-file API cap")
if unexpected:
    raise SystemExit("public main contains changes outside the receipt-only boundary: {}".format(unexpected))
print("status={} behind_by={} changed_files={}".format(comparison_status, behind_by, len(files)))
'

artifact_paths=(
  README.md
  LICENSE
  RESEARCH.md
  RESULTS.md
  signal-steward-threat-model.md
  docs/DEVPOST_DRAFT.md
  docs/HUMAN_GATE_PACKET.md
  docs/PUBLIC_CASES.md
  docs/RELEASE_RECEIPT.md
  docs/architecture-diagram.png
  docs/architecture-diagram.svg
  docs/architecture.md
  docs/demo-script.md
  scripts/verify-release.sh
  scripts/verify-public-release.sh
)

printf '%s\n' '-- public artifacts --'
for artifact_path in "${artifact_paths[@]}"; do
  http_code="$(curl "${curl_args[@]}" -o /dev/null -w '%{http_code}' "${raw_base}/${artifact_path}")"
  printf '%s %s\n' "$http_code" "$artifact_path"
  [[ "$http_code" == 200 ]]
done

png_type="$(curl "${curl_args[@]}" -D - -o /dev/null "${raw_base}/docs/architecture-diagram.png" | awk -F: 'tolower($1) == "content-type" { value=$2 } END { gsub("\r", "", value); sub("^[[:space:]]+", "", value); print tolower(value) }')"
svg_type="$(curl "${curl_args[@]}" -D - -o /dev/null "${raw_base}/docs/architecture-diagram.svg" | awk -F: 'tolower($1) == "content-type" { value=$2 } END { gsub("\r", "", value); sub("^[[:space:]]+", "", value); print tolower(value) }')"
printf 'architecture_png_content_type: %s\n' "$png_type"
printf 'architecture_svg_content_type: %s\n' "$svg_type"
[[ "$png_type" == image/png ]]
[[ "$svg_type" == image/svg+xml ]]

printf '%s\n' '-- repository metadata --'
metadata_json="$(curl "${curl_args[@]}" -H 'Accept: application/vnd.github+json' "$api_base")"
printf '%s' "$metadata_json" | python3 -c '
import json
import sys

metadata = json.load(sys.stdin)
visibility = metadata.get("visibility")
if visibility != "public":
    raise SystemExit("repository visibility is not public: {!r}".format(visibility))
if metadata.get("archived") or metadata.get("disabled"):
    raise SystemExit("repository is archived or disabled")
license_id = (metadata.get("license") or {}).get("spdx_id")
if license_id not in {"Apache-2.0", "MIT"}:
    raise SystemExit("repository license is not MIT/Apache: {!r}".format(license_id))
print("visibility={} archived={} disabled={} license={}".format(visibility, metadata.get("archived"), metadata.get("disabled"), license_id))
'

printf '%s\n' '== public release verification passed =='
