import os
import subprocess
import docker
import coloredlogs, logging
import psutil


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


def create_profile(name, cpu_qty=1, cpu_quota=50, cpu_period=100, 
                   mem=1, swap=2, tz="Etc/Greenwich"):

    # TODO : 
    # - Get actual tz
    # - Validations

    actual_path = os.getcwd()
    profile_dir = os.path.join(actual_path, "profiles", name.lower())
    logger.info(f"Checking profile {name.lower()}...")
    logger.info(f"Checking directory profile {profile_dir}...")

    if not os.path.exists(profile_dir):
        logger.info(f"Creating directory profile {profile_dir}...")
        os.makedirs(profile_dir)
        
    config_path = os.path.join(profile_dir, "config")
    if not os.path.exists(profile_dir):
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
            logger.debug(output.rstrip())

    # Verify if exist shell script run.sh
    sh_file = os.path.join(actual_path, 'profiles', name.lower(), "run.sh")
    logger.info(f"Verifying if run.sh exist... {sh_file}...")

    if not os.path.isfile(sh_file):

        # docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --net=host ubuntufirefox
        logger.warn(f"Creating docker run script to {name.lower()}...")

        # TODO : Verify the browser to map directory or map home directory
        # config_param = f"-v {config_path}:/root/.mozilla"
        config_param = f"-v {config_path}:/root"  # This map the root directory

        # Verify CFS support
        # sched_features = psutil.LinuxScheduler().sched_get_features()
        cpu_param = ""
        # if psutil.LinuxSchedulerFeature.CFS in sched_features:
        #     cpu_param = f"--cpus={cpu_qty} --cpu-quota={cpu_quota} --cpu=period={cpu_period} "
        #     logger.info(f"Using CPU param {name.lower()}...")
        # else:
        #     logger.warn(f"CFS is not enabled. Param CPU not used...")

        command_run = f"docker run -it --rm -e DISPLAY=$DISPLAY " \
                      f"-v /tmp/.X11-unix:/tmp/.X11-unix " \
                      f" {config_param} " \
                      f"{cpu_param} " \
                      f"--memory={mem}g " \
                      f"--memory-swap={swap}g " \
                      f"-e TZ={tz}" \
                      f"--net=host {name.lower()}"

        with open(sh_file, 'w') as shell_script:
            shell_script.write("#!/bin/bash\n")
            shell_script.write(command_run)
            shell_script.close()

    # Docker run
    logger.info(f"Running docker image {name.lower()}...")
    proc_run = subprocess.Popen(["bash " + sh_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    logger.info(f"Executing shell script... {sh_file}")
    # subprocess.run(["bash", sh_file])

    while True:
        output = proc_run.stdout.readline().decode()
        if not output:
            break
        logger.debug(output.rstrip())


def get_profiles():

    actual_path = os.getcwd()
    logger.info(f"Get profiles from {actual_path}...")

    profiles = []
    for profile in os.listdir(os.path.join(actual_path, 'profiles')):
        file = os.path.join(actual_path, 'profiles', profile)
        if os.path.isdir(file):
            profiles.append(profile)

    logger.info(f"Profiles {profiles}...")

    return profiles
    

# def run_profile(name):

#     actual_path = os.getcwd()
#     profile_dir = os.path.join(actual_path, "profiles", name.lower())
#     logger.info(f"Checking profile {name.lower()}...")
#     logger.info(f"Checking directory profile {profile_dir}...")

#     if not os.path.exists(profile_dir):

#         # Verify if image exist and create it
#         logger.info(f"Checking if image {name.lower()} exist...")
#         client = docker.from_env()
#         try: 
#             image = client.images.get(name.lower())
#             logger.debug(f"  Image {image} exist...")
#         except Exception:
#             logger.info(f"Building docker image {name.lower()}...")
#             command_build = f"docker build -t {name.lower()} -f {os.path.join(actual_path, 'machines', 'Dockerfile.Ubuntu.Firefox')} ."
#             logger.info(f"Executing command... {command_build}")
#             proc_build = subprocess.Popen(command_build, 
#                                           stdout=subprocess.PIPE, 
#                                           stderr=subprocess.PIPE, shell=True)
#             while True:
#                 output = proc_build.stdout.readline().decode()
#                 if not output:
#                     break
#                 print(output.rstrip())

#         # Docker run
#         # docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --net=host ubuntufirefox
#         logger.info(f"Running docker image {name.lower()}...")
#         # TODO : Verify the browser to map directory
#         config_param = f"-v {config_path}:/root/.mozilla"
#         command_run = f"docker run -it --rm -e DISPLAY=$DISPLAY " \
#                       f"-v /tmp/.X11-unix:/tmp/.X11-unix " \
#                       f" {config_param} " \
#                       f"--net=host {name.lower()}"
#         proc_run = subprocess.Popen(command_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#         logger.info(f"Executing command... {command_run}")

#         while True:
#             output = proc_run.stdout.readline().decode()
#             if not output:
#                 break
#             print(output.rstrip())

#     else:
#         print(f"The profile {name} already exist")


