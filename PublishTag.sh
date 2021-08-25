#!/bin/bash

read -p 'Rule: ' rule

poetry version $rule
git tag $(poetry version -s)
git push $(poetry version -s)
