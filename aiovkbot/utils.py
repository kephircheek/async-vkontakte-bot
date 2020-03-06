import os
import json
import logging


PRODUCTION_VARS = ['TOKEN', 'CONFIRMATION_CODE', 'SECRET_KEY']
DEVELOPMENT_VARS = ['BOT_HOST', 'BOT_PORT', 'VK_HOST', 'VK_PORT']

def setup_enviroment(debug=True):
    """Create or load json file with basic config
    and export variables to enviroment"""

    if not all(map(os.getenv, PRODUCTION_VARS + (DEVELOPMENT if debug else [])):
        if not os.path.exists('.localenv.json'):
            print('Set enviroment variables:')
            localenv = {var: input(f"{var} = ") for var in PRODUCTION_VARS}

            if debug:
                print('Developer variables:')
                optional = {var: input(f"(optioanl) {var} = ") for var in DEVELOPMENT_VARS}
                localenv.update(optional)

            with open('.localenv.json', 'w') as f:
                json.dump(localenv, f, indent=2)

        else:
            with open('.localenv.json') as f:
                localenv = json.load(f)

        for var, value in localenv.items():
            os.environ[var] = value

    eviroment = {var: os.getenv(var) for var in PRODUCTION_VARS + DEVELOPMENT_VARS}
    logging.debug('Enviroment variables: {enviroment}')


