if [[ $# -ne 0 ]]; then
  if [[ $# -ne 1 ]]; then
    echo "Usage: ./start_backend.sh API_KEY"
    exit 1
  fi

  if [[ ! $1 =~ ^RGAPI-.{8}-.{4}-.{4}-.{4}-.{12}$ ]]; then
    echo "Invalid API_KEY $1"
    exit 1
  fi

  sed -ri "s/API_KEY = .*/API_KEY = '$1'/" ./BigInters/Analyzer/Analyzer.py
fi

source ~/venv/big-inters-server/bin/activate
export FLASK_APP=BigInters
export FLASK_ENV=development
flask run --port 5000
