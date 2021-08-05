import re
from typing import Any
from fastapi import Form
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, Query, Path, Body
from data import *
import jwt
import datetime
from functools import wraps
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
