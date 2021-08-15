#verify-script
clear

set -e
echo "starting verify with pylint and mypy... ";


# --------------------------
mypy "./flask_restx_square" ;
pylint "./flask_restx_square";



echo "end verify. "
