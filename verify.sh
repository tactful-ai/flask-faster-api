#verify-script
clear

set -e
echo "starting verify with pylint and mypy... ";


# --------------------------
mypy "./flask_fastx" ;
pylint -d R0801 "./flask_fastx";



echo "end verify. "
