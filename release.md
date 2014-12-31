# New version

## Test on vagrant image

* `python setup.py sdist` and test the distribution created at `dist` folder;
* `cd demo && vagrant up`
* `vagrant ssh`
* `pip install /world/dist/...`
* Smoke test it


## Actually release

* Bump the version;
* Create a tag (see previous ones for the format);
* `python setup.py sdist upload`