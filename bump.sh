#!/usr/bin/env bash
set -e

VERSION_TYPE=${1:-patch}

LATEST_TAG=$(git describe --tags --abbrev=0)
echo "Latest tag: $LATEST_TAG"

VERSION=${LATEST_TAG#v}

IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

case $VERSION_TYPE in
  major)
    NEW_MAJOR=$((MAJOR + 1))
    NEW_VERSION="$NEW_MAJOR.0.0"
    ;;
  minor)
    NEW_MINOR=$((MINOR + 1))
    NEW_VERSION="$MAJOR.$NEW_MINOR.0"
    ;;
  patch)
    NEW_PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
    ;;
  *)
    echo "Invalid version type: $VERSION_TYPE. Use 'major', 'minor', or 'patch'"
    exit 1
    ;;
esac

NEW_TAG="v$NEW_VERSION"

echo "Updating version to $NEW_VERSION in pyproject.toml"
sed -i '' "s/version = \"$VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

echo "Updating uv.lock"
uv lock

echo "Committing changes"
git add .
git commit -m "Bump version to $NEW_VERSION"

echo "Creating new tag: $NEW_TAG"
if git tag -l | grep -q "^$NEW_TAG$"; then
    echo "Tag $NEW_TAG already exists, deleting and recreating"
    git tag -d "$NEW_TAG"
    git push origin ":refs/tags/$NEW_TAG"
fi
git tag "$NEW_TAG"
git push origin "$NEW_TAG"

echo "Tag $NEW_TAG created and pushed successfully!"
