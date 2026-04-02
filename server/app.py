from openenv.core.env_server import create_app
from env import SupportEnv
from models import Action, Observation


def create_environment():
    return SupportEnv(task_id="easy")


app = create_app(
    create_environment,
    Action,
    Observation,
    env_name="supportops-openenv"
)