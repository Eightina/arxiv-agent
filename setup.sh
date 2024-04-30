# First configure LLM api according to https://docs.deepwisdom.ai/main/zh/guide/get_started/configuration/llm_api_configuration.html
# In this script, you need to configure:
#   * proper python env path
#   * target_dir which locates the metagpt tool dir
# Then this script can:
#   * check your python version
#   * install some dependencies (optional)
#   * create essential dirs for data output and log
#   * create hard links for customized metagpt tools (because they need to be registered under site-packages/metagpt)

# assign python env and check if main version number < 3 or sub version number < 9
python() {
    /home/int.orion.que/dev/app/python/bin/python3.9 "$@"
}
pip() {
    python -m pip "$@"
}
python_version=$(python --version 2>&1)
# extracting main version number
major_version=$(echo "$python_version" | awk '{print $2}' | cut -d'.' -f1)
# extracting sub version number
minor_version=$(echo "$python_version" | awk '{print $2}' | cut -d'.' -f2)
if [[ $major_version -lt 3 ]] || [[ ($major_version -eq 3) && ($minor_version -lt 9) ]]; then
    echo "Error: Python version must be 3.9 or higher." >&2
    exit 1
else
    echo "Python version is 3.9 or higher."
fi

# install dependencies
# pip install bs4
# pip install metagpt


# Check if ./log directory exists, if not, create it
if [ ! -d "./log" ]; then
    mkdir ./log
    echo "Created directory: ./log"
fi
# Check if ./output directory exists, if not, create it
if [ ! -d "./output" ]; then
    mkdir ./output
    echo "Created directory: ./output"
fi
# Check if ./output/outdated directory exists, if not, create it
if [ ! -d "./output/outdated" ]; then
    mkdir ./output/outdated
    echo "Created directory: ./output/outdated"
fi
# Check if ./output/raw directory exists, if not, create it
if [ ! -d "./output/raw" ]; then
    mkdir ./output/raw
    echo "Created directory: ./output/raw"
fi
if [ ! -d "./output/raw" ]; then
    mkdir ./output/pdf
    echo "Created directory: ./output/pdf"
fi


# create hard links for metagpt tools
source_dir="./agent/custom_tools/"
target_dir="/home/int.orion.que/dev/app/python/lib/python3.9/site-packages/metagpt/tools/libs/"
# Iterate through all .py files in the source directory
for file in "$source_dir"*.py; do
    filename=$(basename "$file" .py)
    
    # Create a hard link in the target directory
    ln "$file" "$target_dir/$filename.py"
    
    # Print message
    echo "Created hard link for $file in $target_dir"
done