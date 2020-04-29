if [[ $# -ne 0 ]]; then
  if [[ $# -ne 1 ]]; then
    echo "Usage: ./start_frontend.sh NGROKURL"
    echo "NGROKURL is formatted as some string [a-z0-9]+.ngrok.io or just the [a-z0-9] prefix"
    exit 1
  fi

  if [[ $1 =~ ^[a-zA-Z0-9]+$ ]]; then
    url="$1.ngrok.io"
  else
    url=$1
  fi

  if [[ ! $url =~ ^[a-zA-Z0-9]+.ngrok.io$ ]]; then
    echo "Invalid url found from arg \"$1\". URL found: $url"
    exit 1
  fi

  sed -ri "s/[0-9a-zA-Z]+.ngrok.io/$1/" ./BigIntersFrontend/templates/main_page/index.html
fi

source ~/venv/big-inters-server/bin/activate
export FLASK_APP=BigIntersFrontend
export FLASK_ENV=development
flask run --port 3000
