# mowas converter

Serves mowas messages as geojson using nice python-based Flask-Webframework

### Installation

In an Linux environment install it is recommended to run mowas converter in an python virtualenv

Generate and activate python virtualenv

```sh
virtualenv venv
source ./venv/bin/activate
```

Install requirements

```sh
pip install -r requirements.txt
```

Run mowas_converter

```sh
python mowas_converter.py
```

WSGI example
```sh
        WSGIDaemonProcess mowas_converter user=mowas_converter group=mowas_converter threads=5
        WSGIScriptAlias /mowas_converter /data/mowas_converter/mowas_converter.wsgi

        <Directory /data/mowas_converter/>
                WSGIProcessGroup mowas_converter
                WSGIApplicationGroup %{GLOBAL}
                Options FollowSymLinks Indexes
                Require all granted
        </Directory>
```

### Version

0.0.1-dev
