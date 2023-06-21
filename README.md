
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="https://github.com/ValentinSiegert/aTLAS/raw/master/_logos/atlas_orange.svg" alt="aTLAS orange" height="80">
  </a>
  <h2>TrustLab</h2>
  <p>
    aTLAS – evaluating trust for autonomous web apps in a redecentralized web
    <!--<br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <a href="https://vsr-www.informatik.tu-chemnitz.de/projects/2020/atlas/demo/">View Demo</a>
    ·
    <a href="https://gitlab.hrz.tu-chemnitz.de/vsr/phd/siegert/trustlab/-/issues">Report Bug</a>
    ·
    <a href="mailto:valentin.siegert@informatik.tu-chemnitz.de?subject=Question on aTLAS">Ask Question</a>
  </p>
</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#-about)
  - [Built With](#-built-with)
- [Getting Started](#-getting-started)
  - [Local Setup](#-local-setup)
  - [Setup for VSRians](#-setup-for-vsrians)
- [Usage](#-usage)
  - [Local Usage](#-local-usage)
  - [Usage for VSRians](#-usage-for-vsrians)
- [Insights](#-insights)
  - [Notes](#-notes)
  - [How To Scenario](#-how-to-scenario)
  - [For Later](#-for-later)
- [Authors & Contributors](#-authors--contributors)
- [Acknowledgements](#-acknowledgements)

</details>


## 💡 About

<table>
<tr>
<td>

This is the main repository of the aTLAS testbed which includes the testbed's web server and director.
Therewith, all front-end capabilities are fully included, but not all back-end logic, which is derived
from the [submodule trustlab_host][trustlab-host-repo].
The submodule is used as a library for certain models by the web server and the director and 
includes all aspects of the testbed environment with supervisor and interacting web agents.

> More details are to be found as well at the [project page][atlas-project].

<details>
<summary>Further Details</summary>

The redecentralization of the web introduces new challenges on trusting data from other sources
due to many unknown or even hidden parties.
An application working trustworthy in a decentralized web must evaluate trust and take trustaware decisions
autonomously without relying on a centralized infrastructure.
This autonomy and the huge amount of available applications necessitates the web to be modelled as
an open dynamic Multi-Agent System (MAS).
To evaluate the trust of web agents, the most suitable trust models need to be identified and used.
Despite the various trust models proposed in the literature for evaluating a web agent’s trust, 
the examination of them with different scenarios and configurations is not trivial.
To address these challenges, we initiated aTLAS, a Trust Laboratory of Multi-Agent Systems
which is a web-based wizard testbed for researchers and web engineers to evaluate trust models systematically.
aTLAS will enable future research regarding trust evaluations in a decentralized web.

The aTLAS project intends to examine trust for a redecentralization of the web.
It enables a broad comparison of trust mechanics, scales and models from the literature
within the current state of the art.
Therefore, it runs and evaluates multi-agent system scenarios, which are defined beforehand.
As the redencentralization of the web necessitates it to be modeled as a open dynamic multi-agent system,
such a laboratory can support the current situation where a comparision of trust approaches
for a decentralized web has to be done manually with a high effort.

> Relevant Publications:
> 
> [aTLAS: a Testbed to Examine Trust for a Redecentralized Web][atlas-paper]
> 
> [WTA: Towards a Web-based Testbed Architecture][wta-paper]

</details>
</td>
</tr>
</table>

### 🧱 Built With

1. Python 3.7
2. Django v2
3. Python pipenv
4. Redis Server
5. Microsoft SQL Server with ODBC Driver 17 OR SQLite

## ⚡ Getting Started

> By default, please follow the local setup. The setup for VSRians is only for those knowing what they do there.

### ⚙️ Local Setup

1. Install [Redis][redis-quickstart].

2. Install [MongoDB][mongodb-quickstart].

3. Clone Git Repository, [including all submodules][git-submodules].

4. Setup pipenv in project root:
    ```shell
    pipenv install
    ```
   >For more information on pipenv, cf. [Pipenv: Python Dev Workflow for Humans][pipenv].
        
5. Modify ``Additional Options`` of your django configuration (for no auto-reload after editing scenario files) with:
    ```shell
    --noreload
    ```

6. Install also at least one supervisor, c.f. [submodule trustlab_host][trustlab-host-repo].

### 🏢 Setup for VSRians

<details>
<summary>For VSRians only</summary>

1. Install [Microsoft ODBC Driver 17][microsoft-odbc-driver] (Windows/Linux/MacOS)

2. Install [MongoDB][mongodb-quickstart].

3. Clone Git Repository, [including all submodules][git-submodules].

4. Configure merge driver for dealing with ``.gitattributes`` or rather the merge strategy:
    ```shell
    git config merge.ours.driver true
    ```

5. Setup pipenv in project root:
    ```shell
    pipenv install
    ```
   >For more information on pipenv, cf. [Pipenv: Python Dev Workflow for Humans][pipenv].

   ODBC on MAC:
    - If you installed this formula with the registration option (default), you'll need to manually remove
    ``[ODBC Driver 17 for SQL Server]`` section from odbcinst.ini after the formula is uninstalled.
    This can be done by executing:
        ```shell
        odbcinst -u -d -n "ODBC Driver 17 for SQL Server"
        ```
        
6. Modify ``Additional Options`` of your django configuration (for no auto-reload after editing scenario files) with:
    ```shell
    --noreload
    ```
</details>

## 👟 Usage

> By default, please follow the local usage. The usage for VSRians is only for those knowing what they do there.

### 🏠 Local Usage

1. Run local Redis server in shell
    ```shell
    redis-server
    ```
   
2. Run local [MongoDB][mongodb-quickstart].  
    >Dependent on your OS the execution instructions are part of the guide in the link above. 

3. Run aTLAS:
    ```bash
    python manage.py runserver 8000 --noreload
    ```

4. Run at least on supervisor with the [submodule trustlab_host][trustlab-host-repo] and connect it to aTLAS director.


### 🏢 Usage for VSRians

<details>
<summary>For VSRians only</summary>

1. Change MongoDBURI in [trustlab/lab/config.py](trustlab/lab/config.py) _OR_  
   run local [MongoDB][mongodb-quickstart].  
    >Dependent on your OS the execution instructions are part of the guide in the link above.

2. Run aTLAS:
    ```bash
    python manage.py runserver 8000 --noreload
    ```

3. Run at least on supervisor with the [submodule trustlab_host][trustlab-host-repo] and connect it to aTLAS director.

</details>

## 👀 Insights

### 📃 Notes

- The ``settings.py`` is via ``.gitattributes`` under merge strategy to have always different versions in develop and master branch.
  To hold this construction, **always** merge without fast-forward.
  Thus, always create a new commit, when you merge the two branches.

- djtrustlab is the main Django project with settings.py, trustlab is the subproject with all the code.

- All deploy-configs for daphne and nginx (and deprecated gunicorn) are in ``_deploy-configs/``, c.f. [DEPLOY.md](_deploy-configs/DEPLOY.md).

### 📩 How To Scenario

- Scenario configurations can be placed in ``trustlab/lab/scenarios``.

- Every scenario configuration file has to end with ``_scenario.py``.

- All scenario parameters require to be the upperCase version of the respective ``Scenario.scenario_args`` arguments.

- Possible scenario arguments derive from ``Scenario.scenario_args`` arguments list, where parameters without default value are mandatory for scenario configuration file as well.

- You can make use of the scenario generation script at [_scenario_generation/](_scenario_generation/README.md) to generate larger scenarios.

### ⌚ For Later

- NetworkX for graph structure in backend: https://networkx.github.io/

- NVD3 for graphs and diagrams in frontend: http://nvd3.org/

## ✍ Authors & Contributors

The original setup of this repository is by the first author [Valentin Siegert][valentin-siegert-website].

All authors of this work in alphabetic surname order:

- [Shovra Das](https://github.com/shovradas)
- [Martin Gaedke](https://vsr.informatik.tu-chemnitz.de/people/gaedke)
- Arved Kirchhoff
- [Mahda Noura](https://vsr.informatik.tu-chemnitz.de/people/mahdanoura)
- [Valentin Siegert][valentin-siegert-website]

## 👍 Acknowledgements

The authors acknowledge the work of the following students in alphabetic surname order:

- Jun Li
- Marten Rogall
- Bastian Rose


<!-- Identifiers, in alphabetical order -->
[atlas-logo-orange]: https://github.com/ValentinSiegert/aTLAS/raw/master/_logos/atlas_orange.svg
[atlas-paper]: https://vsr.informatik.tu-chemnitz.de/research/publications/2020/010/
[atlas-project]: https://vsr.informatik.tu-chemnitz.de/projects/2020/atlas/
[demo-extern]: https://vsr-www.informatik.tu-chemnitz.de/projects/2020/atlas/demo/
[demo-intern]: https://vsr-dem0.informatik.tu-chemnitz.de/trustlab/
[git-submodules]: https://git-scm.com/book/en/v2/Git-Tools-Submodules
[microsoft-odbc-driver]: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-2017
[mongodb-quickstart]: https://www.mongodb.com/docs/manual/installation/
[pipenv]: https://pipenv.pypa.io/en/latest/
[redis-quickstart]: https://redis.io/topics/quickstart
[trustlab-host-repo]: https://gitlab.hrz.tu-chemnitz.de/vsr/phd/siegert/trustlab_host
[valentin-siegert-website]: https://vsr.informatik.tu-chemnitz.de/people/siegert
[wta-paper]: https://vsr.informatik.tu-chemnitz.de/research/publications/2021/007/
