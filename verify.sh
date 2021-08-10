#verify-script
clear

echo "strating verify with pylint and mypy... ";

# ----------------------------
echo "start verify autowire.. ";
pylint "./Flask-Restx/Autowire_Decorator/autowire_decorator.py";
mypy "./Flask-Restx/Autowire_Decorator/autowire_decorator.py"

# ----------------------------
echo "start verify create model.. ";
pylint "./Flask-Restx/Autowire_Decorator/model.py" ;
mypy "./Flask-Restx/Autowire_Decorator/model.py" ;

# ----------------------------
echo "start verify path param.. ";
pylint "./Flask-Restx/Autowire_Decorator/path_param.py" ;
mypy "./Flask-Restx/Autowire_Decorator/path_param.py" ;

# ----------------------------
echo "start verify get parser.. ";
pylint "./Flask-Restx/Autowire_Decorator/parser_api.py" ;
mypy "./Flask-Restx/Autowire_Decorator/parser_api.py" ;

# ----------------------------
echo "start verify main app.. ";
pylint "./Flask-Restx/app-v2.py" ;
mypy "./Flask-Restx/app-v2.py" ;


echo "end verify. "
