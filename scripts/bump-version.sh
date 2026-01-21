#!/usr/bin/env bash
#
# bump-version.sh - Bump version across all plugin manifests and changelog
#
# Usage:
#   ./scripts/bump-version.sh <new-version> [--tag]
#
# Examples:
#   ./scripts/bump-version.sh 1.1.0
#   ./scripts/bump-version.sh 2.0.0 --tag
#
# This script updates:
#   - plugins/ralph-it-up-roadmap/.claude-plugin/plugin.json
#   - .claude-plugin/marketplace.json
#   - CHANGELOG.md (moves [Unreleased] to new version with today's date)
#
# With --tag flag, also creates a git tag (v<version>)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Files to update
PLUGIN_JSON="$PROJECT_ROOT/plugins/ralph-it-up-roadmap/.claude-plugin/plugin.json"
MARKETPLACE_JSON="$PROJECT_ROOT/.claude-plugin/marketplace.json"
CHANGELOG="$PROJECT_ROOT/CHANGELOG.md"

usage() {
    echo "Usage: $0 <new-version> [--tag]"
    echo ""
    echo "Arguments:"
    echo "  new-version   Semantic version (e.g., 1.1.0, 2.0.0)"
    echo "  --tag         Also create a git tag (v<version>)"
    echo ""
    echo "Examples:"
    echo "  $0 1.1.0"
    echo "  $0 2.0.0 --tag"
    exit 1
}

# Validate semver format
validate_version() {
    local version="$1"
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo -e "${RED}Error: Invalid version format '$version'${NC}"
        echo "Version must be in semantic versioning format (e.g., 1.0.0, 2.1.3)"
        exit 1
    fi
}

# Get current version from plugin.json
get_current_version() {
    grep -o '"version": *"[^"]*"' "$PLUGIN_JSON" | head -1 | sed 's/.*"\([^"]*\)"/\1/'
}

# Update version in JSON file
update_json_version() {
    local file="$1"
    local new_version="$2"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed requires different syntax
        sed -i '' "s/\"version\": *\"[^\"]*\"/\"version\": \"$new_version\"/g" "$file"
    else
        sed -i "s/\"version\": *\"[^\"]*\"/\"version\": \"$new_version\"/g" "$file"
    fi
}

# Update CHANGELOG.md
update_changelog() {
    local new_version="$1"
    local today
    today=$(date +%Y-%m-%d)

    # Replace [Unreleased] header with new version and add new Unreleased section
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/## \[Unreleased\]/## [Unreleased]\n\n## [$new_version] - $today/" "$CHANGELOG"
        # Update the comparison links at the bottom
        sed -i '' "s|\[Unreleased\]: \(.*\)/compare/v[^.]*\.[^.]*\.[^.]*\.\.\.HEAD|[Unreleased]: \1/compare/v$new_version...HEAD\n[$new_version]: \1/compare/v$(get_current_version)...v$new_version|" "$CHANGELOG"
    else
        sed -i "s/## \[Unreleased\]/## [Unreleased]\n\n## [$new_version] - $today/" "$CHANGELOG"
        sed -i "s|\[Unreleased\]: \(.*\)/compare/v[^.]*\.[^.]*\.[^.]*\.\.\.HEAD|[Unreleased]: \1/compare/v$new_version...HEAD\n[$new_version]: \1/compare/v$(get_current_version)...v$new_version|" "$CHANGELOG"
    fi
}

# Main
main() {
    if [[ $# -lt 1 ]]; then
        usage
    fi

    local new_version="$1"
    local create_tag=false

    if [[ $# -ge 2 ]] && [[ "$2" == "--tag" ]]; then
        create_tag=true
    fi

    validate_version "$new_version"

    local current_version
    current_version=$(get_current_version)

    echo -e "${YELLOW}Bumping version: $current_version -> $new_version${NC}"
    echo ""

    # Update plugin.json
    echo -n "Updating $PLUGIN_JSON... "
    update_json_version "$PLUGIN_JSON" "$new_version"
    echo -e "${GREEN}done${NC}"

    # Update marketplace.json
    echo -n "Updating $MARKETPLACE_JSON... "
    update_json_version "$MARKETPLACE_JSON" "$new_version"
    echo -e "${GREEN}done${NC}"

    # Update CHANGELOG.md
    echo -n "Updating $CHANGELOG... "
    update_changelog "$new_version"
    echo -e "${GREEN}done${NC}"

    echo ""
    echo -e "${GREEN}Version bumped to $new_version${NC}"
    echo ""
    echo "Files modified:"
    echo "  - $PLUGIN_JSON"
    echo "  - $MARKETPLACE_JSON"
    echo "  - $CHANGELOG"
    echo ""

    # Create git tag if requested
    if [[ "$create_tag" == true ]]; then
        echo -n "Creating git tag v$new_version... "
        git tag -a "v$new_version" -m "Release v$new_version"
        echo -e "${GREEN}done${NC}"
        echo ""
        echo "Don't forget to push the tag:"
        echo "  git push origin v$new_version"
    fi

    echo "Next steps:"
    echo "  1. Review changes: git diff"
    echo "  2. Commit: git add -A && git commit -m 'Release v$new_version'"
    if [[ "$create_tag" == false ]]; then
        echo "  3. Tag: git tag -a v$new_version -m 'Release v$new_version'"
    fi
    echo "  4. Push: git push && git push --tags"
}

main "$@"
