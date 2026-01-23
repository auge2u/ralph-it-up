#!/usr/bin/env bash
#
# validate-gates-handler.sh
# Native Claude Code hook for quality gate validation
#
# Replaces validate_quality_gates.py for simple, dependency-free validation.
# Can be run standalone or as a post-execution hook.
#
# Usage:
#   ./validate-gates-handler.sh [--json] [--quiet] [--output-dir DIR]
#
# Exit codes:
#   0 - All gates passed
#   1 - Blocker gates failed
#   2 - No scopecraft directory found
#

set -euo pipefail

# Defaults
SCOPECRAFT_DIR="${PWD}/scopecraft"
OUTPUT_JSON=false
QUIET=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      OUTPUT_JSON=true
      shift
      ;;
    --quiet|-q)
      QUIET=true
      shift
      ;;
    --output-dir|-o)
      SCOPECRAFT_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Check scopecraft directory exists
if [[ ! -d "$SCOPECRAFT_DIR" ]]; then
  if [[ "$OUTPUT_JSON" == true ]]; then
    echo '{"error": "scopecraft directory not found", "result": "FAIL"}'
  else
    echo "Error: scopecraft directory not found at $SCOPECRAFT_DIR" >&2
  fi
  exit 2
fi

# Initialize gate results
declare -A gates
declare -A gate_details
all_passed=true

