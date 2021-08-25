#!/bin/bash

read -p 'Rule: ' rule

poetry version $rule
git add .
git commit -m "New Tag"
git push
git tag v$(poetry version -s)
git push origin v$(poetry version -s)
