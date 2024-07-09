# run_tests.sh
export PYTHONPATH=$(pwd)/src
echo "PYTHONPATH is set to: $PYTHONPATH"
pytest --maxfail=1 -q