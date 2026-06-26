#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="${REPO_ROOT}/data"

clean_dir_contents() {
    local dir="$1"
    [[ -d "$dir" ]] || return 0
    local entry
    shopt -s nullglob dotglob
    for entry in "$dir"/*; do
        rm -rf "$entry"
    done
    shopt -u nullglob dotglob
}

clean_dir_contents "${DATA}/cache/integration/outputs"
clean_dir_contents "${DATA}/cache/integration"
clean_dir_contents "${DATA}/jobs"
clean_dir_contents "${DATA}/output"
clean_dir_contents "${DATA}/online"

rm -rf "${DATA}"/testing/cat_input_* "${DATA}"/testing/cat_output_* 2>/dev/null || true

clean_dir_contents "${DATA}/input/structure/outputs"

rm -f \
    "${REPO_ROOT}/bom.car" \
    "${REPO_ROOT}/bom.json" \
    "${REPO_ROOT}/invoice.json" \
    "${REPO_ROOT}/order.json"

echo "Cleaned ephemeral test data under ${DATA}"
