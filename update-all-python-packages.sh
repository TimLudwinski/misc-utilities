set -x

pip list -o | cut -f1 -d' ' | tr " " "\n" | tail +3 | xargs -n100 pip install -U

set +x
