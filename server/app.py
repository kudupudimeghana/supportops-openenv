from openenv.core.env_server import create_app
from env import SupportEnv
from models import Action, Observation
import uvicorn


def create_environment():
    return SupportEnv(task_id="easy")


app = create_app(
    create_environment,
    Action,
    Observation,
    env_name="supportops-openenv"
)


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()