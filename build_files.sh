 echo "BUILD START"
 python3.9 -m pip install -r requirements.txt
 python3.9 manage.py collectstatic --noinput --clear
 echo "BUILD END"
#!/bin/bash
set -e

# create build folder
mkdir -p staticfiles_build

# install all dependencies
pip install -r requirements.txt

# collect all static files into STATIC_ROOT
python manage.py collectstatic --noinput || true

# if empty, create placeholder
if [ -z "$(ls -A staticfiles_build 2>/dev/null)" ]; then
  echo "No static files collected — placeholder created by build_files.sh" > staticfiles_build/README.txt
fi
