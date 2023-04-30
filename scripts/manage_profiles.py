# Copiar DockerFile?
# Copiar start.sh que ejecute el Browser

import os
import subprocess
import docker
import coloredlogs, logging


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


def create_profile(name):

    actual_path = os.getcwd()
    profile_dir = os.path.join(actual_path, "profiles", name.lower())
    logger.info(f"Checking profile {name.lower()}...")
    logger.info(f"Checking directory profile {profile_dir}...")


    if not os.path.exists(profile_dir):
        logger.info(f"Creating directory profile {profile_dir}...")
        os.makedirs(profile_dir)
        
        config_path = os.path.join(profile_dir, "config")
        logger.info(f"Creating direcotry config {config_path}...")
        os.makedirs(config_path)

        # Verify if image exist and create it
        logger.info(f"Checking if image {name.lower()} exist...")
        client = docker.from_env()
        try: 
            image = client.images.get(name.lower())
            logger.debug(f"  Image {image} exist...")
        except Exception:
            logger.info(f"Building docker image {name.lower()}...")
            command_build = f"docker build -t {name.lower()} -f {os.path.join(actual_path, 'machines', 'Dockerfile.Ubuntu.Firefox')} ."
            logger.info(f"Executing command... {command_build}")
            proc_build = subprocess.Popen(command_build, 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE, shell=True)
            while True:
                output = proc_build.stdout.readline().decode()
                if not output:
                    break
                print(output.rstrip())

        # Docker run
        # docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --net=host ubuntufirefox
        logger.info(f"Running docker image {name.lower()}...")
        command_run = f"docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --net=host {name.lower()}"
        proc_run = subprocess.Popen(command_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        logger.info(f"Executing command... {command_run}")

        while True:
            output = proc_run.stdout.readline().decode()
            if not output:
                break
            print(output.rstrip())

    else:
        print(f"The profile {name} already exist")