# Gate 1: all_outputs_exist (exactly 6 .md files)
file_count=$(find "$SCOPECRAFT_DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
if [[ "$file_count" -eq 6 ]]; then
  gates[all_outputs_exist]="PASS"
  gate_details[all_outputs_exist]="$file_count files"
else
  gates[all_outputs_exist]="FAIL"
  gate_details[all_outputs_exist]="Expected 6, found $file_count"
  all_passed=false
fi

# Gate 2: phases_in_range (3-5 ## Phase headers in ROADMAP.md)
roadmap_file="$SCOPECRAFT_DIR/ROADMAP.md"
if [[ -f "$roadmap_file" ]]; then
  phase_count=$(grep -cE "^## Phase [0-9]" "$roadmap_file" 2>/dev/null || echo 0)
  if [[ "$phase_count" -ge 3 ]] && [[ "$phase_count" -le 5 ]]; then
    gates[phases_in_range]="PASS"
    gate_details[phases_in_range]="$phase_count phases"
  else
    gates[phases_in_range]="FAIL"
    gate_details[phases_in_range]="Expected 3-5, found $phase_count"
    all_passed=false
  fi
else
  gates[phases_in_range]="FAIL"
  gate_details[phases_in_range]="ROADMAP.md not found"
  all_passed=false
fi

# Gate 3: stories_have_acceptance_criteria (5+ Acceptance Criteria sections)
epics_file="$SCOPECRAFT_DIR/EPICS_AND_STORIES.md"
if [[ -f "$epics_file" ]]; then
  ac_count=$(grep -c "Acceptance Criteria" "$epics_file" 2>/dev/null || echo 0)
  if [[ "$ac_count" -ge 5 ]]; then
    gates[stories_have_acceptance_criteria]="PASS"
    gate_details[stories_have_acceptance_criteria]="$ac_count sections"
  else
    gates[stories_have_acceptance_criteria]="FAIL"
    gate_details[stories_have_acceptance_criteria]="Expected >=5, found $ac_count"
    all_passed=false
  fi
else
  gates[stories_have_acceptance_criteria]="FAIL"
  gate_details[stories_have_acceptance_criteria]="EPICS_AND_STORIES.md not found"
  all_passed=false
fi

# Gate 4: risks_documented (3+ risk table rows with Technical/Product/GTM)
risks_file="$SCOPECRAFT_DIR/RISKS_AND_DEPENDENCIES.md"
if [[ -f "$risks_file" ]]; then
  risk_count=$(grep -cE "\| .+ \| (Technical|Product|GTM)" "$risks_file" 2>/dev/null || echo 0)
  if [[ "$risk_count" -ge 3 ]]; then
    gates[risks_documented]="PASS"
    gate_details[risks_documented]="$risk_count risks"
  else
    gates[risks_documented]="FAIL"
    gate_details[risks_documented]="Expected >=3, found $risk_count"
    all_passed=false
  fi
else
  gates[risks_documented]="FAIL"
  gate_details[risks_documented]="RISKS_AND_DEPENDENCIES.md not found"
  all_passed=false
fi

# Gate 5: metrics_defined (North Star Metric section exists)
metrics_file="$SCOPECRAFT_DIR/METRICS_AND_PMF.md"
if [[ -f "$metrics_file" ]]; then
  if grep -q "North Star Metric" "$metrics_file" 2>/dev/null; then
    gates[metrics_defined]="PASS"
    gate_details[metrics_defined]="Section found"
  else
    gates[metrics_defined]="FAIL"
    gate_details[metrics_defined]="North Star Metric section not found"
    all_passed=false
  fi
else
  gates[metrics_defined]="FAIL"
  gate_details[metrics_defined]="METRICS_AND_PMF.md not found"
  all_passed=false
fi

# Gate 6: no_todo_placeholders (zero [TODO], [TBD], [PLACEHOLDER])
# Note: grep returns 1 if no matches, so we use || true to prevent pipefail from exiting
placeholder_count=$( (grep -rE "\[TODO\]|\[TBD\]|\[PLACEHOLDER\]" "$SCOPECRAFT_DIR" 2>/dev/null || true) | wc -l | tr -d ' ')
if [[ "$placeholder_count" -eq 0 ]]; then
  gates[no_todo_placeholders]="PASS"
  gate_details[no_todo_placeholders]="0 placeholders"
else
  gates[no_todo_placeholders]="FAIL"
  gate_details[no_todo_placeholders]="Found $placeholder_count placeholders"
  all_passed=false
fi

# Output results
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [[ "$OUTPUT_JSON" == true ]]; then
  # JSON output for programmatic consumption
  cat <<EOF
{
  "timestamp": "$timestamp",
  "gates": {
    "all_outputs_exist": { "passed": $([ "${gates[all_outputs_exist]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[all_outputs_exist]}" },
    "phases_in_range": { "passed": $([ "${gates[phases_in_range]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[phases_in_range]}" },
    "stories_have_acceptance_criteria": { "passed": $([ "${gates[stories_have_acceptance_criteria]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[stories_have_acceptance_criteria]}" },
    "risks_documented": { "passed": $([ "${gates[risks_documented]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[risks_documented]}" },
    "metrics_defined": { "passed": $([ "${gates[metrics_defined]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[metrics_defined]}" },
    "no_todo_placeholders": { "passed": $([ "${gates[no_todo_placeholders]}" == "PASS" ] && echo true || echo false), "details": "${gate_details[no_todo_placeholders]}" }
  },
  "result": "$([ "$all_passed" == true ] && echo PASS || echo FAIL)"
}
EOF
else
  # Human-readable output
  if [[ "$QUIET" != true ]]; then
    echo ""
    echo "============================================================"
    echo "QUALITY GATE VALIDATION RESULTS"
    echo "============================================================"
    echo ""

    for gate in all_outputs_exist phases_in_range stories_have_acceptance_criteria risks_documented metrics_defined no_todo_placeholders; do
      if [[ "${gates[$gate]}" == "PASS" ]]; then
        echo -e "\033[92m✓ PASS\033[0m [$gate]"
      else
        echo -e "\033[91m✗ FAIL\033[0m [$gate]"
      fi
      echo "       ${gate_details[$gate]}"
      echo ""
    done

    echo "------------------------------------------------------------"

    passed_count=0
    failed_count=0
    for gate in "${!gates[@]}"; do
      if [[ "${gates[$gate]}" == "PASS" ]]; then
        ((passed_count++)) || true
      else
        ((failed_count++)) || true
      fi
    done

    echo "Total: 6 | Passed: $passed_count | Failed: $failed_count"
    echo "------------------------------------------------------------"
    echo ""

    if [[ "$all_passed" == true ]]; then
      echo -e "\033[92m✅ ALL QUALITY GATES PASSED - Ready for LOOP_COMPLETE\033[0m"
    else
      echo -e "\033[91m❌ QUALITY GATES FAILED - Cannot issue LOOP_COMPLETE\033[0m"
    fi
  fi
fi

# Exit with appropriate code
if [[ "$all_passed" == true ]]; then
  exit 0
else
  exit 1
fi
