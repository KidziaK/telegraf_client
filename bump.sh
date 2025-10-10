#!/usr/bin/env bash
set -e

LATEST_TAG=$(git describe --tags --abbrev=0)
echo "Latest tag: $LATEST_TAG"

VERSION=${LATEST_TAG#v}

IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
NEW_TAG="v$NEW_VERSION"

echo "Creating new tag: $NEW_TAG"

git tag "$NEW_TAG"
git push origin "$NEW_TAG"

echo "Tag $NEW_TAG created and pushed successfully!"
