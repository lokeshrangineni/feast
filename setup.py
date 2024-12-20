# Copyright 2019 The Feast Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import glob
import os
import pathlib
import re
import shutil
import subprocess
from subprocess import CalledProcessError
import sys
from pathlib import Path

from setuptools import find_packages, setup, Command

NAME = "feast"
DESCRIPTION = "Python SDK for Feast"
URL = "https://github.com/feast-dev/feast"
AUTHOR = "Feast"
REQUIRES_PYTHON = ">=3.9.0"

REQUIRED = [
    "click>=7.0.0,<9.0.0",
    "colorama>=0.3.9,<1",
    "dill~=0.3.0",
    "protobuf>=4.24.0,<5.0.0",
    "Jinja2>=2,<4",
    "jsonschema",
    "mmh3",
    "numpy>=1.22,<2",
    "pandas>=1.4.3,<3",
    "pyarrow<18.1.0",
    "pydantic>=2.0.0",
    "pygments>=2.12.0,<3",
    "PyYAML>=5.4.0,<7",
    "requests",
    "SQLAlchemy[mypy]>1",
    "tabulate>=0.8.0,<1",
    "tenacity>=7,<9",
    "toml>=0.10.0,<1",
    "tqdm>=4,<5",
    "typeguard>=4.0.0",
    "fastapi>=0.68.0",
    "uvicorn[standard]>=0.14.0,<1",
    "uvicorn-worker",
    "gunicorn; platform_system != 'Windows'",
    "dask[dataframe]>=2024.2.1",
    "prometheus_client",
    "psutil",
    "bigtree>=0.19.2",
    "pyjwt",
]

GCP_REQUIRED = [
    "google-api-core>=1.23.0,<3",
    "googleapis-common-protos>=1.52.0,<2",
    "google-cloud-bigquery[pandas]>=2,<4",
    "google-cloud-bigquery-storage >= 2.0.0,<3",
    "google-cloud-datastore>=2.16.0,<3",
    "google-cloud-storage>=1.34.0,<3",
    "google-cloud-bigtable>=2.11.0,<3",
    "fsspec<=2024.9.0",
]

REDIS_REQUIRED = [
    "redis>=4.2.2,<5",
    "hiredis>=2.0.0,<3",
]

AWS_REQUIRED = ["boto3>=1.17.0,<2", "fsspec<=2024.9.0", "aiobotocore>2,<3"]

KUBERNETES_REQUIRED = ["kubernetes<=20.13.0"]

SNOWFLAKE_REQUIRED = [
    "snowflake-connector-python[pandas]>=3.7,<4",
]

SPARK_REQUIRED = [
    "pyspark>=3.0.0,<4",
]

SQLITE_VEC_REQUIRED = [
    "sqlite-vec==v0.1.1",
]
TRINO_REQUIRED = ["trino>=0.305.0,<0.400.0", "regex"]

POSTGRES_REQUIRED = [
    "psycopg[binary,pool]>=3.0.0,<4",
]

OPENTELEMETRY = ["prometheus_client", "psutil"]

MYSQL_REQUIRED = ["pymysql", "types-PyMySQL"]

HBASE_REQUIRED = [
    "happybase>=1.2.0,<3",
]

CASSANDRA_REQUIRED = [
    "cassandra-driver>=3.24.0,<4",
]

GE_REQUIRED = ["great_expectations>=0.15.41"]

AZURE_REQUIRED = [
    "azure-storage-blob>=0.37.0",
    "azure-identity>=1.6.1",
    "SQLAlchemy>=1.4.19",
    "pyodbc>=4.0.30",
    "pymssql",
]

IKV_REQUIRED = [
    "ikvpy>=0.0.36",
]

HAZELCAST_REQUIRED = [
    "hazelcast-python-client>=5.1",
]

IBIS_REQUIRED = [
    "ibis-framework>=9.0.0,<10",
    "ibis-substrait>=4.0.0",
]

GRPCIO_REQUIRED = [
    "grpcio>=1.56.2,<2",
    "grpcio-reflection>=1.56.2,<2",
    "grpcio-health-checking>=1.56.2,<2",
]

DUCKDB_REQUIRED = ["ibis-framework[duckdb]>=9.0.0,<10"]

DELTA_REQUIRED = ["deltalake"]

