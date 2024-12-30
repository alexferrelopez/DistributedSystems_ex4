In a virtual environment, run the following command to install the required packages:

If necessary, upgrade your version of pip:
```bash
python -m pip install --upgrade pip
```

Install the required packages:
```bash
pip install grpcio
pip install grpcio-tools
```

For windows, install the windows-curses package:
```bash
pip install windows-curses
```

To generate the Python code from the protocol buffer file, run the following command:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messanger.proto
```