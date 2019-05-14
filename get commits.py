import git
import subprocess
import os
import urllib.parse

modules = ["moving_platform", "location_detector", "end_effectors", "gas_detection", "vein_detection", "sound", "rgb_camera",
           "swarm_controller", "power", "manual_control", "display", "voice_interaction", "robot_arm", "distance_sensor",
           "hazard_detection", "microphone", "navigation", "mapping", "swarm_simulation", "communication" , "fire_extinguisher",
           "health_monitor", "load_sensor", "swarm_managment", "swarm_analytics", "thermal_camera", "flame_sensor",
           "gyroscope", "temperature_sensor"]

libraries = ["PWM_library", "USART_library", "internal_communication", "datastructures", "trng_library", "I2C_library"]

others = ["WiringPi", "libusb", "Catch2", "rtos", "hwlib", "r2d2-python-build", "R2D2-build", "R2D2-gists"]

run_path = os.path.dirname(os.path.realpath(__file__))

base_url = "https://github.com/R2D2-2019/"

out_file = None

since_date_specified = True
since_date = None

until_date_specified = True
since_date = None

author_name = ''
author_command_string = ''

def create_list_from_commits(commits):
    commits_per_line = commits.split("\n")
    for commit in range(len(commits_per_line)):
        commits_per_line[commit] = commits_per_line[commit].split(",")
    return commits_per_line

def add_url_to_hash(commit_list,repo_url):
    for commit in range(len(commit_list)):
        commit_list[commit][0] = str(repo_url + "/commit/" + str(commit_list[commit][0]))
    return commit_list

def add_wiki_url_to_hash(repo,commit_list):
    if (len(commit_list) >1):
        for commit in range(len(commit_list)):
            file_name = repo.show(commit_list[commit][0],'--name-only', '--pretty=')
            page_name = file_name[0:-3] #strip .md from file_name
            prev_commit_hash = 0

            if (":" in file_name):
                file_name = file_name.replace(":","\:")
            page_name = urllib.parse.quote(page_name)

            if (len(file_name) is not 0):
                try:
                    commits_for_file = create_list_from_commits(repo.log('--no-merges', '--date=iso', '--pretty=%H,%ad,%s', '--follow' , file_name))
                except:
                    commits_for_file = []
                for i in range(len(commits_for_file)):
                    if commits_for_file[i][0] == commit_list[commit][0]: #found current commit
                        prev_commit_hash = commits_for_file[i-1][0] #get hash from prev commit

            commit_hash = commit_list[commit][0]
            commit_list[commit][0] = str(base_url + "R2D2-2019/wiki/" + page_name + "/_compare/" + str(commit_hash)  + '...' + str(prev_commit_hash))
            commit_list[commit].append(str(base_url + "R2D2-2019/wiki/" + page_name + "/" + str(commit_hash)))

    return commit_list

def print_2d_list(lst):
    for i in range(len(lst)):
        if len(lst[i]) > 1:
            print(lst[i])
        else:
            print("no commits in this repo by " + author_name)
    print()

def write_list_to_csv(commit_list):
    global out_file
    for commit in range(len(commit_list)):
        if (len(commit_list[commit]) <=1):
            out_file.write("no commits in this repo by "+ author_name+ " \n")
            continue
        for item in commit_list[commit]:
            out_file.write(item + ";")
        out_file.write("\n")
    out_file.write("\n")

def write_header_to_csv():
    global out_file
    out_file.write("link to commit; date; commit message \n")

def write_wiki_header_to_csv():
    global out_file
    out_file.write("wiki commits \n")
    out_file.write("compare link; date; commit message; link to commit \n")

def clone_repo(repo_url,repo_name):
    try:
        git.Git("./").clone(repo_url)
    except:
        print()
    return git.Git(run_path + "\\" + repo_name)