ELASTICSEARCH_REQUIRED = ["elasticsearch>=8.13.0"]

SINGLESTORE_REQUIRED = ["singlestoredb<1.8.0"]

COUCHBASE_REQUIRED = ["couchbase==4.3.2"]

MSSQL_REQUIRED = ["ibis-framework[mssql]>=9.0.0,<10"]

FAISS_REQUIRED = ["faiss-cpu>=1.7.0,<2"]
QDRANT_REQUIRED = ["qdrant-client>=1.12.0"]

GO_REQUIRED = ["cffi~=1.15.0"]

MILVUS_REQUIRED = ["pymilvus"]

CI_REQUIRED = (
    [
        "build",
        "virtualenv==20.23.0",
        "cryptography>=43.0,<44",
        "ruff>=0.8.0",
        "mypy-protobuf>=3.1",
        "grpcio-tools>=1.56.2,<2",
        "grpcio-testing>=1.56.2,<2",
        # FastAPI does not correctly pull starlette dependency on httpx see thread(https://github.com/tiangolo/fastapi/issues/5656).
        "httpx==0.27.2",
        "minio==7.2.11",
        "mock==2.0.0",
        "moto<5",
        "mypy>=1.4.1,<1.11.3",
        "urllib3>=1.25.4,<3",
        "psutil==5.9.0",
        "py>=1.11.0",  # https://github.com/pytest-dev/pytest/issues/10420
        "pytest>=6.0.0,<8",
        "pytest-asyncio<=0.24.0",
        "pytest-cov",
        "pytest-xdist",
        "pytest-benchmark>=3.4.1,<4",
        "pytest-lazy-fixture==0.6.3",
        "pytest-timeout==1.4.2",
        "pytest-ordering~=0.6.0",
        "pytest-mock==1.10.4",
        "pytest-env",
        "Sphinx>4.0.0,<7",
        "testcontainers==4.8.2",
        "python-keycloak==4.2.2",
        "pre-commit<3.3.2",
        "assertpy==1.1",
        "pip-tools",
        "pybindgen",
        "types-protobuf~=3.19.22",
        "types-python-dateutil",
        "types-pytz",
        "types-PyYAML",
        "types-redis",
        "types-requests<2.31.0",
        "types-setuptools",
        "types-tabulate",
        "virtualenv<20.24.2",
    ]
    + GCP_REQUIRED
    + REDIS_REQUIRED
    + AWS_REQUIRED
    + KUBERNETES_REQUIRED
    + SNOWFLAKE_REQUIRED
    + SPARK_REQUIRED
    + POSTGRES_REQUIRED
    + MYSQL_REQUIRED
    + TRINO_REQUIRED
    + GE_REQUIRED
    + HBASE_REQUIRED
    + CASSANDRA_REQUIRED
    + AZURE_REQUIRED
    + HAZELCAST_REQUIRED
    + IBIS_REQUIRED
    + GRPCIO_REQUIRED
    + DUCKDB_REQUIRED
    + DELTA_REQUIRED
    + ELASTICSEARCH_REQUIRED
    + SQLITE_VEC_REQUIRED
    + SINGLESTORE_REQUIRED
    + COUCHBASE_REQUIRED
    + OPENTELEMETRY
    + FAISS_REQUIRED
    + QDRANT_REQUIRED
    + MILVUS_REQUIRED
)

DOCS_REQUIRED = CI_REQUIRED
DEV_REQUIRED = CI_REQUIRED

# Get git repo root directory
repo_root = str(pathlib.Path(__file__).resolve().parent)

# README file from Feast repo root directory
README_FILE = os.path.join(repo_root, "README.md")
with open(README_FILE, "r", encoding="utf8") as f:
    LONG_DESCRIPTION = f.read()

# Add Support for parsing tags that have a prefix containing '/' (ie 'sdk/go') to setuptools_scm.
# Regex modified from default tag regex in:
# https://github.com/pypa/setuptools_scm/blob/2a1b46d38fb2b8aeac09853e660bcd0d7c1bc7be/src/setuptools_scm/config.py#L9
TAG_REGEX = re.compile(
    r"^(?:[\/\w-]+)?(?P<version>[vV]?\d+(?:\.\d+){0,2}[^\+]*)(?:\+.*)?$"
)

