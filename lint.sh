isort --profile black naive_fft tests
black naive_fft tests
flake8 --select BLK naive_fft tests
mypy --strict naive_fft tests
