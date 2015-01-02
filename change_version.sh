version=$1
git_tag="v${version}"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version number>"
    exit 2
fi

# Set version and build to version
sed -i .bak -e "s/version = '.*'/version = '${version}'/g" docs/conf.py
sed -i .bak -e "s/release = '.*'/release = '${version}'/g" docs/conf.py

# Replace version in __init__.py
sed -i .bak -e "s/__version__ = '.*'/__version__ = '${version}'/g" pylsdj/__init__.py
sed -i .bak -e "s/version='.*'/version='${version}'/g" setup.py

# Remove backup files
find . -name "*.bak" -exec rm {} \;

# Tag revision as this version in git
git commit -a -m "Bumping version to ${git_tag}"
git tag ${git_tag}
