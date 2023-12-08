# Project Name

Problem Statement: The World Bank has an API and your task is to find the next China. Retrieve and visualise GDP growth rates of nations like India, Vietnam, Indonesia for as long as you can access the data, and tell us what the projected growth rate will be, taking into account population growth and other economic factors. Compare it to a country like Singapore, South Korea and Malaysia, where they were one slow, but grew, and see if you can predict stagnation.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Task](https://taskfile.dev/installation/): Instructions to install task
- [Poetry](https://python-poetry.org/docs/#installation): Instructions to install poetry
- [Docker Compose](https://docs.docker.com/compose/install/): Instructions to install Docker Compose.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/jagadeeshgarapati/economic-indicator.git
    ```

2. Change into the project directory:

    ```bash
    cd economic-indicator
    ```

3. Install dependencies using Poetry:

    ```bash
    task poetry:install
    ```

## Usage

To render the UI, run the following command:

```bash
task render-ui
