# this script is used to create .env file filled with necessary host data as
# a prerequisite for starting local environment

# map host user and group for Linux users (Docker (for Linux) user and group is not same on host and inside container)
current_user="$(id -u)"
current_group="$(id -g)"

# get project dir name to prefix container names with it
project_root_dir_url="$(cd ../../; pwd)"
project_root_dir_name="${project_root_dir_url##*/}"

# get system info
sysname="$(uname -s)"

# act according to system info
# if local development machine is Mac
case "${sysname}" in
  Darwin*)
    if [ ! -f .env ]; then
      echo "COMPOSE_PROJECT_NAME=${project_root_dir_name}_local" >> .env
      echo "USER_ID=1000" >> .env
      echo "GROUP_ID=1000" >> .env
    fi
    ;;
esac
# if local development machine is Linux
case "${sysname}" in
  Linux*)
    if [ ! -f .env ]; then
      echo "COMPOSE_PROJECT_NAME=${project_root_dir_name}_local" >> .env
      echo "USER_ID=$current_user" >> .env
      echo "GROUP_ID=$current_group" >> .env
    fi
    ;;
esac

# temp copy requirements.txt file (deleted after build in Makefile)
if [ ! -L ./requirements.txt ]; then
  cp ../../requirements.txt ./
fi