# Only set use_scm_version if git executable exists (setting this variable causes pip to use git under the hood)
if shutil.which("git"):
    use_scm_version = {"root": ".", "relative_to": __file__, "tag_regex": TAG_REGEX}
else:
    use_scm_version = None

PYTHON_CODE_PREFIX = "sdk/python"

def _generate_path_with_gopath():
    go_path = subprocess.check_output(["go", "env", "GOPATH"]).decode("utf-8")
    go_path = go_path.strip()
    path_val = os.getenv("PATH")
    path_val = f"{path_val}:{go_path}/bin"

    return path_val

class BuildGoProtosCommand(Command):
    description = "Builds the proto files into Go files."
    user_options = []

    def initialize_options(self):
        self.go_protoc = [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
        ]  # find_executable("protoc")
        self.proto_folder = os.path.join(repo_root, "protos")
        self.go_folder = os.path.join(repo_root, "go/protos")
        self.sub_folders = ["core", "registry", "serving", "types", "storage"]
        self.path_val = _generate_path_with_gopath()

    def finalize_options(self):
        pass

    def _generate_go_protos(self, path: str):
        proto_files = glob.glob(os.path.join(self.proto_folder, path))

        try:
            subprocess.check_call(
                self.go_protoc
                + [
                    "-I",
                    self.proto_folder,
                    "--go_out",
                    self.go_folder,
                    "--go_opt=module=github.com/feast-dev/feast/go/protos",
                    "--go-grpc_out",
                    self.go_folder,
                    "--go-grpc_opt=module=github.com/feast-dev/feast/go/protos",
                ]
                + proto_files,
                env={"PATH": self.path_val},
            )
        except CalledProcessError as e:
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")

    def run(self):
        go_dir = Path(repo_root) / "go" / "protos"
        go_dir.mkdir(exist_ok=True)
        for sub_folder in self.sub_folders:
            self._generate_go_protos(f"feast/{sub_folder}/*.proto")


setup(
    name=NAME,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        where=PYTHON_CODE_PREFIX, exclude=("java", "infra", "sdk/python/tests", "ui")
    ),
    package_dir={"": PYTHON_CODE_PREFIX},
    install_requires=REQUIRED,
    extras_require={
        "dev": DEV_REQUIRED,
        "ci": CI_REQUIRED,
        "gcp": GCP_REQUIRED,
        "aws": AWS_REQUIRED,
        "k8s": KUBERNETES_REQUIRED,
        "redis": REDIS_REQUIRED,
        "snowflake": SNOWFLAKE_REQUIRED,
        "spark": SPARK_REQUIRED,
        "trino": TRINO_REQUIRED,
        "postgres": POSTGRES_REQUIRED,
        "azure": AZURE_REQUIRED,
        "mysql": MYSQL_REQUIRED,
        "mssql": MSSQL_REQUIRED,
        "ge": GE_REQUIRED,
        "hbase": HBASE_REQUIRED,
        "docs": DOCS_REQUIRED,
        "cassandra": CASSANDRA_REQUIRED,
        "hazelcast": HAZELCAST_REQUIRED,
        "grpcio": GRPCIO_REQUIRED,
        "ibis": IBIS_REQUIRED,
        "duckdb": DUCKDB_REQUIRED,
        "ikv": IKV_REQUIRED,
        "delta": DELTA_REQUIRED,
        "elasticsearch": ELASTICSEARCH_REQUIRED,
        "sqlite_vec": SQLITE_VEC_REQUIRED,
        "singlestore": SINGLESTORE_REQUIRED,
        "couchbase": COUCHBASE_REQUIRED,
        "opentelemetry": OPENTELEMETRY,
        "faiss": FAISS_REQUIRED,
        "qdrant": QDRANT_REQUIRED,
        "go": GO_REQUIRED,
        "milvus": MILVUS_REQUIRED,
    },
    include_package_data=True,
    license="Apache",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={"console_scripts": ["feast=feast.cli:cli"]},
    use_scm_version=use_scm_version,
    setup_requires=[
        "pybindgen==0.22.0",  # TODO do we need this?
        "setuptools_scm>=6.2",  # TODO do we need this?
    ],
    cmdclass={
        "build_go_protos": BuildGoProtosCommand
    },
)
