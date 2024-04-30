export OPENSSL_HOME=/home/int.orion.que/dev/app/ssl/
export PATH=$OPENSSL_HOME/bin:$PATH
export LD_LIBRARY_PATH=/home/int.orion.que/dev/app/ssl/lib:$LD_LIBRARY_PATH

export PATH=$/home/int.orion.que/dev/app/sqlite3/bin:$PATH
export LD_LIBRARY_PATH=/home/int.orion.que/dev/app/sqlite3/lib:$LD_LIBRARY_PATH

export PATH=/home/int.orion.que/dev/bin:$PATH
export VSCODE_CLI_DATA_DIR=/home/int.orion.que/dev/app/vscode

export PYTHONPATH=/home/int.orion.que/dev/app/python/bin/python3.9
export PATH=/home/int.orion.que/dev/app/python/bin:$PATH

cd /home/int.orion.que/dev/my_programs/arxiv-agent/

python() {
    /home/int.orion.que/dev/app/python/bin/python3.9 "$@"
}
pip() {
    python -m pip "$@"
}
# alias openssl='/home/int.orion.que/dev/app/ssl/bin/openssl'
openssl() {
    /home/int.orion.que/dev/app/ssl/bin/openssl "$@"
}
#  alias sqlite3='/home/int.orion.que/dev/app/sqlite3/bin/sqlite3'
sqlite3() {
    /home/int.orion.que/dev/app/sqlite3/bin/sqlite3 "$@"
}
python /home/int.orion.que/dev/my_programs/arxiv-agent/main.py