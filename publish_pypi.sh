rm -fr build
rm -fr dist
rm -fr simpletemplate.egg-info

python3 setup.py sdist bdist_wheel

twine upload dist/*