def get_commits(repo):
    if (since_date_specified and until_date_specified):
        return repo.log('--no-merges', author_command_string, '--date=iso', '--pretty=%H,%ad,%s', '--all', '--since=' + since_date, '--until=' + until_date )
    elif (until_date_specified):
        return repo.log('--no-merges', author_command_string, '--date=iso', '--pretty=%H,%ad,%s', '--all', '--until=' + until_date)
    elif (since_date_specified):
        return repo.log('--no-merges', author_command_string, '--date=iso', '--pretty=%H,%ad,%s', '--all', '--since=' + since_date)
    return repo.log('--no-merges',author_command_string, '--date=iso', '--pretty=%H,%ad,%s', '--all')

def delete_repo(repo,repo_name):
    del repo
    command = "rmdir /S /Q " '"'+ run_path + "\\" + repo_name + '"'
    subprocess.check_output(command,shell=True)

def get_repo_info(repo_url,repo_name):
    repo = clone_repo(repo_url,repo_name)
    complete_list = add_url_to_hash(create_list_from_commits(get_commits(repo)),repo_url)
    print(repo_name + "\t total commits: " , len(complete_list))
    print_2d_list(complete_list)
    out_file.write(repo_name + ", total commits: " + str(len(complete_list) )+ "\n")
    write_header_to_csv()
    write_list_to_csv(complete_list)
    delete_repo(repo,repo_name)

def get_all_repos():
    get_modules()
    get_libraries()
    get_others()
    get_wiki()

def get_modules():
    print("Modules:")
    for i in range(len(modules)):
        repo_name = modules[i]
        repo_url = base_url + repo_name
        get_repo_info(repo_url,repo_name)

def get_libraries():
    print("libraries:")
    for i in range(len(libraries)):
        repo_name = libraries[i]
        repo_url = base_url + repo_name
        get_repo_info(repo_url,repo_name)

def get_wiki():
    print ("this might take a while:")
    wiki_name = "R2D2-2019.wiki"
    wiki_url = base_url + wiki_name
    repo = clone_repo(wiki_url, wiki_name)

    complete_list = add_wiki_url_to_hash(repo,create_list_from_commits(get_commits(repo)))
    print("wiki: \t total commits:" , len(complete_list) )
    write_wiki_header_to_csv()
    out_file.write("total commits " +  str(len(complete_list)) + "\n")
    print_2d_list(complete_list)
    write_list_to_csv(complete_list)
    delete_repo(repo,wiki_name)

def get_others():
    print("others:")
    for i in range(len(others)):
        repo_name = others[i]
        repo_url = base_url + repo_name
        get_repo_info(repo_url,repo_name)


def UI():
    global author_name
    global author_command_string
    global since_date_specified
    global since_date
    global until_date
    global until_date_specified
    global out_file
    author_name = input("give a author name please: ")
    author_command_string = "--author=" + author_name

    file_name = input("please specify a file name(without extention): ")
    choice = input("get modules,wiki,others,libraries or all or type [one] to get only one repo: ")
    since_date = input("specify the date[MM-DD-YYYY] from wich you want to get commits or type [all]: ")
    until_date =  input("specify the date[MM-DD-YYYY] until you want to get commits or type [all]: ")

    out_file = open(file_name+".csv", "w")
    out_file.write("sep=; \n")
    if (since_date == "all") :
        since_date_specified = False
    elif (len(since_date) != 10) :
        print("invalid date try again ")
        UI()

    if (until_date == "all"):
        until_date_specified = False
    elif (len(until_date) != 10):
        print("invalid date try again ")
        UI()

    if (choice == "modules"):
        get_modules()
    elif (choice == "wiki"):
        get_wiki()
    elif (choice == "libraries"):
        get_libraries()
    elif (choice == "others"):
        get_others()
    elif (choice == "all"):
        get_all_repos()
    elif (choice == "one"):
        repo_name = input("please specify repo_name: ")
        repo_url = base_url + repo_name
        get_repo_info(repo_url,repo_name)
    else:
        print("not a valid option try again")
        UI()
    print()
UI()