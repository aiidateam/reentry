set -ev
case "$TEST_TYPE" in 
    unittests)
        pytest --cov-report=term-missing --cov=reentry
        ;;
    pre-commit)
        pre-commit run --all-files
        ;;
    *)
        echo "Invalid value for TEST_TYPE env variable."
        exit 1
esac
