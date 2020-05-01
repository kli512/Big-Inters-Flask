if [[ $# -ne 0 ]]; then
  echo "Usage: ./start_frontend.sh"
  exit 1
fi

source ~/venv/big-inters-server/bin/activate
export FLASK_APP=BigIntersFrontend
export FLASK_ENV=development
flask run --port 3000
