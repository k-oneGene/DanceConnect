from decouple import config, UndefinedValueError, RepositoryEnv


# print(f'config("ENV_IS_FOR"): {config("ENV_IS_FOR")}')

# TODO: Workaround for Jenkins. See if I can add .env
try:
    ENV_IS_FOR = config('ENV_IS_FOR')

    if ENV_IS_FOR == 'local':
        print('Local Development setting is used')
        from .local import *
    elif ENV_IS_FOR == 'staging':
        print('Staging Setting is used.')
        # from .staging import *
    elif ENV_IS_FOR == 'production':
        print('Production Setting is used.')
        from .production import *
    else:
        print('No settings is found. Please check if .env exist')
except UndefinedValueError:
    print('CI setting is used')
    # from .ci import *
