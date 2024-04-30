LOG_DIR="/home/int.orion.que/dev/my_programs/arxiv-agent/logs"

# if dir exists
if [ -d "$LOG_DIR" ]; then
  # delete all logs
  find "$LOG_DIR" -type f -exec rm -f {} \;
  echo "All logs cleared."
else
  echo "Log dir $LOG_DIR does not exist."
fi

OUTPUT_DIR="/home/int.orion.que/dev/my_programs/arxiv-agent/output"
FILE_TYPES=("*.json" "*.md" "*.pdf")
# loop through all file types
if [ -d "$OUTPUT_DIR" ]; then
    for FILE_TYPE in "${FILE_TYPES[@]}"; do
    # find and delete
    find "$OUTPUT_DIR" -type f -name "$FILE_TYPE" -exec rm -f {} \;
    echo "All $FILE_TYPE files deleted."
    done
else
  echo "Output dir $OUTPUT_DIR does not exist."
fi