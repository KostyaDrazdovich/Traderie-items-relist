import inspect
import os
from functools import partial, wraps
from timeit import default_timer as timer
from unittest.mock import MagicMock

EXPORT_ENV_VAR = 'QAA_CONF_LOAD_MOCKED'
STEP_ENV_VAR = 'QA_STEP_RUNNING'


def step(func=None, log_input=True, log_output=True):
    if not func:
        return partial(step, log_input=log_input, log_output=log_output)

    @wraps(func)
    def wrapper(*args, **kwargs):
        skip_step_print = False
        args_passed = args

        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        if params and params[0] == 'self':
            args_passed = args[1:]
        args_passed = ', '.join([str(arg) for arg in args_passed])
        kwargs_passed = ', '.join(['{0}={1}'.format(k, v) for k, v in kwargs.items()])
        if args_passed and kwargs_passed:
            args_passed += ', '
        if not log_input:
            args_passed = ''
            kwargs_passed = ''

        func_name = func.__name__.replace('_', ' ')
        func_status = 'PASSED'
        print_result = None
        start_time = timer()

        try:
            if bool(os.getenv(EXPORT_ENV_VAR)):
                step_result = MagicMock()
            else:
                skip_step_print = bool(os.getenv(STEP_ENV_VAR))
                os.environ[STEP_ENV_VAR] = '1'
                step_result = func(*args, **kwargs)
            print_result = ' -> {}'.format(step_result) if (step_result and log_output) else ''
            return step_result

        except Exception as e:
            func_status = 'FAILED'
            print_result = ' -> {}'.format(str(e))
            raise e

        finally:
            if not skip_step_print:
                os.environ[STEP_ENV_VAR] = ''

                end_time = timer()
                execution_time = round(end_time - start_time, 1)
                print(
                    '[{execution_time}s] {func_status} {func_name} '
                    '({args_passed}{kwargs_passed}){print_result}'.format(
                        execution_time=execution_time,
                        func_status=func_status,
                        func_name=func_name,
                        args_passed=args_passed,
                        kwargs_passed=kwargs_passed,
                        print_result=print_result,
                    )
                )

    return wrapper
