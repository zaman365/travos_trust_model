
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="https://github.com/ValentinSiegert/aTLAS/raw/master/_logos/atlas_grey.svg" alt="aTLAS orange" height="80">
  </a>
  <h2>TrustLab Host</h2>
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
- [Usage](#-usage)
- [Insights](#-insights)
  - [Connectors](#-connectors)
- [Authors & Contributors](#-authors--contributors)
- [Acknowledgements](#-acknowledgements)

</details>

## 💡 About

<table>
<tr>
<td>

This is the host library of the aTLAS testbed and thus a submodule of the [main repository][trustlab-repo].
It includes the testbed environment, thus the supervisor and the web agents to be simulated.
Further, it serves as a library to the web application and the director with certain [models](models.py).
Additionally, it includes the `evaluator.py` which can be used to execute several scenarios in a sequence based on a CLI command.

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
2. Python pipenv

## ⚡ Getting Started

1. Ensure setup of [aTLAS web application and director][trustlab-repo].

2. If not on same machine as aTLAS, clone submodule.

3. Setup pipenv in submodule root:
    ```bash
    pipenv install
    ```
   >For more information on pipenv, cf. [Pipenv: Python Dev Workflow for Humans][pipenv].

## 👟 Usage

1. Ensure execution of [aTLAS][trustlab-repo].

2. Start supervisor(s), e.g. with a maximum capacity of 10 agents:
    ```bash
    python supervisor.py 10
    ```
   For more specific preferences conduct the help of [supervisor.py](supervisor.py):
   ```bash
    python supervisor.py -h
    ```

<details>
<summary>Evaluator Script</summary>

1. Ensure execution of [aTLAS][trustlab-repo] and of one or more supervisors.
2. Update the [evaluator.py](evaluator.py) with the desired scenarios to execute.
3. Start evaluator
    ```bash
    python evaluator.py
    ```
   For more specific preferences conduct the help of [evaluator.py](evaluator.py):
   ```bash
    python evaluator.py -h
    ```

</details>

## 👀 Insights

Here are insights on the assumptions which are assumed by the code.

### 🔗 Connectors
- The connectors are assumed to be placed in ``connectors`` directory.
- Every connector has its own file, which is named like the class but all lower case and seperated with ``_`` where camel case inserted capital chars.
- A new connector class should be inserted in the choices of the connectors argument in supervisor's argparse.

## ✍ Authors & Contributors

The original setup of this repository is by the first author [Valentin Siegert][valentin-siegert-website].

All authors of this work in alphabetic order:

- [Shovra Das](https://github.com/shovradas)
- [Martin Gaedke](https://vsr.informatik.tu-chemnitz.de/people/gaedke)
- Arved Kirchhoff
- [Mahda Noura](https://vsr.informatik.tu-chemnitz.de/people/mahdanoura)
- [Valentin Siegert][valentin-siegert-website]

## 👍 Acknowledgements

The authors acknowledge the work of the following students:

- Jun Li
- Marten Rogall
- Bastian Rose


<!-- Identifiers, in alphabetical order -->
[atlas-logo-grey]: https://github.com/ValentinSiegert/aTLAS/raw/master/_logos/atlas_grey.svg
[atlas-paper]: https://vsr.informatik.tu-chemnitz.de/research/publications/2020/010/
[atlas-project]: https://vsr.informatik.tu-chemnitz.de/projects/2020/atlas/
[demo-extern]: https://vsr-www.informatik.tu-chemnitz.de/projects/2020/atlas/demo/
[demo-intern]: https://vsr-dem0.informatik.tu-chemnitz.de/trustlab/
[pipenv]: https://pipenv.pypa.io/en/latest/
[trustlab-repo]: https://gitlab.hrz.tu-chemnitz.de/vsr/phd/siegert/trustlab
[valentin-siegert-website]: https://vsr.informatik.tu-chemnitz.de/people/siegert
[wta-paper]: https://vsr.informatik.tu-chemnitz.de/research/publications/2021/007/
